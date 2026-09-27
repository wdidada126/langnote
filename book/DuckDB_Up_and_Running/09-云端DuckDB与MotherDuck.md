# 09 · Using DuckDB in the Cloud with MotherDuck（云端 DuckDB：MotherDuck）

> 覆盖原书第 9 章。目录来源：✅ 官方示例文件 `Chapter_9.ipynb` 标题实抓。MotherDuck = "DuckDB 语法 + 云执行 + 共享目录"；本章之外，本文件收纳全目录的 **ATTACH 跨源与 DuckLake 实测**（任务密度对标组在此收口）。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Getting Started with MotherDuck**：注册/token、`ATTACH 'md:'` 进云目录；**Adding Tables / Creating Schemas / Sharing Databases / Creating a Database / Detaching a Database** 五段云目录 CRUD（✅ 小节题实抓）；**Using the Databases in MotherDuck**（含 Querying Your Database）。
- **Writing SQL using AI**：MotherDuck 内置 text-to-SQL（`prompt()` 类函数）——两本书里唯一的"SQL+LLM"正式小节。
- **Using MotherDuck Through the DuckDB CLI**：**Connecting to MotherDuck / Creating Databases on MotherDuck / Performing Hybrid Queries**：CLI 侧同名入口；"hybrid"=本地引擎与云引擎按表位置自动路由。

## 核心技术清单

- ATTACH 宇宙（本章主纲）：`ATTACH 'md:' AS md`（云）、`ATTACH 'x.db' (TYPE ducklake)`（湖）、`ATTACH 'f.db' (TYPE sqlite)`、`ATTACH 'host=… (TYPE mysql|postgres)`——一套语法统一四类目录。
- 混合查询：本地临时表与云端表同 SQL JOIN，优化器决定搬运方向；`ATTACH` 后 `USE md.db` 切默认上下文。
- 云侧对象：database/schema/table 三层 + Share 原语（provider/consumer）；`read_parquet('s3://md.io/…')` 直读云导入结果。
- AI：`prompt()`/`md.queries` 系（转述 ⚠️ 未实证）。
- 本地对照实验面（本目录新增）：sqlite ATTACH 读写、DuckLake 快照与时间旅行、iceberg 扩展可用性盘点。

## 🔧 实测一：ATTACH 跨源（1.5.5；580 万行本书数据）

1. **写出去**：`ATTACH 'flights2.db' AS fl (TYPE sqlite)` + `CREATE TABLE fl.main.flights AS SELECT …5列…` → **3.16 s / 140 MB**（列存查询引擎直灌行存库，行式写路径不吃亏太多）。
2. **读回来**：`ATTACH … (TYPE sqlite, READ_ONLY)` + `SELECT count(*)` → **0.09 s**（5,819,079 行——下推进 SQLite 侧 count）。
3. **跨源 JOIN**：attached SQLite 表 × 本地 `flights2015.parquet`（`USING(o)`，WN/DL 分组计数）→ 结果与纯 parquet 对照**逐值相同**（DL 875,881 / WN 1,261,855），耗时 **0.19 s vs 对照 0.09 s**——行存桥约 0.1 s 的税在 580 万行量级完全可忽略。
4. **DETACH** ✅ 干净脱钩；重名 ATTACH 需先 DETACH（陷阱见下）。

## 🔧 实测二：DuckLake（core 扩展，版本 d8a1881e ✅）

5. `ATTACH 'ducklake:mylake.db' AS lake (DATA_PATH 'lake_files')` + **CTAS 5,819,079 行 → 0.20 s**；`SELECT count(*) FROM lake.f` **0.02 s**；`ducklake_snapshots('lake')` 列出快照 (0, t0)/(1, t1)。
6. **时间旅行** ✅：`DELETE FROM lake.f WHERE AIRLINE='F9'`（0.07 s，count 5,819,079→5,728,243）后，`SELECT count(*) FROM lake.f AT (VERSION => <旧快照>)` 回看旧值——语法实测定型：**`AT (VERSION => n)`**；`AT VERSION n`、`VERSION AS OF t`、`AT SNAPSHOT` 一律 Parser Error。
7. **内联数据行为** ✅：CTAS/DELETE 后 `DATA_PATH` 目录**无 parquet 落盘**（1M 行表实测 fresh.db 元数据 3.9 MB、数据目录 0 文件）——数据先内联在元数据库，**flush/rewrite 时机**决定湖文件形态；本机构建上 `ducklake_flush_inlined_data('lake.main.f')` 及三参变体均绑定失败（⚠️ 待官方签名核对，勿照抄博客）。
8. **JSON 出口**：`COPY (SELECT AIRLINE, avg(delay) … FROM lake.f GROUP BY 1) TO 'out.json' (FORMAT JSON, ARRAY true)` ✅（14 行）。
9. DuckLake 1.0 官宣与核心扩展地位：沿用姊妹目录已核验链条（✅ 其 00：ducklake.select 根 200 + 仓库 2025-03-03 建仓）→ [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)。

## 🔧 实测三：MotherDuck 与 iceberg 扩展（可用性面）

10. `motherduck` 扩展 **install+load ✅**（版本串 `v1.5.5-2026-09-355`，带构建时间戳）；`ATTACH 'md:'` 需 token/浏览器授权——**本机无账号，云侧行为全部 ⚠️ 文档转述**（不做伪实测；官方站 https://motherduck.com/ ✅ 200 存在性核验）。
11. `iceberg` 扩展 install+load ✅（版本 45163a28；任务口径"icebed"为讹写，实抓名=**iceberg**）；本机无机读公共 Iceberg 仓库凭据，`ATTACH (TYPE ICEBERG)` 查询路径 ⚠️ 未实证——规范面深读转 Iceberg 专书（互链见下）。
12. **DuckLake 函数目录实数** 🔧：`duckdb_functions()` 中 `ducklake%` 共 **21 个**——flush/merge_adjacent/rewrite/expire/cleanup_old_files/delete_orphaned/list_files/table_info/snapshots/table_{insertions,deletions,changes}/commit 族全在册（✅ 名单实抓，见"维护函数面"节）——"在册 ≠ 博客签名"：本机 build 上 flush 系绑定失败（实测 7），调用前先核签名。

## 易错点与陷阱

- **ATTACH 同名冲突**：同库文件二次 ATTACH 报 duplicate catalog——先 `DETACH`；`md:` 与本地 `.db` 重名 schema 时用全限定 `md.main.t`。
- **混合查询的搬运方向**：把云大表 JOIN 本地小表当"必然下推"是误解——观察 `EXPLAIN` 与流量；大数据集先物化到 md 侧再混合。
- **DuckLake"提交即落文件"错觉**：实测 CTAS 后数据内联元数据库（第 7 条）——拿"湖文件"去给 Spark 读前先 flush/rewrite；元数据库（这里 `mylake.db`）才是当前真相主体。
- **时间旅行语法**：只认 `AT (VERSION => n)`（第 6 条实测四连败后的正解）；快照过期策略（`ducklake_expire_snapshots`）在函数列表里 ✅ 但语义未测 ⚠️。
- **sqlite 桥的写事务**：READ_ONLY 之外可回写，但 SQLite 单写者锁与 DuckDB 事务不共享隔离级——跨源写要当分布式事务对待（教训同 DIA 并发叙事）。
- **MotherDuck 免费层认知**：token 管理/网络域外——本章 CLI 三小节的行为（交互式授权、`md:` 默认 ATTACH）以官方文档为准 ⚠️。
- **"内联=没保存"错觉**：实测 7 的"DATA_PATH 空目录"里数据其实已提交进元数据库——本目录快照可查、外部引擎不可见（Spark 读不到文件）；"提交成功"与"湖可读"之间隔着 flush。
- **扩展版本串不是 semver**：motherduck/ducklake 用构建戳/commit 号（`v1.5.5-2026-09-355`/`d8a1881e`，✅ 实抓）——按"≥1.x"写依赖约束对扩展无效；锁平台版本 + 快照扩展清单才是复现的正解。

## ATTACH 目录矩阵速查（本目录实测状态汇总）

| TYPE | 连接样例 | 本机状态 | 关键实测 |
| --- | --- | --- | --- |
| （默认 duckdb） | `connect('x.db')` | ✅ 全通 | 01 章全链 |
| sqlite | `ATTACH 'f.db' (TYPE sqlite, READ_ONLY)` | ✅ 读写全通 | count 0.09 s / 写 3.16 s / 跨源 join 0.19 s（实测一） |
| ducklake | `ATTACH 'm.db' (TYPE ducklake, DATA_PATH …)` | ✅ 核心面通、flush 签名卡 | CTAS 0.20 s / `AT (VERSION=>n)` ✅（实测二） |
| mysql | `ATTACH (TYPE mysql)` | ⚠️ 装成未连（无服务器） | install 13.3 s（02 章） |
| postgres | 同族 scanner | ⚠️ 装成未连 | install 7.8 s（02 章） |
| md:（MotherDuck） | `ATTACH 'md:'` | ⚠️ load ✅、云侧无账号 | 版本串 v1.5.5-2026-09-355（实测三） |
| iceberg | `ATTACH (TYPE ICEBERG …)` | ⚠️ 装成未连 | 版本 45163a28（实测三） |

- 一格一证据：本表把 02/09 两章的"可装 / 可连 / 可查"三态分开记账——扩展世界的诚实基准是"install 成功离能用平均还差一步凭据"。

## DuckLake 维护函数面（21 个在册名单实抓，四分层记忆）

- **落盘系**：`ducklake_flush_inlined_data` / `ducklake_merge_adjacent_files` / `ducklake_rewrite_data_files`——把内联数据变成"真湖文件"（实测 7 卡的是签名，不是缺函数）。
- **清理系**：`ducklake_cleanup_old_files` / `ducklake_delete_orphaned_files` / `ducklake_expire_snapshots`——时间旅行有成本：旧快照不领情地养着旧文件。
- **情报系**：`ducklake_snapshots` / `ducklake_table_info` / `ducklake_list_files` / `ducklake_table_insertions` / `ducklake_table_deletions` / `ducklake_table_changes` / `ducklake_current_snapshot`——排障先跑情报系，再动清理系。
- **事务/配置系**：`ducklake_commit` / `ducklake_last_committed_snapshot` / `ducklake_set_commit_message` / `ducklake_set_option` / `ducklake_options` / `ducklake_settings` / `ducklake_scan` / `ducklake_add_data_files`。
- 红线用法：先 `SELECT function_name, parameter_types FROM duckdb_functions() WHERE function_name='ducklake_…'` 核签名再抄示例（实测 12 的全部教训）。

## 混合查询排障清单（ATTACH 宇宙通用；本章实测提炼）

1. **对象解析三查**：`SHOW DATABASES` → `current_database()` → 全限定名（`md.main.t`/`fl.main.flights`）——"表存在却查不到"九成是默认上下文没切。
2. **下推别想当然**：远端谓词是否下推，看 `EXPLAIN` 里远端 SQL 形状；sqlite count 0.09 s 是下推正样本（实测一 2）。
3. **覆盖率审计**：跨源 JOIN 前先两侧 count + `USING SAMPLE` 估命中——05 章 93.1% 教训在多源场景更贵。
4. **写路径分型**：READ_ONLY 挂载=零风险侦查；写=单写者锁+异源无共同事务（陷阱 5）——先物化回 DuckDB 侧再谈联合作业。
5. **DETACH 收尾**：演练脚本同名二次 ATTACH 必炸（陷阱 1）——脚本开头统一 TRY-DETACH 或换别名。

## 与其他章/书的互链

- 远程 IO 前提（httpfs/s3）→ [08-用DuckDB访问远程数据.md](08-用DuckDB访问远程数据.md)；管道化上云对照（dlt/dbt/Dagster）→ [../DuckDB_in_Action/08-构建数据管道.md](../DuckDB_in_Action/08-构建数据管道.md)
- MotherDuck 的系统章（令牌连接/S3/共享细节）→ [../DuckDB_in_Action/07-云端DuckDB与MotherDuck.md](../DuckDB_in_Action/07-云端DuckDB与MotherDuck.md)——两书该主题互为参照：UAR 重 CLI/AI，DIA 重架构
- DuckLake 生态位（表格式三角）→ [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)、[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)、[../Apache_Iceberg活用入門/07-Catalog生态.md](../Apache_Iceberg活用入門/07-Catalog生态.md)
- 跨源写路径的客户端口径 → [../DuckDB_in_Action/12-附录A-客户端API.md](../DuckDB_in_Action/12-附录A-客户端API.md)
- SQLite 行存库的独立深读（CLI/应用开发两种视角）→ [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（#87 已落盘，与实测一互读）

## 思考题（合上笔记再答）

1. 一套 ATTACH 语法本章统了几类目录？各给一个实测数。（云 md:（转述）/湖 ducklake（0.20s CTAS）/行存 sqlite（0.09s count）/MySQL-PG（装成未连））
2. DuckLake CTAS 之后为什么 DATA_PATH 是空的？对"湖即文件"心智意味着什么？（内联元数据库；flush 前真相在目录 DB）
3. 时间旅行正解语法是什么？另外三种写法错在哪层（Parser/Catalog）？（AT (VERSION => n)；实测 Parser×3、表不存在于快照@v0=Catalog）
4. DuckLake 函数面共几个、四分层各记一个代表？（21 个，实测 12；落盘 flush / 清理 expire / 情报 snapshots / 事务 commit）

## 2026 视角补注

- "DuckDB 是引擎、目录可插"的格局在 2026 已成型：MotherDuck（商业云）、DuckLake（自管湖格式，core 化 ✅）、iceberg 扩展（外湖桥）三形态同场；本目录第 5–11 条给出一机可复现的横向对照。
- AI 小节（prompt 写 SQL）预示了 2025–2026 text-to-SQL 工具链的日常化；本地替代（DuckDB+LLM 直连）不在两书范围 ⚠️。

## 核心概念速览（中英对照）

- **ATTACH** — 把外部目录（云/湖/库）挂进当前 DuckDB 会话的统一动词。
- **混合查询** — Hybrid query：本地与云表同 SQL 路由执行。
- **共享（Share）** — MotherDuck provider/consumer 数据共享原语。
- **DuckLake** — 元数据库+Parquet 的开放湖仓格式（DuckDB 原生）。
- **快照/时间旅行** — Snapshot / `AT (VERSION => n)`。
- **内联数据** — Inline data：未落湖文件前的元数据库暂存形态（实测）。
- **flush/rewrite 函数族** — ducklake_flush_inlined_data / merge_adjacent_files 等维护面。
- **iceberg 扩展** — 外湖桥：REST Catalog ATTACH（本目录仅证可安装）。
- **prompt()** — MotherDuck 内置 text-to-SQL（转述 ⚠️）。
- **构建戳版本** — 扩展版本串 v1.5.5-2026-09-355：非 semver 的扩展常态。
- **函数目录** — duckdb_functions()：签名核验的第一情报源（实测 12 的 21 名单）。

## 最新演进与工业实践

- **DuckLake**：1.0（2026-04-13，官宣链沿用姊妹目录核验 ✅ [../DuckDB_in_Action/11-结语与未来.md](../DuckDB_in_Action/11-结语与未来.md)）后成为"单机湖仓"默认答案；本目录内联/时间旅行实测条目是其一手工场记录。
- **MotherDuck**：持续承担"DuckDB 语法云执行"位（官网 ✅ 200；无账号未实证——两书同口径声明）；DIA 07 的架构叙事 + 本章的 CLI/AI 叙事合看为完整。
- **Iceberg 侧**：iceberg 扩展装用无碍（✅），REST Catalog 读在快速演进（官方文档页 ✅ 200），与 Iceberg 活用入門的 Catalog 章（[../Apache_Iceberg活用入門/07-Catalog生态.md](../Apache_Iceberg活用入門/07-Catalog生态.md)）互为消费/规范两侧。
- **工业实践**：跨源对账（本目录 sqlite×parquet join 0.19 s）说明"以 DuckDB 为查询总线、格式各留其所"是 2026 中小数据平台的现实主流。
- **目录互操作前线**：Iceberg REST Catalog 的读路径在 1.x 线快速演进（本章 iceberg 扩展仅证"可装"）——外湖/自湖（DuckLake）/云托管（md:）三形态的边界每年都在挪，选型以当期文档为准（定性，配套实测见本文件三节）。
