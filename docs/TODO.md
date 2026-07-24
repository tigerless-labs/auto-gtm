# TODO

未进路线图的跟进项，实时记录。路线图级条目进 `docs/design/`。

- **agent-reach 的 Codex 打包缺口**：`agent-reach` 目前是散装 skill（仅 `SKILL.md` + `references/`），无 `.codex-plugin`/marketplace 清单，只能手动软链到 `~/.agents/skills`。若要它在 Codex 走 `codex plugin add`，需补一套 codex-plugin 清单。与 auto-gtm 无关，属其自身打包。
- **builder-pulse 未消费 podcasts/blogs**：`fetch_builder_report.py` 只读 follow-builders feed 的 `x` 数组，订阅名单里的 6 个 podcasts + 2 个 official blogs 从未进入 topic-scout 的热点来源；且当日 feed 快照常小于订阅名单（某日仅 12/26 个 X builder 有帖）。待评估：脚本补消费 podcast/blog 源，或文档不再声称覆盖这些。
