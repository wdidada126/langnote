# 第 8 章 数据的家——MySQL 的数据目录与文件布局

> **原书位置**：第 8 章「数据的家——MySQL的数据目录」，对号章节。原书基于 **MySQL 5.7.22**。
>
> **一句话**：数据目录（`datadir`）是**MySQL 与操作系统之间唯一的约定**：
> 库是目录、表是文件、系统信息在 `mysql` / `sys` / `performance_schema` 这几个库里；
> 🔧 而 8.0 起「表结构」不再是 `.frm` 文件，而是 InnoDB 表（`sdi`）——**这是本书与最新版本之间最大的物理差异**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 datadir 的位置与结构 | `datadir` 下的目录即「库」，库下的文件即「表/索引/日志」 | 备份与迁移的最小单元是「整个目录」或「单文件表空间」 |
| 8.2 系统库 | `mysql`（权限/统计/字典相关）、`sys`、`performance_schema`、`information_schema` | `information_schema` 是只读视图，`performance_schema` 是运行时探针 |
| 8.3 表定义文件的两代形态 | 5.7 是 `库/表名.frm`；🔧 8.0 是 `库/#tablespace1.ibd` 内含 `sdi` 记录 | 8.0 之后「删掉 .frm 也能看到表结构」成为历史 |
| 8.4 表空间文件 | 独立表空间 `.ibd`（默认）、系统表空间 `ibdata1`、临时表空间、undo 表空间（🔧 8.0 独立化）、通用表空间 | 知道文件里装什么，才知道备份与空间回收怎么做 |
| 8.5 日志类文件 | redo `ib_logfile*` / `undo_001*`、binlog、error log、slow log、general log | 物理备份要格外小心 redo/binlog 的一致性 |
| 8.6 目录结构与权限 | 属主必须是运行 `mysqld` 的用户；`datadir` 权限决定实例能否启动 | 容器/挂在卷最常踩的就是权限与 SELinux |
| 8.7 跨版本迁移的坑 | 5.7→8.0 的目录不兼容（字典格式变了） | 不能直接拷目录升级，要用 `mysqldump`/逻辑迁移或官方 in-place 升级路径 |
| 8.8 🔧 8.0+ 的变化清单 | 无 `.frm`、`sdi`、undo 独立、doublewrite 可独立、`ibdata1` 内容大幅减少 | 「`ibdata1` 只装什么」这个问题在 8.0 之后才有明确答案 |
| 8.9 时间与时区 | 墙上/单调时钟、`NOW()` vs `SYSDATE()`、`TIMESTAMP`/`DATETIME` 选型、三处时区与 `mysql.time_zone*` | 「时间」散落在时钟源、列类型、系统表三处，是数据不一致的头号来源 |
| 8.10 日志里的时间戳 | binlog `exec_time` 是**执行耗时**而非事件时间；慢日志 `Start:` 与 `Query_time` 分别取自墙上/单调时钟 | 做审计/回溯要用业务字段与 GTID，不要用 `exec_time` |

## 核心精讲

> 以下均为**教学示意，不参与构建**：本目录不搭建真实实例，示例只用于对齐概念，请勿直接执行。

### 1. 数据目录的树形结构（教学示意，不参与构建）

```
/var/lib/mysql/                          ← datadir
├── ibdata1                   系统表空间（5.7：含字典/change buffer/早期 undo；8.0：doublewrite 等）
├── ib_logfile0 / ib_logfile1  redo log（8.0 起文件名带序号，如 ib_logfile0/ib_logfile1）
├── mysqld-bin.000001           binlog（8.0 默认开）
├── sys/  mysql/  performance_schema/
│   ├── db.opt（5.7：库的字符集定义；8.0 已改为字典表）
│   └── ...
├── yourdb/
│   ├── t.ibd                  独立表空间（8.0 起内含 sdi 表结构记录）
│   ├── t.frm                  🔧 5.7 的旧形态；8.0 已移除
│   └── t_2.ibd                子分区/子表（分区表时）
├── undo_001 / undo_002        🔧 8.0 起的独立 undo 表空间
└── errors.log / slow.log      运维日志（由 log_error、slow 相关配置决定）
```

### 2. 表定义文件的两代形态（教学示意，不参与构建）

| 版本 | 表结构存在哪 | 能否用文本编辑器看 | 风险 |
| --- | --- | --- | --- |
| 5.7 | `库/表名.frm`（二进制，但可 `strings` 出列名） | 勉强 | 手工改 .frm = 破坏实例 |
| 8.0+ | 表空间的 `sdi` 页 + 数据字典表 | 不能 | 手工改文件 = 数据字典与表空间不一致 |

推论：**8.0 之后不能再靠「删库目录下的文件」这种土办法搬表**；
正确做法是 `mysqldump` / 克隆插件 / 逻辑导入。这也是 8.0 数据字典事务化带来的必然而非偶然。

### 3. 各文件「装的是什么」（教学示意，不参与构建）

| 文件 | 装什么 | 何时会膨胀 |
| --- | --- | --- |
| `.ibd` | 表的数据页 + 索引页 + 🔧 `sdi` 表结构 | 数据增长、页分裂碎片 |
| `ibdata1` | 5.7：change buffer / doublewrite / 早期 undo；🔧 8.0：doublewrite、change buffer（可回收） | 历史版本回滚段导致 |
| `ib_logfile*` | redo log，固定大小循环写 | 不膨胀，但太小会频繁 checkpoint |
| `undo_*` | undo 日志（历史版本）🔧 8.0 起默认独立成文件 | 长事务导致版本堆积 |
| `binlog` | 逻辑变更日志（ROW 模式下是行影像） | 不清理就一直涨（需 `PURGE BINARY LOGS`） |

### 4. 系统库各自的职责（教学示意，不参与构建）

| 库 | 角色 | 可否删除 | 典型用途 |
| --- | --- | --- | --- |
| `mysql` | 用户/权限/资源组/统计信息/（8.0 起字典相关表） | 不可 | `SHOW GRANTS`、`GRANT`、加密表 |
| `performance_schema` | 运行时探针（等待事件、锁、IO） | 可（不推荐） | 定位锁等待、IO 瓶颈 |
| `information_schema` | **只读元数据视图**（由字典动态生成） | 不可 | `information_schema.tables` 的统计用法 |
| `sys` | 用视图拼出的可读诊断脚本 | 官方建议不删 | `sys.session`、`sys.host_summary` 等 |

注意：`information_schema` 里看到的行数/长度是**估算或采样值**，不等于磁盘真实占用；
真要精确值要用 `SHOW TABLE STATUS` 或 `information_schema.FILES`（与 `innodb_table_stats` 的持久化口径不同）。

### 5.1 目录结构与「独立表空间」的取舍（教学示意，不参与构建）

| 方案 | 优点 | 代价 |
| --- | --- | --- |
| 全部独立表空间（默认） | 单表可回收、可单独搬动、便于逻辑备份 | 文件数多，元数据开销大 |
| 共享系统表空间 | 文件少 | `ibdata1` 只增不减，DROP 表不回收空间 |
| 通用表空间（`CREATE TABLESPACE`） | 多表一个文件，便于批量管理 | 回收仍需整体重建 |

### 6.1 目录权限与启动（教学示意，不参与构建）

```
datadir 及其所有者、权限必须与启动 mysqld 的用户一致
   ├─ 「Permission denied」→ 常见是挂载卷后属主变成 root
   ├─ SELinux / AppArmor → 容器里常见「磁盘权限被策略拦住」
   └─ 磁盘满（df 与 du 不一致）→ 常有被删未释放的 binlog/临时文件
```

### 6. 备份视角下的目录（教学示意，不参与构建）

| 备份方式 | 用到哪些文件 | 一致性来源 |
| --- | --- | --- |
| 逻辑备份（`mysqldump`） | 表数据（SQL 语句） | 事务一致性靠 `--single-transaction`（InnoDB） |
| 🔧 物理备份（克隆插件） | 整个 datadir 的页 | 在线克隆时先建本地实例再拉页 |
| 第三方物理备份（如 XtraBackup 类工具） | `.ibd` + redo + binlog 位点 | 备份期间持续复制 redo 并重放 |
| 冷拷贝目录 | 全部文件 | ❌ 运行中拷贝会拿到不一致的页 |

> 🔧 官方**克隆插件**（MySQL 8.0.17+ 起 GA）是「在线物理备份 + 快速搭建副本」的标准答案，
> 它把「一致性」问题从 DBA 的手工操作变成了数据字典层的功能。

### 6.0 目录里的「隐藏客人」（教学示意，不参与构建）

除表文件与日志外，`datadir` 下还有一些容易被忽略、却会直接影响可维护性的东西：
临时表空间（排序/临时表溢出）、`binlog index` 与 `binlog xxx.index`（binlog 的坐标文件）、
以及 pid/socket 文件。它们同样占空间、也需要纳入监控与备份范围。

### 6.1 数据目录相关的运维清单（教学示意，不参与构建）

| 任务 | 涉及的目录/文件 | 注意事项 |
| --- | --- | --- |
| 增加磁盘 | 改 `datadir` 目录（停机）或加独立表空间文件 | 改 `datadir` 必须干净关闭后操作 |
| 清理膨胀 | `PURGE BINARY LOGS`、清理旧 undo/临时文件 | binlog 清理前确认从库已消费 |
| 迁移单库 | `mysqldump` / 克隆插件 / 分区 `REORGANIZE` | 🔧 8.0 起不要靠「拷目录」搬表 |
| 排查磁盘满 | `df` vs `du`、被删未释放的文件、`/tmp` 临时空间 | 先看是否有 mysqld 打开着已删除的大文件 |
| 多实例 | 每个实例独立 `datadir` 与 socket/pid 路径 | 避免共用 socket 文件导致连错实例 |
| 只读从库 | `datadir` 的文件所有权与 `read_only` | 只读仍需要写 redo/字典，除非是极严格的离线副本 |

### 6.2 文件与权限的最短排障路径（教学示意，不参与构建）

```
「Can't get charset of 'xxx''」 / 「Can't open file: './db/t.frm'」 类的错误
   → ① datadir 权限/属主 ② SELinux/AppArmor ③ 磁盘配额 ④ 表文件是否真的存在
   → ⑤ 8.0 上还要注意：表文件是 .ibd（含 sdi），不是 .frm
```

### 9. 数据目录里的「时间维度」（教学示意，不参与构建）

> 本小节是把原书未成章的「时间」主题按「落点在哪些文件/系统表」归并到数据目录下。
> 完整版见 [X1-时间追踪专题.md](X1-时间追踪专题.md)。以下结构示意与 `--` 片段**均未在本机编译、未连接任何实例执行**。

**(1) 两种时钟：展示用墙上时钟，计时用单调时钟**

| 用途 | 时钟源 | 出现在 |
| --- | --- | --- |
| 展示「什么时候」 | 墙上时钟（`gettimeofday` / `CLOCK_REALTIME`，可被 NTP 回拨） | 慢日志 `Start:`、错误日志时间戳、`SHOW PROCESSLIST` 的 `Time` |
| 计算「耗时多久」 | 单调时钟（`CLOCK_MONOTONIC`，只增不减） | 慢日志 `Query_time`、`long_query_time` 的比较对象、`performance_schema` 的 `TIMER_*` |

推论：`long_query_time` 与 `Query_time` 基于单调时钟，所以**时钟被回拨也不会出现负耗时**；
一旦慢日志出现异常巨大的 `Query_time`，先怀疑墙上时钟被改动过。

**(2) `NOW()` 与 `SYSDATE()`：复制语义差一个字**

| 函数 | 取值时点 | 在 binlog 里的命运 |
| --- | --- | --- |
| `NOW()` / `CURRENT_TIMESTAMP` | **语句开始时刻**，语句内固定 | ROW 格式下会被具体化为实际写入值 → 主从一致 |
| `SYSDATE()` | 真实调用时刻 | STATEMENT 格式下**不具体化** → 主从可能得到不同结果 |

工程建议：业务代码**不在 SQL 里算时间**，由应用层传入明确值，既避开复制语义坑，也便于测试冻结时间。

**(3) 列类型选型：`TIMESTAMP` 与 `DATETIME`（教学示意，不参与构建）**

| 维度 | `TIMESTAMP` | `DATETIME` |
| --- | --- | --- |
| 存 | 4 字节（+小数位），**存 UTC、读时按会话时区渲染** | 5 字节（+小数位），原样存取 |
| 范围 | `1970-01-01 00:00:01` ~ **`2038-01-01 03:14:07`** | `1000-01-01` ~ `9999-12-31` |
| 隐式规则 | 🔧 `explicit_defaults_for_timestamp=OFF`（5.7 默认）时，`TIMESTAMP NULL` 会被偷偷改写成 `NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 无 |

- ⚠️ **2038 问题至今未解决**：MySQL 至今未把 `TIMESTAMP` 放宽到 64 位。**2026 年新建表请默认用 `DATETIME` 或 `BIGINT` 毫秒**。
- 「UPDATE 之后时间字段莫名变了」的第一排查项就是这个隐式规则。

**(4) 三处时区与 `mysql.time_zone*` 系统表（呼应 8.2）**

```
system_time_zone   ← 启动时从 OS 继承，只读
time_zone          ← global / session / persist，MySQL 真正用来换算的
   ├─ 'SYSTEM'                 跟随 system_time_zone
   ├─ 'Asia/Shanghai'          具名时区，读 mysql.time_zone_name 等表
   └─ '+08:00'                 偏移字符串，不依赖系统表
```
- 🔧 8.0 起 `SET PERSIST time_zone='+08:00'` 会把时区写进 `mysqld-auto.cnf`，重启不丢（5.7 只能改 `my.cnf`）。
- 具名时区依赖 `mysql.time_zone*` 这组系统表；**这组表被误删或未初始化时，具名时区会退化为偏移字符串**，表现为「时区静默变了」。

**(5) 日志里的时间戳（呼应 8.5 的日志类文件）**

- binlog `QUERY_EVENT` 头部的 4 字节 `exec_time` 是**语句执行耗时差**，**不是**「这条记录发生的时间」——用它做审计是错误用法。
- 慢日志的 `Start: timestamp` 是墙上时钟，`Query_time: 0.003512` 是单调时钟之差；两者不是同一维度，不要相减。
- 时间相关故障速查：

| 现象 | 先查什么 |
| --- | --- |
| 主从数据不一致 | 两侧 `@@global.time_zone` / `@@session.time_zone` 是否一致、列是不是 `TIMESTAMP` |
| 报表「当天少了一小时」 | 应用层时区与库时区是否对齐，边界行被算到前后一天 |
| 恢复后时间点对不上 | 逻辑备份（SQL 时间戳已固化）还是克隆/binlog（物理时间点） |

## 版本演进

| 版本 | 关键变化 |
| --- | --- |
| **5.7（原书基线）** | 表结构在 `.frm`；`ibdata1` 承载 change buffer、doublewrite、回滚段；`db.opt` 存库字符集；`mysql_install_db` 初始化 |
| **8.0** | 🔧 **移除 `.frm`**，改用 InnoDB 存储的数据字典 + 每个表空间的 `sdi` 表；🔧 `mysql_install_db` 移除，改为 `mysqld --initialize(--insecure)`；🔧 **undo 表空间默认独立**（`innodb_undo_tablespaces`）；🔧 **克隆插件**可用；🔧 统计信息持久化到 `mysql.stats_*`；🔧 新增 `mysql.*` 中若干字典表 |
| **8.4 LTS** | 🔧 默认字符集 `utf8mb4`、默认认证 `caching_sha2_password`；`mysql_install_db` 彻底移除（8.4 起）；相关工具链随之调整 |
| **9.x** | 🔧 数据字典与克隆能力继续演进；热元数据（如原子 DDL）在 8.0 基础上继续收敛 |
| **MariaDB / PostgreSQL 对照** | MariaDB 的 `.frm` 演化为 `aria_log` / 其字典实现不同，且仍保留 `.frm` 兼容层；PostgreSQL 用 `pg_catalog` 系统表 + `base/<oid>/<filenode>` 目录布局，字典与数据目录是**同一套事务机制**管理的（这也是 PG 能用单事务改结构的原因） |

## 经典论文与原始文献

| 来源 | 作者 / 出处 | 与本主题的关系 |
| --- | --- | --- |
| Mohan 等，*ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollback* | *SIGMOD* 1992 | 「字典/表结构的修改也必须可回滚」，8.0 数据字典事务化的理论背景（本目录此前误记为 R. Hagmann，现已更正） |
| The Transaction Concept: Pragmatic Full Strength Transaction Support | J. Gray，1977 / 收录于《Readings in Database Systems》 | 系统表与用户数据统一管理思想的源头 |
| MySQL 官方文档：Data Directory Structure / Data Dictionary / `sdi` / Tablespace / Removed Features in 8.0 | MySQL 官方文档 | 本章文件清单与版本差异的最终依据 |
| Oracle 官方文档：Data Dictionary 与 Tablespaces | Oracle 官方文档 | 与 MySQL 数据字典布局的对照 |
| PostgreSQL 官方文档：Tablespaces、System Catalogs | PostgreSQL 官方文档 | 系统目录即普通表的另一种实现 |
| SQLite 官方文档：Database File Format | SQLite 官方文档 | 「整个数据库就是一个文件」的极端形态 |

## 近年研究与工业界开源实践（2015–2026）

- **`percona/percona-xtrabackup`（2026-09 实测 ≈1.56k★）**：物理热备的事实标准工具，
  它正是靠「复制 `.ibd` + 追 redo + 记录 binlog 位点」来做一致快照，与本文件第 6 节的表格互相印证。
- **`mysql/mysql-server`（≈12.4k★）**：数据字典相关实现集中在 `storage/innobase/dict/`，
  `sdi` 的序列化逻辑在 `storage/innobase/sdi/`；克隆插件在 `plugin/clone/`。
- **`vitessio/vitess`（≈21.4k★）**：把 MySQL 当成「可水平扩展的存储单元」，
  它的备份/恢复（`vitestreaming`、备份到对象存储）正是围绕「datadir 里的文件语义」展开。
- **`pingcap/tidb`（≈40.6k★）**：逻辑上「一个 KV 空间 = 一个 MySQL 实例」，
  用 `information_schema` 兼容层向上提供 MySQL 元数据视图——是很直观的「数据目录抽象」对照。
- **运维要点**：大实例上 `du` 与 `information_schema.tables` 的口径差异、binlog 未清理导致的磁盘满、
  以及 `/tmp` 临时表空间溢出，是「数据目录相关问题」里最常见的三类。

## 常见误区与本书需修正之处

| # | 常见误区 | 修正（🔧 = 原书出版时未覆盖） |
| --- | --- | --- |
| 1 | 「表结构在 `.frm` 文件里，拷走就能用」 | 🔧 8.0 已无 `.frm`，表结构在表空间的 `sdi` 中 |
| 2 | 「5.7 的 datadir 可以原地拷到 8.0 上」 | 🔧 字典格式不兼容，需按官方升级路径（原地升级工具/`mysqldump`/克隆） |
| 3 | 「`ibdata1` 越来越大的原因和以前一样」 | 🔧 8.0 之后它不再放 undo，膨胀原因变了（change buffer / doublewrite / 历史回滚段） |
| 4 | 「`information_schema` 的行数就是表大小」 | 那是估算；精确值要看 `SHOW TABLE STATUS` / `information_schema.FILES` |
| 5 | 「停服拷贝目录是最稳的备份」 | 运行中拷贝会拿到不一致页；停服也要先确保干净关闭（或flush+锁） |
| 6 | 🔧 本书未覆盖 | 原书基于 5.7.22，**未覆盖** `sdi`、数据字典事务化、undo 表空间独立化、克隆插件，以及 8.4 移除 `mysql_install_db` 带来的初始化流程变化 |
| 7 | 「`mysql` 库可以直接改表来改权限」 | `mysql.user` 等表在 8.0 之后被调整为视图/字典表混杂，直接用 SQL 改权限已不安全，应走 `CREATE USER/GRANT/ALTER USER` |
| 8 | 「备份只要备份 `datadir` 里的 `.ibd`」 | 还需 redo/undo/binlog 位点信息；InnoDB 的 redo 与 binlog 里可能有未合并的变更 |
| 9 | 「`exec_time` 是记录发生的时间」 | 它是**执行耗时差**；审计要用业务时间字段或 GTID + binlog 位置 |
| 10 | 「`TIMESTAMP` 和 `DATETIME` 差不多」 | `TIMESTAMP` 存 UTC、按会话时区渲染、2038 溢出，且 5.7 下有隐式 `ON UPDATE` 规则 |
| 11 | 「慢日志 `Query_time` 可能为负」 | 它基于单调时钟；异常大值可能来自时钟回拨，负值不该出现 |

## 与其他章 / 其他书的联系

- 本册：**03-数据页长什么样.md**（页是文件的内容）、**09-表级别的操作.md**（CREATE/DROP/ALTER 与文件的关系）、
  **10-InnoDB的表结构.md**（字典表细节）、**11-InnoDB内存结构.md**（change buffer 落在系统表空间）、
  **X1-时间追踪专题.md**（本文件 8.9/8.10 的时间主题的独立展开）、
  **X2-日志系统专题.md**（binlog 与 redo 的协作）、**12-基于成本的优化.md**（数据目录里读到的统计信息是成本的燃料）。
- 他册：《数据库系统概念（第6版）》[10-存储和文件结构.md](../数据库系统概念6/10-存储和文件结构.md)（文件组织与目录结构）、
  [16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)（redo/undo 与恢复过程）、
  [17-数据库系统体系结构.md](../数据库系统概念6/17-数据库系统体系结构.md)。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
