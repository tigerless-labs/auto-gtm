# system — two skills: topic distillation → content generation

The pipeline is split into **two skills**. The interface between them is **one human-confirmed topic**: `x-topic-distiller` turns conversations + hotspots into topic drafts; after the human confirms one, `x-content-generator` turns it into content (@ + voice + draft).

## Skill 1 — x-topic-distiller (conversation → topics)

The hotspot and session are **two independent sources** ([topic-source-independence](../ideas/topic-source-independence.md)): a topic can come from hotspot only / session only / both overlapping.

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
    TG["Generate X topics: label kind (share/reflection); share-type carries the in-session entity as an unresolved @ candidate"]
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

```mermaid
flowchart LR
  SKILL1["SKILL.md<br/>orchestration · manual trigger"]
  HF["hotspot-fetcher<br/>call last30days/agent-reach · SKILL.md instruction · soft-enhance"]
  SR["session-reader<br/>read JSONL · 24h · excludes tool results · script"]
  DI["distiller<br/>merge three sources+extract entities/insight · prompt"]
  TG["topic-generator<br/>generate topics+value gate · prompt"]
  SKILL1 --> HF --> DI
  SKILL1 --> SR --> DI
  DI --> TG
  click HF "modules/hotspot-fetcher.md"
  click SR "modules/session-reader.md"
  click DI "modules/distiller.md"
  click TG "modules/topic-generator.md"
```

## Skill 2 — x-content-generator (confirmed topic → content)

Runs **only for the confirmed topic**, never for every draft ([tone-learning-after-confirm](../ideas/tone-learning-after-confirm.md)).

```mermaid
flowchart TD
  subgraph Human
    C["Confirm which topic to go with (from skill 1's drafts, or state a topic directly)"]
    RD["Receive @ account + post drafts"]
  end
  subgraph Agent
    AF["Find the @: use the handle from the source URL, else search X via agent-reach, else skip"]
    TL["Voice: read static exemplars (tone-examples.md) + inlined voice rules; mimic voice not opinions"]
    CW["Draft: 1-2 posts from topic + @ + voice; @ placed naturally + source link for shares"]
  end
  C --> AF --> TL --> CW --> RD
  click AF "modules/at-finder.md"
  click TL "modules/tone-learner.md"
  click CW "modules/content-writer.md"
```

```mermaid
flowchart LR
  SKILL2["SKILL.md<br/>orchestration · manual trigger · input = one confirmed topic"]
  AF["at-finder<br/>handle from source URL → agent-reach fallback → skip"]
  TL["tone-learner<br/>static tone-examples.md + inlined voice rules · no live retrieval"]
  CW["content-writer<br/>draft posts from topic+@+voice · prompt"]
  SKILL2 --> AF --> CW
  SKILL2 --> TL --> CW
  click AF "modules/at-finder.md"
  click TL "modules/tone-learner.md"
  click CW "modules/content-writer.md"
```
