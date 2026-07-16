---
id: tone-learning-after-confirm
type: idea
tags: [post-confirm]
---

# After the human confirms a topic: learn the tone from hot posts and comments (decided)

**The human's judgment**: add a new step to the pipeline. Once the human **confirms which topic** to go with (picks one from the drafts), the agent searches for **hot posts and their comments on the same theme** and studies them to **learn the tone/voice** for that topic.

Breakdown:
- **Trigger**: only after the human explicitly confirms a topic — not for every draft (that would burn tokens on topics that get discarded).
- **What to fetch**: high-engagement posts on the same theme + their top comments (comments reveal what the audience responds to, not just what authors write).
- **Tools**: [agent-reach](../sources/skills/agent-reach.md)'s X channel for precise post/comment retrieval; [last30days](../sources/skills/last30days.md) as fallback for aggregated sentiment. Same soft-enhance discipline as [hotspot-via-external-tools](hotspot-via-external-tools.md): if neither is installed, skip + prompt to install.
- **Output**: tone notes (voice, structure, hook patterns, what the comments reward) + 2-3 exemplar posts as reference.

**Boundary stays**: this step produces **tone reference material**, not the post body. Writing the body/title is still out of scope ([target](../target.md)).
