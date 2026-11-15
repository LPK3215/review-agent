---
title: 混合检索与重排：两路召回、RRF 融合、交叉编码器精排
type: concept
sources: [raw/kb-rag.md, raw/qdrant.md]
updated: 2026-02-14
summary: 向量管语义改写、BM25 管精确串，RRF 绕开两路量纲差异，交叉编码器把「像」变成「对」；附融合与重排的三种做法、Top-K 两段式、单库双路实现与各自失效边界。
---
# 混合检索与重排

## 默认配置

**两路召回 + RRF 融合 + 交叉编码器重排**是当前默认配置：向量管语义改写，BM25 管精确串，RRF 绕开两路量纲不同的问题，重排负责把「像」变成「对」。^[raw/kb-rag.md]

它是 [[entity-vector-rag]] 的增强层，不改检索范式（仍属查询端理解），见 [[concept-retrieval-paradigm]]。

## 融合的三种做法

| 做法 | 优点 | 代价 |
|---|---|---|
| RRF（只看名次） | 稳、无需归一化 | 会把弱路尾部噪声一起带进来 |
| 加权求和 | 可控 | 需归一化分数，权重按语料调 |
| 学习式（LambdaMART 等） | 效果最好 | 要有标注数据 |

RRF 的 k 不是准确率旋钮，调它改变的是名次衰减速度（出自 Cormack 等 2009 SIGIR，k=60 为社区经验值）。^[raw/kb-rag.md]

## 为什么还要 Rerank

粗排是**一维**的：query 与文档各压成一个向量，只比一条轴上的距离，两边零交互；向量维度拉多高都只是把同一条轴拉长。精排是**二维**的：query 与文档拼成一条序列进同一模型，每个 token 与对方每个 token 互相 attend，比的是关系不是距离——一维只能判断「像不像」，二维才能判断「这个条件成不成立」。^[raw/kb-rag.md]

三条路：双塔粗排（离线预算 + ANN，全库毫秒级）；cross-encoder 精排（逐对现场前向，不进索引）；late interaction（[[entity-contextual-retrieval]] 同类的 ColBERT 路线，token 级向量预算 + 查询时 MaxSim，准度近精排、成本近粗排）。^[raw/kb-rag.md]

重排实现三选一：不做（排名噪声原样进 prompt）、云 API（省事但有候选数上限与网络依赖）、本地 BGE（可控但要 GPU；bge-reranker-v2-m3 上限 8192 token 但推荐训练长度 1024，更早的 base/large 是 512）。^[raw/kb-rag.md]

## Top-K 两段式

先粗排放大召回（top-50 起），再精排收敛到进 prompt 的 3~8 条。K 小漏召回、生成无依据；K 大噪声稀释注意力、拉高成本。**有 Rerank 才能放大 K；没有则放大会直接掉准确率。**^[raw/kb-rag.md]

## 两路召回落在哪个库

两路可以分库也可以单库：[[entity-qdrant]] 原生支持稀疏向量（`SparseVector{indices, values}` + 倒排索引），配合多向量配置，可在同一 Collection 内同时存放密集向量与 BM25/SPLADE 类稀疏向量，融合前不必再做跨库 join；这是它相对 [[entity-chroma]]（只存密集向量）的实质差异。^[raw/qdrant.md]^[entity/chroma.md]

## 失效边界

- 中文分词不补专有词，BM25 对业务黑话基本无效；语料全是同义改写型问法时，BM25 增量接近零。^[raw/kb-rag.md]
- 候选数超过重排上限要先截断；召回阶段没捞出来的，精排救不回。^[raw/kb-rag.md]
- 分块把表格切断，两路都救不回来。^[raw/kb-rag.md]
- 多跳问题单条打分不够。^[raw/kb-rag.md]
- 多一路索引与一层精排，延迟与维护成本都会上升。^[raw/kb-rag.md]

## 佐证

[[entity-contextual-retrieval]] 的实测里，上下文 BM25 与 rerank 叠加能进一步压低 top-20 失败率（5.7% → 1.9% 需三者齐上），说明混合与重排是「同一方向上的叠加」而非互斥选项。^[raw/kb-rag.md]^[raw/retrieval-paradigm.md]
