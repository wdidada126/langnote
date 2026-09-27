# 08 在 Presto 中使用 SQL

> 原书第 8 章（中译本 p.115–147）。定位：Presto 的 DDL/DML/查询语法面总览——"SQL-on-Anything" 的方言实况。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 8.1 语句 | 语句分类与 SHOW/DESCRIBE 族 | 自省语法是方言课第一课 |
| 8.2 系统表 | `system.runtime/node`、catalog 元数据表 | 引擎把自省做成表 |
| 8.3–8.5 catalog/schema/Information Schema | 三层命名空间与标准元数据视图 | `information_schema.columns` 是考古铲 |
| 8.6 表 | 列属性、CTAS、复制表、ALTER、DROP、连接器限制 | 建表语义=连接器能力的投影 |
| 8.7 视图 | CREATE/DROP VIEW，无物化 | 视图仅存查询文本 |
| 8.8 会话信息与配置 | SHOW SESSION/SET SESSION/RESET | 参数三级：系统/会话/查询 |
| 8.9 数据类型 | 数值/布尔/变长/datetime/二进制；集合（ARRAY/MAP/ROW）；时态；类型转换 | 类型面=函数面（9 章）的地基 |
| 8.10–8.15 查询主干 | SELECT/WHERE/GROUP BY+HAVING/ORDER BY+LIMIT/JOIN/UNION-INTERSECT-EXCEPT | ANSI 正统，反引号/隐式转换都不惯你 |
| 8.16 分组操作 | GROUP BY CUBE/ROLLUP/GROUPING SETS | 多维聚合一语句成型 |
| 8.17 WITH / 8.18 子查询 | CTE 与标量/EXISTS/集合比较三类子查询 | 可读性优先；物化由优化器决定 |
| 8.19 删除数据 | DELETE 的支持面 | 写侧语义按连接器天差地别 |

## 精讲

### 1. 命名空间与自省的"三层带表"
```text
catalog（连接器实例）
└── schema（源库/库/命名空间）
    └── table（表/视图/源对象映射）
系统层： system.runtime.queries / system.runtime.nodes（运行态）
元数据层： information_schema.schemata|tables|columns（结构态，跨 catalog 统一视图）
函数层：  show functions / describe function（方言面）
```
- `DESCRIBE`/`SHOW CREATE TABLE`/`EXPLAIN` 三件套构成日常"读引擎心智"的入口（8.1+4 章联动）；
- 与 MySQL `information_schema` 的体感差异：Presto 的元数据**实时回源**（尤其 Hive metastore/JDBC），
  无本地副本 → 元数据服务抖动会直接表现为查询报错（第 6 章连接器依赖链）。

### 2. CTAS 是全章枢纽（8.6.2/8.6.3）
```sql
CREATE TABLE hive.dwd.agg_orders
WITH (format='PARQUET', partitioning=ARRAY['day_bucket']) AS
SELECT ..., day FROM mysql.sales.orders;
```
- 一语句完成"跨源读+转换+湖内落地"，`WITH` 属性面**全部透传给连接器**：
  format/partitioning 仅对支持它们的连接器有意义（8.6.6 的限制清单在此生效）；
- 这也是 7.7 轻量 ETL 与 12.2 调优（先收敛再 Join）的执行载体；
- ⚠️ 属性名/取值随发行版与表格式（Hive 表 vs Iceberg 表的 `partitioning`/`write.format` 语义不同）核对。

### 3. 类型系统的两个深坑（8.9）
- **隐式转换保守**：字符串与数值比较会报错而非悄悄转换（对 Hive 老习惯是纠错）——显式 `CAST` 是唯一正道；
- **时态族**：`DATE/TIME/TIMESTAMP/TIMESTAMP(p) WITH TIME ZONE/INTERVAL`，
  `timestamp` 存微秒、时区语义到函数级（`AT TIME ZONE`）——跨源对账错位十有八九出在这里；
- 集合三件套 ARRAY/MAP/ROW 与解嵌套（`UNNEST`，9.14 展开）是 Presto SQL 区别于多数方言的"表达力护城河"。

### 4. 分组操作与窗口的前置（8.16）
`GROUP BY CUBE(a,b)/ROLLUP(a,b)/GROUPING SETS((a),(b))` + `GROUPING()` 判 NULL 语义，
一语句产出多维小计——BI 预聚合不足时的交互式替代；代价是数据翻倍级膨胀，
配合 4.9.4 局部聚合理解其执行形态。**当代对照**：湖上等价物是 Iceberg/Paimon 的聚合演进治理，见
[../Apache_Paimon_Streaming_Lakehouse/06-合并引擎.md](../Apache_Paimon_Streaming_Lakehouse/06-合并引擎.md)（aggregation merge engine）。

### 5. DML 现实检查（8.19）
- INSERT/CTAS 相对普适；**UPDATE/DELETE 仅部分连接器**（Hive 表有限、Iceberg 依赖格式版本与连接器实现）；
- 书中 DELETE 演示的克制是对的：把"湖上更新"当成表格式层的问题（2021 年时点），与互链湖格式笔记一致。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| Presto SQL≈HiveQL | ANSI 严格得多：双引号标识符、无隐式串转数、ORDER BY 需 LIMIT（部分版本可放开 ⚠️） |
| CREATE TABLE 建的是本地表 | 建的是**源系统对象**；连接器不支持则报错或忽略属性（8.6.6） |
| WITH 子句会物化 | 默认内联展开；要物化就 CTAS 落表 |
| 视图能加速 | 视图零物化零缓存，纯命名；加速靠湖内实体化或上层缓存（11.2 RubiX 语境） |

## 与其他章/其他笔记的联系
- 函数与表达式细节 → [09-高级SQL特性.md](09-高级SQL特性.md)；执行形态 → [04-Presto的架构.md](04-Presto的架构.md)；
- 跨源物化 → [07-高级连接器实例.md](07-高级连接器实例.md) 7.6/7.7；
- SQL 方言与 ANSI 谱系 → [../SQL系列·总索引.md](../SQL系列·总索引.md)、[../SQL沉思录.md](../SQL沉思录.md)；
- MySQL 信息结构对照 → [../MySQL必知必会.md](../MySQL必知必会.md)、[../高性能mysql.md](../高性能mysql.md)。

## 本章小结与行动清单

三句话带走：
1. Presto 的 DDL 语义="在源系统里做对象"，任何 `CREATE/ALTER/DROP` 的行为最终由连接器+表格式决定——
   背语法前先背支持矩阵（8.6.6）；
2. 自省三件套（information_schema / SHOW / EXPLAIN）+系统表构成日常工作的 80%；
3. 类型与空值的保守 ANSI 语义是**纠错型设计**：从 Hive 迁移时报的每个错，都是未来线上事故的一次预付。

建表评审模板（湖上新表立项必填）：
- [ ] 目标 catalog/表格式（Hive 表还是 Iceberg 表？v1/v2？）与 `WITH` 属性逐条对应（06/08 联动）；
- [ ] 分区/分布策略：高频谓词列是否进剪裁路径（06.4 分区纪律）；
- [ ] 下游 DML 形态有无 UPDATE/DELETE？（支持面按连接器与格式版本核对 ⚠️）
- [ ] CTAS 来源是否跨源？跨源则按 7.6 检查单加一轮 Exchange 预算；
- [ ] 命名进公共命名空间评审（catalog/schema 名是 API，02 章纪律）。

自测：
- [ ] 视图与 CTAS 的选择判据一句话？（复用频率×新鲜度要求）
- [ ] `GROUPING SETS` 的成本结构？（输出膨胀×聚合两阶段执行形态）

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 三段式命名 | Three-part Naming | catalog.schema.table 的对象寻址 |
| 信息模式 | Information Schema | 跨源统一的元数据视图族 |
| 系统表 | System Tables | `system.runtime.*` 等引擎自省表 |
| CTAS | CREATE TABLE AS SELECT | 查询结果落地为新表（跨源物化枢纽） |
| 表属性 | Table Properties | WITH 子句透传连接器的 format/partitioning |
| 视图 | View | 仅存查询文本的逻辑表，无物化 |
| 会话属性 | Session Properties | SET SESSION 级参数调节 |
| 时态类型 | Temporal Types | DATE/TIME/TIMESTAMP/INTERVAL 及其时区语义 |
| 集合类型 | Nested Types | ARRAY/MAP/ROW 复合数据 |
| 解嵌套 | Unnest | 集合列展开为行的算子/语法 |
| 类型转换 | CAST | 显式类型转换（引擎拒绝多数隐式） |
| 分组集 | Grouping Sets | CUBE/ROLLUP/GROUPING SETS 多维聚合 |
| CTE | Common Table Expression | WITH 子句命名查询片段 |
| 半连接 | Semi Join | EXISTS/IN 语义的只判存在连接 |
| DELETE 支持面 | Delete Support | 连接器对行级删除的差异化实现 |

## 最新演进与工业实践

- **语法面持续扩**：2024–2026 两条线的 SQL 面新增/调整（如 Trino 的资源管理语句改革、
  Iceberg 表 DML 完善、REST API 客户端族）——以官方语言参考为准：
  [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅（经其导航进 SQL 章节）、
  [github.com/prestodb/presto](https://github.com/prestodb/presto) ✅ 内 `docs/` 源。
- **与湖格式 DDL 的合流**：`CREATE TABLE ... WITH (format=...)` 的当代主场是 Iceberg：
  隐藏分区（`partitioning=ARRAY['days(ts)']` 类表达式分区）把本章"分区属性"的语义升级到格式层——
  [../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md](../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md)、
  [iceberg.apache.org/docs/latest/](https://iceberg.apache.org/docs/latest/) ✅。
- **UPDATE/DELETE 终成常态（在湖上）**：Iceberg v2 MoR/CoW 由引擎 MERGE 驱动，
  "8.19 的克制"被格式层接管——[../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md) 及其维护章。
- **国内印证**：B 站 Adhoc 查询大量依赖 CTAS 式结果固化与引擎间语法翻译（LinkedIn 开源 coral
  做 Hive↔Presto 语句转换）——[dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅；
  coral 仓库：[github.com/linkedin/coral](https://github.com/linkedin/coral)（✅ 2026-09 curl 复核可达）。
