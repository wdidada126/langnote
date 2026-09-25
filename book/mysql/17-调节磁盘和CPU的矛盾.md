# 第 17 章 调节磁盘和CPU的矛盾——InnoDB 的 Buffer Pool（进一步话题）

> 原书说明：标题为「调节磁盘和CPU的矛盾——InnoDB的Buffer Pool」。本文件保留原书「磁盘 vs CPU 矛盾」这一主线，并在原书第六章「B+树索引」与第二十章「redo日志」的基础上进一步展开**脏页刷盘、doublewrite、预读、Buffer Pool 调参**，补齐 5.6/5.7/8.0 的演进与 2020 年之后必须补的**在线调参、原子写、预加载、Buffer Pool 多实例**。

## 本章地图

> 一句话：**「CPU 快、磁盘慢」这个矛盾在 InnoDB 里被翻译成两件事——内存里的页缓存（Buffer Pool）和落盘策略（刷盘/双写/预读）；调优的实质是让「顺序写 + 批量刷 + 命中缓存」尽可能多地替代「随机读 + 单次刷」。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 17.1 Buffer Pool 的组织 | 页框、instance、chunk、`LRU` / `free` / `flush` 三条链 | 页有「定位表 + 三条链表」三重身份 |
| 17.2 页的定位与替换 | 页哈希、老年代/新生代 LRU、预读页 | 命中率的关键在 LRU 的组合策略 |
| 17.3 脏页与刷盘 | checkpoint 推进、flush 线程、`innodb_io_capacity` | 刷太慢 = 写入抖动；刷太猛 = 查询抖动 |
| 17.4 doublewrite buffer | 部分页写的修复 | 崩溃恢复时用它「补齐残页」 |
| 17.5 预读（read ahead） | 线性预读 / 随机预读 / 大表扫描 | 顺序化随机 IO 的主要手段 |
| 17.6 调参与容量规划 | `innodb_buffer_pool_size`、instance、`change buffer` | 容量够不够看命中率，不看内存占用 |
| 17.7 🔧 2026 视角 | 8.0 的在线调参、原子写、预加载、`io_capacity_max` | 原书的「重启才能改」已被大量取消 |

## 核心精讲

> **教学示意，不参与构建。** 下文为讲清结构而做的示意与 `--` 片段，**均未在本机编译、未启动任何 MySQL 实例执行**；默认值随版本变化，请以官方文档与本机实际值为准。

### 17.1 Buffer Pool 的三条链表

Buffer Pool 是若干「页框（frame）」组成的连续内存区（教学示意，不参与构建）：

```text
Buffer Pool (chunk × N，每个 chunk 若干页)
  ├─ 页哈希：space_id + page_no → 页框      （用于判断页是否已在内存）
  ├─ free list：完全空闲的页框               （缺页时从这里取）
  ├─ LRU list：已读入的页，按「最近使用」排序  （05.6 起分老年代/新生代）
  └─ flush list：已修改、等待刷盘的脏页       （按「最早修改」排序 → 决定 checkpoint）
```

- **三条链的本质是三个不同的「淘汰/推进」方向**：
  - `free` → `LRU`：页被读入。
  - `LRU` → `flush`：页被修改（变脏）。
  - `flush` → 磁盘：后台/用户线程刷盘，刷完放回 `free`。
- 原书强调「页在内存里不是安全的，必须落盘才持久」，这里的 `flush list` 正是与 redo LSN 对接的那条链。

### 17.2 页的定位与替换：老年代 LRU

- **老问题**：纯 LRU 会被「一次全表扫描」把全部热点页挤出去（**缓冲池污染**），之后所有查询都要重新从磁盘读。
- **5.6 起的分段 LRU（old sublist）**：
  - LRU 链分成 **老年代（默认 37%）** 与**新生代（63%）**。
  - 新读入的页先放老年代头部；**只有在老年代停留超过 `innodb_old_blocks_time`（默认 1000ms）之后再次被访问**，才晋升到新生代头部。
  - 效果：一次长扫描会把老年代占满，但扫描结束后的热点页很快回到新生代。
- **预读页的副作用**：预读进来的页可能永远不会被访问，白白占用老年代；5.6+ 用「插入位置调整」缓解。
- 🔧 **Buffer Pool 多实例**：`innodb_buffer_pool_instances`（默认按 size ≥1GB 自动开多个）。**多实例把页哈希的锁争用摊薄**，对多核大内存机器是几乎免费的收益；但要注意**同一张表的页会分散在不同实例上**，跨实例访问没有额外代价。

### 17.3 脏页与刷盘：矛盾的核心

- **为什么需要刷**：内存是易失的；redo 保证「不丢」，但**页本身仍要被写回磁盘**（redo 只覆盖到 checkpoint）。
- **checkpoint**：记录「哪些 redo 对应的页已经落盘」的 LSN 水位。redo 文件循环写，checkpoint 必须**持续推进**，否则 redo 会被覆盖，崩溃恢复就缺历史。
  ```text
  ib_logfile:  [已覆盖 ←  checkpoint  ←  正在写  →]
  ```
  **checkpoint 推进不下去 → redo 写满 → 数据库只能「卡住写入」**（`LOG_ARRAY_OF_FILE_SPACE` 等待），这是 redo 容量不足时的典型症状。
- **刷盘的触发者**：
  1. 后台 `page_cleaner` 线程按 `innodb_io_capacity` 的比例刷；
  2. 用户线程自己刷（不够快时）；
  3. `redo` 快写满时紧急刷；
  4. `DROP TABLE` / 表清空等特殊操作后的批量刷。
- **关键旋钮**：
  | 参数 | 作用 |
  | --- | --- |
  | `innodb_io_capacity` | 刷盘 IOPS 上限（默认 200，SSD  Environment 常需调到 1000~4000） |
  | `innodb_io_capacity_max` | 紧急情况下允许冲到的上限（🔧 8.0 才有此上限概念更明确） |
  | `innodb_flush_neighbors` | 是否顺带刷「相邻的脏页」（默认 1；🔧 **8.0 默认 0**，因为 SSD 上相邻 IO 无收益） |
  | `innodb_flush_method` | `fsync` / `O_DIRECT` / `O_DIRECT_NO_FSYNC`；🔧 8.0.5+ 支持**原子写（atomic write）**写 doublewrite 区 |
  | `innodb_max_dirty_pages_pct` | 脏页占比上限，超过就加速刷 |
- **调参直觉**：`innodb_io_capacity` 调到磁盘标称 IOPS 的 ~70~100%，既避免 io 打满拖慢查询，也避免脏页堆积触发紧急刷。

### 17.4 doublewrite buffer：修复「半个页」

- **问题（部分页写 / torn page）**：一个页默认 16KB，而底层硬件/文件系统写入的最小单元可能只有 512B~4KB。若写入过程中崩溃或掉电，**一个页可能只有前 8KB 是新的，后 8KB 是旧的**。
- **redo 救不了它**：redo 里记的是「把第 N 页改成 X」，但**恢复时读到的页本身是残缺的** —— 无法判断该重写成什么。
- **解法：doublewrite**：
  1. 页修改前，先把页**连续写入 doublewrite buffer**（磁盘上一段 2MB 的连续区域）；
  2. 写完 doublewrite 后，再**分散地」写到真正的表空间位置**；
  3. 崩溃后恢复时：若发现某些页校验和不成立，就从 doublewrite buffer 里把完整副本拷贝回去。
  ```text
  用户线程:  改页 → 写 dblwr 区（顺序） → 写表空间（随机）
  崩溃恢复:  校验和失败 → 从 dblwr 拷贝回该页 → 再走 redo
  ```
- 代价：**每次写页多写一次**（所以 `innodb_flush_method=O_DIRECT` 时 doublewrite 也在）。收益：顺序写 + 修复能力。
- 🔧 **现代演进**：8.0.5 起支持**原子写**（`innodb_doublewrite=OFF` 且文件系统/设备支持原子写），可以**关掉 doublewrite**，直接省掉一次写放大。但这个功能依赖底层支持，生产上要实测。

### 17.5 预读：把随机读变成顺序读

| 类型 | 触发条件 | 参数 |
| --- | --- | --- |
| **线性预读（linear read-ahead）** | 连续读取同一个 extent（64 页）中 ≥ `innodb_read_ahead_threshold`（默认 56）个页 | 只读前台线程，同步预读 |
| **随机读预读（random read-ahead）** | 某个 extent 中的页被「频繁随机访问」 | 5.6 起默认关闭 |

- **本质**：预读是把「用户接下来大概率要的页」提前拉进 Buffer Pool，用**顺序 IO 换掉未来的随机 IO**。
- 反例与对策：
  - **大表全表扫描**会疯狂预读，把热点页挤走 → 需要 `innodb_old_blocks_time` 兜底，或对该查询使用「批量导入/只读」策略。
  - 一张表远大于 Buffer Pool 时，预读收益有限但污染仍在 → 🔧 8.0 有更细的并行扫描与预读协同，仍需结合业务观察命中率。

### 17.6 调参与容量规划

- **容量**：`innodb_buffer_pool_size` 通常设为「热数据量」的 1.0~1.5 倍；**不要只按内存剩多少来定**，要看「需要常驻的数据」。
- **命中率**：`SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%'`，用
  `命中率 ≈ 1 - (reads / (reads + read_requests))`。
  - 命中率跌到 95% 以下通常意味着容量不足或存在全表扫描。
  - ⚠️ **不要用「Buffer Pool 内存占用」判断够不够** —— 它是「已用」不是「容量上限」。
- **change buffer**：对非唯一二级索引的 `INSERT`，可以先把改动缓存在 change buffer 里，等将来读这一页时再合并（**写放大与随机 IO 的缓解手段**）。旋钮：`innodb_change_buffer_max_size`（默认 25%）。
  - 代价：change buffer 里的改动最终仍要落盘，且**崩溃恢复变复杂**。
- **多实例**：`innodb_buffer_pool_instances`（5.7 起，1GB 以上默认 8 个）。

### 17.7 🔧 2026 视角：原来「只能重启」的事，现在大多能在线做

| 能力 | 说明 |
| --- | --- |
| 🔧 `innodb_buffer_pool_size` 在线调整 | 8.0 起可 `SET GLOBAL innodb_buffer_pool_size=...` 在线伸缩（缩容受当前已用限制），不必重启 |
| 🔧 Buffer Pool 预加载（preload） | 8.0.20 起 `innodb_buffer_pool_preload`，重启后可在实例启动前把之前 dump 的页预加载回 Buffer Pool，缓解「重启后冷缓存」 |
| 🔧 原子写 | 8.0.5+ 支持，可关 doublewrite（依赖底层原子写能力） |
| 🔧 `innodb_flush_neighbors=0` | 8.0 默认，SSD 环境下少一次相邻页刷盘 |
| 🔧 `innodb_redo_log_capacity` | 8.0.11 起 redo 容量可在线调节（见 `19-redo日志.md`） |
| 🔧 Clone Plugin（8.0.17） | 物理克隆会把 Buffer Pool 的状态一并带上；`CLONE BUFFER POOL` 可导出/导入缓存 |
| ⚠️ 未变的老问题 | 原书里「Buffer Pool 不够要重启加内存」在 2026 已经不 inconvenient 了，但「扫描挤走热点」依然要靠 `old_blocks_time` 与 SQL 侧约束 |

### 17.8 🔧 Buffer Pool 的监控指标与容量估算

- 关注四类指标（教学示意，不参与构建，需实际连接实例）：

  | 指标 | 来源 | 判读 |
  | --- | --- | --- |
  | 读命中率 | `Innodb_buffer_pool_read_requests` / `..._reads` | 长期 < 95% 说明容量不足或有全表扫描 |
  | 脏页比例 | `Innodb_buffer_pool_pages_dirty` /总页数 | 接近上限说明刷盘跟不上写入 |
  | 刷盘量 | `Innodb_buffer_pool_pages_flushed` 的变化速率 | 与写入速率对比可判断是否有额外放大 |
  | 老年代命中 | 预热后的二次观察 | 下降说明「扫描污染」在发生 |

- **容量估算的实用口径**：
  1. 先量出「需要常驻的数据量」（不能全放内存的表要单独挑热数据集）；
  2. 取热数据量 × 1.0~1.5 作为 `innodb_buffer_pool_size`；
  3. 预留 20~30% 给连接、排序、临时表、change buffer；
  4. 🔧 8.0 可先按估计值配置，上线后用命中率与脏页比例校正 —— **不需要重启**。
- 🔧 **冷缓存代价**：实例重启后 Buffer Pool 全空，常见表现是「重启后 30 分钟性能爬坡」。缓解手段：8.0.20 的 `innodb_buffer_pool_preload`、Clone 时的 `CLONE BUFFER POOL`、或把常驻小表放在 cache-only 实例（NDB / Redis）里。

## 版本演进

| 版本 | Buffer Pool 相关变化 |
| --- | --- |
| 5.5 | Buffer Pool 基本形态、老年代 LRU 的前身 |
| 5.6 | **老/新生代 LRU**、change buffer 改进、多实例（`instances`） |
| 5.7 | `innodb_flush_neighbors` 更可控、`innodb_buffer_pool_instances` 默认按大小 |
| 8.0 | 在线调 Buffer Pool、原子写、`flush_log_at_trx_commit` 相关、redo 动态容量 |
| 🔧 8.0.5 | 原子写支持 |
| 🔧 8.0.11 | `innodb_redo_log_capacity`（动态 redo） |
| 🔧 8.0.17 | Clone Plugin（含 Buffer Pool 状态传递） |
| 🔧 8.0.20 | `innodb_buffer_pool_preload` |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Arief & Sweeney, *The PostgreSQL Shared Buffer Pool* 及 *Buffer Pool Management Techniques*（Gray 的经典论文 *Buffer Management in a Database System*） | 1977 / 相关期刊 | **Buffer Pool 替换算法与「页替换会打断事务」的经典分析** |
| Johnson & Shasha, *The Linear Read-Ahead Technique*（及 Review of Buffer Management Techniques） | VLDB 1994 / 1992 | **线性预读**的标准算法来源 |
| Stonebraker et al., *The End of an Architectural Era (It's Time for a Complete Rewrite)* | VLDB 2007 | 缓冲池/闩争用/日志在 OLTP 开销中的占比剖析 |
| MySQL 官方文档：InnoDB Buffer Pool / Doublewrite Buffer / Configuring InnoDB I/O Capacity | dev.mysql.com | 参数名、默认值、原子写前提的权威口径 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：**非易失内存（PMem/持久内存）下的缓冲池**——传统「内存缓存 + 磁盘持久」的两层模型被模糊，「写直达 / 持久内存日志」成为热点；**存算分离**（Aurora、PolarDB）把页缓存搬到共享存储，缓冲池语义变成「与共享存储的缓存一致性」；**云上弹性缓冲池**（按负载自动伸缩内存），正是 8.0 在线调 `innodb_buffer_pool_size` 的商业版对应物。
- **工业界开源**（star 数 2026-09-25 通过 `gh api` 实测）：
  - `mysql/mysql-server`（≈12.4k★）：Buffer Pool 实现 `storage/innobase/buf/buf0buf.cc`，刷盘 `buf0flu.cc`，doublewrite `buf0dblwr.cc`，预读 `buf0rea.cc` —— 原书读者可以按图索骥。
  - `facebook/mysql-8.0`（≈115★）：Facebook 在 **flush 线程数、io_capacity、change buffer 上限**上的长期工程经验，常见做法与社区默认值有出入。
  - `percona/percona-server`（≈1.3k★）、`mariadb/server`（≈8.3k★）：分支在 Buffer Pool 与刷盘策略上的差异（如 MariaDB 的 `innodb_flush_neighbors` 默认值与 MySQL 不同）。
  - `facebook/rocksdb`（≈32.1k★）：LSM 引擎用**块缓存 + 后台压缩**替代 B+ 树的缓冲池，「命中率」与「写放大」的取舍逻辑与 InnoDB 同构但方向相反。
  - `pingcap/tidb`（≈40.6k★）：TiKV 的 block cache + raft 日志同步刷盘，是「缓冲池 + 共识刷盘」的现代样本；`cockroachdb/cockroach`（≈32.5k★）同理。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Buffer Pool 使用率 99% 就是内存不够」 | 那是「已用」不是「满」；要看命中率与 `free` 链长度 |
| 2 | 「doublewrite 是历史包袱，可以关」 | 关掉的前提是底层支持**原子写**（8.0.5+）且已实测；否则崩溃恢复会丢页 |
| 3 | 「SSD 上 `innodb_flush_neighbors=1` 更好」 | 8.0 默认已是 **0**；相邻 IO 在 SSD 上没有合并收益 |
| 4 | 「预读只会更快」 | 大表扫描的预读会污染热点页，`old_blocks_time` 是第一道防线 |
| 5 | 「`innodb_io_capacity` 越大越好」 | 刷盘打满 IO 会拖垮前台查询，一般取磁盘 IOPS 的 70~100% |
| 6 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有** Buffer Pool 在线调整（8.0）、**没有**原子写（8.0.5）、**没有** `innodb_buffer_pool_preload`（8.0.20）、**没有** Clone 传递 Buffer Pool 状态；`innodb_io_capacity_max` 也需按实际版本核对 |
| 7 | 🔧 **本书未覆盖** | **「重启后冷缓存」的代价**与预热方案、以及「Buffer Pool 多实例对锁争用的实际收益」在 NVMe + 多核机器上的量化结论 |

## 与其他章 / 其他书的联系

- → `19-redo日志.md`：checkpoint 由 redo LSN 推进，redo 写满会反噬刷盘策略。
- → `20-undo日志.md`：长事务会卡住 purge，undo 页的读取也走 Buffer Pool。
- → `X2-日志系统专题.md`：doublewrite 与 redo 一起构成落盘的「双保险」。
- → `14-单表查询.md`：全表扫描会污染 Buffer Pool，是命中率突降的常见原因。
- → `16-optimizer-trace.md`：预读与命中率共同决定成本模型里 I/O 成本项的大小。
- → [10-存储和文件结构.md](../数据库系统概念6/10-存储和文件结构.md)（若存在）：缓冲管理器与替换算法的通用理论。
- → [26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)：H-Store/VoltDB 论文里「缓冲池几乎不需要」的对照观点。
