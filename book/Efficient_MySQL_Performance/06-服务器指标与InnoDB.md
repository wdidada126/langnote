# 第 6 章 服务器指标（Server Metrics and InnoDB ⚠️ 英文章题回推）

> **取证**：小节标题与页码 ✅ 中译本目录；英文章题 ⚠️ 作者站 `/learn/server-metrics-and-innodb/` 页脚 "**Chapter 6**"；
> 要旨 ⚠️ 依该页 Context（棱镜/光谱比喻）+ Key Points（12 条）/ Pitfalls（8 条）**精读重构**，**不是原书文本**。
> 官方示例仓库有 `ch06/example-6-1,6-2,6-3,6-5,6-6,6-7.sql`（✅ 实抓；**缺 6-4**，说明该例不可复现故未收录——README 自述"只收可复现示例"）。
> 返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜上一章：[05-分片.md](05-分片.md)｜下一章：[07-复制延迟.md](07-复制延迟.md)

## 一句话主旨

**服务器指标是工作负载穿过 MySQL 折射出的光谱**（spectrometry 的反向应用）——
它揭示的是**负载**的性质，不是 MySQL 的性质；所以看指标要先懂"六类指标如何互相推挤"，
再用**高分辨率（≤5 秒）**去看，否则会低估自己的应用。

## 6.1 查询性能与服务器性能对比（✅ 目录，p.164）

✅ Key Point："**MySQL 性能有两面：查询性能与服务器性能**"，且"**查询性能是输入，服务器性能是输出**"。
作者在第 1 章用查询指标解决"哪里慢"，本章反过来用服务器指标解释"**为什么**慢"。
配套 Pitfall：把服务器指标当主角（**Fixating on server metrics, ignoring query metrics and slow queries**）。

## 6.2 正常且稳定：最好的数据库是枯燥的数据库（✅ 目录，p.166）

✅ Key Point 给了"正常"的定义："**正常 = 你的应用在一个一切正常的典型日子里 MySQL 表现出的那个性能**"。
另一条更重要的（✅ Key Point）："**稳定性不限制性能，它保证任何水平的性能可持续**"。
这条与第 4 章"极限处不稳定"是同一个论点的两面（见 [04-访问模式.md](04-访问模式.md) 4.2/4.3）。

## 6.3 关键性能指示器（✅ 目录，p.167）

✅ Key Point 点名 MySQL 的 **四个 KPI**（⚠️ 重构为表）：

| KPI | 语义 | 为什么是它 |
| --- | --- | --- |
| **响应时间** | 用户唯一体验到的量 | 第 1 章的北极星，KPI 之首 |
| **错误** | 超时、锁等待超时、连接失败、死锁 | 用户能直接感知的失败 |
| **QPS** | 单位时间的查询数（负载强度） | 判断"是不是负载涨了" |
| **Threads_running** | 正在执行的线程数 | 并发排队的最灵敏信号 |

## 6.4 指标领域（✅ 目录，p.168）

✅ Key Point："指标领域由**六类**组成：**响应时间、速率（rate）、利用率（utilization）、等待（wait）、错误（error）、访问模式（access pattern）**"。
并且它们**有向相关**（✅ Key Point 原文链条，⚠️ 展开）：

> 速率 ↑ → 推高利用率 → 利用率反压把速率压回去 → 利用率（趋满）产生等待 → 等待超时变成错误。

这张因果图是本册我认为最值钱的一页：**它把几百个散落的 MySQL 状态变量归进一个可推理的骨架**，
也让"我的告警该设在哪一类"变成有答案的问题（→ 6.6）。
"访问模式"作为第六类出现，正是第 4 章论点的指标化投影。

## 6.5 光谱（✅ 目录，p.173）

本章最长的一节（p.173–205），也是章题里 "and InnoDB" 的落点：把六类指标**逐一折射到 InnoDB 的具体计数器**上
（缓冲池读写命中、LRU 与 read-ahead、页刷脏与 I/O 能力、redo/日志压力、信号量/等待）。
作者的自省很关键（✅ Key Points）：

- **只有少数指标对理解服务器性能是必需的**；其余的分别是：噪声、历史遗留、默认关闭、过于技术特定、
  只在特定场景有用、"不是真正的指标只是信息项"——他甚至还列了一条自嘲：
  "有些**凡人之躯不可参透**"（✅ 作者站原文，⚠️ 转述）。
- ✅ Pitfall："**报告所有指标**（多数没用）"、"**画图方式错误（聚合或 roll-up 选错）**"。

InnoDB 机制底图本册不重复：页与缓冲池见 [../mysql/02-Buffer-Pool.md](../mysql/02-Buffer-Pool.md)、
[../mysql/03-数据页长什么样.md](../mysql/03-数据页长什么样.md)、[../mysql/11-InnoDB内存结构.md](../mysql/11-InnoDB内存结构.md)；
磁盘与 CPU 的矛盾见 [../mysql/17-调节磁盘和CPU的矛盾.md](../mysql/17-调节磁盘和CPU的矛盾.md)；
redo 与刷脏顺序见 [../mysql/19-redo日志.md](../mysql/19-redo日志.md)、[../mysql/X2-日志系统专题.md](../mysql/X2-日志系统专题.md)。

## 6.6 监控和警报（✅ 目录，p.206）

三条判据（✅ Key Points/Pitfalls）：

1. **对"用户能体验到的东西"（如响应时间）和"客观极限"告警**，别对 arbitrary threshold 告警；
2. **分辨率要够高**：✅ Key Point "高分辨率（**≤5 秒**）能揭示低分辨率丢掉的细节"，
   Pitfall 直接把 ">10 秒" 判为低分辨率；
3. **不要用平均值评判（硬件资源除外）**：CPU/RAM/磁盘/网络用平均值是可以的，
   **响应时间类必须看分位数**——与第 1 章的 pitfall 完全一致，这是全书第二次强调。

另有一条组织层面的（✅ Pitfall）：**复制延迟要告警给应用负责人，不是 DBA**——
因为延迟是应用的数据可见性问题（下一章展开）。

## 6.7–6.9 小结与两个练习（✅ 目录，p.213–214）

⚠️ 题面未获取。按小节名重构：练习 A（检查 KPI）= 把你环境的四个 KPI 找出来、确认分辨率与保留窗口；
练习 B（检查告警与阈值）= 逐条问"这条告警用户能感知吗？是可动作的吗？阈值是客观极限还是拍脑袋？"

## 🔧 本机机制类比（**这不是 MySQL**）

**（1）计数器要按窗口取差，且必须识别重置**。模拟一个单调增长的指标（每秒采样）：
序列 `[179, 289, 480, 634, 807]`，逐秒增量 `[110, 191, 154, 173]`——**增量本身波动近 2×，
而绝对值一直在涨**：只看绝对值会得出"系统在加速"的错觉，只看平均值会抹掉尖峰。
把计数器重置为 3 后，朴素差值分别给出 **631（虚假尖峰，`results2.json`）** 与
**−2340（负增量，`results.json`）** 两种垃圾输出 → 这就是 `SHOW GLOBAL STATUS` 类计数器必须做
**重置检测 + 单调性校验**的原因（⚠️ MySQL 侧同题：状态变量在重启/重置后归零）。

**（2）全局原子的"指标计数"本身可以是负载**。4 个线程各做 75,000 次自增（合计 300,000）：

| 计数方式 | 耗时 | 比值 |
| --- | --- | --- |
| 每次自增抢一把共享锁 | **72 ms** | 基线 |
| 线程本地计数 + 结束时汇总 | **12 ms** | **5.94×** |

第二轮（200,000 次，单写者）复现同一方向：**42 ms vs 6 ms = 6.8×**（`results.json`/`results2.json`，脚本 `exp.py`/`followup.py`）。
→ 结论只用于说明"**可观测性代码自身有成本，热点行上的计数会退化为串行点**"这一机制
（对应第 4 章的热点行模式），**不是 MySQL 的 performance_schema 开销数字**。

## ⚠️ 官方手册口径（MySQL 8.4 文档转述）

- 状态变量与 `Threads_running`、`Innodb_buffer_pool_*` 系列：
  <https://dev.mysql.com/doc/refman/8.4/en/server-status-variables.html>
- 等待事件汇总（把"响应时间=执行+等待"落到表上）：`events_waits_summary_*`
  <https://dev.mysql.com/doc/refman/8.4/en/performance-schema-wait-summary-tables.html>
- 插桩开关与开销控制（"默认关闭的那一类指标"从哪来）：`setup_instruments` / `setup_consumers`
  <https://dev.mysql.com/doc/refman/8.4/en/performance-schema-setup-tables.html>
- 缓冲池、LRU 与 read-ahead：`innodb_buffer_pool_dump/load`、`innodb_random_read_ahead`
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-buffer-pool.html>
- 响应时间直方图（KPI 的正解之一）：<https://dev.mysql.com/doc/refman/8.4/en/performance-schema-statement-histogram-summary-tables.html>
- 索引/表统计（"信息项"与真指标的区分示例）：<https://dev.mysql.com/doc/refman/8.4/en/index-statistics.html>

## 本章坑（⚠️ 依作者 Pitfalls 条目重构）

把指标当 MySQL 的镜子而非负载的镜子 · 只盯服务器指标 · 报告全部指标 ·
**低分辨率（>10s）** · 聚合/roll-up 选错 · 用平均值（除硬件资源外） ·
**复制延迟告警给 DBA（应给应用负责人）** · 对任意阈值/不可动作事件告警（**寻呼疲劳与脱敏**）。

## 对位阅读

- 等待事件观测法的跨引擎对照（SQL Server wait stats ↔ `events_waits_summary_*`）：
  [../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md](../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md)
- 指标与容量设计的通用作法：[../Database_Tuning/02-调优内核.md](../Database_Tuning/02-调优内核.md)
- 内核参数与指标的关系（本册刻意淡化调参）：[../mysql/11-InnoDB内存结构.md](../mysql/11-InnoDB内存结构.md)、[../MySQL性能调优与架构设计.md](../MySQL性能调优与架构设计.md)
- 监控视角的 MySQL 8 工具链细节：[../MySQL8查询性能优化.md](../MySQL8查询性能优化.md)、[../MySQLDBA工作笔记.md](../MySQLDBA工作笔记.md)
- 告警对象与延迟归属：[07-复制延迟.md](07-复制延迟.md)、[09-其他挑战.md](09-其他挑战.md)

## 核心概念速览（中英对照）

- **查询性能 / 服务器性能** — query vs server performance：输入与输出，一因一果的两面。
- **KPI** — key performance indicators：本书取响应时间、错误、QPS、`Threads_running` 四个。
- **正在运行线程数** — `Threads_running`：并发排队最灵敏的单一信号。
- **六类指标** — six metric classes：响应时间、速率、利用率、等待、错误、访问模式。
- **反压链** — rate→utilization→wait→error：六类指标之间的有向因果关系。
- **棱镜与光谱** — prism and spectrometry：指标是负载穿过 MySQL 折射出的谱，揭示负载而非引擎。
- **正常基线** — normal：你的应用在日常好日子里表现出的那个性能水平。
- **分辨率** — resolution：采集/上报频率；本书判据是 ≤5 秒为高、>10 秒为低。
- **roll-up/聚合错误** — wrong aggregation：跨窗口汇总时选错函数（求平均/求和/取最大）导致图形说谎。
- **可动作告警** — actionable alert：收到的人能立即做点什么；否则是噪声。
- **寻呼疲劳** — pager fatigue：任意阈值与不可动作告警导致团队对告警脱敏。
- **缓冲池命中率** — buffer pool hit ratio：InnoDB 最重要的"利用率"类指标（⚠️ 手册口径）。
- **刷脏** — page flushing：把脏页写回磁盘，InnoDB 里 I/O 利用率的主体。
- **性能模式开销** — Performance Schema overhead：观测代码自身可以成为负载（本册 🔧 演示了机制）。

## 最新演进与工业实践

**2024–2026 现状**：

1. **P95/P99 已经是监控系统的默认能力**：MySQL 侧由 `events_statements_histogram_global` 提供直方图底座（⚠️ 手册口径，见上），
   指标管线侧由 Prometheus/Histogram 类承担；"平均值上大盘"在 2024 年后被视为反模式。
2. **分辨率从 60s 迁向 5–15s 不再是奢侈**：作者 2021 年的 ≤5 秒判据在今天已有普遍实现路径（
   高采集 + 降采样存储），代价是可存储量；本册 🔧（1）说明**为什么必须按窗口取差并检测重置**。
3. **观测开销的可控性提高**：performance_schema 按插桩项开关（⚠️ <https://dev.mysql.com/doc/refman/8.4/en/performance-schema-configuration.html>），
   2024–2026 通行做法是"常开语句摘要 + 按需开等待插桩"，而不是一刀切关成
   （关成不可观测会让第 1 章的"没有查询指标"坑复活）。
4. **同一方法论的跨引擎版本**：SQL Server 的 wait stats 体系与本册六类指标可对读
   [../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md](../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md)。
5. **学术侧对"OLTP 指标解释力"的实证**：Dam et al., *OLTP through the looking glass, and what we found there*,
   SIGMOD 2018, DOI <https://doi.org/10.1145/3226595.3226635>（✅ Crossref 校验）；
   尾部延迟的组织级论证仍是 Dean & Barroso, *The Tail at Scale*, CACM 2013（⚠️ 无 DOI）。
6. **压测与基准工具现状**：<https://github.com/akopytov/sysbench>（✅ 200）与官方
   <https://dev.mysql.com/doc/refman/8.4/en/mysqlslap.html>；注意基准≠你的应用（本章 6.2 的"正常"只能来自生产）。
