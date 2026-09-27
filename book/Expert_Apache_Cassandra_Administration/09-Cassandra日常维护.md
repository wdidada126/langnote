# 09 Maintaining Cassandra（日常维护）

> 原书第 9 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。全部为 ⚠️ 文档转述剧本
> （无实机验证），操作语义以 3.x 官方运维文档域为基线。

## 题纲

维护=让 05 章的机制欠账按日程清偿。本章给"例行日/周/季"三级剧本与四类手术
（重启、修复、压实干预、拓扑变更）的 runbook 骨架，并把每一步挂上 10 章的可观测证据。
运维心法：**单节点动作看集群，集群动作看窗口**。

## 1. 例行节律（runbook 目录）

| 频率 | 动作 | 判据/工具 |
|---|---|---|
| 每日 | 磁盘水位、hinted handoff 积压、压缩待压字节 | 10 章指标三件套 |
| 每周 | **repair 轮转**（全环按 range 分组跑完） | nodetool repair，避开业务峰 |
| 每月 | GC 日志/慢读采样复盘、快照演练恢复一次 | 8 章剧本的彩排 |
| 每季 | 版本评估、JVM/GC 策略复审、容量模型更新 | 文末 2026 演进 |
| 事件驱动 | 节点替换/扩容/DC 变更 | 03 章生命周期剧本 |

## 2. 滚动重启标准剧本（⚠️ 转述）

1. 检查集群"现在健康"（status 全 UN、hint 队列空、压缩无积压）——**别在火上浇油**。
2. `nodetool drain`（先让本节点从环上体面退场、停 CQL 端口）→ 停进程。
3. 改配置/换证书/打补丁 → 启动 → 日志确认入环、无意外 stream。
4. 健康检查过 → 下一台。**一次一台、间隔看延迟直方图**；RF=3 时同 DC 连续重启要更慢。
- 禁忌：重启前不 drain（邻居吃一堆超时+hint 风暴）；多节点同刷配置不做金丝雀。

## 3. 修复（repair）运维学（05 章机理的日程化）

- full vs incremental：incremental 只管"自上次修复以来变化"的 range/文件，日常轮转首选；
  大版本/schema 手术后补一次 full（⚠️ 3.x 口径通述）。
- 并发控制：`-par`（range 并行度）与集群 I/O 预算对表；修复风暴=读延迟毛刺经典根因（11 章）。
- 窗口计算：repair 全环耗时必须 < GC grace 与 hint 窗口的最小值，否则"修复追不上腐化"（04/05 章账单）。
- preview 模式：先跑 `nodetool repair -preview` 看分歧面再决定范围（3.x 可用 ⚠️ 通述）。

## 4. 压实干预与 cleanup/升级收尾

- 手动压实：`nodetool compaction -ks app -cf events [--级别 -T 并行]`；
  典型动机=大表长期不触发自动压实、或修复前减文件数。
- `nodetool cleanup`：decommission/改 RF/改环后，**在新持有者上清旧主残留副本**——
  不做=空间无声泄漏（10 章磁盘水位解释来源之一）。
- major 升级后：sstableupgrade（8 章）+ 重启参数核对 + 协议兼容窗口内禁止混版本跑 LWT 新场景 ⚠️ 通述。

## 5. schema 与系统表维护

- 变更后验一致：`nodetool describecluster` 全节点同版本；不一致→找掉队节点重启/重发变更（06 章雷区回环）。
- 环手术：`invalidate_schema` 类工具慎用（属"合法异端"，先走 8 章快照纪律）。
- 系统表巡检清单：`system.size_estimates`（分区大小画像→4 章评审）、`system.repairs`、
  `system_traces`（开了 TRACING 的会话）、`system_distributed.parent_repair_history`。

## 6. OS/硬件层的维护合同（⚠️ 转述）

- 时钟同步（NTP/PTP）：last-write-wins 用时间戳裁决，**时钟漂移=数据损坏的静默形式**；
  这是 Cassandra 对基础设施最硬的要求，没有之一（04 章竞态的根账）。
- 交换区 vm.swappiness、THP 关闭、文件系统（xfs 主流）、NUMA、RAID/队列深度——
  与任意 Java 大堆服务的清单同构，Cassandra 特有的敏感点是**fsync 延迟**（commitlog）与随机读（压缩期）。
- JVM：3.x 书语境 CMS/并行 GC 为主；2026 年口径看文末。

## 7. 维护工单模板（精读重构的"本章交付物"）

`工单={动作, 前置健康证据(10章截图位), 影响面(节点/DC/环), 回滚点(快照/版本), 完成判据(指标回基线)}`
——四类手术（§2/§3/§4/03 章生命周期）各挂一份，评审时互为 diff 对象。

## 8. 维护一页命令卡（⚠️ 转述）

```bash
# 滚动重启单节点循环（§2）
nodetool drain && pkill -f CassandraDaemon
# 改配置/换证书……
bin/cassandra && nodetool status && nodetool proxyhistograms   # 判据回基线再下一台
# 修复日程（§3）
nodetool repair -preview
nodetool repair -full -par 2 -dc dc1           # 参数面按版本文档核对 ⚠️
# 压实与清残（§4）
nodetool compactionstats; nodetool compaction -ks app -cf events -T 2
nodetool cleanup app events                    # 环变更后必做（防空间泄漏）
# 哨兵三连（§5）
nodetool describecluster; nodetool status; nodetool tpstats
```

## 9. 本章十问（自测）

1. 例行节律表中"每日三件"各自预警什么病？（§1）
2. 重启前不 drain 的两个具体后果？（§2）
3. "一次一台"在 RF=3 同 DC 下为何还要更慢？（§2）
4. incremental 与 full repair 的分工窗口？（§3）
5. repair 全环耗时受哪两个上限约束？（§3/05 章）
6. cleanup 不做会造成什么、何时触发需要？（§4）
7. major 升级收尾的两件事？（§4/8 章）
8. schema 分歧的标准处置链？（§5）
9. 为什么时钟漂移被列为"最硬要求"？（§6）
10. 工单模板四元组缺一项会发生什么？（§7）

## 核心概念速览（中英对照）

- **drain** — 优雅下线：先退环再停进程，邻居无感的重启前提。
- **canary restart** — 金丝雀重启：滚动剧本的节点级灰度。
- **repair rotation** — 修复轮转：全环 range 在 GC grace 窗口内跑完一遍的日程。
- **incremental repair** — 增量修复：只比对/修自上次修复以来变化的段。
- **repair -preview** — 修复预演：只报分歧不传输，估工用的望远镜。
- **cleanup** — 清残：环变更后本节点持有的"不再属于我"的数据回收。
- **compaction -fan** — 手动压实：并行度/级别受控的后台重写干预。
- **sstableupgrade** — 格式升级：major 版本收尾的历史文件重写（8 章）。
- **schema agreement** — schema 一致：describecluster 的运维日常哨兵。
- **size_estimates** — 尺寸画像系统表：喂给 4 章分区评审的活数据。
- **clock skew** — 时钟漂移：LWW 语义下的静默数据腐化源。
- **hint backlog** — 提示积压：不可达窗口内写意图的堆积量，健康度一等指标。
- **runbook** — 运维剧本：动作+证据+回滚点+完成判据的四元组。

## 最新演进与工业实践

- **自动修复入列（✅ 5.0 文档树 "Operating / Auto Repair" 专页实抓）**：5.0 起内置
  自动修复调度——本章"每周人工轮转"降级为兜底审查项；修复 I/O 预算仍要人管。
- **UCS（CEP-26，✅ 同页实抓）**：统一压实把 STCS/TWCS/LCS 选型题合并，
  "压实干预"工单量在 5.x 集群显著下降；3.x 存量集群升级 UCS 前需逐表评估历史窗口 ⚠️ 通述。
- **GC 断代**：JDK 8+CMS 剧本随 5.0 的 **JDK 17** 强制令终结（✅ new features 页实抓）；
  2026 年官方与社区口径为 G1 默认、ZGC/Shenandoah 作超低抖动选项 ⚠️ 通述。
- **控制面自动化**：sidecar（apache/cassandra-sidecar ✅ 在档）与 K8s operator 把
  drain/滚动/金丝雀写进控制器，本书手工 runbook 的读者对象从"操作者"变成"审表者"。
- 理论端对照：修复与反熵的成本模型见
  [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)；
  例行节律方法论与关系库 DBA 习惯的差异见 01 章对位迁移表。
