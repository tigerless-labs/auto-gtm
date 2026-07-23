# rdt — read-only data contract (Reddit)

All Reddit data comes from `rdt` (`rdt-cli`, the plugin's own login-state backend — see [`../../gtm-shared/references/data-layer.md`](../../gtm-shared/references/data-layer.md)), reusing the user's logged-in reddit.com cookie. Set up once (`rdt login`), remembered. No OAuth, no anonymous scraping — both are 403-blocked.

## Read-only whitelist — the ONLY commands a Reddit skill may call

`search` · `read` · `sub` · `sub-info` · `popular` · `all` · `user` · `user-posts` · `user-comments` · `export`

NEVER call a write command: `comment`, `upvote`, `save`, `subscribe`, `logout`. The session cookie has write capability; skills must not exercise it.

## Commands & fields

- `rdt search "<query>" [-r <sub>] [-s relevance|hot|top|new|comments] [-t hour|day|week|month|year|all] [-n N] --yaml -c`
  → posts with `title`, `selftext`, `ups`, `upvote_ratio`, `num_comments`, `subreddit`, `permalink` / `name` (t3_id), `created_utc`.
- `rdt read <post_id> [-s best|top|new|controversial] [-n N] --yaml -c` → post plus comments (`body`, `ups`, author, depth).
- `rdt sub <sub> [-s new|top|hot] [-n N]` → a subreddit's post listing (use `-s new` to sample recent posts).
- `rdt sub-info <sub>` → `subscribers`, `restrict_posting`, `submission_type` (link/self/any), `public_description`, `advertiser_category`, `over18`, `url`.

Default to `-c --yaml` (compact, agent-friendly). Add `--full-text` only when full bodies are required.

## Capability-boundary approximations — state them wherever used

- **Subreddit rules**: `rdt` exposes no full rules text. Approximate posting-compliance from `restrict_posting` + `submission_type` + `public_description`, and say it is an approximation.
- **Removal rate**: not a field. Estimate by sampling `rdt sub <sub> -s new` and counting `removed` / `[removed]`, and say it is a sample-based estimate.
- **No central index / history**: discovery and validation are per-query and live — not corpus-wide trends or cross-user overlap. Skills are on-demand, never continuous monitors.
