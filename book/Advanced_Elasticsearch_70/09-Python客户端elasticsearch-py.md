# Python 客户端 elasticsearch-py（原书 Ch12）

> ⚠️ 主题重构：Ch12 代码目录 `cf_etf`（Python 3.6），含 ETF 数据 bulk 导入与查询脚本。

## 1. elasticsearch-py 客户端概览

`elasticsearch` 是 Elastic 官方 Python 客户端。7.0 时代对应版本约 7.x（PyPI 包名 `elasticsearch`）。

```python
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
if not es.ping():
    raise ConnectionError("ES not reachable")
```

- 底层用 `requests` + urllib3 连接池
- 支持多节点 round-robin、自动故障转移、sniffing

## 2. 文档操作

```python
# Index
es.index(index="cf_etf", id="SPY", body={
    "symbol": "SPY", "name": "S&P 500 ETF", "price": 330.5,
    "category": "equity", "fund_family": "SSGA"
})

# Search
resp = es.search(index="cf_etf", body={
    "query": {"multi_match": {
        "query": "vanguard",
        "fields": ["name^3", "fund_family"]
    }},
    "aggs": {"by_category": {"terms": {"field": "category"}}},
    "size": 10
})
hits = resp["hits"]["hits"]
aggs = resp["aggregations"]["by_category"]["buckets"]
```

## 3. Bulk 辅助函数（helpers）

`elasticsearch.helpers` 提供 Pythonic 批量操作：

```python
from elasticsearch.helpers import bulk, streaming_bulk

actions = [
    {"_index": "cf_etf", "_id": etf["symbol"], "_source": etf}
    for etf in etf_data_list
]
success, failed = bulk(es, actions, chunk_size=2000, raise_on_error=False)
```

- `bulk()`：一次性提交所有 actions——内存受限
- `streaming_bulk()`：生成器逐块提交——大数据集首选
- `scan()`：scroll 遍历的 Python 封装——替代 `search + scroll` 手动循环

## 4. DSL 工具（elasticsearch-dsl-py）

`elasticsearch-dsl` 是高层 DSL 封装：

```python
from elasticsearch_dsl import Search, Q

s = Search(using=es, index="cf_etf") \
    .query(Q("multi_match", query="vanguard", fields=["name", "fund_family"])) \
    .aggs("by_cat", "terms", field="category") \
    .extra(size=20)

response = s.execute()
for hit in response:
    print(hit.meta.score, hit.name)
for bucket in response.aggregations.by_cat:
    print(bucket.key, bucket.doc_count)
```

## 5. 异步客户端（7.x 实验性）

7.0 时代 `elasticsearch-py` 以同步为主——异步 `aiohttp` 连接池为实验特性。2024+ 已成熟（见演进节）。

## 6. 🔧 类比演示（非 ES 行为）

**G1：FTS5 vs elasticsearch-py 的"全文搜索"接口对比**

| 维度 | elasticsearch-py | SQLite FTS5 (Python) |
|---|---|---|
| 连接 | `Elasticsearch([host])` | `sqlite3.connect("db")` |
| 建索引 | `es.indices.create()` + mapping | `CREATE VIRTUAL TABLE ... fts5(...)` |
| 写入 | `es.index()` / `helpers.bulk()` | `INSERT INTO ...` |
| 搜索 | `es.search(body=DSL)` | `SELECT ... WHERE t MATCH 'query'` |
| 聚合 | `es.search(body={"aggs":...})` | `SELECT ... GROUP BY`（仅 SQL） |
| 排序 | `_score` / BM25 | `bm25()` 函数 |

500 行 FTS5 MATCH 与 LIKE 对比（G1 数据见 [01-入门与索引API.md](01-入门与索引API.md)），elasticsearch-py 的 `search()` API 设计直接映射 REST JSON——**SQLite 行为非 ES**。

## 7. 本章要点

- `elasticsearch-py` 是 ES 的"Python 原生接口"——所有 REST 功能 1:1 映射
- `helpers.bulk()` / `streaming_bulk()` 是性能关键——书中 ETF 数据批量导入核心
- `elasticsearch-dsl` 提供 Pythonic 链式 API——但灵活性不如 raw DSL
- 异步生态在 7.0 时代尚不成熟——2024 后已完善

## 核心概念速览（中英对照）

1. **elasticsearch-py** — Elastic 官方 Python 客户端库，封装 REST API
2. **helpers.bulk** — 批量索引辅助函数，自动分块 + 错误收集
3. **streaming_bulk** — 流式批量处理——生成器模式，内存友好
4. **scan** — scroll 遍历的 Python 封装，迭代全量匹配文档
5. **elasticsearch-dsl** — 高层 Python DSL 库，链式构建查询/聚合
6. **Connection Pool** — urllib3 连接池复用，支持多节点 round-robin
7. **Body 参数** — 搜索/索引请求的 JSON 请求体——Python dict 直接传递
8. **TransportError** — 客户端异常层级：ConnectionError / NotFoundError / ConflictError
9. **Sniffing** — 自动发现集群节点列表并维护连接池
10. **chunk_size** — bulk 每批次文档数——影响内存与吞吐平衡
11. **scroll** — 深分页迭代——`_search?scroll=5m` + `_scroll` 游标
12. **Aiohttp** — 异步 HTTP 引擎——elasticsearch-py 7.x 实验性异步支持

## 最新演进与工业实践

- **8.x elasticsearch-py**：客户端 API 重构——`es.search(index=..., query=...)` 扁平参数替代 `body={}`；类型注解完善；官方支持 async（`elasticsearch.AsyncElasticsearch` 基于 `aiohttp`）。版本兼容性：client 8.x ↔ server 8.x/9.x
- **ES|QL Python**：9.x 客户端支持 `es.query_esql(query="FROM idx | WHERE ...")`——管道语言 Python 绑定
- **工业实践**：数据分析场景 pandas 生态更倾向 `esdf`（elasticsearch dataframes）或直接 `pandas.read_sql()` on SQL connector；ML 管道场景（ELSER embedding → index）倾向 elasticsearch-py 的 `es.inference.put_trained_model()` API
- **社区替代**：`esclientlib`（async，已停更）、`async-elasticsearch`（第三方，8.x 后官方 async 成熟后退出）
