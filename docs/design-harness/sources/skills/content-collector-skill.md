---
tags: [pattern]
---

# content-collector-skill — a social-content bookmarking skill, a reusable SKILL.md orchestration + script execution architecture blueprint

Drop a link/screenshot → detect platform → dedup → extract body → AI summary+tagging → save to Feishu Bitable. It is itself a **content-archiving** tool (input an external URL, output an archive record), **not a topic tool**, but its architecture is the most directly reusable blueprint for this project.

**Six-step pipeline**: ① trigger via progressive disclosure (the `description` states it proactively triggers when a link/screenshot is sent or "bookmark" is said); ② platform detection `extract_content.py` uses a pure domain routing table, only outputting "which sub-skill + CSS selector to use," it doesn't scrape itself; ③ dedup `deduplicate.py` with a local JSON cache (30-day TTL/cap 1000) + domain normalization; ④ call a dedicated sub-skill to extract the body; ⑤ AI summary + **structured tagging** (fixed schema: object×2+scene×1+type×1+method×1=5 total, generated independently without referencing the historical pool, code `validate_tags()` validates the count and retries once on failure); ⑥ write to the DB `save_to_bitable.py` v2.2 **forced through a script**.

**Three reusable patterns** (directly effective for "distilling topics from a session"):
- The division of labor between SKILL.md orchestration + script execution: deterministic operations (dedup/write-to-DB/validation) go to scripts, judgment operations (summary/tagging) go to the model prompt.
- Structured output + code validation + retry: constrain the model with a fixed schema, validate the structure in code.
- **Reclaim the Agent's freedom to prevent hallucination**: the author hit the trap of the model fabricating a placeholder URL (`http://view-full-content`), so from v2.2 onward write-type steps are forced through validated scripts, not letting the model call tools freely.

Original source: [github.com/vigorX777/content-collector-skill](https://github.com/vigorX777/content-collector-skill)
