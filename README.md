<h1 align="center">auto-gtm</h1>

<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/tigerless-labs/auto-gtm/main/.claude-plugin/plugin.json&query=$.version&label=release&prefix=v&color=brightgreen" alt="release" />
  <img src="https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex-lightgrey.svg" alt="platform" />
  <img src="https://img.shields.io/badge/output-drafts%20only-blue.svg" alt="drafts only" />
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license MIT" />
</p>

**auto-gtm is a Claude Code / Codex plugin that automates go-to-market for builders who'd rather keep coding** — one skill per scenario × platform. It **scouts** topics from your PRs + today's hotspots, **drafts** X posts and replies and does Reddit community GTM (find subreddits, draft replies and posts), and **polishes** every draft through a no-ai-slop pass. Every skill **stops at drafts** — it never publishes, comments, or performs any platform write.

The wedge: GTM material is **grounded in what you actually shipped and what's being discussed today**, drafted in a voice you chose — **not generated from thin air**. Any marketing request enters through the **`auto-gtm-router`** skill — or type **`/gtm`** — which routes it to the right step and keeps each human checkpoint. On trigger it first asks three things — the **product / repo**, its **highlights**, and **write posts** or **warm up the account** — then routes; all post/comment/topic gathering is limited to the **last 24 hours**.

| | |
|---|---|
| **Built from real work** | Topics come from your GitHub PRs and AI-coding sessions, not thin air. |
| **Rides today's conversation** | Pulls the last 24h of hot threads and builder posts, so you engage where it counts. |
| **Your voice, not AI-slop** | Tone copied from bloggers you like / your own account, then run through no-ai-slop. |
| **Drafts only, safe by default** | Never posts, comments, likes, follows, or DMs; treats every fetched post as untrusted. |
| **Growing** | X and Reddit today, refined iteratively — more platforms rolling out over time. |

## The skills

- **topic-scout** — one topic report for any platform: (a) what you shipped, summarized from your recent **GitHub PRs**; (b) today's relevant **hotspots**, from your data layer + a curated builder list. One paragraph + source link per topic.
- **x-content-generator** — a confirmed topic → an X post drafted in your voice (tone from your favorite bloggers / own account), run through no-ai-slop.
- **x-auto-comment-draft** — finds same-day X posts relevant to your repo → a reply draft per post (tone copied from each post's top replies), with the links.
- **reddit-subreddit-finder** — "which subreddit should I post this in?" → ranked candidates with multi-axis fit, self-promo safety, and a rules summary.
- **reddit-auto-comment-draft** — finds same-day threads in a fitting subreddit → reply drafts (escalation ladder, de-AI'd, new-account posture) plus permalinks. No demand-validation step.
- **reddit-post-drafter** — a confirmed topic → a Reddit post (title + body) in the sub's voice, with an inline rules / self-promo check.

All read-only and drafts-only. They never post, comment, or upvote; you publish.

## Quickstart

### Install

**Claude Code:**

```
/plugin marketplace add tigerless-labs/auto-gtm
/plugin install auto-gtm@tigerless-labs
```

**Codex (CLI ≥ 0.144):**

```
codex plugin marketplace add tigerless-labs/auto-gtm
codex plugin add auto-gtm@tigerless-labs
```

Older Codex versions without the `plugin add` subcommand can install the skills directly (Codex scans `~/.codex/skills`; newer versions also scan `~/.agents/skills`):

```
git clone https://github.com/tigerless-labs/auto-gtm
mkdir -p ~/.codex/skills
ln -s "$(pwd)/auto-gtm/skills/"* ~/.codex/skills/
```

### Update

Refresh the marketplace, then reinstall to pull the latest version.

**Claude Code:**

```
/plugin marketplace update tigerless-labs
/plugin install auto-gtm@tigerless-labs
```

**Codex (CLI ≥ 0.144):**

```
codex plugin marketplace upgrade tigerless-labs
codex plugin add auto-gtm@tigerless-labs
```

Direct-clone / symlink installs just need a `git pull` in the cloned repo.

### Use

Trigger it manually (it never runs on its own) — start with `/gtm` or just say what you want:

```
/gtm my Claude Code plugin
Find me topics for my repo — what I shipped this week plus what's hot today
Turn that topic into an X post
Find X posts about AI dev tools I can reply to
```

### Reddit data setup (one-time)

The Reddit skills read Reddit through `rdt-cli`, reusing your logged-in browser session — no OAuth app, no API key, no password entered:

```
pipx install 'git+https://github.com/public-clis/rdt-cli.git'   # or install rdt-cli into a venv
rdt login       # extracts your browser's reddit.com cookie
rdt status      # should print authenticated
```

Then trigger a Reddit skill:

```
Find the best subreddits to share my Claude Code plugin in
Find Reddit threads about AI GTM tools I can reply to
Write a Reddit post for r/SaaS from this topic
```

## License

MIT — see [LICENSE](LICENSE). Bundled third-party components and their licenses are listed in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
