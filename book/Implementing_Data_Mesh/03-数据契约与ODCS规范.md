# 03 · 数据契约与 ODCS 规范——承诺的语法

> 主题重构册声明：本章章题为笔记作者编排，非原书目录（见 `00` §4）。本章特殊性：**规范文本本身可达**（ODCS 在 Perrin 名下 GitHub 仓库 ✅），故结构描述多为实证，仅"本书如何讲解"部分为 ⚠️ 重构。

## 3.1 契约是什么：从 SLA 话术到可执行工件

数据契约=**域对数据产品做出的一份可机读、可校验、可追责的承诺**。三句话定义其工程性质：

1. **可机读**：YAML/JSON 文件进版本库，不是合同 PDF 也不是 wiki 页面。
2. **可校验**：CI 与运行时能对"承诺 vs 实际"自动判卷（04 章执行线）。
3. **可追责**：契约有 owner、有版本、有变更流程——违约是事件不是玄学。

与相邻概念的分界：契约 ⊃ schema（结构只是其一层）；契约 ≠ API 合同（后者管调用形态，前者管数据含义）；契约 ≠ 政策（政策是治理侧输入，契约为其执行载体之一）。#201 术语表（其 00 §11）中"契约=schema+SLA+许可+政策的可执行承诺集"与此一致。

## 3.2 ODCS：作者自家标准的结构（✅ 规范仓库实抓）

Perrin 是 ODCS 主要推动者（Bitol 主席 ✅，`open-data-contract-standard` 仓库 ✅）。ODCS 契约文件的骨架（按 v3.x 公开规范 ✅，v2→v3 演进见本章末）：

| 段 | 关键字段 | 语义 |
|---|---|---|
| 头 | `version`（规范版本）、`name`、`id`（URN）、`status` | 契约自身身份与生命周期态 |
| 归属 | `owner`、`description`、`contact` | 追责三件套 |
| 模型 | `models[].fields[].type/primary/required/pattern/enum/min/max` | 结构与基础语义 |
| 质量 | `quality[].type/column/description`（SQL 表达式或规则引用） | 域内数据质量承诺 |
| 语义 | `models[].semanticId`、`terms[]`、字段级业务定义 | 跨域可对齐的含义锚点 |
| 信息 | `information[].key/value`（新鲜度、更新时间、SLA 等自定义） | 运维承诺槽位 |
| 合规 | `certificates[]`、`policy[]`、`unstructured_data[]` | 认证/政策/非结构化扩展 |

要点：**质量段允许嵌入可执行表达式**（SQL/正则），这是"联邦治理政策落到数据面"的机关——治理定义规则模板，契约实例化规则（07 章回收）。

## 3.3 契约三层：结构 / 语义 / 运维

- **结构层**：类型、非空、主键、值域——机器最勤快的一层。
- **语义层**：单位、口径、同义词（`temp_c` 是摄氏且已剔除仪器偏差）、`semanticId` 指向术语体系——**02 章 -999 教训的解药**。
- **运维层**：新鲜度（`freshness`）、可用性窗口、延迟预算——消费侧 SLO 的对偶。

实现排序建议（⚠️ 主题级）：先结构后语义再运维；但**气候/观测类域应语义先行**——单位错比空值错更贵。

## 3.4 契约与 schema 注册表的分工

Confluent/Spark 系 schema registry 管**兼容性**（向后/向前演进判定），不管**含义与质量**。成熟形态是双层：注册表守住字节级演化，契约守住承诺级演化；契约引用注册表 schema ID 而非复制之（防双主漂移）。参见 [设计数据密集型应用](../设计数据密集型应用/00-总览与阅读地图.md) 编码演化章的机制底座。

## 3.5 🔧 类比实验组（SQLite/DuckDB 本机实测，**非本书平台行为**）

**🔧-I 结构层承诺=约束即契约（SQLite）**：

```sql
CREATE TABLE readings(ts TEXT NOT NULL CHECK (ts GLOB '[0-9][0-9][0-9][0-9]-*'),
                     value REAL NOT NULL, CHECK (value BETWEEN -100 AND 100)) STRICT;
```

实测：合法行 `('2026-10-01', 21.5)` 入表；违约两行分别被拒：`CHECK constraint failed: value BETWEEN -100 AND 100` 与 `CHECK constraint failed: ts GLOB ...`（E3）。STRICT 表另拒类型漂移——**约束在写入点执行=契约的"左移"形态**。

**🔧-J 契约文件指纹（版本身份）**：把 3.2 骨架实例化为 JSON（`urn:dp:climate:obs:1`，含 min/max 质量段），`sha256[:16]` 实测 `87bcc56b76a69422`（E7）——契约文本+哈希=可发布、可比对的工件身份。

**🔧-K 运行时判卷（DuckDB 按契约规则扫描）**：候选表 3 行，契约规则 `temp_c IS NOT NULL AND temp_c BETWEEN -100 AND 100`，实测违约行 `[('S3',), ('S4',)]`（E7）——同一规则文本，写入点（🔧-I）与读取点（🔧-K）两种执行位置。

**🔧-L 规则复用=平台供给**：DuckDB `CREATE MACRO dp_quality(t) AS (t IS NOT NULL AND t BETWEEN -100 AND 100)` 后逐行判卷 `[('S2',True),('S3',False),('S4',False)]`（E8）——治理模板（宏）与契约实例（引用处）分离的最小类比。

## 3.6 契约写作反模式

- **复制粘贴 schema**：契约只抄列名列型——退化为 3.4 的注册表，白付维护成本。
- **无主契约**：缺 `owner/contact`——违约时找不到人，承诺形同虚设。
- **愿望清单契约**：把所有可能校验全开——首月违约率 90%，消费者学会无视警告，契约信用破产；按违约成本排序逐步收紧。
- **双源漂移**：契约手写一份、dbt/注册表再存一份而不互引——必分叉。

## 3.7 本章要点回写

1. 契约三性质：可机读/可校验/可追责；三层：结构/语义/运维。
2. ODCS 段结构（✅）给了"承诺"的标准语法，质量段可执行表达式是治理落数据面的机关。
3. 契约与 schema registry 是双层互补不是替代。
4. 🔧 实证：同一规则可在写入点（约束）与读取点（扫描）执行——执行位置决定违约成本。

## 3.8 契约实例（ODCS 风骨架，⚠️ 笔记作者重构示例，非原书文本）

气候观测产品 `obs-clean` 的契约文件最小可读形态（🔧-J 指纹即从此文件的规范化 JSON 计算）：

```yaml
version: "3.1"
kind: DataContract
name: obs-clean
id: "urn:dp:climate:obs:1"
status: active
owner: climate-team
description: 观测站日清洗温度观测（摄氏，已剔仪器偏差）
models:
  - name: observation
    fields:
      - name: station
        type: string
        required: true
        description: 观测站 WMO 编号
        quality:
          - type: regex
            description: "^[0-9]{5}$"
      - name: temp_c
        type: double
        required: true
        description: 日均气温，摄氏度
        quality:
          - type: sql
            description: "temp_c BETWEEN -100 AND 100"
      - name: obs_date
        type: date
        primary: true
information:
  - key: freshnessSLA
    value: "P1D"
  - key: lastUpdated
    value: "2026-10-01T06:00Z"
```

读法要点：`quality[].description` 里的 SQL 表达式就是 🔧-K 运行时判卷的同一文本；`information[]` 是自由槽位（新鲜度/更新时间/内部账单价都可放）；`status` 供 04 章状态机消费。**同一份文件同时是：域的产品说明书、CI 的测试规格、目录页的数据源**——三用一件，反之为三件分开维护=3.6 双源漂移反模式。

## 3.9 契约字段速查（写契约时的十项自检）

1. `id` 是否 URN 且含版本槽；2. `owner/contact` 是否指到团队而非个人邮箱；3. 每个字段是否有业务 `description`（非列名复读）；4. 单位是否进语义（temp_c 的 c）；5. 缺测表示法是否声明（NULL 还是哨兵值）；6. 主键/唯一性是否声明；7. 值域上下界是否进 quality；8. 新鲜度 SLA 是否在 information；9. 兼容性策略（允许哪些变更）是否记录；10. 指纹是否发布到消费端可校验处。

## 相关阅读

- 上游：[Data_Mesh/03-数据即产品原则](../Data_Mesh/03-数据即产品原则.md)、[Data_Mesh/10-数据产品设计-提供消费转换](../Data_Mesh/10-数据产品设计-提供消费转换.md)
- 本册：`04` 契约的执行与演化 → `07` 政策即代码
- 机制底座：[设计数据密集型应用/00](../设计数据密集型应用/00-总览与阅读地图.md)

## 核心概念速览（中英对照）

| 英文 | 中文 | 一句话 |
|---|---|---|
| data contract | 数据契约 | 可机读/可校验/可追责的承诺工件 |
| ODCS | 开放数据契约标准 | Bitol 线规范，Perrin 主导（✅） |
| semantic layer (of contract) | 契约语义层 | 单位/口径/semanticId |
| quality expression | 质量表达式 | 契约内可执行校验规则 |
| schema registry | 模式注册表 | 管兼容性演化，与契约双层互补 |
| contract fingerprint | 契约指纹 | 文本哈希=工件身份（🔧-J） |
| left-shifted validation | 左移校验 | 在写入点执行约束（🔧-I） |
| unowned contract | 无主契约 | 缺 owner 的反模式 |

## 最新演进与工业实践

- **ODCS 版本线（✅ jgp.ai 博文标题实抓）**：2025-12-11 v3.1.0（relationships、更丰富元数据、更严校验）；2026-06 v3.2 与 ODPS v1.1 联动（"让 AI 看懂你的数据"）——契约标准正与 LLM 元数据消费场景合流。
- **规范互认**：`datacontract-specification`（datacontract.com 社区线）与 ODCS 并存竞争，字段命名与质量段语法互有借鉴（作者 awesome 清单 ✅ 收录双方生态）；选型时注意本书以 ODCS 系谱为主 ⚠️。
- **工具面**：契约校验 CLI/CI 模板（`data-contract-template` 仓库 ✅）2024 年后进入 GitHub Actions 常规化集成。
- **本册口径**：ODCS 结构段为规范仓库一手 ✅；"本书第 N 章讲契约"级别的对应关系不可达 ⚠️。
