---
id: session-read-range-timewindow
type: idea
tags: [session-input]
---

# Read range: the script reads the CC conversation and filters out tool results (default 24h); when the format changes, let the AI modify the script itself

The input is a conversation over **a time window** (not a single turn). **The main path is the script `read_session.py`** — its key value is to **strip out tool results**, keeping only the human-AI conversation text (saving tokens). Why a script is required: if the agent reads its own context directly, the tool results are already occupying tokens in the context and can't be saved; the script can filter them out before feeding them to the model.

- **Platform**: only supports Claude Code (reads JSONL).
- **Granularity**: default last 24h, overridable.
- **Format risk + response**: CC's JSONL format is officially declared internal/unstable; once it changes and the script reads it wrong, **let the AI modify the script itself** to adapt (the script is short), rather than abandoning the script. See [Distill's Smart History Processing](../sources/skills/distill.md).

- **What to read**: **read only the human-AI conversation text, not tool results** (reverted by human decision). The benefit is a large drop in tokens — tool output is often the largest chunk. The cost is possibly losing some valuable-takeaway sources hidden in tool output (repos/links); accept this trade-off.
