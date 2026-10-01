# 03 Copy Job 与连接器：数据移动 — Copy Job & Connectors（⚠️ 重构章，非原书 TOC）

> 章题为 ⚠️ 推定重构（00 §2）；机制 = 官方文档转述 ⚠️ + ✅ URL；🔧 两处本机实验（DuckDB 1.5.5 /
> SQLite 3.45.3）**仅为 Copy/连接器概念类比，非 Fabric/Data Factory 平台行为**；脚本输出实抓于
> `D:\develops\tmp\dbwave_w9_fdfab\exp_out.txt`。

## 3.1 Copy 的两副面孔：活动 vs 独立 Job（⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/fabric/data-factory/what-is-copy-job` ✅ F7、
`https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview` ✅ A2。

- **Copy activity**：管道内活动，吃参数、走依赖边、可嵌套——编排优先（02/07 章主场）。
- **Copy job**：FDF 中可脱离管道单独创建/运行/监控的**声明式数据移动 item**（✅ F7 标题即
  「What is Copy job in Data Factory」）——「我只想每天把 X 搬到 Y」的最短路径，
  官方入门教程（✅ F8）第一幕就是它。
- 剧本选择规则 ⚠️ 编者归纳：纯搬运 + 计划触发 → copy job；搬运前后有判断/转换/审计 →
  管道内 copy activity；两者可同厂共存，别为「统一」把 copy job 强行管道化。
- 语义内核同源：源数据集（dataset/sink 配置）→ 映射（列名/类型）→ 暂存与复制设置
  （staging、分区、DIU 类概念在 FDF 的支持面 ⚠️ 以现行文档为准）。

## 3.2 连接器（Connectors）：移动面的「接口表」

权威页：`https://learn.microsoft.com/en-us/fabric/data-factory/connector-overview` ✅ F3。要点 ⚠️：

- 连接器清单与「源/仅 sink/双向」能力矩阵以 F3 现行页为准——**引用连接器能力前必查矩阵**，
  同一连接器在 ADF 与 FDF 的支持级别可能不同（F2 compare 页联动）。
- 认证面：账号/服务主体/托管身份等凭据形态 ⚠️；Fabric 项的权限与工作区角色耦合（08 章
  部署时凭据不随包走，需重绑——剧本坑位先登记）。
- 关系型源常用「数据库快照式」读取；变更捕获（CDC 类）能力面 ⚠️ 本册未验到专页 URL，
  增量方案见 07 章水位线剧本（不依赖平台 CDC 的最小公分母写法）。

## 3.3 🔧 实测 E1：Copy 的落地形态——分区 Parquet（非 Fabric 行为）

DuckDB 1.5.5 单机模拟「copy = 带映射的读取 + 按列分区落地」：

```
$ python  # exp_out.txt 实抓
=== T1 Copy job 类比：CSV -> 分区 Parquet（COPY ... PARTITION_BY）===
files: ['order_date=2024-01-05', 'order_date=2024-01-06', 'order_date=2024-01-07']
=== T1 修正校验：分区 Parquet 直读（此前 glob×read 交叉连接计数虚高）===
order_date  n      s
2024-01-05  2 200.50
2024-01-06  1  45.25
2024-01-07  1 300.00
```

- 4 行 CSV 经 `COPY orders TO 'exp/pq' (FORMAT PARQUET, PARTITION_BY (order_date))` 落成
  Hive 式目录——这就是 copy sink「按列分区写出」的可视化本质 ⚠️ 类比。
- **自纠插曲（取证诚实）**：首版校验查询写成 `FROM glob(...), read_parquet(...)` 交叉连接，
  计数虚高为 6/3/3；改为纯 `read_parquet` 后 2/1/1 与源数据吻合——对应工业场景
  「复制完成行数对账」必须用**同一口径**读目标端，glob 文件数 × 行数是最常见的假性差异 ⚠️。

## 3.4 🔧 实测 E4：连接器类比——SQLite 异构源直读（非 Fabric 行为）

python 内置 sqlite3（3.45.3）造 3 行 events 表，DuckDB `ATTACH 'exp/src.sqlite' AS src (TYPE SQLITE)`：

```
=== T4 SQLite ATTACH：异构源接入（连接器类比，sqlite 由 python 内置生成）===
 kind  n
  buy  1
click  2
buy.parquet bytes: 450
```

- 「ATTACH 即注册连接器、跨库 SELECT 即 copy 读取、COPY TO 即 sink 写出」——三步在单机
  复现了 FDF copy 的骨架；**真实平台在此之间还插入了执行层/凭据/限流/重试**（DuckDB 全部
  没有，**非 Fabric 平台行为**，数字不可换算）。
- 迁移类比：`buy.parquet 450 字节` 提醒「小文件成本」在哪个世界都存在——FDF 端表现为
  OneLake 存储与下游扫描放大（06/10 章各回收一次）。

## 3.5 映射与类型系统：copy 的「翻译官」条款（⚠️ 转述）

- 列映射三态 ⚠️（✅ A2 语义族）：同名自动映射 / 显式映射表 / 按位序——剧本纪律：**生产
  管道永远显式映射**，源端加列时自动映射的静默错位是 ETL 事故经典 Top3。
- 类型宽化/窄化与日期时区：源列类型 → 目标列类型的转换矩阵各连接器不同 ⚠️（F3 矩阵页），
  跨时区日期建议全程 UTC 落湖、展示层再转（06 章分区键建议联动）。
- 架构漂移（schema drift）应对 ⚠️：copy 层「宽容落bronze + 校验在silver」两段式，
  与 05 章 notebook 校验、09 章监控告警构成三角防线。

## 3.6 何时不用 Copy（边界剧本）

- 源即湖仓表且同引擎可达 → 直接 SQL/Spark 写（05 章），copy 绕一圈徒增暂存成本 ⚠️。
- 需要行级 upsert 语义 → copy 只负责「搬进暂存」，落地交给 MERGE 剧本（07 章 🔧E3）。
- 高频小批 → 攒批再 copy（对齐 3.4 小文件教训）；事件驱动到达即搬只在「迟到敏感」场景值得 ⚠️。
- SSIS 包 → 不是「一个 copy 活动」能替代的，走 11 章迁移剧本第 2 幕。

## 3.7 与 repo 其他书的联系

- OneLake 落地与快捷方式：本目录 [06 章](06-OneLake与湖仓落地.md)；平台中立侧的存储分层理论
  实链 [../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)（ls 验名 ✅）。
- Fabric 全景浅层：[../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md](../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md) ✅、
  OneLake 组件面 [../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md](../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md) ✅（写前 ls 验名）。
- 波内登记（不链）：#218/#191/#217/#219；#191 若含 copy 性能细节，与本册 3.1「复制设置 ⚠️」
  互为深浅两档。

## 3.8 Copy 排障三问（值班口袋卡 ⚠️ 编者）

1. **口径问**：对账差异是真差异还是读法差异？（🔧E1 自纠：glob×read 交叉连接虚高 6/3/3
   vs 直读 2/1/1——先统一口径再立案）
2. **映射问**：源端加列了吗？显式映射还是自动映射？（3.5：自动映射的静默错位）
3. **形态问**：该用 copy job 还是管道内 copy activity？（3.1：纯搬运 vs 有前后逻辑）

- 三问都否 → 升级查 F3 连接器矩阵与 F2 差异表（01 章「查表不查记忆」条款）。
## 核心概念速览（中英对照）

- **复制活动** — Copy activity：管道内数据移动活动，ADF 语法同源（✅ A2）。
- **复制作业** — Copy job：FDF 独立声明式搬运 item，免管道最短路径（✅ F7）。
- **连接器** — Connector：源/目标两侧的能力矩阵单元（✅ F3），支持面 ADF≠FDF ⚠️。
- **暂存** — Staging：跨环境复制的中转落地层（支持面 ⚠️ 以现行文档为准）。
- **列映射** — Column mapping：同名/显式/按位三态；生产必显式（3.5 纪律）。
- **架构漂移** — Schema drift：源端列变化；bronze 宽容 + silver 校验两段式 ⚠️。
- **Hive 式分区** — Partitioned landing：`order_date=…` 目录形态（🔧E1 实证）。
- **小文件税** — Small-file cost：高频小批落湖的存储/扫描双输（🔧E4 450B 文件类比）。
- **行数对账口径** — Row-count reconciliation：目标端同口径直读，防交叉连接虚高（🔧E1 自纠）。

## 最新演进与工业实践

- **口径演进**（✅ F3/F7 现行页，机制 ⚠️）：连接器矩阵与 copy job 能力面逐月扩张是 Fabric
  文档 2025–2026 的常态节奏；本册所有「支持/不支持」表述均带取证日 2026-10-01 戳，过期先复核。
- **开放格式落地**：copy 直写 Delta/Iceberg 语义的支持面在演进中 ⚠️（未验专页不展开），
  工业界当前主流仍是「copy 落 parquet/暂存 → 表格式层收编」两段式（对照
  [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) 的格式中立叙事 ✅）。
- **工业实践**：①把 3.5 显式映射做成模板化 dataset 参数（07 章联动）；②对账剧本标配
  「源 count vs 目标 count vs 校验和」三层（🔧E1 自纠的直接教训）；③copy job 与 copy activity
  双轨时，在命名前缀上强制区分（`cj-` / `pa-`）⚠️ 编者归纳。
- **本机互鉴** 🔧：E1/E4 脚本 20 行内可复跑（见 `dbwave_w9_fdfab\`），是讲「copy 本质」时
  成本最低的教具（再次标注：**非 Fabric 平台行为**）。
