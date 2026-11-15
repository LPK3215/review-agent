# 【百战程序员】Chroma

> 开源 AI 原生嵌入数据库 —— 让向量搜索像 SQLite 一样简单

---

## 1. 项目简介

### 1.1 什么是 Chroma

Chroma 是一个开源的 **AI 原生嵌入数据库**（Embedding Database），专为构建语义搜索和 AI 应用而设计。它将向量存储、嵌入管理和元数据过滤整合在一个简洁的 API 中，让开发者可以像使用 SQLite 一样轻松地管理向量数据。

Chroma 的核心目标是**降低构建 AI 应用的门槛**，让任何开发者都能快速实现语义搜索、RAG（检索增强生成）和长期记忆功能。

### 1.2 项目背景

| 属性 | 信息 |
|-|-|
| 项目名称 | Chroma |
| 开发组织 | Chroma Inc. |
| 仓库地址 | https://github.com/chroma-core/chroma |
| 官方网站 | https://www.trychroma.com |
| 许可证 | Apache 2.0 |
| 编程语言 | Python / Rust |
| 主要用途 | 向量数据库、语义搜索、RAG |
| GitHub Stars | 18k+ |
| 首次发布 | 2022 年 |
| 语言支持 | Python、TypeScript/JavaScript |

### 1.3 核心功能

| 功能 | 描述 |
|-|-|
| 向量存储 | 高性能向量存储和检索 |
| 内置嵌入 | 支持多种嵌入模型，开箱即用 |
| 元数据过滤 | 强大的元数据过滤查询 |
| 持久化存储 | 支持本地和云端持久化 |
| 分布式部署 | 支持客户端-服务器模式 |
| 框架集成 | 与 LangChain、LlamaIndex 无缝集成 |
| 多模态支持 | 支持文本、图像、音频等多模态嵌入 |
| 简洁 API | 类似 SQLAlchemy 的简洁接口 |

### 1.4 架构定位

<readonly-block type="isv"></readonly-block>

---

## 2. 核心理念与设计哲学

### 2.1 为什么需要向量数据库

传统数据库的问题：

1. **关键词匹配**：无法理解语义相似性
2. **非结构化数据**：难以高效存储和检索
3. **AI 集成复杂**：需要额外的向量存储层
4. **部署门槛高**：大多数向量数据库需要复杂配置

### 2.2 Chroma 的设计哲学

<readonly-block type="isv"></readonly-block>

**核心设计原则：**

| 原则 | 说明 |
|-|-|
| 嵌入式优先 | 可以像 SQLite 一样嵌入应用中使用 |
| 开箱即用 | 默认配置即可工作，无需复杂设置 |
| AI 原生 | 从设计之初就为 AI 应用优化 |
| 开源免费 | Apache 2.0 许可，社区驱动 |
| 可扩展 | 从嵌入式到分布式，按需扩展 |

### 2.3 与其他向量数据库的区别

<readonly-block type="isv"></readonly-block>

---

## 3. 核心概念

### 3.1 架构总览

<readonly-block type="isv"></readonly-block>

### 3.2 核心术语表

| 术语 | 说明 |
|-|-|
| Collection | 集合，类似数据库中的表，存储一组嵌入向量 |
| Embedding | 嵌入向量，文本/图像的向量表示 |
| Document | 原始数据（文本、图像等） |
| Metadata | 元数据，与嵌入关联的附加信息 |
| Query | 查询，用于检索相似嵌入的向量 |
| Distance | 距离，衡量向量相似度的指标 |
| HNSW | 分层可导航小世界图，高效近似最近邻算法 |
| Chunk | 文档分块，将长文档拆分为更小的片段 |

### 3.3 Chroma 数据模型

<readonly-block type="isv"></readonly-block>

### 3.4 距离度量

```Python
# Chroma 支持三种距离度量

# 1. L2 (欧几里得距离) - 默认
# 适合: 一般用途
distance_metric = "l2"

# 2. IP (内积 / 点积)
# 适合: 归一化向量
distance_metric = "ip"

# 3. COS (余弦相似度)
# 适合: 文本语义搜索
distance_metric = "cosine"
```

| 距离度量 | 公式 | 适用场景 | 值范围 |
|-|-|-|-|
| L2 | √(Σ(a-b)²) | 通用 | [0, +∞) |
| IP | 1 - Σ(a\*b) | 归一化向量 | [-1, 1] |
| Cosine | 1 - cos(a,b) | 语义搜索 | [-1, 1] |

---

## 4. 安装与环境配置

### 4.1 基础安装

```Bash
# pip 安装
pip install chromadb

# 或使用 poetry
poetry add chromadb

# 安装完整版本（包含客户端-服务器模式）
pip install chromadb[server]

# 安装最新开发版
pip install git+https://github.com/chroma-core/chroma.git
```

### 4.2 可选依赖

```Bash
# Sentence Transformers 嵌入
pip install sentence-transformers

# Jina AI 嵌入
pip install jina

# Google PaLM 嵌入
pip install google-generativeai

# Cohere 嵌入
pip install cohere
```

### 4.3 验证安装

```Python
import chromadb

# 打印版本
print(chromadb.__version__)

# 创建客户端
client = chromadb.Client()
print("Chroma 安装成功！")
```

### 4.4 环境变量

```
# Chroma 数据存储路径（可选）
CHROMA_PERSIST_DIRECTORY=./chroma_data

# Chroma 服务器地址（客户端模式）
CHROMA_HOST=localhost
CHROMA_PORT=8000

# 认证令牌（云端/服务器模式）
CHROMA_AUTH_TOKEN=your-token
```

### 4.5 项目结构

```
my_chroma_project/
├── .env                 # 环境变量
├── requirements.txt     # 依赖
├── chroma_data/        # Chroma 持久化数据
│   ├── chroma.sqlite3  # 元数据存储
│   └── <collection>/   # 向量数据
└── src/
    ├── main.py         # 入口文件
    ├── embeddings.py   # 嵌入配置
    └── search.py       # 搜索功能
```

---

## 5. 快速入门

### 5.1 最简示例

```Python
import chromadb

# 创建客户端（内存模式）
client = chromadb.Client()

# 创建集合
collection = client.create_collection("my_collection")

# 添加数据
collection.add(
    documents=["这是一段文本", "这是另一段文本"],
    ids=["doc1", "doc2"]
)

# 查询
results = collection.query(
    query_texts=["查询内容"],
    n_results=2
)
print(results)
```

### 5.2 完整基础示例

```Python
import chromadb

def main():
    # 1. 创建持久化客户端
    client = chromadb.PersistentClient(path="./chroma_data")
    
    # 2. 创建集合
    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"description": "知识库集合"}
    )
    
    # 3. 添加文档
    collection.add(
        documents=[
            "Python 是一种解释型、面向对象的高级编程语言",
            "JavaScript 主要用于 Web 前端开发",
            "机器学习是人工智能的一个分支",
            "深度学习使用神经网络处理复杂数据",
            "自然语言处理让计算机理解人类语言",
        ],
        metadatas=[
            {"source": "python_doc", "category": "programming"},
            {"source": "js_doc", "category": "programming"},
            {"source": "ml_doc", "category": "ai"},
            {"source": "dl_doc", "category": "ai"},
            {"source": "nlp_doc", "category": "ai"},
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
    )
    
    print(f"集合中的文档数量: {collection.count()}")
    
    # 4. 查询
    results = collection.query(
        query_texts=["AI 相关技术"],
        n_results=3
    )
    
    print("\n查询结果:")
    for i, (doc, distance) in enumerate(zip(
        results["documents"][0], 
        results["distances"][0]
    )):
        print(f"{i+1}. [距离: {distance:.4f}] {doc}")
    
    # 5. 带过滤的查询
    filtered_results = collection.query(
        query_texts=["编程语言"],
        n_results=2,
        where={"category": "programming"}
    )
    
    print("\n过滤后的结果:")
    for doc in filtered_results["documents"][0]:
        print(f"  - {doc}")

if __name__ == "__main__":
    main()
```

### 5.3 执行流程

<readonly-block type="isv"></readonly-block>

### 5.4 客户端模式

```Python
import chromadb

# 模式 1: 内存模式（最快，数据不持久化）
client = chromadb.Client()

# 模式 2: 持久化模式（数据保存到磁盘）
client = chromadb.PersistentClient(path="./chroma_data")

# 模式 3: 客户端-服务器模式（连接远程服务器）
client = chromadb.HttpClient(host="localhost", port=8000)

# 模式 4: 带认证的客户端
client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    header_auth="Bearer your-token"
)
```

---

## 6. Collection 管理

### 6.1 创建 Collection

```Python
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

# 创建新集合
collection = client.create_collection(
    name="my_collection",
    metadata={
        "description": "我的第一个集合",
        "hnsw:space": "cosine",  # 距离度量
    }
)

# 如果集合已存在，获取它
collection = client.get_collection("my_collection")

# 创建或获取（推荐）
collection = client.get_or_create_collection("my_collection")
```

### 6.2 Collection 属性

```Python
# 获取集合信息
print(f"集合名称: {collection.name}")
print(f"集合 ID: {collection.id}")
print(f"文档数量: {collection.count()}")
print(f"元数据: {collection.metadata}")
```

### 6.3 列出所有 Collection

```Python
# 获取所有集合
collections = client.list_collections()
for col in collections:
    print(f"  - {col.name} (ID: {col.id})")

# 搜索特定集合
collections = client.list_collections(
    where={"name": {"$contains": "knowledge"}}
)
```

### 6.4 删除 Collection

```Python
# 删除指定集合
client.delete_collection("my_collection")

# 或通过 Collection 对象删除
collection.delete()
```

### 6.5 Collection 配置

```Python
# 配置 HNSW 参数
collection = client.create_collection(
    name="optimized_collection",
    metadata={
        "hnsw:space": "cosine",
        "hnsw:M": 16,              # 每个节点的连接数
        "hnsw:ef_construction": 200, # 构建时的搜索范围
        "hnsw:ef_search": 100,      # 查询时的搜索范围
    }
)
```

---

## 7. 嵌入系统（Embeddings）

### 7.1 嵌入架构

<readonly-block type="isv"></readonly-block>

### 7.2 默认嵌入

```Python
import chromadb

# 默认使用 all-MiniLM-L6-v2（Sentence Transformers）
client = chromadb.Client()
collection = client.create_collection("default_embeddings")

# 自动使用默认嵌入
collection.add(
    documents=["这使用默认嵌入"],
    ids=["doc1"]
)
```

### 7.3 OpenAI 嵌入

```Python
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# 创建 OpenAI 嵌入函数
openai_ef = OpenAIEmbeddingFunction(
    api_key="your-openai-api-key",
    model_name="text-embedding-3-small"
)

# 使用 OpenAI 嵌入创建集合
collection = client.create_collection(
    name="openai_embeddings",
    embedding_function=openai_ef
)

# 添加数据（自动生成嵌入）
collection.add(
    documents=["使用 OpenAI 嵌入的文档"],
    ids=["doc1"]
)
```

### 7.4 Sentence Transformers 嵌入

```Python
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# 使用不同的 Sentence Transformers 模型
st_ef = SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-base-zh-v1.5"  # 中文优化模型
)

collection = client.create_collection(
    name="chinese_embeddings",
    embedding_function=st_ef
)
```

### 7.5 Cohere 嵌入

```Python
from chromadb.utils.embedding_functions import CohereEmbeddingFunction

cohere_ef = CohereEmbeddingFunction(
    api_key="your-cohere-api-key",
    model_name="embed-multilingual-v3.0"
)

collection = client.create_collection(
    name="cohere_embeddings",
    embedding_function=cohere_ef
)
```

### 7.6 自定义嵌入函数

```Python
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

class CustomEmbeddingFunction(EmbeddingFunction):
    """自定义嵌入函数示例"""
    
    def __call__(self, input: Documents) -> Embeddings:
        # 实现自定义嵌入逻辑
        # 例如：调用本地模型或第三方 API
        embeddings = []
        for text in input:
            # 这里替换为实际的嵌入逻辑
            embedding = self._get_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def _get_embedding(self, text: str) -> list[float]:
        # 示例：简单哈希作为伪嵌入（仅用于演示）
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        # 转换为固定维度的向量
        embedding = [float(int(hash_obj.hexdigest()[i:i+2], 16)) / 255.0
                    for i in range(0, 32, 2)]
        return embedding

# 使用自定义嵌入
custom_ef = CustomEmbeddingFunction()
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=custom_ef
)
```

### 7.7 多模态嵌入

```Python
from chromadb.utils.embedding_functions import (
    ViTEmbeddingFunction,
    CLIPEmbeddingFunction
)

# 图像嵌入
clip_ef = CLIPEmbeddingFunction()

# 添加图像
collection = client.create_collection(
    name="image_embeddings",
    embedding_function=clip_ef
)

# 添加图像文档
collection.add(
    images=["path/to/image1.jpg", "path/to/image2.jpg"],
    ids=["img1", "img2"],
    metadatas=[{"type": "image"}, {"type": "image"}]
)

# 用文本查询图像
results = collection.query(
    query_texts=["一只猫"],
    n_results=2
)
```

---

## 8. 数据操作（CRUD）

### 8.1 添加数据（Add）

```Python
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_collection")

# 添加单个文档
collection.add(
    ids=["doc1"],
    documents=["这是第一个文档"]
)

# 批量添加
collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "Python 是一种编程语言",
        "JavaScript 用于 Web 开发",
        "机器学习是 AI 的分支"
    ],
    metadatas=[
        {"category": "programming", "year": 2024},
        {"category": "programming", "year": 2024},
        {"category": "ai", "year": 2024}
    ],
    embeddings=[  # 可选：提供预计算的嵌入
        [0.1, 0.2, 0.3, ...],
        [0.4, 0.5, 0.6, ...],
        [0.7, 0.8, 0.9, ...]
    ]
)

print(f"添加后的文档数量: {collection.count()}")
```

### 8.2 获取数据（Get）

```Python
# 获取所有文档
all_docs = collection.get()
print(all_docs)

# 获取指定 ID 的文档
doc = collection.get(ids=["doc1"])
print(doc)

# 带过滤条件获取
filtered = collection.get(
    where={"category": "ai"},
    include=["documents", "metadatas", "embeddings"]
)

# 分页获取
paginated = collection.get(
    limit=10,
    offset=0,
    include=["documents", "metadatas"]
)
```

### 8.3 更新数据（Update）

```Python
# 更新指定文档
collection.update(
    ids=["doc1"],
    documents=["更新后的文本内容"],
    metadatas=[{"category": "updated", "updated_at": "2024-01-01"}]
)

# 批量更新
collection.update(
    ids=["doc1", "doc2"],
    documents=["更新的文档1", "更新的文档2"],
    metadatas=[
        {"status": "updated"},
        {"status": "updated"}
    ]
)

# 更新嵌入（如果提供了嵌入函数）
collection.update(
    ids=["doc1"],
    documents=["新内容"]  # 自动重新生成嵌入
)
```

### 8.4 删除数据（Delete）

```Python
# 按 ID 删除
collection.delete(ids=["doc1"])

# 批量删除
collection.delete(ids=["doc1", "doc2", "doc3"])

# 按元数据条件删除
collection.delete(
    where={"category": "deprecated"}
)

# 删除所有文档
collection.delete(where={})

# 删除整个集合
client.delete_collection("my_collection")
```

### 8.5 Upsert 操作

```Python
# 如果存在则更新，不存在则插入
collection.upsert(
    ids=["doc1", "doc_new"],
    documents=["更新的内容", "全新的内容"],
    metadatas=[
        {"status": "upserted"},
        {"status": "upserted"}
    ]
)
```

---

## 9. 查询与检索

### 9.1 基础查询

```Python
import chromadb

client = chromadb.Client()
collection = client.create_collection("search_demo")

# 添加一些数据
collection.add(
    documents=[
        "Python 是最流行的编程语言之一",
        "JavaScript 用于构建 Web 应用",
        "机器学习可以预测未来趋势",
        "深度学习处理图像识别任务",
        "自然语言处理理解文本含义"
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

# 文本查询
results = collection.query(
    query_texts=["编程语言"],
    n_results=3
)

# 向量查询（使用预计算的嵌入）
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3, ...]],
    n_results=3
)
```

### 9.2 查询结果详解

```Python
results = collection.query(
    query_texts=["AI 技术"],
    n_results=3,
    include=["documents", "metadatas", "distances", "embeddings"]
)

# results 结构：
# {
#     "ids": [["doc3", "doc4", "doc5"]],
#     "documents": [["机器学习...", "深度学习...", "自然语言..."]],
#     "metadatas": [[{...}, {...}, {...}]],
#     "distances": [[0.5, 0.6, 0.7]],
#     "embeddings": [[[...], [...], [...]]]
# }

# 访问结果
for i, doc_id in enumerate(results["ids"][0]):
    doc = results["documents"][0][i]
    distance = results["distances"][0][i]
    metadata = results["metadatas"][0][i]
    print(f"{doc_id}: {doc} (距离: {distance:.4f})")
```

### 9.3 多查询

```Python
# 同时执行多个查询
results = collection.query(
    query_texts=["编程", "AI", "Web 开发"],
    n_results=2
)

# 每个查询返回独立的结果
for i, query_results in enumerate(results["documents"]):
    print(f"\n查询 {i+1} 的结果:")
    for doc in query_results:
        print(f"  - {doc}")
```

### 9.4 查询参数

```Python
results = collection.query(
    query_texts=["query"],
    n_results=5,                    # 返回结果数量
    where={"category": "ai"},       # 元数据过滤
    where_document={"$contains": "机器学习"},  # 文档内容过滤
    include=["documents", "metadatas"]  # 包含的字段
)
```

### 9.5 阈值过滤

```Python
# 只返回距离小于阈值的结果
results = collection.query(
    query_texts=["query"],
    n_results=10,
    where={"$and": [
        {"category": "ai"},
        {"year": {"$gte": 2023}}
    ]}
)
```

---

## 10. 元数据过滤（Metadata Filtering）

### 10.1 过滤语法

```Python
# 简单相等过滤
where = {"category": "ai"}

# 比较操作
where = {"year": {"$gt": 2023}}      # 大于
where = {"year": {"$gte": 2023}}     # 大于等于
where = {"year": {"$lt": 2024}}      # 小于
where = {"year": {"$lte": 2024}}     # 小于等于
where = {"year": {"$ne": 2022}}      # 不等于

# 逻辑操作
where = {"$and": [{"category": "ai"}, {"year": 2024}]}
where = {"$or": [{"category": "ai"}, {"category": "ml"}]}

# 包含操作
where = {"tags": {"$in": ["python", "ml"]}}
where = {"tags": {"$nin": ["deprecated"]}}
```

### 10.2 文档内容过滤

```Python
# 包含特定文本
where_document = {"$contains": "机器学习"}

# 不包含特定文本
where_document = {"$not_contains": "deprecated"}
```

### 10.3 组合过滤

```Python
# 同时使用元数据和文档过滤
results = collection.query(
    query_texts=["AI"],
    n_results=5,
    where={"category": "ai"},
    where_document={"$contains": "深度学习"}
)
```

### 10.4 复杂过滤示例

```Python
# 复杂条件组合
where = {
    "$and": [
        {"$or": [
            {"category": "ai"},
            {"category": "ml"}
        ]},
        {"$and": [
            {"year": {"$gte": 2023}},
            {"year": {"$lte": 2024}}
        ]},
        {"importance": {"$gte": 0.8}}
    ]
}

results = collection.query(
    query_texts=["技术趋势"],
    n_results=10,
    where=where
)
```

---

## 11. 持久化与存储

### 11.1 持久化模式

```Python
import chromadb

# 创建持久化客户端
client = chromadb.PersistentClient(
    path="./chroma_data"  # 数据存储路径
)

# 所有集合都会自动持久化
collection = client.get_or_create_collection("persistent_collection")
collection.add(
    documents=["这将被持久化"],
    ids=["doc1"]
)

# 重启后数据仍然存在
```

### 11.2 存储结构

```
chroma_data/
├── chroma.sqlite3           # SQLite 元数据存储
├── <collection_uuid>/       # 每个集合一个目录
│   ├── data.parquet        # 文档和元数据
│   ├── index/              # HNSW 向量索引
│   │   ├── hnsw.index      # HNSW 索引文件
│   │   └── header.bin      # 索引头信息
│   └── length.bin          # 长度信息
└── WAL/                    # 预写日志
```

### 11.3 备份与恢复

```Python
import shutil
from pathlib import Path

# 备份数据
def backup_chroma(source_dir: str, backup_dir: str):
    """备份 Chroma 数据"""
    source = Path(source_dir)
    backup = Path(backup_dir)
    
    if backup.exists():
        shutil.rmtree(backup)
    
    shutil.copytree(source, backup)
    print(f"备份完成: {backup}")

# 恢复数据
def restore_chroma(backup_dir: str, target_dir: str):
    """恢复 Chroma 数据"""
    backup = Path(backup_dir)
    target = Path(target_dir)
    
    if target.exists():
        shutil.rmtree(target)
    
    shutil.copytree(backup, target)
    print(f"恢复完成: {target}")

# 使用
backup_chroma("./chroma_data", "./chroma_backup_2024")
```

### 11.4 数据迁移

```Python
import chromadb

# 从旧版本迁移
old_client = chromadb.PersistentClient(path="./old_chroma_data")
new_client = chromadb.PersistentClient(path="./new_chroma_data")

# 迁移所有集合
for collection in old_client.list_collections():
    old_collection = old_client.get_collection(collection.name)
    new_collection = new_client.get_or_create_collection(
        name=collection.name,
        metadata=collection.metadata
    )
    
    # 分批迁移数据
    batch_size = 1000
    offset = 0
    while True:
        batch = old_collection.get(
            limit=batch_size,
            offset=offset,
            include=["documents", "metadatas", "embeddings"]
        )
        
        if not batch["ids"]:
            break
        
        new_collection.add(
            ids=batch["ids"],
            documents=batch["documents"],
            metadatas=batch["metadatas"],
            embeddings=batch["embeddings"]
        )
        
        offset += batch_size
        print(f"迁移 {collection.name}: {offset} 条记录")
    
    print(f"集合 {collection.name} 迁移完成")
```

---

## 12. 分布式部署

### 12.1 客户端-服务器模式

```Python
import chromadb

# 启动服务器（命令行）
# chroma run --host localhost --port 8000

# 客户端连接
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)

# 使用与本地模式相同的 API
collection = client.get_or_create_collection("distributed_collection")
```

### 12.2 Docker 部署

```YAML
# docker-compose.yml
version: '3.8'

services:
  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  chroma_data:
```

```Bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f chroma

# 停止
docker-compose down
```

### 12.3 Kubernetes 部署

```YAML
# k8s/chroma-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chroma
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chroma
  template:
    metadata:
      labels:
        app: chroma
    spec:
      containers:
      - name: chroma
        image: chromadb/chroma:latest
        ports:
        - containerPort: 8000
        env:
        - name: IS_PERSISTENT
          value: "TRUE"
        volumeMounts:
        - name: chroma-storage
          mountPath: /chroma/chroma
      volumes:
      - name: chroma-storage
        persistentVolumeClaim:
          claimName: chroma-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: chroma-service
spec:
  selector:
    app: chroma
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer
```

### 12.4 集群模式

```Python
import chromadb

# 连接到 Chroma 集群
client = chromadb.HttpClient(
    host="chroma-cluster.example.com",
    port=8000,
    header_auth="Bearer your-cluster-token"
)

# 所有操作与本地模式相同
collection = client.get_or_create_collection("cluster_collection")
```

---

## 13. LangChain 集成

### 13.1 基础集成

```Python
from langchain_community.vectorstores import Chroma
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

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_langchain"
)

# 检索
results = vectorstore.similarity_search("查询内容", k=3)
```

### 13.2 检索器集成

```Python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
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
print(result["source_documents"])
```

### 13.3 自定义检索策略

```Python
# 最大边际相关性（MMR）检索
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 10,
        "lambda_mult": 0.7  # 多样性权重
    }
)

# 带过滤的检索
retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": {"category": "technical"},
        "k": 3
    }
)
```

---

## 14. LlamaIndex 集成

### 14.1 基础集成

```Python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

# 创建 Chroma 客户端和集合
chroma_client = chromadb.PersistentClient(path="./chroma_llamaindex")
chroma_collection = chroma_client.get_or_create_collection("documents")

# 创建向量存储
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# 创建存储上下文
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 加载文档并创建索引
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("查询内容")
print(response)
```

### 14.2 自定义嵌入

```Python
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# 配置嵌入模型
Settings.embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-small"
)

# 使用自定义嵌入创建索引
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=Settings.embed_model
)
```

---

## 15. 项目实战

### 15.1 项目一：语义搜索引擎

```Python
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import json

class SemanticSearchEngine:
    """语义搜索引擎"""
    
    def __init__(self, collection_name: str = "search_engine"):
        self.client = chromadb.PersistentClient(path="./search_data")
        
        # 使用中文优化的嵌入模型
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-base-zh-v1.5"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: list[dict]):
        """添加文档"""
        self.collection.add(
            documents=[doc["content"] for doc in documents],
            metadatas=[doc.get("metadata", {}) for doc in documents],
            ids=[doc["id"] for doc in documents]
        )
        print(f"已添加 {len(documents)} 个文档")
    
    def search(self, query: str, n_results: int = 5) -> list[dict]:
        """语义搜索"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return formatted_results

# 使用示例
engine = SemanticSearchEngine()

# 添加文档
documents = [
    {"id": "1", "content": "Python 是最流行的编程语言", "metadata": {"category": "programming"}},
    {"id": "2", "content": "JavaScript 用于 Web 开发", "metadata": {"category": "programming"}},
    {"id": "3", "content": "机器学习是 AI 的分支", "metadata": {"category": "ai"}},
]
engine.add_documents(documents)

# 搜索
results = engine.search("编程语言")
for r in results:
    print(f"  [{r['distance']:.4f}] {r['document']}")
```

### 15.2 项目二：RAG 系统

```Python
import chromadb
from openai import OpenAI

class RAGSystem:
    """基于 Chroma 的 RAG 系统"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./rag_data")
        self.collection = self.client.get_or_create_collection("knowledge_base")
        self.openai = OpenAI()
    
    def ingest(self, documents: list[str]):
        """导入文档"""
        # 简单分块
        chunks = []
        chunk_ids = []
        for i, doc in enumerate(documents):
            # 按段落分块
            paragraphs = doc.split("\n\n")
            for j, para in enumerate(paragraphs):
                if para.strip():
                    chunks.append(para.strip())
                    chunk_ids.append(f"doc{i}_chunk{j}")
        
        self.collection.add(documents=chunks, ids=chunk_ids)
        print(f"已导入 {len(chunks)} 个文本块")
    
    def retrieve(self, query: str, k: int = 3) -> list[str]:
        """检索相关文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        return results["documents"][0]
    
    def generate(self, query: str) -> str:
        """生成回答"""
        # 检索相关文档
        context_docs = self.retrieve(query)
        context = "\n\n".join(context_docs)
        
        # 使用 LLM 生成
        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"基于以下上下文回答问题：\n\n{context}"},
                {"role": "user", "content": query}
            ]
        )
        
        return response.choices[0].message.content

# 使用
rag = RAGSystem()
rag.ingest(["这是文档内容..."])
answer = rag.generate("问题是什么？")
print(answer)
```

### 15.3 项目三：多模态搜索

```Python
import chromadb
from chromadb.utils import embedding_functions

class MultiModalSearch:
    """多模态搜索系统"""
    
    def __init__(self):
        self.client = chromadb.Client()
        
        # 使用 CLIP 嵌入支持文本和图像
        self.clip_ef = embedding_functions.CLIPEmbeddingFunction()
        
        self.text_collection = self.client.get_or_create_collection(
            name="text_documents",
            embedding_function=self.clip_ef
        )
        
        self.image_collection = self.client.get_or_create_collection(
            name="images",
            embedding_function=self.clip_ef
        )
    
    def add_text(self, documents: list[str], ids: list[str]):
        """添加文本"""
        self.text_collection.add(documents=documents, ids=ids)
    
    def add_images(self, image_paths: list[str], ids: list[str]):
        """添加图像"""
        self.image_collection.add(images=image_paths, ids=ids)
    
    def search_text(self, query: str, n: int = 5):
        """用文本查询文本"""
        return self.text_collection.query(query_texts=[query], n_results=n)
    
    def search_by_text_in_images(self, query: str, n: int = 5):
        """用文本查询图像"""
        return self.image_collection.query(query_texts=[query], n_results=n)
    
    def search_by_image(self, image_path: str, n: int = 5):
        """用图像查询图像"""
        return self.image_collection.query(images=[image_path], n_results=n)

# 使用
search = MultiModalSearch()
search.add_text(["这是文本"], ["text1"])
search.add_images(["image.jpg"], ["img1"])

# 用文本查询图像
results = search.search_by_text_in_images("一只猫")
```

---

## 16. 生产部署

### 16.1 性能优化

| 优化项 | 配置 | 说明 |
|-|-|-|
| HNSW 参数 | M=16, ef_construction=200 | 平衡精度和速度 |
| 批量操作 | 批量添加/更新 | 减少 API 调用 |
| 索引预热 | 首次查询前预加载 | 减少首次查询延迟 |
| 内存映射 | 使用 mmap | 大数据集优化 |

### 16.2 监控与日志

```Python
import logging
import chromadb

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chromadb")

# 监控集合状态
def monitor_collection(collection):
    """监控集合状态"""
    count = collection.count()
    logger.info(f"Collection {collection.name}: {count} documents")
    
    # 获取样本数据
    sample = collection.get(limit=5)
    logger.info(f"Sample IDs: {sample['ids']}")

# 健康检查
def health_check(client):
    """健康检查"""
    try:
        collections = client.list_collections()
        logger.info(f"Chroma 健康: {len(collections)} collections")
        return True
    except Exception as e:
        logger.error(f"Chroma 健康检查失败: {e}")
        return False
```

### 16.3 备份策略

```Python
import shutil
from datetime import datetime
from pathlib import Path

class ChromaBackup:
    """Chroma 备份管理"""
    
    def __init__(self, data_dir: str, backup_dir: str):
        self.data_dir = Path(data_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self) -> str:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        shutil.copytree(self.data_dir, backup_path)
        
        # 清理旧备份（保留最近 5 个）
        self._cleanup_old_backups(keep=5)
        
        return str(backup_path)
    
    def _cleanup_old_backups(self, keep: int = 5):
        """清理旧备份"""
        backups = sorted(
            [d for d in self.backup_dir.iterdir() if d.is_dir()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for old_backup in backups[keep:]:
            shutil.rmtree(old_backup)

# 使用
backup_manager = ChromaBackup("./chroma_data", "./backups")
backup_path = backup_manager.create_backup()
print(f"备份完成: {backup_path}")
```

### 16.4 安全最佳实践

| 实践 | 说明 |
|-|-|
| 访问控制 | 限制 Chroma 服务器的访问权限 |
| 数据加密 | 对敏感数据进行加密存储 |
| API 密钥管理 | 使用环境变量管理 API 密钥 |
| 网络安全 | 使用 HTTPS 和认证令牌 |
| 审计日志 | 记录所有数据操作 |

---

## 17. 常见问题与排错

### 17.1 错误排查表

| 错误 | 原因 | 解决方案 |
|-|-|-|
| `Collection not found` | 集合不存在 | 使用 `get_or_create_collection` |
| `Dimension mismatch` | 嵌入维度不匹配 | 确保使用相同的嵌入模型 |
| `Invalid embedding function` | 嵌入函数配置错误 | 检查嵌入函数参数 |
| `Data too large` | 内存不足 | 增加内存或使用持久化模式 |
| `Connection refused` | 服务器未启动 | 检查 Chroma 服务器状态 |
| `Permission denied` | 文件权限问题 | 检查数据目录权限 |

### 17.2 调试技巧

```Python
import chromadb

# 1. 检查集合状态
client = chromadb.PersistentClient(path="./chroma_data")
collections = client.list_collections()
print(f"集合数量: {len(collections)}")

for col in collections:
    collection = client.get_collection(col.name)
    print(f"  - {col.name}: {collection.count()} documents")

# 2. 检查嵌入维度
collection = client.get_collection("my_collection")
sample = collection.get(limit=1, include=["embeddings"])
if sample["embeddings"]:
    print(f"嵌入维度: {len(sample['embeddings'][0])}")

# 3. 验证数据完整性
all_docs = collection.get()
print(f"总文档数: {len(all_docs['ids'])}")
print(f"有嵌入的文档: {len(all_docs['embeddings'])}")
```

### 17.3 性能问题排查

```Python
# 问题 1: 查询慢
# 解决: 调整 HNSW 参数
collection = client.get_or_create_collection(
    "optimized",
    metadata={
        "hnsw:M": 32,           # 增加连接数
        "hnsw:ef_search": 200   # 增加搜索范围
    }
)

# 问题 2: 内存占用高
# 解决: 使用持久化模式 + 减少嵌入缓存
client = chromadb.PersistentClient(
    path="./chroma_data",
    settings=chromadb.Settings(
        anonymized_telemetry=False
    )
)

# 问题 3: 批量添加慢
# 解决: 分批添加
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    collection.add(
        documents=[d["content"] for d in batch],
        ids=[d["id"] for d in batch]
    )
```

---

## 18. 框架对比

### 18.1 功能对比表

| 功能 | Chroma | Pinecone | Weaviate | Qdrant | FAISS |
|-|-|-|-|-|-|
| 开源 | ✅ Apache 2.0 | ❌ 商业 | ✅ BSD-3 | ✅ Apache 2.0 | ✅ MIT |
| 嵌入式模式 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 内置嵌入 | ✅ | ❌ | ⚠️ 模块 | ❌ | ❌ |
| 元数据过滤 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 分布式 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 多模态 | ✅ | ⚠️ | ✅ | ✅ | ❌ |
| 部署难度 | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| 社区支持 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### 18.2 性能对比

<readonly-block type="isv"></readonly-block>

### 18.3 选择建议

<readonly-block type="isv"></readonly-block>

---

## 19. 最佳实践

### 19.1 数据处理最佳实践

| 实践 | 说明 |
|-|-|
| 合理分块 | 文档分块大小 500-1000 字符 |
| 去重处理 | 添加前检查重复数据 |
| 元数据丰富 | 为每条数据添加有意义的元数据 |
| 批量操作 | 使用批量添加减少 API 调用 |

### 19.2 嵌入最佳实践

```Python
# ✅ 好的实践 - 选择合适的嵌入模型
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# 中文场景
ef = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-base-zh-v1.5")

# 英文场景
ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# ✅ 好的实践 - 使用一致的嵌入
# 确保查询和数据使用相同的嵌入模型
```

### 19.3 查询最佳实践

```Python
# ✅ 好的查询 - 明确具体
results = collection.query(
    query_texts=["Python 编程语言的特点"],
    n_results=5
)

# ✅ 好的实践 - 使用元数据过滤
results = collection.query(
    query_texts=["编程"],
    n_results=5,
    where={"category": "programming"}
)

# ✅ 好的实践 - 限制返回数量
# 不要返回过多结果，一般 5-10 个即可
```

### 19.4 架构最佳实践

| 实践 | 说明 |
|-|-|
| 分离存储 | 元数据和向量分开管理 |
| 缓存策略 | 热门查询结果缓存 |
| 负载均衡 | 分布式部署时使用负载均衡 |
| 监控告警 | 设置性能监控和告警 |

### 19.5 反模式

| 反模式 | 问题 | 正确做法 |
|-|-|-|
| 一次性加载大量数据 | 内存溢出 | 分批加载 |
| 忽略嵌入维度 | 维度不匹配 | 使用一致的嵌入模型 |
| 不设置元数据 | 无法过滤 | 添加有意义的元数据 |
| 频繁全量重建 | 性能浪费 | 增量更新 |

---

## 20. 附录：API 速查表

### 20.1 客户端 API

```Python
import chromadb

# 创建客户端
client = chromadb.Client()                          # 内存模式
client = chromadb.PersistentClient(path="./data")   # 持久化模式
client = chromadb.HttpClient(host="localhost", port=8000)  # 服务器模式

# 集合管理
collection = client.create_collection("name")
collection = client.get_collection("name")
collection = client.get_or_create_collection("name")
client.delete_collection("name")
collections = client.list_collections()
```

### 20.2 Collection API

```Python
# 添加
collection.add(ids, documents, metadatas, embeddings)

# 获取
collection.get(ids, where, limit, offset, include)

# 查询
collection.query(query_texts, query_embeddings, n_results, where, include)

# 更新
collection.update(ids, documents, metadatas, embeddings)

# Upsert
collection.upsert(ids, documents, metadatas, embeddings)

# 删除
collection.delete(ids, where)

# 计数
collection.count()
```

### 20.3 查询参数

```Python
# include 参数
include = ["documents", "metadatas", "distances", "embeddings"]

# where 参数
where = {"key": "value"}
where = {"key": {"$gt": 10}}
where = {"$and": [condition1, condition2]}

# where_document 参数
where_document = {"$contains": "text"}
where_document = {"$not_contains": "text"}
```

### 20.4 嵌入函数

```Python
from chromadb.utils.embedding_functions import (
    OpenAIEmbeddingFunction,
    SentenceTransformerEmbeddingFunction,
    CohereEmbeddingFunction,
    JinaEmbeddingFunction,
    ONNXMiniLM_L6_V2,
    DefaultEmbeddingFunction
)
```

---

## 总结

Chroma 是一个强大而简洁的向量数据库，它的核心优势在于：

1. **开箱即用**：默认配置即可工作，无需复杂设置
2. **嵌入式优先**：可以像 SQLite 一样嵌入应用中
3. **AI 原生**：为 AI 应用从设计之初就优化
4. **框架友好**：与 LangChain、LlamaIndex 无缝集成

适合场景：

- 快速原型开发
- 嵌入式 AI 应用
- 语义搜索引擎
- RAG 系统
- 个人项目和小型应用

<readonly-block type="isv"></readonly-block>