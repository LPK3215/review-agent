---
title: LLM-Wiki
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 理解全在入库时做完、产物是页面而非索引的知识组织形态；三层三动作，四种失败模式（并发碎、编译失真、查询不一定便宜、目录有上限）。
---
# LLM-Wiki

## 是什么

理解全在入库时做完，产物是页面而不是索引。三层：raw 只读、wiki 由模型独占写、schema 定规则；三个动作：ingest、query、lint。^[raw/retrieval-paradigm.md]

## 与 RAG 的差别

是编译与解释的差别：RAG 每次提问重新推导、不留痕；Wiki 编译一次、之后只改受影响的十几页，知识会累积。读取不靠相似度，从索引页沿交叉链接走。

容易说错的点：Karpathy 那份 gist 只是能贴给 AI 的 idea file，原文强调「这是想法不是实现」；「编译器 vs 解释器」是 AWS 博客的引申，不是他提的。

## 四种失败模式

1. **并发会碎**：65 份 PDF 并发导入生成 245 页，38% 语义重复且各自增量后分叉。
2. **编译会失真**：盲编译灾难性失败率 53%–60%，加对照诊断能找回八成。
3. **查询不一定便宜**：语料仅 24 篇的预注册实验测出查询 token 约为 RAG 的 21 倍。
4. **物理上限**：索引就是 `index.md`，204 页时已 2.8 万 token。

另外编译没消灭检索——只靠目录选页命中率 70.0%，加一条 BM25 到 92.7%。^[raw/retrieval-paradigm.md]

## 证据

Karpathy llm-wiki gist（2026-04，GitHub API 复核受阻，沿用库内记录）；标准化格式为 Google Cloud 2026-06-12 发布的 OKF v0.1。

在 [[concept-retrieval-paradigm]] 中位于写入端、检索单元是概念页。与 RAG 不冲突：Wiki 是知识组织形态、RAG 是检索结构，稳妥解是 Wiki 优先 + 向量兜底，见 [[concept-retrieval-selection]]。
