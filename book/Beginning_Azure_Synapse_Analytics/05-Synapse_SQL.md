# 05 Synapse SQL — Synapse SQL（原书第 5 章，pp.87–118）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_5`，pp.87–118）；章内小节 ⚠️ 推定（无公开样章），
> 按 learn.microsoft.com SQL 文档域（专用池+Serverless 池）主题组织。Synapse SQL 不可本机实测，机制一律
> 「⚠️ 转述 + ✅ URL（2026-10-02 验 200）」；本章含 🔧 类比实验三组（E1/E2/E5，**均非 Synapse 引擎行为**）。

## 5.1 本章在全书中的位置

第 5 章 32 页是全书面值所在：Synapse 的 SQL 面=**专用池（预置 MPP 仓）+ Serverless 池（湖上按需 SQL）**
双子星。分布/索引/分区「物理三要素」与 CTAS/外部表的「装载两件」构成本章主干；读完本章，04 章架构图
的控制节点之下所有「数据为什么快/为什么慢」都有了答案。

## 5.2 专用池的表物理设计三要素

1. **分布（Distribution）** ✅ `sql-data-warehouse/sql-data-warehouse-tables-distribute`：
   - `HASH(key)`：按哈希切片到 60 个分布 ✅；高基数、分布均匀、常作 join 键的列是首选；
   - `ROUND_ROBIN`：轮询均摊，无 locality——无合适分布键时的默认，join 性能差 ⚠️；
   - `REPLICATE`：小维表全节点复制，消灭跨节点 shuffle ✅ 同页。
2. **索引（Index）** ✅ `sql-data-warehouse/sql-data-warehouse-tables-index`：
   默认 **CCI（列存储索引）**；堆（heap）与 BC 树仅作特定装载/staging 用途——与 SQL Server 单机
   「 clustered index 之治」明显分叉（对位盘上
   [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)
   索引/列存章 ⚠️ 选择性对照）。
3. **分区（Partition）** ✅ `sql-data-warehouse/sql-data-warehouse-tables-partition`：按范围分区服务
   「整段装卸/生命周期管理」，**不是**性能银弹（CCI 已有段级 min-max，🔧E3 机理在 02 章演示）。

- 组合处方 ⚠️ 转述 ✅ `sql/best-practices-dedicated-sql-pool`：事实表 HASH(业务自然键或代理键)+CCI；
  维表 REPLICATE+CCI；装载 staging 用 ROUND_ROBIN/heap 再 CTAS 重排。

## 5.3 🔧E1：为什么是列存——扫描形态对比（非 Synapse 引擎/平台行为）

DuckDB（向量化列式）vs SQLite（行存 B-tree），同一张 200 万行 6 列表、同一谓词聚合查询，原始输出：

```text
duckdb python version: 1.5.5
E1 duckdb 2M-row agg: [(400000, 28542857.142857164, 50001.5)] time=0.004s
E1 sqlite  2M-row agg: rows=400000 time=0.084s
PY sqlite runtime: 3.45.3
```

- 读法：同一逻辑查询，列式引擎只需触碰 3 列的压缩段，行存引擎逐行解码整条记录——**列存收益的本质
  是「只读你要的列」+「段级 min-max 跳读」**，与 Synapse CCI 的设计动机同构（✅
  `sql-data-warehouse/sql-data-warehouse-memory-optimizations-for-columnstore-compression` ⚠️ 转述）。
  量级差异随数据规模/冷热/编码而变，本数字仅示意，不可换算 DWU。

## 5.4 🔧E2：分布键选错长什么样——倾斜桶模拟（非 Synapse 引擎/平台行为）

100 万行事件表，热点租户占 20%+，分别按 HASH(tenant) 与轮询分桶到 4 个「伪节点」，原始输出：

```text
E2 HASH dist buckets (tenant, 4 dist nodes):
[(0, 194589), (1, 400999), (2, 178579), (3, 225833)]
E2 ROUND_ROBIN buckets (uniform):
[(0, 250000), (1, 250000), (2, 250000), (3, 250000)]
E2 key cardinality check: distinct tenants = 1000
E2 co-located-ish join wall=0.054s
```

- 读法：node1 吃到 40% 数据（热点租户哈希撞进同一桶）——**分布倾斜**的画像：木桶效应按最胖分布计时
  （⚠️ 云上对应诊断视图 `sys.dm_pdw_dms_cores`/行倾斜查询 ✅ `sql/distribution-advisor`、
  `sql-data-warehouse/analyze-your-workload` 存在性引用）。ROUND_ROBIN 桶绝对均匀但 join 需全量移动——
  这正是 §5.2「分布键=局部性/均匀性折中」的两端。
- Synapse 的官方解法：分布advisor/倾斜检测工具链 ✅ 同页 + 换键重建（CTAS）✅ `sql-data-warehouse/sql-data-warehouse-develop-ctas`。

## 5.5 装载与变换路径：CTAS / COPY / PolyBase / 外部表

- 湖→仓四条路 ✅ `sql/load-data-overview`：**CTAS**（外部表快照转内表，装载+变换一步）、**COPY**
  （管道活动/命令，宽松容错）、**PolyBase 外部表直查**（不落地）、内置分发 ⚠️ 各页细节。
- 外部表工件：专用池侧 ✅ `sql/develop-tables-external-tables` + CETAS ✅
  `sql/create-external-table-as-select`；湖格式支持 Parquet/Delta 等（2021 代 CSV 走视图/格式化 ⚠️）。
- ETL 时序设计（书中「变换在仓内」章法 ⚠️ 推定）：staging→影子表→原子重命名/分区切换，配
  `sql-data-warehouse/sql-data-warehouse-develop-best-practices-transactions` 类事务约束 ⚠️。

## 5.6 Serverless SQL 池：把湖当数据库

- 语义：TDS 端点按需拉起，**按查询处理字节数**计费 ✅ `sql/on-demand-workspace-overview`、
  `sql/best-practices-serverless-sql-pool`；
- 读文件三板斧：`OPENROWSET` 直查 ✅ `sql/query-parquet-files`、`sql/query-json-files`；外部表/视图
  抽象 ✅ `sql/develop-storage-files-overview`；湖仓表（Delta/Iceberg）直读 ✅
  `sql/query-delta-lake-format` 在文档域内存在（本书 02 章表格式的产品侧承接 ⚠️）。
- 成本护栏 ⚠️ 转述：分区裁剪+文件分目录、列裁剪（Parquet 谓词下推，🔧E3 的机理）、用视图固化
  解析逻辑防全量扫；查询历史计量 ✅ `sql/query-history-storage-analysis`。
- 与 Cosmos DB 分析存储的联邦 ✅ `sql/query-cosmos-db-analytical-store`（09 章回收）。

## 5.7 🔧E5：统计信息与计划选择——SQLite ANALYZE 实验（非 Synapse 引擎/平台行为）

```text
E5 plan WITHOUT ANALYZE: [(3, 0, 0, 'SCAN t'), (7, 0, 0, 'SEARCH s USING INTEGER PRIMARY KEY (rowid=?)')]
E5 plan AFTER ANALYZE: [(3, 0, 0, 'SCAN t'), (7, 0, 0, 'SEARCH s USING INTEGER PRIMARY KEY (rowid=?)')]
E5 stat1 rows: [('s', None, '1000'), ('t', 't_a', '100000 2000')]
```

- 读法（诚实记录负结果）：本例统计信息落地为 `sqlite_stat1`（100000 行 t 表上索引 t_a 估计 2000 行/键值），
  但该连接串的查询形态（主键查找侧已最优）未触发计划翻转——**统计影响的是代价估计，不保证所有计划
  改变**；对照 Synapse「自动统计 + 手动 CREATE STATISTICS 装载后补」的告诫 ✅
  `sql-data-warehouse/sql-data-warehouse-tables-statistics`（CTAS/大批装载后更新统计，否则优化器拿
  默认值开盲盒 ⚠️ 转述）。
- 工业纪律：装载管道尾部固定挂 `UPDATE STATISTICS ... WITH FULLSCAN`（按表规格）⚠️ 转述 ✅ 同页。

## 5.8 资源与并发治理

- 资源类（resource class）划定单查询内存/并行度 ✅ `sql-data-warehouse/resource-classes-for-workload-management`；
  工作负载组/重要性 ✅ `sql-data-warehouse/sql-data-warehouse-workload-management`；
- 内存/并发预算公式类文档 ✅ `sql-data-warehouse/memory-concurrency-limits`——并发不是免费项，
  大内存类×高并发=排队/降级（⚠️ 转述，数字随代际变化不抄录）；
- 结果集缓存/有序 CCI/物化视图三件加速件 ✅ `sql-data-warehouse/performance-tuning-result-set-caching`、
  `sql-data-warehouse/performance-tuning-ordered-cci`、`sql-data-warehouse/performance-tuning-materialized-views`。

## 核心概念速览（中英对照）

- **三种分布** — HASH/ROUND_ROBIN/REPLICATE：局部性、均匀性、零移动三者不可兼得的选型三角 ✅。
- **列存储索引** — Clustered Columnstore Index (CCI)：专用池默认物理形态，压缩+段裁剪+向量化执行。
- **60 分布** — 60 Distributions：专用池固定分布数（SQL Server 谱系遗留），节点数与其解耦 ⚠️。
- **CTAS/CETAS** — CREATE TABLE (EXTERNAL) AS SELECT：装载即变换的核心工件 ✅。
- **外部表** — External Table：湖文件的仓侧/Serverless 侧表抽象 ✅ develop-tables-external-tables。
- **OPENROWSET** — Serverless 行集函数：无需 DDL 直查 Parquet/CSV/Json 湖文件 ✅。
- **分布倾斜** — Distribution Skew：热点键使最胖分布主导墙钟时间（🔧E2 演示，非 Synapse）。
- **自动统计** — Auto Statistics：装载后需 UPDATE STATISTICS 的优化器输入（🔧E5 类比，非 Synapse）。
- **资源类/工作负载组** — Resource Class/Workload Group：单查询内存与并发的治理闸门 ✅。
- **结果集缓存** — Result-set Caching：同查询文本命中缓存返回旧结果的新鲜度换性能开关 ✅。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **专用池→Fabric data warehouse 的能力承接**：T-SQL/CCI/分布模型保留，治理面转向容量体系 ✅
  https://learn.microsoft.com/en-us/fabric/data-warehouse/workload-management；性能红线清单迁移为 ✅
  https://learn.microsoft.com/en-us/fabric/data-warehouse/guidelines-warehouse-performance。
- **Serverless 的继任形态**：Fabric 侧「short-term querying/查询加速」把「湖文件按需 SQL」并入仓库
  工件 ✅ https://learn.microsoft.com/en-us/fabric/data-warehouse/query-warehouse（2026-10-02 验 200）。
- **旧 slug 勘误（本册实证的取证副产品）**：2021 代 `sql-data-warehouse-tables-distribution` 已 404，
  现役为 `sql-data-warehouse/sql-data-warehouse-tables-distribute` ✅；`sql/adaptive-query-execution` 404——自适应类
  特性并入工作负载管理文档域 ⚠️。登记 [00](00-总览与阅读地图.md) §2。
- **工业实践基线**：星型事实表 HASH+CCI、维表 REPLICATE、装载后补统计、影子表切换——2026 年
  Fabric 迁移文档仍原样承认这套纪律 ✅（guidelines 页含同族建议）；Gen2 SKU 升级窗口 ✅
  `sql-data-warehouse/upgrade-to-latest-generation`、`sql-data-warehouse/gen2-migration-schedule`。
- **盘上互查**：云仓同代机制对照见
  [../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)（分布键=style 键）、
  [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)
  与 [../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)
  （聚簇键替代分布键路线）——波规点名云仓对位，均已实链 ✅。
