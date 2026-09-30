# Ingest 管道与探索性分析（原书 Ch9–10）

> ⚠️ 主题重构：Ch9 代码 `ingest_pipeline`，Ch10 代码 `exploratory_data_analysis` + `business_analytics.xlsx`。两章合并——pipeline 预处理数据、EDA 分析数据，构成"写入→分析"闭环。

## 1. Ingest Pipeline 架构

ES 7.0 Ingest Node 在索引/更新前执行处理器链（Processor Chain），将数据转换逻辑从应用侧下沉到 ES 集群。

```
客户端 → Ingest Node → [Processor 1 → Processor 2 → … → Processor N] → Indexing Node
```

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/ingest.html ✅ 200

## 2. 常用处理器（Processors）

| 处理器 | 功能 | 典型场景 |
|---|---|---|
| `set` | 设字段值 | 添加计算字段/默认值 |
| `remove` | 删字段 | 脱敏/省空间 |
| `rename` | 重命名字段 | schema 演进 |
| `convert` | 类型转换 | string→long/date |
| `date` / `date_index_name` | 日期解析 | 时间字段标准化 |
| `grok` | 正则模式提取 | 非结构化日志解析 |
| `split` | 分隔字符串为数组 | CSV 字段拆分 |
| `join` | 数组拼接为字符串 | 标签合并 |
| `script` | Painless 脚本 | 复杂条件逻辑 |
| `foreach` | 遍历数组元素执行子处理器 | 批量字段处理 |
| `append` | 追加值到数组字段 | 标签追加 |
| `geoip` | IP→地理位置 | 访问日志地理化 |
| `user_agent` | UA 解析 | 浏览器/OS/设备分类 |

## 3. Pipeline 定义与使用

```json
// PUT _ingest/pipeline/etf_enrich
{
  "description": "Enrich ETF data",
  "processors": [
    { "convert": { "field": "price", "type": "float" } },
    { "script": {
        "source": "ctx.price_change_pct = (ctx.price - ctx.prev_close) / ctx.prev_close * 100"
    }},
    { "remove": { "field": "internal_id", "ignore_missing": true } }
  ]
}
```

使用方式：
1. 索引时指定：`POST /cf_etf/_doc?pipeline=etf_enrich`
2. 设为默认：`PUT /cf_etf/_settings { "index.default_pipeline": "etf_enrich" }`
3. reindex 时触发：`POST _reindex { ... "pipeline": "etf_enrich" ... }`

## 4. Painless 脚本（Ch9 隐含）

ES 7.0 内置 Painless 脚本语言（Java-like 语法，白名单沙箱安全）：
- 可用位置：Ingest Processor、Update Script、Query `script_score`、Aggregation `script`
- 书中 Ch9 `ingest_pipeline` 代码含 script processor 示例

## 5. 探索性数据分析（EDA）场景

Ch10 `exploratory_data_analysis` + `business_analytics.xlsx`——用聚合 + Kibana 做 ETF 市场数据探索：

- **单字段分布**：`terms`（fund_family 分布）、`histogram`（price 分布）
- **时间序列**：`date_histogram` + `avg(price)` + `moving_avg` 趋势线
- **交叉分析**：`terms(category)` → 嵌套 `avg(price)` + `stats(volume)`
- **异常发现**：`percentiles(price, [1, 5, 95, 99])` 检测极端值
- **相关性探索**：多字段 `script` 打分 + `top_hits` 返回样本

## 6. 🔧 类比演示（非 ES 行为）

**G5：Analyzer Pipeline 类比 Ingest Pipeline**

FTS5 tokenizer chain（`porter unicode61`）≈ Ingest Pipeline 中的 `lowercase` + `stemmer` 处理器——都在数据入库前做转换。区别：
- FTS5 仅文本转换（不可改字段/做脚本）；ES Ingest 可跨字段计算、查外部 API（geoip）
- **非 ES 行为**

**G3：SQL 数据清洗 vs Ingest Pipeline**

```sql
-- DuckDB 类比：入库前转换
INSERT INTO target
SELECT
  CAST(price AS DOUBLE),
  (price - prev_close) / prev_close * 100 AS change_pct,
  id AS symbol
FROM source
WHERE internal_id IS NOT NULL;
```

DuckDB/SQLite 的入库转换靠 SQL INSERT-SELECT 或 trigger——ES Ingest Pipeline 是声明式处理器链，不需要写 SQL。**非 ES 行为**。

## 7. 本章要点

- Ingest Pipeline 将 ETL 逻辑下沉到 ES 集群——减少应用侧代码
- grok + geoip + user_agent 是日志场景的三大处理器
- script processor 是万能胶水——但性能需关注（Painless 编译缓存）
- EDA 实操 = 聚合框架（Ch8）的场景应用
- Logstash（Ch13）是 pipeline 的上游生态——两者功能有重叠但定位不同

## 核心概念速览（中英对照）

1. **Ingest Node** — ES 集群中专门执行预处理管道的节点角色（或 co-node 功能）
2. **Pipeline** — 有序处理器链，在文档索引/更新前执行转换
3. **Processor** — 管道中的最小处理单元（set/grok/date/script…）
4. **Painless** — ES 内置脚本语言，Java-like 语法 + 白名单安全沙箱
5. **Grok** — 基于命名正则模式的日志解析处理器
6. **GeoIP** — IP→地理位置富化处理器（MaxMind GeoLite2 数据库）
7. **default_pipeline** — 索引级默认管道设置，无需每次请求指定
8. **final_pipeline** — reindex 操作时的管道覆盖（与 default_pipeline 互补）
9. **EDA** — Exploratory Data Analysis：无预设假设地用聚合探索数据结构
10. **Script Processor** — 用 Painless 脚本实现任意条件逻辑的处理器
11. **Foreach Processor** — 遍历数组字段对每个元素执行子处理器
12. **On Failure** — 管道级/处理器级失败处理路径（类似 try-catch）

## 最新演进与工业实践

- **ES 8.x/9.x**：Ingest Pipeline 核心不变——新增 `inference` 处理器（调用 ML 模型做文本分类/回归/embedding，8.0+）；`reroute` 处理器（8.9+，按文档内容路由到不同索引）。`on_failure` 机制成熟
- **Elastic 可观测性栈**：Logs/APM/Metrics 全走 ingest pipeline 预处理——书中"手动 pipeline"已升级为 Elastic Agent + Fleet 自动管理
- **工业实践**：日志场景 Logstash 与 Ingest Node 的选择标准——Logstash 适合"复杂转换+外部缓冲"；Ingest Node 适合"索引侧轻量富化"。2024 后 Elastic Agent 统一采集层，Logstash 角色缩减
- **经典参考**：Elastic 官方 Ingest Node 文档 https://www.elastic.co/guide/en/elasticsearch/reference/7.17/ingest.html ✅ 200；7.17 文档页在 2026 仍在线但标记 EOL（2026-02 EOL 公告 ⚠️）
