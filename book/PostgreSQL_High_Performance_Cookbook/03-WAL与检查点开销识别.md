# 第 3 章 WAL 与检查点开销识别（⚠️ 章题为中文重建，非原书目录引用）

> 《PostgreSQL High Performance Cookbook》第 3 章精读重构。recipe 锚点 ✅ 实抓自官方代码仓
> `Chapter 03/Chapter3.txt`（"Identifying checkpoint overhead"）；阅读地图见
> [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 3.1 本章定位

第 1 章量了硬件写能力，本章回答"PG 自己制造了多少写"：WAL 生成、检查点风暴、缓冲缓存占用。
官方 txt 实录给出两个标志性动作：`SELECT * FROM pg_stat_activity WHERE wait_event = 'CheckpointLock'`
与 `CREATE EXTENSION pg_buffercache` 查共享缓冲——**以等待事件与缓存透视定位检查点开销**，
这正是 9.6 新引入的 wait_event 观测体系的首次实战（2017 基线的时代印记）。

## 3.2 配方地图（✅ txt 实抓 + ⚠️ 章内其余配方为主题归并）

1. Identifying checkpoint overhead（✅ 官方题录；本章 txt 仅此代表题，其余 ⚠️ 按 README 与
   9.6 文档语境归并：检查点参数调优、WAL 卷布局、缓冲缓存分析）

## 3.3 代表配方精读

### 配方：Identifying checkpoint overhead

- **观测面**：
  - `pg_stat_activity` 按 `wait_event_type='Timeout' AND wait_event='CheckpointSyncStateChange'?`——
    官方 txt 原样为 `wait_event = 'CheckpointLock'`（✅ 实抓原文；PG 各版 wait 事件名有增删，
    以当日文档为准 ⚠️）。
  - `pg_stat_bgwriter`：`checkpoints_timed/req`、`buffers_checkpoint`——检查点写了多少脏页、
    超频检查点（req 占比高）说明 `max_wal_size` 太小。⚠️ 转述+✅ 手册（文末 URL）。
  - `log_checkpoints=on` 后日志直接给"MM seconds to complete, XX MB of WAL written"。
- **判读规则**（社区共识，⚠️）：`checkpoints_req >> checkpoints_timed` → 加大 `max_wal_size` 或
  提高写入端并行度摊平；单次检查点耗时逼近 `checkpoint_timeout` → `checkpoint_completion_target`
  调大（当日 0.5→0.75/0.9，PG14+ 默认 0.9 ✅ 手册核对项，细节 ⚠️）。
- **fsync 视角**：检查点是周期性写风暴，与第 1 章 fsync/seek 基准对表——盘能力不足时表现为
  周期性 TPS 毛刺，这是"检查点抖动"的经典指纹。

### 配方：Working with pg_buffercache（✅ txt 实录）

- `CREATE EXTENSION pg_buffercache; SELECT ... FROM pg_buffercache` 看共享缓冲里**哪些 relation
  占了哪些页**：缓存命中率低是"占缓存的不对"而非"缓存太小"的第一嫌疑。
- 配合第 12 章索引块统计、第 11 章冷热缓存实验，构成"内存-页"证据链。
- ⚠️ 该视图是观测不是优化：调 `shared_buffers` 前必须先用它证明工作集装不下。

### 配方：WAL 相关参数与布局（⚠️ 主题归并）

- `wal_buffers`（9.6 起 -1=自动按 SLRU 启发）、`checkpoint_timeout`、`max_wal_size`/`min_wal_size`、
  `full_page_writes`（停用的风险与 PITR 破坏——当日即告诫，今依旧）、`commit_delay/commit_siblings`
  （组提交，现代 SSD 上基本放弃）。⚠️ 转述，✅ 手册 runtime-config-wal。
- 把 WAL 放独立卷的建议在 2017 有意义（HDD seek 竞争），NVMe 多队列时代此配方多数场景**已失效**——
  见 3.6 与演进节。

## 3.4 机制小深潜：检查点与"两阶段"

检查点=写 Redo 记录→fsync 数据文件→更新 pg_control→按 completion_target 平滑刷脏→截断 WAL。
理解"脏页平滑写"才能理解为什么 bgwriter 与 checkpointer 分工（PG9.4 起 checkpointer 独立进程，⚠️）。
对照阅读：[../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md](../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md)
（写放大另一半来自死元组）与 [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md) 的 WAL/缓冲管理章。

## 3.5 repo 对照

- 通用视角的日志式恢复与"组提交/延迟写"权衡：[../Database_Tuning/02-调优内核.md](../Database_Tuning/02-调优内核.md)。
- 引擎对照：InnoDB 的 redo 刷写点与 doublewrite vs PG 全页写——[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)。
- PG16 时代的同题食谱（性能与并发章含 buffer/IO 新观测）：[../PostgreSQL_16_Administration_Cookbook/05-性能与并发.md](../PostgreSQL_16_Administration_Cookbook/05-性能与并发.md)。

## 3.6 🔧 类比实测（非 PostgreSQL 行为；PG 不可装 ✅ where psql 无输出）

- **X-C（sqlite3 3.45.3）**：1000 次单行提交，WAL 模式下 `synchronous=OFF` ≈0.01s vs `synchronous=FULL`
  0.38s（**约 27 倍**）——"每次提交都 fsync"的成本直测，类比 PG `synchronous_commit=off` 与组提交的
  收益方向；⚠️ PG 语义（WAL 段/归档/复制约束）远复杂于 sqlite 档位。
- **X-D（sqlite3）**：5 万行+全表 UPDATE 后 `-wal` 文件 0.90MB，`PRAGMA wal_checkpoint(TRUNCATE)`
  即时完成、WAL 归 0B，主库文件 0.45MB——"检查点=WAL 回收"的最小演示；⚠️ 非 PG 的
  CheckpointLock/双进程语义。复现：`D:\develops\tmp\dbwave_w5_pgperfcb\exps.py / exps3_out.txt`。
- **对位启示**：sqlite 的 WAL 是"帧追加、检查点回写主文件"，PG 的 WAL 是" redo 日志、检查点只标前沿"
  ——X-D 演示的是前者，切勿混作 PG 恢复语义（详见内核分析册）。

## 3.7 适用性判断（2026）

观测三件套（log_checkpoints / pg_stat_bgwriter / pg_buffercache）**原样可用且仍是标准动作**；
参数默认值与"独立 WAL 卷"经验已大幅位移；PG18 异步 IO 让"检查点刷脏 vs 预读竞争"有了新变量。见文末。

## 高频坑与实操清单

- `max_wal_size` 过小 → checkpoints_req 暴涨，检查点从"定时"变"追债"；判读只看 req/timed 比例。
- 归档滞后（archive_command 失败重试）→ pg_wal 涨爆磁盘：检查点截不动未归档段（07 章联动告警）。
- `full_page_writes=off` 省 WAL 的诱惑：物理备份即刻不可靠，除非接受"备份策略整体重做"（07 章铁律）。
- wait_event 名字随版本增删（9.6 首版体系尤其不稳），巡检 SQL 要按大版本维护字典，勿硬编码多年。⚠️
- `shared_buffers` 不是越大越好：超过 OS 可缓存工作集后收益归零，先用 pg_buffercache 证明"装不下"。
- 检查点参数别单点调：completion_target/timeout/max_wal_size 是一个三角，动一角看两角（手册语境 ✅）。
- `commit_delay` 组提交在现代 SSD/高并发下多为负收益——保留此配方只为读懂旧书，不推荐照抄。⚠️
- WAL 独立卷配方在 NVMe 上多数场景失效，但**归档目标卷**仍值得与数据卷分离（爆炸半径隔离）。⚠️
- 冷启动恢复时间=未检查点 WAL 量/回放速率：`max_wal_size` 调大同时要把 RTO 预算改给运维知情。
- pg_buffercache 查询本身全表扫槽位，大 shared_buffers 下别在高峰跑（观测也有税，08 章同精神）。
- 章间联动：本章数字口径承接 01 章 fsync/IOPS 基线，判读输出喂给 04 章 sar/iostat 历史归档。

## 核心概念速览（中英对照）

- **预写日志** — WAL (Write-Ahead Logging)：修改落盘前先写日志的持久化协议。
- **检查点** — Checkpoint：把脏页刷盘并前移 redo 起点、允许截断旧 WAL 的动作。
- **检查点等待** — CheckpointLock/超时等待事件：会话受阻于检查点阶段的可见性证据。
- **背景写进程** — bgwriter：摊平脏页写入的辅助进程（与 checkpointer 分工）。
- **完成目标** — checkpoint_completion_target：检查点把刷脏平滑到一个时间窗内的比例旋钮。
- **最大预写日志尺寸** — max_wal_size：触发"超频检查点"的 WAL 量阈值。
- **全页写** — full_page_writes：防页撕裂的 WAL 加倍写，关闭需接受备份失效风险。
- **组提交** — commit_delay/commit_siblings：攒多事务一次 fsync 的老配方（SSD 时代基本弃用）。
- **缓冲缓存透视** — pg_buffercache：列出共享缓冲每个槽位归属对象的扩展视图。
- **检查点统计** — pg_stat_bgwriter：timed/req 计数与 buffers_checkpoint 写量视图。
- **写毛刺** — Checkpoint jitter：周期性检查点叠加盘瓶颈造成的 TPS 凹坑。

## 最新演进与工业实践

- **文档基线**：WAL 与检查点参数 ✅ https://www.postgresql.org/docs/current/runtime-config-wal.html；
  资源/IO 参数 ✅ https://www.postgresql.org/docs/current/runtime-config-resource.html（curl 200，2026-09-27）。
- **默认值迁移**：`checkpoint_completion_target` 默认 0.5→0.9（PG14，⚠️ 转述）、`wal_level=replica` 默认
  （PG9.6 起，本书基线恰好踩在该变更上 ✅ 版本事实）、`log_checkpoints` 默认转 on（PG15 线，⚠️）。
- **观测升级**：PG13+ 等待事件体系继续加密（IO 类 wait event 于 PG13 引入 ⚠️）；PG16 新增 `pg_stat_io`
  视图按 backend/进程类型统计读写，替代部分 pg_buffercache+自造统计的 2017 配方。⚠️ 转述+✅ monitoring-stats。
- **异步 IO 冲击（本章最大演进）**：PG18 `io_method=worker|io_uring` 重做预读/组合写，
  "检查点刷脏 vs 顺序预读"的 IO 调度竞争模型需要重估——当日"WAL 独立卷"经验的最终墓碑。
  ✅ https://www.postgresql.org/docs/release/18.0/（入口实查；细则 ⚠️ 转述）。
- **工业实践**：托管云（RDS/Aurora/Cloud SQL）把 WAL offload 到共享存储，检查点对用户半透明；
  自建高写入系统常见做法=大 `max_wal_size`+监控 checkpoints_req 比例+Prometheus
  postgres_exporter 告警。⚠️
