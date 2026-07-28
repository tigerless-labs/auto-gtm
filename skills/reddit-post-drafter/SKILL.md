---
name: reddit-post-drafter
description: >
  Turn a confirmed topic into a Reddit post (title + body) for a specific subreddit — in the sub's voice, de-AI'd, new-account posture, with an inline rules/self-promo check.
  **Manually triggered** — use after a topic is confirmed (typically from topic-scout) and the user says "write the Reddit post / draft this as a post for r/X". Reads only, never posts — the human publishes. Data via rdt (read-only).
---

# reddit-post-drafter — write a Reddit post from a topic

Given **one confirmed topic** and a target subreddit, draft the post (title + body) that fits the sub and a **new, zero-karma account**. Never posts — output is the draft + a rules/self-promo check for the human.

Shared contracts: [`rdt-readonly`](../reddit-shared/references/rdt-readonly.md) · [`reddit-voice`](../reddit-shared/references/reddit-voice.md) · [`guardrails`](../reddit-shared/references/guardrails.md) · [`no-ai-slop`](../no-ai-slop/SKILL.md) · [`storage`](../gtm-shared/references/storage.md).

## Flow

### 1. Target + rules
Use the user-specified sub, else the stored choice (`~/Documents/auto-gtm/<product-slug>/subreddits.md`), else run `reddit-subreddit-finder`. From `reach fetch-reddit sub-info <sub>` summarize `submission_type`, `restrict_posting`, self-promo rules, flair (guardrails). If the sub bans self-promo and the topic is promotional, **say so and stop** — suggest the comment skill instead.

### 2. Learn the voice
Read the sub's high-upvote **posts** (`reach fetch-reddit sub <sub> -s top`) and mimic how titles and bodies actually read there — length, formatting, how much story vs. ask. Over that, read the voice samples per [`tone`](../gtm-shared/references/tone.md). This is an original post — no per-thread overlay.

### 3. Draft
- Frame as **value / story**, not an ad: what you built, what it's for, what you learned — the product is the subject, not a pitch.
- Respect the new-account gate: no link-dump; a link only where the sub allows and it's the natural payoff.
- Give **1–2 title options + one body**.

### 4. De-AI pass — no-ai-slop (mandatory)
Run the draft through the bundled **no-ai-slop** skill — apply [`../no-ai-slop/SKILL.md`](../no-ai-slop/SKILL.md), verify against [`../no-ai-slop/eval.md`](../no-ai-slop/eval.md). No draft ships without this step.

## Output

An md with: **title option(s)** and the **body** in a fenced ` ```text ` block (one-click copyable), the target sub, and an **inline rules + self-promo: safe/risky** note. State plainly: the human posts. This skill does not publish.

## Boundary

Read-only via `rdt`. Drafts only — never posts or upvotes. Selecting the topic is `topic-scout`; finding the community is `reddit-subreddit-finder`; drafting replies is `reddit-auto-comment-draft`.
