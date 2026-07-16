---
tags: [incumbent]
---

# Lingzao user manual — an existing Xiaohongshu/self-media operations skill collection, 11 built-in skills total

Lingzao is a skill plugin pack installed in an Agent (Workbuddy / Claude / Codex, etc.), designed around the Xiaohongshu operations execution chain: diagnose→benchmark→topic→title→cover→publish→review. Triggered by Chinese prompts, it internally routes to the corresponding skill automatically.

**The current 11 built-in skills**: `xhs-account-diagnosis` (account diagnosis), `xhs-note-breakdown` (single-note breakdown), `xhs-benchmark-account-finder` (find benchmark accounts), `benchmark-copy-rewrite` (benchmark copy imitation), `xhs-title-writer` (title design), `xhs-keyword-design` (keyword embedding), `xhs-keyword-to-content-package` (from keyword/link/screenshot/inspiration material → topic + 4-7 page image-text + body), `xhs-cover-lab` (cover), `handdrawn-route-map-card` (hand-drawn card), `xhs-prepublish-check` (pre-publish check), `xhs-postpublish-review` (post-publish review).

**Relationship to this project (the key gap)**: the closest one, `xhs-keyword-to-content-package`, takes as input **ready-made material the user actively feeds in** (keyword/link/screenshot) and produces a topic; but it has **no** capability to "automatically distill a topic from a period of conversation history/session with AI." This is exactly the gap this workspace is deciding on.

Original source: [Lingzao basic usage manual (Feishu, 2026-07-13)](https://my.feishu.cn/docx/Y2HQdj5mzoFx4vxfij3cl9TRnjh)
