# 第 19 章 说过的话就一定要做到——redo 日志

> 原书说明：标题为「说过的话就一定要做到——redo日志」，基于 MySQL 5.7.22 撰写。本文件按其思路展开 **mtr / LSN / write-ahead / checkpoint / 崩溃恢复**，并补齐 5.7/8.0 的演进与 2020 年之后必须补的**无锁 log buffer、redo 写线程、动态容量、Clone 应用 redo**。

## 本章地图

> 一句话：**redo 是「说过的话」的账本——先把账记下来（write-ahead），再慢慢改地；LSN 是这条账本上的页码，checkpoint 是「已落地到哪一页」的水位线，崩溃恢复就是「把水位之后的所有账重做一遍」。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 19.1 为什么需要 redo | 内存易失、页修改在内存 | WAL：先记日志，后改页 |
| 19.2 mtr（最小事务） | 页改动 + redo 记录的原子单位 | 一个 mtr 要么全生效、要么全不生效 |
| 19.3 LSN：日志上的时间轴 | 单调递增字节偏移；日志序号 vs flush 序号 | **LSN 就是 InnoDB 的时间轴** |
| 19.4 写前日志与落盘档位 | `innodb_flush_log_at_trx_commit`、log buffer | durable 是有档位的 |
| 19.5 checkpoint：水位线 | 推进机制、redo 写满会怎样 | checkpoint 不推进 = 写入卡死 |
| 19.6 崩溃恢复的四步 | 分析 → 重做 → 回滚 → 收尾 | 「重做历史 + 回滚未提交」 |
| 19.7 组提交与多线程 redo | 一次 fsync 服务一批事务 | 吞吐的胜负手 |
| 19.8 🔧 2026 视角 | 无锁 log buffer、redo 写线程组、动态容量、Clone 应用 redo | 5.7 的单线程 redo 模型已被重写 |
| 19.9 三套日志的协作全景 | binlog / redo / undo 的分工、内部 XA、组提交、`sync_binlog` × `innodb_flush_log_at_trx_commit`、容量与 PITR | redo 只管崩溃恢复，复制与 PITR 只能靠 binlog，undo 还要给 MVCC 让路 |
| 19.10 🔧 2026 视角二 | 无锁 log buffer、redo 写线程组、动态容量、Clone 应用 redo | 5.7 的单线程 redo 模型已被重写 |

## 核心精讲

> **教学示意，不参与构建。** 下文结构与 `--` 片段仅用于说明 redo 的组织方式，**未在本机编译、未启动任何 MySQL 实例执行**；具体数值随版本变化。

### 19.1 为什么需要 redo

- **矛盾**：修改在 Buffer Pool 里做（快，但掉电即失）；直接写回磁盘（慢，且随机 IO）。
- **WAL（Write-Ahead Logging）**：**任何页的修改，必须先写 redo，才允许改内存页**。
  ```text
  改页前：把「第 4 号表第 7 号页，把 a 从 1 改成 2」写进 redo（并落盘）
  然后  ：在 Buffer Pool 里把该页改成新值（脏页）
  之后  ：后台择机刷盘
  ```
- 等等：**为什么页坏了 redo 也能修？** 因为 redo 记的是「物理页改动的增量」，恢复时按顺序**重放这些改动**，就能把页重建出来 —— 但前提是**页本身没有损坏**（这就是 doublewrite 存在的原因，见 `17-调节磁盘和CPU的矛盾.md`）。
- redo 是**物理**日志（行级物理日志的近似），undo 才是逻辑日志 —— 这个区分是理解崩溃恢复顺序的关键。

### 19.2 mtr（mini-transaction）：redo 的原子单位

- **定义**：一次「页访问 + 修改」的最小单位。一个事务包含多个 mtr；一个 B+ 树节点的分裂/合并是一个 mtr。
- **两阶段提交**（教学示意，不参与构建）：
  ```text
  mtr begin：
      修改页 A（在 Buffer Pool）
      修改页 B（B+ 树分裂时必然发生）
      生成若干条 redo 记录，写入 log buffer
  mtr commit（策略 = mtr 级 mini-transaction 提交）：
      - 若在「普通模式」：把该 mtr 的 redo 写入 log buffer 并标记 mtr 边界
      - 若在「崩溃恢复需要的模式」：强制把 redo 刷盘
  ```
- **为什么需要 mtr 边界**：崩溃恢复必须知道「页 A 和页 B 的这次改动是同时发生的」，否则会重放出**半棵 B+ 树**。mtr 的边界标记（单条 redo 记录可以同时覆盖多个页的修改）就是给恢复器的「事务性气味」。
- **两种刷盘策略**：
  - **普通提交**：redo 留在 log buffer，由后台线程择机刷盘 —— 吞吐高。
  - **强制提交**（如某些 DDL、复制相关场景）：该 mtr 的 redo 立刻 fsync —— 延迟高但保证无丢失窗口。

### 19.3 LSN：日志上的坐标

- **LSN（Log Sequence Number）**：redo 空间中**单调递增的字节偏移量**。
  ```text
  log 文件0: [ 0 -------- 4MB -------- 8MB -> ][ 循环回 0 处 ]
                 ↑ flush_lsn（已落盘）      ↑ current_lsn（已写入）
  ```
- 几个容易混淆的序号（教学示意，不参与构建）：
  | 序号 | 含义 |
  | --- | --- |
  | `log_sequence_number`（LWN / current LSN） | 已产生到的日志位置 |
  | `log_flushed_to_disk_lsn` | 已 fsync 到磁盘的位置 |
  | `last_checkpoint_lsn` | 上次 checkpoint 记录的位置（决定 redo 需要保留多少） |
  | 页头里的 `FIL_PAGE_LSN` | 该页最后被修改时的 LSN |
- **一个经典推论**：如果 `页头 LSN > 已刷盘的 LSN`，说明这个页的改动**日志已落盘、页本身还没落盘**，恢复时必须重做；反之则无需重做。
- 查看方式（教学示意，不参与构建，需实际连接实例）：`SHOW ENGINE INNODB STATUS` 的 `LOG` 段，或 8.0 的 `performance_schema` / `SHOW GLOBAL STATUS` 里以 `Innodb_lsn` 开头的若干项。

### 19.4 写前日志的落盘档位

- **log buffer**：一块固定大小的内存（默认 16MB，8.0 可配），事务的 redo 先写这里，再由后台线程批量刷盘。
- **落盘时机由 `innodb_flush_log_at_trx_commit` 决定**（详见 `X2-日志系统专题.md`）：

  | 值 | 提交时行为 | 掉电损失 |
  | --- | --- | --- |
  | 1（默认） | 写 log buffer + fsync | 无 |
  | 2 | 写 log buffer + 写 OS cache，每秒 fsync | ≤1 秒 |
  | 0 | 每秒写盘 + fsync | ≤1 秒 |

- 另外，`innodb_log_buffer_size` 决定单次能缓冲多少 redo；**大事务（一次改很多页）会突破 log buffer**，导致中途强制刷盘。

### 19.5 checkpoint：让 redo 能循环起来

- **为什么需要**：redo 文件是固定大小、循环覆盖的。它只保留「checkpoint 之后」的历史。若 checkpoint 不推进，redo 就被写满，**数据库无法继续写入**（表现为写入卡死或刷盘加剧）。
- **推进条件**：checkpoint LSN 之后的**所有脏页**都必须已落盘。
- **推进太慢的原因**：
  - 刷盘线程不够（`innodb_page_cleaners`）；
  - `innodb_io_capacity` 设得太低；
  - 有大量长事务导致无法回收 undo/页；
  - Buffer Pool 里脏页太多（接近 `innodb_max_dirty_pages_pct`）。
- 症状识别：`SHOW ENGINE INNODB STATUS` 中 `Log sequence number` 与 `Last checkpoint at` 差距持续拉大 → **redo 空间不足的前兆**。
- 🔧 **解决手段（8.0）**：`innodb_redo_log_capacity` 可以在线调大 redo 容量，而不必像 5.7 那样改 `innodb_log_file_size` 并重启。

### 19.6 崩溃恢复的四步（教学示意，不参与构建）

```text
① 分析阶段（analysis）
   从最后一个 checkpoint 处扫描 redo，重建「脏页集合」与「未提交事务集合」
② 重做阶段（redo / repeating history）
   按顺序重放 redo 记录，把 checkpoint 之后的所有改动重做一遍
   —— 这一步「不问缘由」，所以叫 repeating history
③ 回滚阶段（undo / as-needed）
   对 ② 中「未提交事务」改过的页，用 undo 做回滚
④ 收尾
   更新 checkpoint 水位；清除临时表等；打开只读/读写
```

- **为什么第 ② 步不需要「知道原因」**：这正是 ARIES 的核心思想 —— **先重复历史，再按需回滚未提交事务**。原书把它讲成「说过的话一定要做到」，而这一步刚好相反：**不管当时为什么改，先照做，再把没commit 的撤销**。
- 与 binlog 的关系：redo 里「prepare 但未 commit」的事务，要回查 binlog 决定提交还是回滚（内部 XA，见 `X2-日志系统专题.md` 13.5）。
- 恢复耗时与「最后一次 checkpoint 距今多久」强相关 —— 这正是**定期备份 + PITR 训练**的价值。

### 19.7 组提交：一次 fsync 服务一批事务

- **问题**：每个事务都 fsync → fsync 次数 = 事务数 → QPS 被 IOPS 锁死。
- **解法**：把同一批次的事务 redo 拼在一起，一次写盘一次 fsync（详见 `X2-日志系统专题.md` 13.6）。
  ```text
  事务 T1 ┐
  事务 T2 ├─→ 同一个 log buffer 片段 → 一次 write → 一次 fsync → 各自标记提交
  事务 T3 ┘
  ```
- 收益：理论上把「事务吞吐」与「磁盘 fsync 频率」解耦。
- 🔧 现代形态（8.0+）：
  - **无锁 log buffer 写入**：多事务并发写 log buffer 不再需要互斥锁竞争，靠原子操作；
  - **独立的 redo 写线程组**（`innodb_log_writer_threads` 相关机制）：把「写 log buffer」与「刷盘」解耦到不同线程，减少用户线程被卡在 IO 上的时间。

### 19.9 三套日志的协作全景（教学示意，不参与构建）

> 原书没有一章把 binlog / redo / undo 放在一处；本小节按「redo 视角」把它们的关系补齐。
> 完整展开见 [X2-日志系统专题.md](X2-日志系统专题.md)。以下示意与片段**均未在本机编译、未启动实例执行**。

**(1) 谁管什么：一张对照表**

| 维度 | binlog（归档日志） | redo log（重做日志） | undo log（回滚日志） |
| --- | --- | --- | --- |
| 所属层 | **Server 层**（与引擎无关） | InnoDB 引擎层 | InnoDB 引擎层 |
| 内容 | 逻辑/半逻辑的「语句或行镜像」序列 | **物理页改动的增量**（含 LSN） | **逻辑**撤销语句 + 版本链节点 |
| 生命周期 | 滚动文件，可长期保留 | **循环覆盖写**，只覆盖 checkpoint 之后的窗口 | 提交后由 purge 在**最老活跃 read view 之后**回收 |
| 用途 | **复制、PITR、审计** | **崩溃恢复**、页修复 | **回滚**、一致性读（MVCC） |
| 谁消费 | 从库 IO/SQL 线程、`mysqlbinlog` | 崩溃恢复、克隆、Buffer Pool 预热 | `ROLLBACK`、快照读 |

三条硬结论：**只靠 redo 做不了 PITR**（它是循环的）；**只靠 binlog 做不了崩溃恢复**（它是逻辑的）；
**redo 是物理日志、undo 才是逻辑日志**，这个区分决定了恢复器重放的是页改动而非 SQL。

**(2) 内部 XA（两阶段提交）：redo 与 binlog 的原子性协调**

```text
1) InnoDB prepare：写 redo（含 prepare 标记），按 innodb_flush_log_at_trx_commit 决定是否 fsync
2) 写 binlog（cache → 文件，按 sync_binlog 决定是否 fsync）
3) InnoDB commit：写 redo commit 记录、释放锁、标记事务结束
```
- 崩溃发生在 ①与③之间时，恢复器回查 binlog：**有对应记录则补提交，没有则回滚**。
- 也就是说，**binlog 是协调者，InnoDB 是参与者** —— 这正是 19.6 里「prepare 但未 commit」那个判断的由来。
- 旁证：关掉 binlog 能明显提速，正是少了一次这种 prepare/写盘协调。

**(3) 组提交：一次 fsync 服务一批事务**

- 问题：每事务各 fsync 一次 → fsync 次数 = 事务数 → QPS 被磁盘 IOPS 锁死。
- 解法：一批事务**共用一个 fsync**。
  - **binlog 组提交**：lead 事务收集同批次 followers，统一写盘统一 fsync；5.7 起拆成 flush / sync / commit 三阶段，**各阶段可有不同的事务集合**，并发度大幅提升。
  - **redo 组提交**：同批次事务的 redo 一起写盘（见 19.7 的示意）。
- 关键实现细节：**组提交依赖「提前解锁」（early lock release）**——prepare 后就放行锁，才有足够多事务挤进同一批。
- 🔧 相关参数：`binlog_group_commit_sync_delay`（主动延迟攒事务）、`binlog_group_commit_sync_no_delay_count`（攒够就不等）。
  **这是唯一一种「主动加延迟换吞吐」的手段**，常用于批量导入与从库。

**(4) 持久性矩阵：`sync_binlog` × `innodb_flush_log_at_trx_commit`**

| `sync_binlog` | `innodb_flush_log_at_trx_commit` | 持久性 | 典型场景 |
| --- | --- | --- | --- |
| 1 | 1 | 最强（宕机不丢已提交） | 金融/订单主库 |
| 1 | 2 | 掉电可能丢最近 1 秒已提交事务 | 可接受抖动的业务库 |
| 0 | 0 | 最弱（崩溃丢 1 秒） | 只读从库/离线分析 |
| N>1 | 1 | 折中 | 老版本常见配置 |

> 这是**配置学结论而非实测数据**；实际行为还受 `innodb_flush_method`（是否 `O_DIRECT`）、写缓存与 RAID 电池影响。

**(5) 容量与磁盘规划（呼应 08 的数据目录）**

| 日志 | 容量来源 | 满了会怎样 |
| --- | --- | --- |
| binlog | `max_binlog_size` + 保留策略 | 到期自动清理（`binlog_expire_logs_seconds`）；磁盘满则写入失败 |
| redo | 🔧 `innodb_redo_log_capacity`（8.0.11 起可在线调） | checkpoint 不推进 → **写入卡死** |
| undo | 回滚段 + 历史链表长度（由 purge 决定） | 长事务卡 purge → 文件撑大 |

直觉：**redo 太小** → 高频 checkpoint → 写入周期性抖动；**redo 太大** → 崩溃恢复窗口变长、RTO 变差；
**undo 膨胀**要先把最老活跃事务解决掉，undo 文件不会立刻缩小。

**(6) 日志能力 vs 恢复目标**

| 恢复目标 | 需要什么 |
| --- | --- |
| 掉电/崩溃 | redo + doublewrite（崩溃恢复自动完成） |
| 误删数据回到 5 分钟前 | 备份 + binlog 回放 |
| 主库损坏换机器 | 备份 + 克隆/GTID 追平 |
| 只要某几行 | `mysqlbinlog` 解析到行级（代价最高） |

一句话：**没有经过「从备份恢复」演练的备份等于没有备份**；PITR 演练同时验证了 binlog 是否完整、时区与 GTID 是否一致。

## 版本演进

| 版本 | redo 相关变化 |
| --- | --- |
| 5.5 | redo 文件固定 2×48MB（2 个文件 ×48MB），写满即推进 checkpoint |
| 5.6 | `innodb_log_files_in_group` / `innodb_log_file_size` 可配；undo 独立表空间 |
| 5.7 | 组提交三阶段；`innodb_undo_log_truncate`；log buffer 相关参数更细 |
| 8.0.11 | **`innodb_redo_log_capacity` 取代旧参数，容量可在线调节** |
| 🔧 8.0.x | 无锁 log buffer 写入；redo 写线程组；原子写（8.0.5）可省 doublewrite |
| 🔧 8.0.17 | Clone Plugin：**应用 redo** 完成分布式恢复 |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Haerder & Reuter, *Principles of Transaction-Oriented Recovery* | ACM Computing Surveys 15(4), 1983 | WAL 与恢复三原则 |
| Mohan et al., *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks* | SIGMOD 1992 | **重复历史 + 按需 undo**；mtr 与脏页集合 |
| Agrawal, Daly, Farber, *Durability of Multi-Level Transactions...*（及 ARIES 系列的 *Buffer Management in ARIES*） | VLDB 1990/1991 | ARIES 的页管理与恢复细节 |
| O'Neil et al., *The Log-Structured Merge-Tree*（LSM） | Acta Informatica 1996 | 日志结构化的另一条路线（与 redo 的取舍对照） |
| Gray & Reuter, *Transaction Processing: Concepts and Techniques* | Morgan Kaufmann 1993 | LSN、checkpoint、WAL 的标准表述 |
| MySQL 官方文档：InnoDB Redo Log / CHECKPOINT / Clone | dev.mysql.com | LSN 语义、checkpoint 行为、动态容量的权威口径 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：**持久内存（PMem）下的 redo**——把 redo 直接写在持久内存上可省一次拷贝与 fsync；**存算分离下的 redo 下沉**（Aurora 把 redo 送到存储层由存储引擎自己重放，MySQL 8.0 的 Clone 已是「redo 作为恢复载体」的现成样本）；**组提交与批量持久化**（RocksDB 的 *Durability for Free*, OSDI 2016）；**Aether: A Scalable Approach to Logging**（PVLDB 2010）提出把日志按「写入者组」聚合，思想与 InnoDB 组提交同源。
- **工业界开源**（star 数 2026-09-25 通过 `gh api` 实测）：
  - `mysql/mysql-server`（≈12.4k★）：redo 实现 `storage/innobase/log/log0log.cc`，mtr `log0mtr.cc`，恢复 `log0recv.cc`；动态容量在 `log0log.cc` 的 `innodb_redo_log_capacity` 解析处。
  - `facebook/mysql-8.0`（≈115★）：Group Replication、并行复制与 redo 落盘路径上的工程优化。
  - `percona/percona-server`（≈1.3k★）：较早支持大 redo 与 sekira 相关调优经验。
  - `pingcap/tidb`（≈40.6k★）与 `cockroachdb/cockroach`（≈32.5k★）：raft log 即 redo，崩溃恢复与共识重启合二为一。
  - `postgres/postgres`（≈22.2k★）：WAL + `checkpoint_timeout` / `max_wal_size` 的 checkpoint 管理，与 InnoDB 的 checkpoint 机制是可直接对照的设计。
  - `clickhouse/clickhouse`（≈50.1k★）：几乎不用 WAL（靠 mesh 复制 + 批量落盘），是「redo 不是必需品」的反例。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「redo 是把 SQL 语句记下来，重放一遍就恢复了」 | redo 是**物理页增量**；重做的是「页改动」而不是 SQL |
| 2 | 「提交成功 = 数据已在磁盘」 | 提交成功只保证 **redo 已落盘**（或已进 OS cache），页可能还在内存 |
| 3 | 「redo 越大越好」 | 太大 → 崩溃恢复极慢；太小 → 频繁 checkpoint 造成写入抖动（对 MySQL 8.0 用 `innodb_redo_log_capacity`） |
| 4 | 「崩溃恢复是把所有 redo 从头重放」 | 只重放 **checkpoint 之后**的部分；checkpoint 越新恢复越快 |
| 5 | 「恢复时先回滚再重做」 | ARIES 的顺序是 **重做（重复历史）→ 再回滚未提交** |
| 6 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有** `innodb_redo_log_capacity` 动态容量（8.0.11，原书用「重启改 `innodb_log_file_size`」）、**没有**无锁 log buffer 与 redo 写线程组、**没有** Clone Plugin 应用 redo（8.0.17） |
| 7 | 🔧 **本书未覆盖** | **组提交在 redo 侧的具体实现**原书只在「两阶段提交」里一笔带过；2026 的调优题（"如何让 QPS 从 2k 到 8k"）答案绝大多数就在这里 |
| 8 | 🔧 **本书未覆盖** | **三套日志的协作全景**（binlog/redo/undo 的分工与容量规划、`sync_binlog` × `innodb_flush_log_at_trx_commit` 矩阵、备份/PITR 与日志的关系）原书分散在 13/19/20 章且未合观；见本文件 19.9 |
| 9 | 「binlog 和 redo 都能做恢复」 | 只靠 redo 做不了 PITR（循环覆盖），只靠 binlog 做不了崩溃恢复（逻辑日志） |
| 10 | 「事务提交后 undo 立刻没用了」 | 还有最老 read view 可能读它；purge 受最老活跃事务限制（长事务 → undo 膨胀） |

## 与其他章 / 其他书的联系

- → `20-undo日志.md`：redo 重做之后由 undo 回滚未提交事务，二者是恢复的两半。
- → `X2-日志系统专题.md`：binlog 与 redo 的两阶段提交、组提交、binlog 三种格式与 GTID。
- → `18-事务的庐山真面目.md`、`21-事务隔离级别与MVCC.md`：持久性与隔离性承诺的兑现者。
- → `17-调节磁盘和CPU的矛盾.md`：doublewrite 与 checkpoint 的推进依赖刷盘能力。
- → `18-事务的庐山真面目.md`：持久性承诺的兑现者。
- → `21-事务隔离级别与MVCC.md`：版本链的清理受 undo purge 限制，而 purge 又受最老 read view 限制。
- → [16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)（若存在）：ARIES 的完整论证。
- → [26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)：组提交与 early lock release 的性能史。
