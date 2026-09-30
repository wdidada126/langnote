# 第 11–12 章：RAC 的故障诊断 · 利用 SQL 顾问分析和修复 SQL 问题

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；RAC/顾问行为为 11gR2–12cR1 口径转述，无 Oracle 实测）。类比实验见 [02 号文件 🔧G1](02-GC缓冲区忙等待、自适应游标共享与SPM.md)（非 Oracle）。

## 本文件定位

第 11 章把第 3 章的"集群等待事件"下钻到集群ware 层（CRS/GI 组件、节点驱逐、VIP 漂移），是全书唯一跨出数据库进程边界的章；第 12 章把第 4/5 章手工判断的计划问题交给官方顾问流水线。一章向下（基础设施），一章向上（自动化决策）。

## 第 11 章 RAC的故障诊断

### 11.1 分层故障模型（⚠️ 转述）

1. **互联层**：私有网延迟/丢包 → 症状是 gc 类等待与 cluster time 齐涨；先于任何库内分析，用 OS 面（ping/ethtool/交换机计数）证实。
2. **GI/CRS 层**：cssd 心跳丢失触发**节点驱逐（eviction）**，`ora.cssd`/`evmd` 日志与 `$CRS_HOME/log/<node>/` 系列是第一现场；11gR2 起以 `olssys`/alert log 结构化输出替代老版 srvctl 时代的散乱日志。
3. **VIP 层**：节点故障后 VIP 漂移到存活节点，客户端连接秒级重路由——VIP 未监听/SCAN（11.2 起）配置错是"应用连不上但库是好的"的头号假故障。
4. **实例层**：instance recovery 由幸存节点的 SMON/GRD（全局资源目录）回放，重启时长与 redo 应用速率相关——不是"实例崩了等运维"而是等 GLM/GES 队列清账。

### 11.2 取证清单（⚠️ 转述）

- `crsctl stat res -t` / `srvctl config database` 对照集群资源与库配置漂移（改过 diskgroup 没改 srvctl 是经典事故）。
- `v$cache_transfer`、`v$cr_block_receive_time` 类直方图定位"慢在传输还是慢在排队"。
- 驱逐原因读 cssd log 的 `misscount`/`disktimeout` 参数组合；公共存储心跳（ voting 磁盘）IO 抖动是另一大触发源——**集群病常是存储病**。

### 11.3 处置原则（⚠️ 转述）

- 先"隔离故障节点恢复服务"（rebalance/service 重分布），后查根因；RAC 的价值正是牺牲单点换可服务性。
- 补丁与版本一致性：GI 与 RDBMS home 的 PSU 错位会制造跨版本 Cache Fusion 兼容 BUG（社区口径的高频坑）。

## 第 12 章 利用SQL顾问来分析和修复SQL问题

### 12.1 三件顾问（⚠️ 转述）

| 工具 | 回答的问题 | 输出 | 许可面 |
|---|---|---|---|
| SQL Tuning Advisor | 单条 SQL 为什么慢、怎么修 | 统计补齐/SQL Profile/结构建议/计划比较 | Tuning Pack |
| SQL Access Advisor | 物化视图/索引/分区建议集 | 批量变更脚本（可含收集统计） | Tuning Pack |
| SQL Performance Analyzer | 一次变更（升级/改参数/改 schema）对 SQL 集合的整体影响 | AWR/STA 前后对比报告，标回归语句 | Tuning Pack |

- 与第 5 章接口：STA 发现回归 → SPM 把旧好计划回钉 → 顾问给出新计划的长期修法。三章构成"检测-止血-治疗"闭环。

### 12.2 实操口径（⚠️ 转述）

- 任务入口：`ADVISOR` 页（EM）或 `DBMS_ADVISOR`/`DBMS_SQLTUNE` API；批量模式喂 `AWR` 任务（TOP SQL 自动进顾问）适合"每周体检"而非救火。
- SQL Profile 的本质是给优化器的额外信息（hint 集），**不保证计划恒定**——与 SPM 的"计划恒定"职责区分，是社区高频误解。
- 建议分级：统计类建议可直接跑；结构类建议（加索引/MV）必须回 CBOF 的选择度/聚簇因子口径复核——顾问不做副作用审计。

## 🔧 类比引读（非 Oracle）

- [02 号文件 🔧G1](02-GC缓冲区忙等待、自适应游标共享与SPM.md)："等待窗口只把失败变成延迟"——对应本章 11.1：互联与心跳超时的调参（misscount/disktimeout）同样只是**给故障处置争取时间**，不解决 IO 抖动根因。
- [05 号文件 🔧G3](05-AWR分析优化.md)：统计翻转实验——对应 12.2：SQL 顾问第一条建议永远是"补统计"，🔧G3 证明统计确实能单独翻转计划，该建议不是敷衍。

## 11.4 案例演练：白天节点被驱逐（⚠️ 按章主题结构化）

1. 止血：确认 VIP/SCAN 重路由生效、存活节点已接走业务（11.1 第 3 层），再谈取证——RAC 的默认剧本是"先服务后根因"。
2. 定性：cssd 日志的 misscount/disktimeout 触发链——私有网丢包与 voting 磁盘 IO 抖动两条主源，各用 OS 证据（网络计数/多路径延迟）二选一。
3. 清账：存活节点 alert 看实例恢复的 GRD 回放与 redo apply 速率，估出"完全恢复服务"的分钟数并通报。
4. 残留：磁盘组 rebalance 状态核对（余量不足时 rebalance 卡住会伪装成"业务慢"），再决定被逐节点何时归队。
5. 闭环：触发点回填 11.2 清单；整改方向=心跳路径与业务 IO 物理隔离（管理网/独立盘组）。

## 12.3 顾问产出采纳清单（⚠️ 转述）

- 统计类建议：先核对自动收集任务是否覆盖该对象——一次性重跑与长期机制要分清。
- SQL Profile：采纳时保存 profile 定义与生成输入；它不保证计划恒定，长期钉用请走 SPM（第 5 章）。
- 结构类建议（索引/MV）：回 CBOF 的选择度、聚簇因子与位图副作用口径复核；写路径成本单独立项评估（第 18 章"双向合同"）。
- 计划比较产物：新计划灰度用 SPM staging 装载，验证后再 accept，不直接换生产基线。

## 12.4 常用口径命令骨架（⚠️ 通用形态示意，非原书清单）

```text
-- 顾问任务（DBMS_SQLTUNE 入口）
DECLARE tsa NUMBER; BEGIN
  tsa := DBMS_SQLTUNE.CREATE_TUNING_TASK(sql_id=>'...');
  DBMS_SQLTUNE.EXECUTE_TUNING_TASK(tsa);
  SELECT DBMS_SQLTUNE.REPORT_TUNING_TASK(tsa) FROM DUAL; END;
-- RAC 状态面
crsctl stat res -t ; srvctl config database -d ...
v$session → BLOCKING_INST_ID 跨节点阻塞链（第 3 章接口）
```

## 症状 → 动作速查表

| 症状 | 第一动作 | 章节 |
|---|---|---|
| gc 等待与 cluster time 齐涨 | 先查私有网/存储心跳，后查库内热点 | Ch.11 |
| 节点被驱逐 | cssd/evmd 日志找 misscount 触发源 | Ch.11 |
| 应用连不上但库健康 | VIP/SCAN 监听与 srvctl 配置对账 | Ch.11 |
| 单条 SQL 突慢 | 顾问任务+计划比较，Profile 或 SPM 止血 | Ch.12 |
| 升级前怕计划回归 | STA 捕获 SQLSET 预演 | Ch.12 |
| 索引建议满天飞 | 回 CBOF 口径做副作用复核 | Ch.12 |

## 自测题

1. 节点驱逐的两个常见触发源分别位于哪一层？
2. 为什么"集群病常是存储病"？给出心跳路径证据。
3. VIP 漂移与 SCAN 的关系？哪一种假故障由此产生？
4. SQL Profile 为什么不能当"计划钉"用？该用哪个机制？
5. STA 的输出如何驱动 SPM 动作？说出流水线顺序。
6. 顾问的结构类建议为什么要人工复核？用第 5 章直方图知识举一例反例。
7. 节点驱逐演练中"先止血后根因"分别落在 11.1 分层模型的哪两层？
8. rebalance 卡住为什么会伪装成"业务慢"？说出传导链。

## 核心概念速览（中英对照）

- **网格基础设施** — GI/CRS：集群ware 层（Cluster Synchronization 等栈） ⚠️
- **节点驱逐** — Node Eviction：心跳超时后隔离节点保护数据一致性 ⚠️
- **投票磁盘** — Voting Disk：成员仲裁介质，IO 抖动的受害者 ⚠️
- **VIP** — Virtual IP：故障时漂移以快速重路由连接的地址层 ⚠️
- **SCAN** — Single Client Access Name：11.2 起的集群接入别名层 ⚠️
- **全局资源目录** — GRD：Cache Fusion 的块角色登记簿 ⚠️
- **实例恢复** — Instance Recovery：幸存节点回放 redo/undo 清账 ⚠️
- **SQL 调优顾问** — SQL Tuning Advisor：单语句四型建议流水线 ⚠️
- **SQL Profile** — SQL Profile：注入优化器的侧信道信息 ⚠️
- **SQL 访问顾问** — SQL Access Advisor：MV/索引/分区集合建议 ⚠️
- **SQL 性能分析器** — STA：变更前后 SQLSET 回归对比 ⚠️
- **TOP SQL 自动体检** — AWR Task：顾问批量模式的进料口 ⚠️

## 最新演进与工业实践

- **GI 演进**：19c 起 GI/RDBMS 合并 home 策略、Flex ASM 弱化对共享存储心跳的依赖；23ai 的 `crsctl` 体系继续是 RAC 排错主入口（docs.oracle.com 19c/23ai Grid Infrastructure 文档 ✅ 域名可达，内容 ⚠️ 未直读）。
- **顾问自动化**：Auto Task（自动 SQL Tuning）夜间跑 TOP SQL 并在"收益>10x 且计划可验证"时自动落地 Profile（12c 引入、19c 默认开）——第 12 章的手工顾问变为审批制 ⚠️ 转述。
- **许可现实**：Diagnostics/Tuning Pack 的许可审计是工业界长期痛点；社区以 Statspack+AWR 报表自给的低配路线仍普遍 ⚠️。
- **跨引擎对照**：SQL Server 的 Query Store +自动调优（#68 兄弟册主题）与 SPM+Auto Task 同构；PG 的 `pg_stat_statements`+auto_explain 对应顾问"发现"半边——排错自动化的三大厂实现互为镜像 ⚠️ 转述。
