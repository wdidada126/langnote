# InnoDB 的内存结构——change buffer、自适应哈希索引与后台线程

> **原书位置**：主题对应第 11 章附近对「change buffer / AHI / 内存结构」的介绍，以及第 2、17 章的内存参数；
> 本文件名沿用任务映射表 `11-InnoDB内存结构.md`。原书基于 **MySQL 5.7.22**。
>
> **一句话**：InnoDB 的内存由「**一块大池 + 若干专项缓冲 + 一组后台线程**」组成；
> 其中 **change buffer 把随机写变成缓冲写、AHI 把 B+ 树查找变成哈希查找**，
> 这两个结构的存在，让 InnoDB 在「写多读少」与「点查为主」两类负载上都有明显优势。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 内存都花在哪 | Buffer Pool（最大）+ change buffer + log buffer + AHI + 字典缓存 + 锁系统 + 线程栈 | 只看 `innodb_buffer_pool_size` 会漏掉一截真实内存 |
| 11.2 change buffer（原 insert buffer） | 非唯一二级索引的写操作先在内存里排队，等目标页「被用到」时再合并 | 把随机 I/O 变成「顺路修一下」，代价是崩溃后恢复变久 |
| 11.3 change buffer 的三个前提 | ① 二级索引 ② 非唯一（唯一需立即查重）③ 目标页不在池时才缓冲 | 满足不了就要真实读页，反而更慢 |
| 11.4 自适应哈希索引（AHI） | 对「频繁访问的 B+ 树页」建哈希索引，把树查找降为一次哈希 | 「自适应」= 引擎自己判断热点，无需人工干预 |
| 11.5 redo log buffer | 事务写入先落内存日志缓冲，按组提交批量 fsync | 组提交把「每个事务一次 fsync」变成「一批一次」 |
| 11.6 后台线程 | master/IO/Purge/Cleaner 等线程各自负责刷脏、purge、合并 change buffer | 它们沉默时系统很顺，一旦积压就会「连环暴雷」 |
| 11.7 purge 与 undo 回收 | 清理由 MVCC 不再需要的 undo 版本；长事务会让 purge 停摆 | 长事务 → undo 膨胀 → 磁盘涨，是经典故障 |
| 11.8 🔧 8.0+ 的变化 | change buffer 默认占池 1/4、redo 的 log buffer 与子线程组、undo 独立表空间、`innodb_dedicated_server` | 默认值与启动方式在 2020 年之后都有调整 |

## 核心精讲

> 以下均为**教学示意，不参与构建**：本目录不搭建真实实例，示例只用于对齐概念。

### 1. 内存版图（教学示意，不参与构建）

```
InnoDB 进程内存 ≈
  ├─ Buffer Pool        （最大头，含数据页/索引页/change buffer 页）
  ├─ log buffer         （redo 的暂存区，默认 16MB 量级）
  ├─ AHI 结构           （基于 Buffer Pool 里的页建的哈希索引）
  ├─ 字典缓存 / 表定义对象
  ├─ 锁系统调用内存（行锁对象、等待结构）
  └─ 各种线程栈与临时结构
```

🔧 实务建议：**规划内存时要给上述所有项留出余量**，只按 buffer pool 估会让实例 OOM 或触发 swap。

### 2. change buffer 的工作方式（教学示意，不参与构建）

```
INSERT/UPDATE 影响非唯一二级索引，且目标索引页不在 Buffer Pool
   → 不立即读盘，而是把「这次修改」记在 change buffer 里

之后三种情况触发「合并（merge）」：
  ① 那个二级索引页后来被读进 Buffer Pool → 顺路合并（最常见）
  ② change buffer 的空间达到上限 → 主动合并一部分
  ③ 后台线程周期性合并
合并时：把同一索引页上的多次修改合并成一次页写入 → 随机写被摊薄
```

为什么「唯一索引用不上」：**唯一性检查必须立刻看到全量数据**，
如果改动先落在缓冲区里，就无法保证「另一个会话不会插进同一个值」。

### 3. change buffer 的代价（教学示意，不参与构建）

| 收益 | 代价 |
| --- | --- |
| 写吞吐明显提升（随机变顺序） | 崩溃后恢复时间变长（要合并未落盘的缓冲） |
| 减少写入时的读 I/O | 写密集场景下 change buffer 会吃掉 1/4 的池内存 |
| 大批量导入受益最大 | 若之后无人读这些索引，收益可能抵消不掉代价 |

工程判断：**「写多读少 + 二级索引多」的表最适合**；「几乎只读的报表表」收益不大。

### 4. AHI 的工作方式（教学示意，不参与构建）

```
B+ 树页被反复以「相同键值范围」访问
   → InnoDB 为该页（或该页上的某个键值区间）建立哈希索引
   → 之后的等值查询可以直接一次哈希定位，省掉树下降的几层
```

三个要点：
1. AHI **只在内存中**，不落盘，重启即丢；
2. AHI 是**等值友好、范围不友好**（范围查询仍然走 B+ 树）；
3. AHI 的维护本身有 CPU 成本；写入密集时可通过参数关闭（以官方文档为准）。

### 5. redo log buffer 与组提交（教学示意，不参与构建）

```
事务提交 → 写 redo 到 log buffer（内存）→ 按组提交批量 fsync 到 redo 文件
                                            ↑
                        一批事务共享一次 fsync，代价从 O(n) 降到 O(1) 的 I/O 次数
```

这解释了两个常见现象：
- **「小事务 QPS 有上限」**——上限往往不是 CPU，而是 fsync 次数与组提交的批大小；
- **事务越大，`innodb_flush_log_at_trx_commit=2` 越危险**——丢的是最近若干秒的提交。

### 6. 后台线程与「为什么会连环暴雷」（教学示意，不参与构建）

```
master / IO 线程   ：刷脏、合并 change buffer、checkpoint 推进
purge 线程         ：清理不再需要的 undo 版本（受最老活跃 ReadView 限制）
page cleaner       ：按脏页比例与 IO 能力自适应刷脏

链条示例：
   一个超长事务（或一次性大 select）→ 最老 ReadView 迟迟不前进 → purge 停摆
   → undo/历史版本堆积 → 表空间膨胀 → 更慢 → 下一个故障
```

这类问题在监控上表现为「磁盘空间涨、延迟涨，但 QPS 没变」，
排查时第一步通常是查最老活跃事务（`information_schema.innodb_trx`）。

### 6.1 内存规划的一个估算思路（教学示意，不参与构建）

```
innodb_buffer_pool_size = 64GB 时，进程总内存大致还要加上：
  log buffer             ~16MB
  AHI 结构               视热点而定，通常几百 MB 到 1–2GB
  字典缓存 / 表定义对象    每表几十 KB 到数百 KB × 表数
  行锁与等待结构          取决于并发与锁数量
  线程栈                 thread_stack(默认 256KB 量级) × 连接数
  ────────────────────────────────
  合计 ≈ buffer pool 的 5%–10%（连接数高时线程栈占比会上升）
```

结论：**「只给 buffer pool 留内存」的做法在连接数上千的实例上会出事**；
`innodb_dedicated_server` 🔧（8.0+）能按机器规格自动分配，但要与容器内存 limit 一起评估。

## 版本演进

| 版本 | 关键变化 |
| --- | --- |
| **5.7（原书基线）** | change buffer 上限默认 25% 池内存；AHI 默认开；`innodb_log_buffer_size` 默认 16MB；undo 在系统表空间 |
| **8.0** | 🔧 **undo 表空间默认独立**；🔧 change buffer 相关参数与默认值调整（默认 `innodb_change_buffer_max_size=25`）；🔧 `innodb_dedicated_server` 可自动设置 log buffer 等；🔧 redo log 写入路径与后台线程重构（log writer/log flusher 线程组，逐版本核对文档）；🔧 移除部分旧线程 |
| **8.4 LTS** | 🔧 内存分配与后台线程默认值继续调整；`innodb_dedicated_server` 的语义更符合「专供 InnoDB」 |
| **9.x** | 🔧 与 HeatWave 共存下的内存划分策略继续演进 |
| **MariaDB / PostgreSQL 对照** | MariaDB 用 **Innodb 相关插件 + Aria**，AHI 与 change buffer 的实现细节不同；PostgreSQL 无 AHI，靠共享缓冲 + 内核缓存；其后台「autovacuum」对应的正是 InnoDB 的 purge 角色 |

## 经典论文与原始文献

| 来源 | 作者 / 出处 | 与本主题的关系 |
| --- | --- | --- |
| The Log-Structured Merge-Tree | O'Neil, Cheng, Gouda, Gray，*Acta Informatica* 33(4), 1996 | 「先在内存/web 层缓冲写入、到量再与磁盘合并」正是 change buffer 的学术同构 |
| The Bw-Tree | Levandoski et al.，*SIGMOD* 2013 | 无锁 B+ 树与页级乐观并发，可与 AHI 的「加速层」思路对照 |
| A Fast File System for UNIX | McKus et al.，*ACM TOCS* 2(3), 1984 | 顺序化写与日志结构的经典论证 |
| MySQL 官方文档：Change Buffer / Adaptive Hash Index / InnoDB Startup Options | MySQL 官方文档 | 适用条件、参数与版本差异的权威依据 |
| MySQL 官方文档：InnoDB Multi-Versioning（purge 与历史链表） | MySQL 官方文档 | purge 受「最老活跃事务」限制的解释 |
| InnoDB 源码 `storage/innobase/buf/`、`log/`、`ibuf/` | `mysql/mysql-server`（≈12.4k★） | change buffer 实现在 `ibuf0ibuf.cc`，AHI 在 `buf0cci.cc`/`ha0ha.c` |

> 说明：本次核查中**没有找到可靠的「Insert Buffering in InnoDB」学术论文**，
> 因此这里只写机制与官方文档依据，不做论文杜撰。

## 近年研究与工业界开源实践（2015–2026）

- **`mysql/mysql-server`（2026-09 实测 ≈12.4k★）**：change buffer 的实现在
  `storage/innobase/ibuf/ibuf0ibuf.cc`，AHI 在 `storage/innobase/hash/`；
  redo 的日志线程组与组提交在 8.0 之后有明显重构，可通过 `performance_schema` 观察等待。
- **`facebook/rocksdb`（≈32.1k★）**：把「缓冲写 + 合并」做到极致（memtable + compaction），
  是 change buffer 思想在 LSM 路线上的完整形态；读放大与空间放大是其代价。
- **`clickhouse/clickhouse`（≈50.1k★）**：写路径几乎不做「页缓存」，而是 parts 的合并，
  与 InnoDB 的「合并式写」同构但粒度更大。
- **`pingcap/tidb`（≈40.6k★）**：底层 RocksDB 承担合并，TiDB 层用「大事务/小事务」策略减少写放大，
  可对照理解「写路径上到底该不该延迟落盘」。
- **运维要点**：AHI 与 change buffer 都不宜「一直开着不管」；
  在纯写负载下可通过 `innodb_adaptive_hash_index=OFF` 与调整 change buffer 上限换取稳定延迟，
  具体以对应版本的官方文档为准。

## 常见误区与本书需修正之处

| # | 常见误区 | 修正（🔧 = 原书出版时未覆盖） |
| --- | --- | --- |
| 1 | 「change buffer 就是缓存」 | 它是**延迟写入的修改集合**，不是读取缓存 |
| 2 | 「唯一索引也能用 change buffer」 | 不能：唯一性必须立即校验 |
| 3 | 「AHI 越多越好」 | AHI 是估出来的，维护有成本，且只对等值访问友好 |
| 4 | 「purge 只是清理」 | purge 受 **最老活跃事务**限制，长事务会让它停摆并导致膨胀 |
| 5 | 「文件大小不变说明没堆积」 | 8.0 起 undo 在独立表空间，膨胀表现在 `undo_*` 文件上 |
| 6 | 🔧 本书未覆盖 | 原书基于 5.7.22，**未覆盖** undo 表空间独立化、redo 日志线程组、`innodb_dedicated_server` 的内存自动分配，以及 8.4 的默认值变化 |
| 7 | 「change buffer 是永久的」 | 它只是内存/写路径上的缓冲，数据最终必须合并进索引页；崩溃后仍要合并 |
| 8 | 「AHI 不影响正确性」 | 正确，但它只影响性能；关掉它查询会变慢但结果一致 |

## 与其他章 / 其他书的联系

- 本册：**02-Buffer-Pool.md**（内存主体）、**03-数据页长什么样.md**、**05-InnoDB数据页结构.md**（脏页刷回与 doublewrite）、
  **08-MySQL的数据目录.md**（`ibdata1` / undo 文件）、**10-InnoDB的表结构.md**（字典缓存位置）。
- 他册：《数据库系统概念（第6版）》[16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)（组提交、WAL、purge 的理论版）、
  [15-并发控制.md](../数据库系统概念6/15-并发控制.md)（行锁与闩的两层结构）、
  [26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)（日志与 checkpoint 的开销剖析）；
  缓冲与缓存设计可对照《深入理解计算机系统》与《多处理器编程的艺术（2）》相关章节。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
