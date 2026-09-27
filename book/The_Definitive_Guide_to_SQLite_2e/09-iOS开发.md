# 09 · iOS Development with SQLite（iOS 上的 SQLite）

> 原书第 9 章（Crossref 章题 ✅：`..._9` "iOS Development with SQLite"）。小节划分 ⚠️ 推定。
> 取证边界：本机无 macOS/iOS，**iOS 系统库行为一律 ⚠️ 转述**；🔧 实验是"发行版人格"类比
> 实验（用本机 Android-lineage CLI 3.50.6 演示"系统自带 SQLite"的通用形态，非 iOS 实测）。

## 1. 本章在 2010 年的语境

2010 年正是 iPhone OS 4.0 时代，书里这一章的原始素材：iPhone 自带 libsqlite3.dylib，
Objective-C 时代没有官方 ORM，开发者直接对 C API 编程或用社区包装（FMDB 同年诞生 ⚠️ 转述）。
本章的知识点构成：

1. **系统库使用姿势**：工程链接 `libsqlite3.dylib` + 头文件即得 C API；**不可**自带新版替换
   （当时 App Store 审核与符号冲突的告诫 ⚠️）。
2. **沙盒文件布局**：数据库放 Documents/Library（2010 的 iCloud 同步语义分界是热门话题 ⚠️）；
   "单文件=沙盒资产"与备份/同步策略的拉扯——这正是 01 章"文件即数据"理念的平台化。
3. **移动端锁纪律**：后台任务超时（watchdog）与 SQLITE_BUSY 重试预算；主线程不跑长查询的
   最早形态告诫。
4. **移动 SQLite 的普适机制**：journal/WAL 文件行为、`synchronous` 与断电（手机=常断电设备，
   书中把 FULL 档劝退语气调到最高）——机制与平台无关，可迁移到本册其他章。

## 2. 精读要点（重构）

- 章眼的时代判断：**"SQLite 是移动应用的默认存储层"**——2010 年写来是前瞻，2026 年是考古
  正确性的证明；但当年围绕它的手艺（手写 C 包装、sqlite3_stmt 生命周期管理）被 Core Data
  （内嵌 SQLite store）与后来的 GRDB/FMDB 抽象吸收 ⚠️（生态史转述）。
- Apple 侧 2026 现状：系统仍随附 SQLite（版本与节奏由 OS 更新决定，**不保证与上游同步**；
  `sqlite_source_id` 自证口径 ⚠️ 未本机可验）；SwiftData/Core Data 在其上；直接链 C API 仍可行。
- 值得保留的跨平台教训：手机文件系统（flash + 电源不可靠）让"提交点=安全点"的日志协议
  成为刚需——05 章的崩溃实验在移动语境就是日常。

## 3. 🔧 实测（类比窗）：系统自带发行版的"人格指纹"

方法声明：本机无 iOS；用 Android-lineage CLI 3.50.6（同一"系统自带库"现象学）跑同构检查，
外推逻辑：`compile_options` 空返回=发行方未导出自定义编译旗标，与 Apple/Android 系统库的
保守裁剪姿态一致（姊妹册 🔧 已证 platform-tools 版空返回，本册复现 ✅）。

| 检查项（CLI 脚本 `cli.sql`） | 结果 |
| --- | --- |
| `PRAGMA journal_mode=WAL` | 返回 `wal` ✅（系统发行版同样全功能 WAL） |
| 20,000 行递归 CTE 造数 + `.mode box` 查询 | `n=20000`，`av` 正常输出，Run Time real 0.002 s |
| `EXPLAIN QUERY PLAN SELECT * FROM m WHERE v>0.5`（无索引时） | `SCAN m` ✅ |
| `PRAGMA compile_options` | **空返回**（对照 CPython 发行 43 项 🔧 E1）——"发行版人格"铁证 |
| 溢出语义 `CAST(9223372036854775808 AS INTEGER)` | `9223372036854775807`（钳制到 int64 上界，全平台一致语义 ✅ 双发行复测） |
| CLI 退出后文件表 | 只剩 `cli.db`——**`-wal/-shm` 在最后连接关闭时检查点并删除**（对照 E5 中途三文件）|

对 iOS 迁移者的实际含义：不要假设系统库带任何编译旗标（load_extension 类能力在两家系统
库中都默认不可用 ⚠️+🔧07 章 CPython 证据旁支）；要新特性/装载能力就得自带 amalgamation
重编译——2010 书的建议今天仍是唯一路径。

## 4. 2010 语境 vs 2026 现状对位

| 本书设定（iOS4 时代） | 2026 现状 | 锚点 |
| --- | --- | --- |
| libsqlite3.dylib 手工链接 | 仍可用；Swift 时代主流是 Core Data/GRDB/FMDB 包装 ⚠️ | — |
| 系统 SQLite 版本滞后是常态 | 依旧滞后但幅度收窄；OS 大版本才整包升级 ⚠️（无法本机取证，登记缺口） | — |
| WAL 在 iOS 的适用争论（2010 尚无 WAL） | Apple 平台 WAL 广泛使用；网络卷/同步目录禁忌不变（wal.html ⚠️ 建议原文核对） | 3.7.0 ✅ |
| 备份=自己写文件复制仪式 | `sqlite3_backup_*`/`Connection`级 API 成熟；iOS 侧"关闭-拷贝-再开"仍是最笨但可用的方案 ⚠️ | [backup.html](https://www.sqlite.org/backup.html) ✅200 |
| 手机断电→FULL 保命 | 语义不变；WAL+NORMAL 的移动端权衡成为新范式 ⚠️（社区通行说法，未官方背书） | — |

## 5. 常见误区

1. 把"引擎一致"当成"发行一致"：SQL/事务语义同源（🔧 E9 溢出/扫描计划全同），**编译旗标
   面天差地别**（🔧 options 43 vs 0）——书中"iOS 上没有 FTS 要自己编"的教训按发行版重估。
2. 以为 -wal 文件常驻 ⇒ 最后连接关闭会检查点+清理（🔧 E9 文件表；移动"拷走 .db 即备份"
   的窗口因此存在，但**不可依赖**——E5 中途三文件就是反例）。
3. 在主线程跑 `VACUUM`/全表迁移：2010 watchdog 与 2026 功耗/ANR 是同一条物理线的延长。

## 6. 互链

- 姊妹册的平台章缺位由本册补足；镜像分工见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 对位表。
- 发行版人格实验的母题：[01-SQLite导论.md](01-SQLite导论.md)（E1）与 [10-Android开发.md](10-Android开发.md)（E9/E10）。
- 文件/日志机制本体：[05-设计与理念.md](05-设计与理念.md)。
- Android 官方文档入口（引用不作内容依据）：developer.android.com（本会话超时 ⚠️，见 00 缺口登记）。

## 7. 移动嵌入清单（2010 书 + 2026 实践合并版，两平台通用）

| 项 | 动作 | 本册依据 |
| --- | --- | --- |
| 建库时 | 定 `page_size`（对齐 flash 4K 🔧 两发行默认 4096） | E1 |
| 每次连接 | WAL + busy_timeout + synchronous 三件套集中设 | E2/E5 |
| 写路径 | 显式事务攒批；UI 线程只排短事务 | 🔧 E2 776× |
| 迁移 | `user_version` 版本戳 + 备份先行 | 🔧 E1/E6 |
| 崩溃面 | 冷启动先开库让热日志回滚，再谈业务 | 🔧 E5 崩溃实验 |
| 空间 | 删除后按需 FULL VACUUM（增量只削尾） | 🔧 E5 |
| 备份 | backup API 或"静默期三文件齐拷" | E5/E9 |
| 观测 | 发行版人格探测（version/compile_options 自报） | 🔧 E9 |

## 8. 类比窗方法论与 iOS 差分声明

类比实验证明的是**引擎共性**（SQL 语义、锁协议、WAL 文件生命周期、溢出钳制——🔧 全项）；
不能证明的是 **Apple 发行个性**（系统库具体版本、dyld 装载限制、审核政策、Core Data 之上
的行为差异——⚠️ 全部未本机取证）。引用本章 🔧 数字时请带此声明；iOS 真机最小验证动作：
`adb` 的对应物是设备端跑一段 C 探测 `sqlite3_libversion()/sqlite3_compileoption_used(...)`，
一次跑完即可回填本表右列（读者作业 ⚠️）。

## 9. 本章自检卡（一问一答）

1. Q：为什么系统自带 SQLite 反而要先查 compile_options？ A：功能面=编译期事实（🔧 空 vs 43）。
2. Q：iOS 上拷 .db 安全窗口何时出现？ A：最后连接干净关闭后（🔧 E9 wal/shm 消失态）。
3. Q：手机为何把 synchronous 话题权重拉满？ A：电源不可靠=崩溃模型常态化（05 章协议）。
4. Q：系统库能 load_extension 吗？ A：默认不能（07 章 CPython 旁证 + ⚠️ 平台政策）。
5. Q：溢出 CAST 的平台差异？ A：无——钳制语义跨发行一致（🔧 E9 双测）。
6. Q：EQP 在移动发行上降级吗？ A：不（🔧 `SCAN m` 同款输出）。
7. Q：WAL 在网络目录？ A：不可用（⚠️ wal.html）。
8. Q：备份 API 的页粒度为谁设计？ A：防长读事务挡写者（🔧 E6 pages=16 示范）。
9. Q：2010 手写 C 包装今天还有必要吗？ A：框架抽象之下锁语义仍在，出事仍需本章知识。
10. Q：类比窗与伪实测的分界？ A：显式声明"测的是谁、外推到哪"——本章每处 ⚠️/🔧 标注即分界。

## 核心概念速览（中英对照）

- **系统自带库** — system-shipped SQLite：OS 分发、版本由 OS 节奏决定的形态。
- **发行版人格** — build fingerprint：同版本不同 compile_options（🔧 43 vs 0）。
- **libsqlite3.dylib** — iOS 链接目标（⚠️ 2010 史实，2026 仍存）。
- **沙盒存储** — app sandbox：单文件理念在 iOS 文件布局中的落地。
- **watchdog 预算** — 移动主线程时间红线：busy 重试/长查询设计的约束源。
- **int64 钳制** — 溢出转 INTEGER 截顶语义（🔧 双发行一致）。
- **关闭即检查点** — last-connection WAL 清理（🔧 文件表证据）。
- **Core Data/GRDB/FMDB** — iOS 上层包装生态 ⚠️（2010→2026 演化线）。
- **自带 amalgamation** — 需要旗标能力的唯一路径（07 章同题）。
- **网络卷禁忌** — WAL over NFS 不可用（⚠️ 转述 wal.html）。
- **断电安全** — crash/power-loss durability：移动语境把 05 章协议推到台前。
- **类比窗方法论** — 不可跑平台的 🔧 替代：同引擎不同发行做差分，边界如实标注。

## 最新演进与工业实践

- 2010→2026 iOS 侧的常数：SQLite 仍是平台存储底座；变数：官方推荐入口从"C API 手工管理"
  移到声明式框架，但**性能/锁纪律课**反而绕不过去（框架泄漏底层事务行为时，本书知识复活）。
- Apple 发布说明显示其系统 SQLite 持续打安全补丁（CVE 响应线 ⚠️ 转述，未逐条核验）；
  上游 3.5x 的 WASM/浏览器线与 iOS 无直接交集。
- 实践建议（2026）：移动端一律 WAL + busy_timeout + 迁移批处理化；对"系统库版本"写探测代码
  （`sqlite_version()` 运行时自报）而非硬编码假设——本册 🔧 各章实验即模板。
