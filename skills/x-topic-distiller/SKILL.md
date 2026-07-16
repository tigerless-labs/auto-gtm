---
name: x-topic-distiller
description: >
  Distill X/Twitter post topics from a window of recent AI coding-agent conversation (Claude Code or Codex), combined with current hotspots.
  **Manually triggered** — use when the user says things like "help me come up with X topics from our recent chat /
  distill a tweet idea / pull one X-worthy takeaway from this conversation".
  Only does "conversation → topic" distillation; does not write the body/title or publish.
---

# x-topic-distiller — distill X topics from a conversation session

Turn a window of recent AI conversation, together with current hotspots, into topics worth posting on X. Topics come in two kinds: **share-type** (share a tool/person/product that surfaced in the conversation, @-mention its author) and **reflection-type** (an original reflection/insight; @-mention a relevant account when one exists).

## When to trigger

**Manual only.** Run only when the user explicitly asks to "distill X topics from the recent conversation / think up a tweet / pull a takeaway to post on X". Never automatic, never in the background.

## Two independent sources

Hotspots and the session are **independent sources**. A topic can come from: hotspot only / session only / the overlap of both (overlap is strongest). Don't assume any ordering between them — weigh them together at the end.

## Flow

### 1. Fetch hotspots (soft-enhance)

Call an external tool for recent trends, one of:
- `last30days` (if installed as a skill) — recent-opinion aggregation, best fit.
- `agent-reach` (if installed) — multi-platform retrieval.

**Soft-enhance:** if neither is installed, **skip this step and continue as normal**, and at the end **prompt the user**: "Install last30days or agent-reach to ground topics in current hotspots." Don't withhold topics just because there are no hotspots.

### 2. Read the conversation (via script, filtering out tool results)

Use the script matching the **host agent you are running in** — **its key value is stripping out tool results**, keeping only human-AI conversation text, to save tokens (reading context directly can't save this: tool results are already occupying tokens there).

**In Claude Code** (`${CLAUDE_SKILL_DIR}` is set by Claude Code):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/read_session.py"            # default: last 24h
python3 "${CLAUDE_SKILL_DIR}/scripts/read_session.py" --hours 72 # when the user wants another range
```

Reads `~/.claude/projects/<cwd-mapping>/*.jsonl` (per-project directories).

**In Codex** (no env var — run the script via its path relative to this SKILL.md's directory, which you know from having read this file):

```bash
python3 <skill-dir>/scripts/read_codex_session.py                # default: last 24h, current project only
python3 <skill-dir>/scripts/read_codex_session.py --hours 72     # another range
python3 <skill-dir>/scripts/read_codex_session.py --all-projects # across all projects
```

Reads `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` (global, date-partitioned; the script filters to the current project by each file's `session_meta.payload.cwd`).

> ⚠️ Both agents' JSONL formats are internal and may change between versions. If a script's output is clearly wrong (errors / missing fields / tool results leaking in), **just edit that script to fit the new format** — each is short and documents its parsing strategy in the header: Claude Code = take `text` of user/assistant messages by `role`, skip `tool_use`/`tool_result` blocks; Codex = prefer `event_msg` lines of type `user_message`/`agent_message`, fall back to `response_item` messages minus injected context. Filter by `timestamp` within the window, then rerun.

### 3. Distill (merge the three sources)

Distill from hotspots + session:
- **Entity extraction:** tools/products/people mentioned in the conversation → candidate @-targets.
- **Insight/reflection extraction:** one takeaway that stands on its own, or one reflection worth sharing.
- Weigh all three source combinations (hotspot only / session only / overlap).

### 4. Value gate

**Not every conversation yields a postable topic.** If there's no real substance, **say plainly "this conversation has no topic worth posting" and stop** — don't force one.

### 5. Generate X topics + @

For each topic:
- **Share-type** → @ the in-session entity: first look up [`references/x_handle_map.md`](references/x_handle_map.md) for the handle; if not found, use `agent-reach` to search X as a fallback; if still not found, skip the @.
- **Reflection-type** → **after the topic is set**, use `agent-reach` to search X for same-theme accounts/posts to @; if `agent-reach` isn't installed, **prompt the user to install it** and give the topic without an @.

## Output

Output format is not enforced. By default, give per topic: **a one-line topic angle + kind (share/reflection) + suggested @ account (or mark "to-search / none") + why it's worth posting (1 line)**. Follow the user's format if they ask for another.

## Boundary

Only produces **topics**. Does not write the body, the title, formatting, or publish — those go to other tools/people.
