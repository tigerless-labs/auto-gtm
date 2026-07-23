# Third-Party Licenses

auto-gtm bundles the following third-party open-source components. Their original
license text and copyright notices are preserved in each component's directory.

## skills/no-ai-slop

- **Source:** https://github.com/petergyang/no-ai-slop
- **License:** MIT — Copyright (c) 2026 Peter Yang
- **Included:** `SKILL.md`, `eval.md`, `LICENSE` (vendored verbatim, unmodified)
- **Full license text:** [`skills/no-ai-slop/LICENSE`](skills/no-ai-slop/LICENSE)

A general-purpose content skill that edits drafts into sharper, more human
writing (or detects AI-slop patterns without rewriting). Used in auto-gtm as
the content-polish pass for generated posts and drafts.

## skills/topic-scout/assets/builders.json

- **Source:** https://github.com/zarazhangrui/follow-builders
- **License:** MIT — Copyright (c) Zara Zhang
- **Included:** a trimmed snapshot (handle + name only) of the curated AI-builder
  X list from follow-builders' `feed-x.json`.

Used by `topic-scout` to bias hotspot topics toward the builders the user follows.
The posts themselves are fetched through the user's own data layer (`rdt` /
agent-reach), not from follow-builders' feed — only the curated handle list is vendored.

## last30days (method reference, not vendored)

- **Source:** https://github.com/mvanhorn/last30days-skill
- **License:** MIT — Copyright (c) mvanhorn

`topic-scout` borrows the *approach* — keyless, reasoning-model-planned
multi-platform recency search — but vendors no code from it.
