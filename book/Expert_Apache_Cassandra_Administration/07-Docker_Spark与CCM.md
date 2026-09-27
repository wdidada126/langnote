# 07 Cassandra on Docker, Apache Spark, and the Cassandra Cluster Manager（Docker、Spark 与 CCM）

> 原书第 7 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。本章三件套都属"周边生态"，
> 2026 年变化全书最大，文末对位表逐条给实证。容器/集群不本机实测 ⚠️。

## 题纲

- **Docker**：把 02/03 章的部署剧本容器化——镜像、卷、网络、多节点 compose，试验便利与
  生产审慎的边界。
- **Spark**：Cassandra 作为分析管道的一端——连接器两条 API（RDD/DataFrame）+ 旁路 bulk
  生成 SSTable 的第三条高速路。
- **CCM**：Cassandra Cluster Manager，开发者/测试者的多节点假集群一键起停，也是 CI 里
  "版本回归"的事实标准工具。

## 1. Docker（书语境：docker-compose 初兴）

```bash
docker run -d --name c1 -v /data/c1:/var/lib/cassandra \
  -e CASSANDRA_CLUSTER_NAME=lab cassandra:3.11   # 官方 library 镜像（tag 现状见文末⚠️）
```

- 容器化三注意（⚠️ 转述）：数据卷必须外置（05 章"不可变 SSTable"决定了目录即遗产）；
  gossip 端口在 bridge 网络下的地址通告问题（listen/broadcast 地址要与网络拓扑对表）；
  资源限制与 `HEAP_SIZE` 环境变量联动，别让 JVM 按宿主机内存自动算。
- 多节点：compose 定义 seed 服务+3 节点、固定 DC/rack 环境变量；跨主机则回 03 章剧本。
- 本书时代的生产观：**容器=试验场，裸机/VM=生产**——2026 年这条已经反转（文末）。

## 2. CCM：一键假集群（开发/CI 工具，勿上生产）

```bash
pip install ccm
ccm create test -v 3.11 -n 3 -s --snitch=GossipingPropertyFileSnitch
ccm node2 decommission          # 演练 03 章生命周期剧本
ccm populate -n 4 -s            # 或预建 4 节点
ccm stress                      # 内置 cassandra-stress 调用
```

- 定位：在**单机**上跑多进程模拟多节点，改 yaml/换 JVM 参数/回放日志都在手边；
  回归测试与"故障剧本彩排"（03/09 章的验收单可在 ccm 上走纸面推演 ⚠️ 本目录未实机执行）。
- 版本参数直接吃 Apache tarball，也能指本地构建——它是"版本升级彩排"的最佳低代价舞台。

## 3. Spark：连接器的三条通道（3.x/Spark 2.x 书语境）

- **DataFrame 读写**（默认推荐）：
  `spark.read.format("org.apache.cassandra.sql.spark.CassandraSource")`（旧 API 风格 ⚠️ 通述），
  谓词下推按分区裁剪；写侧 `df.write...option("writeConcurrency", ...)`。
- **RDD API**：`sc.cassandraTable("ks","tbl")` 扫描全表（token 切分并行）、
  `saveAsCassandraTable` 批量写——运维盯的是扫描并发与表端读放大（11 章联动）。
- **Bulk output（旁路高速路）**：Spark 直接**生成 SSTable** 再 bulk load（8 章 sstableloader
  的集群版），绕开 CQL 写路径——TB 级灌数的正解；代价：要对 schema/分区器严格同构，出错恢复复杂。
- 运维视角的通用警告：Spark 作业是"合法的内建流量洪水"，
  并发×分区扫描宽度要与集群 tpstats/compaction 余量对表（10 章）。

## 4. 本章组合拳的边界

- 试验栈（Docker/CCM）回答"行为会不会这样"，分析栈（Spark）回答"数据怎么进出最快"；
  **两者都不回答**"生产拓扑怎么活十年"——那是 03/09/12 章的主场。
- 书内示例版本（Cassandra 3.x、Spark 2.x、连接器 2.x、compose v1/v2）到 2026 全部代际过期，
  迁移清单见文末。

## 5. 三工具命令卡（⚠️ 转述，容器/集群未本机实测）

```bash
# Docker：单节点试验 + 侦察
docker exec -it c1 cqlsh -e "DESCRIBE CLUSTER"
docker exec -it c1 nodetool status
docker inspect -f '{{range .Mounts}}{{.Source}}{{end}}' c1   # 核数据卷真的在外

# CCM：生命周期彩排（03 章剧本的纸面推演）
ccm create lab -v 3.11 -n 3 -s
ccm node1 status; ccm node2 decommission -b   # 退役+重建环
ccm updateconf "concurrent_reads: 64" && ccm restart   # 参数实验
ccm remove lab                               # 用完即焚

# Spark：连接器最小读路（DataFrame，2.x 旧 API 风格 ⚠️）
spark-shell --packages datastax:spark-cassandra-connector:2.0-x-s_2.11
scala> spark.read.format("org.apache.cassandra.spark.sql.CassandraSource")...
# 写侧盯两件事：writeConcurrency 与目标集群 tpstats（10 章）
```

## 6. 本章十问（自测）

1. 容器化三注意各挂在 05 章哪条机理上？（§1）
2. bridge 网络下为什么 listen/broadcast 要分开想？（§1）
3. CCM 的定位红线（能做什么/绝不能做什么）？（§2）
4. ccm 如何做"版本升级彩排"？（§2/8 章 sstableupgrade）
5. 连接器三通道分别绕开/保留了写路径的哪些环节？（§3）
6. bulk output 的速度来源与其正确性前提？（§3）
7. Spark 作业为什么是"合法流量洪水"？盯哪两个指标？（§3/10 章）
8. token-aware 对性能的意义？（速览）
9. 2026 年三件套的仓库归属各自变成什么？（文末表）
10. "Stargate 落幕"与"UPTOPIA"两个书单注记的核验结论？（文末/00 章）

## 核心概念速览（中英对照）

- **Docker volume** — 数据卷外置：/var/lib/cassandra 落宿主存储，容器可弃、数据不可弃。
- **broadcast address** — 通告地址：NAT/bridge 网络下 gossip 对他节点可见的身份地址。
- **CCM** — Cassandra Cluster Manager：单机多进程假集群 CLI，pip 安装。
- **populate** — 预建：ccm 一键拉起 N 节点并启动。
- **spark-cassandra-connector** — Spark 连接器：DataFrame/RDD/bulk 三通道适配器。
- **predicate pushdown** — 谓词下推：把过滤按分区键裁剪推到表端，省两侧带宽。
- **bulk output format** — 旁路 SSTable 生成：绕 CQL 写路径的 TB 级装载。
- **cassandra-stress** — 压测器：CCM 内置调用，也是 11 章基准工具。
- **token-aware** — token 感知：连接器/驱动按副本落点选连接，减少协调跳转。
- **saveToCassandra** — DataFrame 写入：选项含并发、if-not-exists、分组写入。
- **write concurrency** — 写并发：客户端并行度与表端 memtable/压实余量的平衡旋钮。
- **CI matrix** — 版本回归矩阵：CCM 多版本起停支撑升级/修复用例自动化。

## 最新演进与工业实践

（本章对位表的取证口径：✅ api.github.com/pypi 实抓，github.com 页本机直连超时故以 API 元数据核验；具体章目对位以各章目录版为准。）

| 书内技术栈（2017） | 2026-09 现状 |
|---|---|
| `datastax/ccm` | 仓库已迁 **apache/cassandra-ccm**（riptano/ccm 301 重定向核验 ✅），pypi `ccm` **3.1.5**（✅），最后 push 2026-04（✅）——仍活跃 |
| `datastax/spark-cassandra-connector` | 已迁 **apache/cassandra-spark-connector**，最新 release **v3.5.1**（✅）；开源连接器全面 Apache 社区化 |
| `datastax/java-driver` | 已迁 **apache/cassandra-java-driver**，最新 **4.19.3**（✅） |
| Docker 试验为主、裸机生产 | 反转：**K8s/operator 成新建主流**；官方 sidecar 项目 apache/cassandra-sidecar 在档（✅）；datastax/cass-operator 仓存在但最后 push 2023-12（✅ API），后续维护归属按 ⚠️ 存疑处理 |
| Stargate（本书出版后才出现的 API 网关，2020 起） | 任务注记"UPTOPIA/Stargate 落幕"：**核验结果**——stargate/stargate 仓未归档、最后 push 2026-07-05（✅ API 实抓），"完全落幕"证据不足 ⚠️；"UPTOPIA" 经 Crossref/网络检索无法确指 ⚠️；DataStax 本体已于 2025-02 被 IBM 完成收购（媒体报道口径 ⚠️） |
| 书内 Spark 2.x/连接器 2.x API | 连接器 3.x 面向 Spark 3.x，包名/配置键大改；3.5.1 支持 Cassandra 5.0（✅ release 语境） |

- 对位阅读：数据管道视角另见 [../ApachePulsar原理解析与应用.md](../ApachePulsar原理解析与应用.md)（流式生态邻座，若关心"Spark 之外"的现代化）。
- 概念史注：Flink 书
  [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)
  的连接器生态可对照"Cassandra 作为流终点"的 2017-2026 变化 ⚠️（该链接为总览级互见，具体章目以对方目录版为准）。
