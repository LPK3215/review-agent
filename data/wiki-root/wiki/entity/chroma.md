---
title: Chroma（开源 AI 原生嵌入数据库）
type: entity
sources: [raw/chroma.md]
updated: 2026-02-15
summary: Apache 2.0 的开源向量数据库，主打「像 SQLite 一样嵌入应用」：内置嵌入、元数据过滤、HNSW 索引，可平滑扩到客户端-服务器部署。
---
# Chroma（开源 AI 原生嵌入数据库）

## 是什么

Chroma 是 Chroma Inc. 维护的开源向量数据库（Apache 2.0，Python/Rust，2022 年首发，GitHub 18k+），把自己定位成「AI 原生的 SQLite」：一个 pip 装完就能用的嵌入数据库，把向量存储、嵌入生成、元数据过滤合成一套 API。^[raw/chroma.md]

## 关键能力

- **嵌入式优先**：`chromadb.Client()` 内存模式、`PersistentClient` 落盘，无需独立服务。^[raw/chroma.md]
- **内置嵌入**：默认 all-MiniLM-L6-v2，可换 OpenAI、Sentence Transformers（中文常用 BAAI/bge-base-zh-v1.5）、Cohere、Jina、CLIP 多模态，或自定义 EmbeddingFunction。^[raw/chroma.md]
- **元数据 + 文档双重过滤**：`where` 支持比较（$gt/$gte/$lt/$lte/$ne）、逻辑（$and/$or，可嵌套）、集合（$in/$nin），`where_document` 支持 $contains/$not_contains；过滤可与向量检索同次下推。^[raw/chroma.md]
- **HNSW 近邻索引**：距离度量 L2（默认）/IP/Cosine，可用 `hnsw:M`、`ef_construction`、`ef_search` 调精度与速度。^[raw/chroma.md]
- **可伸缩部署**：嵌入式 → `chroma run` 客户端-服务器 → Docker/K8s 集群，API 不变。^[raw/chroma.md]

## 数据模型

Collection 是组织单位（类比表），记录为 `{id, document, embedding, metadata}`；持久化目录含 `chroma.sqlite3`（元数据）+ 每集合子目录（data.parquet、HNSW 索引、WAL）。^[raw/chroma.md]

## 写入与查询 API

写入侧 `add` / `update` / `upsert` 支持传入预计算 embeddings 跳过内置嵌入；`get` 支持 where、limit/offset 分页与 include 选字段。查询侧可传 `query_texts` 或 `query_embeddings`，支持一次提交多个 query 并行返回，结果结构为按 query 分组的二维数组（ids/documents/metadatas/distances/embeddings）。^[raw/chroma.md]

删除支持按 id、按 where、`where={}` 全清三种粒度。注意 Chroma 没有原生阈值过滤参数，`n_results` 是取前 K 而非距离截断，需要阈值须在应用侧对 distances 二次筛。^[raw/chroma.md]

## 框架集成

LangChain：`Chroma.from_documents` 建库、`as_retriever` 检索，自带 MMR（`fetch_k` + `lambda_mult` 控多样性）与 filter 检索；LlamaIndex：`ChromaVectorStore` + `StorageContext`，嵌入模型通过 `Settings.embed_model` 指定。^[raw/chroma.md]

## 适用与边界

适合原型开发、个人项目、中小型语义搜索与 RAG、需要随应用一起分发的离线场景；大规模生产要额外评估分布式与性能上限。与 Pinecone（闭源托管）、Weaviate、Qdrant、FAISS 的对比见 [[source-chroma]] 的对比表。^[raw/chroma.md]

## 与检索范式的关系

Chroma 是「查询端理解」路线的默认基础设施：它存的是切好的块向量，块与上下文的关系靠调用方（如 [[entity-contextual-retrieval]] 在入库时补上下文）自行解决；参见 [[concept-retrieval-paradigm]]。因为没有稀疏向量，它做不了 [[concept-hybrid-retrieval]] 的单库双路，混合检索须另起一个 BM25 索引跨库融合——这正是它与 [[entity-qdrant]] 的实质差异。^[raw/chroma.md]^[raw/qdrant.md]^[concept/hybrid-retrieval.md]

## 实践红线

入库与查询必须用同一嵌入模型（否则 Dimension mismatch）；批量写入分批（原文示例每批 100–1000）；别频繁全量重建，用 update/upsert 增量；元数据要提前设计，否则后期无法过滤；备份即拷贝数据目录并保留最近 N 份。^[raw/chroma.md]
