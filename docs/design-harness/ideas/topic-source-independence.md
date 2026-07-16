---
id: topic-source-independence
type: idea
tags: [topic-design]
---

# Hotspot and session have no necessary before/after relationship: a topic can come from hotspot only / session only / both overlapping

The hotspot ([recent trending fetched via external tools](hotspot-via-external-tools.md)) and the session ([24h conversation history](session-read-range-timewindow.md)) are **two independent topic sources**, with no necessary dependency of one before the other. An X topic can:
- **Come from hotspots only**: a topic is recently trending but was never discussed in the conversation → it can still become a topic.
- **Come from the session only**: a valuable takeaway/reflection in the conversation, unrelated to any current hotspot → it can still become a topic.
- **Overlap of both**: what was discussed in the conversation happens to hit a recent hotspot → the strongest topic (both substance and momentum).

Therefore, architecturally the two are **parallel and independent** inputs, merged and considered across the three source types at the generation stage. In display order the hotspot comes before reading the session (the human's requirement), but that is only layout, not a hard dependency.
