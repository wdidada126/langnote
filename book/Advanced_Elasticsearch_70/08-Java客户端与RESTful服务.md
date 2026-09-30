# Java 客户端与 RESTful 服务（原书 Ch11+14）

> ⚠️ 主题重构：Ch11 代码目录 `java_rest_client`（JDK 8），Ch14 代码含 Maven 项目 + `java_rest_client` 子目录。两章合并——Ch11 介绍 HLRC 基础，Ch14 升级为 RESTful 服务。

## 1. ES 7.0 Java 客户端谱系

7.0 时代 Java 客户端：
- **TransportClient**（已废弃，7.x 删除）——书中基线不再使用
- **Low Level REST Client**——HTTP 封装，手动 JSON 序列化
- **High Level REST Client (HLRC)**（`org.elasticsearch.client.RestHighLevelClient`）——7.0 推荐，类型化 API，Builder 模式构建请求

官方文档：https://www.elastic.co/guide/en/elasticsearch/client/java-rest/7.17/index.html（⚠️ 7.17 路径推定，可能已调整）

## 2. HLRC 核心用法

```java
// Ch11 典型代码 ⚠️ 转述
RestHighLevelClient client = new RestHighLevelClient(
    RestClient.builder(new HttpHost("localhost", 9200, "http"))
);

// Index
IndexRequest request = new IndexRequest("cf_etf").id("SPY")
    .source(Map.of("symbol","SPY","name","S&P 500 ETF","price",330.5));
IndexResponse response = client.index(request, RequestOptions.DEFAULT);

// Search
SearchRequest searchRequest = new SearchRequest("cf_etf");
SearchSourceBuilder source = new SearchSourceBuilder()
    .query(QueryBuilders.multiMatchQuery("vanguard", "name", "fund_family"))
    .size(10)
    .aggregation(AggregationBuilders.terms("by_category").field("category"));
searchRequest.source(source);
SearchResponse searchResponse = client.search(searchRequest, RequestOptions.DEFAULT);
```

- Bulk Processor：`BulkProcessor` 类自动缓冲+定时 flush——写入性能关键
- Scroll API：深分页遍历——`client.searchScroll()`

## 3. Ch14：构建 RESTful 服务

Ch14 Maven 项目将 HLRC 封装为 Spring MVC / JAX-RS RESTful API 层：

```
客户端 HTTP → REST Controller → Service Layer → HLRC → ES Cluster
```

- 典型端点：`GET /api/etf/search?q=xxx` → 内部转 ES `multi_match`
- 错误处理：ES `version_conflict` → HTTP 409；`index_not_found` → 404
- 配置：ES 连接池、超时、重试在 `application.yml` / Maven `pom.xml` 声明

## 4. Bulk 写入最佳实践（Java）

| 参数 | 建议值 | 说明 |
|---|---|---|
| `bulkSize` | 1000–5000 docs | 单次 bulk 条目数 |
| `flushInterval` | 5s | 定时 flush（不管 size） |
| `backoffPolicy` | exponential | 429 限流重试 |
| `concurrentRequests` | 1–2 | 同时在途的 bulk 数 |

## 5. 连接管理与安全

- `RestClient` 内部用 Apache HttpClient——连接池复用
- 7.0 默认无认证；生产配 `CredentialsProvider` + TLS（`https`）
- `RequestOptions.DEFAULT` 可覆盖 per-request 超时/headers

## 6. RESTful 服务层设计模式（Ch14）

书中 Ch14 项目结构（Maven + Java）展示的架构层：

```
HTTP Client → [Spring MVC / JAX-RS Controller]
                  → Service Layer (业务逻辑)
                    → HLRC (ES 操作封装)
                      → ES Cluster
                  ← JSON Response ← SearchResponse ← ES
```

- **DTO 转换**：ES `_source` JSON → Java POJO（Jackson/Gson 反序列化）→ API Response DTO
- **错误映射**：ES `ElasticsearchStatusException` → HTTP 4xx/5xx + 结构化错误体
- **分页**：`from + size`（浅分页）/ `search_after`（深分页）——`from+size` 受 `max_result_window` 限制（默认 10000）
- **聚合透传**：ES aggregations JSON → API Response 的 `meta`/`facets` 字段——前端 Kibana 替代方案

⚠️ 原书 Ch14 细节转述自代码目录结构推断。

## 7. Scroll API 深分页（Java）

```java
SearchScrollRequest scroll = new SearchScrollRequest(scrollId);
scroll.scroll(TimeValue.timeValueMinutes(5));
SearchResponse response = client.searchScroll(scroll, RequestOptions.DEFAULT);
```

- 首次 `search` 带 `scroll=5m` → 返回 `scroll_id`
- 逐批 `searchScroll` 直到 `hits.hits` 为空
- **注意**：scroll 上下文有 TTL 且占内存——导出全量用 PIT（Point in Time，7.10+）替代

## 8. 🔧 类比说明

本章为 Java 生态集成——无 SQLite/DuckDB FTS5 直接类比点。但 Bulk 写入模式可类比 SQLite `PRAGMA journal_mode=WAL` + `BEGIN; INSERT; COMMIT` 批量事务（非 ES 行为）。

## 9. 本章要点

- HLRC 是 7.0 时代 Java 开发首选——8.x 后被新 Java Client（`co.elastic.clients.elasticsearch`）替代
- Ch14 的 RESTful 服务封装是"ES 作为后端存储"的典型架构——应用层不暴露 ES 原始 API
- Bulk Processor 配置直接影响索引吞吐——书中 ETF bulk 数据导入场景

## 核心概念速览（中英对照）

1. **HLRC** — High Level REST Client：ES 7.0 推荐的 Java 类型化客户端，Builder API
2. **Low Level REST Client** — HTTP 基础封装，手动 JSON 序列化，跨版本兼容
3. **TransportClient** — 旧版 TCP 层客户端（7.0 已废弃）
4. **BulkProcessor** — HLRC 内置批量写入处理器，自动缓冲/定时 flush/重试
5. **RestHighLevelClient** — HLRC 核心类，extends AbstractClient
6. **SearchSourceBuilder** — 搜索请求构建器：query + aggs + sort + size
7. **QueryBuilders** — 静态工厂类：termQuery/matchQuery/boolQuery 等
8. **AggregationBuilders** — 聚合构建器：terms/avg/dateHistogram 等
9. **Scroll API** — 深分页遍历——保留搜索上下文，逐批返回
10. **JAX-RS / Spring MVC** — Java RESTful Web 服务框架，Ch14 封装层
11. **RequestOptions** — 客户端级请求配置（超时/headers）
12. **Connection Pool** — HttpClient 连接池复用，避免频繁 TCP 握手

## 最新演进与工业实践

- **8.x Java API Client**（`co.elastic.clients`）：HLRC 于 7.16 废弃、8.0 彻底替代——新客户端基于 Jackson/JSON 而非 ES 内部类型，类型安全 + 序列化性能更好（https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/index.html ⚠️ 推定 URL）
- **9.x**：Java API Client 持续演进——ES|QL 查询支持加入；HLRC 已无维护
- **Spring Data Elasticsearch**：Ch18 详述——但 Spring Data 5.x（2023）底层已切换到 Java API Client，不再用 HLRC
- **工业实践**：Java 微服务访问 ES 的标准 = Spring Data ES（高层抽象）或 Java API Client（精确控制）；Ch14 的"手写 RESTful 包装"模式在 2026 已被 API Gateway + ES 安全层取代——直接暴露 ES API 的做法减少
