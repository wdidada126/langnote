# 01 Cassandra 简介与谱系（原书第 1 章口径 ⚠️ 推定重构）

> 本章为精读重构题纲（非原书文本）。知识基线=Cassandra 2.x 时代公开文档与社区共识；
> 集群行为一律 ⚠️ 不实测。书与目录的取证状态见 [00-总览与阅读地图](00-总览与阅读地图.md)。

## 1.1 题纲

1. Cassandra 是什么：分布式、去中心化、最终一致优先的宽列存储
2. 谱系：Amazon Dynamo 的一致性/去中心模型 × Google BigTable 的数据模型
3. 出生地 Facebook：收件箱存储替换 MySQL 的动机（写扩散、可扩展、高可用）
4. 开源与 Apache 顶级项目历程；DataStax 公司与"发行版 vs 开源版"生态
5. 2.x 时代的关键转折：Thrift → CQL 原生协议、vnode、LWT、collections
6. 适用与不适用：OLTP 高写、海量 KV、时序/计数——但不要拿它当关系库

## 1.2 Facebook 的问题与 Dynamo 的答案（⚠️ 转述）

Facebook 2008–2010 年的收件箱（Inbox）需要在多数据中心做高可用消息存储：MySQL 主从在
"每个节点都要能写、网络分区时不能停"的需求下成为瓶颈。Cassandra 吸收了 Dynamo 的四个
核心件——**gossip 成员管理、一致性哈希数据分布、向量时钟（后演化为 LWW/时间戳冲突解决）、
 hinted handoff 与读修复**——再套上 BigTable 的"列族/有序分区"数据模型，形成"能水平扩展、
 无单点、写优先"的存储。理解本章的检验标准：能说出"Cassandra 里为什么没有主节点"，
 以及"为什么它的 INSERT 几乎总是成功而代价在别处"。

与理论端的对读关系：谱系与复制语义的通论在
[../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)（领袖/无领袖复制谱）与
[../设计数据密集型应用/06-分区.md](../设计数据密集型应用/06-分区.md)（一致性哈希）已给出；
本册 07/08 章是这些概念在 Cassandra 2.x 的实现细节。Dynamo 论文精读在
[../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md](../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md)（✅ 盘上存在）。

## 1.3 版本谱系速览（书中 2.x ↔ 现实）

| 版本 | 书中相关度 | 关键变化（⚠️ 社区共识转述） |
|---|---|---|
| 0.6/0.7 | 考古 | thrift API 时代；《cassandra实战》（郭鹏）基线，见 [../cassandra实战.md](../cassandra实战.md) |
| 0.8 | 背景 | 引入 CQL（beta）；密钥环概念成型 |
| 1.0/1.2 | 1e TDG 主体 | 原生协议 v1（2.0 前夜）；1.2 引入 **vnode**（实验） |
| 2.0 | 本册重点 | **CQL 取代 Thrift 成主接口**、原生协议 v1、LWT（Paxos）、混合索引（2i 成熟）、字节数组安全性 |
| 2.1 | 本册重点 | **UDT/tuple、物化视图（实验）、TWCS 出现**；协议 v2 |
| 2.2 | 本册重点 | 协议 v3、CDC 前身讨论（book 后社区落地）⚠️、默认压缩与内存表改进 |
| 3.0 | 书末余波 | 新 SSTable/压缩日志、原生协议 v4 前后、thrift 默认关闭 |
| 4.0/5.0/6.0 | 演进节 | thrift 移除、JDK17/SAI/vector/UCS、Accord/TCM——见 [00 §4 跨代对位表](00-总览与阅读地图.md) |

注：表中 2.x 细节为社区通行口径 ⚠️（官方 3.11/4.0/5.0 文档可反查 NEWS 记录）；3.x 运维侧
实证另见姊妹册 [../Expert_Apache_Cassandra_Administration/01-Apache_Cassandra简介.md](../Expert_Apache_Cassandra_Administration/01-Apache_Cassandra简介.md)。

## 1.4 设计取舍：AP 优先 + 可调一致性

CAP 语境里 Cassandra 传统归为 AP（分区容忍+可用优先），但"一致性"被做成**每查询可选的旋钮**
（CL 级别，08 章展开）：R+W>N 的 quorum 算术、ALL 的强读、ONE 的快脏读。书中反复强调的
"right-tuning"世界观：

- 可用性不是免费午餐：写全部成功意味着冲突被延迟解决（LWW 时间戳/counter 合并）。
- 性能预算要显式分配到"写放大/读放大/空间放大"三本账（LSM 共性，06 章的 SSTable 视角）。
- "无单点"≠"无运维"：gossip、修复、压实都在替你付账（#89 册的运维纵深端）。

一致性谱系的理论框架在 [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)；
本册 08 章给 CQL 侧的落地语义，两册互读。

## 1.5 数据模型一句话史

Cassandra 对外暴露的是"类 SQL 的表"（CQL），对内仍是分区键→聚簇列的宽列存储：

```sql
-- 2.x 口径示意（非实测）
CREATE KEYSPACE inventory WITH replication = {'class':'SimpleStrategy','replication_factor':3};
CREATE TABLE inventory.items (
  sku text, month int, day int,
  qty int, updated timeuuid,
  PRIMARY KEY ((sku, month), day)   -- 分区键 (sku,month)，聚簇列 day
);
```

读这段代码的正确方式：`PRIMARY KEY` 的第一个分量决定**数据在集群里怎么摆放**（分区），
其余分量决定**分区内怎么排序**（聚簇）——这是 05 章建模的公理，也是它和关系表最本质的区别。

## 1.6 本章在全目录中的挂点

- 想跑起来 → [02-安装部署与cqlsh](02-安装部署与cqlsh.md)
- 想懂数据模型细节 → [03-数据模型与核心概念](03-数据模型与核心概念.md)
- 想理解"为什么没有主节点" → [07-集群架构与Gossip](07-集群架构与Gossip.md)
- 想知道"AP 旋钮具体怎么拧" → [08-一致性与读写路径](08-一致性与读写路径.md)
- 想知道"这书 2026 还值不值得读" → [00 §8 FAQ](00-总览与阅读地图.md) 与本页文末演进节
- 管理员视角的同题章节 → #89 册 [05-Cassandra架构](../Expert_Apache_Cassandra_Administration/05-Cassandra架构.md)

## 核心概念速览（中英对照）

- **宽列存储** — Wide-column store：以"分区键+列"组织的分布式存储，BigTable 数据模型家族。
- **去中心化** — Decentralized / leaderless：无主节点，节点对等，写入任意副本入口。
- **gossip** — Gossip protocol：节点间周期广播成员与状态信息，取代中心注册表。
- **一致性哈希** — Consistent hashing：以 token 环决定分区归属，扩缩容只搬局部。
- **向量时钟** — Vector clock：Dynamo 的冲突谱系记录；Cassandra 主线演化为时间戳 LWW。
- **最终一致** — Eventual consistency：不承诺即时全局可见，依赖修复与读修复收敛。
- **hinted handoff** — Hinted handoff：副本暂时不可写时由邻居代存提示，恢复后补写。
- **读修复** — Read repair：读路径发现副本不一致时顺带异步修复。
- **CQL** — Cassandra Query Language：2.x 起的主接口，SQL 外观但按分区语义设计。
- **原生协议** — Native (CQL binary) protocol：替代 thrift 的客户端二进制协议，v1/v2/v3 对应 2.x 系。
- **LWT** — Lightweight Transaction：`IF` 条件的 Paxos 线性化写，慢但强。
- **vnode** — Virtual node：每节点持多段虚拟 token，均衡数据与流式搬迁粒度。
- **DataStax** — DataStax：Cassandra 主要商业支持者；本书作者供职体系的来源背景 ⚠️。
- **AP 优先** — AP-first：CAP 语境的默认立场，配合每查询一致性旋钮。

## 最新演进与工业实践

（2026-09 口径；除注明外均本会话 `curl` 实抓 ✅）

- **版本现状**：Latest GA=**5.0（5.0.9，2026-08-07）**，4.1.12/4.0.21 受支，6.0 有专版文档但
  站点标预发布（版本选择器已现 7.0）。源：https://cassandra.apache.org/_/download.html
- **书中 2.x 全部退役**：thrift 4.0 起移除（NEWS 原文 "Starting version 4.0, Thrift is no longer
  supported"，✅ https://raw.githubusercontent.com/apache/cassandra/cassandra-4.0/NEWS.txt ）；
  2.x SSTable 格式不可被现代版直读，升级路径必须经 3.x/4.x 逐级 ⚠️。
- **谱系的当代回声**：6.0 官方新特性清单 **ACID Transactions (Accord)、Transactional Cluster
  Metadata（TCM）、Constraints**——Dynamo 式"最终一致"正被补上可串行化事务与事务化元数据，
  与本章"AP+旋钮"世界观构成正面对照。源：
  https://cassandra.apache.org/doc/6.0/cassandra/new/index.html 、
  https://cassandra.apache.org/doc/6.0/cassandra/architecture/accord.html （站标预发布 ⚠️）。
- **工业采用**：Netflix/Discord/Apple 等大规模画像持续是社区演讲素材 ⚠️（本册不引入未核数字）；
  国内语境下 Cassandra 热度低于 MySQL/PG 系，选型讨论可对照
  [../数据库系列·总索引.md](../数据库系列·总索引.md) 的 NoSQL 书目带。
- **读法建议**：本章所有"版本大事记"以 00 的跨代对位表为准轴；生态厂商动态（IBM 收购 DataStax
  等）沿用 #89 册 00 的实抓基线（其 §4 生态行），两册合并即 2013→2026 的 Cassandra 编年。
