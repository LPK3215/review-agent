---
title: GraphRAG
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 把摘要从查询时临场发挥改为索引时预计算：抽实体建图、社区预写摘要，治「整体主题是什么」，代价是建图贵且语料必须静态。
---
# GraphRAG

## 是什么

把摘要从查询时的临场发挥改为索引时的预计算：抽实体建图、按关系密度聚成社区、每圈预写摘要，社区摘要相当于物化视图。^[raw/retrieval-paradigm.md]

## 与相邻方案差异

与 [[entity-vector-rag]] 的差别是从「找相似片段」变成「沿关系追查」，另加全局归纳能力。它真正治的不是多跳，而是「这批材料的主题是什么」——这类问题本质是摘要任务，答案不在任何一块里。

## 代价与边界

- 建图贵、查询贵、语料必须静态。
- 实测：600 token 窗口、约 100 万 token 语料、16GB 虚拟机，建图 281 分钟；全局查询 20 秒起，单次读几十万 token。
- 只对「把全文塞进上下文」省钱，对向量检索是纯增量；单跳细节型问题上论文自己承认向量 RAG 更强。

^[raw/retrieval-paradigm.md]

## 证据与维护状态

Edge et al.《From Local to Global: A Graph RAG Approach to Query-Focused Summarization》arXiv:2404.16130；microsoft/graphrag（MIT）。**该仓未归档、2026-11-09 仍有推送、README 无维护模式声明**，所以「不上图」的正当理由是「不到 500 页」或「问题不是全局归纳类」，不能拿「仓库停维护」当理由。^[raw/retrieval-paradigm.md]

在 [[concept-retrieval-paradigm]] 中位于写入端（预计算摘要）；更新贵的问题由 [[entity-lightrag]] 的并集增量应对。选型见 [[concept-retrieval-selection]]。
