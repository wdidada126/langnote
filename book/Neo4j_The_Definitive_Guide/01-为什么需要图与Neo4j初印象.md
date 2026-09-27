# 01 · 为什么需要图与 Neo4j 初印象（Ch.1，章题为 ⚠️ 逆推重构）

> 取证锚点（✅ 实抓官方配套仓库 `neo4j-the-definitive-guide/book` chapter01 目录）：figures 含 `figure-1-1-graph-whiteboard`（白板上的图）、`figure-1-2-company-relational-model`（公司数据的关系模型）、`figure-1-3-graph-model`、`figure-1-4-property-graph-model`、`figure-1-5-block-storage`（块存储）、`figure-1-7-cypher-ascii-art`；cypher 脚本 17 个，从 `000-create-database` 到 `016-shortest-2`，中间是 preview-data、one-track/one-playlist、merge-all-sample-*、index/constraint-creation、find-similar-playlists、merge-similarities、recommendation、shortest-1/2；另含 `relational-schema/schema.md`。本章重构 = 这组工件讲了一件什么事。

## 1.1 本章在全书的站位：一张白板图开始的论证

第 1 章用**同一个贯穿全书的业务域（Spotify 歌单/艺人/曲目）**走完“关系模型 → 属性图模型 → 第一条 Cypher → 第一个推荐查询 → 第一条最短路径”的全链路。这不是装饰性导论：配套仓库把 `relational-schema/schema.md` 与图模型脚本并排放，说明作者的讲法是**“先把你脑子里的表画出来，再当场推翻它”**。

与 [../Graph_Databases_2e/02-关联数据的存储选择.md](../Graph_Databases_2e/02-关联数据的存储选择.md) 的差异：GD2e 从“JOIN 重建邻接的代价”做理论批判，本章从“建模一张图到跑通查询只要 17 个脚本”做上手论证——同一命题的两种体裁。

## 1.2 图、属性图与“联系是一等公民”

本章给出的属性图（property graph）要素（⚠️ 依据 figures 1-1/1-4 逆推）：

- **节点（Node）**带标签（`Playlist`、`Track`、`Artist`）与属性（名称、流媒体数）；
- **关系（Relationship）**有类型、方向、属性（`LISTENS_TO {count}`）；
- 标签/类型都是**索引入口**而非存储分界——同一节点可带多标签。

“块存储”图（figure 1-5）的功能是把**免索引邻接（index-free adjacency）**一次讲透：关系记录物理上指向节点记录，跳一跳是指针跟随而非索引查找。该图在 GD2e 02/06 章有同源论述（⚠️ 两书图号不同，概念同源）。

## 1.3 Cypher：ASCII 画出来的模式匹配

`figure-1-7-cypher-ascii-art` 对应本章的语法观：`(a)-[:REL*1..6]->(b)` 这种字符画就是查询本身。本章脚本序列暴露的教学顺序值得记录：

1. `000-create-database`：多数据库意识从第 1 章就有（5.x 语义，`CREATE DATABASE playlists`）；
2. `001-preview-data`：先 `LOAD CSV ... LIMIT` 看数据再建模（对应 figure `neo4j-load-csv-preview-tracks/playlists`）；
3. `002/003` 读一条 track/playlist → `004/005` MERGE 幂等写入 → `006-007` 批量 merge：读→写→幂等的三级台阶；
4. `008/009` 索引与约束创建**先于**数据增长发生（性能是设计期决策，不是事故后补救）；
5. `012-find-similar-playlists` → `013-merge-similarities`：相似性先算出来、再物化为 `SIMILAR` 边——**计算结果沉淀为图结构**是本书贯穿 Ch.3/Ch.12 的母题；
6. `014-recommendation`：一跳 `SIMILAR` + 过滤已听 = 推荐；
7. `015/016-shortest-*`：全书第一条最短路径查询出现在第 1 章而非算法章——作者把“图能回答的问题”当作卖点本身。

## 1.4 为什么是 Neo4j，而不是“图能力”泛指

官方简介（✅ 豆瓣实抓）说读者应能“判断 PoC 阶段的务实决策”。本章的决策框架（⚠️ 逆推）：数据里有**多跳联系 + 模式约束 + 遍历即查询**三特征才上图；只是“带外键的报表”就别上。对照 [../nosql精粹.md](../nosql精粹.md) 的聚合视角：图库买到的是“关系免 JOIN 成本”，付出的是聚合局部性丧失。

## 1.5 🔧 概念类比实测：模式匹配就是边表自连接（DuckDB，非 Neo4j 行为）

**声明：以下为 SQL 在关系引擎上复现图语义的教学类比，证明不了 Neo4j 的任何性能/行为。**

用本书 Ch.8 官方数据 `chapter08/gnr-genres.csv`（✅ tarball 实抓，6 行：5 个“Guns N' Roses”变体 + 1 个 Gunship，艺人行带 `"[hard rock, heavy metal]"` 字符串列表列），DuckDB 1.5.5（Python 包）解析为 `edges(aid, genre)` 9 行后，把 Cypher 模式 `(a)-[:HAS_GENRE]->(g)<-[:HAS_GENRE]-(b)` 翻译为一次自连接：

```sql
SELECT a.artist, b.artist, count(*) AS shared
FROM edges a JOIN edges b ON a.genre=b.genre AND a.aid<b.aid
GROUP BY 1,2;
```

实测输出（🔧 demo3.py 运行记录）：`Guns N' Roses↔Guns N' Roses(fused) 共享2个流派（hard rock, heavy metal）`、`Guns N' Roses↔GNR 2 个`、`Guns 'N' Roses↔Guns N' Roses 1 个` 等 5 对。要点：①“模式→连接”的翻译机械可行；②但每一跳都是一次新 join，路径变长时代价组合爆炸——这正是 GD2e 02 章“关系代数没有邻接一等公民”论断（见 [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)）在本章的具象。完整 BFS/分量实验见 ./08 与 ./12 章。

## 1.6 本章易踩的口径坑

- 本章示例基于 **5.26 LTS**（✅ 仓库 README），`CREATE DATABASE`、`SHOW DATABASES` 等在 4.x 单库版不可用 ⚠️；
- 书中“推荐”是 `SIMILAR` 边的共现近似，不是 Ch.13 的向量召回——两代技术在同一数据集上对照，是本书刻意安排的演进叙事 ⚠️（逆推）；
- 块存储图讲的是社区版单存储卷形态，企业版分布式存储另说 ⚠️。

## 1.7 一页纸小结

| 问题 | 本章给的答案 |
|---|---|
| 我的数据需要图吗 | 多跳联系是查询主角时需要；报表不需要 |
| 属性图三件套 | 节点(标签+属性)/关系(类型+方向+属性)/两者皆可属性 |
| 为什么遍历快 | 免索引邻接=指针跟随，代价与图总量无关、与半径有关 |
| 第一周做什么 | 建库→预览 CSV→约束与索引→MERGE 幂等导入→模式查询 |
| 计算结果放哪 | 物化回图（SIMILAR 边），下次查询变一跳 |

## 1.8 三个代表脚本的注解式回放（⚠️ 依仓库文件名与 Cypher 通行语法重构）

其一，幂等导入（`004-merge-one-track` 一类）：

```cypher
// 示意重构：CSV 一行 → 一个 Track 节点 + 到 Artist 的关系
LOAD CSV WITH HEADERS FROM 'file:///tracks.csv' AS row
MERGE (t:Track {id: row.trackId})
ON CREATE SET t.name = row.trackName, t.popularity = toInteger(row.popularity);
```

要点是 `MERGE` 的匹配键必须有唯一约束兜底（`009-constraint-creation` 的存在意义），否则 MERGE 退化为“查不到就永远新建”⚠️。

其二，相似歌单（`012-find-similar-playlists`）：以共同曲目数为权重的对称评分——

```cypher
// 示意重构：两歌单共享曲目的数量与余弦近似
MATCH (a:Playlist)-[:HAS_TRACK]->(t:Track)<-[:HAS_TRACK]-(b:Playlist)
WHERE a.id < b.id
WITH a, b, count(t) AS common, a.size, b.size
WHERE common > 5
MERGE (a)-[s:SIMILAR]->(b)
SET s.score = toFloat(common) / sqrt(toFloat(a.size) * b.size);
```

其三，最短路径（`015/016-shortest-*`）：`shortestPath((x)-[:SIMILAR*]->(y))` 一行表达“两堆听歌品味之间的桥梁”——同样的问题在 SQL 里是递归闭包（本目录 🔧 类比在 ./08 完整跑过）。

## 1.9 本章埋下的全书伏笔清单

- `000-create-database` → Ch.9/Ch.10 的多库与集群拓扑；
- `008/009` 索引与约束 → Ch.5 计划选择、Ch.7 文本索引；
- `012/013` 相似性物化 → Ch.3 语义关系论、Ch.12 共现算法、Ch.13 向量近邻（物化 vs 现算的三步演进）；
- `014` 推荐 → Ch.13 LLM 混合推荐的原型；
- `015/016` 最短路径 → Ch.5 里它是最贵操作之一的伏笔。

## 1.10 概念边界（本章不回答什么）

- 不回答“图数据库内部怎么实现”——那是 Ch.9/10 与 GD2e 06 章；
- 不回答“Cypher 为什么这样设计语法”——见 [../Graph_Databases_2e/03-使用图进行数据建模.md](../Graph_Databases_2e/03-使用图进行数据建模.md) 的声明式论证；
- 不比较 Neo4j 与其他图库的吞吐——本册是单产品深潜书，横向选型请回 [../nosql精粹.md](../nosql精粹.md)。

## 核心概念速览（中英对照）

- **属性图模型** — Property Graph Model：节点/关系均可携带键值属性的图数据模型
- **免索引邻接** — Index-Free Adjacency：邻居通过物理指针直连，遍历不查索引
- **Cypher** — Cypher：用 ASCII 字符画表达图模式的声明式查询语言
- **幂等写入** — Idempotent Merge：`MERGE` 保证同模式只建一次，重跑导入不产生重复
- **相似性物化** — Materialized Similarity：共现计算结果写成 `SIMILAR` 边供后续一跳查询
- **标签** — Label：节点的类型标记，兼作索引入口，可多标签
- **关系类型** — Relationship Type：边的语义名，方向有意义
- **多数据库** — Multi-database：5.x 实例内多库隔离（书用独立 playlists 库）
- **最短路径** — Shortest Path：图上两定点间跳数/权重最小路径，第 1 章即登场
- **流媒体数据集** — Spotify Dataset 2023：全书贯穿的真实歌单/艺人/曲目数据 ⚠️ Kaggle 直链已失效
- **PoC 决策** — Proof-of-Concept Decisions：官方简介四要点之一，本书的叙事起点

## 最新演进与工业实践

- **GQL 标准定标（2024）**：Cypher 语法家族于 2024 年随 ISO/IEC 39075:2024 定标。Neo4j 官方逐条对照 Cypher 与 GQL 的符合性附录：https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/ （curl 200 ✅）；ISO 目录页 https://www.iso.org/standard/76120.html （403，仅入口链接）。含义：本章教的模式语法大部分已进入国际标准，跨图库迁移成本下降 ⚠️（方言仍在）。
- **版本现状**：书钉 5.26 LTS（✅ README），官方文档 current 已切换日历版本（2025.06/2026.02 表述见 Cypher 手册实抓页 ✅），5.x 处于维护期，新特性走 2025.x/2026.x 轨道 ⚠️（LTS 支持矩阵页本机不可达）。
- **云托管替代**：本章本地 Docker 流程在工业实践正被 AuraDB（https://neo4j.com/product/auradb/ ，200 ✅）吸收；PoC 阶段“装什么”的答案越来越多是“先不开服务器”⚠️。
- **同类书目对位**：属性图世界观详见 [../Graph_Databases_2e/03-使用图进行数据建模.md](../Graph_Databases_2e/03-使用图进行数据建模.md)；“块存储”式内核叙述的现代通用版在 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)；🔧 类比引擎的权威用法见 [../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)。
