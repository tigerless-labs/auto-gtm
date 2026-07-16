# tone-learner — learn the tone from hot posts + comments on the confirmed theme

Part of **skill 2: x-content-generator**.

Responsibilities:
- **Trigger**: only for the **confirmed topic** — never for every draft (skips the tokens on discarded topics; [tone-learning-after-confirm](../../ideas/tone-learning-after-confirm.md))
- Search for **hot posts on the same theme + their top comments** (comments reveal what the audience rewards, not just what authors write)
- Tools: **agent-reach's X channel** for precise post/comment retrieval; **last30days** as fallback for aggregated sentiment; same **soft-enhance** discipline — if neither is installed, skip + prompt to install
- Output: **tone notes** (voice, structure, hook patterns, what the comments reward) + 2-3 exemplar posts as reference
- Judgment step (what counts as "the tone") → goes through a **prompt**; retrieval delegates to external tools via SKILL.md instruction (no new script)

Boundary:
- Produces tone reference material; drafting consumes it downstream in content-writer

Basis: [tone-learning-after-confirm idea](../../ideas/tone-learning-after-confirm.md), the confirmed topic from [topic-generator](topic-generator.md)
