# 05 · Warehouse 数仓与 SQL 端点 —— Learn Microsoft Fabric（⚠️ 主题重构章）

> **降级声明**：原书目录未获任何渠道实证（负结果台账见 [00 · 总览与阅读地图](00-总览与阅读地图.md) §2），本章为主题重构章。
> 机制 = 官方文档转述 ⚠️（✅ <https://learn.microsoft.com/en-us/fabric/data-warehouse/>，2026-10-02 验 200）；
> 🔧 本机 SQLite/DuckDB 类比，**非本书引擎/平台行为**。兄弟册同题：
> [../Fundamentals_of_Microsoft_Fabric/05-Warehouse数仓引擎与选型.md](../Fundamentals_of_Microsoft_Fabric/05-Warehouse数仓引擎与选型.md)（不同书，见 00 §3）。

## 1. 本章定位

- Warehouse item = Fabric 的**经典数仓位**：T-SQL 表面、列存底座、与湖仓同数据不同职责（⚠️ 转述）。
- 教学书的典型问题：「我已经有 Lakehouse，为什么还要 Warehouse？」——本章以「引擎性格」回答（⚠️ 推定主线）。

## 2. 仓库形态与 T-SQL 面（⚠️ 转述官方 data-warehouse 域）

- 建表即 DDL/DML 全 SQL；查询走 SSMS/SSMS-等价客户端或网页体验；与 BI 语义模型的 Direct Lake
  直读是核心卖点（[10 章](10-PowerBI语义模型与DirectLake.md)）（⚠️ 转述）。
- 存算分离：数据以列存形态落 OneLake，计算按容量供给；仓库本体「像一个逻辑实体，不像一台机器」（⚠️ 转述推定表述）。
- SQL Server 血统谱系登记（波内对位义务）：T-SQL 方言与执行语义的历史包袱/纵深在盘上
  [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)（波 1）与
  [../SQL_Server_2022_Administration_Inside_Out/](../SQL_Server_2022_Administration_Inside_Out/00-总览与阅读地图.md)（波 7 在盘）——
  **Fabric 仓库 ≠ SQL Server 引擎的托管搬运**，方言同源、架构异源（⚠️ 判读，具体内核构成微软未公开逐层证实）。

## 3. Lakehouse vs Warehouse 选型地图（⚠️ 转述+重构决策表）

| 维度 | Lakehouse（04 章） | Warehouse（本章） |
|---|---|---|
| 主人群 | Spark/Python 工程师 | T-SQL 分析师/DBA |
| 写入面 | 笔记本/管道高频分布式写 | SQL DML + 批量装载 |
| 表语义 | Delta 事务表 | 列存表（平台托管布局） |
| BI 路径 | 语义模型亦可直读 | Direct Lake 主场（10 章） |
| 典型工件 | 分层原始域 | 星型/宽表集市 |
| 演进 | 开放表格式互操作面 | T-SQL 生态兼容面 |

- 判例法（⚠️ 重构）：同一份 Gold 数据，「谁写谁负责」——Spark 域写湖表、SQL 域建仓表，
  跨面用快捷方式/镜像衔接，避免双头维护。

## 4. 🔧 本机类比：行存导入 vs 列存直查（非本书平台行为）

```text
E5 数仓引擎性格类比（SQLite 3.45.3 vs DuckDB 1.5.5，1,000,000 行事件表，2026-10-02 实测）：
  SQLite 建表+逐行灌入：1,448.2ms（行存写入路径）；行存聚合 count+sum：67.9ms
  DuckDB 同数据列存聚合：1.7ms（≈40.3× 于 SQLite 聚合）
  注：DuckDB 侧含已就位 Parquet/内存表热态；SQLite 侧为裸行存无索引全扫。
迁移直觉：仓库型负载（大范围聚合）由列存+向量化赢下两个数量级；
  「把行存习惯（逐行 DML、索引点查）带进列存域」是教学书应拦截的第一错（⚠️ 推定）。
（本实验仅类比，**非 Fabric Warehouse 行为**：其列存布局、分布键、缓存策略均平台托管 ⚠️）
```

## 5. SQL 端点家族辨析（⚠️ 转述）

- 湖仓 SQL 端点（只读，04 章）/ 仓库（读写）/ SQL 数据库 item（事务面，2024 后新增）——
  三者的权限、连接体验与用途边界是 DP-600 式考点（⚠️ 转述；SQL 数据库的文档路径本轮未单独
  验链，登记缺口，引用请当日核实 <https://learn.microsoft.com/en-us/fabric/>）。
- 连接面：标准 TDS/Azure SQL 式连接串与 Entra 认证；驱动生态与本地开发器对接（⚠️ 转述）。

## 6. 性能与成本直觉（⚠️ 转述 + 🔧 类比回链）

- 查询快慢三问：数据在哪（湖/仓布局）？谁在等（容量排队，02 章 CU）？扫描量多大（分区/谓词）？
- 并行摊薄墙钟的量化直觉回链 [02 章 §4 🔧 E6](02-许可容量与租户开通.md)；zone-map/剪枝级
  存储直觉可借 [../Tuning_the_Snowflake_Data_Cloud/04-微分区.md](../Tuning_the_Snowflake_Data_Cloud/04-微分区.md)
  的 🔧 实验互讲（跨册类比，标注非 Fabric）。
- 教学项目处方（⚠️ 重构）：星型事实表按月分区、维表小表广播心智、装载用批量 COPY/管道而非
  逐行 INSERT——与 06 章集成面衔接。

## 7. 本章在盘上目录版中的对位

- 兄弟册 05 章：选型地图视角；本章：T-SQL 工程 + 类比视角（00 §3 辨析表）。
- 数仓方法论：[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)（Kimball 流程在云仓 item 上的再实现）。
- 云仓镜像章：Redshift/Snowflake/BigQuery 三册的「仓库对象模型」章可与 §2 对读（登记于 00 §6）。
- 索引：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 8. SQL 面速查矩阵（重构表，⚠️ 口径当日核实）

| 面 | 读写 | 典型对象 | 归属章 |
|---|---|---|---|
| 湖仓 SQL 端点 | 只读 | Delta 表 | 04 |
| Warehouse | 读写 | 列存表/视图 | 本章 |
| SQL 数据库 item | 读写（事务） | 应用表/暂存层 | §5 |
| 镜像目标 | 平台写入为主 | 源库镜像表 | 06 |

- 判读纪律：四面的**权限继承路径不同**（工作区/模型/源凭据），排障先定位面再定位层（11 章回链）。

## 9. 教学 FAQ（重构问答位，⚠️ 非原书）

- **问：从 Synapse/ADB 迁移，T-SQL 脚本要重写多少？**
  答：方言层多数可重放，要重做的是「排队与容量心智」+「跨库语句拆分」——迁移项目按
  「语法通过率」和「语义等价率」两本账分别验收（⚠️ 转述共识，清单当日核）。
- **问：仓库要不要手动建索引/分区？** 答：Fabric 仓库叙事是「布局托管」，先跑真实负载
  观测再谈调优；把 SQL Server 索引反射弧带进来常做成负优化（⚠️ 转述+判读）。
- **问：仓和湖同一份数据要不要双写？** 答：默认**不**——用镜像/直读把「一份写入、多面消费」
  立起来；双写只在过渡期设时限与对账任务（03/06 章联动）。

## 10. 章末自测（重构题，⚠️ 非原书习题）

1. 复述选型表六个维度，各给一个选型翻转的业务信号。
2. 🔧 E5 的 ≈40.3× 数字说明什么、不说明什么（列存方向律 vs 平台量化承诺）。
3. 「谁写谁负责」原则下，写出你项目里每张 Gold 表的唯一写入者矩阵。
4. 连 Fabric 仓时排障顺序：认证→网络→方言三级二分（连接面 ⚠️ 当日核驱动清单）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 仓库项 | Warehouse item | T-SQL  surfaces 的数仓实体 |
| 列存 | columnar storage | 仓库聚合性能的结构根源 |
| 存算分离 | decoupled storage/compute | 数据在湖、算按容量供给 |
| T-SQL | Transact-SQL | 方言同源、引擎异源的 SQL 面 |
| SQL 数据库 | SQL database item | 事务型 SQL 面（与仓库分工） |
| 只读端点 | read-only endpoint | 湖仓的 T-SQL 观察窗 |
| 批量装载 | bulk load | 列存友好的进数方式 |
| 集市 | data mart | Gold 层的常见仓侧形态 |

## 最新演进与工业实践

- 域动态（⚠️ 转述）：仓库与「SQL 数据库/湖仓直读」的能力线持续互渗——官方把 Fabric 的 SQL 面
  叙事从「Synapse 后继」转向「统一 SQL 体验」；任何「仓库就是某引擎」的断言都应回到当日
  ✅ 域页（<https://learn.microsoft.com/en-us/fabric/data-warehouse/>，2026-10-02 验 200）核对（⚠️ 纪律）。
- 工业实践：迁移项目常见路径 = Synapse/ADB 仓脚本 → Fabric Warehouse 重放，方言兼容率高但
  排队与容量语义需重建心智（⚠️ 转述社区共识）；数仓治理侧建议沿用盘上方法论册的一致性
  维度检查表，再映射到 item 权限（00 §6 对位）。
