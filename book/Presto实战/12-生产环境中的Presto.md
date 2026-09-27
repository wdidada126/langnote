# 12 生产环境中的 Presto

> 原书第 12 章（中译本 p.211–233）。定位：运维主战场——监控读图、SQL/内存/并发/调度/网络/JVM 七类调优与资源组。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 12.1 Web UI 监控 | 集群级细节、查询列表、查询细节视图（stage DAG/task 分布） | 读图能力=排障速度 |
| 12.2 SQL 查询调优 | 分区裁剪、广播/分区 Join 选择、先收敛再联表 | 调优七分靠写法 |
| 12.3 内存管理 | 通用/保留内存池、查询熔断、溢出 spilling | 内存是 Presto 的头号死因 |
| 12.4 任务并发性 | driver 线程数、split 并发 | CPU 密集与 IO 密集的配比艺术 |
| 12.5 工作节点调度 | 任务/节点切片调度、本地调度策略 | 数据亲和 vs 均衡的拉锯 |
| 12.6 网络数据交换 | Exchange 并发与缓冲大小 | shuffle 通道的油门与刹车 |
| 12.7 JVM 调优 | GC 选型与停顿目标 | 引擎内存池之下 JVM 兜底 |
| 12.8 资源组 | 层级定义、调度策略（QA/Fair/MaxRunning/Weighted）、选择器规则 | 多租户的引擎内宪法 |

## 精讲

### 1. 监控读图三步法（12.1）
1. 列表页：找 `state` 异常滞留（QUEUED 久=资源组排队/容量不足；RUNNING 久=看下一层）；
2. 查询详情：stage 树看**最长支路**（关键路径），关注每 stage 的 tasks/failed、input/output 行数与字节；
3. task→driver 展开：找倾斜（单 task 输入量远超中位数=数据倾斜；单 operator 耗时占比>80%=算子瓶颈）。
配套指标面：`jmx` 连接器与外部采集（Prometheus exporter ⚠️ 生态件，不在本书范围）——
把 12.1 的"看图"升级为"看曲线"。

### 2. 内存体系与溢出（12.3）
- 内存池：general pool（常规算子）+ reserved pool（尖峰），`query.max-memory`/`per-node` 双熔断；
- 溢出：`experimental.spill-enabled`（⚠️ 参数名按版本）把聚合/排序/Join 中间态落盘——
  **可用但悬崖深**：交互式 SLA 下溢出≈失败前兆，宁可让熔断杀查询、事后治理写法；
- 排障链：`Exceeded memory pool capacity` → 看 stage 输入量（先收敛？）→ 看统计（CBO 广播误选？4.12 补 ANALYZE）→ 最后才动内存参数。

### 3. 并发/调度/网络三联调（12.4–12.6）
- `task.max-worker-threads`：driver 并行度基线（≈核数的倍数，CPU 密集取 2–4×⚠️ 经验值非书中保证）；
- 切片调度：`node_scheduler` 相关参数决定 split 亲和性（HDFS 块位置感知 vs 轮询均衡）；
- Exchange 缓冲：`task.http-response-*`、exchange client 并发数——大 Exchange stage 的吞吐与协调器/worker 内存共同约束；
  这条"拉式 shuffle 不落盘"的特性（4.7）意味着**网络缓冲=背压机制**：调大缓冲治标，上游产出过快治本。

### 4. 资源组：引擎内的多租户宪法（12.8）
```text
root
├── etl（maxRunning=20, queueing 上限+超时策略）
├── bi_dashboard（软/硬 CPU 限额, memory 限额）
└── adhoc_explorer（低优先, TopN 兜底限额）
```
- 层级配额 + `softCpuLimit/硬限` + CPU 配额族（参数名 ⚠️ 按版本核对，社区文档以 `cpu-quota` 系列表述）；
- 调度策略四选：`query_priority`（默认，优先级队列）、`fair`（组间公平）、`max_running`（严格并发）、
  `weighted`+`weighted.fair`（老查询提权防饿死——"老化"机制）；
- 选择器：按用户/源 IP/客户端标签把查询归组——与 10 章认证联动（无认证则选择器无抓手）。
**当代注脚**：Trino 线其后以"资源管理（resource groups → resource management/ADmission control）"体系取代
（书中时代的 `priority`/`PRIORITY` 族在 Trino 新版本已换代 ⚠️ 以 Trino 483 文档核对：
[trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅）。

### 5. SQL 调优清单（12.2 的可迁移版）
1. 分区列谓词进 WHERE（06 章纪律）；2. 大 Join 前子查询收敛+预聚合；3. `EXPLAIN` 看广播端是否真小表；
4. 高基数 `count(DISTINCT)` 换 `approx_*`（09 章）；5. ORDER BY 必配 LIMIT；6. CTE 重复引用先物化；
7. 统计缺失的表补 `ANALYZE`。与通用叙事互链 [../大数据SQL优化.md](../大数据SQL优化.md)。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| 慢查询先调参 | 八成的"参数问题"是写法/统计问题；先 EXPLAIN+读 stage 图再动配置 |
| 资源组=SLA 保证 | 它管排队与并发，不管单查询快慢；端到端 SLA 还需路由（13 章）与物化层 |
| Web UI 保留所有历史 | 查询记录有保留窗口，事故复盘要靠事件监听器落外部存储（10 章联动） |
| 溢出开了就稳 | 溢出拖长尾+打满磁盘 IO；交互式场景把它当保险丝不是变速箱 |

## 与其他章/其他笔记的联系
- 机制原理 → [04-Presto的架构.md](04-Presto的架构.md)（内存池/Exchange/局部聚合都在此埋线）；
- 部署与参数面 → [05-生产环境部署.md](05-生产环境部署.md)；审计与选择器前提 → [10-安全.md](10-安全.md)；
- 集群级路由 → [13-真实世界的案例.md](13-真实世界的案例.md)；
- 通用优化与统计 → [../大数据SQL优化.md](../大数据SQL优化.md)、[../数据库性能调优.md](../数据库性能调优.md)、
  [../千金良方_MySQL性能优化金字塔法则.md](../千金良方_MySQL性能优化金字塔法则.md)（书根存在 ✅，自检通过）。

## 本章小结与行动清单

三句话带走：
1. 调优顺序铁律：**写法 → 统计 → 资源组 → 参数**——前两步治本，后两步治标；跳步调参等于把事故延后并加价；
2. 内存与 Exchange 是同一件事的两面（在途数据不是堆内就是线上），12.3/12.6 要合并阅读；
3. 资源组是引擎内唯一的"制度"，但它管不到跨集群与物化层——完整 SLA = 资源组 + 路由 + 物化三层共建。

月度运维演练清单（SRE 视角）：
- [ ] 慢查询 Top10 读图会：每条给出 stage 关键路径结论与治理动作（写法/统计/扩容三选一）；
- [ ] 资源组压测：模拟 BI 高峰+ETL 并发，验证排队/超时/老化策略符合预期；
- [ ] 单 worker 拔除演练：确认告警可见、失败查询可重放、拓扑恢复时间记录在案；
- [ ] 参数表回归：核对自上次版本升级后失效/改名的参数（书模板 vs 现版本 diff）；
- [ ] 复盘数据回看窗口：Web UI 保留不足的部分是否已由监听器/日志补全（10 章审计联动）。

自测：
- [ ] `Exceeded memory pool capacity` 的完整排障链是什么？（12.3 三步）
- [ ] 为什么公平调度（fair/weighted）不适合 ETL 组？（老化提权反而挤占交互式配额）

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 查询详情视图 | Query Detail UI | stage DAG/task/driver 三级钻取的读图入口 |
| 关键路径 | Critical Path | 决定查询总时的最长 stage 支路 |
| 数据倾斜 | Data Skew | 单 task 承载远超均值的输入量 |
| 通用内存池 | General Memory Pool | 常规算子的引擎级内存配额 |
| 保留内存池 | Reserved Memory Pool | 吸收尖峰的第二配额 |
| 溢出 | Spilling | 中间态落盘的保险机制，性能悬崖 |
| Driver 并发 | Task Concurrency | worker 内算子链并行度 |
| 切片调度 | Split Scheduling | split 到节点的分派策略（亲和/均衡） |
| 网络交换缓冲 | Exchange Buffer | 拉式 shuffle 的在途数据上限（背压） |
| 资源组 | Resource Group | 层级化配额+准入的租户容器 |
| 选择器规则 | Selector Rules | 按用户/来源把查询路由进资源组 |
| 加权老化调度 | Weighted (Age-based) Scheduling | 防饿死的等待时间加权策略 |
| CPU 配额 | CPU Quota | 资源组的算力限额（软/硬两档） |

## 最新演进与工业实践

- **运维观测现代化**：查询详情导出（`system.runtime.queries` 归档/`EXPLAIN ANALYZE` 增强）、
  Prometheus/Grafana 生态件已成标配（社区 exporter 非官方 ⚠️）；官方监控文档入口：
  [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅ 经导航的 admin/monitoring 章。
- **资源治理换代**：Trino 以新资源管理框架替代老 resource groups（准入控制/排队改革，483 文档为现状 ✅）；
  prestodb 侧参数族随 0.29x 演进（[github.com/prestodb/presto/releases](https://github.com/prestodb/presto/releases) ✅）——
  照抄本书参数名前务必按版本对表。
- **内存与执行层重写的影响**：Velox 原生执行改变内存核算模型（arena 分配、spilling 语义重实现）——
  [github.com/facebookincubator/velox](https://github.com/facebookincubator/velox) ✅、DOI
  [10.14778/3554821.3554829](https://doi.org/10.14778/3554821.3554829) ✅（VLDB 2022）；互见 [../../db/db.md](../../db/db.md)。
- **国内印证**：美团/B 站都把"资源组+路由+物化"三层联动作为交互查询 SLA 的完整答案：
  [tech.meituan.com Presto 实践](https://tech.meituan.com/2014-06-16/presto.html) ✅、
  [dbaplus B 站原文](https://dbaplus.cn/news-73-4481-1.html) ✅（Dispatcher 限流降级即资源组之上的平台层）。
- **通用调优心法互链**：[../大数据SQL优化.md](../大数据SQL优化.md)、[../数据库性能调优.md](../数据库性能调优.md)。
