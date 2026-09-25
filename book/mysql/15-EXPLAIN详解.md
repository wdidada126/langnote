# 第 15 章 EXPLAIN 详解

> 原书说明：标题为「EXPLAIN详解」，基于 MySQL 5.7.22 撰写。本文件按列逐个拆解
> **`id` / `select_type` / `table` / `type` / `possible_keys` / `key` / `key_len` / `ref` / `rows` / `filtered` / `Extra` / `partitions`**，
> 并补齐 5.7 与 8.0 两代输出的差异、`FORMAT=TREE/JSON` 与 🔧 `EXPLAIN ANALYZE`。
>
> ⚠️ 本目录**不提供可运行的环境**：所有 SQL 与结构示例都是**教学示意，不参与构建**，未在本机编译、未连接任何 MySQL 实例执行。

## 本章地图

> 一句话：**`EXPLAIN` 是「计划单」——它把优化器的选择以列的形式摊开。
> 读它的顺序不是从左往右，而是「**先看 `type` 判贵贱，再看 `key`/`key_len` 判用没用上，再看 `rows` 判估算准不准，最后看 `Extra` 判细节代价**」；
> 而 `EXPLAIN ANALYZE` 把这张单子从「报价」换成「发票」。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 15.1 它会执行你的语句吗 | 普通 `EXPLAIN` 不执行；`EXPLAIN ANALYZE` **一定执行** | 在线上库对 DML 用 `ANALYZE` 前请想清楚副作用 |
| 15.2 列全景 | 12 个常用列各回答什么问题 | 每列都是优化器某个决策的直接呈现 |
| 15.3 `id` 与 `select_type` | 查询形状（简单/主查询/子查询/派生/UNION） | 先看结构，再看单行的贵贱 |
| 15.4 `type`：从 `system` 到 `ALL` 的价格梯度 | 七种访问方法与 `index_merge` 的位置 | `type` 是「扫描粒度」的粗度量，不是唯一判据 |
| 15.5 `possible_keys` / `key` / `key_len` / `ref` | 候选索引、实际索引、索引用了多少前缀、关联列 | `key_len` 越短越省，但它不等于「索引一定用得完整」 |
| 15.6 `rows` 与 `filtered` | 估算行数与筛除比例（都为估算） | 与实测差一个数量级 ⇒ 先修统计（见 `13-统计数据.md`） |
| 15.7 `Extra` 词典 | `Using index`、`Using index condition`、`Using temporary`、`filesort`、`join buffer` 等 | 细节代价全在这一列，缺 `Using index` 就是回表信号 |
| 15.8 `partitions` 与分区表 | 命中的分区 | 分区裁剪是否有效看这一列 |
| 15.9 三种输出格式 | `CLASSIC` / 🔧 `TREE` / `JSON`（含 `cost_info`） | 树状输出更适合人眼，JSON 更适合脚本 |
| 15.10 🔧 `EXPLAIN ANALYZE` | `actual time`、`rows`、`loops` | 估算与实测的唯一直接对照口径 |
| 15.11 一个八步读法 | 从「哪一行最该优化」到落地动作 | 读计划是技能，也是有固定动作的流程 |
| 15.12 🔧 2026 视角 | 8.0 起 `ANALYZE`、成本信息、`FORMAT=JSON` 的扩展列 | 5.7 的列集合在今天只是**子集** |

## 核心精讲

> **教学示意，不参与构建。** 下文所有片段与结构示意**未在本机编译、未连接任何 MySQL 实例执行**；
> 列名与取值随版本变化，请以官方文档的当版 `EXPLAIN` 条目为准。

### 15.1 只有 ANALYZE 会执行

| 用法 | 是否执行语句 | 备注 |
| --- | --- | --- |
| `EXPLAIN SELECT ...` | 不执行 | 安全，可在线上使用 |
| `EXPLAIN UPDATE/DELETE` | 不执行（但建议先在测试环境） | 部分版本对 DML 有额外约束，以官方条目为准 |
| `EXPLAIN ANALYZE SELECT ...` | **会执行** | 会真实跑一遍，读写、触发器、自增都会被触发 |
| `EXPLAIN FOR CONNECTION n` | 读连接正在跑的计划 | 排查偶发慢查询的现场工具 |

工程提醒：**线上库上想看真实耗时，优先用慢日志 + `performance_schema`，而不是 `EXPLAIN ANALYZE` 顺手跑一条 UPDATE。**

### 15.2 列全景：每列回答一个问题

| 列 | 在回答什么 |
| --- | --- |
| `id` | 这个 SELECT 属于查询的哪一层（数字大的先执行） |
| `select_type` | 这个 SELECT 的角色（简单查询 / 子查询 / `UNION` / 派生等） |
| `table` | 这一行描述的是哪张表，或 `<derivedN>` / `<subqueryN>` 这类内部产物 |
| `partitions` | 命中哪些分区 |
| `type` | 访问方法的粗分类（贵贱） |
| `possible_keys` | **候选**索引（不一定被选中） |
| `key` | **实际**选中的索引 |
| `key_len` | 用了索引的多少前缀（字节数） |
| `ref` | 与索引比较的是什么（常量、列、函数） |
| `rows` | **估算**要扫多少行 |
| `filtered` | 剩余行数的百分比（估算） |
| `Extra` | 附加信息：回表、临时表、排序、下推等 |

### 15.3 `id` 与 `select_type`：先看形状

| `select_type` | 出现场景 | 读的时候要注意 |
| --- | --- | --- |
| `SIMPLE` | 不含 `UNION` / 子查询的查询 | 最常见；若你写了子查询却看到 `SIMPLE`，说明已被规则改写掉（见 `14-基于规则的优化.md`） |
| `PRIMARY` / `SUBQUERY` / `DEPENDENT SUBQUERY` | `UNION` 主句 / 非相关子查询 / 相关子查询 | **`DEPENDENT` 常常是坏味道**：它会对外层每行重复执行一次 |
| `DERIVED` | 派生表（若未被合并） | 配合 `Extra` 里的 `Materialize` 看 |
| `MATERIALIZED` | 被物化的子查询/CTE | 说明走了一次临时表 |
| `UNION` / `UNION RESULT` | `UNION` 的第二段与去重段 | `UNION` 默认去重 ⇒ 会有一次去重代价；要保留重复请用 `UNION ALL` |

- `id` 相同的一批行属于同一个 SELECT；`id` 越大越先执行；上下相邻的行之间是「驱动 / 被驱动」关系。

### 15.4 `type`：从 `system` 到 `ALL` 的价格梯度

| `type` | 含义 | 典型场景 |
| --- | --- | --- |
| `system` | 表最多一行（系统表） | 近乎常数 |
| `const` | 主键/唯一键等值，最多一行 | 主键点查 |
| `eq_ref` | **连接**时被驱动表用唯一索引等值匹配 | 连接列有主键/唯一索引时的最优形态 |
| `ref` | 非唯一索引等值匹配 | 常见且可接受，行数随重复值放大 |
| `ref_or_null` | 等值或 `IS NULL` | 允许 NULL 的等值查询 |
| `range` | 区间扫描（`>`、`BETWEEN`、`LIKE 'x%'`、`IN`） | 有索引但非点查 |
| `index_merge` | 多个索引的结果求交/并 | 多条件 OR/AND 时的补救手段 |
| `index` | 全索引扫描（常伴随覆盖索引） | 比 `ALL` 窄一些，但仍是 O(索引行数) |
| `ALL` | 全表扫描 | 优化的第一目标 |

读法要点：

- 顺序不是「取的准绳」，**总价才是**。一个 `range`（回表多）可能输给 `index`（覆盖、不回表）。
- 连接场景里 **`eq_ref` → `ref` 的退化**要特别关注：它意味着被驱动表的连接列上没有唯一索引，**每一行都要多扫一小段**，
  并且是锁/latch 争用的放大器（见 `22-锁.md`）。
- `index_merge` 出现时先别高兴：它往往是「索引设计不佳 + 谓词写得太散」的信号，多数情况靠改写谓词/补联合索引更划算。

### 15.5 索引三列：`possible_keys` / `key` / `key_len` / `ref`

| 列 | 常见误读 | 正确理解 |
| --- | --- | --- |
| `possible_keys` | 「这些都能走」= 会走 | 只是**候选**；它为空通常说明**确实没有可用索引** |
| `key` | 空 = 没优化 | 空时先回到 `where`/统计/隐式转换，而不是立刻 `FORCE INDEX` |
| `key_len` | 越短越好 | 它反映**用了几个列的多少前缀**；过长说明索引可能被浪费，过短说明可能没用上联合索引的全部列 |
| `ref` | 只有常量 | 它也可以是列（连接条件）或 `func` |

- 隐式类型转换的高频现场：`type=ALL` + `key=NULL` + `possible_keys` 有值 + 列是 `varchar` 而常量是数字。
  这不是优化器坏了，是**转换让索引不可用**。

### 15.6 `rows` 与 `filtered`：估算，但不是事实

- `rows` 是优化器**估算**要处理的行数（来自统计信息，见 `13-统计数据.md`），
  `filtered` 是「按 `WHERE` 条件过滤后预计剩余的比例」。
- 两者相乘大致是「预计返回行数」的口径，可用于快速定位「哪一行扫得最凶」。
- **真实对照只能靠 `EXPLAIN ANALYZE` 的实测行数**（🔧 8.0.18 起）。
- 经验阈值：`rows` 与实测差一个数量级 ⇒ 统计信息或选择性估算出了问题，先修统计再谈调参。

### 15.7 `Extra` 词典（按重要性排序）

| `Extra` 值 | 含义 | 行动建议 |
| --- | --- | --- |
| `Using index` | **覆盖索引**，无需回表 | 好现象；想更稳可考虑扩索引列 |
| `Using index condition` | **索引条件下推（ICP）**，部分过滤在引擎层做 | 正常且高效 |
| `Using where` | 行取出后由 Server 层再过滤 | 若没配 `Using index`，说明回表后才发现不匹配 |
| `Using join buffer (Block Nested Loop)` | 无索引可用的连接，靠内存缓冲配对 | 补索引或改小表驱动 |
| `Using temporary` | 需要临时表（`GROUP BY` / `DISTINCT` 等） | 尽量让 `GROUP BY` 走索引 |
| `Using filesort` | 需要额外排序 | 让 `ORDER BY` 命中索引顺序，或接受代价 |
| `Select tables optimized away` | 优化器直接得出结果（如 `MIN`/`MAX` 走索引） | 无需处理，是优化器的小胜利 |
| `Impossible WHERE` | 条件永假，无需取数 | 说明 SQL 可能有逻辑错误 |
| `Using index for group-by` | `GROUP BY` 直接走索引 | 好现象 |
| `Range checked for each record` | 每次取行都要试区间，优化器不敢用 | 通常在复杂连接里出现，需拆查询 |

- 一条速记：**看不到 `Using index` 时，先问「回表了吗」；看到 `temporary` + `filesort` 时，先问「排序能不能走索引」。**

### 15.8 `partitions`：分区裁剪的证据

- `partitions` 列列出这一行实际会访问的分区（🔧 该列自 5.7 起可用，语法与行为以官方条目为准）。
- 出现「建了分区却全表扫」时，第一看这个列**是否发生了分区裁剪**：没裁剪说明 `WHERE` 里没有分区键条件，
  或转换让分区键失效（函数、隐式转换）。
- 分区表的适用面很窄（管理便利 > 性能），不要为了「快」而分区（见 `09-表级别的操作.md`）。

### 15.9 输出格式：看人 vs 看机器

| 格式 | 特点 | 用途 |
| --- | --- | --- |
| 默认（CLASSIC） | 一行一个表的表格 | 日常速读 |
| 🔧 `FORMAT=TREE` | 缩进树 + 代价信息，层级关系最直观 | **推荐**给人读 |
| `FORMAT=JSON` | 结构化输出，含 `query_block` 与 `cost_info` | 脚本对比计划、做回归基线 |
| 🔧 `FORMAT=JSON` 的 `cost_info` | 展示各候选路径的估算代价 | 把「为什么选它」落到数字上 |

```text
EXPLAIN FORMAT=TREE SELECT ...;      -- 示意，未执行
```

### 15.10 🔧 `EXPLAIN ANALYZE`：从报价到发票

```text
EXPLAIN ANALYZE SELECT ...;          -- 示意，会真实执行，未执行
```

输出里最该盯的字段（示意，字段名随版本可能微调）：

| 字段 | 告诉你什么 |
| --- | --- |
| `actual time: X..Y` | 该节点首次返回一行与全部返回完的**实测**耗时 |
| `actual rows` | **实测**行数（与 `rows` 估算对照） |
| `loops` | 该节点被进入多少次（连接里等于驱动行数） |

- 典型用法：先看**最外层最贵的那一行**，再看它的子节点的 `actual rows` 与估算 `rows` 的差距。
- 注意它**会真的执行**：只读查询可以，写操作与触发器的副作用必须先在测试环境验证。
- 它与 `optimizer_trace` 的分工：`ANALYZE` 给「实际发生了什么」，`trace` 给「优化器当时以为是什么」。

### 15.11 八步读法：把计划变成动作

| 步 | 动作 | 判据 |
| --- | --- | --- |
| 1 | 看 `type`，找 `ALL` / 退化的 `ref` | 定位最贵的一行 |
| 2 | 看 `key` / `key_len`，确认索引是否真的用上 | 未用上先查隐式转换与统计 |
| 3 | 看 `rows` 与 `filtered`，确认估算是否可信 | 差一个数量级 ⇒ 修统计或建直方图 |
| 4 | 看 `Extra`，确认回表 / 临时表 / 排序 | `Using index` 缺失即回表；`temporary`+`filesort` 即额外代价 |
| 5 | 看 `id` / `select_type`，确认子查询是否被改写 | `DEPENDENT SUBQUERY` 大概率要改写 |
| 6 | 若计划怪异，开 `optimizer_trace` 看改写与候选成本 | 改写没发生 ⇒ 规则层；改写有 ⇒ 成本层 |
| 7 | 落地动作：改统计 / 补索引 / 改写法 / 用提示（按序尝试） | 提示是最后手段 |
| 8 | 固化：把计划与耗时写进回归基线 | 下大版本前必做 |

### 15.12 🔧 2026 视角：8.0 之后多了什么

| 新增/变化 | 版本 | 对本章的影响 |
| --- | --- | --- |
| `EXPLAIN` 的成本细节（JSON 输出） | 🔧 8.0 系 | 计划单上直接给出估算代价 |
| `FORMAT=TREE` | 🔧 8.0 | 层级化输出，人读首选 |
| `EXPLAIN ANALYZE` | 🔧 8.0.18 | 估算 vs 实测的对照口径 |
| `EXPLAIN FOR CONNECTION` | 🔧 8.0 | 排查在跑的慢查询 |
| `partitions` 等列 | 5.7 起 | 分区裁剪是否发生一眼可见 |
| 🔧 8.4 LTS / 9.x | 待核对官方条目 | 列名与默认值可能继续变化，**升级前务必重读当版文档** |

## 版本演进

| 版本 | `EXPLAIN` 相关的变化 |
| --- | --- |
| 5.7（原书基线） | `partitions`、`filtered` 列可用；`FORMAT=JSON` 可用 |
| 8.0 | 🔧 `FORMAT=TREE`；🔧 `EXPLAIN ANALYZE`；🔧 `EXPLAIN FOR CONNECTION`；JSON 输出的 `cost_info` |
| 🔧 8.4 LTS | 输出与默认值继续微调（以官方 Changed/Removed 条目为准） |
| 🔧 9.x | 计划输出与优化器内部结构同步演进（须以当版文档为准） |

## 经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Selinger 等，*Access Path Selection in a Relational Database Management System* | *SIGMOD* 1979 | `EXPLAIN` 所展示的「访问方法」分类的原始定义 |
| Graefe，*Volcano: An Extensible and Parallel Query Evaluation System* | IEEE Data Engineering Bulletin 11(4), 1990 | 计划树的枚举与执行模型，树状输出的来历 |
| Poosala & Ioannidis，*Estimation of Selection Cardinality: A Comparison of Five Histograms* | *ICDE* 1995 | 解释 `rows` 为什么是估算、误差从哪来 |
| Neumann，*Efficiently Making (Almost) Any Query Optimization Fast* | CIDR 2011 | 「估算 vs 实测」对照对优化器设计的意义 |
| MySQL 官方文档：EXPLAIN / EXPLAIN ANALYZE / Optimizer Trace | dev.mysql.com | 列名、`Extra` 取值与输出格式的权威口径 |

## 近年研究与工业界开源实践（2015–2026）

- **研究/工程主线**：**算子级可观测**——`EXPLAIN ANALYZE` 的思路被普遍化到数据库可观测工具里
  （per-node 的 `rows/time/loops`），并与分布式执行（每个节点自己的 plan）结合，
  成为「查询诊断」的通用口径。
- **工业界做法**：把「计划指纹 + 耗时」作为**发布前回归项**，在大版本升级、索引变更后自动对比。
- **工业界开源**（star 数 2026-09-25 通过 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测）：
  - `percona/percona-toolkit`（**≈1.55k★**）：`pt-query-digest` / `pt-index-usage` / `pt-explain`，
    把 `EXPLAIN` 从「一次看一行」变成「批量找问题」。
  - `mysql/mysql-server`（**≈12.4k★**）：计划输出与 `EXPLAIN ANALYZE` 的实现现场。
  - `mysql/mysql-router`（**≈148★**）：连接层中间件，可作为「不改实例也能改计划」的对照。
  - `github/gh-ost`（**≈13.6k★**）：在线改表会重写表结构与索引，改完必须重看计划（与 `09-表级别的操作.md` 呼应）。
  - `vitessio/vitess`（**≈21.4k★**）：`VExplain` 与查询诊断能力，是「分布式环境下怎么看计划」的样本。
  - `postgres/postgres`（**≈22.2k★**）：`EXPLAIN (ANALYZE, BUFFERS)` 的成熟形态，是 8.0 之前的最佳对照。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`EXPLAIN` 会执行这条语句」 | 普通 `EXPLAIN` 不执行；**只有 `EXPLAIN ANALYZE` 会** |
| 2 | 「`possible_keys` 有值就一定会走这个索引」 | 那只是**候选**；实际是否走看 `key` |
| 3 | 「`rows` 是表的行数」 | 那是**估算**；与实测差得远说明统计该刷新了 |
| 4 | 「`type=range` 一定比 `type=ALL` 好」 | 总价才是判据；回表多的 `range` 可能输给覆盖索引的 `index` |
| 5 | 「看到 `index_merge` 就是优化赢了」 | 它常是索引设计不佳的补偿手段，优先改谓词或补联合索引 |
| 6 | 「`Extra=Using where` 说明索引没用了」 | ICP 场景下它是**引擎层下推过滤**的正常标记，要看是否伴随 `Using index` |
| 7 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有** `FORMAT=TREE`、`EXPLAIN ANALYZE`、`EXPLAIN FOR CONNECTION`，
  也没有 JSON 输出里的 `cost_info` 细节 |
| 8 | 🔧 **本书未覆盖** | 2026 年「计划指纹回归」「算子级可观测」已是把 `EXPLAIN` 变成工程工具的常态做法，原书没有涉及 |

## 与其他章 / 其他书的联系

- → `12-基于成本的优化.md`：`type` 与 `rows` 都来自那一章的估算结论。
- → `13-统计数据.md`：`rows` 不准时，先修统计而不是怀疑计划。
- → `14-基于规则的优化.md`：`select_type` 里的 `SIMPLE` / `DERIVED` / `MATERIALIZED` 是那一章改写结果的执行层痕迹。
- → `16-optimizer-trace.md`：`analyzer` 回答「为什么」，本章回答「是什么」。
- → `14-单表查询.md`（第 10 章）、`15-连接查询.md`（第 11 章）：七种访问方法与连接算法的原理。
- → `07-B树索引的使用.md`：回表与覆盖索引决定了 `Extra` 里有没有 `Using index`。
- → `22-锁.md`：走索引与不走索引，锁的范围差得很远，计划要先读对。
- → [13-查询优化.md](../数据库系统概念6/13-查询优化.md)：《数据库系统概念（第6版）》中查询计划的规范化讨论。
- → `00-总览与阅读地图.md`（[00-总览与阅读地图.md](00-总览与阅读地图.md)）｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
