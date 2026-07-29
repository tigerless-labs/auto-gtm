<h1 align="center">auto-gtm</h1>

<p align="center">
  <img src="https://img.shields.io/badge/release-v0.2.34-brightgreen.svg" alt="release" /> <img src="https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex-lightgrey.svg" alt="platform" /> <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license MIT" />
</p>

**auto-gtm** is a Claude Code / Codex plugin that drafts your X and Reddit posts and replies from your PRs and today's hotspots.

From your repo's recent PRs and the day's hot threads it proposes topics; from a topic you pick it drafts posts shaped for X and Reddit; and it finds relevant same-day threads and drafts comments on them. Tone is copied from bloggers you choose or your own account, and for comments, from each thread's top replies. Enter through `/auto-gtm:start` or the `auto-gtm-router` skill.

| | |
|---|---|
| **Built from real work** | Topics come from your GitHub PRs and AI-coding sessions, not thin air. |
| **Rides today's conversation** | Pulls the last 24h of hot threads and builder posts, so you engage while they're live. |
| **Your voice, not AI-slop** | Tone copied from bloggers you like or your own account, then run through no-ai-slop. |
| **Safe by default** | Treats every fetched post as untrusted input, never as an instruction. |
| **Growing** | X and Reddit today, with more platforms over time. |

## The skills

- **topic-scout**: one topic report for any platform, no questions asked. (A) The few product topics most worth posting — a composite launch story built from your highlights, plus what you shipped, from your recent GitHub PRs; it picks rather than listing everything, keeping only the highlights a skeptic outside your repo would still grant you, and what doesn't make the cut isn't shown. (B) Recent hotspots in full — a builder digest (X / blogs / podcasts, summarized per builder and episode) plus other hot topics from your data layer, every item with its source link, never capped. Every run is archived to `~/Documents/auto-gtm/<product>/topics/`, so yesterday's report is still there tomorrow.
- **x-content-generator**: a confirmed topic → an X post drafted in your voice (tone from your favorite bloggers or own account), run through no-ai-slop.
- **x-auto-comment-draft**: finds same-day X posts relevant to your repo → a reply draft per post (tone copied from each post's top replies), with the links.
- **reddit-subreddit-finder**: "which subreddit should I post this in?" → ranked candidates with multi-axis fit, self-promo safety, and a rules summary.
- **reddit-auto-comment-draft**: finds same-day threads in a fitting subreddit → reply drafts (escalation ladder, de-AI'd, new-account posture) plus permalinks. No demand-validation step.
- **reddit-post-drafter**: a confirmed topic → a Reddit post (title and body) in the sub's voice, with an inline rules / self-promo check.

## Quickstart

### Install

**Claude Code**, typed in the Claude Code prompt (the `/` slash commands):

```
/plugin marketplace add tigerless-labs/auto-gtm
/plugin install auto-gtm@tigerless-labs
```

**Codex** (CLI, desktop app, or IDE), run in your terminal:

```
codex plugin marketplace add tigerless-labs/auto-gtm
codex plugin add auto-gtm@tigerless-labs
```

> **On the Codex desktop app**, its sandbox needs one setup step before the Reddit/X tools work. Simplest — paste this to Codex and it installs and configures itself:
>
> ```
> Install auto-gtm and set it up: https://github.com/tigerless-labs/auto-gtm/blob/main/docs/codex-desktop-setup.md
> ```
>
> The manual steps are in [docs/codex-desktop-setup.md](docs/codex-desktop-setup.md).

Older Codex versions without the `plugin add` subcommand can install the skills directly (current Codex scans `$HOME/.agents/skills`; older builds used `~/.codex/skills`):

```
git clone https://github.com/tigerless-labs/auto-gtm
mkdir -p ~/.agents/skills
ln -s "$(pwd)/auto-gtm/skills/"* ~/.agents/skills/
```

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

> **Desktop app**: run these in its integrated terminal (on Windows, PowerShell — not WSL), or just ask Codex to. Restart after.

Direct-clone / symlink installs just need a `git pull` in the cloned repo.

### Use

Trigger it manually (it never runs on its own). Start with `/auto-gtm:start`, or say what you want:

```
/auto-gtm:start my Claude Code plugin
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

**X / Twitter** works keyless out of the box (host WebSearch floor). For higher-fidelity results, optionally install `twitter-cli` and set your cookie once:

```
pipx install twitter-cli            # v0.8.5+
export TWITTER_AUTH_TOKEN=...        # from a Cookie-Editor export of x.com
export TWITTER_CT0=...
```

On the Codex desktop app, `export` doesn't reach the tools — see [docs/codex-desktop-setup.md](docs/codex-desktop-setup.md).

The builder pulse (top-builder posts, blogs, and podcasts) needs no setup; it reads public feeds, keyless.

Then trigger any skill:

```
Find the best subreddits to share my Claude Code plugin in
Find Reddit threads about AI GTM tools I can reply to
Write a Reddit post for r/SaaS from this topic
Find X posts about AI dev tools I can reply to
```

## License

MIT — see [LICENSE](LICENSE). Bundled third-party components and their licenses are listed in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
