# topic-generator — generate X topics (two content types) + value gate

Responsibilities:
- Assemble the X post topic, where the source can be **hotspot only / session only / overlap** ([topic-source-independence](../../ideas/topic-source-independence.md))
- **Two content types + @ ordering** ([at-ordering](../../ideas/at-ordering.md)):
  - Share-type: @ the **in-session entity** directly (already extracted by the distiller) — first look up the `x_handle_map` static table for the handle; if not found, fall back to agent-reach or skip
  - Reflection-type: **after the topic is set**, use **agent-reach to search X** for bloggers/posts on the same subject to @ (out-of-session); **if not installed, prompt the user to install it** while still producing topics without the @
- **Value gate**: if there's no substance, skip it, don't force it
- Judgment steps → go through a **prompt**

Boundary:
- Only produces topics, does not write body/title/publishing
- Output format not constrained for now (no fixed schema)

Basis: [X topic style idea](../../ideas/x-topic-style-ganhuo-at-creators.md), the upstream distiller's output
