---
title: Contextual Retrieval（上下文检索）
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: Anthropic 提出的索引期补丁：给每块补 50–100 token 位置说明，三者叠加可将 top-20 失败率从 5.7% 降到 1.9%。
---
# Contextual Retrieval（上下文检索）

## 是什么

不改变检索机制，只在索引时给每个块补一段 50–100 token 的位置说明（文档叫什么、属于哪一章、这段在讲谁）。补的是「块自己是谁」——这是切块时丢掉、检索期调权重也补不回来的信息。^[raw/retrieval-paradigm.md]

## 做法与叠加

三个做法可叠加：位置说明、上下文 BM25、rerank；叠得越多降幅越大。它是补丁，不是路线。

## 代价与数字

- 一次性 $1.02 / 百万 document token，且必须靠 prompt caching 才成立。
- 官方测的是英文语料，中文需重测。
- 补不了块与块之间的关系。

Anthropic 2024-09-19《Introducing Contextual Retrieval》给出 top-20 块检索失败率：基线 5.7% → 3.7%（仅上下文嵌入，降 35%）→ 2.9%（+上下文 BM25，累计 49%）→ 1.9%（+rerank，累计 67%）。**报 1.9% 时必须说明是三者齐上。**^[raw/retrieval-paradigm.md]

在 [[concept-retrieval-paradigm]] 里属查询端一格（索引时补块），建立在 [[entity-vector-rag]] 之上；关系类需求仍需 [[entity-graphrag]]。选型见 [[concept-retrieval-selection]]。
