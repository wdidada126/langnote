# 第 2 章 MySQL 源代码基本要点（MySQL Source Code Basics ⚠️ 英文章题反构）

> 原书章：第 2 章（中文正版目录实抓：「MySQL源代码基本要点」）。二级小节**全部实抓**：Unix Shell / BitKeeper / 准备系统：从BitKeeper树构建MySQL / 从源代码分发版本构建 / 将MySQL安装到系统目录 / 源代码目录布局 / 准备系统：在调试程序中运行MySQL / 以调试程序为向导探索源代码 / gdb使用基本要点 / 在源代码中查找信息 / 值得关注的断点和变量 / 修改源代码 / 编码指南 / 不断更新BitKeeper知识库 / 提交补丁。
> 本章是全书「动手层」：教读者把 4.1/5.0 源码树立起来，在 gdb 里走一条 SQL。

## 2.1 本章地图

| 节群 | 内容 | 2007 年口径的结论 |
| --- | --- | --- |
| Unix Shell | 开发环境假设：*nix 命令行、脚本化构建 | Windows 是一等公民之外的二等平台 |
| BitKeeper 取树 | bk client 拉开发树；理解「树」与「tarball」的差别 | 开发树是权威，发布包是次等快照 |
| 构建与安装 | `./build.sh`/configure + make；安装到系统目录的布局 | autotools 时代的标准流程 |
| 目录布局 | `sql/` 内核、`client/`、`storage/`、`mysys/`、`include/`、`tests/` | 目录即架构：读码路线图 |
| gdb 走查 | 断点选择（命令分发、执行入口）、盯 THD 与协议变量 | 单线程走查是理解内核最快路径 |
| 修改与提交 | 编码指南（C 为主、保守可移植）；BK 补丁流 | 贡献流程尚未 Web 化 |

## 2.2 核心精讲（历史语境）

- **BitKeeper 时代**：MySQL 用 BitKeeper 管理公开开发树（免费工具换商业授权的独特生态位），小节「不断更新BitKeeper知识库」「提交补丁」即教读者与主干同步并把改动回传。这段是「为什么 MySQL 后来先用 Mercurial/Bazaar、2013 再迁 Git」的前史；读代码考古学的人，本章给出的其实是**版本管理四十年的一条支线**。
- **目录布局是穿越期最长的知识**：当年认下 `sql/sql_parse.cc`（命令分发）、`sql/sql_select.cc`（选择与执行）、`mysys/`（跨平台工具库）、`storage/<engine>/`，今天在 8.x 树里大部分**仍然有效**——只是新增了 `sql/auth/`、`sql/iterators/`、`sql/dd/`（数据字典 C++ 化）等，`sql/` 内部文件也更碎。
- **gdb 断点地图**（按书中思路转述）：连接线程收到包后进入命令分发（`dispatch_command`），由此分头进入解析（`mysql_parse`）、优化（`JOIN::optimize` 时代）、执行与 NET 回包。「值得关注的断点和变量」小节的本质是给 THD→协议→handler 三层对象做指针标注。
- **教学示意**（不参与构建）：`break dispatch_command` → 客户端发一句 `SELECT 1` → 单步进解析与执行。这条链在 8.0.18+ 只是换了执行器内脏（迭代器火山模型、`Query_expression::execute`），断点位置几乎原样可复用——本章知识「折旧率」全书最低。
- **编码指南的时代性**：2007 年指南以 C 为主：显式资源管理、避免 STL、可移植性优先。今日树内 handler/执行器/DD 均为 C++14/17，并引入 clang-format 统一风格——「读旧码用旧规范、提交新码看 CONTRIBUTING」的分裂正是本章内容今天需要人工打补丁的原因。

## 2.3 「历史语境」清单

| 书中做法 | 今天（8.x 源码） | 备注 |
| --- | --- | --- |
| bk client 拉 BitKeeper 树 | Git；官方镜像 GitHub mysql/mysql-server | 4.1/5.0 完整树官方已不提供 ⚠️ |
| build.sh + autotools | CMake 唯一入口（5.5 起过渡、8.0 固化） | 书中构建命令整体作废 |
| 「安装到系统目录」布局 | 仍类似（basedir/datadir 二分），但多出 keyring、组件目录等 | 概念兼容 |
| C 编码指南 | C++ 混合内核 + clang-format | 风格规范换代 |
| 邮件列表 + BK 提交 | GitHub PR / bugs.mysql.com 报告 | 贡献通道变化 ⚠️ 细则未实抓 |

## 2.4 常见误区与修正

| 误区 | 修正 |
| --- | --- |
| 「照书命令拉源码编译」 | BK 通道已死；改用 GitHub 镜像某 tag（如 5.0/5.1 归档 tag 视镜像收录 ⚠️）或发行版 SRPM |
| 「目录布局知识会过期」 | `sql/`、`mysys/`、`storage/` 三大分区三十年稳定；过期的是具体文件名与新增子层 |
| 「gdb 章节只是老黄历」 | 断点走查法仍是今天读 8.x 源码的第一课，只需把执行器断点换成迭代器 |

## 2.5 与《MySQL 是怎样运行的》（../mysql/）对位

- mysql/ 目录**不读源码**、以行为与参数为轴（其 00 声明「不启动任何 MySQL 实例」，所有 SQL 标「教学示意」）；本书恰相反，第 2 章是全书方法论地基。
- 两书走查法对照：本书「gdb 断点走查」↔ 那本「EXPLAIN/optimizer trace 走查」（[../mysql/16-optimizer-trace.md](../mysql/16-optimizer-trace.md)）——代码级 vs 计划级，互补不互斥。

## 2.6 与其他书的联系

- 方法论互证：[../数据库系统实现.md](../数据库系统实现.md)（先骨架后细节的读码观）。
- 本目录内：布局认完看对象 → [03-核心类结构与变量.md](03-核心类结构与变量.md)；线程与请求生命周期 → [06-基于线程的请求处理.md](06-基于线程的请求处理.md)；协议入口函数走查 → [04-客户端与服务器通信.md](04-客户端与服务器通信.md)。
- 旧笔记：[../深入理解MySQL核心技术.md](../深入理解MySQL核心技术.md)。

## 核心概念速览（中英对照）

1. **BitKeeper** — BK：2000 年代 MySQL 使用的分布式版本工具，本书时代的取源方式。
2. **开发树** — development tree：主干源码，功能超前发布版约一个大版本。
3. **源代码目录布局** — source layout：`sql/`、`mysys/`、`storage/` 等目录到架构模块的映射。
4. **build.sh / configure** — 老构建脚本：autotools 时代入口，今已被 CMake 取代。
5. **gdb 走查** — source-level walkthrough：以断点+单步理解请求生命周期的方法。
6. **dispatch_command** — 命令分发函数：连接线程收到包后的总入口，经典断点位。
7. **THD** — thread descriptor：一线程一请求的核心上下文对象（第 3 章主角）。
8. **补丁流程** — patch workflow：BK 知识库提交时代贡献方式的统称。
9. **编码指南** — coding guidelines：当年以 C 为主、强调保守可移植的规范。
10. **mysys** — 基础工具库：跨平台封装（字符串/文件/线程原语）层。
11. **迭代器执行器** — iterator executor：8.0.18+ 替代旧 JOIN 推执行的内脏（对位用新词）。
12. **教学示意** — illustrative code：本目录所有片段仅供理解、不参与构建。
13. **化石层** — fossil layer：借指书中 5.0 机制在今日源码中的残留位置。

## 最新演进与工业实践

- **版本管理路线（转述）**：MySQL 内核 2005–2010 用 Mercurial、2010–2013 用 Bazaar（Launchpad 时代），2013 年迁 Git 并以 GitHub 为公开镜像——本书 BitKeeper 内容整体为前史。✅ 实测可达（200）：https://github.com/mysql/mysql-server 。
- **构建现状**：8.x 源码构建以 CMake 为唯一入口；boost 依赖策略随小版本变化 ⚠️（官方文档域 dev.mysql.com 对本网络 403，转述）。
- **调试实践**：今日走查一条 SELECT 仍从 `dispatch_command` 断起（`sql/sql_parse.cc` 位置未变 ✅ 可由 GitHub 树核验）；执行器新路径看 `sql/iterators/`；优化器行为核对可用 `optimizer_trace`（两书方法在 8.x 会师）。
- **旧版源码获取**：4.1/5.0 tarball 已不在官网下载列表 ⚠️；社区通行做法是发行版 SRPM 或第三方存档。本目录**不推荐未经验证的 PDF/源码镜像源**（版权与安全）。
- **社区贡献练手场**：Percona Server 公开接受 PR 且文档开放（✅ https://github.com/percona/percona-server ；✅ https://docs.percona.com/percona-server/8.0/threadpool.html ），是把「读懂本书第 2 章」变现为「提交过 MySQL 系补丁」的现实路径。
- **仓库配套文件**：本书示例引擎官方镜像含 `ha_csv-4.1.cc/.h` 与 `ha_csv-5.1.cc/.h` 两版（✅ 实测文件存在于 https://github.com/dev2sec/Understanding-MySQL-Internals ），恰好演示了「跨大版本维护 SE 示例」的接口漂移——这比任何文字都直观地说明 4.1→5.1 handler API 变了多少。
