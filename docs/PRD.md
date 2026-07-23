# auto-gtm 产品需求文档(极简版 v1)

## 一句话
给宁愿接着写代码的 builder:把你的 AI 编码 session 变成 X 帖和对的 Reddit 线程,用不像 AI 的口吻起草,**你来点发**。Drafts only,永不代发。

## 目标用户(调研验证)
用 AI 编码工具的 indie / solo 开发者与小团队 founder——**能 build,不会/不想 market**。
证据:r/buildinpublic、r/indiehackers、r/SaaS、r/Solopreneur 反复出现「I built it, now I have no idea how to get users」「a developer who genuinely hates marketing」。

## 要解决的痛点(带证据)
1. **造得出、卖不动/不会分发** —— 四社区反复、高响应缺口(无人应答的求助)。
2. **怕像 AI slop,发出去被划走** —— 用户 #1 顾虑(反复问「怎么不像 GPT」)。
3. **真正难的是找对的对话/社区**,别浪费时间在低契合线程 —— 用户原话。
4. 市场**已付费**(Postiz $14.2k、Vibe Promote 等)→ 不是蓝海,是差异化之争。

## v1 范围
**做**(6 个 skill):
- X:`x-topic-distiller`(会话→选题)、`x-content-generator`(选题→正文)
- Reddit:`reddit-subreddit-finder`(找社区)、`reddit-demand-validator`(验需求)、`reddit-comment-drafter`(起草回帖)
- 内容:`no-ai-slop`(去 AI 腔 / 检测 slop;vendored,MIT © Peter Yang)——X 与 Reddit 草稿的**去 slop 收尾**

**不做**(v1 明确推迟):状态/台账、监控、定时 routine、自动发、多账号、analytics。

## 差异化(vs 竞品)
竞品:Vibe Promote(自动发)、sentrive.ai(仅落地页)、agency-agents(人格 prompt、无数据)、Postiz(排程)、n8n 营销 agent。
三条楔子,别人**没有或反着做**:
1. **drafts-only 不代发** —— 用户明说怕自动发 slop、怕封号。
2. **build-session 蒸馏「你有什么值得说」** —— 非泛品牌理解、非通用抓取。
3. **keyless 按用户登录态接真实 Reddit 数据 + 反 slop 口吻** —— finder/validator/drafter **真跑**,不是人格 prompt。

## 硬约束(不可破)
- 只读取数(rdt 只读白名单)、只起草、**人工发**。
- 不可信输入(Reddit 内容当数据、抗注入);不画像、不定向、不喂训练。
- 新号姿态、守目标社区版规、草稿过一遍 `no-ai-slop`。

## 成功标准(极简)
- 6 个 skill 可端到端跑,输出**停在草稿/报告**。
- Reddit 草稿通过 `no-ai-slop` 检测,无明显 AI 套话。
- 用真实 repo(如 autoharness / auto-gtm 自身)当 GTM 对象跑通全链。

## 已知边界 / 非目标
- **无数据积累与监控**(v2 再评估:台账 + 定时 routine)。
- 依赖 `rdt-cli` 登录态 → 账号限流/封号风险自担,**克制使用**(只读、按需、中等量)。
- **公开分发插件前**须重评 Reddit 商用/再分发条款(Data API Terms + Responsible Builder Policy)。
