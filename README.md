# auto-gtm

A Claude Code / Codex plugin that **automates the build-in-public slice of go-to-market**: it turns your recent AI-coding sessions into X/Twitter posts.

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

