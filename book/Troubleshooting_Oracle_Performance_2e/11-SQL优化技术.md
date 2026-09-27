# Ch11 SQL Optimization Techniques（SQL 优化技术）— 原书 p.359–418 · Part IV Optimization

> ⚠️ 文档转述。本章是 Part IV"武库总目录"：七种干预手段，每种固定三段（官方目录 ✅：How It Works / When to Use It / Pitfalls and Fallacies）。

## 本章定位

- 进入"动手改"的世界。作者的排序即立场：
  - 前四项改"语句与环境本身"（治本）：访问结构、语句、hint、执行环境；
  - 后三项"不改语句强锁计划"（治标但可治理）：Stored Outlines、SQL Profiles、SPM。
- 全章暗线：**干预越强，语句与计划之间的可追溯性越弱**——每种手段都要先问代价与失控半径。

## 11.1 Altering the Access Structures（改访问结构，p.360）

- How（360）：加/改索引、物化视图、分区——最直接的干预。
- When（361）：症状指向访问路径缺失且结构债可还时。
- Pitfalls（361）：**为一个语句加索引的边际成本是全库 DML 与维护窗口**；重叠索引、结构膨胀。以"访问路径家族"整体思考（Ch13/Ch14 展开）。

## 11.2 Altering the SQL Statement（改语句，p.361）

- How（361）：等价重写以消除"优化器看不懂的形状"（10.4 Restriction Not Recognized 的对症药）：拆 OR、NOT IN→NOT EXISTS、去包裹函数、WITH/MERGE 重排。
- When（363）：谓词形态问题导致计划结构性错误时。
- Pitfalls（363）：**改语句风险最高收益也最高——必须有结果等价性证明意识**（测试用例+行数/校验和对照）。
- 中文世界的这条线即 ../Oracle查询优化改写技巧与案例.md 全书主题（辨析见 00 §5：师庆栋/罗炳森原创，非本书译本）。

## 11.3 Hints（提示，p.363–372）

- How（363）：注释级指令作用于优化阶段；合法集随版本变（`V$SQL_HINT`）；**写法只从 Outline Data 抄**（Ch10 接口）。
- When（370）：临时验证假设（hint 是实验仪器不是交付物）、驱动改写到达不了的变换（LEADING/USE_NL/INDEX/FULL/OUTLINE 族）。
- Pitfalls（370）：**静默失效**（名字错/对象名错/不可满足时不报错只忽略）、随结构漂移整体失效、升级后 hint 组合变枷锁。
- 11g+ 的 `OPT_PARAM` hint：把 Ch9 的会话参数装进单语句的合法通道（干预半径收缩到语句级）。

## 11.4 Altering the Execution Environment（改执行环境，p.372）

- How（372）：会话/系统参数、统计注入、SQL 级环境（与 Ch9 路线图衔接）。
- When（375）：环境与负载特征系统性错配时。
- Pitfalls（375）：环境型修复把问题扩散给所有语句——回扣 Ch9 路线图第 5 步（台账）。

## 11.5 Stored Outlines（p.375–385）【1e 遗产，2e 定性"遗产技术"】

- How（375）：按 signature 匹配的强制计划+绑定约束包。
- When（385）：仅存留于 10g/11g 老站点；11g 起被 SQL Profile/SPM 取代。
- Pitfalls（385）：跨版本不可携、hint 文本硬匹配脆弱、权限模型怪异。**作者明确：新项目禁用**——本节价值转为"理解 SPM 为何这样设计"的历史课。

## 11.6 SQL Profiles（p.387–402）

- How（387）：SQL Tuning Advisor 的产物形态——**不是锁计划，而是注入成本校正系数**（让成本模型在该语句上对准现实）；存 `dba_sql_profiles`。
- When（401）：根因是统计/模型偏差而语句不该动时；STA 的 ACCEPT 路径或手工 `DBMS_SQLTUNE.IMPORT_SQL_PROFILE`（跨环境迁移）。
- Pitfalls（402）：profile 是补丁不是修复——统计改善后它会变成反向偏差源；force_matching 语义风险；与 ACS/baselines 的相互作用。**作者同时要求：用完 profile 必须回头补统计（Ch8）**。

## 11.7 SQL Plan Management（SPM，p.402–417）

- How（403）三支柱：
  - **捕获**：`optimizer_capture_sql_plan_baselines` / 手动 `LOAD_PLANS_FROM_*`；
  - **选择**：cost-based，但只在 baseline 内选，新计划先入历史；
  - **演化**：`DBMS_SPM.TUNE/ACCEPT_SQL_PLAN_BASELINE`——新计划凭真实执行统计胜出才转正（12.2+ 自动演化任务）。
- When（417）：升级防御（先捕获旧好计划）、第三方不可改语句、计划翻转止血。
- Pitfalls（417）：baseline 腐化（陈旧计划压制更优解）、跨环境导入的统计/结构一致性前提、**"SPM 保证稳定、不以性能为第一目标"的定位误解**。
- 全书闭环位：捕获（Ch10）→ 校准（Ch8）→ 锁定（11.7）→ 受控演化。

## 本章取证清单

- 七族技术名/页码/三段式：✅ 官方 Contents PDF 逐条。
- 各机制实现细节（profile 校正系数语义、SPM 演化判据）：⚠️ 文档转述。

## repo 对读

- ../Database_Tuning/04-调优关系系统.md：Shasha 的"重写+索引"双栏是 11.1/11.2 的数学化版本；其"避免 hint"立场与 11.3 Pitfalls 同调。
- ../高性能mysql.md：MySQL 8.0.21+ 才有 SQL 级 hint，无 SPM 等价物（社区靠 ProxySQL 锁计划）——对照显出 SPM 体系完整度 ⚠️ 转述。
- ../数据库高效优化.md：profile/baseline 中文实操稀缺，本章可当系统教程。
- ../Oracle12c数据库应用与开发/07-SQL性能诊断与调优实践.md：STA 教材化版。

## 场景→技术选型速查

| 场景 | 首选 | 次选 | 别用 | 依据节 |
|---|---|---|---|---|
| 自己能改代码、结构性坏形状 | 11.2 改写 | 11.1 加结构 | hint 交付 | 治本优先 |
| 第三方不可改、根因是统计偏差 | 11.6 SQL Profile（同时补统计） | 11.7 SPM 锁计划 | 11.5 Outlines | — |
| 升级防御 | 11.7 SPM 先捕获后升级 | optimizer_features_enable 过渡 | 裸升级 | — |
| 验证一个计划假设 | 11.3 hint（实验完删除） | OPT_PARAM 会话级 | 永久 hint | — |
| 全站点系统性错配 | 11.4 环境+Ch9 路线图 | — | 逐语句 hint | 干预半径 |
| 计划翻转急救 | 11.7 load 好计划 | 11.6 profile 顶着 | — | — |

## 自测题（闭卷复述）

1. "干预越强，可追溯性越弱"——用七族技术各举一处体现。
2. SQL Profile 为什么不锁计划？它注入的是什么、何时会反噬？
3. SPM 三支柱各自的开关/视图/任务名是什么？
4. baseline 腐化的成因与治理动作？
5. hint 静默失效的三种触发方式与检测方法？
6. OPT_PARAM hint 把哪类风险缩小到什么范围？
7. Stored Outlines 被判死刑的两条技术原因？
8. force_matching 的适用与危险场景各一？
9. "用完 profile 必须回头补统计"为什么是义务？
10. 改写语句的等价性证明至少给哪两样证据？

## 易混点与补记

- hint 是指令不是建议这句老话只对了一半：环境不满足时优化器可以静默忽略（⚠️ 转述）。
- OUTLINE 全文与 hint 子句的差别是可移植性：前者能喂给 SQL Profile/SPM 重建。
- 21 种转换清单要背的是"方向"不是名字：合并类（view merging/unnesting）、展开类（OR expansion）、剪枝类（predicate movement）三族。
- NO_EXPAND、NO_MERGE 这类反串是"取消优化器的优化"，用来恢复语义直觉，不是性能开关。
- 同一条 SQL 用 hint 强制与用 Profile 强制，效果等价但治理成本完全不同：后者可演进、前者入代码。

## 核心概念速览（中英对照）

- **访问结构** — Access Structures：索引/MV/分区等物理辅助对象
- **语句改写** — Altering the SQL Statement：等价重写显露可优化形状
- **提示** — Hints：语句级优化指令；静默失效是最大特性
- **Outline Data** — 计划蓝图：hint 唯一可靠来源
- **OPT_PARAM** — 环境参数提示：系统旋钮装进单语句
- **Stored Outlines** — 存储大纲：已退役的计划锁定件
- **SQL Profile** — 成本校正集（STA 产物）
- **SQL Tuning Advisor** — STA：自动调优顾问（许可受限）
- **SPM** — SQL Plan Management：捕获-选择-演化三支柱
- **Plan Baseline** — 计划基线：受信任计划集
- **Evolution** — 计划演化：以实测成绩转正
- **force_matching** — 忽略字面量差异套用计划
- **干预半径** — 手段强度 vs 可追溯性的守恒暗线

## 最新演进与工业实践

- **19c/23ai 对位**：STA/SQL Profile 在自治云被 Automatic SQL Tuning 与 SQL Monitoring/Insight 页吸收；**SPM 仍是 Oracle 官方承诺长期存在的唯一计划治理机制**；自动优化任务链（directive→auto stats→auto index→SPM evolve）把本章后三族串成流水线 ⚠️ 转述。
- **开源对位**：PostgreSQL pg_hintplan（hint）、无内建 SPM；MySQL 8 hint + ProxySQL 规则；DuckDB 走"轻干预重统计"——三层干预体系（hint/profile/SPM）仍为 Oracle 独有完整度 ⚠️ 转述。
- **文档锚**：SPL/CHG 相关 26 版文档族可达（docs.oracle.com/en/database/oracle/oracle-database/26/ ✅）。
- 社区共识：hint 治理（清点、失效检测、版本升级回归）仍是 2026 年大厂的年度工程活动，11.3 Pitfalls 常读常新。
