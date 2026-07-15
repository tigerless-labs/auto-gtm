---
tags: [pattern]
---

# content-collector-skill — 社交内容收藏 skill，可复用的 SKILL.md 编排 + 脚本执行架构蓝本

丢链接/截图 → 判平台 → 去重 → 抽正文 → AI 摘要+打标签 → 存飞书多维表格。它本身是**内容归档**工具（输入外部 URL，产出归档记录），**不是选题工具**，但架构是本项目最直接可复用的蓝本。

**六步流水线**：① 触发用渐进式披露（`description` 写明发链接/截图/说"收藏"时主动触发）；② 平台检测 `extract_content.py` 用纯域名路由表，只输出"该用哪个子 skill + CSS selector"，自己不抓；③ 去重 `deduplicate.py` 本地 JSON 缓存（30天TTL/上限1000）+ 域名归一化；④ 调专职子 skill 抽正文；⑤ AI 摘要 + **结构化打标签**（固定 schema：对象×2+场景×1+类型×1+方法×1=5个，独立生成不参考历史池，代码 `validate_tags()` 校验数量、失败重试一次）；⑥ 写库 `save_to_bitable.py` v2.2 **强制走脚本**。

**三个可复用模式**（对"从 session 沉淀选题"直接有效）：
- SKILL.md 编排 + 脚本执行的分工：确定性操作（去重/写库/校验）交脚本，判断性操作（摘要/打标签）交模型 prompt。
- 结构化输出 + 代码校验 + 重试：用固定 schema 约束模型，代码验结构。
- **收回 Agent 自由度防幻觉**：作者踩过模型编造占位符 URL（`http://查看完整内容`）的坑，v2.2 起写入类步骤强制走验证过的脚本，不让模型自由调工具。

原始来源：[github.com/vigorX777/content-collector-skill](https://github.com/vigorX777/content-collector-skill)
