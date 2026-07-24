# Tone — how auto-gtm chooses and applies voice (shared contract)

The single source of truth for tone. Every drafting skill (X/Reddit posts and replies) follows this; skills add only their platform's per-thread overlay. Two axes, **not** one ranked ladder.

## Voice — HOW it sounds (a fallback chain)

1. **Favorite bloggers** — the handles + their **~10 stored sample posts** in `~/Documents/auto-gtm/bloggers.md`.
2. **The user's own account** — same file, ~10 of their own posts captured alongside.
3. **Bundled fallback** — when no bloggers are set: X uses [`../../x-content-generator/references/tone-examples.md`](../../x-content-generator/references/tone-examples.md); Reddit uses the target sub's own high-upvote posts/comments (see [`../../reddit-shared/references/reddit-voice.md`](../../reddit-shared/references/reddit-voice.md)).

Mimic cadence and structure, **never opinions**.

## Content — WHAT it says (the user's explicit ask this run)

The user's ask governs content and format. It is a **different axis**, not a rung below the voice sources. On conflict, satisfy the ask's content **inside** the chosen voice's form (e.g. "make it two updates" → two first-person moves in the voice, not two headings).

## Per-thread overlay — replies only

When drafting a **reply**, also mimic that specific thread's top-voted replies' cadence — for this thread, not their opinions:
- **X:** `twitter tweet URL_OR_ID` → the post's top replies.
- **Reddit:** `rdt read <post_id> -s top` → the thread's top comments.

Original posts (X post / Reddit post) have no per-thread overlay.

## First capture & storage — once

The **first time** the user names favorite bloggers (and their own account), fetch **~10 posts each** via the [data layer](data-layer.md) (`twitter user-posts @handle`) and store the handles + samples to `bloggers.md` — see [storage.md](storage.md). Later runs **read the stored samples** — no re-fetch. **Refresh only when the user asks.** If `bloggers.md` is missing/empty and the user hasn't named anyone, use the bundled fallback and offer to capture bloggers.
