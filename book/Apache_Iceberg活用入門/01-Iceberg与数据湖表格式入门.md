# 第 1 章 Iceberg 与数据湖表格式入门

> ⚠️ 章题为**推定**（示意日文名：Apache Iceberg とは / データレイクとテーブルフォーマット），原书真实目录未核实，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 本章技术内容以 [iceberg.apache.org 官方文档](https://iceberg.apache.org/spec/) 与 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md) 的存储基础为准。

## 本章地图

> 一句话：**Iceberg 不是存储格式、不是计算引擎，而是「表的元数据规范」——它把一张表定义成一棵可原子替换的文件树，从而让任何引擎都能在对象存储上做 ACID 读写。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 数据湖的老问题 | Hive 表 = 目录约定，无事务无 schema 真相 | 目录即表 → 一切可靠性都是「祈祷」 |
| 1.2 表格式是什么 | 规范化的元数据层：表状态 = 一组文件 | 表格式管「表」，文件格式管「字节」 |
| 1.3 Iceberg 的定位 | 引擎中立、规范先行、多实现 | 同一张表可被 Spark/Flink/Trino 并发安全地读写 |
| 1.4 与 Delta/Hudi 的对照 | 事务日志 vs 元数据树 vs timeline | 能力趋同，哲学不同：Iceberg 押注「开放规范」 |
| 1.5 规范版本 | format-version 1/2/3 各代能力 | 表创建时定版，能力随版本解锁 |
| 1.6 生态地图 | 引擎、catalog、云托管 | 学 Iceberg = 学规范 + 学一个引擎的接入 |

## 核心精讲

> **教学示意，不参与构建。** 下述目录结构与 SQL 仅说明机制，未在本机搭建任何集群验证。

### 1.1 数据湖的老问题：为什么「目录 + Parquet」不够

传统 Hive 表在对象存储上就是：

```text
warehouse/db/orders/            ← 「表」= 这个目录
├── dt=2024-01-01/part-0000.parquet
├── dt=2024-01-02/part-0000.parquet
└── ...                         ← schema 存在 Hive Metastore，分区=目录名约定
```

它的结构性缺陷（每一条都是 Iceberg 设计動机的反面）：

1. **没有事务**：写入 = 往目录丢文件 + `ALTER TABLE ADD PARTITION`。半途失败留下「半新半旧」的表；两个作业并写互相踩。
2. **列表即规划**：查询计划要先 `LIST` 目录/读文件 footer 拿 schema 与统计，大表上仅规划就要分钟级（对象存储 LIST 既慢又按次计费）。
3. **分区是物理目录**：`PARTITION BY (dt string)` 把「按天分区」这个**决策**烧进了路径。想改成按月分区？只能重写全部历史数据（见第 3 章）。
4. **schema 与数据脱钩**：Metastore 里的列定义和 Parquet 文件里的列名可以悄悄不一致；改列名会让所有按位置读的老文件错位（见第 4 章）。
5. **没有行级修改**：改一行 = 重写整个分区。

一句话总结：**Hive 表的状态散落在「目录结构 + Metastore + 文件内容」三处，没有任何一处是权威快照**。

### 1.2 表格式：把「表」重新定义为「一组文件」

Iceberg 的核心动作只有一步：**表的所有状态（schema、分区规则、当前数据文件清单、历史）全部写进一套自描述的元数据文件**，放在表自己的 `metadata/` 目录里：

```text
orders/
├── metadata/
│   ├── 00007-3f2a....gz                 ← table metadata 文件（当前版本）
│   ├── snap-1097xxxx-....avro            ← manifest list（每个快照一个）
│   ├── <uuid>-0.m0.avro                  ← manifest file（列出数据/删除文件）
│   └── ...
├── data/
│   ├── 00000-0-....parquet               ← 数据文件（Parquet/ORC/Avro，Iceberg 不关心行格式）
│   └── ...
```

于是：

- **读表** = 从 catalog 拿到 metadata 文件路径 → 顺着 manifest list/manifest 找到该快照**恰好引用**的那批文件。列表操作从「扫目录」变成「读几个小的索引文件」，规划复杂度与表大小解耦。
- **写表** = 新数据先写成新文件 → 生成新 manifest/manifest list → 最后**原子地**把 catalog 指针从旧 metadata 文件换成新的。换指针前读者看到的永远是旧快照——这就是 ACID 的全部来源（第 6 章）。
- **回滚/时间旅行** = 把指针换回旧的 metadata 文件（第 2 章）。

对照第 1.1 节：**Iceberg 把三处散落状态收敛成一棵有根（metadata 文件）的树，根的改变是原子的。**

### 1.3 Iceberg 的定位：规范先行（spec-first）

Iceberg 2017 年诞生于 Netflix（内部需求：超大规模 Hive 表的元数据瓶颈与多引擎读写），2018 年进入 Apache 孵化器、2020 年毕业为顶级项目。它的差异化定位是：

- **它首先是一份规范**（[Table Specification](https://iceberg.apache.org/spec/)），定义上面那棵树里每个文件的字段；
- **参考实现是 Java 核心库**（`api/core`），Spark/Flink 引擎扩展都构建其上；此外有 Python（pyiceberg）、Go（iceberg-go）、Rust（iceberg-rust）、C++（arrow-iceberg）等**独立实现**；
- **catalog 也协议化**：REST Catalog 规范让「一套客户端 ↔ 任意合规服务端」（第 7 章）。

对读者的含义：**「会 Iceberg」= 懂规范 + 会你所用引擎的 connector 配置**。规范里找得到的行为才是可移植的行为，这一点贯穿本目录。

### 1.4 三剑客对照：同一问题的三种答案

| 维度 | Iceberg | Delta Lake | Hudi |
| --- | --- | --- | --- |
| 表状态载体 | 层级元数据树（metadata→manifest list→manifest） | 事务日志 `_delta_log`（JSON+Checkpoint Parquet） | Timeline（commits + `.hoodie` 元数据） |
| 出生地/哲学 | Netflix；**开放规范 + 多实现** | Databricks；以 Spark 为中心，协议后补 | Uber；以「管道」为中心，强 MoR 记录级索引 |
| 行级删除 | v2 delete files（第 5 章） | 早期仅 CoW，后有 Deletion Vectors | 原生 MOR 日志式（block-level log） |
| 分区演化 | **一等公民**（多 spec 共存，第 3 章） | 分区生成列 + 有限演化 | 多种 partitioner，演化需迁移 |
| 引擎耦合 | 刻意引擎中立 | 与 Spark 深度绑定 | 与 Spark/Flink 双栈 |

详细的横向机制对比见 [../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md](../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md)；Hudi/Delta 的深入各自成书：[../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)、[../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)。结论：**能力在趋同（都在补 ACID、演化、维护工具链），分歧在「谁是第一等公民：规范、引擎还是管道」**。

### 1.5 format-version：表级别的「格式版本号」

建表时通过属性 `format-version` 定版（Spark：`TBLPROPERTIES ('format-version' = '2')`），**事后基本不可逆**（v1→v2 可升级，v2→v3 依版本支持情况）：

| 版本 | 关键内容（依据 spec） |
| --- | --- |
| v1 | 基线：不可变表的分析型管理。schema/分区规范/快照链/manifest 树，**无行级修改** |
| v2 | **行级更新与删除**：delete files（position/equality）、序列号（`sequence-number`）、manifest list 强制、更严格的写入方要求；UPDATE/DELETE/MERGE 的地基 |
| v3 | 扩展类型（纳秒时间戳、`unknown`、`variant`、geospatial）、列默认值、**row lineage**（行级血缘：`first-row-id`/`added-rows` 贯通到行）、**deletion vector**（Puffin 二进制删除向量取代 position delete）、表加密密钥声明 |

🔧 2025 年初版书大概率成稿于 v3 定稿（2025 年中）前后，读到「v2 是最新」的表述时按上表补。

### 1.6 生态地图：要学的三样东西

1. **规范本身**（本目录 02–06 章）；
2. **一个 catalog**：Hive Metastore / AWS Glue / 自建 REST（Polaris、Lakekeeper）/ 云托管（第 7 章）；
3. **一个引擎 connector**：Spark/Flink/Trino/Kafka Connect…（第 9 章）。

入门常见的最小闭环：Hadoop/REST catalog + Spark + S3/本地文件系统，即可复现本目录所有示意操作。

## 版本演进与兼容性

- 时间轴：2018 入孵化 → 2020 TLP → 1.0（2022，v2 成熟）→ 1.4（2023，加密/视图提案）→ 1.5（2024，GA 视图、表维护服务）→ 1.6–1.8（2024–2025，maintenance 编排增强、REST spec 迭代）→ 1.9+/1.11（2025–2026，v3 落地）。
- 规范与实现的版本是**两条线**：spec 里 format-version 决定「数据长什么样」；Iceberg 发行版决定「库支持到哪个 format-version、有哪些过程」。跨引擎协作时以**表定住的 format-version** 为兼容性判据。
- 兼容性底线（规范明言）：v1 表可升 v2（需要补 sequence number 语义）；老引擎读到不认识的 format-version 应直接报错而非猜测——「先失败，后静默」是表格式的安全惯例。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「Iceberg 是一种新的文件格式」 | 文件格式仍是 Parquet/ORC/Avro；Iceberg 管的是**表级**元数据（第 2 章） |
| 「用了 Iceberg 就必须换查询引擎」 | 表格式与查询引擎解耦；同一张表可被 Spark 批、Flink 流、Trino ad-hoc 并发访问（第 9 章多引擎矩阵） |
| 「Iceberg ≈ Delta/Hudi 的另一个品牌」 | 哲学差异在 1.4；尤其：**规范先于实现**，不锁定任何云/引擎 |
| 「元数据都在对象存储上，所以离线不可用」 | catalog 侧确实要在线可达（HMS/Glue/REST）；但表内容自描述，`register_table`/路径改写过程可把表「搬活」（第 8 章） |
| 「schema/分区演化听起来要重写数据，先不上」 | 两者都只是元数据操作（第 3、4 章），这正是 Iceberg 的卖点 |
| 「format-version 以后随时能升」 | 定版影响所有写入方，升级需全引擎同步支持；新项目直接 v2 起步，别等 |

## 与其他章 / 其他书的联系

- 1.2 的「文件树」在 [02-元数据三层结构.md](02-元数据三层结构.md) 逐字段展开；1.1 的分区之痛与演化在 [03-隐藏分区与分区演化.md](03-隐藏分区与分区演化.md)、[04-Schema演化.md](04-Schema演化.md)。
- 1.1 的「没有行级修改」的解法在 [05-行级删除与删除文件.md](05-行级删除与删除文件.md)；「原子换指针」的完整论证在 [06-ACID与乐观并发控制.md](06-ACID与乐观并发控制.md)。
- 存储层基础（列式文件、footer 统计、对象存储特性）：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)；数据湖→湖仓的宏观叙事：[../湖仓架构大规模数据平台的设计和实现/01-湖仓架构简介.md](../湖仓架构大规模数据平台的设计和实现/01-湖仓架构简介.md)。
- 「目录即表」的对照反面教材其实是「数据字典即表」的传统 DB：[../数据库系统概念6/10-存储和文件结构.md](../数据库系统概念6/10-存储和文件结构.md)。

## 思考题

1. 为什么说「Iceberg 表可以离线解析」？哪些信息**不**在对象存储上、必须依赖 catalog？
2. 一张 10 万文件的 Hive 表和同样的 Iceberg 表， planner 各自要做多少 I/O？差异的根源是什么？
3. 你在选表格式：团队全栈 Databricks 且只信 Spark ——1.4 的表格里哪一行最影响你的决策？
4. v1 表上执行 DELETE 会怎样（报错还是静默）？这体现了 1.5 的什么原则？
