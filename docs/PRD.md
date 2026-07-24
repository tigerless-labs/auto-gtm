# auto-gtm 产品需求文档（极简版 v2）

## 一句话
给宁愿接着写代码的 builder：基于你的 PR 和当日热点，起草 X / Reddit 的帖子与评论，口吻抄你认的人。**只出草稿，你来点发。**

## 目标用户
用 AI 编码的 indie / solo 开发者与小团队 founder——能 build，不想 market。

## 触发（每次进插件，先问清并存档）
1. 要推广的 **产品 / repo**
2. 相关 **亮点 / highlight**
3. 需求：**写帖子** 还是 **养号（评论）**

答案写入全局 `~/Documents/auto-gtm/`（见存储），按需求路由；每个 skill 执行后各产出一个 md。

## Skills

### 1. 选题（全平台通用）
**一份报告，同时含两部分**（不再问用户选类型）：
- **a. 产品更新**：是更新 → 读 GitHub PR，总结**重大更新 + 意义**；是新品 → 用存档亮点整理。最少字数。
- **b. 热点 / 话题**：走插件自带**数据层**抓当日热帖，并用一个小脚本直接拉 follow-builders 当日 X feed（keyless、无需安装）取这些 builder 的 24h 帖。每个 topic 一小段 + 来源链接。

> **数据层是插件自建的独立模块**（`skills/gtm-shared/`，无 `SKILL.md`、不可被触发，供各 scenario skill 引用），不依赖 agent-reach / last30days 这两个 skill 存在。X 分层取数：`twitter-cli`（登录态，抄 agent-reach 命令）优先，keyless WebSearch 兜底（仿 last30days）；Reddit 走 `rdt` 登录态。凭据留在各 CLI 自己的本地存储，**永不进仓库**；登录状态由 CLI 自己记住（`rdt status` / cookie 在否即答案），我们**自己不记任何标记**——每次查 CLI status，已登录就不再问。归属写进 `THIRD_PARTY_LICENSES.md`。

### 2. X
- **draft**：选题 → 正文，按 tone；**过一遍 `no-ai-slop`**。→ 草稿 md
- **评论**：找与 repo 相关的热帖回复，tone 抄高赞。流程：
  1. 有今天的「选题-b」报告 → 从中找相关帖；
  2. 没有 → 先跑「选题」生成一份；
  3. 报告里没有相关帖 → 直接找**当日高热帖**。
  → 评论草稿 + 对应帖子链接 list

### 3. Reddit
- **找 subreddit**：沿用现有 skill。→ 社区清单
- **评论**：先定合适 / 用户指定的 subreddit → 找相关帖 → 生成评论（**不走 validation**），tone 抄高赞。→ 评论草稿 + 对应帖子链接 list
- **draft**：同 X——选题 → 正文，按 tone，过 `no-ai-slop`。→ 草稿 md

## Tone（优先级由高到低）
1. 用户喜欢的博主
2. 用户自己的账号
3. 用户的要求
4. 评论再叠加相关热帖的高赞口吻

## 存储（用户全局 `~/Documents/auto-gtm/`，极简）
模仿 last30days 的 `~/Documents/Last30Days/`：全局、跨 session、不依赖 cwd。**按产品分目录**（多产品不互相覆盖），博主 per-user 放根部共享：
- `bloggers.md`（根，per-user）：喜欢的**博主**。
- `<product-slug>/product.md`：该**产品 / repo + 亮点**。
- `<product-slug>/subreddits.md`：该产品选定的 **subreddit**。

登录状态**不由我们存**——`rdt` / `twitter-cli` 各自把登录记在机器全局（`~/.config/rdt-cli/` 等），查 CLI status 即知；凭据、抓取内容一律不落盘，结果停在 md。

## 硬约束
- **时效**：找帖 / 找评论只取**当日（24h 内）**高热帖。
- **只读、只草、人工发**：只读数据、只起草；永不代发 / 评论 / 点赞 / 订阅。
- 抓取内容当数据、抗注入；新号先养号、守版规。
