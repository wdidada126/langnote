# 07 · Using DuckDB with JupySQL（DuckDB 与 JupySQL）

> 覆盖原书第 7 章。目录来源：✅ 官方示例文件 `Chapter_7.ipynb` 标题实抓。JupySQL（`%sql` 魔法）是"SQL -first 笔记本"的载体：本章教它在 DuckDB 上的完整闭环——连接、查询、片段(snippet)复用、`%sqlplot` 可视化，最后把同样的姿势伸向 MySQL。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Installing JupySQL** → `pip install jupysql`（+ DuckDB 走 `duckdb-engine`/原生 duckdb）。
- **Magic commands to use JupySQL to interact with your data sources**：`%sql/%sqlplot/%table/%schema` 魔法总览。
- **Loading the sql Extension**：`%load_ext sql`。
- **Integrating with DuckDB**：`%sql duckdb://`（内存）与文件库连接串；notebook 逐条注释两种形态（✅ 实抓）。
- **Performing Queries / Storing Snippets**：查询与 `--save/--execute` 片段复用。
- **Visualizations**：**Histograms / Box Plots / Pie Charts / Bar Plots** 四节 `%sqlplot`。
- **Integrating with MySQL**：三种凭据姿势——**Using Environment Variables / Using an .ini File**（示例仓库自带 `connections.ini`，✅ 树实抓）**/ Using keyring**。

## 核心技术清单

- 栈层次：IPython magic（jupysql）→ SQLAlchemy Dialect（duckdb-engine）→ 原生 duckdb DBAPI——三层各可单独用，jupysql 是"表壳+计划缓存+绘图"层。
- 连接串：`duckdb://`（内存）、`duckdb:///相对.db`、`mysql://user:pw@host/db`（走 mysqlconnector/pymysql）。
- 结果面：`Result = %sql SELECT…` → `.DataFrame()/.PolarsDataFrame()`；`--persist/--persist-replace` 把 df 送进库；`interact` 反查。
- Snippets：`--save name SELECT…` 存为可组合 CTE，下游 `WITH x AS (SELECT * FROM name)` 引用（`Generating CTE with stored snippets` 日志 ✅ 实测）。
- `%sqlplot histogram/boxplot/pie/bar`：SQL 侧聚合 + matplotlib 出图，图不进内存全量。
- 凭据卫生：环境变量 > `.ini` > keyring；连接串模板化。

## 🔧 实测（jupysql **0.11.1**（pip 解析所得）/ duckdb-engine **0.17.0** / SQLAlchemy 2.1.1 / ipython 9.17.1 / duckdb 1.5.5；本书 580 万行航班数据）

1. **加载与连接**：`%load_ext sql` **1.79 s**（import 风暴）；`%sql duckdb://` **0.60 s** 建连。
2. **查询通道**：`%sql SELECT count(*) FROM 'flights2015.parquet'` → **5,819,079 / 0.05 s**；分组 Top-2 `[('WN',1261855),('DL',875881)]` **0.02 s**——魔法壳对原生引擎的时延税在毫秒级（结果小场景）。
3. **持久化往返**：`%sql CREATE TABLE samp AS SELECT … USING SAMPLE 500000 ROWS` ✅；回查 `SELECT count(*) FROM samp` **0.00 s**（50 万行计数）。
4. **结果出口漂移** ✅：`res.df()` 在 0.11.1 **不可用**（AttributeError 明示改 `.DataFrame()`/`.PolarsDataFrame()`）；`%sql -o df` 参数不识别（UsageError）——成书（2024，jupysql 0.10 代）代码到 2026 要改这两处。
5. **Snippet 语义** ✅：`--save topcarriers …` 返回 ResultSet；再跑 `--execute topcarriers` 返回 **None**（本版执行但对象不回传）；`SELECT * FROM topcarriers` 触发 CTE 展开（日志 "Generating CTE with stored snippets: 'topcarriers'"）——片段=视图糖。
6. **duckdb-engine（SQLAlchemy 层）**：`pd.read_sql("SELECT count(*) FROM 'flights2015.parquet'", engine)` **0.04 s**（原生同查 0.00 s）；groupby 出口 **0.01 s**（原生 0.02 s，相当）；**大结果分水岭**：拉 2M 行进 pandas，engine **14.40 s** vs 原生 `.df()` **3.38 s**——**4.3 倍行级转换税**。
7. **MySQL 侧**：`mysql_scanner` 扩展可装（13.3 s ✅）但本机无 MySQL 服务器，jupysql→MySQL 全链 **⚠️ 未实证**；`.ini/keyring` 姿势按 notebook 小节结构转述。

## 易错点与陷阱

- **魔法壳不是性能通道**：小聚合无所谓，**大结果集一律绕开 jupysql 出口**（实测 4.3× 税）——要么 SQL 里先聚合，要么 `duckdb.connect(...).to_arrow_table()` 直取。
- **`duckdb://` 与原生连接不共享对象**：魔法里建的表，`duckdb.connect()` 新连接看不到（不同引擎实例）；文件库（`duckdb:///x.db`）才跨会话持久。
- **snippet 当"物化表"用**：它是每次展开的 CTE，重复 `--execute` = 重复计算；高频复用就 `CREATE TABLE AS`。
- **`%sqlplot` 的数据侧成本**：histogram 会真跑 `width_bucket` 聚合——先 EXPLAIN/估行数再画。
- **连接串里的凭据**：notebook 明文 `mysql://u:p@…` 是教学写法；.ini/keyring 才是提交写法（本章三节的排序本身就是答案）。
- **版本矩阵**：jupysql/ipython/sqlalchemy 三者互相有兼容窗（本机 pip 把 jupysql 解到 0.11.1 而非最新）——笔记本栈升级要三件套一起演。
- **`.df()` 不只是慢、是没了**：0.11.1 直接 AttributeError 并明示 `.DataFrame()`（实测 4）——老 notebook 先全局替换结果出口再谈运行。
- **`--execute` 返回 None 不是失败**：本版执行但不回传对象；要看结果写 `SELECT * FROM snippet`（实测 5）——把 None 当崩溃会掉进反复 `--save` 的坑。

## 笔记本 SQL 工作流模板（实测号注记版）

```python
%load_ext sql                       # 首次 import 风暴 1.79 s（实测 1），内核复用后免
%sql duckdb:///analysis.db          # 文件库=跨会话持久；duckdb:// 仅内存（陷阱 2）
```

```sql
-- 缓存层：把"反复用"缩成小表（实测 3：SAMPLE 500,000 建 samp）
CREATE TABLE IF NOT EXISTS samp AS
SELECT * FROM 'flights2015.parquet' USING SAMPLE 500000 ROWS;
-- 定义层：业务口径命名进 snippet（实测 5：片段=视图糖/CTE 展开）
--save topcarriers SELECT AIRLINE, count(*) c FROM samp GROUP BY 1
-- 组合层：片段拼片段，只有最外层 SELECT 真执行
SELECT * FROM topcarriers WHERE c > 100000 ORDER BY c DESC LIMIT 5;
```

- 出口规则：小结果 → `.DataFrame()`（实测 4 的改后写法）；大结果 → 不过魔法壳，`duckdb.connect(...).to_arrow_table()` 直取（4.3× 税，实测 6）。
- snippet 无统计无物化——正式管道把等价逻辑升级为 CTAS 落库表（02 章流水线），片段只当笔记本内的口径备忘。

## %sqlplot 四图模板（本章 Visualizations 小节 × 本目录数据）

```sql
%sqlplot histogram --column DEPARTURE_DELAY --table samp --bins 50
%sqlplot boxplot   --column DEPARTURE_DELAY --group AIRLINE --table samp
%sqlplot pie       --column AIRLINE --table samp
%sqlplot bar       --column AIRLINE --table samp
```

- 成本提醒：histogram/boxplot 在 SQL 侧真跑 `width_bucket`/分位聚合（陷阱 4）——画图吃 `samp` 缓存是 %sqlplot 的定位，5.8M 原表直画是自虐。
- 与 05 章"matplotlib/folium 路线"的分工：%sqlplot 卖点=**图跟着 SQL 走**、结果不过 df 落地——中小结果集可视化闭环；地图与精细排版仍归 Python 侧库。

## 凭据卫生清单（本章 MySQL 三小节排序的升级版）

1. **零明文红线**：notebook 单元格里不出现 `mysql://u:p@…`——git 历史与共享截图是两大泄露面。
2. **env 优先**：`%env DB_PWD`/`.env`+启动器注入，单机 CI 两相宜（本章小节 ①）。
3. **`.ini` 次之**：官方示例自带 `connections.ini` 即此形态（✅ 树实抓）——文件进 `.gitignore`、权限收紧。
4. **keyring 最佳**：OS keychain 承载存储、notebook 只引用服务名——多人多机同步的终点（小节 ③）。
5. **连接串模板化**：`mysql+mysqlconnector://user:{pwd}@host/db`，只让 pwd 一位浮动——轮换改一处。
6. **同规约适用 DuckDB 侧**：08/09 章的 `CREATE SECRET`/token 与本章同-code-of-practice——凭据与查询永远分离。

## 何时该离开 JupySQL（本目录实测给出的退出清单）

- 大结果必须进宿主对象 → 原生 `.df()`/Arrow（4.3× 税，实测 6）。
- 要看执行计划/调优 → 原生连接 `EXPLAIN`（魔法壳回显碍事）。
- 复用逻辑已成资产 → snippet 升级为视图/表，再进 dlt/dbt 管道（DIA 08 章叙事）。
- 要事务控制与多连接并发 → 原生 connection 对象。
- 反面"该留"信号：交互报表 + 多库统一门面（本章 MySQL 节）+ sqlplot 轻绘图——这四样 JupySQL 在 2026 仍是最短路径。

## 与其他章/书的互链

- 不经 SQLAlchemy 的直连世界 → [04-DuckDB与Polars.md](04-DuckDB与Polars.md)、[01-DuckDB入门.md](01-DuckDB入门.md)
- SQL 底料与本章查询语法 → [03-SQL速成与CLI.md](03-SQL速成与CLI.md)；MySQL 抽数另一条路（scanner）→ [02-数据导入DuckDB.md](02-数据导入DuckDB.md)
- 同场景的 DIA 口径（关系 API/DBAPI 直用）→ [../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)、矩阵与并发一言 → [../DuckDB_in_Action/12-附录A-客户端API.md](../DuckDB_in_Action/12-附录A-客户端API.md)
- 行式事务库的笔记本生态对位 → [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（#87 已落盘：sqlite3 CLI/应用侧叙事与本章"魔法壳"叙事互为两种 notebook 路线）。

## 思考题（合上笔记再答）

1. jupysql→pandas 与原生 `.df()` 拉 2M 行差几倍？根因？（4.3×；SQLAlchemy 结果对象逐行转换）
2. `--save` 片段与 `CREATE TABLE` 的语义差？（CTE 糖 vs 物化；复用频率决定）
3. 为什么本章特意讲 .ini 与 keyring？给出你的 notebook 凭据卫生清单。
4. `%sqlplot` 为什么先建 `samp` 再画？4.3× 税怎么测出来的？（sqlplot 在 SQL 侧真跑聚合，画缓存=定位正确；拉 2M 行进 pandas：engine 14.40 s vs 原生 `.df()` 3.38 s——实测 6）

## 2026 视角补注

- JupySQL（Ploomber 出品）2024→2026 主线加了 `ggtables`/`--interact` SQL 单元格 UI 等；本机装到的 0.11.1 属"兼容锁"代际——文档站 jupysql.ploomber.io 本网络不可达 ⚠️，PyPI 页 ✅ 可查版本史。
- "笔记本 SQL 三形态"（jupysql / duckdb-engine / 原生）+ Polars 的 `SQLContext`（04 章）构成 2026 年的完整选择空间；DuckDB 官方客户端文档只列后者两类（clients 矩阵 ✅），jupysql 属社区层——两书互补处正在于此。

## 核心概念速览（中英对照）

- **魔法命令** — IPython magics（%sql/%sqlplot）：单元格级 SQL 壳。
- **连接串** — Connection string：`duckdb://`/`mysql://` URL 寻址。
- **Dialect** — SQLAlchemy 方言：duckdb-engine 的桥接口。
- **片段** — Snippet（--save）：命名 CTE 复用单元。
- **持久化** — --persist：DataFrame→表的一键通道。
- **结果对象** — ResultSet：`.DataFrame()/.PolarsDataFrame()` 出口。
- **SQL 绘图** — %sqlplot：聚合在 SQL、绘制在 matplotlib。
- **凭据链** — env/.ini/keyring：三档卫生等级。
- **行级转换税** — 大结果经通用 DB 层的放大成本（实测 4.3×）。
- **实例隔离** — 引擎实例边界：`duckdb://` 内存库不跨连接。

## 最新演进与工业实践

- **栈版本实测**（本机）：jupysql 0.11.1 + duckdb-engine 0.17.0 + SQLAlchemy 2.1.1 + ipython 9.17.1 组合可用（importlib.metadata 实抓 ✅）；PyPI 项目页（https://pypi.org/project/jupysql/ 、 https://pypi.org/project/duckdb-engine/ ✅ 200）为版本权威源。
- **趋势**：2024 后"魔法层"叙事收窄——marimo/quarto 等新一代笔记本要么原生 SQL 单元格、要么直连引擎；jupysql 的价值位收敛到**snippet 组合 + sqlplot + 多库统一门面**（本书三节 MySQL 姿势学即是跨库部分）。
- **工业实践**：报表型笔记本的通行分层 = SQL 聚合（DuckDB）→ 小结果进 pandas 画图 → 凭据外置；本目录的 4.3× 税数据是"大结果不过壳"红线的量化依据（🔧 自测）。
