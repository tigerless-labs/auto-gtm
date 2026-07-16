# file-structure — the design landed on disk

The skill's own file structure (following [content-collector's SKILL.md orchestration + script execution](../sources/skills/content-collector-skill.md)):

```
x-topic-distiller/
├── SKILL.md                     orchestration + manual trigger; extraction/generation go through prompt; hotspot and reflection-type @ search written as "call external tools" instructions
├── scripts/
│   └── read_session.py          reads Claude Code JSONL, default 24h, reads only conversation text, not tool results (the only local deterministic script)
└── references/
    └── x_handle_map.md          share-type in-session entities → X handle static table (high-frequency entities use the table, long-tail falls back to agent-reach)
```

**Only `read_session.py` is a script** — it is a local data transformation (parsing/filtering JSONL). Hotspot data-fetching and reflection-type @ search are both **calling external tools** (last30days / agent-reach); they are delegation and just need to be written into SKILL.md instructions, not turned into scripts.

Judgment steps (extraction, topic generation) build no script; they are written in the SKILL.md prompt and executed by the Agent.

## Module → file

- [hotspot-fetcher](modules/hotspot-fetcher.md) → SKILL.md instruction: call last30days / agent-reach
- [session-reader](modules/session-reader.md) → `scripts/read_session.py`
- [distiller](modules/distiller.md) → the merge+extraction prompt inside SKILL.md
- [topic-generator](modules/topic-generator.md) → the generation prompt inside SKILL.md + `references/x_handle_map.md` (share-type @) + SKILL.md instruction to call agent-reach (reflection-type @ search)

SKILL.md's trigger mode: **human manual trigger**, see [trigger-timing idea](../ideas/trigger-manual.md).
