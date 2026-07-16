# session-reader — the script reads the CC conversation and filters out tool results

Responsibilities:
- Use `scripts/read_session.py` to read recent conversations (default 24h, overridable)
- **Key: strip out tool results**, keep only the human-AI conversation text (saving tokens) — this is exactly the reason for using a script rather than letting the agent read the context directly
- Only supports **Claude Code** (reads JSONL)

Boundary:
- Deterministic operations → go through a **script**
- CC's JSONL format is officially declared unstable → when it changes, **let the AI modify the script itself** to adapt (best-effort, not abandoning the script)
- **Parallel and independent** from hotspot-fetcher, no before/after dependency ([topic-source-independence](../../ideas/topic-source-independence.md))

Basis: [read-range idea](../../ideas/session-read-range-timewindow.md), [Distill's Smart History Processing](../../sources/skills/distill.md)
