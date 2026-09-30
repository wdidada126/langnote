# 搜索 API 与相关性（原书 Ch6）

> ⚠️ 主题重构：Ch6 代码 `search_api` 含 suggester bulk、custom analyzer 配置、`cf_etf_view.json`（ETF 搜索视图）。

## 1. Search API 请求结构

ES 搜索请求 = REST 路径 + 请求体（Query DSL JSON）：
- 简单：`GET /cf_etf/_search?q=etf&size=10`
- 完整（Request Body）：`POST /cf_etf/_search` + JSON body

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/search-request-body.html ✅ 200

## 2. Query DSL 核心查询

### 叶子查询（Leaf Clause）

| 查询 | 字段类型 | 语义 |
|---|---|---|
| `match` | text | 分词后 OR 查——全文检索主力 ✅ https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-match-query.html |
| `term` | keyword | 精确值——不过 analyzer |
| `range` | date/numeric | 范围过滤 |
| `prefix` | keyword/text | 前缀匹配 |
| `wildcard` | keyword/text | `*`/`?` 通配 |
| `regexp` | keyword/text | 正则匹配 |
| `geo_distance` | geo_point | 球形距离 |
| `ids` | `_id` | 按文档 ID |

### 复合查询（Compound）

`bool` 查询四种子句：`must`（AND + 打分）、`filter`（AND + 不打分）、`should`（OR + 加分）、`must_not`（NOT + 不打分）。

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-bool-query.html ✅ 200

## 3. multi_match 与跨字段搜索

书中 ETF 场景：用户输入 "vanguard total" 应同时搜 `name` 和 `fund_family` 字段。

```json
{
  "multi_match": {
    "query": "vanguard total",
    "fields": ["name^3", "fund_family"],
    "type": "best_fields"
  }
}
```

- `best_fields`（默认）：取最佳字段得分——适合至少一个字段高度匹配
- `most_fields`：多字段得分求和——适合同一查询分散在多字段
- `cross_fields`：多字段视为一个字段——适合同义词跨字段
- `phrase`/`phrase_prefix`：短语级匹配

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-multi-match-query.html ✅ 200

## 4. 相关性调优：Boost、Rescore、Function Score

- 字段级 boost：`"fields": ["name^3", "fund_family^1"]`（`^` 权重乘 BM25 得分）
- 查询级 boost：`"boost": 2`
- Rescore：对 top N 结果用更昂贵的打分重新排序——书中场景：初筛 top 50 → rescore 精排 top 10

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/search-request-rescore.html ✅ 200

- Function Score：组合衰减函数（`gauss`/`linear`/`exp`）+ `field_value_factor` + `script_score`——地理距离衰减、时间衰减的经典方法

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-function-score-query.html ✅ 200

## 5. Suggesters（建议器）

书中 Ch6 代码含 `cf_etf_suggester_bulk.json` + `cf_etf_suggester_mappings.json`——completion suggester 或 term suggester 示例。

- **Completion Suggester**：用 FST（有限状态转换机）前缀补全——`suggest` 请求体，需 mapping 中声明 `completion` 类型字段
- **Term Suggester**：编辑距离（Levenshtein）拼写纠错
- **Phrase Suggester**：词对词纠错
- **Context Suggester**：补全 + 过滤（如按地区/语言）

## 6. 🔧 类比演示（非 ES 行为）

**G2：bm25() 字段权重 vs ES boost**（SQLite FTS5）

FTS5 `bm25(docs, 10.0, 1.0)` 中第一个权重（10.0）= title 字段权重，类比 ES `name^3`。两者均基于 BM25 公式的线性加权变体。区别：
- ES BM25 默认参数 `k1=1.2, b=0.75` 可调（`similarity` 设置）；FTS5 BM25 不可调
- ES 支持 `function_score` 衰减函数；FTS5 仅 bm25()/rank()
- **非 ES 行为**

**G1 补充：FTS5 trigram 子串搜索 vs ES ngram**

```python
# FTS5 trigram 子串匹配
conn.execute("CREATE VIRTUAL TABLE trigram_test USING fts5(body, tokenize='trigram')")
conn.execute("INSERT INTO trigram_test VALUES('elasticsearch distributed')")
r = conn.execute("SELECT * FROM trigram_test WHERE trigram_test MATCH 'lastre'").fetchall()  # 子串命中
```

- ES `ngram`/`edge_ngram` token filter 实现部分匹配（`partial matching`）——FTS5 trigram tokenizer 是近似机制，非等价

## 7. 本章要点

- Query DSL 是 ES 搜索的"SQL"——bool 组合 + 叶子查询覆盖 90% 场景
- `match` vs `term` 是经典面试题：前者经 analyzer 分词，后者直接查倒排
- `multi_match` type 选择（best_fields/cross_fields）对结果影响大
- TDG [../Elasticsearch_The_Definitive_Guide/08-相关性实战与精确值搜索.md](../Elasticsearch_The_Definitive_Guide/08-相关性实战与精确值搜索.md) 的 TF-IDF→BM25 演进是概念基础

## 核心概念速览（中英对照）

1. **Query DSL** — 基于 JSON 的结构化查询语言，ES 搜索的核心接口
2. **bool 查询** — 复合查询：must/filter/should/must_not 四种子句组合
3. **match 查询** — 文本字段分词后查询——默认 OR 语义，可 operator=and
4. **term 查询** — 精确值查询，不分词，keyword 字段专用
5. **multi_match** — 跨字段搜索，type 参数控制打分策略
6. **BM25** — Best Matching 25：TF-IDF 改进的概率检索模型，ES 5.0+ 默认相似度算法
7. **boost** — 查询/字段权重乘数，线性缩放得分
8. **Rescore** — 初筛后对 top N 精排，二次打分
9. **function_score** — 函数打分组合（衰减函数/脚本/字段值因子）
10. **Completion Suggester** — FST 前缀补全器，mapping 需 `completion` 类型
11. **Phrase Prefix** — 短语前缀查询，match_phrase_prefix
12. **_search 端点** — POST /idx/_search + Request Body，7.0 标准搜索入口

## 最新演进与工业实践

- **ES 8.x Retrievers + RRF**：8.9+ 引入 `retrievers` 抽象（`standard`/`rrf`/`knn`），RRF（Reciprocal Rank Fusion）混合 BM25 + 向量检索——搜索排序从"纯词法"扩展到"语义+词法"混合。书中 boost/rescore 思路仍适用
- **ES|QL 查询**：`FROM idx | WHERE MATCH(field, "query") | SORT _score DESC | LIMIT 10`（9.0 GA）——Query DSL 仍是主力但管道语言提供新选项
- **ELSER（Elastic Search with Learned Sparse Encodings）**：Elastic 自有稀疏向量模型（8.8+），将文本转为加权 token 向量——搜索相关性扩展到语义层
- **工业实践**：搜索质量工程 = 召回（analyzer/查询类型）→ 粗排（BM25+boost）→ 精排（Learning to Rank/XGBoost 模型）——书中 boost/rescore/function_score 对应粗排-精排衔接层
- **经典论文**：Robertson & Zaragoza 2009 "The Probabilistic Foundation of BM25" 是理解 ES 打分的根基；TF-IDF 经典 Salton & Buckley 1988（⚠️ DOI 未核验，以标题引用）
