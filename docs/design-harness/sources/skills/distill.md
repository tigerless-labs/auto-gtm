---
tags: [session-input]
---

# Distill / Knowledge Distiller — 最接近"从 AI 对话 session 沉淀"的开源 skill，但产出是摘要非选题

Claude Code skill，专做知识提取。核心特性 **Smart History Processing**：不给具体文本时，自动提炼对话历史里的近期消息——这正是本项目要的"读 session"那一半能力。

**做什么**：五阶段推理 comprehend→extract→restructure→simplify→verify，把凌乱的 thought dump / 会议记录 / 密集技术文本重构成可读、按重要性排序的结构化文档，声称保留 100% 原始信息。附带能力：insight prioritization（最重要的结论前置）、automated context enrichment（补隐含背景）。

**与本项目的关系（半个匹配）**：来源对（AI 对话 session），但**产出错**——它出的是结构化摘要/文档，不是 post topic/选题。要用它就得把它当"读 session"的前半段，后面再接一个选题生成模块。

来源：[mcpmarket 列表](https://mcpmarket.com/tools/skills/knowledge-distiller)（主要托管在 MCP Market，未找到确认的 GitHub 源仓库）。
