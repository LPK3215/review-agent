---
title: Qdrant 向量数据库完全指南（原文摘要）
type: source
sources: [raw/qdrant.md]
updated: 2026-02-14
summary: Qdrant 的 Rust 高性能定位、Collection/Point/Payload 数据模型、量化与多向量/稀疏向量、过滤与索引、分布式部署、LangChain/LlamaIndex 集成与同类对比的压缩摘要。
---
# Qdrant 向量数据库完全指南（原文摘要）

## 定位与背景

Qdrant（读「quadrant」）由 Qdrant Solutions GmbH 用 Rust 开发，2021 年首发，Apache 2.0（另有商业许可），GitHub 24k+，语言支持 Python/Rust/Go/TS，面向生产环境的向量相似度搜索引擎与数据库，主打「极致性能 + 丰富过滤 + 生产就绪 + 灵活部署」，自称专为 RAG、推荐系统、语义搜索设计。^[raw/qdrant.md]

原文五条设计原则：性能优先（Rust）、过滤即搜索（payload 过滤与向量检索深度集成）、生产就绪（分布式/高可用/认证/监控）、开发友好（SDK/REST/Web UI）、成本优化（量化减 4–8x 内存）。^[raw/qdrant.md]

## 核心概念

- **Collection**：类比表，一组向量点。
- **Point**：一条数据（id + vector + payload）。
- **Payload**：与向量绑定的结构化元数据，可建索引、可过滤。
- **Segment / Shard / Replica**：物理存储单元 / 逻辑分片 / 冗余副本。
- **HNSW**：核心近邻索引；**WAL**：预写日志保证持久性；**Quantization**：量化压缩内存。^[raw/qdrant.md]

距离度量四选：Cosine（文本语义，推荐）、Euclid（图像特征）、Dot（推荐系统）、Manhattan（稀疏特征）；Cosine 与 Dot 建议先归一化。^[raw/qdrant.md]

## 安装与快速入门

Docker 单机（REST 6333 / gRPC 6334，挂 `qdrant_storage` 卷）、Python `pip install qdrant-client`（含 `[local]` 本地模式）、Rust/Go/TS 官方客户端、Docker Compose（含 healthcheck `/readyz` 与内存限额）。最简链路：create_collection → upsert(PointStruct) → query_points(limit) → delete。^[raw/qdrant.md]

本地模式 `QdrantClient(":memory:")` 纯内存、`QdrantClient(path="./qdrant_local_data")` 落目录，API 与远程完全相同，但**不是嵌入式数据库**（见 [[entity-qdrant]]）。^[raw/qdrant.md]

## Collection 管理与配置

`create_collection` 的基础参数是 `vectors_config`（VectorParams: size/distance/on_disk/quantization_config），高级可再加 `optimizers_config`（indexing_threshold、memmap_threshold、segment_number、max_segment_size、vector_quantity_index_threshold）、`hnsw_config`（m、ef_construct、full_scan_threshold）、`wal_config`（wal_capacity_mb、wal_segments_ahead）、`on_disk_payload`。多向量把 `vectors_config` 写成「名字→VectorParams」字典。^[raw/qdrant.md]

`get_collection` 返回点数、已索引向量数、status、optimizer_status；`get_cluster_info` 看活跃分片；快照四操作 create/list/upload/delete 支持在线零停机备份恢复。^[raw/qdrant.md]

## CRUD 与查询 API

- 写入：`upsert`（单点或批量 PointStruct）、`set_payload`/`delete_payload` 改字段、`delete` 按 ID 列表或按 Filter 条件；批量建议分批（原文示例 1000/批）。^[raw/qdrant.md]
- 搜索：`query_points` 支持 `score_threshold`、命名向量 `using`、`with_payload`（可只列字段）、`with_vectors=False`、`query_batch_points` 批量多 query。^[raw/qdrant.md]
- 推荐 `recommend`：正例/负例驱动（`best_score` 或 `average_vector`）。^[raw/qdrant.md]
- 聚合 `groups` 按 payload 字段分组（group_by / group_size），`count` 带过滤计数。^[raw/qdrant.md]
- `scroll` 分页遍历全量点（offset 链式）。^[raw/qdrant.md]
- 搜索参数：`hnsw_ef`、`exact`、量化 `rescore`/`rescale`。^[raw/qdrant.md]

## 过滤系统

`Filter` 的 must/should/must_not 组合；`MatchValue`/`MatchAny` 精确与多值匹配（多值 = OR）、`Range(gte/lte)` 数值与时间范围、`GeoRadius`/`GeoBoundingBox` 地理过滤、`HasIdCondition` 按 ID；`should` 可配 `min_should` 设下限。设计理念是「过滤即搜索」：payload 过滤与向量检索深度集成，而非先过滤再搜。^[raw/qdrant.md]

## 向量能力三档

1. **量化**：`ScalarQuantization`（INT8，`quantile=0.99`，`always_ram=True`）与 `ProductQuantization`，压缩 4–8x 内存，配 `rescore`/`rescale` 可找回精度；原文给三档权衡：低内存（Scalar）/均衡（Scalar + rescore）/高精度（不量化）。^[raw/qdrant.md]
2. **多向量**：一个点挂多个命名向量（如 text 768 / image 512），查询时 `using` 指定。^[raw/qdrant.md]
3. **稀疏向量**：`SparseVector{indices, values}` + `Sparse-Inv-Idx` 倒排索引（可设 full_scan_threshold），适合 BM25/SPLADE 风格的关键词匹配与 one-hot 类特征。^[raw/qdrant.md]

## 部署与运维

- 单机 Docker、本地 `:memory:`/`path=`、Docker Compose、K8s StatefulSet（headless Service + volumeClaimTemplates）。
- 分布式：`shard_number`、`replication_factor`、`ShardingMethod.AUTO`，P2P 端口 6335 与共识端口 6336，`CLUSTER__BOOTSTRAP` 指向首节点；`get_cluster_info` 查活跃分片与状态。
- **快照**：`create_snapshot` / `download_snapshot` / `upload_snapshot` 支持在线零停机备份恢复，原文给出 QdrantBackup 封装示例。
- Payload 索引类型：KEYWORD / INTEGER / FLOAT / BOOL / TEXT（可配分词器）/ GEO。
- 安全：API Key、TLS、IP 访问控制、快照加密、日志审计（生产五件套）。^[raw/qdrant.md]

## 集成与实战

官方 SDK：Python（`qdrant-client`，含 `[local]` 本地模式）、Rust、Go、TypeScript。LangChain 用 `Qdrant.from_documents` 与 `QdrantRetriever`（可接 `RetrievalQA`），LlamaIndex 用 `QdrantVectorStore` + `StorageContext`；中文场景可配 `BAAI/bge-base-zh-v1.5`。原文给出两个实战项目：QdrantRAGSystem（ingest→retrieve→generate，text-embedding-3-small 1536 维）与 RecommendationSystem（正负例 + `exclude_ids` 过滤 + 相似物品排除自身）。^[raw/qdrant.md]

## 同类对比（原文口径）

Qdrant 独有稀疏向量与地理过滤，量化与 gRPC 齐全，但**不支持嵌入式**——这正是 [[entity-chroma]] 的强项。原文表格中 Pinecone 闭源、Weaviate 无量化、Milvus 无稀疏向量、Chroma 无量化/稀疏/多向量/分布式。性能维度上 Qdrant 与 Pinecone 在延迟、吞吐、内存效率、过滤性能均给满星，Milvus/Weaviate 略低，部署难度则以 Pinecone 最低、Milvus 最高。^[raw/qdrant.md]

## 排错与最佳实践

- 错误表：Connection refused / Collection not found / Dimension mismatch / No space left on device / Memory limit exceeded / Snapshot failed，各附原因与解法。^[raw/qdrant.md]
- 性能三问：搜索慢调 `hnsw_ef`；内存高改 `on_disk=True` + 量化；插入慢调大 `indexing_threshold`。^[raw/qdrant.md]
- Collection 设计（分片/副本/维度/距离/on_disk）；分批导入（100–1000 条一批）；查询时 `with_payload` 只列需要字段、`with_vectors=False`、filter 缩小搜索空间、批量查询；运维上定期快照、监控点数与延迟、容量规划、测试环境先行升级。^[raw/qdrant.md]
