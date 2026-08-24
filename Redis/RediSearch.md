# RediSearch

A query and indexing engine for Redis, providing secondary indexing, full-text search, vector similarity search and aggregations.

RediSearch 是 Redis 官方推出的一个查询和索引引擎模块，它为 Redis 带来了全文搜索、向量相似度搜索和聚合分析等高级能力。

简单来说，它让 Redis 从一个高性能的键值缓存，升级为一个功能强大的实时搜索引擎和向量数据库。

### 核心能力

| 核心能力 | 主要特点 |
| :--- | :--- |
| 全文搜索 | 支持字段权重、精确短语、模糊匹配、多语言词干提取和中文分词，并能对数十亿文档进行分布式搜索。 |
| 向量搜索 | 支持 `FLAT`（精确）和 `HNSW`（高性能近似）两种索引算法，可对高维向量进行 KNN 或范围查询，非常适合构建推荐系统或 RAG（检索增强生成）应用。 |
| 结构化过滤 | 支持对数值、地理位置（GEO）和标签（TAG）等字段进行过滤和范围查询，实现复杂的混合查询。 |

### 工作原理与性能

它与我们之前讨论的 Redis“统一对象模型”不同。RediSearch 并没有使用 Redis 原生的数据结构（如有序集合）来构建索引，而是独立实现了高度优化的倒排索引、压缩位图等专用数据结构，以实现更强大的搜索功能和更低的内存占用。

在性能方面，根据官方早期公开的基准测试，RediSearch 在特定场景下的速度被认为比 Elasticsearch 等解决方案快 120% 到 500%。

### 如何开始使用

对于你的项目来说，集成 RediSearch 主要有两种方式：

1.  使用 Redis Stack：这是最简单的方式。Redis Stack 将 RediSearch 与 RedisJSON、RedisTimeSeries 等模块打包在一起，开箱即用。你可以直接通过 Docker 快速启动：`docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server`。
2.  作为模块加载：如果是独立的 Redis 服务器，需要单独下载并加载 RediSearch 模块。需要特别留意的是，从 Redis 8.0 开始，RediSearch 已经成为其核心的一部分，不再需要独立安装。

### 常用命令示例

它的操作命令以 `FT.` 前缀开头，非常直观。

```bash
# 1. 创建索引：为 'product:' 前缀的 Hash 创建索引，包含标题、描述和价格字段
FT.CREATE idx:product ON HASH PREFIX 1 product: SCHEMA title TEXT WEIGHT 5.0 description TEXT price NUMERIC

# 2. 查询数据：在 'idx:product' 中搜索包含 "full hd tv" 的文档
FT.SEARCH idx:product "full hd tv"

# 3. 高级查询：使用价格过滤，查找 200 到 300 元之间的产品
FT.SEARCH idx:product "@title:tv @price:[200 300]"
```

### 对你项目规划的潜在影响

在你的项目路线图中（尤其是 P2 常用命令阶段），RediSearch 是一个需要单独考虑和规划的能力扩展，因为它并非 Redis 的核心命令，而是一个功能强大的模块。评估它是否与你项目的目标（如实现一个与 Redis 完全兼容的替代品，或构建一个增强型的数据平台）相符，将是一个关键的决策点。

如果未来考虑集成，可以从以下几个方面着手：
*   集成测试：在你的 CI 流程（P0 阶段）中，增加对 Redis Stack（包含 RediSearch 模块）的测试环境，确保基础命令与模块的兼容性。
*   核心语义适配：思考 RediSearch 创建的索引（Index）和文档（Document）在你的“统一对象模型”中如何抽象和表示。
*   性能基准：在 P5（资源治理）阶段，将 RediSearch 的索引内存占用和查询性能纳入压测范围。

如果需要进一步了解 RediSearch 与原生 Redis 命令的交互细节，或者它在具体业务场景中的最佳实践，我们可以继续深入探讨。