# 02 — Spark 架构与执行模型

> 原书 Ch 3: Spark's Anatomy

---

## Spark 应用的生命周期

✅ **Spark 应用 = 1 个 Driver + N 个 Executor**

```
                    ┌──────────────────────┐
                    │   Cluster Manager    │
                    │  (YARN/K8s/Standalone)│
                    └──────┬───────────────┘
                           │ 分配资源
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Executor │ │ Executor │ │ Executor │
        │ Task     │ │ Task     │ │ Task     │
        │ Task     │ │ Task     │ │ Task     │
        └──────────┘ └──────────┘ └──────────┘
              ▲
              │
        ┌──────────┐
        │  Driver  │
        │SparkSess │
        └──────────┘
```

### Driver 的职责
- ✅ 维护 SparkSession
- ✅ 将用户程序转换为 DAG
- ✅ 通过 SparkContext 向 Cluster Manager 申请资源
- ✅ 将 Task 分配给 Executor 执行
- ✅ 收集并聚合执行结果

### Executor 的职责
- ✅ 执行 Task 并返回结果
- ✅ 为需要缓存的数据提供内存存储（Storage 层）
- ✅ 每个应用有自己独立的 Executor 进程

---

## 作业执行层次

```
Application (应用)
  └── Job (作业, 由 Action 触发)
        └── Stage (阶段, 以 Shuffle 为边界)
              └── Task (任务, 最小执行单元, 1:1 对应数据分区)
```

✅ **Stage 划分**：以 Shuffle Boundary 为界，窄依赖在同一 Stage，宽依赖切分 Stage
✅ **Task 调度**：每个 Task 处理一个 Partition，是并行度的基本单位

### 窄依赖 vs 宽依赖

| 类型 | 操作示例 | 是否需要 Shuffle | Stage 影响 |
|------|----------|------------------|------------|
| 窄依赖 (Narrow) | map, filter, union | 否 | 同一 Stage |
| 宽依赖 (Wide) | groupByKey, reduceByKey, join | 是 | 切分 Stage |

> 交叉引用: [bigdata/03-Shuffle与宽依赖](../bigdata/03-Shuffle与宽依赖.md) 对 Shuffle 机制有更深入讨论

---

## Spark 的内存模型

✅ **统一内存管理**（Spark 2.0+）：Execution 内存与 Storage 内存共享同一区域，可动态借用。

```
Executor 内存布局
├── Execution Memory (执行内存)
│   ├── Shuffle 中间数据
│   ├── Join 操作的 Hash 表
│   └── 聚合操作的缓冲区
├── Storage Memory (存储内存)
│   ├── 缓存的 RDD/DataFrame 分区
│   └── Broadcast 变量
├── User Memory (用户内存)
│   └── 用户数据结构、UDF 对象
└── Reserved Memory (保留内存)
    └── Spark 内部对象 (~300MB)
```

⚠️ `spark.memory.fraction` (默认 0.6) 控制执行+存储占总内存的比例
⚠️ `spark.memory.storageFraction` (默认 0.5) 控制存储内存的最小保留比例

---

## Spark UI 关键页面

| 页面 | 内容 | 调试用途 |
|------|------|----------|
| Jobs | 作业列表、Stage 关系 | 定位慢作业 |
| Stages | Task 级别指标 | 发现数据倾斜 |
| Storage | 缓存的 RDD/DataFrame | 确认 cache 生效 |
| Environment | 配置参数 | 确认参数设置 |
| Executors | Executor 资源使用 | 监控内存/磁盘 |
| SQL | 查询的物理计划 | 分析 Catalyst 优化 |

✅ `spark.ui.port` (默认 4040) 访问 Spark UI
✅ 历史服务器 `spark.history.fs.logDirectory` 查看已完成应用

---

## 集群管理器对比

| 管理器 | 部署复杂度 | 适用场景 | 动态资源 |
|--------|-----------|----------|----------|
| Standalone | 低 | 开发/小型集群 | ✅ |
| YARN | 中 | 企业级 Hadoop 生态 | ✅ |
| Kubernetes | 高 | 云原生/弹性伸缩 | ✅ |

⚠️ 本书出版时 Mesos 仍受支持；Spark 3.0 已移除 Mesos 支持。

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：Executor ≈ DuckDB 工作线程**
- DuckDB 用多线程并行执行 Pipeline；Spark 用多 Executor 多 Task 并行
- DuckDB 单机内线程共享内存；Spark Executor 间需 Shuffle 通信
- ⚠️ 非本书引擎行为

🔧 **类比 2：Spark Stage ≈ DuckDB Pipeline**
- DuckDB 将查询分解为 Pipeline（以 blocking operator 为界）
- Spark 将 Job 分解为 Stage（以 Shuffle 为界）
- 两者都是并行执行的基本调度单位
- ⚠️ 非本书引擎行为

🔧 **类比 3：Spark UI ≈ SQLite `.timer on` + `EXPLAIN QUERY PLAN`**
- Spark UI 提供全链路可视化监控
- SQLite 的 `.timer` 和 `EXPLAIN` 提供单机版调试信息
- 功能层级不同，但目的相同：定位性能瓶颈
- ⚠️ 非本书引擎行为

🔧 **类比 4：Cluster Manager ≈ 操作系统进程调度**
- Cluster Manager 为应用分配 Executor（类似 OS 为进程分配 CPU）
- YARN ResourceManager ≈ Linux CGroup 调度器
- ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 驱动器 | Driver | 应用的主进程，维护 SparkSession |
| 执行器 | Executor | 工作进程，执行 Task |
| 作业 | Job | Action 触发的完整计算 |
| 阶段 | Stage | 以 Shuffle 为界的计算阶段 |
| 任务 | Task | 最小执行单元，对应一个 Partition |
| 窄依赖 | Narrow Dependency | 父分区→子分区一对一映射 |
| 宽依赖 | Wide Dependency | 父分区→子分区多对多映射 (Shuffle) |
| 统一内存管理 | Unified Memory Management | 执行与存储内存动态共享 |
| 集群管理器 | Cluster Manager | 分配集群资源 |

---

## 最新演进与工业实践

**架构层面的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| 统一内存管理 | 1.6+ / 2.0 GA | 取代静态内存模型，减少 OOM |
| AQE (Adaptive Query Execution) | 3.0 GA | 运行时动态优化 Shuffle 分区数、Join 策略 |
| Spark Connect | 3.4+ | 解耦客户端与 Driver，gRPC 通信 |
| Project Tungsten | 1.4-2.x | 二进制内存管理、代码生成、缓存友好的数据结构 |
| Photon (Databricks) | 3.5+ | 非 JVM 原生向量引擎，绕过 JVM GC |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- AQE 已成为生产环境默认开启项 (`spark.sql.adaptive.enabled=true`)
- Spark Connect 正在重塑 PySpark 的部署模式——客户端不再需要 JVM
- Databricks Photon 引擎在 TPC-DS 基准中表现突出，但属商业闭源
- Kubernetes 已成为云上新部署的首选集群管理器
- 流批对照: [Introduction_to_Apache_Flink](../Introduction_to_Apache_Flink/05-规模化部署与运维.md) 对比了 Flink 的部署模型
