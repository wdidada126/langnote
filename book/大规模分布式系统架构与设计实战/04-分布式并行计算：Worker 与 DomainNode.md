# 第 4 章　分布式并行计算：Worker 与 DomainNode

> 原书用 Worker（计算单元）+ DomainNode（域节点）来描述「把任务分到多机并行跑」，
> 意图对标 Hadoop MapReduce。MapReduce 有论文、有分片/调度/容错完整语义；
> fourinone 的并行计算模型书里以 API 演示为主，**分片策略、失败重试、数据本地性、
> 中间结果 shuffle 等关键环节的深度存疑**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 并行计算要解决的问题 | 数据分片、任务派发、聚合结果 | 不止「多线程」，还有容错与数据 locality |
| 4.2 Worker 与 DomainNode | 计算单元 + 其宿主域 | 类似 MapReduce Task + NodeManager 雏形 |
| 4.3 任务派发与聚合 | 主把活分给 Worker，收结果 | 缺失败重试/推测执行等生产语义，存疑 |
| 4.4 与 MapReduce 对照 | 能力重叠但成熟度差距大 | Hadoop 15670★ vs fourinone 85★ |
| 4.5 模型总评 | 🔧 缺 shuffle/本地性/容错细节 | 教学示意级，非生产级 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 4.1 一个并行计算的最小骨架（教学示意）

```text
# 教学示意，不参与构建：并行求和的两种范式
MapReduce 范式:
    map(task):   处理分片 -> 产出 <key, value> 列表
    shuffle:     按 key 归并到 reducer（网络传输，最贵的一步）
    reduce(task): 聚合同 key 的值
fourinone 范式（依 API 文档重构）:
    Worker.doTask(input):  在 DomainNode 上执行一段逻辑
    主节点收集各 Worker 的返回，自行聚合
    -> 相当于"用户自己写 map + 自己写收口"，shuffle 由用户负责
```

### 4.3 生产级并行计算不能省略的环节

| 环节 | 为什么不能省 | MapReduce 怎么做 | fourinone 是否覆盖（存疑） |
| --- | --- | --- | --- |
| 数据本地性 | 避免跨网络搬数据 | 调度尽量把任务放到数据所在节点 | 未展示，存疑 |
| 失败重试 | 节点必挂 | 任务失败重新调度 | 未展示，存疑 |
| 推测执行 | 慢节点拖垮整体 | 同任务跑两份取快者 | 未展示，存疑 |
| 中间 shuffle | 跨 key 归并必经网络 | 框架托管 | 由用户自管，易错 |

> 这张表说明：fourinone 把「并行计算」简化成了「多机跑函数 + 主节点收结果」，
> 而 MapReduce 真正难的恰恰是上表右两列。书里对这些难点的处理深度**未能核实，存疑**。

## 版本演进

- 本书无第二版记录。
- **2013 年口径**：Hadoop MapReduce 是主流，Spark（2014 论文）尚未普及；
  「轻量并行框架」有市场空间。
- **2026 年视角**：MapReduce 已被 **Spark / Flink** 取代；
  批流一体、列式、内存计算是常态。fourinone 的「类 MapReduce 简化版」既不如 MapReduce 成熟，
  也不如 Spark 先进。
- 🔧 **必须补入**：Spark（2014）、Flink（流式，2015 前后）之后，简化版 MapReduce 的价值
  基本归零；今天的并行计算默认答案是「专用引擎 + K8s/YARN 调度」。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Dean, Ghemawat《MapReduce: Simplified Data Processing on Large Clusters》 | OSDI 2004 | 并行计算范式源头（本书对标对象） |
| Zaharia et al.《Resilient Distributed Datasets (RDD)》 | NSDI 2012 | Spark，内存容错计算 | 
| Zaharia et al.《Faster Straggler Mitigation》(推测执行相关) | 多文 | 慢节点处理 |
| 本书引用情况 | — | **未给出明确原始文献**；以 API 演示为主，存疑 |

## 近年研究与工业界开源实践（2015–2026）

- **Hadoop** `apache/hadoop` **15670★**（2026-09-27 实测，含 MapReduce + YARN + HDFS）。
- **Spark** `apache/spark`（体量远超 fourinone，行业默认批处理引擎）、
  **Flink** `apache/flink`（流式/批流一体主流）。
- **fourinone** `fourinone/fourinone` **85★**：并行计算模块的真实采用近乎可忽略。
- **调度层**：YARN / Kubernetes（128032★）才是今天承载并行计算的调度底座，
  fourinone 的 DomainNode 自管调度在现代视角下既不标准也不可扩展。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「多机跑函数 = 分布式计算」 | 缺数据本地性/容错/推测执行/shuffle，只是并行执行 | 🔧 本书 |
| 2 | 「fourinone 能替代 Hadoop」 | 成熟度、生态、采用量差数量级（85 vs 15670） | 🔧 本书 + 笔记原文 |
| 3 | 「并行计算很简单」 | 真正难在失败处理与数据搬运，书里深度不足 | 🔧 2026 视角 |
| 4 | shuffle/容错机制书中未展开 | 未能核实 fourinone 是否具备，**存疑** | 本书存疑 |
| 5 | 缺少基准对比 | 无可复核的吞吐/加速比数据，「轻量」无证据 | 笔记原文 |

## 与其他章 / 其他书的联系

- **本书内**：4.2 Worker/DomainNode ← [02-核心模型](02-核心模型：Domain·Park·Node·FttpAdapter·Worker.md)；
  计算任务常通过 [05-分布式文件](05-分布式文件：FttpAdapter·fttp.md) 读写数据。
- [../大规模分布式存储系统/13-大数据.md](../大规模分布式存储系统/13-大数据.md)
  ——MapReduce 及其扩展（Tenzing/Dryad/Pregel）、流式计算（Storm）的系统讲法。
- [../设计数据密集型应用/10-批处理与流处理.md](../设计数据密集型应用/10-批处理与流处理.md)
  ——批/流处理的现代视角，对照本章简化模型。
- [../分布式系统/00-总览与阅读地图.md](../分布式系统/00-总览与阅读地图.md)（van Steen）
  ——分布式计算的通用模型。
