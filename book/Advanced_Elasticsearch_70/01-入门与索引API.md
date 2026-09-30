# ES 7.0 入门与索引 API（原书 Ch1–2）

> ⚠️ 本章为主题重构：原书 Ch1 无代码目录（纯导论），Ch2 代码为 `index_api`。内容据 GitHub README 特征列表、ES 7.0 官方文档及 Packt 同类书风格推定。

## 1. ES 7.0 核心变化概览

ES 7.0（2019-04 GA）是里程碑版本，相对书中时代前的 6.x：
- **Types 默认禁用**——URL 固定 `_doc`，不再有 `/{index}/{type}` 路径；官方文档 https://www.elastic.co/guide/en/elasticsearch/reference/7.17/mapping-types.html ✅ 200
- `_all` 字段移除，替代方案 `copy_to` 或 `multi_match`
- 分布式集群协调层重写（基于 Raft 共识，替代 Zen discovery）
- `track_total_hits` 默认截断 10000（性能考量）
- BM25 自 5.0 起即为默认相似度；7.0 延续
- 与 [../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md) §4 大对位表逐行对照阅读

## 2. 架构心智模型

- **Cluster → Node → Index → Shard → Segment** 五层嵌套
- 倒排索引：term dictionary（FST）+ posting list（跳表 + Roaring bitmap）
- Lucene 段不可变；写入 = 新段 + refresh（1s 默认）→ merge
- 主分片数创建后不可改；改需 reindex（见 02 章）

⚠️ 以上 ES 行为转述自官方文档；本册不安装 ES 集群。

## 3. Index API 基本用法

`PUT /my_index/_doc/1` 指定 ID 索引；`POST /my_index/_doc` 自增 ID。
请求体即 JSON 文档，写入时经 translog → refresh → searchable → flush → segment。

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-index_.html ✅ 200

## 4. REST 入门与 Postman 实操

原书用 Postman 6.6.1 作为 REST 客户端，手动发 JSON 请求。7.0 默认绑定 localhost:9200，响应 `content-type: application/json`。

关键 REST 端点：
- `GET /` 集群健康
- `_cat/indices?v` 索引列表 ✅ https://www.elastic.co/guide/en/elasticsearch/reference/7.17/cat.html
- `_cluster/health?wait_for_status=green` ✅ https://www.elastic.co/guide/en/elasticsearch/reference/7.17/cluster.html

## 5. 🔧 类比演示（非 ES 行为）

**G1：FTS5 倒排 vs LIKE 全表扫描**（SQLite 3.45.3）

```python
# 建 500 行 FTS5 虚拟表
conn.execute("CREATE VIRTUAL TABLE articles USING fts5(title, body, tokenize='porter unicode61')")
for i in range(500):
    conn.execute("INSERT INTO articles VALUES(?,?)", (f"Article {i}", f"Elasticsearch distributed search engine test {i}"))
```

| 方式 | 命中 | 耗时 | 机制 |
|---|---|---|---|
| `FTS5 MATCH 'search AND engine'` | 500 | ~0.55ms | 倒排 posting list 交集 |
| `LIKE '%search%' AND body LIKE '%engine%'` | 500 | ~0.26ms | 全表逐行扫描 |

500 行小数据集 LIKE 更快（无索引开销），但万级以上 FTS5 优势显现——**类比 ES 倒排在大数据集上的检索优势，非 ES 行为**。

**G5：Porter 词干化**（`tokenize='porter'`）：searching → search，searches → search——类比 ES analyzer 的 stemmer filter。

## 6. 7.0 集群部署快速参考

书中默认环境：单节点开发模式，`elasticsearch.yml` 关键配置：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `cluster.name` | elasticsearch | 集群标识 |
| `node.name` | hostname | 节点名称 |
| `path.data` | ./data | 数据目录 |
| `bootstrap.memory_lock` | false | 锁堆内存防 swap |
| `network.host` | 127.0.0.1 | 7.0 默认仅本地绑定 |

启动命令（⚠️ 转述，本环境不可装）：
```bash
./bin/elasticsearch -E discovery.type=single-node -E xpack.security.enabled=false
```
验证：`curl http://localhost:9200` 返回 JSON（version.number=7.0.0, tagline="You Know, for Search"）。

## 7. 倒排索引直觉建立

倒排索引回答的核心问题："哪些文档包含词项 X？"——从 term 到 posting list 的映射：

```
"elasticsearch" → [doc1, doc3, doc7]
"distributed"   → [doc1, doc5]
"search"        → [doc2, doc3, doc5]
```

`MATCH 'elasticsearch AND search'` → `[doc1,doc3,doc7] ∩ [doc2,doc3,doc5]` = `[doc3]`。

FTS5 `MATCH` 即此模型——G1 类比。Lucene 层用 FST 压缩 term dictionary + 跳表/位图存 posting list——深度见 TDG [../Elasticsearch_The_Definitive_Guide/12-倒排索引数据结构.md](../Elasticsearch_The_Definitive_Guide/12-倒排索引数据结构.md)。

## 8. 本章要点

- 7.0 types 删除是全书 API 基线——对照 TDG 1.x/2.x 需翻译（大对位表 #1–2 行）
- Index API 的 refresh/translog 机制是 NRT 的核心——TDG 原理细节可对照
- Postman 工作流适合 REST 概念建立，但 2026 年推荐 Kibana Dev Tools（见 [10-ElasticStack生态与Docker.md](10-ElasticStack生态与Docker.md)）
- 集群健康三态（green/yellow/red）是运维第一观测点——`_cluster/health` API

## 核心概念速览（中英对照）

1. **倒排索引** — Inverted Index：term → doc_id 列表映射，全文检索的核心数据结构
2. **段** — Segment：Lucene 不可变索引单元，多段合并为更少的有序段
3. **近实时** — Near Real-Time (NRT)：文档写入后默认 ~1s 可搜（refresh_interval）
4. **分片** — Shard：索引的水平切分单元，分布在不同节点上
5. **translog** — Transaction Log：写入持久化日志，防止内存段丢失
6. **类型** — Type（7.0 已废弃）：1.x/2.x 的索引内子分类，7.0 删除
7. **集群健康** — Cluster Health：green/yellow/red 三态，反映分片分配状态
8. **_cat API** — Simple text-based cluster inspection API for indices/nodes/shards
9. **RESTful API** — ES 的唯一通信接口，所有操作经 HTTP JSON 请求
10. **Postman** — 轻量级 REST 客户端工具，书中用于手动构建 ES 请求

## 最新演进与工业实践

- **2024–2026 现状**：ES 已演进至 8.x→9.x 时代（https://www.elastic.co/docs/release-notes/elasticsearch ✅ 200）。9.x 捆绑 Lucene 10（https://lucene.apache.org/core/ ✅ 200）、JDK 21+ ZGC、ES|QL 管道语言 GA（https://www.elastic.co/docs/reference/query-languages/esql ✅ 200）。
- **语义检索栈**：`semantic_text` 字段（https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text ✅ 200）、k-NN 向量检索（https://www.elastic.co/docs/solutions/search/vector/knn ✅ 200）、ELSER 稀疏向量、RRF 混合排序——完全超出本书 7.0 时代。
- **许可变更**：ES 7.10 为 Apache-2.0 末代（2021 年 AWS 据此分叉 OpenSearch https://opensearch.org/ ✅ 200）；ES 8+ 转 SSPL/Elastic License v2。
- **工业采用**：Elastic Cloud（Serverless 形态）、OpenSearch 托管服务（AWS/Azure/GCP）为当前主流；自建 ES 集群仍见于大型互联网/金融。Packt 后续无 Advanced ES 8/9 版——社区转官方文档 + 极客时间等课程。
- **经典参考**：TDG（#98）的倒排索引原理（[../Elasticsearch_The_Definitive_Guide/12-倒排索引数据结构.md](../Elasticsearch_The_Definitive_Guide/12-倒排索引数据结构.md)）仍为最佳入门材料，概念保鲜 12 年。
- **Elastic Agent**（8.x 起）：统一采集器替代 Filebeat + Metricbeat 独立部署——书中 Postman 手动时代已远
- **ES|QL 时代影响**：`FROM idx | LIMIT 10` 替代部分 REST 查询——但 Index API（写入）仍走 REST 不变
