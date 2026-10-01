# 03 BigQuery 数据类型、函数与 UDF（Google BigQuery Data Types）

> 对应原书 **Ch.3 "Google BigQuery Data Types"**（章题与 16 个节题 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测 200（✅）。
> 含 🔧 类比实验 T4（DuckDB LIST/STRUCT 对位 RECORD/REPEATED，**非 BigQuery 行为**）。

## 本章在本书中的位置

本章是 Ch.4/Ch.5 两场 SQL 大戏的词表与语法底座：类型 → 运算符 → 三类函数（日期时间/字符串/正则）→ 转换函数 → UDF。作者的编排暴露了业务背景（保险行业数据，Foreword 里他自述 ⚠️ 转述）：大量篇幅花在**脏数据清洗（sanitizing）与转换时机（装载前 vs 装载后）**——这不是炫技章，是"ETL 工程师的进货质检"章。

## 3.1 支持的数据类型（Supported data types）

2017 Standard SQL 类型表（书中主线，⚠️ 转述 + ✅ https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/data-types）：

| 类型 | 书中要点 | 今日增补（见演进节） |
| --- | --- | --- |
| INT64 | 唯一整数族，64 位 | INT8/16/32/64、NUMERIC/BIGNUMERIC 已入列 ⚠️ |
| FLOAT64 | 双精度 | 同 |
| STRING | UTF-8 无上限表述 | 同 |
| BOOL / BYTES | 布尔 / 字节串 | 同 |
| DATE / TIME / DATETIME / TIMESTAMP | 四件套，时区坑在 TIMESTAMP | 同 |
| STRUCT / ARRAY | **嵌套记录/数组原生类型** | 字段可 EXPRESS 选择性 ⚠️ |
| GEOGRAPHY / NUMERIC | 2017 当年新面孔，书里当"新特性"讲 | 早已转正 ⚠️ |

- 书中核心告诫（重构）：BigQuery **没有 INTEGER/VARCHAR 方言同义词**，类型写错装载即整行报错——"schema 是合同"心智。
- RECORD/REPEATED 的 Legacy 血统：书里两处混用 Standard 的 STRUCT/ARRAY 与 Legacy 的 RECORD/REPEATED 叫法（Ch.5 "Querying nested and repeated records" 即 Legacy 词汇），读者需建立**一物两名映射表**（⚠️）。

## 3.2 类型注意事项与数据转换（Data type considerations / Converting data）

- 隐式转换极少：书里给了 CAST/TRY_CAST/SAFE_CAST 三兄弟，**SAFE_CAST 失败回 NULL 不回滚整查询**，是清洗管道的主角（✅ https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/functions-all）。
- 日期字符串→TIMESTAMP 的格式串（`%Y-%m-%d %H:%M:%S` + UTC 偏移）单独成段；作者反复强调**装载源文件先统一 UTC，展示层再换时区**（⚠️ 转述）。
- NULL 语义与 `IS NOT NULL`、`IFNULL/COALESCE` 的取舍放在转换小节末尾——为 Ch.4 聚合坑埋伏笔。

## 3.3 数据清洗与转换时机（Sanitizing data / When to transform: before or after loading?）

本章最有工程味的一节（重构其论点）：

1. **装载前转换（GCS 上洗）**：适合规则稳定、量大、可批处理——省 BQ 计算费（扫描小、schema 干净）；
2. **装载后转换（SQL 里洗）**：适合规则探索期——保留原始行，用派生表/视图固化；
3. 作者裁决：**"原始数据永不丢失 + 清洗层前置"** 的折中——先落原始表（staging），同项目 SQL 生成干净表；这在 2017 是罕见的清醒表述（对照今天"bronze/silver/gold 分层"即其直系后代 ⚠️ 通识）。
- 工具预告：本节末尾点名 Dataprep——把"装载前洗"的活儿外包给可视化清洗服务（Ch.8 正式展开）。

## 3.4 运算符与函数巡礼（Arithmetic/Comparison Operators、Date Time/String/Regular Expression Functions、Functions for transformation）

- 算术/比较：与 ANSI 差异点在于**除零不报错回 NULL（Legacy 行为）vs Standard 报错**（书里以此作为两方言行为差异的头号案例 ⚠️）。
- 日期时间函数：`PARSE_DATE/PARSE_TIMESTAMP`、`TIMESTAMP_TRUNC`（Ch.5 分区表查询直接复用）、`DATE_DIFF/DATE_ADD`。
- 字符串：`SPLIT/CONCAT/STRING_AGG`（后者 2017 新上，书里当新玩具 ⚠️）、`LPAD/FMTRY` 家族。
- 正则：`REGEXP_MATCH/REPLACE/EXTRACT/REPLACE`——作者用邮编与电话格式清洗做贯穿例（叙事重构）；正则函数与 Legacy `OMIT RECORD IF` 的关系在 Ch.4 收口。
- 转换函数族：`CAST/SAFE_CAST/FLOOR/CEIL/ROUND` + 格式解析，构成 3.2 的弹药库。

## 3.5 UDF：用户自定义函数（Mastering transformation with UDFs / considerations / format）

- 语法（书中原型，⚠️ 转述）：

```sql
CREATE TEMP FUNCTION clean_zip(z STRING)
RETURNS STRING
AS (SAFE_CAST(REGEXP_REPLACE(z, r'[^0-9]', '') AS STRING));
SELECT clean_zip(zip) FROM staging.addresses;
```

- 两个时代差异必须登记：**书中写 "JavaScript UDF"**（`OPTION (description=...)`、@lib 语法），Library 型 UDF 今天受安全策略收紧（⚠️ 转述）；**Lambda 表达式**（2019 年加入）书里没有，今天配 ARRAY 高阶函数（`transform/filter`）才是嵌套清洗的正解。
- 书中三条告诫（重构）：TEMP FUNCTION 不持久、UDF 内不能引用表、函数过多会推高查询字节 → 与 dry run 联查成本。
- 🔧 **本机类比 T4（DuckDB 1.5.5，非 BigQuery 行为）**：STRUCT/ARRAY 与 UNNEST 的直觉——

```python
con.sql("CREATE TABLE docs AS SELECT i id, ['t'||(i%3)::VARCHAR,'t'||(i%7)::VARCHAR] tags,
         {'a':i,'b':i*2} st FROM range(10000) t(i)")
con.sql("SELECT id, unnest(tags) tag, st.a FROM docs LIMIT 2").fetchall()
# 实测: [(0,'t0',0),(0,'t0',0)]
con.sql("SELECT array_length(tags) FROM docs LIMIT 1").fetchone()  # (2,)
```

  LIST(≈ARRAY)+STRUCT(≈RECORD)+UNNEST(≈Cross Join Unnest) 在本机 1 秒内建立"嵌套即表"的肌肉记忆；注意这只是**语法直觉类比**，BigQuery 的嵌套列在存储层仍按列摊平（REPEATED 的 4 万条限制、嵌套列不再二级嵌套等规则**不在类比范围**，⚠️ 以官方 data-types 页为准）。

## 3.6 小练习两则（本目录自拟，覆盖本章全部主干）

```sql
-- 练习一：装载前 vs 装载后各洗一半（3.2/3.3/3.4 全家桶）
SELECT
  SAFE_CAST(REPLACE(income, '$', '') AS INT64)          AS income_num,   -- 货币串→INT64
  PARSE_DATE('%b %e, %Y', date_str)                     AS d,            -- 英文日期串→DATE
  REGEXP_EXTRACT(phone, r'(\d{3})-\d{4}')               AS area          -- 正则取区号
FROM staging.raw_orders;

-- 练习二：UDF 固化口径 + 数组直觉（3.5，STRUCT/ARRAY 语义见 🔧 T4）
CREATE TEMP FUNCTION age_days(b DATE) AS (DATE_DIFF(DATE '2017-06-01', b, DAY));
SELECT name, ARRAY(SELECT age_days(dob)) AS ages FROM staging.babies LIMIT 10;
```

- 两题的自测点：SAFE_CAST 是否吃下了脏行、PARSE_DATE 格式串是否对应源样、DATE_DIFF 参数序（大减小在 Standard 里靠方向参数）、UDF 是否声明为 TEMP；
- 书中配套例（邮编/电话清洗）与练习一同构，**在 bq 命令行里用 `--dry_run` 各估一次扫描字节**，把 Ch.2 心法同步复习。

## 阅读策略与坑

1. 3.1 类型表 + 3.3 转换时机是本章可带走的**两件资产**；函数巡礼当字典用；
2. 书里混排的 Legacy 词汇（RECORD/OMIT RECORD IF/LEN/IN 分区符）见一处划一处——Ch.4 会给全表；
3. SAFE_CAST + 正则的组合例值得在任意引擎默写一遍（🔧 直觉同构，但**报错/NULL 语义各家不同**，勿迁移结论）；
4. UDF 章末 Further Reading 节指向官方参考——那正是本章最该配着读的材料（✅ https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/user-defined-functions）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 数据类型 | data types | INT64/STRING/TIMESTAMP/STRUCT/ARRAY/GEOGRAPHY |
| 记录/数组 | RECORD & REPEATED / STRUCT & ARRAY | Legacy 名与 Standard 名一对映射 |
| 安全转换 | SAFE_CAST / TRY_CAST | 失败回 NULL 不炸查询 |
| 数据清洗 | sanitizing data | 装载前后把脏值规整 |
| 转换时机 | transform before/after loading | 原始层保留+清洗前移的折中 |
| 解析日期 | PARSE_DATE / PARSE_TIMESTAMP | 字符串→时间，格式串定生死 |
| 截断时间 | TIMESTAMP_TRUNC | 分区查询的谓词搭子 |
| 字符串聚合 | STRING_AGG | 行转列逗号串（当年新函数） |
| 正则族 | REGEXP_MATCH/REPLACE/EXTRACT | 清洗主武器 |
| 用户自定义函数 | UDF (JavaScript) | TEMP FUNCTION 三件套语法 |
| 高阶函数 | ARRAY transform/filter | 书后时代补 UDF 表达力 |
| 除零行为 | divide by zero: NULL vs error | 两方言头号行为差异 |

## 最新演进与工业实践

- **类型扩容**：INT8/16/32、NUMERIC→**BIGNUMERIC**（2020）、JSON 原生类型（2023，⚠️ 转述）——书中"INT64 一根独苗"的时代结束；✅ https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/data-types。
- **UDF 家族**：永久化函数（Persistent UDF，2019）、表值 TVF、远程模型函数 **AI.GENERATE 一族**（⚠️ 转述；✅ 概念页 https://docs.cloud.google.cn/bigquery/docs/bqml-introduction）——JS UDF 独大的书中格局已换代。
- **Legacy SQL 终局**：书中大量 Legacy 对照内容随方言于约 2024-06-30 停止服务而彻底退役（⚠️ 转述；✅ 遗留页 https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/legacy-sql 仍可达、已标注停用）。
- **清洗即产品**：作者 3.3 的"staging+派生"主张今天由 **dbt 分层（bronze/silver/gold）**与 BigFlow/Data Previews 工具化（⚠️ 通识转述）；盘上近邻：数仓方法论见 [../BigQuery_for_Data_Warehousing/03-批量装载与流式摄入.md](../BigQuery_for_Data_Warehousing/03-批量装载与流式摄入.md)。
- **嵌套建模仍是难课**：数组超限、嵌套展平爆炸等坑十年未变，TDG 册高级查询章给了系统解法（[../Google_BigQuery_TDG/08-高级查询.md](../Google_BigQuery_TDG/08-高级查询.md)）。
