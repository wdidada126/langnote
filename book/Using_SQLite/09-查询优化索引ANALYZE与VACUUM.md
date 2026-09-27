# 09 · 查询优化、索引、ANALYZE 与 VACUUM ⚠️ 章号推定

> 主题锚定：优化器工作方式（启发式→统计式）、索引类型与覆盖索引、EXPLAIN /
> EXPLAIN QUERY PLAN、ANALYZE 与 sqlite_stat1、页缓存与 VACUUM 家族。
> 官方依据：[eqp.html](https://sqlite.org/eqp.html) ✅、[lang_analyze.html](https://sqlite.org/lang_analyze.html) ✅、
> [lang_vacuum.html](https://sqlite.org/lang_vacuum.html) ✅、
> [mmap.html](https://sqlite.org/mmap.html) ✅（curl 实测 2026-09-27；
> `queryplanelang.html` 404，正确页为 `eqp.html` ✅）。

## 1. 优化器：三十年"规则式"内核 + 可选统计

SQLite 没有代价模型默认值：无 `sqlite_stat1` 时按**启发式**（能用索引的 WHERE 项数、
可转换性、rowid 直达优先）选计划；`ANALYZE` 写入每索引"平均不同值数"后升级为统计式。
书中"SQLite 的优化器简陋"的叙述在 3.8 属实；2026 版本文档仍坚持"极简内核 + 手工可控"
哲学（eqp.html ✅），但启发式已加厚（🔧 实验 B：现代版**不跑 ANALYZE 也已选对**索引）。

三种基本访问路径（官方旧版"查询规划器"专页 `queryplanelang.html` 现 404 ⚠️，
现行口径并入 [eqp.html](https://sqlite.org/eqp.html) ✅ 与优化器相关页）：
- Rowid Lookup（`WHERE id=?`，最快，直达叶）；
- Index Lookup（二级索引→回表 rowid）；
- Full Scan（SCAN）。

🔧 本机 EQP 文案（3.45.3 实测）：`SCAN main` →
`SEARCH main USING INDEX ix_main_cat (cat=?)` →
`SEARCH main USING COVERING INDEX ix_cov (cat=?)` ——三态齐活，读 EQP 即读访问路径。

## 2. 🔧 实测 A：索引的量化价值与覆盖索引

方法：200,000 行表（cat 200 随机值 + val REAL + pad 40B），查询
`SELECT id,val FROM main WHERE cat='c7'`（命中 969 行），三种索引状态计时。

| 状态 | EQP | 耗时 |
| --- | --- | --- |
| 无索引 | `SCAN main` | 0.018–0.022 s |
| `ix_main_cat(cat)` | `SEARCH … USING INDEX (cat=?)` | 0.0034–0.0044 s（**~5×**） |
| `ix_cov(cat,val,id)` | `SEARCH … USING COVERING INDEX` | 同数量级，**零回表**（三列全在索引内） |

覆盖索引要点（书中概念，🔧 文案证实）：EQP 直接写 COVERING，查询根本不触主表页——
报表类"固定几列"查询的最优解；代价是索引体积与写放大。

## 3. 🔧 实测 B：ANALYZE 与 sqlite_stat1

方法：`orders(flag TEXT 二值, name TEXT 20 万唯一)`，两个单列索引；查询
`WHERE flag='f1' AND name='name199999'` 对比 ANALYZE 前后。

结果（🔧）：
- ANALYZE 前：计划已选 `ix_o_name`（现代启发式胜出；书中"两个候选必须 ANALYZE"
  的时代经验在 3.45 上**不再必然**）；
- `ANALYZE` 后 `sqlite_stat1`：`('orders','ix_o_name','200000 1')`、
  `('orders','ix_o_flag','200000 100000')`——"总行数 平均重复度"两数字语义亲验；
- 计划不变、耗时 0.0002→0.0001 s（本例统计与直觉一致，价值在**防翻车**：
  数据倾斜时统计是唯一防线；`PRAGMA optimize` 增量维护（3.18.0 ✅ changes.html）为现代做法。

## 4. VACUUM 家族：DELETE 不还空间，空间要"讨"

书中机制（lang_vacuum.html ✅ + fileformat.html ✅）：
`DELETE` 只把页挂进 **freelist**（文件内回收复用，**不缩文件**）；
`auto_vacuum` 三态（NONE/FULL/INCREMENTAL）与 `PRAGMA incremental_vacuum(N)`；
`VACUUM` 整库重建（tmp 里重排、原子替换——顺带整理碎片页序）。

🔧 实测 C（Python 3.45.3，auto_vacuum=INCREMENTAL 建库，3 万行 × 300 B）：

| 阶段 | page_count | freelist | 文件大小 |
| --- | --- | --- | --- |
| 灌满 | 2,319 | 0 | 9.50 MB |
| `DELETE WHERE id>15000` + commit | 2,319 | **1,157** | **9.50 MB（纹丝不动）** |
| `PRAGMA incremental_vacuum(500)` | 1,819 | 657 | 7.45 MB（**精确吐回 500 页**） |
| `VACUUM`（0.087 s） | 1,161 | 0 | 4.76 MB |

解读三条：
1. 删除一半数据文件零缩小——"表变小≠库变小"，运维预算看的是后者（DBRE
   [../Database_Reliability_Engineering/04-数据有界与生命周期.md](../Database_Reliability_Engineering/04-数据有界与生命周期.md)
   的删除账单实验用的正是这套 freelist 语义）；
2. `incremental_vacuum(N)` 逐批归还，适合"在线慢慢缩"（每页写日志、可中断）；
   VACUUM 一把梭需 ~2× 峰值磁盘、期间独占写锁（lang_vacuum ✅ 事务性条款）；
3. `VACUUM` 后 `auto_vacuum` 值**保留**（🔧 实测仍为 2=INCREMENTAL；它按当前模式重建）。

## 5. 页缓存、mmap 与"快查询"的手感清单

- `cache_size`：页缓存（🔧 05 章 8.6× 冷热实验）；负值=KB；
- `mmap_size`：把库文件内存映射，省 read() 系统调用（[mmap.html](https://sqlite.org/mmap.html) ✅；
  默认 0=关，本机 CPython `DEFAULT_MMAP_SIZE=0` 🔧；收益场景为大文件顺序扫，⚠️ 本会话未做 mmap A/B）；
- `count(*)` 优化（书中趣谈至今有效）：`SELECT count(*) FROM t` 在 SQLite 扫
  最小索引/表页——🔧 01 章实验里 200 次连接+count 合计 26.4 ms 侧面可见其廉价；
  想要真 O(1) 就用 `sqlite_sequence`/触发器计数（工程老话）。
- 表达式索引与 `PRAGMA function_list`（🔧 02 章 module/function 自省）配套使用。

## 6. 与湖仓/数仓视角的对位（任务指定互链）

SQLite 的 ANALYZE/VACUUM 在仓库世界对应 **统计收集 + compaction**：
[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)
里 Iceberg/Delta 的 `rewrite_data_files` 干的正是"freelist→文件级"的同类工作
（对象存储没有 in-place 页，小文件问题取代碎片页问题）；
[../数据仓库工具箱3.md](../数据仓库工具箱3.md) 的维度表索引策略在 SQLite 语境 = 
覆盖索引 + `WITHOUT ROWID`。单机引擎的维护三件套（ANALYZE/索引整理/空间归还）
在两本笔记中都能找到列存翻版——[#134 DuckDB UAR·09 云端与 DuckLake](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md) 的
维护函数面（21 个 `ducklake_*`，其实测 12）即"空间归还"的对位（波尾闭环 2026-09-27）。

## 7. 本章带走三条

1. 读 EQP 是 SQLite 调优的第一语言：SCAN/SEARCH/COVERING 三词即病情（🔧 实验 A 全部文案可复测）。
2. ANALYZE 的作用从"选对索引"演变为"防数据倾斜翻车"，配合 `PRAGMA optimize` 常态化。
3. 空间是"借"不是"还"：删除只进 freelist，缩文件必须明说（incremental_vacuum/VACUUM，
   🔧 9.50→4.76 MB 全程可复现）。

## 核心概念速览（中英对照）

- **EQP** — EXPLAIN QUERY PLAN：访问路径报告（SCAN/SEARCH/USING INDEX/COVERING）
- **启发式优化** — heuristic planner：无统计时按规则排序候选计划
- **sqlite_stat1** — 统计表：`表 索引 行数 平均重复数` 三元组
- **ANALYZE** — 统计采样语句：写 stat1（还有 stat1/stat2/stat3/stat4 四代 ✅ lang_analyze 页）
- **PRAGMA optimize** — 增量 ANALYZE（3.18.0，2017-03-30 ✅ changes.html 实证），连接关闭前调用
- **覆盖索引** — covering index：查询列全在索引键中，零回表
- **部分索引** — partial index：带 WHERE 的索引（3.8.0，2013-08-26 ✅ changes.html 实证，恰是本书基线版）
- **freelist** — 空闲页链：DELETE 后归还给库内复用的页清单
- **auto_vacuum** — 自动回收模式：NONE/FULL/INCREMENTAL 三态（🔧 pragma 值 0/1/2）
- **incremental_vacuum(N)** — 分批缩库：一次最多释放 N 页（🔧 精确 500）
- **VACUUM** — 整库重建：去碎片+缩文件+按当前 auto_vacuum 模式重写
- **mmap_size** — 内存映射窗口：以 page fault 换 read() 的读加速
- **WITHOUT ROWID** — 索引组织表：小行多索引场景的空间/缓存双省

## 最新演进与工业实践

- **stat4 与索引选择增强**：`sqlite_stat4` 最迟于 3.8.6（2014-08-15）已见于 changelog ✅
  （实测定位），FTS5 首见于 3.8.11（2015-07-27 ✅）；本会话 🔧 默认生成的是 stat1；
- **优化器常新年费**：2026 changelog 中 3.53.4 修复条目仍在处理"3.24.0 老 bug"与
  "AI 报告的问题"（✅ changes.html 直读）——**优化器至今仍是 SQLite 改动最勤的部分**，
  升级版本要带 EQP 回归基线（🔧 方法：把关键查询 EQP 文本存档 diff）；
- **RETURNING/UPSERT 的间接红利**（3.35/3.24 ✅）：减少"查了再写"的双计划成本；
- **工业实践**：移动端用 `PRAGMA incremental_vacuum` 做后台瘦身、桌面端用
  `VACUUM INTO '快照文件'` 做分发（3.27.0 ✅）；与 DuckDB 对位差异（无统计代价模型 vs 
  有自适应执行）已在 [#134 DuckDB UAR·01 画像实测](../DuckDB_Up_and_Running/01-DuckDB入门.md) 展开（波尾闭环）；
  可先读 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md) 
  的列存视角。
- **取证清单（本章）**：eqp.html ✅、lang_analyze.html ✅、lang_vacuum.html ✅、
  mmap.html ✅、fileformat.html ✅、changes.html ✅、queryplanelang.html ❌404（弃用，
  以 eqp.html 为准）；🔧 实验 A/B/C 数据源 `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt`
  与 EXP9c/独立 iv 复测（本会话记录）。⚠️ `PRAGMA optimize` 版本（3.18）、mmap 收益幅度：
  前者为官方页叙事口径未逐字核，后者本会话未做 A/B。
