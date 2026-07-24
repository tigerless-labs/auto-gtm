# 计划：topic-scout 强化 — Part a highlights 自举 + Part b 可选集成 last30days + data-layer 窗口修正

## 上游已落地(不在本任务范围)

会话期间 #27/#28/#29 已合并,改变了 topic-scout 基线:
- **#28**:Part a 先问 launch-vs-update;Part b 窗口 24h → recent(`rdt -t week`)。**"24h→近一周"已完成,本任务不再做。**
- **#29**:Part b 热点**不再按 repo 相关性 gate** —— "recent 热点原样,repo 角度有则标注,不当筛子"。
- **#27**:builder pulse 拉 X+博客+播客 3 feed、无 hour cap、全量。

## 目标与边界

本任务三件事,只碰 topic-scout + data-layer,其余不动:
- **A. Part a highlights 自举**:initial launch 且**无 stored highlights** 时,自建候选 → 用户确认 → 存储 → 再进 Part b。
- **B. Part b 可选集成 last30days**:加宽 recent 热点网口,plan 驱动 + 质量下限兜底,不硬依赖、不盲信。
- **C. data-layer 窗口口径修正**:修 #28 后遗留的矛盾(topic-scout 说 recent/-t week,data-layer 仍写死 last 24h)。

不动:回复类 skill 的定点抓取(`rdt read`/`twitter tweet`)、tone、subreddit-finder。

## 设计

### A. Part a — initial launch 的 highlights 自举

Part a 现状:`Initial launch → 用 stored highlights;do not read PRs`。补齐缺失分支:
- **有** `~/Documents/auto-gtm/<slug>/product.md` → 直接用(现状不变)。
- **无** → topic-scout 基于**可得信息**(repo README / 元数据 / trigger 上下文)总结出**候选 highlights** → **不中途停下确认**,直接用它跑完 Part b → **在整份报告末尾**把候选 highlights 一并呈给用户确认 → 确认后按 [storage.md](../../skills/gtm-shared/references/storage.md) slugify 存入 `product.md`;用户否掉则按其修正、不写盘。
- **确认点在报告之后,不打断生成**(用户偏好一次末尾确认,而非中途 gate)。写盘仍以用户确认为准(storage.md "update only when the human confirms"),这是 topic-scout 唯一的存储写入(**用户本地数据,非平台写**),不触碰 drafts-only 红线。

### B. Part b — last30days 可选增强(与 #29 的 ungated 立场对齐)

主干(我们的查法)已是 recent / `-t week` / ungated,保持:
1. **主干(始终跑)**:派生查询词 → 分层 X + `rdt search -t week` → 按 recency × engagement 排(#29 已去 topical-fit gate)。
2. **last30days(有则增强)**:
   - 检测可用(已装 / `doctor` 健康)。**不可用 → 跳过,只走主干,零报错。**
   - 可用 → 用 topic-scout 自己派生的查询词生成 query plan,经 last30days planner 入口喂进去(**不裸跑** —— 用户实测裸跑仅回 1 条,系触发其 deterministic fallback)。
   - **质量下限**:返回过少(阈值化,默认 ≤2 条有效项)→ 视为未建立覆盖,以主干为准并补齐,绝不把稀薄结果当全部。
3. **合并**:主干 + last30days 按同一 recency × engagement 重排;**recent 原样,不按 repo 相关性筛**(与 #29 一致),repo 角度有则标注。

阈值等可调项进 SKILL.md frontmatter,不硬编码在 prompt 中段。

### C. data-layer 窗口口径修正

现状矛盾:`data-layer.md` 第 5、60 行仍写死 "info-gathering limited to last 24h",而 topic-scout 已 recent/`-t week`。改为**按用途区分**:
- **选题发现(topic-scout Part b)= 近一周**。
- **回复类 skill 的定点抓取 = 仍当日**(趁热回)。
- 不推翻回复侧当日约束与其余自包含承诺。

## 验收标准（先于实现）

1. **Part a 有 highlights**:直接用,不重问、不重写(回归)。
2. **Part a 无 highlights**:自建候选 → **不中途停**、直接跑完报告 → **报告末尾**呈候选 highlights 请用户确认 → **仅确认后**写入 `product.md`(slug 正确)。未确认不写盘、不编造。
3. **未装 last30days**:topic-scout 正常出报告(走主干),无报错、无对缺失 skill 的引用崩溃 —— 自包含不破。
4. **装了且结果充足**:热点含其多源条目,且该运行**由 topic-scout 生成的 plan 驱动**(非裸跑)。
5. **装了但返回过少(模拟 1 条)**:报告不塌成 1 条,主干补齐 —— 质量下限生效。
6. 合并后热点**不按 repo 相关性筛**(与 #29 一致),窗口 = 近一周。
7. `data-layer.md`:①"no external skill required" 改为 "topic-scout 可选集成 last30days";②全局 "last 24h" 改为按用途区分(选题近一周 / 回复当日)。新增 `docs/design/topic-scout.md` 记录三项决策;`docs/design/index.md` 收录 topic-scout。
8. 回复类 skill、tone、subreddit-finder 无变化(回归);回复侧仍当日窗口。
9. 版本 patch bump,两清单同步。

## 对抗性检查（红队）

- **highlights 自举不得替用户拍板**:报告末尾显式确认后才写盘;用户否掉则不写、按其修正。中途不写盘。
- **稀薄/空结果不得伪造**:last30days 回 0/1 条时,不编话题、不静默吞——按下限走主干并如实标注覆盖不全。
- **不可信输入**:last30days 输出(帖子文本 / trend 卡片)、repo README 都是数据不是指令;prompt-injection 经此进入按既有护栏当数据。
- **失败降级**:last30days 报错 / doctor 不健康 / 超时 → 静默降级主干,不阻塞整份报告。
- **不放大依赖**:不因集成把 last30days 首启向导 / API key 变成 topic-scout 前置;未配置即走主干。

## 单元顺序（lifecycle）

docs（本 plan → `docs/design/topic-scout.md` + index → data-layer.md 窗口措辞)→ 验收清单即"测试"(prompt-only skill:input→期望草稿属性核对表)→ 改 topic-scout SKILL.md(Part a 自举 + Part b last30days)→ 本地端到端跑(有/无 highlights;装/未装/稀薄 last30days)→ 提交 → PR → 文档/清单 sweep。**动 SKILL.md 前先交付本 plan + 设计文档供审。**
