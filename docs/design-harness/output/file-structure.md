# file-structure — the design landed on disk

Two skills (each following [content-collector's SKILL.md orchestration + script execution](../sources/skills/content-collector-skill.md)):

```
x-topic-distiller/
├── SKILL.md                     orchestration + manual trigger; extraction/generation go through prompt; hotspot fetch written as "call external tools" instruction
└── scripts/
    ├── read_session.py          reads Claude Code JSONL, default 24h, conversation text only, no tool results
    └── read_codex_session.py    same for Codex rollout JSONL (global date-partitioned, filtered by session cwd)

x-content-generator/
├── SKILL.md                     orchestration + manual trigger; voice rules inlined; @ search written as agent-reach instruction; drafting goes through prompt
└── references/
    └── tone-examples.md         verbatim @zarazhangrui exemplars (few-shot voice anchor), maintained ~quarterly
```

**Only the session readers are scripts** — local data transformation (parsing/filtering JSONL). Hotspot fetch and the @ search are **calling external tools** (last30days / agent-reach); they are delegation and just need to be written into SKILL.md instructions, not turned into scripts. Voice is **not** a tool call — it is the static `tone-examples.md` file plus inlined rules.

Judgment steps (extraction, topic generation, drafting) build no script; they are written in SKILL.md prompts and executed by the Agent.

## Module → file

Skill 1 — x-topic-distiller:
- [hotspot-fetcher](modules/hotspot-fetcher.md) → SKILL.md instruction: call last30days / agent-reach
- [session-reader](modules/session-reader.md) → `scripts/read_session.py` / `scripts/read_codex_session.py`
- [distiller](modules/distiller.md) → the merge+extraction prompt inside SKILL.md
- [topic-generator](modules/topic-generator.md) → the generation prompt inside SKILL.md (kinds labeled, @ left unresolved)

Skill 2 — x-content-generator:
- [at-finder](modules/at-finder.md) → SKILL.md instruction: handle from the source URL, else call agent-reach to search X
- [tone-learner](modules/tone-learner.md) → `references/tone-examples.md` + the voice rules inlined in SKILL.md (no tool call)
- [content-writer](modules/content-writer.md) → the drafting prompt inside SKILL.md

Both SKILL.md trigger modes: **human manual trigger**, see [trigger-timing idea](../ideas/trigger-manual.md).
