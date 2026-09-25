# 04 · 事务、redo / undo / 归档与恢复

> **本章地图**：**事务的 ACID 在 Oracle 里怎么落地**（原子性靠 undo、持久性靠 redo、隔离性靠 SCN + ITL + 一致性读）→ **redo 的物理形态**（redo log file、redo log buffer、LSN / SCN、`.log` 序列号）→ **LGWR 的写时机六条**→ **undo 表空间**（回滚段、一致性读构建旧版本、`ORA-01555`）→ **检查点**（LRBA、检查点 SCN、MTTR、`fast_start_mttr_target`）→ **归档模式**（ARCn、online redo log 切换、归档目标）→ **实例恢复与介质恢复的区别**→ **闪回技术家族**→ 与 [`数据库系统概念6/26-高级事务处理.md`](../数据库系统概念6/26-高级事务处理.md) 的互链。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 Oracle 实现 ACID 的四件套

| ACID | Oracle 的实现机制 | 对应本章小节 |
| --- | --- | --- |
| **A 原子性** | **undo 表空间**里的回滚段：修改前先记旧值；失败时按回滚段把块回滚 | 1.3 |
| **C 一致性** | **SCN + ITL + 一致性读（consistent read）**：读操作按 SCN 构造旧版本 | 1.3、1.4 |
| **I 隔离性** | **行锁记在块头 ITL**（不是独立对象）；**读不加锁**（MVCC 式一致性读） | 1.3 |
| **D 持久性** | **redo（WAL）**：先写 redo 到 log buffer，LGWR 顺序写盘，提交即"落定" | 1.2、1.5 |

一句话版本：**"改数据前先写 undo，改数据时同时产生 redo，提交前 redo 必须已经落盘"**——这就是 WAL。

### 1.2 redo 的物理形态与 LSN

```
    内存                                     磁盘
┌────────────────┐                    ┌───────────────────────┐
│ redo log buffer│  --LGWR 顺序写-->  │ online redo logfile #1│ ──ARCn──► archive log
│ （几 MB~几十MB）│                    │   （50MB~几GB，循环用）  │            *.arc
└────────────────┘                    └───────────────────────┘
```

必须记住的三组概念：

1. **Redo 是"变化向量"（change vectors），不是"前像/后像"**。一条 redo 记录描述的是"在哪个块的哪个偏移上做了什么样的字节级修改"。这引出一个极重要的工程结论：**drop 一个表不会产生大量 redo，但 insert/update 大量行会**；也解释了为什么 **RMAN 的块介质恢复（BMR）** 能在极少 redo 的情况下恢复一个坏块。
2. **LSN / SCN 是 redo 的定位坐标**。Oracle 里更常提的是 **SCN（System Change Number）**，64 位单调递增；而 "LSN" 一词在 Oracle 语境里常指 **redo 记录里的 "change number / block#+offset" 组合**（`v$logmnr_contents` 里有 `SCN`、`RS_ID` 等）。严格来说：
   - **SCN = 逻辑时钟**（也是事务隔离与一致性的判定依据）；
   - **redo 记录中的步进地址（LSN-like）= 物理定位**（用于应用 redo 时按序定位块）。
3. **online redo log 是循环的**：写满一个日志组切到下一组，全部写满再回绕——**回绕到还没归档完的组，就是"归档模式缺失"导致的实例挂起**。

### 1.3 undo 表空间：一致性读的工厂

- **每条被改动的行，其旧版本被写进 undo 表空间**（在改动数据块之前或同时）；
- 一个长查询开始时记录一个 **SCN**；之后读到别人已改的行，就**顺着 undo 里的版本链把旧版本拼出来**，于是看到的是"查询开始时的一致性快照"；
- **`ORA-01555: snapshot too old`** 就是"回滚段里要找的旧版本已经被覆盖"——**不是查询慢，是 undo 不够**；
- 12c 起有 **undo 表空间的自动扩容与保留期管理**（`undo_tablespace` + `undo_retention` + `RETENTION GUARANTEE`）。

教学示意，不参与构建：

```sql
-- 检查点与 undo 现状（教学示意，不参与构建）
SELECT name, value FROM v$parameter
 WHERE name IN ('undo_tablespace','undo_retention','fast_start_mttr_target','log_buffer');
SELECT tablespace_name, status, retention, retention_alignment FROM dba_tablespaces
 WHERE contents = 'UNDO';
```

### 1.4 一致性读与 ITL：Oracle 隔离性的实现

```
    会话 A                        会话 B（读）
 ────────────────────────────────────────────────
  UPDATE emp SET sal=sal+100 WHERE empno=7369;
    └─ 数据块头 ITL 加一个事务槽
       （锁就在这里，行本身没有锁标记）
                                  SELECT sal FROM emp WHERE empno=7369;
                                    └─ 读到该块，发现 ITL 中事务未提交
                                       → 用查询开始时的 SCN
                                       → 去 undo 里取该行的旧版本
                                       → 读到 sal 的前值  ✅ 读不被写阻塞
```

与 [`数据库系统概念6/15-并发控制.md`](../数据库系统概念6/15-并发控制.md) 对照：

| 概念 | 《数据库系统概念》第 15 章 | Oracle 的实际实现 |
| --- | --- | --- |
| 锁的粒度与存放 | 锁管理器维护锁表 | **锁在块头 ITL 里**，没有独立锁表 |
| 读是否加锁 | 2PL 下读也加锁（S 锁） | **普通读不加锁**（一致性读），写写之间才互斥 |
| 隔离级别 | ANSI 四个级别 | **默认 Read Committed**；Serializable 需显式指定；**Oracle 没有脏读** |
| 写偏斜 | SI 允许，需 SSI | Oracle 默认隔离级别下**也可能出现写偏斜**（SI 的固有缺陷） |
| 长事务代价 | 锁持有久 | **undo 保留时长**成为瓶颈（长事务 → `ORA-01555`） |

### 1.5 LGWR 的六种触发时机

1. **提交时**（`COMMIT` 非立即组提交时 LGWR 立即写）——这是"提交"语义的实现；
2. **redo log buffer 三分之一满 / 到达 1 MB**（阈值由 `_log_io_size` 控制）；
3. **LGWR 超时（约 3 秒）**；
4. **DBWn 要写脏块前**，必须保证这些块的相关 redo 已经落盘（**写前写日志的强制点**，也是 `log file sync` 的成因之一）；
5. **日志切换**（`ALTER SYSTEM SWITCH LOGFILE`）；
6. **表空间 hot backup 开始/结束**（alter tablespace begin backup）。

> 由此可以理解 **`log file sync` 等待事件**：用户提交后要等 LGWR 把它的 redo 写完才拿到"提交成功"的确认。所以它高，第一嫌疑是 **磁盘写延迟（尤其是 NFS/ SAN 上的 redo 卷）**、**redo 太小**、**归档跟不上**、或者 **高并发提交**（组提交反而救你）。

### 1.6 检查点：把"恢复要重做的部分"限制住

- **LRBA（Lowest Redo Block Address）** = 上次检查点写到哪里；
- **检查点 SCN（CKPT SCN）** = 小于它的 redo 都已落盘；
- 发生实例崩溃后，**恢复只需要从 LRBA 开始重放 redo**（"前滚 roll forward"），再按 undo 回滚未提交事务（"后滚 roll back"）——这两步合起来就是 **ARIES 的 repeating history + rollback** 思路；
- `fast_start_mttr_target` 让 Oracle 自动调检查点频率，目标是把**崩溃恢复时间（MTTR）**控制住。

### 1.7 归档模式：不是"建议"，是"前提"

| 状态 | 后果 |
| --- | --- |
| **NOARCHIVELOG** | online redo 回绕即覆盖；**只能做不完全恢复**；DG 不可用 |
| **ARCHIVELOG** | ARCn 把日志复制到归档目标；可做**完全恢复与时间点恢复**；DG 的前提 |

教学示意，不参与构建：

```sql
-- 看归档状态（教学示意，不参与构建）
SELECT log_mode, force_logging, supplemental_log_data_min FROM v$database;
SELECT dest_id, destination, status, error FROM v$archive_dest WHERE dest_id = 1;

-- 强制一次日志切换，观察 ARCn 动作
ALTER SYSTEM SWITCH LOGFILE;
-- 指定时间点恢复（RMAN，教学示意，不参与构建）
-- RMAN> RECOVER DATABASE UNTIL TIME '2026-09-01 12:00:00';
```

## 二、版本演进

| 版本 | 事务 / 恢复相关变化 |
| --- | --- |
| 10g | Flash Data Checksum、`_use_adaptive_log_file_size` 前身；ADDM 恢复建议 |
| 11g | **Active Data Guard**（standby 可 open read-only 同时应用日志）；`UNDO` 自动管理成熟 |
| 12.1 | 12.1.0.2 起 `deferred redo`（standby 上的块恢复）；`RETENTION GUARANTEE` 更完善 |
| 12.2 | 日志 buffer 自动伸缩；`supplemental logging` 更易配置（对 CDC 很关键） |
| 19c | **持续 PRC（贯穿式更新）**：IM 列存与行存的更新统一；ADG 的**快速重做（Fast Start Failover）**、12.1 起的 `standby` 增量恢复 |
| 23c | 自治恢复（Autonomous Recovery）；向量与 JSON 变化也纳入 redo 体系 |

🔧 **2026 年必须补的四条**：
1. **闪回技术家族的现状**：Flashback Query（依赖 undo，只能回看"保留期内"）、Flashback Table（依赖 Flashback Log + undo）、**Flashback Drop（回收站）**、**Flashback Database（依赖 Flashback Log，且数据库必须处于 archivelog 且未 open 过）**、**Flashback Data Archive（FDA，表空间级保留数年的历史版本，用于合规审计）**，以及 **12c 起的 `ALTER DATABASE FLASHBACK`**。本书时代只把它当"第 16 章的一节功能介绍"。
2. **12.2 起的 `standby` 相关增强**与 Debezium 类 CDC 对 **supplemental logging** 的依赖——现在做 Oracle CDC，首选是 **LogMiner**（普通/补充日志）或 **GoldenGate / Debezium for Oracle**，而不是"闪回"。
3. **`_use_adaptive_log_file_size` 让 redo buffer 自动伸缩**，因此老经验里的"`log_buffer` 设 3MB"反而可能拖慢（Oracle 会自动调，但显式设置会 **禁用**自动调整）。
4. **AWR 中"恢复相关"指标**（如 `Log File Sync` 的 WAIT_CLASS 归属）与许可边界：诊断包之外查这些视图仍会受限（见 `07`）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Jim Gray《The Transaction Concept: Virtues and Limitations》 | VLDB 1981 | **事务与 WAL 的奠基文献**，redo 机制的理论起点 |
| Haerder & Reuter《Principles of Transaction-Oriented Database Recovery》 | ACM Computing Surveys 15(4), 1983 | **通用理论，非 Oracle 专属**：STEAL / NO-STEAL、FORCE / NO-FORCE、DICTIONARY 决策矩阵 |
| Mohan 等《ARIES: A Serializability-Preserving Recovery Algorithm With Repeating History》 | SIGMOD 1992 | **通用理论，非 Oracle 专属**：analysis / redo / undo 三阶段，与 Oracle 的实例恢复流程同构 |
| Bernstein & Newcomer《Principles of Transaction Processing》 | 2009（Morgan & Kaufmann 教材） | 事务处理系统的完整教材，TP monitor / XA / 两阶段提交 |
| Gray & Reuter《Transaction Processing: Concepts and Techniques》 | 1993（书） | 事务处理的百科式手册 |
| Oracle《Oracle Database Administrator's Guide》"Oracle Database Backup and Recovery / Flashback" | Oracle 官方文档（非论文） | redo/undo/检查点/闪回的权威描述 |

> 说明：redo / undo / 检查点 / 恢复是**通用数据库理论**，Oracle 只是其中一种实现。上述文献均为**通用理论，非 Oracle 专属论文**，明确标注以免误引。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **Aurora 的"日志即数据库"**（SIGMOD 2017 论文 *Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases*）：**通用理论，非 Oracle 专属**——把 redo 从"待落盘的数据"变成"持久性的唯一载体"，消除双写。
  - **早期锁释放（early lock release）**：*Aether: A Scalable Approach to Logging*（PVLDB 2010）；H-Store 的每一步。
  - **日志优化的持续研究**：*FaRM*（SIGMOD 2015，RDMA + 日志）、*Calvin*（SIGMOD 2012，确定性事务先定序再执行）。这些都不是 Oracle 论文，但解释了为什么"组提交 + 顺序写"是 OLTP 的常数级优化。
- **工业界开源**（star 为 2026-09-25 `gh api` 实测）：
  - `debezium/debezium`（≈13152★）：开源 CDC 框架。**对应 Oracle 侧的两种取日志方式——LogMiner（SQL 层解析 redo）与 Binary Reader（直接读 redo 二进制）**，对日志有不同要求（LogMiner 需要 ` supplemental logging`，这也是本章 1.7 提到的"必须给 supplemental log 的原因"）。
  - `pingcap/tidb`（≈40586★）： Percolator 事务模型（Google OSDI 2010）的开源实现，用 `start_ts`/`commit_ts` 做 MVCC，与 Oracle 的 SCN 一致性读是同一思想的不同实现。
  - `oceanbase/oceanbase`（≈10291★）：国产开源分布式数据库，**兼容 Oracle  syntax/PL 的部分最多**，其事务与多版本实现思路可与本章对照。
  - `mysql/mysql-server` / `mysql/19-redo日志.md` 等笔记：[`book/mysql/19-redo日志.md`](../mysql/19-redo日志.md) 是 redo 机制的另一套实现（MySQL 的 redo 是"物理页镜像 + 逻辑"混合，且**崩溃恢复不回滚未提交事务，靠 binlog/undo 二阶段提交**），与 Oracle 对照读很有价值。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "提交时数据块已经写进数据文件了" | 提交只保证 **redo 落盘**；数据块仍在 SGA 里脏着，由 DBWn 择机写 | 全部 9 本 |
| 2 | "读操作会被写操作阻塞" | Oracle 的**一致性读不加锁**：读会去 undo 取旧版本；**只有写与写互斥** | 全部 9 本 |
| 3 | "`ORA-01555` 是查询太慢导致的" | 根因是**回滚段里需要的旧版本被覆盖**，即 undo 不足或存在超长查询/超长事务 | 12c 教材（第 16 章闪回）未讲清 |
| 4 | "redo 里记录的是改之前的值" | **redo 记录的是字节级变化向量**，不是前后像；这是 RMAN BMR 能少 redo 恢复单块的原因 | 全部 9 本 |
| 5 | "归档模式只是备份的前提，慢的时候可以关掉" | 关归档会让所有时间恢复与 DG 失效，且需要先 clean shutdown 再 mount 才能改 | DBA 攻坚指南（第 1/2 章）有流程约束 |
| 6 | "DDL 也会参与事务回滚" | **DDL 会隐式提交**（commit before/after），不可回滚——这是最常见的"我回滚了怎么还在" | SQL 应用及误区分析（第 13 章）提到事务，但未点出隐式提交 |
| 7 | 🔧 "闪回可以查到任意时间点的数据" | Flashback Query 依赖 **undo 保留时间**（默认分钟级，除非开 RETENTION GUARANTEE 或 FDA）；**表被 TRUNCATE 后 Flashback Query 也救不了**（要靠 Flashback Drop 或 RMAN） | 🔧 12c 教材第 16 章的功能罗列易被误读 |
| 8 | 🔧 "`log_buffer` 固定设 3MB 更好" | 12.2 起有 `_use_adaptive_log_file_size`，**显式设 `log_buffer` 会禁用自动伸缩**，反而可能造成更频繁的小写入 | 🔧 全部 9 本（成书均早于 2018） |
| 9 | 🔧 "现在做数据同步还是用 LogMiner / 闪回" | 现状：**Debezium**（≈13152★）+ GoldenGate + Oracle 自身的 CDC 是主流；使用它们的**前提是打开 supplemental logging**，这属于本轮讲的内容 | 🔧 全部 9 本未覆盖 CDC 生态 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`03-存储结构-表空间与段区块.md`](03-存储结构-表空间与段区块.md)（undo 表空间与 redo 日志文件的物理落点）
- **下一章**：[`05-索引与约束.md`](05-索引与约束.md)（DML 越多，redo 与 undo 越大，索引会让它翻倍）
- **强相关（理论）**：[`数据库系统概念6/26-高级事务处理.md`](../数据库系统概念6/26-高级事务处理.md)（ARIES、WAL、组提交、长事务与补偿事务；本章 1.4 的表与之互补）
- **强相关（理论）**：[`数据库系统概念6/15-并发控制.md`](../数据库系统概念6/15-并发控制.md)（多版本协议、快照隔离、写偏斜；Oracle 的默认隔离级别也逃不开 SI 的写偏斜）
- **其他书笔记**：[`book/mysql/21-事务隔离级别与MVCC.md`](../mysql/21-事务隔离级别与MVCC.md)（InnoDB 的 MVCC 与 Oracle 的对比）
- **强相关**：[`12-备份恢复容灾与DataGuard.md`](12-备份恢复容灾与DataGuard.md)（本章的"恢复"是那一章的方法论来源：实例恢复 vs 介质恢复）
- **强相关**：[`07-SQL性能诊断与调优实践.md`](07-SQL性能诊断与调优实践.md)（`log file sync` 等待事件的完整归因链）
- **其他书**：《DBA攻坚指南》讲"用 undo 闪回查询 + LogMiner 做数据追溯与恢复"的实战步骤，是本章 1.3 的运维化延伸；《高并发 Oracle 数据库系统的架构与设计》从容灾与高并发角度讲 Data Guard。
