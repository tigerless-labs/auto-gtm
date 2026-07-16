---
name: x-topic-distiller
description: >
  Distill X/Twitter post topics from a window of recent AI coding-agent conversation (Claude Code or Codex), combined with current hotspots.
  **Manually triggered** — use when the user says things like "help me come up with X topics from our recent chat /
  distill a tweet idea / pull one X-worthy takeaway from this conversation".
  Only does "conversation → topic" distillation; does not write the body/title or publish.
---

# x-topic-distiller — distill X topics from a conversation session

Turn a window of recent AI conversation, together with current hotspots, into topics worth posting on X. Topics come in two kinds: **share-type** (share a tool/person/product that surfaced in the conversation) and **reflection-type** (an original reflection/insight). Resolving the @ account, learning the tone, and drafting the post all belong to the downstream `x-content-generator` skill.

## Stance: sincere altruism

Every topic must be posted **for the reader's benefit** — sharing high-signal cognition with genuine felt reflection, never self-promotion or engagement bait. The test for every candidate topic: **what does the reader walk away with?** It must be at least one of:

1. **A resource/tool** they can use (with attribution to its author);
2. **A framework** — a takeaway packaged as a portable structure ("2 types of…", "3 tiers of…");
3. **A reframe** — a counterintuitive one-line restatement of something familiar ("Learning ≠ Education");
4. **A lived observation elevated to insight** — a first-hand scene that leads to a broader conclusion ("A student told me X → which means Y about the industry").

If a candidate gives the reader none of the four, it fails the value gate below.

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

**Before reading, ask the user to choose the scope** (e.g. via AskUserQuestion): **current project only** or **all projects**? Don't assume — the user decides per run. If they already stated the scope in their request (e.g. "from all my recent conversations"), skip the question and use what they said.

Use the script matching the **host agent you are running in** — **its key value is stripping out tool results**, keeping only human-AI conversation text, to save tokens (reading context directly can't save this: tool results are already occupying tokens there).

**In Claude Code** (`${CLAUDE_SKILL_DIR}` is set by Claude Code):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/read_session.py"                 # default: last 24h, current project only
python3 "${CLAUDE_SKILL_DIR}/scripts/read_session.py" --hours 72      # when the user wants another range
python3 "${CLAUDE_SKILL_DIR}/scripts/read_session.py" --all-projects  # sessions from ALL projects (each message labeled @project)
```

Reads `~/.claude/projects/<cwd-mapping>/*.jsonl` (per-project directories) by default; `--all-projects` scans every project directory under `~/.claude/projects/` instead. Use it when the user wants topics from all their recent conversations, not just this repo's.

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

**Not every conversation yields a postable topic.** Apply the reader-takeaway test from the Stance section: each candidate must give the reader a resource, a framework, a reframe, or a lived observation elevated to insight. If no candidate passes, **say plainly "this conversation has no topic worth posting" and stop** — don't force one.

### 5. Generate X topics

For each topic, label the kind:
- **Share-type** → attach the in-session entity (tool/person/product, raw name) as the candidate @ target — don't resolve the handle here. The strongest share-type angle is **tool + cognition claim** — not "I used X" but "X reveals something most people haven't realized yet".
- **Reflection-type** → no @ target yet; searching one is downstream work. The strongest reflection-type angle is **first-hand scene → broader insight** — anchor the reflection in something that actually happened in the session, then elevate.

## Output

Output format is not enforced. By default, give per topic: **a one-line topic angle + kind (share/reflection) + candidate entity to @ (share-type only, unresolved) + the reader takeaway (which of the four: resource / framework / reframe / observation→insight) + why it's worth posting (1 line)**. Follow the user's format if they ask for another.

## Boundary

Only produces **topics**. Once the user confirms one, resolving the @, learning the tone, and drafting the post go to the **`x-content-generator`** skill; publishing goes to other tools/people.
