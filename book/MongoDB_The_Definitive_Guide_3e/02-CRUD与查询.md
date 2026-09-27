# 02 CRUD 与查询（原书第 3–4 章）

> 书目：《MongoDB: The Definitive Guide, 3rd Edition》（Kristina Chodorow, O'Reilly, 2013）。精读重构笔记，非原书文本；取证见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 实测环境：pymongo 4.18.2 import 级验证 🔧；无 mongod ⇒ 行为类结论 ⚠️ 未实测。

## 章骨架（中文小节 ✅ 实抓自人邮第 2 版目录）

- 第 3 章 创建、更新和删除文档：3.1 插入（批量插入、插入校验）/ 3.2 删除 / 3.3 更新（文档替换、修改器、upsert、更新多文档、返回被更新文档）/ 3.4 写入安全机制
- 第 4 章 查询：4.1 find（返回字段、limit）/ 4.2 查询条件（比较、OR、`$not`、条件语义）/ 4.3 特定类型查询（null、正则、数组、内嵌文档）/ 4.4 `$where` / 4.5 游标（limit/skip/sort、避免大 skip、查询选项、一致结果、游标生命周期）/ 4.6 数据库命令

## 精读笔记

### 1. 写路径（Chapter 3）

- `insert` 默认不校验（快），**批量插入**靠写多读少的吞吐；`update` 两形态：整文档替换 vs 修改器（`$set/$inc/$push/$pull/$rename/...`）；`upsert`；默认 `update` 只改一条，多改要 `multi:true`（后 API 改为 `updateMany`）。
- **写入安全机制（write concern）是本章灵魂**：2013 书用 `getLastError`/`safe`/`fsync`/`w` 讲"确认层级"；`_id` 冲突、非法 BSON 都靠它捕获。作者反复警告：默认写是"fire-and-forget"。
- 删除：`remove`（后拆 `deleteOne/deleteMany`）；批量清集合用 `drop` 而非逐条删（空间不回收的坑在 18 章回收）。

### 2. 读路径（Chapter 4）

- 查询选择器 = 文档模式匹配：`{field: {$gt: 3, $lt: 9}}`；`$in/$nin/$all/$size/$elemMatch`；逻辑 OR 用 `$or` 或数组值。
- 正则、null（"缺失字段也匹配 null"这一反直觉语义专门成节）、数组按元素匹配、内嵌文档匹配"字段对可乱序"语义。
- `$where` 能跑任意 JS——本书已示警（无法用索引、注入面），2026 实践中几乎判死刑。
- 游标：`find` 返回游标，批取默认约 20 批/16MB 封顶；`limit/skip/sort`；**大 skip 是性能炸弹**（仍要扫过并丢弃）；`snapshot`/`slaveOk` 等高级选项讲"一致结果"——这些命令级旋钮后来大多被**会话/因果一致性 API** 替代。
- 4.6 数据库命令：`runCommand`、`dbStats/collStats/count`、`explain`（7/5 章的优化入口）。

## 2013 基线 → 2026 现状对位勘误

| 本书说法（2013） | 2026 现状 | 依据 |
|---|---|---|
| write concern 经 `getLastError`/`safe` 表达 | 现代 **WriteConcern 对象 + acknowledged/majority**；`getLastError` 命令早已移除；驱动默认 `retryWrites=true`（PyMongo 3.9+/新驱动世代） | ✅ https://www.mongodb.com/docs/manual/core/read-write-concern/ ⚠️（该页未逐一核验，机制为官方文档长期事实） |
| 单文档写入原子；多文档需应用自控（journaling 章强调"MongoDB 不提供跨文档事务"） | **4.0 副本集多文档 ACID 事务、4.2 扩展到分片集群**（session + txnNumber + readConcern majority 前提）；"事务是例外而非常态"的设计哲学保留 | ✅ https://www.mongodb.com/docs/manual/core/transactions/（页面实抓） |
| 读取一致性靠 `slaveOk`/`snapshot`/主从延迟手工管理 | **Read Concern 层级**（local/available/majority/linearizable/snapshot）+ **因果一致性会话**；`$readSource` 类需求被 read preference + tags 规范化 | ⚠️ 层级清单为官方长期文档事实 |
| 游标超时/生命周期需小心（空闲 10 分钟被杀） | `noCursorTimeout` 语义仍在，但驱动普遍默认 **non-timeout + `killCursors`**；新增 **awaitData/tailable 游标** 配合 change streams 消费 | ⚠️ |
| 大 skip 低效 | 结论不变；官方新增 **`let`/索引提示与 search after 式分页（`$search`/Atlas pagination）** 作为替代叙事 | ⚠️ |
| 无部分匹配之外的高级谓词 | 新增 `$expr`（聚合表达式进查询）、`$jsonSchema` 查询辅助、`$regex` 仍非首选（Atlas Search 接管文本） | ⚠️ |

## 概念到系列的锚点

- 一致性语义术语（单调读/读己之写/因果）在 [../设计数据密集型应用.md](../设计数据密集型应用.md) 第 9 章讲得最干净，建议对照 11 章文件（本书复制应用接口）。
- "默认弱一致、按需增强"同样是 [../Redis设计与实现.md](../Redis设计与实现.md) 里持久化/复制讨论的底色。

## 核心概念速览（中英对照）

- **修改器** — Update Operators（`$set/$inc/$push`）：就地部分更新，避免整文档替换。
- **upsert** — Update or Insert：无匹配则插入。
- **写入安全机制** — Write Concern（旧称 safe/getLastError）：写操作确认强度（副本数/journal）。
- **选择器** — Query Selector / Filter：BSON 模式匹配查询条件。
- **`$elemMatch`** — 数组元素复合条件匹配。
- **`$where`** — JS 谓词，索引失效 + 注入面，2026 视为遗留。
- **游标** — Cursor：服务端查询句柄，批取（getMore）；大 `skip` 仍全扫。
- **tailable 游标** — 尾随游标：持续读 capped 集合/oplog，change streams 的思想前身。
- **explain** — 计划解释器：`indexOnly/cursor/nscanned`（5 章）。
- **retryable writes** — 可重试写（3.6+，现代驱动默认）：网络抖动幂等重发。⚠️ 未实测
- **事务** — Multi-document ACID Transactions（4.0+/4.2 分片）：书基线之后的最大能力增量。✅ 官方页实抓
- **因果一致性** — Causal Consistency（会话级"读己之写"）：替代书中 `slaveOk` 手工戏法。

## 最新演进与工业实践

- **API 形状对照（🔧 import 级，pymongo 4.18.2）**：`Collection.bulk_write`、`InsertOne/UpdateOne/DeleteMany`、`write_concern` 模块均可导入——即本书 3.1.1"批量插入"的现代化身 `bulk_write`（ordered/ordered=False + bypassDocumentValidation）。行为性能需服务端 ⇒ ⚠️ 未实测。
- **`update(remove=False)` → `update_one/update_many/replace_one`**：PyMongo 4.x 已移除旧 `update()`/`insert()`/`remove()` 顶层别名（改 `insert_one/insert_many/delete_one/delete_many`）——搬 2013 代码上 4.x 驱动必改。⚠️ 迁移清单以官方 Upgrade Guide 为准（https://pymongo.readthedocs.io ⚠️ 本环境未验证可达）
- **skip 分页 → 键集分页（keyset/seek）**：社区长期共识（`{_id: {$gt: last}}`），书 4.5.2 的告诫在 2026 仍是面试/规范高频题；Atlas 文本/向量搜索另提供专用分页参数。
- **写确认默认值变迁**：新驱动默认 `w:1 + retryWrites=true`，"majority 是否默认"是跨版本大坑（4.0+ 集群默认 majority readConcern 的前提），生产必须显式声明——与本书"默认不安全"的精神一致且更工程化。
- **事务的现代用法**：官方建议"设计仍按无事务，事务用于少数多文档一致性场景"；性能开销与 oplog 膨胀约束使"第 8 章反范式优先"仍是主线（见 05 文件）。
