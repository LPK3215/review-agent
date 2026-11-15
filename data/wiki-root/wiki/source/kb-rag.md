---
title: 文档处理与 RAG 主题总览（问答清单 + 方案取舍）
type: source
sources: [raw/kb-rag.md]
updated: 2026-11-12
summary: 一份把 RAG 问题清单、六种检索形态速查、解析/切分/Embedding/混合检索/Rerank/引用各环节取舍压成判断句的主题总览，附 ESG-Extractor 与 Yuxi 两项目选型与面试答法。
---
# 文档处理与 RAG 主题总览

原文件是「问题清单 + 要点对比 + 我的取舍」三段式主题文档，覆盖从解析到引用的全链路；检索范式的横向对比已独立成 [[source-retrieval-paradigm]]，本页只留速查与指针。机制层正文见 [[source-rag-total]] 与 [[concept-rag-pipeline]]。^[raw/kb-rag.md]

## 一、问题清单结构

题面按七层组织：整体流程与范式、检索范式（六种形态）、文档解析、切分、Embedding、查询理解与意图路由、向量存储与检索、知识库管理、引用溯源。面试深挖点在「你为什么不直接用向量 RAG」与「成本落在哪一侧」。^[raw/kb-rag.md]

## 二、检索范式速查

一条轴：理解放在写入端还是查询端，详见 [[concept-retrieval-paradigm]]。

| 形态 | 理解时点 | 何时选 |
|---|---|---|
| [[entity-vector-rag]] | 查询端 | 500 页以上、单跳事实、广而新 |
| [[entity-contextual-retrieval]] | 查询端（索引时补块） | 检索常漏、块里缺主语 |
| [[entity-graphrag]] | 写入端（预计算摘要） | 要整体判断且语料静态 |
| [[entity-lightrag]] | 写入端（动态增量） | 数据天天变又要关系推理 |
| [[entity-document-tree-navigation]] | 索引端（结构先行） | 答案散在相隔几十页的多个章节 |
| [[entity-llm-wiki]] | 写入端（理解全部前置） | 500 页内、有负责人审核、知识要复利 |
| [[entity-openviking]] | 换一层 | 真实问题是「Agent 上下文怎么管」 |

要点：六者不在同一层，混成一排比优劣会得出「RAG 过时了」的错结论。组合的四条路（向量找入口再图扩展、向量定位文档再树深读、Wiki 存核心加长尾 RAG、Wiki 反哺其他模式）按代价从低到高排列，第四条收益最快。融合的代价不是技术而是治理：同一知识多处存一份，源一改四处失效。^[raw/kb-rag.md]

判定三步：先数页数（不到 500 页别上 RAG），再看问题形态，最后看知识性质，见 [[concept-retrieval-selection]]。^[raw/kb-rag.md]

## 三、检索、语义、执行：三层不是演进线

RAG/GraphRAG 回答「怎样取证」，本体论回答「业务对象怎样表达、允许怎样改变」。上本体不等于不用检索：文档证据仍要检索，业务操作仍由具体服务执行。**通用本体**（W3C OWL 2）给的是建模能力，推不出审批与回写；**厂商运营本体**（Palantir Ontology）是产品定义，带 Action Types、Functions 与平台权限——把产品能力当成「本体」通用含义是最常见误读。一项业务动作能否执行取决于四件事：定义了规则、绑定了实现、配置了权限、底层系统支持；只把对象命名清楚，一步都没到。见 [[concept-ontology]]。^[raw/kb-rag.md]

## 四、解析与切分

- 解析：ESG-Extractor 走 MinerU Hybrid（本地 Pipeline 解版面、复杂页交 Qwen-VL 的 VLM），表格与图文混排还原好，代价是外部 API 的成本与延迟；Yuxi 走 LightRAG/Neo4j 图抽取，保留实体关系但不擅长原文还原。扫描件用 PaddleOCR（PP-OCRv6，GPU）注入原流程。^[raw/kb-rag.md]
- 结构保护：自研 ESGStructureAwareNodeParser 防表格被切断、指标可对齐。^[raw/kb-rag.md]
- 切分：结构感知切分保语义完整；chunk 太小召回噪声多、太大稀释相关性；overlap 防边界信息丢失；中文要考虑 BPE tokenizer 对 CJK 的分词影响。^[raw/kb-rag.md]

## 五、Embedding 与更新

本地 CUDA 部署 BGE-M3：多语言强、支持稠密/稀疏/ColBERT 三向量、可离线，代价是 GPU 资源。文档更新走 collection 版本化重建（可追溯、可回滚，代价是占空间），而非全量重灌。^[raw/kb-rag.md]

## 六、存储与混合检索

向量库选 Milvus（HNSW + 版本化）：分布式、GPU、生产可用，代价是 etcd/MinIO/Pulsar 运维重；轻量场景的默认基础设施可看 [[entity-chroma]]。^[raw/kb-rag.md]

**混合检索默认配置**：两路召回（向量管语义改写、BM25 管精确串）+ RRF 融合 + 交叉编码器重排。融合三选一：RRF 只看名次，稳但会带入弱路尾部噪声；加权求和需归一化且要按语料调权重；学习式融合（LambdaMART）最好但要有标注。重排三选一：不做（噪声进 prompt）、云 API（有候选上限与网络依赖）、本地 BGE（可控但要 GPU）。RRF 的 k 不是准确率旋钮，调它改变名次衰减速度（Cormack 2009，k=60 为社区经验值）。详见 [[concept-hybrid-retrieval]]。^[raw/kb-rag.md]

**为什么还要 Rerank**：粗排是一维的——query 与文档各压成向量，只比一条轴，两边零交互；精排是二维的——拼成一条序列进同一模型，token 级互相 attend，比的是关系而非距离。向量维度拉多高都只是把同一条轴拉长。第三条路 late interaction（ColBERT）：token 向量预算好，查询时 MaxSim，准度近精排、成本近粗排。边界：精排只对 top-20~50 做，延迟随候选线性涨；输入长度受限（bge-reranker-v2-m3 推荐 1024 token）；召回没捞到的精排救不回。^[raw/kb-rag.md]

**Top-K**：先粗排放大到 top-50 起，再精排收敛到进 prompt 的 3~8 条；有 Rerank 才能放大 K，没有则放大会直接掉准确率。^[raw/kb-rag.md]

## 七、知识库管理与引用溯源

多库隔离用 collection 级 + 版本化（互不污染、可回滚，管理变复杂）。引用溯源维护 chunk↔原文页码映射，前端高亮/跳转；金融与 ESG 这类严谨场景必须可核查。^[raw/kb-rag.md]

## 八、我的取舍（作者自述，2026-11 三次并入）

- **检索策略**：向量 + BM25 两路 RRF 再叠重排，四个函数手搓不引框架，链路短好定位；代价是多一路索引与精排延迟、BM25 要维护分词词典；失效边界是语料全是同义改写型问法（BM25 无增量）、分块把表格切断（两路都救不回）。^[raw/kb-rag.md]
- **知识底座形态**：事实形态是 [[entity-llm-wiki]]——raw 是剪藏与项目目录，wiki 是正文，schema 是 AGENTS.md 与 README，ingest 由 AI 会话执行、lint 靠链接校验脚本；不建向量库因为规模只千余篇、grep 加链接导航够用。代价是放弃语义召回、提问要贴合库内用词、跨文档多跳靠人工反链；失效边界是超过几千篇或要回答「谁依赖谁」。^[raw/kb-rag.md]
- **范式选型**：按问题形态路由不按技术栈站队；低于 500 页不做 RAG，单跳走向量 + rerank，块缺主语补 Contextual Retrieval，要整体判断且语料静态才上图，知识要复利才建 Wiki。边界：语料天天变则图路线成本落回重建端；没有审核人的项目上 Wiki，错误会以权威口吻沉淀。^[raw/kb-rag.md]

## 与已有页面的关系

检索范式的机制与数字见 [[source-retrieval-paradigm]] 与 [[concept-retrieval-paradigm]]；选型流见 [[concept-retrieval-selection]]；向量库实现见 [[source-chroma]] / [[entity-chroma]]；全链路机制见 [[source-rag-total]] / [[concept-rag-pipeline]]。^[raw/kb-rag.md]
