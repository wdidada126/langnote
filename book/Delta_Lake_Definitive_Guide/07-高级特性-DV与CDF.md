# 第 8 章 高级特性：Deletion Vectors、CDF 与表能力扩展

> 原书第 8 章「Advanced Features」（配套仓库 ch08 明确以 Deletion Vectors / merge-on-read 为主轴）。
> 本文件收拢 Delta 的「协议增强层」：**DV、Change Data Feed、生成列/标识列、CHECK、collation、
> type widening、row tracking**。机制口径参照 delta.io/Databricks 公开文档；代码为**自拟教学示意，非书中原文**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 Deletion Vectors | CoW → MoR 的转向 | DELETE/UPDATE 从「重写文件」变「追加位图」 |
| 8.2 DV 的工程后果 | 读放大、OPTIMIZE 物化、引擎兼容 | 写便宜了，读要多做一次过滤 |
| 8.3 Change Data Feed | 行级变更日志 | 把「谁变了」变成可订阅的数据 |
| 8.4 生成列 / 标识列 | 派生值入 schema | 分区列自动化、全局行 id |
| 8.5 CHECK 约束 | 后到的真约束 | 写入求值强制，替代部分质量管道 |
| 8.6 collation / type widening | 大小写不敏感、类型拓宽 | 都是 writer feature 家族的成员 |
| 8.7 row tracking | 内部行唯一键 | DV/克隆增量等特性的底座之一 |

## 核心精讲

### 8.1 Deletion Vectors：把删除变成附加信息

Copy-on-Write 的痛点（第 2 章 3.4）：改 1 行重写 1 个文件。DV 的答案：

```text
UPDATE t SET x=1 WHERE id=42;
① 定位含 id=42 的 parquet 文件 F
② 不重写 F；写一个 DV 文件：_deletion_vector_<uuid>.bin（Roaring bitmap，记录行号 1789）
③ commit：新 add action 引用 F，并在 action 里挂 deletionVector 元数据（大小/基数/路径）
```

- 行号语义：DV 记录的是**文件内绝对行位置**；同一文件后续被多个事务删不同行，
  DV 会累积/替换（新版本 DV 引用同一数据文件）。
- reader 行为：扫文件时加载 bitmap，**跳过被标记行**（merge-on-read）。
- 开关：`ALTER TABLE t SET TBLPROPERTIES (delta.enableDeletionVectors = true)`
  （DBR 10.4+ / OSS 3.2 方向；新表默认趋势是开）。协议侧体现为 writer feature `deletionVectors`
  （🔧 协议表中 DV 归 writer version 3 / table feature）。

### 8.2 DV 的工程后果（面试与生产都常考）

| 维度 | CoW | MoR（DV） |
| --- | --- | --- |
| 单次 UPDATE 代价 | O(文件大小) | O(1)：写一个小 bitmap |
| 读放大 | 无 | 每文件多读 DV + 逐行过滤 |
| 点查/OLAP 混合负载 | 友好 | 高频 DML + 高频读需要物化平衡 |
| 修复手段 | — | `OPTIMIZE` 时物化 DV（重写文件把删除落地）|
| VACUUM 职责 | 清 remove 的文件 | 还要清 DV 文件 |
| 引擎兼容 | 广 | 旧 reader 遇 DV 拒读（minReaderVersion 抬高） |

- 经验法则：**DML 频繁、读吞吐要求高的大表最受益**；几乎不删的 append-only 表无收益。
- DV 与 data skipping 的相互作用：bitmap 计数进入 stats，扫描计划里「全删文件」可直接裁掉。
- 🔧 趋势：Databricks 上 DELETE/UPDATE/MERGE 自动选择 CoW/MoR 由引擎决定，运维关注
  「DV 基数积压 → 强制 OPTIMIZE」这条新告警线。

### 8.3 Change Data Feed（CDF）

```sql
-- 教学示意
ALTER TABLE orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

SELECT * FROM TABLE(changes_of("orders", 10, 15));      -- SQL 函数形式（版本区间）
```

```python
# 流式读变更
(spark.readStream.format("delta")
  .option("readChangeFeed", "true")
  .option("startingVersion", 0)
  .table("orders"))
```

- 输出列：原表列 + `_change_type`（`insert_update_postimage` /
  `insert_update_preimage` / `delete` / `readable_change`… 以文档口径为准）
  + `_commit_version` + `_commit_timestamp`。
- 语义：**preimage/postimage 成对**给出 UPDATE 前后镜像——下游可精确还原 CDC 事件。
- 机制：开启后 commit 会额外生成 change 文件（记录受影响行的新旧镜像），**只对开启之后的版本有效**。
- 与第 6 章文件 7.3 的关系：普通流读=净插入；**CDF 流读=完整变更**。这是 Delta 侧 CDC 的正解，
  替代「软删列 + 下游猜」的土办法（详见 `10` 文件 CDC/SCD 章）。
- 代价：写放大（变更行要落 change 数据）、存储增长；下游消费同样受 VACUUM 窗口约束。

### 8.4 生成列与标识列

```sql
-- 教学示意：生成列自动填分区键
CREATE TABLE events (
  ts TIMESTAMP,
  event_date DATE GENERATED ALWAYS AS (CAST(ts AS DATE)),   -- 生成列
  user_id BIGINT,
  payload STRING
) PARTITIONED BY (event_date);

CREATE TABLE audit (
  row_id BIGINT GENERATED ALWAYS AS IDENTITY   -- 单调标识列
  (SEQUENCE START 1 NO CYCLE),
  ...
);
```

- 生成列：值由表达式派生，写入不能指定；**把「分区列维护」从管道代码里消灭**
  （bronze 层常用 `GENERATED ALWAYS AS (CAST(col(...) AS DATE))`）。
- 标识列：全局单调 id（依赖 row tracking），做去重/审计锚点；DBR 14.x+ 提供。

### 8.5 CHECK 约束

```sql
-- 教学示意
ALTER TABLE orders ADD CONSTRAINT amount_nonneg CHECK (amount >= 0);
```

- 写入时求值、违反即失败；约束本体存在表 properties（`delta.constraints.<name>`）。
- 能力边界：单行谓词；跨行/跨表业务规则仍需管道（第 11 章数据质量对照 [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)）。
- 时间线提醒：这是**后到的真约束**——2024 之前的「Delta 只有 NOT NULL」说法要更新。

### 8.6 collation 与 type widening

- **collation**：`USING COLLATION NOCASE`（DBR 15.2+ / Delta 特性 `collations`）
  让字符串比较/键值大小写不敏感——SCD/维度表的经典「Alice/alice 分裂」问题的根治。
- **type widening**：writer feature，允许 `int→bigint`、`float→double`、decimal 加宽、
  嵌套子列加宽等**免重写变更**（只改元数据）；读侧按新类型解码旧文件。
  🔧 OSS 3.x 引入、4.0 扩面；旧 reader 遇宽类型子集会按特性拒绝。

### 8.7 row tracking

- 每行附加内部 `_row_id`/`_row_commit_version`（writer feature `rowTracking`），
  跨重写保持稳定——是标识列、增量克隆、DV 物化计数等特性的底座；用户一般不直接查询，
  但排查「克隆后行级血缘」时会遇到。

## 版本演进

| 特性 | DBR / OSS 轨迹（以官方 release notes 为准） |
| --- | --- |
| DV | DBR 10.4 预览 → 9.1 LTS GA → OSS 3.2/3.3 方向；DV 默认化趋势 |
| CDF | DBR 9.1+ / OSS 2.2+（语法/函数名两边渐有差异） |
| 生成列 | DBR 较早；OSS 3.x 跟进 |
| CHECK | DBR 9.1 / OSS 3.0 |
| collation | DBR 15.2+；OSS 表特性 |
| type widening | DBR 14.x / OSS 3.x→4.0 扩面 |
| identity/row tracking | DBR 13.3–15.x 逐步 |

## 文献与文档

- delta.io *Deletion Vectors*（含「The main idea / Merge-on-read explained」主题，与配套仓库 ch08 一致）、*Change Data Feed*、*Table Features* 协议表。
- Databricks docs：*Constraints*、*Generated columns*、*Identity columns*、*Collations*。
- 对照读物：Apache Iceberg spec 的 delete files（v2 MoR）——两条格式在 MoR 上殊途同归。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「开了 DV 就不用 OPTIMIZE」 | DV 只延迟重写，不消灭重写；基数积压会拖慢读，仍需物化 |
| 2 | 「CDF 可以回看开启前的变更」 | 只对开启后的版本生效 |
| 3 | 「CHECK 能替代数据质量管道」 | 单行谓词而已；跨行/时效性/新鲜度另说 |
| 4 | 「type widening 任意改类型」 | 只有安全拓宽方向；string→int 之类仍需重写 |
| 5 | 「新特性对下游透明」 | 每个特性都动协议版本，先核对消费引擎支持表（第 5 章文件 6.6） |

## 与其他章 / 其他书的联系

- ← `02`：8.1 的对照基线是 CoW 写放大；8.3 补 3.8 时间旅行看不到的「行级变更」。
- ← `06`：7.3 的净插入流缺口由 CDF 闭合。
- → `09`：OPTIMIZE 物化 DV、liquid clustering 的取舍；→ `10`：CDC 模式首选 CDF。
- → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)：Roaring bitmap 与 parquet 行组的关系。
