# system — skeleton of the X topic-distillation skill

The hotspot and session are **two independent sources** ([topic-source-independence](../ideas/topic-source-independence.md)): a topic can come from hotspot only / session only / both overlapping.

## Flow (human / agent swimlanes, pure logic)

```mermaid
flowchart TD
  subgraph Human
    T["Manual trigger: distill X topics from recent conversations"]
    R["Receive X topic drafts / or be told there's nothing worth posting"]
  end
  subgraph Agent
    H["Check hotspots: call external tools (soft-enhance; if not installed, skip+prompt to install)"]
    S["Read session: Claude Code JSONL, last 24h, excludes tool results"]
    M["Merge three sources: hotspot only / session only / overlap"]
    G{"Value gate: has substance?"}
    TG["Generate X topics: share-type @in-session entities; reflection-type searches X for bloggers to @ after the topic is set"]
  end
  T --> H
  T --> S
  H --> M
  S --> M
  M --> G
  G -- yes --> TG --> R
  G -- no --> R
  click H "modules/hotspot-fetcher.md"
  click S "modules/session-reader.md"
  click M "modules/distiller.md"
  click TG "modules/topic-generator.md"
```

## Architecture (modules; judgment goes through prompt / deterministic goes through script)

```mermaid
flowchart LR
  SKILL["SKILL.md<br/>orchestration · manual trigger"]
  HF["hotspot-fetcher<br/>call last30days/agent-reach · SKILL.md instruction · soft-enhance"]
  SR["session-reader<br/>read JSONL · 24h · excludes tool results · script"]
  DI["distiller<br/>merge three sources+extract entities/insight · prompt"]
  TG["topic-generator<br/>generate topics+value gate+reflection-type @ search · prompt"]
  SKILL --> HF --> DI
  SKILL --> SR --> DI
  DI --> TG
  click HF "modules/hotspot-fetcher.md"
  click SR "modules/session-reader.md"
  click DI "modules/distiller.md"
  click TG "modules/topic-generator.md"
```
