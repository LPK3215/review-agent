---
title: 文档树导航（Document Tree Navigation）
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 以章节为检索单元、模型自行选章读原文的多步阅读法，专治答案散在相隔几十页多章节的场景。
---
# 文档树导航（Document Tree Navigation）

## 是什么

检索单元是章节。不建向量不切块，把文档解析成结构树，模型自己选章节、读原文、不够再补一章。^[raw/retrieval-paradigm.md]

## 与相邻方案差异

把「一次召回」换成「多步阅读」。专治答案散在相隔几十页的多个章节、只召回最相似那段就会漏前置条件的场景。

## 代价与边界

- 只适合章节清晰的长文档（年报、合同、手册、接口文档）。
- 延迟高、token 花得多，token 随跳数线性涨。
- 建树同样会出错，扫描件要先解决解析与 OCR。
- 通常当副手，不当唯一通道。

## 证据

VectifyAI/PageIndex（MIT），自述 vectorless、reasoning-based。在 [[concept-retrieval-paradigm]] 中位于索引端（结构先行）。选型见 [[concept-retrieval-selection]]。
