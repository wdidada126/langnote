# 第 9 章 湖仓架构：Medallion 分层设计

> 原书第 9 章「Architecting Your Lakehouse」。medallion（青铜/白银/黄金）是 Databricks 提出的
> 数据分层法，本章把它落到 Delta 的表能力上。本文件按「**每层的契约 → 层间流转 → 治理与成本**」重写。
> SQL/伪代码为**自拟教学示意，非书中原文**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 为什么分层 | 混层仓库的三大病灶 | 分层 = 给不同角色不同真相 |
| 9.2 Bronze 契约 | 不可变、源格式保真、只追加 | 重放能力的来源 |
| 9.3 Silver 契约 | 清洗、去重、实体统一、CDC 语义 | 唯一的「业务真相层」 |
| 9.4 Gold 契约 | 面向消费域的聚合/宽表 | 为 BI/AI 的读模式优化 |
| 9.5 层间技术映射 | 每层用 Delta 的什么特性 | 特性选错 = 架构塌方 |
| 9.6 组织视角 | 数据域 × 层的矩阵、DLT | 层是技术手段，域是组织手段 |
| 9.7 成本与保留 | retention/VACUUM/分层存储 | bronze 最便宜、gold 最贵 |

## 核心精讲

### 9.1 分层的动机（先讲病灶再讲名词）

不分层的湖 = 「所有读者共享同一堆原始文件」：上游 schema 一变全楼崩塌；测试脏数据混进报表；
审计要求保原始、BI 要求清洗后，两种需求在同一张表上不可能同时满足。
**medallion 的本质是把「保真」与「可用」解耦到不同层，各自演化。**

```text
sources ──> bronze ──(清洗/去重/关联)──> silver ──(聚合/建模)──> gold ──> BI / ML / 共享
            原始留痕                      实体真相                  消费视图
```

### 9.2 Bronze：原始留痕层

设计契约（原书反复强调）：

- **只追加、不可变**：`delta.appendOnly = true` 直接写进表属性，防手滑 UPDATE。
- **schema 保真**：源系统长什么样存什么样（Kafka 消息原文、CDC envelope 原样），
  解析失败进 `_corrupt_records` 列而不是丢行。
- **保留期 = 重放需求**：存 1–10 年常见；logRetention/deletedFileRetention 都设大
  （反正 appendOnly 几乎没有 VACUUM 对象）。
- 表属性示例（教学示意）：

```sql
CREATE TABLE bronze.kafka_orders (value STRING, topic STRING, partition INT, offset LONG, ts TIMESTAMP)
USING DELTA TBLPROPERTIES (delta.appendOnly = true,
  delta.logRetentionDuration = '3650 days', delta.deletedFileRetentionDuration = '400 days');
```

### 9.3 Silver：实体真相层

- 内容：类型化 schema、去重后的业务实体、跨源统一命名；**允许 UPDATE/MERGE/CDF**。
- 关键技巧（对应前几章机制）：
  - 去重：批内 `ROW_NUMBER()` + MERGE（第 6 章文件 7.2）；
  - CDC 捕获：开 **CDF**，下游直接消费变更而非自己 diff；
  - SCD2 维度：MERGE 实现历史化（第 10 章文件专讲）；
  - 分区策略：事件时间列 + 生成列，避免手填。
- silver 是「唯一可信」的兑现层：质量期望（新鲜度、完整性）应在此层显式度量（对照
  [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)）。

### 9.4 Gold：消费视图层

- 形态：聚合事实（daily_revenue）、宽表（customer_360）、特征表（ML features）。
- 优化取向完全偏读：Z-ORDER/liquid by 高频连接键、预聚合、甚至物化成 Delta 共享对象（第 12 章文件）。
- gold 允许「多份冗余」——按消费域复制聚合结果是正常的，与仓库范式化直觉相反。

### 9.5 层 × Delta 特性映射表（本章的考试重点）

| 特性 | bronze | silver | gold |
| --- | --- | --- | --- |
| appendOnly | ✅ 常开 | ❌ | ❌（除非快照发布制） |
| MERGE/UPDATE | ❌ 不需要 | ✅ 核心 | 视口径 |
| CDF | 可选 | ✅ 建议开 | 可选（对外供数） |
| DV | 无意义（不删） | ✅ DML 高频受益 | 视读放大权衡 |
| 分区 |  ingestion 日期/来源 | 业务事件日期 | 消费查询键（常 liquid/Z-ORDER） |
| VACUUM retention | 长（1 年+） | 7 天基线 | 按下游停摆窗口放大 |
| 时间旅行 | 很少用 | 常用（修数对照） | 发布前冻结（SHALLOW CLONE） |

### 9.6 组织视角：层是手段，域是结构

- **数据域 × 层矩阵**：orders 域、clickstream 域各自走完 bronze→silver；
  gold 按消费域（finance/marketing/product）跨域组装——避免「单一大银层」变成新瓶颈。
- **DLT（Delta Live Tables）/ 🔧 Lakeflow**：声明式管道（预期状态 + 质量规则 + 依赖图），
  把 medallion 从「约定」变成「编译器」：自动重试、编排、血缘。原书以 DLT 讲部署，思想同构于
  [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md) 的质量契约。
- 团队分工：bronze 属平台组、silver 属数据工程/域团队、gold 属分析工程——
  **层的边界就是团队交接面**（Conway 定律在数据栈的再现）。

### 9.7 成本与保留的算术

- 层间数据量单调递减（bronze 含全部历史与噪声，gold 只含结论）：
  **存储成本大头在 bronze，计算成本大头在 silver→gold 的加工**。
- bronze 用低频访问存储 + 长保留；gold 全热 + 短历史（可从 silver 重建，历史版本价值低）。
- 重跑策略：silver 以下「可全量重建」（bronze 是真相备份），gold 层「增量刷新」——
  这个不对称决定了各层的 VACUUM/CDF/克隆配置。

## 版本演进

| 时间 | 事件 |
| --- | --- |
| 2020 | Databricks 提出 medallion 术语（blog + 白皮书） |
| 2021–2023 | DLT GA：管道即代码、质量约束内建 |
| 🔧 2024–2025 | DLT 演进为 Lakeflow（统一编排品牌）；materialized views 承接部分 gold 层职责 |

## 文献与文档

- Databricks *The Medallion Architecture* 白皮书/文档（层级定义原口径）。
- Databricks docs *Delta Live Tables / Lakeflow*。
- 《What is the Medallion Architecture?》（Denny Lee 等历次演讲与本书第 9 章互为表里）。
- 对照：Kimball 维度建模在 gold 层的适用性（[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)）。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「bronze 洗一洗更干净」 | bronze 的价值恰恰是脏且真；清洗放 silver |
| 2 | 「三层必须都存在」 | 小团队可两层起步，但「保真/可用分离」的契约不能省 |
| 3 | 「gold 能回写到 silver」 | 单向数据流是纪律；回写让血缘与重建逻辑崩坏 |
| 4 | 「medallion = 批架构」 | 每层都可以流式（第 6 章文件 7.5）；层是逻辑契约不是调度周期 |
| 5 | 🔧 「DLT 是唯一实现方式」 | Airflow/Dagster + 纯 Delta SQL 同样能落 medallion；DLT 只是把纪律产品化 |

## 与其他章 / 其他书的联系

- ← `06`：层间流转的流式实现；← `07`：CDF/DV 在 silver 的落位。
- → `10`：silver→gold 的聚合与维度建模性能；→ `11`：层间授权模型（ bronze 不给 BI 授是 UC 默认姿势）。
- → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)：Kappa 与 medallion 的对照。
- → [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)：质量规则的分层部署。
- → 《Engineering Lakehouses with Open Table Formats》精读：**待建**（该书对分层与多格式管道有更工程化的展开，建成后与本章互链）。
