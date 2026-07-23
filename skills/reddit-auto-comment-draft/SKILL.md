---
name: reddit-auto-comment-draft
description: >
  Find Reddit threads relevant to your repo inside a fitting subreddit and draft replies to them — an escalation ladder of variants, de-AI'd, new-account posture, each with the thread permalink and an inline rules summary.
  **Manually triggered** — use when the user says "comment on Reddit for my repo / find threads to reply to / warm up my Reddit account". Reads only, never posts — the human publishes. Data via rdt (read-only).
---

# reddit-auto-comment-draft — find threads, draft replies

Locate a fitting subreddit, find same-day threads your repo can credibly speak to, and draft reply variants that fit the sub and a **new, zero-karma account**. No demand-validation step. Never posts — output is drafts + permalinks + a rules summary for the human.

Shared contracts: [`rdt-readonly`](../reddit-shared/references/rdt-readonly.md) · [`reddit-voice`](../reddit-shared/references/reddit-voice.md) · [`guardrails`](../reddit-shared/references/guardrails.md) · [`no-ai-slop`](../no-ai-slop/SKILL.md) · [`storage`](../gtm-shared/references/storage.md).

## Flow

### 1. Pick the subreddit
Use the **user-specified** sub, else the stored choice (`.auto-gtm/subreddits.md`), else run `reddit-subreddit-finder` and take the top safe fit. Summarize its self-promo rules from `sub-info` (guardrails) before drafting.

### 2. Find relevant threads (no validation)
Derive terms from the product/highlights. `rdt search "<terms>" -r <sub> -s relevance -t day` — **relevance, last 24h**. Keep on-topic threads with a real reply opening; skip anything already well-answered. Pull each with `rdt read <post_id> -s top` for the post + top comments.

### 3. Learn the voice
Mimic the subreddit's high-upvote comments' cadence and structure (`rdt sub <sub> -s top` or the thread's top replies), **not their opinions**. See reddit-voice. (Tone priority, see storage: favorite bloggers → own account → user's ask → top-upvoted replies.)

### 4. Draft the escalation ladder
Per thread, three labeled variants, most restrained first:
- **no product mention** — pure help to the thread;
- **soft product mention** — help first, product named only where it's the natural answer;
- **founder perspective** — "we built X because…", only where the thread invites it.

Default posture: value-first, **no links in a first-touch reply** (new-account gate). If the account isn't warmed up, keep to the restrained end.

### 5. De-AI pass — no-ai-slop (mandatory)
Run every variant through the bundled **no-ai-slop** skill — apply [`../no-ai-slop/SKILL.md`](../no-ai-slop/SKILL.md), verify against [`../no-ai-slop/eval.md`](../no-ai-slop/eval.md). Anything that reads like an assistant gets rewritten as the subreddit would actually say it. No draft ships without this step.

## Output

A list, one entry per thread: the **permalink**, the three variants (restrained → forward) in fenced ` ```text ` blocks, and an **inline rules summary** (guardrails). State plainly: the human posts — via claude-in-chrome into the reply box, or copy-paste. This skill does not publish.

## Config

Subreddit(s), threads-found cap (default ~5), variant set (default the three above), voice-sample size (default ~15 top comments), search window (default `-t day`). Override per request.

## Boundary

Read-only via `rdt`. Drafts only — never comments, posts, or upvotes. Publishing is a human action. Finding communities is `reddit-subreddit-finder`; writing an original post is `reddit-post-drafter`.
