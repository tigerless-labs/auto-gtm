---
description: Start the auto-gtm go-to-market flow — orient a marketing request and route it to the right skill (drafts only, never posts).
argument-hint: Optional — what you want to promote (e.g. "my Claude Code plugin")
---

Start the auto-gtm go-to-market flow.

Invoke the **`auto-gtm-router`** skill now and follow it exactly to route this request: **$ARGUMENTS**

- If no target was given above, first ask what they want to promote — a product/project plus a one-line pitch — then route.
- Route by stage, announce "Using \<skill\> to \<purpose\>", and hand off to the matching skill. Do not do the work in this command.
- Keep every auto-gtm rule: read-only data, **drafts only, the human posts**, stop at each human checkpoint, never publish.
