# 第 9 章 并行流处理大规模数据集：MapCollect 模型

> 用并行流做「map + collect」：把元素转换后收集到集合/分组/分区（`Collectors.groupingBy`/`partitioningBy`/`toMap`）。与 8 章 MapReduce 对照——本书独有「两模型分别适用」的剖析。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 收集器 | `toList`/`toSet`/`toMap` |
| 分组 | `groupingBy` + 下游收集器 |
| 分区 | `partitioningBy`（谓词二分） |
| 并发收集 | `toConcurrentMap`/`groupingByConcurrent` |

## 二、核心精讲

### 2.1 🔧 `groupingBy` 的并发版
- 并行流里 `Collectors.groupingBy` 内部仍要合并各段 Map，开销不小；高并发用 `groupingByConcurrent` + `toConcurrentMap` 直接写 `ConcurrentHashMap`（🔧 但 `toMap` 的 merge 函数要有幂等/可结合语义）。

### 2.2 `toMap` 冲突
- 键冲突默认抛 `IllegalStateException`（🔧 用 `toMap(key, v, mergeFn)` 指定合并；或 `(k,v1,v2)->v1` 取首/末）。

## 三、版本演进 / 论文 / 前沿

- 论文：JDK 8 `Collectors` API 设计（Stuart Marks 等）；函数式收集器源自 FP 的 fold/group。
- 工业界：Vavr/eclipse-collections 提供并行集合；kotlinx `groupingBy`（协程友好）。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "并行流 group 一定快" | 用 groupingByConcurrent |
| 2 | "toMap 冲突静默覆盖" | 默认抛；显式 mergeFn |
| 3 | "收集器有副作用" | 收集器须无状态可并行 |
