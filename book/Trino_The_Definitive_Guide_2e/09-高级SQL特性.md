# 第 9 章 高级SQL特性（Advanced SQL Features ⚠️ 英题推定）

> 对应原书第二部分第 9 章：函数与表达式宇宙。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。SQL 为教学示意。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 9.1 函数和运算符介绍 | 标量/聚合/窗口三分 + 命名空间 | 分类即查询手册的目录 |
| 9.2–9.4 标量/布尔/逻辑运算符 | 三值逻辑与短路语义 | NULL 传播规则是一切坑的母法 |
| 9.5 BETWEEN / 9.6 IS NULL | 范围与存在性判断 | BETWEEN 闭区间；`<>` 遇 NULL 是 unknown |
| 9.7–9.9 数学/三角/随机 | 数值函数族 | 精度/舍入跨源差异点 |
| 9.10–9.13 字符串/映射/Unicode/正则 | 文本处理全家桶，`regexp_extract` 系列 | 正则引擎是 RE2/Joni 血统 ⚠️ 细节看文档 |
| 9.14 解嵌套复杂数据类型 | UNNEST：数组/映射打平成行 | CROSS JOIN UNNEST 是方言签名动作 |
| 9.15 JSON函数 | json_extract(_scalar) 一族（392 时代 JSON 是 VARCHAR） | 原生 JSON 类型属后期演进 ⚠️ 见文末 |
| 9.16 日期和时间函数 | 时区转换/截断/interval 算术 | TIMESTAMP WITH TIME ZONE 的正道入口 |
| 9.17 直方图 | histogram(state)→映射，approx 家族前奏 | 百万基数的「近似频数表」 |
| 9.18 聚合函数 | 标准聚合 + approx_distinct 等概率算法 | HLL/分位草图是 Trino 招牌 |
| 9.19 窗函数 | OVER/帧/排序 + 命名窗口 | 帧默认 RANGE 的坑与 Pg 一致 |
| 9.20 lambda表达式 | transform/filter/reduce 的高阶函数伴侣 | 数组列上的 map-filter-reduce |
| 9.21 地理空间函数 | geometry 类型与空间算子，Web UI 插件可视化 | 湖上 GIS 查询的 SQL 门面 |
| 9.22 预处理语句 | PREPARE/EXECUTE/参数化 | 驱动侧与协议侧的汇合点 |
| 9.23 小结 | — | 函数手册读法：分类 → 示例 → 下推性 |

## 核心精讲

### 1. 三值逻辑与 NULL 代数（9.2–9.6 的母题）

```sql
-- 教学示意：一切判断的三种结果 true/false/unknown
SELECT x IS NULL, NOT (x > 5), x <> 'a' FROM t;   -- x 为 NULL 时三列分别 true/unknown/unknown
SELECT count(*) FROM t WHERE x > 5;   -- NULL 行被 unknown 静默排除
```

聚合与 WHERE 的 NULL 语义错位是湖上「数据明明在、查出来没有」的第一大原因；`COALESCE`/`IS DISTINCT FROM`（NULL-safe 比较）是标配解药（对照 [../SQL反模式.md](../SQL反模式.md) 的 NULL 篇）。

### 2. UNNEST + lambda：复合类型的二重奏（9.14/9.20）

```sql
-- 教学示意：数组列打平成行，再高阶加工
SELECT u.uid, tag
FROM users u CROSS JOIN UNNEST(u.tags) AS t(tag);

SELECT transform(tags, x -> upper(x))            -- lambda：逐元素映射
     , filter(tags, x -> x LIKE 'vip%')          -- 过滤保列
     , reduce(scores, 0.0, (s, x) -> s + x, s -> s)  -- 折叠
FROM users;
```

这是 Trino SQL 与 HiveQL 拉开表达力差距的核心区：嵌套列（ARRAY/MAP/ROW）+ 高阶函数 ≈ 行内微型管道，免去「先炸开再聚合回去」的往返（与 PG 数组函数族气质不同，可并读 [../SQL编程思想.md](../SQL编程思想.md) 类书目）。

### 3. 概率算法家族（9.17/9.18）

- `approx_distinct(x)`：HLL 草图，基数估计默认误差 ~2.3%（`WHERE` 精度可调 ⚠️ 参数名以文档为准）。
- `approx_percentile(x, array[0.5,0.99])`：分位数/SLA 报表主力。
- `histogram(x)`：值→频数的**映射**，可 `CAST` 进 TDigest 再取 `value_at_quantile`——书用这条链演示「一页内存装下百万基数分布」。
- 组合技：湖上 UV 日报 = `approx_distinct` + 分区裁剪（08 章 WHERE 纪律）；精确去重留给小分区。
- 理论坐标：这些草图算法（HyperLogLog、Count-Min、TDigest）在 [../../db/db.md](../../db/db.md) 论文线与 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md) 的近似查询节各有一席。

### 4. 时区正确姿势（9.16）

```sql
-- 教学示意：UTC 存储 → 会话时区展示，别用字符串存时间
SELECT date_trunc('hour', ts) , 
       ts AT TIME ZONE 'Asia/Shanghai'   -- 392 起 AT TIME ZONE 可用 ⚠️ 函数语义按文档
FROM events;
```

湖上最常见的事故：写入端用字符串/本地时区，Trino 按 session timezone 解释，日报差 8 小时。修复路径 = 类型升级（TIMESTAMP(3) WITH TIME ZONE）+ `to_unixtime/from_unixtime` 校对。

### 5. 地理空间与可视化（9.21）

`GEOMETRY` 类型 + ST_ 系列函数（st_contains/st_distance 等），配官方 Web UI 的地理空间插件渲染。湖上「地图能查」的意义：轨迹/围栏/POI 分析不再需要先把数据搬进 PostGIS（PostGIS 对照在 repo 的 PG 系笔记，见总索引）。

### 6. 预处理语句（9.22）

`PREPARE p FROM SELECT ... WHERE x = ?; EXECUTE p USING 42;` —— 计划复用与注入防护的 SQL 层语义，JDBC 客户端走 `PreparedStatement` 即协议层同款（03 章）。Trino 侧还有 plan caching（多版持续演进 ✅ release notes 高频项），把「参数相同→复用优化结果」做成引擎行为。

### 7. 函数手册读法（9.23 的方法论）

官方函数页按「标量/聚合/窗口/集合/地理空间/JSON…」分类 ✅——每个函数只需问三件事：返回类型与 NULL 语义、是否可下推（决定 4.6 收益）、是否有 approx 兄弟（决定成本）。本章 23 节的厚度，本质是一张「三问 × N」的矩阵。

## 常见误区

- `approx_distinct` 当精确值进财务口径（误差进报表是事故；精确留给小分区或预聚合）。
- 窗口帧默认 RANGE 与 PG 一致但 Hive 系多按 ROWS 直觉写——迁移期逐句核对（对照 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)）。
- 正则/字符串函数套在分区列上杀下推（08 章 sargable 规则在函数时代的变体）。
- 392 书稿把 JSON 一律 `VARCHAR + json_extract`：483 有原生 JSON 类型路线后，新代码别再手工 CAST（文末演进有账）。
- `histogram()` 结果直接当最终报表：它是中间结构，需配 `CAST(... AS qdigest)`/TDigest 语义链 ⚠️ 具体类型名按 483 函数页。

## 与其他章/其他书的联系

- 每个函数的「下推性」判断回 [04-Trino架构.md](04-Trino架构.md) RBO 节 + 各 connector 页。
- 聚合/窗口的 OLAP 理论面在 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md)；近似算法论文线 [../../db/db.md](../../db/db.md)。
- 与 Spark SQL 函数对照（transform/reduce 等价物）：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)、[../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)。

## 核心概念速览（中英对照）

1. **标量函数** — scalar function：行内一对一变换。
2. **三值逻辑** — three-valued logic：true/false/unknown 的判断代数。
3. **IS DISTINCT FROM** — null-safe comparison：把 NULL 当普通值的比较。
4. **UNNEST** — 解嵌套：数组/映射列打平成行（CROSS JOIN 形态）。
5. **lambda 表达式** — lambda：高阶函数的行内匿名函数 `x -> ...`。
6. **transform/filter/reduce** — 高阶数组函数族：列上 map-filter-fold。
7. **approx_distinct** — HLL 基数：概率式去重计数。
8. **approx_percentile** — 近似分位：SLA/分位数报表主力。
9. **直方图函数** — histogram()：值→频数的可合并映射结构。
10. **TDigest/Q-Digest** — 分位草图：与 histogram 组合取分位。
11. **AT TIME ZONE** — 时区算子：时间戳的展示时区转换。
12. **date_trunc** — 时间截断：按粒度对齐的分组前件。
13. **GEOMETRY** — 空间类型：ST_ 函数族与地图可视化的地基。
14. **PREPARE/EXECUTE** — 预处理语句：参数化与（协议层）计划复用。
15. **plan caching** — 计划缓存：引擎侧按查询+会话复用优化产物（483 持续演进项 ✅）。

## 最新演进与工业实践

- **JSON 数据类型**：392 之后 Trino 引入原生 JSON 值类型与配套函数线（官方函数/类型文档 ✅ 基线 483；引入版本号本次未逐版核实 ⚠️），半结构化湖表分析的体验从「VARCHAR 手剥」进化到「列式 JSON 路径」。
- **地理空间线**：官方 blog 长期科普 OLAP 引擎中的空间分析（blog feed 条目 ✅ [trino.io/blog/feed.xml](https://trino.io/blog/feed.xml)），湖上轨迹/围栏查询用 Trino 替代「先入 PG」的场景增多（趋势转述 ⚠️）。
- **近似算法产品化**：`approx_*` 家族扩到新输入类型、合并语义优化是 release notes 常客（✅ release-483 索引 [release-483.html](https://trino.io/docs/current/release/release-483.html) 回溯可查）；「UV 类指标一律 approx + 误差预算」成为 BI 团队常规口径（工程实践 ⚠️）。
- **函数下推矩阵**：JDBC 型 connector 的函数下推清单逐版加长（483 release notes 的 PostgreSQL/SQL Server 连接器节 ✅），函数「能不能下推」从玄学变成查表题。
- **命名/别名规范**：SQL 函数族官方页按类别分组维护 ✅ [docs current](https://trino.io/docs/current/overview.html)（Functions and operators 分区）——跟书时先读 483 函数页的「变更注记」，再对旧例。
