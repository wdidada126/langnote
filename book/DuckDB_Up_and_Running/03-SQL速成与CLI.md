# 03 · A Primer on SQL（SQL 速成与 CLI）

> 覆盖原书第 3 章。目录来源：✅ 官方示例文件 `Chapter_3.ipynb` 标题实抓。本章服务"SQL 生手/转型者"：先立 CLI，再用一本书的数据（航班）走完 join/聚合/分析三板斧。对已有 SQL 心智的读者，这一章是"方言差异点清单"。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Chapter 3. A Primer on SQL**
  - **Using the DuckDB CLI**：CLI 安装（notebook 逐条给出 **Linux/Windows/macOS 三种安装命令**，✅ 代码实抓：Windows `winget install DuckDB.cli` 型一行式）；`.sql` 文件、`commands.sql`（官方示例仓库根含 90 B 的 `commands.sql`，✅ 树实抓）。
  - **DuckDB SQL Primer**，下分三节：
    - **Joining Tables**：INNER/LEFT 与多表串联（flights×airports×airlines 三表）。
    - **Aggregating Data**：`GROUP BY/HAVING`、`count/sum/avg`。
    - **Analytics**：面向分析的组合拳（分布、Top-N、按维度切片——本章把"SQL 是为分析服务的手"讲明白）。

## 核心技术清单（DuckDB 方言相对标准 SQL 的增量，本书示例可触达者）

- 文件即表：`FROM 'flights.parquet'`；列名保留大小写需双引号（Kaggle 源列 `Carrier` vs 转换后 `AIRLINE`——实测两镜像列风格不同）。
- 位置引用与 `GROUP BY ALL`：`SELECT AIRLINE, count(*) … GROUP BY ALL`（本目录实测用法 ✅）。
- 友好字面量：`INTERVAL`、`'2015-01-01'::DATE` 自动转型；CSV 表头自动 `header=true`。
- 聚合扩展函数：`quantile_cont/quantile_disc`、`approx_top_k`、`mode()`、`median()`（数组参数分位数一次出 p50/90/99，✅ 实测）。
- `PIVOT/UNPIVOT` 一等公民语法（本书未教、DIA 第 4 章主讲——差异处引兄弟目录）：[../DuckDB_in_Action/04-高级聚合与数据分析.md](../DuckDB_in_Action/04-高级聚合与数据分析.md)。
- `USING SAMPLE 200000 ROWS`：抽样即子句（本目录实测 ✅）。
- 大小写不敏感的标识符折叠与 `DESCRIBE`/`SHOW` 元数据族。
- 参数化：`execute(sql, params)`（注意 1.5.5 `con.sql` 位置参数已移除）。
- QUALIFY/ASOF/LATERAL：DIA 深讲，本章只标注"UAR 全书未覆盖 ASOF——05 章实验节补足"。

## 🔧 实测（1.5.5；580 万行航班表上的三板斧）

1. **三表 JOIN 覆盖率**：`flights ⋈ airports(322) ⋈ airlines(13)` 后按 spheroid 版本查询——5,729,195 非取消航班中 5,332,914 行能同时命中两端机场（**93.1% 覆盖**，示例仓库 airports.parquet 为 322 子集所致；⚠️ 全量 1,807 机场另计）。
2. **聚合**：`SELECT AIRLINE, count(*) … GROUP BY ALL ORDER BY 2 DESC LIMIT 3` → `[('WN',1261855),('DL',875881),('AA',725984)]`，**4.04 s（远程 12 文件直查）** / 本文件化后 **0.02–0.06 s** 级。
3. **分位数（Analytics 节典型题）**：按航司 `quantile_cont(DEPARTURE_DELAY, 0.9)` 取 p90 最差 Top-2 → `NK 60.0 分钟、F9 50.0 分钟`，**0.06 s**/5.7M 行。
4. **CLI**：独立二进制在本机不可达（GitHub release 资产下载 http:000，网络受限 ⚠️）；CLI 行为（点命令、`.sql` 执行）**⚠️ 文档转述**，未实测。Python 侧等价：`con.execute(open('x.sql').read())` ✅。
5. **列名风格陷阱实证**：同一 book 数据 `airports.parquet` 为 `IATA_CODE/AIRPORT/CITY/STATE/LATITUDE`（Kaggle 风），`flights.parquet` 为 `YEAR/MONTH/…`（大写蛇形）——JOIN 前 `DESCRIBE` 先对齐，`"Carrier"` 与 `AIRLINE` 不可混（实测 Binder Error 直接教做人）。
6. **抽样**：`USING SAMPLE 200000 ROWS` 与全量在同一谓词下行数 200k/5.8M、结果均值口径一致（spatial 校验即在此完成，见 [05 章](05-用DuckDB做探索性数据分析.md)）。
7. **EXISTS 半连接** 🔧：`SELECT count(*) FROM flights f WHERE EXISTS (SELECT 1 FROM airports a WHERE a.IATA_CODE=f.ORIGIN_AIRPORT AND a.STATE='NY')` → **246,235 行 / 0.04 s**——按维表属性筛事实，EXISTS 天然防行数膨胀，计数口径的安全牌。
8. **每组 Top-1 窗口** 🔧：`row_number() OVER (PARTITION BY AIRLINE ORDER BY DEPARTURE_DELAY DESC)` 取 rn=1 → DL 1289 / B6 1006 分钟（各航司最晚点航班），**0.02 s**（5.8M 行窗口排序）——"组内极值"题式的标准解。
9. **标量宏** 🔧：`CREATE MACRO delay_hours(m) AS m/60.0` 后按宏聚合 → NK 0.266 h / UA 0.241 h 最差 Top-2，**0.02 s**——"单位换算进宏、口径全库统一"是 macro 的正用。
10. **基数与粒度** 🔧：`count(DISTINCT ORIGIN_AIRPORT)=628`、`count(DISTINCT TAIL_NUMBER)=4897`（**0.03 s**）；`count(*)−count(DISTINCT TAIL_NUMBER)=5,814,182`——580 万航班对 4897 架飞机，粒度教学最佳反例：问"多少架飞机"必须先 `GROUP BY TAIL_NUMBER` 再数。
11. **NULLS 是保留字** 🔧：`SELECT count(*) nulls FROM …` 直接 Parser Error（`ORDER BY … NULLS FIRST/LAST` 的那个 NULLS）——缺失率列名用 `n_null` 或加双引号。

## 易错点与陷阱

- **PRIMER 的读者陷阱**：示例 SQL 常以 `%` 通配写进 `LIKE`，与 Python DBAPI 参数位冲突——`execute("… LIKE '%x%'")` 会炸（同 DIA 06 陷阱，两书共坑）。
- **GROUP BY 位置号 vs ALL**：`GROUP BY ALL` 把非聚合列全进键，SELECT 里多带一列就悄悄改了粒度——上生产前显式写键。
- **双引号 ≠ 单引号**：DuckDB 里 `"col"` 是标识符、`'lit'` 是字符串（Postgres 家族规矩），notebook 里从 SQLite 方言抄来的双引号字面量会静默变成列引用。
- **NULL 参与聚合**：`avg(DEPARTURE_DELAY)` 自动剔 NULL，但 `count(*)−count(col)` 的缺失率口径要显式算——分析结论里"平均延误"类指标先声明分母（本目录全部均值查询都带 `IS NOT NULL`）。
- **ORDER BY 的 NULL 位置**：默认 NULLS LAST（ASC），与多数行式库相反——Top-N 榜单两书口径要对齐。
- **CLI 不在手时的替代**：`python -c "import duckdb; duckdb.sql('…').show()"` 覆盖 90% 练习场景；`duckdb.execute` 多语句要分开喂。
- **FILTER 与 WHERE 的分母位**：比率指标的分子进 `FILTER`、全局过滤进 `WHERE` 会悄悄改分母口径——取消率类指标应"无 WHERE、条件全进 FILTER"（05 章实测 9 即此形态）。
- **`UNION` 的序陷阱**：UNION 去重会重排行序，榜单类查询即使源里有 ORDER BY 也要在最外层重写——"UNION 加了排序不生效"多为读法误解。

## 分析 SQL 五板斧模板（本章×05 章统一口径，全部有实测号）

```sql
-- ① 过滤+聚合+排序（Top-N 榜单；实测 2）
SELECT AIRLINE, count(*) c FROM 'flights2015.parquet' GROUP BY 1 ORDER BY c DESC LIMIT 3;
-- ② 条件计数（分子分母同屏；05 章实测 9：MQ 取消率 5.10%）
SELECT count(*) FILTER (WHERE CANCELLED=1) cancels, count(*) total FROM …;
-- ③ 半连接/反连接（维表属性筛事实；实测 7）
SELECT … WHERE EXISTS (SELECT 1 FROM dim d WHERE d.k = f.k AND d.state = 'NY');
-- ④ 每组 Top-k（窗口+过滤；DuckDB 可再简写 QUALIFY——DIA 03 章主讲）
SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY AIRLINE
               ORDER BY DEPARTURE_DELAY DESC) rn FROM …) WHERE rn = 1;
-- ⑤ 缺失/基数画像（先量再聚；实测 10/11）
SELECT sum(CASE WHEN DEPARTURE_DELAY IS NULL THEN 1 ELSE 0 END) AS n_null,
       count(*) AS n FROM …;   -- 实测 86,153 / 5,819,079 ≈ 1.48%（05 章实测 11）
```

- 五板斧对应"榜单 / 占比 / 筛选 / 组内极值 / 数据质量门"——比 20 个孤立语法点更实用的，是这五个动作的排列组合。

## 方言差异卡（从 MySQL/SQLite 迁来的单向适配清单）

| 日常行为 | DuckDB 1.5.5 | 撞点 |
| --- | --- | --- |
| `"x"` 是字符串字面量（MySQL 默认） | `"x"` 是标识符、`'x'` 才是字符串 | 复制粘贴 SQL 第一坑（本目录陷阱 3） |
| 宽松 GROUP BY | 非聚合列报错更严；`GROUP BY ALL` 是方言糖 | ALL 悄悄改粒度（陷阱见上） |
| 反引号标识符 / `#` 注释 | 标准 `--`、`/* */`；标识符双引号 | sed 风速记会炸 |
| NULL 升序排头（MySQL 8） | 默认 NULLS LAST | Top-N 榜单反向（陷阱 5） |
| 类型亲和（SQLite 啥都能存） | 强类型 + 显式 CAST | SQLite 迁移代码全灭重灾区 |
| `AUTO_INCREMENT` | `SEQUENCE`/`GENERATED` 列 | 只影响写演示 |
| `DATE_FORMAT()` 族 | `strftime`/`strptime`（SQLite 风） | MySQL 写法需换 |

- 一句话口诀：**双引号是列、NULL 收尾、亲和没来**。

## 与其他章/书的互链

- 本章只到"会写"，写得快写得好在 [05-用DuckDB做探索性数据分析.md](05-用DuckDB做探索性数据分析.md)（窗口/PIVOT/ASOF 全上量实测）。
- 方言全谱（QUALIFY/LATERAL/列表/宏/lambda）→ [../DuckDB_in_Action/03-执行SQL查询.md](../DuckDB_in_Action/03-执行SQL查询.md)。
- CLI 点命令/扩展管理细目 → [../DuckDB_in_Action/02-快速上手CLI与扩展系统.md](../DuckDB_in_Action/02-快速上手CLI与扩展系统.md)。
- 优化器视角的同题对照（单机进程内 vs MPP）→ [../大数据SQL优化.md](../大数据SQL优化.md)。
- SQL 标准与关系理论根基 → [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md) 的互链表所指理论书目。

## 思考题（合上笔记再答）

1. 为什么本章示例里 `airports.parquet` 的 322 行子集能把 JOIN 覆盖率打到 93%？剩余 7% 是什么？（取消航班剔除 + 子集缺机场；实测两数 5,729,195→5,332,914）
2. `GROUP BY ALL` 在什么场景会悄悄错？给出防御写法。（多余非聚合列改粒度；显式键列表）
3. p90 延误 Top-2 是哪两家、多少分钟？换成"最准点"Top-2 你怎么改？（NK 60.0/F9 50.0；ORDER BY 2 ASC）
4. 五板斧各报一个本章实测数。（榜单 WN 1,261,855 / 取消率 MQ 5.10%（05 章）/ NY 出港 246,235 行 / DL 最晚 1289 分钟 / NULL 1.48%——实测 7–11）

## 2026 视角补注

- 官方"SQL dialect"文档族持续扩充（引根：https://duckdb.org/docs/stable/clients/overview ✅ 及各扩展文档站 200），2024 书稿里的方言点全部在册；ASOF/PIVOT 已是我方两书共推的"标准武器"。
- 1.x 的查询语义（NULL 序、抽样、quantile）未见过破坏性变更——**方言层比客户端 API 层稳**，升级脚本优先改 API 调用面而不是 SQL 本体（本目录 00 漂移清单佐证）。

## 核心概念速览（中英对照）

- **文件即表** — Query files directly：FROM 接路径的方言糖。
- **GROUP BY ALL** — 全非聚合列入键的便利子句。
- **USING SAMPLE** — 行抽样子句（伯努利/系统/行数）。
- **分位数族** — quantile_cont/disc：精确分位，支持数组参数。
- **近似 Top-K** — approx_top_k：Sketch 类高频值统计。
- **NULLS LAST 默认** — 升序时 NULL 排尾。
- **DESCRIBE/SHOW** — 元数据速查双件套。
- **参数位** — `?`/named params：`execute` 通道防注入。
- **PRIMER 三角** — Join/Aggregate/Analyze：本章教学三动作。
- **列风格漂移** — 大小写与蛇形/驼峰混源：JOIN 前对齐 schema。

## 最新演进与工业实践

- **CLI 分发现状**：官方安装页（https://duckdb.org/install/ ✅，DIA 00 同引）给六类平台一行式安装；本目录网络受限未实测，行为口径仍以官方文档为准 ⚠️。
- **SQL 工作台生态**：DBeaver/DataGrip/NestJS 等经 JDBC/DuckDB-Wasm 消费同一方言（客户端矩阵 ✅），教材间差异只在"用哪种壳"。
- **两书共读结论**：UAR 第 3 章 + DIA 第 3/4 章 ≈ 一份完整方言地图；先 UAR 后 DIA 的人不会在 DIA 第 4 章迷路，反之可跳过 UAR 3 只查差异点。
- **工业实践**：分析 SQL 评审清单（NULL 分母、抽样偏差、GROUP BY ALL 粒度）在 2024–2026 的数据工程博客里反复出现——本章"易错点"即其浓缩。
