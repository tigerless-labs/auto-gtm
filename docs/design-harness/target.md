# target — acceptance criteria for output

The human's requirements for output are registered here; output fulfils this list,
and every requirement is checkable. When a requirement changes, the agent re-derives
the affected parts of output in the same turn.

## Purpose

Design a skill: **distill X/Twitter post topics from a period of conversation sessions with AI, combined with current hotspots**.
The target platform is pinned to **X/Twitter**. It only handles the "conversation → topic" extraction; the body/title/publishing after the topic is out of scope.

## Current requirements

- [ ] Input is **conversation session history** (Distill-style Smart History Processing), not keywords/links hand-fed by the user
- [ ] **Combine current hotspots**: during extraction, tap into the external-signal layer (Agent-Reach / last30days) to supplement topics with recent-trending evidence — this is core, not optional
- [ ] Output is a **post topic**; **the output format is not constrained for now** (no fixed schema yet)
- [ ] Architecture follows **SKILL.md orchestration + script execution**: judgment steps (extraction/generation) go through prompt, deterministic steps (data-fetching/dedup) go through script

## Fulfilment map

- input=conversation session history → [session-reader](output/modules/session-reader.md)
- combine current hotspots → [hotspot-fetcher](output/modules/hotspot-fetcher.md)
- output=post topic (format unconstrained) → [topic-generator](output/modules/topic-generator.md)
- architecture=SKILL.md orchestration + script execution → [system.md](output/system.md) + [file-structure.md](output/file-structure.md)
