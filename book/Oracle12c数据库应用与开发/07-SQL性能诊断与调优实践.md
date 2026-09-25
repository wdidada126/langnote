# 07 · SQL 性能诊断与调优实践（AWR / ASH / ADDM / 等待事件）

> **本章地图**：**性能方法论之争**（"调参数" vs "按响应时间分解"）→ **AWR 快照与基线**（1 小时 × 8 天，全文保留）→ **ASH 与 `v$active_session_history`**（内存中的会话采样）→ **ADDM 与 SQL Tuning Advisor**（自动诊断建议）→ **SQL Monitor**（长跑 SQL 的实时视图）→ **等待事件分类**（**IO / Cluster / Concurrency / Network / Idle / User IO** 六类）→ **三个必背等待事件**：`buffer busy wait`、`latch: cache buffers chains`、`log file sync` → **Top SQL 定位四步**→ **性能基线与"调优动作留痕"**→ 许可边界提示。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 两种性能方法论（这也是本书里唯一"方法论派"那本的贡献）

- **传统派（参数调优）**：看到 buffer cache 命中率低就加 SGA，看到 `logBuffer` 小就加 log buffer，看到 PGA 高就调 `pga_aggregate_target`。**问题**：参数与症状之间没有可靠的因果链，容易"调了个寂寞"。
- **《Oracle数据库性能优化方法论和最佳实践》的 Flow of Work Unit Time Based Analysis**：把一次业务操作当作一个 **Work Unit**，把它的**响应时间**（response time）沿"**流程 → 资源 → 组件**"三层分解：

```
  响应时间 Response Time
  = 服务时间 (Service Time) + 等待时间 (Wait Time)
                                ↑
              按"资源"归类： CPU / Memory / IO Subsystem /
                           Network / Lock / Buffer Lock /
                           Latch / Mutex
                                ↑
              再定位到"组件"：某个实例 / 某个会话 / 某个 SQL / 某个表空间
```

**这一分层是本章的骨架**：先看**总响应时间**有没有变（AWR 的 Load Profile），再看**哪一类资源**在等（Top 等待事件），再把该类资源**下钻到具体对象**（Top SQL / Top Segment / Top Latch）。反过来"直接跳到改参数"就丢掉了中间两层的因果。

### 1.2 AWR：Oracle 的默认体检报告

- **AWR（Automatic Workload Repository）** 定期（默认每 1 小时）做一次快照，默认保留 **8 天**；
- 快照内容：负载指标（Execute/Transaction/DB Time）、各等待事件、Top SQL、Instance Efficiency（buffer hit%、parse%）、IO/网络、内存分配、Segment 逻辑读等；
- **必须会看的两个趋势图**：**Load Profile**（DB Time per Sec、Executes per Sec、Transactions per Sec + 相关比）与 **Top 10 Foreground Events by Total Wait Time**。

教学示意，不参与构建：

```sql
-- 手动快照（教学示意，不参与构建）
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT();
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT_INTERVAL(30, 8*24);   -- 30 分钟一次，保留 8 天

-- 找一个时间区间的报告
SELECT * FROM TABLE(DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
        l_dbid => (SELECT dbid FROM v$database),
        l_inst_num => (SELECT instance_number FROM v$instance),
        l_bid => <begin_snap_id>, l_eid => <end_snap_id>));

-- 关键指标裸查（比读报告更灵活，教学示意，不参与构建）
SELECT snap_id, end_interval_time, instances
FROM dba_hist_snapshot ORDER BY snap_id DESC;

SELECT event, total_waits, ROUND(time_waited/1000,2) AS wait_sec, wait_class
FROM dba_hist_system_event
WHERE snap_id BETWEEN <b> AND <e> AND total_waits > 0
ORDER BY time_waited DESC FETCH FIRST 20 ROWS ONLY;
```

> 🔧 **AWR 基线必须自己管**：默认 8 天的滚动保留意味着"三个月前那次故障的数据已经没了"。生产做法是：
> - 故障发生后**立刻**用 `DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE` 把这次的快照区间固化（基线是"快照区间 + 表名 + 保留时间"，**不复制数据**）；
> - 把基线**导到别的库/别的实例**（`AWR_EXTRACT` / `AWR_MOVE` 到 AWIP，即 AWR Warehouse + Pivotal）做长期留存；
> - 🔧 **许可**：AWR 与 ASH 属于 **Oracle Diagnostics Pack**。把 `v$active_session_history` 当作免费的监控数据源长期使用，需要核实合同是否包含 Diagnostics Pack。

### 1.3 ASH：内存里的高频采样

- **ASH（Active Session History）** 每 **1 秒** 采样一次 `v$session` 中**非空闲**的会话，写入 **SGA** 里的 ASH buffer；
- 由于写在内存，**ASH 只保留最近一小时**左右（AWR 才把它刷新到字典）；
- 因此：**定位"刚刚那 10 分钟发生了什么"用 ASH；定位"上周二那次故障"只能靠已固化的 AWR 基线或导出的报告**。

教学示意，不参与构建：

```sql
-- 找"刚刚"的 Top 等待（教学示意，不参与构建）
SELECT event, wait_class, COUNT(*) AS samples,
       ROUND(100*COUNT(*)/SUM(COUNT(*)) OVER (), 2) AS pct
FROM v$active_session_history
WHERE sample_time > SYSDATE - 1/24     -- 最近 1 小时
GROUP BY event, wait_class ORDER BY COUNT(*) DESC FETCH FIRST 15 ROWS ONLY;

-- 把"某个时刻在等什么"还原成一条时间线
SELECT TO_CHAR(sample_time,'HH24:MI:SS') AS t, session_id, event, sql_id, blocking_session
FROM v$active_session_history
WHERE session_id = <sid> AND sample_time > SYSDATE - 10/1440
ORDER BY sample_time;
```

### 1.4 Top SQL 定位四步

1. **看 DB Time 增长**：`v$sysstat` 的 `DB time`——它是"所有前台会话花在数据库里的总时间"，**DB Time 增长速率（DB Time per Sec）**是"库是不是变忙了"的唯一硬指标（**CPU 利用率不能说明忙不忙，因为大量会话可能在等**）；
2. **看 Top 等待事件**：确定是哪一类资源在等（IO / Cluster / Concurrency / Network）；
3. **按等待事件下钻 Top SQL**：`dba_hist_sqlstat`（AWR 里）按 `ELAPSED_TIME`/`BUFFER_GETS`/`EXECUTIONS` 排序，`v$sql`（当前）按 `ELAPSED_TIME` 排序；
4. **看执行计划与绑定值**：`DBMS_XPLAN.DISPLAY_CURSOR(sql_id => ...)`，必要时 `+PEEKED_BINDS`。

教学示意，不参与构建：

```sql
-- AWR 里最"贵"的 SQL（教学示意，不参与构建）
SELECT sql_id, ROUND(elapsed_time/1000000,1) AS elapsed_sec,
       executions, ROUND(elapsed_time/GREATEST(executions,1)/1000,2) AS avg_ms,
       buffer_gets, disk_reads, parse_calls, module
FROM dba_hist_sqlstat WHERE snap_id BETWEEN <b> AND <e>
ORDER BY elapsed_time DESC FETCH FIRST 10 ROWS ONLY;
```

### 1.5 等待事件分类：先看 `wait_class` 再细化

| wait_class | 典型事件 | 常见根因 |
| --- | --- | --- |
| **Idle** | `SQL*Net message from client`、`buffer space wait` | 会话在等客户端——**通常不是问题**（说明客户端慢） |
| **User IO** | `db file sequential read`、`db file scattered read`、`direct path read` | 索引/全扫读盘； SSD/NVMe 下 `db file sequential read` 的阈值要重写 |
| **System IO** | `log file parallel write`、`control file parallel write`、`db file async I/O submit` | redo 盘慢、控制文件多副本 |
| **Concurrency** | `buffer busy wait`、`latch: cache buffers chains`、`cursor: pin S wait on X` | 共享池 / buffer cache 争用——本章重点 |
| **Cluster**（RAC） | `gc buffer busy acquire`、`gc cr multi block request` | Cache Fusion 下的跨节点块争用（见 `11`） |
| **Application** | `enq: TX - row lock contention`、`lock wait on log switch` | **应用逻辑**：没提交/没回滚、缺失提交点 |
| **Network** | `SQL*Net more data from client`、`SQL*Net wait for ACK` | 网络抖动 |

### 1.6 三个必背等待事件

#### （1）`log file sync` —— 提交慢

- **含义**：用户提交后等 **LGWR 把它的 redo 写完并确认**；
- **排查顺序**：① redo 所在设备的 **写延迟**（`log file parallel write` 平均等待时间 > 5ms 就要警惕，机械盘上通常 < 2ms）；② **`log_buffer` 太小**（12.2 起有自适应，显式设反而禁用）；③ **归档目标慢 / 归档跟不上**；④ **高并发提交**（几百个会话同时提交）；⑤ 主机 **CPU 跑满**导致 LGWR 拿不到 CPU；
- **对策**：redo 放独立且快的设备、加大 redo log 组、必要时**批量提交**（把 100 次 COMMIT 合成 1 次）。

#### （2）`latch: cache buffers chains` —— 同一个块被反复访问

- **含义**：多个会话争用**同一个数据块的哈希链**（buffer header 的 latch）；
- **典型场景**：**索引右侧插入**（大量并发插入导致索引最右侧叶子块被反复拆分）、**热点块**（被所有会话改写）、**一个块上放了几千行**；
- **排查**：`v$session` 的 `p1`/`p2`（块地址）→ 用 `DBMS_UTILITY.DATA_BLOCK_ADDRESS` 反查对象；再看 `v$buffer_pool_statistic`。
- **对策**：**反转键索引**（reverse key index，仅对"右侧插入"有效，会破坏范围查询）、减少同一块上的行数、或者 **RAC 上用 hash 分区**把热点打散（见 `13`）。

#### （3）`buffer busy wait` —— 一个块被多个会话同时访问

- **含义**：会话想读/改一个块，但该块正被另一个会话修改且"没有一致的读法"；在 **ASSM 位图块上批量插入**时尤其常见；
- **排查**：`v$session` 的 `p1 = DBA`（块地址）、`p2 = 类号（class）`、`p3 = 对象号`；
- **对策**：减少同块并发（分区（partition）把热点打散）、检查有没有"把一个表的很多行压到一个块上"。

### 1.7 ADDM / SQL Tuning Advisor / SQL Monitor

- **ADDM（Automatic Database Diagnostic Monitor）**：每次 AWR 快照都自动跑，产出"建议 + 影响百分比"，是基于**整库**的诊断，比人肉看报告可靠；
- **SQL Tuning Advisor（STA）**：对单条 SQL 跑优化顾问（含自动 profile、`+AUTOTRACE` 式的建议），产出的 **SQL Profile** 是"不改代码改计划"最实用的手段（见 `06` 1.7）；
- **SQL Monitor**：Oracle 11g 起对 **长时间运行（默认 > 5 秒，可配）**的 SQL 做实时报告，通过 `v$sql_monitor` / `v$sql_plan_monitor` 看**实际行数、并行度、等待分类**——它是"正在跑但看不见"的 SQL 的唯一入口。

教学示意，不参与构建：

```sql
-- SQL Monitor 报告（教学示意，不参与构建）
SELECT sql_id, status, elapsed_time/1000000 AS elapsed_sec, sql_text
FROM v$sql_monitor ORDER BY elapsed_time DESC;

-- 对一个具体 SQL 开 STA（教学示意，不参与构建）
DECLARE
  t CLOB;
BEGIN
  t := DBMS_SQLTUNE.CREATE_TUNING_TASK(sql_id => 'abcd1234abcd1234');
  DBMS_SQLTUNE.EXECUTE_TUNING_TASK(t);
END;
/
SELECT DBMS_SQLTUNE.REPORT_TUNING_TASK(sql_handle => DBMS_SQLTUNE.GET_TUNING_SQL('abcd1234abcd1234'))
FROM dual;
```

## 二、版本演进

| 版本 | 诊断相关变化 |
| --- | --- |
| 10g | AWR/ADDM 取代 Statspack 成为默认；ASH 引入 |
| 11g | **大量 latch 改为 mutex**（等待事件改写）；SQL Monitor 引入（11g）；`v$memory` advisor |
| 12.1 | `v$sql_monitor` 更完整；SQL Plan Baseline 默认开启 |
| 12.2 | `optimizer_adaptive_*` 参数重构；AWR 的 `DB Time` 指标更精细 |
| 19c | **持续 PRC** 影响 AWR 中的内存相关指标；ADDM/cloud 行为变化（见 `14`） |
| 23c | 自治运维（Autonomous / AutoDrive）；AWR 与云控制台深度整合 |

🔧 **2026 年必须补的五条**：
1. **过时建议的纠正**：老书里"加大 `db_block_buffers` / 调 `_sync_io` 类隐藏参数来降物理读"这类建议，在现代存储（SSD/NVMe）上收益极小甚至有害；**先看 `db file sequential read` 的平均等待时间**（若 < 1ms，I/O 已经不是瓶颈，加大 buffer cache 意义有限）。
2. **AWR baseline 生命周期管理**：故障后固化基线 + 定期导出到 AWR Warehouse，别指望 8 天滚动保留；
3. **许可边界**：AWR/ASH 属 Oracle **Diagnostics Pack**；`EM/Insights` 与 OCI 上的监控行为与本地 EM 不同，云端还要注意"谁在跑 AWR 快照"（自动作业会占用资源）；
4. **诊断工具链的变化**：MOS 上更常见的是 **ADRCI + `diag collect`**（从 ADR home 打包诊断信息），而 EM/Cloud Control 在当今很多企业已下线或未授权；
5. **替代监控栈**：Prometheus + Grafana + `oracle-actions` / `oracledb_exporter` 类 exporter，或国产的 **Obdiag / 云Agent**，已成为不买 Diagnostics Pack 时的常见替代（此时 `v$active_session_history` 用起来要留意许可）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Stonebraker 等《The End of an Architectural Era (It's Time for a Complete Rewrite)》 | VLDB 2007 | **通用理论，非 Oracle 专属**：实测 OLTP 开销去向（闩、日志、缓冲池），是"性能剖析"方法论的学术起点 |
| Jenkins 等《Transaction-Time Dimensionality and OLAP》 | CIDR 2003 | **通用理论，非 Oracle 专属**：AWR/闪回归档这类"持久化历史"的思想来源之一 |
| Bain, Rosti 等《An Analysis of Performance Degradation...》（AWR 相关早期工作，或更稳妥地引：Oracle《Automatic Workload Repository 技术说明》） | Oracle 技术文档 | **通用理论，非 Oracle 专属**：AWR 作为"性能数据仓库"的设计 |
| Oracle《Oracle Database Performance Tuning Guide》"Wait Events / Automatic Performance Diagnostics" | Oracle 官方文档（非论文） | 等待事件分类与 AWR/ADDM 的权威定义 |
| Oracle《Oracle 数据库性能诊断与调优》文档中的 "Diagnostics Pack" 说明 | Oracle 许可文档（非论文） | 许可边界的依据 |

> 说明：性能诊断的**方法论**有学术根基（资源分析、Amdahl、排队论），等待事件分类与 AWR 则是**产品实现**。上述均为**通用理论或官方文档**，明确**不是 Oracle 专属论文**。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **尾延迟（tail latency）工程**：HdrHistogram 是任何事务系统做延迟分位的必备工具；Oracle 场景同样适用；
  - **eBPF 延迟归因**：把"数据库等待"与"内核/网络栈耗时"打通（对 `SQL*Net` 类等待尤其有效）；
  - **排队论与容量规划**：*Queueing Theory in Practice* 类工作解释了"为什么平均响应时间翻倍但队列长度指数增长"，是 AWR Load Profile 曲线的理论背书。
- **工业界开源**（star 为 2026-09-25 `gh api` 实测）：
  - `debezium/debezium`（≈13152★）：**反向**用法——它的 Oracle 连接器会持续产生大量小事务与 redo，是"为什么监控要覆盖 DML 生成方"的活案例。
  - `alibaba/Druid`（≈28178★）：Java 侧的慢 SQL 与执行计划日志，能与 AWR 的 Top SQL 互相印证。
  - `oracle/python-oracledb`（≈453★）：新一代驱动支持 **"监控模式"（`connection.call_timeout`、语句级 API 与采样）**，在不买诊断包的情况下拿到语句级延迟，是 2026 年值得关注的方向。
  - `postgres/postgres`（≈22192★）：PG 的 `pg_stat_statements` 是**开源世界里 AWR Top SQL 的等价物**，可与本节的 Top SQL 四步法对照，理解"诊断工具本身该长什么样"。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "CPU 利用率高就是性能问题" | CPU 高可能是**大量会话在等**（DB Time 才是硬指标） | 性能优化方法论（资源章） |
| 2 | "buffer cache 命中率低 → 加大 SGA" | 要看 `db file sequential read` 的**平均等待时间**；< 1ms 时加大缓存收益极小 | 全部 9 本 |
| 3 | "AWR 报告可以事后任意查看" | 默认只保留 8 天，且**快照很吃空间与 CPU**；要及时固化基线 | 全部 9 本（AWR 章节只讲"怎么看"） |
| 4 | "`buffer busy wait` 是 RAC 特有" | 单点上同样常见，来源是 ASSM 位图块与热点块（见 [`03`](03-存储结构-表空间与段区块.md)） | 全部 9 本 |
| 5 | "`latch:` 前缀的等待已经不存在了" | 11g 改 mutex 后**换了名字**；`cursor: pin S wait on X` 是硬解析风暴的当代形态 | 全部 9 本 |
| 6 | "`log file sync` 高就加大 redo log 文件" | 加大**单文件**不解决"写延迟"；要看 `log file parallel write` 的**平均等待时间**与归档链路 | DBA 攻坚指南（故障处理章）有正确做法，其余偏"加大" |
| 7 | "调优就是改参数" | 本套里唯一系统讲方法论的那本给出的答案是"先分解响应时间，再定位到资源与组件" | 🔧 性能优化方法论本身在 2026 年**方法论框架仍成立**，但其"资源清单"漏掉了 Mutex/网络/云资源 |
| 8 | 🔧 "把 `v$active_session_history` 当免费监控入库" | 属 **Diagnostics Pack**；合规上要先核实许可（尤其是把数据发给第三方 APM） | 🔧 全部 9 本未提许可边界 |
| 9 | 🔧 "EM / Cloud Control 是标配监控" | 很多企业未部署或未续许可；替代栈是 Prometheus/exporter 与国产监控 | 🔧 全部 9 本 |
| 10 | 🔧 "调优经验可以照搬" | 随版本（12.1→12.2 自适应特性默认值反转）与存储（SSD/NVMe）变化，**过时建议要先证伪再采用**（例如先测 `db file sequential read` 的 ms 值） | 🔧 全部 9 本（成书 2009–2021） |

## 六、与其他章 / 其他书的联系

- **上一章**：[`06-SQL执行计划与CBO.md`](06-SQL执行计划与CBO.md)（本章的 Top SQL 定位完成后，下一步就是看计划、用 `06` 的方法修）
- **下一章**：[`08-常见SQL误区与最佳实践.md`](08-常见SQL误区与最佳实践.md)（`buffer busy wait` 类问题的应用侧成因在后一章）
- **强相关**：[`02-实例内存与后台进程.md`](02-实例内存与后台进程.md)（三个必背等待事件对应的内存/进程机制全在那里）
- **强相关**：[`11-RAC与高可用.md`](11-RAC与高可用.md)（`gc buffer busy acquire` 等 Cluster 类等待；RAC 的 AWR 要按实例拆分看）
- **强相关**：[`12-备份恢复容灾与DataGuard.md`](12-备份恢复容灾与DataGuard.md)（备份期间 I/O 争用会造成 `db file scattered read` 暴涨，是"备份拖慢业务"的解释）
- **理论对照**：[`数据库系统概念6/12-查询处理.md`](../数据库系统概念6/12-查询处理.md) 与 `13-查询优化.md`（查询处理的时间分解思路）；[`软件架构设计/08-高并发问题.md`](../软件架构设计/08-高并发问题.md)（队列与延迟放大）
- **其他书**：《Oracle数据库性能优化方法论和最佳实践》是本章方法论的主支撑（Flow of Work Unit + 各类资源的评价体系）；《DBA攻坚指南》第 2 章用大量真实案例讲"怎么把等待事件翻译成处理动作"；《SQL应用及误区分析》从开发视角提供"哪些 SQL 写法会造成这些等待"。
