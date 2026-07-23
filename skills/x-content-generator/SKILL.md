---
name: x-content-generator
description: >
  Generate X/Twitter post content from a confirmed topic: learn the voice from reference exemplars, then draft.
  **Manually triggered** — use after a topic is confirmed (typically from x-topic-distiller) and the user says things like "turn this topic into a post / write it up".
  Takes "topic → content"; does not distill topics (that's x-topic-distiller) and does not publish.
---

# x-content-generator — generate X content from a confirmed topic

Given **one confirmed topic**, do the content-side work: learn the voice, draft.

## Stance

Give the reader something worth their time, in a sincere voice, never engagement bait. If the shared thing is already sharp (a formula, a one-liner, a clean insight), let it stand — the thing itself is enough. Do not bolt your own hot-take on top.

## Flow

### Learn the voice and draft

- Voice rules:
  - First person, conversational, short lines. "The best writing sounds like talking."
  - No em-dashes.
  - If the shared thing is already sharp, let it stand — don't add your own hot-take.
  - Every sentence must carry real information — cut any line that doesn't.
- Read the full [`references/tone-examples.md`](references/tone-examples.md) for verbatim exemplars. **Mimic cadence/structure, not opinions.**
- Run every draft through the bundled **no-ai-slop** skill before finalizing — apply [`../no-ai-slop/SKILL.md`](../no-ai-slop/SKILL.md) and verify against [`../no-ai-slop/eval.md`](../no-ai-slop/eval.md).
- Write **1-2 drafts**; include the source link for shares.

## Output

1-2 drafts, each with the source link for shares.

## Boundary

Starts from a confirmed topic (distillation is `x-topic-distiller`). Drafts only; does not publish.
