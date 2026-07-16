# hotspot-fetcher — call external tools to fetch recent trending signals

Responsibilities:
- Call an external-signal tool (**last30days** or **agent-reach**) to fetch recent trending
- **No script** — write a "call external tools" instruction in SKILL.md, called directly by the Agent (delegation, not a local data transformation)
- Does not build its own crawler
- Is **one of the independent topic sources** ([topic-source-independence](../../ideas/topic-source-independence.md)) — the hotspot itself can become a topic, and is displayed before reading the session

Boundary:
- **Soft-enhance**: when the tool is not installed, **still produce topics** (based on the session) while **prompting the user to install** last30days/agent-reach
- Parallel and independent from session-reader, no before/after dependency

Basis: [hotspots via external tools idea](../../ideas/hotspot-via-external-tools.md), [last30days](../../sources/skills/last30days.md), [agent-reach](../../sources/skills/agent-reach.md)
