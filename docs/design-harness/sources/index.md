# sources — evidence cards (grouped under tag headings; projection regenerated with the cards)

## incumbent: the incumbent product being compared, used to locate the gap
- [Lingzao user manual](incumbent/lingzao-manual.md) — 11 built-in skills, missing exactly the one for "distilling topics from a conversation session"

## pattern: reusable architecture blueprint
- [content-collector-skill](skills/content-collector-skill.md) — SKILL.md orchestration + script execution; structured output+validation+retry; reclaim the Agent's freedom to prevent hallucination

## session-input: does the "read conversation session / distill" half, but the output is not a topic
- [Distill / Knowledge Distiller](skills/distill.md) — Smart History Processing automatically reads conversation history, produces a structured summary
- [immortal-skill](skills/immortal-skill.md) — distills a persona profile from external IM chat logs

## topic-output: does the "produce a post topic" half, but the source is scraped platform hotspots
- [topic-generation skill cluster](skills/topic-generators.md) — wewrite / wechat-topic-radar / xiaohongshu-ops-skill

## external-signal: supplements topics with external trending/data (external-validation source for topics, not extracted from the conversation)
- [Agent-Reach](skills/agent-reach.md) — 16-platform general data-fetching base, breadth+raw material, strong on domestic platforms
- [last30days](skills/last30days.md) — 8-source recent-sentiment research, depth+finished product, built-in 30-day window+engagement

## downstream-publish: does the "publish" half after the body exists (out of this skill's scope, adjacent link in the chain)
- [x-article-publisher-skill](skills/x-article-publisher.md) — one-command Markdown → X Articles draft via browser automation, draft-only (834⭐)
