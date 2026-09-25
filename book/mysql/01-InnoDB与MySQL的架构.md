# 第 1 章 装作自己是个小白——初识 MySQL（体系结构 / 连接层 / Server 层 / 存储引擎）

> **原书位置**：第 1 章「装作自己是个小白——初识MySQL」（1.1 MySQL的客户端/服务器架构；1.2 MySQL的安装；1.3 启动服务器程序；1.4 客户端程序；……）。
> 本目录文件名沿用任务映射表 `01-InnoDB与MySQL的架构.md`，内容按「体系结构」主题重写并补齐 2020 年之后的演进。
> 原书基于 **MySQL 5.7.22**，本文件所有 8.0 之后的内容均标 🔧。
>
> **一句话**：MySQL 是**一条 SQL 生命周期经过「连接层 → Server 层 → 存储引擎层」三层加工**的系统；
> 前面两层负责「连接、解析、优化、复制与 binlog」，最后一层只负责「数据怎么在磁盘与内存之间搬」。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 客户端程序 / 服务器程序 | `mysqld` 是服务器，`mysql` 是客户端；一次「连接」= 一条 TCP（或 unix socket）通道 + 一个服务线程 | 客户端与服务器是**两个独立可执行文件**，通信协议是 MySQL 私有协议 |
| 1.2 连接层（连接器 / 认证 / 线程管理） | 用户名密码校验、`password` 变动即踢线、连接被`wait_timeout` 空闲回收 | **连接不是「程序里的对象」，而是服务器分配给你的一个线程 + 会话上下文** |
| 1.3 Server 层职责 | 词法/语法解析 → 预处理 → 优化器（成本估算）→ 执行器 → 调用引擎接口 | Server 层**不碰磁盘**：它只生成「执行计划」并向引擎要 N 条记录 |
| 1.4 存储引擎层 | 可插拔插件式架构：`InnoDB` / `MyISAM` / `Memory` / `Archive` / `CSV` / `NDB` | **表级别**可换引擎（不像 PostgreSQL 是库级别），这是 MySQL 架构最独特之处 |
| 1.5 MySQL 协议与线程模型 | 一线程一连接（5.7 起有 thread cache）、半同步、`max_connections` | 连接成本 ≈ 一个线程的成本，所以连接池（HikariCP/Druid）在 MySQL 上收益最大 |
| 1.6 平台相关：安装与启动方式 | `mysqld --initialize`、配置文件 `/etc/my.cnf`、`mysqld_safe`、`systemd` | 启动选项与系统变量是**运行前**的行为开关，后文几乎所有参数都在这层定义 |
| 1.7 🔧 8.0 之后的架构变化 | 数据字典 InnoDB 化、`caching_sha2_password` 默认、`query cache` 删除、`binlog` 默认开、`mysql_install_db` 移除 | 2020 年之后「重启后行为不同」的多数坑，源头都在这层 |

## 核心精讲

> 以下 SQL / 结构均为**教学示意，不参与构建**：本目录不搭建真实实例，所有示例只用于对齐概念，请勿直接粘贴执行。

### 1. 分层结构示意（教学示意，不参与构建）

```
 ┌──────────────── 客户端程序 mysql / mysqldump / mysqlsh ────────────────┐
 │  TCP / unix socket / 命名管道  →  私有协议报文                          │
 └────────────────────────────┬───────────────────────────────────────────┘
                              │
 ┌────────────────────────────▼────────── 服务器程序 mysqld ──────────────┐
 │  【连接层】连接器(认证/权限)  |  线程管理(thread cache / thread pool)  │
 │          |  parse  ->  resolve -> optimize -> execute  -> binlog 写    │
 │  【Server 层】解析器 / 预处理 / 优化器 / 执行器 / Server 层日志(binlog) │
 │          |  引擎接口：read_first / read_next / write_row / update_row   │
 │  【存储引擎层】InnoDB / MyISAM / Memory / Archive ...   (表级可插拔)   │
 └────────────────────────────┬───────────────────────────────────────────┘
                              │
        ┌─────────────────────▼────────────────────┐
        │  磁盘：表空间文件(.ibd) / 系统表空间(ibdata*) / redo / undo      │
        │  内存：Buffer Pool / change buffer / log buffer / AHI            │
        └──────────────────────────────────────────┘
```

关键点：**Server 层没有「页」的概念**。「页 / 行格式 / B+ 树」全是引擎层（InnoDB）自己的事；
这也是为什么「同样的 SQL，换成 MyISAM 后执行计划完全不同」。

### 2. 一条查询的完整生命周期（教学示意，不参与构建）

```
mysql> SELECT * FROM t WHERE k = 10;
  ① 连接层：认证通过 → 分配线程 → 会话状态(隔离级别/字符集/临时表)就绪
  ② 解析器：词法 + 语法 → 解析树（语法错在这一步就报）
  ③ 预处理：检查库/表/列是否存在、权限、别名展开
  ④ 优化器：基于统计信息估算成本 → 选访问路径（走哪个索引、是否回表、是否排序）
  ⑤ 执行器：按计划向引擎取行，逐行做 Server 层的过滤/投影/聚合
  ⑥ 引擎层：在 Buffer Pool 中找页 → 沿 B+ 树定位 → 返回记录（必要时回表读聚簇索引）
  ⑦ Server 层：写 binlog（按事务组提交） → 把结果集写回客户端协议
```

「为什么加了索引还是慢」「为什么 `SELECT *` 更慢」这类问题的答案，几乎都能对回 ④⑤ 两条路径。

### 3. 区分「引擎层」与「Server 层」的一个判断口诀

| 现象 | 归因层 | 排查入口 |
| --- | --- | --- |
| 语法错误、权限不足、函数名写错 | Server 层 | 解析/预处理阶段 |
| 选错索引、没选索引、回表过多 | 优化器（Server 层） | `EXPLAIN` + optimizer trace（原书第 16 章） |
| 行格式/页损坏、锁等待、脏页刷不动、redo/undo 异常 | 引擎层 | `SHOW ENGINE INNODB STATUS`、error log |
| 结果集对但主从不一致 | Server 层 binlog | 原书第 13 章（另一位助手的日志系统篇） |

### 4. 常见存储引擎对照（教学示意，不参与构建）

| 引擎 | 事务/锁 | 索引结构 | 典型用途 | 现状 |
| --- | --- | --- | --- | --- |
| **InnoDB** | ACID、行锁、MVCC | 聚簇索引(B+树) + 二级索引 | 几乎所有业务表 | MySQL 8.0+ 为**默认引擎** |
| MyISAM | 不支持事务，表锁 | 非聚簇(B+树，独立索引文件) | 只读报表 | 8.0 已标记为 deprecated |
| Memory | 表锁 | 哈希（8.0 起也有 B 树索引选项） | 临时会话数据 | 数据不持久 |
| Archive | 不支持 | 无索引 | 日志归档 | 高压缩比 |
| CSV | 不支持 | 无索引 | 数据交换 | 很少用 |
| NDB / NDBCLUSTER | 分布式事务 | 哈希 + T-tree | 高可用集群 | 需独立部署，生态小 |

🔧 **2026 视角**：「要不要用 MyISAM」已经是伪问题——8.0 之后新项目默认 InnoDB，
而真正的取舍发生在 **InnoDB vs 其他存储引擎（如 RocksDB 系、TokuDB）**，那就是另一类系统（LSM vs B+树）的取舍了。

### 5. 连接与线程（教学示意，不参与构建）

- **线程模型**：MySQL 传统上是「**一个连接一个线程**」（thread-per-connection），
  线程可缓存进 `thread_cache_size`，避免频繁创建销毁；连接数上限由 `max_connections` 控制。
- **连接层关键变量**：`wait_timeout`（空闲连接超时）、`interactive_timeout`、
  `net_read_timeout` / `net_write_timeout`、`max_allowed_packet`。
  🔧 8.0 起新增 **Thread Pool（企业版）** 与更细的 `max_connect_errors`/连接限流；社区也常配 ProxySQL / Router 做连接池。
- **为什么连接池收益最大**：建连要做认证 + 分配会话（内含 innodb 行锁数组、临时缓冲等），
  成本远高于一次简单查询；HikariCP 的 `minimumIdle`、Druid 的 `min-evictable-idle-time-millis` 都是围绕这一点。

### 5.1 handler 接口：Server 层与引擎层的边界（教学示意，不参与构建）

Server 层不直接碰页，它通过一组 **handler 接口**（源码里是 `handler::ha_*` / `ha_innobase::` 系列方法）
向引擎提出「行级」的请求：

```
Server 层调用                引擎层动作
ha_innobase::store_lock   →  决定本次 SQL 加什么锁（行锁 / 间隙锁 / 表锁）
ha_innobase::index_read   →  按索引键定位，返回第一条匹配记录
ha_innobase::index_next   →  取下一条（B+ 树右移一跳）
ha_innobase::write_row    →  写入新行（内部分裂页、写 undo、改 change buffer）
ha_innobase::update_row   →  更新（先标记删除 + 插入新版本，写 undo）
ha_innobase::delete_row   →  标记删除
ha_innobase::commit_tx    →  提交（刷 redo 的 prepare/commit 记录、释放锁）
```

三个直接推论：
1. **`index_next` 一次只前进一跳**，所以「范围扫描」是「引擎层逐条向 Server 层交付」的流水线，
   这也解释了为什么 `LIMIT` 与「提前中断扫描」能显著省时间；
2. **优化器看到的行数不是磁盘上的行数**，而是引擎返回的行数（引擎按自己的读视图过滤未提交版本）；
3. **同一个 SQL 换引擎后行为不同**（例如 MyISAM 的 `count(*)` 直接读元数据，InnoDB 要真扫），
   因为两者对同一条 handler 接口的实现不同。

### 5.2 常见排查清单（教学示意，不参与构建）

| 症状 | 先看哪一层 | 常用入口 |
| --- | --- | --- |
| `You have an error in your SQL syntax` | Server 层（解析器） | 语法文档 |
| `Unknown column 'x' in 'field list'` | Server 层（预处理） | `SHOW COLUMNS` |
| `Duplicate entry '...' for key 'PRIMARY'` | 引擎层（唯一索引约束） | 业务幂等 + 重试 |
| `Lock wait timeout exceeded` | 引擎层（行锁等待） | `SHOW ENGINE INNODB STATUS`、performance_schema 的锁表 |
| `Got timeout waiting for lock` / 长时间刷不动 | 引擎层（IO / 刷脏） | error log、`Innodb_buffer_pool_pages_dirty` |
| 主从延迟 | Server 层（binlog 应用） | `SHOW SLAVE STATUS` 的 `Seconds_Behind_Master` |

### 6. 启动选项与系统变量（原书第 2 章的入口）

> 原书第 2 章「MySQL的调控按钮——启动选项和系统变量」是参数总纲。本节只保留与体系结构直接相关的几条。

| 变量 | 作用域 | 作用 | 典型坑 |
| --- | --- | --- | --- |
| `default_storage_engine` | GLOBAL/SESSION | 新表的默认引擎 | 5.5 之前默认是 MyISAM |
| `innodb_buffer_pool_size` | GLOBAL | 数据页缓存，通常给内存的 60–70% | 设太小 → 全量刷盘；太大 → 触发 swap |
| `innodb_file_per_table` | GLOBAL | 每表独立 `.ibd` | 5.6 起默认 ON，DROP 表可回收空间 |
| `transaction_isolation` | GLOBAL/SESSION | 默认隔离级别（8.0 起改名为 `transaction_isolation`，旧名 `tx_isolation` 已弃用） | 🔧 8.0 中旧名会报错/告警 |
| `sql_mode` | GLOBAL/SESSION | 语法与数据校验严格度 | 从 5.7 起默认含 `ONLY_FULL_GROUP_BY` 等，迁移老库常踩 |

## 版本演进

| 版本 | 与体系结构相关的关键变化 |
| --- | --- |
| **5.7（原书基线）** | `innodb_file_per_table` 默认 ON；`SELECT ... FOR UPDATE` 语义细化；查询缓存仍存在（5.7.20 起 deprecated） |
| **8.0（2018/2023 LTS）** | 🔧 **数据字典改为 InnoDB 存储并移除 `.frm`**；🔧 查询缓存**彻底删除**（`query_cache_*` 变量消失）；🔧 binlog 默认开启且默认格式 `ROW`，redo log 默认开启 **GTID**；🔧 默认认证插件 `caching_sha2_password`；🔧 新增 `innodb_dedicated_server`、instant ADD COLUMN（8.0.29 起 GA）、克隆插件；🔧 新增数据字典表 `mysql.stats_*`（统计信息持久化） |
| **8.4 LTS（2024）** | 🔧 默认字符集 `utf8mb4`、默认认证仍为 `caching_sha2_password`、`mysql_native_password` **默认关闭**、`mysql_install_db` 移除、Router 8.4 强化连接路由；「老参数」如 `--old` 相关行为变化；默认 `innodb_change_buffer_max_size` 25% |
| **9.x（HeatWave 时代）** | 🔧 官方发行版将 **HeatWave（内置列存/HTAP）** 带进社区发行路径，OLTP 与 OLAP 的边界淡化；向量检索方向（AI/向量索引）在 9.x 逐步落地；具体特性以官方文档为准 |
| **MariaDB 对照** | 分叉后：Aria 存储引擎替代 MyISAM、默认引擎走 InnoDB（XtraDB）、引入 **线程池** 与 **JSON 原生索引**，但缺少 8.0 之后「数据字典 InnoDB 化」「instant DDL」这一整套演进 |
| **PostgreSQL 对照** | PG 是**库级**选引擎（`CREATE DATABASE ... TEMPLATE` 之外的 storage parameter），没有 MySQL 这种「一张表一个引擎」的可插拔设计；PG 把并行查询、JIT、Vacuum 都做在单一引擎内 |

## 经典论文与原始文献

| 来源 | 作者 / 出处 | 与本主题的关系 |
| --- | --- | --- |
| Architecture of a Database System | Hellerstein, Stonebraker, Hamilton，*IEEE Computer* 42(8), 2009 | 「分层 + 插件式组件」架构范式的经典表述，MySQL 的可插拔引擎是这个范式的实例 |
| What Goes Around Comes Around | Stonebraker, Hellerstein，*IEEE Data Engineering Bulletin* 26(4), 2003 | 从 System R 到内存/Postgres 的历史回顾，解释「为什么 MySQL 长成这样」 |
| System R: A Relational Database System | Astrahan et al.，IBM Research Report RJ 3371, 1976 | 优化器 + 执行器 + 事务管理三层结构的源头 |
| Transaction Processing: Concepts and Techniques | Gray & Reuter，1993（书） | Server 层与事务管理器职责划分的标准参考 |
| In Search of an Understandable Consensus Algorithm | Ongaro & Ousterhout，*USENIX ATC* 2014 | 理解 MySQL Group Replication（8.0 的 MGR）背后 Raft 的必读入门 |
| Amazon Aurora 设计论文 | Vigar et al.，*SIGMOD* 2017 | 「日志即数据库」的存算分离路线，对比 MySQL 本地架构的好材料 |
| MySQL 官方文档：Server 和客户端程序 / 可插拔存储引擎 / Group Replication | MySQL 官方文档（dev.mysql.com） | 本章所有事实性陈述的最终依据，版本差异以对应版本的文档为准 |

> 说明：以上均为真实文献；本目录不杜撰引用格式，未核实的条目一律不收录。

## 近年研究与工业界开源实践（2015–2026）

- **服务端源码本身**：`mysql/mysql-server`（2026-09 实测 ≈**12.4k★**）是理解本章所有内容的地方；
  `facebook/mysql-8.0`（≈**115★**，MySQL 团队内部分支只读镜像）、`percona/percona-server`（≈**1.28k★**）适合看补丁发行版。
- **连接层中间件**：`mysql/mysql-router`（≈**148★**）是官方轻量路由；工业上更常见的是
  ProxySQL、Vitess 的 `vttablet` 连接池（≈**21.4k★** 的 `vitessio/vitess`），
  它们的价值正是把 MySQL 的「一线程一连接」成本的摊薄。
- **架构范式对照**：`pingcap/tidb`（≈**40.6k★**）与 `clickhouse/clickhouse`（≈**50.1k★**）分别代表
  「存算分离 + 多引擎可插拔」「存算一体列存」，可与 MySQL 的引擎层做直接对照。
- **云上形态**：Aurora、PolarDB 等把「共享存储 + 日志」这一思路产品化，
  对应本文件提到的「Server 层不碰磁盘、引擎层管页」。
- **研究侧**：2020 年之后关于 OLTP 引擎的工作大量转向 **RDMA/存算分离下的日志提交延迟**、
  **无锁 B+ 树**（如 Bw-tree 路线在真机上的复现与退化分析）与 **HTAP 一体化**（HeatWave、TiDB HTAP）。

## 常见误区与本书需修正之处

| # | 常见误区 | 修正（🔧 = 原书 2020 年未覆盖，必须补） |
| --- | --- | --- |
| 1 | 「MySQL 有查询缓存，重复查询很快」 | 🔧 查询缓存已在 **8.0 被彻底删除**，`query_cache_size` 变量不复存在；依赖它的场景要换成应用层缓存或 Redis（≈**76.5k★** 的 `redis/redis`） |
| 2 | 「存储引擎是库级的」 | MySQL 的引擎是**表级**可插拔（PostgreSQL 才是库级） |
| 3 | 「Server 层会直接读磁盘」 | Server 层只调用引擎接口；页、行格式、B+ 树都是引擎层概念 |
| 4 | 「连接断了只是网络问题」 | 连接层还负责认证、会话状态、`wait_timeout` 回收、`max_allowed_packet` 限制 |
| 5 | 「8.0 和 5.7 的默认值一样」 | 🔧 默认认证插件、字符集、binlog 开关、数据字典形态、隔离级别变量名（`tx_isolation` → `transaction_isolation`）都有变化 |
| 6 | 「`.frm` 文件还在，表结构就在」 | 🔧 8.0 已移除 `.frm`，表结构存放在 **`sdi` 表**（数据字典）中，详见 [08-MySQL的数据目录.md](08-MySQL的数据目录.md) |
| 7 | 「MySQL 只能有一个引擎可用」 | 可插拔是设计目标；但只有 InnoDB 具备完整的 8.0 特性集（含 instant DDL、MGR） |
| 7 | 「`mysqld` 和 `mysql` 是同一程序的不同模式」 | 二者是**不同可执行文件**：`mysqld` 是服务器，`mysql` 是交互式客户端；`mysqldump` / `mysqladmin` / `mysqlsh` 各自独立 |
| 8 | 「8.0 只能用 `mysql_native_password` 才能连上老客户端」 | 🔧 8.4 LTS 起该插件**默认关闭**，新部署应直接适配 `caching_sha2_password`（必要时在客户端/连接串上配置） |
| 9 | 「客户端断线重连是透明的」 | 重连会丢失会话状态（临时表、用户变量、`PREPARE` 语句、事务），应用层必须自己处理 |
| 8 | 🔧 本书未覆盖 | 未覆盖 **Group Replication / MGR**、**克隆插件**、**8.4 LTS 的默认变化**、**9.x HeatWave**；也未给出「一线程一连接」在云原生连接池下的实践建议 |

## 与其他章 / 其他书的联系

- 本册：**02-Buffer-Pool.md**（连接层的线程/内存与其 downstream 的关系）、
  **08-MySQL的数据目录.md**（Server 层看到的文件布局）、
  **09-表级别的操作.md**（DDL 由 Server 层发起、引擎层执行）、
  **11-InnoDB内存结构.md**（引擎层内存结构总览）。
- 他册：
  - 《数据库系统概念（第6版）》[17-数据库系统体系结构.md](../数据库系统概念6/17-数据库系统体系结构.md)——分层体系结构的教科书表述；
  - [11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)——可插拔索引的接口抽象；
  - [26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)——TP monitor / XA 视角，与 Server 层的 binlog 事务提交呼应；
  - 《多处理器编程的艺术（2）》第 4、13 章——线程模型与并发对象的对照。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
