---
tags: [topic-output]
---

# 选题生成类 skill 集群 — 会产出 post topic，但来源是抓平台热点而非对话 session

一批做"选题/爆款打分"的开源 skill，产出正是 post topic（选题+标题），但**来源全是抓平台热点**，不是从你和 AI 的对话里沉淀——占本项目要的"产出选题"那一半。

- **wewrite** — 公众号全流程，含热点抓取、选题评分、素材采集、排版推送：[github.com/imraywang/wewrite](https://github.com/imraywang/wewrite)
- **wechat-topic-radar** — 带"爆款评分引擎"的公众号选题，24h 全网巡逻抓热点 + 按账号人设打分，喂 Top 5 选题+标题：[知乎教程](https://zhuanlan.zhihu.com/p/2026785087346190276)
- **xiaohongshu-ops-skill** — 小红书运营，含"选题灵感 + 知识库沉淀"模块，是集群里最接近本项目场景的（值得看它怎么把沉淀和选题串起来）：[github.com/Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill)

**与本项目的关系**：这一半提供"选题生成 + 爆款打分"的 prompt/schema 参考。核心差别是 input——本项目的 input 是对话 session，不是平台热点流。
