# 09 Medallion 分层管道端到端实战 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题重构章（00 §5 口径），对位原书"数据工程师主干"的端到端管道部分。机制 ✅ 转述
> `fundamentals/end-to-end-tutorials`（当日 200，00 §9 台账）+ data-engineering 域 `tutorial-*`
> 文件族清单实抓（GitHub fabric-docs 目录取证通道）。🔧 复用 E4/E2/E3（无新增实验）。
> Medallion 机制正主在盘上 Delta 册 08 章实链；波内 #220 食谱册只登记不链。

## 9.1 Medallion 是契约分层，不是文件夹分层

bronze/silver/gold 三层 = **读写契约**的三级，不是目录树的三级 ⚠️（通识口径，与开源栈一致）：

- **bronze**：原始保真——只追加、只加审计元数据、不做业务变换；可重放的"事实底账"。
- **silver**：清洗一致——去重、 conforms（统一命名/类型/编码）、SCD、业务规则第一次生效。
- **gold**：服务取向——聚合/宽表/语义就绪，读方是 BI 与应用，不是工程师自己。

分层成立的三条件（缺一即"伪分层"）：每层有**独立表事务**（Delta 表为单元，回链 `03` 章
"表是契约单元"）、独立**刷新水位**（🔧E4）、独立**读方承诺**（bronze 不许 BI 直连 ⚠️）。

方法论祖谱回链：[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)
——Bill Inmon 的 CIF"整合数据"与 Ralph Kimball 总线矩阵是"分层集成"的工程前史；Medallion 是其在
湖上的执行形态。Fabric 内三层默认同驻一个 Lakehouse 的表（✅ `lakehouse-overview`，00 §9 引用台账），
gold 亦可落 Warehouse——路由判据就是 `08` 章四问，本章不重复。

## 9.2 官方教程链的重构（✅ 页族实抓 → 步骤表）

当日 200 的 `end-to-end-tutorials` 是总枢纽；data-engineering 域目录清单实抓含
`tutorial-lakehouse-introduction/get-started`、`tutorial-build-lakehouse`、
`tutorial-lakehouse-data-ingestion`、`tutorial-lakehouse-data-preparation`、
`tutorial-lakehouse-build-report`、`tutorial-lakehouse-clean-up`、`load-data-lakehouse`、
`lakehouse-notebook-load-data` 等页名（✅ 文件族取证；⚠️ 页面内容未逐页转述，本表按工程师叙事展开）：

| # | 教程步骤 | 页名证据（✅） | 本册落点 |
|---|---|---|---|
| 1 | 建湖与目录结构 | `create-lakehouse` | 03 章 |
| 2 | 数据接入 bronze | `load-data-lakehouse` / `tutorial-lakehouse-data-ingestion` | 05/06 章 |
| 3 | bronze→silver 准备与转换 | `tutorial-lakehouse-data-preparation` / `lakehouse-notebook-load-data` | 04 章笔记本 |
| 4 | silver→gold 聚合与服务 | `tutorial-lakehouse-build-report`（汇入报表侧 ⚠️） | 08 章 |
| 5 | 清理与治理收尾 | `tutorial-lakehouse-clean-up` | 10 章 |

⚠️ 重构立场：官方教程是"点按钮"动线；本章把它读回成**管道解剖图**——每步背后是哪层契约、
哪个失败模式，才是数据工程师的增量。

## 9.3 三层各自的工程约定（本册核心交付 ⚠️+✅）

| 层 | 写路径 | 读路径 | 关键契约 | 组件锚（本册章） |
|---|---|---|---|---|
| bronze | 追加 only + 审计列（✅ `audit-columns-copy-job` 页名，05 章） | 只有 silver 作业 | 不可变保真；错了重放不覆写 | 05 Copy job / 06 Mirroring |
| silver | MERGE/去重/SCD2（✅ Delta MERGE 语义，回链盘上 Delta 册 02/10 章） | gold 作业、特征工程 | 唯一键/非空率断言先于消费 | 04 笔记本变换 |
| gold | 全量重算或分区微批（⚠️ 视口径变更频率） | BI/应用/即席 SQL | 口径变更=发布事件，有评审 | 08 Warehouse/湖端点 |

时间旅行是 silver/bronze 的**审计合规器**（🔧E2：旧快照文件不动）——"谁改了什么口径"在
Delta 历史里自带答案 ⚠️，这在 2024 前的 ETL 栈里要靠日志系统额外建设。

## 9.4 🔧 复用账：bronze 摄取重放与 silver 维护（非 Fabric 行为）

本机实测（`exp.py`，2026-10-02，SQLite 3.45.3 + DuckDB 1.5.5；数字只作量级类比）：

```text
[E4] full-refresh#1 loaded rows=100000 427.78 ms; incremental#2 after 2 new source rows
     loaded=2 rows 13.16 ms (only delta moved; watermark now 2024-06-16 08:00:00)
[E2] commit(v2)=67.74 ms; as-of v1 rows=200000, as-of v2 rows=250000;
     old snapshot unchanged (immutable files = delta files appended)
[E3] scan-10-frags rows=200000 2.16 ms; OPTIMIZE-analog rewrite 47.44 ms;
     scan-merged rows=200000 1.21 ms; bytes 3.05MB -> 3.03MB; rowcount identical: True
```

- **E4 → bronze**：水位表+严格 `>` 语义是"首刷贵、二刷便宜"的全部秘密；重放不脏表
  （05 章铁律 2/3 的本机证据）。
- **E2 → silver**：MERGE 提交后旧版本整体可读——补数/改口径的作业可以对着 as-of 快照
  做**前后对账**再发布 ⚠️（工程建议，非平台承诺）。
- **E3 → silver 的小文件税更重**：每批 MERGE 都产 delta 文件，转换层是碎片制造机；
  维护面（✅ `lakehouse-table-maintenance` 页名，03 章）在 silver 的使用频率高于 bronze。

## 9.5 编排：Pipeline item 的活动骨架（✅ 页 → ⚠️ 骨架）

✅ `pipeline-overview`（00 §9 台账）给活动/依赖/重试三要素；⚠️ 本章给出分层管道的标准骨架：

1. bronze 段：摄取活动（Copy job/Dataflow 活动按 05 章三岔路选）→ 行数断言活动。
2. silver 段：笔记本活动（04 章作业化形态）→ 质量门（唯一键/空值率）→ 失败仅重试当前段
   （幂等前提=E4 水位 + E2 MERGE，重放安全）。
3. gold 段：SQL/notebook 聚合 → 发布通知（10 章监控中心挂告警）。
4. 跨段**检查点串联**：段间靠表就绪（+水位推进）传递，不靠"上游成功"这个脆弱信号 ⚠️。

Spark job definition（✅ `spark-job-definition` 页名）承担 silver/gold 段的"作业化正身"，
被 Pipeline 活动引用或独立触发（⚠️ 两种姿势平台皆有）。开源对照：Pipeline≈Airflow DAG
（05 章已实链 `Modern_Data_Engineering_with_Spark/08-Airflow工作流编排.md`）。

## 9.6 质量与可观测的内置件与自建件

- 内置 ⚠️✅：审计列（05 章 ✅ 页名）、血缘（10 章）、笔记本输出日志（04 章）。
- 自建（工程师责任区 ⚠️）：**分层断言表**——bronze 行数对账（源 vs 落）、silver 唯一键+
  非空率、gold 口径抽检；🔧E5 的"行数+聚合双核对"是最小可用验收器，进 runbook。
- 接盘上学科正主：[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)、
  [../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)
  ——平台监控 ≠ 数据可观测（后者管"值不值得信"，前者管"跑没跑成"⚠️）。

## 9.7 端到端推演（一条管道的八步 ⚠️ 叙事）

① 01 章建工作区/容量 → ② 03 章建 Lakehouse、定三层表命名 → ③ 02 章 Shortcut 挂外部原始区
（零拷贝，🔧E1）→ ④ 05 章 Copy job 落 bronze+审计列+水位表 → ⑤ 04 章笔记本 bronze→silver
（MERGE，🔧E2）→ ⑥ silver 维护面 compaction（🔧E3）→ ⑦ 08 章四问定 gold 落湖表还是仓 →
⑧ 10 章挂部署管道+监控告警。每步的失败模式已在对应章"误区"节挂号——本章是把挂号单串成
巡检路线 ⚠️。

## 9.8 误区清单（⚠️ 编者语）

1. **bronze 做业务变换**——重放即毁账；变换是 silver 的合同。
2. **gold 当垃圾桶**——所有"来不及分层"的临时表堆进 gold，服务面变垃圾场。
3. **全量重算一把梭**——租户级自杀（🔧E4 的账：增量把 427ms 级开销压到 13ms 级量位 ⚠️ 不外推）。
4. **三层拆三个 Lakehouse**——同湖多表即可；拆湖只增加权限与发现成本（OneLake 前提是 ✅ 平台事实）。
5. **编排无检查点、全链一把重试**——50 步管道一步红全链重跑；段间断点+幂等才敢值守。
6. **把官方教程点完当学会**——按钮动线≠契约设计；本章 9.3 的表才是可迁移资产 ⚠️。

## 9.9 与盘上诸书的联系

- Medallion 机制正主（开源 Delta 形态）：
  [../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md](../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md)
  （盘上实名已验，实链 ✅）——三层语义、CDC/SCD 细节在其 10 章（06 章已链）。
- 岗位管道通识：[../Modern_Data_Engineering_with_Spark/07-数据管道与结构化应用.md](../Modern_Data_Engineering_with_Spark/07-数据管道与结构化应用.md)
  与编排对照其 08 章（05 章已链）。
- 转换层开放生态对位：[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)、
  [../Unlocking_dbt/00-总览与阅读地图.md](../Unlocking_dbt/00-总览与阅读地图.md)——dbt 模型分层
  ≈medallion 的 SQL-only 方言；Fabric 用 notebook+spark-job 承担同角色（05 章 dbt-job 接缝）。
- 平台地图姊妹章：[../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md](../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md)。
- 方法论祖谱：[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)（9.1 已链）。
- 波内登记（不链）：#218 入门册（其教程动线本章 9.2 已给重构版）、#220 食谱册（9.3 骨架的
  逐场景配方归它）。

## 核心概念速览（中英对照）

- **分层契约** — Layered Contract：层=读写承诺的差集，不是目录树 ⚠️。
- **青铜层** — Bronze：追加保真+审计列，可重放不可覆写 ✅⚠️。
- **白银层** — Silver：MERGE/去重/SCD，业务规则第一次生效 ✅。
- **黄金层** — Gold：服务取向，口径变更=发布事件 ⚠️。
- **水位重放** — Watermark Replay：首刷贵二刷便宜的账本（🔧E4）。
- **as-of 对账** — Time-Travel Reconciliation：改口径前后各读一版快照互核（🔧E2 引申 ⚠️）。
- **转换碎片税** — Transform Fragmentation Tax：MERGE 批批产 delta 文件（🔧E3 引申 ⚠️）。
- **检查点串联** — Checkpoint Chaining：段间以表就绪传递，不靠上游成功信号 ⚠️。
- **断言分级** — Tiered Assertions：bronze 行数/silver 键性/gold 口径，各自验收 🔧E5 模式。
- **单湖多层** — One Lake, Many Layers：OneLake 内同湖多表即足，拆湖无收益 ✅⚠️。

## 最新演进与工业实践

2024→2026（取证 2026-10-02；URL 台账见 00 §9）：

- **教程链官方化**：`end-to-end-tutorials`（200 实测）+ `tutorial-*` 文件族（✅ 目录清单实抓）
  说明平台方把 medallion 动线收编为官方叙事——方法论产品化的标志 ⚠️；本册立场：官方给按钮、
  本册给契约（9.3 表）。
- **三分决策件复用**：`decision-guide-pipeline-dataflow-spark`（200 实测）同样裁决本章 9.5 的
  编排选型——每层用活动还是 notebook 还是独立 job，官方骨架+本机账（🔧E4）租户内定稿。
- **旧链化石**：`/fabric/data-engineering/concepts-mapping`、`how-to-ingest-data`、
  `transform-data-spark` 均实测 404（00 §9 禁引清单）——2024 出版时点的教程引文需全部重验。
- **工业实践画像** ⚠️（通识）：成熟租户的 medallion 收敛形态是"bronze 只追加+保留期、
  silver 单写入者（一表一作业）、gold 双环境（LTAP 报表位）"；常见败因=多写入者并发
  MERGE 同表与 gold 口径漂移，前者靠 03 章表级事务心智、后者靠 10 章发布门治理。
- **DP-700 旁证再引**：认证大纲把 lakehouse ingestion/preparation 列为独立考域（01 章已
 ⚠️ 弱证据登记）——与本章 9.2 步骤表结构性一致，可作章序合理性的人证级旁证 ⚠️。
