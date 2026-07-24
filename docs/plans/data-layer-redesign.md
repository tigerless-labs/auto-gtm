# 计划：数据层重设计（主流方案 + OS 匹配 + 精简 fallback）

## 背景与动因

现有数据层是「散文契约叫 agent 直呼裸 CLI」：X 走 `twitter-cli`，Reddit 走 `rdt` 单路、无兜底、无体检。三点问题：

1. **押错了赌注**：`rdt` 上游 2026-03 停更；契约把 keyless 说成「Reddit 无此路」，而 2026-05-28 Reddit 官宣弃用未认证 `.json`（并点名 RSS 下一个），把 keyless 判了死刑——但**认证路径不受影响**。
2. **不是主流件**：2026 开源主流已收敛到「认证库」——X 用 `twikit`/`twscrape`，Reddit 用 `PRAW`（实时）+ Arctic Shift（历史）。我们用的 `twitter-cli`/`rdt` 是小众成员。
3. **没有 OS 匹配**：认证要浏览器 cookie，而各 OS 取法不同（Windows Chrome v20 应用绑定加密合法工具取不了），契约没交代。

方向：**认证优先，keyless 只当 best-effort 兜底**；用可 vendor 的主流库替换小众 CLI；OS 差异集中在「从哪个浏览器取 cookie」一处。详见 [`../design/data-layer.md`](../design/data-layer.md)。

## 边界与不变量

- **只读、drafts-only、按用途的时窗**（选题回看约一周；回帖当日）——不变。
- **每用户自带登录**，凭证只留在各库自己的本地库，绝不进仓库/草稿/日志——不变。
- **合规红线**：Reddit 正起诉爬取方；X 账号爬取违反 ToS 且有封号风险。只读、低频、自带登录是可辩护姿态；**绝不集成 stealer 类 v20 破解**。
- keyless 从「基线」降级为「best-effort 兜底」，用时声明数据为近似。

## 单元与验收（文档先于测试，测试先于代码）

### 单元 1 — 设计与契约（本 PR）
- **验收**：
  - `docs/design/data-layer.md` 落地：两级链（认证主路 → keyless 兜底）、OS cookie 矩阵、三步 fallback、库选型与 vendor 策略、合规红线；`docs/design/index.md` 链接并标为取数权威。
  - `data-layer.md` 契约加「重设计方向」区并指向设计文档；修正与 2026 现状冲突的措辞（keyless 现状、Reddit 认证路仍成立）；现有可运行指令保持不变（不破坏在跑的 skill）。
  - `rdt-readonly.md` 修正「必须 rdt / 匿名 403 即必须登录」的过时框定；补 2026-05 keyless 死亡与 RSS 待宰的能力注记；把 `rdt` 定位为「Reddit cookie 会话」的一种实现。
  - `docs/TODO.md` 记录单元 2+ 的实现跟进；两个 manifest patch 版本号。

### 单元 2 — 测试（先写失败测试）
- **验收**：`reach/` 的取数入口与 OS-aware cookie 取用有 fixture 测试——断言 fallback 顺序（认证→兜底）、OS 分支选择、以及「兜底时标注近似」这一不变量；红队用例覆盖注入与私据泄漏。用 fixtures，不打真实平台。

### 单元 3 — 可执行数据层 `reach/`
- **3a 编排 + OS cookie 核心（已落地）**：`reach/session.py`（OS-aware cookie：Firefox 全平台明文读取 / Chromium mac+Linux 委托 / Win-Chrome 认栽）+ `reach/run.py`（三步 fallback 契约即代码、degrade 信号、status 不泄凭证）+ `config/data-layer.json`（stdlib 零依赖，故用 JSON 而非 YAML）收纳旋钮。单元 2 测试转绿。
- **3b 认证适配器（已落地）**：`reach/backends.py`。
  - **Reddit（rdt）**：只读白名单**在代码里强制**（写命令直接拒绝、不 shell）、`reddit_available` 读 `rdt status`、`authenticated_available` 兼看 rdt 登录态；本机端到端验证通过（`sub-info` 取回真实订阅数，plan 首选 authenticated）。
  - **X（twscrape）**：`x_fetch` 按 twscrape 真实 API 写（cookie-only 账号 + `async search`，只读只搜、不发帖），fake API 单测覆盖 cookie 接线/查询/归一化/limit。**端到端验证通过**：`session` 从 Chrome 取 `x.com` cookie（source=chromium）→ `x_fetch` 取回真实推文。选 twscrape 的原因：2026-07 实测 `twikit` 2.3.3（最新）挂在 X 反爬握手（`Couldn't get KEY_BYTE indices`），`twscrape` 用同一份 cookie 能出结果——正是「认证库随平台反爬每数周会断」的实例，也印证 keyless 兜底的必要。
- **3b 剩余（待续）**：`PRAW` 升级路；vendor `twscrape`/`PRAW`/yt-dlp cookie 提取的纯 Python 源（先核 license）；给 X 账号 DB 一个稳定的 per-user 落点（现用 per-call 临时库，总用当前 cookie）。

### 单元 4 — 接线与端到端
- **验收**：消费方 skill（`topic-scout` 等）取数从裸 CLI 改到 `reach.run`，行为/触发/停在草稿不变；本地装插件跑通全链；`data-layer.md` 契约从「方向」升级为「现状」。

## 风险

- **平台反爬攻防**：认证库随 X/Reddit 改版每数周会断——vendor 版本需可更新，且保留 keyless 兜底避免整链挂掉。
- **Windows Chrome v20**：合法手段取不了 cookie，认栽（手动粘贴 / 改 Firefox），不碰破解。
- **许可**：vendor `twikit`/`PRAW`/yt-dlp cookies 前核对各自 license 允许随插件分发。
