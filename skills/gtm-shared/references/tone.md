# Tone — what to read before you draft

Samples calibrate how it sounds. The opinions stay the user's own.

- **Where** — `~/Documents/auto-gtm/bloggers.md`, in two blocks: the user's favorite bloggers, and the user's own account, ~10 verbatim posts each.
- **An empty block** — ask for that one by name. Once the user answers, fetch ~10 posts via the [data layer](data-layer.md) (`reach fetch-x --query "from:<handle>"`) and store them ([storage](storage.md)). Later runs only read. Refresh when asked.
- **The user skips** — use the bundled examples ([X](../../x-shared/references/tone-examples.md), [Reddit](../../reddit-shared/references/reddit-voice.md)) and say which voice the draft ended up in.
- **Replies don't use these samples** — a reply takes its sample from the thread it answers, and each comment-draft skill says how. The blocks here are posts, and a post's shape doesn't transfer to a reply.
