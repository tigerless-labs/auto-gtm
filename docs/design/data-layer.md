# 数据层设计 — 认证优先，keyless 兜底

auto-gtm 取 X / Reddit 数据的取数逻辑权威。契约与命令在 [`data-layer.md`](../../skills/gtm-shared/references/data-layer.md)（skill 侧，承载 how）；本文只讲边界与为什么。

## 为什么这样选

2026 的两个事实定了方向：

- **匿名时代结束**。X 2023 锁死 guest 访问；Reddit 2026-05-28 弃用未认证 `.json` 并点名 RSS 下一个。**但认证路径不受影响**——登录态与官方 API 照常。
- **开源主流已收敛到认证库**：X 用 `twikit`/`twscrape`，Reddit 用 `PRAW`（实时）+ Arctic Shift（历史）。都是「复用登录态」这一家族，纯 Python、可随插件分发。

结论：**押认证，不押 keyless**。keyless 从基线降为 best-effort 兜底——它随时可能被平台掐断，只用来保证「永不 dead-end」，用时声明数据为近似。

## 两级链

每个平台就两级，外加一个可选升级——不搞多层多后端。

- **X**：`twscrape`（主路，登录态）→ keyless 兜底（host WebSearch）。`twscrape`/`twikit` 同为主流；2026-07 实测 `twikit` 挂在 X 反爬握手（`KEY_BYTE indices`），`twscrape` 用同一份 `auth_token`+`ct0` 能取回实时结果，故选 `twscrape`。
- **Reddit**：cookie 会话（主路，登录态）→ keyless 兜底（host WebSearch）；有 OAuth 凭证时可升级到 `PRAW`（最稳）。

Arctic Shift 不进链——它只有滞后一两月的历史数据，不满足选题回看约一周、回帖当日的时窗；需要历史时单独取。

## OS 匹配 — 只在「从哪个浏览器取 cookie」这一处分叉

认证级要一个浏览器 cookie。取法按 OS：

| OS | cookie 来源 | 说明 |
|---|---|---|
| macOS | Firefox → Chromium | 都行；Chromium 需一次 Keychain 授权 |
| Linux | Firefox → Chromium | 都行 |
| Windows | Firefox（自动）；Chrome 手动 | Chrome v20 应用绑定加密，合法工具取不了 |

**规律**：Firefox 全平台通吃（明文库）；Chromium 只在 mac/Linux 自动可取；Windows + Chrome 必须手动导入。Windows Chrome 的破解只有 stealer 类项目能做，**明确不碰**——违背最小权限与 fail-safe。

## Fallback 顺序

三步，统一：有可用认证会话就用；没有就按 OS 取一次 cookie 建会话；仍不行就走 keyless 兜底并声明近似。不设大 doctor，只保留一行 status 报「认证 OK / 走兜底」及所经浏览器来源。

## 塞进插件（零安装）

`twscrape`、`PRAW`、以及 cookie 提取（yt-dlp 的提取器 + 一段 Firefox 读取）都是纯 Python，随插件分发，装完即用。`OpenCLI` 是桌面 app + 浏览器扩展，塞不进——只当「用户碰巧装了就白捡」的可选增强。

## 与安全护栏的关系

只读、drafts-only、按用途时窗、每用户自带登录——不变。取数在单一入口收口，只读与兜底降级都在这一处发生，便于在唯一咽喉点设护栏。合规上，Reddit 正起诉爬取方、X 账号爬取有封号风险，故坚持只读低频自带登录，且不集成任何破解式取数。
