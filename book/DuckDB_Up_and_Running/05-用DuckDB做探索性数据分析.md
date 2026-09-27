# 05 · Performing EDA with DuckDB（用 DuckDB 做探索性数据分析）

> 覆盖原书第 5 章（notebook 原题拼写 "Performintg EDA"，✅ 实抓）。全书的"数据科学主场"：拿 **2015 美国航班延误数据集**（Kaggle `usdot/flight-delays`，第三方笔记仓库明记本书用此数据 ✅）做一次完整的 EDA——地图/空间、描述统计、延误归因，DuckDB + spatial + GeoPandas 三线合流。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **2015 Flight Delays Dataset**：数据底座（580 万行级 flights + airports + airlines；官方示例已预转 `year=2015/month=XX/flights.parquet` Hive 分区，✅ 仓库树实抓）。
- **Geospatial Analysis → Displaying a Map → Displaying All Airports on the Map**：绘图与地图打底（notebook 路线 ⚠️ 推定 matplotlib/folium 族）。
- **Using the spatial Extension in DuckDB**：`INSTALL spatial` 后几何函数进 SQL。
- **Use the Shapely library to convert latitude and longitude into Point datatype**（含子节 Converting …）：经纬度→POINT 的两条路（Shapely 在 Python 侧 / 函数在 SQL 侧）。
- **Converting a pandas DataFrame to a GeoPandas GeoDataFrame**（含 Displaying airport locations、**Finding nearby airports**）：空间检索下推/上抛的分工示范。
- **Performing Descriptive Analytics**，八连子节 ✅：按州/市数机场、`GROUP BY` 州内机场总量、起降对航班量、各航司取消航班、按星期航班量、机场代码核验（含"剔除取消后按工作日算占比"子题）、**延误最常见时段**、**延误最多/最少航司**。

## 核心技术清单

- 空间三件套：`ST_Point(lon,lat)`、`ST_Contains(polygon, point)`、`ST_Buffer/ST_Distance_Spheroid`；WKT 直书 `ST_GeomFromText('POLYGON((x y,x y,…))')`。
- 分析 SQL 全在本书语境里补齐：窗口 `rank()/ROWS 移动帧`、`PIVOT … ON … USING sum()`、`quantile_cont` 数组分位、`USING SAMPLE`。
- **ASOF JOIN**（本书未教、本目录补测的"EDA 时间线利器"）：不等值"取最近前值"连接，语法 `ASOF JOIN … USING (ts)` / `ASOF LEFT JOIN`。
- GeoPandas 桥：DuckDB 出聚合/过滤结果 → Python 侧画图；`Shapely.geometry.Point` 与 WKT 互转。
- 描述统计口径库：`mode()/median()/approx_quantile`、`count(*) FILTER (WHERE …)`、除零与 NULL 分母防御。

## 本章数据卡（实测底座，本目录实抓）

| 对象 | 值 |
| --- | --- |
| flights2015.parquet | 5,819,079 行 / 144 MB（08 章 HTTPS 冷拉物化） |
| airports.parquet | 322 行（Kaggle 子集；全量 1807 站不在内——覆盖率 93.1% 的根因） |
| airlines.parquet | 14 家航司（WN 1,261,855 班居首） |
| DEPARTURE_DELAY | NULL 86,153（1.48%）/ 中位数 −2 / p90 35 / p99 168（分钟，实测 11） |

## 🔧 实测（1.5.5；全部跑在本书航班数据 5,819,079 行上）

1. **PIVOT**：`PIVOT (SELECT AIRLINE, MONTH, count(*) …) ON MONTH USING sum(c)` 得 14 航司×12 月矩阵 **0.53 s**（首行 AA：44059/39835/45966/44770…）。
2. **窗口**：月内"最晚点航司 Top-3"（`rank() OVER (PARTITION BY MONTH ORDER BY avg_delay DESC)`）→ 36 行 **0.90 s**；`ROWS BETWEEN 1000 PRECEDING` 移动均值扫 5,732,926 行 **0.34 s**。
3. **ASOF JOIN（2M 订单 × 200k 价格刻度）**：`ASOF JOIN USING(ts)` **0.24 s**、`ASOF LEFT JOIN` 0.07 s、结果 1,999,999/2,000,000 行（右表覆盖不满时 INNER 丢 1 行——语义直观验证）；**等价朴素相关子查询在 10k 订单上就要 114.84 s**（2M 外推 ≈6.4 小时）——ASOF 存在的意义一组讲透。
4. **quantile/描述统计**：全航司 p90 延误 0.06 s（NK 60.0/F9 50.0 最差 Top-2）；单月（month=06）503,897 行、平均出发延误 13.99 分钟 **2.08 s**（含 HTTPS 拉取）。
5. **spatial**（322 机场子集）：`ST_Contains` 美国中部盒区取 **81** 机场（0.00 s）；`ST_Point(1,2)→'POINT (1 2)'` WKT 环回 ✅；`ST_Distance_Spheroid(ORD,JFK)=1,546,776.94`——⚠️ **与官方 DISTANCE（英里）对表平均相对差 0.37**：函数返回量纲/椭球参数需以已知基准校准后再用于业务结论（实测教训，见陷阱）。
6. **JOIN 覆盖**：非取消航班 5,729,195 中两端机场同时在 322 子集里的 **5,332,914（93.1%）**——"Finding nearby airports"式空间查询要先量数据覆盖，否则静默丢 7%。
7. **抽样**：`USING SAMPLE 200000 ROWS` 上做逐行距离核对，有效样本 63,396/200,000（NaN 经 `NOT isnan()` 滤除）——EDA 阶段抽样+显式 null/NaN 门是标配。
8. **median+mode 一枪画像** 🔧：`SELECT AIRLINE, median(DEPARTURE_DELAY), mode(ORIGIN_AIRPORT) … WHERE DEPARTURE_DELAY IS NOT NULL GROUP BY 1` → UA 中位 1.0 分钟（众数机场 ORD）、WN 0.0（MDW）、DL −1.0（ATL），**0.08 s**/5.8M 行——"中位+众数枢纽"一行看穿一家航司。
9. **FILTER 取消率榜** 🔧：`count(*) FILTER (WHERE CANCELLED=1)` 与 `count(*)` 分子分母同屏 → MQ 5.10%、EV 2.66%、US 2.05%，**0.02 s**——分母不假外求。
10. **approx_top_k 高频尾号** 🔧：`approx_top_k(TAIL_NUMBER, 5)` → N947FR/N739GB/N511SW/N7719A/N374SW（**0.03 s**）——先 Sketch 定方向，要精确再 count(DISTINCT)。
11. **缺失与分位一次出** 🔧：`DEPARTURE_DELAY` NULL **86,153/5,819,079 ≈ 1.48%**（**0.01 s**；列名慎用 `nulls`，保留字，见 03 章实测 11）；`quantile_cont(…,[0.5,0.9,0.99])` 一次出 [−2, 35, 168] 分钟（**0.12 s**）——p99=168 是"延误故事"的离群门。

## 易错点与陷阱

- **ST_Distance_Spheroid 的"数值像米就是米"**：本目录与 DOT 官方距离对表出现 0.37 平均相对差——单位/椭球口径不明时**先用两个已知机场对校准**，再下结论（两本书都爱跑真数据，但只有对上外部基准才算验证）。
- **经纬度顺序**：`ST_Point(x=lon, y=lat)`——与所有"（纬度,经度）"习惯相反，写反的点散落在赤道附近大洋里，`ST_Contains` 结果为 0 才知道错。
- **WKT 语法**：坐标对之间必须逗号（实测 `'POLYGON((-100 30 -100 45…))'` 直接 Invalid Input）；首尾点要闭合。
- **ASOF 不是万金油**：等值键只一个、"取最近前值"语义；要"前后都取"用 `PLUS/ALL` 变体或窗口（版本能力以官方文档为准 ⚠️ 未逐一测）。
- **移动帧 ORDER BY 列选错 = 语义漂移**：上面 0.34 s 的帧按延误值排序（演示机制），真实"时间滑窗"须先物化出真时间戳列——航班源数据里 `DEPARTURE_TIME` 是 VARCHAR "HHMM"，直接 RANGE INTERVAL 会报类型错（实测撞墙）。
- **avg 的 NULL 分母陷阱**：`avg(DEPARTURE_DELAY)` 自动剔 NULL，但"取消航班延误记 0"类建模错误从过滤开始——本章口径统一 `WHERE DEPARTURE_DELAY IS NOT NULL`。
- **PIVOT 的列爆炸**：MONTH 作 key 只有 12 列，换成航班号就四位数级列爆炸——先 `IN (…)限值`再 PIVOT。
- **mode() 的单面孔**：并列众数只返回其一、不告警——"众数枢纽"结论在双峰分布上要拿 `approx_top_k`/groupby 计数复核（⚠️ 并列语义未逐测，给双信号口径）。
- **median 的叙事误读**：DL 中位 −1 分钟不是"普遍早到"，是"分布中心贴零"——中位数配 p90/p99（实测 11）一起讲才不失真。
- **FILTER 的分母位**：全局过滤写进 WHERE 会把分母一起削掉——取消率类指标"无 WHERE、条件全进 FILTER"（实测 9 形态）。

## EDA 标准动线（本章数据验证过的顺序）

1. **质量门**：行数 / DESCRIBE / NULL 率（实测 11）/ distinct 基数（03 章实测 10）——四个数答不出就别碰均值。
2. **单变量分布**：median + quantile_cont 数组 + mode（实测 8/11）——集中趋势与尾巴三件套。
3. **分群对比**：GROUP BY + FILTER + Top-N（实测 9/4）——分子分母同屏。
4. **时间结构**：MONTH PIVOT 矩阵（实测 1）+ 移动帧（实测 2）——先转置后滑动。
5. **跨表归因**：JOIN 前先量覆盖率（实测 6 的 93.1%）——空间/外键皆"覆盖先行"。
6. **离群门**：p99 与 p90 的落差决定截尾策略（实测 11 的 168 vs 35）——"平均数的谎言"多半在这一步被拆穿。
- 动线首尾都是"先量数据再写结论"：这就是本章 EDA 教学法的全部。

## 延误归因问题树（八连小节之后的"为什么"层）

- 延误是"少数航司烂"还是"所有航司有烂天"？→ 按司 p90（实测 4：NK 60/F9 50）vs 按月分布位移（实测 1 PIVOT）——"中位稳、尾巴坏"与整体右移的归因方向完全不同。
- "时段"是天气还是排班？→ 星期计数 + 移动帧看周期（实测 2），分位数组看尾巴（实测 11）——周五 p99 vs 周二 p99 比"周五均值 vs 周二均值"更有诊断力。
- 机场拥堵与航司质量能否分离？→ `AIRLINE × 出发机场` 分组中位数（实测 8 形态）——WN 在 MDW 也快，就不是机场的锅。
- 取消和延误是同一件事吗？→ 全量/剔取消/延误有值三段 FILTER 口径各算一遍（实测 9 + 03 章五板斧②）——八连第 ⑥ 子题的口径即此。
- 经验法则：问题树每个分支都要能落到一条实测 SQL 上——EDA 的"解释力"是分母喂出来的。

## 分析 SQL 弹药包（本章实测形态，抄了就能测）

```sql
SELECT AIRLINE, median(DEPARTURE_DELAY) med, mode(ORIGIN_AIRPORT) hub,
       quantile_cont(DEPARTURE_DELAY, [0.5,0.9,0.99]) qs,
       count(*) FILTER (WHERE CANCELLED=1) cancels, count(*) n
FROM 'flights2015.parquet'
WHERE DEPARTURE_DELAY IS NOT NULL
GROUP BY 1 ORDER BY med DESC;      -- 一行合并实测 8/9/11，5.8M 行 <0.1 s 级
-- 月内最晚点 Top-3（实测 2 的 rank 模板）：
SELECT * FROM (SELECT MONTH, AIRLINE, avg(DEPARTURE_DELAY) ad,
               rank() OVER (PARTITION BY MONTH ORDER BY avg(DEPARTURE_DELAY) DESC) r
               FROM 'flights2015.parquet' WHERE DEPARTURE_DELAY IS NOT NULL
               GROUP BY 1,2) WHERE r <= 3;
```

## 与其他章/书的互链

- 武器库口径的完整推导（QUALIFY/LATERAL/ASOF 语义细节）→ [../DuckDB_in_Action/04-高级聚合与数据分析.md](../DuckDB_in_Action/04-高级聚合与数据分析.md)
- 本章数据从哪来（Hive 分区/HTTP 直读）→ [08-用DuckDB访问远程数据.md](08-用DuckDB访问远程数据.md)；落湖与共享 → [09-云端DuckDB与MotherDuck.md](09-云端DuckDB与MotherDuck.md)
- 单机进程内分析调优对照 MPP 口径 → [../大数据SQL优化.md](../大数据SQL优化.md)；向量执行原理 → [../../db/db.md](../../db/db.md)
- 空间数据工程视角（GeoParquet/谓词下推）→ [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md) 的存储层章节

## 思考题（合上笔记再答）

1. ASOF 与"等价朴素查询"的实测差距有多大？为什么朴素版无法被优化器救回来？（0.24 s vs ≥115 s@10k；相关子查询逐行回表，无共享排序结构）
2. 本章哪些查询必须过"外部基准"这道关？举 spheroid 例子。
3. 用一条 PIVOT 把"航司×月航班量"转置，指出它的 GROUP BY/ON/USING 三部分各管什么。
4. EDA 质量门的四个数是什么（本章数据上）？p90 与 p99 差多少分钟、说明什么？（行数/DESCRIBE/NULL 率 1.48%/基数 628 机场·4897 架——实测 11 与 03 章实测 10；35→168 分钟：尾巴极重，均值叙事前先截尾或换分位）

## 2026 视角补注

- 航班延误这类"公开大 CSV→Parquet 分区→进程内 SQL EDA"链路已成数据教学的标准开局；2026 年同类数据集（如 DOT 官方 On-Time 全量 2 亿行级）本机依旧可跑——DIA 10 章 TPC-H/NYC 出租车与本目录航班三套数据集互为量级参照。
- spatial 扩展在 1.5.5 已可一行安装（实测 23.5 s），并携 **326 个 `st_*` 函数**（✅ `duckdb_functions()` 实抓）——GeoParquet 读写与 R-Tree 索引是 2024 后新卖点（官方 spatial 文档页 ✅ https://duckdb.org/docs/stable/extensions/spatial.html）。

## 核心概念速览（中英对照）

- **探索性数据分析** — EDA：先看图/分布/离群再建模的循环。
- **空间函数族** — Spatial extension / st_*：SQL 侧几何谓词与度量。
- **WKT** — Well-Known Text：`POINT/ POLYGON` 文本几何。
- **ASOF JOIN** — 时序"最近前值"不等值连接。
- **移动帧** — ROWS BETWEEN n PRECEDING：滑窗统计。
- **PIVOT** — 行转列聚合语法（ON key USING agg）。
- **分位数** — quantile_cont：连续插值分位，支持数组一次多分位。
- **Hive 分区** — 目录即列：year=/month= 升格查询谓词。
- **数据覆盖率** — JOIN 命中占比（本章 93.1% 实测）。
- **NaN 防御** — isnan()/NULLIF：距离与比率先滤再聚。

## 最新演进与工业实践

- **spatial 生态**：DuckDB spatial 由 community→core 化推进（安装即可用 ✅ 实测；文档 https://duckdb.org/docs/stable/extensions/spatial.html 200），GeoParquet 1.0（2024-11）把"空间列存"标准化，本书"SQL 内做空间"路线与之一脉。
- **窗口/PIVOT/ASOF 现状**：全部进入 1.x 稳定方言；ASOF JOIN 的算法口径（Sort-Merge 类）与关系理论梳理可在论文线追根 → [../../db/db.md](../../db/db.md)。
- **工业实践**：延误分析同款"外部基准校准"教训广泛见于地理数据工程博客（单位/椭球/坐标系三件套）；本目录 0.37 相对差为自测实证。
- **延伸**：想在本章数据上继续做"管道与质量"（GE/约束），转 DIA 第 8 章 dlt 叙事 → [../DuckDB_in_Action/08-构建数据管道.md](../DuckDB_in_Action/08-构建数据管道.md)。
