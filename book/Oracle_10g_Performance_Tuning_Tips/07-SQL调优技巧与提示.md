# 07 SQL调优技巧与提示 — Oracle Database 10g Performance Tuning Tips & Techniques（精读重构）

> ⚠️ 主题重组口径（章号非原书章号，降级声明见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §3）。本章=语句级技巧库：改写谱、hint 家族、分页/集合惯用法与 10g 自动调优三件新器。
> Oracle 行为 ⚠️ 转述；官方锚点 ✅：B14211 Ch11《SQL Tuning Overview》/Ch12《Automatic SQL Tuning》/Ch16《Optimizer Hints》/Ch18《Plan Stability》（目录实抓在册）。

## 1. 改写的总纲：把意图说得更可优化（⚠️ 通说）

- 三问前置 ⚠️（本目录全书纪律）：优化器**缺什么料**（统计）？被什么**形状骗**（复杂视图/嵌套）？**能不能不这么问**（需求改写）？
- 惯用改写谱（10g 时代正典，✅ 中文纵深对读 [../Oracle查询优化改写技巧与案例.md](../Oracle查询优化改写技巧与案例.md)——盘上辨析注：师庆栋系中文原创非译书，见 TOP 00 同款结论）：
  - `IN (子查询)` ⇄ `EXISTS` ⇄ 半连接：10g CBO 已自动做 unnest/subquery 变换（✅ B14211 Ch13 查询变换域；成本解剖 [../Cost_Based_Oracle_Fundamentals/09-查询变换.md](../Cost_Based_Oracle_Fundamentals/09-查询变换.md)）——**先证明变换没发生再手工**。
  - `OR` 两侧索引异族 → `OR-Expansion` 失效场合手工 `UNION ALL` 拆分 ⚠️。
  - 谓词可索引化：函数包裹列（`TRUNC(dt)=...`）→ 范围改写（`dt >= ... AND dt < ...`）或函数基索引（`06`）。
  - 隐式转换杀手：VARCHAR 列配数字字面量→全表（`TO_NUMBER` 反方向则安全）⚠️——贴士册高频条目。

## 2. 分页、排序与"取前 N"的 10g 惯用法（⚠️）

- ROWNUM 三明治（内层排序→中层 ROWNUM 上限→外层去下限）：本册时代标准配方；12c `FETCH FIRST/OFFSET` 之后退役（演进节记）。
- `ORDER BY` 供序消灭排序（🔧 类比 D4 已在 `03` 章实证计划级消失，✅ 非 Oracle 行为）；复合索引尾列接排序列是设计期技巧（`06` 章列序律）。
- `GROUP BY` 两路：`SORT GROUP BY`（排序后折叠）vs `HASH GROUP BY`（哈希表驻留）——内存不足前者可溢出、后者易膨胀 ⚠️；`GROUP BY` 位置索引供序可省排序+早停 ⚠️。
- 集合运算：`UNION` 隐含去重税（`SORT UNIQUE`）——确知无重叠改 `UNION ALL` 是本册最经典一档贴士 ⚠️。

## 3. Hint 家族图谱（⚠️ 通说；✅ B14211 Ch16 在册）

| 族 | 代表 | 用途边界 |
|---|---|---|
| 访问路径 | `INDEX/NO_INDEX/FULL/ROWID` | 纠"该走没走/不该走乱走" |
| 连接 | `LEADING/USE_NL/USE_HASH/USE_MERGE` | 钉驱动序与算法（配 🔧 D5 谱系直觉） |
| 变换 | `MERGE/NO_MERGE/UNNEST/PUSH_PRED` | 视图与子查询形态控制 |
| 优化器模式 | `ALL_ROWS/FIRST_ROWS_n` | 语句级目标函数切换 |
| 并行 | `PARALLEL/DISABLE_PARALLEL` | 批处理窗口武器 |
| 杂项 | `/*+ MONITOR */(11g 后)` `OPT_ESTIMATE` | 后期代际，本册未及 |
- 纪律 ⚠️：hint=**单语句、全注释、可回收**；批量 hint 注入=把技术债写成方言。hint 拼错会被静默忽略（`V$SQL_OPTIMIZER_ENV`/`DBMS_XPLAN` 的 Note 段验效）✅ 文档在册。
- `OPT_ESTIMATE`（11g）之前，本册时代纠偏靠 Outlines/手工 hint——两代边界见演进节。

## 4. 10g 自动调优三件器（✅ 目录在册；机理 ⚠️ 转述）

1. **SQL Tuning Advisor**：输入 SQL Tuning Set/手工清单，产出四路建议（统计/结构/profile/并行）；`DBMS_SQLTUNE` 家族 ⚠️。
2. **SQL Profile**：纠偏系数包（不改语句文本），`ADJUST_PLANS` 类工件；相比 hint 的可移植性更高但仍是"补丁"⚠️。
3. **SQL Tuning Sets/Plan Stability**：把"计划锁住"从 9i Stored Outlines（本册仍当正解 ⚠️）过渡到 10g 的 SQL Profile/11g SPM——**本册恰站在 Outline→SPM 的断代线上**。
- 许可提示 ⚠️：Tuning Pack 是独立许可件（与 Diagnostics Pack 分家）——贴士册语境默认企业全件，实际部署先查合同。

## 5. 绑定变量的语句级战术（⚠️ 承接 `05` 解析经济学）

- 该绑：OLTP 高频语句（解析税主导）；该 literal：DSS 月变语句+强倾斜列（直方图价值主导）——"全绑 or 全不绑"都是教条。
- peeking 悖论的操作层绕法（本册时代 ⚠️）：倾斜列去直方图/用字面量/绑定值范围收敛；11g ACS 出现前这些都是脏活。
- `cursor_sharing=SIMILAR` 的隐藏雷：绑与非绑双份游标 ⚠️；`FORCE` 后接 bind-aware 演进——2026 口径一律"应用侧显式绑定为纲"。

## 6. 案例骨架：一条报表 SQL 的调优流水（⚠️ 通说情景）

1. autotrace 初诊：`consistent gets` 千万级+`SORT GROUP BY` 巨大排序 → 疑料歪。
2. 计划复核 `V$SQL_PLAN`：Est Rows 与实际差 200 倍（`05` 铁律）→ 重采统计+加 TOP-N 直方图 → 计划翻成哈希路径。
3. 仍慢：`LEADING` 验证驱动序假设 → 实为连接顺序错 → 永久解是改写连接谓词形状而非留 hint。
4. 收尾：删 hint、锁统计、把该 SQL 放进 STS 做升级回归（11g 后叫 SPA 的前身仪式 ⚠️）。
- 全程与 TOP 2e 的"可复现问题"章法共法 ✅（[../Troubleshooting_Oracle_Performance_2e/11-SQL优化技术.md](../Troubleshooting_Oracle_Performance_2e/11-SQL优化技术.md)）；学院派"改写即语义等价证明" ⚠️ 对读 ✅ [../Database_Tuning/00-总览与阅读地图.md](../Database_Tuning/00-总览与阅读地图.md)。

## 7. 贴士清单抽样（⚠️ 体裁还原，均已标注代际风险）

- `UNION ALL` 替 `UNION`（无重叠时）｜`EXISTS` 内层加索引列短路｜避免 `SELECT *`（覆盖索引机会+解析字典税）｜`ROWNUM` 早停利用索引供序｜`WITH` 物化重复子查询（12c 前 INLINE 不可靠）｜`MERGE` 整合批量 upsert（9i 引入，本册时代新宠）｜`BULK COLLECT` 归 `09`｜`NOCACHE/ORDER` 序列与主键热点归 `06/08`。
- 反例警示 ⚠️：`/*+ RULE */` 残留（RBO 已死仍被抄）、`HINT` 包全表（`FULL(t) USE_HASH` 一把梭）——2026 代码考古时这两类最常见，正是本册流传期的滥用证词。

## 8. Hint 不生效的排查序（⚠️ 通说；贴士滥用自救指南）

1. **拼写与位置**：hint 必须在 `/*+` 紧跟首个关键字后；注释内多空格/换行可致静默失效 ✅（B14211 Ch16 词法域）。
2. **验效通道**：`DBMS_XPLAN` 输出的 Note 段/Outline Data 反推——hint 被吸收会在此留痕 ⚠️；未留痕=没吃到或被变换改写。
3. **语句变形**：视图合并/子查询展开后目标行源已非你指名的形状——先 `NO_MERGE/UNNEST` 定形再谈访问路 ⚠️。
4. **绑定窥视干扰**：hint 在但计划仍漂=多子游标问题（`05` peeking），检查 `V$SQL` CHILD 计数 ⚠️。
5. **统计饥饿**：CBO 把 hint 路径成本算到不可接受会部分放弃（hint 非强制令）⚠️——补料永远先于加 hint。
6. **版本方言**：跨库搬运的 hint 含已删/改名项（`USE_CONCAT` 族幸存者少 ⚠️）；升级回归时用 SPA/SQL Test 批量验效（11g 化产品，`07` 演进节）。
- 心法 ⚠️：**hint 是语句的"临时脚手架"**——长期存在的 hint=未还的技术债，登记进重构 backlog 才是正道。

## 9. 计划稳定性工程：Outline→Profile→SPM 断代志（⚠️ 重组）

- 9i **Stored Outlines**：按语句指纹锁一版计划全家桶；痛点=抓取窗口仪式、版本脆断、容量规划——本册时代仍是"正统"，贴士以"核心 SQL 先 Outline"为主调 ⚠️。
- 10g **SQL Profile**：Advisor 产纠偏系数包，保留语句可演进性；比 Outline 温和但仍是"外挂"；与 `04` 章自动调优任务合流为夜间 SQL 调优窗 ⚠️。
- 11g+ **SPM**：演进中的 Baseline 采纳制（验证→晋级→回滚），计划漂移的制度化答案——**本册恰停在 Outline 遗照与 SPM 出生证之间的书页上**（史料位置，`05` 章铁律的治理面）。
- 工程常量（跨三代 ⚠️→✅）：核心 SQL 清单、变更冻结窗、计划回归的自动化检测——今天叫 query fingerprinting/plan pinning，换了方言没换问题。
- 与盘上现代治理对照 ✅：[../Troubleshooting_Oracle_Performance_2e/09-配置查询优化器.md](../Troubleshooting_Oracle_Performance_2e/09-配置查询优化器.md)（2014 视角的优化器参数治理）与 [../Oracle_Database_Problem_Solving/02-GC缓冲区忙等待、自适应游标共享与SPM.md](../Oracle_Database_Problem_Solving/02-GC缓冲区忙等待、自适应游标共享与SPM.md)（ACS/SPM 案例标本）。

### 附记：改写案头小抄（⚠️ 通说速查，全部先证变换未发生）

- 谓词形状：`LIKE 'abc%'` 可索引 / `LIKE '%abc'` 不可（函数基/全文另案）；`!=/NOT IN` 常诱全扫；`IS NULL` 复合索引可救 ⚠️。
- 连接形状：`IN`↔`EXISTS` 经验律（小结果集 EXISTS、大驱动集 IN——口诀而已，10g CBO 多已自动 ⚠️）；笛卡尔积报警=连接谓词漏写检查 ⚠️。
- 聚合形状：`GROUP BY` 先滤后聚（谓词下推位）、`HAVING` 能变 `WHERE` 全变 ⚠️；`DISTINCT` 是排序去重税的别名 ⚠️。
- 分页形状：ROWNUM 三明治务必内层先排序（否则语义错+性能双杀）⚠️；深翻真是业务问题（→ 盘上 TOP 数据访问章 ✅ [../Troubleshooting_Oracle_Performance_2e/13-优化数据访问.md](../Troubleshooting_Oracle_Performance_2e/13-优化数据访问.md)）。
- 集合形状：`UNION ALL` 默认派（确认无重叠或不在乎去重）；`INTERSECT/MINUS` 半连接改写更可控 ⚠️。
- 使用法：本抄每条都只是"候选假设"——第 8 节排查序与第 6 节流水才是裁决程序 ⚠️。
- 与中文改写正典连读 ✅：[../Oracle查询优化改写技巧与案例.md](../Oracle查询优化改写技巧与案例.md)、[../SQL优化核心思想.md](../SQL优化核心思想.md)——三者构成"10g 现场→中文系统→现代手册"的改写谱。

### 附记二：语句调优的三种"不改"（⚠️ 防过度工程）

- 不改已最优：计划健康+等待谱正常+服务时间匹配业务量级——留档即可，动它是制造回归 ⚠️。
- 不改语义可疑：改写前先与业务确认口径（`DISTINCT` 掉不掉、`NULL` 算不算），性能方案不能顺手改答案 ⚠️。
- 不改他人语句：跨团队 SQL 的 hint/改写需代码属主签字——本册时代叫"DBA 别越界"，今天叫变更管理 ⚠️。
- 三条"不改"与 §8 排查序互为表里：先确认"该改、能改、归我改"，再进入第 6 节流水 ⚠️。
- 诚实边界：本附记是目录级重组断言（⚠️），非原书文字；三条纪律在 TOP 2e 章法中有同款现代表述 ✅（[../Troubleshooting_Oracle_Performance_2e/14-优化连接.md](../Troubleshooting_Oracle_Performance_2e/14-优化连接.md) 等章）。
### 附记三：语句调优复盘三问（⚠️ 收口）

- 一问语义：改写前后结果集等价吗（边界 NULL/去重/排序稳定性）⚠️——不等价的"提速"是缺陷提前上线。
- 二问依赖：新计划绑定的前提（统计形态/数据分布/绑定值域）写进注释了吗——hint 与改写都吃前提，前提变化=计划变化 ⚠️。
- 三问出口：上线后用什么账验证（AWR 同窗对比/`V$SQL` 计划快照），回滚开关在哪 ⚠️（`01` 章闭环纪律的语句级投影）。
- 三问通过，本章技巧才算"调优"；缺一即"碰运气" ⚠️ 重组断言。
- 全章终句：10g 给了 DBA 第一套自动调优工具，也留下了"自动工件要人审"的永恒副歌——SPM/自动索引时代这句更响 ⚠️→✅。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 提示 | Optimizer hint | 语句内向优化器下的指令 |
| 查询变换 | Query transformation | 优化器对语句的等价重写 |
| 子查询展开 | Unnesting | 嵌套子查询变连接 |
| 或扩张 | OR-expansion | OR 拆并各自走索引 |
| 行号分页 | ROWNUM pagination | 10g 时代标准翻页三明治 |
| SQL 调优集 | SQL Tuning Set (STS) | 语句+执行上下文仓库 |
| SQL 概要 | SQL Profile | 语句外的纠偏系数集 |
| 计划稳定性 | Plan stability（Outlines→SPM） | 锁计划谱系的中间代 |
| 自适应调优 | Automatic SQL Tuning | 10g 的自动窗口任务 |
| 绑定/字面 | Bind vs literal | 复用与可估形的取舍 |

## 最新演进与工业实践

- **代际更替 ✅**：11g **SQL Plan Management（Baseline/Evolution）** 全面替代 Stored Outlines（10g 的 Outline 贴士即化石），11g ACS 接管 peeking 脏活；**SQL Performance Analyzer（SPA）/Database Replay** 把"升级回归"仪式产品化（10.2 目录已收录 ✅ B14211 Ch21/22，工业普及在 11g+）；12c `FETCH FIRST/OFFSET` 终结 ROWNUM 三明治；12c 结果缓存与 SQL Pattern Analytics；19c `APPROX_COUNT` 族、自动优化任务接管 Profile 生成——口径见 19c/23ai PTG（✅ 门户实抓 00 §12.7）。
- **hint 的当代地位 ⚠️**：仍是纠偏最后手段且文档明令"先统计后 hint"；`OPT_ESTIMATE`/`LEADING` 家族现役，`MONITOR` 配合 SQL Monitor 成标准取证动作。
- **改写技巧的长寿面**：`UNION ALL` 去重税、谓词可索引化、隐式转换防治——三件套在 MySQL/PostgreSQL/SQL Server 文档里逐条有对应说法（对读 ✅ [../SQL优化核心思想.md](../SQL优化核心思想.md)、[../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md)）；本章体裁是"跨引擎 SQL 性能素养"的早期汇编。
- **2026 姿势**：学"语句级调优系统方法"请直接读 TOP 2e `09–15` 章（✅ 在盘 16 章实证）；本册章价值=10g 断代线上（Outline→SPM、手工→Advisor 交接期）的工业现场记录，凡"照抄当年配方"处务必先查对应新文档。
