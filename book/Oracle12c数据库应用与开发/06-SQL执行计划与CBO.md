# 06 · SQL 执行计划与 CBO（优化器）

> **本章地图**：**执行计划怎么读**（`EXPLAIN PLAN` / `DBMS_XPLAN` / `v$sql_plan`）→ **优化器的三个阶段**（解析 / 查询转换 / 计划生成）→ **统计信息**（表/列/索引/系统级，`DBMS_STATS` 与直方图）→ **基数估算**（CBO 的命门）→ **成本模型**（CPU 成本 + I/O 成本；`optimizer_mode`）→ **访问路径**（见 [`05`](05-索引与约束.md)）→ **表连接**（嵌套循环 / 哈希连接 / 排序合并；12c 起还有 **笛卡尔连接**与 **并行连接**）→ **绑定变量与窥探 / 自适应游标共享（ACS）**→ **hint 与 SQL Plan Baseline / Profile**→ **并行执行**。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 读执行计划的三种姿势（从外到内）

```
--------------------------------------------------------------------------
| Id  | Operation          | Name | Rows  | Bytes | Cost (%CPU)| Pstart| Pstop |
--------------------------------------------------------------------------
|   0 | SELECT STATEMENT   |      |     1 |    38 |     3   (0)|       |       |
|*  1 |  INDEX RANGE SCAN  | IDX_E|     1 |    38 |     3   (0)|       |       |
--------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   1 - access("EMPNO"=7369)
```

读法要点：

1. **从内往外读**（`Id` 大的先执行：上例中 `Operation` 列里 `*1` 是叶子，先执行，再往上汇总）；
2. **`Rows` 是"CBO  estimated 行数"，不是实际行数**——所以它和真实行数差得越远，计划就越不可信；
3. **`Cost` 是相对成本，不是毫秒**；`(%CPU)` 是 CPU 成本占比；
4. **看 `Predicate Information`**：`access`（用来定位行，可走索引）与 `filter`（用来过滤，读了再筛）分列两边——**一个谓词写在 access 还是 filter，直接决定这个 SQL 快不快**；
5. 操作符要看全：`HASH JOIN`、`MERGE JOIN`、`NESTED LOOPS`、`SORT`、`TABLE ACCESS FULL`、`PARTITION RANGE ALL`、`PX ...`（并行）等。

教学示意，不参与构建：

```sql
-- 三种获取计划的姿势（教学示意，不参与构建）
EXPLAIN PLAN FOR SELECT * FROM emp WHERE deptno = 20;
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- 最常用：直接看已执行过的游标（含实际行数 A-/A-R）
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => 'xxxxxxxxxxxxx'));

-- 差别在哪：看 CBO 的估算依据
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => 'xxxxxxxxxxxxx', format => 'ALL +OUTLINE'));
```

### 1.2 优化器的三个阶段与"查询转换"

CBO 不是"收到 SQL 直接出计划"，它先做一串**等价改写**，这些改写决定了你写的 SQL 长什么样：

| 转换 | 含义 | 例子 |
| --- | --- | --- |
| **视图合并（view merging）** | 把子查询的视图拉平 | `WHERE x IN (SELECT ... FROM v)` → 直接连 v 的底表 |
| **子查询展平（subquery unnesting）** | 把 `IN`/`EXISTS`/`ANY` 子查询转成表连接 | 这是 `IN` 与 `EXISTS` 性能差不多的原因 |
| **谓词推进（predicate pushdown）** | 把过滤条件推到视图内部 | |
| **连接谓词推出（join predicate pushdown）** | 并行/分区场景把谓词推给远端 | |
| **排序消除（sort elimination）** | 用索引顺序替代排序 | `ORDER BY` 列恰好是索引前导列 |
| **OR 展开 / 转换（`OR-expansion`）** | `WHERE a=1 OR a=2` 拆成 `UNION ALL` | 就是这一条让 `IN` 列表变快 |
| **半连接/反连接转换** | `IN`/`EXISTS` → `SEMI`/`ANTI` join | 正是 `NOT EXISTS` 比 `NOT IN` 稳的原因 |

**重要结论**：因为子查询展平与 `OR` 展开的存在，**"手写 SQL 与优化器改写后的 SQL 性能差不多"是有条件的**——当 SQL 里有复杂视图、聚合、以及 `ROWNUM` 与 `DISTINCT` 的相互作用时，转换会被限制，此时手写重写才显著有效。

### 1.3 统计信息与直方图：CBO 的输入

CBO = **f(sql 转换) × f(统计信息) × f(数据分布)**。三者任一失真，计划就错。

- **表级统计**：行数、块数、平均行长（`USER_TABLES.NUM_ROWS` 等，注意这些列**只在收集统计后才有值**）；
- **列级统计**：最小值、最大值、NDV（不同值数量）、NULL 数；
- **直方图**：NDV 很高（比如 > 254，12c 起更宽松）的列默认值是 **Height-Balanced** 直方图，采样不足时会失真；
- **系统统计（system statistics）**：`CPU 速度、IO 速度、多块读计数（`optimizer_index_cost_adj`、`optimizer_dml_rate`、`db_file_multiblock_read_count` 的有效值）**——**系统统计缺失（12c 起默认不收集）是最常见的"优化器估算离谱"的原因之一**。

教学示意，不参与构建：

```sql
-- 收集统计（教学示意，不参与构建）
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(
    ownname => 'MYSHOP', tabname => 'EMP',
    estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
    method_opt   => 'FOR ALL COLUMNS SIZE AUTO',   -- 让 Oracle 决定哪些列要直方图
    cascade      => TRUE,                          -- 同时收集索引
    degree       => 8);                            -- 并行度
END;
/
-- 看列的统计与直方图桶数
SELECT column_name, num_distinct, num_nulls, density, histogram, num_buckets
FROM user_tab_columns WHERE table_name='EMP';
-- 12c 起：看优化器对某次执行的选择过程
-- SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id=>'...', format=>'+PEEKED_BINDS'));
```

### 1.4 基数估算：CBO 的命门

CBO 用**选择率（selectivity）**× 总行数估算每一步返回多少行。选择率的估算规则：

| 谓词 | 估算 |
| --- | --- |
| `col = literal` | 1 / NDV |
| `col > v`（无直方图） | 默认值（约 5%）——**与真实分布无关** |
| `col LIKE 'x%'` | 默认 10% |
| 多个谓词 AND | **各选择率相乘**（独立性假设）——这是偏差的主要来源 |
| 有直方图时 | 按桶内实际分布估——**更准，但也更依赖采样质量** |

**为什么"多条件 AND 相乘"是灾难**：`WHERE status='A' AND region='CN' AND cat='X' AND dt=...` 每个条件 1% → 估算 1e-8 行 → CBO 认为"几乎只有一行"→ 选 **嵌套循环** 且认为索引极好 → 实际返回 50 万行。这就是"一个 SQL 突然从 0.1 秒变成 300 秒"最常见的剧本。

**修复手段**（按代价从低到高）：收集直方图、收集扩展统计（`DBMS_STATS.GATHER_TABLE_STATS` 的 `method_opt => 'FOR COLUMNS (a,b,c) SIZE ...'`，12c 起支持多列统计）、改 SQL 结构、加 hint。

### 1.5 表连接的三种方式与适用场景

| 方式 | 适用 | 代价构成 |
| --- | --- | --- |
| **NESTED LOOPS** | 外表返回**少量行**、内表有**唯一/低选择率索引** | 每驱动一行读一次内表 |
| **HASH JOIN** | **大表 join 大表**，一个可分批 | 构建 hash 表（PGA!）→ 探查 |
| **MERGE JOIN** | 两表都**有序**（索引或已排过） | 匹配时几乎不再有 I/O，但要排序 |
| **CARTESIAN（笛卡尔）** | 一般是** bug**（缺连接条件） | 行数暴涨，生产事故 |

> **hash join 是 PGA 的主要杀手**：以为在"跑 SQL"，其实在**消耗 PGA**。`WORKAREA_SIZE_POLICY=AUTO` 下，hash join 的 build phase 若 PGA 不够会**溢出到临时表空间**（`v$sql_workarea_active_all` 可以看到溢出的 SQL）。这把 `05` 章的索引讨论与 `02` 章的 PGA 讨论串起来了。

教学示意，不参与构建：

```sql
-- 看 Sql 的工作区（workarea）是否溢出到临时表空间
SELECT sql_id, operation_type, work_area_size, actual_mem_used, num_rows
FROM v$sql_workarea_active_all;
```

### 1.6 绑定变量、窥探与自适应游标共享（ACS）

| 概念 | 含义 |
| --- | --- |
| **绑定变量** | `WHERE sal > :b` —— 让同一条 SQL 复用执行计划 |
| **绑定变量窥探（peeking）** | 硬解析时**窥视 first fetch 的绑定值**并按它生成计划 |
| **自适应游标共享（ACS，12c 起）** | 发现"同一 SQL 在不同绑定值下最优计划不同"时，**自动并行生成多个子游标**，各按各自的值范围执行 |
| **字面量绑定（literal binding）** | `WHERE sal > 1000` 直接写值 → 计划永远按 1000 估，但对 OLAP 反而常常更准 |

**实践结论**：

- **OLTP（高并发、同构请求）→ 必须绑定变量**（省解析、省 shared pool）；
- **OLAP/报表（少量执行、异构参数）→ 字面量更好**（每次都能按真实值估）；
- ACS 是 12c 之后给"OLTP 也有倾斜参数"的解法，但**代价是同一 SQL 出现多个子游标**（`v$sql` 里同一 `sql_id` 多行，`version_count` 上升），可能造成 shared pool 膨胀与"计划突然重复编译"。

### 1.7 hint、SQL Profile 与 Plan Baseline

| 手段 | 谁维护 | 持久性 | 适用 |
| --- | --- | --- | --- |
| **hint（注释）** | 开发写在 SQL 里 | 跟随 SQL 文本 | 临时压制某个问题；**改 SQL 才失效** |
| **SQL Profile** | `SQL Tuning Advisor` 生成，`DBMS_SQLTUNE` 导入 | 数据库字典 | 不改应用代码就能拿到"更好的计划"（**这是 OLTP 上最有价值的**） |
| **Plan Baseline** | `DBMS_LOAD balanced / DBMS_SPM` | 数据库字典 | **冻结好计划，防止升级/统计变化导致回归** |

> 生产上最实用的一条：**"某条 SQL 稳定运行了三年，某天突然慢了"——第一件事不是加 hint，而是用 `SQL Tuning Advisor` 生成 SQL Profile**，因为改应用代码要发版。

教学示意，不参与构建：

```sql
-- 冻结计划（教学示意，不参与构建）
DECLARE
  v_ret VARCHAR2(20);
BEGIN
  v_ret := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(sql_id => 'abcd1234abcd1234');
END;
/
-- 基线里看已有哪些计划
SELECT signature, plan_id, enabled, accepted FROM dba_sql_plan_baselines;
```

### 1.8 并行执行

- **并行度来源**：表上的 `PARALLEL` 属性、hint `/*+ PARALLEL(8) */`、会话级 `ALTER SESSION FORCE PARALLEL QUERY`、以及 `PARALLEL_DEGREE_POLICY`（12c 起可 AUTO/ADAPTIVE）。
- **代价**：并行**不省 CPU**，它用多进程把工作切分，**消耗更多 PGA/临时表空间**，并在 12c 起通过 **并行语句队列（`parallel_degree_limit`、`PARALLEL_SERVERS_TIME_LIMIT`）** 排队控制吞吐。
- **最常见的错用**：给一个 OLTP 高频 SQL 加 `PARALLEL(4)`，结果把实例的资源吃光，整库变慢。

## 二、版本演进

| 版本 | 优化器相关变化 |
| --- | --- |
| 10g | 自适应游标共享雏形；`optimizer_index_cost_adj` 更常用 |
| 11g | 12c 之前最"完美"的一版；SQL Plan Management（baseline）成熟；`optimizer_adaptive_features` 的前身 |
| **12.1** | **默认启用自适应特性**：`optimizer_adaptive_features` 默认 TRUE，`optimizer_adaptive_sql_plan` 引入（规划阶段统计信息缺失时**自动做嵌套循环→哈希连接的转换、自动创建索引**） |
| **12.2** | **自适应特性默认关闭**（改为 `optimizer_adaptive_features=FALSE`），改为更可控的 `optimizer_adaptive_plan`/`plan_hash_2` —— 这是**版本迁移时最著名的"计划突然变了"来源** |
| 18c/19c | 自适应能力继续保留在 `optimizer_adaptive_*` 参数里；`DBMS_AUTO_INDEX` 出现 |
| 21c/23c | **自动索引 GA**（19c/21c 预研）；数据库内建 AI/向量优化路径 |

🔧 **2026 年必须补的四条**：
1. **`optimizer_adaptive_features` 在 12.1 与 12.2 的默认值相反**——跨版本"同 SQL 不同计划"的头号原因。升 12.1 → 12.2/19c 时，**先查这个参数再分析问题**（详见 `14` 的版本坑）。
2. **`result_cache` 的默认行为在 12.x 有变化**，与 `CLIENT_RESULT_CACHE` 联动，可能造成"同样的 SQL 结果不刷新"的意外（也是缓存一致性问题）。
3. **`MAX_STRING_SIZE=EXTENDED`** 之后 `VARCHAR2(32767)` 的**行长度可能超过块大小**，导致行链接与并行度估算错误。
4. **`DBMS_STATS` 的 `method_opt` 与扩展统计（multi-column statistics）** 在 12c 之后才完整可用，本书时代的常见做法（`SIZE AUTO` + 手动直方图）已足够，但值得补"扩展统计"这一层。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Elmasri & Stadler 等《Query Processing in Database Systems》相关章节 | 教材（如《Fundamentals of Database Systems》） | **通用理论，非 Oracle 专属**：选择率估算、连接算法（嵌套循环/排序合并/散列）的复杂度分析 |
| Selinger 等《Access Path Selection in a Relational Database Management System》 | SIGMOD 1979 | **通用理论，非 Oracle 专属**：System R 的**动态规划**执行计划选择，是所有关系库优化器的思想源头 |
| Goel 等《Optimizer Statistics-Based Query Reconfiguration in Hypertable》（或更贴近的：《Cardinality Estimation for Joins》） | 综述文献 | **通用理论，非 Oracle 专属**：基数估算误差的累积效应 |
| Graefe《 volcano / cascade 优化器框架》 | *The Volcano Optimizer Framework*（IEEE Data Eng. Bull. 1993） | **通用理论，非 Oracle 专属**：迭代式计划搜索框架 |
| Oracle《Oracle Database SQL Tuning Guide》"Overview of the Optimizer" | Oracle 官方文档（非论文） | 查询转换、成本模型、hint 的权威描述 |

> 说明：**关系查询优化是数据库领域的通用理论**，上述均为**通用理论，非 Oracle 专属论文**。Oracle 的 CBO 在细节（自适应计划、Plan Baseline）上自行演进，其权威描述在 Oracle 官方文档而非学术论文中。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **ML xCBO**：*Learning to Optimize Queries*（*Deep-Learned Cardinality Estimator*, SIGMOD 2019）、*Theta System*（VLDB 2019）等，用学习模型替代直方图估算基数；
  - **基数误差研究**：*Cardinality Estimation on Cardinality Estimation*（VLDB 2019）系统刻画了误差如何沿计划树传播——这正是本章 1.4"AND 相乘"灾难的学术表述；
  - **可观测性与归因**：eBPF 与 HdrHistogram 类工具用于把"某条 SQL 慢"定位到资源层（见 `07`）。
- **工业界开源**（star 为 2026-09-25 `gh api` 实测）：
  - `alibaba/Druid`（≈28178★）：连接池内置 **Oracle 慢 SQL 与执行计划输出**，是"开发侧看见 CBO 行为"最常见的入口。
  - `apache/shardingsphere`（≈20804★）：中间件层的**执行计划路由与分片下推**，逻辑与本章 "查询转换/谓词推进" 同构。
  - `pingcap/tidb`（≈40586★）：优化器源码（`planner/core`）是**开源世界里最接近现代 CBO 的完整实现**，读它比读任何 Oracle 内部文档都更能理解本章 1.2/1.4 的机制。
  - `debezium/debezium`（≈13152★）：虽然偏 CDC，但其 Oracle 连接器会按 SQL 指纹与日志位点工作，可反向观察"SQL 标识 / 绑定值 / 执行计划"三者的关系。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "`Rows` 列就是 SQL 返回的行数" | 它是 **CBO 估算值**；与实际差得多往往就是问题的根源 | SQL 优化最佳实践（统计信息章） |
| 2 | "`EXPLAIN PLAN` 看到的就是实际计划" | 它只反映**未执行的估算**；实际计划要看 `DBMS_XPLAN.DISPLAY_CURSOR`（含真实行数） | 全部 9 本（多数用 `EXPLAIN PLAN` 举例） |
| 3 | "统计信息收一下就好了" | 若**选择率模型本身错**（多列相关、数据倾斜），要补**直方图**与**扩展统计** | SQL 优化最佳实践（统计信息章） |
| 4 | "12c 和 12.2 的优化器行为一致" | **不一致**：`optimizer_adaptive_features` 在 12.1 默认 TRUE、12.2 默认 FALSE，会引起计划回归 | 全部 9 本（成书早于 2018） |
| 5 | "绑定变量永远是好的" | OLAP 场景字面量更准；OLTP 才必须绑定 | SQL 优化最佳实践（游标章）讲的是开发视角，未给 OLAP/OLTP 的分界 |
| 6 | "加 hint 是修复计划问题的正道" | hint 跟着 SQL 走，改代码才失效；更稳的是 **SQL Profile / Plan Baseline** | 全部 9 本 |
| 7 | "并行能提升 OLTP 性能" | 并行是**吞吐换资源**，OLTP 高频 SQL 上加并行会拖垮实例 | 高并发 Oracle 书（内部扩展维）未提这一反面 |
| 8 | 🔧 "`result_cache` 默认不会带来意外" | 12.x 起 `client_result_cache` / `server result cache` 行为与旧版不同，**数据不刷新**与多子游标是实际踩过的坑 | 🔧 全部 9 本 |
| 9 | 🔧 "自动索引是好事" | 19c/21c/23c 的**自动索引会偷偷建索引**，需要显式开关与监控；同时"ML 优化器"在学术界方兴但工业界仍以可控为先 | 🔧 全部 9 本均未覆盖 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`05-索引与约束.md`](05-索引与约束.md)（索引提供访问路径，CBO 决定选哪条）
- **下一章**：[`07-SQL性能诊断与调优实践.md`](07-SQL性能诊断与调优实践.md)（本章讲"计划怎么来"，下一章讲"怎么发现它错了"）
- **强相关**：[`08-常见SQL误区与最佳实践.md`](08-常见SQL误区与最佳实践.md)（本章的"基数估算"与"索引失效"在后一章以反模式形式出现）
- **理论对照**：[`数据库系统概念6/13-查询优化.md`](../数据库系统概念6/13-查询优化.md)（动态规划连接顺序搜索、代价模型、统计信息；本章 1.2/1.3 的学术版）
- **其他书**：《SQL优化最佳实践》是本套里 CBO 部分的主支撑——原理篇（优化器/成本/执行计划/统计信息/解析/游标/绑定变量）+ 实战篇（查询转换/访问方式/表关联/半反连接/子查询/排序/并行）几乎与本章同构，建议对照读；《SQL应用及误区分析》第 7–12 章从开发视角讲索引/约束的实际效果。
