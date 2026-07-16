# at-finder — resolve the @ account for the confirmed topic

Part of **skill 2: x-content-generator**.

Responsibilities:
- Use the handle if the user already gave it (e.g. lifted from the **source URL** of a share)
- Otherwise **search X via agent-reach** for an account to @; if agent-reach isn't installed, prompt to install and continue without the @
- If still unknown, **skip the @** (a wrong @ tags a real person — worse than none)
- Runs only for the **confirmed topic**

Boundary:
- Resolves the @ only; voice and drafting are downstream

Design change: the old **`x_handle_map` static table was dropped** — handles now come from the source URL or an agent-reach search. The share/reflection kind-split no longer drives a separate @ path.

Basis: [at-ordering idea](../../ideas/at-ordering.md), the confirmed topic from [topic-generator](topic-generator.md)
