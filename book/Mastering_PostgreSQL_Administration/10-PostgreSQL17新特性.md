# 10 · PostgreSQL 17 新特性（原书第 10 章）

> 对应原书章：**Ch.10 New Features of PostgreSQL 17**（✅ Crossref DOI `..._10`）。
> 官方摘要原句（✅）："In this chapter, we explore the new features of PostgreSQL v17 in depth, along
> with the steps for configuring, installing, and initializing the database cluster. PostgreSQL v17 is
> compatible with a wide range of operatin…"
> 口径声明：章题与摘要 ✅ 实抓；特性清单以官方发行说明/发布新闻为据 ⚠️ 转述（本机无 PG17，不装不跑，
> 无一条实测；本章也是全书"版本时效"最敏感的一章，读前先扫尾部演进节）。

## 本章地图

| 主题 | 你能做到 | 关键对象/参数/命令 |
| --- | --- | --- |
| 17 主线四件套 | 判断哪些特性直接改变现有工作流 | SQL/JSON、pipeline、增量备份、pg_createsubscriber ⚠️ |
| 优化器/执行 | 认出计划里新形态 | 多列统计扩展、IN 值列表优化、内存管理（hash agg 批式化）⚠️ 转述 |
| 复制与高可用 | 用 17 简化迁移/HA 拓扑 | 逻辑复制槽 failover 选项、pg_upgrade 链路增强 ⚠️ |
| 运维与可观测 | 把新视图/工具挂进面板 | pg_stat_recovery_prefetch、vacuum I/O 优化、pg_waldump 增强 ⚠️ |
| 客户端与类型 | 前端侧变化 | libpq pipeline mode、pg_dump/pg_restore 并行改进 ⚠️ |

## 核心精讲（⚠️ 文档转述重构）

### 1. SQL/JSON 标准化：本章对 08 章迁移工程的隐性增益

PG17 落地 SQL:2023 核心 JSON 对象构造/查询族：`JSON_TABLE()`（把 JSON 文档摊成关系表）、
`JSON_EXISTS/JSON_QUERY/JSON_VALUE`（路径表达式取自 SQL:2016 一脉），与旧的 `->`/`->>`/jsonb 函数系
并行共存（⚠️ 转述）。运维语境三价值：
1. 报表层少建中间表：日志宽表里的 JSON 列直接 `JSON_TABLE` 摊平（07 章面板补数场景）；
2. 迁移期双写校验：Oracle 端 JSON 字段与 PG jsonb 对账可用同一套路径表达式思路改写（08 章）；
3. jsonb 存储与索引不变，**标准函数走的是 SQL 层糖 + 优化器新入口**，老业务无感 ⚠️。

### 2. 增量备份：5 章工具矩阵的官方答案

`pg_basebackup --incremental=backup_manifest`：以**上一份全量的 manifest** 为基线，只拷贝自那以后
被修改过数据页块的文件集（页级判定依赖 VM/FSM 系信息，03 章地基），恢复=全量+各级增量按序重放 ⚠️。
意义：把 pgBackRest 系的"增量+保留策略"压力接回原生半程（仓库管理/合并仍要靠工具或脚本，
合并增量的官方 CLI 位当年未随发布落地，引用时口径要收紧 ⚠️ 转述）。

### 3. 逻辑复制与升级链：pg_createsubscriber 改写法

- **pg_createsubscriber**（17 新增，回灌 16.4）：把一个流复制备库**就地转换成发布者**，
  客户端连接串不用改——"升级时只断一次"的原生套路（05/09 章升级/切换场景，替代大量手工脚本）⚠️。
- **复制槽 failover**：`pg_create_logical_replication_slot(..., failover => true)`
  允许物理备库上失效的槽逻辑上"接管"，为"槽高可用"补了官方半块砖 ⚠️ 转述。
- `pg_upgrade` 在 17 继续吃版本链路细节（逻辑槽/订阅保留线），与 Cookbook 07 章食谱成对 ⚠️。

### 4. 性能与可观测面速览（逐条 ⚠️ 转述）

| 特性 | 一句话 | 关联章 |
| --- | --- | --- |
| libpq pipeline mode | 单连接多查询流水（非并发），吞吐敏感客户端的批量泵 | 01 章连接路径 |
| VACUUM 流式读 | 不再把整表挤进 shared_buffers，大表维护对热数据扰动小 | 03/06 章 |
| 恢复期预取统计 `pg_stat_recovery_prefetch` | 崩溃恢复/备库回放 IO 画像新视图 | 07 章 |
| 优化器：多列统计可用于表达式、IN 列表优化 | 选择性估计更准，行数爆炸场景回落 | 盘上优化器笔记 |
| `ALTER SYSTEM` 可设 per-database 角色参数族扩展 | 参数治理粒度再细 | 02 章 |
| pg_dump 并行与过滤增强、`--exclude-table` 族扩列 | 大库导出减负 | 05 章 |

### 5. 与第 2 章闭环的"装机侧"增量

原书本章把"配置/安装/初始化"并列讲（✅ 摘要原文含此句）：17 的 initdb 默认线变化（如
`icu` 相关默认、locale provider 选项延续 16 的框架）属"新集群一天一个样、老集群纹丝不动"类——
**只有新建集群吃到**，升级老库务必别把"文档新默认"脑补成"我已生效" ⚠️ 转述。判据：
`SELECT * FROM pg_settings WHERE name ILIKE '%icu%|%locale%'` 对照 `source` 列（01 章参数四级覆盖法）。

### 6. 本章无 🔧 声明

PG17 特性清单的每一条都需要真实 PG 实例才能实测，本机不装不跑（00 章纪律），故本章零 🔧；
方言映射类的 🔧 见 08 章、日志/空间语义类见 05/06 章。

## 常见坑与判读

| 现象 | 第一判读 | 取证动作（⚠️ 转述） |
| --- | --- | --- |
| "17 有增量备份"却找不到合并命令 | 原生只给生产端，合并靠工具/手工编排 | 先定恢复侧流水线再决定要不要上原生增量 ⚠️ |
| JSON_TABLE 用得欢但迁移到 15 老库报错 | 版本特性非全链默认 | 报表 SQL 头部标注最低版本要求 |
| pg_createsubscriber 跑完订阅不动 | 备库角色/权限前置未满足（REPLICATION 属性） | 04 章权限清单过一遍 |
| 升级完监控掉底 | exporter 的查询引用了改名列/视图 | 面板 SQL 对照发行说明"监视性统计视图"变更节 ⚠️ |
| 以为 pipeline mode=连接池 | 它只是单连接流水 | 并发模型见 01 章进程/池化框架 |

## 与其他章 / 其他笔记的联系

- 本册：02 章（17 装机默认线）；03 章（增量备份的页级判定地基）；05 章（增量备份入工具矩阵）；
  06 章（VACUUM 流式读）；07 章（新视图接入面板）；08/09 章（pg_createsubscriber/逻辑复制对
  去 O 通道的替代位）；01 章（pipeline mode）。
- [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)：
  PG16 基线全图——两册版本对表（其 00 的"版本基线提醒"与本节配对使用）。
- [../PostgreSQL技术内幕_查询优化深度探索.md](../PostgreSQL技术内幕_查询优化深度探索.md)：
  优化器增量的中文源码语境（IN 优化/统计扩展的"为什么"）。
- [../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 核心概念速览（中英对照）

1. **SQL/JSON** — JSON_TABLE/JSON_* 标准族：SQL:2023 风格的 JSON 查询/构造入口（17 落地）。
2. **增量备份** — incremental backup (pg_basebackup --incremental)：以上一 manifest 为基线的页块差集备份。
3. **备份清单** — backup manifest：全量的"体检报告"，也是增量的基线锚。
4. **流水线模式** — libpq pipeline mode：单连接多语句流水提交，非并发连接的替代品。
5. **订阅者转换器** — pg_createsubscriber：备库就地转发布端的官方升级/切换工具。
6. **可失效转移槽** — failover replication slot：逻辑槽在备库失效后的官方接管位（17 半块砖）。
7. **恢复预取统计** — pg_stat_recovery_prefetch：回放/恢复期 IO 预取画像视图。
8. **VACUUM 流式读** — streaming read for vacuum：大表维护不再冲刷共享缓冲（06 章续）。
9. **ICU 默认线** — default collation provider：新集群排序规则的代际切换（只惠新建库 ⚠️）。
10. **多列扩展统计** — extended statistics on expressions：表达式/多列相关性的选择性燃料。
11. **回灌策略** — backport（16.4 收 pg_createsubscriber）：特性随小版本下放的老客户端照顾。
12. **版本基线** — 17.x：本册全书命令/默认值的时间戳，读任何一节先对齐它。

## 最新演进与工业实践

- **PG18 已登场（2025-09/10 窗口）**：官方 current 文档线含 release-18（✅
  https://www.postgresql.org/docs/current/release-18.html 实抓 200），在支版本表 ✅
  https://www.postgresql.org/support/versioning/ 实抓 200。18 主线：异步 I/O（AIO 框架，顺序扫描/
  vacuum 先接入）、`uuidv7()`、虚拟生成列、NOT NULL 约束目录化提速、B-tree skip scan 等 ⚠️ 转述——
  对本书 17 基线的冲击集中在 **IO 模型（01/03/06 章语境需重校）** 与**备份/升级链** ⚠️。
- **本书的 17 视角在 2026 的定位**：05 章的增量备份、07 章的新视图在 18 继续可用且增强；
  JSON_TABLE 生态已成报表层默认写法（Superset/Metabase 适配跟进 ⚠️ 转述）。
- **工业实践**：云上托管实例的大版本推进普遍滞后社区 6–12 个月，"书基线=云默认线"不成立，
  选型时把 17 特性按云厂商 GA 表逐条核对 ⚠️ 转述。
- **官方信息入口（全部 ✅ 实抓 200，2026-09-27）**：
  https://www.postgresql.org/docs/release/17.0/ ；
  https://www.postgresql.org/about/news/postgresql-17-released-2953/ ；
  https://www.postgresql.org/docs/current/release-17.html 。
- **缺口诚实登记 ⚠️**：原书第 10 章的选取清单（哪些特性给了实操步骤、哪些仅列表）未获样章，
  本文件按官方 Major Changes 框架重建，条目标注均 ⚠️。
