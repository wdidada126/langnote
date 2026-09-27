# 01 · Introducing Elasticsearch（初识 Elasticsearch）

> 取证基座：章题与二级节（1.1 Solving search problems / 1.2 Exploring typical use cases / 1.3 Summary）✅ Manning getTocHtml?id=548 实抓；正文为精读重构，⚠️ 为转述/推定，🔧 为本机类比（SQLite 3.45.3 FTS5 / DuckDB 1.5.5，**非 ES 行为**）。

## 章定位

全书起点：为什么「搜索」是一个数据库引擎解决不了（或解决不好）的问题，Elasticsearch 用哪三板斧解决——快（倒排索引）、准（相关性打分）、懂人话（全文匹配超越精确匹配）；然后给出三类典型落地姿势与第一次跑通安装验证。对位本系列：概念底座可先看 [../Elasticsearch_The_Definitive_Guide/01-入门与基础查询.md](../Elasticsearch_The_Definitive_Guide/01-入门与基础查询.md)。

## 内容地图（原书二级节 ✅ 实抓）

- 1.1 用 Elasticsearch 解决搜索问题：1.1.1 快速搜索 / 1.1.2 保证相关性 / 1.1.3 超越精确匹配
- 1.2 探索典型用例：1.2.1 作为主后端 / 1.2.2 挂在既有系统旁 / 1.2.3 配合既有工具 / 1.2.4 主要特性 / 1.2.5 对 Lucene 的扩展 / 1.2.6 数据分层结构 / 1.2.7–1.2.9 装 Java、下载启动、验证

## 1.1 搜索问题的三个层次（⚠️ 转述）

1. **快**：`LIKE '%term%'` 型扫描在文本库上随数据量线性劣化；倒排索引把「词→文档」预计算，查询变成Posting List 的交并。
2. **准**：搜索结果要按「与查询的相关程度」排序，而非时间/主键；1.x 默认 TF-IDF 族打分（BM25 自 ES 5.0 才成默认，✅ https://www.elastic.co/guide/en/elasticsearch/reference/5.0/breaking-changes-5.0.html 实抓）。
3. **懂人话**：用户写「running shoes」，库里存「run shoe」也得命中——需要分词、词干化、同义处理（第 5 章展开）。

🔧 类比组 A（本册 4 组类比之一，SQLite 3.45.3 真实跑过）：

```sql
CREATE VIRTUAL TABLE docs USING fts5(title, body, tokenize='unicode61');
-- 5 条语料后：
SELECT rowid FROM docs WHERE docs MATCH 'search OR searching';
-- 命中 rowid {3,5}：词项查询走倒排，而非扫描
CREATE VIRTUAL TABLE v USING fts5vocab(docs,'row');
SELECT term, doc, cnt FROM v WHERE term IN ('search','searching','inverted');
-- ('index',1,1) ('inverted',1,1) ('search',1,2) ('searching',1,1)
```

fts5vocab 输出的就是「词项→文档数/出现次数」的**词项字典+倒排表投影**，与 ES 1.x 文档讲的 inverted index 同构；但 FTS5 无打分调优、无分布式、无 mapping——**不可把此处行为外推到 ES**。

## 1.2 三类用例与 ES 特性（⚠️ 转述 + 对位）

| 用例 | 姿势 | 工程含义 |
|---|---|---|
| ES 作主后端 | 文档直接进 ES，不另设 RDBMS | 1.x 事务/关系弱，2015 年即属激进姿势；今天对应「日志/可观测后端」主流场景 |
| 挂在既有系统旁 | DB 存真相，ES 存可搜索投影，双写或异步同步 | 本册餐厅应用即此路线；对位 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 的「索引是数据的派生物」视角 |
| 配合既有工具 | Logstash 采集、Beats/Kibana 展示等生态 | 生态线 2026 现状见演进节 |

特性清单（⚠️ 转述）：分布式与零配置发现、近实时（NRT，默认 refresh 1s 量级）、JSON 文档 + HTTP REST、schema-free 但有 mapping、多租户索引。对 **Lucene 的扩展**：Lucene 是单机 Java 库（索引+查询引擎），ES 加集群、分片复制、REST API、聚合——这段与本目录 [../从Lucene到Elasticsearch.md](../从Lucene到Elasticsearch.md)（gitee 题录占位，登记对位）同题；深入版见 [../Elasticsearch_The_Definitive_Guide/04-Lucene入门.md](../Elasticsearch_The_Definitive_Guide/04-Lucene入门.md)。

**1.x 数据分层**（后续全书词汇表）：cluster ⊃ index ⊃ type ⊃ document ⊃ field；物理侧 index 切 shard（主/副本），shard 即一个 Lucene 实例。type 在 7.x 废弃、8.x 移除（✅ https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html 实抓）——读 2015 文本时把 type 心智替换为「索引名即类型」。

## 1.2.7–1.2.9 首跑三步（⚠️ 转述）

装 JDK（1.x 时代强依赖外部 Java）→ 解压 ES 二进制、`bin/` 启动（默认 9200 HTTP/9300 节点间 transport）→ `curl localhost:9200` 看版本 JSON 即成功；再装 elasticsearch-head 插件做可视化（该插件已死，见演进节）。本环境实测确认 **ES 不可装**：本机无 ES 可执行文件，Docker registry 拉取超时/403（2026-09-27 实测，过程见 00 顶部声明），故本章全部 ⚠️ 不伪装跑通。

## 工程要点与常见坑

- 2015 年常见误区：把 ES 当唯一数据源——1.x 无持久事务保证；今天官方也仍建议「DB 为真相、ES 为投影」或明确接受其文档库定位（⚠️）。
- head/marvel 类浏览器插件依赖已删的 `_plugin/_head` 路径，照书装会在 2.x+ 直接报错。
- 「零配置发现」的组播在云上会误合集群——1.x 即有此坑，7.0 后组播被彻底移除、改 seed hosts（⚠️，✅ 总述见 https://www.elastic.co/docs/deploy-manage/upgrade）。

## 延伸阅读（repo 内）

- NoSQL 谱系定位：[../nosql精粹.md](../nosql精粹.md)、[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)（文档模型对照）、[../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)（「搜索是二级索引」另一种取舍）
- 七周视角的 ES 章：[../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md](../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md)
- 论文线：[../../db/db.md](../../db/db.md)（倒排索引与检索谱系挂点）

## 首跑流水对照（1.x 原书式 ⚠️ 转述）

```bash
# 1) 装 JDK 后解压 ES，默认配置直接起
bin/elasticsearch                # 控制台打印节点名与集群名 [Sun Tzu]
# 2) 验证 HTTP 面
curl localhost:9200
# → { "name":"Sun Tzu", "cluster_name":"elasticsearch", "version":"1.x", "tagline":"You Know, for Search" }
# 3) 可视化（书中第一步插件）
bin/plugin -install mobz/elasticsearch-head
# → 浏览器 http://localhost:9200/_plugin/head/ 看到空集群面板
# 4) 索引第一份文档（下一章展开）
curl -XPUT localhost:9200/restaurants/type/1 -d '{ "name":"Elastica" }'
curl 'localhost:9200/_search?q=elastica'
```

⚠️ 本环境 ES 不可装（00 顶部实测声明），以上为文献口径转述；`_plugin/head` 路径在 2.x+ 已死，`-install` 语法亦被 `elasticsearch-plugin install` 取代（⚠️）。

## 2026 复读清单

- [ ] 「快/准/懂人话」三问能否各举一个自己系统的反例？
- [ ] cluster⊃index⊃(type 已死)⊃document 的现代默写：cluster⊃index⊃document。
- [ ] NRT 1s 刷新在自己的测试代码里造成过多少假阴性？
- [ ] 「DB 真相 + 搜索投影」的双写链路，现在由 CDC/ingest 还是自研同步器承担？
- [ ] 首跑改用官方 Docker 镜像/K8s Operator 或 Elastic Cloud，安全默认开——跳过 01 装机叙事。

## 章内问答（自测）

**Q1 为什么关系库 B+树帮不了全文搜索？**
A：B+树擅长前缀可比较的等值/区间；`%middle%` 类模式无索引可走，倒排把匹配移到「词项字典 O(log V) +  posting 交并」。🔧 组 E 的 DuckDB 全扫对照即其代价实测。

**Q2 「主后端」用例为什么在 2015 年被书中劝退？**
A：1.x 无事务、无外键、schema 弱约束；书中立场是「旁挂投影」为主流，主后端仅在文档即真相的域（日志/目录）成立。

**Q3 ES 与 Lucene 的边界一句话？**
A：Lucene=单机索引/查询库（段、倒排、打分原语）；ES=在其上加 REST、分片、复制、发现、聚合与近实时刷新。

## 核心概念速览（中英对照）

1. **倒排索引** — Inverted Index：词项到文档列表的映射，全文搜索的核心数据结构。
2. **相关性** — Relevance：按匹配质量而非物理顺序排列结果的机制。
3. **全文匹配** — Full-text Matching：经分词/归一后按词命中，超越逐字符精确匹配。
4. **近实时** — Near Real-Time (NRT)：写入后约 1 秒可被搜索的刷新模型。
5. **集群** — Cluster：一组共享状态的节点集合，以 cluster.name 聚合。
6. **索引** — Index：同类文档的物理容器，切分为分片。
7. **类型** — Type：1.x 的 index 内逻辑子类，7.x 起废弃、8.x 移除。
8. **分片** — Shard：索引的水平切片，即一个 Lucene 实例，有主/副本之分。
9. **文档** — Document：JSON 原子记录，ES 的最小存储单元。
10. **Lucene** — Lucene：Apache 单机搜索库，ES 的引擎内核。
11. **词项** — Term：分词与归一后的索引最小单位。
12. **REST over HTTP** — HTTP REST API：ES 的全部操作面，1.x 默认 9200 端口。

## 最新演进与工业实践

- **版本跨度**：2015 基线 1.x → 5.0（2016，BM25 默认 ✅ https://www.elastic.co/guide/en/elasticsearch/reference/5.0/breaking-changes-5.0.html）→ 7.x（types 废弃）→ 8.0（types 移除 ✅ https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html）→ 9.x（官方文档 current 已入 9.x 时代，发布列表 ✅ https://www.elastic.co/docs/release-notes/elasticsearch，访问日期 2026-09-27）。
- **装机体验翻案**：今天首跑是 Docker 官方镜像或 Elastic Cloud，**默认开启 TLS 与账号认证**，8.x 首启生成 enrollment token——书里「curl 裸连 9200」不再安全可用（⚠️ 转述官方部署文档，✅ 总入口 https://www.elastic.co/docs/deploy-manage/upgrade）。
- **Serverless**：Elastic Cloud Serverless 把「装 ES」变成「开项目」，自动扩缩与按量计费，索引分层对用户隐去（✅ https://www.elastic.co/cloud/serverless，访问 2026-09-27）。
- **许可与分叉**：2021-01 ES/Kibana 退出 Apache-2.0 改 SSPL+ELv2 双许可（✅ https://www.elastic.co/blog/licensing-change）→ AWS 依 7.10 分叉 OpenSearch（✅ https://opensearch.org/ 实抓可达）→ 2024-08 Elastic 又为 ES/Kibana 增补 AGPLv3 选项回归开源（⚠️ 官方博客 slug 本环境不可达，二手报道 ✅ https://www.apmdigest.com/elastic-announces-open-source-license-elasticsearch-and-kibana-source-code）；Elasticsearch 本体许可证现文 ✅ https://www.elastic.co/licensing/elastic-license。
- **收购与生态线**：Elastic 近年并购（如 Blue Medora 2021、Jina AI 2025 等）业界广泛报道，⚠️ 本环境未能一手验证官方博客 slug，仅登记为待考；搜索侧生态（Search Labs 与向量/推理新能力）✅ https://www.elastic.co/search-labs。
- **监控插件**：书中 elasticsearch-head 等浏览器插件全部退役，现代替代为 Kibana 栈监控（⚠️ 转述；对应 1.x 插件章的今值见本目录 12 章演进节）。
- **工业实践**：日志可观测（ELK→Elastic Observability）、检索增强生成（RAG）的向量底座、企业搜索三分天下；概念层「倒排为何快」仍与本册一致，FTS5 类比在 2026 依旧是最低成本的心智模型（本册 🔧 组 A）。
