---
tags: [external-signal]
---

# last30days — recent-sentiment research tool, 8 sources + engagement aggregation (depth + finished product)

A research skill (built into this session, already Ready with 8 sources): dedicated to "what has everyone been saying in the last 30 days." It pulls posts **and engagement** from Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and web, aggregated by topic (the last run for "AI news releases funding controversy" produced 55 items).

**Key difference (vs. agent-reach)**: half as many sources, but it welds **recency (30-day window) + engagement signal + topic aggregation** into the pipeline, working out of the box to directly produce "how everyone sees it." Essentially zero config. Its positioning is an **upper-layer research finished product**, not a data-fetching primitive.

**Relationship to this project (external-signal)**: if the topic skill needs **ready-made recent sentiment/trending signals** to verify "is anyone talking about this topic now, and how trending is it," using it is easier than agent-reach. It likewise supplements the "external validation of topics," not the extraction of topics from the conversation session itself.
