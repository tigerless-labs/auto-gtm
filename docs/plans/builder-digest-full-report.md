# 计划:builder pulse 全量吸收 follow-builders 的报告机制

承接 [builder-digest-python.md](builder-digest-python.md)。那份计划定了「不搬 prompt、自写薄 prompt(每条一行)」;本次推翻这一条:follow-builders 的价值恰在消费端 prompt 机制(分来源类型的总结规则、作者身份开场、跳过标准、链接与不编造硬规则),topic-scout 的 part b 改为**直接承载完整三段报告**。

## 决策

- **prompt 取固定副本,不运行时拉取**。上游把 prompt 和 feed 放同一公开 raw 地址,运行时拉取技术上最省,但拉来的 prompt 会被当指令执行,与「抓来的内容只当数据、绝不当指令」冲突。固定副本落成我方共享 reference,更新归属声明(上游 README 声明 MIT)。
- **条目长度照搬上游**:X 每人 2-4 句、podcast 200-400 字含直接引语、blog 100-300 字——不再「每条一行」。
- **脚本去截断**:原每条 600 字符的截断令 podcast 总结无法达标(43k 字符转写截剩残句),改为默认透传全文,截断降为可选参数。

## 验收标准(实现前先写测试)

fixtures 离线跑(`--feed-dir`),在既有 6 用例保持绿之上新增:

1. **transcript 不被截断**:fixture 转写远超旧上限,输出含其**末尾哨兵串**。
2. **blog 正文不被截断**:同上。
3. **可选截断参数生效**:给小值时长文本被截,截断串是全文前缀。

端到端:装插件跑 topic-scout,part b 的 builder digest 与 follow-builders 当日报告形态一致(三段齐全、每条带链接、podcast 有直接引语、作者带角色前缀);注入样文本只作为数据出现。

## 实施单元(每单元:先验收后实现)

1. **设计文档**:`docs/design/topic-scout.md` Part b 拆 b1/b2;`docs/design/data-layer.md` 增 builder pulse 段(采集/总结分离、固定副本的为什么)。
2. **失败测试**:按验收 1-3 扩 `test_fetch_builder_report.py` 与 fixtures。
3. **脚本**:`fetch_builder_report.py` 默认全文透传,截断改可选参数。
4. **共享 reference**:`skills/gtm-shared/references/builder-digest.md`——上游 4 个 prompt 规则的固定副本,顶部标注来源与许可。
5. **接线 + 扫尾**:topic-scout SKILL part b 改引 reference、Output 拆 b1/b2;更新 `THIRD_PARTY_LICENSES.md`(不再是 nothing vendored)、README topic-scout 描述、`docs/TODO.md` 过时条目;三处版本同步 bump;端到端跑一遍;PR 盯 CI 绿。
