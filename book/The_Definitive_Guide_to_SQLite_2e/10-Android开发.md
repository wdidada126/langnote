# 10 · Android Development with SQLite（Android 上的 SQLite）

> 原书第 10 章（Crossref 章题 ✅：`..._10` "Android Development with SQLite"）。小节划分 ⚠️ 推定。
> 取证优势声明：本机 `sqlite3` CLI **即 Android platform-tools 发行件（3.50.6，32-bit）**——
> 与 Android 系统同一血统的构建，本章 🔧 是真·平台发行实测（引擎同源；设备内 Java API 层仍 ⚠️）。

## 1. 本章在 2010 年的语境

2010 = Android 1.5/1.6/2.x 时代，SQLite 是平台钦定本地存储：`SQLiteOpenHelper`/`SQLiteDatabase`
Java 包装 + 游标遍历是教科书姿势（当年教程 API 群像 ⚠️ 转述）。书中该章的知识点：

1. **平台封装三层**：JNI（android_database_sqlite.cpp）→ Java `android.database.sqlite` →
   ContentProvider 协议——SQLite 在 Android 不只是库，还是**组件间数据总线**的地基。
2. **升级仪式**：`onCreate/onUpgrade` 版本迁移模式（`user_version` PRAGMA 的工程化 ✅，
   🔧 E1：默认 0；官方推荐拿它当 schema 版本戳——Android 框架就是这么做的 ⚠️ 转述）。
3. **事务与锁的设备语境**：`beginTransaction/setTransactionSuccessful` 包装；`SQLiteDatabaseLocked`
   异常 = SQLITE_BUSY 的 Java 化；单写线程模型被框架强制（02 章协议的平台回声）。
4. **`SQLiteQueryBuilder`/注入防御**：selection 参数模板化——2010 SQL 注入焦虑的框架答案。

## 2. 精读要点（重构）

- 本章真正的长期价值在**"平台如何驯服一个嵌入式引擎"**：用 Java 门面消灭裸句柄、用模板
  消灭字符串拼接、用单写队列消灭 busy 风暴——三条纪律在 2026 的任何 SQLite 嵌入层（浏览器
  OPFS 包装、游戏引擎封装）都原样重现。
- 2010 的 Android 特有坑（书中重点）：Cursor 不 close → 数据库锁滞留；`query()` 返回的
  CursorWindow 大小上限（约 2 MB ⚠️ 精确值随版本变）；跨进程 ContentProvider 游标的
  Binder 传输预算。
- 与 iOS 章（[09-iOS开发.md](09-iOS开发.md)）的镜像差异：Android 从第一天就把"自带新版
  SQLite 进 APK"当常规操作（APK 可带 .so），而 iOS 当年被审核压制 ⚠️——同一引擎，两种发行政治。

## 3. 🔧 实测（E9+E10，platform-tools CLI 3.50.6 = Android 血统发行件）

| 观察 | 数字/结果 |
| --- | --- |
| 发行件人格 | `PRAGMA compile_options` **空返回**（CPython 发行 43 项对照 🔧 E1）——系统发行=保守编译铁证 |
| `PRAGMA journal_mode=WAL` | `wal` 成功；事务中三文件显形（同引擎行为，05 章 E5 已量：db 4096 B/-shm 32768 B/-wal 8272→45352 B） |
| 递归 CTE 灌 20,000 行 + 聚合 | `.mode box` 输出 `n=20000`；查询 Run Time real **0.002 s** |
| 无索引范围查询计划 | `SCAN m`（EQP 一行流 ✅；建 `ix` 后 sqlite_master index 计数 1） |
| 整数溢出语义 | `CAST(9223372036854775808 AS INTEGER)` → `9223372036854775807`（与 CPython 发行一致，钳制非报错） |
| CLI 退出后的 WAL 清理 | 目录只剩 `cli.db`，-wal/-shm 消失（最后连接检查点删除 ✅） |
| CLI 事务对照（E10，`cli2.db`） | `BEGIN; INSERT×3; COMMIT` Run Time **0.029 s**（含建两表），裸 autocommit 建表 0.002 s 级 |
| 单语句 autocommit 成本（python，同引擎） | 300 条插入：FULL 3.0 ms/条，OFF 1.2 ms/条；**NORMAL 5.6 ms/条**（Windows fsync 抖动，⚠️ 单次采样） |

设备内验证清单（无真机 ⚠️，登记为读者作业）：`adb shell` 进应用 db 目录看 -journal/-wal；
`ContentResolver` 游标跨进程尺寸上限复测——机制面由 🔧 桌面同引擎实验背书。

## 4. 2010 语境 vs 2026 现状对位

| 本书设定（Android 1.x/2.x） | 2026 现状 | 锚点 |
| --- | --- | --- |
| 直接 `SQLiteOpenHelper` | 官方推 **Room**（编译期查询校验 + schema 迁移 DSL），底层仍是 `androidx.sqlite`→系统 SQLite | developer.android.com 超时未直验 ⚠️（文档名 Room 为通识 ✅） |
| 系统 SQLite 版本≈3.6.x 时代 | 现代设备系统库已 3.4x+；本机 platform-tools 携带件即 **3.50.6**（🔧 版本串含 2025-09-22 源戳） | `sqlite3 --version` 🔧 |
| WAL 尚未出生（成书时点） | Android 官方曾长期默认 journal、Room 时代 WAL 为推荐；闪存 + `synchronous` 权衡是设备级课题 ⚠️ | 3.7.0 ✅ changelog |
| `attach`/`load_extension` 手工活 | 系统发行不提供装载口（🔧 E9 空 options 旁证）；需扩展=自带 .so 重编译 | 07 章同题 |
| ContentProvider 是数据共享正解 | 仍兼容存在，但跨应用共享重心转向文件/云；Provider 的 SQL 注入面教训进入安全教材 ⚠️ 转述 | — |

## 5. 常见误区

1. 把 Java 层异常当锁语义：`SQLiteDatabaseLockedException` 背后就是 02 章的 SHARED/RESERVED
   协议（🔧 E6 同场景 C 直拍）；超时预算在框架层被重写，勿用默认值裸奔。
2. 以为自带 .so 即安全：多 APK 各带不同引擎版本 + 同库文件 = 格式/旗标分裂（01 章
   "发行版人格"跨应用复发）。
3. 忽视 CursorWindow 上限做 `SELECT *` 大字段：设备症状"游标空/崩溃"，桌面 CLI 同语句无感
   （⚠️ 平台特定，机制归属 Binder/窗口拷贝）。
4. 把 `user_version` 当业务字段：它就是为 schema 迁移保留的（🔧 E1 默认 0，Room 的 schemaId
   体系在其上 ⚠️）。

## 6. 互链

- 同引擎不同发行对照实验：[01-SQLite导论.md](01-SQLite导论.md)（CPython 43 项）、
  [09-iOS开发.md](09-iOS开发.md)（发行政治）。
- 姊妹册 CLI 章（`.import`/点命令全表）：[../Using_SQLite/03-命令行Shell的配置与使用.md](../Using_SQLite/03-命令行Shell的配置与使用.md)。
- 事务/锁机制本体：[02-快速上手.md](02-快速上手.md)、[05-设计与理念.md](05-设计与理念.md)。
- 官方文档入口（本会话不可达，登记缺口）：`android.database.sqlite` / Room 指南 ⚠️。

## 7. 读者真机作业单（把 ⚠️ 变成你机器上的 🔧）

```bash
# 1) 进任意 root/调试设备，观察文件生命周期
adb shell
cd /data/data/<pkg>/databases
ls -l                    # 看 .db / .db-journal / .db-wal / .db-shm 的在场条件
sqlite3 app.db 'PRAGMA journal_mode;'   # 设备自带 CLI 同款探测
# 2) 制造"崩溃+热日志"：app 内开事务插入后 kill -9，重进看行数回滚
# 3) ContentProvider 大字段：SELECT * 拉 >2MB BLOB，观察 CursorWindow 异常文案
```

（以上为操作步骤设计，本会话无设备，结果一律待验 ⚠️；机制预期全部由 05/02 章 🔧 实验背书。）

## 8. 框架层↔引擎层名词对译（Java 读者救急表）

| Java/框架面 | C/引擎真相 | 本册实验锚 |
| --- | --- | --- |
| `beginTransaction()` | BEGIN(DEFERRED) + 框架锁 | E2 |
| `setTransactionSuccessful()+end()` | COMMIT/ROLLBACK | E2 savepoint |
| `SQLiteDatabaseLocked` | SQLITE_BUSY | 🔧 E6 0.534 s 等待 |
| 单写连接队列 | 单写者协议的上层化 | 05 章矩阵 |
| `onUpgrade(db,old,new)` | `user_version` 比较 + 迁移 SQL | 🔧 E1 默认 0 |
| `insertWithOnConflict(REPLACE)` | INSERT OR REPLACE（换 rowid 陷阱） | 🔧 E4 分叉 |
| Room `@Query` 校验失败 | 引擎 prepare_v2 编译期报 | 06 章 |
| WAL 禁用位（旧框架） | journal_mode=delete 钉死 | E9 可自开 WAL |

## 9. 本章自检卡（一问一答）

1. Q：本机 CLI 与 Android 什么关系？ A：platform-tools 发行件，同血统构建 🔧 3.50.6。
2. Q：系统发行给你扩展位吗？ A：options 空=没编（🔧 E9）；自带 .so 是唯一正路。
3. Q：框架为什么强推事务 API？ A：fsync 账单 + 锁滞留双杀（🔧 E2/E6 桌面同景）。
4. Q：-wal 何时消失？ A：最后连接关闭检查点后（🔧 E9 vs E5 两态）。
5. Q：ContentProvider 游标能跨进程随意大？ A：窗口尺寸上限约束（⚠️）。
6. Q：user_version 被谁征用？ A：OpenHelper/Room 迁移体系（🔧 字段存在）。
7. Q：Java 层异常等价 C 错误码吗？ A：粗粒度映射，扩展码信息会丢（06 章码表对照）。
8. Q：2010 手写 SQL 注入防御现在谁管？ A：编译期校验 + 模板化 API（框架答案，语义仍归引擎）。
9. Q：自带新引擎的代价？ A：包体 + 同库多引擎版本分裂风险（09 章"发行政治"对句）。
10. Q：本章 🔧 能替代真机测试吗？ A：不能——替代的是"机制理解"，替代不了"平台行为"。

## 核心概念速览（中英对照）

- **SQLiteOpenHelper** — Android 建库/升版门面（onCreate/onUpgrade）。
- **SQLiteDatabase** — Java 包装：query/insert/beginTransaction 族。
- **ContentProvider** — 组件间数据总线：游标跨进程协议。
- **CursorWindow** — 游标结果窗口：设备侧隐式尺寸上限（⚠️）。
- **user_version** — schema 版本戳 PRAGMA（🔧 E1 默认 0）。
- **单写队列** — 框架强制的写线程模型：SQLITE_BUSY 的上层消解。
- **Room** — 2026 官方 ORM 层：编译期校验 + 迁移 DSL（⚠️ 名称通识）。
- **platform-tools 发行件** — 🔧 本机 CLI 3.50.6：Android 血统构建。
- **空 compile_options** — 系统发行人格（🔧 E9）。
- **自带 .so** — APK 打包自定义引擎的 Android 特权（对照 iOS 审核史 ⚠️）。
- **SQLiteQueryBuilder** — selection 模板化：注入防御的框架答案。
- **WAL 清理时机** — 最后连接关闭（🔧 文件表两态证据）。
- **fsync 档位** — FULL/OFF/NORMAL 设备闪存语境再解读（🔧 3.0/1.2/5.6 ms）。
- **adb 实验清单** — 真机验证的读者作业面（⚠️ 缺口登记）。

## 最新演进与工业实践

- 系统引擎线：本机 platform-tools 携 3.50.6（2025-09 源戳 🔧），说明 Android 发行链与上游
  3.5x 同步节奏良好；3.53.4（2026-07-24 ✅）为上游最新。
- 应用层线：Room + Coroutines/Flow 的响应式查询（挂起函数包查询）成默认写法 ⚠️（文档不可达，
  按社区共识标注）；本书"手工 Cursor 遍历"手艺退守到性能剖析与救火场景。
- 跨端观察：Kotlin Multiplatform/Flutter/sqlite3_flutter_libs 让"自带引擎"再次成为主流，
  2010 年"用系统库省包体"的权衡公式已反转（⚠️ 趋势转述）。
- 取证纪律：本文件所有设备内行为（CursorWindow 大小、审核政策、版本滞后）未本机复现者
  一律 ⚠️；CLI 血统件给出的 🔧 数字可跨到桌面直接复核。
