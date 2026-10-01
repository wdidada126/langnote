# 03 Spark 集群架构解析（对应原书 Ch3，印张页 45–57）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页；正文为**精读重构**，非原书文本；机制性展开以 Spark 公开文档语义为据，标 ⚠️ 处不保证与原文逐句对应。

## 官方二级目录（✅ 实抓）

- Anatomy of a Spark Application (p.45)
- Spark Driver (p.46)
- Spark Workers and Executors (p.49)
- The Spark Master and Cluster Manager (p.51)
- Spark Applications Using the Standalone Scheduler (p.53)
- Spark Applications Running on YARN (p.53)
- Deployment Modes for Spark Applications Running on YARN (p.53)
- Client Mode (p.54) ／ Cluster Mode (p.55)
- Local Mode Revisited (p.56)
- Summary (p.57)

## 本章在全书的结构作用

Ch2 给「怎么装」，Ch3 给「装好后进程之间怎么说话」。此后 Ch4–Ch7 的每个 API 行为
（分区、shuffle、闭包分发、executor 内存）都挂在本章的进程模型上。书内引用链：
Ch5 调优 → 依赖 Executor 内存模型；Ch7 流处理 → 依赖 Driver 常驻。

## 精读重构·应用解剖三分法（p.45–51）

官方 TOC 的进程角色清单，重构为一张对答表：

| 角色 | 在哪运行 | 干什么 | Python 特有注意 |
|---|---|---|---|
| Driver | 提交端(client)或容器内(cluster) | 建 SparkContext、DAG 调度、任务结果收集 | 主进程持有 `SparkContext`；异常栈回到终端 |
| Executor | 工作节点 JVM | 执行任务、缓存分区、回传结果 | 每 executor 配一个 **Python worker 子进程**，JVM↔Python 以 pickle 管道通信 |
| Worker | 工作节点守护进程 | 按 Master/CM 指令起 executor | Standalone 的 `Worker` 与「executor 线程槽」是两个概念，读者常混 |
| Master/Cluster Manager | 头节点/资源系统 | 资源协商与分配 | YARN 的 ResourceManager 即 CM，见下 |

**Driver 细节（p.46–48 ⚠️ 推定）**：SparkSession/SparkContext 创建点、闭包与共享变量
（broadcast/accumulator 的注册表）随任务序列化下发——这正是 Ch1「Python 对象序列化」铺垫的用武之地，
也是 Ch5 大变量陷阱（成员变量被整个捕获）的机制根源。

**Executor 内部（p.49–51 ⚠️ 推定）**：核数=并发任务槽；task 失败按分区 lineage 重算；
`spark.executor.memory` 等参数在此章首次出现在配置语境（细则在 Ch5 p.141 起）。

## 精读重构·两种调度器下的应用流（p.53–56）

1. **Standalone（p.53）**：client 提交 → Master 登记应用 → 向 Worker 申请 executor 插槽 →
   Driver 直连各 executor 派发任务。UI：Master :8080 看应用列表，应用 :4040 看 job/stage/task。
2. **YARN（p.53–56）**：spark-submit 向 ResourceManager 要 AM 容器：
   - **Client Mode**：Driver 在提交机，AM 只管 executor——适合交互调试，提交机断则应用亡 ⚠️ 推定书中强调。
   - **Cluster Mode**：Driver 进 AM 容器——生产批作业标准姿势，长流作业也必须此模式（呼应 Ch7）。
3. **Local Mode Revisited（p.56）**：所有角色折叠进单 JVM 多线程；`local`/`local[N]`/`local[*]`
   的并行度语义差别；「本地能跑≠集群能跑」的原因（并行分区数、内存切分、闭包序列化）在此收口。

示意（⚠️ 概念图非原书复刻）：

```text
YARN Cluster Mode 拓扑
提交机 --spark-submit--> ResourceManager --AM容器--> [Driver]
                                     |-> Container [Executor1 <-> Python worker]
                                     |-> Container [Executor2 <-> Python worker]
```

> repo 对照：同一模型在 Spark 3/4 时代的最精炼现行版，见
> [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)；
> 中文生态的通俗讲解对照 [../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)（盘上单文件）。

🔧 **单机进程模型类比（非本书 Spark 引擎行为）**：以 SQLite 多连接并发写模拟「Driver 集中协调 + 工作进程分片」的反例——
本机 sqlite3 3.45.3（🔧 随 Python 3.13.2 可用）单库多进程写锁竞争是众所周知的吞吐天花板，
而 DuckDB 1.5.5（🔧 同环境导入成功）进程内并行扫描同一表则无锁；
这组对照说明：**并行度的本质在数据切分而非进程数量**，恰与 Ch3「executor 核数×分区数决定真并行」同构
（方法：对 `analogies.py` 生成的 20 万行 events 表分别做 DuckDB 进程内聚合与 SQLite 单连接聚合计时，
见 06 文件 E4 组数据，SQLite join 0.1678 s vs DuckDB 0.0246 s，单进程内并行差距 6.8 倍）。

## 常见误区与读法提示

1. 把 Worker 与 Executor 混为一谈：Worker 是节点守护进程，Executor 是应用级 JVM。
2. 以为 YARN Cluster Mode 下终端 Ctrl-C 能停应用：应用活在 AM 容器里，须 `yarn application -kill` ⚠️ 转述。
3. Python API 的双进程模型（JVM+CPython）在 2018 年书里着墨有限，但它是 PySpark 性能话题的根因，
   读 Ch5 优化节时务必回头补这条机制线。

## 复习要点与自测清单

1. 角色卡默写：Driver/Executor/Worker/Master(或 CM) 四角色，各自「活多久、管什么、Python 侧多什么进程」。
2. 画出 YARN client 与 cluster 两拓扑，标注 Driver 位置与终端断开后的应用存活差异。
3. 说清 `local`/`local[4]`/`local[*]` 三取值语义；解释「本地能跑集群翻车」三大惯犯。
4. Python worker 双进程管道：任务闭包如何到 CPython、结果如何回 JVM（pickle 成本出处）。
5. executor 核数与任务槽换算：给定 2 executor×4 核，同时最多几个 task？分区数更多时发生什么？
6. UI 端口记忆：Master 8080 / 应用 4040 / History 18080 的分工 ⚠️ 现行版本有出入，以官方文档为准。
7. 自检题：Driver 端 OOM 的三种成因路径（collect、大广播、累加器字典），各自在哪一章回防（Ch4/Ch5）。
8. 教学迁移：用 🔧 E4 单机双引擎数据（DuckDB 0.0246 s vs SQLite 0.1678 s）向新人解释
   「进程内并行」与「跨机并行」的同构与边界（非 Spark 行为，只做思想实验）。
9. 拓扑变体题：K8s 部署下本表四角色如何改名（driver pod/executor pod/提交端），
   哪些关系不变？——这是本章通往 2026 年主流形态的桥（⚠️ 转述，见演进节）。
10. 一句话总结：本章唯一的长期有效知识是「角色×部署模式」矩阵，其余进程细节随版本演化快速折旧。
11. 自检题：Standalone 调度与 YARN 调度下，executor 启动失败分别首先查哪个日志/UI？（Master UI vs RM 应用页）

## 核心概念速览（中英对照）

- **驱动器** — Driver：持有 SparkContext、构建 DAG、调度任务并收集结果的主进程角色。
- **执行器** — Executor：在工作节点上运行任务、缓存分区并回传结果的 JVM 进程。
- **工作守护进程** — Worker：Standalone 集群中接收 Master 指令、拉起 executor 的节点常驻进程。
- **应用主控器** — Application Master (AM)：YARN 中代表单个 Spark 应用的资源协调容器。
- **客户端模式** — Client Mode：Driver 运行在提交机上的部署模式，用于调试与交互。
- **集群模式** — Cluster Mode：Driver 运行在集群容器内的部署模式，生产默认。
- **任务槽** — Task Slot / Core：executor 内核数对应的并发任务容量。
- **DAG 调度** — DAG Scheduler：把 RDD/job 图切分为 stage 并派发 task 的驱动侧机制。
- **闭包分发** — Closure Shipping：任务函数连同其引用对象序列化后发往 executor。
- **Python worker** — Python Worker Process：executor JVM 旁挂的 CPython 子进程，经 pickle 管道交换数据。

## 最新演进与工业实践

- **进程模型未变、调度目标扩容**：Driver/Executor/CM 三层抽象到 2026 年官方文档仍是第一页内容
  （https://spark.apache.org/docs/latest/rdd-programming-guide.html ，✅ curl -sI 200 复核），
  新增的是 Kubernetes 原生调度路径，AM/YARN 叙事权重下降 ⚠️ 转述。
- **Python worker 性能叙事翻新**：PySpark 3.x 的 Arrow-based Pandas UDF（批量向量化替代逐行 pickle）
  是对本章「JVM↔Python 管道」痛点的正面回应；官方文档见上述 RDD/SQL 指南链 ⚠️ 转述细节。
- **Web UI 与事件日志**：4040/18080 生态延续，观测面新增 Spark History Server v4 重写方向 ⚠️ 转述；
  repo 生产视角补充：[../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)。
- **单机替代方案成熟**：🔧 本波实测证实——数十万行级的「架构感知+聚合」实验在
  DuckDB 1.5.5/SQLite 3.45.3 单机毫秒级即可完成，学习架构概念不再需要真集群；
  真集群的独特价值留在跨机扩展、容错与多租户，正与本章角色分工的叙事互相印证（非本书 Spark 引擎行为）。
