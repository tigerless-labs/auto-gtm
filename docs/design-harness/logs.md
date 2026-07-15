# logs — append-only change ledger (covers both the ideas and output layers)

Convention: each line is `- date · card/doc · action · delta (minimal old → new) · reason`;
record the **delta itself**; once output exists, one line per layer per change;
append only, never rewrite old lines.

- 2026-07-15 · sources/incumbent/lingzao-manual · create · ∅ → 灵造 11-skill 清单+缺口 · 记录被对比的现有产品
- 2026-07-15 · sources/skills/content-collector-skill · create · ∅ → 架构蓝本(6步流水线+3复用模式) · 最直接可复用的实现参考
- 2026-07-15 · sources/skills/distill · create · ∅ → Smart History Processing · 做"读 session"半，产出是摘要非选题
- 2026-07-15 · sources/skills/immortal-skill · create · ∅ → IM聊天记录→人格画像 · 错位参考(来源/产出都偏)
- 2026-07-15 · sources/skills/topic-generators · create · ∅ → wewrite/topic-radar/xhs-ops 集群 · 做"产出选题"半，来源是平台热点
- 2026-07-15 · sources/index · update · 空骨架 → 4 tag 分组 · 投影随卡片重建
- 2026-07-15 · sources/skills/agent-reach · create · ∅ → 16平台取数底座 · 选题外部热度来源候选(广度/原料)
- 2026-07-15 · sources/skills/last30days · create · ∅ → 8源近期舆情 · 选题外部热度来源候选(深度/成品)
- 2026-07-15 · sources/index · update · +external-signal 组(2卡) · 新增选题外部验证来源类
- 2026-07-15 · target · update · 空 → Purpose(对话→选题+结合热点)+6验收项 · 人类设定 target；热度佐证升为核心，边界=只管对话→选题
- 2026-07-15 · target · update · 6验收项 → 4项(删"校验重试"+"收回自由度"；schema 改为"输出格式暂不约束") · 人类精简；不锁输出格式
- 2026-07-15 · target · update · Purpose "一段"→"一段时间"(人类手改) + 钉死 X/Twitter · 平台锁定 X；读取范围暗示为时间窗
- 2026-07-15 · ideas/x-topic-style-ganhuo-at-creators · create · ∅ → X选题风格(干货+@作者+3动作) · 转录人类判断(讨论点1)
- 2026-07-15 · ideas/session-read-range-timewindow · create · ∅ → 读取范围=时间窗+2待定子问题 · 转录人类判断(讨论点2)
- 2026-07-15 · ideas/hotspot-via-external-tools · create · ∅ → 热点走外部工具+1待定子问题 · 转录人类判断(讨论点3)
- 2026-07-15 · ideas/index · update · 1卡 → 3卡(3 tag 组) · 投影随卡片重建
- 2026-07-15 · ideas/x-topic-style-ganhuo-at-creators · update · 单类(分享+@) → 两类(+反思/原创见解) · 人类扩展选题内容类型，自动 merge
- 2026-07-15 · ideas/trigger-manual · create · ∅ → 人手动触发(与content-collector主动触发相反) · 转录人类判断
- 2026-07-15 · ideas/session-read-range-timewindow · update · 2待定 → 已定(平台=仅Claude Code, 粒度=默认24h可覆盖)，剩tool结果待定 · 人类拍板
- 2026-07-15 · ideas/x-topic-style-ganhuo-at-creators · update · 反思型"不必@" → "不强制@,有相关帖子/博主更好" · 人类细化(中途补)
- 2026-07-15 · ideas/index · update · 3卡 → 4卡(+trigger组) · 投影随卡片重建
- 2026-07-15 · output · create · ∅ → 首次装配(system-design): index+system+file-structure+4模块 · 人类发起 assemble
- 2026-07-15 · output/system · create · ∅ → 双mermaid(泳道流程图+模块架构图,含click) · 骨架
- 2026-07-15 · output/modules/{session-reader,distiller,hotspot-fetcher,topic-generator} · create · ∅ → 4模块(责任+边界+依据) · 2待定项在模块内标注
- 2026-07-15 · target · update · Fulfilment map 空 → 4项需求→output文件映射 · 首次装配填充
- 2026-07-15 · ideas/session-read-range-timewindow · update · tool结果待定 → 读+预过滤控token · 人类拍板(读吧)
- 2026-07-15 · ideas/hotspot-via-external-tools · update · 硬/软待定 → 软增强(没装照常出题+提示) · 人类拍板
- 2026-07-15 · output/modules/session-reader · sync · 待定 → 读tool结果+预过滤 · 随idea同步
- 2026-07-15 · output/modules/hotspot-fetcher · sync · 待定 → 软增强 · 随idea同步
- 2026-07-15 · ideas/at-ordering · create · ∅ → @顺序(in-session先行/out-of-session选题后)+推荐混合 · 转录人类新问题，待拍板
- 2026-07-15 · ideas/index,output/index · update · 清2待定标注 +at-ordering条目 · 投影同步
- 2026-07-15 · ideas/at-ordering · update · 待定 → 已定(分享型in-session/反思型定题后搜X) · 人类拍板
- 2026-07-15 · ideas/session-read-range-timewindow · update · 读tool结果 → 不读tool结果(省token) · 人类改回
- 2026-07-15 · ideas/topic-source-independence · create · ∅ → 热点/session独立三来源(热点only/session only/重合) · 转录人类新判断
- 2026-07-15 · output/system · sync · 线性(session→distill→hotspot→gen) → 双来源并行(hotspot+session→合并→gen)，热点排前 · 随idea重画双图
- 2026-07-15 · output/modules/{session-reader,hotspot-fetcher,distiller,topic-generator} · sync · 对齐不读tool结果/软增强/三来源/@分型 · 随idea
- 2026-07-15 · output/file-structure · sync · +search_handles.py(反思型@搜索); read_session 不读tool结果; 顺序热点在前 · 随idea
- 2026-07-15 · ideas/at-ordering + output/modules/topic-generator · update · 反思型@搜索补工具名=agent-reach(X通道) · 人类指出漏写工具
- 2026-07-15 · output/modules/topic-generator + ideas/at-ordering · update · 反思型没装 agent-reach → 提示用户装 · 人类要求一致提醒
- 2026-07-15 · output/file-structure + hotspot-fetcher + system(架构图) · update · 砍 fetch_hotspot.py/search_handles.py，只留 read_session.py；hotspot/@搜索改 SKILL.md 指令委托 · 人类执行脚本精简
- 2026-07-15 · output/file-structure + topic-generator · update · x_handle_map 定为"静态表+agent-reach兜底"(清待定) · 人类拍板
- 2026-07-15 · (实现) skills/x-topic-distiller · create · 设计 → 真 skill(SKILL.md+read_session.py+x_handle_map.md) · 按 output 实现，打包成 CC 插件(.claude-plugin/plugin.json+marketplace.json)+README
- 2026-07-15 · (验证) read_session.py · verify · 实测本会话 · 工具结果零泄漏(WebSearch/浏览器=0)，加 isSidechain 过滤去子agent噪声；注意 CC 的 JSONL 格式官方声明不稳定，脚本 best-effort
