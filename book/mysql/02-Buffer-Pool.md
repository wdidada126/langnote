# Buffer Pool——InnoDB 的内存心脏（页框 / free list / LRU / flush）

> **原书位置**：主题对应第 2 章「MySQL的调控按钮——启动选项和系统变量」中的内存参数，以及第 17 章「调节磁盘和CPU的矛盾——InnoDB的Buffer Pool」（这位主题的深度展开由另一位助手负责）。
> 本文件名沿用任务映射表 `02-Buffer-Pool.md`。原书基于 **MySQL 5.7.22**。
>
> **一句话**：Buffer Pool 是**一块按「页框（frame）」切分的固定大小内存**，InnoDB 用它同时缓存数据页、索引页、
> undo 页、change buffer 页；**所有「内存与磁盘之间」的性能矛盾，本质上都是这块的容量管理问题。**

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 为什么必须有缓冲池 | 磁盘随机读 ~10ms 级 vs 内存 ns 级，差 4–5 个数量级 | 关系模型隐藏了 I/O，缓冲池是它最大的「作弊底牌」 |
| 2.2 页框与页的映射 | Buffer Pool 切成固定大小**页框**，与磁盘页 1:1 对应；哈希索引快速定位页 | 页框是「槽位」，页是「内容」，二者不同概念 |
| 2.3 free list | 空闲页框链表，需要页时从 free list 摘一个 | 空闲页用完后才开始淘汰，淘汰策略由此成为核心 |
| 2.4 LRU 链表（分 young / old 两段） | 默认 `innodb_old_blocks_pct=37`，新页先入 **old 区头部**，满足「在 old 区停留超过 `innodb_old_blocks_time`」才晋升 young | **这是为了防止一次全表扫描把整个缓冲池冲掉** |
| 2.5 flush 链表 | 脏页串在 flush list 上按 lsn 顺序刷盘，后台线程周期性推进 | 刷脏不是「立刻写」，而是**顺序化 + 批量化**的后台工作 |
| 2.6 预读（read ahead） | 线性预读（`innodb_read_ahead_threshold`）、随机预读（8.0 起默认关闭） | 预读命中则省一次 I/O，预读错误则白白占用带宽 |
| 2.7 脏页比例与 checkpoint | `innodb_max_dirty_pages_pct`、刷新速率随脏页比例自适应 | 脏页比例失控 → 查询突然变慢（经典的「刷脏风暴」） |
| 2.8 🔧 多实例与自动 sizing | `innodb_buffer_pool_instances`、`innodb_dedicated_server`、NUMA 绑定 | 大内存机器不划分实例会出现严重的**链表争用** |
| 2.9 🔧 与 2020 年的差异 | 8.0 的 LRU 改进、`doublewrite` 页结构、change buffer 占用 1/4 | 原书口径的默认值已不能直接照搬 |

## 核心精讲

> 以下 SQL / 结构均为**教学示意，不参与构建**：本目录不搭建真实实例，示例只用于对齐概念。

### 1. 内存布局示意（教学示意，不参与构建）

```
          Buffer Pool（固定大小，如 128MB，按 16KB 页框切分）
 ┌──────────────────────────────────────────────────────────────┐
 │ free list │  LRU-young 段（≈63%）  │  LRU-old 段（≈37%）     │
 │ 空闲页框  │  真正热的数据/索引页    │  刚读入的「待观察」页   │
 │           │                        │  有指针指向更老的页      │
 │           ├────────────────────────┼──────────────────────────┤
 │           └─ flush list（脏页，按 lsn 有序）──────────────────┘
 └──────────────────────────────────────────────────────────────┘
        ↑ 页哈希表（hash(table_space_id, page_no) → frame）
```

三条链表各司其职，常被混淆：**free list 管「我有空位吗」，LRU 管「该踢谁」，flush list 管「谁要写回」**。

### 2. LRU 的两段式设计（教学示意，不参与构建）

```
新读入的页 → 插到 old 段头部
              │
              ├─ 1 秒内再次被访问（如随后立刻扫描读）→ 直接滞留 old，不晋升
              └─ 停留超过 innodb_old_blocks_time（默认 1000ms）→ 晋升到 young 段头部
淘汰时：从 young 段尾部开始踢（因为 young 段里的页至少被「用过两次」）
```

这个设计的实际收益：**一次 `SELECT * FROM 大表` 只会污染 old 段**，缓冲池里真正的热页基本无恙。
反过来说，如果业务里频繁出现「超大全表扫描 + 短连接」，old 段仍可能被打穿。

### 3. 页框、页、记录的关系（教学示意，不参与构建）

```
磁盘上的页（16KB）= 缓冲池中的一个页框（16KB）
  └─ 页内：页头 + 行记录（一行或多行）+ 页目录（槽位指针）
        └─ 行记录通过「下一次页面偏移(9~20 字节)」串成单向链表
```

- **页大小**：`innodb_page_size` 默认 **16KB**（5.6/5.7/8.0 一致），可在初始化时指定 4K/8K/16K/32K/64K。
- **页框数量** ≈ `innodb_buffer_pool_size / 16KB`；例如 128MB 池 ≈ 8192 个页框（还要为描述块、锁信息等留出额外内存）。

### 4. 关键变量速查（教学示意，不参与构建）

| 变量 | 默认（5.7/8.0 典型） | 说明 |
| --- | --- | --- |
| `innodb_buffer_pool_size` | 128MB（8.0 变 128MB） | 核心容量 |
| `innodb_buffer_pool_instances` | 1（>1GB 时自动 8，8.0 有 `innodb_buffer_pool_chunk`） | 🔧 减少链表争用 |
| `innodb_old_blocks_pct` | 37 | old 段占比（5.7 起从 5% 提到 37%） |
| `innodb_old_blocks_time` | 1000（ms） | old 段停留门槛 |
| `innodb_free_list_len` | 运行时 | 查看当前空闲页框数 |
| `innodb_max_dirty_pages_pct` / `_pct_lwm` | 75 / 0 | 脏页水位与刷盘阈值 |
| `innodb_lru_scan_depth` | 1024 | 每秒 LRU 扫描深度 |
| `innodb_flush_neighbors` | 1（8.0 改 0？逐版本核对文档） | 是否刷「相邻」页 |
| `innodb_change_buffer_max_size` | 25（8.0 起，旧名 `innodb_change_buffer_max_size` 原为 `innodb_change_buffer_max_size`） | change buffer 最多占池的比例 |

> 注：上表部分默认值在不同小版本间有调整，**以你所用版本的官方文档为准**；本目录不提供「应该照抄的数字」，
> 只提供「为什么是这个量级」。

### 5. 一次 SELECT 经过缓冲池的路径（教学示意，不参与构建）

```
① 查页哈希表：目标页是否已在池内？
   ├─ 在 → 在 LRU 中提升该页（移到 young 头），返回帧指针
   └─ 不在 → ① 从 free list 取空闲框；② 取不到则按 LRU 淘汰一个「干净页」；
             ③ 从表空间读入磁盘页 → 插入 LRU old 头 → 建哈希映射
② 若这页被修改 → 标记脏 → 挂到 flush list（不立刻写盘）
③ 后台：flush list 按 lsn 顺序刷脏 + change buffer 合并 → free list 回收
```

### 6. 缓冲池相关的排障速查（教学示意，不参与构建）

| 症状 | 可能原因 | 先看什么 |
| --- | --- | --- |
| 查询延迟长期抖动、突然变差 | 刷脏风暴（脏页比例逼近上限） | `Innodb_buffer_pool_pages_dirty * 16KB / innodb_buffer_pool_size` |
| 大量小表访问后性能骤降 | 全表扫描把 old 段打穿 | 慢查询里是否存在无 `WHERE` 的扫描 |
| 内存已用 90%+ 但吞吐上不去 | 页框不足导致频繁换页 | `Innodb_buffer_pool_pages_free` 长期接近 0 |
| 高并发下 `buf_pool_mutex` 竞争 | 单实例 + 大池 | `innodb_buffer_pool_instances`（大内存机器应 >1） |
| 启动时加载极慢 | 池太小，重启后重新预热 | 加大 `innodb_buffer_pool_size`，或配合预热策略 |
| 重启后 IO 突然很高 | 池里的热页全丢（change buffer 未合并完） | error log 中的 change buffer 合并耗时 |

### 6.1 一个粗略的容量估算（教学示意，不参与构建）

```
一页 16KB；每行假设 200 字节 → 一页约可放 80 行
表有 1 亿行 → 数据约需 1.25M 页 ≈ 20GB
加上二级索引（假设 1 个，键 + 行指针约占行长的 30%）：再放大约 20–40%
结论：只想「热数据常驻」则不必把整表塞进池，而是靠「访问频次」区分冷热。
```

这个估算说明：**「加到多少内存能搞定」是个伪问题**，真正的问题是「你的工作集有多大」。

### 7. 观测命令（教学示意，不参与构建）

SHOW 语句只读取运行实例的运行时信息，不构成构建步骤：

```sql
-- 查看缓冲池大致规模（生产上不要对大表跑全表统计）
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW STATUS LIKE 'Innodb_buffer_pool_pages_%';
```

`Innodb_buffer_pool_pages_dirty / _data / _free / _total` 的比值，就是判断「内存是否够用」的第一手指标。

## 版本演进

| 版本 | 关键变化 |
| --- | --- |
| **5.7（原书基线）** | `innodb_old_blocks_pct=37`、`innodb_old_blocks_time=1000` 已就位；`innodb_lru_scan_depth` 可调；change buffer 上限默认 **25%**（`innodb_change_buffer_max_size`） |
| **8.0** | 🔧 新增 `innodb_dedicated_server`（按内存/CPU 自动设定 buffer pool、log buffer、IO capacity 等，可用 `ON`/`OFF`/`AUTO`）；🔧 Buffer Pool 支持 **chunk 机制**与在线扩容（`innofd_buffer_pool_size` 相关）；🔧 移除「预刷脏线程」相关旧选项，刷新线程模型改为后台线程组；🔧 默认 `innodb_flush_neighbors=0`（NVIDIA 等论文驱动的改动，逐版本核对文档） |
| **8.4 LTS** | 🔧 `innodb_dedicated_server` 行为与默认值继续调整；默认内存分配更强调「专供 InnoDB」的整体比例，官方文档有专门的「Section 主机内存分配」说明 |
| **9.x** | 🔧 与 HeatWave 共存后，OLTP 实例的 buffer pool 更强调「可预测」而非「尽量大」 |
| **MariaDB 对照** | 同样有 pool of buffers，但把大部分 LRU 参数放进 `innodb_buffer_pool_*`，行为与 MySQL 8.4 有差异；MariaDB 用 Aria 替代 MyISAM 做临时表 |
| **PostgreSQL 对照** | PG 用 `shared_buffers`（默认仅 128MB）+ 依赖 OS page cache 两层缓存，LRU 由内核管，调优点位完全不同 |

## 经典论文与原始文献

| 来源 | 作者 / 出处 | 与本主题的关系 |
| --- | --- | --- |
| 2Q 替换算法 | Shah, Motivala, Ramakrishnan，*IEEE TKDE*，2004 | 「两级队列」思想的具体化，与 InnoDB 的 young/old 两段 LRU 同源 |
| LRU-K 缓冲区替换算法 | Jiang & Zhang，*IJITDM*，2004 | SQL Server 用的「记住历史 K 次访问」路线，解释「为什么朴素 LRU 不够」 |
| CLOCK-Pro | Jiang, Chen, Zhang，*ICCAD* 2005 | CLOCK 变体，通过扫描计数区分冷热，是无锁化缓存淘汰的常见思路 |
| 操作系统教材中的页面置换 | —— | 与 OS 的页面置换（FIFO/OPT/LRU/Clock）对照理解，InnoDB 只是换了个名字 |
| MySQL 官方文档：Buffer Pool / InnoDB Startup Options | MySQL 官方文档 | 本章默认值与变量语义的最终依据 |
| Linux 内核文档（`madvise`、`swap`、NUMA） | kernel.org 文档 | 理解「大页 + NUMA + swap」如何决定缓冲池的**实际**有效容量 |

> 说明：以上均为真实文献。原书没有专门一篇讲缓冲池的论文，因此这里用「真实算法论文 + 官方文档」替代，
> 不杜撰 MySQL 方面的论文题目。

## 近年研究与工业界开源实践（2015–2026）

- **`redis/redis`（2026-09 实测 ≈**76.5k★**）**：近似 LRU（`maxmemory-policy allkeys-lru` 用概率计数而非精确 LRU），
  以及 LFU（volatile-lfu）策略，是「精确性 vs 内存开销」取舍的经典样本。
- **`h2o/h2o`（≈**11.5k★**）**：Web 服务器的缓存也面临同一问题，其缓存实现大量使用「分桶 + 惰性过期」，
  与 InnoDB 的 LRU 差异在于**不需要与磁盘页 1:1 对齐**。
- **`clickhouse/clickhouse`（≈**50.1k★**）**：主存/磁盘两层的缓存策略由 `mark_cache_size`、文件系统缓存等共同决定，
  列存的「批量读」让预读价值比行存更大。
- **`facebook/mysql-5.6` / `mysql/mysql-server`（≈12.4k★）**：Buffer Pool 的核心实现在
  `storage/innobase/buf/buf0buf.cc`（`buf_LRU_get_free_block` 走 free list / LRU 淘汰，
  `buf_flush_list` 走刷脏）。
- **`mysql/mysql-server` 上的 NUMA 实践**：大内存机器上 `numactl --interleave=all` 常比绑 NUMA 节点更能压住延迟抖动，
  这类结论来自线上运维而非论文。
- **研究侧**：近年关于缓冲管理的工作集中在 **CXL / 持久内存下的分层缓存**（内存池不再只有一层）、
  **存算分离下远端内存的页调度**，以及 **OLAP 场景的「扫描优先」缓存**（ClickHouse 的 `mark_cache` 即此类）。

## 常见误区与本书需修正之处

| # | 常见误区 | 修正（🔧 = 原书出版时未覆盖） |
| --- | --- | --- |
| 1 | 「缓冲池越大越好」 | 超过物理内存的 70–80% 后，换页、`swap`、NUMA 不亲和会让收益反转 |
| 2 | 「全表扫描会清空缓冲池」 | 有 old 段保护（`innodb_old_blocks_time`），但**大事务+长扫描仍会打穿 old 段** |
| 3 | 「脏页一定很脏」 | 脏页只是「内存已改、磁盘未改」，不代表里面是不一致数据 |
| 4 | 「刷脏是前台操作」 | 有后台线程；但脏页比例逼近上限时，前台查询会被拖慢（刷脏风暴） |
| 5 | 「淘汰一个页就要写盘」 | 只有**脏页**必须写；干净页直接弃用即可 |
| 6 | 🔧「`innodb_dedicated_server` 是老参数」 | 它是 **8.0 新增**的自动配置开关，是 2020 年之后最值得优先评估的一项 |
| 7 | 🔧「单实例缓冲池够用了」 | 大内存机上应设 `innodb_buffer_pool_instances`（或依赖 8.0 的 chunk 自动划分）以降低链表争用 |
| 8 | 🔧 本书未覆盖 | 未覆盖 change buffer 占池比例的实际影响、8.4 的内存分配新默认值、以及 NUMA/大页（`innodb_buffer_pool_instances` + `huge pages`）对有效容量的影响 |
| 9 | 「池越大，预热越快」 | 预热速度取决于启动后前台查询的驱动；池大不等于「立刻热」 |
| 10 | 「`innodb_old_blocks_time` 越大越好」 | 调大能更好地防污染，但会拖慢「小表刚被读就要再读」的场景（如短连接频繁访问同一批小表） |
| 11 | 🔧「一个池实例就够」 | 8.0 有 chunk 机制与在线调整；但高并发 + 大池时多实例仍是降低争用的常规手段，需按内存规模权衡 |

## 与其他章 / 其他书的联系

- 本册：**03-数据页长什么样.md**（页框里装什么）、**05-InnoDB数据页结构.md**（页内结构）、
  **06-B树索引.md**（B+ 树节点就是被缓存的页）、**11-InnoDB内存结构.md**（change buffer / log buffer 同池分配）、
  另一位助手的 **17 Buffer Pool 深度篇**。
- 他册：《数据库系统概念（第6版）》[10-存储和文件结构.md](../数据库系统概念6/10-存储和文件结构.md)（缓冲管理器章节）、
  [15-并发控制.md](../数据库系统概念6/15-并发控制.md)（缓冲池闩与行锁的关系）、
  《多处理器编程的艺术（2）》第 9 章「链表与加锁粒度」（LRU 链表的并发优化）；
  原理侧还可参考《深入理解计算机系统》关于虚拟内存与局部性的讨论。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
