# 09 · Oracle→PostgreSQL 数据复制：Oracle GoldenGate（原书第 9 章）

> 对应原书章：**Ch.9 Data Replication from Oracle to PostgreSQL Using Oracle GoldenGate**（✅ Crossref
> DOI `..._9`）。官方摘要原句（✅）："Oracle GoldenGate is a comprehensive software application that
> offers various solutions like data replication, data integration, data transformation, data streaming,
> data high availability, real-time data transactions an…"
> 口径声明：章题与摘要 ✅ 实抓；正文为按 Oracle 官方文档口径的精读重构 ⚠️ 转述——**Oracle/GG 本机
> 不可安装不可运行，全章无 PG/Oracle 实测**；🔧 节用 SQLite 触发器搭建 capture→apply 玩具链路，
> 只演示 CDC 架构骨架，**不代表 GG 或 PG 逻辑解码的性能与语义**。

## 本章地图

| 主题 | 你能做到 | 关键对象/参数/命令 |
| --- | --- | --- |
| GG 架构拆解 | 画出 Extract→Pump→Trail→Replicat 数据流 | 集成捕获、trail 文件、checkpoint 表 ⚠️ |
| OGG for PostgreSQL | 说清目标端投递形态与前置 | 21c 起官方支持 PG 目标（⚠️ 版本口径见演进节）、逻辑解码前置 |
| 零停机迁移编排 | 排初始装载+增量追平+切换三拍 | `replicat handlecollisions`、序列接管、校验窗口 ⚠️ |
| GGSCI 运维 | 看延迟、追进度、清积压 | `info extract all`、`lag replicat`、stats 报表 ⚠️ |
| 故障与取舍 | 判断"断链/漂移/冲突"处置 | 丢弃事务重放、改 scn/seq 起点、对比原生逻辑复制 ⚠️ |

## 核心精讲（⚠️ 文档转述重构）

### 1. 与 08 章的分工

Ora2Pg 解决"搬一次"，GoldenGate 解决"不停搬 + 搬完还能并行跑"。选型判据一句话：**允许停机窗口用
08 章路线；要求分钟级切换或双向回退用本章**。回退通道（PG→Oracle 反向同步保命）也是 GG 相对
单向脚本的独有价值 ⚠️。

### 2. 架构：日志抽取 + 队列 + 重放三段式

- **Extract（抽取）**：读源库重做日志/归档做 CDC（变更数据捕获），"集成抽取"直读日志不走触发器，
  源库负担小；按表过滤/列映射在参数文件内完成 ⚠️。
- **Data Pump（送达）**：把本地 trail 切片推送到远端 trail——网络断点续传与压缩的载体。
- **Replicat（应用）**：读远端 trail，把变更重放成目标库 SQL/批量装载；`batchsql`/并行度决定吞吐。
- **checkpoint 机制**：进程断点续传的游标（源端 LSN/seq#，目标端可落表）——**所有 CDC 系统的命根**，
  🔧 演示第 5 节的 seq 列就是它的玩具化。
- 目标端为 PostgreSQL 时（OGG for PostgreSQL，⚠️ 转述）：GG 以客户端身份直写目标表，需要目标端
  账号与模式先行建好（08 章结构迁移的产物），并关注目标端索引/约束对重放速率的反比效应。
  官方文档入口 ✅ https://docs.oracle.com/en/middleware/goldengate/ （实抓 200）。

### 3. 零停机切换三步曲

1. **基线装载**：一致性快照 + 记录起始 SCN（`FLASHBACK_SCN` 类参数）——起点错了全盘歪 ⚠️；
2. **增量追平**：Replicat 从起始 SCN 重放；`handlecollisions` 容忍基线/增量重叠区的双写冲突；
   lag 收敛到秒级即"追平"；
3. **切换与接管**：应用停写→最终对账（行数/校验和/抽样业务对单，08 章校验清单复用）→流量切 PG→
   序列 `setval` 接管→**保留反向通道一个观察期**再退役源端。
   窗口里最容易翻车的三件事：序列重号、触发器/任务双跑、大事务把 lag 拉爆 ⚠️。

### 4. 运维面与常见取舍

- GGSCI 三板斧：`info all`（进程态）、`lag <group>`（trail 落后）、`stats <group>, total`（吞吐）；
  告警盯 lag 与 trail 磁盘占用（pump 断了 trail 会堆爆源端文件系统 ⚠️）。
- **限制清单**（⚠️ 转述）：DDL 复制需专项配置且两端语法不保真（对象类变更多数要人管）；
  大对象/LOB 调优特殊；无主键表默认按全列匹配，性能与正确性双差——**迁移前先补主键**（与 08 章
  校验联动）；字符集转换在抽取端做，目标端乱码查 NLS 参数。
- 与原生方案对比位：PG 侧逻辑复制只能"PG 当源"；Oracle 当源时社区开源替代是 Debezium+Kafka 类
  （架构同构：logminer/CDC→outbox→sink ⚠️ 转述，本册不展开）。

### 5. 🔧 本机概念演示：capture→apply 骨架（SQLite，非 GG/PG 结论）

方法：Python sqlite3 **3.45.3**（本机实测；脚本存盘 `D:\develops\tmp\dbwave_w3_pgadmin\`），
用触发器把源表变更写入 `cdc_log(seq,op,id,oldv,newv)`（≈trail），再按 seq 单线程有序重放到目标库
（≈replicat），带 ver 列记录应用进度（≈checkpoint 表）：

```
capture: total=5300 I=5000 U=200 D=100     # 5000 插入 + 200 更新 + 100 删除全被抓到
apply  : 5300 条有序重放后 target=4900 == source=4900；sum(length(v)) 校验和一致 True
```

**可迁移概念**（✅ 方法论，⚠️ 数字非引擎结论）：①CDC 正确性三要素在此全现形——**捕获不漏
（触发器/日志全覆盖）、单分片内有序（seq 递增）、幂等应用（INSERT OR REPLACE/UPSERT）**；
GG 的 trail 切片、checkpoint 表、handlecollisions 各对应其一。②触发器式捕获（本演示）与
日志式捕获（GG 集成抽取/PG 逻辑解码）的差别正是"业务路径上多一笔写"vs"旁路读日志"——
08 章说源库侵入、本演示即侵入成本的具象。③校验和比对 = 第 3 步切换前的对账原语。

## 常见坑与判读

| 现象 | 第一判读 | 取证动作（⚠️ 转述） |
| --- | --- | --- |
| Replicat 持续 lag 不收敛 | 目标端索引/约束拖慢重放，或大事务墙 | 装载期临时降级非关键索引；调 batchsql/并行 |
| 切换后偶发主键冲突 | 基线 SCN 与增量起点没咬住 | 复核起始位点；对账脚本兜底 |
| 源端磁盘告警 | Pump 断链 trail 堆积 | `info extract, detail` 看远端写失败；清历史前先确认已送达 |
| 目标行数对但值不对 | 无主键表全列匹配更新打偏 | 补主键/唯一键重配；抽样对单 ⚠️ |
| DDL 变更后开始报错 | 对象漂移未被复制 | 变更窗口冻结策略：结构变更走双端人工发布 |
| 双向同步列值"回环" | 缺反循环配置 | 按 GG 反循环机制标记本地事务（两端参数都要查）⚠️ |

## 与其他章 / 其他笔记的联系

- 本册：08 章（结构/代码迁移是复制的前置）；04 章（两端复制账号权限面）；05 章（日志/槽的
  PG 侧心智）；03 章（目标端装载的页/TOAST 视角）；10 章（PG16/17 逻辑复制增强改变"要不要 GG"的答案）。
- [../PostgreSQL_16_Administration_Cookbook/07-复制高可用与升级.md](../PostgreSQL_16_Administration_Cookbook/07-复制高可用与升级.md)：
  PG 原生复制食谱版（对等替代位）。
- [../设计数据密集型应用.md](../设计数据密集型应用.md)：CDC/变更日志/最终一致的理论正源（第 9 章口径）。
- [../Pro_SQL_Server_Internals/16-事务日志备份与高可用.md](../Pro_SQL_Server_Internals/16-事务日志备份与高可用.md)：
  同"日志即真理"哲学的另一家实现。
- [../../db/db.md](../../db/db.md)：复制/流式论文线索引。
- 波内互链义务：`Streaming_Databases/`（#167，CDC 上游理论）与 `PostgreSQL_10_High_Performance_3e/`
  （#64，逻辑复制性能侧）；见 00 登记表。

## 核心概念速览（中英对照）

1. **GoldenGate (GG/OGG)**：Oracle 旗下的商业日志型复制套件，去 O 零停机主力。
2. **变更数据捕获** — CDC (change data capture)：从日志/触发通道旁路捕获行级变更。
3. **抽取进程** — Extract：源端读日志、产出变更记录的进程。
4. **数据泵** — Data Pump：trail 跨机搬运工，断点续传位点所在。
5. **重放进程** — Replicat：目标端消费 trail 并幂等重放。
6. **轨迹文件** — trail file：变更持久化队列，落盘切片，lag 与磁盘告警的主对象。
7. **检查点表** — checkpoint table：应用进度游标的持久化（🔧 演示的 seq/ver 列原型）。
8. **集成抽取** — integrated capture：直读重做日志、免触发器的低侵获取数模式。
9. **碰撞处理** — handlecollisions：基线/增量重叠区双写容忍开关。
10. **切换对账** — cutover reconciliation：行数+校验和+业务抽样的三层验收。
11. **反向通道** — reverse replication：PG→Oracle 回退保命链路。
12. **OGG for PostgreSQL**：GG 官方目标端形态，以客户端身份直写 PG（⚠️ 前置条件见演进节）。

## 最新演进与工业实践

- **OGG for PostgreSQL 时效口径**：Oracle 自 21c 时代提供官方 PostgreSQL 支持（Big Data/PG 服务线），
  版本矩阵、认证 OS 与 PG 版本支持随官方公告滚动更新——本册不背版本号，落地前以
  ✅ https://docs.oracle.com/en/middleware/goldengate/ （实抓 200）的支持矩阵为准 ⚠️ 转述。
- **开源替代走强**：Debezium（Kafka Connect 生态的 CDC 框架）+ pgoutput/wal2json 目标端 sink
  已成"不想买 GG"的默认组合；2024–2026 云厂商迁移服务也多是这层的托管壳 ⚠️ 转述
  （Debezium 仓库链接本轮未验证不附，主代理可补 https://debezium.io/）。
- **PG16/17 逻辑复制增强改变格局**：备库可发布（16）、大事务并行应用、`failover` 槽（17）、
  pg_createsubscriber（17/16.4）——**PG→PG 段基本告别 GG**，GG 的剩余主场是"Oracle 当源"那一段 ⚠️ 转述
  （✅ https://www.postgresql.org/docs/release/17.0/ 实抓 200）。
- **双向/多活谨慎化**：行业共识回到"单主切换 + 观察期"，双向回环案例多用于谈判期回退而非长期形态 ⚠️。
- **缺口诚实登记 ⚠️**：原书 GG 实操所用版本、参数文件逐行讲解、截图环境未获样章，本章按官方
  文档主流口径重建。
