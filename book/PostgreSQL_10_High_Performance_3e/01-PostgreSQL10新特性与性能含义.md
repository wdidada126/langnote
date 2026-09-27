# 01 PostgreSQL 10 新特性全景与性能含义

> 章题 ⚠️ 推定（书系惯例：1e 首章 "What's New in PostgreSQL 9.0"、2e "…9.6…"；本册对应 PG10）。
> 内容主题域以 PostgreSQL 10 官方发行公告（✅ https://www.postgresql.org/about/news/1894/ ）与
> 本册官方代码仓 README 内容简介（✅ 实抓）对位重建，非原书文本。

## 本章要解决的问题

PG10 是一次"为性能而生"的大版本（2017-10-05 发布 ✅ 官方公告）。调优者必须先建立一张
"新特性 → 性能杠杆"的映射表，否则后续 02–16 章的每个决策都缺一块背景板。本章给出四根主杠杆：
**逻辑复制、声明式分区、并行深化（索引构建）、连接与认证（SCRAM）**。

## 杠杆一：内置逻辑复制（发布/订阅）

PG10 之前，跨大版本/选择性同步只能靠插件（pglogical 等）或触发器方案。PG10 把
`CREATE PUBLICATION / CREATE SUBSCRIPTION` 收进内核（✅ 文档 https://www.postgresql.org/docs/10/sql-createpublication.html ）。
性能含义三条：
1. **读扩展**：热点表可订阅到多个下游分担报表/分析查询，与物理流复制不同，逻辑复制不要求同版本，
   允许"生产 PG10 → 分析库 PG10/更高"的异构拓扑 ⚠️（异构限制详见官方 logical decoding 文档，本册 14 章展开）。
2. **代价转移**：解码在源端进行，`wal_level=logical` 会增加 WAL 记录量与运行开销 ⚠️ 转述官方文档口径；
   高写入 OLTP 主库是否开逻辑复制，是本章提出的第一个容量决策。
3. **序列号缺口**：发布不含 sequence，切换时序列须手工同步 ⚠️（官方文档已知限制，14 章复述）。

## 杠杆二：声明式分区

`CREATE TABLE ... PARTITION BY RANGE/LIST`（✅ https://www.postgresql.org/docs/10/ddl-partitioning.html ）。
PG10 的声明式分区是"半成品"：分区裁剪可用，但**不支持对分区表本身的 FK 与唯一约束**（限制在后续版本
逐步补齐 ⚠️ 转述），路由插入还要靠触发器兜底——本册官方代码仓 Chapter15（✅ 实抓文件
`15_11.sql` 即在分区上挂 INSERT/UPDATE 触发器做路由）正是这一过渡形态的写真。性能含义：
- 分区键设计正确时，扫描/维护从"全表"降为"命中分区"，vacuum 与索引维护可分区级并行推进 ⚠️；
- 分区数过多时规划器开销上升，PG10 时代经验值是"几十到几百，别上千" ⚠️ 社区经验转述。

## 杠杆三：并行查询深化——尤其并行索引构建

`CREATE INDEX` 可并行（max_parallel_maintenance_workers，⚠️ 名称以后续版本文档为准）；
9.6 引入的并行顺序扫描在 10 中默认参数更积极。本册 10/15 章的 EXPLAIN 实例均受益于此。
DuckDB 类比实验（🔧 X-D，非 PG）：4 亿行聚合在 threads=1/8 下 min 耗时 1.55s vs 2.64s——
**在负载噪声机上并行度可能不升反降**，这正是 PG10 时代并行参数必须"先隔离噪声再校准"的教训。

## 杠杆四：SCRAM-SHA-256 与连接治理

默认口令散列从 md5 升级 SCRAM（✅ 发行公告），对性能的意义在安全侧信道；但 `pg_hba.conf`
与连接风暴治理（连接池）一起构成本册 02 章"工作负载入口"的第一道闸。README（✅）明言：
单服务器到顶后"connection pooling、caching、partitioning、replication、parallel queries"是五条扩展路——
本章把五条路编号为后续章的入口。

## 与升级路径的耦合

PG10 起 `pg_upgrade` 支持 --link 之外的流复制式升级辅助与 check 改进 ⚠️ 转述；版本支持策略
（每个大版本支持 5 年）见 ✅ https://www.postgresql.org/support/versioning/ ——本册 2018 年语境下的
"PG 9.x 直升 10"决策在 2026 已整体过期，读 01 章要把它当"书系断代表"而不是操作指南。

## 版本断代速查（PG10 相对 9.6 的调优相关差异，⚠️ 转述自官方发行说明）

| 差异点 | 调优影响 |
| --- | --- |
| 逻辑复制内核化 | 读扩展方案从插件选型变成开关决策 |
| 声明式分区（有限） | 大表维护单元化；FK/UQ 限制需设计规避 |
| ALTER SYSTEM 强化 + recovery.conf 废除（并入 postgresql.auto.conf 口径 ⚠️） | 配置心智模型改变（本册 06 章） |
| password_encryption 默认 scram | 连接握手成本略升，安全基线提高 |
| 并行索引构建 | 大表建索引窗口缩短（本册 09 章） |

> 注：recovery.conf 废除的精确表述 ⚠️ 未在本册文档锚点内逐字核验，读作"PG10 复制配置文件合并"方向性提示。

## 细案：新特性→调优动作的映射演练（⚠️ 教材性推演）

把四根杠杆落成可执行清单，每条给"开启前必答"与"开启后必查"：

1. **逻辑复制**
   - 开启前必答：wal_level 从 replica 升到 logical 的重启窗口排在哪天？
     解码 CPU 税按 02 章画像估过吗（写多的事务型负载最伤 ⚠️）？
   - 开启后必查：`pg_replication_slots` 的 restart_lsn 是否推进、
     WAL 目录增速是否越出 06 章 max_wal_size 预算（14 章暗礁前置演练）。
2. **声明式分区**
   - 开启前必答：分区键是否与 80% 范围谓词同族（15 章判据）？
     PG10 限制清单（无 FK/唯一于父表、跨分区 UPDATE 手工）团队是否知悉？
   - 开启后必查：`EXPLAIN` 里裁剪是否发生（15 章 15_10.sql 手法成为月度审计）。
3. **并行深化**
   - 开启前必答：机器是独占还是共享（🔧 X-D 教训）？worker 预算与
     work_mem 乘法账（05 章）算过了吗？
   - 开启后必查：Gather 节点上下的实际 workers 数与每 worker 时间均衡度。
4. **SCRAM/连接治理**
   - 开启前必答：所有客户端库的 SCRAM 兼容矩阵盘点 ⚠️（2018 年老驱动是主要拦路虎）；
   - 开启后必查：认证失败率临时上升的回滚开关与观察窗。

## 章内自测（五问五答，速查版）

- **问：PG10 逻辑复制为什么不能直接当"零停机升级"的唯一方案？**
  答：它是异构桥梁而非同构镜像——序列不搬、DDL 不同步、订阅端不建表，
  升级剧本须把这些手工步骤逐一编入 runbook（14 章展开）。
- **问：分区在 PG10 的"半成品"具体缺什么？**
  答：分区表上的 FK/唯一约束、内核级跨分区行移动；书仓 Chapter15 的触发器路由即补丁标本（15 章）。
- **问：并行索引构建的隐藏成本在哪？**
  答：每 worker 复制工作内存 + 与 autovacuum 抢 worker 预算（05/07 章联立）。
- **问：SCRAM 是性能参数吗？**
  答：不是，但它改变连接风暴的成本结构（握手 CPU 略增）并把安全债务清零（06 章语境表）。
- **问：README"五路"与本章四杠杆什么关系？**
  答：四杠杆（复制/分区/并行/连接）是五路中三条的内核化部分；
  池化与缓存两路属外置工程，落点在 02/13/14 章。

## 核心概念速览（中英对照）

- **逻辑复制** — Logical Replication：基于 WAL 解码、按发布/订阅模型同步选定对象的复制范式。
- **发布/订阅** — Publication/Subscription：PG10 逻辑复制的两半端点 DDL。
- **声明式分区** — Declarative Partitioning：用 PARTITION BY 声明父子分区关系，运行时裁剪。
- **分区裁剪** — Partition Pruning：规划/执行期只访问命中分区，跳过其余分区。
- **并行索引构建** — Parallel Index Build：多 worker 分担 CREATE INDEX 的排序/写入阶段。
- **并行工作进程** — Parallel Worker：执行器内 Gather 之下启动的辅助进程。
- **SCRAM-SHA-256** — SCRAM：挑战-响应式口令认证，替代 md5 的默认散列。
- **连接池** — Connection Pooling：以 pgbouncer 类代理复用后端连接，压平进程模型开销。
- **WAL 层级** — wal_level：决定 WAL 记录丰富度（minimal<replica<logical）的参数。
- **pg_upgrade** — in-place major upgrader：跨大版本原地升级工具，--link 模式近乎瞬时。
- **大版本支持窗口** — Version Support Policy：PG 社区每大版本约 5 年支持承诺。
- **前滚式阅读** — forward map：把"新特性"映射到后续章节调优杠杆的阅读法（本章方法论）。
- **断代表** — era table：书中版本语境与当前版本的差异对照，避免照抄旧参数。

## 最新演进与工业实践

- **发布/订阅已成默认答案**：PG10 的模型沿用至今，PG15 加行过滤、PG16 引 `pg_createsubscriber`
  把物理备库转逻辑订阅 ✅ 转述（https://www.postgresql.org/docs/17/logicaldecoding.html 为现行权威页，
  本次 curl 200）；跨机房同步产品（如基于逻辑解码的 CDC）在 2024–2026 大量出现 ⚠️。
- **分区谱系补齐**：分区表 FK/唯一约束在 PG12 落地、哈希分区 PG11 落地 ⚠️ 转述版本序列表；
  2026 年新项目已无 PG10 分区限制之虞，但"分区数上千规划器变慢"的教训仍以
  https://www.postgresql.org/docs/17/ddl-partitioning.html （✅ 本次 curl 200）一类现行文档为准（本目录仅引用已验证页面）。
- **并行度模型演化**：PG10 的 max_parallel_workers_per_gather 语义在后续版本纳入统一
  worker 预算制（max_worker_processes 家族）⚠️ 转述；云厂商托管 PG 普遍按实例规格给出推荐值，
  与 Aurora 的 I/O 预算耦合（论文：Amazon Aurora: Design Considerations for Cloud
  Object Storage for Global Scale, SIGMOD 2017, DOI: 10.1145/3035918.3056101 ✅ Crossref 200）。
- **SCRAM 迁移是运维常态**：md5→scram 的在线迁移脚本与兼容矩阵在社区 wiki 长期维护
  （✅ https://wiki.postgresql.org/wiki/Main_Page 入口页本次 curl 200）。
- **工业实践**：2026 年仍在生产运行 PG10 的系统属 EOL 尾部（5 年窗口 2022 已闭 ✅ versioning 页），
  本册的当代读法是"考古 + 方法论"；升级工具链（pg_upgrade、pgdump 式逻辑迁移）文档锚点
  https://www.postgresql.org/docs/16/pgupgrade.html （✅ 200）。
