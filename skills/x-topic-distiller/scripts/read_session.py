#!/usr/bin/env python3
"""
read_session.py — 读取最近一段时间的 Claude Code 对话文字（跳过 tool 结果）。

设计原则：
- 只读人-AI 对话文字，**不读 tool 结果**（省 token）。
- 默认最近 24h，--hours 可覆盖。
- 仅适配 Claude Code（读 ~/.claude/projects/<cwd-hash>/*.jsonl）。

⚠️ 重要：Claude Code 的 JSONL 记录格式是**内部的、版本间可能变化**，官方不保证稳定。
本脚本是**防御式 best-effort** 解析：字段缺失/结构变化时尽量降级、不崩。
若某次输出明显不对，改用 `/export` 导出后手动喂给 skill。
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime, timedelta, timezone


def project_dir_for_cwd(cwd: str) -> str:
    """按 Claude Code 规则把 cwd 映射到 projects 子目录名：非字母数字 → '-'。"""
    return re.sub(r"[^a-zA-Z0-9]", "-", cwd)


def parse_ts(obj: dict):
    """尽量从一行里取 ISO 时间戳；取不到返回 None。"""
    ts = obj.get("timestamp") or obj.get("time") or obj.get("createdAt")
    if not ts or not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_text(msg: dict):
    """从一条 message 里抽纯文本；跳过 tool_use / tool_result / thinking。
    返回 (role, text) 或 None（该行不是可用的对话文字）。"""
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
            # 只保留纯文本块；tool_use / tool_result / thinking 一律跳过
            if btype == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"].strip())
        text = "\n".join(p for p in parts if p).strip()
        return (role, text) if text else None

    return None


def read_file(path: str, cutoff: datetime, fallback_ok: bool):
    """读一个 jsonl 文件，产出 (ts, role, text) 列表（已按 cutoff 过滤）。"""
    out = []
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
    except OSError:
        return out
    # 整个文件都比 cutoff 老，且没有逐行时间戳可依赖时，直接跳过
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
                # 跳过子 agent 的 sidechain 转录（噪声，非主对话）
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
                    # 没有逐行时间戳：退回文件 mtime 判断
                    if not (file_recent and fallback_ok):
                        continue
                out.append((ts, res[0], res[1]))
    except OSError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser(description="读取最近的 Claude Code 对话文字（跳过 tool 结果）")
    ap.add_argument("--hours", type=float, default=24, help="回看多少小时（默认 24）")
    ap.add_argument("--cwd", default=os.getcwd(), help="目标项目工作目录（默认当前）")
    ap.add_argument("--projects-root", default=os.path.expanduser("~/.claude/projects"),
                    help="Claude Code projects 根目录")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)

    proj_dir = os.path.join(args.projects_root, project_dir_for_cwd(os.path.abspath(args.cwd)))
    if not os.path.isdir(proj_dir):
        print(f"[read_session] 找不到该项目的 session 目录：{proj_dir}\n"
              f"（该项目在 Claude Code 里还没有对话记录，或路径映射规则已变）", file=sys.stderr)
        sys.exit(2)

    files = [os.path.join(proj_dir, f) for f in os.listdir(proj_dir) if f.endswith(".jsonl")]
    if not files:
        print(f"[read_session] {proj_dir} 下没有 .jsonl 记录", file=sys.stderr)
        sys.exit(2)

    rows = []
    for path in files:
        rows.extend(read_file(path, cutoff, fallback_ok=True))

    # 有时间戳的在前、按时间排序；无时间戳的（靠 mtime 收进来的）排最后
    rows.sort(key=lambda r: (r[0] is None, r[0] or now))

    if not rows:
        print(f"[read_session] 最近 {args.hours}h 内没有可用的对话文字", file=sys.stderr)
        sys.exit(2)

    for ts, role, text in rows:
        stamp = ts.astimezone().strftime("%Y-%m-%d %H:%M") if ts else "??"
        print(f"\n[{stamp} {role}]\n{text}")


if __name__ == "__main__":
    main()
