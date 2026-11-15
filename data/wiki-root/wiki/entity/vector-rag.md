---
title: 向量 RAG（Vector RAG）
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 查询端理解的基线检索形态：另存可查索引，块切出来即与上下文断开，单跳强而跨章节/追关系/全局归纳弱。
---
# 向量 RAG（Vector RAG）

## 是什么

在模型参数之外另存一份可查索引，索引负责找、原文负责读。它改变的不是模型能力，而是「谁负责记住事实」——从权重交给外部存储。^[raw/retrieval-paradigm.md]

## 与相邻方案差异

- 与微调：知识可热插拔，改知识不用重训。
- 与长上下文：每次只带相关片段，成本不随总量线性涨。
- 出发点（Lewis et al. 2020）不是「检索更准」，而是知识密集型任务打不过专门训练模型、给不出来源、没有更新通道。

## 代价与边界

块是切出来的，切的那一刻就与上下文断开；向量还原不成原文（数字、人名、条件在压缩时丢失），故索引必须同时存原文与向量。单跳事实强，**跨章节取证、跨文档追关系、全局归纳三类任务全露短板**。^[raw/retrieval-paradigm.md]

## 证据

Lewis et al.《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》NeurIPS 2020，arXiv:2005.11401。NQ 上 626M 参数 RAG 达 44.5 EM，11B 闭卷 T5 仅 34.5——参数不是知识的好容器，索引才是。^[raw/retrieval-paradigm.md]

在 [[concept-retrieval-paradigm]] 中处于查询端一格；其块丢失的位置信息可由 [[entity-contextual-retrieval]] 补，关系与全局问题交给 [[entity-graphrag]] / [[entity-lightrag]]。选型见 [[concept-retrieval-selection]]。
