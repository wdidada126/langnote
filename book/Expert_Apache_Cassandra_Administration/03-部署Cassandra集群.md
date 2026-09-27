# 03 Deploying a Cassandra Cluster（部署 Cassandra 集群）

> 原书第 3 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。集群行为无法本机实测，
> 全章 ⚠️ 文档转述（基线：Cassandra 3.x 官方运维文档 + 本书语境）。

## 题纲

从单机到生产集群的部署剧本：拓扑设计（节点数/RF/DC/rack）、seed 与 gossip 的 bootstrap 仪式、
snitch 选型、端口与防火墙矩阵、多 DC 的 NetworkTopologyStrategy，以及"加减换节点"的
生命周期三件套（bootstrap / decommission / replace）。本章的运维心法：**拓扑是一次性决定，
代价要用多年偿还**。

## 1. 拓扑设计清单（动手前先回答的六个问题）

1. 节点总数与复制因子：最小可用生产形态 RF=3（跨 3 台机器/3 个可用区）；RF=2 仅容忍单失。
2. DC 布局：几个 DC、每个 DC 的 RF 各是多少（3.9 前的"全局 RF"写法与
   `remote_nodes_first` 一类参数已不可靠 ⚠️ 通述）→ 直接 NetworkTopologyStrategy 每 DC 独立。
3. rack/可用区：同 DC 内跨 rack 分散（配合 snitch 身份文件，02 章）。
4. 种子节点：每 DC 2~3 个固定 seed；seed 只管 bootstrap/汇合，不是"主"。
5. 单机数据量预算：磁盘 × 压缩率 × RF，留 compaction 双倍空间（11 章）。
6. 版本与升级窗口：major 升级需 sstableupgrade（8 章）→ 部署时即写好版本基线。

## 2. Bootstrap 仪式（⚠️ 转述）

- 首节点：`auto_bootstrap=false`（或新集群无 seed 互指）；启动后 `nodetool ring` 成环。
- 后续节点：配好同 `cluster_name` + 指向 seed → 启动即自动：gossip 会合 → 认领 token
  （vnodes 默认 256 个随机 token ⚠️ 通述）→ 从相邻 replica **stream** 所属数据 → 进入正常服务。
- 进度观察：`nodetool netstats`（streaming 进度）、system.log 的 bootstrap 序列。
- 禁忌：别让两个节点同时 bootstrap 同一批 token 的大流量（先加一个、流完再加下一个）；
  手工 `initial_token` 仅限非 vnode 古董集群。

## 3. Snitch：让集群认识"位置"

| Snitch | 用途 | 运维注记 |
|---|---|---|
| SimpleSnitch | 单机/试用 | 多 DC 禁用 |
| PropertyFileSnitch | 静态文件映射 IP→DC/rack | 云环境 IP 漂移即失效 |
| **GossipingPropertyFileSnitch** | 本机身份来自 rackdc.properties，其余 gossip 传播 | 生产默认推荐 |
| EC2Snitch/ECSnitch | 云区域自动识别 | 跨账号/VPC 需改 API（略） |
| CloudnativeSnitch | K8s 语境后起 ⚠️ | 4.x 时代普及，非本书内容 |

- snitch 决定"就近读写"的路由语义，与 CL 里的 LOCAL_* 家族（LOCAL_QUORUM/LOCAL_ONE）联动；
  选错 snitch = LOCAL_QUORUM 语义错位，是"写了没读到"类玄学工单的头号根因 ⚠️ 转述。

## 4. 端口与防火墙矩阵（3.x）

| 端口 | 用途 | 暴露面 |
|---|---|---|
| 7000/7001 | 节点间（TLS） | 仅集群内/DC 间专线 |
| 7199 | JMX | 仅运维网段 |
| 9042 | CQL 原生 | 客户端 |
| 9160 | thrift | 3.0 起默认关（NEWS ✅），规划上视为已死 |

- 节点间加密（internode_encryption all/dc/rack）在 12 章展开；部署期就定好，后补证书 = 全集群滚动重启。

## 5. 多 DC 部署（本书"expert"成色的第一处）

- 每 DC 独立 RF：`{'class':'NetworkTopologyStrategy','dc1':3,'dc2':3}`；DC 内跨 rack 天然均衡。
- 写语义：`EACH_QUORUM`（跨 DC 全数确认，慢但零数据丢失窗口）vs `QUORUM`（全局过半，
  DC 隔离性差）vs 应用层"本 DC 写+异步读修"——理论框架见
  [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)、
  [../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md](../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md)。
- DC 间带宽预算：修复流量、hint 重放、（如启用）跨 DC 读 repair 都走这条线——上线前压测它。
- 双 DC 升三 DC、单 DC 拆双 DC：加 DC 后对新 DC 逐节点 `nodetool rebuild`（⚠️ 转述，
  与 decommission 区别见 9 章剧本）。

## 6. 节点生命周期剧本（与 09 章维护互引）

- **加**：bootstrap（本节 2）。
- **减**：`nodetool decommission` → 数据回流环上其余 replica；全程观察 netstats；
  前提：RF 足够，减完不跌破 RF 安全线。
- **换**（机器死透）：新机 `replace_address/replace_node` + `auto_bootstrap=false` →
  只接管原节点的 token/数据，**不从全网重流**；死节点 decommission 不回来时这是唯一正解 ⚠️ 转述。
- **缩容顺序纪律**：先 decommission 腾节点，再缩 RF（改复制策略是 schema 级动作，不是运维脚本）。

## 7. 部署验收单（精读重构的"本章小结"）

1. `nodetool status` 全 UN、每 DC 的 L（负载）方差 < 10%。
2. `nodetool describecluster`：schema 版本一致（不一致先跑 `nodetool describecluster`+修复流程，9 章）。
3. 从每个 rack 各发起 QUORUM 读写实测（⚠️ 转述：本目录未实机执行）。
4. 重启任一节点，观察其以原 token 重新入环、无意外全量 stream。
5. seed 清单文档化：未来三年所有部署脚本都要引用它。

## 8. 部署侦察命令卡（⚠️ 转述）

```bash
# 环与成员
nodetool status / ring / describecluster        # 成员、环、schema 一致
grep -E 'seeds|num_tokens|cluster_name' conf/cassandra.yaml
cat conf/cassandra-rackdc.properties            # dc=dc1 rack=r1 + prefer_local
# 拓扑验收
nodetool netstats                               # bootstrap 流进度
nodetool rebuild -- dc2_seed_ip                 # 加 DC 后逐节点回灌（⚠️ 语法按文档）
# 生命周期剧本纸面推演（ccm 可做，见 07 章）
nodetool drain                                  # 重启前
nodetool decommission                           # 退役
nodetool replace_address /tmp/dead_node_token   # 顶替流程的 token 导出（若死节点还能启动）
# replace 参数写进新机配置后启动；auto_bootstrap=false 先行（语法细节 ⚠️ 以文档为准）
```

## 9. 本章十问（自测）

1. 拓扑设计六问里，磁盘预算为什么要乘 RF 再加压缩余量？（§1）
2. RF=2 与 RF=3 的"容灾差"具体差在哪一维？（§1）
3. seed 节点的准确职责是什么、常见误解是什么？（§2/速览）
4. bootstrap 的三步仪式与两个观察窗？（§2）
5. GossipingPropertyFileSnitch 相比 PropertyFileSnitch 的运维优势？（§3）
6. LOCAL_QUORUM 语义与 snitch 的耦合关系？（§3）
7. 7000/7199/9042 各自的暴露面结论？（§4）
8. EACH_QUORUM 与 QUORUM 在 DC 失联时的行为差异？（§5）
9. decommission 与 replace 的适用前提分界？（§6）
10. 部署验收单第 3 条为什么要"从每个 rack 各发一次"？（§7）

## 核心概念速览（中英对照）

- **bootstrap** — 引导入环：新节点 gossip 会合→认领 token→流式补齐数据。
- **decommission** — 退役下线：把节点数据流回环上其余副本再离场。
- **replace_node** — 顶替复活：新硬件接管死亡节点的 token，不触发全网重流。
- **seed node** — 种子节点：gossip 汇合入口，非主从语义中的"主"。
- **snitch** — 位置感知器：把 IP 翻译成 DC/rack，驱动就近路由与 LOCAL_* CL。
- **GossipingPropertyFileSnitch** — 生产首选 snitch：本机身份文件+全局 gossip 传播。
- **NetworkTopologyStrategy** — 拓扑复制策略：按 DC 独立设 RF，多 DC 的唯一正解。
- **EACH_QUORUM** — 每 DC 法定数：跨 DC 强确认写，代价是延迟与 DC 耦合。
- **streaming** — 流式传输：bootstrap/decommission/repair 的数据搬运机制。
- **netstats** — 网络状态视图：stream/提示/迁移进度的观察窗。
- **ring** — 令牌环：一致性哈希下全集群的 token 分布图。
- **rack awareness** — 机架感知：副本跨 rack 分散，单 rack 故障不丢多数派。
- **schema agreement** — schema 一致：describecluster 的必验项，不一致是事故引信。

## 最新演进与工业实践

- **5.0 部署形态（✅ 官方文档导航实抓）**：官方文档树已有 Docker 与 K8s 专题入口、
  sidecar 项目 apache/cassandra-sidecar 在档（api.github.com 200 ✅）——2026 年新建集群的主流是
  K8s+operator（如 datastax/cass-operator，⚠️ 仓活跃度存疑），本书"手改 yaml+systemd"剧本
  的留存价值在存量裸机集群与升级考试。
- **vnodes 已是唯一叙事**：单 token 手工分配（initial_token）在 4.x+ 文档里只作兼容注脚；
  5.0 的自动均衡（load balancing）方向使"加减节点的流控"进一步交给策略而非人工 ⚠️ 趋势转述。
- **thrift 端口从规划中消失**：4.0 彻底移除（✅ NEWS.txt）；2.x 时代"9160 暴露内网"的旧脚本
  是升级 4.0 的必删项。
- **多 DC 语义的新底座**：5.0 的 UCS/自动修复（Auto Repair，✅ 官方文档导航在档）把本章"修复流量
  预算"从人肉日程变成策略对象；概念对照仍回
  [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md) 的 leaderless 复制节。
