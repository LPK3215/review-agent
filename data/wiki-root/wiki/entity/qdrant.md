---
title: Qdrant（Rust 编写的高性能向量数据库）
type: entity
sources: [raw/qdrant.md]
updated: 2026-02-14
summary: Apache 2.0 的开源向量数据库，Rust 编写、生产向：payload 过滤与向量搜索深度集成，支持量化、多向量、稀疏向量与地理过滤，可单机可分布式，但不提供嵌入式模式。
---
# Qdrant（Rust 编写的高性能向量数据库）

## 是什么

Qdrant（读「quadrant」）是 Qdrant Solutions GmbH 用 Rust 开发的向量相似度搜索引擎与数据库（Apache 2.0，另有商业许可，2021 年首发，GitHub 24k+），自我定位是「为 AI 应用的生产级向量搜索」，优势集中在性能、payload 过滤、分布式与安全方面。^[raw/qdrant.md]

与 [[entity-chroma]] 的设计取向正好互补：Chroma 是「像 SQLite 一样嵌进应用」，Qdrant 是「像数据库一样扛生产流量」。^[raw/qdrant.md]

## 关键能力

- **HNSW 索引 + payload 过滤深度集成**（「过滤即搜索」），`Filter` 的 must/should/must_not 组合，配 `MatchValue`/`MatchAny` 精确与多值、`Range` 数值与时间范围、`GeoRadius`/`GeoBoundingBox` 地理、`HasIdCondition` 按 ID；`should` 可配 `min_should` 下限。^[raw/qdrant.md]
- **量化**：Scalar（INT8，`quantile` 常用 0.99）与 Product，压缩 4–8x 内存，`always_ram=True` 常驻内存，查询时配 `rescore`/`rescale` 找回精度。^[raw/qdrant.md]
- **多向量**：一个 Point 挂多个命名向量（如 text 768 / image 512），查询时 `using` 指定。^[raw/qdrant.md]
- **稀疏向量**：原生 `SparseVector{indices, values}` + `Sparse-Inv-Idx` 倒排索引，可承载 BM25/SPLADE 类关键词召回——这一点让它在混合检索里可做单库双路。^[raw/qdrant.md]
- **生产特性**：分片（`shard_number`）+ 副本（`replication_factor`）的分布式（P2P 6335 / 共识 6336 双端口）、在线快照备份（create/list/upload/delete_snapshot，零停机）、API Key/TLS/IP 访问控制/快照加密、REST 6333 与 gRPC 6334 双协议、内置 Web UI。^[raw/qdrant.md]
- **Payload 索引**：KEYWORD/INTEGER/FLOAT/BOOL/TEXT（可配分词器 tokenizer、min/max_token_len、lowercase）/GEO 六类，可建全文索引。^[raw/qdrant.md]

## 数据模型

Collection → Point（id + vector + payload）；物理层用 Segment，逻辑层用 Shard 与 Replica；持久性靠自动开启的 WAL。距离度量四选：Cosine（文本语义搜索默认推荐）、Euclid（图像特征匹配）、Dot（推荐系统）、Manhattan（稀疏特征）。^[raw/qdrant.md]

Collection 创建可调 `optimizers_config`（indexing_threshold、memmap_threshold、segment_number、max_segment_size）、`hnsw_config`（m、ef_construct、full_scan_threshold）、`wal_config`（wal_capacity_mb、wal_segments_ahead）与 `on_disk_payload`；单向量与多向量用 `VectorParams` 或「名字→VectorParams」字典两种写法。^[raw/qdrant.md]

## 查询能力

- `query_points` 主入口：`limit`、`score_threshold`、命名向量 `using`、`with_payload`（可只列字段）、`with_vectors=False`；`query_batch_points` 一次提交多 query。^[raw/qdrant.md]
- `query_points(ids=[...])` 按 ID 取点；`recommend` 用正/负例驱动（strategy 可选 `best_score` 或 `average_vector`）；`groups` 按 payload 字段分组聚合，`count` 带过滤计数；`scroll` 用 offset 链式遍历全量点。^[raw/qdrant.md]
- 搜索参数 `search_params`：`hnsw_ef`（越大越准越慢）、`exact`（精确搜索）、量化 `rescore`/`rescale`。^[raw/qdrant.md]

## 部署形态

Docker 单机（推荐，挂 `qdrant_storage` 卷）、Docker Compose、K8s StatefulSet（3 副本 + headless Service + volumeClaimTemplates）、多节点集群（`CLUSTER__ENABLED` + BOOTSTRAP 指向首节点）。SDK 本地模式 `QdrantClient(":memory:")` 或 `QdrantClient(path="./data")` 提供与远程完全相同的 API，纯内存或落本地目录，无需起服务。**注意：它没有嵌入式库模式**，本地模式仅是 SDK 便捷用法，不是 Chroma 那种随应用分发的嵌入式数据库。^[raw/qdrant.md]

## 框架集成与实战

LangChain：`Qdrant.from_documents` 建库、`QdrantRetriever` 接 `RetrievalQA`；LlamaIndex：`QdrantVectorStore` + `StorageContext`；中文场景可换 `BAAI/bge-base-zh-v1.5` 嵌入。原文两个实战项目：QdrantRAGSystem（embed → upsert → query → 拼上下文 → LLM）与 RecommendationSystem（用户向量 + `must_not`/`exclude_ids` 过滤 + 相似物品）。^[raw/qdrant.md]

## 在检索栈中的位置

作为向量库，它承担 [[concept-hybrid-retrieval]] 中的两路召回底座：密集向量走 HNSW，稀疏向量走倒排索引，可在同一 Collection 内完成 RRF 融合前的一步。它也是 [[entity-vector-rag]] 这类查询端理解路线的基础设施，存切好的块向量，不改变「理解发生在查询端」这一范式（见 [[concept-retrieval-paradigm]]）。^[raw/qdrant.md]^[concept/hybrid-retrieval.md]

## 同类对比（原文口径）

原文功能表以 Qdrant 为「最全」一侧：开源 Apache 2.0、Rust 编写，量化、稀疏向量、多向量、payload 索引、地理过滤、分布式、gRPC 全部 ✅，唯独嵌入式 ❌——这正是 Chroma 的强项。Pinecone 闭源、无稀疏与地理；Weaviate 无量化/稀疏/多向量；Milvus 无稀疏与地理；Chroma 无量化/稀疏/多向量/分布式。性能五维评分 Qdrant 与 Pinecone 在延迟、吞吐、内存效率、过滤性能均满分，Milvus/Weaviate 略低；部署难度则 Pinecone 最容易、Qdrant 中等、Milvus 最难。^[raw/qdrant.md]

## 选型红线

- 需要嵌入应用内、离线分发 → 选 [[entity-chroma]]，Qdrant 不合适。
- 需要稀疏向量/地理过滤/量化压内存/分布式/多向量 → Qdrant 是原文对比中少数全齐的选项。
- 入库与查询嵌入模型必须一致，否则 Dimension mismatch；批量导入分批（100–1000/批）；查询只取需要的 payload 字段并 `with_vectors=False`，用 filter 缩小搜索空间、能用批量就批量。^[raw/qdrant.md]
- 运维：定期快照备份、监控点数/延迟/内存、容量规划留余量、升级先在测试环境验证。^[raw/qdrant.md]

## 排错速查

`Connection refused`（服务未起）、`Collection not found`（未建库）、`Dimension mismatch`（嵌入维度不一致）、`No space left on device` / `Memory limit exceeded`（容量与内存）、`Snapshot failed`（磁盘或权限）。搜索慢先调 `hnsw_ef`，内存高改 `on_disk=True` + 量化，插入慢调大 `indexing_threshold`。^[raw/qdrant.md]
