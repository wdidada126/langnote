# 02 CRUD 与查询（原书第 3–4 章）

> 书目：《MongoDB: The Definitive Guide, 3rd Edition》（Kristina Chodorow, O'Reilly, 2013）。精读重构笔记，非原书文本；取证见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 实测环境：pymongo 4.18.2 import 级验证 🔧；无 mongod ⇒ 行为类结论 ⚠️ 未实测。

## 阅读目标

- 掌握写路径（insert/update/remove + 修改器 + upsert）与"确认层级"（write concern 前身）的完整语义。
- 掌握读路径：选择器语法、特殊类型匹配、游标生命周期与 skip/sort 的性能语义。
- 识别本章 2026 年需要整体替换的概念：getLastError 方言、无事务假设、slaveOk 一致性戏法。

## 章骨架（中文小节 ✅ 实抓自人邮第 2 版目录）

- 第 3 章 创建、更新和删除文档：3.1 插入并保存文档（批量插入、插入校验）/ 3.2 删除文档 / 3.3 更新文档（文档替换、使用修改器、upsert、更新多个文档、返回被更新的文档）/ 3.4 写入安全机制
- 第 4 章 查询：4.1 find 简介（指定返回字段、限制）/ 4.2 查询条件（条件、OR、`$not`、条件语义）/ 4.3 特定类型的查询（null、正则、数组、内嵌文档）/ 4.4 `$where` / 4.5 游标（limit/skip/sort、避免大 skip、高级查询选项、获取一致结果、游标生命周期）/ 4.6 数据库命令

## 精读笔记

### 1. 写路径（第 3 章）

- `insert` 默认不校验（快）；`save` = 有 `_id` 则整替换；**批量插入**靠写多读少场景的吞吐红利。
- `update` 两形态：整文档替换 vs **修改器**（`$set/$unset/$inc/$push/$addToSet/$pop/$pull/$rename/$`位置符）——作者立场：修改器是文档库的"部分更新 SQL"，优先于取回-改-写回。
- `upsert`；默认 update 只改一条、多改要 `multi:true`（现代 API：`update_one/update_many/replace_one`）。
- `findAndModify`（现 `findOneAndUpdate` 前身）："返回被更新的文档"选项的原子读改写——书中把单文档原子性吹捧为唯一的并发原语，2026 年它仍然优雅且免事务。
- **写入安全机制是本章灵魂**：2013 用 `getLastError`/`safe`/`fsync/j`/`w=n` 讲"确认层级"；默认写是 fire-and-forget，作者反复示警。
- 删除：`remove`（后拆 `deleteOne/deleteMany`）；清集合用 `drop` 而非逐条删（但书中警告 drop 后空间归还的引擎差异——11 文件续谈）。

### 2. 读路径（第 4 章）

- 选择器 = 文档模式匹配：比较符 `$gt/$gte/$lt/$lte/$ne/$in/$nin`；`$all/$size/$elemMatch`；`$or` 与"值即数组"的隐式 OR。
- 类型专场：**null 同时匹配"字段缺失"**（反直觉，专节强调）；正则（前缀锚定才吃索引）；数组按元素匹配；内嵌文档点号路径匹配与"整文档匹配字段对不可乱序"规则。
- `$where`：任意 JS 谓词——书中已示警（不吃索引、注入面、慢），2026 实践中基本判死刑。
- 游标：`find` 返回服务端游标，批取（首批约 101 条、其后按 16MB 封顶；书世代默认值有差异，⚠️ 细节未核）；`limit/skip/sort`；**大 skip 是性能炸弹**（照样扫过再丢弃）。
- "获取一致结果"：`slaveOk` 关掉、`snapshot` 模式、或强制主读——都是无事务时代的手工一致性；游标生命周期（空闲超时、`killCursor`）单列成节。
- 4.6 数据库命令：`runCommand`、`dbStats/collStats/count`、`explain`（第 5/7 章优化的入口）。

### 3. 选择器速查（按书中 4.2–4.3 重组）

| 族 | 成员 | 一句话语义 | 索引友好度（书语境） |
|---|---|---|---|
| 比较 | `$gt/$gte/$lt/$lte/$eq/$ne/$in/$nin` | 区间与集合成员 | 区间/`$in` 可走；`$ne/$nin` 基本全扫 |
| 逻辑 | `$or/$and/$not/$nor` | 布尔组合（键名写 `$or` 会撞字段名——书中陷阱） | `$or` 需各支路都有索引才不崩 |
| 元素 | `$exists/$type` | 字段存在性/BSON 类型 | 弱；配 partial/sparse 索引是现代解法 ⚠️ |
| 数组 | `$all/$size/$elemMatch` | 全含/定长/元素级复合条件 | `$size` 不加速；`$elemMatch` 防跨元素误配 |
| 求值 | `$regex/$where/$expr` | 正则/JS 谓词/表达式 | 前缀锚定正则吃索引；`$where` 判死刑 |
| 地理 | `$near/$within`（6.4 预告） | 距离/包含 | 需地理索引（03 文件） |

### 4. 游标生命周期深潜（4.5 的机制内核）

- `find()` 只创建句柄；首次 `getNext` 才真正下发查询。批取协议：首批复约 101 条/上限 4MB⚠️（书世代数值），其后按 16MB 封顶——**"limit 小于首批阈值就只取一次批"** 这类冷知识当年是面试谈资，如今交给驱动池化。
- 服务端游标默认 10 分钟空闲回收：客户端忘关 = 泄漏（书中演示 `close()`；现代驱动 `killCursors` 自动回收）。
- **tailable 游标**：贴 capped 集合尾部持续轮询——空读也消耗往返；这是"尾随 oplog 做变更订阅"的全部家当，change streams（3.6+）出现后此类轮询代码整体报废（07 文件）。
- sort 的两种执行：有索引则顺树扫描；无索引则内存排序集（32MB 时代阈值⚠️），超限当年直接报错、后可落盘——`SORT_IN_MEMORY` 至今能在 explain 里认出这条路径。
- 游标与 `getMore` 的账：翻页成本 = 已扫文档数，这就是"大 skip 是炸弹"的物理原因；键集分页把成本恒定为 O(limit)。

### 5. 更新结果的"两个 n"：nMatched vs nModified（写路径最隐蔽的语义缝）

- 书时代 `update` 的回执是 `getLastError` 里的 `n`（匹配数）；现代 CRUD 结果对象拆成三个数：`matchedCount / modifiedCount / upsertedCount`（PyMongo API 形状 🔧 可导入验证，行为 ⚠️ 未实测）。
- 分家的原因正是修改器语义：`$set {a:1}` 打到 `a` 已是 1 的文档——**匹配成功但零改动**，matched=1、modified=0；"更新没生效"的排查若只看 matched 会完全跑偏（书中"multi 忘开"是另一种表现，同一族）。
- 推论到工程纪律：关键写路径要**断言 modifiedCount**（或先 findAndModify 拿返回文档验证），而不是"没抛异常就算成功"；这与 3.4"写没报错≠写成功"的确认层级教义一脉相承——一个防传输层丢，一个防语义层空转。
- upsert 的第三计数：`upsertedCount=1` 时新文档 `_id` 由服务端生成，客户端拿不到就要二跳查询——现代驱动用 `returnDocument/returnNewDocument` 在 `findOneAndUpdate` 一次拿全，书里 `findAndModify` 的 `new:true` 选项即其前身。⚠️（文档转述）

## 常见误区（书中显式纠正的）

1. "更新没生效"——默认只更新第一条匹配；multi 忘了开。
2. "$set 数组下标"越界会产生空洞（null 填充）。
3. "sort 后 skip 翻页不怕慢"——两三千页后每跳都是全扫。
4. "null 查询 = 字段为 null"——还包含字段不存在。
5. "写没报错 = 写成功"——默认无确认，主崩溃即丢。
6. "`{$push: {a: [1,2]}}` 追加两个元素"——错，塞进一个嵌套数组；要 `$each`。数组修改器是当年事故率最高的一族。
7. "查询 `{a:1, b:2}` 会匹配 `{b:2, a:1, c:3}` 文档"——选择器按键值对匹配与顺序无关，但**内嵌文档整体匹配**却严格除序——两副面孔同章出现，书中专门对比。
8. "updatedExisting/n 一个数就够"——匹配≠修改：`$set` 同值空转时 matched=1/modified=0，断错数=错验收（精读第 5 节）。
9. "`$size` 能加速数组查询"——它不进索引，纯扫描判定；要加速得靠多键索引+`$elemMatch` 组合（03 文件）。

## 2013 基线 → 2026 现状对位勘误

| 本书说法（2013） | 2026 现状 | 依据 |
|---|---|---|
| 写确认经 `getLastError`/`safe` | 现代 **WriteConcern 对象（w/j/wtimeout）+ majority**；`getLastError` 命令已移除；驱动默认 `retryWrites=true` | ⚠️（官方读写关注文档通识） |
| 单文档写原子；多文档要应用自控 | **4.0 副本集 / 4.2 分片集群多文档 ACID 事务**；"事务是例外而非常态"哲学保留 | ✅ https://www.mongodb.com/docs/manual/core/transactions/ |
| 一致性读靠 `slaveOk/snapshot` 戏法 | **Read Concern（local/majority/linearizable/snapshot）+ 因果一致性会话**；read preference 规范化 | ⚠️ |
| 游标空闲 10 分钟被杀要严防 | 现代驱动默认非超时游标 + 自动 `killCursors`；tailable 游标与 change streams 分工 | ⚠️ |
| 大 skip 告诫 | 结论原样有效；键集分页（`{_id: {$gt: last}}`）为社区标准解，Atlas 搜索另有专用分页参数 | ⚠️ |
| 查询语言止于选择器 | 新增 `$expr`（聚合表达式进查询）、`$jsonSchema` 校验、文本/向量检索外移到 Atlas Search 家族 | ⚠️ |
| `findAndModify` 拼写 | 服务端命令 `findAndModify` 仍在；驱动 API 更名 `findOneAndUpdate/Replace/Delete`（CRUD 规范） | ✅ 驱动文档实抓（PyMongo 站） |
| 示例全部 mongo shell 语法 | 生产脚本迁 mongosh + 语言驱动；shell 助手函数大量沿用同名 | ✅ mongosh 页 |

## 交叉连接

- 一致性语义术语学（单调读/读己之写/因果/快照）：[../设计数据密集型应用.md](../设计数据密集型应用.md) 第 9 章——配 07 文件读收益最大。
- 游批/getMore 协议与 capped 集合上的 tailable 游标实验：[03-索引与特殊集合.md](03-索引与特殊集合.md)（4.5 末小节与 6.3 专节的互文）。
- "默认弱确认、按需增强"的 KV 对照（Redis 写丢失权衡）：[../Redis设计与实现.md](../Redis设计与实现.md)。
- 与 SQL DML 的语法/心理对照：[../高性能mysql.md](../高性能mysql.md)。

## 核心概念速览（中英对照）

- **修改器** — Update Operators（`$set/$inc/$push`）：就地部分更新，免整文档替换。
- **upsert** — Update or Insert：无匹配则插入。
- **写入安全机制** — Write Concern（旧 safe/getLastError）：写确认的副本/持久化层级。
- **选择器** — Query Selector / Filter：BSON 模式匹配。
- **`$elemMatch`** — 数组元素复合条件匹配（防跨元素误配）。
- **`$where`** — JS 谓词：索引失效 + 注入面，2026 遗留物。
- **游标** — Cursor：服务端查询句柄，getMore 批取；大 skip 仍全扫。
- **tailable 游标** — 尾随游标：持续读 capped 集合/oplog，change streams 思想前身。
- **findAndModify** — 原子读改写：无事务时代的并发原语（今 findOneAndUpdate）。
- **explain** — 计划输出：书世代 `indexOnly/nscanned`，现代 `winningPlan/executionStats`。
- **retryable writes** — 可重试写（3.6+ 现代驱动默认）：网络抖动幂等重发。⚠️
- **事务** — Multi-document ACID（4.0/4.2）：书基线后最大能力增量。✅
- **因果一致性** — Causal Consistency：会话级"读己之写"，替代 slaveOk 手工活。
- **matchedCount/modifiedCount** — 更新回执双计数：匹配与真改分离（现代 CRUD 规范结果对象）。
- **点路径（dot notation）** — `"a.b.0"` 式字段寻址：内嵌/数组局部更新的语法地基。

## 最新演进与工业实践

- **API 形状对照（🔧 import 级）**：pymongo 4.18.2 中 `bulk_write` 与 `InsertOne/UpdateOne/DeleteMany`、`write_concern` 模块可导入——即书 3.1.1 批量插入的现代化身（ordered/bypassDocumentValidation 选项）；性能断言 ⚠️ 未实测。
- **驱动迁移断代**：PyMongo 4.x 移除顶层 `update()/insert()/remove()` 别名（改 `update_many/insert_many/delete_many`）——搬 2013 代码上 4.x 必撞墙；官方 Upgrade Guide 为准 ⚠️（pymongo.readthedocs.io 本环境未核验）。
- **写确认默认值变迁**：现代默认 `w:1 + retryWrites=true`；"majority 是否默认"是跨版本大坑（4.0+ 多数派读关注的前提链条），生产显式声明——与本书"默认不安全"精神一致但更工程化。
- **键集分页共识**：书 4.5.2 的告诫在 2026 是面试/规范高频题：`limit/skip` 深翻页一律改 seek-method（`_id` 或排序键续标），聚合侧 `$sort+$skip+$limit` 同理。
- **事务的现代用法**：官方口径"设计仍按无事务，事务兜底少数多文档场景"；开销（事务协调/oplog 膨胀）使第 8 章反范式优先仍是主线（05 文件）。✅ 事务页实抓
- **读侧新大陆**：`$vectorSearch`/`$search` 不属于本章 CRUD，但消费同一集合体系——入门书语境的"查询"在 2026 已三分天下（选择器/聚合/搜索）。✅ stage 页实抓
- **write concern 谱系一句话**：`{safe:true}` → `getLastError{w:...}` → OP_MSG 时代 WriteConcern 对象内嵌进每次写 → `w:majority + j:true` 成为"重要数据"默认话术；确认从"独立命令"进化为"写的一部分"，书中 3.4 的担忧以工程化方式兑现。⚠️（协议细节为通识）
- **批量写的现代形态**：`insert_many(ordered=False)`、`bulk_write` 混合 InsertOne/UpdateOne/DeleteMany——书中"批量插入"的性能红利叙事不变，API 从"往连接上连发"变为受控批处理原语（🔧 import 级可验，收益 ⚠️ 未实测）。
- **count 的下落**：书中 4.6 的 `count` 命令在新驱动被 `count_documents`（精确，走聚合 `$match+$group`）与 `estimated_document_count`（元数据估算）二分取代——"计数也要问精度"是本章教义的延续。⚠️（驱动 API 名称以官方文档为准）
- **官方读写关注文档可直查**（2026-09 curl 200）：写确认 https://www.mongodb.com/docs/manual/core/write-concern/ 、读路由 https://www.mongodb.com/docs/manual/core/read-preference/ ——3.4 与 4.5 两节的现代方言以此二页为准。
- **delete 一族的家谱**：`remove({})` → `deleteMany({})`，但清库正道仍是 `drop`（日志学上 drop 是一条 oplog 记录、deleteMany 是一亿条——06 文件 oplog 解剖的推论；复制滞后与 oplog 窗口都被它吃掉，07 文件公式）。⚠️
