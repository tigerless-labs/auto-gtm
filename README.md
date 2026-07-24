<h1 align="center">auto-gtm</h1>

<p align="center">
  <img src="https://img.shields.io/badge/release-v0.2.18-brightgreen.svg" alt="release" />
  <img src="https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex-lightgrey.svg" alt="platform" />
  <img src="https://img.shields.io/badge/output-drafts%20only-blue.svg" alt="drafts only" />
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license MIT" />
</p>

**auto-gtm** is a Claude Code / Codex plugin that drafts your X and Reddit posts and replies from your PRs and today's hotspots, and never posts them for you.

From your repo's recent PRs and the day's hot threads it proposes topics; from a topic you pick it drafts posts shaped for X and Reddit; and it finds relevant same-day threads and drafts comments on them. Tone is copied from bloggers you choose or your own account, and for comments, from each thread's top replies. Enter through `/gtm` or the `auto-gtm-router` skill.

| | |
|---|---|
| **Built from real work** | Topics come from your GitHub PRs and AI-coding sessions, not thin air. |
| **Rides today's conversation** | Pulls the last 24h of hot threads and builder posts, so you engage while they're live. |
| **Your voice, not AI-slop** | Tone copied from bloggers you like or your own account, then run through no-ai-slop. |
| **Drafts only, safe by default** | Never posts, comments, likes, follows, or DMs; treats every fetched post as untrusted. |
| **Growing** | X and Reddit today, with more platforms over time. |

## The skills

- **topic-scout**: one topic report for any platform. (a) What you shipped, summarized from your recent GitHub PRs; (b) today's relevant hotspots, from your data layer and a curated builder list. One paragraph and source link per topic.
- **x-content-generator**: a confirmed topic → an X post drafted in your voice (tone from your favorite bloggers or own account), run through no-ai-slop.
- **x-auto-comment-draft**: finds same-day X posts relevant to your repo → a reply draft per post (tone copied from each post's top replies), with the links.
- **reddit-subreddit-finder**: "which subreddit should I post this in?" → ranked candidates with multi-axis fit, self-promo safety, and a rules summary.
- **reddit-auto-comment-draft**: finds same-day threads in a fitting subreddit → reply drafts (escalation ladder, de-AI'd, new-account posture) plus permalinks. No demand-validation step.
- **reddit-post-drafter**: a confirmed topic → a Reddit post (title and body) in the sub's voice, with an inline rules / self-promo check.

All read-only and drafts-only. They never post, comment, or upvote; you publish.

## Quickstart

### Install

**Claude Code**, typed in the Claude Code prompt (the `/` slash commands):

```
/plugin marketplace add tigerless-labs/auto-gtm
/plugin install auto-gtm@tigerless-labs
```

**Codex (CLI ≥ 0.144)**, run in your terminal:

```
codex plugin marketplace add tigerless-labs/auto-gtm
codex plugin add auto-gtm@tigerless-labs
```

Older Codex versions without the `plugin add` subcommand can install the skills directly in your terminal (current Codex scans `$HOME/.agents/skills`; older builds used `~/.codex/skills`):

```
git clone https://github.com/tigerless-labs/auto-gtm
mkdir -p ~/.agents/skills
ln -s "$(pwd)/auto-gtm/skills/"* ~/.agents/skills/
```

### Codex desktop app

The desktop app installs the same way as the CLI above (`codex plugin marketplace add` / `codex plugin add`) — skills sync across the app, CLI, and IDE. Two host settings make the data layer work inside the app's sandbox:

**1. Let the tools reach the network.** The default `workspace-write` sandbox blocks outbound network, so `rdt` / `twitter` / `opencli` calls fail until you opt in. In `~/.codex/config.toml`:

```toml
[sandbox_workspace_write]
network_access = true
```

Keep `workspace-write` and enable only the network — don't switch to `danger-full-access`, which also drops file protections.

**2. Do the one-time credential setup outside the sandbox.** The sandbox blocks writes outside your project, so `rdt login` (it writes your reddit cookie under your home dir) fails when run from inside the app. Run the [Data setup](#data-setup-one-time) steps once in a plain system terminal; each CLI's store is machine-global, and the app reads it back at run time (reads outside the workspace are allowed).

For X higher-fidelity mode, the app doesn't inherit shell env vars and strips `*TOKEN*` vars from subprocesses, so `export TWITTER_AUTH_TOKEN=…` never reaches `twitter`. Either inject them in `~/.codex/config.toml`:

```toml
[shell_environment_policy]
set = { TWITTER_AUTH_TOKEN = "…", TWITTER_CT0 = "…" }
```

or use OpenCLI's browser login (`opencli twitter …`), which needs no env vars. Restart the app after editing `config.toml`.

> **Windows:** the desktop sandbox has known bugs (`danger-full-access` can still run read-only; `elevated` can write outside the workspace). On Windows, run the data CLIs from a system terminal or WSL rather than relying on the in-app sandbox.

### Update

**Claude Code**, in your terminal (restart after to apply):

```
claude plugin marketplace update tigerless-labs
claude plugin update auto-gtm@tigerless-labs
```

**Codex (CLI ≥ 0.144):**

```
codex plugin marketplace upgrade tigerless-labs
codex plugin add auto-gtm@tigerless-labs
```

Direct-clone / symlink installs just need a `git pull` in the cloned repo.

### Use

Trigger it manually (it never runs on its own). Start with `/gtm`, or say what you want:

```
/gtm my Claude Code plugin
Find me topics for my repo — what I shipped this week plus what's hot today
Turn that topic into an X post
Find X posts about AI dev tools I can reply to
```

### Data setup (one-time)

Set a backend up once and auto-gtm reuses it. You're only prompted when one isn't ready. Credentials stay in each tool's own local store, never in this repo.

**Reddit** reads through `rdt-cli`, reusing your logged-in browser session. No OAuth app, API key, or password needed:

```
pipx install 'git+https://github.com/public-clis/rdt-cli.git'   # or install rdt-cli into a venv
rdt login       # extracts your browser's reddit.com cookie
rdt status      # should print authenticated
```

**X / Twitter** works keyless out of the box (host WebSearch floor). For higher-fidelity results, optionally install `twitter-cli`:

```
pipx install twitter-cli            # v0.8.5+
```

On a desktop it reuses your logged-in x.com browser session automatically — no token to paste, the same as `rdt` for Reddit. Only on a headless / SSH box set the cookie manually:

```
export TWITTER_AUTH_TOKEN=...        # x.com → F12 → Application → Cookies
export TWITTER_CT0=...
```

On the Codex desktop app, `export` doesn't reach the tools — set these in `config.toml` or use OpenCLI instead ([Codex desktop app](#codex-desktop-app)).

The builder pulse (top-builder daily posts) needs no setup; it reads a public feed, keyless.

Then trigger any skill:

```
Find the best subreddits to share my Claude Code plugin in
Find Reddit threads about AI GTM tools I can reply to
Write a Reddit post for r/SaaS from this topic
Find X posts about AI dev tools I can reply to
```

## License

MIT — see [LICENSE](LICENSE). Bundled third-party components and their licenses are listed in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
