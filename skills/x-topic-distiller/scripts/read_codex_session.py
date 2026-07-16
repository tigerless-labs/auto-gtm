#!/usr/bin/env python3
"""
read_codex_session.py — 读取最近一段时间的 Codex CLI 对话文字（跳过 tool 结果）。

设计原则：
- 只读人-AI 对话文字，**不读 tool 结果 / reasoning**（省 token）。
- 默认最近 24h，--hours 可覆盖。
- 仅适配 Codex CLI（读 ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl）。
- Codex 的 session 是全局按日期存的，不按项目分目录；本脚本用每个文件
  首行 session_meta.payload.cwd 过滤出当前项目的会话（--all-projects 可关掉过滤）。

rollout 行格式（v0.13x–0.14x 实测）：
  {"timestamp": ISO8601, "type": <RolloutItem 类型>, "payload": {...}}
提取策略（优先级从高到低）：
1. event_msg/user_message、event_msg/agent_message —— 干净的用户/助手文字
   （response_item/message/user 里混有 AGENTS.md、environment_context 等注入，噪声大）。
2. 某文件里一条 event_msg 都没有时，降级用 response_item/message（role=user/assistant），
   跳过 developer role 和以 "<"、"# AGENTS.md" 开头的注入文本。

⚠️ 重要：Codex 的 rollout 格式是**内部的、版本间可能变化**，官方不保证稳定。
本脚本是**防御式 best-effort** 解析：字段缺失/结构变化时尽量降级、不崩。
若某次输出明显不对，直接改本脚本适配新格式后重跑。
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta, timezone


def parse_ts(s):
    if not s or not isinstance(s, str):
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def sessions_root_default():
    codex_home = os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex")
    return os.path.join(codex_home, "sessions")


def iter_rollout_files(root: str, cutoff: datetime):
    """遍历 sessions/YYYY/MM/DD/*.jsonl，按日期目录剪枝（早于 cutoff 前一天的整天跳过）。"""
    cutoff_day = (cutoff - timedelta(days=1)).date()
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        parts = rel.split(os.sep)
        # 在 YYYY/MM/DD 层做剪枝；解析不了的目录名不剪（防御式）
        if len(parts) == 3:
            try:
                day = datetime(int(parts[0]), int(parts[1]), int(parts[2])).date()
                if day < cutoff_day:
                    continue
            except ValueError:
                pass
        for fn in filenames:
            if fn.endswith(".jsonl"):
                yield os.path.join(dirpath, fn)


def looks_injected(text: str) -> bool:
    """response_item 用户消息里被 Codex 注入的上下文（AGENTS.md、环境、权限说明等）。"""
    t = text.lstrip()
    return t.startswith("<") or t.startswith("# AGENTS.md")


def extract_response_item_text(payload: dict):
    """降级路径：从 response_item/message 里抽文字。返回 (role, text) 或 None。"""
    if payload.get("type") != "message":
        return None
    role = payload.get("role")
    if role not in ("user", "assistant"):
        return None
    content = payload.get("content")
    parts = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                if block.get("type") in ("input_text", "output_text", "text"):
                    parts.append(block["text"].strip())
    elif isinstance(content, str):
        parts.append(content.strip())
    text = "\n".join(p for p in parts if p).strip()
    if not text:
        return None
    if role == "user" and looks_injected(text):
        return None
    return (role, text)


def read_file(path: str, cutoff: datetime, want_cwd):
    """读一个 rollout 文件，返回 (ts, role, text) 列表；不属于目标项目时返回 []。"""
    events = []      # event_msg 提取的（首选）
    fallback = []    # response_item 提取的（备用）
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get("type")
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}

                if t == "session_meta":
                    # 用 cwd 过滤项目；取不到 cwd 时不过滤（防御式）
                    cwd = payload.get("cwd")
                    if want_cwd and isinstance(cwd, str) and os.path.abspath(cwd) != want_cwd:
                        return []
                    continue

                ts = parse_ts(obj.get("timestamp"))
                if ts is not None and ts < cutoff:
                    continue

                if t == "event_msg":
                    et = payload.get("type")
                    msg = payload.get("message")
                    if et == "user_message" and isinstance(msg, str) and msg.strip():
                        events.append((ts, "user", msg.strip()))
                    elif et == "agent_message" and isinstance(msg, str) and msg.strip():
                        events.append((ts, "assistant", msg.strip()))
                elif t == "response_item":
                    res = extract_response_item_text(payload)
                    if res:
                        fallback.append((ts, res[0], res[1]))
    except OSError:
        return []
    return events if events else fallback


def main():
    ap = argparse.ArgumentParser(description="读取最近的 Codex CLI 对话文字（跳过 tool 结果）")
    ap.add_argument("--hours", type=float, default=24, help="回看多少小时（默认 24）")
    ap.add_argument("--cwd", default=os.getcwd(), help="目标项目工作目录（默认当前）")
    ap.add_argument("--all-projects", action="store_true",
                    help="不按 cwd 过滤，读所有项目的会话")
    ap.add_argument("--sessions-root", default=sessions_root_default(),
                    help="Codex sessions 根目录（默认 $CODEX_HOME/sessions 或 ~/.codex/sessions）")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)
    want_cwd = None if args.all_projects else os.path.abspath(args.cwd)

    if not os.path.isdir(args.sessions_root):
        print(f"[read_codex_session] 找不到 Codex sessions 目录：{args.sessions_root}\n"
              f"（本机没装 Codex CLI，或 CODEX_HOME 指向了别处）", file=sys.stderr)
        sys.exit(2)

    rows = []
    for path in iter_rollout_files(args.sessions_root, cutoff):
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
        except OSError:
            continue
        if mtime < cutoff:  # 整个文件最后写入都早于窗口，跳过
            continue
        rows.extend(read_file(path, cutoff, want_cwd))

    # 去重（resume/fork 可能把同一段历史重写进新文件）
    seen = set()
    deduped = []
    for ts, role, text in rows:
        key = (role, text)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((ts, role, text))

    deduped.sort(key=lambda r: (r[0] is None, r[0] or now))

    if not deduped:
        where = "所有项目" if args.all_projects else f"项目 {want_cwd}"
        print(f"[read_codex_session] 最近 {args.hours}h 内 {where} 没有可用的对话文字\n"
              f"（若该项目确实用过 Codex，可能是 rollout 格式变了——按脚本头部注释改脚本适配）",
              file=sys.stderr)
        sys.exit(2)

    for ts, role, text in deduped:
        stamp = ts.astimezone().strftime("%Y-%m-%d %H:%M") if ts else "??"
        print(f"\n[{stamp} {role}]\n{text}")


if __name__ == "__main__":
    main()
