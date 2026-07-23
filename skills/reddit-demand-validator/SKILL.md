---
name: reddit-demand-validator
description: >
  Validate a demand hypothesis on Reddit — grade matching posts by signal strength (four buckets, Money Talk highest) with an evidence permalink per claim.
  **Manually triggered** — use when the user asks "is there real demand for X on Reddit / do people actually want this / validate this need".
  Takes "hypothesis → demand-signal report"; on-demand (not a monitor), reads only, never contacts users. Data via rdt (read-only).
---

# reddit-demand-validator — grade Reddit demand signal

Given a demand hypothesis (plus optional target subreddits), search Reddit and grade the matching posts by **behavioral signal strength**, each backed by a permalink and date. On-demand: a one-shot report, not continuous monitoring or alerting.

Shared contracts: [`rdt-readonly`](../reddit-shared/references/rdt-readonly.md) · [`guardrails`](../reddit-shared/references/guardrails.md).

## Why this exists

Keyword alerting floods noise. The value is the **grading layer** — ranking matches by behavior and response gap — not the keyword match itself.

## When to trigger

Manual only. Run when the user asks to validate demand, or whether people want X on Reddit.

## Flow

### 1. Gather
Derive query terms from the hypothesis. Search **within the target subreddits** (use finder's candidates if none were given): `rdt search "<terms>" -r <sub> -s relevance -t year` (`-t month` for freshness). Cross-subreddit `-s top` floods off-topic viral posts — restrict with `-r` and sort by relevance. Keep on-topic matches; pull the strongest threads with `rdt read <id>` for context and comments.

### 2. Grade — four buckets, highest first
Classify each matching post/comment:
- **Money Talk** — pays, would pay, mentions price/budget ("shut up and take my money"). Highest.
- **Solution Requests** — "looking for / any tool that / how do I". Active demand.
- **Pain Points** — complaints, frustration, self-built workarounds.
- **Hot Discussions** — high engagement on the topic, weaker intent.

### 3. Weight
Overlay **response gap + momentum**: a small thread with unanswered Money Talk outranks a large off-topic one. Optional competitor lens — search a competitor's name inside industry subs, split complaints (your opportunity) vs praise (learn from).

## Output

A demand-signal report: matches grouped by bucket (Money Talk first), each with a quote + permalink + date; then a one-paragraph read on overall strength. Stops here for the human to judge.

## Config

Search window (default `-t year`), threads-read cap (default ~15), target subs (default cross-subreddit). Override per request.

## Boundary

Read-only via `rdt`. Reports only — no posting, no DMs, no contacting users, no targeting lists. On-demand, not a monitor. Finding communities is `reddit-subreddit-finder`; drafting a reply is `reddit-comment-drafter`.
