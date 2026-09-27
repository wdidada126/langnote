# 04 · 建模演进：重构、索引与 Genre（Ch.4，章题为 ⚠️ 逆推重构）

> 取证锚点（✅ 实抓配套仓库 chapter04/cypher，13 个脚本）：`001-rel-type-refactor-1`、`002-recommendation-1`、`003-rel-type-refactor-2`、`004-artistNameIndex`、`005-loadGenres`、`006-genreConstraint`、`007-refactor-genre`、`008..010/013-refactor-playlist-linked-1..5`、`012-recommendation-2`。叙事线：**边类型改名手术 → 艺人索引 → Genre 炸开成节点 → playlist-linked 大重构 → 推荐查询换代**。这是全书“模式演进”主题最集中的一章。

## 4.1 关系类型不可变？改给你看

Cypher 没有 `ALTER RELATIONSHIP TYPE`。`rel-type-refactor-1/2` 演示标准的“造新删旧”四步手术（⚠️ 语法按通行做法重构）：

1. 匹配旧边，聚合出端点与属性；
2. `CREATE`（或 MERGE）新类型边并复制属性；
3. `DELETE` 旧边；
4. 分批跑（`CALL {} IN TRANSACTIONS`），避免手术本身撑爆事务日志。

工程含义：类型名是 schema 决策，但**改错不是死刑**——本书故意在第 3 章留一个“不理想命名”到第 4 章动刀，教学用心明显。

## 4.2 artistNameIndex：先为查询形状建索引

`004-artistNameIndex` 在名字属性（非键）上建索引。区别于 Ch.2 的唯一约束（键），这里索引服务的是**查找入口形状**：“用户输入艺人名字搜歌单”。

索引三梯度（本章归纳 ⚠️）：

- 唯一约束：实体键，MERGE 前提（Ch.2）；
- 范围索引（RANGE INDEX）：`=`、`<`、`>`、字符串前缀；
- 全文/文本索引：`CONTAINS`/模糊——本章只开个头，Ch.7 全章展开。

`003` 重构脚本里按名字找艺人再连边，若没有此索引就是全扫——**重构成本与索引presence 在同一章出现不是巧合**。

## 4.3 Genre：属性提升为节点的完整流程

三连 `loadGenres → genreConstraint → refactor-genre` 是教科书式的“属性节点化”：

- 把 `"[hard rock, heavy metal]"` 字符串炸成 `(:Genre {name})` 节点 + `(:Track)-[:HAS_GENRE]->(:Genre)`；
- 先 `Genre` 唯一约束再 MERGE——顺序与 Ch.2 纪律一致；
- 炸开收益：流派成为遍历枢纽（同流派艺人互达）、聚合主键、可挂描述属性；
- 炸开代价：边数放大（曲目×流派），god node 风险——“popular”这类流派度数爆炸，Ch.5 的 `degrees-*` 脚本处理的就是这类节点 ⚠️（衔接推定）。

🔧 概念注记（DuckDB，非 Neo4j）：同一个炸开动作在关系侧是 `unnest(str_split(...))`，02 章实测记录显示炸开前 `[synthwave]` 因括号残裂成两个值——**节点化会放大脏数据**，清洗要前置于炸开。

## 4.4 playlist-linked 重构：五步大手术

`refactor-playlist-linked-1..5` 加中间一个 recommendation-2，是全仓库步数最多的重构序列（✅ 文件名）。重构推测其形 ⚠️：把“歌单直接连艺人”（`LISTENS_TO` 快捷边）改回经由曲目的规范形态，或相反——把派生的高频模式提升为快捷边。五步分解的共性动作：

1. 盘点旧模式基数（count）；
2. 小样本试手术（LIMIT）；
3. 全量分批（IN TRANSACTIONS）；
4. 新旧并存期双查对照；
5. 删旧 + 重建受影响索引。

“新旧并存 + 双读对照”正是微服务 schema 迁移在图库的翻版，对照 [../设计数据密集型应用.md](../设计数据密集型应用.md) 的扩展-回填-收缩（expand/contract）模式。

## 4.5 recommendation-1 → recommendation-2：模型变了，查询也要换代

`002` 与 `012` 同名不同实现：Genre 节点化之后，相似/推荐可走 `(p)-[:HAS_TRACK]->(t)-[:HAS_GENRE]->(g)<-[:HAS_GENRE]-(t2)<-[:HAS_TRACK]-(p2)` 之类语义更宽的路径。本章论点（⚠️ 重构）：

- 推荐质量对模型形状敏感——同一业务意图有多个模式化表达；
- 每跳都是成本：路径加长必须重新 PROFILE（交给 Ch.5）；
- 模型演进的验收 = 旧查询仍绿 + 新查询更快/更准。

## 4.6 本章的模式管理纪律（重构者总结）

- 重构永远配“回滚脚本意识”：造新删旧序列里，删是最后一步；
- 索引随模型迁移：Genre 节点化后，旧 Track.genre 上的索引/约束要么跟进要么显式作废；
- 一次只动一个变量：类型改名手术与 Genre 炸开之间插了独立提交点（脚本序 ✅ 佐证）；
- 数据说话：重构前后各跑一次验收查询集（承 03 章）。

## 4.7 与 GD2e 建模章的正误差

[../Graph_Databases_2e/03-使用图进行数据建模.md](../Graph_Databases_2e/03-使用图进行数据建模.md) 强调“节点 vs 关系的辨别”“避免把节点当属性包”；本章的 Genre 手术是其逆问题——**把属性包升格为节点**的时机与工程。两书合读才是完整的“粒度升降级”课。

## 4.8 索引生命周期操作卡（5.x 语义 ⚠️ 转述，命令以手册为准）

| 动作 | 语句形态（示意） | 在线能力 | 备注 |
|---|---|---|---|
| 建 | `CREATE INDEX name IF NOT EXISTS FOR (n:L) ON (n.p)` | 在线，后台回填 | `IF NOT EXISTS` 惯例 ✅（Ch.2 同款） |
| 看 | `SHOW INDEXES YIELD name, state, populationProgress` | — | 只有 ONLINE 才可服务查询 |
| 等 | `CALL db.awaitIndexes(timeout)` | — | 导入/重构后的标准收尾 ⚠️ |
| 删 | `DROP INDEX name`（先 WAIT 语义可选） | 在线 | 删除窗口内查询静默退化回扫描 |
| 重建 | 5.x 无原地 REBUILD：drop+create | — | 重构期双索引并存是常态 ⚠️ |

`004-artistNameIndex` → `006-genreConstraint` 正是这张卡的两行实操：range 索引服务**查找形状**，约束服务**实体身份**——生命周期相同、语义职责不同，验收查询要分开写。

## 4.9 “改类型名”在跨存储谱系里的位置（对照注记）

本章四步手术（4.1）如果放到其他存储看，会发现它是**普遍规律的图库实例**：

- 关系库改列名：`ALTER ... RENAME` 只动 catalog，数据不搬——因为列名不进元组编码；
- ES 改字段类型：mapping 不可变，只能 reindex + 别名切换——因为分词结果已进倒排文件；
- Neo4j 改关系类型：类型写死在关系记录头部（记录存储视角见 [../Graph_Databases_2e/06-图数据库的内部结构.md](../Graph_Databases_2e/06-图数据库的内部结构.md)，5.x 落盘形态见本册 Ch.9）——**编码进物理布局的语义，改 = 重写数据**。

铁律：**凡进入存储编码的 schema 决策都是迁移工程，不是元数据操作**。凡只在指针层的才是改名。判断一个“小改动”贵不贵，先问它落在这条线的哪边。

## 4.10 Genre 炸开的容量预估练习（方法重构 ⚠️）

动手前填三个空（数字全部来自 Ch.2 体检清单，✅ 方法论）：

1. 平均曲目流派数 g、曲目总数 N → 新边 ≈ N×g、新节点 ≈ |unique genre|；
2. 最大流派度 D_max → 超过 10^5 直接预读 Ch.5 degrees 缓解清单；
3. 流派读写比 → 读多写少则炸开值；高频变动则保留字符串属性再议。

🔧 关系侧预演（DuckDB 1.5.5，非 Neo4j 行为）：demo2.py 在 gnr 6 行真数据上 `unnest(str_split(...))` 炸出 artist–genre 边表，行数放大约 1.8 倍（6 行原始 → 9 条边 ✅ 运行输出）——真实 Spotify 数据多流派尾更长，这个放大系数就是第 1 空的直观校准；同时炸开把 `[synthwave]` 括号残裂的脏值**一分为二地暴露**（02 章 2.6 注脚），验证“清洗前置于炸开”。

## 核心概念速览（中英对照）

- **类型重构** — Relationship Type Refactor：造新边、复制属性、删旧边的在线手术
- **属性节点化** — Promote Property to Node：把共享值（流派）提升为节点与关系
- **范围索引** — Range Index：服务等值/区间/前缀查询的二级入口
- **扩展-回填-收缩** — Expand/Contract/Backfill：新旧模式并存迁移三板斧
- **双读对照** — Dual-Read Validation：迁移期新旧路径结果比对的验证法
- **度数放大** — Degree Blow-up：炸开操作使边数成倍增长的容量后果
- **查找入口** — Lookup Entry：按名字/输入形状建的索引，非键索引的动机
- **分批手术** — Batched Refactor：重构写操作同样必须 IN TRANSACTIONS
- **模型敏感度** — Model Sensitivity：同查询在不同模型形状上的性能/质量方差
- **验收查询集** — Acceptance Query Suite：重构前后跑同一查询清单

## 最新演进与工业实践

- **2025.x 的 schema 通道**：`CREATE INDEX`（range/point/text/vector 家族）语法延续 5.x；本书使用的索引管理过程在 current 文档化（https://neo4j.com/docs/cypher-manual/current/indexes/ ，入口经 01 已证域可达 ✅，逐页未核 ⚠️）。
- **向量索引加入家族**：属性→节点的旧梯度外，2024 起索引清单多了语义向量索引（`CREATE VECTOR INDEX ... (dfw)`），Genre 之类文本可“节点化+向量化”并行存在——Ch.13 主题，见 https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ （200 ✅）。
- **工业实践口径**：schema 迁移的“新旧并存+回滚点”纪律与关系库 online DDL、MongoDB schema versioning 同族，对位阅读 [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)。
- **LDBC 与建模评测**：属性图基准（LDBC Benchmark 家族）把“模式形状→查询代价”变成可复现实验，是本章手工 PROFILE 论证的学界放大版 ⚠️（趋势转述）；论文追踪见 [../../db/db.md](../../db/db.md)。
