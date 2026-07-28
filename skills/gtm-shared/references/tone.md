# Tone — what to read before you draft

Voice is material, not a rule to satisfy. Read the samples, then write as yourself.

## Where the samples live

`~/Documents/auto-gtm/bloggers.md`, in two blocks: the user's favorite bloggers, and the user's own account, each with ~10 verbatim posts.

## When a block is missing

Ask for the one that's missing, by name. A file that already lists bloggers but has an empty own-account section is still missing a block — a non-empty file is not a complete file.

Once the user names a handle, fetch ~10 posts via the [data layer](data-layer.md) (`reach fetch-x --query "from:<handle>"`) and store them — see [storage.md](storage.md). Later runs read the file. Refresh only when the user asks.

If the user would rather skip, use the bundled examples — X: [`../../x-shared/references/tone-examples.md`](../../x-shared/references/tone-examples.md); Reddit: the target sub's own high-upvote posts, see [`../../reddit-shared/references/reddit-voice.md`](../../reddit-shared/references/reddit-voice.md) — and say which voice the draft ended up in.

## What the samples are for

They calibrate how it sounds. The opinions stay the user's own.

## Replies read the thread too

- **X:** `reach fetch-x --tweet-url URL` → the post and its top replies.
- **Reddit:** `reach fetch-reddit read <post_id> -s top` → the thread's top comments.

Same use: the cadence of that thread, not its opinions. Original posts skip this.
