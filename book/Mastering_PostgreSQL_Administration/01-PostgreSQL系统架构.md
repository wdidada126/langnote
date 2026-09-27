# 01 · PostgreSQL 系统架构（原书第 1 章）

> 对应原书章：**Ch.1 PostgreSQL System Architecture**（✅ Crossref DOI `10.1007/979-8-8688-1507-2_1`）。
> 官方摘要原句（✅）："In this chapter, we learn about the origin of PostgreSQL, its architecture, and its
> components and understand the various components of PostgreSQL during a client connection request."
> 口径声明：章题与摘要 ✅ 实抓；**本章正文为按 PG16/17 官方文档口径的精读重构 ⚠️ 转述**，非原书文本；
> 本机无 PostgreSQL 实例，所有命令/视图一律文档转述，不冒充实测。

## 本章地图

| 主题 | 你能做到 | 关键对象/参数/命令 |
| --- | --- | --- |
| 演进史定位 | 说清 POSTGRES→PostgreSQL 谱系与版本节奏 | 伯克利 POSTGRES(1986)→95→6.0(1997)→当前 17/18 ⚠️ |
| 进程模型 | 画出 postmaster 与子进程全景图 | postmaster/backend、checkpointer、bgwriter、walwriter、autovacuum launcher、walsender/walreceiver ⚠️ |
| 共享内存 | 判断一块内存归谁管 | shared_buffers、MAX_CONNECTIONS 派生的锁/缓冲槽、加量需重启（postmaster 启动时 mmap）⚠️ |
| 一次连接的路径 | 排查"连不上"卡在哪一环 | TCP/libpq → postmaster fork backend → pg_hba 认证 → roles → syscache 装载 ⚠️ |
| 后台写与检查点 | 区分两个"谁把脏页刷盘"的角色 | bgwriter（增量刷）vs checkpointer（全量脏页+FSM，触发点）⚠️ |

## 核心精讲（⚠️ 文档转述重构）

### 1. 谱系与定位

PostgreSQL 源自 1986 年加州大学伯克利分校 Stonebraker 主持的 POSTGRES 项目（目标：修正关系模型对
复杂对象/多版本存储的支持不足），1994 年 Post95 加入 SQL，1996 年 6.0 起改称 PostgreSQL 并采用
"每年一个大版本"的节奏（社区惯例 9 月前后发布，✅ PG17 新闻页 2024-09-26 可作样本）。对 DBA 而言，
谱系的意义是理解**设计取舍的年代层积**：MVCC 的快照语义来自多版本存储的初衷，而大量运维参数
（vacuum、冻结）都是为多版本回收付账的机制。⚠️

### 2. 进程模型：一连接一进程

- postmaster（PG16 起文档亦称 PostgreSQL server process）是启动后的常驻父进程：持有监听套接字，
  为每个新客户端连接 **fork 一个 backend 进程**；backend 之间不共享用户态内存，通信全靠
  共享内存段 + 轻量级锁（LWLock）/自旋锁。⚠️
- 常驻后台进程族（可用 `SELECT * FROM pg_stat_activity WHERE backend_type LIKE 'checkpointer%'` 等观察 ⚠️）：
  - **checkpointer**：按超时/手动 CHECKPOINT 把所有脏页+FSM 页刷盘并在 WAL 记检查点记录；
  - **bgwriter**：周期性把"最冷"脏页提前刷出，降低 backend 查询被同步刷页绊住的概率；
  - **walwriter**：把 WAL 缓冲刷盘（wal_writer_delay 控制）；
  - **autovacuum launcher / workers**：按阈值表拉起 worker 做 vacuum/analyze（详见 06 章）；
  - **walsender / walreceiver**：流复制两端；逻辑解码亦由 walsender 承担；
  - **background worker**：扩展挂载点（pg_background、部分监控代理走此通道）。⚠️
- 与 MySQL-InnoDB 的"单进程多线程"根本不同：PG 每连接一个 OS 进程 → 连接成本高 → 连接池
  （PgBouncer 等）几乎是标配，这正是盘上 PG16 Cookbook 服务器控制章把 PgBouncer 放进主线的架构原因。
  对照读物：[../Understanding_MySQL_Internals/01-MySQL历史与架构.md](../Understanding_MySQL_Internals/01-MySQL历史与架构.md)
  讲了线程模型一侧；[../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md)（InnoDB 线程池）。

### 3. 共享内存三块地

- **shared_buffers**：页缓存 + WAL 缓冲（wal_buffers）。postmaster 启动时一次性 mmap，**改大必须重启**；
  社区经验值 RAM 的 1/4 只是起点，真正判据是 `pg_stat_bgwriter.buffers_backend`（backend 自己写脏页的
  比例）是否偏高。⚠️
- **锁与进程表**：max_connections 派生（改 shared_buffers 不动它也要重启的原因）。
- **work_mem 类不在共享内存**：排序/哈希按"每操作每 backend"私有分配，是"连接数 × 算子数"乘法放大的
  隐形炸弹（05/06 章性能语境反复出现）。⚠️

### 4. 一次连接请求的完整路径

libpq（或 pgbouncer 转发）→ postmaster accept → fork backend → 读 `postgresql.conf` 的继承副本 →
`pg_hba.conf` 按"用户/库/地址/方法"四元组匹配 → 认证（scram-sha-256 默认线）→ 角色与会话参数初始化 →
backend 从共享内存 syscache/relcache 读系统目录建立表可见性视图。任何一环失败都有对应报错面
（`no pg_hba.conf entry` vs `password authentication failed` vs `too many connections`），
这是连接类故障分诊的骨架。⚠️ 与 [../PostgreSQL_16_Administration_Cookbook/01-安装配置与服务器控制.md](../PostgreSQL_16_Administration_Cookbook/01-安装配置与服务器控制.md)
的四元组排查表互为"机制↔操作"两面。

### 5. 从架构到物理层的下钻预告

backend 读页的路径：先查 shared_buffers，未命中则读 OS 页缓存/文件 → 这就是 03 章物理结构的入口；
写路径的"预写日志先行"（WAL 记录先落盘、脏页后异步刷）留给 05 章备份恢复做读者的心智地基。
官方机制文档：⚠️（转述，未实测），参考线 https://www.postgresql.org/docs/current/wal-internals.html （✅ 实抓 200）。

## 常见坑与判读

| 现象 | 第一判读 | 取证动作（⚠️ 转述） |
| --- | --- | --- |
| 连接报 `sorry, too many clients already` | 达到 postmaster 连接槽上限，非故障是容量 | `pg_stat_activity` 按 state 分组计数；接连接池 |
| 改 shared_buffers 后 reload 不生效 | 共享内存在 postmaster 启动时定型 | 看 `pg_settings.context='postmaster'`，安排重启窗口 |
| 检查点期间写延迟尖峰 | checkpoint_completion_max 太紧或 CHECKPOINT 手动太密 | `pg_stat_bgwriter`/`pg_stat_checkpoints` 的 timed/req 比例 |
| CPU 高但 top 里是"很多 postgres 进程" | 进程模型正常形态，勿按 MySQL 习惯找线程 | 用 `pid` 列关联 `pg_stat_activity` 定位具体 backend |
| Docker/容器里 OOM | 每 backend 私有一块 work_mem，容器内存被乘法吃光 | 限连接 + 降 work_mem + cgroup 监控 |

## 与其他章 / 其他笔记的联系

- 本册：03 物理结构（页/FSM/VM 是本章存储侧的续集）；04 管理（连接路径尾段的角色/目录展开）；
  05 备份恢复（WAL 先行心智在本章建立）；06 维护（后台进程族的日常对手）；07 监控（本章各进程都有视图入口）。
- [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)：进程/内存架构的中文源码级版本，深读首选。
- [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)：同一架构知识的"食谱版"，操作对照。
- [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)：
  线程模型 + 存储引擎接口的对照面，两册合读才有"进程 vs 线程、单体 vs 插件引擎"的完整坐标系。
- [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)：SQL Server
  的进程/线程混合模型（Resource Governor 语境），异构 DBA 的第三个参照系。
- 系列登记：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 核心概念速览（中英对照）

1. **主进程** — postmaster (server process)：监听并 fork backend 的父进程，共享内存的持有者。
2. **后端进程** — backend process：一连接一进程的会话实体，PG 并发模型的基本单元。
3. **检查点进程** — checkpointer：全量刷脏页并写检查点记录，恢复/复制一致性的锚点。
4. **后台写进程** — background writer：预刷冷脏页，平滑 backend 的同步写。
5. **WAL 写进程** — WAL writer：按节拍刷 WAL 缓冲，与 wal_sync 语义配合。
6. **自动清理调度** — autovacuum launcher/worker：阈值驱动的 vacuum/analyze 执行体。
7. **复制发送/接收** — walsender / walreceiver：流复制与逻辑解码的进程两端。
8. **共享缓冲区** — shared_buffers：页缓存 + WAL 缓冲，改之必重启（context=postmaster）。
9. **工作内存** — work_mem：backend 私有的排序/哈希预算，连接数乘法放大。
10. **主机认证** — pg_hba.conf 四元组：用户/库/地址/方法，连接路径的第一道闸。
11. **系统缓存** — syscache/relcache：backend 启动后从系统目录构建的对象可见性快照。
12. **预写日志** — WAL (write-ahead logging)：先写日志再改数据页的持久性契约（详见 05 章）。

## 最新演进与工业实践

- **版本线**：PG17（2024-09-26，✅ https://www.postgresql.org/about/news/postgresql-17-released-2953/ 实抓 200）
  之后 PG18 已发布并进入 current 文档线（✅ https://www.postgresql.org/support/versioning/ 与
  https://www.postgresql.org/docs/current/release-18.html 均实抓 200）。进程模型自 9.x 以来保持稳定，
  最大增量是 PG18 的**异步 I/O 子系统**（io_method=worker/io_uring，顺序扫描/VACUUM 走 AIO）⚠️ 转述，
  它改变的是"backend 怎么读页"，不改本章进程拓扑骨架。
- **PG17 连接面**：libpq **pipeline mode**（批量流水但不并发同一连接）进主线，PgBouncer 2.x 亦跟进支持
  （session/transaction 池语义差异需注意）⚠️ 转述。运维心智：一连接一进程 → 池化仍是一切云上部署默认项。
- **可观测性**：`pg_stat_checkpoints` 在 PG16 起独立成视图（原混在 bgwriter 里），本章检查点判读表已按新视图口径写 ⚠️。
- **工业实践**：云上托管（RDS/Azure Database for PG/Cloud SQL）不改架构只改"谁能重启"；
  CloudNativePG（✅ https://github.com/cloudnative-pg/cloudnative-pg 实抓 200）把 postmaster/standby
  生命周期交给 K8s operator，本章的进程族是读懂其 pod 内 sidecar 布局的钥匙。
- **延伸阅读锚点**：WAL 内部机制官方文档 ✅ https://www.postgresql.org/docs/current/wal-internals.html （curl 200，2026-09-27）。
