# 09 高可用、集群与 Oracle 产品版图（⚠️ 推定重构章 · 对应原书"HA/Clusters/Products"主题域）

> 章名与章号为 ⚠️ 主题重构（[00 §二降级声明](00-总览与阅读地图.md)）。本章是导游册的收官格：RAC、Data Guard、可用性家族，以及"版本与产品版图"总览。Oracle 侧一律 ⚠️ 转述；🔧 为 SQLite/DuckDB 实测，非 Oracle——**尤其不是 RAC**。

## 1. 可用性的两种灾难语义（⚠️ 转述）

- 单实例故障=可用性问题：实例没了、数据还在（[02 章](02-物理存储结构与表空间.md) 文件面）——重启+SMON 实例恢复即可 ⚠️（🔧 T15 给了最小可测版本）。
- 存储/站点故障=可用性+数据双问题：需要**另一份数据副本**——Data Guard 的立场 ⚠️；RAC 的立场不同：换的是**计算**不是数据（共享存储仍在）。
- 导游册的一句话地图：RAC=扩展性+计算冗余；Data Guard=站点级冗余；备份恢复（[06 章](06-服务器工具与实用程序.md)）=最后防线；三者回答三个不同问题——混用是选型事故之源 ⚠️。

## 2. RAC：一个数据库多个实例（⚠️ 转述）

- 形态：多主机实例挂载**同一**数据库文件（共享存储/ASM），节点间高速互联（interconnect）跑缓存融合（cache fusion）——块的全局一致性由 GCS/GES 协议族协调 ⚠️（术语级转述，深论留给 #74 主题域，登记不链）。
- 集群栈：Clusterware（节点成员/资源编排/故障漂移）+ SCAN（客户端接入抽象，[04 章](04-网络连接与服务器进程.md) 已见）+ 服务（service）为迁移单元 ⚠️。
- 代价清单（导游册必给 ⚠️）：许可/运维复杂度/互联敏感/热点块争用（seq 块 ITL 链）——"先优化单实例再谈 RAC"是社区老话 ⚠️。
- 🔧 T4c 反衬（非 Oracle、非 RAC）：SQLite 的多进程读写=文件锁协作（🔧 实测第二写者 `database is locked`）；DuckDB 无跨进程共享形态——"共享磁盘多计算体"在本机开源栈**没有可测对应物**，这个"测不到"本身就是 RAC 复杂性的注脚：块级一致性协议是专有工程重资产 ⚠️。

## 2b. RAC 故障域推演（⚠️ 转述；导游册"代价清单"的展开版）

- 节点死亡：该机上的实例崩溃恢复由存活节点的 SMON/实例恢复线接管，服务经 Clusterware 漂移重连 ⚠️——用户感知=会话重连，不是数据丢失。
- 互联抖动：缓存融合协议对延迟敏感，私网质量差时全局块转换排队，表现为"gc" 类等待 ⚠️（等待事件命名以官方为准）——诊断面在 [TOP/02](../Troubleshooting_Oracle_Performance_2e/02-关键概念.md) 语境之外，登记给 #74 主题域（只登记）。
- 存储故障：共享磁盘是全组单点——这正是 RAC 与 Data Guard 互补而非互斥的几何证明 ⚠️（[02 章](02-物理存储结构与表空间.md) 文件面的最坏情形）。
- 推演结论：RAC 换掉的是"计算单点"，换不掉"数据单点"；把它当灾备卖是成书年代就存在的误读 ⚠️。

## 3. Data Guard 与恢复家族（⚠️ 转述）

- 主库→备库管道=redo 传输+应用：物理备库（块级重放，可读 ⚠️ 随版本放开）/逻辑备库（SQL 级重放）⚠️。
- 角色动作：switchover（计划内互换）vs failover（故障接管，含丢失量抉择）；FSFO/观察者仲裁 ⚠️；快照备库（测试复用）⚠️。
- RPO/RTO 二轴：同步/异步传输档位定 RPO，切换自动化程度定 RTO——"0 丢失与 0 停机不可兼得"的三角 ⚠️。
- 🔧 **T14 · 只读备库类比**（非 Oracle）：`file:...?mode=ro` URI 实测读成功（2 行）、写入被拒（`attempt to write a readonly database`）——"可查询的副本+写去主"的最小肌肉记忆；真备库的 redo 应用管线在此不可见 ⚠️。
- 🔧 **T15 · 崩溃恢复类比**（非 Oracle）：子进程事务中途 `os._exit(9)` → 实测热日志驻留（hot journal left: True）→ 主连接重开只读到已提交 1 行、未提交分支被回滚（journal cleaned: False，留待下一写者清理）——"恢复者惰性开工"：Oracle 侧 SMON 开机前滚+回滚的自动线 ⚠️ 与之同一性原理、不同工业化程度。

## 3b. 🔧 T14/T15 最小复现代码（非 Oracle、非备库；机制/错误码/布尔=本次实测，行数随示例库装载微调——原实验 G6 已提交为 1 行，此处复用 T14 库故见 2 行）

```python
import sqlite3, subprocess, sys, os
# —— T14：只读"备库"（真备库的 redo 管线不在此）——
main = sqlite3.connect("m.db")
main.execute("CREATE TABLE t(x)"); main.execute("INSERT INTO t VALUES(1),(2)")
rep = sqlite3.connect("file:m.db?mode=ro", uri=True)
rep.execute("SELECT count(*) FROM t").fetchone()   # 🔧 (2,) 读成功
rep.execute("INSERT INTO t VALUES(9)")             # 🔧 OperationalError:
#   attempt to write a readonly database —— "副本可读、写回主库"的最小肌肉记忆
# —— T15：崩溃留热日志 ——
child = "import sqlite3;s=sqlite3.connect('m.db');s.execute('BEGIN');" \
        "s.execute('INSERT INTO t VALUES(99)');import os;os._exit(9)"
subprocess.run([sys.executable, "-c", child])      # 🔧 事务未提交即硬死
os.path.exists("m.db-journal")                     # 🔧 True（热日志驻留）
recovery = sqlite3.connect("m.db")
recovery.execute("SELECT count(*) FROM t").fetchone()  # 🔧 (2,)：99 不在——未提交分支被回滚
os.path.exists("m.db-journal")                     # 🔧 True（cleaned: False，
#   未清理——留待下一写者，"恢复者惰性开工"的实测语义）
```

- 三条边界声明：① 🔧 的"回滚"发生在文件层 journal 重放，Oracle ⚠️ 是 undo 段+SMON，机制不同族；② 没有"第二份数据"——ro URI 读的是同一个文件，与备库的独立副本本质不同；③ 崩溃点不可控（os._exit 跳过所有清理），恰是"恢复正确性"最恶劣考场。

## 4. 复制与消息类增量（导游册点名制 ⚠️ 转述）

- Streams/GoldenGate 定位差：库内捕获 vs 异构日志集成 ⚠️；成书年代正是 Streams→GG 叙事更替期。
- 本目录立场：复制话题的现代延长线在系列内由分布式各册承接（总索引登记）；本章只保留"日志集成=redo 语义的出口"这一概念钩 ⚠️。

## 5. 版本与产品版图（⚠️ 转述；条款以官方现行口径为准）

- 版本阶梯（XE/SE/SE2/EE）⚠️：容量/特性闸门的商业骨架；选项制（RAC/DG 压缩分区等挂 EE）⚠️——导游册的"特性清单"实为**采购地图**。
- 工具版图收口（[06 章](06-服务器工具与实用程序.md) 之外）：EM/Cloud Control→企业舰队；APEX→应用层；BI 族（Answer/Discoverer 类史词 ⚠️）→分析层；应用服务器/开发工具谱系一句话点名 ⚠️。
- 多租户预告（12c）：CDB/PDB=把"库"变成容器内租户 ⚠️——若本书止于 11g/12c 之交，此处正是其版图的天然断点；后续由 19c/23ai 册（在盘 [23ai 管理册](../Pro_Oracle_23ai_Administration/00-总览与阅读地图.md)）接棒。

## 5b. 版图速查小表（⚠️ 转述；"特性→章节"反向索引）

| 特性词 | 住哪个版本层（⚠️ 以官方为准） | 本目录归置 |
|---|---|---|
| RAC/Data Guard | EE 选件叙事 ⚠️ | 本章 §2/§3 |
| 分区/压缩/并行 | 曾 EE 独占，后部分下沉 ⚠️ | [08 章](08-仓库实施分区物化视图与装载.md)/[07 章](07-数据仓库基础与体系结构.md) |
| 多租户 CDB/PDB | 12c+ 独立选件 ⚠️ | 本章 §5+23ai 册 |
| XE 容量闸门 | 免费/学习层 ⚠️ | [00 章](00-总览与阅读地图.md) 版本基线对表 |

- 读法：这张表是导游册"采购地图"论断的压缩件——**每一行都可能随官方条款移动**，所以只给词、不给定价。

## 6. 自测（能复述=过关）

1. RAC/DG/备份三件套各回答什么问题？各换掉什么（计算/站点/副本时点）？
2. cache fusion 为什么让 RAC 与"应用层分库"不可互换？（⚠️ 术语级即可）
3. switchover vs failover 的决策轴？同步传输定住哪个轴？
4. 🔧 T14 类比的三个失真点（redo 管线/角色仲裁/丢失量）？
5. 🔧 T15 里"journal cleaned: False"说明恢复者什么性格？映射 SMON 哪条线（⚠️）？
6. 版本阶梯为什么"既是技术表又是采购表"？给一个导游册会点名的特性闸门例（⚠️）。
7. §2b 推演：互联抖动为何会伪装成"数据库慢"？该先看哪一层证据（⚠️ 等待语义级）？
8. 🔧 3b 边界声明②：为什么"同一文件 ro 打开"在概念上甚至不如"独立文件+手工同步"接近真备库？

## 7. 本章互链登记（目标均已在盘验证）

- → [Pro_Oracle_23ai_Administration/00-总览与阅读地图.md](../Pro_Oracle_23ai_Administration/00-总览与阅读地图.md)：23ai 管理版图与可用性工具的现代操作面。
- → [#42 TOP/00](../Troubleshooting_Oracle_Performance_2e/00-总览与阅读地图.md)：RAC/并行对性能诊断的侵入面；[#23 CBOF/00](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)：并行与代价的接口。
- → [03 章](03-实例内存与后台进程.md)（恢复者名册）、[04 章](04-网络连接与服务器进程.md)（SCAN/服务）、[06 章](06-服务器工具与实用程序.md)（备份线）、[02 章](02-物理存储结构与表空间.md)（文件面）。
- → 波内兄弟 #61（安全纵深）/#74（内部机制纵深）：本章两处"点名不展开"的现代接管者；目录未落盘，只登记不链。
- 佐证链接（搜索引擎确认存活）：https://en.wikipedia.org/wiki/Redo_log （⚠️ 存在性佐证，正文不可读）。

## 核心概念速览（中英对照）

- **高可用** — HA：以冗余换连续服务的工程族。
- **RAC** — Real Application Clusters：共享磁盘多实例 ⚠️。
- **缓存融合** — Cache Fusion：跨节点块所有权协议 ⚠️。
- **Clusterware/SCAN** — 集群栈与接入抽象 ⚠️（[04 章](04-网络连接与服务器进程.md)）。
- **Data Guard** — redo 传输+应用的主备制度 ⚠️。
- **物理/逻辑备库** — 块级 vs SQL 级重放 ⚠️。
- **switchover/failover** — 计划互换 vs 故障接管 ⚠️。
- **RPO/RTO** — 丢失量/停机时长两轴 ⚠️。
- **GoldenGate** — 日志集成复制旗舰 ⚠️。
- **版本阶梯** — Edition Ladder：XE/SE/EE 的闸门地图 ⚠️。
- **mode=ro** — 🔧 只读打开（备库可读的最小类比）。
- **热日志回滚** — 🔧 崩溃残留 journal 的未提交回滚实测。
- **故障域** — Failure Domain：一次故障理论上波及的边界 ⚠️（§2b 推演单位）。
- **OSM/服务漂移** — 集群资源迁移单元 ⚠️（Clusterware 语义级）。
- **快照备库** — Snapshot Standby：备库临时可读可测的轮换形态 ⚠️。

## 最新演进与工业实践

- **Oracle 侧**：23ai 时代多租户/自治数据库重构了"HA 叙事"——备份/切换/补丁由平台代理（Autonomous 的 ACD/回滚语义 ⚠️ 转述）；RAC 仍是 on-prem 旗舰但在新增部署中占比被云迁移稀释 ⚠️ 转述。
- **对照生态**：云原生把"站点冗余"下沉为对象存储多副本+计算无状态重启（K8s 探针），Data Guard 式"引擎内建备库"在开源侧对应物是 PG 流复制/MySQL group replication ⚠️ 转述；SQLite/DuckDB 的分布式化外包给上层（litestream/CDC 工具）——本章的三层分工在 2020 年代被拆散重排 ⚠️ 类比。
- **开源对照（🔧 现行）**：SQLite 官方长期立场=单写者+备份策略而非集群（本次 T14/T15 实证其能力边界）；litestream/rocksdb 系 replicated 方案属外部接管 ⚠️ 转述。
- **概念寿命**：RPO/RTO、同步/异步三角、"先单实例后集群"三件事在 SRE 文献里以 error budget/副本协议面貌长存 ⚠️——导游册本章是全目录与可靠性工程线的最近接头。
- **取证注脚**：本章 🔧 结果复现自 `D:\develops\tmp\dbwave_w7_oraess\exp2.py`（G6.1/G6.2 组，os._exit 子进程模拟崩溃）；未安装任何 Oracle 组件，RAC/备库全为 ⚠️ 文档级转述。
