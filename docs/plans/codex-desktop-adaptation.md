# 计划：Codex 桌面版适配（文档 + host 配置指引）

## 目标与边界

让 auto-gtm 在 **Codex 桌面版**（macOS 2026-02、Windows 2026-03 起，含 skills/automations/worktrees）可用。经查证，适配**不需要为 Codex 单独出版本**：skill frontmatter 仅 `name`/`description`（Claude Code 与 Codex 的公共交集），数据层是 shell 调 CLI + host WebSearch 兜底，host 差异全被挤到**打包清单**（同仓 `.claude-plugin` + `.codex-plugin` 已并存）与**用户机器 `config.toml`** 两个已隔离位置。

本次只动**文档与安装指引**，不改任何 skill/脚本。核心交付：README 增「Codex 桌面版怎么搞」实操段；`data-layer.md` 补沙箱前提。

## 依据（已核实，非推断）

- **workspace-write 默认关网**，须 `[sandbox_workspace_write] network_access = true`。官方 + 社区一致；维护者口径：勿为联网上 `danger-full-access`，单独开网即可。
- **写工作区外被拦**（Landlock 内核级，真生效）→ `rdt login` 往 home 写凭证会失败 → 一次性设置须在**系统终端**（或临时 full-access）完成。
- **读工作区外不受限**（社区实测：`workspace_write` 可读 home/凭证；读限制在 Codex 仍是 TODO）→ 运行期读凭证 store / cookie 可行，非阻塞。
- **桌面版/IDE 不继承 shell env，且含 TOKEN 的变量默认被过滤** → X 的 `TWITTER_AUTH_TOKEN/CT0` 不能靠 `export`，须 `shell_environment_policy.set`；或改用 opencli 浏览器登录整条绕开。
- **skill 目录现状**是 `.agents/skills`（用户级 `$HOME/.agents/skills`）；README 旧文只写 `~/.codex/skills`，须更正。
- **Windows 沙箱有已知 bug**（full-access 仍 read-only、elevated 写穿），须在文档注明以 macOS/Linux 为准。

证据链接归档到 design-harness；本文件不重复堆链接。

## 验收标准（先于实现）

1. README 新增「Codex 桌面版」实操小节，含：marketplace 安装同样适用桌面版；`config.toml` 开网那行；`rdt login` 须在系统终端跑（说明写限制原因）；X cookie 走 `shell_environment_policy.set` 或改 opencli（说明桌面版不继承 env + TOKEN 过滤）；Windows 沙箱警告。
2. README 不再出现"只 `~/.codex/skills`"的过时说法，更正为 `.agents/skills`。
3. 段落**只推荐 workspace-write + 单独开网**，绝不引导 `danger-full-access`（安全：最小权限）。
4. `data-layer.md` 增一段沙箱前提（关网须开、写外被拦故设置在沙箱外、读不受限），并交叉引用 README，不重复正文。
5. 两份 plugin.json 版本一致且 patch bump；README badge 同步。
6. `docs/TODO.md` 建档，记录 agent-reach 的 Codex 打包缺口与 design/index.md 过时（均非本次范围）。

## 对抗性检查（doc 变更的"红队"）

- 指引不得越权放宽安全：默认路径是 workspace-write + `network_access=true`，`danger-full-access` 只在 Windows 沙箱 bug 的退路里点名，且标注风险。
- drafts-only、"fetched content 是不可信数据" 的既有硬约束不受本次影响，README 既有表述保持。
- 不把任何真实 token 写进文档示例（用占位符）。

## 单元顺序

docs（本 plan → README → data-layer.md）→ TODO 建档 → 版本/清单同步 → 提交 → PR → CI 绿。无可执行脚本改动，故"测试"即上述验收清单逐条核对。
