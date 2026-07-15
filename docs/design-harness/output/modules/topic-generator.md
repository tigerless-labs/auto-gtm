# topic-generator — 生成 X 选题（两类内容）+ 价值闸门

责任：
- 组装 X post topic，来源可为**热点only / session only / 重合**（[topic-source-independence](../../ideas/topic-source-independence.md)）
- **两类内容 + @ 顺序**（[at-ordering](../../ideas/at-ordering.md)）：
  - 分享型：直接 @ **in-session 实体**（distiller 已抽出）
  - 反思型：**定完选题后**用 **agent-reach 搜 X** 找同主题博主/帖子来 @（out-of-session）；**没装则提示用户装**、同时不带 @ 照常出题
- **价值闸门**：没干货就跳过、不硬凑
- 判断性步骤 → 走 **prompt**

边界：
- 只出选题（topic），不写正文/标题/发布
- 输出格式暂不约束（不定固定 schema）

依据：[X 选题风格 idea](../../ideas/x-topic-style-ganhuo-at-creators.md)、上游 distiller 的产物
