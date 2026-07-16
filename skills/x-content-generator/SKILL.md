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

## Stance: sincere altruism

Every draft must **give the reader something to walk away with** — a resource, a framework, a reframe, or a lived observation elevated to insight — and read as genuine felt reflection, never self-promotion or engagement bait. Baseline writing patterns live in [`references/style-benchmarks.md`](references/style-benchmarks.md) (currently benchmarked on @zarazhangrui); read it before drafting. Core rules:

- **Open with the concrete** (a scene, a person, a number), then elevate to the insight — the experience earns the right to the opinion.
- **Share-type = tool + cognition claim**: not "I used X" but "X reveals something most people haven't realized yet"; always @ the author (attribution is part of the altruism).
- **Package multi-point takeaways as numbered frameworks**; compress single takeaways into a reframe one-liner.
- **Conversational voice, short lines** — "the best writing sounds like talking"; no corporate tone, no thread boilerplate.
- **Product/tool mentions are pain-point stories** — value first, product second.

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

- **Voice anchor (who it sounds like):** start from [`references/style-benchmarks.md`](references/style-benchmarks.md) (rules + why they work) and inject 3-5 verbatim exemplars from [`references/tone-examples.md`](references/tone-examples.md) whose *shape* matches the draft's intent. **Learn voice, not opinions** — mimic cadence/hook/structure, never lift her takes.
- **Theme signal (what lands on this topic):** refine with live retrieval — this axis is about the *topic*, not her voice:
- Search for **hot posts on the same theme + their top comments** — use `agent-reach`'s X channel for precise retrieval; `last30days` as fallback.
- **Soft-enhance:** if neither is installed, skip live retrieval, draft from the style benchmarks alone, and prompt the user to install one.
- Study them and output **tone notes**: voice, structure, hook patterns, and **what the comments reward** (comments reveal what the audience responds to, not just what authors write) + 2-3 exemplar posts as reference.

### 3. Generate the content

Write **1-2 post drafts** based on the topic + the @ + the tone notes, honoring the Stance section (reader takeaway, concrete-first opening, conversational voice). Follow the tone notes' voice/structure/hook patterns; place the @ naturally. If live retrieval was skipped, draft from the style benchmarks — note the draft is benchmark-grounded but not theme-grounded.

## Output

Per run: **the @ account (or "none found") + tone notes with exemplars (or "skipped — install agent-reach/last30days") + 1-2 post drafts**. Follow the user's format if they ask for another.

## Boundary

Starts from a confirmed topic — topic distillation lives in `x-topic-distiller`. Produces drafts only; does not publish.
