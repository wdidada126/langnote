# 第 4 章 开源实现与 OpenTSDB 案例（⚠️ 章题为推定；章位实锤）

> 对应原书第 4 章。章位有 ✅ 实据（第 3 章译文路线图段原话："第四章会提供如何使用现有开源软件
> 来最好地实现这些概念的建议"），章题为 ⚠️ 推定；章内主题按封底学习点（✅ 豆瓣实抓）
> "The benefits and limitations of OpenTSDB" 对位重构为 OpenTSDB 深潜。
> **本章涉引擎（OpenTSDB/HBase/Graphite/InfluxDB）本机一律不装不跑，全部 ⚠️ 文档转述**；
> 🔧 演示仅用 sqlite3/DuckDB 复现"乱序吸收"概念。

## 章定位与中心论题

第 3 章给了设计空间，第 4 章给**参照实现**：OpenTSDB（Stag OpenTSDB 团队，跑在 HBase 上）
逐条兑现 3.3 的 rowkey 处方，同时暴露该路线的工程代价（运维 HBase 集群、UID 表、热点）。
读法：把它当"概念 → 实现"的翻译词典，而非选型手册（选型看演进节的 2024–2026 版图）。

## 逐节精读重构

### 4.1 OpenTSDB 数据模型：度量 + 标签 + UID

- ⚠️ 文档转述（据 opentsdb.net 概念文档口径，✅ 200 可达）：一条时序 = metric + 标签键值集；
  字符串到 3 字节 UID 的映射表（tsdb-uid）是写入前置——**2.3 高基数特性的直接兑现**，
  也是运维事故常见源（UID 表膨胀/备份）。
- 时序点 = (metric, timestamp, value, tags)，写后不可变（2.1）；查询 = 时间区间 + 标签匹配 +
  聚合器（avg/min/max/sum）+ downsample 器——**聚合与降采样是一等 API 参数**，
  对照 🔧D1/D2（03 章）里手工 SQL 的全部工作在此变成一次请求参数。

### 4.2 rowkey 布局与热点治理

- ⚠️ 转述：tsdb 表 rowkey ≈ [盐前缀][metric UID][timestamp（分钟对齐）][tag UID 对]，
  列限定符 = 时间偏移——3.3 基本设计的逐字段落地；
  分钟对齐让"同一分钟的多点"聚进一行，即 3.4 的"blob 打包"粒度选择。
- **热点**：新分钟总是"最大 rowkey"，纯递增写集中末段 region → 盐前缀（加盐/反转）打散，
  代价是跨序列扫描要扇出——"rowkey 盐化"作为通用技法在盘上另见
  [../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md](../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md)
  （Cassandra 分区键的同款问题）。
- ⚠️ 转述：TSD 节点无状态、查询层并行扫 region、结果在 TSD 聚合——
  "存储无状态 + 计算前置"的 Lambda 味架构，与
  [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md) 的批流分工讨论对照。

### 4.3 收益与局限（封底学习点"benefits and limitations"对位）

| 收益（⚠️ 转述重构） | 局限（⚠️ 转述重构） |
| --- | --- |
| 借 HBase 线性扩展，PB 级监控史实可行 | 部署 = 养 HBase+ZooKeeper+HDFS 三件套，小负载过重 |
| rowkey 布局使"序列 × 区间"读近 O(1) 定位 | 标签组合爆炸 → UID 表与倒排缺失，全标签扫描退化 |
| 聚合/降采样/速率计算在查询层内置 | 乱序容忍有限（默认 3h 窗口，可调），超窗迟到点拒写 |
| 分钟对齐 blob 压缩比高 | 高频（亚秒）与事件型（带字符串值）数据不适配 |

- 历史裁决（⚠️ 转述 + 04 末演进节实证）：2016–2020 监控用例整体迁出 HBase 系，
  OpenTSDB 归档；但"局限"列的四条恰是新一代引擎的 feature list——本书案例的教学价值在此。

### 4.4 同代对照：Graphite/Whisper 与 InfluxDB（⚠️ 全转述，不装不跑）

- **Graphite + Whisper**：单序列单文件、定长 chunk、稀疏分配（✅ 文档站
  https://graphite.readthedocs.io/en/latest/ 200 可达，机制细节 ⚠️ 转述）——
  3.1"平面文件"路线的**单序列极限版**：文件内无读放大问题，代价是文件数 = 序列数
  （百万级 inode 压力，恰撞 3.1 的小文件悖论）。
- **InfluxDB**：单机 Go + TSM（LSM 变体），InfluxQL/行协议——把本书"HBase 之上再搭一层"
  的三件套压缩成单二进制（⚠️ 转述，✅ https://docs.influxdata.com/influxdb/v2/ 200 可达；
  v2/v3 演进与 Cloud 口径未逐字核实，标 ⚠️）。
- 盘上互链：InfluxDB 类引擎的摄入前置（采集/消息总线）见
  [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)。

### 4.5 乱序与迟到：存储侧的"吸收"语义（🔧 演示主场）

- 概念框架：计算侧对"乱序"做**承诺**（水位线，见
  [../Streaming_Systems/03-水位线.md](../Streaming_Systems/03-水位线.md)）；
  存储侧对乱序做**吸收**——只要 (series, ts) 键唯一且幂等 upsert，到达序不影响终态。
- 🔧 **演示 D3（sqlite3 + DuckDB 1.5.5，非时序引擎行为）**，脚本同 03 章
  （`D:\develops\tmp\dbwave_w3_timeseries\demo.py`）：
  1. **到达序不变性**：200,000 行打乱到达序，`INSERT OR REPLACE INTO raw2`（主键
     (series,ts) WITHOUT ROWID）：🔧 实测 **0.87s**（vs 顺序插入 0.17s，随机写放大 ~5×），
     与顺序版逐行 EXCEPT 比对**差异 0 行**——终态与到达序无关；
  2. **迟到点吸收**：向已建好 5min rollup 的库补写 5,000 个迟到点（随机落入已有时间轴），
     全量重算聚合：桶数 7,000→7,000，全体桶均值 49.2687→49.2863——迟到修正 =
     受影响桶重算，rollup 层需失效重建（sqlite 无自动失效，手工全算 0.09s 级）；
  3. **DuckDB 对照（D3b）**：同一 2,000 点按两种到达序入两表，全桶重算后
     `SELECT sum(v) FROM pts = SELECT sum(v) FROM pts2` → 🔧 `True`（20 桶全等）。
- ⚠️ 转述的引擎差异：OpenTSDB 靠 HBase cell 版本 + 乱序窗口拒收超窗点；
  Prometheus 对乱序近乎零容忍（head block 时间窗，超窗拒写，需 remote write 层解决）；
  InfluxDB/TSM 靠 LSM 合并吸收任意乱序——"存储侧吸收带宽"正是各 TSDB 的分化点
  （TS-Benchmark ✅ DOI 10.1109/ICDE51399.2021.00057 将其列为一等工作负载维度）。

## 与相关书目的衔接

- [../Streaming_Systems/03-水位线.md](../Streaming_Systems/03-水位线.md)：乱序的"承诺 vs 吸收"对偶（4.5）；
- [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)：摄入管道与 TSD 无状态层的架构同族；
- [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)：Kafka 前置时的乱序来源与分区策略；
- [../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md](../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md)：盐化/分区键热点的姊妹讨论；
- [../设计数据密集型应用.md](../设计数据密集型应用.md)：LSM 合并 = 乱序吸收的一般机制；
- [../Cassandra_The_Definitive_Guide/（本波兄弟，写作期不链空，见 00 第七节互链义务）]、
  [../Streaming_Databases/（本波兄弟，写作期不链空，见 00 第七节互链义务）]：
  宽列处方第二代表 / 连续聚合对 4.1"内置降采样"的流式化。

## 核心概念速览（中英对照）

- **OpenTSDB** — 跑在 HBase 上的开源 TSDB（本书主案例，现已归档 ⚠️）
- **UID 映射表** — tsdb-uid：metric/tag 字符串 → 3 字节 ID 的前置字典，高基数治理点
- **分钟对齐** — minute-aligned rowkey：同一分钟点聚入一行（blob 粒度决策）
- **rowkey 盐化** — salting：前缀打散递增写热点，换跨序列扫描扇出
- **无状态查询层** — stateless TSD：并行扫 region、本地聚合的薄计算层
- **乱序窗口** — out-of-order tolerance：引擎允许迟到写入的时间界（OpenTSDB 默认 3h ⚠️）
- **幂等 upsert** — idempotent insert：(series,ts) 键唯一 + REPLACE，到达序不影响终态（🔧D3）
- **Whisper** — Graphite 的单序列定长稀疏文件，平面文件路线极限版
- **TSM** — Time-Structured Merge Tree：InfluxDB 的 LSM 变体（⚠️ 转述）
- **吸收 vs 承诺** — absorption vs commitment：存储侧消化乱序 / 计算侧用水位线声明乱序界
- **rollup 失效** — rollup invalidation：迟到点使物化聚合层需重算（🔧D3 手工演示）
- **降采样器** — downsampler：查询 API 的一等参数，🔧D1/D2 手工 SQL 的产品化

## 最新演进与工业实践

- **OpenTSDB 终局**：官方仓库归档、社区停止维护（⚠️ 转述；✅ http://opentsdb.net/ 200 可达，
  页面仍可访问；github.com 直连被网络策略阻断，归档日期未能本会话核验）。
- **监控用例的代际更替（2024–2026）**：
  - **Prometheus**：✅ https://prometheus.io/docs/introduction/overview/（200 实抓）——
    pull 模型 + 标签选择器成为云原生监控事实标准；其 TSDB 论文级细节散见官方设计文档（⚠️）；
  - **VictoriaMetrics / Thanos / Mimir**：长保留与多租户扩展层（⚠️ 转述；仓库 URL 已登记于
    02 章演进节，github.com 直连受限未核验 star 数）；
  - **InfluxDB**：✅ https://docs.influxdata.com/influxdb/v2/（200 实抓）；v3/IOx 引擎重写
    口径 ⚠️ 未逐字核实，不展开；
  - **QuestDB**：✅ https://questdb.io/（200 实抓）——列存 + JIT 的行式引擎，
    走"SQL 一等公民 + 零拷贝"路线，与本书 HBase 路线正交；
  - **M3DB**：✅ https://m3db.io/（200 实抓）——Unreal 系指标存储，"无状态协调 + 分片环"
    是 4.2 架构问题的当代答卷（⚠️ 细节转述）。
- **学术基准**：TS-Benchmark（ICDE 2021，✅ DOI 10.1109/ICDE51399.2021.00057 Crossref 200）
  把 4.3"收益/局限"表变成可测指标；Apache IoTDB（✅ DOI 10.1145/3589775）代表 HBase 自建路线
  之后"专用引擎"路线的学术化。
- **本书处方 today**：2026 年新监控栈几乎不会再选"HBase 上搭 TSDB"；但 4.2 的三个问题
  （热点、扇出、字典膨胀）以新形态活在每个引擎的 issue tracker 里——案例会死，问题不死。
