# topic-generator — generate X topics (two content types) + value gate

Part of **skill 1: x-topic-distiller**.

Responsibilities:
- Assemble the X post topic, where the source can be **hotspot only / session only / overlap** ([topic-source-independence](../../ideas/topic-source-independence.md))
- **Label the kind** ([at-ordering](../../ideas/at-ordering.md)):
  - Share-type: carries the **in-session entity** (already extracted by the distiller) as an **unresolved @ candidate** — raw name only; handle lookup happens downstream in at-finder (skill 2)
  - Reflection-type: no @ target yet — searching one is downstream work, done **after the topic is confirmed**
- **Value gate**: if there's no substance, skip it, don't force it
- Judgment steps → go through a **prompt**

Boundary:
- Only produces topics; @ resolution, tone learning, and drafting live in **skill 2: x-content-generator**
- Output format not constrained for now (no fixed schema)

Basis: [X topic style idea](../../ideas/x-topic-style-ganhuo-at-creators.md), the upstream distiller's output
