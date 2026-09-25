# 第 8 章 Compaction 与表维护

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Iceberg 维护过程文档（rewrite_data_files/manifests、expire、orphan）、
> Hudi 文档（Compaction/Clustering/Cleaner）、Delta 文档（OPTIMIZE、VACUUM、Liquid Clustering、DV）。
> 性能视角对照 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 | 小文件问题：湖仓的熵增 | 元数据层把问题显式化，也才让它可治理 |
| 8.2 | bin-pack：所有格式的 baseline | 合并 = 一次"add+remove"的元数据事务 |
| 8.3 | 排序与聚簇：从 Z-order 到 Liquid Clustering | 布局即索引 |
| 8.4 | 三格式 compaction 语义对照 | COW 重写 / MOR 物化 / 烘焙 DV |
| 8.5 | 删除与保留治理 | delete file / log / DV 的"烘焙"，expire/vacuum/clean |
| 8.6 | 维护调度工程 | 什么时候做、用多大资源、如何不被维护拖垮 |

## 核心精讲

### 8.1 熵增的来源清单

```text
流式提交（每分钟一批）→ 每批一小组小文件
行级 UPSERT/DELETE     → 影子文件（delete file/log/DV）堆积
分区演化/重桶          → 旧布局文件成为"裁剪盲区"
失败作业               → 孤儿文件（无快照引用）
```

危害链：查询规划读元数据变慢（manifest 数/commit 重放长度线性涨）→
扫描任务数爆炸（每文件固定开销：S3 GET、footer 读）→ 队列与调度饱和。
**表格式没有制造小文件，它只是让"文件清单"变成一等公民之后，
清单膨胀从隐疾变成了可度量、可治理的指标。**

### 8.2 bin-pack 的统一抽象

三家 bin-pack 在协议层是同一件事：

```text
读若干小文件（或其已合并产物）
→ 写出 target-size 的大文件
→ 一次提交：add 新文件 + remove 旧文件（数据内容不变，集合等价）
```

Iceberg `rewrite_data_files(strategy=>binpack, target-file-size=>mb)`；
Hudi MOR compaction（deltacommit 队列驱动，log→base）；
Delta `OPTIMIZE`（含 DV 烘焙：把标记删除的行物化剔除）。
关键差异在**触发与执行模型**：Iceberg/Delta 由显式作业触发；
Hudi 的 compaction 是**表内置异步服务**（第 4 章 4.6），写者自动排产。

### 8.3 布局优化：排序是更高级的 compaction

| 技术 | 格式 | 思路 | 演化点 |
| --- | --- | --- | --- |
| sort within files | Iceberg sort order | 全表声明一个排序（如 `ts, id`），重写时执行 | 与 spec 绑定，可演化 |
| Z-order | Delta OPTIMIZE ZORDER BY / Hudi | 多维交错排序，多谓词联合裁剪 | 🔧 Delta 已不推荐新表用 |
| Hilbert | Hudi layout strategy | 比 Z-order 更好的局部性 | 实验/工具支持 |
| **Liquid Clustering** | Delta 🔧 | 无显式分区，clustering 列 + 增量 OPTIMIZE，后台渐进收敛布局 | 解决"分区选型不可逆"的痛点 |
| clustering（sort columns） | Hudi | layout strategy 声明式重排（replacecommit 原子切换） | 与 MOR/索引协同 |

共同本质：**在"写代价（重排数据）"与"读代价（裁剪失效）"之间买期权**。
Liquid Clustering 的聪明处是把期权改成分期付款——每次 OPTIMIZE 只重排
最近命中的一部分（incremental re-clustering）。

### 8.4 三格式 compaction 语义对照

| 维度 | Iceberg | Hudi | Delta |
| --- | --- | --- | --- |
| 主要对象 | 小文件 + 烘焙 delete files | MOR log files → base file | 小文件 + 烘焙 DV |
| 触发 | 显式 procedure/job | 写端自动阈值 + async service | 显式 OPTIMIZE / 平台自动 |
| 提交形态 | 普通快照追加 | `compaction.requested→inflight→replacecommit` | replace 型提交（add+remove） |
| 与并发写关系 | 重写时新 delete/新快照按校验规则合并 | 增量写继续进新 log，compact 旧组（经典交错，6.5） | 期间并发 UPSERT 走冲突检测 |
| 失败语义 | 无提交即无效（孤儿等 GC） | instant 留 inflight，可重试/回滚 | 无提交即无效 |

### 8.5 保留与清理：三种"垃圾"三把扫帚

```text
垃圾类型                扫帚（格式 → 动作）
被快照历史引用的旧文件   expire（Iceberg）/ vacuum（Delta）/ cleaner（Hudi）
无快照引用的孤儿         remove_orphan_files / vacuum 的孤儿阶段 / Hudi 类似回收
过长的元数据链           RewriteManifests / checkpoint 压缩（Delta 自动）/
                        Hudi MDT 压缩 + timeline 裁剪
```

三条铁律（运维事故高发）：

1. **retention ≥ max(下游最慢读取时长, time travel 承诺, 回滚演练窗口)**；
   VACUUM 短 retention 配 7 天以上的 BI 报表回溯 = 数据损坏；
2. **expire 与并发写的先后**：Iceberg expire 后引用旧快照的长事务提交失败
   （6.3 矩阵），清理作业要排进低峰；
3. **孤儿清理必须"older_than 足够老"**：并发作业的中间文件不能按
   "没被引用"就删——默认数天保留正是为此。

### 8.6 调度工程

- **预算化**：按"日增量 × 重排比"估 compaction CU；
  bin-pack ~1x，全表 Z-order/大重聚类可到 3–10x 扫描成本；
- **背压信号**：Hudi 看 `compaction lag`（instant 数/字节）、
  Iceberg 看 delete file 总数与 manifest 数、Delta 看
  DV 比例与 `_delta_log` 长度——**滞后 = 读端在为写端付利息**；
- **策略分层**：热分区高频小 compact（Hudi async inline）、
  冷数据周末大重排；
- 🔧 托管选项：各云（S3 Tables、Databricks serverless OPTIMIZE、
  Confluent/Starburst 等治理器）把 8.2–8.5 产品化，选型时把"谁来跑维护作业"
  计入 TCO。

## 例子：一张流式 UPSERT 表的一天（Hudi MOR，教学示意）

```text
00:00–23:59  每分钟 deltacommit：写 log blocks（append 便宜）
阈值到       产生 37 个 compaction.requested
白天         async compactor 以固定并行度消化（限流，防抢占写入资源）
cleaner      保留 N 个 instant：删被 compact 取代的旧 log/base
02:00        clustering（周日策略）：按 (region, ts) 重排上季分区
监控告警     compaction lag > 12h → 提高 compactor 资源（读端 P99 已在恶化）
```

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "compaction 是性能优化，可长期不做" | MOR/DV 表不做 compaction 会让**读路径成本超线性恶化**，并放大冲突检测工作量 |
| "文件越大越好" | 超过单任务可并行粒度（且重写代价≈文件大小）后收益反转；目标由查询选择率决定 |
| "Z-order 万能" | 单谓词高选择率时 Z-order 劣于普通排序（前缀失配）；列数>4 后裁剪急剧衰减 |
| "维护作业只读不写" | 维护本身就是**正式提交者**（replacecommit/add+remove），必须参与第 6 章的并发协议 |

## 与其他章的联系

- 8.2/8.4 → 03 章 3.5、04 章 4.6、05 章 5.5 的横切汇总；
- 8.3 布局 ↔ 7.5 分区演化的"重写收敛"步骤；
- 8.5 并发约束 → 06 章；8.6 背压 → 10 章流式管线的落地前提；
- 扫描侧优化对照 → [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)、
  [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。

## 思考题

1. bin-pack 的"集合等价提交"在第 6 章三家协议下各要校验什么？
   构造一个"bin-pack 与 UPSERT 并发"的交错，说明谁输谁赢及原因。
2. 推导 MOR 表 compaction 滞后时查询成本的粗略模型：
   `C ≈ base读 + Σlog读 + 合并开销`，用指标（log 文件数/块大小）验证告警阈值。
3. Liquid Clustering 宣称"免分区"。从 8.3 与 7.5 联合论证：
   它消灭了什么、又引入了什么新的维护义务？
4. 给一个保留策略论证：BI 回溯 14 天 + 审计要求 90 天可回放 + 存储预算紧。
   三格式各用哪些旋钮（refs/savepoint/tag）拼出方案？哪里必须妥协？
