---
title: 文档处理与 RAG 完整正文（原文摘要）
type: source
sources: [raw/rag-total.md]
updated: 2026-11-13
summary: 十九章 RAG 总纲的压缩摘要：定义与适用、七步链路与离线六环节、解析与分块九策略、Embedding 与向量库、混合检索与重排、上下文组装与生成、多轮与评估、成本与高级形态、生产化与安全、排查与选型。
---
# 文档处理与 RAG 完整正文（原文摘要）

原文是一份十九章的模块唯一正文（1233 行），定位「每个标题下写满机制、参数、代码与坑」。本页按章节压缩成判断句，机制细节落在 [[concept/rag-pipeline]]、[[concept/hybrid-retrieval]]、[[concept/rag-production]] 与各检索形态实体页。^[raw/rag-total.md]

## 一、RAG 是什么

RAG = 检索 + 增强 + 生成三个动作，不是模型也不是框架，而是系统组装方式：模型不变，把「它该知道什么」从参数搬到每次调用的上下文里。传统大模型三道坎（知识过时、幻觉、知识盲区）用同一个解法：把依据放进提示词，让模型做阅读理解而非回忆。^[raw/rag-total.md]

RAG 带来五个变化：事实性提高、可溯源、更新即生效、成本低于微调、私有数据不出库。^[raw/rag-total.md]

与微调、长上下文的分工：知识频繁变、要给出处、文档在外部 → RAG；要固定语气与输出结构 → 微调；文档不多一次读完 → 长上下文。判断三问即「变不变、要不要出处、多不多」。三者可叠加，最常见组合是 RAG 供事实、微调管风格。典型误用是拿 RAG 做风格约束、拿微调灌知识、拿长上下文替代检索。^[raw/rag-total.md]

不适用场景：实时交易决策（延迟不可控）、完全无结构无标注语料（切不准）、要求 100% 准确的合规结论（检索只能降低风险，不能担保）。^[raw/rag-total.md]

三条架构路线：2-Step RAG（固定两步，控制力高、延迟稳定）、Agentic RAG（检索是工具，次数不定）、Hybrid RAG（查询增强 + 检索验证 + 答案验证）。**起步一律 2-Step**，因为只有它能在同一批输入上做可归因的对照；Agentic 的检索次数不固定，做对照时说不清是策略好还是多搜了几轮。^[raw/rag-total.md]

## 二、完整链路

三个模块：检索器、增强器、生成器，失效表现分别是「无依据/旧版本」「挤掉指令或上下文不足」「自由发挥」。在线七步：查询处理 → 相似度检索 → 重排（可选）→ 上下文组装 → 生成 → 后处理（可选）→ 返回并附来源。^[raw/rag-total.md]

离线六环节：加载 → 解析 → 清洗 → 分块 → 向量化 → 入库建 ANN 索引。**解析与分块决定检索上限**，后面重排只能在已入库候选里挑。三种相似度度量（余弦 / 欧氏 / 内积）必须与建索引时一致。^[raw/rag-total.md]

## 三至六、解析、分块、Embedding、向量库

解析：模型看到的是文本不是 PDF，解析错则无法补救；六种输入各有工具（MinerU 版面模型、PaddleOCR、pdfplumber/PyMuPDF、多模态描述）；表格要单独保护（整表成块或按行切重复表头、表名列名写进块文本）；清洗三件事（去页眉页脚、合并断行、保留结构标记）；中文四特殊（分词边界、全角半角、无标点、跨页表）；验收三条。^[raw/rag-total.md]

分块必须切的三个理由；九种策略（固定长度、滑动窗口、递归字符、语义、按结构、父子文档、Small-to-Big、分层索引、Agentic 分块）；参数经验值 chunk 512–1024 token / overlap 50–100 / 每块 ≥100 字 / 必带元数据；按文档类型分组配参数；五个坑。^[raw/rag-total.md]

Embedding：两端必须同模型同预处理；选型五看（MTEB Retrieval 列、语言、维度 768–1024 平衡、最大输入匹配块大小、部署方式）；领域失配比维度不足更常见，用二十对「问题—应命中片段」的 Top-5 命中率判断；微调三元组与整库重建代价；增量更新三法，**只加不删是最常见错误**。^[raw/rag-total.md]

向量库：七个库先看规模、再看运维、最后看基础设施复用；五种索引（Flat / IVF / HNSW / PQ / DiskANN）；HNSW 三参数中线上只调 `ef`；分区与标量过滤要先过滤再检索；现实建议单机 Chroma/FAISS、生产 Milvus/Qdrant、已有 Postgres 用 pgvector。^[raw/rag-total.md]

## 七至八、检索与重排

三种召回与 BM25 三变量（idf / k1 / b）；中文必须先分词且补专有词。融合三种、RRF 的 k 不是准确率旋钮；两路不设阈值会让候选被噪声撑满。查询侧四种加工判断顺序：改写 → 拆分 → HyDE。多库隔离三档。关键词五法（TF-IDF / BM25 / ES / SPLADE / ColBERT）的取舍。四段流程 topM → topN → RRF topP → Rerank topK；四组对照实验设计（只向量 / 只 BM25 / RRF / 叠 Rerank，固定其余变量，top-k 跑 3/5/10 三档）。详见 [[concept/hybrid-retrieval]]。^[raw/rag-total.md]

重排：一维只回答像不像、二维才回答对不对；双塔/交叉/迟交互三种结构；流程 100 → 20 → 5；模型四选。**召回没捞到的重排救不回**，多跳问题单条打分不够。^[raw/rag-total.md]

## 九至十、组装、生成与多轮

组装四件事（位置、体积、编号、多样性 MMR）；U 型注意力效应把高分块交替放首尾；预算比例（片段 ≤ 一半、历史 ≤ 四分之一）；提示词四条规则；**拒答与召回是一对**，按置信度分三层；生成侧四种优化。多轮失效源于「它」本身歧义，工程默认先改写独立查询，状态记三样，超五轮就压。详见 [[concept/rag-pipeline]]。^[raw/rag-total.md]

## 十一、评估

必须分两段评。五个核心指标（Context Precision / Recall / Relevancy、Faithfulness、Answer Relevancy）；RAGAs 四字段；四种评估方式；数据集 20–50 条分常规/边界/对抗三组，**没有无答案样本就测不出拒答**，调参与测试样例分开。指标与人工成本的切分见 [[answers/answer-rag-eval-metrics]]。^[raw/rag-total.md]

## 十二、性能与成本

四个瓶颈：查询向量化 → ANN 检索 → 重排 → 生成；**绝大多数「RAG 很慢」瓶颈在生成**。降本顺序：减注入块数 → 换小模型 → 才考虑缓存与蒸馏。^[raw/rag-total.md]

## 十三、高级形态与检索范式

五种增强：HyDE、Self-RAG（六种标签，少做无用检索但多轮判断延迟上升）、LongRAG（大块 4K–8K）、GraphRAG、多模态 RAG、Agentic RAG。六种检索形态按「理解在写入端还是查询端」一条轴排序，见 [[concept/retrieval-paradigm]]。^[raw/rag-total.md]

| 小节 | 落到的页 |
|---|---|
| GraphRAG 构建两阶段、局部/全局检索、四个工程难点 | [[entity/graphrag]] |
| 文档树导航（节点只存三件事、模型主导多步阅读、只适合章节清晰文档） | [[entity/document-tree-navigation]] |
| LLM-Wiki 三层（raw/wiki/schema）三动作（ingest/query/lint）与规模化难点 | [[entity/llm-wiki]] |
| Contextual Retrieval：位置说明 50–100 token，失败率 5.7%→3.7%→2.9%→1.9%，成本 $1.02/百万 token，靠 prompt caching | [[entity/contextual-retrieval]] |
| LightRAG：节点边集并集更新，重建口径 1,399 万 token，四领域胜率 54.8/52.0/52.8/49.6 只是几乎打平 | [[entity/lightrag]] |
| OpenViking：`viking://` 下 resources/memories/skills，两层摘要，AGPL-3.0，未公开十万级延迟 | [[entity/openviking]] |
| 成本三数（<200,000 token 不做 RAG；281 分钟建图；全局查询 20 秒起）与三步判定 | [[concept/retrieval-selection]] |

^[raw/rag-total.md]

融合四条路：向量找入口图做扩展、向量定位文档树导航深读、按知识稳定性分工、**Wiki 反哺其他模式（整理过的 Markdown 建向量库优于原始 PDF，收益最快）**。治理代价：同一条知识在四种结构各存一份，源或权限一改四处同步失效。^[raw/rag-total.md]

Ontology 是换一层而非演进线第三代：通用本体给建模能力，运营本体分语义与执行；动作可执行取决规则、实现、权限、底层支持四件事；两类 MCP 面向不同人群且「改结构」与「执行动作」须分别授权。详见 [[concept/ontology]]。^[raw/rag-total.md]

## 十四至十六、生产化、安全、排查

索引与查询分离；四条降级（检索挂降级纯生成并声明无引用、重排超时跳过精排、重建双版本切流量、trace 回查）；监控四条曲线联合判读（命中率跌+拒答涨=召回坏了；命中率正常+拒答涨=提示词或阈值改坏）。安全四道边界与入库/输出两处脱敏、审计日志本身也要脱敏。五个误区与排查顺序（先检索、再生成、最后组装）。详见 [[concept/rag-production]]。^[raw/rag-total.md]

## 十七至十九、框架、实验与文件地图

框架选型口诀：学习与做对照选 LangChain/LlamaIndex，交付选 Dify/MaxKB，解析难就上 RAGFlow；换框架不改原理，只改写代码的方式。^[raw/rag-total.md]

实验状态：未跑。方向池 D04 混合召回（Recall@k 分精确词/语义改写统计）、D05 检索重排（nDCG@k、证据命中率、额外时延）、D06 结构切分（证据完整率、引用定位正确率、索引体积）、D07 图谱辅助（多跳覆盖率、无关扩展比例）。共同口径：固定测试集与模型版本，每轮只切一个变量，收益与代价一起记。^[raw/rag-total.md]

文件地图：本文是模块唯一正文；框架与产品手册归 AgentHarness 手册。原件 `RAG 检索增强生成技术.md`（1968 行）、`RAG技术深度实战.md`（942 行）、`从0到1搭建RAG系统.md`（115 行）已并入本文并删除，未保留的只有行业案例罗列、技能树、发展展望与公众号推广内容。^[raw/rag-total.md]
