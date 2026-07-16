---
id: voice-from-static-exemplars
type: idea
tags: [post-confirm]
conflicts: [tone-learning-after-confirm]
---

# Voice comes from a maintained static exemplar file, not live per-run retrieval (decided)

**The human's judgment**: for the confirmed topic, voice/tone is anchored by a **maintained static file of verbatim exemplars** (currently @zarazhangrui posts) plus a few inlined voice rules — the agent does **not** fetch hot posts and comments live on each run.

Breakdown:
- **Why**: voice is stable and **orthogonal to the topic** — you learn how someone sounds from any of their posts, regardless of the current topic. Per-run live retrieval added cost and noise (and tempted echoing others' opinions) without improving voice.
- **What replaces it**: a curated exemplar file, grouped by post shape, refreshed on a cadence (not every run); the second skill step reads it and mimics cadence/structure, never opinions.
- **Timing unchanged**: this still runs only **after the human confirms a topic** — the shared judgment with [tone-learning-after-confirm](tone-learning-after-confirm.md); what this supersedes is only that card's **live-retrieval mechanism**.
- **Consequence**: live retrieval ([agent-reach](../sources/skills/agent-reach.md) / [last30days](../sources/skills/last30days.md)) is removed from the content skill; agent-reach now serves only the @ search.

**Boundary stays**: produces voice reference, not the post body ([target](../target.md)).
