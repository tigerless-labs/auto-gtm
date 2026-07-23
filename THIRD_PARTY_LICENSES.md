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

## follow-builders (runtime data source, nothing vendored)

- **Source:** https://github.com/zarazhangrui/follow-builders
- **License:** MIT (declared in the upstream README; the repo ships no standalone
  `LICENSE` file, so there is no verbatim license text to vendor) — Copyright (c) Zara Zhang

The data layer's builder pulse (`skills/gtm-shared/scripts/fetch_builder_report.py`)
fetches follow-builders' public daily feed (`feed-x.json`) at runtime and prints a
filtered 24h digest. No file from follow-builders is vendored into this repo — the
feed is read live, keyless, over HTTPS.

## agent-reach (method reference, not vendored)

- **Source:** https://github.com/Panniantong/Agent-Reach
- **License:** see upstream

The data layer's X access ([`skills/gtm-shared/references/data-layer.md`](skills/gtm-shared/references/data-layer.md))
copies agent-reach's concrete `twitter-cli` command set and search retry chain. No
code is vendored; the plugin does not require the agent-reach skill to be installed.

## last30days (method reference, not vendored)

- **Source:** https://github.com/mvanhorn/last30days-skill
- **License:** MIT — Copyright (c) mvanhorn

The data layer's keyless X floor borrows last30days' *approach* — a keyless,
reasoning-model-planned web-search fallback — but vendors no code from it.
