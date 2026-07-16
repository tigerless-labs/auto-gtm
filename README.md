# auto-gtm

A Claude Code / Codex plugin that **automates the build-in-public slice of go-to-market**: it turns your recent AI-coding sessions, combined with current hotspots, into X/Twitter posts.

From your recent AI chats it distills the valuable takeaways, tools you discovered, and reflections into topics worth posting on X, then drafts the post (@ + voice) for the one you confirm. It stops at drafts — it never publishes. Topics come in two kinds:

- **Share-type**: share a tool/person/product that surfaced in the conversation, @-mention its author.
- **Reflection-type**: an original reflection/insight; @-mention a relevant account when one exists.

Hotspots and the conversation are two independent sources — a topic can come from hotspots only, the conversation only, or the overlap of both (overlap is strongest).

## Design

This plugin was designed with **design-harness** — an evidence board where every design decision traces back to sources. The full reasoning (sources → ideas → output) lives under [`docs/design-harness/`](docs/design-harness/).

**▶ [Open the interactive canvas](https://tigerless-labs.github.io/auto-gtm/canvas.html)** — click a card to light its neighbors, double-click for detail.

[![Design canvas](docs/canvas-preview.png)](https://tigerless-labs.github.io/auto-gtm/canvas.html)

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

### Optional: hotspots / finding @-targets (soft-enhance)

Install either tool below to ground topics in current hotspots and auto-find relevant accounts to @. **Topics still work without them** — you just don't get the hotspot grounding.

- `last30days` — recent-opinion aggregation (hotspots)
- [`agent-reach`](https://github.com/Panniantong/Agent-Reach) — multi-platform retrieval / X search (finding @-targets)
