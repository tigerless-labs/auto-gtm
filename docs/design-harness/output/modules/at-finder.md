# at-finder — resolve the @ account for the confirmed topic

Part of **skill 2: x-content-generator**.

Responsibilities:
- **Two paths by kind** ([at-ordering](../../ideas/at-ordering.md)):
  - Share-type: look up the in-session entity in the **`x_handle_map` static table** (high-frequency entities use the table); if not found, fall back to **agent-reach X search**; if still not found, skip the @
  - Reflection-type: use **agent-reach to search X** for accounts/posts on the same subject to @ (out-of-session); **if not installed, prompt the user to install it** and continue without the @
- Runs only for the **confirmed topic** — never for every draft

Boundary:
- Resolves the @ only; tone and drafting are tone-learner / content-writer (downstream)

Basis: [at-ordering idea](../../ideas/at-ordering.md), the confirmed topic from [topic-generator](topic-generator.md)
