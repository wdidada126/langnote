# 04 流式摄入与 Kinesis 配方（2e Ch4）

> 取证强度：✅ 强（官方 2E 仓 Chapter04 实抓：`kinesis_data_generator_template.json`（Kinesis 数据生成器 CloudFormation 模板）、`2024-01-09-000.gz`/`2024-01-11-000.gz`（Firehose 命名风格的 gz 对象）、`part_table_insert1/2.sql`、`chapter_4_CFN.yaml`）。样例数据日期 2024-01——2e 成书期换代的实证（00 §5 表）。
> 三态：✅ URL/命令实证｜⚠️ 转述推定｜🔧 DuckDB 1.5.5（**非 Redshift 行为，方言已按 DuckDB 改写**）。

## 1. 本章定位

批（Ch3）之后的第二进水口：**流式摄入**。Redshift 侧的流式正统姿势不是"直连流"，而是 **流 → Kinesis Data Firehose（缓冲/压缩/转码）→ S3 → COPY/AUTO COPY 微批入表**——仓内 gz 对象的文件名（日期-序号）正是 Firehose S3 输出布局的指纹（✅ 文件名实抓；SMT 缓冲语义 ⚠️ 转述）。

## 2. 配方地图

| 配方 | 要素 | 取证 |
|---|---|---|
| Kinesis 造数 | 生成器 CFN 模板（shard/吞吐参数化） | ✅ kinesis_data_generator_template.json 实抓 |
| Firehose→S3→COPY | 缓冲间隔/大小、SNI/gzip 解压、IAM role ARN 挂载 COPY | ⚠️ 转述；✅ https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-source-s3.html 同址 200 |
| 入仓节奏 | AUTO COPY/自管微批（5min/15min 档） | ⚠️ 转述（r_COPY 总锚 ✅ https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html 同址 200） |
| INSERT 兜底小流 | part_table_insert1/2.sql——两批 VALUES 插入演示小量直写 | ✅ 文件名+首行 SQL 形态实抓 |
| 流式进阶（MSK/Managed Flink） | 2024 后官方线 | ⚠️ 转述，见演进节 |

## 3. 深潜一：为什么"流先落湖再进仓"（⚠️ 转述+✅ 锚）

1. Redshift 的写路径为**大批并行 COPY** 优化；高频小 INSERT 会制造大量 1MB 块碎片与未排序区（→ 本册 03 VACUUM 账）；
2. Firehose 的"缓冲+压缩+失败重试"恰好补齐流与批之间的阻抗失配：S3 前缀布局 `s3://bucket/prefix/YYYY/MM/DD/HH/...` 或扁平日期名（仓内 gz 即扁平式 ✅）；
3. COPY 侧配套：`REGION`+`IAM_ROLE`、`ACCEPTINVCHARS`/`TRIMBLANKS` 处理脏流数据、`COMPUPDATE` 关闭省 CPU（⚠️ 转述；✅ copy-parameters 锚同上）。
4. 现代替代：MSK/Kinesis → Managed Flink → 直接 `INSERT`（微批）或 **Kinesis Zero-ETL 摄取管道**（2024+ GA 线 ⚠️ 转述，专页本册实测已 302→mgmt/ 根，登记）。

## 4. 深潜二：入仓后的"迟到与乱序"三件套（⚠️ 转述）

- 分区列派生：装载 SQL 里 `date_trunc('day', ingest_ts)` 建事件日列，下游按日增量合并（复用 ch3 暂存法）；
- 去重键：流重试⇒重复行，按业务主键 row_number 收敛（→ 本册 07 的 🔧 D5 数字）；
- 水位线：以 `max(shipdate_dt)` 系统表记录批次高水位，COPY 后写控制表（工程惯例 ⚠️；目录锚 ✅ r_COPY/系统表族在 00 §2-7）。
- 对照学习：Trino/BigQuery 的流式入仓观感差异见 [../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md](../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md) 与 [../Google_BigQuery_TDG/04-将数据加载到BigQuery.md](../Google_BigQuery_TDG/04-将数据加载到BigQuery.md)（BQ Streaming Buffer 把"流阻抗"收进引擎内部——与 Redshift 外挂 Firehose 形成架构对照）。

## 5. 🔧 实测：UNLOAD 反向账（分区导出+过滤压缩；兼作 08/12 出口课）

脚本 demo.py（D2），DuckDB 1.5.5——**非 Redshift 行为，方言已按 DuckDB 改写**（Redshift 对应语句为 `UNLOAD ('select...') TO 's3://...' FORMAT AS PARQUET PARALLEL ON ALLOWOVERWRITE`，语义 ⚠️ 转述+✅ https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html 同址 200）：
1. 5e6 行 `COPY TO parquet PARTITION_BY(yr)`：**684ms→7 文件 67.3MB**，同表 csv 356.3MB——**5.3× 压缩比**，解释"为何流式落地选列存格式"；
2. 过滤子集+gzip csv UNLOAD（73.2 万行）：**2915ms→9.3MB**——gzip 压缩耗时主导（对比 parquet 路径快 4×），Redshift UNLOAD 的 COMPRESSION GZIP 同样吃 CPU（⚠️ 同向转述）；
3. 尺寸账：csv(356.3MB) → parquet(67.3) → 过滤 gzip(9.3/子集)——"导出粒度=下游 COPY 并行度"这条 cookbook 铁律在本组数字上自明。

## 6. 常见坑与最佳实践（⚠️ 转述+✅ 锚）

1. Firehose 缓冲过小→S3 海量小对象→COPY 文件数惩罚（每文件固定开销）；宁 5min/64MB 起步再调（⚠️）。
2. gz 内是 csv：Redshift COPY 解压吃 leader 节点 CPU——`COMPUPDATE RAW`+装后 ANALYZE 补偿（⚠️）。
3. 乱序时间列进 SORTKEY 首列：当日热点块永远未排序，ATO 也救不了——事件时间与到达时间分列（→ 本册 03 §6-3）。
4. COPY 清单要幂等：同对象重放=重复行；控制表记 `s3 key` 已装集合（→ §4 三件套）。
5. INSERT 兜底只用于 <千行级小流；两批 `part_table_insert*.sql` 的示范即此边界（✅ 文件名实抓，量级 ⚠️ 推定）。

## 7. 系列互链

- 概念版摄入全景：[../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md](../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md)（COPY/流式/零ETL 三分支）；
- 流式引擎本体：[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)、[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)（水位线/乱序处理学理）；消息面 [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)；
- S3 列存格式账本互证：[../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md](../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md) §🔧（Parquet vs 行存 2.5×——本册 D2 的 5.3× 同象不同数据，诚实并注）；
- 本册上游：03（批装载）；下游：05（编排触发）。

## 8. 配方演绎一：Firehose→S3→COPY 时序（⚠️ 转述重构；✅ gz 对象命名与 etl 目录形态互证 03/04 两章）

```
producer(kinesis_data_generator CFN ✅) → Kinesis stream(shard 数=吞吐预算)
  → Firehose(S3 目标桶, BufferInterval 60–900s / BufferSize 5–15MB 两闸门 ⚠️,
             压缩 GZIP ✅ 落地对象即证, 错误前缀重试)
  → S3 s3://bucket/prefix/2024-01-09/000.gz   (✅ 仓内文件名族)
  → COPY events FROM 's3://bucket/prefix/2024-01-09/' GZIP MANIFEST OPTIONAL(⚠️)
  → 控制表登记：batch_key='2024-01-09', row_count=SELECT count(*) 对账
```
两闸门哲学：**先攒后搬**——延迟下限=BufferInterval，上限=区间×重试；"秒级"诉求请转投 Zero-ETL（→10）。

## 9. 配方演绎二：入仓 SQL 面（⚠️ 转述示例，非原书文本）

```sql
-- 日分区装载 + 幂等重放（复用 03 章合并骨架）
COPY stg_events FROM 's3://lake/stream/etl/events/'
  IAM_ROLE 'arn:aws:iam::...:role/redshift-load' REGION 'us-west-2'
  GZIP FORMAT AS JSON 'auto' STATUPDATE OFF;          -- JSON 'auto'：⚠️→06
DELETE FROM events USING batch_done b
 WHERE events.event_date = b.batch_date;              -- 先清同批：重放安全
INSERT INTO events SELECT * FROM stg_events;
INSERT INTO batch_done SELECT DISTINCT event_date FROM stg_events;  -- 水位入账
```
要点：**装载目标先指 stg 再合并**（直写事实表=放弃幂等权）；batch_done 是本章的"记账本"。

## 10. 吞吐参数速查（⚠️ 转述，数字以官方配额页为准）

| 旋钮 | 方向 | 副作用 |
|---|---|---|
| shard 数 | ↑并行读 | Firehose 每 shard 独立缓冲→小对象更多 |
| BufferInterval/Size | ↑大批少 | 延迟↑；COPY 文件数↓（→§6-1） |
| 压缩格式 | gzip/zstd/parquet 转换 | CPU 在 Firehose 侧还是 COPY 侧的归属转移 |
| COPY 并发 | AUTO COPY 队列（→03） | WLM slot 竞争（→08） |
| stg 表拆分 | 按小时/按日 | 合并 SQL 的 DELETE 范围即幂等边界 |

## 11. 本章自查五问

1. 为什么"流直连 Redshift INSERT"在 2024 仍是反模式而 2026 被 Zero-ETL 改写？
2. Firehose 转 Parquet 后 COPY，gzip csv 路的哪两个成本被转移给了谁？
3. manifest 与日期通配二选一的判据？（→03 §6-5）
4. batch_done 控制表挡住的是哪一类事故？
5. 迟到 3 天的事件会命中哪一步 SQL？该补什么？（→§4 水位线）

## 核心概念速览（中英对照）

- Kinesis Data Streams — KDS：分片型流服务，本章造数源
- Kinesis Data Firehose — Firehose：流→S3 缓冲落地盘（压缩/转码/重试）
- 微批入仓 — micro-batch COPY：以固定节奏消费 S3 落地对象
- AUTO COPY — AUTO COPY：COPY 排队并行化的系统托管
- 数据生成器模板 — generator CFN template：仓内造流工具
- 迟到数据 — late-arriving data：事件时间晚于水位到达
- 高水位线 — high-watermark：已摄入最大事件时间/批次记号
- 小对象惩罚 — small-file penalty：S3 碎文件拖垮 COPY 并行收益
- UNLOAD — UNLOAD：仓→S3 反向导出（Parquet/Gzip/分区）
- 幂等装载 — idempotent load：重放不产生重复行的装载设计
- 流阻抗失配 — stream-vs-columnar impedance：高频小写与列存大批写的结构性冲突
- MSK/Managed Flink — 2024+ 官方流式替代线（⚠️）

## 最新演进与工业实践

- **Zero-ETL 收编流式（2024→2026）**：Kinesis/MSK 作为 Zero-ETL 摄取管道源的官方化，让"Firehose+S3+COPY 三部曲"降级为需要精细控制的场景（⚠️ 转述；✅ 主站 https://aws.amazon.com/redshift/ 200 实测 2026-09-28；Zero-ETL 专页实测 302→mgmt/ 根，改版登记）。
- **UNLOAD 到开放表格式**：UNLOAD Iceberg 目录+托管表双向打通，"仓的出口"并入湖治理（⚠️ 转述；对照 [../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md) 湖侧同款叙事）。
- **工业实践**：Flink→Redshift 的 sink（JDBC 攒批+COPY 回读）仍是大厂主流；小团队直接 Managed Flink+Zero-ETL（⚠️ 转述）；与 Kafka 生态对接的 schema 注册表（Glue Schema Registry）承担列漂移防线（⚠️）。
- **取证提醒**：本章"Firehose 布局指纹"系文件名风格推证（✅ 名实抓/⚠️ 归属推断），非官方声明。
