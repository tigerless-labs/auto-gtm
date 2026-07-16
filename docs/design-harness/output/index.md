# output — assembled artifacts (form set by target)

X topic-distillation skill design (system-design form):

- [system.md](0-system.md) — skeleton: flowchart (human/agent swimlanes) + architecture diagram (modules)
- [file-structure.md](file-structure.md) — design landed on disk: file tree + module→file mapping
- modules/ — one file per module
  - [session-reader](modules/session-reader.md) — reads the 24h Claude Code session
  - [distiller](modules/distiller.md) — entity extraction + insight/reflection extraction
  - [hotspot-fetcher](modules/hotspot-fetcher.md) — calls external tools to fetch trending
  - [topic-generator](modules/topic-generator.md) — generates the two X topic types + value gate

Current design points: hotspot and session are **parallel and independent** dual sources (a topic can come from hotspot only / session only / overlap); the session **does not read tool results** (saving tokens); the hotspot is **soft-enhance**; the @ ordering splits by content type (share-type in-session, reflection-type searches X after the topic is set).
