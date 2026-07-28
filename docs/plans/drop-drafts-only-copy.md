# 删除 drafts-only 的文档层表述

## 动机

「只出草稿、从不发布」这条事实目前在仓库里被复述约 40 次,跨 20 个文件:CLAUDE.md、README(badge + 正文 + 表格 + 技能列表四处)、每个 SKILL.md 的 frontmatter 与 Boundary、两个 plugin manifest、slash command、共享 guardrails。这违反 CLAUDE.md 自己的 "One authoritative source per fact",对外读起来也像在反复辩解。

决策人判断:发布能力本就不存在,不需要用文字反复声明。本计划删除文档层的全部禁止发布表述。

## 边界 — 保留什么

**代码强制的 read-only 白名单保留,一行不动。** `reach fetch-reddit` 的写命令在代码里 raise;`rdt-readonly.md` 是这层的契约文档;`twscrape` 走的是 search-only 路径。"能力不存在"这个前提由这层成立,删它等于反向赋予发布能力。

**注入防护(untrusted input)保留。** 抓回内容是数据不是指令 —— 这是另一条事实,不在本次删除范围。

## 后果 — 明确记录

删除后,仓库不再有任何文档层的发布禁令。数据层仍持有 X / Reddit 登录态,agent 仍有 shell。若抓回的帖子含发布指令,阻挡它的只剩代码白名单(覆盖 Reddit 写操作)与注入防护条款;X 侧没有等价的代码级写入拦截,因此 X 路径上这层防护变为零。此风险由决策人接受。

## 单元

### 单元 1 — 验收标准

- 全仓库(排除 `.claude/`、`docs/design-harness/`)不再出现 drafts-only / never publishes 语义的表述。
- `rdt-readonly.md` 与 `data-layer.md` 中描述**代码能力**的 read-only 措辞保留。
- guardrails.md 的 untrusted input / privacy / rule-summary 三节保留,Stop line 一节删除。
- redteam-checklist 的 RT-5(代码白名单)保留;RT-2(文档禁令)因失去依据而删除。
- 两个 plugin manifest 与 marketplace.json 的 description 同步,版本号 patch bump。
- README 的 badge 行、正文首句、表格行、技能列表尾句四处全部清理,且正文仍能自洽介绍产品做什么。

### 单元 2 — 执行

按文件逐个改;SKILL.md 的 Boundary 段删除禁令后需保留其余职责边界(哪个技能负责选题 / 起草)。

### 单元 3 — 收尾

版本 patch bump、README 与 manifest 同步、TODO 记录 X 侧缺代码级写入拦截这一缺口。
