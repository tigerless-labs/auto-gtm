---
name: reddit-subreddit-finder
description: >
  Rank candidate subreddits for a product/topic on Reddit — multi-axis fit + self-promo safety + a rules summary per candidate.
  **Manually triggered** — use when the user asks "which subreddit should I post this in / find communities for this / where's my audience on Reddit".
  Takes "topic → ranked subreddits"; reads only, never joins or posts. Data via rdt (read-only).
---

# reddit-subreddit-finder — rank subreddits for a topic

Given a GTM object (a product/topic in one line), return a **ranked table of candidate subreddits** with fit, self-promo safety, and a rules summary. On-demand and live: no central index — fit is computed from what `rdt` returns now, not from corpus overlap.

Shared contracts: [`rdt-readonly`](../reddit-shared/references/rdt-readonly.md) · [`guardrails`](../reddit-shared/references/guardrails.md).

## When to trigger

Manual only. Run when the user asks where to post, or to find communities/audience for a topic.

## Flow

### 1. Find candidates
Derive query terms from the GTM object. `reach fetch-reddit search "<terms>" -s relevance -t year` — **relevance, not top** (top biases to mega-subs and off-topic viral posts). Keep only on-topic posts, and collect the subreddits they recur in as candidates.

### 2. Profile each candidate
`reach fetch-reddit sub-info <sub>` for `subscribers`, `restrict_posting`, `submission_type`, `public_description`. For a rough removal signal, sample `reach fetch-reddit sub <sub> -s new` and read each post's `removed` / `removed_by_category` field (per-post, not a single grep count).

### 3. Score — multi-axis, relative
Judge three axes per candidate from the data, and rank **relatively** across candidates (no fixed numbers):
- **audience match** — how on-topic its content/description is to the GTM object;
- **self-promo tolerance** — from `submission_type` + the removal signal + the rules summary (`restrict_posting` is near-universally `true`, so weak on its own);
- **activity** — subscribers plus recent post cadence.

### 4. Safety + rules
Per candidate emit a hard **self-promo: safe / risky** flag consistent with its rules, a rules summary (see guardrails; it is an approximation), and a one-line tailored entry angle.

## Output

A ranked table, best first:

`subreddit | subscribers | fit (audience / tolerance / activity) | self-promo safe? | rules summary | entry angle`

Stops here for the human to choose a community.

## Config

Candidate count (default ~8), search window (default `-t year`), removal-sample size (default ~25). Override per request.

## Boundary

Read-only via `rdt` (whitelist in rdt-readonly). Ranks only — never joins, subscribes, or posts. Drafting a reply is `reddit-auto-comment-draft`; writing a post is `reddit-post-drafter`.
