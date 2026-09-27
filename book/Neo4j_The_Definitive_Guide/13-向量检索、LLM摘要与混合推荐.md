# 13 · 向量检索、LLM 摘要与混合推荐（Ch.13，章题为 ⚠️ 逆推重构，00 阅读地图口径）

> 取证锚点（✅ 实抓配套仓库 chapter13）：`cypher/001-community-samples.cypher` 全文（社区 44386 采样 10 曲：`MATCH (c:Community)-[:HAS_PLAYLIST]->(p) WHERE c.id=44386 ... ORDER BY rand() LIMIT 10`）；`python-scripts/01-community-summaries.py`（`from openai import OpenAI`、`model="gpt-4.1-mini"`、`text-embedding-3-small`、`db.create.setNodeVectorProperty(n,'summaryEmbedding',$embedding)` ✅ 逐行实读）；`02-playlist-recommendation.py`（`CALL db.index.vector.queryNodes('communitySummary', 20, $vector)` 与 `('question', 20, ...)` 双索引召回 ✅）；README（venv → .env → **两条 `CREATE VECTOR INDEX ... OPTIONS {indexConfig: {'vector.dimensions': 1536}}`** ✅）；requirements.txt（`neo4j`、`openai>=1.6.1`、`python-dotenv` ✅）；figures 13-7 community-samples、13-8 summary-chatgpt、13-9 vector-model、13-10 user-query-phase、13-11 recommendation。全书终章：**图结构当知识库、LLM 当翻译官、向量索引当门铃**。

## 13.1 终章位置学：为什么是这四位一体

书的后半部节奏（09 存储 → 10 集群 → 11 观测 → 12 算法 → 13 智能）对应官方简介第四拍“把图库并入既有企业架构”——而 2025 年语境下“并入”的最热路径就是 LLM/RAG 栈。本章把 Ch.12 的社区（结构化粗分组）、Ch.7 的检索三段式（7.9 预告兑现）、Ch.8 的实体真相（数据不干净一切皆然）全部收拢，落到一个可跑的双脚本管道上（✅ README 步骤齐全）。

## 13.2 向量索引：索引家族的第五格（✅ CREATE 语句实抓）

```cypher
CREATE VECTOR INDEX communitySummary FOR (n:Community) ON n.summaryEmbedding
  OPTIONS { indexConfig: { `vector.dimensions`: 1536 } };
```

（原文照录维度设定 ✅；第二索引 `question` 挂在 `:Question` 节点。）三点工程含义：

- 1536 维 = `text-embedding-3-small` 的输出宽度（✅ 两相对照）——**索引定义与 embedding 模型是婚约关系**，换模型=换维度=重建；
- 向量索引与 Ch.4 的 range/Ch.7 的 FTS 同属一个 catalog（`SHOW INDEXES` 统一可见 ⚠️ 惯例转述），7.11 决策树最后一支在此闭合；
- 节点属性承载向量（`db.create.setNodeVectorProperty` ✅）：向量是**节点的特征**，不是外挂库的镜像——图+向量单存储收敛的宣言句。

## 13.3 管道 A：社区 → 摘要 → 嵌入（✅ 01 脚本函数链）

`get_community_sample_tracks()`（13.1 引用的采样 Cypher，随机 10 曲）→ `get_chat_completion()`（gpt-4.1-mini + PROMPT_TEMPLATE ✅）→ 返回 JSON（`import json` ✅ 暗示结构化摘要：文本+问题列表）→ `store_community_summary()` 存属性 + `store_community_embedding()` 存 `summaryEmbedding` + `store_question_with_embedding()` 把**摘要衍生问题**也嵌入成 `:Question` 节点（✅ 函数名全链）。

关键设计（⚠️ 重构判断）：召回目标不是社区本身而是“用户可能问的问题”——Question 节点是查询分布的**代理索引**，属于 RAG 工程里“假问题真召回”（HyDE 思路的近亲）的图谱落地。

## 13.4 管道 B：提问 → 双路向量召回 → 生成（✅ 02 脚本）

`USER_QUESTION` 嵌入 → `find_similar()` 同时打 `communitySummary` 与 `question` 两个向量索引（k=20 ✅）→ 合并上下文 → `generate_response()`（同模型 ✅）。`13-10-user-query-phase.png`（✅ 图名）表明存在“建库期/查询期”两相分解——**重活（嵌入）全在离线相，在线相只有一次 embedding + 两次近邻**。13-9 vector-model 图给的是这盘棋的模型总览（图名逆推 ⚠️）。

## 13.5 混合检索骨架与 RRF（7.9 兑现 + 🔧 玩具实测）

本章官方配方是“图遍历 + 向量”的混合：向量选社区、`HAS_PLAYLIST` 出歌单（✅ 02 脚本语义）。🔧 概念类比（纯 python，非 Neo4j 行为）：`demo5_ch13.py` 用 4 条手写 5 维体裁向量 + `cos()` + RRF（1/(60+rank)）复现融合骨架，真跑输出 ✅：

- 向量 KNN（查询=硬摇滚向量）：`Guns N' Roses 系 > 车库复兴 > 合成器夜跑`；
- 全文路（关键词 `guns`）命中 1 条；
- RRF 融合终序：`c44386: Guns N' Roses 系 (0.03279) > c42 车库 (0.01613) > c17 合成器 (0.01587)`。

读法：两路都首推的对象分数叠加登顶、单路命中者被压后——**RRF 不消分数只排序位**，这就是官方混合配方里“融合层”的最小可懂形态。向量索引内部机制（HNSW 图跳/IVF 桶）归兄弟册 `Vector_Databases`（已落盘实链：[../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)，ANN 索引专章 [../Vector_Databases/05-ANN索引之二-从NSW到HNSW.md](../Vector_Databases/05-ANN索引之二-从NSW到HNSW.md)）：Neo4j 的 `vector.similarityFunction: cosine` 默认与 kNN 语义与其第 3 章相似度理论直接对位 ⚠️（对位为目录判断）。

## 13.6 工程边角：权限、新鲜度与幻觉面

- **权限**：向量召回同样要先过 Ch.6 的元素模式裁域（社区/Question 节点的 READ/TRAVERSE），否则“摘要泄露子图”成为新漏洞面 ⚠️（推演）；
- **新鲜度**：社区会漂移（12.5 阈值/重跑），摘要与嵌入是**派生缓存**——3.3“边即缓存”三问（频率/陈旧/一致性）原样适用于 `summaryEmbedding`；
- **成本**：管道 A 的 LLM 调用量 = 社区数（4158 个 ✅ 书中实数，含 2246 孤点）——先按 12.5 结论裁掉孤点社区再烧 API，是最便宜的混合优化 ⚠️（重构者算账）；
- **幻觉**：在线相的回答只引用召回的 summary 文本（✅ 脚本以 data=similar 组 prompt），可溯源性靠社区→歌单→曲目的三级证据链（13.3 采样 Cypher 即回放入口）。

## 13.7 全收束：从“为什么需要图”到“图的终局用途”

Ch.1 的相似歌单愿望（白板三问），Ch.2 灌进真数据，Ch.3/4 把语义刻进模式，Ch.5–8 让查询在生产里活下来，Ch.9–11 让机器睡得着觉，Ch.12 让图自己长出结构（社区），Ch.13 给结构装上嘴（摘要+问答）。**属性图的世界观在本章兑现为：结构即语料，遍历即溯源。** 与 GraphRAG 社区报告的业界范式（微软系等）同型 ⚠️（趋势转述，未引具体论文页）；GQL/向量标准化与图+检索论文线追踪归 [../../db/db.md](../../db/db.md)。

## 13.8 环境与版本取证（✅ 全部实抓自 requirements/README）

| 工件 | 内容 | 工程含义 |
|---|---|---|
| requirements.txt | `neo4j`（不钉版）、`openai>=1.6.1`、`python-dotenv>=1.0.0` | 驱动面信任 latest；LLM 客户端钉 1.x API 形态（`client.chat.completions` ✅ 脚本用法与之一致） |
| .env 模板 | `NEO4J_URI/USER/PASSWORD/DATABASE=book` + `OPENAI_API_KEY` | 库名 `book` 为 Ch.13 专用库（10 章多数据库的又一次兑现） |
| README 前置 | python venv + 两条 CREATE VECTOR INDEX 手工执行 | **索引建库不在脚本内**——schema 决策留给人，数据管道留给代码，分界清晰 |
| 书基线 | Neo4j 5.26 LTS（✅ 00 第一节）+ 1536 维 embedding | 5.13+ 才有向量索引（⚠️ 引入版本转述）；LTS 选择保证 Ch.9-12 与 13 同版本可复演 |

🔧 本机对照（非书环境，纯 python 标准库即可跑）：demo5_ch13.py 无第三方依赖（`math`/列表推导），说明 13.5 的融合语义与任何 SDK 无关——**先懂 RRF 的序位数学，再选框架**。

## 13.9 这条管道的验收清单（重构 ⚠️）

- **召回质量**：对 N 条金标准问题记录 communitySummary/question 两路的 hit-rate@k 与重叠率——两路全 miss 的问题列表就是下一批 Question 的原料（自扩展闭环 ✅ 脚本结构天然支持）；
- **溯源完整**：每条回答能沿“社区→HAS_PLAYLIST→曲目→ARTIST”回放证据（13.6 链路的 Cypher 化断言）；
- **成本可算**：离线相 LLM 调用数 = 有效社区数（先裁 2246 孤点 ✅）；在线相 = 1 embedding + 2 kNN + 1 completion；
- **重建可演**：换 embedding 模型 = drop 两个向量索引 + 全量重嵌入——把 13.2 “婚约”写成一条 runbook；
- **权限可验**：以 6.8 三角中“另一角色跑同一查询”的姿势，验证向量召回不越权。

## 13.10 反模式备忘（终章回扫全目录 ⚠️ 重构者判断）

| 反模式 | 病症 | 前章解药 |
|---|---|---|
| 一切文本都嵌入 | 精确键查询变概率游戏 | 7.11 决策树：键支不动 |
| 摘要不失效 | 社区漂移后答非所问 | 3.3 三问 / 13.6 |
| Question 一茬生成长 | 索引膨胀、互相吞召回 | 8.8 SOP 的回归位 |
| 只测端到端 | 分不清 embedding 差还是图烂 | 13.9 分层指标 |
| 向量索引当备份用 | embedding 丢了没源头 | Ch.9 恢复演练含 Community/Question |

## 13.11 与 GraphRAG 业界范式的对表（⚠️ 趋势转述，未引论文原文）

微软系 GraphRAG 的“实体抽取→社区分层→社区报告→全局/局部检索”四段，与本章“Ch.1 建模的既有图→Ch.12 社区→摘要→双索引问答”逐项可对齐——差别在**起点**：业界范式常从裸文本冷启动建图，本书图早已在 Ch.1–8 被生产化。这给了一个务实结论：**已有生产图库的团队做 GraphRAG，是从 Ch.12 起跑，不是从 Ch.1 重来**。13-11 recommendation 图（✅）收尾的正是这条最短路径。

## 13.12 接棒路线与资源（把本章当起点的人）

| 想做的事 | 本章已给 | 下一步 |
|---|---|---|
| 换自建 embedding | OpenAI 两家调用 ✅ | 本地开源模型：只改 `embed_text()`，维度婚约（13.2）跟着改 |
| 用官方框架 | 双脚本裸骨架 ✅ | neo4j-graphrag 生态线（⚠️ 未实抓页，名目转述）替换手写融合 |
| 检索要更快/更大 | kNN 直调 | ANN 内部机制：兄弟册实链 [../Vector_Databases/05-ANN索引之二-从NSW到HNSW.md](../Vector_Databases/05-ANN索引之二-从NSW到HNSW.md) |
| 图也要 LLM 帮建 | 图是既有的 | 反向管道（文本→图抽取）超出本书范围，归论文线 [../../db/db.md](../../db/db.md) |
| 全链上生产 | 13.9 验收单 | Ch.11 面板加召回/成本两指标、Ch.9 演练含 Question 库 |

终章的最后一条工程提醒：**本章没有新语法**——`CREATE VECTOR INDEX`、`queryNodes`、驱动调用，全部是前 12 章纪律在 AI 场景的直译。把书读到这里，“生产级 GraphRAG”应该已经不像一个新话题 ⚠️（重构者结语）。

## 核心概念速览（中英对照）

- **向量索引** — Vector Index：属性向量上的近似最近邻入口（✅ CREATE 实抓）
- **向量维度婚约** — Dimension Contract：索引配置与 embedding 模型的强耦合 ✅
- **节点内向量** — On-Node Embedding：`setNodeVectorProperty` 的收敛立场 ✅
- **社区摘要** — Community Summary：LLM 生成的社区语义画像（13-8 ✅）
- **假问题索引** — Question Nodes：以预期查询代理召回的嵌入节点 ✅
- **双索引召回** — Dual Index Recall：summary+question 两路 kNN 并集 ✅
- **两相管道** — Index/Query Phase：离线嵌入、在线近邻（13-10 ✅）
- **RRF 融合** — Reciprocal Rank Fusion：只认序位的混合召回合并法 🔧
- **混合检索** — Hybrid Search：向量/词法/图谓词的多路召回骨架（7.9 兑现）
- **摘要漂移** — Summary Staleness：派生文本+向量的缓存失效问题
- **证据链回放** — Evidence Traversal：社区→歌单→曲目→艺人的溯源路 ✅
- **自扩展闭环** — Self-growing Question Set：双路全 miss 的问题回喂 Question 索引（13.9）

## 最新演进与工业实践

- **原生向量索引现状**：5.13/5.14 引入的向量索引在 2025.x 与全文索引同框为官方混合检索配方（https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ 200 ✅，本目录多章已证）；`vector.dimensions`/`vector.similarity.function` 配置面延续 ✅（同上页族）。
- **模型换代**：书中钉的是 `gpt-4.1-mini` + `text-embedding-3-small`（✅ requirements/脚本）——OpenAI 模型线在 2025–2026 持续更名/换代（⚠️ 转述），迁移成本主要在**维度变更触发向量索引重建**（13.2 婚约条款）；requirements `openai>=1.6.1`（✅）是客户端下限而非充分版本。
- **GraphRAG 工业化**：社区摘要→分层检索的范式自 2024 起由多套开源实现（neo4j-graphrag 官方库、LangChain/LlamaIndex 集成）模板化 ⚠️（生态页未逐一实抓，不引 URL）；本章双脚本的价值在于展示**未用框架的最小可跑骨架**——框架化后每个函数都有对位积木。
- **兄弟册分工**：ANN 索引原理与评测（HNSW/IVF、recall@k）实链 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)；本册贡献的是“向量作为图属性”的存储/权限/新鲜度视角——两册合读为图+向量混合检索的完整拼图（00 §七第 1 条登记已兑现）。
- **论文与标准线**：GQL 符合性附录（https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/ 200 ✅）不含向量部分——语义索引仍是厂商扩展层，标准化是 2026+ 观察点 ⚠️（判断）。
- **托管面对位**：Aura 系产品同样暴露向量索引与混合检索配方（https://neo4j.com/product/auradb/ 200 ✅ 入口，页内细节未逐抓 ⚠️）——本章双脚本改连 `NEO4J_URI` 即云上可跑，自管/托管差异被驱动层吸收 ✅（README .env 结构佐证换连即迁）。
- **本目录收束**：至此 13 章全部建成；01–13 的验证链、🔧 三处（01/08/12）+1 处融合玩具（13.5/13.8 demo5）均在 `D:\develops\tmp\dbwave_w3_neo4j\` 可复跑，repo 零构建产物。
