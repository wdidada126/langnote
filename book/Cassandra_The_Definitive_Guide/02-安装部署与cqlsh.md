# 02 安装部署与 cqlsh（原书"Basic Cassandra Operations"口径 ⚠️ 推定重构）

> 精读重构（非原书文本）。本章全部命令为 **2.x 文档口径转述，⚠️ 未实测**（共通纪律：Cassandra
> 不装不跑）；3.x 同题的运维化展开在姊妹册 #89（链接见文末）。

## 2.1 题纲

1. 运行前提：JDK（2.x 时代 JDK 7/8）、内存与磁盘布局经验值
2. 发行形态：tarball 解压即装；包管理/云镜像非主流
3. 配置三件套：`cassandra.yaml`、`cassandra-rackdc.properties`、`cassandra-env.sh`/`jvm.options`
4. 目录布局：data/、commitlog/、saved_caches/、hints/、cassandra.log/system.log
5. 单节点启动与 `nodetool info/statusring`；`cqlsh` 的进入与退出
6. 最小多节点：seeds 的作用与误解、`listen/broadcast/rpc` 地址族、SNITCH 先默认后改
7. 第一次 CQL：keyspace→表→插入→按分区键查询（与 05 章建模衔接）
8. 运维边界：书中"装完能跑"≠"能上生产"，生产拓扑归 #89 册 03 章

## 2.2 安装与配置骨架（⚠️ 2.x 口径）

```bash
# 典型 2.x 流程（转述自官方安装文档，未实测）：
tar xzf apache-cassandra-2.2.x-bin.tar.gz && cd apache-cassandra-2.2.x
# 目录权限：log/data/commitlog 指向独立盘
bin/cassandra            # 后台启动，log/cassandra.log 看引导日志
bin/nodetool info        # 单节点自检：ID/generation/uptime
bin/nodetool statusring  # 或 nodetool ring（token 环视图）
bin/cqlsh 127.0.0.1 9042 # CQL 原生协议端口（非旧 thrift 的 9160）
```

`cassandra.yaml` 的最小必改集（书中口径 ⚠️）：

- `cluster_name`、`num_tokens`（默认 256=vnode 时代开关）、`data_file_directories`、
  `commitlog_directory`、`saved_caches_directory`
- `seed_provider`（`SimpleSeedProvider`，seeds 只是"新节点问路的第一站"，**不是主节点**——高频误解）
- `listen_address`（节点间通信）、`broadcast_address`（云/NAT 后）、`rpc_address`/`storage_port`(7000)
- `partitioner`（默认 `Murmur3Partitioner`，2.x 后期建议弃 Random+单 token 手排）

`cassandra-env.sh`/`jvm.options`：堆大小 `MAX_HEAP_SIZE`（社区经验 ≤8–16G，书中时代更保守）、
`HEAP_NEWSIZE`、G1/CMS 手调——这些"JVM 手工技艺"在 2026 已被官方文档淡化但仍是 GC 排障基本功 ⚠️。

## 2.3 cqlsh 与第一批对象

```sql
-- cqlsh 交互（2.x 口径）
CREATE KEYSPACE demo WITH replication =
  {'class':'NetworkTopologyStrategy','DC1':3};
USE demo;
CREATE TABLE users (id uuid PRIMARY KEY, name text, email text);
INSERT INTO users (id, name, email) VALUES (now(), 'carpenter', 'j@c.q');
SELECT * FROM users WHERE id = <那个uuid>;      -- 必须带分区键（对照 04/05 章）
UPDATE users SET name='Carpenter J.' WHERE id = ...;
DELETE FROM users WHERE id = ...;               -- 产生墓碑，对照 06 章
COPY users TO 'users.csv'; COPY users FROM 'users.csv';  -- cqlsh 内置导入导出
TRUNCATE users;                                  -- 比批量 DELETE 干净得多
```

cqlsh 要点：`COPY` 是客户端逐行工具（慢、单表、适合小数据），大批量装载书中口径走 sstableloader
或后来的 Spark bulk ⚠️（运维侧详见 #89 册 08 章）。`DESCRIBE` 族命令是读"表真实分布"的显微镜：
`DESCRIBE TABLE` 会暴露 partition/cluster key 结构，建模期高频使用（05 章回环）。

## 2.4 多节点最小集群与"seeds 三原则"

书中反复出现的拓扑练习：两台虚拟机改 `broadcast_address` + 相同 seeds 启动，`nodetool ring`
看到两段 token 即成环。社区沉淀的 seed 运维原则（⚠️ 转述）：

1. seeds 列表要长期稳定，节点重启时靠 seeds 完成"问路"加入 gossip；
2. 每个机架保留 1 个 seed，别把所有节点都写成 seed；
3. 节点全部冷启动（如新集群）时所有节点都需要 seed——按此逻辑选 3 个持久化写死。

snitch 从默认 `SimpleSnitch` 改 `PropertyFileSnitch`/`EC2Snitch` 必须**滚动逐个改**，否则
副本放置会在中途漂移——这是书中"安装章"给运维埋下的第一个坑 ⚠️（对照 #89 册 03 章的 DC 部署纵深）。

## 2.5 版本/端口的时代错位提醒（2026 读法）

- 书中 `rpc_address`/`start_rpc`（thrift 9160）语境已整体作废：4.0 起 thrift 移除（✅
  https://raw.githubusercontent.com/apache/cassandra/cassandra-4.0/NEWS.txt ）；9042 native 端口独存。
- 2.x 的 `conf/cassandra.yaml` 大量键在 4.x/5.x 迁移或改名（如 compaction/throttle 族）；
  5.0 起 JDK 17 基线（✅ https://cassandra.apache.org/doc/latest/cassandra/new/index.html 内 "JDK 17" 行）。
- 现代部署首选容器/operator（#89 册 07 章与 00 生态行口径）；本章的 tarball 流程只剩"理解
  配置文件出身"的教学价值。

## 2.6 本章在全目录中的挂点

- 装完就建模 → [05-数据建模](05-数据建模.md)；语法细节 → [04-CQL查询语言](04-CQL查询语言.md)
- 配置项逐个深水区 → [10-配置与集群运维](10-配置与集群运维.md)
- 管理员向同题 → [../Expert_Apache_Cassandra_Administration/02-安装Cassandra与CQL_Shell入门.md](../Expert_Apache_Cassandra_Administration/02-安装Cassandra与CQL_Shell入门.md)、[03-部署Cassandra集群](../Expert_Apache_Cassandra_Administration/03-部署Cassandra集群.md)
- 0.7 时代安装史（thrift 原生形态）→ [../cassandra实战.md](../cassandra实战.md)

## 核心概念速览（中英对照）

- **tarball 部署** — Tarball install：解压即用的发布形态，配置全在 conf/ 目录。
- **cassandra.yaml** — cassandra.yaml：集群行为主配置文件，书中时代改动即重启生效。
- **seeds** — Seed nodes：新节点加入 gossip 的问路点，非协调主非仲裁集合。
- **native transport** — Native transport：9042 端口 CQL 二进制协议，与 thrift(9160) 并存于 2.x。
- **cqlsh** — cqlsh：内置 Python 客户端，带 COPY/DESCRIBE/TRACING 等运维小抄。
- **COPY TO/FROM** — cqlsh COPY：客户端逐行 CSV 导入导出，小数据集工具而非装载器。
- **nodetool** — nodetool：JMX 驱动的集群瑞士军刀（info/status/ring/repair/flush...）。
- **token ring** — Token ring：一致性哈希环的可视输出，`nodetool ring`/`statusring`。
- **broadcast_address** — Broadcast address：对外宣告地址，NAT/云环境的解耦开关。
- **snitch** — Snitch：拓扑感知插件，决定"离我近的副本"如何定义。
- **Murmur3Partitioner** — Murmur3 partitioner：2.x 默认分区器，token 均匀性更好 ⚠️。
- **saved caches** — Key/row cache：加速读的热度缓存文件，重启会重新预热。
- **commitlog 目录** — Commit log directory：预写日志落盘位置，独立盘是书中铁律 ⚠️。

## 最新演进与工业实践

（除注明外均本会话 curl 实抓 ✅；集群仍 ⚠️ 不实测）

- **启动形态**：5.0 起 JDK 17 为基（4.0 曾支持 Java 11）——`cassandra-env.sh` 手调堆时代结束，
  容器环境以 `jvm-server.options`+内存限额为主。源：
  https://cassandra.apache.org/doc/latest/cassandra/new/index.html 、
  https://cassandra.apache.org/doc/4.0/cassandra/new/index.html
- **配置面翻新**：4.0 引入大量虚拟表（virtual tables）用于内省；5.0 有 `system_views` 日志虚表
  与 guardrails 更多护栏项——"装完看一眼"从翻日志变成查 `SELECT * FROM system_views.xxx`。
- **cqlsh 换血**：4.0 起 cqlsh 基于新官方 Python 驱动重写（书内 2.x cqlsh 的输出格式/命令细节 ⚠️ 作废）。
- **装载工具链**：`sstableloader` 仍在（5.0 文档 Managing/Bulk loading 小节）；大装载主路径
  变为 Spark connector 与云侧批量导入（对照 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md) 的数据接入世界观）。
- **发行现状**：5.0.9 GA（2026-08-07）；6.0 文档站已可浏览但标预发布 ⚠️——安装页 URL 请以官方
  下载页为入口：https://cassandra.apache.org/_/download.html
- **工业实践**：新建集群走 K8s operator/sidecar（apache/cassandra-sidecar）已成默认路径 ⚠️ 转述
  （存在性经 #89 册 api.github.com 核验），裸 tarball 仅存教学与升级演练价值。
