# tone-learner — voice from the static exemplar reference

Part of **skill 2: x-content-generator**.

Responsibilities:
- Voice comes from a **maintained static file** `references/tone-examples.md` (verbatim @zarazhangrui posts) plus the **voice rules inlined in SKILL.md** — not live per-run retrieval
- **Learn voice, not opinions**: mimic cadence/structure, never lift the exemplars' takes
- Voice rules: first person, short lines, concrete-first, no em-dashes, every sentence carries real information, and — if the shared thing is already sharp — don't add your own hot-take
- No script, no external tool call

Boundary:
- Supplies the voice; drafting consumes it in content-writer (the shipped skill merges the two into one step, "Learn the voice and draft")

Design change: the earlier design learned tone from **live hot-posts + comments retrieval** (agent-reach / last30days) on the confirmed theme. That was dropped for a **static, maintained exemplar file**. Voice is stable and orthogonal to the topic, so per-run retrieval added cost and noise without improving voice; live retrieval was removed from this skill (agent-reach now only serves the @ search in at-finder). The static exemplars are the "thick context" a thin skill leans on.

Basis: [tone-learning-after-confirm idea](../../ideas/tone-learning-after-confirm.md) (its "after confirm" timing still holds; the live-retrieval mechanism is superseded), `references/tone-examples.md`
