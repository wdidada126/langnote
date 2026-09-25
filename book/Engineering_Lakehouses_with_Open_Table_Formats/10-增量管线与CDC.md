# 第 10 章 增量管线与 CDC

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Iceberg 增量读/分支文档、Hudi 增量查询与 CDC 文档、Delta Change Data Feed /
> Structured Streaming 文档、Flink CDC / Debezium 公开资料。
> 对照：[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)、
> [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 | 为什么"增量"是湖仓的原生能力 | 快照差集天然就是 changelog |
| 10.2 | 增量读：三格式 API 对照 | 从"两快照之间"到"带变更明细" |
| 10.3 | Change Data Feed 的两种强度 | diff（净效果）vs cdc（前后镜像） |
| 10.4 | 流式写入：source→sink 的 exactly-once | txn 动作/epoch、Flink checkpoint 对齐 |
| 10.5 | CDC 入湖端到端蓝图 | Debezium → 格式 UPSERT 的映射表 |
| 10.6 | 分层增量：branch 与管线编排 | 用元数据能力替代拷贝 |

## 核心精讲

### 10.1 快照链 = 免费的 changelog 骨架

批处理时代的增量靠水位列（`updated_at`）或 Kafka 重放。湖仓多了一条路：
**表本身就是版本化的文件集合**，于是：

```text
增量 = snapshot(B) \ snapshot(A)  （按清单差分：新增/删除/替换的文件）
明细 = 若表记录了行级变更（delete file/log/DV/CDC 文件）则可还原到行
```

第一层（文件级差分）三家都有且默认支持；第二层（行级、含前后镜像）
需要 MOR/CDF 类特性。**选型时要区分"我要的是 delta load 还是 CDC 流"。**

### 10.2 增量读 API 对照（概念签名）

| 能力 | Iceberg | Hudi | Delta |
| --- | --- | --- | --- |
| 两版本间新增 | `incremental-append`（start/end snapshot） | Incremental 查询（`latest_state`） | `readChangeFeed`（版本区间，净效果） |
| 含删除的差分 | 快照差 + delete file 语义 | `tail_follow`/`cdc` 模式 | CDF（需开启表属性） |
| 前后镜像 | 🔧 v3 row lineage（`_change_ordinal/_operation`） | `bootstrap` + cdc（`_hoodie_before/after_image`） | CDF：`_change_type` + pre/image 列 |
| 流式消费 | Flink/Spark 以快照为微批推进 | 原生：增量 instant 即微批单元 | Structured Streaming（日志尾轮询） |

共同语义：**消费进度 = 记录"已读到哪个版本"**（Iceberg snapshot-id /
Hudi instant time / Delta version），下游只需持久化一个游标。

### 10.3 两种强度的"变更"

```text
diff 语义：UPSERT 后只知"这行变了"（净效果，压缩掉中间态）
cdc 语义：保留 update_before / update_after / delete / insert 全序列
```

- Iceberg 默认只有 diff（且 MOR 中间态不可见）；
- Delta CDF 打开后，写端在提交时**额外产出 cdc 文件**（带 `_change_type` 等
  元数据列），读端版本区间即得行级审计流；
- Hudi 的 log blocks 天然保留中间态，`cdc` 查询模式 + bootstrap
  可给下游一个 Debezium 风格的流。

一个容易忽略的工程含义：**开启 CDF/CDC ≈ 写放大**（多写一份变更文件），
并且改变"历史保留"的责任边界（10.6 的回滚窗口）。

### 10.4 流式写入的 exactly-once

三条支撑链（缺一不可）：

1. **格式层幂等**：Delta `txn` 动作（appId→epoch）；Iceberg Flink sink
   把 checkpoint id 写入快照属性；Hudi instant + `write.status` 恢复；
2. **引擎层进度**：Spark Structured Streaming 的 `_spark_checkpoints`
   （source offset + sink txn 同一原子提交）/ Flink 两阶段提交或
   幂等 sink（与 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)
   的 checkpoint↔commit 对齐原理一致）；
3. **提交频率旋钮**：checkpoint 间隔 = 表提交间隔 = 规划链增速
   （8.6 背压视角）。**"每秒提交"对管线是新鲜度胜利、对表是元数据债务**。

### 10.5 CDC 入湖端到端蓝图

```text
业务库(MySQL/PG) → Debezium/Flink-CDC → Kafka（按表分 topic，key=pk）
     → 湖写入器（Spark Structured / Flink）按表 UPSERT：
        Hudi：record key = pk，precombine = ts_ms（乱序去重）
        Iceberg(Flink)：equality delete 缓冲 + 定期 compaction（3.4）
        Delta：MERGE INTO（匹配键取 source 高版本）
```

映射要点：

| CDC 概念 | 落湖对应 | 陷阱 |
| --- | --- | --- |
| 主键 | Hudi record key / Iceberg 唯一性假设 | Iceberg 不强制唯一：上游重复投递 = 静默双行 |
| 事务顺序 | precombine/版本列 | 乱序分区变更会"复活"旧值 |
| schema change | 7 章演化 | 宽表加列若走旁路重写会打断增量读 |
| delete | 软删除文件/DV | 下游增量读 diff 不含被物理 compact 掉的旧中间态 |
| bootstrap | 全量快照阶段 | 与增量衔接的"水位"要靠格式版本对齐而非时间戳 |

### 10.6 分层增量：branch 当"发布通道"

```text
main ←— 实时管线连续写（append/UPSERT，新鲜但"脏"）
  │  promote（一次原子 fast-forward）
stage/batch ←— 批质量门（对账、DQ 断言通过）后从 main 的某快照切出
```

Iceberg refs（branch+tag，3.1）、Hudi savepoint/branch、Delta tag/branch
🔧 均已支持类似语义。价值：**下游"读已发布版本"与上游"读实时版本"
解耦**，避免每层管线各自重放拷贝一份（存储与时效双赢）。
配套的增量读游标管理（10.2）+ 保留策略（8.5）构成
"**湖内 ELT**"的骨架：跨层依赖从"拷贝 + 调度"变成"版本 + 断言"。

## 例子：分钟级增量集市（Iceberg，教学示意）

```sql
-- 下游作业每 5 分钟：读 main 分支新增，写集市增量表
SELECT * FROM sales.events
  FOR SYSTEM INCREMENTAL
  WHERE snapshot_id BETWEEN :last_consumed AND :current;   -- 概念签名
-- 同时：质量作业对 :current 打 tag 'dq-passed-<n>'，BI 只读 tag 序列
```

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "增量读保证不丢不重" | 游标持久化在**下游**：下游崩在读完未记游标之间，重放或丢数取决于下游自身幂等（10.4） |
| "CDC 入湖后表就能当 CDC 源" | diff-only 配置下中间态已被 compaction 抹掉；给下游供 cdc 需开 CDF/保留窗口 |
| "流式提交越频越好" | 新鲜度收益边际递减、元数据/冲突成本线性涨（6.7、8.6）；按消费者 SLO 定 |
| "增量管线天然跨表一致" | 单表快照一致；订单头/明细两表各自提交，跨表自洽靠设计（1.5 思考题的回收） |

## 与其他章的联系

- 10.2/10.3 → 03 章 3.4（delete 语义）、04 章 4.2（log blocks）、05 章 5.1（cdc 动作）；
- 10.4 → 06 章（提交/txn）；10.5 → 07 章（schema change 旁路）；
- 10.6 → 08 章（保留与背压）；
- 上游生态 → [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)；
  流引擎 → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。

## 思考题

1. 文件级差分（10.1）在"同一文件被 compaction 重写"时给出什么假信号？
   三格式各自如何标记"内容不变仅布局变"（dataChange/replacecommit/重写语义）以消除它？
2. 为 10.5 的表画一张"乱序度 × 格式"的容错矩阵：哪个单元必须依赖
   precombine/版本列，哪个可以靠幂等重放兜底？
3. 设计题：下游要求"湖内 CDC 总线"（任何表变更可订阅）。
   基于 10.3 + 10.6，给出 CDF 开启范围、retention、消费游标的三层约定。
4. 把"branch 发布"与调度工具的"基线依赖"对比（12 章数据质量视角），
   说明湖内版本化替换掉了 ETL 的哪两类作业。
