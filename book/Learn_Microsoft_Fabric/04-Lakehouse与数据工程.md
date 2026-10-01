# 04 · Lakehouse 与数据工程 —— Learn Microsoft Fabric（⚠️ 主题重构章）

> **降级声明**：原书目录未获任何渠道实证（负结果台账见 [00 · 总览与阅读地图](00-总览与阅读地图.md) §2），本章为主题重构章。
> 机制 = 官方文档转述 ⚠️（✅ <https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview>，2026-10-02 验 200）；
> 🔧 本机 DuckDB 类比，**非 Fabric 平台行为**。兄弟册同题：
> [../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md](../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md)（不同书，辨析见 00 §3）。

## 1. 本章定位

- Lakehouse item = 数据工程师的主工作台：文件（Files）+ 表（Tables）双面孔，表即 Delta 事务表
  （⚠️ 转述）。教学书在此章通常完成读者第一个「从原始文件到可信表」的闭环（⚠️ 推定）。

## 2. 表与文件的两副面孔（⚠️ 转述官方 lakehouse-overview）

- **文件面**：湖项内可上传/浏览原始文件（CSV/JSON/Parquet…），笔记本与管道都按路径直读——
  保留数据湖的开放性。
- **表面**：托管表（managed）由平台维护 Delta 事务日志；另有外部表（externally managed）
  指向湖内/湖外的开放表（Iceberg/Hudi/Delta）——治理边界不同（⚠️ 转述，细则当日页核实）。
- SQL 端点：湖项自带 T-SQL 只读端点（查表不建表），让 SQL 人群零门槛进入 Delta 世界（⚠️ 转述）。
- 与 Spark 面：笔记本即 Spark 运行时消费这些表——语言与 API 细节在 [08 章](08-Notebooks与Spark工作负载.md)（⚠️ 转述）。

## 3. Delta 底座的事务语义

- ACID、Time Travel、`OPTIMIZE` 式整理在 Fabric 多以托管/自动形态出现——用户看到的行为是
  「读快照一致 + 后台整理」，而非手写维护命令（⚠️ 转述；命令面是否开放随版本变动，不写死）。
- 理论纵深（盘上实链）：[../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)——
  事务日志、VACUUM、Z-Order 的**开放 Delta** 语义全集；Fabric 是其厂商裁剪面。
- Iceberg 张力：湖原生表走 Delta、互操作层给 Iceberg——「一份数据两种元数据」的路线图判读见
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)（⚠️ 推定提醒）。

## 4. 小文件问题与整理（🔧 本机类比，非 Fabric 行为）

```text
E2 小文件代价类比（DuckDB 1.5.5 + 1,000,000 行事件数据，2026-10-02 实测）：
  切成 20 个碎片 Parquet（按 seq 区间 COPY，BETWEEN 端点重叠 → 总行数 1,000,019）
  多文件视图扫描 count(*)：2.2ms
  单文件扫描 count(*)：0.9ms（≈2.4× 元数据/文件打开开销差）
  注：本机文件缓存热态下差距已压缩；冷存储对象存储上差距会放大（文件数=请求数）。
（类比仅演示「文件碎片放大固定开销」；Fabric 的自动 compaction 策略为平台行为，本机不可测 ⚠️）
```

## 5. 快照与时间旅行（🔧 本机类比，非 Fabric 行为）

```text
E3 Delta 快照语义类比（DuckDB + Parquet 双版本 + manifest 指针，2026-10-02 实测）：
  snap_v1（500,000 行） / snap_v2（追加至 1,000,000 行）
  manifest.json 记录版本→文件指针；as-of-v1 查询：1.0ms → 500,000 行, min(seq)=0
  v2 追加后 v1 文件不动：不可变基文件 + 指针前移 = 时间旅行的最小实现
（类比仅演示「版本=指针」结构；Fabric/Delta 的事务日志并发控制、冲突重试本机未覆盖 ⚠️）
```

- 迁移结论：把「读旧版本」理解为**元数据指针选择**而非数据复制，就同时理解了 Delta、
  OneLake 快照、以及 05 章仓库列存分层的代价结构。

## 6. 分层建模：Medallion 教学位（⚠️ 转述社区/微软通用范式）

- Bronze（原样落地）→ Silver（清洗/标准化）→ Gold（业务聚合）：Fabric 教学书的标准项目骨架；
  每层落湖表、层间用笔记本/管道推进（⚠️ 转述；微软官方范式名，是否本书章内小节 ⚠️ 推定）。
- 与 Kimball 星型的相处：Gold 层常直接是星型/宽表——方法论祖谱见
  [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)；
  湖仓时代「谁定义一致性」之争对读 [../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)（⚠️ 推定提醒）。
- 工程守则（⚠️ 重构）：同表禁多写入者混用引擎（Spark 写入 + T-SQL 并发 ALTER 的边界要先查
  当日文档再下结论——本目录不给未实证承诺）。

## 7. 上手机 checklist（⚠️ 重构练习位）

1. 建湖项；上传样例 CSV 到 Files；用笔记本 `spark.read` 与 SQL 端点各读一次同一 Delta 表。
2. 观察 `Files` 里表目录的分区/日志文件形态（对照 🔧 E2 的碎片直觉）。
3. 做一条 Bronze→Silver 管道；跑两次验证幂等；查版本历史读旧快照（对照 🔧 E3）。
4. 用外部表挂载一个湖外 Delta/Iceberg 目录，记录与托管表的权限/维护差异。

## 8. 本章在盘上目录版中的对位

- 兄弟册 04 章（Delta 生态选型视角）↔ 本章（动手/类比视角）；引用请分别注明册别（00 §3 辨析表）。
- Hudi/Paimon 对照：[../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)、
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。
- Spark 引擎层：[../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md)（RDD/ shuffle 机理，本册 08 章够用即可）。
- 索引：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 9. 教学 FAQ（重构问答位，⚠️ 非原书）

- **问：同一个 Gold 表，Spark 写完想用 T-SQL 改一列，安全吗？**
  答：跨写入者的元数据竞态取决于平台对并发 DDL 的处置——先在测试湖项做双引擎交替写压力
  实验再上生产；本册不给未实证的「可以/不可以」（⚠️ 纪律）。
- **问：托管表和外部表怎么选？** 判据三问：谁负责 compaction？谁负责保留期？迁移时带走
  什么？托管=平台全责+高集成，外部=自持文件+跨工具可携（⚠️ 转述+重构）。
- **问：分层一定要三层吗？** 答：Bronze 是审计资产不是仪式；小项目可 Silver 起步，但**必须在
  目录里写明缺层理由**，否则半年后无人敢删（⚠️ 重构共识）。

## 10. 边界诚实声明

- 未逐条实证项：湖表维护命令开放面、自动整理的触发策略、外部表支持格式全集——
  一律当日查 ✅ lakehouse-overview（2026-10-02 验 200）并与 Delta 专册交叉。
- 🔧 E2/E3 的适用边界：只演示「文件数放大开销」「版本=指针」两件事；Delta 的事务日志
  并发控制、冲突重试、Z-Order 效果均未在本机覆盖（非本书平台行为）。

## 11. 章末自测（重构题，⚠️ 非原书习题）

1. 画出 Files 面与 Tables 面各自的消费者（人/笔记本/SQL 端点/镜像目标）。
2. 用小文件代价实验数字（2.2ms vs 0.9ms）推导：对象存储上 200 个碎片文件的扫描会发生什么。
3. as-of 读旧快照的三种用途（审计回放/训练可复现/误删对账）各配一个项目场景。
4. 写出「表清单+分层归属+写入者唯一性」三列矩阵骨架（§6 工程守则的交付化）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 湖仓项 | Lakehouse item | 文件+事务表双面孔容器 |
| 托管表 | managed table | 平台维护事务日志的 Delta 表 |
| 外部管理表 | externally managed table | 指向开放表的治理别名 |
| SQL 端点 | lakehouse SQL endpoint | 只读 T-SQL 进湖大门 |
| 事务日志 | transaction log (Delta) | 快照/时间旅行的元数据底座 |
| 小文件 | small file problem | 文件数放大请求与固定开销 |
| 整理 | compaction/OPTIMIZE | 碎片归并的维护动作 |
| 分层 | medallion (bronze/silver/gold) | 湖仓项目分层范式 |

## 最新演进与工业实践

- 文档域信号：湖仓相关页在 2025–2026 已迁至 `data-engineering` 路径（✅ 本页 2026-10-02 验 200；
  旧路径 /fabric/data-science/lakehouse-overview 已 404——波 5 册 00 §7 化石清单可互证）——
  信息架构重组本身记录了「湖仓从 ML 附庸到数据工程主业」的定位迁移（⚠️ 判读）。
- 工业实践：湖仓项目的第一交付物常被要求是「表清单 + 分层归属 + 写入者唯一性矩阵」；
  Delta↔Iceberg 双头策略评估周期缩短，选型章引用请同时带上当日官方页（⚠️ 转述）。
- 展望纪律：本册不对「Fabric 是否会全面转向 Iceberg 优先」下断言——属未实证路线图（⚠️）。
