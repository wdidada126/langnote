# 05 笔记本与 Spark 活动集成 — Notebook & Spark Activities（⚠️ 重构章，非原书 TOC）

> 章题为 ⚠️ 推定重构（00 §2）；机制 = 官方文档转述 ⚠️ + ✅ URL；Fabric/Spark 平台本机不可实测（⚠️），
> 零新装纪律下 pyspark 不装（波6 #215 先例沿用），代码优先概念以 SQLite/DuckDB 轻类比标注 🔧。

## 5.1 代码优先活动家族（⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity` ✅ F5、
`https://learn.microsoft.com/en-us/fabric/data-factory/spark-job-definition-activity` ✅ F6。

- **Notebook 活动**：管道中运行 Fabric 笔记本（Spark 内核），传参、取输出、接依赖边——
  FDF 编排与数据工程代码资产的**主接缝**（✅ F5 主题）。
- **Spark job definition 活动**：不跑整本笔记本、只提交**已发布的 Spark 作业定义 item**——
  「库函数级」粒度，比笔记本更可单测/可复用（✅ F6 主题）。
- 两者并存的意义 ⚠️ 编者评述：笔记本=交互式资产自动化，作业定义=工程化资产编排化；
  Playbook 成熟度阶梯正是从前者走向后者。
- 其他转换活动（存储过程、Web/Azure Function 类 ✅ ADF 同族 A3 目录；FDF 支持面 ⚠️ 认 F2）
  本章不展开，登记于 11 章决策树叶子。

## 5.2 参数与输出的跨对象流动（02 章动态内容的延伸）

- 管道参数 → 笔记本微单元格参数（`mssparkutils.notebook.run` 类调用参数语义 ⚠️ 以 Fabric
  笔记本现行文档为准，本册未验专页）；笔记本返回值 → 管道变量 → 下游活动输入——
  形成「编排层状态机 + 计算层事务」的双层结构 ⚠️。
- 剧本模板 ⚠️ 编者归纳：笔记本内**只做计算与断言**，把「下一步去哪」的决策以返回值
  （状态码/计数）交还管道——逻辑混写的笔记本无法被 09 章监控定位。
- 失败语义透传：笔记本非零退出/异常 → 活动 Failed → onFailure 边接管（02 章 2.3 三件套
  在代码侧的对应面）。

## 5.3 与 Lakehouse 表的协作面（06 章前置 ⚠️）

- 笔记本/Spark 作业读写 Lakehouse 表（Delta 语义）是 FDF 剧本的默认转换执行方式（✅ F1
  概览主题延伸 ⚠️）；表格式机制纵深不在本册，指向盘上湖仓格式册群（5.6）。
- 「copy 落暂存 → Spark 收编成表」两段式（03 章 3.6）中，本章活动就是第二段 executor。
- 小文件治理：微批高频落地后 Spark 侧 compaction（合并小文件）作为独立子管道剧本，
  定时/事件触发（03 章 🔧E4 的 450 字节教训在平台规模下的放大版 ⚠️）。

## 5.4 选型：Notebook 活动 vs Spark job definition 活动 vs SQL（⚠️ 编者决策表）

| 场景 | 首选 | 理由 |
| --- | --- | --- |
| 探索期清洗逻辑 | Notebook 活动 | 迭代快，业务可见 |
| 稳定核心转换 | Spark job definition | 可单测、粒度小、复用清晰 |
| 纯集合运算/口径层 | SQL（存储过程/Warehouse 侧 ⚠️） | 优化器托管、审计面成熟 |
| 跨源重逻辑（UDF/算法） | Spark 作业 | 代码资产全能力面 |

- 与 04 章 4.1 表拼齐：无代码/SQL/笔记本/作业定义四级——「reliable pipelines」（副题 ✅）
  的选型地图完整；每升一级，可测试性↑、业务自维护性↓。

## 5.5 🔧 概念类比（轻量，非 Fabric 平台行为）

- 「管道传参给计算单元、取回状态码」的单机最小实现：python 调度 sqlite3 依次执行
  建表→装载→`PRAGMA integrity_check` 并据返回决定下一步——对应 5.2 双层结构
  （编排层状态机/计算层断言）。SQLite 3.45.3 内置零新装；无并发作业队列、无 CU 计量
  （**非 Fabric 平台行为**）。
- 03/07 章的 E1/E3 已分别实证「搬运段」与「MERGE 收编段」，本章活动即平台里把两段
  缝起来的针——三段合看就是完整 bronze→silver 剧本（11 章终章串联）。

## 5.6 与 repo 其他书的联系

- 波内登记（不链）：#191《The Data Engineer's Guide to Microsoft Fabric》与本 5.1/5.4
  重叠度全书最高（数据工程视角的笔记本/Spark 纵深），分工：本册管「编排怎么挂」，
  它管「代码怎么写」（写检日盘上无目录，主代理波尾总表裁决互挂）。
- Spark 阵营教材（盘上实链，ls 验名 ✅）：
  [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)、
  [../Apache_Spark_2_Data_Processing/00-总览与阅读地图.md](../Apache_Spark_2_Data_Processing/00-总览与阅读地图.md)。
- Delta/表格式机制：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) ✅；
  Fabric 侧 Lakehouse 组件浅层：[../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md](../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md) ✅（ls 验名）。
- 湖仓计算引擎中立理论：[../Practical_Lakehouse_Architecture/05-湖仓架构的计算引擎.md](../Practical_Lakehouse_Architecture/05-湖仓架构的计算引擎.md) ✅。

## 5.7 笔记本返回值契约示例（5.2 纪律的具象 ⚠️ 编者示例，非书中代码）

```
# notebook 末尾单元格约定（伪码示意）
return {
  "status": "partial",            # success | partial | failed
  "rows_in": 120400,
  "rows_out": 120310,
  "rows_quarantined": 90,         # 04 章隔离表计数
  "max_watermark_seen": "2026-09-30T23:58:00Z"  # 07 章「用数据里的水位」
}
```

- 管道侧：契约字段缺失的返回不算成功——09 章数据层告警直接消费此 JSON 的计数列。
- 契约三禁 ⚠️：禁只回 True/False（丢隔离信息）、禁回时钟值（防漂移）、禁把日志当返回值
  （排障走 F4 钻取，02 章 2.4）。

## 5.8 本章自测（答案均在上文 ⚠️ 编者）

1. Notebook 活动 vs Spark job definition 活动的成熟度阶梯怎么排？（5.1/5.4）
2. 「双层结构」指哪两层？参数与状态各怎么走？（5.2）
3. 「copy 落暂存 → Spark 收编」两段式里本章占哪段？（5.3）
4. 小文件 compaction 为什么值得做成独立子管道？（5.3，03 章 🔧E4 教训）
5. 四级转换选型地图中，纯集合运算首选什么？（5.4：SQL 档）
6. 返回值契约三禁是什么？（5.7）
## 5.9 一页小结卡（背卡式 ⚠️ 编者）

- 接缝：管道 ↔ 代码资产 = Notebook / Spark job definition 两活动（✅ F5/F6）。
- 阶梯：笔记本（快）→ 作业定义（稳）；核心转换逐级上移。
- 契约：status / rows_in / rows_out / rows_quarantined / max_watermark 五字段。
- 两段式：copy 暂存 + Spark 收编；compaction 独立子管道。
## 核心概念速览（中英对照）

- **笔记本活动** — Notebook activity：管道内运行 Fabric 笔记本的接缝活动（✅ F5）。
- **Spark 作业定义活动** — Spark job definition activity：提交已发布 Spark 作业 item（✅ F6）。
- **双层结构** — 编排状态机 + 计算断言：参数下行、状态上行（5.2 剧本模板 ⚠️）。
- **成熟度阶梯** — 笔记本→作业定义：Playbook 化程度标尺 ⚠️ 编者评述。
- **两段式收编** — copy 暂存 + Spark 成表：03 章 3.6 的第二段 executor（⚠️）。
- **小文件 compaction** — 文件合并子管道：定时/事件触发的独立剧本（5.3）。
- **四级转换选型** — 无代码/SQL/笔记本/作业定义：与 04 章拼齐的选型地图（5.4）。
- **失败透传** — 异常→Failed→onFailure：代码侧与 02 章三件套的对应面 ⚠️。

## 最新演进与工业实践

- **Fabric Spark 资产化**（⚠️ 转述方向，URL 面：✅ F6 专页存在本身即信号）：Spark job
  definition 作为独立 item 进入 Git 集成与部署管线对象清单（08 章联动），「作业即资产」
  是 2025–2026 文档线的明确趋势；复核入口 F6 现行页。
- **Copilot 写代码面**：Fabric 的 Copilot 家族（✅ F9 为 DF 侧页）向笔记本/SQL 延伸的口径
  以现行文档为准 ⚠️，本册不预测边界。
- **工业实践**：①核心转换的笔记本必须配「返回值契约」（成功/部分成功/隔离行数三件套），
  否则 09 章监控只能看到绿/红两色 ⚠️ 编者归纳；②作业定义单测放 CI（08 章剧本第 4 步）；
  ③pyspark 本地环境属重资产，团队普遍以「Fabric 内测试 + 本机 DuckDB 语义预演」替代
  （本册零新装纪律同款取舍，🔧 5.5）。
- **本机互鉴** 🔧：5.5 的 sqlite3 调度类比 + 03/07 章实验即可在单机讲透「编排-计算接缝」，
  无需真 Spark（**非 Fabric 平台行为**）。
