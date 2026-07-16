# output — assembled artifacts (form set by target)

X posting pipeline, **two skills** joined by one human-confirmed topic (system-design form):

- [system.md](0-system.md) — skeleton: per-skill flowcharts (human/agent swimlanes) + architecture diagrams (modules)
- [file-structure.md](file-structure.md) — design landed on disk: file trees + module→file mapping
- modules/ — one file per module
  - **skill 1: x-topic-distiller** (conversation → topics)
    - [session-reader](modules/session-reader.md) — reads the 24h session (Claude Code or Codex)
    - [distiller](modules/distiller.md) — entity extraction + insight/reflection extraction
    - [hotspot-fetcher](modules/hotspot-fetcher.md) — calls external tools to fetch trending
    - [topic-generator](modules/topic-generator.md) — generates the two X topic kinds + value gate (@ stays unresolved)
  - **skill 2: x-content-generator** (confirmed topic → content)
    - [at-finder](modules/at-finder.md) — resolves the @: share-type via `x_handle_map`→agent-reach, reflection-type via X search
    - [tone-learner](modules/tone-learner.md) — learns the tone from hot posts + comments on the confirmed theme
    - [content-writer](modules/content-writer.md) — drafts 1-2 posts from topic + @ + tone notes

Current design points: hotspot and session are **parallel and independent** dual sources (a topic can come from hotspot only / session only / overlap); the session **does not read tool results** (saving tokens); the hotspot is **soft-enhance**; skill 1 stops at topics — the @ ordering splits by kind but **resolution happens in skill 2**, which runs **only for the human-confirmed topic** (at-finder → tone-learner → content-writer), producing drafts but not publishing.
