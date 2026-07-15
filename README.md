# post-topic-generation

一个 Claude Code 插件：**从一段时间的对话 session 中沉淀出 X/Twitter 选题**，并结合当前热点。

只做"对话 → 选题"的提炼——把你最近和 AI 聊出来的干货、发现的工具、产生的反思，变成值得发到 X 的选题；不写正文、不发布。选题分两类：

- **分享型**：分享对话里冒出的工具/人/产品，@ 其作者。
- **反思型**：原创反思/见解，有相关博主也 @。

热点与对话是两个独立来源，一条选题可以只来自热点、只来自对话、或两者重合（重合最强）。

## Quickstart

### 安装

```
/plugin marketplace add tigerless-labs/post-topic-generation
/plugin install post-topic-generation@tigerless-labs
```

### 使用

在 Claude Code 里手动触发（它不会自动跑）：

```
从最近 24 小时的对话帮我沉淀几条值得发的 X 选题
```

想换时间范围：

```
从最近 3 天的对话想 X 选题
```

### 可选：接热点 / 找 @ 对象（软增强）

装了下面任一工具，选题能结合当前热点、并自动找相关博主 @；**没装也能出选题**，只是不带热度佐证。

- `last30days` — 近期舆情聚合（热点）
- [`agent-reach`](https://github.com/Panniantong/Agent-Reach) — 多平台取数 / X 精准检索（找 @ 对象）
