# 第 19–20 章：使用 SQLT 提升查询性能 · 处理 XA 分布式事务的问题

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；Oracle 行为为 11gR2–12cR1 口径转述，无 Oracle 实测）。本文件 🔧 组为 SQLite SAVEPOINT 部分回滚类比，**非 Oracle 行为**。

## 本文件定位

第 19 章是"单条 SQL 的法证层"：SQLT 工具把前面所有章的证据（游标库、AWR 历史、10053 追踪）自动汇成一份诊断档案；第 20 章是全书唯一"跨库事务"章：XA/两阶段提交的悬挂与超时，故障域超出单实例，取证面也超出单库视图。

## 第 19 章 使用SQLT提升查询性能

### 19.1 工具画像（⚠️ 社区/作者文档转述）

- SQLTXPLAIN（俗称 SQLT）= Mauro Pagano 的免费诊断脚本集（MOS Note 初发，后迁 GitHub）：给一个 sql_id，产出一份含文本/HTML 的档案包。
- 采集面四类证据一次拉齐：①游标库现计划与执行统计（`v$sql`/`v$sqlstat`）；②AWR 历史计划时间线（`dba_hist_sqlstat`/`dba_hist_sql_plan`，回看第 10 章）；③优化器侧信道（10053 追踪、SQL 追踪、系统/对象统计）；④环境对照（参数/统计/权限/对象版本）。
- 与 10053 的关系：SQLT 不解释"成本怎么算错"，那是 CBOF 第 14 章 10053 精读的活；SQLT 把 10053 抓进档案供 Lewis 式阅读——**先取证后归因**的分工。

### 19.2 用法阶梯（⚠️ 转述）

1. `sqlcommon.sql` 常规诊断（sql_id 或 SQLHA hash 输入）→ 出主报告。
2. `sqldiag.sql` 诊断"诊断本身"（工具权限/诊断表坏境自检）。
3. Method-R 三件套（作者后期扩展）：mr_analyze（TOP 事件）、mr_broadcast（计划时间线）、mr_trace_it（会话级追踪）——把第 9/10 章的手工作画成脚本。
4. 计划突变案的标准动线：SQLT 档案里的"计划时间线"找翻转 snap → 对齐该 snap 前后的统计/绑定/参数变更 → 回第 4/5 章处置。
5. 归档纪律：诊断输出落工单库（SQLT 的 `SQLTXPLAIN` 用户与诊断表留存），复发性问题靠比对历史档案而不是重跑。

### 19.3 边界（⚠️ 转述）

- SQLT 只读诊断面（除诊断表 schema），不改计划不执行变更；Tuning Pack 许可问题不因其免费而豁免（读 AWR 视图仍受许可约束——第 9 章红线）。
- 对第 11 章 RAC 案：SQLT 按实例采集，全局问题需逐节点跑或用其 RAC 变体脚本。

## 第 20 章 处理XA分布式事务的问题

### 20.1 症状面（⚠️ 转述）

- 应用报 `ORA-01591`（锁定了可疑分布式事务）、挂起行长时间不可操作；`DBA_2PC_PENDING` 有残留记录，事务处于"prepared 未 commit"的两阶段中间态。
- 中间件（TP Monitor/应用服务器 JTA）与数据库的 XA 会话失配：超时 `ORA-02040`?（远程库连接串失效）与 XA ER 状态错乱、分支局部结果与全局决议不一致。
- 隐性面：悬挂 UNDO 使块持续被"未来提交"污染——第 3 章热点与第 1 章一致性读都可能被其牵出次生症状。

### 20.2 诊断路径（⚠️ 转述）

1. `DBA_2PC_PENDING`/`DBA_2PC_NEIGHBORS`：拿到 local/trans 事务 ID、状态与参与节点清单。
2. `DBMS_XA.XA_RECOVER`：从数据库侧枚举可恢复的 XA 分支（RM 侧真相）；与 TP Monitor 的 TM 侧记录对账——**两边都有才算完整证据**，任何一侧独断都可能错杀。
3. 会话-分支映射：`v$session` 中 XA 类型会话与 `X$KTUXE` 类内部视图（社区口径，官方不承诺）辅助判断活跃分支。
4. 时间要素：核对 `XA COMMIT/ROLLBACK` 超时参数与中间件全局超时配置是否小于分支恢复窗口（典型配置病）。

### 20.3 处置与预防（⚠️ 转述）

- 决议已明（TM 侧有终态）：让自动恢复机制重放提交/回滚（`DBMS_SYSTEM` 设置事件 10026 打开自动恢复跟踪，社区口径）。
- 决议缺失（TM 记录丢失）：人工 `COMMIT FORCE 'local_id', n` / `ROLLBACK FORCE ...`，以 `DBA_2PC_PENDING` 与业务侧数据对账后执行——**强制决议是本章的最高危操作**，错一个分支即制造静默不一致。
- 预防：全局事务超时链（TM 超时 > RM 超时）；跨库改单库+本地幂等；XA 会话池化复用（12c 连接池/DRCP 场景下 XA 亲和）；RAC+XA 组合的锁面热点回到第 3/16 章工具箱。

## 19.4 常见误区（⚠️ 社区口径）

- "SQLT 会给修复方案"——它是取证器不是决策器：修复动作回第 4/5/12 章机制库选。
- "免费工具=无许可问题"——工具免费，但它读的 AWR 视图照旧踩 Diagnostics/Tuning Pack 线（第 9 章红线）。
- "档案越厚越安全"——没有基线对照的档案只是库存；复发案的价值在跨档案 diff。

## 20.4 超时链演练：制造悬挂再收服（⚠️ 按章主题结构化）

1. 三张卡同图核对：TM 全局超时 / RM（DB）事务超时 / 连接池借出超时——`TM > RM > 池` 的次序被反置是最高频错误配置。
2. 制造：测试库 XA 分支 prepare 后强杀中间件进程，得到一条受控悬挂。
3. 收服：`DBMS_XA.XA_RECOVER` 枚举 → 与业务流水三方对账 → COMMIT/ROLLBACK FORCE 走完并留判据记录。
4. 自动恢复验证：事件 10026 跟踪后台 recover 的触发与重试，确认"决议可达"链路活着。
5. 台账：季度统计悬挂成因分布（中间件重启/断网/超时错配），预防分派回对应配置层——本章的"预防"是一份配置审计清单，不是单个参数。

## 🔧 实验 G5 · SAVEPOINT 部分回滚（非 Oracle；Python 3.13 / SQLite 3.45.3）

```text
### G5 distributed/partial rollback (XA vs SAVEPOINT)
after partial rollback -> [('A', -100), ('B', 90)]
```

- 方法：单事务内 `BEGIN` → 分支 A 写入 → `SAVEPOINT sp1` → 分支 B 写入 → 模拟 B 失败 `ROLLBACK TO sp1` → B 重试修正写入 90 → `COMMIT`。结果 A 的 -100 保留、B 的 100 撤销、90 生效。
- 对照 XA：SAVEPOINT 给了"部分回滚"的**单库局部**版本；XA 的 prepared 态是它的分布式推广——只是"决议记录"从 undo 换成了 `DBA_2PC_PENDING`，必须跨进程持久化。悬挂事故的本质即"有 sp1 但没有可靠的人记住要 COMMIT 还是 ROLLBACK"。**单文件内不存在这个缺口，分布式才有**。

## 关联阅读

- 计划归因深读（10053 成本解剖）：[../Cost_Based_Oracle_Fundamentals/14-10053跟踪文件.md](../Cost_Based_Oracle_Fundamentals/14-10053跟踪文件.md)；ACS/SPM 处置：[02-GC缓冲区忙等待、自适应游标共享与SPM.md](02-GC缓冲区忙等待、自适应游标共享与SPM.md)
- 悬挂 UNDO 的次生面：[01-LOB段调优与UNDO损坏处理.md](01-LOB段调优与UNDO损坏处理.md)；RAC+XA 锁热点：[06-RAC故障诊断与SQL顾问.md](06-RAC故障诊断与SQL顾问.md)
- 跨引擎排错对照（2PC 同题）：[../MySQL排错指南.md](../MySQL排错指南.md)

## 症状 → 动作速查表

| 症状 | 第一动作 | 章节 |
|---|---|---|
| 单 SQL 计划突然翻转 | SQLT 档案看计划时间线定位翻转点 | Ch.19 |
| 要归因"成本为何算错" | 档案取 10053，转 CBOF 第 14 章读法 | Ch.19 |
| ORA-01591 行锁悬挂 | DBA_2PC_PENDING + XA_RECOVER 两侧对账 | Ch.20 |
| TM 记录丢失 | COMMIT/ROLLBACK FORCE（先业务对账） | Ch.20 |
| XA 频繁超时 | 核对 TM/RM 超时链与池化配置 | Ch.20 |
| 悬挂牵出一致性读慢 | 先清悬挂再谈 LOB/热点（回看 1/3 章） | Ch.20 |

## 自测题

1. SQLT 四类证据各来自哪些视图？其中哪两类构成"计划时间线"？
2. 为什么说 SQLT 与 10053 精读是"取证/归因"分工？
3. 免费工具为什么不豁免 Tuning Pack 许可？读 AWR 视图的合规线在哪？
4. 两阶段提交中 TM/RM 各持有什么证据？缺一侧会怎样？
5. COMMIT FORCE 的前置条件与不可逆代价是什么？
6. 🔧G5 中 `ROLLBACK TO sp1` 对应 XA 世界的哪个动作？差异在哪？
7. 悬挂 XA 事务如何把第 3 章问题"牵"出来？给出传导链。

## 核心概念速览（中英对照）

- **SQLT** — SQLTXPLAIN：Pagano 的单 SQL 诊断档案工具 ⚠️
- **计划时间线** — Plan Timeline：同 sql_id 跨快照的计划演变序列 ⚠️
- **Method-R** — Method-R：作者的事件驱动 SQL 诊断方法论脚本组 ⚠️
- **诊断留存** — Diagnostic Archive：SQLT 用户与诊断表的历史档案面 ⚠️
- **两阶段提交** — 2PC：prepared/commit 两段式的全局事务协议 ⚠️
- **TM/RM** — Transaction/Resource Manager：全局协调者与分支资源库 ⚠️
- **悬挂事务** — In-Doubt Transaction：决议缺失的 2PC 中间态 ⚠️
- **DBA_2PC_PENDING** — 悬挂事务登记视图：local ID/状态/参与节点 ⚠️
- **XA_RECOVER** — DBMS_XA.XA_RECOVER：RM 侧枚举可恢复分支 ⚠️
- **强制决议** — COMMIT/ROLLBACK FORCE：人工替 TM 做终态决定 ⚠️
- **保存点** — SAVEPOINT：🔧 单事务内的部分回滚锚（非 Oracle）
- **超时链** — Timeout Chain：TM>RM 的超时配置次序纪律 ⚠️

## 最新演进与工业实践

- **SQLT 现状**：作者 GitHub 持续维护并衍生 DBORAD/eDB360 全库体检；Method-R 培训体系将其方法论化——本书时代的"手工 SQLT"已发展为"标准取证流程" ⚠️（github.com/mauropagano 域名检索命中 ✅，细节未直读）。
- **XA 的阵型转移**：微服务兴起后"跨库 XA"让位于 Saga/TCC 等最终一致模式；Oracle 侧 XA 仍在传统 ESB/银行清算存量系统中大量服役，`DBA_2PC_PENDING` 取证学不变 ⚠️ 转述。
- **许可新势**：23ai 将 ASH 等诊断面免费化，第 9/19 章的"无 Tuning Pack 降级路径"整体改善（docs.oracle.com 23ai 许可文档 ✅ 域名可达，内容未直读 ⚠️）。
- **跨引擎镜像**：PostgreSQL 的 `pg_prepared_xacts`+`COMMIT PREPARED`、MySQL XA 的 `XA RECOVER`/`XA COMMIT x FORCE`——悬挂事务处置在各引擎同构；🔧G5 演示的 SAVEPOINT 是它们的单机退化版，"决议持久化"才是分布式新税。
