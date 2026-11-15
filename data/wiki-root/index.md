# Wiki Index

> 由代码从页面 frontmatter 重建，勿手改。

## source（6）

- [[source/chroma]] Chroma 的定位、核心概念、嵌入系统、CRUD/查询/过滤 API、持久化与部署、框架集成、实战与选型对比的压缩摘要。
- [[source/flow-control]] 编排模式、错误分层、幂等、检查点与 HITL 的机制总纲，附 D11 断点恢复对照实测数据。
- [[source/kb-rag]] 一份把 RAG 问题清单、六种检索形态速查、解析/切分/Embedding/混合检索/Rerank/引用各环节取舍压成判断句的主题总览，附 ESG-Extractor 与 Yuxi 两项目选型与面试答法。
- [[source/qdrant]] Qdrant 的 Rust 高性能定位、Collection/Point/Payload 数据模型、量化与多向量/稀疏向量、过滤与索引、分布式部署、LangChain/LlamaIndex 集成与同类对比的压缩摘要。
- [[source/rag-total]] 十九章 RAG 总纲的压缩摘要：定义与适用、七步链路与离线六环节、解析与分块九策略、Embedding 与向量库、混合检索与重排、上下文组装与生成、多轮与评估、成本与高级形态、生产化与安全、排查与选型。
- [[source/retrieval-paradigm]] 六种检索形态按「理解发生在写入端还是查询端」一轴排序，附成本数字、三步判定流、面试口径与治理要点。

## entity（9）

- [[entity/chroma]] Apache 2.0 的开源向量数据库，主打「像 SQLite 一样嵌入应用」：内置嵌入、元数据过滤、HNSW 索引，可平滑扩到客户端-服务器部署。
- [[entity/contextual-retrieval]] Anthropic 提出的索引期补丁：给每块补 50–100 token 位置说明，三者叠加可将 top-20 失败率从 5.7% 降到 1.9%。
- [[entity/document-tree-navigation]] 以章节为检索单元、模型自行选章读原文的多步阅读法，专治答案散在相隔几十页多章节的场景。
- [[entity/graphrag]] 把摘要从查询时临场发挥改为索引时预计算：抽实体建图、社区预写摘要，治「整体主题是什么」，代价是建图贵且语料必须静态。
- [[entity/lightrag]] 针对 GraphRAG 重建贵的问题，用节点/边并集做增量更新；宏观能力来自查询时双路打图，对 GraphRAG 仅打平。
- [[entity/llm-wiki]] 理解全在入库时做完、产物是页面而非索引的知识组织形态；三层三动作，四种失败模式（并发碎、编译失真、查询不一定便宜、目录有上限）。
- [[entity/openviking]] 以 viking:// 虚拟文件系统组织 Agent 全部上下文（resources/memories/skills），检索先定位目录再下钻；是换一层而非第七条检索路线。
- [[entity/qdrant]] Apache 2.0 的开源向量数据库，Rust 编写、生产向：payload 过滤与向量搜索深度集成，支持量化、多向量、稀疏向量与地理过滤，可单机可分布式，但不提供嵌入式模式。
- [[entity/vector-rag]] 查询端理解的基线检索形态：另存可查索引，块切出来即与上下文断开，单跳强而跨章节/追关系/全局归纳弱。

## concept（14）

- [[answers/answer-multi-kb-isolation]] 越权检索的正确解法是「每块带权限元数据、先过滤再检索」，分库/分 collection 只作为强隔离兜底；并给出多形态融合下的权限失效同步与审计口径。
- [[answers/answer-rag-eval-metrics]] 按「需不需要标准答案」「需不需要人工」两轴切分 RAG 评估指标，给出可全自动链路与人工只该花的三处。
- [[answers/answer-sqlitesaver-scenarios]] SqliteSaver 属存储四档中的「单机验证」档，用于单机单进程跑通检查点/interrupt/恢复；生产要多进程共享须换 PostgresSaver，且存储选型不解决「恰好一次」。
- [[concept/agent-reliability]] Agent 相对普通服务多出一层「可中断、可恢复、副作用可重放」；失败分四类且只有瞬时故障值得重试，配合预防/检测/恢复三道防线。
- [[concept/checkpoint-recovery]] super-step 粒度、pending writes、durability 三档与存储四档的四类「停下」，以及 D11 实测中重做步骤与重复副作用的变化。
- [[concept/hybrid-retrieval]] 向量管语义改写、BM25 管精确串，RRF 绕开两路量纲差异，交叉编码器把「像」变成「对」；附融合与重排的三种做法、Top-K 两段式、单库双路实现与各自失效边界。
- [[concept/idempotency]] 超时重试与节点重入都会让同一逻辑执行两次；幂等键、先查后写、状态机三种做法，以及「高风险动作放确认之后」的落位原则。
- [[concept/interrupt-hitl]] interrupt 不得被 try/except 吞、多断点顺序锁定、payload 可序列化、前置副作用幂等；HITL 四种决策与条件中断优于一刀切。
- [[concept/ontology]] 通用本体（W3C OWL 2）给建模能力，Palantir 运营本体分语义与执行两部分；动作能否执行取决于规则、实现、权限、底层支持四件事同时成立，两类 MCP 的授权对象也不同。
- [[concept/rag-pipeline]] 从文档解析（MinerU Hybrid / PaddleOCR）到结构感知切分、BGE-M3 与版本化更新、混合检索加 HyDE、chunk↔原文映射，给出每段的选型理由、代价与失效边界；附在线七步、离线六环节、三种相似度度量与多轮改写、生成组装。
- [[concept/rag-production]] 索引与查询分离、四条降级路径、四条监控曲线与联合读法、四道安全边界与双重脱敏、五个误区与「先检索后生成最后组装」的排查顺序、上线清单。
- [[concept/retrieval-paradigm]] 用「理解的时点」一轴统一向量 RAG、Contextual Retrieval、GraphRAG、LightRAG、文档树导航、LLM-Wiki 六种形态，附成本与失效数字、融合四条路与治理代价。
- [[concept/retrieval-selection]] 先数页数、再看问题形态、最后看知识性质的三步判定流，以及 Wiki 优先 + 向量兜底、出处标注与负责人制度。
- [[concept/workflow-orchestration]] 链式/路由/并行/协调者-工作者/评估者-优化者/自主循环六种编排的结构、代价与一棵选型判定树。
