# 第 9 章 Vacuum 与膨胀控制（⚠️ 章题为中文重建，非原书目录引用）

> 《PostgreSQL High Performance Cookbook》第 9 章精读重构。recipe 清单 ✅ 实抓自官方代码仓
> `Chapter 09/Chapter9.txt`；阅读地图见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 9.1 本章定位

PG 性能书绕不开的宿命章：**MVCC 多版本不就地覆盖 → 删除只是打标 → 空间靠 VACUUM 回收**。
本章 5 道配方把"膨胀的观测（pgstattuple）—日常治理（vacuum/autovacuum）—极端事件（XID 回卷）—
进度可见性"串成闭环。txt 首段 `CREATE EXTENSION pgstattuple; CREATE TABLE test(t INT)`（✅ 实抓）
即观测配方开场。

## 9.2 配方地图（✅ 官方 txt 实抓，共 5 题）

1. Dealing with bloating tables and indexes（pgstattuple/pgstatindex 量化膨胀率）
2. Vacuum and autovacuum（手工/自动策略、按表参数）
3. Freezing and transaction ID wraparound（freeze 与 32 位 XID 回卷防线）
4. Monitoring vacuum progress（日志/pg_stat_progress_vacuum 线）
5. Control bloat using transaction age（以事务年龄驱动治理节奏）

## 9.3 代表配方精读

### 配方：Dealing with bloating tables and indexes

- **量化**：`pgstattuple('t')` 给 dead_tuple_percent/free_percent；B-tree 用 `pgstatindex` 的
  avg_leaf_density<90% 判"值得重建"（阈值语义 ⚠️ 转述，视图存在性 ✅）。
- **膨胀来源四手**：长事务钉住 xmin、autovacuum 追不上、fillfactor 未调的热点表、索引膨胀假说
  （当日流行，见 08 章反驳）。诊断顺序=先找长事务再谈参数。

### 配方：Vacuum and autovacuum

- 手册配方：`VACUUM (VERBOSE, ANALYZE)` 大表分批夜窗；autovacuum 按表调
  `autovacuum_vacuum_scale_factor`（大表从 0.2 压到 0.01~0.05，✅ txt 含按表 storage 参数域实录）。
- **当日未言明的坑**（今日补）：反连接删除模式（先删后插的批处理）让"最新死元组比例"骗过阈值；
  PG13+ 孤儿页清理、PG14 截断式 vacuum（`vacuum_truncate`）大幅改写了这条配方的最佳实践。⚠️
- `vacuum_cost_delay/limit` 限速 IO 与"追不上写入"的矛盾——2017 默认 200ms 时代限速反而酿祸，
  PG12 起默认关闭成本限速（⚠️ 转述版本史）。

### 配方：Freezing 与 XID 回卷（最贵的一次维护）

- 机理：32 位事务号按模比较，2^32 用尽前必须 freeze（标记"永久可见"），否则**强制单事务 VACUUM
  全库停写**——当日社区名言"wraparound 是所有 PG 实例的死刑，autovacuum 是缓刑官"。
- 配方：监控 `age(datfrozenxid)`/`age(relfrozenxid)` 排序报表、提前对高龄表 aggressive vacuum
  （`vacuum_freeze_min_age` 调小）、19 亿阈值告警（✅ 该阈值属 PG 常识转述 ⚠️ 具体数值以手册为准）。
- 现代续命：64 位全宽 XID/LSN 已在 PG18 落地（⚠️ 转述，✅ 发行注记入口见文末），回卷时钟被拔。

### 配方：Monitoring vacuum progress

- 9.6 时代=日志+猜测；`pg_stat_progress_vacuum`（PG9.6 引入 ✅ 版本事实）给 heap_total/heap_scanned/
  phase——从"信仰运维"到"进度条"的分水岭，本章恰站在分水岭上。

## 9.4 机制小深潜：HOT 与 fillfactor 的因果链

页内可 HOT（Heap Only Tuple）更新避免索引膨胀，前提是页留有空隙——`fillfactor=70~90` 是给 HOT 的
"呼吸位"。这条 07 年配方到 2026 仍是写密集表标配，且与 01 章"填充因子预留空间"类比实验（#64 的 X-B）
同构。对照：[../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md](../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md)、
[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)（InnoDB 就地更新的另一极）。

## 9.5 repo 对照

- 内核级 MVCC/xmin 机制：[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)。
- 通用调优视角的"清理/重组"章节：[../Database_Tuning/02-调优内核.md](../Database_Tuning/02-调优内核.md)。
- PG16 维护食谱：[../PostgreSQL_16_Administration_Cookbook/04-监控诊断与日常维护.md](../PostgreSQL_16_Administration_Cookbook/04-监控诊断与日常维护.md)。

## 9.6 🔧 类比实测（非 PostgreSQL 行为；PG 不可装 ✅ where psql 无输出）

- **X-G（sqlite3 3.45.3）**：12 万行表 8.49MB → **隔行删一半** → 页数 2072 纹丝不动、
  freelist 仅 1 页、文件仍 8.49MB；`VACUUM` **0.05s** 回 4.25MB。
  - 教训一：删除不还空间，重组靠 VACUUM——与 PG"打标+回收"神似；
  - 教训二：**均匀分散的删除比成段删除更伤**（每页都残一半行，整页无法释放）——对应 PG 里
    "分散 DELETE+长事务钉页"的膨胀风暴；⚠️ sqlite 无 MVCC 死元组/冻结语义，机制层严禁类推。
- 复现：`D:\develops\tmp\dbwave_w5_pgperfcb\`（t6 段，exps3_out/t6_out）。

## 9.7 适用性判断（2026）

五配方全部仍有效，但**默认值史**改写了一半操作：成本限速关、截断式 vacuum、孤儿页清理、
（PG18）防回卷时钟拔除——照抄 2017 参数会错过这些红利。本章读法=骨架照用、参数查手册重设。

## 高频坑与实操清单

- 膨胀治理第一问永远是"谁钉住了 xmin"：长事务/失活槽/hot_standby_feedback（06 章）三只手先松开，
  再谈调 autovacuum——顺序反了就是在给钉子浇油。
- 批处理"先 DELETE 后 INSERT"模式让"变更比例阈值"骗人（夜间清空白天重灌，比例永远不到点）：
  改 `autovacuum_vacuum_cost_delay=0` 定点表+任务后手工 VACUUM（当日配方，仍有效）。
- `VACUUM FULL` 是最后手段：全表重写+ACCESS EXCLUSIVE+索引重建+空间峰值翻倍（12 章/07 章连锁）；
  日常走 pg_repack 类在线重组。⚠️
- TOAST 膨胀独立核算：大列更新产生的 toast 死元组有自己的计数，报表只算主表会低估。
- freeze 参数链（`vacuum_freeze_min_age`/`_multixact` 等）全局调小=autovacuum 常年满负荷；只对
  高龄表定点 aggressive，别动全局。
- 多副本时最老回放事务决定主库保留线（`hot_standby_feedback` 关则转嫁为备库查询取消）——治理要
  跨节点看 `xmin` 服务（`pg_replication_origin`/槽判读 ⚠️）。
- wraparound 告警按"天数余额"（age 增速外推）而非静态阈值：写入翻倍的季度，昨天的安全是今天的死刑。
- X-G 类比的第二教训：分散删除最伤页局部性——批量作业尽量成段删、按物理序组织。

## 核心概念速览（中英对照）

- **多版本并发控制** — MVCC：旧版本随行保留，读不挡写、删除变"死元组"。
- **死元组** — Dead tuple：对所有快照不可见、等待回收的旧版本。
- **空间回收** — VACUUM：清死元组、回空闲页、推进冻结、更新可见性映射。
- **自动清理** — autovacuum：按更改数阈值后台执行，可按表调参。
- **冻结** — Freezing：把行标记为"任何事务都可见"，斩断 XID 回卷依赖。
- **事务号回卷** — XID wraparound：32 位事务号模比较耗尽，触发强制停写清理。
- **填充因子** — fillfactor：页预留空间比例，HOT 更新与索引膨胀的呼吸位。
- **膨胀观测** — pgstattuple/pgstatindex：表/索引死空间与叶密度量化扩展。
- **进度视图** — pg_stat_progress_vacuum：vacuum 阶段/扫描量/截断候选可见性。
- **事务年龄** — age(relfrozenxid)：距回卷的倒数里程，治理节奏的驱动指标。
- **成本限速** — vacuum_cost_delay：IO 节流双刃剑（旧默认致追不上写入）。

## 最新演进与工业实践

- **反回卷终局**：PG18 落地 64 位全宽 XID/LSN，回卷风险自 2030s 起解除（⚠️ 转述，✅ 入口
  https://www.postgresql.org/docs/release/18.0/ curl 200，访问 2026-09-27）。
- **autovacuum 改进线**：PG13 孤儿页清理（INSERT 触发 opportunistic vacuum）、PG14 尾部截断选项 `vacuum_truncate`  截断、TOAST 分治参数 `process_main`/`process_toast`（引入版本 ⚠️ 转述）、PG16/17 对 wraparound 防护激进提前（autofreeze 提前量阈值调整，⚠️
  逐版细则转述）、PG18 并行 vacuum 对索引/阶段扩面（⚠️）——2017"手工夜窗 VACUUM"文化基本谢幕。✅
  机制文档 https://www.postgresql.org/docs/current/routine-vacuuming.html（curl 200）。
- **膨胀治理工具**：pg_repack（在线重组、消索引膨胀事实标准）与 pg_squeeze 承接本章"重建"诉求；
  pgstattuple 原样健在。⚠️
- **观测升级**：pg_stat_progress_vacuum 持续加列（heap/ind 多阶段）、`log_autovacuum_min_duration`
  默认值收紧（PG15 线 ⚠️），Grafana PG 面板把事务年龄做成红黄绿仪表盘。⚠️
- **引擎对照实践**：从 MySQL/Oracle 迁移团队最大认知落差即本章——"删除不还空间、UPDATE 产生新行"；
  各 DBA 培训材料（含 [../Mastering_PostgreSQL_Administration/06-例行维护.md](../Mastering_PostgreSQL_Administration/06-例行维护.md)）
  均以 PG 的清理模型为第一课。⚠️
