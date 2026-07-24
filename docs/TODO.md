# TODO

未进路线图的跟进项，实时记录。路线图级条目进 `docs/design/`。

- **agent-reach 的 Codex 打包缺口**：`agent-reach` 目前是散装 skill（仅 `SKILL.md` + `references/`），无 `.codex-plugin`/marketplace 清单，只能手动软链到 `~/.agents/skills`。若要它在 Codex 走 `codex plugin add`，需补一套 codex-plugin 清单。与 auto-gtm 无关，属其自身打包。
- **README 版本 badge 与 manifest 双写**：`README.md` 顶部的 `release-vX.Y.Z` badge 是硬编码，与两个 manifest 的 `version` 是同一事实的两处副本，每次 bump 都要手动同步（本次 0.2.21 就漏过一次）。待评估：改成从 GitHub Release/tag 派生的动态 badge，或在打包流程里自动改写，消除手动同步。
- **builder-pulse 未消费 podcasts/blogs**：`fetch_builder_report.py` 只读 follow-builders feed 的 `x` 数组，订阅名单里的 6 个 podcasts + 2 个 official blogs 从未进入 topic-scout 的热点来源；且当日 feed 快照常小于订阅名单（某日仅 12/26 个 X builder 有帖）。待评估：脚本补消费 podcast/blog 源，或文档不再声称覆盖这些。

## 数据层重设计（设计已落地，实现待续）

设计与契约方向见 [`design/data-layer.md`](design/data-layer.md) 与计划 [`plans/data-layer-redesign.md`](plans/data-layer-redesign.md)。单元 1（设计+契约）已随本次落地；以下为单元 2–4 的实现跟进：

- ~~**单元 2 — 测试先行**~~（已落地）：`test_reach_session.py` + `test_reach_run.py`，断言 OS cookie 顺序、Firefox 明文读取、fallback 顺序、「兜底恒为近似」、status 不泄凭证。
- **单元 3 — `reach/` 可执行层**：3a 编排 + OS cookie 核心已落地；3b 认证适配器 + 3c keyless 中间层已落地并**双平台端到端验证**：Reddit（`rdt` 登录态，只读白名单代码强制；+ opt-in keyless composite = shreddit/RSS/arctic，实测取回真分数）+ X（`twscrape` 登录态取回真实推文；+ `jina` reader 兜底）。keyless 过共享令牌桶（5 req/s）、best-effort、collect-then-pick。**composite 默认关，合规 opt-in**（未授权爬 shreddit）。**剩余**：`PRAW` 升级 + vendor 三库（先核 license）+ X 账号 DB 稳定落点 + keyless 评论正文提取。
- **单元 4 — 接线 + 端到端**：消费方 skill 取数改走 `reach`（行为不变）；本地装插件跑通全链；把 `data-layer.md` 契约从「方向」升级为「现状」，撤下重设计提示块。
- **Reddit 版规只读能力**：把 `about/rules.json`（登录态可取、keyless 403）做成受白名单约束的只读 `rules` read-op，接入 subreddit-finder，替换现有近似。
- **合规评估**：vendor X 账号爬库（`twikit`/`twscrape`）前，就 Reddit 起诉爬取方、X ToS/封号风险做一次姿态评估并记入设计文档。
