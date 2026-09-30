# 第 6–7 章：DDL 优化技巧和技术 · 管理、优化、调整大型数据库

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；Oracle 行为均为 11gR2–12cR1 口径转述，无 Oracle 实测）。本文件无 🔧 组，类比实验见同目录 01/02/04/05/10 号文件（均标非 Oracle）。

## 本文件定位

第 6 章管"改结构怎么不炸"（建索引/移动/分裂等 DDL 的耗时、锁与恢复代价），第 7 章管"库变大之后所有运维动作都要重算成本"。两章是变更保障线的前半：先学会便宜地改（6），再学会在 TB 级现实里规划改（7）。

## 第 6 章 DDL优化技巧和技术

### 6.1 症状面（⚠️ 转述）

- 生产窗口建一个二级索引超窗；`ALTER TABLE MOVE` 把表锁到变更结束，应用报 `ORA-00054`。
- 批量 DDL 后 UNDO/REDO 暴涨，闪回区撑爆触发 `ORA-01555` 连锁（回看第 2 章链路与第 8 章备份窗口）。
- 索引重建期间 `ORA-00600 [ktuAssertCnt]` 一类内部断言（老版本 BUG 面，社区口径）。

### 6.2 工具箱（⚠️ 转述，按"代价从低到高"排）

1. **并行 DDL**：`CREATE INDEX ... PARALLEL n` + 建完改回 PARALLEL 1（防后续 DML 意外走并行）；12c 起 `PARALLEL AUTO` 由并行执行框架自适应。
2. **NOLOGGING + 补备份**：批量加载/重建走 NOLOGGING 省 REDO，但对象在介质故障后不可恢复——必须"NOLOGGING 变更 + 立即备份该对象"配对执行（与第 8 章协议）。
3. **ONLINE 选项**：`CREATE INDEX ONLINE` / `ALTER TABLE ... REBUILD PARTITION ONLINE`，以日志表临时双写换可用性，代价是窗口加长与额外 UNDO。
4. **DBMS_REDEFINITION 在线重定义**：结构大改（换分区方式/加密列）不动用长时间锁：物化视图依赖同步 ccons 阶段完成切换。
5. **交换分区（EXCHANGE PARTITION）**：秒级把预建表灌进分区表/移出历史分区，是大库加载与归档的正门（与第 13 章数据泵、第 7 章 ILM 衔接）。
6. **延迟段创建**（11.2 Deferred Segment Creation）：空表零段，批量建 schema 不再堆碎段——但注意导出老工具对"无段表"的坑。

### 6.3 统计与验证纪律（⚠️ 转述）

- 并行统计收集 `DBMS_STATS.GATHER_TABLE_STATS(degree=>n, cascade=>TRUE)`；大表先用 `estimate_percent=>DBMS_STATS.AUTO_SAMPLE_SIZE`。
- 变更后立即验证计划：`EXPLAIN PLAN` 不够，取游标实际计划（衔接 SQLT，第 19 章）；锁住关键统计（`LOCK_STATISTICS`）防变更窗口内漂移（与第 5 章 SPM 互补：SPM 钉计划，统计锁钉依据）。

## 第 7 章 管理、优化、调整大型数据库

### 7.1 大库的"成本重算"清单（⚠️ 转述）

| 运维动作 | TB 级下的新约束 | 缓解 |
|---|---|---|
| 全库备份 | 窗口>夜间 | 增量滚动 L0/L1 + 压缩 + 变更跟踪（Ch.8） |
| 统计收集 | 单表小时级 | 分区级增量统计（11g Incremental Stats）、并行 |
| 空间管理 | ASSM 位图段头热点 | 分区切细、避免单段超密插入（回看 Ch.3） |
| 一致性读 | 长查询撞保留窗口 | UNDO 放大+guarantee 分级、ADG 分流 |
| 模式演进 | MOVE 不可用（锁面） | 区间/哈希分区+交换+在线重定义（Ch.6） |
| 数据倾斜 | 单分区超大热块 | 拆分策略/子分区/归档冷数据（SSD 分层，Ch.17） |

### 7.2 分区设计口径（⚠️ 转述）

- 分区是"运维单位"不是"性能单位"：先问按什么切能同时服务备份窗口、归档（ILM）、可用性（分区级 ONLINE 操作）与并发热点。
- 12c 新武器： interval 分区（自动按时间扩展，救"忘了加分区"这一经典生产事故）、近似索引（Global 非分区索引+本地化扫描裁剪）、多分区键限制仍在 2 键内。
- 位图索引在大库 OLTP 侧禁用（并发锁放大），DSS 侧保留（机理见 CBOF 位图章）。

### 7.3 大库专属的诊断视角（⚠️ 转述）

- 备份验证常态化：`RESTORE ... VALIDATE` + `DBV` 抽检（第 8 章细则）——大库经不起"第一次恢复测试就失败"。
- 增长模型：AWR 里按对象类别的块读增长趋势做 6 个月容量外推（AWR 章的方法在此复用）。
- 段级健康：碎片率、行迁移（`analyze ... list chained rows`/`v$sysstat` 中 table fetch continued row）、高水位空洞——三者都先用在线办法回收，别指望停机窗口。

## 6.4 案例演练：给 4TB 分区表加一个二级索引（⚠️ 按章主题结构化）

1. 估窗：先在同型表的子分区上做一次对照构建，记录耗时与并行效率。
2. 路径选型：`PARALLEL + NOLOGGING` 建，完工立即配对对象级备份（第 8 章协议）。
3. 锁面核对：需要 ONLINE 语义（表上 DML 不能停）则改 ONLINE 构建，评估日志表额外代价（6.2 第 3 项）。
4. 统计：建完并行收集表+索引统计，比对关键 SQL 的 plan_hash_value 是否已按预期变化（衔接第 19 章 SQLT）。
5. 回归防线：把旧好计划先载入 SPM 基线，再让新索引生效，保留回退位。
6. 失败位：并行构建中断留 UNUSABLE，走 DROP 重建而非指望第二遍在线更快。

## 7.4 常见误区（⚠️ 社区口径）

- "分区=查询快"——分区首要收益是运维性（交换/维护/窗口），裁剪失败时反而多一层开销。
- "全局索引不能用"——正确表述是：用则必须绑定维护预案与备份窗口评估。
- "大库必须上 Exadata"——本册为通用存储口径；硬件取向看第 17 章的成本画像再决定。
- "MOVE 表就是快"——MOVE 携带索引重建与统计失效双连击，窗口预算要按 6.4 全流程估。

## 症状 → 动作速查表

| 症状 | 第一动作 | 章节 |
|---|---|---|
| 建索引超维护窗口 | 并行+NOLOGGING+补备份三件套 | Ch.6 |
| DDL 期间应用 ORA-00054 | 改 ONLINE 路径或重定义 | Ch.6 |
| 大表换分区方案 | DBMS_REDEFINITION 或新建+交换分批 | Ch.6/7 |
| 忘加分区致 ORA-0001 类插入失败 | interval 分区改造+应急手工加分区 | Ch.7 |
| 统计收集拖垮窗口 | 增量统计+对象级锁定 | Ch.6/7 |
| 行迁移计数上升 | 链式行清单+在线 MOVE 受影响分区 | Ch.7 |

## 关联阅读

- 变更前后计划验证：[10-SQLT与XA分布式事务.md](10-SQLT与XA分布式事务.md)；备份协议：[04-RMAN备份恢复最佳实践.md](04-RMAN备份恢复最佳实践.md)
- 统计与优化器机理：[../Cost_Based_Oracle_Fundamentals/07-直方图.md](../Cost_Based_Oracle_Fundamentals/07-直方图.md)、[../Troubleshooting_Oracle_Performance_2e/08-对象统计信息.md](../Troubleshooting_Oracle_Performance_2e/08-对象统计信息.md)
- 物理设计正典：[../Troubleshooting_Oracle_Performance_2e/16-优化物理设计.md](../Troubleshooting_Oracle_Performance_2e/16-优化物理设计.md)
- 23ai 时代的管理口径：[../Pro_Oracle_23ai_Administration/00-总览与阅读地图.md](../Pro_Oracle_23ai_Administration/00-总览与阅读地图.md)

## 自测题

1. 为什么 NOLOGGING 必须与"立即补备份"配对？不配对会在哪种故障下暴露？
2. ONLINE 索引构建的"日志表"为什么消耗额外 UNDO？
3. 交换分区为什么是"大库加载与归档的正门"？给出两个方向（灌入/移出）的例子。
4. 延迟段创建对老版本导出工具有什么坑？
5. 11g 增量统计对复合分区表有哪些不生效形态？⚠️ 说出你能记起的一条限制。
6. interval 分区救的是哪一类经典生产事故？原理是什么？
7. 案例演练第 5 步里，为什么"旧计划先入基线"要发生在"新索引生效"之前？
8. "MOVE 表就是快"这条误区里藏着哪两项常被漏算的连击成本？

## 核心概念速览（中英对照）

- **在线重定义** — DBMS_REDEFINITION：以物化视图同步实现在线换结构 ⚠️
- **分区交换** — Exchange Partition：秒级互换表与分区，数据不动元数据动 ⚠️
- **并行 DDL** — Parallel DDL：多进程分段建索引/移动 ⚠️
- **NOLOGGING** — Nologging：跳过 REDO 的快改路径，牺牲可恢复性 ⚠️
- **延迟段创建** — Deferred Segment Creation：空表不分配段 ⚠️
- **增量统计** — Incremental Statistics：按分区统计聚合出表级统计 ⚠️
- **间隔分区** — Interval Partition：按插入自动扩展的时间分区 ⚠️
- **行迁移** — Chained/Migrated Rows：行增大后指针跳转，读取代价翻倍 ⚠️
- **自动段空间管理** — ASSM：位图管理块空闲度，段头自带热点属性 ⚠️
- **信息生命周期** — ILM：热温冷分层的数据管理策略 ⚠️
- **统计锁定** — Lock Statistics：防止关键表统计被收集任务改写 ⚠️

## 最新演进与工业实践

- **自动索引接管第 6/7 章一部分**：19c/23ai Autonomous DB 的 Automatic Indexing 每月批量决策索引创建/废弃（默认维护窗口内执行），DDL 风暴变成审计日志 ⚠️ 转述；docs.oracle.com 的 Autonomous 指南章节 ✅（域名可达）。
- **分区上限放宽**：121 非 CDB/19c 对分区表规模、12c 对 interval/引用分区的完善，使"以分区为运维单位"成为大库默认架构；23ai 继续加强 JSON 关系二元与分区的组合 ⚠️。
- **变更窗口消亡论**：DevOps 数据库流水线（Liquibase/Flyway 对 Oracle 方言）把 6.2 工具箱包成受审迁移脚本，NOLOGGING/补备份配对以流水线阶段固化 ⚠️ 转述。
- **大对象归档外置**：工业实践中冷数据出 Oracle 进对象存储+外部表/BFP（数据库表内仅热切片），第 7 章"增长模型"变成出仓速率规划——与仓库线 [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md) 的归档视角互链。
