# 03 HBase（Introducing HBase）——列簇与大数据

> 对应官方页实抓目录（✅）：Day1 CRUD and Table Administration｜Day2 Working with Big Data｜Day3 Taking It to the Cloud｜Wrap-Up。
> HBase 依赖 Hadoop/HDFS + ZooKeeper，本机**无安装**（`where` 无果，⚠️ 不装不测）；运行行为全 ⚠️ 转述。🔧 类比用 DuckDB 1.5.5 复现「列存/范围扫/列剪枝」的**语义**，**非 HBase 行为**。
> 同谱系纵深：宽列的另一代表 Cassandra 见 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)、运维见 [../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md](../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md)。

## 3.0 HBase 是什么、坐标在哪

- HBase = Apache 对 Google **BigTable** 论文的开源实现：跑在 HDFS 之上的**分布式、稀疏、多维排序映射**（rowkey → column family → column qualifier → timestamp → value）。
- 定位：**写吞吐与水平扩展优先**，面向「海量行、按 rowkey 前缀范围扫、单行内多列局部更新」的日志/时序/宽表场景；**不提供** SQL join、二级索引（原生）、事务（跨行）——那是 Phoenix/其它层的事。
- 与 Cassandra 分野：HBase **强依赖 HDFS + ZooKeeper**、单点 RegionServer 归属明确；Cassandra 去中心化 gossip。⚠️ 转述（书把两者都归「列簇/宽列」genre，实现哲学不同）。

## 3.1 Day 1：CRUD 与表管理

- **hbase shell** 交互：`create 'tbl','cf1','cf2'`（表 + 列簇）、`put`、`get`、`scan`、`delete`、`disable/drop`。
- **数据模型四元组**：`rowkey`（字典序排序，决定范围扫效率）、`column family`（物理存储分组，数量宜少）、`qualifier`（列名，可动态增）、`timestamp`（版本）。
- **命名空间（namespace）**：类似 schema 的逻辑分组、权限边界。
- ⚠️ 转述：Day1 强调 **rowkey 设计是 HBase 的第一性问题**——前缀决定热点、字典序决定扫描代价，与关系库「随便加索引」的心智完全不同。

## 3.2 Day 2：与大数据协作

- **列簇与版本**：一列可存多版本（`VERSIONS => n`）；列簇数影响 flush/compaction 与局部性——书建议「列簇宜 ≤2~3，读写热点分簇」。
- **区域（Region）**：表按 rowkey 范围切成 Region，分布在 RegionServer；自动分裂（split）是扩展单位。
- **与 MapReduce/Spark 集成**：HBase 作 MR 输入输出（`TableInputFormat`），把「扫全表做聚合」交给计算层，而非 HBase 自身。
- **Compaction / WAL / Flush**：LSM 式写放大与后台合并（与 Cassandra 同源思路，见 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)）。
- ⚠️ 转述：Day2「working with big data」的核心信息是——HBase 只解决「存与按 key 取」，**分析要靠外部引擎**。

> 🔧 **类比组 F：范围扫 + 列剪枝（非 HBase，DuckDB 1.5.5 读 Parquet）**
> HBase「按 rowkey 前缀范围扫、只读需要的列」的直觉，可在**列式文件 + SQL 引擎**上拿到一手感觉。本机生成 `wide(rowkey, cf, v1, v2, v3)` 10 万行写入 Parquet 后：
> ```sql
> SELECT count(*) FROM 'wide.parquet' WHERE rowkey BETWEEN 1000 AND 1999;  -- 范围扫
> SELECT sum(v1)      FROM 'wide.parquet';                                 -- 只读 v1（列剪枝）
> ```
> 真实输出：范围扫命中 **1000** 行、耗时 **0.0075s**；`sum(v1)` 触发列剪枝，耗时 **0.0023s**（✅ 数字，DuckDB 1.5.5）。意义：「按 key 范围取 + 不读无关列」正是 HBase/宽列与列存共有的两个省钱动作。声明：Parquet/DuckDB ≠ HBase（无 Region/列簇/ZooKeeper），此处仅类比「扫描局部性」语义。

## 3.3 Day 3：上云

- **托管形态（⚠️ 转述 + ✅ 生态现状）**：EMR on EC2 跑 HBase、云厂商托管（阿里云/AWS 类），把 HDFS/ZooKeeper 运维外包；冷热分离、对象存储作底层。
- **访问层**：Java/Thrift/REST 客户端；SQL 需求靠 **Phoenix**（把 HBase 变 SQL 宽表，二级索引）等覆盖层——但 Phoenix 已随 HBase 主线活跃度下降 ⚠️。
- **迁移/备份**：`Snapshot`、`CopyTable`/`ExportImport`、DistCp。
- 书的结论：Day3 把「为什么上云」讲成运维成本——HBase 的 HDFS+ZK 三件套运维门槛是它被 Cassandra/DynamoDB 蚕食的原因之一。

## 3.4 Wrap-Up：HBase 适合什么、不适合什么

- **适合**：数十亿行、高写入吞吐、按 rowkey 前缀的范围读、稀疏列、需要与 Hadoop/Spark 同底层数据湖协作。
- **不适合**：需 ad-hoc 多维分析/聚合、需跨行事务、需复杂二级检索（→ ES）、运维团队无法扛 HDFS+ZK。
- ⚠️ 转述：作者把 HBase 归为「为『大』而生，规模不到就别上」的库——本册特意与 DynamoDB（07）对照：**同样宽列，一个自建一个托管**。

## 3.5 本册内互链

- 宽列另一半托管谱系 → [07-DynamoDB托管NoSQL.md](07-DynamoDB托管NoSQL.md)（同为列簇思路，运维模型相反）。
- 列存/文件格式底层 → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)（Parquet/ORC 与 🔧 组 F 直接呼应）。
- 文档/键值对照看数据模型差异 → [04-MongoDB文档模型.md](04-MongoDB文档模型.md)、[08-Redis数据结构服务器.md](08-Redis数据结构服务器.md)。

## 3.6 常见坑与设计要点（⚠️ 转述，HBase 通识）

- **rowkey 热点**：单调递增 key（时间戳打头）会把所有写压到同一 Region——需**加盐/哈希前缀/反转**打散。
- **列簇数陷阱**：列簇 >3 后 flush/compaction 互相牵连、局部性反降；「读热点」与「写热点」分簇。
- **没有 join / 二级索引**：任何「按非 rowkey 字段查」要么预构建反向表（另一种 rowkey 的表），要么外挂 Phoenix/ES——这是与关系库最根本的体验落差。
- **单元格 vs 行原子**：HBase 只保证**单行内原子性**（行级 MVCC），跨行事务要 Chukwa/Tephra 之类覆盖层 ⚠️。
- **运维三件套**：HDFS + ZooKeeper + RegionServer 任一起波都影响可用性；书用这点解释「为何很多人宁用托管 Dynamo（[07](07-DynamoDB托管NoSQL.md)）」。

## 3.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 设计一张「网站点击流」表：`rowkey=reverse(uid)+ts`，谈为什么反转能防热点、`scan` 前缀怎么取。
2. 给同一份数据设计 1 个列簇 vs 2 个列簇，讨论读写局部性差异（⚠️ 概念题，运行不可本机测）。
3. **跨库题**：HBase 存原始事件、把「按标签聚合」的活交给 Spark（见 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)），体会「HBase 只存不算」。
4. 🔧 迁移题：把 3.2 的列剪枝直觉用本机 DuckDB+Parquet 复现（见 🔧 组 F），再改 SQL 观察耗时变化。

## 3.8 hbase shell 小抄（⚠️ 书体例反推 + ✅ 官方 CLI 常识）

| 目的 | HBase shell | 关系库对照（[02](02-PostgreSQL关系锚点.md)） |
| --- | --- | --- |
| 建表（列簇） | `create 't','cf1','cf2'` | `CREATE TABLE`（无列定义，只有簇） |
| 写单格 | `put 't','row','cf1:q','val'` | `UPDATE … SET`（单元格级、带 ts） |
| 取一行 | `get 't','row'` | `SELECT … WHERE pk=?` |
| 范围扫 | `scan 't',{STARTROW=>,STOPROW=>}` | `WHERE pk BETWEEN`（但无二级索引） |
| 版本数 | `{VERSIONS=>n}` | 关系库无内建多版本 |
| 命名空间 | `create_namespace 'ns'` | `CREATE SCHEMA` |

> 记忆钩子：HBase 的一切快都来自「**知道 rowkey**」；一旦「不知道 key、只想按属性查」，就掉进 Scan 地狱——这是宽列 genre 的立身之本与天花板（对照 DynamoDB 的 Query-vs-Scan，见 [07](07-DynamoDB托管NoSQL.md) 🔧）。

## 3.9 宽列谱系三角：HBase / Cassandra / DynamoDB

三者同出 BigTable/Dynamo 论文血脉，却站在三种运维哲学上——本册用 HBase 与 DynamoDB 两章（[03](03-HBase列簇与大数据.md)/[07](07-DynamoDB托管NoSQL.md)）夹住 Cassandra 这个「盘上更完整的宽列代表」：

| 维度 | HBase（本章） | Cassandra（专册） | DynamoDB（[07](07-DynamoDB托管NoSQL.md)） |
| --- | --- | --- | --- |
| 协调 | ZooKeeper + HDFS | gossip，去中心 | AWS 全托管 |
| 访问 | rowkey + Scan | CQL + 主键 | PK/SK + Query |
| 计算 | 外置 MR/Spark | 库内轻 | 库内轻 + Streams→Lambda |
| 运维负担 | 重（三件套） | 中（自己管集群） | 轻（锁云） |

> 结论（⚠️ 转述）：**选宽列前，先选的是「谁运维」**，模型只是结果。盘上 Cassandra 纵深见 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md) 与 [../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md](../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **BigTable** — 谷歌论文，HBase 的理论原型（稀疏多维排序映射）。
- **行键 / rowkey** — 字典序主键，决定范围扫与热点的第一性设计。
- **稀疏** — sparse：空列不占存储，宽表也可以是「洞很多」的映射。
- **列簇 / column family** — 物理存储分组，数量宜少；跨簇局部性差。
- **列限定符 / qualifier** — 列名，可动态增长，实现稀疏列。
- **区域 / Region** — 按 rowkey 范围切分的水平分片与分裂单位。
- **RegionServer** — 托管 Region 的工作节点。
- **ZooKeeper / HDFS** — HBase 的协调与存储底座（运维门槛来源）。
- **W-TinyLFU / KV 分离** — HBase 3.x 缓存策略改进（⚠️ 转述）。
- **列剪枝 / column pruning** — 只读所需列的省 IO 手法（与列存共有）。
- **多版本 timestamp** — 单元格按时间戳保留多版本。
- **命名空间 / namespace** — 表的逻辑分组与权限边界。
- **Phoenix** — HBase 之上的 SQL + 二级索引覆盖层 ⚠️。
- **列剪枝 / column pruning** — 只读所需列的省 IO 手法（与列存共有）。

## 最新演进与工业实践

- **版本（⚠️ 转述 + 生态现状）**：HBase 主线 2.x 长期为生产基线，**3.0** 引入面向新硬件的改进（如 Java 11+、KV 分离/W-TinyLFU 缓存、协处理器与 replication 增强）。官方站 https://hbase.apache.org/ ✅ 实测 200（本轮 `curl -sIL`）。
- **被「湖仓 + 托管」两端挤压**：2018→2026，HBase 的经典「日志/宽表海量写」场景大量迁向对象存储上的 Iceberg/Delta（湖仓）与云托管 NoSQL（DynamoDB/Spanner）；HBase 仍在电信/广告/计费等超大规模存量位稳固。
- **计算下推外置化**：分析不再走 MR，而由 Spark/Trino 读 HBase 或直读湖仓；本册 🔧 组 F 的「列剪枝 + 范围扫」直觉在 Iceberg 上以分区裁剪 + 列投影复刻，见 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
- **同类对比**：与 Cassandra（同为 BigTable 谱系、去中心化）在 2026 仍是「自建宽列」双雄，取舍看是否需要 HDFS/Spark 同底层——详见 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)。
- **取证口径**：本章目录 ✅ 官方页实抓；安装/Region 分裂/Phoenix 等运行细节 ⚠️ 转述（本机无 HBase）；仅 🔧 组 F 为 DuckDB 1.5.5 一手数字，且明确非 HBase 行为。
- **一句话回扣全书**：HBase 教给读者的不是命令，而是「**rowkey 即命运**」——它把「先想访问模式」这件事用最粗暴的方式（无索引、按 key 计费/扫描）刻进直觉，与 DynamoDB（[07](07-DynamoDB托管NoSQL.md)）互为自建/托管两面的同一课。
