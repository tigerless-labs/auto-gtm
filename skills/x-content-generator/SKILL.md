---
name: x-content-generator
description: >
  Generate X/Twitter post content from a confirmed topic: learn the voice from reference exemplars, then draft.
  **Manually triggered** — use after a topic is confirmed (typically from topic-scout) and the user says things like "turn this topic into a post / write it up".
  Takes "topic → content"; does not select topics (that's topic-scout) and does not publish.
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
  - Fight the default register: your instinct is tidy release-note prose (summary
    opener, "Update one:" headings, parallel structure, closing moral). The
    exemplars never do this — open with a scene or a first-person action.
  - When the user's structural ask conflicts with the exemplars' shape (e.g.
    "make it two updates"), satisfy the content of the ask inside the voice —
    two first-person moves, not two headings. On form, the exemplars win.
- **Tone source, in priority order** (see [`../gtm-shared/references/storage.md`](../gtm-shared/references/storage.md)):
  1. the user's **favorite bloggers** (`~/Documents/auto-gtm/bloggers.md`) — fetch a few of their recent posts with `twitter user-posts @handle` ([data layer](../gtm-shared/references/data-layer.md)) and mimic their cadence;
  2. the user's **own account**;
  3. the user's **explicit ask** this run.
  Fall back to the bundled exemplars below when none is available.
- Read the full [`references/tone-examples.md`](references/tone-examples.md) for verbatim exemplars. **Mimic cadence/structure, not opinions.**
- Run every draft through the bundled **no-ai-slop** skill before finalizing — apply [`../no-ai-slop/SKILL.md`](../no-ai-slop/SKILL.md) and verify against [`../no-ai-slop/eval.md`](../no-ai-slop/eval.md).
- Write **1-2 drafts**; include the source link for shares.

## Output

1-2 drafts, each with the source link for shares.

**Present every draft inside a fenced code block** (```text), exactly as it would be pasted into X — line breaks included, no markdown formatting (no bold/headers/bullets) inside the draft. **Never format drafts as blockquotes (`>`)** — they render as uncopyable bars in chat UIs. The code block is what makes it one-click copyable; commentary about the draft goes outside the block.

Example shape:

````
### Draft 1

```text
We removed the trend-fetching step from our topic skill.

Your own coding sessions are the content pipeline. Chasing hotspots is the opposite of building in public.

https://github.com/example/repo
```
````

## Boundary

Starts from a confirmed topic (selection is `topic-scout`). Drafts only; does not publish.
