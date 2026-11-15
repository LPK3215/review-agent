---
title: LightRAG
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 针对 GraphRAG 重建贵的问题，用节点/边并集做增量更新；宏观能力来自查询时双路打图，对 GraphRAG 仅打平。
---
# LightRAG

## 是什么

解决的不是 RAG 的老问题，而是 [[entity-graphrag]] 自己造成的问题：新数据一进来社区划分就变，原摘要整批作废。做法是把新抽的节点集、边集与旧的取并集，是 INSERT 不是重建。^[raw/retrieval-paradigm.md]

## 宏观能力来源相反

- GraphRAG 靠索引时预写的摘要：静态、稳定、贵。
- LightRAG 靠查询时把问题拆成主题词与实体词两路打图：动态、便宜，代价是结论随关键词漂。

## 代价与数字

- 首建不便宜，同样逐块抽实体，量级与 GraphRAG 抽取阶段相当（「首建便宜」是误解）。
- 增量会让图越来越稠，需定期合并剪枝。
- 同规模新数据整体重建约 1,399 万 token（1,399 社区 × 2 遍 × 每份约 5,000 token）；检索 <100 token/次。
- 对 GraphRAG 的 Overall 胜率四领域：54.8% / 52.0% / 52.8% / **49.6%**，第四个领域是输的——「全面超越」不成立。

^[raw/retrieval-paradigm.md]

## 证据

Guo et al.《LightRAG》EMNLP 2025，arXiv:2410.05779；HKUDS/LightRAG（MIT，40,645★，2026-11-11）。

在 [[concept-retrieval-paradigm]] 中位于写入端（动态增量），检索单元是关系 + 向量。选型见 [[concept-retrieval-selection]]。
