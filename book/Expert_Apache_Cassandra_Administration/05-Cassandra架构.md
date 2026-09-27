# 05 Cassandra Architecture（Cassandra 架构）

> 原书第 5 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。机理转述以 Cassandra 3.x/4.x
> 官方文档为基线（⚠️ 集群不可本机实测）；两处 sqlite3 类比演示为 🔧 实测，**演示的是概念本身，
> 不是 Cassandra 的行为**。

## 题纲

运维手册为什么需要架构章：因为 8/9/10/11 章的每个动作（备份、修复、监控、调优）都在
为这里讲的机制付账。主线：**环与成员（gossip）→ 写路径（commitlog/memtable/hint）→
读路径（bloom/索引/墓碑/读修复）→ 后台整理（compaction/反熵）**。

## 1. 环与成员：谁在哪、谁活着

- 一致性哈希环（Murmur3 分区器默认）：token 区间→副本集合；vnode 让每节点占多段小区间，
  均衡与再分配粒度都靠它。概念对照 [../设计数据密集型应用/06-分区.md](../设计数据密集型应用/06-分区.md)。
- **gossip**：每秒抽样推送状态（心跳带应用状态：加载、generation、DC/rack），
  失败判定用 **phi-accrual 故障探测器**——"节点可疑/死亡"是统计推断，不是心跳超时布尔值；
  这解释了为何"网络抖一下"会触发 hint 与读延迟毛刺 ⚠️ 转述。
- 与 DDCA 09 章互见：Cassandra 用"怀疑+quorum+修复"绕开了共识协议的停机代价。

## 2. 写路径（逐跳，⚠️ 转述）

1. 客户端→协调者（任选）；协调者算出分区→RF 副本集合，本地写 commitlog+memtable。
2. 并行 fan-out 到其余副本；按 CL 收集 ack；不可达副本的写打包成 **hint** 暂存。
3. memtable 满/超时→**刷盘为 SSTable**（append-only，不可变）；commitlog 段按表共享、
   可回收（3.x 的多表共享 commitlog 设计 ⚠️ 通述）。
4. 断电恢复 = 重放 commitlog 重建 memtable——**单节点崩溃零丢写**；
   集群级丢不丢由 CL 与 RF 决定（不是"最终一致"三个字决定的）。

## 3. 读路径与读修复

- 副本选择=**动态快照**（按延迟/错误率打分，非固定优先表）⚠️ 通述。
- 协调者并行：本节点 memtable+SSTable（bloom filter → 分区索引 → 顺序读）；
  远端副本先取 **digest**，不一致才回读全数据（digest 协议省带宽）→ **read repair** 异步/按比例修补分歧。
- 读放大清单：墓碑链、过度宽分区、多表反范式、SASI/2i 散扫（4/11 章回环）。

## 4. 一致性：quorum 演算（🔧 sqlite3 类比实测）

**声明**：用 sqlite3 三个独立库文件模拟三副本表（`D:\develops\tmp\dbwave_cass\r{0,1,2}.db`），
演示"R+W>N 读必见写"与 read-repair 的补写动作；**分片、hint、digest 等 Cassandra 机制不在模拟范围**。

方法：三库各建 `t(k,v,ts)`；模拟 CL=ONE 写仅落副本 0（副本 1/2 当时不可达）；
随后 QUORUM(R=2) 读 {0,1}——脚本输出 `witnesses divergence: {0: ('A',100)}`，
证实**只读到一个版本、且副本间出现分歧**；协调者按"最新时间戳胜出"回写 {1,2} 后三库全等；
再模拟副本下线后的 CL=ALL 写，语句直接 `ProgrammingError` 失败——对应"任一必达副本不可达即写失败"。

结论（可迁移到任意 quorum 系统，⚠️ 非 Cassandra 实测）：
- CL=ONE+R=QUORUM 的分歧能被 read-repair **收敛**，但分歧存在期间其它读方可能读旧；
- ALL/SERIAL 的代价=可用性直接扣减；运维上"CL 不是越严越好，而是与 RF/拓扑/延迟预算联立求解"。

## 5. 反熵：Merkle 树与 repair（🔧 sqlite3 类比实测）

Cassandra 3.x 的修复流程（⚠️ 转述）：副本组对同 token range 各建 Merkle 树
（range 分叶子、逐层哈希），比对根→不同则**下降子树**定位分歧叶子→只流该子范围；
full/incremental/preview 三种模式，`nodetool repair` 全环轮转（每周节奏，9 章）。
Dynamo 论文的 merkle 反熵原型见 [../../paper/doi_10.1145_1294261.1294281/00-精读笔记.md](../../paper/doi_10.1145_1294261.1294281/00-精读笔记.md)；
复制理论端对照 [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)（in-scope repair 一节）。

**🔧 演示**（`D:\develops\tmp\dbwave_cass\m{0,1,2}.db`，非 Cassandra）：三库各 16 行、
切 4 个 range 做叶子摘要，根=叶子拼接再 MD5；对副本 2 删除一行后：
根哈希 `dd6d33269c7f / dd6d33269c7f / 6a4efab7d4bc` → 检测到分歧；
逐叶子比对**只命中 range(13,16)**（副本 2 该段 3 行 vs 其它 4 行），其余三段免传输——
这就是"repair 流量正比分歧而非正比数据量"的算术本质。

运维推论（书内语境）：range 切得越细定位越准但比对越贵（3.x 后期引入 merkle depth 参数
`repair_session_max_tree_depth` 控制树深 ⚠️ NEWS 语境）；大分区+长 TTL 会让修复窗口失控。

## 6. Compaction 三兄弟（机理归本章，选型归 09/11 章）

- **STCS**：大小分层，写友好、读放大随层数涨——默认通用。
- **LCS**： leveled，读友好、写放大高——点查 SLA 紧的表。
- **TWCS**：时间窗分层，治时序数据"跨代混压+过期数据常驻"——3.x 时代时序表标配（⚠️ 通述，
  引入 minor 版本细节不可实证）。
- 压缩的运维账单：磁盘放大（双份空间）、I/O 限流（`compaction_throughput`）、
  大分区=长压缩（`nodetool compactionstats`，10 章）。

## 7. SSTable 解剖（备份/工具章的前置，8 章回环）

- 文件族（3.x）：`-Data / -Index / -Summary / -Statistics / -CompressionInfo / -TOC`；
  分区索引稀疏化（index interval），bloom filter 序列化存 Data 内 ⚠️ 通述。
- 不可变性决定一切：更新=新 timeuuid 版本插入，旧值靠压缩+GC grace 清理。
- 由此得三条运维铁律：直接改数据目录=异端（修复要用 sstable 工具族，8 章）；
  快照天然一致（hard link，8 章）；压缩策略改动不影响已存文件、只影响未来产出。

## 8. 路径侦察命令卡（⚠️ 转述）

```bash
nodetool ring / gossipinfo              # 环与成员视图
nodetool tpstats                        # 写读/repair/hint 各池 pending
nodetool compactionstats                # 压实队列与进度
nodetool netstats                       # stream/hint 流动
nodetool cfstats app.events             # 表级读写/墓碑/缓存计数
nodetool snapshot -ks app               # 动任何"异端"手术前的保险（8 章）
nodetool repair -preview                # 分歧面预演（9 章日程的探针）
# CQL 侧：SELECT * FROM system.size_estimates;  SELECT * FROM system_distributed.parent_repair_history;
```

## 9. 本章十问（自测）

1. phi-accrual 与"心跳超时判死"的语义差及其运维后果？（§1）
2. 写路径中"本地即算成功的前半"由什么持久化保证？边界在哪？（§2）
3. hint 窗口默认多长？超窗的准确损失是什么（对照速览条目）？（§2）
4. digest 读省什么、read repair 三种触发各是什么？（§3）
5. 🔧 quorum 演示里，CL=ONE 写+QUORUM 读暴露了什么、又收敛于什么？（§4）
6. "ALL/SERIAL 的代价=可用性直接扣减"在演示中如何体现？（§4）
7. merkle 演示里为何修复流量正比分歧而非数据量？（§5）
8. range 切细的收益与代价、3.x 后期控树深的参数名？（§5）
9. STCS/LCS/TWCS 各自的账单倾向与适用表画像？（§6）
10. SSTable 不可变性推出的三条运维铁律？（§7）

## 核心概念速览（中英对照）

- **consistent hashing ring** — 一致性哈希环：token 空间到副本的映射底座。
- **gossip** — 流言协议：去中心化成员/状态传播，秒级抽样推送。
- **phi-accrual failure detector** —  phi 故障探测：以统计怀疑代替定时判死。
- **dynamic snapshot** — 动态快照读：按延迟/错误率实时选择副本读集。
- **digest read** — 摘要读：先比哈希再回读全文，省带宽的副本核对。
- **read repair** — 读修复：读路径顺手（或后台）收敛分歧副本。
- **Merkle tree** — 默克尔树：range 分叶逐层哈希，反熵定位分歧的索引结构。
- **anti-entropy repair** — 反熵修复：比对 Merkle 树后仅流分歧子树。
- **hinted handoff window** — 提示窗口：默认 3h；超窗则未达副本永久缺写，只能靠 repair 从存活副本补回（低 CL 下连存活副本数都可能跌破 RF）。
- **commitlog segment** — 提交日志段：多表共享、可回收的本地持久化单元。
- **memtable flush** — 刷盘：内存表冻结为不可变 SSTable 的转换点。
- **SSTable** — 排序字符串表：append-only 不可变文件族（Data/Index/Summary/…）。
- **bloom filter** — 布隆过滤器：SSTable 级"肯定不存在"快答，fp 率可调。
- **STCS/LCS/TWCS** — 三种压实：通用/读优先/时序优先的后台重写策略。
- **GC grace** — 墓碑宽限期：repair/hint 收敛窗的安全垫。

## 最新演进与工业实践

- **5.0 换血三件（✅ 官方 new features 页实抓）**：**trie memtable（CEP-19）** 与
  **trie SSTable（CEP-25）** 把跳表+稀疏索引换成trie 结构（大分区扫描与内存占用显著改善 ⚠️ 效果
  以官方口径转述），**UCS（CEP-26）**统一压实——本章"三兄弟选型题"在 2026 年变成默认题。
- **thrift 之死与协议演进**：4.0 移除 thrift（✅ NEWS.txt）；原生协议 v5/实验 v6、
  cqlsh 重写（4.0+）使"架构图上的客户端层"整层翻新 ⚠️ 版本细节按官方文档口径。
- **repair 自动化**：5.0 文档树出现 Auto Repair 运维页（✅ 导航实抓），merkle 比对从
  "DBA 周历"变成守护任务；sqlite3 演示（🔧）只证明算法本质，不证明 Cassandra 实现。
- **理论坐标**：本机制组（quorum/反熵/不可变 SSTable+LSM）与
  [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md) 的 LSM 章、
  [../分布式数据库入门进阶与实战/07-存储引擎基础与LSM型Key-Value存储.md](../分布式数据库入门进阶与实战/07-存储引擎基础与LSM型Key-Value存储.md)
  互为印证；Dynamo 论文线经 [../../db/db.md](../../db/db.md) 索引可达。
