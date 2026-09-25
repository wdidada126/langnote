# 第 16 章 神兵利器——optimizer trace 的神奇功效

> 原书说明：标题为「神兵利器——optimizer trace 的神奇功效」，基于 MySQL 5.7.22 撰写。本文件按其思路展开「成本和规则优化」两条线，并补齐 5.7/8.0 的成本模型改进与 2020 年之后必须补的**直方图、`EXPLAIN ANALYZE`、并行查询 `n_jobs`、CTE 物化**。

## 本章地图

> 一句话：**MySQL 优化器做两件事——先按「规则」改写 SQL（子查询转连接等），再按「成本」在若干条候选路线里挑最便宜的一条；`optimizer_trace` 就是把这两件事的中间产物完整录下来。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 16.1 两条优化线 | 规则优化（改写）/ 成本优化（选路） | 规则决定候选集，成本决定赢家 |
| 16.2 成本模型的组成 | I/O 成本 + CPU 成本、页读取、记录评估 | 所有估算最终都折算成「读多少页、比多少行」 |
| 16.3 `optimizer_trace` 怎么用 | 开启、执行、`SELECT ... FORMAT=JSON` | 一次会话内切换，勿长期打开 |
| 16.4 trace 的三个关键阶段 | `rows_estimated` / `rows_actual`、`considered_access_paths`、`reconsidering_access_paths` | 重点看「估算 vs 实际」的鸿沟 |
| 16.5 统计信息从哪来 | 持久化统计、采样、`information_schema` 表 | **统计不准是选错路线的头号原因** |
| 16.6 规则优化：改写清单 | 子查询转连接、派生表合并、外连接转内连接、`semijoin` | 改写常比「加索引」更立竿见影 |
| 16.7 排序与连接的成本连带 | `filesort` 成本、`join` 顺序比较 | 单表便宜不代表整体便宜 |
| 16.8 🔧 2026 视角 | 直方图、`EXPLAIN ANALYZE`、`n_jobs`、8.0 提示变化 | 2020 年之后「看优化器」的方式彻底变了 |

## 核心精讲

> **教学示意，不参与构建。** 下文 SQL 片段与 JSON 结构仅为讲清 trace 的字段含义，**未在本机编译、未连接任何 MySQL 实例执行**；trace 里的具体数字随版本与数据分布变化。

### 16.1 两条优化线：规则与成本

- **规则优化（基于规则的优化，RBO 色彩）**：把 SQL 改写成「等价但更好执行」的形态。
  - 子查询 → 半连接 / 连接；
  - 派生表（派生查询）→ 合并进外层（若可行）；
  - 外连接 → 内连接（若 `WHERE` 保证不可能为 NULL）；
  - `IN (subquery)` → `semijoin` 策略（duplicates weed-out / firstmatch / loosescan / materialization）。
- **成本优化（CBO）**：为每条候选路线估算成本，取最小。
  - 候选路线包括：全表扫描、各个索引的全扫描、各个索引的范围扫描、索引 + 回表、覆盖索引等。
- 原书的核心比喻很贴切：**规则优化决定「有哪些选项」，成本优化决定「选哪个」**。二者谁先谁后、是否有循环（rule-based rewriting 可能反复触发），是 5.6/5.7 优化器重构前后的主要差别。

### 16.2 成本模型的两块砖：I/O 成本与 CPU 成本

- 优化器把一切折算成两种单位（对应 `mysql.engine_cost` / `mysql.server_cost` 两张表，可改）：
  - **I/O 成本**：读一个页的代价，默认 ≈1.0（范围扫描时按落在缓冲池/磁盘分别计）。
  - **CPU 成本**：处理一行记录的代价，默认 ≈0.2（读取行）与 0（键值比较，便宜得多）。
- 于是**「回表」很贵**这件事被自然表达出来：
  ```text
  覆盖索引扫描：读 100 页 + 处理 10000 行 = 100 × 1.0 + 10000 × 0.2
  二级索引 + 回表：读 100 页 + 10000 次回表（每次 ≈ 若干页 × 1.0）+ 处理 10000 行
  → 回表把成本放大了几十倍，优化器因此可能在「range」与「full scan」之间翻案
  ```
- 🔧 **成本模型是可调的**：`SELECT @@innodb_page_cost` 这类引擎成本可以改；但**改成本参数是最后的手段**，先改统计与索引。

### 16.3 `optimizer_trace` 怎么用

```sql
-- 教学示意，不参与构建
SET optimizer_trace="enabled=on";          -- 仅当前会话生效
SELECT * FROM t1 JOIN t2 ON t1.a = t2.b;   -- 要观察的语句
SELECT * FROM information_schema.OPTIMIZER_TRACE;
SET optimizer_trace="enabled=off";
```

- 注意点：
  - `information_schema.OPTIMIZER_TRACE` 每会话只保留**最后一条**被跟踪的语句。
  - 输出很大（`FORMAT=JSON` 可压缩），长期打开会拖慢会话，属于**排查期工具**。
  - `optimizer_trace_max_mem_size` 太小会截断 trace，导致看不到后半段（常见「trace 里没有 `reconsidering_access_paths`」的原因）。
- 原书推荐的操作流程，2026 年依然有效：
  1. `EXPLAIN` 看走没走索引；
  2. 走错 → `optimizer_trace` 看**为什么**（估算行数差多少）；
  3. 估算离谱 → 修统计 / 加直方图 / 改索引；
  4. 估算正常但仍然选错 → 考虑索引提示或 `STRAIGHT_JOIN`。

### 16.4 trace 结构里最值得看的字段

| 字段 | 含义 | 典型问题 |
| --- | --- | --- |
| `rows_estimated` | 优化器**估算**要扫描的行数 | 与 `rows_actual` 差一个数量级 = 统计不可信 |
| `rows_actual` | **实际**扫描行数（只在 `EXPLAIN ANALYZE` / 部分 trace 字段里可见） | 估算/实际鸿沟的直接证据 |
| `considered_access_paths` | 所有被考虑过的访问路径及各自成本 | 看看有没有「根本没被考虑」的索引 |
| `reconsidering_access_paths` | **因连接顺序变化而重新评估**（多表连接时反复出现） | 说明优化器在连接顺序上做了回溯 |
| `cost_info` | 各路径的 I/O / CPU 成本明细 | 用来解释「为什么它选了 A 而不是 B」 |
| `steps` / `transformation` | 规则改写步骤（如 `semijoin`、`derived_merge`） | 看优化器做了哪些等价变换 |
| `index_info` | 被评估的索引及选择率 | 索引存在但选择率被高估 |

- 一句话经验：**trace 里最有价值的是「`rows_estimated` 与实际差多少」，而不是「最终选了哪个」**。

### 16.5 统计信息：优化器的眼睛

- MySQL 的统计有两种存放方式：
  - **非持久化**（5.6 之前 / 部分场景）：每次 `ANALYZE` 后只存内存，重启丢失。
  - **持久化统计信息**（5.6+ `innodb_stats_persistent`，5.7 默认开）：写入 `mysql.innodb_table_stats` / `mysql.innodb_index_stats`。
- 采样方式：`innodb_stats_persistent_sample_pages`（默认 20 页）采样估算索引选择性。
  - **采样少 = 估算差**。一张 5000 万行的表只采样 20 页，遇到**数据倾斜**（99% 同值）必然估算离谱。
- 🔧 **直方图（8.0）**：`ANALYZE TABLE t UPDATE HISTOGRAM ON col WITH 100 BUCKETS;`，结果存在 `information_schema.COLUMN_STATISTICS`。它 Cost 模型能拿到**真实分布**，是针对「倾斜列索引选错」的手术刀级方案。
- 运维提示：`ANALYZE TABLE` 会刷新统计但也会带来负载，生产上建议**在低峰期 + 只读从库**执行。

### 16.6 规则优化：改写清单（原书第 14 章的对照）

| 改写 | 触发条件 | 收益 |
| --- | --- | --- |
| 子查询 → 半连接（`semijoin`） | `IN (subquery)` / `=ANY` | 避免「外层每行跑一次子查询」 |
| `semijoin` 策略选择 | `firstmatch` / `duplicates weed out` / `loosescan` / `materialization` | trace 里可见选择 |
| 派生表合并（`derived_merge`） | 派生表无聚合/`LIMIT`/`DISTINCT` 等阻挡条件 | 把派生条件下推，减少临时表 |
| 派生表物化 | 有 `GROUP BY` / `DISTINCT` / `LIMIT` 等 | 生成临时表，可能反而更快 |
| 外连接 → 内连接 | `WHERE` 中对右表列有限制条件 | 缩小搜索空间 |
| 常量折叠 / 表达式简化 | `WHERE 1=1`、`a=1 AND a=1` | 减少运行时计算 |
| 🔧 8.0：CTE 默认**不**自动合并 | `WITH` 查询默认物化 | 报表 SQL 里「同一张表扫多次」的常见来源 |

- 🔧 注意：5.7 把 `derived_merge` 默认打开，8.0 对 CTE 的处理又变了一轮；**从 5.7 升到 8.0 后，复杂 SQL 的 `EXPLAIN` 形态变化是常态**，不要假设「优化器一定更聪明」。

### 16.7 单表便宜 ≠ 整体便宜

- 多表连接时，优化器会为**每一层**重新评估访问路径，这就是 trace 里大量出现 `reconsidering_access_paths` 的原因。
- 排序成本也会被计入：若最终输出需要 `filesort`，优化器会把「排序本身的成本」折算进候选路线的比较。
- 因此排查连接慢查询时，要看的是**整棵执行计划的代价树**，而不是某一层的 `type`。

### 16.9 🔧 一套可复用的排查流程

```text
① EXPLAIN                     → 走的什么路线（估算）
② 路线不对？开 optimizer_trace → 看 considered_access_paths 与 rows_estimated
③ rows_estimated 离谱          → ANALYZE TABLE / 建直方图（倾斜列）
④ rows_estimated 正常但仍选错   → 补缺失索引 / 用 8.0 优化器提示 / 重建统计
⑤ 仍不解决                    → EXPLAIN ANALYZE 看 rows_actual，确认是不是执行器的问题
⑥ 生产上必须改计划              → 隐藏索引灰度，或 STRAIGHT_JOIN（先记录理由）
```

- 使用 `optimizer_trace` 的三条纪律（原书风格的做法，2026 依然适用）：
  1. **只在排查时开**，不要在长期运行的实例上打开；
  2. 每次只跟踪一条语句，`information_schema.OPTIMIZER_TRACE` 会被覆盖；
  3. **把 trace 当作提交记录留档** —— 「这条 SQL 为什么选了 A 路线」在半年后仍然是最有价值的信息。
- ⚠️ 一个常被忽略的事实：**trace 里的 `rows_estimated` 出现一次并不足为奇；只有当它与「语句真实的匹配行数」差一个数量级以上时，才说明统计或基数估算出了问题。**
- ⚠️ `optimizer_trace` 的**局限**：它是**静态成本比较**的录像，不含任何真实执行数据 —— 所以它对「改写阶段为什么没做某个变换」（`reconsidering_access_paths` 缺失）很有解释力，但对「估算行数为何偏离」只能给出一个方向。要看到真实行数与真实耗时，必须上 `EXPLAIN ANALYZE`，或在 5.7 上对比 `EXPLAIN` 的 `rows` 与随后 `EXPLAIN ANALYZE` 的实际值。
- 🔧 **把 trace 固化为回归测试**：对几条核心慢 SQL，在 CI/发布前的脚本里采集 `optimizer_trace` 的关键字段（最终选中的 `access_path`、`rows_estimated`、改写步骤），与历史基线比对 —— 索引变更、统计刷新、大版本升级都能在上线前被提前发现。

## 版本演进

| 版本 | 优化器相关变化 |
| --- | --- |
| 5.6 | 优化器重构；`semijoin`；持久化统计可配；ICP/MRR |
| 5.7 | 成本模型改进（范围扫描按页估算）；`derived_merge` 默认开；`OPTIMIZER_TRACE` 输出更细 |
| 8.0 | 直方图、隐藏索引、降序索引、表达式索引；优化器提示大幅简化；CTE 不默认合并 |
| 🔧 8.0.18 | `EXPLAIN ANALYZE`（真正执行并输出实测耗时/行数） |
| 🔧 8.0.22 | 并行查询 `n_jobs`，部分算子可并行 |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Selinger et al., *Access Path Selection in a Relational Database Management System* | SIGMOD 1980 | 成本式访问路径选择的开山之作 |
| Chaudhuri, *An Overview of Query Optimization in Relational Systems* | PODC 1995（invited talk 综述） | 规则与成本两条优化线的经典划分 |
| Markl et al., *Improving Row Estimation by Database Statistics*（ Leopold/Markl 相关统计直方图工作） | VLDB 2003 / 后续 | 直方图与基数值统计的经典研究 |
| MySQL 官方文档：Optimizer Trace / Optimizer Cost Model / Histograms | dev.mysql.com | trace 全部字段与成本常量的权威定义 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：**基数估计（cardinality estimation）**重新成为热点——传统直方图/采样在 2020 年后被「学习型估计」（用深度/线性模型预测选择率）挑战，多个 VLDB/SIGMOD 工作提出替代方案；** Learned Index **（Learned B-Tree，SIGMOD 2018） similarly 用模型替代索引结构；**可解释优化器**：`optimizer_trace` 这类「让优化器决策可见」的思路，在学术上演进为对「估算误差归因」的形式化研究。
- **工业界开源**（star 数 2026-09-25 通过 `gh api` 实测）：
  - `mysql/mysql-server`（≈12.4k★）：trace 实现 `sql/sql_optimizer.cc` 的 `TRACE_OPTIMIZER` 段；优化器 `sql/join_optimizer/`；直方图 `sql/sql_update.cc` 与 `Opt_hists`。
  - `facebook/mysql-8.0`（≈115★）：Facebook 在成本模型与统计采样上的长期工程调整，是「成本模型被业务环境重写」的真实样本。
  - `pingcap/tidb`（≈40.6k★）：优化器完全基于统计 + 直方图，并且**每张表可按分区维护统计**，比 MySQL 的单表统计更细。
  - `cockroachdb/cockroach`（≈32.5k★）、`postgres/postgres`（≈22.2k★）：**`EXPLAIN (ANALYZE, BUFFERS)`** 可以给出实际行数、实际缓冲池命中和逐算子耗时，与 MySQL 8.0 的 `EXPLAIN ANALYZE` 是同一思路的成熟形态。
  - `duckdb/duckdb`（≈41.7k★）、`clickhouse/clickhouse`（≈50.1k★）：**profiling 内建在优化器里**（`EXPLAIN ANALYZE SELECT ...` 默认可用），可作为「MySQL 该往哪走」的路线图。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`EXPLAIN` 出来的就是最终计划」 | `EXPLAIN` 只给**估算**；8.0 要看到真实行数用 `EXPLAIN ANALYZE` |
| 2 | 「trace 里没看到某个索引就是没考虑」 | 有时是**改写阶段就把它排除了**（如物化路径），要看 `steps`/`transformation` |
| 3 | 「trace 被截断了是 bug」 | 通常 `optimizer_trace_max_mem_size` 太小，调大即可 |
| 4 | 「统计信息是准的，所以计划不该错」 | 采样只有 20 页；倾斜列必然估错，需要直方图 |
| 5 | 「改 `engine_cost` 就能让优化器选我想要的索引」 | 调成本是全局副作用，会拖累其他 SQL，优先级远低于改索引/统计 |
| 6 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有**直方图（8.0）、**没有** `EXPLAIN ANALYZE`（8.0.18）；`rows_estimated` 与 `rows_actual` 的对比方法，正是 2026 年排查「优化器选错」的第一步 |
| 7 | 🔧 **本书未覆盖** | **8.0 的 CTE 默认不合并 / 派生表物化策略**会让复杂 SQL 的 trace 结构与 5.7 完全不同；`n_jobs`（8.0.22）并行也让「成本 vs 时间」不再线性可比 |

## 与其他章 / 其他书的联系

- → `14-单表查询.md`：本章「候选路线」就是 14.1 那张 `type` 表。
- → `15-连接查询.md`：连接顺序与连接算子的选择，`reconsidering_access_paths` 的主场。
- → `17-调节磁盘和CPU的矛盾.md`：预读与 Buffer Pool 命中率直接影响 I/O 成本项。
- → `19-redo日志.md`、`20-undo日志.md`：DML 的改动量与 purge 会影响统计的实时性。
- → `X1-时间追踪专题.md`：时间列的范围条件选择性也进入成本估算。
- → [13-查询优化.md](../数据库系统概念6/13-查询优化.md)（若存在）：查询优化器视角的标准表述。
- → [11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)：选择性、基数与索引结构的教科书口径。
