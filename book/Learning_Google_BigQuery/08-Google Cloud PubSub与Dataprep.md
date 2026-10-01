# 08 Google Cloud Pub/Sub 与 Dataprep 数据整备（Google Cloud Pub/Sub）

> 对应原书 **Ch.8 "Google Cloud Pub/Sub"**（含收束节 **Google Cloud Dataprep**；章题与节题 ✅ QQ 阅读电子版实抓，159–171 页逐页探针验证）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测：pubsub/docs/overview 200 ✅、dataprep 全线 404 ⚠️。
> 含 🔧 类比实验 T3（SQLite 微批提交直觉，**非 BigQuery Streaming Insert 行为**）。

## 本章在本书中的位置

终章收两件事：**数据怎么实时进来**（Pub/Sub → BigQuery）与**脏数据怎么整备**（Dataprep）。作者把流式放在最后是有意的——Ch.4 教会查、Ch.5 教会省、Ch.6 教会编程、Ch.7 教会展示之后，才轮到"让数据自己流起来"。这章也是全书对 2026 读者最"概念先行"的一章：Pub/Sub 模型十年稳定，而 BigQuery 侧的落地通道（insertAll → Streaming Insert 封装 → Storage Write API）换了三代发动机。

## 8.1 Pub/Sub 模型与定价（Introduction → Cloud Pub/Sub pricing 四节）

- 核心概念对（✅ https://docs.cloud.google.cn/pubsub/docs/overview，2026-10-02 镜像 200）：**topic（发布总线）/ subscription（消费视图）**、pull vs push、至少一次投递语义；消息即字节包，schema 自理。
- 书中操作双路径（重构自节题）：**Console 建 topic+订阅、SDK `gcloud pubsub topics create` 一行**；配 `pubsub` Python 客户端发样例消息。
- 2017 定价口径（书中原表 ⚠️）：按月基础费 + 每 GB 消息量 + API 调用次数分项——今天该模型已重构（订阅 pull/push 计费项变化、schema 注册独立计费 ⚠️ 转述），**定价表禁止照抄，只留"消息量×调用数"两个成本杠杆**。
- 关键限制（作者反复叮嘱 ⚠️）：消息**不是队列**（无优先级、保留期有限默认 7 天）、重复投递是常态——消费端必须幂等。

## 8.2 消息落地 BigQuery（Message output formats / Importing message data into BigQuery）

- 书中协议（⚠️ 转述）：每消息一条 JSON 行（NDJSON 心智），BQ 侧以 **Streaming Insert / 当时的 BigQuery 订阅通道**接收，延迟"秒级可见"是本书最大卖点句。
- 三代通道对账（重构）：书里的直连玩法 → 官方曾推 Pub/Sub→BQ 专线 → 今天的推荐解是 **BigQuery sink（Dataflow/托管管道）+ Storage Write API**；流式缓冲表（streaming buffer）、最长 6 小时才完成合并的经典告诫（⚠️ 各代细节不同，以 ✅ https://docs.cloud.google.cn/bigquery/docs/streaming-data-into-bigquery 现状为准）。
- 运维坑（书中实例，重构）：流式行**不能即时被外部表/部分 JOIN 语义看见**、乱序与迟到数据要靠 `_PARTITIONTIME`/事件时间双轨——这一节今天读 TDG 装载章更准（[../Google_BigQuery_TDG/04-将数据加载到BigQuery.md](../Google_BigQuery_TDG/04-将数据加载到BigQuery.md)）。

### 🔧 T3：微批提交直觉（SQLite 3.45.3 WAL，非 BigQuery 行为）

```python
# 2000 次逐行 commit: 0.92s   vs   20 批×100 行 commit: 0.01s  → 85 倍差
for i in range(2000): s.execute("INSERT INTO rows VALUES(?,?)",...); s.commit()
for b in range(20): s2.executemany(...); s2.commit()
```

"逐条落盘"在任何引擎都是反模式；BigQuery 流式面的真实机制（批式化写 API、行→列后台合并）**远比本类比复杂**，这里只取"攒批再提交"一条直觉，结论不可外推到 BigQuery 延迟/计费数字（⚠️）。

## 8.3 Google Cloud Dataprep（章末整备节）

- 2017 形态（⚠️ 转述）：Trifacta 血统的可视化清洗服务，**按 job 计费**；流程=连 GCS/S3 文件 → 数据剖析(profile) → 界面拼清洗规则（列合并、正则替换、行列变换）→ 导出到 GCS/仓。Ch.3 "装载前洗"主张的托管实现。
- 作者判词（重构）：分析师可自主完成 80% 脏活，规则即代码可复用；天花板是超大数据量与复杂分支逻辑，仍要回 SDK/SQL。
- 时代眼泪（诚实登记）：**Dataprep 文档已全线不可达**（dataprep/docs/* 镜像 404 ✅实测）：产品并入 Dataflow 家族（Cloud Data Prep），2025 起以 **BigQuery Data Canvas**（自然语言/AI 辅助整备）为门面 ⚠️ 转述——本章是本三册里唯一把"已消失产品"写成正章的标本。
- 概念迁移指南（给今天的读者）：Dataprep 三能力（剖析/规则/调度）现由 **Data Previews + Data Canvas + Dataflow 模板**承接；盘上工程化替代阅读 [../BigQuery_for_Data_Warehousing/04-Dataflow托管管道.md](../BigQuery_for_Data_Warehousing/04-Dataflow托管管道.md)。

## 8.4 全书结构回收（Summary 之后）

八章连成一条完整动脉：**GCP 版图(1) → 命令行(2) → 类型与清洗(3) → 查询(4) → 省与控(5) → 程序化(6) → 呈现(7) → 流式与整备(8)**。Further reading 收束节把读者发配到官方 docs/社区——Packt 短册的标准终点。三册合读时的分工（见 00 辨析表）：本书给手感，TDG 给机制，BQDW 给工程。

## 8.6 端到端例题：把一条点击流送进仓库（2017 版与 2026 版双写）

**书中版（三节命令的合流，⚠️ 转述重构）**：

```bash
gcloud pubsub topics create clicks                 # 8.1 SDK 节
gcloud pubsub subscriptions create clicks_sub --topic clicks
echo '{"event":"click","url":"/cart","ts":"2017-05-01T12:00:00Z"}' \
  | gcloud pubsub topics publish clicks --message="$(cat)"
# BigQuery 侧：Console 里给订阅挂"导入至 BigQuery"通道，目标表 proj.stream.clicks
# 表侧走当日 Streaming Insert（Ch.6 的 insertAll 协议自动代发）
bq query 'SELECT COUNT(1) FROM `proj.stream.clicks`'   # 秒级可见（书时代卖点）
```

**2026 版等价骨架（⚠️ 转述，通道名以官方页为准）**：

```bash
gcloud pubsub topics create clicks
# 方案 A：Dataflow 模板 PubsubToBigQuery（托管管道，BQDW 04 号章的主场）
# 方案 B：应用直写 Storage Write API -append 流（gRPC 批量、schema 对齐校验）
# 方案 C：仍走订阅推送，但消费端攒批提交（🔧 T3 的 85 倍教训）
gcloud dataflow jobs run clickload --gcs-location=gs://dataflow-templates/latest/Pubsub_to_BigQuery \
  --parameters=topic=projects/p/topics/clicks,bQProject=p,bQDataset=stream,bQTable=clicks
```

- 三方案共同的新增考点：**schema 一致性从"表定义检查"提前到"topic 注册检查"**（Pub/Sub Avro 强制 2021 ⚠️）——书中"坏行进死信自己捞"的裸奔时代结束；
- 读法建议：把 8.6 当 00 表"2017→2026 总表"的放大样——同一业务意图，三代管道，五倍可靠。

## 8.7 本章检查单（重构自书中例题失败榜 + 社区高频问题 ⚠️）

- [ ] JSON 字段名/类型与目标表严格一致（insertAll 行级报错逐行看）；
- [ ] 消息带事件时间列，别只信 ingestion 分区（迟到数据策略想清楚）；
- [ ] 订阅保留期与重试退避配好，死信队列 2026 已原生（⚠️）；
- [ ] 消费端幂等键（去重靠表约束或 dedup 列，书中手记"我们靠 SELECT DISTINCT 安慰自己"式自嘲 ⚠️ 重构）；
- [ ] 成本三查：Pub/Sub 消息量、流式插入 API 数、BQ 侧高频小查询聚合（Ch.4/T5 算术复用）。

## 阅读策略与坑

1. 8.1 的"至少一次+幂等消费"是全章唯一不过期的硬知识；
2. 8.2 的延迟承诺读的时候要乘以时代系数（书 200ms 级、现 Storage Write API 亚秒级，数字均 ⚠️ 以官方页为准）；
3. Dataprep 节当"数据整备产品史前史"读，动手层直接跳 Dataflow/Data Canvas 文档；
4. 本章例题依赖 GCP 项目真实计费面，**零成本替代**：本地用 🔧 T3 + 00 表 T6 组合模拟"入仓前形态"。

## 8.8 Dataprep 规则示例走读（重构：点选 20% 干脏活 80% 的往事）

一个书中风格的最小流程（CSV 脏点击日志 ⚠️ 界面细节未逐字核对）：

1. 连 GCS 采样 10 万行 → 自动剖析面板给出**每列类型推断+空值率+Top 值分布**（今天 Data Previews 同构）；
2. 对 ts 列点选 "Timestamp from text"，对 url 列拆分 query 参数为 STRUCT（正则模板）；
3. 合并重复列、丢弃全 NULL 列——每步自动生成一行类 SQL 规则（**规则即文档**的早期形态）；
4. "Merge 全量并输出到 GCS/BQ"→ 规则可存为 recipe 复用（书里强调分析师可把 recipe 交给调度 ⚠️，作者对"没讲调度"的自嘲呼应 Foreword 的 near-real-time 愿望）。

### 学完本章自测四题

1. 为什么"至少一次投递"逼着下游带幂等键？书中方案与今日方案？（DISTINCT 安慰 ⚠️ vs schema enforcement + dedup 列）
2. Streaming Insert 的行级 errors 数组怎么处理才算对？（部分成功语义，坏行进侧表复查——Ch.6 协议回收）
3. 🔧 T3 的 85 倍差在 BigQuery 流式端对应什么设计？（批式化的 Storage Write API 通道 ⚠️ 结论不外推）
4. Dataprep 消失后，其"剖析/规则/调度"三能力今天各落在哪个产品？（Data Previews / Data Canvas / Dataflow·Composer ⚠️）

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 主题/订阅 | topic / subscription | 发布-订阅两对象 |
| 拉取/推送 | pull / push | 消费两端形态 |
| 至少一次 | at-least-once delivery | 重复投递常态化 |
| 幂等消费 | idempotent consumer | 去重责任在下游 |
| 消息保留 | message retention | 默认有限期非归档 |
| 流式插入 | streaming insert / insertAll | 行级 JSON 入口 |
| 存储写 API | Storage Write API | 现代高吞吐通道 |
| 流式缓冲 | streaming buffer | 未合并行暂住区 |
| 数据整备 | data preparation | Dataprep 所治之事 |
| 剖析 | data profiling | 先看图再定规则 |
| 清洗规则复用 | reusable transforms | 规则即代码 |
| 数据画布 | BigQuery Data Canvas | Dataprep 的 AI 后裔 |

## 最新演进与工业实践

- **摄入面重铺**：Streaming Insert（书中）→ **Storage Write API**（gRPC 流、Schema FEC、Exactly-once Append 流、限流语义变化 ⚠️ 转述；✅ streaming-data-into-bigquery 页首推位）；Pub/Sub→BQ 专线通道退役/改版（⚠️）。
- **整备面换代**：Dataprep→Cloud Data Prep→**Data Canvas + Data Previews**，自然语言清洗（Gemini 辅助 ⚠️）成为 2025-26 门面——本章 8.3 的可视化点选方法论换了 UI 复活。
- **实时数仓常态化**：CDC 全家桶（Datastream ✅ pubsub 邻链、BigQuery CDC 导出 ⚠️）、近实时物化视图（✅ materialized-views-intro）接住"秒级新鲜度"的 2026 期望，书中"流式=新鲜"单点叙事已成基础设施矩阵。
- 工业实践：**流式三道闸**是社区共识——入仓前 schema registry（Pub/Sub schema enforcement 2021 ⚠️）、入仓幂等键、入仓后质量断言（information_schema + 测试框架 ⚠️）；治理视角续读 [../BigQuery_for_Data_Warehousing/08-数据治理与长期适应.md](../BigQuery_for_Data_Warehousing/08-数据治理与长期适应.md)。
