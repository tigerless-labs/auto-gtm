# 数据层设计 — 认证优先，keyless 兜底

auto-gtm 取 X / Reddit 数据的取数逻辑权威。契约与命令在 [`data-layer.md`](../../skills/gtm-shared/references/data-layer.md)（skill 侧，承载 how）；本文只讲边界与为什么。

## 为什么这样选

2026 的两个事实定了方向：

- **匿名读大幅收紧，但没全死**。X 2023 锁死 guest 访问；Reddit 2026-05-28 弃用未认证 `.json`（`search.rss` 也已 429 节流）。**但认证路径不受影响**，且 Reddit 的 `svc/shreddit/*` 分片端点 + 单 sub listing RSS + arctic 归档**实测仍 200、带真实分数/评论数**（2026-07 亲测）——只是它们属**未授权爬取**，正是 Reddit 起诉的模式。
- **开源主流已收敛到认证库**：X 用 `twscrape`/`twikit`，Reddit 用 `PRAW`（实时）+ Arctic Shift（历史）。都是「复用登录态」这一家族，纯 Python、可随插件分发。

结论：**押认证做主路**。keyless 分两档：X 的 host WebSearch / jina 是低保真 best-effort 兜底；Reddit 那套 shreddit 富 keyless 虽能跑，但因合规风险**默认关闭、显式 opt-in**（见下）。所有 keyless 数据用时都声明近似。

## 链：认证主路 → keyless 中间层 → WebSearch 兜底

保持精简——主路一条，中间一档 keyless，最后 WebSearch 地板。

- **X**：`twscrape`（主路，登录态）→ `jina` reader（对已知推文 URL 取整推+对话；X 无 keyless 搜索）→ host WebSearch 兜底。`twscrape`/`twikit` 同为主流；2026-07 实测 `twikit` 挂在 X 反爬握手（`KEY_BYTE indices`），`twscrape` 用同一份 `auth_token`+`ct0` 能取回实时结果，故选 `twscrape`。
- **Reddit**：cookie 会话（主路，登录态；有 OAuth 凭证可升级 `PRAW`）→ **keyless composite（opt-in，默认关）** → host WebSearch 兜底。

Arctic Shift 只作 keyless composite 内的分数回填，不单独进链——它是滞后一两月的历史快照，不满足选题回看约一周、回帖当日的时窗。

## keyless composite（Reddit，opt-in，合规风险）

一套匿名富取数：`svc/shreddit` listing（真实 upvote + 评论数）+ 单 sub listing RSS（广度）+ `svc/shreddit/comments`（top 评论）+ arctic（分数回填）。best-effort——每个 probe 失败返回空、不抛，逐级跌落。所有请求过**共享令牌桶（5 req/s，burst 5）**，防并发踩踏端点。

**为什么默认关**：这是对 `svc/shreddit/*` 的**未授权爬取**，正是 Reddit 起诉爬取方（点名 Anthropic）的模式。复用用户自己的登录（rdt/PRAW）更可辩护。故它是**显式 opt-in**，风险摆在用户面前；不 opt-in 时 Reddit 只走登录态 + WebSearch 兜底。

## OS 匹配 — 只在「从哪个浏览器取 cookie」这一处分叉

认证级要一个浏览器 cookie。取法按 OS：

| OS | cookie 来源 | 说明 |
|---|---|---|
| macOS | Firefox → Chromium | 都行；Chromium 需一次 Keychain 授权 |
| Linux | Firefox → Chromium | 都行 |
| Windows | Firefox（自动）；Chrome 手动 | Chrome v20 应用绑定加密，合法工具取不了 |

**规律**：Firefox 全平台通吃（明文库）；Chromium 只在 mac/Linux 自动可取；Windows + Chrome 必须手动导入。Windows Chrome 的破解只有 stealer 类项目能做，**明确不碰**——违背最小权限与 fail-safe。

## Fallback 顺序

沿链逐级跌落：有可用认证会话就用；没有就按 OS 取一次 cookie 建会话；仍不行落到中间 keyless（X 的 jina / Reddit 的 opt-in composite）；再不行走 WebSearch 兜底并声明近似。每档 best-effort——失败返回空、不抛，交给下一档。**collect-then-pick**：判「认证可用」要同时满足「库可导入 **且** 有 cookie」，避免装了但未登录的首选把可用后备遮蔽。不设大 doctor，只保留一行 status 报所经档位与浏览器来源（**绝不含 cookie 值**）。

## 塞进插件（零安装）

`twscrape`、`PRAW`、以及 cookie 提取（yt-dlp 的提取器 + 一段 Firefox 读取）都是纯 Python，随插件分发，装完即用。`OpenCLI` 是桌面 app + 浏览器扩展，塞不进——只当「用户碰巧装了就白捡」的可选增强。

## 与安全护栏的关系

只读、drafts-only、按用途时窗、每用户自带登录——不变。取数在单一入口收口，只读与兜底降级都在这一处发生，便于在唯一咽喉点设护栏。合规上，Reddit 正起诉爬取方、X 账号爬取有封号风险，故坚持只读低频自带登录，且不集成任何破解式取数。
