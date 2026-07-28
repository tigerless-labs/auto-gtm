# rdt — read-only data contract (Reddit)

Reddit data comes from `rdt` (`rdt-cli`), the plugin's **cookie-session** backend, invoked **through `reach fetch-reddit <cmd> [args…]`** — see [`../../gtm-shared/references/data-layer.md`](../../gtm-shared/references/data-layer.md). Skills never shell `rdt` directly; `reach` reuses the user's logged-in reddit.com cookie (`rdt login`, once) and returns `rdt`'s raw stdout unchanged. Anonymous scraping is a dead end (unauthenticated `.json` deprecated 2026-05-28, 403 with silent-fail; Reddit flagged RSS next) and new OAuth-app approval is effectively closed — so a login-state session is the durable path. `rdt` is **one** login-state option; `PRAW` is the mainstream upgrade when the user already holds OAuth credentials.

## Read-only whitelist — enforced in code

`status` · `search` · `read` · `sub` · `sub-info` · `popular` · `all` · `user` · `user-posts` · `user-comments` · `export`

`reach fetch-reddit` **refuses any command outside this list in code** (a write command raises before anything shells out) — this restriction is a code chokepoint, not a prose convention. NEVER attempt a write command: `comment`, `upvote`, `save`, `subscribe`, `logout`. The session cookie has write capability; the whitelist is what prevents its use.

(`status` is the read-only auth check — `authenticated: true|false`; `reach fetch-reddit` also reports a degrade signal when `rdt` is missing or unauthenticated.)

## Commands & fields

Invoke each as `reach fetch-reddit <cmd> [args…]`; the `<cmd> [args]` grammar and returned fields are:

- `search "<query>" [-r <sub>] [-s relevance|hot|top|new|comments] [-t hour|day|week|month|year|all] [-n N] --yaml -c`
  → posts with `title`, `selftext`, `ups`, `upvote_ratio`, `num_comments`, `subreddit`, `permalink` / `name` (t3_id), `created_utc`.
- `read <post_id> [-s best|top|new|controversial] [-n N] --yaml -c` → post plus comments (`body`, `ups`, author, depth).
- `sub <sub> [-s new|top|hot] [-n N]` → a subreddit's post listing (use `-s new` to sample recent posts).
- `sub-info <sub>` → `subscribers`, `restrict_posting`, `submission_type` (link/self/any), `public_description`, `advertiser_category`, `over18`, `url`.

Default to `-c --yaml` (compact, agent-friendly). Add `--full-text` only when full bodies are required.

## Capability-boundary approximations — state them wherever used

- **Subreddit rules**: `rdt` exposes no full rules text (`sub-info` only wraps `about.json`). Approximate posting-compliance from `restrict_posting` + `submission_type` + `public_description`, and say it is an approximation. (Full `rules[]` IS reachable via the login-state session — verified against `about/rules.json` — but keyless fetch of it 403s; the redesign adds it as a sanctioned read-op, so until then rules stay an approximation here.)
- **Removal rate**: not a field. Estimate by sampling `reach fetch-reddit sub <sub> -s new` and counting `removed` / `[removed]`, and say it is a sample-based estimate.
- **No central index / history**: discovery and validation are per-query and live — not corpus-wide trends or cross-user overlap. Skills are on-demand, never continuous monitors.
