# InnoDB 的表结构——内部数据字典与「表到底记了什么」

> **原书位置**：主题对应第 8 章「数据的家」与第 9 章「存放页面的大池子——InnoDB的表空间」中涉及表定义存放的部分；
> 本文件名沿用任务映射表 `10-InnoDB的表结构.md`。原书基于 **MySQL 5.7.22**。
>
> **一句话**：InnoDB 启动时必须先把「这张表长什么样」读进内存，这些描述就叫**数据字典**；
> 5.7 里它是一组 `SYS_*` 表，🔧 8.0 里它被改造成事务化、可回滚、与表数据同源的 InnoDB 表（`sdi`），
> 这一改造是「原子 DDL」能成立的前提。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 为什么要数据字典 | 表定义、列定义、索引定义是「元数据」，但必须**持久且事务化** | 元数据与数据一致性 = 原子 DDL 的地基 |
| 10.2 5.7 的 `SYS_*` 字典表 | 表（SYS_TABLES）、列（SYS_COLUMNS）、索引（SYS_INDEXES）、索引列（SYS_FIELD_COLS）、表空间、外键 | 字典本身就是**行记录**，存在 InnoDB 表里 |
| 10.3 表定义里「看不见」的列 | 隐藏列 `DB_TRX_ID`、`DB_ROLL_PTR`；无主键时的隐藏 `ROW_ID` | 每行都比你定义的列多 3–6 字节（这是 MVCC 的基础） |
| 10.4 字典缓存与字典锁 | 表定义首次访问时读字典并在内存中缓存；DDL 时换掉缓存 | 「第一次查询慢」常常是字典读 + 缓存未命中 |
| 10.5 联合索引在字典里怎么存 | 二级索引记录「索引列顺序 + 索引 id」，叶子指针指向主键 | 索引列顺序是「存储层事实」，不是 SQL 层的建议 |
| 10.6 🔧 8.0 的新形态 | `sdi` 存表结构；`mysql.tables` / `mysql.columns` / `mysql.indexes` 等字典表；字典 InnoDB 化 | 8.0 之后 `.frm` 彻底消失 |
| 10.7 字典与 `information_schema` | `information_schema` 的视图由字典动态生成 | 它是「视图」不是「表」，因此不能 `UPDATE` |
| 10.8 字典相关的坑 | 表缓存（`table_open_cache`）耗尽、字典不一致、`innodb_force_recovery` 下读字典 | 元数据问题常表现为「能连上但打不开表」 |

## 核心精讲

> 以下均为**教学示意，不参与构建**：本目录不搭建真实实例，示例只用于对齐概念。

### 1. 一张表在 InnoDB 里被拆成几份「描述」（教学示意，不参与构建）

```
「表」= 字典里的三条记录 + 表空间里的页
  ├─ SYS_TABLES      ：表名 / 表空间 ID / 列数 / 标志位（行格式、主键是否为聚簇等）
  ├─ SYS_COLUMNS     ：列号 / 列名 / 主类型 / 长度 / 是否可空 / 字符集
  ├─ SYS_INDEXES     ：索引 ID / 表名 / 是否唯一 / 类型（聚簇=PRIMARY） / 页号 / B+ 树根
  ├─ SYS_FIELD_COLS  ：索引 ←→ 列的对应关系（含列在索引里的顺序与前缀长度）
  └─ SYS_TABLESPACES ：表空间 ID ↔ 文件路径 / 大小
```

推论：**「建表」在 InnoDB 里就是往这几张字典表里 INSERT 几行**；
所谓「`CREATE TABLE` 很快」，本质上是「字典写入 + 分配一个段/若干页」这么快。

### 2. 隐藏列：你没定义的那几个字段（教学示意，不参与构建）

```
CREATE TABLE t (id BIGINT PRIMARY KEY, name VARCHAR(50));  -- 你定义了 2 列

InnoDB 实际存储的行 = id | name | DB_TRX_ID(6B) | DB_ROLL_PTR(7B)   (+ 主键前的隐藏 ROW_ID)
                             ↑ 事务 ID         ↑ 回滚指针
```

- `DB_TRX_ID`：修改该行的事务 ID，决定「谁有资格看到这个版本」；
- `DB_ROLL_PTR`：指向 undo 段里的旧版本，构成**版本链**（MVCC 的基础，见另一位助手的 21 章）；
- 这两列合计 13 字节，是 InnoDB「每行都比你写的多几字节」的直接原因。

### 3. 索引在字典里怎么被描述（教学示意，不参与构建）

```
PRIMARY  → SYS_INDEXES 里 type=聚簇，叶子 = 完整行（含隐藏列）
idx_name → SYS_INDEXES 里 type=二级，叶子 = (name, 主键值)
           SYS_FIELD_COLS 里记录：索引 idx_name 使用的列顺序 = [name]，前缀长度 = 全列
```

因此「联合索引 (a,b)」在字典里的信息只有一句：**先按 a 排、再按 b 排**。
这解释了为什么最左前缀规则不是「SQL 优化建议」，而是**存储层的物理事实**。

### 4. 字典缓存与「第一次查询慢」（教学示意，不参与构建）

```
进程启动 / 表首次被访问
   → 读取字典表相关行 → 在内存中构建「表定义对象」（列类型、索引、外键…）
   → 之后同一张表的访问直接用内存对象
DDL 之后 → 旧定义被标记作废 → 下一次访问重新加载
```

工程含义：
- 大量小表 → 表定义对象 + 表缓存会成为内存与打开文件的压力（`table_open_cache`）；
- DDL 频繁 → 每次都要重读字典并换缓存，这正是不利于高频 DDL 的原因之一。

### 5. 🔧 8.0 的字典形态（教学示意、以官方文档为准，不参与构建）

| 项 | 5.7 | 8.0+ |
| --- | --- | --- |
| 表定义载体 | `SYS_*` 字典表 + `.frm` 文件 | InnoDB 存储的数据字典 + 每个表空间的 `sdi` 记录 |
| DDL 原子性 | 无（失败可能留下不一致） | 🔧 **原子 DDL**，失败可回滚 |
| 可见性 | 字典表对用户基本不可见 | 🔧 提供 `mysql.tables`、`mysql.columns`、`mysql.indexes`、`mysql.index_column_usage`、`mysql.table_spaces` 等字典表供查询 |
| 崩溃恢复 | `.frm` 与表数据可能不一致 | 字典与数据同在 InnoDB 表中，用同一套 redo/undo 恢复 |

### 6. 观测（教学示意，不参与构建）

```sql
-- 只看元数据，属于只读信息收集，不构成构建步骤
SELECT table_name, table_rows, data_length FROM information_schema.tables
WHERE table_schema = 'mysql' ORDER BY data_length DESC LIMIT 10;
```

注意 `information_schema.tables.TABLE_ROWS` 在 InnoDB 下是**估算值**，
它不是 `SELECT COUNT(*)` 的结果，不能用于容量核算；精确值只能真数一遍。

### 6.1 字典、表缓存与「打不开表」类故障（教学示意，不参与构建）

```
现象                                 → 与字典/元数据的关联
「Table 't' doesn't exist」但实际在   → 字典里没有，或 catalog（表定义缓存）与文件不一致
重启后表结构变了                      → 有未提交的 DDL  Impacts（🔧 8.0 起不该发生）
表能连上、查表时报 "Incorrect key file" → 索引定义与页内容不匹配（页损坏或字典不一致）
information_schema 查不到新表        → 统计信息/字典表未刷新（ANALYZE 或等待后台刷新）
```

### 6.2 字典行数与表行数的区别（教学示意，不参与构建）

| 视角 | 看什么 | 用途 |
| --- | --- | --- |
| 逻辑 | `information_schema.tables`（由字典生成） | 结构核对、容量估算（估算值） |
| 物理 | `information_schema.FILES` / `SHOW TABLE STATUS` | 真实空间占用 |
| 存储 | 表空间里的 `sdi` 页 | 崩溃与恢复时的最终依据 |

记住一条：**字典是「写下来的真相」，表缓存是「读进内存的副本」；两者的差异只在 DDL 与崩溃后出现。**

### 6.3 列定义里那些「隐含参数」（教学示意、以官方文档为准，不参与构建）

```
CREATE TABLE t (
  id  BIGINT unsigned NOT NULL AUTO_INCREMENT,   -- unsigned 影响值域与 JOIN 比较
  ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
```

- `AUTO_INCREMENT` 值与自增行为（含 🔧 8.0 的「重启不回退」语义变化）都记在字典里；
- `UNSIGNED` 混用时比较可能触发隐式转换，从而让索引失效（见 07）；
- `DEFAULT CHARSET` 决定每个列的字符集 id，改字符集往往是重建级操作（见 09）。

## 版本演进

| 版本 | 关键变化 |
| --- | --- |
| **5.7（原书基线）** | `SYS_*` 字典表 + `.frm`；表定义改了文件，DDL 不保证原子 |
| **8.0** | 🔧 数据字典 InnoDB 化，`.frm` 移除；🔧 原子 DDL；🔧 `sdi` 存在于每个表空间的第一个页区；🔧 统计信息持久化（`mysql.stats_*`）；字典表对用户可查 |
| **8.4 LTS** | 🔧 默认值与工具链继续调整（移除 `mysql_install_db` 等），字典表的使用方式更规范 |
| **9.x** | 🔧 元数据管理与热 DDL 继续演进，以官方文档为准 |
| **MariaDB / PostgreSQL 对照** | PostgreSQL 的目录本身就是普通表（`pg_class` 等），所以 DDL 天然是事务；MariaDB 保留 `.frm` 兼容层，字典实现与 MySQL 8.0 分道扬镳 |

## 经典论文与原始文献

| 来源 | 作者 / 出处 | 与本主题的关系 |
| --- | --- | --- |
| ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollback | R. Hagmann，*SIGMOD* 1992 | 「元数据也是数据，也要走 redo/undo」的标准论证 |
| The Transaction Concept: Pragmatic Full Strength Transaction Support | J. Gray，1977 | 事务概念与其「用于系统目录」的原始主张 |
| MySQL 官方文档：Data Dictionary / Data Dictionary Tables / `sdi` / Atomic DDL | MySQL 官方文档 | 8.0 字典形态与原子 DDL 的权威说明 |
| MySQL 官方文档：`information_schema` 简介 | MySQL 官方文档 | 为什么它是视图、为什么给出的是估算值 |
| PostgreSQL 官方文档：System Catalogs | PostgreSQL 官方文档 | 「目录 = 普通表」的实现路线 |
| InnoDB 源码 `storage/innobase/dict/`、`storage/innobase/sdi/` | `mysql/mysql-server`（≈12.4k★） | 字典定义（`dict0mem.h`）与 `sdi` 序列化的位置 |

## 近年研究与工业界开源实践（2015–2026）

- **`mysql/mysql-server`（≈12.4k★）**：8.0 的字典与 `sdi` 实现集中在 `storage/innobase/sdi/` 与
  `storage/innobase/dict/`；原子 DDL 让「失败即回滚」成为默认语义。
- **`percona/percona-server`（≈1.28k★）**：发行版在字典、undo 与监控上的补丁，常可作为新特性的先行观察点。
- **`pingcap/tidb`（≈40.6k★）**：元信息（schema）单独存储并支持多版本快照 schema，
  由此实现「在线改表不加锁」——与 MySQL 8.0 的原子 DDL 是同一趋势的分布式版本。
- **`mysql/mysql-router`（≈148★）** 与 ProxySQL / Vitess 一类中间件：缓存并重写 SQL，
  也是「元数据一致性」的另一个视角（缓存的表定义如果落后，会产生诡异错误）。
- **工程要点**：`information_schema` 的估算值、`table_open_cache` 的命中率、
  以及「DDL 之后 `information_schema` 是否立刻反映新结构」这三个问题，是元数据类故障的高频来源。

## 常见误区与本书需修正之处

| # | 常见误区 | 修正（🔧 = 原书出版时未覆盖） |
| --- | --- | --- |
| 1 | 「我定义了 3 列，每行就存 3 列」 | 还有隐藏的 `DB_TRX_ID`、`DB_ROLL_PTR`（+ 无主键时的 `ROW_ID`） |
| 2 | 「`information_schema.tables.TABLE_ROWS` 是精确行数」 | InnoDB 下是估算值 |
| 3 | 「表定义改了就永久生效」 | 重启后仍生效 ≠ 未提交的 DDL 也生效；🔧 8.0 起 DDL 是原子的，失败会回滚 |
| 4 | 「字典在内存里，所以关机就没了」 | 表定义先落盘（5.7 的 `.frm` / 🔧 8.0 的 `sdi`）才有意义 |
| 5 | 🔧 本书未覆盖 | 原书基于 5.7.22，**未覆盖** 8.0 的 `sdi`、原子 DDL、字典表可见化，以及它们对 DDL 事故率的改变 |
| 6 | 「列类型只是声明」 | 它决定了隐藏列、行格式与页内布局；改列类型是重建级操作（见 09） |
| 7 | 「`information_schema` 可以当元数据表来 JOIN」 | 它是视图，且部分字段是估算值；用它做容量核算会得出错误结论 |

## 与其他章 / 其他书的联系

- 本册：**01-InnoDB与MySQL的架构.md**（Server 层如何用字典）、**08-MySQL的数据目录.md**（文件与 `sdi`）、
  **09-表级别的操作.md**（DDL 与原子性）、**10 的下篇 11-InnoDB内存结构.md**（字典缓存所在的内存在哪）。
- 他册：《数据库系统概念（第6版）》[17-数据库系统体系结构.md](../数据库系统概念6/17-数据库系统体系结构.md)（数据字典概念）、
  [14-事务.md](../数据库系统概念6/14-事务.md)、[16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)（元数据事务与恢复）。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜大纲版：[mysql是怎样运行的.md](mysql是怎样运行的.md)
