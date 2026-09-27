# 05 CouchDB（Relaxing on the Couch）——文档与复制

> 对应官方页实抓目录（✅）：Day1 CRUD, Fauxton, and cURL Redux｜Day2 Creating and Querying Views｜Day3 Advanced Views, Changes API, and Replicating Data｜Wrap-Up。
> CouchDB 本机**无安装**（⚠️ 不装不测）；HTTP/复制/视图重建的运行行为一律 ⚠️ 转述。🔧 类比用 SQLite 3.45.3 复现「map/reduce 视图=预计算物化表」的语义，**非 CouchDB 行为**。
> 谱系：同为文档 genre 的对照见 [04-MongoDB文档模型.md](04-MongoDB文档模型.md)；复制/最终一致原理见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。

## 5.0 CouchDB 的世界观：一切皆 HTTP + 最终一致

CouchDB = Apache 的**面向文档、以 REST/HTTP 为原生 API、内建双向复制**的数据库。它把 Web 的无状态、缓存、离线优先思想搬进数据库：数据是 JSON 文档，查询是 **MapReduce 视图**，同步是**复制 + 冲突版本（rev）**。与 Mongo「中心化的强一致倾向」相对，CouchDB 天生为**分布式、离线、多主写入**设计。

## 5.1 Day 1：CRUD、Fauxton 与 cURL

- **文档即 JSON**：每文档带 `_id`（可自选）与 `_rev`（每次写递增的版本戳，乐观并发核心）。
- **CRUD over HTTP**：`POST/GET/PUT/DELETE /db/{id}`；**更新必须带当前 `_rev`**，冲突则 `409`——写模型天然是「读-改-写 + 版本」。
- **Fauxton**：官方 Web UI（书时代替换了旧 Futon）用于建库/看文档/编辑视图。
- **cURL Redux**：Day1 大量用 `curl` 直接打 REST，凸显「CouchDB = HTTP 应用」。
- ⚠️ 转述：Day1 用 HTTP/`curl` 跑通建库、插入、按 `_id` 取、带 `_rev` 更新。

## 5.2 Day 2：创建与查询视图（Views）

- **设计文档（design document，`_design/…`）**：存放视图定义（JS 函数）。
- **map 函数**：对每个文档 `emit(key, value)`；**reduce 函数**：按键归并（`_sum/_count/_stats` 内置或自定义）。
- **视图即物化索引**：查询 `GET /db/_design/x/_view/y` 命中**惰性构建、可持久化**的结果；不查则不更新——把 OLAP 成本摊到读时。
- **`include_docs`、`descending`、`range(startkey/endkey)`**：视图的切片与联查。

> 🔧 **类比组：map/reduce 视图 = 预计算物化表（非 CouchDB，SQLite 3.45.3）**
> CouchDB 的「视图把聚合结果存下来、读时近乎 O(1)」可用 SQLite 手工模拟——它**没有物化视图，所以你得自己把 GROUP BY 结果写进一张表**（这恰好演示了视图要「预计算并持久化」的本质）：
> ```sql
> CREATE TABLE v(author TEXT PRIMARY KEY, posts INT, total INT);
> INSERT INTO v SELECT author, COUNT(*), SUM(views) FROM posts GROUP BY author;  -- 这是 reduce
> SELECT total FROM v WHERE author='amy';                                        -- 读视图
> ```
> 真实输出：视图 `[('amy',3,17), ('bob',2,6), ('cid',1,1)]`，按 `_id=amy` 读 `total=17`、耗时 **0.00001s**（✅）。要点：`GROUP BY author`≈map+reduce 的聚合，`SELECT … WHERE author=…`≈按 key 打视图；与 [../数据库系统概念6/11-索引与散列.md](../数据库系统概念6/11-索引与散列.md) 的「物化视图/聚簇」概念同源。声明：SQLite ≠ CouchDB，无 JS map/reduce、无 B-tree 视图文件，仅类比「预计算换读时」语义。

## 5.3 Day 3：高级视图、Changes API 与复制

- **高级视图**：多 `reduce`/`rereduce`、`_list`/`_show` 函数（把视图渲染成任意响应）、筛选器（filter）。
- **Changes API（`_changes`）**：**追加式变更日志**，客户端带 `last_seq` 增量拉取——离线同步与事件驱动的底座（与 Kafka/DDIA 的「变更数据捕获」同一思想）。
- **复制（Replication）**：`_replicator` 把本地库与远端库**双向同步**，用 `_rev` 树检测冲突；**多主 + 最终一致**是 CouchDB 招牌。
- **冲突处理**：复制产生的冲突文档标 `_conflicts`，由应用自选胜出 `_rev`——「冲突交给业务」哲学。
- ⚠️ 转述：Day3 是本册最有「分布式味道」的一章，但 Changes/replication 的真实行为不可本机测。

## 5.4 Wrap-Up：CouchDB 适合什么、不适合什么

- **适合**：离线优先/移动端（PouchDB 客户端对拷）、多站点写入、以文档为单位、能接受最终一致、要把「同步」当一等公民的应用。
- **不适合**：需强一致读、复杂即时 ad-hoc 查询（视图预计算有延迟）、高频小聚合。
- ⚠️ 转述：作者把 Couch 与 Mongo 并列文档 genre 的用意，正是展示**同模型下两种一致性/复制哲学**的分野。

## 5.5 本册内互链

- 文档模型强索引/聚合对照 → [04-MongoDB文档模型.md](04-MongoDB文档模型.md)。
- 复制/最终一致/CAP 收尾 → [09-收尾选型与CAP.md](09-收尾选型与CAP.md)。

## 5.6 常见坑与设计要点（⚠️ 转述，CouchDB 通识）

- **视图是「陈旧快照」**：`reduce` 结果惰性更新，刚写入立即查视图可能读到旧值——要「新鲜」需 `stale=false` 等待重建，牺牲延迟。
- **`_rev` 冲突不是 bug 是特性**：多主写入必产生分叉版本，应用要有「选胜 + 合并」策略，不能假装冲突不存在。
- **JS map/reduce 有硬约束**：`emit` 的值要可 JSON 序列化、`reduce` 必须确定性且可 `rereduce`（分区重算）——不像 SQL 聚合那样随便写。
- **无 ad-hoc 查询**：CouchDB 不提供 Mongo 式丰富选择器，「没建视图的查询」要么建视图要么 `all_docs` 全扫——比 Mongo 更「视图中心」。
- **复制带宽**：双向复制传的是文档+rev 树，网络成本随库大小走；过滤复制（filter/selector）用来减负。

## 5.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 给「博客」设计 `_design/by_author` 视图（`emit(author, 1)` + `_sum`），体会 map/reduce 两段。
2. 用本机 🔧（SQLite 手建物化表）复现「视图=预计算」，再讨论「为什么不每次现算」。
3. **跨库题**：本地 PouchDB 与远端 CouchDB 双向复制，模拟离线写→上线冲突→手动选 `_rev`（概念题，运行不可本机测）。
4. 思辨题：CouchDB 的最终一致 + 视图陈旧，与 DynamoDB 的最终一致读（[07](07-DynamoDB托管NoSQL.md)）在「读旧」上体验是否同源？

## 5.8 CouchDB HTTP/视图小抄（⚠️ 书体例反推 + ✅ 官方常识）

| 目的 | CouchDB 写法（HTTP） | Mongo 对照（[04](04-MongoDB文档模型.md)） |
| --- | --- | --- |
| 建库 | `PUT /db` | `use db` |
| 写文档 | `PUT /db/id {_rev,…}` | `updateOne` |
| 读文档 | `GET /db/id` | `findOne` |
| 建视图 | `PUT /db/_design/x {views…}` | `createIndex` + 聚合 |
| 查视图 | `GET /db/_design/x/_view/y?key=…` | `aggregate([{$group…}])` |
| 变更流 | `GET /db/_changes?since=seq` | Change Streams |
| 复制 | `POST /_replicator {source,target}` | （无内建双向） |

> 记忆钩子：CouchDB = 「**文档 + HTTP + 视图 + 复制**」四件套；它的每一项都在为「离线 / 多站点 / 端同步」服务，这也是它与 Mongo（更中心化、更丰富查询）分野的根（见 [04](04-MongoDB文档模型.md)）。

## 5.9 CouchDB 复制拓扑与一致性（⚠️ 转述，Couch 通识）

CouchDB 的复制不是「主从备份」，而是**任意拓扑的对等同步**：
- **单向 / 双向 / 过滤复制**：`_replicator` 文档声明 source↔target，可带 filter/selector 只同步子集（移动端只拿自己的数据）。
- **rev 树（revision tree）**：每次写生成新 `_rev` 挂在父版本下，形成分叉树；复制比对两库的树，**分叉即冲突**，胜出叶由应用选。
- **持续复制（continuous）** vs 一次性：`_changes` 轮询 / longpoll 让两端近乎实时收敛——但收敛是「最终」，不是「即时」。
- **CRDT 式思想的前身**：把冲突显式暴露、交给业务合并，与 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) 里「无冲突复制数据类型」的论述同源；Couch 用 rev 树 + 应用合并，比 CRDT 更「手动」。

> 这条复制线是 CouchDB 相对 MongoDB（[04](04-MongoDB文档模型.md)）最独特的资产，也是本册在文档 genre 里放两个库的全部理由——**同模型，两种对「分布式写」的回答**：Mongo 用副本集多数派近中心化，Couch 用多主最终一致。

## 5.10 何时选 Couch 而非 Mongo（本册双文档库的对立答案）

| 诉求 | 选 CouchDB | 选 MongoDB（[04](04-MongoDB文档模型.md)） |
| --- | --- | --- |
| 离线/端同步 | ✅ 复制+PouchDB 是立身之本 | ✖ 需另配同步层 |
| 复杂即时 ad-hoc 查询 | ✖ 视图预计算、不擅即席 | ✅ 丰富选择器+索引 |
| 强一致读 | ✖ 默认最终一致 | ✅ 多数派写/读 |
| 多站点写合并 | ✅ rev 树显式暴露冲突 | △ 事务能避但不能多主随意写 |

> 一句话：**CouchDB 把「同步」做进数据库内核，MongoDB 把「查询」做进数据库内核**。同是文档 genre，一个为「断网也能改、上线再合」而生，一个为「随时复杂查、近实时一致」而生——这正是本书为什么要用两章讲文档模型。

## 核心概念速览（中英对照）

- **REST/HTTP 原生** — CouchDB 把数据库操作映射到 HTTP 动词。
- **文档 `_id`/`_rev`** — 标识与版本戳，乐观并发的载体。
- **rev 树** — revision tree：分叉版本集合，冲突检测的载体。
- **设计文档** — design document：`_design/x` 存视图/列函数。
- **map / reduce** — 视图两函数：按键发射、按键归并。
- **视图（物化）** — view：惰性构建、持久化的聚合索引。
- **`_changes`** — 追加式变更日志，增量同步底座。
- **复制（replication）** — 多主双向同步，用 `_rev` 树比对。
- **冲突（`_conflicts`）** — 复制冲突文档，胜出 `_rev` 交应用选。
- **最终一致** — eventual consistency：Couch 的一致性默认姿态。
- **乐观并发** — optimistic concurrency：无 `_rev` 则拒写。
- **Fauxton** — 官方 Web 管理界面（替代旧 Futon）。

## 最新演进与工业实践

- **版本（⚠️ 转述 + ✅ 仓库现状）**：CouchDB 从书基线 1.x/2.x 进入 **3.x**——主打**单节点可扩到多节点、性能与 F1 查询优化器改进**。GitHub 仓库 https://github.com/apache/couchdb ✅ 实测 200；官网 https://couchdb.apache.org/ ✅ 200。
- **多节点成熟化**：早期「集群弱」的批评在 2.x/3.x 用分片数据库（sharded databases）+ 分区间复制部分回应；但相对 Mongo/PG 的中心化生态，Couch 仍偏「离线优先 / 端同步」 niche。
- **PouchDB 端侧**：浏览器/移动端的 PouchDB 与 CouchDB 双向复制，构成「本地库 + 云同步」应用栈，是 2018→2026 最稳的工程落地点 ⚠️。
- **思想外溢**：CouchDB 的 `_changes`（追加日志 + `last_seq`）几乎就是 CDC/事件溯源的早期范式，正规论述见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。
- **取证口径**：目录 ✅ 官方页实抓；复制/changes/视图重建运行细节 ⚠️ 转述（本机无 CouchDB）；🔧 视图物化类比 = SQLite 3.45.3 一手数字且非 CouchDB 行为。
