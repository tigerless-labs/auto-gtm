#!/usr/bin/env python3
"""
read_session.py — read recent Claude Code conversation text (skipping tool results).

Design:
- Read only human-AI conversation text, **not tool results** (to save tokens).
- Default last 24h; override with --hours.
- Claude Code only (reads ~/.claude/projects/<cwd-hash>/*.jsonl).
- A repo's worktree/subdirectory sessions live in sibling dirs ("<cwd-hash>-…");
  they are included by default (rows labeled @<worktree>), --exact-cwd opts out.

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


_RAW_JSONL_RE = re.compile(r'^\{"(?:parentUuid|uuid|sessionId|message|type|snapshot)"')


def scrub_embedded_jsonl(text: str) -> str:
    """Compaction digests can embed raw transcript JSONL inside message text under an
    '# Episode window' section. Truncate at that marker, and drop any stray raw
    transcript-record lines — they are tool-result-grade noise, not conversation."""
    kept = []
    for ln in text.splitlines():
        stripped = ln.strip()
        if stripped.startswith("# Episode window"):
            break
        if _RAW_JSONL_RE.match(stripped):
            continue
        kept.append(ln)
    return "\n".join(kept).strip()


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
        text = scrub_embedded_jsonl(content)
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
        text = scrub_embedded_jsonl("\n".join(p for p in parts if p))
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
    ap.add_argument("--all-projects", action="store_true",
                    help="Read sessions from ALL Claude Code projects, not just the one for --cwd")
    ap.add_argument("--exact-cwd", action="store_true",
                    help="Only the exact cwd's session dir; skip worktree/subdirectory sessions")
    ap.add_argument("--projects-root", default=os.path.expanduser("~/.claude/projects"),
                    help="Claude Code projects root directory")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)

    if args.all_projects:
        if not os.path.isdir(args.projects_root):
            print(f"[read_session] projects root not found: {args.projects_root}", file=sys.stderr)
            sys.exit(2)
        proj_dirs = sorted(
            os.path.join(args.projects_root, d)
            for d in os.listdir(args.projects_root)
            if os.path.isdir(os.path.join(args.projects_root, d))
        )
    else:
        mapped = project_dir_for_cwd(os.path.abspath(args.cwd))
        proj_dir = os.path.join(args.projects_root, mapped)
        proj_dirs = [proj_dir] if os.path.isdir(proj_dir) else []
        if not args.exact_cwd:
            # Sessions run inside the project's worktrees / subdirectories land in sibling
            # dirs whose mangled name extends the project's ("<mapped>-…", e.g.
            # "<mapped>--claude-worktrees-<branch>"). They are this repo's sessions too.
            try:
                proj_dirs += sorted(
                    os.path.join(args.projects_root, d)
                    for d in os.listdir(args.projects_root)
                    if d.startswith(mapped + "-") and os.path.isdir(os.path.join(args.projects_root, d))
                )
            except OSError:
                pass
        if not proj_dirs:
            print(f"[read_session] no session directory for this project: {proj_dir}\n"
                  f"(this project has no Claude Code conversation yet, or the path-mapping rule changed)",
                  file=sys.stderr)
            sys.exit(2)

    rows = []
    seen_files = 0
    for proj_dir in proj_dirs:
        # Label rows for attribution: all-projects mode uses the project's mangled dir name;
        # single-project mode labels worktree/subdirectory sessions with their suffix.
        base = os.path.basename(proj_dir)
        if args.all_projects:
            label = base.lstrip("-")
        elif base != mapped:
            suffix = base[len(mapped):].lstrip("-")
            for prefix in ("claude-worktrees-", "worktrees-"):
                if suffix.startswith(prefix):
                    suffix = suffix[len(prefix):]
                    break
            label = suffix
        else:
            label = ""
        try:
            names = os.listdir(proj_dir)
        except OSError:
            continue
        for name in names:
            if not name.endswith(".jsonl"):
                continue
            seen_files += 1
            for ts, role, text in read_file(os.path.join(proj_dir, name), cutoff, fallback_ok=True):
                rows.append((ts, role, text, label))

    if seen_files == 0:
        where = args.projects_root if args.all_projects else proj_dirs[0]
        print(f"[read_session] no .jsonl transcripts under {where}", file=sys.stderr)
        sys.exit(2)

    # Timestamped rows first, sorted by time; rows without timestamps (kept via mtime) last
    rows.sort(key=lambda r: (r[0] is None, r[0] or now))

    if not rows:
        print(f"[read_session] no usable conversation text in the last {args.hours}h", file=sys.stderr)
        sys.exit(2)

    for ts, role, text, label in rows:
        stamp = ts.astimezone().strftime("%Y-%m-%d %H:%M") if ts else "??"
        head = f"[{stamp} {role} @{label}]" if label else f"[{stamp} {role}]"
        print(f"\n{head}\n{text}")


if __name__ == "__main__":
    main()
