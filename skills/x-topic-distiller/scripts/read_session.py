#!/usr/bin/env python3
"""
read_session.py — read recent Claude Code conversation text (skipping tool results).

Design:
- Read only human-AI conversation text, **not tool results** (to save tokens).
- Default last 24h; override with --hours.
- Claude Code only (reads ~/.claude/projects/<cwd-hash>/*.jsonl).

⚠️ IMPORTANT: Claude Code's JSONL transcript format is **internal and may change between
versions**; it is not a stable public contract. This script is a **defensive best-effort**
parser: it degrades gracefully on missing fields / structural changes rather than crashing.
If the output is clearly wrong, edit this script to fit the new format (see SKILL.md).
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime, timedelta, timezone


def project_dir_for_cwd(cwd: str) -> str:
    """Map cwd to its projects subdir name per Claude Code's rule: non-alphanumeric -> '-'."""
    return re.sub(r"[^a-zA-Z0-9]", "-", cwd)


def parse_ts(obj: dict):
    """Best-effort ISO timestamp from a line; None if unavailable."""
    ts = obj.get("timestamp") or obj.get("time") or obj.get("createdAt")
    if not ts or not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_text(msg: dict):
    """Extract plain text from a message; skip tool_use / tool_result / thinking.
    Returns (role, text), or None if the line is not usable conversation text."""
    if not isinstance(msg, dict):
        return None
    role = msg.get("role")
    if role not in ("user", "assistant"):
        return None
    content = msg.get("content")

    if isinstance(content, str):
        text = content.strip()
        return (role, text) if text else None

    if isinstance(content, list):
        parts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            # Keep only plain text blocks; skip tool_use / tool_result / thinking
            if btype == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"].strip())
        text = "\n".join(p for p in parts if p).strip()
        return (role, text) if text else None

    return None


def read_file(path: str, cutoff: datetime, fallback_ok: bool):
    """Read one jsonl file, yielding a list of (ts, role, text) filtered by cutoff."""
    out = []
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
    except OSError:
        return out
    # If the whole file is older than cutoff and no per-line timestamps are available, skip
    file_recent = mtime >= cutoff
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Skip sub-agent sidechain transcripts (noise, not the main conversation)
                if obj.get("isSidechain") is True:
                    continue
                msg = obj.get("message") if isinstance(obj.get("message"), dict) else obj
                res = extract_text(msg)
                if not res:
                    continue
                ts = parse_ts(obj)
                if ts is not None:
                    if ts < cutoff:
                        continue
                else:
                    # No per-line timestamp: fall back to file mtime
                    if not (file_recent and fallback_ok):
                        continue
                out.append((ts, res[0], res[1]))
    except OSError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser(description="Read recent Claude Code conversation text (skipping tool results)")
    ap.add_argument("--hours", type=float, default=24, help="How many hours to look back (default 24)")
    ap.add_argument("--cwd", default=os.getcwd(), help="Target project working directory (default: current)")
    ap.add_argument("--projects-root", default=os.path.expanduser("~/.claude/projects"),
                    help="Claude Code projects root directory")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)

    proj_dir = os.path.join(args.projects_root, project_dir_for_cwd(os.path.abspath(args.cwd)))
    if not os.path.isdir(proj_dir):
        print(f"[read_session] no session directory for this project: {proj_dir}\n"
              f"(this project has no Claude Code conversation yet, or the path-mapping rule changed)",
              file=sys.stderr)
        sys.exit(2)

    files = [os.path.join(proj_dir, f) for f in os.listdir(proj_dir) if f.endswith(".jsonl")]
    if not files:
        print(f"[read_session] no .jsonl transcripts under {proj_dir}", file=sys.stderr)
        sys.exit(2)

    rows = []
    for path in files:
        rows.extend(read_file(path, cutoff, fallback_ok=True))

    # Timestamped rows first, sorted by time; rows without timestamps (kept via mtime) last
    rows.sort(key=lambda r: (r[0] is None, r[0] or now))

    if not rows:
        print(f"[read_session] no usable conversation text in the last {args.hours}h", file=sys.stderr)
        sys.exit(2)

    for ts, role, text in rows:
        stamp = ts.astimezone().strftime("%Y-%m-%d %H:%M") if ts else "??"
        print(f"\n[{stamp} {role}]\n{text}")


if __name__ == "__main__":
    main()
