# 第 8 章 并行流处理大规模数据集：MapReduce 模型

> 用并行流实现 MapReduce：`map`（转换）+ `reduce`（归约）、`collect`（收集）、`combiner` 角色。与葛一鸣 6 章、手册 6 章互补，本书明确区分「MapReduce 模型」与「MapCollect 模型」。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| map | 元素转换（无状态） |
| reduce | 可结合二元归约 |
| combiner | 并行段本地预归约 |
| 陷阱 | 共享可变累加器 |

## 二、核心精讲

### 2.1 🔧 `reduce` 必须有 combiner 且可结合
- 并行流把数据分段，每段先本地 reduce，再 `combiner` 合并；累加器与 combiner 都要**可结合、无状态**（🔧 否则结果不确定；用 `Collectors` 的 `reducing` 自带正确 combiner）。

### 2.2 别用共享可变状态
- 在 `forEach` 里累加共享变量 → 竞态（🔧 用 `reduce`/`collect` 返回新值，或 `Collectors.summingInt`；这是函数式并发的核心纪律）。

## 三、版本演进 / 论文 / 前沿

- 论文：Dean-Ghemawat MapReduce（OSDI'04，Google）；Lämmel Google 的 MapReduce 函数式模型（2007）；JDK 8 Stream。
- 工业界：Apache Hadoop/Spark（分布式 MapReduce）、Flink（流批一体）；本地并行流是单 JVM 版。
- 开源 stars（2026-09）：spark 44k / flink 25k / hadoop 15k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "forEach 里累加共享变量" | 用 reduce/collect |
| 2 | "reduce 顺序无关" | 必须可结合+有 combiner |
| 3 | "并行流跑 commonPool 做 IO" | 隔离/虚拟线程 |
