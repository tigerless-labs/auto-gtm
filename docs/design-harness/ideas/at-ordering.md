---
id: at-ordering
type: idea
tags: [topic-design]
---

# Ordering for identifying who to @: in-session entities first, out-of-session @ after the topic (decided)

The human's question: how do we know which bloggers we can @ — after finding the topic or before? What is the order?

Breaking it down, there are **two types of @ sources**, with different orderings:
- **In-session entities (before the topic, already present at the distill stage)**: tools/people/products mentioned in the session → @ directly. This corresponds to **share-type** topics — the entity itself is the core of the topic, so the entity comes first.
- **Out-of-session related accounts (after the topic, requires external search)**: in **reflection-type** topics, the related bloggers are often not in the conversation → you need the topic/insight first, then go to X to search for bloggers/posts on the same subject to @. The topic comes first.

**Decided (by the human)**: adopt a hybrid —
- **Share-type**: in-session entities first; the tools/people/products extracted at the distill stage are @-ed directly.
- **Reflection-type**: do an **out-of-session @ search** after the topic — once the topic/insight is set, use [agent-reach](../sources/skills/agent-reach.md)'s X channel to search for bloggers/posts on the same subject to @ (agent-reach is good at precise X retrieval / reading the timeline; last30days is sentiment aggregation and unsuitable for finding specific accounts). If agent-reach is not installed, **prompt the user to install it** and meanwhile still produce topics without the @.

The two types each follow their own ordering, with no unified before/after. Related: [X topic style](x-topic-style-ganhuo-at-creators.md).
