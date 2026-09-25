# 第 5 章 Delta Lake 表格式机制

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Delta Lake 协议文档（Delta Protocol / Transaction Log / Deletion Vectors / Liquid Clustering 官方文档）、Delta 1.x/3.x 发布说明。SQL 为教学示意。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 | 事务日志的形状 | commit JSON 是动作流，checkpoint 是物化视图 |
| 5.2 | 读路径：重放 + 裁剪 | 为什么 Delta 规划"看日志尾巴" |
| 5.3 | 提交协议与命名约定 | 版本号即互斥锁 |
| 5.4 | 行级更新：从 COW 到 deletion vectors | 与 Iceberg v2/Hudi MOR 的趋同 |
| 5.5 | 表管理设施：OPTIMIZE / VACUUM / ZORDER / Liquid Clustering | 维护动作的协议语义 |
| 5.6 | 协议演化：capabilities、table features、UniForm | 兼容性如何被"声明"出来 |

## 核心精讲

### 5.1 commit JSON：一组带 schema 的动作

`_delta_log/<20位补零版本>.json` 每行一个动作（协议文档给每类动作定了字段）：

```text
commitInfo   操作者、操作类型、读/写窗口（含 predicate 读集，供冲突检测）
protocol     minReader/minWriterVersion + 启用的 table features 列表
metaData     schema、partitionColumns、configuration、id
txn          流式写入的 appId→epochTxnVersion（幂等重放的锚点）
add / remove 文件进/出当前状态（add 带 partitionValues、stats JSON、
             dataChange 标志、删除向量引用）
cdc          Change Data Feed 的 cdc 文件（按 _change_type 标注 insert/update_preimage/…）
domainMetadata 各特性的私有元数据挂点（如 clustering、row tracking）
```

checkpoint（`<v>.checkpoint.parquet`，每 10 个版本一份默认）把 ≤v 的
add/remove **折叠成"当前活文件全集 + 元数据"** 的 parquet；
🔧 **V2 checkpoint** 进一步把分区、统计（v2stats 内嵌 DV 信息）、
以及 action vector（位图，配合多部分上传安全）拆列存化。

一句话对照 Iceberg：**Delta 的"当前状态"是算出来的（重放），
Iceberg 的是写进去的（manifest 树引用）**；checkpoint 就是把计算结果缓存成引用。

### 5.2 读路径

```text
定位 ≤V 的最新 checkpoint(.snapshot 文件加速) → 载入活文件集
→ 重放 checkpoint 之后至 V 的 commit → 应用 add/remove/DV
→ 按 partitionValues + per-file stats 裁剪 → 扫描任务
```

per-file `stats` 是 JSON 字符串（min/max/nullCount + 🔧 新版本 per-column
计数），粒度到文件级、无独立"manifest 层"——因此**分区裁剪强、文件内统计弱于
Iceberg 的多级漏斗**，超大表规划依赖 checkpoint 新鲜度与 DV 处理（协议中
`DeletionVectorDescriptor` 记录相对路径 + 大小 + 匹配行数列）。

### 5.3 提交协议：靠"文件名不可重复"完成 CAS

无 catalog 参与时，Delta 的并发协议是**文件系统上的乐观锁**：

```text
读当前版本 N（+ 自己生成的 N+1 commit 内容）
原子尝试创建 _delta_log/(N+1).json   ← 存在即失败（S3 条件写/HDFS createFile）
失败 → 读胜出者 commit → 与自己的读集/写集做冲突校验
     → 无冲突则基于新版本重算 N+2 再试；有冲突则抛 ConcurrentAppend/
       ConcurrentTransaction/ConcurrentUpdate
```

要点：**协议只承诺"串行化的元数据变更"，不承诺"不白干"**——数据文件已写好，
校验失败时成为孤儿（VACUUM 的 `--retention` 外再清）。完整冲突矩阵在第 6 章。

- **blind append 快路径**：纯 append 无读集，跳过冲突检测直接提交，
  这是 Delta 高频小提交仍然稳定的原因；
- **txn 动作**：流式 source 把 offset 写进 txn(appId)，崩溃重放时
  跳过已提交 epoch——**Exactly-once 的账本**。

### 5.4 行级更新与 DV

- 早期：UPDATE/DELETE/MERGE = 重写命中分区的全部相关文件（纯 COW，写放大恐怖）；
- 🔧 现在：**deletion vectors**（parquet 存行号位图）标记失效行，
  新值走新文件；`MERGE` 写 DV 而非重写；读端 DV 反连接。
  与 Iceberg v2 position delete/DV、Hudi DV 三家趋同（第 8 章统一视角：
  **"影子删除 + 异步烘焙"是行级更新的收敛解**）；
- 前提：**row tracking**（内部 `_rowId`）稳定行身份，DV 才有挂靠点。

### 5.5 表管理设施

| 动作 | 协议语义 | 旋钮 |
| --- | --- | --- |
| OPTIMIZE | 一次 replace 型提交：add 合并后文件 + remove 旧文件 | bin-patch / 🔧 smart（自动布局）；ZORDER 列 / liquid clustering |
| VACUUM | 删除"已不被 <V-retention 之后任何快照引用"的文件 | retention（默认 7 天）；**长时间旅行读者会被它背刺** |
| RESTORE / CLONE | 把版本指针切回旧 snapshot（shallow clone 仅拷元数据） | clone 是迁移/分支的基础设施 |
| DESCRIBE HISTORY | 列 commitInfo 摘要 | 审计入口 |

### 5.6 协议演化与 UniForm

- 兼容性模型：**minReaderVersion/minWriterVersion + 特性表**
  （v3 协议改为显式 table features 列表，未支持特性可拒绝读/写）；
- **column mapping**：靠内部 `delta.id`↔外部名映射实现安全的
  rename/remove/add-reorder——解决"Hive/Parquet 改列名静默错数据"的世仇（第 7 章）；
- **UniForm**：同一份数据 + 后台在 commit 时生成 Iceberg/Hudi 元数据镜像，
  让三格式引擎"各认各的 catalog 入口"读同一张物理表（第 9 章互操作主角之一）。

## 例子：一次 UPDATE 在日志里留下什么

```jsonc
// _delta_log/00000000000000000042.json（教学示意，字段省略大半）
{"commitInfo":{"operation":"UPDATE","readVersion":41, ...}}
{"protocol":{"minReaderVersion":3,"minWriterVersion":7,
             "writerFeatures":["deletionVectors","rowTracking"]}}
{"remove":{"path":"part-...parquet","deletionVector":
           {"storagePart":"...","sizeInBytes":512,"numDeletedValues":37}}}
{"add":{"path":"part-...new.parquet",
        "deletionVector":{"relativePath":"...dv.json","numDeletedValues":4},
        "stats":"{\"minValues\":{\"amt\":1},\"maxValues\":{\"amt\":999}}",
        "dataChange":true}}
```

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Delta 开源版 = Databricks 体验" | OPTIMIZE 自动调度、 Liquid Clustering 全自动托管、 SQL DDL 糖属平台能力；开源协议内核一致，运维面自己补 |
| "VACUUM 只是清垃圾" | 它是**保留策略执行器**：retention 必须 ≥ 最长时间旅行/慢读者窗口，否则损坏历史 |
| "checkpoint 删了只是变慢" | 早期版本丢了 checkpoint 仍可全量重放；**日志本身断了才致命**——但运维上 _delta_log 必须与数据同备份域 |
| "有 DV 就不用 OPTIMIZE" | DV 只解决写放大，不解决小文件/读放大；烘焙进新 base 仍靠 OPTIMIZE |

## 与其他章的联系

- 5.3 提交协议 → 第 6 章冲突矩阵全展开；
- 5.4 DV → 与 03 章 3.4、04 章 4.2 并列为"影子删除"三实现；
- 5.5 维护 → 第 8 章；5.6 UniForm → 第 9 章；
- 与 Delta 专书（规划中的姊妹笔记，见 00 章）的分工：本章只保留"协议层"骨架。

## 思考题

1. "纯 append 走 blind 快路径、覆写操作走冲突检测"——推导：流式作业
   （append）与批 UPSERT（overwrite）同表并发时，**谁会被谁重试**？
   读 `commitInfo.readVersion` 能否事后复原这个交错？
2. Delta 的 checkpoint 每 10 版一份：把"读放大（重放 commit 数）"与
   "写放大（checkpoint 生成开销）"写成间隔的函数，说明默认值 10 的权衡。
3. column mapping 用内部 id 解耦列名。对比 Iceberg field-id：
   两者在"旧 Parquet 文件不含 id"这一点上如何统一处理？
   （提示：Iceberg 靠 `column.id` parquet 元数据，Delta 靠 schema 重写映射。）
4. 若把 _delta_log 想象成 binlog、checkpoint 想象成 redo checkpoint，
   对照 [../mysql/19-redo日志.md](../mysql/19-redo日志.md)：哪些 InnoDB 概念
   在这里**没有**对应物？（提示：崩溃恢复、LSN 复用）为什么不需要？
