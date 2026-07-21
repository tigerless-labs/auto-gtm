# 实现计划 — Reddit 工具族三 skill

分支 `feat/reddit-skills`。设计见 `docs/design/reddit/`；本计划只排实现单元与验收，不重复设计事实。

## 前置（已完成）
- 取数层 rdt-cli 已装（`~/.local/bin/rdt` v0.4.2）、已登录态（`rdt status` authenticated）。
- 设计文档层已合入 PR #2。

## 技术决策
- **prompt-only skills，无重脚本**：分类/打分/起草是 LLM 工作；取数经 Bash 调 `rdt`（`--yaml -c` 默认），SKILL.md 指令驱动，不写解析脚本除非必要。
- **只读命令白名单**：`search / read / sub / sub-info / popular / all / user* / export`；禁 `comment/upvote/save/subscribe/logout`。
- **近似信号（能力边界，需在 SKILL.md 注明）**：版规=`restrict_posting`+`submission_type`+`public_description` 近似（rdt 无全文规则）；删帖率=抽样近期帖 `removed` 比例近似。

## 共享引用（一处，三 skill 复用）
- rdt 只读命令契约与输出取用约定
- Reddit 声音与社区规范（反硬广、reddiquette、新号姿态、反-AI 措辞黑名单与 de-ai 过滤）
- 版规前置摘要话术（finder + drafter 共用）
- 停手线与不可信输入护栏话术
- 位置：实现时定，使各 reddit SKILL.md 可相对引用且不被 skill 加载器误认为 skill。

## 构建单元（每单元验收 = 对应设计文档的「验收标准」，此处不复述）
1. **共享引用文件** — 上述四类内容落盘；三 skill 引用之。
2. **subreddit-finder SKILL.md** — 多轴契合度 + 安全轴 + 版规前置 + 定制角度；验收见 `subreddit-finder.md`。
3. **demand-validator SKILL.md** — 四桶 + 响应缺口/势能；按需验证非持续告警；验收见 `demand-validator.md`。
4. **comment-drafter SKILL.md** — 升级梯多版 + de-ai + 新号门槛 + 版规内联；只起草不发；验收见 `comment-drafter.md`。
5. **打包同步** — `.claude-plugin` + `.codex-plugin` 两清单加三 skill；README 更新；版本 patch。
6. **端到端验证** — 三 skill 各用 **autoharness repo** 当题材真实跑一遍：trigger → 取数 → 产出 → 停手；含对抗用例（transcript/帖子注入、代发指令、隐私泄露）。

## 顺序与门槛
U1 先行（其余依赖它）→ U2/U3/U4 可并行 → U5 → U6。每单元过其设计文档验收（含对抗项）才算完成；每绿点提交、推送。
