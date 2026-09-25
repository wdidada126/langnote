# 第 9 章 Spark / Flink / Trino 实战与多引擎协作

> ⚠️ 章题为**推定**（示意日文名：Spark / Flink / Trino での活用），原书真实目录未核实，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 依据：官方 `docs/spark-configuration.md`、`docs/spark-ddl.md`（已核对建表/演化语法）、`docs/flink-connector.md`（已核对：connector 经表属性路由 catalog、`catalog-type`/`catalog-impl` 配置）、`docs/multi-engine-support.md`（作为核对入口）。Trino/Presto 侧参数细节**未逐一核实**，以「核对方法」给出。

## 本章地图

> 一句话：**引擎侧的一切差异收敛为三件事：catalog 怎么接、提交语义怎么映射（overwrite/MERGE/upsert）、维护入口有没有——把这三列在每引擎上各填一遍，多引擎协作就不会互相踩。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 connector 分层 | 引擎扩展 ≠ 核心库 ≠ catalog | runtime jar 的依赖地狱从认清分层开始 |
| 9.2 Spark 实战 | 配置、读写、流式、扩展 | SQL 主战场（第 1–8 章示例几乎全用它） |
| 9.3 Flink 实战 | SQL catalog、DS Writer、checkpoint=提交 | 流式入湖主战场；提交频率由 checkpoint 决定 |
| 9.4 Trino 实战 | 查询引擎位：读为主、DDL/维护为辅 | v2 删除合并与剪枝行为要按版本核对 |
| 9.5 多引擎矩阵 | 功能×引擎对照与红线 | 不支持 delete 的引擎必须禁写 |
| 9.6 典型架构 | CDC 入湖→批修正→即席查 | 三引擎各就各位的样版图 |

## 核心精讲

> **教学示意，不参与构建。** 版本号/参数以官方文档为准；配置片段按 connector 惯例示意。

### 9.1 分层：runtime jar、核心库、catalog 客户端

```text
引擎进程
└─ iceberg-<engine>-runtime-<ver>_<scala>   （自带 core + spark/flink 适配 + 全部 catalog 客户端）
     └─ 你只需要再加：对象存储 SDK（如 hadoop-aws）、引擎本体
```

- 用 **runtime（`-bundle`）包**，不要手工拼 api/core/parquet——版本错配是入门第一坑；
- catalog 依赖决定额外 JAR：Hive 需要引擎版本匹配的 hive-metastore 与 HMS 客户端；REST/Glue 走对应 SDK；
- 引擎侧「扩展注册」：Spark 用 `spark.sql.extensions`；Flink SQL 的 catalog DDL；Trino 用 `etc/catalog/*.properties`——三种机制，本质都是「把 Catalog 实例挂到命名空间」。

### 9.2 Spark（OLAP/ETL 主战场）

```properties
# spark-submit --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.x.x
spark.sql.catalog.prod=org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.prod.type=rest                 # 或 hive/hadoop/jdbc/glue/nessie
spark.sql.catalog.prod.uri=https://polaris.../iceberg
spark.sql.catalog.prod.warehouse=s3://bucket/wh/
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
```

- 有 extensions 才有 `CALL` 过程、`MERGE INTO`、分区/列演化 DDL（第 3/4/8 章）；
- 读：`df = spark.read.format("iceberg").option("snapshot-id", ...)`；SQL：`VERSION AS OF` / `TIMESTAMP AS OF`、增量 `IN (SELECT ...)`/`incremental` 选项、元数据表（§2.7）；
- 写：`writeTo(t).createOrReplace()`、`create/replace/append` 系列；`INSERT OVERWRITE` 的语义 = **命中的（动态）分区整区替换**——与 Hive「往目录丢文件式 overwrite」在动态分区场景差异明显（Iceberg 是 replace 语义的快照提交，第 2.3 节；细节以 spark-writes 文档核对）；
- DELETE/UPDATE/MERGE 的 CoW/MoR 模式：§5.7；
- 流式：`readStream`（增量读快照，`streaming` 选项、可用 tag 固定起点）、`writeTo(t).toStream()`（每 micro-batch 一提交）——与 Flink 的差别本质是「提交节奏由微批还是 checkpoint 决定」；
- 排错主线：异常里先找 `commit failed / validation exception`（第 6 章）→ 元数据表看现场（§2.7）→ 别先动引擎参数。

### 9.3 Flink（CDC/流式入湖主战场）

已核对（flink-connector 文档）：Flink SQL 可**经表属性路由到任意 catalog**（`'catalog-type'='rest'`/`hive`/`hadoop`/`custom` + `warehouse`/`catalog-impl`），即一张 Flink 表引用 prod 库的 Iceberg 表而无需先 `CREATE CATALOG`。

- **提交模型**：Flink 的提交挂在 **checkpoint** 上：一次 checkpoint 成功 → 一次（每表）Iceberg 提交。所以：checkpoint 间隔 = 数据可见延迟 = 快照产生频率 = 第 8 章 manifest 碎片的源头；「exactly-once sink + 1 分钟」= 每天 ~1440 快照，务必配每日 expire/rewrite；
- 写入参数（`write.distribution-mode=hash/range` 控制同分区单写者避免碎文件、bucket 对齐 upsert key 等）、`commit.retry.*`（第 6 章参数在 Flink 提交超时语境复用）、分区提交器/动态分区（🔧 `partition-committer` 新版能力，细节未核实，用前查 flink-configuration）；
- **upsert 模式**（1.6+）：按主键自动等值删除（equality delete，§5.4），CDC 乱序由序列号与合并语义兜住（§5.5）——「Flink CDC → Iceberg ODS → Spark MERGE 修正」的管道就建在这上面；
- DS Writer API：无 SQL 的作业（Kafka→Iceberg 自定义路由）；
- Flink 侧**没有** Spark 式全量 `CALL` 过程面：维护通常仍交给 Spark 作业或独立调度（§8.7 的引擎分工由来）。

### 9.4 Trino（交互式查询/ETL 入口）

- 挂载：`connector.name=iceberg` + `iceberg.catalog.type`（`hive_metastore`/`rest`/`glue`/`jdbc`/`nessie`…）+ warehouse/凭证；🔧 `rest` 与凭证细节按 Trino release 核对（**本节未逐项核实**）；
- 强项：谓词下推到 Iceberg 的 manifest 剪枝（§3.3 的两级漏斗在 Trino planner 的执行者）、`SELECT` 大规模并发 ad-hoc；支持 `INSERT/DELETE/UPDATE/MERGE`（写模式按版本核对）、`CALL` 面较小（`remove_orphan_files`/`delete_orphan_files`、`expire_snapshots`、`rollback_to_snapshot` 等核心维护过程 Trino 有对应实现，参数名可能不同——以 Trino 文档的 Iceberg connector 页核对）；
- **性能注意**：读 v2 MoR 表要现场合并删除（§5.8），交互式 SLA 敏感的库要么 CoW 化要么及时 compaction；时间旅行/增量在 Trino 用 `FOR ts AS OF` 语法族；
- 常见事故：某 Presto/Trino 老版本不支持多 spec（旧分区目录被忽略或报错）或 format-version=2 整表拒读——第 3/5 章反复强调的「引擎版本 = 表能力下限」。

### 9.5 多引擎矩阵：怎么查、红线在哪

权威入口：官方 `docs/multi-engine-support.md`（一张版本×功能矩阵，随发行版更新；写作时未逐格抄录，防止过期数据污染笔记——**每次引擎升级后重查此页是本目录建议的固定动作**）。矩阵之外，三条工程红线从机制直接导出：

1. **删除红线**：任一读者不支持 v2 delete → 它「看得见表、看不见删除」（数据静默错误）→ 不支持 delete 合并的引擎禁止写 MoR 表、最好只读 CoW 化视图；
2. **演化红线**：任一写者不支持多 spec/v3 默认值 → 它按旧语义写文件即污染（§4.8 同类）→ 新特性上线前全引擎跑「最小读写断言」；
3. **维护红线**：谁跑维护谁独占（§6.6 剧本 3；§8.7 偏序），多引擎写同表时维护调度中心化。

### 9.6 样版架构（教学示意）

```text
业务 DB ─CDC→ Kafka ─Flink SQL(upsert sink, checkpoint=1min)→ Iceberg ODS(v2, MoR)
                                                    │ 每日: rewrite(CoW 物化)+expire(保 7d+tag)
 批修正/维度建模 ─ Spark MERGE INTO ────────────────┤
                                        Iceberg DWD/ADS（day+bucket 分区, sort 后 binpack）
 BI/即席/监控 ─ Trino ──────────────────────────────┘   治理: REST catalog（权限+vending）+ tags 发布
```

各层对应的机制章：Flink 入湖=第 5/6/9.3；Spark 修正=§5.7；Trino 消费=§3.3/§9.4；发布=§7.5（WAP/tag）；维护节奏=§8.7。

## 版本演进与兼容性（connector 侧）

- Spark：3.x 线为主；`runtime-3.4/3.5/4.0` 并行发布，Iceberg 发行版对 Spark 大版本支持窗口有限——升级先看官方 support matrix；Spark 4 合入后部分行为（ANSI、时区）联动变化（细节未核实，标 🔧 自查）；
- Flink：1.17/1.18+ 线；upsert 模式（1.6）、动态分区提交器、水mark 对齐（🔧）渐次增强；Flink 与 Spark 同表时 `write.format.default`/分布模式不一致会放大碎片；
- Trino：每版本快改（v3 支持、DV 读取、rest catalog），务必按发行说明核对；Presto(ADB) 与 Trino 分叉后功能面差异大（本目录不混谈）；
- 其余生态（Doris/StarRocks/DuckDB/ClickHouse/pyiceberg/iceberg-rust/Arrow ADBC…）：**存在且演进极快**，接入前按各自文档+multi-engine 页双重核对（此处刻意不给清单，防过期）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「runtime 版本对不上也能跑」 | class 冲突/NoSuchMethodError 只是最礼貌的报错；静默按旧 spec 解释才是灾难 |
| 「Flink checkpoint 越短越好」 | 提交频率→快照/manifest 债→查询劣化（§9.3）；延迟与利息要一起算 |
| 「Trino 只是查询引擎，不碰写」 | 它能 MERGE/CALL，参数面还不同；多引擎写同表前先做 §9.5 红线评审 |
| 「增量读 = 每次从上次位点扫」 | 增量读以快照为单位、遇 replace 快照语义特殊（§8.2）；用 tag 锚定位点是稳妥做法 |
| 「一个表支持全部引擎」 | 能力 = min(引擎版本, 表 format-version)：第 5 章的 delete、第 3 章的多 spec、v3 类型都可能被某引擎卡住 |
| 「扩展没装也能 CALL」 | Spark 缺 extensions 时过程/MERGE 直接语法错误——排查第一站（§9.2） |

## 与其他章 / 其他书的联系

- 本章是 02–08 章机制的「投影面」：提交语义 → [06-ACID与乐观并发控制.md](06-ACID与乐观并发控制.md)；MERGE/upsert → [05-行级删除与删除文件.md](05-行级删除与删除文件.md)；catalog 挂接 → [07-Catalog生态.md](07-Catalog生态.md)；维护分工 → [08-表维护操作.md](08-表维护操作.md)。
- 姊妹目录：[../Use_Iceberg_with_Spark/02-Catalog配置与接入.md](../Use_Iceberg_with_Spark/02-Catalog配置与接入.md)、[03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)、[06-维护过程与流式写入.md](../Use_Iceberg_with_Spark/06-维护过程与流式写入.md)（Spark 向深入）；[../Engineering_Lakehouses_with_Open_Table_Formats/11-引擎集成与工程化落地.md](../Engineering_Lakehouses_with_Open_Table_Formats/11-引擎集成与工程化落地.md)（平台视角）；[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)（Flink 机制地基）、[../湖仓架构大规模数据平台的设计和实现/05-湖仓架构的计算引擎.md](../湖仓架构大规模数据平台的设计和实现/05-湖仓架构的计算引擎.md)。
- Spark 内部机制（shuffle/流式微批）：[../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)、[../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)。

## 思考题

1. 为什么「Flink 1 分钟 checkpoint + 从不 expire」的表，Trino 规划会越来越慢？用 §2.4 解释。
2. 团队要「Flink 写 MoR、Spark 每日物化、Presto 老版本只读」：§9.5 三条红线各命中哪条？给出治理动作。
3. Spark `INSERT OVERWRITE` 与 Hive  overwrite 在「动态分区」上的语义差异是什么？写错会多删/少删？
4. 给 §9.6 的 ODS 层加 WAP（§7.5）：哪些环节要改？审计不过时如何回退成本最低？
5. 为什么「查 multi-engine 矩阵」要成为每次引擎/表格式升级的固定动作，而不是入职时背一张表？
