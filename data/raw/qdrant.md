# Qdrant

> 高性能开源向量数据库 —— 为 AI 应用提供极速向量搜索与过滤

---

## 1. 项目简介

### 1.1 什么是 Qdrant

Qdrant（发音为"quadrant"）是一个开源的**高性能向量相似度搜索引擎和数据库**，使用 Rust 编写，专为生产环境设计。它提供了强大的向量搜索、过滤和聚合能力，支持密集向量、稀疏向量和多向量，是构建 AI 应用（如 RAG、推荐系统、语义搜索）的理想选择。

Qdrant 的核心优势在于：

- **极致性能**：Rust 编写，内存安全且高效
- **丰富过滤**：支持复杂的 payload 过滤条件
- **生产就绪**：支持分布式部署、快照备份、JWT 认证
- **灵活部署**：从单机嵌入式到大规模集群，按需扩展

### 1.2 项目背景

| 属性 | 信息 |
|-|-|
| 项目名称 | Qdrant |
| 开发组织 | Qdrant Solutions GmbH |
| 仓库地址 | https://github.com/qdrant/qdrant |
| 官方网站 | https://qdrant.tech |
| 许可证 | Apache 2.0 / 商业许可 |
| 编程语言 | Rust |
| 主要用途 | 向量搜索引擎、语义搜索、RAG |
| GitHub Stars | 24k+ |
| 首次发布 | 2021 年 |
| 语言支持 | Python、Rust、Go、TypeScript/JavaScript |

### 1.3 核心功能

| 功能 | 描述 |
|-|-|
| 向量搜索 | HNSW 索引，毫秒级近似最近邻搜索 |
| Payload 过滤 | 强大的结构化数据过滤系统 |
| 稀疏向量 | 原生支持稀疏向量（BM25、SPLADE 等） |
| 多向量 | 一个点可以有多个命名向量 |
| 向量量化 | Scalar / Product 量化减少内存占用 |
| 分布式 | 自动分片和副本，水平扩展 |
| 快照备份 | 支持在线快照，零停机备份恢复 |
| gRPC & REST | 双协议支持，高性能 gRPC 接口 |
| Web UI | 内置可视化控制台 |
| 多租户 | 基于 payload 的原生多租户隔离 |

### 1.4 架构定位

<readonly-block type="isv"></readonly-block>

---

## 2. 核心理念与设计哲学

### 2.1 为什么选择 Rust

<readonly-block type="isv"></readonly-block>

### 2.2 核心设计原则

| 原则 | 说明 |
|-|-|
| 性能优先 | Rust 编写，极致的搜索和写入性能 |
| 过滤即搜索 | 强大的 payload 过滤与向量搜索深度集成 |
| 生产就绪 | 分布式、高可用、安全认证、监控 |
| 开发友好 | Python SDK、REST API、Web UI |
| 成本优化 | 向量量化技术减少 4-8x 内存占用 |

### 2.3 与其他向量数据库的区别

<readonly-block type="isv"></readonly-block>

---

## 3. 核心概念

### 3.1 架构总览

<readonly-block type="isv"></readonly-block>

### 3.2 核心术语表

| 术语 | 说明 |
|-|-|
| Collection | 集合，类似数据库的表，存储一组向量点 |
| Point | 点，集合中的一个数据单元（向量 + payload） |
| Vector | 向量，数据的数值表示（密集向量或稀疏向量） |
| Payload | 有效载荷，与向量关联的结构化元数据 |
| Segment | 段，Collection 的物理存储单元 |
| HNSW | 分层可导航小世界图，核心索引算法 |
| Quantization | 量化，通过压缩减少向量内存占用 |
| Replica | 副本，数据的冗余拷贝 |
| Shard | 分片，Collection 的逻辑分区 |
| WAL | 预写日志，保证数据持久性 |

### 3.3 数据模型

<readonly-block type="isv"></readonly-block>

### 3.4 距离度量

| 度量 | 说明 | 适用场景 | 归一化 |
|-|-|-|-|
| Cosine | 余弦相似度 | 文本语义搜索 | 推荐 |
| Euclid | 欧几里得距离 | 图像特征匹配 | 可选 |
| Dot | 点积 | 推荐系统 | 推荐 |
| Manhattan | 曼哈顿距离 | 稀疏特征 | 可选 |

---

## 4. 安装与环境配置

### 4.1 Docker 安装（推荐）

```Bash
# 单机模式
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant

# 后台运行
docker run -d \
    --name qdrant \
    -p 6333:6333 \
    -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    -e QDRANT__SERVICE__GRPC_PORT=6334 \
    qdrant/qdrant
```

### 4.2 Python SDK 安装

```Bash
# 安装 Python SDK
pip install qdrant-client

# 安装完整版本（包含本地模式依赖）
pip install qdrant-client[local]

# 验证安装
python -c "import qdrant_client; print(qdrant_client.__version__)"
```

### 4.3 其他语言 SDK

```Bash
# Rust
cargo add qdrant-client

# Go
go get github.com/qdrant/go-client

# TypeScript/JavaScript
npm install @qdrant/qdrant-js
```

### 4.4 Docker Compose 部署

```YAML
# docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__SERVICE__API_KEY=your-secret-key
      - QDRANT__STORAGE__OPTIMIZERS__INDEXING_THRESHOLD_KB=20000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G

volumes:
  qdrant_data:
```

### 4.5 项目结构

```
my_qdrant_project/
├── docker-compose.yml
├── .env
├── qdrant_storage/        # Qdrant 持久化数据
├── src/
│   ├── main.py
│   ├── collections.py
│   └── search.py
└── tests/
```

---

## 5. 快速入门

### 5.1 最简示例

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# 创建客户端
client = QdrantClient("localhost", port=6333)

# 创建集合
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=128, distance=Distance.COSINE),
)

# 插入向量
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(id=1, vector=[0.1]*128, payload={"text": "hello"}),
        PointStruct(id=2, vector=[0.2]*128, payload={"text": "world"}),
    ]
)

# 搜索
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*128,
    limit=3
)
print(results)
```

### 5.2 完整基础示例

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue
)

def main():
    # 1. 创建客户端
    client = QdrantClient("localhost", port=6333)
    
    # 2. 创建集合
    client.create_collection(
        collection_name="tech_docs",
        vectors_config=VectorParams(
            size=384,  # all-MiniLM-L6-v2 的维度
            distance=Distance.COSINE
        ),
    )
    
    # 3. 插入数据
    points = [
        PointStruct(
            id=1,
            vector=[0.1]*384,
            payload={
                "text": "Python 是一种解释型编程语言",
                "category": "programming",
                "year": 2024
            }
        ),
        PointStruct(
            id=2,
            vector=[0.2]*384,
            payload={
                "text": "JavaScript 用于 Web 开发",
                "category": "programming",
                "year": 2024
            }
        ),
        PointStruct(
            id=3,
            vector=[0.3]*384,
            payload={
                "text": "机器学习是 AI 的分支",
                "category": "ai",
                "year": 2024
            }
        ),
    ]
    
    client.upsert(collection_name="tech_docs", points=points)
    print(f"集合中的点数量: {client.count('tech_docs').count}")
    
    # 4. 基础搜索
    results = client.query_points(
        collection_name="tech_docs",
        query=[0.15]*384,
        limit=3,
        with_payload=True
    )
    
    print("\n搜索结果:")
    for point in results.points:
        print(f"  ID: {point.id}, Score: {point.score:.4f}")
        print(f"  Payload: {point.payload}")
    
    # 5. 带过滤的搜索
    filtered_results = client.query_points(
        collection_name="tech_docs",
        query=[0.15]*384,
        limit=2,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value="programming")
                )
            ]
        ),
        with_payload=True
    )
    
    print("\n过滤搜索结果:")
    for point in filtered_results.points:
        print(f"  [{point.score:.4f}] {point.payload['text']}")
    
    # 6. 删除数据
    client.delete(
        collection_name="tech_docs",
        points_selector=[1, 2]
    )

if __name__ == "__main__":
    main()
```

### 5.3 执行流程

<readonly-block type="isv"></readonly-block>

### 5.4 本地模式（无需服务器）

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# 创建本地客户端（纯内存，无需启动服务器）
client = QdrantClient(":memory:")

# 或使用临时目录持久化
client = QdrantClient(path="./qdrant_local_data")

# 所有 API 与远程模式完全相同
client.create_collection(
    collection_name="local_collection",
    vectors_config=VectorParams(size=128, distance=Distance.COSINE)
)
```

---

## 6. Collection 管理

### 6.1 创建 Collection

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, OptimizersConfigDiff,
    HnswConfigDiff, WalConfigDiff
)

client = QdrantClient("localhost", port=6333)

# 基础创建
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE,
        on_disk=True  # 向量存储在磁盘上
    ),
)

# 高级创建（带优化配置）
client.create_collection(
    collection_name="optimized_collection",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=10000,      # 低于此阈值不建索引
        memmap_threshold=20000,        # 高于此阈值使用 mmap
        segment_number=2,              # 段数量
        max_segment_size=20000,        # 最大段大小
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                          # 每个节点的连接数
        ef_construct=200,              # 构建时的搜索范围
        full_scan_threshold=10000,      # 全扫描阈值
    ),
    wal_config=WalConfigDiff(
        wal_capacity_mb=32,            # WAL 容量
        wal_segments_ahead=4,          # 预分配段数
    ),
    on_disk_payload=True,              # payload 存储在磁盘上
)
```

### 6.2 Collection 配置

```Python
from qdrant_client.models import (
    VectorParams, Distance, VectorsConfig,
    Distance
)

# 单向量配置
vectors_config = VectorParams(
    size=768,
    distance=Distance.COSINE,
    on_disk=False,
    quantization_config=None
)

# 多向量配置
vectors_config = {
    "text": VectorParams(size=768, distance=Distance.COSINE),
    "image": VectorParams(size=512, distance=Distance.COSINE),
}

client.create_collection(
    collection_name="multi_vector_collection",
    vectors_config=vectors_config
)
```

### 6.3 Collection 信息查询

```Python
# 获取 Collection 信息
info = client.get_collection("my_collection")
print(f"Collection 名称: {info.name}")
print(f"向量维度: {info.config.params.vectors.size}")
print(f"距离度量: {info.config.params.vectors.distance}")
print(f"点数量: {info.points_count}")
print(f"已索引: {info.indexed_vectors_count}")
print(f"状态: {info.status}")
print(f"优化状态: {info.optimizer_status}")

# 获取集群信息
cluster_info = client.get_cluster_info()
print(f"活跃节点: {cluster_info.active_shard_count}")
```

### 6.4 Collection 列表与删除

```Python
# 列出所有 Collection
collections = client.get_collections()
for col in collections.collections:
    print(f"  - {col.name}")

# 删除 Collection
client.delete_collection("my_collection")
```

### 6.5 Collection 快照

```Python
# 创建快照
snapshot_info = client.create_snapshot("my_collection")
print(f"快照路径: {snapshot_info.name}")

# 列出快照
snapshots = client.list_snapshots("my_collection")
for snap in snapshots:
    print(f"  - {snap.name} ({snap.size} bytes)")

# 从快照恢复
client.upload_snapshot(
    collection_name="restored_collection",
    snapshot="./snapshots/snapshot.snapshot"
)

# 删除快照
client.delete_snapshot("my_collection", snapshot_name="snapshot.snapshot")
```

---

## 7. 向量操作（CRUD）

### 7.1 插入/更新（Upsert）

```Python
from qdrant_client.models import PointStruct

# 单个点
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, ...],
            payload={"text": "文档内容", "category": "tech"}
        )
    ]
)

# 批量插入
points = [
    PointStruct(id=i, vector=[0.1]*384, payload={"index": i})
    for i in range(1000)
]
client.upsert(collection_name="my_collection", points=points)
```

### 7.2 查询（Query）

```Python
# 按 ID 查询
result = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    with_payload=True
)

# 查询单个点
point = client.query_points(
    collection_name="my_collection",
    ids=[1, 2, 3],
    with_payload=True
)

# 不返回向量
result = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    with_payload=True,
    with_vectors=False
)
```

### 7.3 更新 Payload

```Python
# 更新指定点的 payload
client.set_payload(
    collection_name="my_collection",
    payload={"category": "updated", "version": 2},
    points=[1, 2, 3]
)

# 删除特定 payload 字段
client.delete_payload(
    collection_name="my_collection",
    keys=["deprecated_field"],
    points=[1, 2]
)
```

### 7.4 删除（Delete）

```Python
# 按 ID 删除
client.delete(
    collection_name="my_collection",
    points_selector=[1, 2, 3]
)

# 按过滤条件删除
from qdrant_client.models import Filter, FieldCondition, MatchValue

client.delete(
    collection_name="my_collection",
    points_selector=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchValue(value="deprecated")
            )
        ]
    )
)
```

### 7.5 批量操作

```Python
from qdrant_client.models import PointStruct

# 批量 Upsert（推荐分批处理）
def batch_upsert(client, collection_name, data, batch_size=1000):
    """批量插入数据"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        points = [
            PointStruct(
                id=item["id"],
                vector=item["vector"],
                payload=item["payload"]
            )
            for item in batch
        ]
        client.upsert(collection_name=collection_name, points=points)
        print(f"已插入 {min(i+batch_size, len(data))}/{len(data)} 条")

# 使用
data = [
    {"id": i, "vector": [0.1]*384, "payload": {"index": i}}
    for i in range(10000)
]
batch_upsert(client, "my_collection", data)
```

---

## 8. 高级查询（Query API）

### 8.1 向量搜索

```Python
# 基础向量搜索
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=10,
    score_threshold=0.7  # 相似度阈值
)

# 使用已命名向量搜索（多向量 Collection）
results = client.query_points(
    collection_name="multi_collection",
    query=[0.1]*384,
    limit=10,
    using="text"  # 指定使用哪个向量
)

# 批量向量搜索
results = client.query_batch_points(
    collection_name="my_collection",
    queries=[
        [0.1]*384,  # 查询 1
        [0.2]*384,  # 查询 2
    ],
    limit=5
)
```

### 8.2 推荐搜索

```Python
from qdrant_client.models import RecommendRequest

# 基于正例和负例推荐
results = client.recommend(
    collection_name="my_collection",
    positive=[1, 2, 3],     # 相似于这些点
    negative=[4, 5],         # 不相似于这些点
    limit=10
)

# 基于 payload 过滤的推荐
results = client.recommend(
    collection_name="my_collection",
    positive=[1],
    negative=[],
    limit=10,
    recommend_params={
        "strategy": "best_score"  # 或 "average_vector"
    }
)
```

### 8.3 聚合查询

```Python
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue
)

# 按 payload 分组聚合
results = client.groups(
    collection_name="my_collection",
    group_by="category",
    limit=10,
    group_size=3,
    query_filter=Filter(
        must=[
            FieldCondition(key="year", range={"gte": 2023})
        ]
    )
)

# 聚合统计
results = client.count(
    collection_name="my_collection",
    count_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="ai"))
        ]
    )
)
print(f"AI 类文档数量: {results.count}")
```

### 8.4 Scroll 查询

```Python
# 遍历所有点
all_points = []
offset = None

while True:
    result, next_offset = client.scroll(
        collection_name="my_collection",
        limit=100,
        offset=offset,
        with_payload=True,
        with_vectors=False
    )
    all_points.extend(result)
    if next_offset is None:
        break
    offset = next_offset

print(f"总点数: {len(all_points)}")
```

### 8.5 搜索参数优化

```Python
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=10,
    search_params={
        "hnsw_ef": 128,        # HNSW 搜索范围（越大越精确，越慢）
        "exact": False,         # True 则使用精确搜索（慢但准确）
        "quantization": {
            "rescore": True,    # 量化后重新打分
            "rescale": True,    # 重新缩放
        }
    }
)
```

---

## 9. 过滤系统（Filtering）

### 9.1 过滤架构

<readonly-block type="isv"></readonly-block>

### 9.2 精确匹配过滤

```Python
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue, MatchAny
)

# 精确匹配
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="ai"))
        ]
    )
)

# 多值匹配（OR）
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchAny(any=["ai", "ml", "nlp"])
            )
        ]
    )
)
```

### 9.3 范围过滤

```Python
from qdrant_client.models import Range

# 数字范围
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="year",
                range=Range(gte=2023, lte=2024)
            )
        ]
    )
)

# 时间范围
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="timestamp",
                range=Range(gte=1700000000)
            )
        ]
    )
)
```

### 9.4 复合过滤

```Python
# AND 组合
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="ai")),
            FieldCondition(key="year", range={"gte": 2023}),
        ]
    )
)

# OR 组合
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        should=[
            FieldCondition(key="category", match=MatchValue(value="ai")),
            FieldCondition(key="category", match=MatchValue(value="ml")),
        ],
        min_should=1  # 至少满足一个
    )
)

# NOT 组合
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="ai"))
        ],
        must_not=[
            FieldCondition(key="status", match=MatchValue(value="deprecated"))
        ]
    )
)
```

### 9.5 地理位置过滤

```Python
from qdrant_client.models import GeoRadius, GeoPoint

# 搜索某半径内的点
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=10,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="location",
                geo_radius=GeoRadius(
                    center=GeoPoint(lon=116.4, lat=39.9),  # 北京
                    radius=10000  # 10km
                )
            )
        ]
    )
)

# 搜索某矩形区域内的点
from qdrant_client.models import GeoBoundingBox

results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=10,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="location",
                geo_bounding_box=GeoBoundingBox(
                    top_left=GeoPoint(lon=116.0, lat=40.0),
                    bottom_right=GeoPoint(lon=117.0, lat=39.0)
                )
            )
        ]
    )
)
```

### 9.6 ID 过滤

```Python
from qdrant_client.models import HasIdCondition

# 搜索特定 ID 范围
results = client.query_points(
    collection_name="my_collection",
    query=[0.1]*384,
    limit=5,
    query_filter=Filter(
        must=[
            HasIdCondition(has_id=[1, 2, 3, 4, 5])
        ]
    )
)
```

---

## 10. 向量量化（Quantization）

### 10.1 量化类型

<readonly-block type="isv"></readonly-block>

### 10.2 Scalar 量化

```Python
from qdrant_client.models import VectorParams, Distance, ScalarQuantization

# 创建带 Scalar 量化的集合
client.create_collection(
    collection_name="scalar_quantized",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type=ScalarQuantizationType.INT8,
            quantile=0.99,        # 量化范围
            always_ram=True       # 始终在 RAM 中
        )
    )
)

# 搜索时使用量化加速
results = client.query_points(
    collection_name="scalar_quantized",
    query=[0.1]*768,
    limit=10,
    search_params={
        "quantization": {
            "rescore": True,      # 量化后重新打分
        }
    }
)
```

### 10.3 Product 量化

```Python
from qdrant_client.models import (
    VectorParams, Distance, ProductQuantization
)

# 创建带 Product 量化的集合
client.create_collection(
    collection_name="product_quantized",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    quantization_config=ProductQuantization(
        product=ProductQuantizationConfig(
            type=ProductQuantizationType.INT8,
            always_ram=True
        )
    )
)

# 搜索
results = client.query_points(
    collection_name="product_quantized",
    query=[0.1]*768,
    limit=10,
    search_params={
        "quantization": {
            "rescore": True,
            "rescale": True,
        }
    }
)
```

### 10.4 量化配置优化

```Python
# 内存 vs 精度权衡
quantization_configs = {
    # 低内存方案：Scalar INT8
    "low_memory": {
        "type": "scalar",
        "quantile": 0.99,
        "always_ram": True
    },
    
    # 中等方案：Scalar INT8 + rescore
    "balanced": {
        "type": "scalar",
        "quantile": 0.99,
        "always_ram": True,
        "rescore": True
    },
    
    # 高内存方案：不量化
    "high_accuracy": {
        "type": "none"
    }
}
```

---

## 11. 分布式部署与集群

### 11.1 集群架构

<readonly-block type="isv"></readonly-block>

### 11.2 集群部署（Docker Compose）

```YAML
# docker-compose-cluster.yml
version: '3.8'

services:
  qdrant_node1:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_node1_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__P2P__PORT=6335
      - QDRANT__CLUSTER__CONSENSUS__PORT=6336
      - QDRANT__CLUSTER__BOOTSTRAP=None
    networks:
      - qdrant_cluster

  qdrant_node2:
    image: qdrant/qdrant:latest
    ports:
      - "6433:6333"
      - "6434:6334"
    volumes:
      - qdrant_node2_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__P2P__PORT=6335
      - QDRANT__CLUSTER__CONSENSUS__PORT=6336
      - QDRANT__CLUSTER__BOOTSTRAP=qdrant_node1:6335
    depends_on:
      - qdrant_node1
    networks:
      - qdrant_cluster

  qdrant_node3:
    image: qdrant/qdrant:latest
    ports:
      - "6533:6333"
      - "6534:6334"
    volumes:
      - qdrant_node3_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__P2P__PORT=6335
      - QDRANT__CLUSTER__CONSENSUS__PORT=6336
      - QDRANT__CLUSTER__BOOTSTRAP=qdrant_node1:6335
    depends_on:
      - qdrant_node1
    networks:
      - qdrant_cluster

volumes:
  qdrant_node1_data:
  qdrant_node2_data:
  qdrant_node3_data:

networks:
  qdrant_cluster:
    driver: bridge
```

### 11.3 分布式 Collection 操作

```Python
from qdrant_client.models import (
    VectorParams, Distance, ShardingMethod
)

# 创建分片 + 副本的 Collection
client.create_collection(
    collection_name="distributed_collection",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    shard_number=3,             # 3 个分片
    replication_factor=2,       # 每个分片 2 个副本
    sharding_method=ShardingMethod.AUTO,
)

# 查看集群状态
cluster_info = client.get_cluster_info()
print(f"活跃分片: {cluster_info.active_shard_count}")
print(f"集群状态: {cluster_info.status}")

# 查看 Collection 的分片分布
collection_info = client.get_collection("distributed_collection")
for shard_info in collection_info.shard_transfers:
    print(f"分片转移: {shard_info}")
```

### 11.4 Kubernetes 部署

```YAML
# qdrant-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant
spec:
  serviceName: qdrant-headless
  replicas: 3
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
      - name: qdrant
        image: qdrant/qdrant:latest
        ports:
        - containerPort: 6333
          name: http
        - containerPort: 6334
          name: grpc
        - containerPort: 6335
          name: p2p
        env:
        - name: QDRANT__CLUSTER__ENABLED
          value: "true"
        - name: QDRANT__CLUSTER__BOOTSTRAP
          value: "None"
        volumeMounts:
        - name: qdrant-storage
          mountPath: /qdrant/storage
  volumeClaimTemplates:
  - metadata:
      name: qdrant-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: qdrant-headless
spec:
  clusterIP: None
  selector:
    app: qdrant
  ports:
  - port: 6333
    name: http
  - port: 6334
    name: grpc
  - port: 6335
    name: p2p
```

---

## 12. Payload 索引与优化

### 12.1 Payload 索引

```Python
from qdrant_client.models import PayloadSchemaType, PayloadIndexParams

# 创建 Payload 索引
client.create_payload_index(
    collection_name="my_collection",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD  # 关键词索引
)

# 创建数值索引
client.create_payload_index(
    collection_name="my_collection",
    field_name="year",
    field_schema=PayloadSchemaType.INTEGER  # 整数索引
)

# 创建文本索引（全文搜索）
client.create_payload_index(
    collection_name="my_collection",
    field_name="text",
    field_schema=PayloadIndexParams(
        text_index={
            "tokenizer": "word",
            "min_token_len": 2,
            "max_token_len": 20,
            "lowercase": True
        }
    )
)

# 创建地理索引
client.create_payload_index(
    collection_name="my_collection",
    field_name="location",
    field_schema=PayloadSchemaType.GEO
)
```

### 12.2 索引类型

| 索引类型 | 说明 | 适用场景 |
|-|-|-|
| KEYWORD | 关键词索引 | 分类、标签过滤 |
| INTEGER | 整数索引 | ID、年份、数量 |
| FLOAT | 浮点数索引 | 评分、距离 |
| BOOL | 布尔索引 | 标志位 |
| TEXT | 全文索引 | 文本搜索 |
| GEO | 地理索引 | 位置查询 |

### 12.3 Payload 优化

```Python
# 获取 Payload 索引信息
collection_info = client.get_collection("my_collection")
for index_name, index_info in collection_info.payload_schema.items():
    print(f"索引: {index_name}, 类型: {index_info.data_type}")

# 删除 Payload 索引
client.delete_payload_index(
    collection_name="my_collection",
    field_name="category"
)
```

---

## 13. 多向量支持（Multi-Vectors）

### 13.1 多向量 Collection

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient("localhost", port=6333)

# 创建多向量 Collection
client.create_collection(
    collection_name="multi_vector_collection",
    vectors_config={
        "text": VectorParams(size=768, distance=Distance.COSINE),
        "image": VectorParams(size=512, distance=Distance.COSINE),
    }
)

# 插入多向量点
client.upsert(
    collection_name="multi_vector_collection",
    points=[
        PointStruct(
            id=1,
            vector={
                "text": [0.1]*768,
                "image": [0.2]*512
            },
            payload={"caption": "一张图片"}
        )
    ]
)
```

### 13.2 多向量查询

```Python
# 使用特定向量搜索
results = client.query_points(
    collection_name="multi_vector_collection",
    query=[0.1]*768,       # 文本向量
    using="text",           # 指定使用 text 向量
    limit=10
)

# 使用图像向量搜索
results = client.query_points(
    collection_name="multi_vector_collection",
    query=[0.2]*512,        # 图像向量
    using="image",          # 指定使用 image 向量
    limit=10
)

# 混合查询
# 通过多次查询组合不同向量类型的结果
```

---

## 14. 稀疏向量（Sparse Vectors）

### 14.1 稀疏向量概述

稀疏向量是一种特殊的向量表示形式，其中大部分元素为零，只有少数非零值。它特别适合表示：

- **BM25 风格的文本嵌入**：每个词对应一个非零维度
- **关键词匹配**：高度区分性的特征
- **分类特征**：one-hot 编码风格的特征

### 14.2 稀疏向量 Collection

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, SparseVector,
    PointStruct, SparseIndexParams
)

client = QdrantClient("localhost", port=6333)

# 创建稀疏向量 Collection
client.create_collection(
    collection_name="sparse_collection",
    vectors_config={
        "sparse_text": VectorParams(
            size=100000,  # 词汇表大小
            distance=Distance.DOT,
            index=SparseIndexParams(
                type="Sparse-Inv-Idx",  # 倒排索引
                full_scan_threshold=10000
            )
        )
    }
)

# 插入稀疏向量
client.upsert(
    collection_name="sparse_collection",
    points=[
        PointStruct(
            id=1,
            vector={
                "sparse_text": SparseVector(
                    indices=[10, 50, 200],  # 非零维度索引
                    values=[0.1, 0.5, 0.8]  # 对应值
                )
            },
            payload={"text": "example document"}
        )
    ]
)
```

### 14.3 稀疏向量搜索

```Python
# 稀疏向量搜索
results = client.query_points(
    collection_name="sparse_collection",
    query=[0.1]*768,  # 密集查询向量
    using="dense",     # 使用密集向量
    limit=10
)

# 或使用稀疏向量搜索
results = client.query_points(
    collection_name="sparse_collection",
    query_sparse=SparseVector(
        indices=[10, 50, 200],
        values=[0.1, 0.5, 0.8]
    ),
    limit=10
)
```

---

## 15. LangChain / LlamaIndex 集成

### 15.1 LangChain 集成

```Python
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 加载文档
loader = TextLoader("document.txt")
documents = loader.load()

# 文档分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = text_splitter.split_documents(documents)

# 创建 Qdrant 向量存储
vectorstore = Qdrant.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    host="localhost",
    port=6333,
    collection_name="langchain_docs",
    distance_func="Cosine",
)

# 检索
results = vectorstore.similarity_search("查询内容", k=3)

# 相似度检索（带分数）
results_with_scores = vectorstore.similarity_search_with_score("查询内容", k=3)
for doc, score in results_with_scores:
    print(f"[{score:.4f}] {doc.page_content[:100]}")
```

### 15.2 LangChain 检索器

```Python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import QdrantRetriever

# 创建检索器
retriever = QdrantRetriever(
    client=vectorstore.client,
    collection_name="langchain_docs",
    embeddings=OpenAIEmbeddings(),
    search_kwargs={"k": 3}
)

# 创建 QA 链
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 查询
result = qa_chain.invoke("问题是什么？")
print(result["result"])
```

### 15.3 LlamaIndex 集成

```Python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext
from qdrant_client import QdrantClient

# 创建 Qdrant 客户端
qdrant_client = QdrantClient(host="localhost", port=6333)

# 创建向量存储
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="llamaindex_docs"
)

# 创建存储上下文
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 加载文档
documents = SimpleDirectoryReader("./data").load_data()

# 创建索引
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("查询内容")
print(response)
```

### 15.4 自定义向量函数

```Python
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# 使用中文优化的嵌入模型
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# 创建向量存储
vectorstore = Qdrant.from_documents(
    documents=docs,
    embedding=embeddings,
    host="localhost",
    port=6333,
    collection_name="chinese_docs"
)
```

---

## 16. 项目实战

### 16.1 项目一：RAG 问答系统

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI
import numpy as np

class QdrantRAGSystem:
    """基于 Qdrant 的 RAG 系统"""
    
    def __init__(self, collection_name="knowledge_base"):
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
        self.openai = OpenAI()
        
        # 创建 Collection
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI text-embedding-3-small
                distance=Distance.COSINE
            ),
        )
    
    def _generate_embedding(self, text: str) -> list[float]:
        """生成嵌入向量"""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def ingest(self, documents: list[str]):
        """导入文档"""
        points = []
        for i, doc in enumerate(documents):
            embedding = self._generate_embedding(doc)
            points.append(
                PointStruct(
                    id=i,
                    vector=embedding,
                    payload={"text": doc}
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"已导入 {len(documents)} 个文档")
    
    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        """检索相关文档"""
        query_embedding = self._generate_embedding(query)
        
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=k,
            with_payload=True
        )
        
        return [
            {
                "text": point.payload["text"],
                "score": point.score
            }
            for point in results.points
        ]
    
    def generate(self, query: str) -> str:
        """生成回答"""
        context_docs = self.retrieve(query)
        context = "\n\n".join([d["text"] for d in context_docs])
        
        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"基于以下上下文回答问题：\n\n{context}"},
                {"role": "user", "content": query}
            ]
        )
        
        return response.choices[0].message.content

# 使用
rag = QdrantRAGSystem()
rag.ingest(["这是第一个文档内容", "这是第二个文档内容"])
answer = rag.generate("问题是什么？")
print(answer)
```

### 16.2 项目二：推荐系统

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class RecommendationSystem:
    """基于 Qdrant 的推荐系统"""
    
    def __init__(self, collection_name="recommendations"):
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
    
    def add_item(self, item_id: int, embedding: list[float], features: dict):
        """添加推荐项"""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=item_id,
                    vector=embedding,
                    payload=features
                )
            ]
        )
    
    def recommend(self, user_embedding: list[float], exclude_ids: list[int] = None, k: int = 10):
        """获取推荐"""
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=user_embedding,
            limit=k,
            query_filter={
                "must_not": [
                    {"has_id": exclude_ids}
                ] if exclude_ids else []
            },
            with_payload=True
        )
        
        return [
            {
                "id": point.id,
                "score": point.score,
                **point.payload
            }
            for point in results.points
        ]
    
    def similar_items(self, item_id: int, k: int = 5):
        """获取相似物品"""
        # 先获取物品的向量
        results = self.client.query_points(
            collection_name=self.collection_name,
            ids=[item_id],
            with_vectors=True
        )
        
        if not results.points:
            return []
        
        item_embedding = results.points[0].vector
        
        # 搜索相似物品
        similar = self.client.query_points(
            collection_name=self.collection_name,
            query=item_embedding,
            limit=k + 1,  # +1 因为会包含自身
            with_payload=True
        )
        
        return [
            {
                "id": point.id,
                "score": point.score,
                **point.payload
            }
            for point in similar.points
            if point.id != item_id
        ]

# 使用
rec = RecommendationSystem()

# 添加物品
rec.add_item(
    item_id=1,
    embedding=[0.1]*768,
    features={"name": "商品A", "category": "electronics"}
)

# 推荐
recommendations = rec.recommend([0.1]*768, exclude_ids=[1], k=5)
print(recommendations)
```

---

## 17. 生产部署

### 17.1 性能优化配置

```Python
from qdrant_client.models import (
    VectorParams, Distance, OptimizersConfigDiff, HnswConfigDiff
)

# 高性能配置
client.create_collection(
    collection_name="high_performance",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE,
        on_disk=True
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,       # 更大的索引阈值
        memmap_threshold=50000,        # 使用 mmap 处理大段
        segment_number=4,              # 更多段，更好的并发
        max_segment_size=30000,
        vector_quantity_index_threshold=1000,
    ),
    hnsw_config=HnswConfigDiff(
        m=32,                          # 更高的连接数
        ef_construct=256,               # 更深的构建
        full_scan_threshold=50000,      # 大数据集使用全扫描
    ),
)
```

### 17.2 监控与告警

```Python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant")

# 监控 Collection 状态
def monitor_collection(client, collection_name):
    """监控 Collection 状态"""
    info = client.get_collection(collection_name)
    
    logger.info(f"Collection: {info.name}")
    logger.info(f"  状态: {info.status}")
    logger.info(f"  点数量: {info.points_count}")
    logger.info(f"  已索引向量: {info.indexed_vectors_count}")
    logger.info(f"  优化器状态: {info.optimizer_status}")
    
    return info

# 健康检查
def health_check(client):
    """健康检查"""
    try:
        collections = client.get_collections()
        logger.info(f"Qdrant 健康: {len(collections.collections)} collections")
        return True
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return False
```

### 17.3 备份与恢复

```Python
import os
from datetime import datetime

class QdrantBackup:
    """Qdrant 备份管理"""
    
    def __init__(self, client, backup_dir="./backups"):
        self.client = client
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, collection_name: str) -> str:
        """创建快照备份"""
        snapshot_info = self.client.create_snapshot(collection_name)
        
        # 下载快照
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        local_path = os.path.join(
            self.backup_dir,
            f"{collection_name}_{timestamp}.snapshot"
        )
        
        # 从服务器下载快照
        self.client.download_snapshot(
            collection_name=collection_name,
            snapshot_name=snapshot_info.name,
            destination_path=local_path
        )
        
        return local_path
    
    def restore_backup(self, collection_name: str, snapshot_path: str):
        """从快照恢复"""
        # 上传快照
        self.client.upload_snapshot(
            collection_name=collection_name,
            snapshot_path=snapshot_path
        )

# 使用
backup_manager = QdrantBackup(client)
backup_path = backup_manager.create_backup("my_collection")
print(f"备份完成: {backup_path}")
```

### 17.4 安全配置

| 配置项 | 说明 | 推荐值 |
|-|-|-|
| API Key | 启用 API 密钥认证 | 必选 |
| TLS | 启用 HTTPS | 生产环境必选 |
| 访问控制 | 限制访问 IP | 只开放必要 IP |
| 快照加密 | 快照文件加密 | 敏感数据 |
| 日志审计 | 记录所有操作 | 生产环境 |

---

## 18. 常见问题与排错

### 18.1 错误排查表

| 错误 | 原因 | 解决方案 |
|-|-|-|
| `Connection refused` | Qdrant 服务未启动 | 检查 docker 容器状态 |
| `Collection not found` | Collection 不存在 | 使用 `create_collection` 创建 |
| `Dimension mismatch` | 向量维度不匹配 | 确保嵌入维度与 Collection 一致 |
| `No space left on device` | 磁盘空间不足 | 清理磁盘或增大存储 |
| `Memory limit exceeded` | 内存不足 | 增加内存或使用磁盘存储 |
| `Snapshot failed` | 快照创建失败 | 检查磁盘空间和权限 |

### 18.2 调试技巧

```Python
# 1. 检查 Collection 状态
info = client.get_collection("my_collection")
print(f"状态: {info.status}")
print(f"点数量: {info.points_count}")

# 2. 检查集群状态
cluster = client.get_cluster_info()
print(f"节点数: {len(cluster.result.peers)}")
print(f"分片数: {cluster.result.raft_info}")

# 3. 检查向量维度
point = client.query_points("my_collection", ids=[1], with_vectors=True)
if point.points:
    vector_dim = len(point.points[0].vector)
    print(f"向量维度: {vector_dim}")
```

### 18.3 性能问题排查

```Python
# 问题 1: 搜索慢
# 解决: 调整 HNSW 参数
results = client.query_points(
    collection_name="my_collection",
    query=query_vector,
    limit=10,
    search_params={
        "hnsw_ef": 256,  # 增加搜索范围
    }
)

# 问题 2: 内存占用高
# 解决: 使用磁盘存储 + 量化
client.update_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE,
        on_disk=True
    ),
)

# 问题 3: 插入慢
# 解决: 调整优化器配置
client.update_collection(
    collection_name="my_collection",
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=50000,
    )
)
```

---

## 19. 框架对比

### 19.1 功能对比

| 功能 | Qdrant | Pinecone | Weaviate | Milvus | Chroma |
|-|-|-|-|-|-|
| 开源 | ✅ Apache 2.0 | ❌ | ✅ BSD-3 | ✅ Apache 2.0 | ✅ Apache 2.0 |
| 语言 | Rust | Go | Go | Go | Python |
| 向量量化 | ✅ Scalar/Product | ✅ | ❌ | ✅ | ❌ |
| 稀疏向量 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 多向量 | ✅ | ✅ | ❌ | ✅ | ❌ |
| Payload 索引 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 地理位置 | ✅ | ❌ | ✅ | ❌ | ❌ |
| 分布式 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 嵌入式 | ❌ | ❌ | ❌ | ❌ | ✅ |
| gRPC | ✅ | ❌ | ❌ | ✅ | ❌ |

### 19.2 性能对比

| 指标 | Qdrant | Pinecone | Milvus | Weaviate |
|-|-|-|-|-|
| 查询延迟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 吞吐量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 内存效率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 过滤性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 部署难度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

### 19.3 选择建议

<readonly-block type="isv"></readonly-block>

---

## 20. 最佳实践

### 20.1 Collection 设计

| 实践 | 说明 |
|-|-|
| 合理分片 | 根据数据量设置 shard_number |
| 副本策略 | 高可用需求设置 replication_factor≥2 |
| 向量维度 | 与嵌入模型维度一致 |
| 距离度量 | Cosine 适合语义搜索 |
| 磁盘存储 | 大数据集设置 on_disk=True |

### 20.2 数据导入

```Python
# ✅ 好的实践 - 批量导入
def batch_import(client, collection_name, documents, embeddings):
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        batch_embeddings = embeddings[i:i+batch_size]
        
        points = [
            PointStruct(
                id=i + j,
                vector=embedding,
                payload={"text": doc}
            )
            for j, (doc, embedding) in enumerate(zip(batch, batch_embeddings))
        ]
        
        client.upsert(collection_name=collection_name, points=points)
        print(f"导入进度: {min(i+batch_size, len(documents))}/{len(documents)}")

# ✅ 好的实践 - 使用 WAL
# WAL 已自动启用，确保数据持久性
```

### 20.3 查询优化

```Python
# ✅ 好的实践 - 选择性加载
results = client.query_points(
    collection_name="my_collection",
    query=query_vector,
    limit=10,
    with_payload=["text", "category"],  # 只加载需要的字段
    with_vectors=False,                  # 不加载向量节省带宽
)

# ✅ 好的实践 - 使用过滤减少搜索空间
results = client.query_points(
    collection_name="my_collection",
    query=query_vector,
    limit=10,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="tech"))]
    ),
    search_params={"hnsw_ef": 128}
)

# ✅ 好的实践 - 批量查询
results = client.query_batch_points(
    collection_name="my_collection",
    queries=[query1, query2, query3],
    limit=10
)
```

### 20.4 运维最佳实践

| 实践 | 说明 |
|-|-|
| 定期快照 | 使用快照备份数据 |
| 监控指标 | 监控点数量、查询延迟、内存使用 |
| 日志管理 | 配置合适的日志级别 |
| 容量规划 | 预估数据增长，留有余量 |
| 版本升级 | 先在测试环境验证 |

---

## 21. 附录：API 速查表

### 21.1 客户端 API

```Python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# 创建客户端
client = QdrantClient(host="localhost", port=6333)  # 远程
client = QdrantClient(":memory:")                     # 内存模式
client = QdrantClient(path="./qdrant_storage")        # 本地持久化

# Collection 管理
client.create_collection(collection_name, vectors_config)
client.get_collection(collection_name)
client.get_collections()
client.delete_collection(collection_name)
client.update_collection(collection_name, **kwargs)
```

### 20.2 Collection API

```Python
# 创建
client.create_collection(
    collection_name,
    vectors_config,
    shard_number=1,
    replication_factor=1,
    optimizers_config=None,
    wal_config=None,
    hnsw_config=None,
    quantization_config=None,
    on_disk_payload=False
)

# 获取
collection = client.get_collection(collection_name)

# 列出
collections = client.get_collections()

# 删除
client.delete_collection(collection_name)

# 优化
client.update_collection(
    collection_name,
    optimizer_config=OptimizersConfigDiff(...)
)
```

### 20.3 向量操作 API

```Python
# Upsert
client.upsert(collection_name, points)

# 搜索
results = client.query_points(
    collection_name, query, limit, query_filter, search_params
)

# 推荐
results = client.recommend(
    collection_name, positive, negative, limit
)

# 滚动
points, offset = client.scroll(collection_name, limit, offset)

# 删除
client.delete(collection_name, points_selector)
```

### 20.4 过滤器 API

```Python
# 精确匹配
FieldCondition(key="field", match=MatchValue(value="value"))

# 多值匹配
FieldCondition(key="field", match=MatchAny(any=["v1", "v2"]))

# 范围
FieldCondition(key="field", range=Range(gte=1, lte=10))

# 地理
FieldCondition(key="field", geo_radius=GeoRadius(center=GeoPoint(...), radius=...))

# 逻辑组合
Filter(must=[...], should=[...], must_not=[...])
```

### 20.5 Collection 管理 API

```Python
# 快照
client.create_snapshot(collection_name)
client.list_snapshots(collection_name)
client.delete_snapshot(collection_name, snapshot_name)

# Payload 索引
client.create_payload_index(collection_name, field_name, field_schema)
client.delete_payload_index(collection_name, field_name)

# 集群
client.get_cluster_info()
```

---