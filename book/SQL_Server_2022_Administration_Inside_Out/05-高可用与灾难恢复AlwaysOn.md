# 05 高可用与灾难恢复：Always On（目录版 · 精读重构）

> ⚠️ 主题重构章（取证降级见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第三节）。SQL Server/Windows Failover Cluster 不可本机实测：全章"转述 + ⚠️"，✅ Learn 验真 URL 为准绳；🔧 E3 用本机 SQLite 3.45.3 演示同步持久化代价，标注非本书引擎行为。

## 本章地图

1. HA 与 DR 的词汇表：RTO/RPO/故障转移/仲裁
2. Always On 可用性组（AG）：拓扑、同步模式与角色
3. 故障转移三种姿势与仲裁模型
4. 读写分离、备份卸载与监听器
5. FCI 与日志传送：AG 之外的两件旧兵器
6. Linux 上的 AG 与容器化 HA 边界
7. 🔧 E3：同步提交耐久代价的可测同构

## 一、先把合同签明白：RTO/RPO

- RPO=能丢多少数据（日志链与提交耐久决定下限）；RTO=能停多久（切换自动化与客户端重连决定上限）⚠️。
- HA 解决"本机/本数据中心故障"，DR 解决"整地域失联"——两级方案常异构（同城同步副本+异地异步副本）⚠️。
- 与 04 章衔接：AG 副本靠**日志硬复制**（不是备份文件搬运）喂数据；日志传送（Log Shipping）才是"备份+还原"的穷人版复制 ⚠️。

## 二、AG 拓扑与同步语义

- 官方总览（术语/组件/约束）✅ https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server
- 核心对象 ⚠️ 转述：可用性组（库集合）、可用性副本（每实例一员）、可用性数据库（每库在两副本上的镜像体）、监听器（客户端入口虚拟网络面）。
- 提交语义三态：SYNCHRONOUS_COMMIT（同步提交，RPO=0 前提）/ ASYNCHRONOUS_COMMIT（异步，容忍滞后）/ 配置同步但提交异步的"只同步配置"态（异地常用）⚠️。
- 健康信号：`sys.dm_hadr_availability_replica_states` 等 DMV 族（接 08 章观测线）；SUSPEND/RESUME 是运维刹车，别当故障 ⚠️。
- 库级约束面：AG 内库不可单独离线玩、tempdb 不在组内、登录/作业/链接服务器**不随组复制**（需脚本化同步）⚠️——"切换后登录失效"是第一大经典事故。
- 🔧 **实验 E3（SQLite 3.45.3，非本书引擎行为）**：300 笔单行独立提交，`PRAGMA synchronous=FULL` 耗时 108.6ms vs `NORMAL` 3.7ms（≈29 倍）。FULL≈每次提交 fsync WAL——类比 SQL Server 同步提交副本"本地写日志+等到副本落地才回 ACK"的耐久税；NORMAL≈异步的"先回 ACK 后补耐久"。**同步模式买的是 RPO，付的是提交延迟**——这条曲线在任何 WAL 引擎都成立。仅通用机制演示。

## 三、故障转移与仲裁

- 三种姿势 ⚠️：自动（同步提交+健康+AUTO_FAILOVER_READY 就绪）、手动（计划内切换，维护窗口主力）、强制（`FORCE_FAILOVER_ALLOW_DATA_LOSS`，最后逃生门，可能丢数据+需手工清理）。
- Windows FC 仲裁（Quorum）决定"谁有资格说对方死了"：节点多数+见证（文件共享/云见证）⚠️；仲裁配错=裂脑或"全对变全错"。
- 首填辅助（SEEDING）：AG 初始化用备份还是自动种子（自动种子要求版本兼容+路径约定）⚠️；大库首填是"上线第一天最慢的路"，规划期就要演练（接 04 章还原窗口工程）。
- 灰度升级剧本：双副本先升一台→切换→再升另一台，把 01 章的升级风险折半 ⚠️ 转述。

## 四、读写分离与监听器

- 次要副本可读（SECONDARY_ALLOW_READS）：报表/备份卸载/查询分摊；`APPLICATION_INTENT=READ_ONLY` 连接串路由 ⚠️。
- 备份卸载 ⚠️：把 FULL 备份放到次副本执行是经典红利，但日志备份节奏仍以主副本链为准（细节以产品文档为准 ⚠️）。
- 监听器（Listener）：一个 DNS 名+IP 多端口指向组内路由；客户端层的多子网/负载均衡认知决定连接池参数（连接超时/故障转移伙伴 FailoverPartner）⚠️。
- 路由不完美时的务实解：连接串写死主+应用层重试，比强攻监听器玄学更可运维 ⚠️（观点，非官方口径）。

## 五、FCI 与日志传送：两件旧兵器的适用位

- FCI（故障转移集群实例）：共享盘+实例整体漂移，保护**实例**而非单库；无读副本红利、无库级粒度 ⚠️（共享存储侧依赖 SAN/Storage Spaces Direct 类设施）。
- 日志传送：备份→拷贝→还原的流水线，零许可门槛、分钟级 RPO、切换靠手工脚本 ⚠️；仍是"跨网差、预算零"场景的正当选择。
- 三件套选型速判 ⚠️：AG（库集合+读副本+自动切）＞ FCI（实例级+共享存储）＞ LP（跨地域便宜慢）。

## 六、Linux 与容器的 HA 边界

- AG on Linux： pacemaker 承担资源管控与仲裁代理，`mssql-server-ag2` 资源代理 + 隔离容器化部署的存储红线 ✅ https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-availability-group-overview。
- 容器单副本是常态形态（K8s StatefulSet 卷持久化）；跨 Pod 的 AG 复杂度高，2024–2026 工业实践多让位于"云上托管实例做 HA、本地容器做弹性"的分工 ⚠️ 转述。
- 主机名/证书/网络策略在 Linux 线的三件事与 Windows 线完全不同源，切换脚本要分叉维护 ⚠️。

## 七、与其他章/其他笔记的联系

- 日志链是 AG 的动脉 → [04-备份还原与恢复模型.md](04-备份还原与恢复模型.md)；副本容量与 tempdb 独立 → [02-实例配置与内存TempDB管理.md](02-实例配置与内存TempDB管理.md)、[03-数据库存储与文件组管理.md](03-数据库存储与文件组管理.md)。
- 切换后的告警与观测 → [08-监控排障DMV扩展事件与查询存储.md](08-监控排障DMV扩展事件与查询存储.md)；演练作业化 → [10-自动化作业与混合云运维.md](10-自动化作业与混合云运维.md)。
- 内核口径（日志流与硬复制的 LSN 语义）→ [../SQL_Server_2012_Internals/03-日志与恢复.md](../SQL_Server_2012_Internals/03-日志与恢复.md)。
- 开源同构：MySQL 组复制/InnoDB Cluster 与 PG 流复制+Patroni 的同步/异步与仲裁语义 → [../MySQL运维内参.md](../MySQL运维内参.md)、[../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)（写前 ls 验名通过）。

## 八、常见坑清单（⚠️ 转述整理，非原书条文）

1. **登录/作业不随 AG 迁移**：切换后应用连得上库、进不了门——登录脚本化同步是组建立的第一个附件 ⚠️。
2. **异步副本设了自动故障转移**：配置层面允许但语义上是"拿 RPO 赌 RTO"——自动切要求同步提交，想清再配 ⚠️。
3. **仲裁见证放故障域内**：云见证选在同城同区，区域故障把"裁判"一起带走 ⚠️。
4. **次副本当备库乱写**：读意图连接串没配，报表流量写进主库还抱怨"AG 没卸载效果" ⚠️。
5. **种子网络没预留带宽**：自动种子首次同步打满出口，顺带把 03 章卷预算击穿 ⚠️。
6. **SUSPEND 忘 RESUME**：维护刹车当故障，日志积压后红字一片，恢复先补数据再追链 ⚠️。
7. **DR 演练没含"回切"**：单向切换人人会，回切的数据追平与 DNS 缓存才是事故高发段 ⚠️。

## 九、拓扑速查卡（⚠️ 示意）

| 场景 | 拓扑建议 | RPO/RTO 量级 |
| --- | --- | --- |
| 同城双机房 | 主+同步次×2，仲裁见证第三域 | RPO≈0 / 分钟级自动切 |
| 异地容灾 | 主+异步远次，手动切+预案 | 分钟级 / 小时级 |
| 读卸载 | 同步次允许读+监听器路由 | 不改变可用性档位 |
| 预算零 | 日志传送 | 分钟~小时 / 手工 |

- 判读口诀 ⚠️：同步保数据、异步保距离、仲裁保决策、监听保入口——四样缺一样，方案就不是写下来的那个。

## 十、本章回看自测

- 同步提交到底在"等谁"？🔧E3 给出的方向性结论是什么？（二·E3）
- 自动故障转移三条件？（三）
- 切换后"登录失效"的根因与工程解？（二/八·1）
- AG、FCI、日志传送三选一的两轴判据？（五）
- Linux 线把仲裁交给谁？（六）

## 十一、复现与延伸（可选自修）

- 🔧 复现 E3（SQLite 3.45.3，非本书引擎行为）：同机同表分别 `PRAGMA synchronous=FULL/NORMAL`，各跑 300 笔单行独立提交计时（本机 108.6ms vs 3.7ms）；想再看 RPO 差异可 `kill -9` 进程后重启对比丢没丢尾部事务——"耐久税"与"丢多少"是一枚硬币两面。
- 延伸阅读：日志硬复制的 LSN 语义 [../SQL_Server_2012_Internals/03-日志与恢复.md](../SQL_Server_2012_Internals/03-日志与恢复.md)；Linux AG/pacemaker 官方路线 ✅ availability-group-overview（Linux 线，见第六节 URL）。
- 自修题三则：① 为何异步副本配自动故障转移是语义冲突（→三节）；② 监听器与 FailoverPartner 连接串双保险的故障矩阵推演（→四节）；③ FCI+AG 组合何时值得（观点题，无标准答案，写下判据）。

## 核心概念速览（中英对照）

- **可用性组** — Availability Group (AG)：库集合级复制与切换单元。
- **可用性副本** — Availability Replica：每实例成员身份，主/次两角色。
- **同步提交** — Synchronous Commit：副本落地后才 ACK，RPO=0 的代价曲线（🔧E3）。
- **异步提交** — Asynchronous Commit：低延迟高容忍，故障转移可能丢尾部日志。
- **自动故障转移** — Automatic Failover：仲裁+健康+就绪三条件齐备才动。
- **强制故障转移** — Forced Failover：允许数据损失的逃生门。
- **仲裁/见证** — Quorum/Witness：集群"谁说了算"的投票模型。
- **监听器** — Listener：客户端统一的虚拟网络入口。
- **应用意向路由** — ApplicationIntent：读写分离的连接串开关。
- **自动种子** — Automatic Seeding：AG 初始化免手工备份搬运。
- **FCI** — Failover Cluster Instance：共享存储上的实例级漂移。
- **日志传送** — Log Shipping：备份-拷贝-还原的慢速廉价复制。
- **RPO/RTO** — 恢复点/恢复时间目标：数据损失与停机预算的合同条款。

## 最新演进与工业实践

- AG 能力持续向标准版下沉（基础 AG 两副本）改变了"HA=Enterprise 专属"的预算结构 ✅ 总览页口径 ⚠️ 细节以 editions 页为准。
- Linux/pacemaker 路线使 AG 进入 K8s 周边生态；云上则普遍以 Azure SQL MI/托管实例的自动 HA 替代自建 AG ⚠️ 转述（衔接 [10-自动化作业与混合云运维.md](10-自动化作业与混合云运维.md)）。
- DR 演练自动化：把"强切+回切"写成季度 Runbook 并接入 08 章观测面留痕，是 2024–2026 审计常见要求 ⚠️。
- 同步税的现代缓解：NVMe+同城光纤让 SYNCHRONOUS_COMMIT 的提交延迟降至毫秒级，"RPO=0 不贵"成为同城新基线 ⚠️ 转述（🔧E3 给出方向性直觉，数值不可外推）。
- 开源对照读物：MySQL 半同步复制与 PG 流复制/Patroni 的同步税与仲裁设计 → [../MySQL技术内幕_InnoDB存储引擎2.md](../MySQL技术内幕_InnoDB存储引擎2.md)、[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)、[../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)。
