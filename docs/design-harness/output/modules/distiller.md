# distiller — distill substance from the session: entities + insight

Responsibilities:
- **Merge three sources**: hotspot only / session only / both overlapping ([topic-source-independence](../../ideas/topic-source-independence.md))
- **Extract entities**: tools/products/people in the session → candidate @ targets
- **Extract insight/reflection**: one conclusion that stands on its own, or a reflection worth stating
- Judgment steps → go through a **prompt** (not a script)

Boundary:
- Only distills, does not generate finished topics (handed to the downstream topic-generator)
- Does no external data-fetching (handed to the upstream hotspot-fetcher)

Basis: [X topic style idea](../../ideas/x-topic-style-ganhuo-at-creators.md), [content-collector's prompt/schema pattern](../../sources/skills/content-collector-skill.md), [Distill](../../sources/skills/distill.md)
