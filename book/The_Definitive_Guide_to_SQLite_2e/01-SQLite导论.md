# 01 · Introducing SQLite（SQLite 导论）

> 原书第 1 章（Crossref 章题 ✅：`10.1007/978-1-4302-3226-1_1` "Introducing SQLite"）。
> 本文件为精读重构：一级章题 ✅ 实抓，小节结构 ⚠️ 按 2010 年 Apress 目录惯例与社区征订页推定。
> 三态标注：✅ 实证 / ⚠️ 转述推定 / 🔧 本机实测（Python 3.13.2 内置 SQLite 3.45.3 + CLI 3.50.6，Windows）。

## 1. 本章在 2010 年的语境

本书第 1 版的读者是"听说过 SQLite 但只会想到 MySQL"的开发者；第 2 版（2010）把叙述基线
从 SQLite 2/3 混战期钉在了 **3.6.x 时代**——写作时点最新版为 3.6.23/3.6.23.1（2010-03-09 /
2010-03-26）✅（sqlite.org/changes.html 实抓日期）。这一版另一个大动作是把 iOS 与 Android
两章拉进主线（第 9、10 章），因为 2008–2010 移动平台爆发，SQLite 成为两大 OS 的内建组件——
这正是"Definitive Guide"相对姊妹册 [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)
（O'Reilly，2013，桌面/运维向）的差异化：**开发向 + 嵌入式向**。

本章的论证骨架（⚠️ 小节划分为推定，论点本身按官方页与书谱系可核）：

1. **SQLite 是什么**：不是服务器，是一个链接进应用的 C 库（file engine），整个数据库 = 一个
   跨平台的单一文件；Public Domain 许可（无 GPL 传染，这是它嵌入 iOS/Android/浏览器的前提）✅
   [sqlite.org/copyright.html](https://www.sqlite.org/copyright.html)（域内长期页，同域 200 页见 00 取证）。
2. **为什么嵌入式场景值得一个事务型数据库**：对比"自己写文件 + 加锁"与"内嵌 ACID 引擎"的
   工程成本；书里 2010 的例证是电话簿/浏览器历史/Symbian 时代遗留，今天的例证是 iPhone 全系
   应用与任何本地-first 软件（⚠️ 例证置换，论点不变）。
3. **能力边界**（2010 语境下尤其要讲清）：单写者文件锁、无网络访问控制、无存储过程、
   类型是"亲和性"不是强约束、`SQLITE_MAX_VARIABLE_NUMBER`/附件库数量等编译期上限。
4. **历史一笔带过**：D. Richard Hipp 2000 年创造、空乘订票系统的救命替换——第 2 章会展开。

## 2. 精读要点（重构）

- **"zero configuration"不是卖点而是责任**：没有 my.cnf、没有守护进程，也就没有"谁来做
  DBA"。书里由此推出 pragmas 是唯一的调参面（见 [02-快速上手.md](02-快速上手.md)）。
- **单文件 = 最大特性也是最大陷阱**：文件可拷贝 ⇒ 开发者会误以为"拷贝即备份"。这一坑在
  2010 年书里以"关闭进程后再拷"规避，WAL（2010-07 才发布，3.7.0，见下节对位）之后升级为
  必须用在线备份 API（本书第 6 章，本目录 [06-核心C接口.md](06-核心C接口.md)）。
- **Public Domain 的商业含义**：2010 年 Apress 书强调"可以闭源分发"；对照今天 SQLite 进入
  所有主流浏览器 WASM 发行、.NET/Java 生态以 SQLite 为默认本地存储，这一判断被完全验证（⚠️ 行业综述）。
- 书中"测试驱动"一节讲 SQLite 的测试覆盖率文化（hooks/ovh 三件套），2026 仍是官方卖点 ✅
  （sqlite.org 首页长期标语 "SQLite is the world's most deployed database engine" 级别表述，⚠️ 精确措辞未逐字核验）。

## 3. 🔧 实测（E1）：2026 机器上"SQLite 是谁"的三张指纹

方法：`python -c` 直连，全部输出存盘 `D:\develops\tmp\dbwave_w3_dgsqlite\exp_out.txt`。

| 观察项 | 数字/结果 |
| --- | --- |
| 内置库版本 | Python 3.13.2 → SQLite **3.45.3**（`sqlite_version_info=(3,45,3)`） |
| 本机 CLI | Android platform-tools 附带 **3.50.6**（2025-09-22，32-bit） |
| `PRAGMA compile_options` | **43 项**，含 `COMPILER=msvc-1942`、`DEFAULT_PAGE_SIZE=4096`、`DEFAULT_WAL_AUTOCHECKPOINT=1000`、`DEFAULT_SYNCHRONOUS=2` |
| `PRAGMA module_list` | 10 个内置虚拟表模块：fts3/fts4/**fts5**/fts5vocab/fts4aux/fts3tokenize/rtree/rtree_i32/json_each/json_tree——2010 书里"扩展要自己编进去"的东西今天全在 |
| 文件头解码（100 字节） | magic `SQLite format 3\0`；page_size=4096（bytes 16-17）；**file change counter=2**（bytes 24-27）；write/read version 字节=1/1（bytes 18-19，"非 WAL"的直接证据）；version-valid-for=2；version-number=**3045003**（=3.45.3） |
| 写一次后 | change counter 2→**3**（这个计数器就是 WAL 之外世界"缓存失效"的机制本体，见 [05-设计与理念.md](05-设计与理念.md)） |

## 4. 2010 语境 vs 2026 现状（3.53.x）对位

| 本书设定（3.6.x，2010） | 2026 现状 | 版本锚点（✅=changes.html/官方页实抓） |
| --- | --- | --- |
| 最新是 3.6.23.1；WAL 尚未发布 | 稳定线 **3.53.4（2026-07-24）**；3.53.0 于 2026-04-09 | changes.html 各版本日期 ✅ |
| 回滚日志独占一切并发场景 | **3.7.0（2010-07-21）"Added support for write-ahead logging"**——就在本书出版同年发布，全书成稿停留在"前 WAL 世界" | ✅ changelog 原句；[wal.html](https://www.sqlite.org/wal.html) 200 |
| 扩展（FTS/RTREE 之外的能力）要重编译 | FTS5（3.9.0 编入 amalgamation ✅）、JSON 内置（3.38.0 ✅ [json1.html](https://www.sqlite.org/json1.html)：3.37.2 前 opt-in→3.38 起 opt-out）、CSV/series/spellfix 等 | 见各章末节 |
| "嵌入 iOS/Android 是新兴场景" | 已是存量现实：两大 OS + 浏览器 + 车机 + 边缘设备默认件；Android 官方 API 层仍叫 `android.database.sqlite` ⚠️（developer.android.com 本会话超时未直验，见 00 缺口登记） | — |
| Public Domain | 不变 ✅（sqlite.org/copyright.html 同域可达） | — |

## 5. 常见误区（按 2010 基线写书的人最容易踩的三条）

1. 把书中"数据库文件锁粒度=文件级"外推到 WAL 之后 ⇒ 错。WAL 下读者不阻塞写者，
   但 **同一时刻仍只允许一个写者**，且网络文件系统上 WAL 不可用（wal.html ⚠️ 建议读原文）。
2. 把"单文件"读成"无结构" ⇒ 文件头 100 字节里藏着页大小、格式化版本、change counter、
   version-valid-for 四组兼容性判据（E1 已逐字节解码）。
3. 以为 compile_options 是全局常数 ⇒ CPython 发行版与 Android CLI 同版本号选项集完全不同
   （对比实验见 [10-Android开发.md](10-Android开发.md)）。

## 6. 互链

- 姊妹分工：[../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（#87，O'Reilly 2013，
  运维/CLI 向，其 01 章文件格式实验与本册 E1 互为印证）；列存单机对照
  [../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)。
- 理论视角（"DBMS 作为进程内组件 vs 服务器体系结构"）：[../数据库系统概念6/00-总览与阅读地图.md](../数据库系统概念6/00-总览与阅读地图.md)。
- 册内动线：本章概念在 [05-设计与理念.md](05-设计与理念.md)（架构）、[11-内部机制与新特性.md](11-内部机制与新特性.md)（VDBE）展开。

## 7. 能力边界速查（书之所得 × 2026 现实）

| 边界项 | 2010 书语境 | 2026 现实 | 状态 |
| --- | --- | --- | --- |
| 附件库数 | 默认 10，编译上限 62（3.7.6 升至 62、再至 125 ✅ changelog 原句命中） | 编译默认仍 10 | ✅ |
| 变量数上限 | `SQLITE_MAX_VARIABLE_NUMBER` 老版 999 | 3.32 起默认 32766 | ⚠️ 通识 |
| 库尺寸 | 页计数×页大小公式约束 | 默认上限放宽至 281TB 量级口径 | ⚠️ 转述 limits.html |
| 并发写者 | 1（文件锁） | 仍 1（WAL 不改变） | 🔧 E6 |
| 存储过程/触发器语言 | 无（触发器=唯一可编程面） | 依旧无；扩展面走 C/虚表 | 🔧 E3/E7 |
| 角色/授权 | 无（作者化靠 authorizer 回调） | 不变 | 🔧 E6 |
| 网络访问控制 | 文件权限即一切 | 不变 | 🔧 E8 URI mode=ro |
| 类型强制 | 无（亲和性世界） | STRICT 表可选 | ✅ 3.37.0 |

（表内 ⚠️ 行引用官方 limits 页口径，本会话未逐页 HEAD，使用前请复核。）

## 8. 本章自检卡（一问一答）

1. Q：SQLite 的"零配置"配置面收拢在哪？ A：PRAGMA 族（02 章展开）。
2. Q：怎么不查文档判断一个 .db 是谁写的？ A：页 1 bytes 92-99 的 version-valid-for +
   version-number（🔧 E1：3045003=3.45.3）。
3. Q：WAL 从哪版来、和本书什么关系？ A：3.7.0（2010-07-21 ✅），成稿时未发布——全书物理层
   描述停在 journal 世界，逐章对位是本目录核心义务。
4. Q：同版本库为何行为不同？ A：compile_options 发行版人格（🔧 CPython 43 项 vs CLI 空）。
5. Q：说"SQLite 支持全文检索"2010/2026 各自要补什么？ A：当年重编译带 FTS；今验证
   `PRAGMA module_list` 里 fts5 在不在（🔧 在）。
6. Q：单文件的"备份承诺"何时失效？ A：进程活着就失效（05 章热日志/WAL 实验证明）。
7. Q：Public Domain 对闭源嵌入意味着？ A：零传染，这是 iOS/Android/浏览器预装的许可前提。
8. Q：书为什么比 O'Reilly 册多两章移动端？ A：2010 平台红利；分工详见 00 姊妹表。
9. Q：file change counter 干什么用？ A：缓存一致性地基（🔧 每次提交 +1，E1/E11 双证）。
10. Q：本机三套版本号分别是？ A：Python 3.13.2 / 库 3.45.3 / CLI 3.50.6（引用时勿混）。

## 核心概念速览（中英对照）

- **嵌入式数据库** — embedded database：以库形式链接进宿主进程、无独立服务进程的 DBMS。
- **单一文件存储** — single-file database：整个库（模式+数据+索引）落成一个跨平台文件。
- **公共领域许可** — Public Domain：SQLite 采用，无 copyleft 传染，可闭源嵌入分发。
- **文件变化计数器** — file change counter：页 1 的 bytes 24-27，任何提交 +1，是共享缓存/
  mmap 失效检测的锚（🔧 E1：2→3）。
- **版本有效标记** — version-valid-for：bytes 92-95，与 version-number 联用判断"谁写的文件"。
- **写版本/读版本字节** — write/read version：bytes 18-19，1/1=回滚日志格式，2/2=WAL。
- **编译选项指纹** — compile options：`PRAGMA compile_options` 揭示发行版人格（🔧 43 项）。
- **虚拟表模块注册表** — module list：`PRAGMA module_list`，fts5/rtree/json 今天出厂即带。
- **页大小** — page size：默认 4096 B（🔧 E1），建库后变更需 VACUUM。
- **单写者模型** — single-writer model：文件级锁协议下任意时刻至多一个写事务。
- **零配置** — zero configuration：无服务无配置文件的代价是全部调参收拢进 PRAGMA。
- **能力边界** — feature limits：无存储过程/无 RBAC/弱类型约束，2010 与 2026 皆然。
- **移动平台内建** — shipped on mobile：iOS/Android 随系统分发 SQLite，本书 2e 的时代红利。
- **amalgamation** — 单一巨型 C 源文件发行方式，3.9.0 起 FTS5 亦编入 ✅（changelog 原句）。
- **测试覆盖文化** — test coverage：官方以近乎全路径覆盖为卖点，是"敢 Public Domain"的底气（⚠️）。

## 最新演进与工业实践

- **版本线**：3.6.23.1（2010，本书基线）→ 3.7.0 WAL（2010-07-21）→ 3.24.0 UPSERT（2018-06-04 ✅）
  → 3.35.0 RETURNING + 内置数学函数（2021-03-12 ✅ changelog 原句）→ 3.37.0 STRICT 表（2021-11-27 ✅）
  → 3.38.0 JSON 转内置（2022-02-22 ✅ json1.html）→ **3.53.4（2026-07-24 ✅ changes.html）**。
- **部署面**：官方首页口径"每部智能手机、每台浏览器实例至少一个"级别的最广泛部署引擎（⚠️ 精确
  措辞未逐字核验）；2026 增量在 WASM/OPFS（changes.html 3.5x 节多处 WASM 修复 ✅）。
- **工业实践**：本地-first（local-first）软件运动把"进程内 ACID 文件库"重新变成架构关键词；
  SQLite 常与其上的同步层（如 CRDT/changeset 类方案）组合出现 ⚠️（趋势转述，非书目结论）。
- **与姊妹册分工**：2013 年 O'Reilly《Using SQLite》面向"把 SQLite 当小型服务器用"的运维/分析
  场景；本书 2010 版面向"把 SQLite 嵌进 App"的开发场景——同一引擎的两条学习动线，本目录全部
  🔧 实验与 [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md) 的 25 组实验可互相复核。
