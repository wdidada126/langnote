# Postgres/PostgreSQL
c语言写的

PostgreSQL 版本历史记录

PostgreSQL 是一个持续发展的开源关系型数据库管理系统，自1997年发布第一个正式版本以来，每年都会推出新的大版本，每个版本支持周期为5年。

主要版本发布时间线

版本 发布时间 支持结束时间 状态
PostgreSQL 18 2025年9月25日 预计2030年11月 开发中
PostgreSQL 17 2024年9月26日 2029年11月 支持中
PostgreSQL 16 2023年9月14日 2028年11月 支持中
PostgreSQL 15 2022年10月13日 2027年11月 支持中
PostgreSQL 14 2021年9月30日 2026年11月 支持中
PostgreSQL 13 2020年9月24日 2025年11月 即将结束
PostgreSQL 12 2019年10月3日 2024年11月 已结束
PostgreSQL 11 2018年10月18日 2023年11月 已结束
PostgreSQL 10 2017年10月5日 2022年11月 已结束
PostgreSQL 9.6 2016年9月29日 2021年11月 已结束
PostgreSQL 9.5 2016年1月8日 2021年2月 已结束

各版本关键特性
PostgreSQL 9.x 系列
• 9.0 (2010年)：引入流复制和热备份
• 9.1 (2011年)：支持同步复制和外部数据封装器(FDW)
• 9.2 (2012年)：增加JSON数据类型和级联复制
• 9.3 (2013年)：支持物化视图和JSON操作增强
• 9.4 (2014年)：引入JSONB数据类型和逻辑解码
• 9.5 (2016年)：支持UPSERT和行级安全性
• 9.6 (2016年)：引入并行查询功能

PostgreSQL 10.x 系列
• 10 (2017年)：引入声明式表分区和逻辑复制

PostgreSQL 11.x 系列
• 11 (2018年)：改进并行处理和分区表

PostgreSQL 12.x 系列
• 12 (2019年)：增加Generated Columns和表达式索引

PostgreSQL 13.x 系列
• 13 (2020年)：增强索引和分区功能，改进并行处理效率

PostgreSQL 14.x 系列
• 14 (2021年)：增强并行查询、更多聚合功能和JSON改进

PostgreSQL 15.x 系列
• 15 (2022年)：优化索引、并行处理和安全特性

PostgreSQL 16.x 系列
• 16 (2023年)：改进查询执行性能和批量加载数据性能

PostgreSQL 17.x 系列
• 17 (2024年)：vacuum性能提升、I/O层和查询执行优化，扩展JSON功能

PostgreSQL 18.x 系列
• 18 (2025年)：引入异步I/O子系统、虚拟生成列、UUIDv7支持等新特性

版本支持策略

PostgreSQL社区采用以下版本支持策略：
• 每年第四季度发布新的大版本
• 每个大版本支持5年维护周期
• 维护期间每季度发布小版本进行漏洞修复
• 目前支持的最低版本为PostgreSQL 13

查看版本信息
可以通过以下方式查看PostgreSQL版本：
-- 查看完整版本信息
SELECT version();

-- 查看简洁版本号
SHOW server_version;
PostgreSQL的持续发展体现了其在性能、安全性、可扩展性方面的不断优化，已成为企业级应用的首选数据库之一。


## 命名
是的，Postgres 就是 PostgreSQL 数据库，两者指的是同一个东西。不过，这个名称的演变背后有一段有趣的历史。
可以这样理解：
•   Postgres 是它的原名和历史简称，更口语化，常用于日常交流和命令行操作。
•   PostgreSQL 是它的官方全称，强调了它对 SQL 标准的完整支持。

名称演变简史
1.  Ingres： 在加州大学伯克利分校，Michael Stonebraker 教授领导开发了一个名为 Ingres 的数据库项目（1970年代）。这是一个开创性的关系数据库。
2.  Post-Ingres： Ingres 项目结束后，Stonebraker 团队开始研究新一代的数据库系统，旨在解决关系模型的一些局限性（如支持复杂数据类型）。这个新项目被命名为 Postgres，意思是 “后-Ingres”。
3.  Postgres95： 在1994年，项目增加了对 SQL 语言的支持（最初使用一种名为 POSTQUEL 的查询语言）。为了反映这一重大变化，1995年版本被重新发布为 Postgres95。
4.  PostgreSQL： 1996年，为了更好地体现其与 SQL 的紧密联系，项目再次更名为 PostgreSQL（结合了 “Post-Ingres” 和 “SQL”）。这个名称一直沿用至今，成为官方全称。

日常使用中的习惯
尽管官方名称是 PostgreSQL，但在不同场景下，人们的用法有所不同：
场景 常用名称 示例
官方文档、网站 PostgreSQL “Welcome to the PostgreSQL official site.”
命令行、包管理 postgres（指服务/进程） sudo systemctl start postgresql （服务名） <br> psql -U username （客户端）<br> 但数据库服务进程名通常是 postgres
日常交流、文章 Postgres（更简洁、流行） “我们公司的系统用的是 Postgres。”
商标、法律文件 PostgreSQL PostgreSQL Global Development Group
总结
• 是的，Postgres 就是 PostgreSQL，就像 “Coke” 就是 “Coca-Cola” 一样。
• PostgreSQL 是正式、完整的名称，强调了其企业级特性和 SQL 标准兼容性。
• Postgres 是广为人知、被广泛接受的简称，发音更简单，在技术社区中更流行。
所以，当您听到有人说 “Postgres” 时，可以完全放心地认为他指的就是 PostgreSQL 数据库。

## pg扩展
TimescaleDB是PostgreSQL的扩展，专为时序数据设计，支持高效处理高频数据写入和复杂查询。
PostgreSQL（简称 PG）拥有非常强大的扩展（Extensions）生态系统，允许用户在不修改核心数据库的前提下，添加新功能，如时序数据、地理信息、JSON 处理、全文检索、审计日志等。
你提到的 TimescaleDB 是其中最著名的扩展之一。下面我为你系统地整理 PostgreSQL 常见且重要的扩展，并分类说明。

##  一、PostgreSQL扩展简介
PostgreSQL扩展是通过 `CREATE EXTENSION extension_name;` 安装的模块，可以添加：
- 新的数据类型
- 函数
- 操作符
- 索引方法
- 过程语言
- 物化视图增强
- 外部数据包装器（FDW）

##  二、常用 PostgreSQL 扩展分类与推荐
### 1️⃣ 时序/时间序列数据库

| 扩展 | 说明 |
|------|------|
| TimescaleDB | 最流行的时序数据库扩展，基于 PG 构建，支持自动分片（hypertable）、连续聚合、降采样，兼容 SQL，适合 IoT、监控、金融等场景。 |
| Prometheus + Promscale | Promscale 是 Timescale 公司推出的，将 Prometheus 数据存储在 PG 中的适配器，结合 PG 强大查询能力。 |

>  官网：https://www.timescale.com

### 2️⃣ 地理空间数据（GIS）

| 扩展 | 说明 |
|------|------|
| PostGIS | 最强大的地理信息系统扩展，支持空间数据类型（POINT, POLYGON）、空间索引（GIST）、空间函数（距离、相交、缓冲区等），广泛用于地图、导航、城市规划。 |
| address_standardizer | 地址标准化（如“北京市朝阳区” → 标准格式） |
| fuzzystrmatch | 模糊字符串匹配，常用于地址相似度计算 |

>  官网：https://postgis.net

### 3️⃣ 全文检索与搜索

| 扩展 | 说明 |
|------|------|
| pg_trgm | 基于 trigram 的模糊匹配，支持 `LIKE`, `ILIKE`, `~` 的 GIN/GIST 索引加速 |
| pg_bigm | 针对日语等双字节语言的全文检索优化 |
| zhparser | 中文分词插件（配合 `tsvector` 使用），用于中文全文检索 |
| tsearch2 | 旧版全文检索（已集成进核心） |

### 4️⃣ JSON 与 NoSQL 功能增强

| 扩展 | 说明 |
|------|------|
| jsoncdc | JSON 变更数据捕获（实验性） |
| plv8 | 使用 JavaScript 编写存储过程（V8 引擎），适合处理复杂 JSON |
| orafce | 提供 Oracle 兼容函数，包括 JSON 处理函数 |

> 注意：PG 本身对 `JSONB` 支持极强，多数场景无需额外扩展。

### 5️⃣ 安全与审计

| 扩展 | 说明 |
|------|------|
| pgAudit | 企业级审计扩展，支持详细记录 DDL、DML 操作，符合 PCI-DSS、HIPAA 等合规要求。 |
| sslinfo | 获取客户端 SSL/TLS 连接信息 |
| pgcrypto | 提供加密函数（如 `crypt()`, `hmac()`, `gen_salt()`），用于密码哈希、数据加密 |

>  pgAudit 官网：https://pgaudit.org

### 6️⃣ 高可用与复制

| 扩展 | 说明 |
|------|------|
| repmgr | 开源的 PostgreSQL 复制管理工具，支持主从切换、监控、故障转移。 |
| wal2json | 将 WAL 日志转换为 JSON 格式，用于 CDC（变更数据捕获），常用于数据同步、ETL。 |
| pglogical | 逻辑复制扩展（基于 wal2json 增强），支持跨版本、选择性复制表。 |

### 7️⃣ 过程语言（支持多种编程语言写函数）

| 扩展 | 语言 | 说明 |
|------|------|------|
| plpython3u | Python | 可在数据库中执行 Python 脚本 |
| plperl | Perl | Perl 函数支持 |
| pltcl | Tcl | Tcl 脚本支持 |
| plv8 | JavaScript | 高性能 JS 函数（推荐用于 JSON 处理） |

---

### 8️⃣ 外部数据访问（FDW - Foreign Data Wrapper）

允许 PG 查询外部数据源，像本地表一样使用。

| 扩展 | 说明 |
|------|------|
| postgres_fdw | 跨 PostgreSQL 实例查询（推荐替代 `dblink`） |
| file_fdw | 将 CSV、文本文件映射为表 |
| mysql_fdw | 查询 MySQL 数据库 |
| oracle_fdw | 查询 Oracle 数据库 |
| odbc_fdw | 通过 ODBC 连接任意数据库 |
| redis_fdw | 查询 Redis 数据 |
| http_fdw | 调用 REST API 并映射为表 |

---

### 9️⃣ 性能与监控

| 扩展 | 说明 |
|------|------|
| pg_stat_statements | 记录所有 SQL 执行统计（调用次数、耗时、I/O 等），性能分析必备。 |
| auto_explain | 自动记录慢查询的执行计划 |
| pg_hint_plan | 允许通过注释指定查询执行计划（类似 Oracle hint） |
| pg_buffercache | 查看 shared buffer 中缓存的数据页 |

---

###  其他实用扩展

| 扩展 | 说明 |
|------|------|
| uuid-ossp | 生成 UUID（v1, v4 等），PG 13+ 已内置 `gen_random_uuid()` |
| unaccent | 去除音调符号（如 é → e），用于模糊搜索 |
| intarray | 优化整数数组操作（排序、交集、索引） |
| ltree | 层次化数据（如组织架构、路径）的存储与查询 |
| hstore | 键值对存储（类似简单 JSON，但更轻量） |
| dict_int | 全文检索字典，去除数字（用于日志分析） |

---

## 🧰 三、如何查看和管理扩展？

### 1. 查看已安装扩展
```sql
SELECT * FROM pg_extension;
```

### 2. 查看可用扩展
```sql
SELECT * FROM pg_available_extensions;
```

### 3. 安装扩展（以 pg_stat_statements 为例）
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

### 4. 卸载扩展
```sql
DROP EXTENSION pg_stat_statements;
```

---

## 四、安装扩展的方式

1. 包管理器安装（推荐）
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql-contrib postgresql-15-timescaledb-2

   # CentOS/RHEL
   sudo yum install postgresql15-contrib timescaledb-2-postgresql-15
   ```

2. 从源码编译安装
   - 适用于定制化或最新版本

3. 使用 Docker 镜像
   ```bash
   docker run -d --name pg -e POSTGRES_PASSWORD=pass timescale/timescaledb:latest-pg15
   ```

## 五、总结：你该关注哪些扩展？

| 使用场景 | 推荐扩展 |
|---------|----------|
| 时序数据（监控、IoT） | TimescaleDB |
| 地图、位置服务 | PostGIS |
| 审计、合规 | pgAudit |
| 性能分析 | pg_stat_statements, auto_explain |
| 多数据源整合 | postgres_fdw, mysql_fdw, file_fdw |
| 中文全文检索 | zhparser + `tsvector` |
| 安全加密 | pgcrypto |
| 逻辑复制/CDC | wal2json, pglogical |

---

TimescaleDB 是你提到的重点，它本质上是一个“超集”扩展，不仅增强时序能力，还自带性能优化、压缩、多节点集群等功能，是目前最成熟的 PG 时序解决方案。

如果你正在处理时间序列数据，强烈建议尝试 TimescaleDB。
## doc
https://www.postgresql.org/docs/9.1/transaction-iso.html

![pg_ssi](./imgs/db/pg_ssi.jpg)

A Critique of ANSI SQL Isolation Levels
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf

CLOG管理
CLOG（Commit Log）在数据库系统中，特别是PostgreSQL中，用于记录事务的最终状态。以下是对CLOG管理的简要概述：

概述：
CLOG日志记录的是事务的最终状态，包括事务的提交、终止等状态。
CLOG日志管理器负责管理CLOG日志缓冲池，该缓冲池基于SLRU（Sequential LRU）策略实现。
日志结构：
PostgreSQL中事务系统一共记录了四种事务状态，包括事务正在运行、已提交、被终止和子事务已提交。
由于需要记录的事务状态只有四种，因此只需要2个字节就能记录一个事务状态信息。
一个页面（8K）能保存32K个日志记录，每个CLOG日志文件段由32个页组成，因此能保存1M个日志记录。
日志文件：
CLOG日志文件保存在PGDATA/pg_xact目录下。
文件命名使用段号（segment number），以4位16进制数字命名。
理论上可以存在的CLOG日志文件数量受限于事务ID的范围，但实际数量会少于理论值。
日志定位：
给定一个事务ID（xid），可以通过一个四元组（<segmentno, Pageno, Byte, Bindex>）定位到其在日志中的位置。
其中，segmentno是段号，Pageno是页号，Byte是页面偏移，Bindex是字节内偏移。

串行快照隔离 SSI
Serial Snapshot Isolation

Posgres的MVCC实现牛逼不，牛。serial snapshot isolation是很强。
是的,PostgreSQL的MVCC(Multiversion Concurrency Control,多版本并发控制)实现确实非常强大和出色。其中的串行快照隔离(Serial Snapshot Isolation)是PostgreSQL MVCC的核心机制之一,是它支持高并发读写的关键所在。
具体来说,PostgreSQL的MVCC及串行快照隔离机制有以下几个优点:
1. 高并发性能
   - MVCC允许多个事务并发读取同一数据,而不会相互阻塞。这大大提升了数据库的并发处理能力。
   - 串行快照隔离确保每个事务看到的数据都是一致的,不会出现脏读、不可重复读等问题。
2. 事务隔离性
   - 串行快照隔离是最高级别的隔离级别,可以避免幻读等隔离问题。
   - 即使事务之间存在并发,也能保证事务的原子性和隔离性。
3. 快照一致性
   - MVCC机制会为每个事务维护一个数据快照,确保事务内部看到的数据是一致的。
   - 即使数据在事务执行过程中发生变更,事务内部也能看到一致的快照数据。
4. 数据库恢复
   - MVCC的快照机制有利于数据库的恢复和审计,可以轻松地实现点in时间恢复。
5. 低锁开销
   - MVCC不需要对数据行加锁即可实现并发控制,大大降低了锁的开销。
总的来说,PostgreSQL的MVCC及串行快照隔离机制是其数据库引擎的核心优势之一,确实是非常出色的并发控制技术。这也是PostgreSQL广受欢迎的重要原因之一。

好的,让我来详细介绍一下串行快照隔离(Serializable Snapshot Isolation,SSI)的论文和代码实现。

论文方面:

- 串行快照隔离最初由Michael Cahill等人在2008年发表于SIGMOD会议上的论文《Serializable Isolation for Snapshot Databases》中提出。
- 论文中提出了一种基于依赖图的SSI算法,可以在不牺牲并发性的情况下实现可串行化的事务隔离。
- 论文详细阐述了SSI的原理和实现细节,包括如何检测和解决可串行化冲突。

代码实现方面:

- PostgreSQL就是最著名采用SSI机制的数据库系统之一。
- PostgreSQL的SSI实现主要集中在以下几个模块:
  1. 事务管理模块:维护事务的快照信息和依赖关系。
  2. 锁管理模块:检测可串行化冲突并加锁。
  3. 查询执行模块:根据事务快照提供一致的数据视图。
  4. 恢复模块:支持基于SSI的数据库恢复。
- PostgreSQL的SSI实现在9.1版本中引入,并在之后的版本中不断完善和优化。
- 除了PostgreSQL,Oracle数据库和某些NoSQL数据库如FaunaDB也采用了类似的SSI机制。

总的来说,串行快照隔离是一种非常强大的并发控制技术,通过精心设计的算法和数据结构实现,确保了数据库事务的正确性和高并发性能。PostgreSQL在这方面的实现可以说是业界的标杆之一。

可串行化冲突
确保即使多个事务同时执行，每个事务的执行结果也应该与它们按某种顺序串行执行的结果相同
在数据库系统中，可串行化冲突是指两个或多个事务的操作可能导致数据不一致或读取错误的一种情况，尤其是在并发环境下。可串行化是数据库并发控制的一个目标，旨在确保即使多个事务同时执行，每个事务的执行结果也应该与它们按某种顺序串行执行的结果相同。下面我将进一步解释这个概念。

### 什么是可串行化？
在英文中，“可串行化冲突”通常被称为 Serializable Conflict。这个术语主要用来描述在数据库并发控制中，保证事务执行结果与按某种顺序串行执行的结果相同的一种机制。此外，当提到具体的冲突类型时，通常会使用以下英文术语：
1. Write-Read Conflict - 写读冲突
2. Write-Write Conflict - 写写冲突
3. Read-Write Conflict - 读写冲突

这些术语帮助描述并发事务中可能发生的不同类型的数据访问冲突，这些冲突需要通过并发控制机制如锁定或时间戳排序来管理，以实现事务的可串行化。
可串行化是衡量数据库并发事务执行结果正确性的一个标准。如果一个并发执行的事务集合可以被重排为一个不产生冲突的串行执行序列，那么这个事务集合就是可串行化的。

### 冲突与可串行化
在并发环境中，冲突通常发生在以下两个事务之间：
1. 读写冲突（Write-Read Conflict）：当事务A修改了一个数据项，而事务B随后读取了同一个数据项，这种情况下，如果事务A和B是并发执行的，事务B可能会读取到错误的数据。
2. 写写冲突（Write-Write Conflict）：当两个事务都试图修改同一个数据项时，如果没有适当的同步机制，最终的数据可能会反映两个事务中的任何一个或两个事务都没有正确执行。
3. 读写冲突（Read-Write Conflict）：如果事务A读取了一个数据项，而事务B随后修改了同一个数据项，在事务A基于旧数据做出决策后，事务B的修改可能会导致事务A的决策失效。

### 如何实现可串行化？

数据库系统通常通过两种主要的并发控制技术来实现事务的可串行化：

1. 锁定机制（Locking）：数据库管理系统使用锁来控制对数据项的访问。基本策略包括共享锁（用于读取操作）和排他锁（用于写入操作）。通过这种方式，锁定机制确保没有其他事务可以访问同一数据项进行冲突操作。

2. 时间戳排序（Timestamp Ordering）：每个事务在开始时分配一个唯一的时间戳。数据库系统根据事务的时间戳来决定事务的执行顺序，确保时间戳较早的事务能够在时间戳较晚的事务之前执行相关操作。

### 总结

可串行化冲突的管理对于确保数据库操作的正确性和一致性至关重要。通过有效的并发控制机制，如锁定和时间戳排序，数据库系统能够提供可靠和一致的数据访问，即使在多个用户和应用程序并发访问的情况下也是如此。

在C++中，有许多开源库可以帮助实现线程同步和可串行化冲突。一个常用的库是Intel的Threading Building Blocks (TBB)。TBB提供了高级并行编程抽象，可以方便地实现线程安全和高效的并行计算。

下面是一个使用TBB实现可串行化冲突的示例代码：

### 使用Intel TBB实现可串行化冲突

首先，你需要安装Intel TBB库。如果你还没有安装，可以通过以下方式安装：

- 在Linux上，你可以使用包管理器安装，比如`apt-get`：
```bash
sudo apt-get install libtbb-dev
```

- 在Windows上，你可以从Intel官网下载安装包。

接下来，是示例代码：

```cpp
#include <iostream>
#include <vector>
#include <tbb/tbb.h>

// 共享资源
int shared_resource = 0;

// 一个线程执行的函数
void increment(int thread_id) {
    tbb::mutex::scoped_lock lock(mtx);  // 锁定互斥锁
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 使用tbb::parallel_for并行执行线程
    tbb::parallel_for(0, num_threads, [](int i) {
        increment(i);
    });

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. TBB库：包括头文件`tbb/tbb.h`来使用TBB库中的功能。
3. 互斥锁：使用`tbb::mutex`来保护共享资源的访问。
4. 线程函数：`increment`函数在访问和修改共享资源前锁定互斥锁。
5. 主函数：
    - 使用`tbb::parallel_for`并行执行线程，避免了手动管理线程的创建和同步。
    - 打印最终的共享资源值。

TBB库提供了更高层次的抽象，使并行编程更加简洁和高效。通过使用`tbb::parallel_for`，我们可以轻松地并行执行多个线程，并保证线程安全。

在C++中实现可串行化冲突（Serializable Conflict）通常涉及使用线程锁（如互斥锁）来确保多个线程不会同时访问和修改共享资源。以下是一个示例代码，演示了如何在C++中实现可串行化冲突。

这个例子使用了`std::mutex`来保护对共享资源的访问。`std::mutex`是一个标准的互斥锁，它可以确保同时只有一个线程可以访问共享资源。

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

// 共享资源
int shared_resource = 0;

// 互斥锁
std::mutex mtx;

// 一个线程执行的函数
void increment(int thread_id) {
    // 锁定互斥锁
    std::lock_guard<std::mutex> lock(mtx);
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 创建并启动多个线程
    for (int i = 0; i < num_threads; ++i) {
        threads.push_back(std::thread(increment, i));
    }

    // 等待所有线程完成
    for (auto& th : threads) {
        th.join();
    }

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. 互斥锁：`std::mutex mtx`用来保护对共享资源的访问。
3. 线程函数：`increment`函数是每个线程执行的代码，它在访问和修改共享资源前锁定互斥锁，并在修改完成后自动解锁（由`std::lock_guard`管理）。
4. 主函数：
    - 创建并启动多个线程，每个线程运行`increment`函数。
    - 使用`std::thread`类创建线程，并存储在一个`std::vector`中。
    - 使用`join`方法等待所有线程完成。
    - 打印最终的共享资源值。

在这个例子中，`std::lock_guard`自动管理互斥锁的锁定和解锁，可以确保即使在异常情况下互斥锁也会被正确解锁。这种机制可以有效避免由于线程竞态条件（race conditions）导致的数据不一致问题。

冲突可串行化(Conflict Serializable)是指一个并发执行的事务集合,在执行顺序上等价于某个串行执行的事务集合,也就是说,任何并发执行的情况都可以转换成某个串行执行的情况

冲突等价(ConﬂictEquivalence) 可串行化调度(Serializable Schedules),事务事务(transaction)是在数据库上执行的一个或多个操作构成的序列,用来完成数据库系统的高级功能。

https://geek-docs.com/dbms/dbms-tutorial/dbms-conflict-serializability.html

产品架构  Shared-Everything

https://zhuanlan.zhihu.com/p/656483356

德歌
https://github.com/digoal/blog

### pg scheme
pg数据库下面有模式(scheme)，模式下面有表

[PostgreSQL 在国内公司应用](https://www.zhihu.com/question/19685185)

Greenplum开源
Massively Parallel Postgres for Analytics
Experience Greenplum Database, an open-source massively parallel data platform for analytics, machine learning and AI 

支持存储过程debug

sp（存储过程的作用

编程，避免大量的sql中间数据在网络上传输

### windows 10 安装版本

PostgreSQL 10.8
[PostgreSQL查看版本信息](https://blog.csdn.net/kmblack1/article/details/78721653)

PostgreSQL 10.12 Documentation

https://www.postgresql.org/docs/10/index.html


卸载了，中国电信云安装


开发语言 c

sql解析 flex bison

source repo
https://github.com/postgres/postgres



maillist

centos 7安装

https://www.postgresql.org/download/linux/redhat/

postgresql权限管理，如何添加一个网段的ssl访问权限？
配置参考文档：https://www.jianshu.com/p/21d25c0d6ab4

180.167.0.0/16
PostgreSQL安装后默认只能localhost:5432访问

本机登录
su - postgres
qsql -U postgres ？？？

核心的登录命令
psql "postgresql://[用户名]:[密码]@[服务器地址]:[端口]/[数据库名称]"
示例：psql postgresql://postgres:123456@192.168.51.17:5432/database

https://www.jianshu.com/p/823702d6643e
psql -Upostgres -h 118.182.97.157 -p 5432 -d postgres
psql -Upostgres -h 118.182.97.157 sonarqube
CREATE DATABASE sonarqube;
\q

命令行方式登录PostgreSQL

配置文件
/var/lib/pgsql/10/data/pg_hba.conf

在 PostgreSQL 10 中，要允许任何 IP 地址访问数据库，您需要进行以下配置更改：
1. 找到 PostgreSQL 的配置文件 `postgresql.conf`。在 Linux 上，该文件通常位于 `/etc/postgresql/10/main` 目录下；在 Windows 上，它通常位于 `C:\Program Files\PostgreSQL\10\data` 目录下。
2. 打开 `postgresql.conf` 文件，并找到以下配置项：

   ````conf
   #listen_addresses = 'localhost'    # 默认值为 'localhost'
   ```

   ````
2. 将 `listen_addresses` 的值修改为 `'*'`，以允许来自任何 IP 地址的连接：
   ````conf
   listen_addresses = '*'
   ```

   ````
3. 保存并关闭 `postgresql.conf` 文件。
4. 在 PostgreSQL 10 中，还需要修改 `pg_hba.conf` 文件来配置访问控制规则。找到并打开 `pg_hba.conf` 文件。
5. 在 `pg_hba.conf` 文件中，为允许任何 IP 地址访问数据库，请添加以下规则到文件的末尾：

   ````conf
   # 允许来自任何 IP 地址的连接
   host    all             all             0.0.0.0/0               md5
   ```

   这条规则允许任何 IP 地址以 `md5` 加密方式连接到任何数据库。

   ````
6. 保存并关闭 `pg_hba.conf` 文件。
7. 重新启动 PostgreSQL 服务器，以使配置更改生效。
请注意，允许任何 IP 地址访问数据库存在一定的安全风险。建议仅在开发或受信任的环境中使用此配置。在生产环境中，应该明确指定允许访问数据库的 IP 地址范围，并采取其他安全措施来保护数据库。

### pgsql 创建数据库
navicate图形界面创建数据库？ 登录，进命令行 CREATE DATABASE dbname;

PostgreSQL 创建数据库
https://www.runoob.com/postgresql/postgresql-create-database.html


PostgreSQL 数据库内核分析

https://book.douban.com/subject/6971366/

适合刚开始研读PG源代码的朋友
数据库执行计划用到了动态规划和图论等相关知识
开源数据库中，对空间地理数据支持比较好的要数PG的插件Postgi

Oracle ACE

第九届PostgreSQL中国技术大会
张文升
著有书籍《PostgreSQL实战》
《PostgreSQL指南：内幕探索》

/postgres# find . -name "*.y"
./contrib/cube/cubeparse.y
./contrib/seg/segparse.y
./src/test/isolation/specparse.y
./src/backend/replication/repl_gram.y
./src/backend/replication/syncrep_gram.y
./src/backend/utils/adt/jsonpath_gram.y
./src/backend/bootstrap/bootparse.y
./src/backend/parser/gram.y
./src/bin/pgbench/exprparse.y
./src/pl/plpgsql/src/pl_gram.y
