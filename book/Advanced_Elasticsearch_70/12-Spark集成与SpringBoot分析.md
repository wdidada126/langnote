# Spark 集成与 Spring Boot 分析（原书 Ch17–18）

> ⚠️ 主题重构：Ch17 代码目录 `eshadoop` + `eshadoop_docker`（elasticsearch-hadoop 连接器 + Docker 环境），Ch18 代码目录 `sprintboot-es-analytics`（Spring Boot 项目）。两章合并——大数据栈与 Web 框架两条集成路线。

## 1. elasticsearch-hadoop 连接器（Ch17）

`elasticsearch-hadoop`（现名 `elasticsearch-spark`）将 ES 索引暴露为 Spark/Hadoop RDD/DataFrame 数据源。

### 核心概念

- ES 索引 ↔ HDFS 文件的双向映射：每个 shard 视为一个"文件分片"
- 读写通过 Hadoop InputFormat/OutputFormat API——Spark 的 `sc.newAPIHadoopRDD()`
- EsSpark 封装：`fromElasticsearch(sc, "cfg")` → RDD[Writable]

### PySpark 示例

```python
# elasticsearch-spark 3.x (对应 ES 7.x) ⚠️ 转述
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETF Analysis") \
    .config("es.nodes", "localhost") \
    .config("es.port", "9200") \
    .config("es.index.auto.create", "true") \
    .getOrCreate()

# Read from ES
rdd = spark.sparkContext.newAPIHadoopRDD(
    inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf={"es.resource": "cf_etf/_doc"}
)

# Write to ES
spark.sparkContext.parallelize([
    {"symbol": "SPY", "name": "S&P 500 ETF", "price": 330.5}
]).saveNewEsHadoopDataset({"es.resource": "cf_etf/_doc"})
```

### Docker 环境

书中 `eshadoop_docker` 目录提供 ES + Spark + Hadoop 的 Docker Compose 编排——快速搭建本地 Spark-ES 联调环境。

## 2. elasticsearch-spark DataFrame 模式

```scala
// Scala ⚠️ 转述
val spark = SparkSession.builder()
    .config("es.nodes", "localhost:9200")
    .getOrCreate()

// Read DataFrame
val df = spark.read.format("org.elasticsearch.spark.sql")
    .load("cf_etf/_doc")

df.createOrReplaceTempView("etf")
val result = spark.sql(
    "SELECT category, AVG(price) FROM etf GROUP BY category ORDER BY 2 DESC"
)

// Write DataFrame to ES
result.write.format("org.elasticsearch.spark.sql")
    .option("es.resource", "etf_stats/_doc")
    .mode("append")
    .save()
```

- 自动推断 DataFrame schema → ES mapping（或反向）
- `pushdown` 参数：`es.pushdown` = true 时 Spark 谓词下推到 ES query/filter——减少网络传输

## 3. 适用场景

| 场景 | 说明 |
|---|---|
| 离线聚合分析 | Spark 做复杂 ML/统计 → 结果写回 ES 供 Kibana 展示 |
| 数据管道 | HDFS/S3 → Spark 转换 → ES 索引 |
| 日志富化 | Spark JOIN 维表 → 写回 ES |
| 搜索增强 | Spark ML 算相关性分 → 存回 ES → ES function_score 用 |

## 4. Spring Data Elasticsearch（Ch18）

`sprintboot-es-analytics` Spring Boot 项目——Spring Data ES 提供声明式 Repository 模式：

```java
// Entity ⚠️ 转述
@Document(indexName = "cf_etf")
public class Etf {
    @Id private String symbol;
    @Field(type = FieldType.Text, analyzer = "english") private String name;
    @Field(type = FieldType.Double) private Double price;
    @Field(type = FieldType.Keyword) private String category;
    @Field(type = FieldType.Keyword) private String fundFamily;
}

// Repository
public interface EtfRepository extends ElasticsearchRepository<Etf, String> {
    List<Etf> findByNameContaining(String keyword);
    List<Etf> findByCategoryAndPriceGreaterThan(String cat, Double min);
}
```

- `@Document` → ES mapping 自动映射
- `@Field` → 字段类型/分析器声明
- `ElasticsearchOperations` → 低层操作（search/save/bulk）
- `CriteriaQuery` / `NativeSearchQueryBuilder` → 复杂查询构建

## 5. Spring Boot 配置

```yaml
# application.yml ⚠️ 转述
spring:
  elasticsearch:
    rest:
      uris: http://localhost:9200
      connection-timeout: 5s
      read-timeout: 30s
```

- Spring Data ES 3.x 底层使用 HLRC（对应 ES 7.x）——5.x 后切到 Java API Client（8.x）
- 自动 mapping：启动时 `ElasticsearchRepository` 扫描 `@Document` 类 → 创建索引+mapping

## 6. 🔧 类比说明

- Spark 谓词下推 ≈ SQLite `EXPLAIN QUERY PLAN` 中 `SEARCH TABLE USING INDEX`——减少扫描量；非 ES 行为
- Spring Data `@Document` 声明 ≈ SQLite `CREATE TABLE` schema——非 ES 行为
- `pushdown` 机制概念类比 DuckDB 的 `PRAGMA enable_object_cache` 远程文件谓词下推——非 ES 行为

## 7. 本章要点

- elasticsearch-hadoop 是"离线计算→在线存储"的管道——Spark ML 结果回写 ES 是经典模式
- `es.pushdown` 是性能关键——无下推时全索引扫描回 Spark 再过滤
- Spring Data ES 提供"JPA 风格"的声明式 ES 访问——快速构建 CRUD 微服务
- 7.0 时代 elasticsearch-hadoop 与 Spark 版本矩阵严格对应——书中 Spark 2.4/ES 7.0 搭配
- Ch17+18 合计构成"ES 不是孤岛"的全景——上游 Spark/批处理，下游 Spring/实时 Web

## 核心概念速览（中英对照）

1. **elasticsearch-hadoop** — ES↔Hadoop/Spark 连接器：InputFormat/OutputFormat 双向读写
2. **EsSpark** — elasticsearch-hadoop Spark 封装：`fromElasticsearch`/`saveToElasticsearch`
3. **谓词下推** — Pushdown：将 Spark filter 转化为 ES query/filter，减少数据传输
4. **DataFrame 模式** — `org.elasticsearch.spark.sql` 格式：自动 schema 推断
5. **Spring Data Elasticsearch** — Spring 框架 ES 数据访问抽象层，`@Document` 声明映射
6. **ElasticsearchRepository** — Spring Data Repository 接口：CRUD + 查询派生方法
7. **@Document** — Spring Data ES 注解：声明实体与 ES 索引映射关系
8. **@Field** — Spring Data ES 注解：字段类型/分析器指定
9. **CriteriaQuery** — Spring Data ES 查询构建器：链式条件组合
10. **NativeSearchQueryBuilder** — 原生 DSL 包装器：复杂查询/聚合逃生舱
11. **InputFormat / OutputFormat** — Hadoop MapReduce API：ES 数据源/目标的底层接口
12. **es.resource** — 核心配置参数：指定 `index/type`（7.0 后 `index/_doc`）读写目标

## 最新演进与工业实践

- **elasticsearch-spark 8.x/9.x**：连接器更名 `elasticsearch-spark`（去掉 hadoop 后缀）——对应 ES 8.x+、Spark 3.x。版本矩阵：https://www.elastic.co/guide/en/elasticsearch/hadoop/current/install.html ⚠️ 路径推定。`es.pushdown` 默认 true（8.x 起）
- **Spark 生态变化**：2026 年 Spark Structured Streaming + Delta Lake/Iceberg 成主流湖仓——ES 作为 sink 的场景缩减为"搜索索引"而非通用分析——日志场景转 ClickHouse/DuckDB 做 OLAP、ES 做全文检索
- **Spring Data ES**：Spring Data 2024.0（4.x）底层已切到 Java API Client（`co.elastic.clients`），不再用 HLRC；`@Document` 注解体系不变；Spring Data 5.x 支持 ES 8.x/9.x——书中 Spring Boot 2.x/ES 7.x 组合已过时
- **工业实践**：Spark→ES 模式在"批量特征工程→在线搜索"管道中仍活跃（如电商推荐：Spark 算 i2i 向量→ES dense_vector 索引→kNN 搜索）；Spring Data ES 在 Java 微服务 CRUD 场景存活率最高——日志/可观测性场景倾向直接 ES Java Client + 定制层
- **替代方案**：Kafka Connect Elasticsearch Sink（轻量）、Debezium CDC → ES（实时同步）、Logstash JDBC input（定时拉取）——Spark 方案适合"重计算+批量写"，轻量场景转上述替代
