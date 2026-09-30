# 07 · Advanced SQL（Ch7 · OLAP/CTE/MERGE 的高阶武器架）

> 章名 ✅ InformIT 出版社页实抓；正文 ⚠️ 转述重构，语法示意非实测。

## 一、章定位

9.x 时代 DB2 的 SQL 能力跃迁：分析函数（OVER）、分组集、公用表表达式与递归、变更表（mutation tables）、层级查询。对 DBA 而言本章是"看懂应用 SQL 计划"的前置，对开发者是"少写游标循环"的转换点。

## 二、OLAP/窗口函数（⚠️ 转述）

1. 谱系：`RANK/DENSE_RANK/ROW_NUMBER/COUNT/SUM/AVG ... OVER (PARTITION BY ... ORDER BY ... ROWS/RESETS UNBOUNDED PRECEDING)`。
2. 位移族：`LAG/LEAD/FIRST_VALUE/LAST_VALUE/NTH_VALUE`（后两者版本覆盖 ⚠️ 存疑）。
3. 分桶：`NTILE(n)`；周期聚合配 `FETCH FIRST` 出 Top-N by group 的三层套娃模板。
4. 计划形态：窗口函数引入 spool/sort（TBLOCK ⚠️ 算子名以 EXPLAIN 现行为准），大分区窗口吃排序内存（→14 章 sortheap）。

## 三、分组集与立方（⚠️ 转述）

- `GROUP BY ROLLUP(a,b)/CUBE(a,b)/GROUPING SETS((a),(a,b),())` + `GROUPING()` 判层级小计行。
- 与 MQT 汇总表（05 章）互补：MQT 预聚合、分组集现算；数据量决定路线。
- `SELECT * FROM FINAL TABLE(DELETE ...)` 类变更表在第七节单列——但作者把"OLD/NEW TABLE"与分组集同章讲，读时别混：前者是 DML 副产物关系，后者是聚合语法糖。

## 四、CTE 与递归（⚠️ 转述）

1. `WITH c AS (SELECT ...) SELECT ...`：命名步骤、可读性、优化器一般**内联展开**（非物化）——与临时表取舍是经典 DBA 题。
2. 递归：`WITH RECURSIVE tree(... AS (种子 UNION ALL 递归体) )` + `WITH RECURSIVE`/`CYCLE`?（DB2 用 `WITH RECURSIVE` + 列类型定义，环检测靠 `FETCH FIRST` 或 CASE 截断，⚠️ 具体语法核现行）。
3. 变更表：`INSERT INTO ... FROM FINAL TABLE(UPDATE ...)` 审计快照范式；`NEW TABLE/OLD TABLE`。
4. 层级查询：`START WITH ... CONNECT BY PRIOR`（DB2 9.5 加入兼容 Oracle 方言，⚠️ 版次存疑）——与递归 CTE 双轨并行是本时期特色。

## 五、其他高阶件（清单式，⚠️）

- `MERGE` 与 SCD Type-2 模板（06 章接口）。
- 全外连接语义与 ANSI 混用陷阱（老 `(*)` 方言 vs JOIN，9 时代两代 SQL 并存）。
- 相关标量子查询消改解相关：DB2 优化器自动去相关（简单式），复杂仍需手工改 JOIN——731 考点。
- `VALUES` 独立语句与表构造器；`INSERT INTO t SELECT ... FROM FINAL TABLE(...)`。
- 同义/多表视图的键保留更新规则回看 05 章。

## 六、EXPLAIN 视角读本章（与 09/14 章接口）

```text
db2expln -d demo -q "SELECT dept, SUM(salary),
  RANK() OVER (ORDER BY SUM(salary) DESC) FROM emp GROUP BY dept" -g -t
```

- 读输出三件事：访问方式（IX/TL/HSAP ⚠️ 码表）、是否出现 SORT/TBLOCK、基数估计与 STATS_TIME 新鲜度（→12 章）。
- 分析函数常见形态：基表扫+SORT+WINDOW 函数算子；分区数多时 temp table space 压力（→11 章 TEMP）。

## 七、易错雷点（例题库精华）

1. `RANK` 与 `DENSE_RANK` 并列跳号差异选错出报表事故。
2. `ROWS BETWEEN` 帧界（UNBOUNDED PRECEDING）与逻辑"至今"口径不一致。
3. 递归 CTE 无界环 → 指数爆炸；先 `FETCH FIRST` 兜底。
4. GROUPING SETS 与 NULL 真实值混淆（用 `GROUPING()` 区分）。
5. CTE 内嵌 DML 带副作用：多次引用同一含 `FINAL TABLE` 的 CTE 行为未定义类（⚠️ 保守读法）。
6. CONNECT BY 与递归 CTE 结果顺序无保证（ORDER SIBLINGS BY 属 Oracle 兼容面 ⚠️ 存疑）。

## 八、自查问题

- 说出窗口帧 ROWS vs RANGE 差异与 DB2 支持面（⚠️）。
- 分组集三种写法各自产出行数算式？
- 递归 CTE 与 CONNECT BY 的选型三问？
- FINAL TABLE 审计范式的最小代码？
- CTE 何时该降级为全局临时表？给出统计口径依据。
- 本章哪个语法与 Oracle 同源、哪个与 SQL:2003 同源？（分层记忆）
- 与 #93 Databases Illuminated（登记名，SQL 标准叙事）在本章的互补点？
- 方言表中 RETURNING 与 FINAL TABLE 的语义谁更通用？（第九、十节合读）
- MERGE 的 WHEN 子句缺 NOT MATCHED 分支会发生什么？（回读第二节第 3 条）
- 分组集行数算式：CUBE(a,b,c) 产多少组小计组合？（第三节）

## 九、语法引入时间轴（⚠️ 保守口径）

| 语法件 | 进入 DB2 的大致版次 | 备注 |
|---|---|---|
| OLAP 函数 OVER | 8.x 已有雏形→9 完善 | ⚠️ 分界存疑 |
| ROLLUP/CUBE/GROUPING SETS | SQL:2003 对齐期，9.x | ⚠️ |
| CTE（WITH）/RECURSIVE | 早期版本已具（8 系） | 书中作"复习+进阶" |
| 变更表 FINAL/NEW/OLD | 9 时代 | 原书本章明讲 |
| MERGE | 8.2/9 | 06 章接口 |
| CONNECT BY | 9.5（Oracle 兼容） | ⚠️ 版次存疑 |
| MATCH_RECOGNIZE | 书后（11.1） | 本册无 |

## 十、跨引擎方言对照（迁移速记）

| 需求 | DB2 | Oracle | PG/MySQL8 |
|---|---|---|---|
| 限行 | FETCH FIRST n ROWS ONLY | ROWNUM/FETCH FIRST | LIMIT |
| 层级 | CONNECT BY(9.5⚠️)/递归 CTE | CONNECT BY | 递归 CTE |
| 小计 | GROUPING SETS | GROUPING SETS | GROUP BY ROLLUP（子集） |
| DML 取像 | FINAL TABLE | RETURNING | RETURNING |
| 序列取值 | NEXTVAL FOR seq | seq.NEXTVAL | nextval()/AUTO_INCREMENT 异 |
| 窗口帧 | ROWS BETWEEN | 同 | 同 |

## 十一、快速回看卡（本文件内导航）

- 帧界口诀：第二节第 1 条括注 RESETS? 以现行语法核，雷点 2 给了事故版本。
- 递归防爆三招：FETCH FIRST 兜底/深度列截断/先小样本验。
- CTE vs GTT 选择三问：复用次数/物化收益/统计可见性（第四节第 1 条展开）。
- EXPLAIN 三件事：第六节列表——本章所有语法最终都要在计划里现形。
- 与后续章接口：MERGE 装载面→06 章；统计/基数→12 章；WLM 管资源→14 章。
- 半结构化预告：本章"表达力"叙事在 08 章以 XML 重演一遍，读 08 时可回看本节方言表。

## 核心概念速览（中英对照）

- **OLAP function** — 分析函数：OVER 子句的行间计算族
- **window frame** — 窗口帧：ROWS/RANGE BETWEEN 定义的计算窗
- **RANK/DENSE_RANK** — 排名：跳号与不跳号两种并列处理
- **grouping sets** — 分组集：一次查询出多层小计
- **ROLLUP/CUBE** — 上卷/立方：分组集语法糖
- **CTE** — 公用表表达式：WITH 命名的查询步骤
- **recursive CTE** — 递归 CTE：种子+递归体的闭包计算
- **mutation table** — 变更表：NEW/OLD/FINAL TABLE 取 DML 前后像
- **MERGE** — 合并：条件写一体化（06 章呼应）
- **decorrelation** — 去相关：标量子查询改连接
- **FETCH FIRST n ROWS ONLY** — 前 n 行：DB2 限行方言
- **CONNECT BY** — 层级遍历：Oracle 兼容方言（9.5 ⚠️）

## 最新演进与工业实践

- SQL 标准追赶：Db2 11.5/12 补齐 `MATCH_RECOGNIZE`（行模式识别）、JSON 函数族（JSON_TABLE 等）、聚合 `FILTER`——本章语法已"地板化"，新考点在 JSON 半结构化面（⚠️ 转述；入口 ✅ https://www.ibm.com/docs/en/db2 ）。
- 工业实践位移：OLAP 函数重活移向 DuckDB/ClickHouse 等分析引擎，DB2 侧窗口查询仍以交易报表为主；概念层跨引擎同构——可在 DuckDB 跑同款语法做对照实验（本目录纪律：类比不标 🔧，因非本书行为域，参见 00 文件登记表）。
- 递归与图查询：SQL/PGQ 属性图标准化进程中（⚠️ 论文线 [../../db/db.md](../../db/db.md)），DB2 尚无对应面——本书本章内容在 2026 的价值转为"关系表达力谱系"认知。
- 认证线：731 不考深 SQL，733 考；与 `IBM_Db2_11_1_Certification_Guide`（登记名）SQL 域互补。
- 教学锚点：与《高性能mysql》同代窗口章节对照（[../高性能mysql.md](../高性能mysql.md)）可见 MySQL 8 与 DB2 9.5 在 RANK/CTE 上几乎同期落地。
