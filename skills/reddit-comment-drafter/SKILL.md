---
name: reddit-comment-drafter
description: >
  Draft a Reddit reply for a specific thread — an escalation ladder of variants, de-AI'd, new-account posture, with the thread permalink and an inline rules summary.
  **Manually triggered** — use when the user gives a thread and asks "help me draft a reply / how should I respond to this".
  Takes "thread → reply drafts"; reads only, never posts — the human publishes. Data via rdt (read-only).
---

# reddit-comment-drafter — draft a Reddit reply

Given a thread (id or permalink) plus the GTM object and what you've actually built, draft reply variants that fit the subreddit and a **new, zero-karma account**. Never posts — output is drafts + permalink + a rules summary for the human to publish.

Shared contracts: [`rdt-readonly`](../reddit-shared/references/rdt-readonly.md) · [`reddit-voice`](../reddit-shared/references/reddit-voice.md) · [`guardrails`](../reddit-shared/references/guardrails.md) · [`no-ai-slop`](../no-ai-slop/SKILL.md).

## When to trigger

Manual only. Run when the user gives a thread and asks for a reply draft.

## Flow

### 1. Read context
`rdt read <post_id> -s top` for the post and top comments — what is actually being discussed and what has already been answered.

### 2. Learn the voice
Fetch the subreddit's high-upvote comments (`rdt sub <sub> -s top`, or from the thread) and mimic their cadence and structure, **not their opinions**. See reddit-voice.

### 3. Draft the escalation ladder
Three labeled variants, most restrained first:
- **no product mention** — pure help to the thread;
- **soft product mention** — help first, product named only where it's the natural answer;
- **founder perspective** — "we built X because…", only where the thread invites it.

Default posture: value-first, **no links in a first-touch reply** (new-account gate). If the account isn't warmed up, keep to the restrained end.

### 4. De-AI pass — no-ai-slop (mandatory)
Run the bundled **no-ai-slop** skill on every variant before output: apply the patterns in [`../no-ai-slop/SKILL.md`](../no-ai-slop/SKILL.md) and verify against [`../no-ai-slop/eval.md`](../no-ai-slop/eval.md). Anything that reads like an assistant gets rewritten as the subreddit would actually say it. No draft ships without this step.

## Output

The three variants (restrained → forward), the thread permalink, and an **inline rules summary** (guardrails). State plainly: the human posts — via claude-in-chrome into the reply box, or copy-paste. This skill does not publish.

## Config

Variant set (default the three above), voice-sample size (default ~15 top comments). Override per request.

## Boundary

Read-only via `rdt`. Drafts only — never comments, posts, or upvotes. Publishing is a human action. Finding communities is `reddit-subreddit-finder`; validating demand is `reddit-demand-validator`.
