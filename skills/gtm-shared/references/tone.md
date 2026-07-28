# Tone — what to read before you draft

Samples calibrate how it sounds. The opinions stay the user's own.

- **Where** — `~/Documents/auto-gtm/bloggers.md`, in two blocks: the user's favorite bloggers, and the user's own account, ~10 verbatim posts each.
- **An empty block** — ask for that one by name. Once the user answers, fetch ~10 posts via the [data layer](data-layer.md) (`reach fetch-x --query "from:<handle>"`) and store them ([storage](storage.md)). Later runs only read. Refresh when asked.
- **The user skips** — use the bundled examples ([X](../../x-shared/references/tone-examples.md), [Reddit](../../reddit-shared/references/reddit-voice.md)) and say which voice the draft ended up in.
- **Replies** — read that thread too: `reach fetch-x --tweet-url URL`, or `reach fetch-reddit read <post_id> -s top`. Its cadence, not its opinions.
