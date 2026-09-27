# 07 MVCC、Vacuum 与表膨胀

> 章题 ⚠️ 推定（书系 1e/2e 均有 Vacuum/Bloat 专章；本册主题域 ✅ 实证：官方代码仓 `Chapter07`
> 以 `SELECT *,xmin,xmax FROM t` + `txid_current()` 演示 MVCC 可见性位，`7_5.sql` 直接
> INSERT `pg_autovacuum` 系统目录做**按表 autovacuum 禁控**（vac_base_thresh/vac_scale_factor/
> vac_cost_delay/freeze_min_age 全量字段）；`Chapter09` 夹另有 25 个脚本与膨胀观测呼应）。
> 本章是全册技术含量最高、2026 年仍最有生命力的一章。非原书文本。

## 一、xmin/xmax：一行数据的生死簿（7_1.sql ✅ 现场）

```
 s | i |  xmin  | xmax
---+---+--------+-----
 1 | 0 | 158208 |   0
```
- `xmin` = 插入者事务号，`xmax` = 删除/更新者事务号（0=活着）。UPDATE = 插新行版本 + 旧行打 xmax，
  **这就是"死元组（dead tuple）"的全部起源**；
- `txid_current()` 在书中演示取当前事务 id 以对照可见性——快照可见性判定即
  "xmin 已提交且 xmax 未提交（或 xmax≥我的快照）"⚠️ 转述社区标准模型；
- 工程后果：任何 UPDATE 风暴都会转化为（a）表膨胀、（b）索引同样膨胀（索引项也带 tid 版本）、
  （c）vacuum 负载，三位一体，缺一不可地要一起监控（11 章视图族）。

🔧 类比实验 X-C（sqlite3 3.45.3，**非 PG**）：10 万行 21.6MB → DELETE 60% → 文件仍 21.6MB
（空闲页未归还操作系统；本轮实测 `PRAGMA freelist_count` 读数为 0，与 SQLite 内部延迟整理有关 ⚠️ 观察如实记录）
→ `VACUUM` 0.10s 后 8.7MB。**共同定律：删除只是标记，物理收缩需要重组动作**。
**PG 差异声明**：PG 的死元组是 MVCC 多版本产物、由 autovacuum 按阈值收割、且 HOT 更新可把新版本
留在页内不碰索引（SQLite 无对应物）；VACUUM 一词两边同名但语义不同源。exps.py 段 C。

## 二、VACUUM 的三重职责（sql-vacuum 语义，⚠️ 转述官方文档）

1. **回收死元组空间**为可重用（不缩文件；`VACUUM FULL` 才重写缩身，代价是全表锁 ⚠️）；
2. **冻结（freeze）**：32 位事务号回卷前的强制老化（autovacuum 的 naptime 风暴常源于此）；
3. **更新可见性映射与统计**：为规划器与维护窗口服务。
   权威锚点：✅ https://www.postgresql.org/docs/10/sql-vacuum.html 与
   现行版 ✅ https://www.postgresql.org/docs/16/sql-vacuum.html （curl 200）。

## 三、autovacuum 按表治理（7_5.sql ✅ 原文机制）

书仓 7_5.sql 用 INSERT INTO pg_autovacuum 直接写系统目录为 `mytable` 设
`enabled=false` 与阈值 -1（回退全局）——这是 **PG10 时代的手法**：当时 autovacuum 参数
（autovacuum_vacuum_scale_factor=0.2 / vacuum_base_threshold=50 / cost_delay 族）
的按表覆盖要碰目录表，社区更通行的正法是 `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor=...)` ⚠️。
**PG13+ 已提供 `autovacuum_enabled` 等 reloption 与后方的 Vacuum 费用模型改造（PG13 的
vacuum cost 重设计、PG15-17 的 autovacuum 环形队列与 anti-wraparound 跳变治理 ⚠️ 转述版本史）**。
判读口诀 ⚠️ 教材性：
- 大表（>千万行）scale_factor 0.2 太迟钝 → 用绝对阈值（PG13 起有 insert-driven 阈值思想 ⚠️）；
- 热小表要更激进；写风暴表允许适度膨胀换顺序 IO，但冻结窗口必须预留。

## 四、膨胀（bloat）的度量工具箱

- 观测面：`pg_stat_user_tables.n_dead_tup / n_mod_since_analyze`（7_5.sql 系统目录手法的现代观测入口，
  阈值覆盖已改走 reloptions，见上节版本注记）；
- 解剖面：pgstattuple（精确但重）/ pgstattuple_approx（快但估）⚠️ 扩展名转述；书仓 Chapter09 夹
  的 25 脚本族即此类巡检的雏形（✅ 存在性实证）；
- 索引膨胀与表膨胀分开记：BRIN（PG9.5 起）对追加型大表近乎免疫 ⚠️，B-tree 则是重灾区；
- 2018 年书语境 vs 现在：PG13/14 的 VACUUM 速度数量级改进 + PG17 的 buffer 优化 ⚠️ 转述，
  使"膨胀失控"在新版本显著缓和——但 MVCC 根因不变，本章模型仍是必读。

## 五、与 HOT 的关系（⚠️ 转述社区文档）

HOT（heap-only tuple）更新：被更新列无索引引用且页内有空间时，新版本不进索引——
膨胀与索引维护双降。**填充因子的用途即在此**：`fillfactor=90` 给每页预留 HOT 槽位。
🔧 类比 X-B（sqlite3，非 PG）：同量 10 万行，顺序主键插入 219 页 vs 随机主键插入 266 页（+21%）——
演示"原地插入需要页内预留空间，否则结构分裂放大占用"；PG 的 fillfactor 是**主动预支**该空间
换 HOT 率，SQLite 无 fillfactor 参数（B 树页分裂被动承受），只可类比空间语义不可类比机制。exps.py 段 B。
MySQL InnoDB 的页内更新对照见 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)
所在书系的 07/11 分册主题 ⚠️。

## 细案：膨胀事故的第一响应剧本（⚠️ 教材性，字段名 ✅ 实抓自书仓 7_1/7_5.sql）

```sql
-- T0 定位：谁在膨胀、多快
SELECT relname, n_dead_tup, n_mod_since_analyze, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;
-- T1 查钉住水位的长事务（膨胀加速器，12 章备份/14 章槽同根）
SELECT pid, xact_start, now()-xact_start AS age, state, query
FROM pg_stat_activity WHERE xact_start IS NOT NULL ORDER BY age DESC LIMIT 5;
-- T2 查 autovacuum 是否在跑/被限流
SELECT pid, backend_start, query FROM pg_stat_activity WHERE query ILIKE 'autovacuum%';
-- T3 决策：手工 VACUUM（不 FULL）补刀热表；冻结逼近则提高该表 autovacuum 激进度的 reloptions
VACUUM (VERBOSE, ANALYZE) mytable;
```

剧本要点：
- **顺序即诊断**：T1 永远先于任何加参数动作——一个 8 小时长事务能让全库阈值调优全部白做；
- VACUUM FULL 只在"确认要缩文件且能接受锁表窗口"时进入变更流程，非常规手段（07 章三重职责的边界）；
- 处置后 24h 内回看 n_dead_tup 曲线是否转头，否则升级到 11 章检查点/脏速率联查。

## 章内自测（四问四答）

- **问：UPDATE 一列会复制整行吗？**
  答：会——新版本整行入堆，这就是窄化高频列与 HOT 设计（本章第五节）的意义。
- **问：为什么索引也要 vacuum？**
  答：索引项同样携带版本 tid，死元组在索引里先表现为膨胀再表现为扫描变慢（09 章效益视图联动）。
- **问：fillfactor 调低的净收益怎么量？**
  答：HOT 率上升（idx 维护省）vs 表页数上升（扫描/缓存多付），用 pg_stat_user_tables 两栏做 A/B（🔧 X-B 仅类比空间语义）。
- **问：autovacuum 全开为什么还会 wraparound 事故？**
  答：费用限流+阈值迟钝叠加超大表，冻结线追不上回卷线——阈值绝对化配置（本章第三节）即防此。

## 核心概念速览（中英对照）

- **死元组** — Dead Tuple：xmax 已提交、对任何快照不可见的行版本，待 vacuum 回收。
- **行版本** — Tuple Version：MVCC 下 UPDATE 产生的新版本链。
- **xmin/xmax** — 事务号位：每行版本的出生/死亡事务 id（7_1.sql 实证）。
- **可见性映射** — VM：记录页是否全可见的位图，VACUUM 副产品、HOT 判据。
- **HOT 更新** — Heap-Only Tuple：免索引维护的页内链式更新。
- **填充因子** — fillfactor：每页预留自由空间比例，HOT 率的预算旋钮。
- **冻结** — Freeze/XID Wraparound：事务号回卷防护，autovacuum 的硬 deadline。
- **autovacuum 阈值** — Vacuum Thresholds：scale_factor+base_threshold 决定的启动线（7_5.sql）。
- **VACUUM 费用延迟** — Cost-based Throttling：vacuum_cost_delay/limit 的削峰机制。
- **表膨胀** — Table Bloat：高水位不降导致的存储与扫描放大。
- **pgstattuple** — 膨胀精测扩展：逐块统计活/死元组占比 ⚠️ 转述。
- **VACUUM FULL** — 重写式收缩：缩文件但持 AccessExclusiveLock 的核弹选项。

## 最新演进与工业实践

- **版本演进主线**：PG13 重写 VACUUM（TID 存储结构、费用模型）⚠️ 转述，PG14 引入
  `VACUUM/MERGE` 选项族，PG15+ 持续推进 autovacuum 对 insert-heavy 表与 wraparound 的
  自适应；2026 现行文档 ✅ https://www.postgresql.org/docs/17/runtime-config-autovacuum.html （curl 200）。
- **膨胀监控产品化**：pgmonitor/pgx_scripts 等社区脚本库内置 bloat 估算查询 ✅ 仓库存在性经
  api.github.com 校验（github.com/okbob/pspg、github.com/postgrespro/pg_wait_sampling 同法 ✅）；
  书仓 Chapter09 手join 的 25 脚本在 2026 基本可被现成扩展替代 ⚠️。
- **仍是面试必考**：HOT/fillfactor/wraparound 三件套因 PG10 时代事故高频而沉淀为通用知识；
  与 [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md) 的空闲空间管理章对读最佳（✅ 盘上互链）。
- **工业教训存档**：2019–2024 多起公开事故（大表 autovacuum 停摆→磁盘暴涨→冻结风暴）复述的
  正是本章三职责的失控顺序 ⚠️ 转述社区事后报告文体，未取单一 URL 故不注链接。
