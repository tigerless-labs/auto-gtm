---
name: x-content-generator
description: >
  Generate X/Twitter post content from a confirmed topic: find the account to @, learn the tone from hot posts + comments on the same theme, then draft the post.
  **Manually triggered** — use after a topic is confirmed (typically one produced by x-topic-distiller) and the user says things like "turn this topic into a post /
  find who to @ and the tone / write it up".
  Takes "topic → content"; does not distill topics (that's x-topic-distiller) and does not publish.
---

# x-content-generator — generate X content from a confirmed topic

Given **one confirmed topic** (usually picked from x-topic-distiller's drafts, or stated directly by the user), do the content-side work: resolve the @ account, learn the tone of what performs on this theme, and produce a post draft.

## When to trigger

**Manual only.** Run only when the user has a confirmed topic in hand and asks to generate content for it. Never for every topic draft — only the confirmed one (skips the tokens on discarded topics).

## Input

One topic + its kind:
- **Share-type** — shares a tool/person/product; comes with the in-session entity to @.
- **Reflection-type** — an original reflection/insight; the @ target is unknown and must be searched.

If the kind isn't labeled, infer it from the topic itself.

## Flow

### 1. Find the @

- **Share-type** → first look up [`references/x_handle_map.md`](references/x_handle_map.md) for the entity's handle; if not found, use `agent-reach` to search X as a fallback; if still not found, skip the @.
- **Reflection-type** → use `agent-reach` to search X for same-theme accounts/posts to @; if `agent-reach` isn't installed, **prompt the user to install it** and continue without an @.

### 2. Learn the tone

- Search for **hot posts on the same theme + their top comments** — use `agent-reach`'s X channel for precise retrieval; `last30days` as fallback.
- **Soft-enhance:** if neither is installed, skip this step, continue, and prompt the user to install one.
- Study them and output **tone notes**: voice, structure, hook patterns, and **what the comments reward** (comments reveal what the audience responds to, not just what authors write) + 2-3 exemplar posts as reference.

### 3. Generate the content

Write **1-2 post drafts** based on the topic + the @ + the tone notes. Follow the tone notes' voice/structure/hook patterns; place the @ naturally. If step 2 was skipped, still draft — just note the draft is not tone-grounded.

## Output

Per run: **the @ account (or "none found") + tone notes with exemplars (or "skipped — install agent-reach/last30days") + 1-2 post drafts**. Follow the user's format if they ask for another.

## Boundary

Starts from a confirmed topic — topic distillation lives in `x-topic-distiller`. Produces drafts only; does not publish.
