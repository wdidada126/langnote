# 02 Installing Cassandra and Getting Started with CQL Shell（安装与 cqlsh 入门）

> 原书第 2 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。安装/命令细节以
> Apache Cassandra 3.11 官方文档（✅ 可达，https://cassandra.apache.org/doc/3.11/cassandra/getting_started/installing.html ）
> 为知识基线转述，未本机实测集群 ⚠️。

## 题纲

本章解决"把单机 Cassandra 立起来并说出第一句 CQL"：tarball 安装的文件布局、Java/Python 前置、
关键配置文件的分工、启动与自检三连（`nodetool info/statusring/version`），以及 cqlsh 的
连接、COPY、描述与会话级旋钮。DBA 视角的隐含主线是：**装完之后第一件事不是建表，是认识配置文件**。

## 1. 前置与安装路径（3.x 基线）

- 三选一：源码构建 / **二进制 tarball**（书与生产主流）/ 发行版包（rpm/deb）。
- 硬前置：3.x 要 **Java 8**（7 已废）✅ 文档口径；cqlsh 依赖 **Python 2.7**（3.x 时代）⚠️ 通述。
  2026 对位见文末（JDK 17、Python 3、cqlsh 换实现）。
- tarball 目录导读（运维必须记住的五个）：
  - `bin/`：`cassandra`（启动器，读环境）、`cqlsh`、`nodetool`、`sstable*` 工具族。
  - `conf/`：**cassandra.yaml**（集群行为主开关）、cassandra-env.sh（JVM）、
    cassandra-rackdc.properties（snitch 身份）、commitlog_archiving.properties、log4j/logback。
  - `data/`、`commitlogs/`、`saved_caches/`：数据三兄弟目录（3.x 起另有 hints/、cdc_raw/ 子目录 ⚠️）。
- 安装即踩的坑（转述 ⚠️）：`MAX_INDEXED_KEYS`/`HEAP_SIZE` 类环境变量在 cassandra-env.sh 里
  按内存自动算；单机试用可 `auto_bootstrap=false` 防误拉流；`-f` 前台启动便于观察。

## 2. 首次启动与自检

```bash
bin/cassandra            # 后台，日志看 system.log
bin/nodetool info        # ID / uptime / load / token
bin/nodetool status      # 单机也应显示 UN / L=数据量
bin/cqlsh 127.0.0.1 9042 # 原生传输端口（thrift 在 3.0 起默认不启动，NEWS.txt 3.0 ✅）
```

- 日志判读：`system.log` 里出现 "Starting listening for CQL clients" 才算可用；
  gossip 完成、token 环确立的逐行语义在第 5/10 章接管。
- 单机默认即"RF=1 集群"：不要在生产用 SimpleStrategy 单机裸跑（3 章的部署剧本从这里分叉）。

## 3. cassandra.yaml 首读清单（本章视角，09/11 章再调）

| 参数 | 默认倾向 | DBA 关注点 |
|---|---|---|
| `cluster_name` / `num_tokens` | 256 | 改环 = 重建集群级动作 ⚠️ |
| `listen_address` / `rpc_address` | localhost | 跨机不通九成是这里 |
| `seed` 列表 | - | 只影响 gossip  bootstrap 起点（3 章） |
| `commitlog_sync` | periodic | batch 模式的可用性代价（5/11 章） |
| `memtable_*` / `compaction_*` | 自适应 | 11 章调优主战场 |
| `authenticator` | AllowAll | 生产装好当天就换 PasswordAuthenticator（12 章） |
| `start_native_transport` / 9042 | on | 客户端唯一该见的门 |

## 4. cqlsh 入门（会话即工具箱）

- 连接参数：`-u/-p`（启用认证后必带）、`--ssl`、`-k keyspace`；退出 `.quit`。
- 元命令：`DESCRIBE`（schema/cluster/table）、`SOURCE 脚本`、`PAGING ON/OFF`、
  `TRACING ON`（11 章诊断入口）、`CONSISTENCY`（会话级 CL，默认 LOCAL_QUORUM ⚠️ 推定）。
- **COPY 命令**：`COPY t FROM 'f.csv' WITH DELIMITER=... AND HEADER=...`；
  定位是**万行级**导入导出，百万级要 sstableloader（8 章）——这是 cqlsh 最常被误用的点。
- 第一组对象：

```sql
CREATE KEYSPACE demo WITH replication =
  {'class':'SimpleStrategy','replication_factor':1};
CREATE TABLE demo.posts(id uuid, title text, body text,
  PRIMARY KEY (id));
INSERT INTO demo.posts(id,title,body) VALUES(now(),'t','b');
SELECT * FROM demo.posts WHERE id = ...;   -- 必须带分区键（4 章全章苦口）
```

- `cassandra-stress`/`cassandra -f` 属工具篇，在 9/11 章按需转述。

## 5. 本章的运维判例（精读重构 ⚠️）

1. "起不来" → 先看 system.log 最后 20 行 + `jinfo` 验证 heap；九成是 JVM/端口/目录属主。
2. "能 ping 不能连" → 9042 与 7000/7001 的防火墙矩阵，rpc_address 是否 0.0.0.0。
3. "cqlsh 连得上、驱动连不上" → 协议版本与驱动代际错配（4.x 驱动不再支持 2.x 协议 ⚠️ 通述）。
4. 单机试用把 `authenticator` 改了忘改回 → 用 `cassandra/cassandra` 默认口令进，再改（12 章）。

## 6. 装机/侦察一页命令卡（3.x 语境 ⚠️ 转述）

```bash
# 前置侦察
java -version                      # 要 8
python --version                   # cqlsh 要 2.7（3.x 时代）
ulimit -n 100000; swappiness 检查   # OS 合同见 09 章

# 安装与首启
tar xzf apache-cassandra-3.11.x-bin.tar.gz && cd $_
grep -E 'listen_address|rpc_address|authenticator|seed' conf/cassandra.yaml
bin/cassandra -f                   # 首启前台看日志
bin/nodetool info; bin/nodetool status; bin/nodetool ring

# cqlsh 侦察流
bin/cqlsh
DESCRIBE CLUSTER; DESCRIBE KEYSPACES;
CONSISTENCY LOCAL_QUORUM; TRACING ON; PAGING ON;
COPY demo.posts TO 'posts.csv' WITH HEADER = TRUE;
```

## 7. 本章十问（自测）

1. tarball 的五个关键目录分别承载什么生命周期数据？（§1）
2. 3.0 之后 thrift 与 9042 的地位各如何？依据出处？（§1/§5、NEWS.txt ✅）
3. `nodetool info` 与 `status` 的分工？（§2）
4. 首启日志里"可服务"的标志行是什么？（§2）
5. cassandra.yaml 首读清单里，哪三个参数管"连不上"类工单？（§3）
6. COPY 与 sstableloader 的量级红线各在哪？（§4/8 章）
7. cqlsh 的会话级 CL 与 TRACING 分别服务什么诊断？（§4/11 章）
8. "能 ping 不能连"的两种根因？（§5）
9. `auto_bootstrap=false` 什么时候该设？（§1）
10. 2026 年拿本书脚本上 5.x 跑，先修哪两样前置？（文末）

## 核心概念速览（中英对照）

- **tarball install** — 二进制包安装：解压即用，配置全在 conf/，发行版差异自担。
- **cassandra.yaml** — 主配置：集群行为开关的单一事实源。
- **cassandra-env.sh** — JVM 环境：堆大小、GC、JMX 开关脚本。
- **cassandra-rackdc.properties** — DC/Rack 身份文件：配合 GossipingPropertyFileSnitch。
- **native transport** — 原生传输：9042 端口 CQL 二进制协议，thrift 的替代者。
- **nodetool info/statusring** — 自检三连：节点身份、环视图、版本。
- **cqlsh** — CQL shell：元命令（COPY/DESCRIBE/TRACING/CONSISTENCY）丰富的交互壳。
- **COPY FROM/TO** — CSV 搬运：万行级导入导出，非批量装载工具。
- **system.log** — 系统日志：启动成败的第一现场。
- **auto_bootstrap** — 引导开关：新集群/环手术时防自动拉流。
- **seed node** — 种子节点：gossip  bootstrap 的会合名单（非永久父节点）。
- **num_tokens** — vnode 数：默认 256，决定数据在环上的切分粒度。
- **authenticator** — 认证器：AllowAll→Password 的上线第一步。

## 最新演进与工业实践

- **JDK/Python 断代（✅ 官方 5.0 new features 页实抓，doc/latest/cassandra/new/index.html ）**：
  5.0 要求 **JDK 17**（drop JDK8/11）；cqlsh 在 4.0 起改为基于新驱动+Python 3 实现，3.x 的
  旧 cqlsh 与 Python 2.7 双双进博物馆——拿本书脚本在 5.x 跑，先修运行前置。
- **thrift 终局（✅ NEWS.txt 4.0 实抓）**："Starting version 4.0, Thrift is no longer supported"，
  yaml 中 start_rpc/rpc_port 一并移除；若你在 3.x 集群保留了 thrift 端口（本书语境可能默认已关），
  升 4.0 前必须迁完全部 thrift 客户端。
- **官方安装文档迁移**：3.11 文档仍在档（✅ 200），但当前推荐路径变为
  tarball（_/download.html ✅）→ Docker（官方镜像存在，hub.docker.com 本机不可达 ⚠️）→ K8s operator；
  "改 cassandra-env.sh 手调 JVM"在新部署里多数被容器资源限制取代（03/07 章）。
- **工具链现状（✅ api.github.com 实抓）**：apache/cassandra-java-driver 最新 4.19.3；
  pypi `ccm` 3.1.5（2026-04 活跃，见 07 章）——本地"起个测试集群"的正道仍是 ccm 或容器而非手改 yaml。
- 概念对位：驱动/协议代际讨论见
  [../分布式数据库入门进阶与实战/01-什么是分布式数据库与SQL-NoSQL-NewSQL.md](../分布式数据库入门进阶与实战/01-什么是分布式数据库与SQL-NoSQL-NewSQL.md)
  的 NoSQL 生态节。
