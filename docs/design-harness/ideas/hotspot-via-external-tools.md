---
id: hotspot-via-external-tools
type: idea
tags: [external-signal]
---

# Hotspot acquisition via external tools: recommend the user install last30days or agent-reach; the skill does not build its own scraping

The hotspot step does not build its own crawler; it relies on ready-made external-signal tools — [last30days](../sources/skills/last30days.md) (a recent-sentiment finished product) or [agent-reach](../sources/skills/agent-reach.md) (a multi-platform data-fetching base). The skill only needs to call them; which one to install is up to the user (installing one is recommended).

**Dependency mode: soft-enhance** — when the tool is not installed, it **still produces topics** (based on the session itself) while **prompting the user to install** last30days/agent-reach to get trending evidence. The hotspot is "icing on the cake" and does not block the main flow.
