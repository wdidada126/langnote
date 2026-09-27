# 01 · PostgreSQL 入门与集群初探（原书第 1–2 章合并）

> 对应原书 Part 1 前章：Ch1 *Introduction to PostgreSQL*、Ch2 *Getting to Know Your Cluster*（✅ 官方 README 章题）。
> 三态标注：✅ 取证 / ⚠️ 转述推定 / 🔧 本机 SQLite/DuckDB 类比实测（**非 PostgreSQL 行为**）。
> 本章在原书的体例：What you will learn → Abstract → 正文 → Conclusions → References → Verify Your Knowledge（✅ README 体例声明，下同各章）。

## 1. 为什么是 PostgreSQL（Ch1 立意）

- 本书基线为 **PostgreSQL 16**，卖点一句话："用 PG 16 构建高性能数据库方案"（✅ README 副题）。
- 目标读者：从零学 PG 者 + 想构建健壮、可扩展数据库应用的开发者（✅ README "Who this book is for"）。
- 前置：不要求 PG 经验，但预期熟悉数据库与 SQL 基础概念（✅ README）。
- 官方导语对 PG 的定性：世界增长最快的开源对象-关系 DBMS，企业级特性、可扩展、安全、高效、生态丰富（✅ README 文案；逐条技术展开为 ⚠️ 转述）。
- 血缘（⚠️ 通识转述）：源自 1986 年 UC Berkeley POSTGRES 项目（Stonebraker 主持），"PG"承"Post-Ingres"之意；MVCC 是理解一切 PG 行为的第一性视角（✅ https://www.postgresql.org/docs/current/mvcc.html ）。
- 版本节奏 ✅（versioning 页实抓，2026-09-27）：
  - 大版本一年一发、各支持五年；
  - 16 首发 2023-09-14，17 首发 2024-09-26，18 首发 2025-09-25；
  - 读本书时（2026）PG 16 已非最新，当前主力 18.6/17.11——差异集中在各章文末演进节。

## 2. 集群拓扑与对象层级（Ch2 主干）

对象层级（⚠️ 转述 + ✅ 文档锚点）：

- **cluster（集群）**：一个数据目录 + 一套后台进程，管理 N 个数据库；
- **database**：隔离单元（模板库 template0/template1 ⚠️，✅ sql-createdatabase.html 可达已验）；
- **schema**：库内命名空间，`public` 为默认；
- **对象**：表/索引/视图/函数/序列……全部登记在系统目录。

进程模型（⚠️+✅ 文档口径）：

- 一 **postmaster** 父进程监听，每客户端连接 fork 一个 **backend** 进程（process-per-connection，非线程模型）；
- 后台帮手：checkpointer、background writer、WAL writer、autovacuum launcher、stats collector——Ch2 点名、Ch11/16 展开（⚠️ 转述，✅ wal-internals/mvcc 页族）。

配置与自查面：

- 参数层次：命令行 > `postgresql.auto.conf`（ALTER SYSTEM）> `postgresql.conf` > 编译默认，会话可 `SET`（✅ https://www.postgresql.org/docs/current/config-setting.html ）。
- 系统目录即数据库自己写的"说明书"：`pg_database`、`pg_settings`、`pg_stat_activity`（⚠️+✅ https://www.postgresql.org/docs/current/monitoring-stats.html ）。
- 起手三连 ⚠️（书风）：`SELECT version();`、`SHOW data_directory;`、`\conninfo`；WAL 概念第一次露脸（✅ https://www.postgresql.org/docs/current/wal-internals.html ）。

## 3. 实验环境：逐章 Docker 与 forumdb（本书工程特色 ✅）

- 官方仓 `docker-images/` 提供 **chapter_05..chapter_19 逐章镜像** + `standalone` 基镜像（✅ 树实证，全清单见 00 取证节）：

```shell
$ cd docker-images
$ sh run-pg-docker.sh chapter_05   # 起第 5 章专用容器（README 原文示例）
```

- 不用 Docker 的自建路径（✅ README "Creating the example database"）：

```shell
$ cd setup
$ sh 001-create-database-users.sh          # 建角色 luca 与 enrico
$ psql -U postgres < 002-forum-database.sql # 建用户 forum、库 forumdb 并灌种子数据
```

- 书写约定 ✅（README "Command prompts"）：`$`=OS 提示符、`forumdb=>`=普通会话、`forumdb=#`=超管会话、root 操作走 `sudo(1)`。
- 勘误义务 ✅（README Errata）：Ch3 p58 若干 `IF EXIST` 应为 `IF EXISTS`——本目录全部按勘误后口径书写。

## 4. 🔧 类比实测：「单机文件库 vs 服务器集群」两种世界观

本机无 PostgreSQL（`where psql` 未检出 ✅ 实测），用两台可跑引擎对照"客户端如何认识自己的库"（**非 PostgreSQL 行为**；SQLite CLI 3.50.6、DuckDB 1.5.5，产物 sq1.out/duck.out）：

```text
$ sqlite3 sq1.db ".databases"
main -> sq1.db             # 库=单个文件；无 cluster/schema 服务器层

$ python -c "import duckdb; ..."
> con.sql("SELECT current_setting('auto_checkpoint')")  -> (True,)
> import duckdb; duckdb.__version__                     -> '1.5.5'
                           # 有 GUC 味道的 setting，但仍是进程内嵌/单写者
```

三世界观对照表 ⚠️：

| 维度 | PostgreSQL 16 | SQLite | DuckDB |
|---|---|---|---|
| 库的载体 | $PGDATA 目录+服务进程 | 单文件+内嵌 | 单文件+内嵌 |
| 连接模型 | 每连接一 backend 进程 | 进程内句柄 | 进程内连接对象 |
| 自我观测 | pg_database/pg_settings | PRAGMA database_list | duckdb_settings() |

结论：Ch2"了解你的集群"的世界观动作（SHOW/系统目录/统计视图）在嵌入式引擎退化为 PRAGMA/函数——先摸清"我在连什么、里面有什么"再动手，方法论可迁移。

## 5. 与其他册的分工

- 安装/initdb/服务器控制配方：[../PostgreSQL_16_Administration_Cookbook/01-安装配置与服务器控制.md](../PostgreSQL_16_Administration_Cookbook/01-安装配置与服务器控制.md)。
- 架构内幕深化：[../Mastering_PostgreSQL_Administration/01-PostgreSQL系统架构.md](../Mastering_PostgreSQL_Administration/01-PostgreSQL系统架构.md)、[../Mastering_PostgreSQL_Administration/02-安装与初始化.md](../Mastering_PostgreSQL_Administration/02-安装与初始化.md)。
- 性能版基线对照（PG 10 时的架构叙述）：[../PostgreSQL_10_High_Performance_3e/01-PostgreSQL10新特性与性能含义.md](../PostgreSQL_10_High_Performance_3e/01-PostgreSQL10新特性与性能含义.md)。
- 中文内核全景：[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)。
- 多引擎扫盲对照：[../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md](../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md)。

## 6. 本章自测（重构版，仿原书 Verify Your Knowledge 体例；题目为本目录自拟 ⚠️）

1. **问**：一个 PG 集群与一个数据库的区别？**答**：集群=数据目录+共享进程组；一集群可含多库，跨库不可直接 JOIN（呼应 [04 号文件](04-高级语句_连接与递归查询.md)）。
2. **问**：`forumdb=#` 与 `forumdb=>` 提示符含义？**答**：`#`=超管/管理员语境、`>`=普通用户（✅ README 约定）。
3. **问**：process-per-connection 带来什么运维后果？**答**：连接贵 ⇒ 池化必备（→ [02-用户与连接管理.md](02-用户与连接管理.md) 演进节）。
4. **问**：改 `pg_hba.conf` 要重启吗？**答**：不需要，reload 即可；改 `listen_addresses` 需重启 ⚠️。
5. **问**：本书实验环境两条路？**答**：逐章 Docker 脚本或 setup 双脚本建 forumdb（✅ README）。

## 核心概念速览（中英对照）

1. **集群** — cluster：一个数据目录+一套共享后台进程管理的数据库集合。
2. **数据目录** — data directory / $PGDATA：postgresql.conf、pg_hba.conf、base/、pg_wal/ 之根。
3. **后端进程** — backend process：每连接一进程的服务器模型。
4. **预写日志** — WAL：先写日志后写页，恢复/复制/PITR 之根。
5. **MVCC** — 多版本并发控制：读写互不阻塞的实现哲学。
6. **系统目录** — system catalogs：描述数据库的表（pg_database/pg_class/pg_settings）。
7. **统计收集器** — statistics collector：pg_stat_* 的数据源。
8. **超级用户** — superuser：集群初始管理员 postgres。
9. **元命令** — psql metacommands：`\l` `\dt` `\d` `\conninfo`，客户端行为非 SQL。
10. **逐章镜像** — per-chapter Docker images：本书示例环境自足的工程特色 ✅。
11. **forumdb** — 示例论坛库：posts/categories 贯穿全书。
12. **版本支持期** — versioning policy：一年一大版本、五年支持 ✅。

## 最新演进与工业实践

- **PG 16→18 现状**（✅ https://www.postgresql.org/support/versioning/ ，访问 2026-09-27）：当前受支持 18.6 / 17.11 / 16.15 / 15.19 / 14.24（14 最后支持到 2026-11）；本书 16 基线仍安全，但新学内容请随手对照 current 文档。
- **PG 17 结构级看点**（✅ https://www.postgresql.org/docs/release/17.0/ ）：json_table、CREATE OR REPLACE VIEW 列重排、vacuum 改进——运维线详见 [../Mastering_PostgreSQL_Administration/10-PostgreSQL17新特性.md](../Mastering_PostgreSQL_Administration/10-PostgreSQL17新特性.md)。
- **PG 18 结构级看点**（✅ https://www.postgresql.org/docs/release/18.0/ ）：异步 I/O 执行器（io_method）、虚拟生成列、OAuth——架构世界观未变，进程模型仍是 process-per-connection ⚠️。
- **工业实践** ⚠️：生产优先用发行版打包或官方镜像 `postgres:16`；本书"逐章容器"与 devcontainer/环境即代码同脉；连接模型决定了 PgBouncer 几乎必选（[02 号文件](02-用户与连接管理.md)展开）。
- **文档锚点**（✅ 可达）：https://www.postgresql.org/docs/current/mvcc.html 、https://www.postgresql.org/docs/current/config-setting.html 、https://www.postgresql.org/docs/current/monitoring-stats.html 。
