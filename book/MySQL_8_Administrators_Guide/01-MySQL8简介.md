# 第 1 章精读重构——MySQL 8 简介

> 原书章题：Introduction to MySQL 8（⚠️ 英题由中文章题回译）；中题 ✅ 社区译本（见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第五节）。
> 本文件为**精读重构**，不是原书文本；本章无官方代码包（仓库无 Chapter01 目录，✅ 实测），
> 内容骨架依 MySQL 8.0 手册"一般信息/新特性"主题域重构（⚠️），手册页经可达镜像 mysql.net.cn 逐一 200 核验。

## 1.0 全书导言（本书的体裁声明）

- Packt "Administrator's Guide" 系的写法：**每章=一组任务 + 命令演示 + 注意事项**，不追求原理纵深
  （与 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md) 的源码体裁、
  [../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md) 的机制体裁构成 MySQL 书栈的三种笔法）。
- 读者画像 ⚠️ 推定：有 5.7 运维经验、需要把日常任务清单整体切到 8.0 语义的系统管理员/初级 DBA。
- 目标承诺（依社区译本前言主题 ✅ 转述）：安装-管理-复制-安全-调优-排错的一条龙，配可下载代码包（✅ 仓库 12 个章目录）。
- 本书与姊妹册的关系：同作者组在 Packt MySQL 8 线还有面向大数据/配方体的册子；本仓盘上对应物是
  [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md)（性能轴）
  与 [../MySQL8查询性能优化.md](../MySQL8查询性能优化.md)（Krogh 调优轴），三者互不覆盖。

## 1.1 本章定位

全书的"版本语义导览"：MySQL 从 Oracle 收购（2008/2010）到 8.0（2018-04-19 GA ✅ endoflife.date 实抓 releaseDate=2018-04-19）
的历史线、5.7→8.0 的破坏性变更地图，以及"管理员视角的 8.0 新特性清单"。它决定了后 14 章的一切默认值口径。

## 1.2 8.0 管理员必须内化的版本语义（⚠️ 手册转述）

| 变更 | 5.7 旧行为 | 8.0 行为 | 管理员影响 |
| --- | --- | --- | --- |
| 数据字典 | frm 文件 + 系统表分散 | InnoDB 事务化数据字典，frm 退役 | 表结构与元数据崩溃一致性（✅ mysql.net.cn/doc/refman/8.0/en/introduction.html 主题域） |
| 默认字符集 | latin1 | utf8mb4 | 新建库表免设四字节；老库迁移须显式 CONVERT |
| 默认认证插件 | mysql_native_password | caching_sha2_password | 旧客户端连不上是 8.0 第一事故源（详见 [11-安全.md](11-安全.md)） |
| GTID | 默认 OFF | 默认 ON | 拓扑变更脚本要重审（[08-复制.md](08-复制.md)） |
| 查询缓存 | 有（且常成瓶颈） | **整体移除** | 所有"调 query_cache"经验作废 |
| 优化器 | — | 降序索引、直方图、GROUP BY 不再隐式排序 | ORDER BY/GROUP BY 语义审查 |
| JSON | 伪 BLOB | 部分二进制化 + 多值索引可用 | 文档型用法进入主库（[04-数据类型.md](04-数据类型.md)、[07-索引.md](07-索引.md)） |
| 角色 | 无 | CREATE ROLE 语法 + SET DEFAULT ROLE | 授权模型现代化 |

## 1.3 版本策略史（书内语境 vs 2026 现状）

- 书中语境：8.0 是"下一代特性发布线"（DMR）的起点，当时预计 8.1/8.2… 短周期演进。
- 实际演化 ✅（endoflife.date/mysql，2026-09-27 实抓 API）：Oracle 于 2023 年重排为
  **LTS + Innovation 双线**——8.4 为首个 GA LTS（2024-04-30 发布，支持至 2029，EOL 2032-04-30），
  9.0 起 Innovation 每季一发（9.0 2024-07-01 → 9.7 2026-04-21），8.0 已于 2025-04-30 停止常规支持、
  2026-04-30 EOL。**本书的"8.0"已是生命周期末端版本**，读时须做版本翻译（各章末节负责）。

## 1.4 与 repo 的分工与互链

- 历史与源码语境的纵深版：[../Understanding_MySQL_Internals/01-MySQL历史与架构.md](../Understanding_MySQL_Internals/01-MySQL历史与架构.md)
  （Pachev 2003 视角的同一部历史，本册 1.2 表即其 20 年后的续章）。
- 8.0 运行时原理底图：[../mysql/01-InnoDB与MySQL的架构.md](../mysql/01-InnoDB与MySQL的架构.md)（连接器/插件式存储引擎分层，
  本册只给"有哪些层"的任务清单，层内机制全在彼册）。
- 性能世界观入口（选读后跳）：[../Efficient_MySQL_Performance/01-查询响应时间.md](../Efficient_MySQL_Performance/01-查询响应时间.md)。
- 中文入门对照：[../MySQL必知必会.md](../MySQL必知必会.md)（开发者轴）；[../高性能mysql.md](../高性能mysql.md) 第 1 章同题但含更多硬件史。
- 分叉史预告（波尾义务 A）：同波 #57 `Migrating_to_MariaDB/` 只登记不链。

## 1.5 八.0 明星特性展开（管理员视角，⚠️ 手册主题域重构）

1. **窗口函数与 CTE**：`RANK() OVER (PARTITION BY …)`、`WITH RECURSIVE`——巡检 SQL 从"变量接力"变回集合运算；
   递归 CTE 直接支撑了"表空间→表→分区"三级 information_schema 联动报表的写法简化。
2. **公用表表达式 + 物化优化**：8.0 对派生表/CTE 的合并与物化策略改了多版，EXPLAIN 形态对比放 12 章实操口径。
3. **JSON 增强**：`JSON_TABLE`（8.0.4+）把 JSON 数组拍平成关系行——"文档能力"第一次真正进入 DBA 工具箱；
   与多值索引（8.0.17，见 [07-索引.md](07-索引.md)）配套构成"关系-文档混合"叙事。
4. **角色与密码策略组件化**：`CREATE ROLE`/`SET DEFAULT ROLE`；validate_password 插件→组件（13 章扩展框架的首个落点）。
5. **二进制日志与复制内核**：GTID 默认 ON、事务压缩、写集并行（8.0.26，成书后）——8 章主线。
6. **数据字典原子 DDL**：DDL 不再留半成品对象（8.0 最被低估的企业级特性，5 章在线改表语境复用）。
7. **优化器新武器清单**：降序索引、不可见索引、直方图（`ANALYZE TABLE … UPDATE HISTOGRAM`）、
   `EXPLAIN ANALYZE`（8.0.18）——12 章的弹药库。

## 1.6 读法建议（本册特色：任务清单体）

1. 把 1.2 表打印贴墙——本书后 14 章每一条 `SET`/`GRANT` 都要先过这张表（5.7 时代教程的默认值多数已变）。
2. "简介"章没有代码包不是偶然：Packt 仓库从 Chapter02 起有 SQL/命令清单（✅ GitHub tree 实抓），
   印证本书从"安装"才进入动手环节。
3. 全书读法按"装机线（2-3）→建模线（4-7）→扩展线（8-10）→防线（11/15）→性能线（12/14）→生态线（13）"六段推进，
   任何一段都可以被 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第四节阅读地图直接跳入。
4. **2026 语境防坑清单**（本目录的统一翻译规则）：
   - 凡"8.0 新"字样 → 默认已是 8.4 LTS 基线，不再是卖点；
   - 凡"5.7 兼容"字样 → 8.4 起大量兼容项被移除，按 ⚠️ 处理；
   - 凡插件（plugin）语境 → 优先查是否已有组件（component）等价物（13 章）；
   - 凡"支持期内"字样 → 一律以 ✅ endoflife.date 实抓日期为准（1.3 节）。

## 核心概念速览（中英对照）

- **数据字典** — Data Dictionary：8.0 起表/列/权限等元数据集中存于受保护的 InnoDB 表，消除 frm 与运行时状态两张皮。
- **破坏性变更** — breaking change：如移除查询缓存、GROUP BY 去隐式排序、默认认证插件更换，升级前必须逐项核对。
- **utf8mb4** — 8.0 默认字符集：完整 Unicode（含 emoji）四字节编码，与 5.7 默认 latin1 的索引长度预算完全不同。
- **caching_sha2_password** — 8.0 默认认证插件：SHA-256 + 服务端缓存快速路径，替代 mysql_native_password。
- **GTID 事务** — Global Transaction Identifier：uuid:number 全局事务号，8.0 默认开启，简化故障切换（详见 08 章）。
- **窗口函数** — Window Function：8.0 SQL 层头号补强（RANK/OVER），管理员用它写报表型巡检 SQL。
- **公用表表达式** — CTE（WITH 子句）：8.0 支持递归 CTE，运维脚本可读性大增。
- **不可见索引** — Invisible Index：对优化器隐藏但继续维护的索引，8.0 起用"删之前先隐身"的安全流程。
- **LTS / Innovation** — 长期支持版/创新版：2023 后 MySQL 版本双轨制，本书成书时尚不存在，读时须映射（1.3 节）。
- **DML/DDL** — 数据操纵/定义语言：简介章给管理员的最小语法地图（SELECT… 与 CREATE/ALTER…）。
- **信息模式** — INFORMATION_SCHEMA：8.0 数据字典的用户视图门面，巡检与监控全靠它（⚠️ 表列以手册为准）。
- **原子 DDL** — Atomic DDL：一条 DDL 要么全成要么全败，8.0 起不再留下"半截表"（1.5 节第 6 条）。
- **直方图** — Histogram：列值分布统计（等高桶/TopN），补 B+ 树统计信息盲区，8.0 优化器新输入（12 章）。
- **X DevAPI** — X 协议开发接口：8.0 随 X Plugin 提供的文档/对象关系双模 API（13 章生态位）。
- **mysql_native_password 停用线** — 默认认证插件迁移：8.0 换 caching_sha2、8.4 默认停用 native，横跨全书的最大兼容坑。
- **查询缓存移除** — Query Cache removal：8.0 直接删除整条缓存路径，5.7 经验清单第一行作废项。

## 最新演进与工业实践

- **版本线 2026 现状**（✅ https://endoflife.date/mysql 与其 `/api/mysql.json`，2026-09-27 实抓，curl 200）：
  8.0 EOL 2026-04-30；8.4 LTS 为当前生产主力（支持到 2029-04-30/延保 2032-04-30）；Innovation 线已至 9.7（2026-04-21）。
  工业口径：**新立项一律 8.4 LTS，本书中"8.0 独有卖点"多数已回灌为 8.4 基线**。
- **8.0→8.4 增量语义**（⚠️ 手册主题域转述，规范链接 dev.mysql.com/doc/refman/8.4/en/，本环境 403 仅书目引用）：
  8.4 默认 mysql_native_password 插件"默认停用"（非删除）、JSON_TABLE/JSON 函数扩充、副本降级等。
- **向量与 AI 语境**：9.x Innovation 引入向量类型相关能力属 Oracle 官方口径，⚠️ 本目录未取得一手 changelog，不作结论；
  工业界当前更常见的"MySQL + 向量"路线是走应用层（⚠️ 转述，检索见 2026 社区文章）。
- **经典对照读物**：8.0 新特性官方权威列表见 dev.mysql.com "What's New in MySQL 8.0"（⚠️ 403 规范链接）；
  中文社区可达镜像 https://mysql.net.cn/doc/refman/8.0/en/introduction.html （✅ 2026-09-27 实测 200）。
- **本仓对位实践**：读本章后接 [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md)
  建立"性能=查询响应时间"度量观，再回本册动手章，是本波实测缺席环境下的最优路径。
