# 06 — 数据发现与 Spark SQL 目录（Data Discovery and the Spark SQL Catalog）

> 《Modern Data Engineering with Apache Spark》第 6 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_6` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark SQL Catalog 官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

「让数据可被找到」的一章：Spark SQL Catalog 是表的元数据中枢——库/函数/视图的注册、查询、生命周期。工程叙事上它承接第 3 章的「表语义 vs 路径语义」分岔，开启第 7 章管道组织（管道产物要注册才可消费）与第 12 章分析面（分析师从目录出发而非从目录树出发）。

## 2. Catalog 对象模型（⚠️ 按章题域重构）

- 三级命名：`catalog.namespace.identifier`；Spark 2.x 单命名空间模型在 3.0 升级为多部分命名（V2 支持，⚠️ 本书展开深度未证实）。
- `spark.catalog` API：listTables/listColumns/listFunctions/currentDatabase/createTable 等——程序化发现的面。
- SQL 侧：`SHOW TABLES`、`DESCRIBE FORMATTED`、`SHOW CREATE TABLE`、`REFRESH TABLE`——交互发现的三件套。
- 缓存管理：`cacheTable`/`uncache`/`clearCache`（性能话题与元数据话题在 catalog 交汇）。

## 3. 视图家族辨析（本章最易考人的小节，⚠️ 重构）

| 对象 | 生命周期 | 跨 Session 可见 | 物化 |
|------|----------|----------------|------|
| TempView (`createOrReplaceTempView`) | 当前 Session | 否 | 否 |
| GlobalTempView (`createOrReplaceGlobalTempView`) | 所有 Session（`globaltemp` 库） | 是 | 否 |
| 永久视图 (`CREATE VIEW`) | Metastore 持久 | 是 | 否 |
| 物化表/缓存 | 取决于实现 | 是（表） | 是 |

- 事故高发区：把 DataFrame 注册成 tempView 后跨作业引用；GlobalTempView 的 `globaltemp.` 前缀遗漏。
- Hive Metastore 作为默认持久层：`spark.sql.warehouse.dir` 与 metastore_db 的本地形态正是本书 local platform 的落点（⚠️ 推定其演示形态）。

## 4. 数据发现工作流（工程册的「发现」= 元数据 + 采样 + 血缘雏形）

1. `SHOW NAMESPACES/TABLES` 圈定候选。
2. `DESCRIBE` + `SELECT ... LIMIT` 双验 schema 与真实样本。
3. `df.printSchema()` 对齐类型；注意 metastore 记录与文件实际 schema 漂移（写时不校验的历史包袱）。
4. 函数面 `SHOW USER FUNCTIONS` 复用已有 UDF 注册。
5. 文档外溢：目录不含业务语义，README/列注释纪律由工程规范补位（⚠️ 重构的目录解读）。

## 5. 🔧 实测·类比：SQLite 的 schema 中枢 = 最小 catalog（非 Spark 行为）

```python
import sqlite3
s = sqlite3.connect("demo.db")
s.execute("CREATE TABLE cust(id INTEGER PRIMARY KEY, name TEXT)")
s.execute("CREATE VIEW vip AS SELECT * FROM cust WHERE id>100")
print(s.execute("SELECT name,type FROM sqlite_master ORDER BY type,name").fetchall())
print(s.execute("PRAGMA table_info(cust)").fetchall())
```

- 观察：`sqlite_master` 即目录（表/视图注册处），`PRAGMA table_info` 即 `DESCRIBE`——「SQL 引擎=数据+目录」的最小实例。
- 类比映射：Spark catalog ↔ sqlite_master；永久视图 ↔ SQLite VIEW（持久）；TempView ↔ `CREATE TEMP VIEW`（会话级）——**SQLite 连 temp 视图都给了你对偶概念**，视图家族的持久性差异一句话讲清。
- 边界：无多命名空间/无缓存语义/无 V2 插件目录（DuckDB 亦仅弱扩展），Spark 的 catalog 插件（Iceberg/Paimon 自带目录）在此不可见（🔧）。

## 6. 目录即接口：为 12 章与湖仓埋线

- 分析消费者「从目录出发」的路径（→ 第 12 章）。
- 湖仓表格式自带元数据层并**反向接管 catalog**（Iceberg REST Catalog、Paimon 的文件目录两种形态）：对位 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)、[../Apache_Paimon_Streaming_Lakehouse/04-元数据层快照与清单.md](../Apache_Paimon_Streaming_Lakehouse/04-元数据层快照与清单.md)。
- 「namespace 三段式」在 2022 是前瞻话题，2024–2026 已是开放目录标准战（Unity/Polaris）：对位 [../Apache_Polaris_TDG/00-总览与阅读地图.md](../Apache_Polaris_TDG/00-总览与阅读地图.md)、[../Data_Governance_with_Unity_Catalog 谱系见总索引（登记不链）]。

## 7. 校读清单

- 作者是否演示 `spark.catalog.listTables()` 的 Python 编程面？——决定本章是否服务自动化场景。
- 是否配置 `spark.sql.catalog.*` 挂外部目录？——2022 年多数教材未跟进 V2 catalog，需校准。
- 血缘工具（Spline/Marquez）是否被提及？——预期没有，属本书留白（⚠️）。

## 8. 本地 catalog 的地盘图（本书 local platform 语境，⚠️ 推定重构）

```text
~/workspace/
├── spark-warehouse/            # warehouse.dir：默认库的表数据落点
│   └── <db>.db/<table>/        # 目录名即命名空间投影
├── metastore_db/               # derby 元数据（本地 derby 内嵌形态）
└── derby.log                   # metastore 进程的喧嚣见证
```

- 升级路径：derby → 外置 Postgres 后端 metastore（并发读写解禁）→ V2 catalog（湖格式自持元数据）——三级跳恰是 2022→2026 工业迁徙的缩影。
- 工程提醒：`metastore_db` 被多 Session 同时打开是 derby 第一事故；外置化是所有「团队本地平台」的第一步（⚠️ 通行经验）。

## 9. 本章实验卡（⚠️ 非原书代码）

1. 建两张表（一路径一表），`SHOW TABLES`/`DESCRIBE FORMATTED` 记录二者元数据差异——§1「表 vs 路径」实证。
2. `createOrReplaceTempView` 后**新开 Session** 查询失败 → 换 `createOrReplaceGlobalTempView` 加 `globaltemp.` 前缀成功：视图家族生命周期的十秒教学。
3. 手工移动表目录下的文件后 `SELECT` 报错 → `REFRESH TABLE` 治愈：metastore 与数据的裂缝肉眼化。
4. `spark.catalog.listColumns()` 编程遍历全库，导出「schema 盘点 CSV」——发现工作流 §4 的脚本化。
5. 注册一个 UDF 后 `SHOW FUNCTIONS` 对比系统函数：命名空间里的「人类痕迹」清点。

## 10. 校读问答（五问五答）

- **Q：本章会不会太薄？** A：catalog 单讲确实薄——本书把它与「数据发现」并题正解：对象模型+工作流两腿，缺一即 API 清单。
- **Q：血缘在这里讲吗？** A：不预期（2022 教材通病）；补位读法见演进节工具线与 [../Data_Governance_Elsevier 谱系登记见总索引]。
- **Q：V2 多部分命名值得学吗？** A：值——它是 Iceberg/Paimon 目录挂载的语法前提（§6 两链接待命）。
- **Q：缓存节（§2 末）重要吗？** A：对工程决策重要、对元数据模型无关——目录顺手管了物理缓存，历史耦合，⚠️ 读时留意作者如何取舍。
- **Q：Spark 4.x 变化？** A：ANSI 默认改变列校验严格度、V2 接口继续稳定；derby 内嵌仍仅限玩具级并发（⚠️ 转述 + 文档校核）。

## 11. 章末锚点卡（速记三线，⚠️ 目录制）

- 一条主线：catalog=数据资产的户籍系统——没有它，3/4 章的产出只是散落的文件。
- 一条警戒线：derby 内嵌 metastore 禁并发；「本地玩具」与「团队平台」的第一道分水岭（§8 三级跳起点）。
- 一条接口线：表语义（3 章分岔）→ 注册（本章）→ 发现（12 章消费面）——数据生命线的中段。
- 记忆钩：视图家族四行表（§3）+ `sqlite_master` 对偶实验（§5）——两个锚点把「注册表」抽象钉死。
- 前瞻：开放目录（Polaris/Unity）把户籍系统升级为海关（治理+发现合一）——演进节的两链在盘可点。

## 核心概念速览（中英对照）

- **Spark SQL 目录** — Spark SQL Catalog：表/函数/命名空间的元数据中枢。
- **命名空间** — Namespace：三段式命名中的中间层（≈库）。
- **临时视图** — TempView：Session 级注册的逻辑查询别名。
- **全局临时视图** — GlobalTempView：跨 Session、`globaltemp` 库承载的临时注册。
- **永久视图** — Persistent View：写入 metastore 的视图定义。
- **Hive Metastore** — Hive Metastore：Spark 默认的持久元数据服务。
- **DESCRIBE FORMATTED** — Describe：查列、存储、位置、属性的发现命令。
- **REFRESH** — Refresh Table：让 metastore 与文件实际状态重对齐。
- **缓存表** — Cached Table：`cacheTable` 注册到内存的加速对象。
- **目录插件** — Catalog Plugin（V2）：湖格式自管元数据并暴露给 Spark 的机制。

## 最新演进与工业实践

- **开放表格式目录成为主战场（2023–2026）**：Iceberg REST Catalog 规范、Apache Polaris、Unity Catalog 开源化——本书的 Hive Metastore 默认叙事已让位于「目录即治理平面」；盘上系统展开 [../Apache_Polaris_TDG/00-总览与阅读地图.md](../Apache_Polaris_TDG/00-总览与阅读地图.md)。
- **Spark 4.x**：V2 命名空间/目录接口持续稳定，ANSI 默认使目录里的类型检查更严（⚠️ 转述；校核 ✅ https://spark.apache.org/docs/latest/sql-programming-guide.html）。
- **数据发现工具外置**：元数据抓取（DataHub/OpenMetadata/Amundsen）把「发现」从 SQL 客户端移入专用 UI；Spark catalog 退化为其中一类源（⚠️ 观察性陈述）。
- **发现即合规**：EU 数据法案与行业合规推动「列级血缘+所有权」进入目录默认字段，本书的「README 纪律」被产品化为目录属性（⚠️ 观察性陈述）。
- **SQLite/DuckDB 对照提醒**：本目录 §5 类比仅示意「目录=注册表」抽象；生产 Spark 的并发 metastore（MySQL/PG 后端 + 缓存）性能行为需另行校核官方文档（⚠️）。
