---
title: OpenViking
type: entity
sources: [raw/retrieval-paradigm.md]
updated: 2026-11-11
summary: 以 viking:// 虚拟文件系统组织 Agent 全部上下文（resources/memories/skills），检索先定位目录再下钻；是换一层而非第七条检索路线。
---
# OpenViking

## 是什么

`viking://` 下开一棵虚拟文件系统——`resources/` 放文档与代码（知识库就是这一个目录）、`memories/` 放偏好与经验、`skills/` 放怎么做任务。每个目录自动生成两层摘要（一句话 + 结构与要点），原文按需才读；检索先定位目录或子树，再往下钻。^[raw/retrieval-paradigm.md]

## 定位差异

前面几条路线回答「这批知识怎么被找到」，它回答「Agent 知道的所有东西怎么放进一个能管的空间」；知识只是其中一个目录。它换的是层，不是第七条路线。

## 代价与边界

- AGPL-3.0，商用分发要过法务；要独立起服务；依赖嵌入与视觉模型提供方。
- 官方未公开十万级文件下的延迟与成本。
- LoCoMo 上自报的准确率提升是自家模型组合跑的，无第三方复现。

## 证据

volcengine/OpenViking（AGPL-3.0，41,984★，2026-11-11）。在 [[concept-retrieval-paradigm]] 中列为「换一层」；若真实问题是 Agent 上下文管理，[[concept-retrieval-selection]] 里建议选这类上下文系统，其余检索方案降格为其 `resources/` 下的选项。
