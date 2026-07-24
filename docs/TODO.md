# TODO

未进路线图的跟进项，实时记录。路线图级条目进 `docs/design/`。

- **agent-reach 的 Codex 打包缺口**：`agent-reach` 目前是散装 skill（仅 `SKILL.md` + `references/`），无 `.codex-plugin`/marketplace 清单，只能手动软链到 `~/.agents/skills`。若要它在 Codex 走 `codex plugin add`，需补一套 codex-plugin 清单。与 auto-gtm 无关，属其自身打包。
- **`docs/design/index.md` 已过时**：仍列 `x-topic-distiller`、`reddit-demand-validator`、`reddit-comment-drafter` 等旧 skill 名，与当前 `skills/` 不符，待一次专门的设计文档对齐。
