# auto-gtm

A Claude Code / Codex plugin that **automates go-to-market** — one skill per scenario × platform. Today it covers **X/Twitter** (turn your AI-coding sessions into posts) and **Reddit community GTM** (find subreddits, validate demand, draft replies). Every skill stops at drafts/analysis — it never publishes, comments, or performs any platform write.

## X/Twitter

From your recent AI chats it distills the valuable takeaways, tools you discovered, and reflections into topics worth posting on X, then drafts the post in your voice for the one you confirm. It stops at drafts — it never publishes. Topics come in two kinds:

- **Share-type**: share a tool/person/product that surfaced in the conversation.
- **Reflection-type**: an original reflection/insight.

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

Older Codex versions without the `plugin add` subcommand can install the skill directly (Codex scans `~/.codex/skills`; newer versions also scan `~/.agents/skills`):

```
git clone https://github.com/tigerless-labs/auto-gtm
mkdir -p ~/.codex/skills
ln -s "$(pwd)/auto-gtm/skills/x-topic-distiller" ~/.codex/skills/
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

Trigger it manually in Claude Code / Codex (it never runs on its own):

```
Distill a few X-worthy topics from the last 24 hours of our conversation
```

Change the time range:

```
Come up with X topics from the last 3 days of conversation
```

## Reddit community GTM

Three manually-triggered Reddit skills — all read-only and drafts-only. They never post, comment, or upvote; you publish.

- **reddit-subreddit-finder** — "which subreddit should I post this in?" → ranked candidates with multi-axis fit, self-promo safety, and a rules summary.
- **reddit-demand-validator** — "is there real demand for X on Reddit?" → matching posts graded by signal strength (Money Talk highest), each with an evidence permalink.
- **reddit-comment-drafter** — give it a thread → reply drafts (escalation ladder, de-AI'd, new-account posture) plus the permalink.

### Reddit data setup (one-time)

These skills read Reddit through `rdt-cli`, reusing your logged-in browser session — no OAuth app, no API key, no password entered:

```
pipx install 'git+https://github.com/public-clis/rdt-cli.git'   # or install rdt-cli into a venv
rdt login       # extracts your browser's reddit.com cookie
rdt status      # should print authenticated
```

Then trigger a skill:

```
Find the best subreddits to share my Claude Code plugin in
Validate demand on Reddit for an AI GTM tool aimed at indie developers
Draft a reply to this Reddit thread: <thread url>
```

