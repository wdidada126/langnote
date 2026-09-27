# 01 · SQLite 概述（An Overview of SQLite）⚠️ 章号推定

> 主题锚定：SQLite 是什么、为什么存在、能力边界在哪。机制描述全部对齐
> sqlite.org 官方文档（[whentouse.html](https://sqlite.org/whentouse.html) ✅、
> [fileformat.html](https://sqlite.org/fileformat.html) ✅），文末 🔧 为本会话实测。

## 1. 一个"库"而不是"服务器"

SQLite 的颠覆点不在 SQL 方言，而在**进程模型**：没有守护进程、没有账号体系、
没有 socket——整个"数据库服务器"就是一个 C 库，链接进你的应用程序，
读写目标就是**一个普通文件**。这带来三个直接后果：

- **零配置**：`sqlite3('app.db')` 即完成"建库 + 连接 + 认证"全过程；
  没有安装后初始化，没有 `GRANT`，没有监听端口；
- **事务型 ACID**：崩溃/断电不产生"半提交"（原子提交协议，见 [atomiccommit.html](https://sqlite.org/atomiccommit.html) ✅ 与 08 章锁协议）；
- **单文件 = 单实体**：备份 = 复制文件（有前提，见 08 章在线备份），
  分发一个嵌入式存储引擎 = 发一个 `.db`。

书中给过的量化印象（体积）：库核心数百 KB 级、内存占用可低至几十 KB，
适合从机顶盒到手机的一切设备。⚠️ 具体 KB 数随构建选项浮动，官方测试与质量口径见
[testing.html](https://sqlite.org/testing.html)（✅ 实抓 200）；历史上的体积对比页
（size.html）在当前站点已 404，引用旧数字前先复核。

## 2. 历史与许可证：公有领域意味着什么

- 2000 年 D. Richard Hipp 为飞行维修系统（离线、不能装数据库、不能联网）
  设计"随应用走的数据库"，此后 SQLite 成为内核/浏览器/手机 OS 的标配组件。
- 许可证为 **Public Domain**（无许可证的"许可证"）：可静态链接进闭源产品、
  可 fork 改名、可写进任何发行版而无一纸义务。这是它能"出现在每个设备上"
  的法律基础——GPL 的 MySQL 嵌入分发要面对传染性争议，SQLite 无此顾虑。
- 官方口号 "Small. Fast. Reliable. Choose any three."（✅ 实抓自
  [sqlite.org/index.html](https://sqlite.org/index.html) 页面标语）——
  注意这是自谦的反话：SQLite 的目标是三个都要，放弃的是"多写并发"这一项。

## 3. 能力边界：什么时候不该用（书中判断 + 2026 仍成立）

官方 "When To Use SQLite" ✅ 与书一致的分界线：

| 不适合 | 原因 | 替代方向 |
| --- | --- | --- |
| 高并发写、多进程写同一库 | 写锁全库粒度（文件级锁；WAL 也只是缓解，见 08 章） | C/S 数据库 |
| 客户端跨公网直连的集中库 | 无网络协议、无用户认证；把 DB 文件放 NFS 上并发访问是被官方明令禁止的场景 | 服务端引擎 |
| 超大 BLOB/二进制资产库 | 单文件膨胀拖垮备份与 VACUUM（🔧 见 09 章实测） | 对象存储 + SQLite 存元数据 |
| 需要 Oracle/SQL Server 级企业审计 | 无行级安全、无细粒度权限体系 | 见 [../Database_Reliability_Engineering/03-扩展性与可用性设计.md](../Database_Reliability_Engineering/03-扩展性与可用性设计.md) 的规模化视角 |

**与系列对读**：[../Understanding_MySQL_Internals/07-存储引擎接口.md](../Understanding_MySQL_Internals/07-存储引擎接口.md)
里 InnoDB 是"服务器内的插件引擎"；SQLite 反过来——"引擎就是全部，服务器不存在"。
同一张 B+ 树页思想，两个宿主。

## 4. 体系结构速览（对应书中第 1 章的架构图主题）

```
SQL 文本 → 令牌/解析器 → 查询编译器(字节码) → VDBE 虚拟机
                                                  ↓
                             后端: B-tree 页存储 ←→ pager(页缓存/锁/journal)
                                                  ↓
                                        OS unix file I/O (VFS 抽象层)
```

- **VFS（Virtual File System）**是 SQLite 的可移植性心脏：所有文件 I/O、锁、
  mmap 都走一张 C 函数指针表。win32/unix 是内置实现，memory-only 用于 `:memory:`。
  02/05 章的编译话题、08 章的锁话题都最终落到这一层。
- **pager** 决定页如何进出缓存、journal/WAL 如何写——第 8、9 章的性能实验
  全在这层发生（🔧 09 章 cache_size 实验直接命中）。
- 与 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)
  的解剖图对读：Database Internals 把"页存哪、日志怎么刷"讲成通用原理，SQLite 是
  该原理最小可读实现——读它源码是系列内公认的最佳引擎入门路径。

## 5. 🔧 实测（本会话，Python 3.13.2 / SQLite 3.45.3，Windows）

### 实验 A：打开一个数据库到底"重"不重（零配置的定量证明）

方法：对同一 73,728 字节、18 页的库，重复 `sqlite3.connect()` +
`SELECT count(*)` + `close()` 共 200 次，计时。

结果：总耗时 **26.4 ms，单次 0.132 ms**（含进程内新建连接对象、读文件头、
执行查询）。对比 MySQL 走 TCP 握手 + 认证的"连接成本"量级（毫秒到几十毫秒），
SQLite 的"连接"几乎免费——这正是书中"每个函数调用开一个库都划算"论断的实测支撑。

### 实验 B：单文件即全部——页与文件头解剖

方法：建表 `t(x INTEGER PRIMARY KEY, s TEXT)` 插入 500 行（约 72 KB），
用 Python 读文件前 100 字节，按 [fileformat.html](https://sqlite.org/fileformat.html) ✅
官方头布局解码；随后删一行再提交。

结果：
- 文件头 16 字节 magic：`SQLite format 3\000`；
- 解码第 16-17 字节：**page size = 4096**（compile_options 里 `DEFAULT_PAGE_SIZE=4096` 一致，见 02 章）；
- 第 56-59 字节：text encoding = 1（UTF-8）；`PRAGMA page_count` = 18，
  `PRAGMA freelist_count` = 0（删过的页归还进 freelist 后为 1，见 09 章）；
- 整个数据库**就这 18 页**，没有任何 sidecar 文件——"数据库 = 文件"不是比喻。

### 实验 C：WAL 模式下文件"不再是单文件"

方法：`PRAGMA journal_mode=WAL` 后写 5000 行提交，列目录。

结果：`exp8_wal.db` 4,096 B + **`-wal` 61,832 B + `-shm` 32,768 B**。
"单文件"是 rollback journal 模式的承诺；WAL 下有效实体变成三文件，
"直接复制主文件当备份"在 WAL 下不再安全（08 章备份实验呼应；
DBRE 笔记 [../Database_Reliability_Engineering/07-数据作为生产资料与备份恢复.md](../Database_Reliability_Engineering/07-数据作为生产资料与备份恢复.md)
的热拷贝反例实验同题）。

## 6. 本章带走三条

1. 选 SQLite 的判据不是"数据量小"，而是**写并发模型匹配**：一写多读几乎一切场景成立；多写就要设计分片（每写者一文件）。
2. Public Domain 是它能成为"设备默认件"的第一原因，评估嵌入式存储时法律成本先于技术成本。
3. 单文件承诺有例外（WAL、-shm），备份纪律要按 journal 模式分类讨论——08 章与 DBRE 07 章文件。

## 核心概念速览（中英对照）

- **嵌入式数据库** — embedded database：以库形式链接进宿主进程、无独立服务器的数据库
- **零配置** — zero-configuration：无需安装/初始化/账号即开即用
- **公有领域** — public domain：无版权许可，商用/修改/再分发无任何附加义务
- **ACID 事务** — ACID transaction：原子性/一致性/隔离性/持久性，SQLite 靠 journal 原子提交达成
- **VDBE** — virtual database engine：SQLite 内部的字节码虚拟机，执行编译后的 SQL
- **VFS** — virtual file system：SQLite 对 OS 文件 I/O 与锁的抽象接口层
- **pager** — 分页器：页缓存 + journal/WAL 读写调度的内部子系统
- **页** — page：SQLite 文件的最小 I/O 单位（默认 4096 B，建库时定死）
- **文件头** — file header：前 100 字节，记录 page size/编码/格式版本/变更计数器
- **WAL** — write-ahead log：写前日志模式，读写并发大幅优于 rollback journal
- **-shm** — shared memory index：WAL 的共享内存索引侧文件（伴随 -wal 存在）
- **单写者模型** — single-writer model：任意时刻只允许一个写事务，是并发上限的根源
- **原子提交** — atomic commit：崩溃后库要么完全提交要么完全回滚的协议
- **`:memory:`** — memory database：以内存为宿主的特殊文件名，进程退出即蒸发

## 最新演进与工业实践

- **最新稳定版 3.53.4（2026-07-24）**：官方 [changes.html](https://sqlite.org/changes.html) 与
  [download.html](https://sqlite.org/download.html) 本会话实抓 ✅；该书 3.8.x 基线距今约 40 个次版本，
  但文件格式（format 3）从未破坏性变更——2004 年的库文件在 3.53 上直接打开，这是"嵌入式
  = 长寿格式"的行业教科书案例。
- **"何时使用"官方口径未变**（[whentouse.html](https://sqlite.org/whentouse.html) ✅）：手机端/桌面应用/
  站点后台存储/分析临时落地仍是推荐区；多客户高并发写应用仍被劝退。2026 新增的推荐场景是
  **AI 应用本地态**（向量/对话历史落盘），常见搭配是 sqlite-vec 类扩展（⚠️ 第三方，未经本会话核验其仓库）。
- **严格模式对位**：3.37 STRICT 表与 3.44 起的 `PRAGMA defer_foreign_keys` 等把"宽松哲学"
  变成可选项而非强制（06/07 章实测）。
- **系列互链**：并发能力边界的工程处理见
  [../Database_Reliability_Engineering/05-无停机变更.md](../Database_Reliability_Engineering/05-无停机变更.md)
  （小库的 expand-contract 变更实验即跑在 SQLite 上）；
  行存单机 vs 列存单机的当代对位见 [#134 DuckDB: Up and Running·01 入门](../DuckDB_Up_and_Running/01-DuckDB入门.md)
  （波尾闭环 2026-09-27：其"列存直查 10M 行聚合 0.03 s"与本目录行存画像恰成镜像）。
- **取证清单（本章）**：whentouse.html ✅、fileformat.html ✅、index.html ✅、
  atomiccommit.html ✅（均 curl 200，2026-09-27）；实验 A/B/C 脚本产物
  `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt`。⚠️ 未核验：历史体积报告具体数字
  （官方 size.html 现 404，本会话实测）、原书页码与前言署名（O'Reilly 403）。
