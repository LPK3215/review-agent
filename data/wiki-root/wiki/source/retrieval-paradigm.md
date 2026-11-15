---
title: 检索范式选型：六种形态与理解的时点（原文摘要）
type: source
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-12
summary: 六种检索形态按「理解发生在写入端还是查询端」一轴排序，附成本数字、三步判定流、面试口径与治理要点。
---
# 检索范式选型：六种形态与理解的时点

原文出自公众号「文艺理科生Owen」《别急着上 GraphRAG》，经核实重写。定位是专项层选型对照，机制细节指向「文档处理与RAG总纲」13.4–13.13。

## 核心轴

六种形态的分歧压到一处：**理解在什么时候发生**。写入端＝入库时把理解做完，查询直接读；查询端＝入库只存原文，查询现算。每往写入端移一格，查询便宜一分、错误固化一分、语料变更重建成本涨一分。选型实质是「挑你愿意在哪一端犯错」。^[raw/retrieval-paradigm.md]

| 形态 | 理解时点 | 检索单元 |
|---|---|---|
| 向量 RAG | 查询端 | 片段 |
| Contextual Retrieval | 查询端（索引时补块） | 片段 + 位置说明 |
| GraphRAG | 写入端（预计算摘要） | 关系 |
| LightRAG | 写入端（动态增量） | 关系 + 向量 |
| 文档树导航 | 索引端（结构先行） | 章节 |
| LLM-Wiki | 写入端（理解全部前置） | 概念页 |
| OpenViking | 换一层 | 目录树 |

详见 [[concept-retrieval-paradigm]]。^[raw/retrieval-paradigm.md]

## 六形态一句话

- **向量 RAG**：另存一份可查索引，索引负责找、原文负责读；块一切出来就与上下文断开。NQ 上 626M 参数 RAG 44.5 EM vs 11B 闭卷 T5 34.5。见 [[entity-vector-rag]]。
- **Contextual Retrieval**：索引时给每块补 50–100 token 位置说明；top-20 失败率 5.7%→3.7%→2.9%→1.9%（三者齐上），$1.02/百万 document token。见 [[entity-contextual-retrieval]]。
- **GraphRAG**：抽实体建图、社区预写摘要，治「整体主题是什么」；约 100 万 token 建图 281 分钟，全局查询 20 秒起。见 [[entity-graphrag]]。
- **LightRAG**：并集增量解决 GraphRAG 重建贵；检索 <100 token/次，Overall 胜率 54.8/52.0/52.8/49.6，第四领域是输的。见 [[entity-lightrag]]。
- **文档树导航**：检索单元是章节，多步阅读；只适合结构清晰的长文档。见 [[entity-document-tree-navigation]]。
- **LLM-Wiki**：理解全前置成页面，三层（raw/wiki/schema）三动作（ingest/query/lint）；并发会碎、编译失真、目录有上限。见 [[entity-llm-wiki]]。
- **OpenViking**：虚拟文件系统，知识只是 resources/ 一个目录，换一层而非第七条路线。见 [[entity-openviking]]。

## 三步判定与治理

先数页数（<500 页整库塞上下文，例外是要可审核编译产物则用 LLM-Wiki）→ 再看问题形态（单跳/漏检/整体判断/天天变/跨章节）→ 最后看知识性质（广而新 vs 少而精）。稳妥解是混合：Wiki 命中优先、向量检索兜底，并标注出处类型、指定负责人。详见 [[concept-retrieval-selection]]。^[raw/retrieval-paradigm.md]

## 面试口径要点

30 秒版：先给轴不给清单，每条只说补哪个洞/主要代价/何时选，抛一条硬数字（281 分钟 / 1.9% / 500 页），收尾给三步判据。高频追问：不用 GraphRAG 的两条正当理由；贵在「跑」不在代码；LightRAG 只是打平；Contextual Retrieval 是索引期补丁需报三档降幅；Wiki 与 RAG 不同层；长上下文仍需 RAG；防错误沉淀靠治理与「没人负责别上 Wiki」。^[raw/retrieval-paradigm.md]

## 边界

成本数字来自各自论文与官方博客，非实测；GraphRAG「仓库已进维护模式」一说经核实不成立（未归档、2026-11-09 仍有推送、README 无该声明），故「不上图」不能拿停维护当理由。Karpathy gist 仅为 idea file，「编译器 vs 解释器」是引申表述；LLM-Wiki 一组数字出自 AWS 博客未逐条复算。^[raw/retrieval-paradigm.md]
