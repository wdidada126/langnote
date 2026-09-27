# 第 3 章 使用Trino（Working with Trino ⚠️ 英题推定）

> 对应原书第一部分第 3 章。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。示例为教学示意。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 3.1 Trino CLI | 官方 Java 交互终端，脚本模式可管道化 | 一切客户端里最「原生」的排错入口 |
| 3.2 Trino JDBC驱动 | 标准 JDBC 方言适配，BI/Java 应用的通用胶水 | 驱动 jar 即含 shaded 依赖，拿来即用 |
| 3.3 Trino与ODBC | C++/Excel/Tableau 等非 JVM 生态入口 | 与 JDBC 同层，配置 DSN 略繁 |
| 3.4 客户端库 | Python `trino`、Node、Go 等官方/社区库 | pandas 一行 `trino_python` 风格取数是 Python 侧日常 |
| 3.5 Trino Web UI | 8080 端口内嵌 UI：查询列表、stage 树、JSON plan | 第 12 章调优的主战场从这扇门进 |
| 3.6 使用Trino执行SQL | 会话、事务边界、查询即提交的语义提醒 | Trino 只读为主，DML 依赖 connector 能力 |
| 3.7 小结 | — | 客户端选定后，进 Part II 看内核 |

## 核心精讲

### 1. CLI：最小可用，也是最大公约数

```bash
# 教学示意
trino --server http://localhost:8080 --catalog tpch --schema tiny
trino -f report.sql --output-format=CSV_HEADER  # 批处理/定时任务形态
```

要点：CLI 是 fat jar（`java -jar trino-cli-*-executable.jar`），版本与服务器兼容性走标准 SQL + JDBC 语义，通常不必严格同版。

### 2. JDBC/ODBC：BI 接的到底是「协议」不是「引擎」

- JDBC 驱动类 `io.trino.jdbc.TrinoDriver`，URL 形如 `jdbc:trino://host:8080/catalog/schema`；无密码时也**必须**给 `user=`（多数默认访问控制会拒绝匿名）。
- ODBC 走 DSN/驱动管理器，Windows 侧 Tableau/Excel、Linux 侧 C++ 应用经它接入；与 JDBC 平级，二者都只认 Trino 的 SQL 方言与结果协议。
- 483 文档的客户端总览 ✅ [client.html](https://trino.io/docs/current/client.html)：官方把 client 分为 drivers（JDBC/ODBC）+ apps（CLI 等）+ libraries（Python 等）+ API（REST）。

### 3. Python 客户端（3.4 的当代主流量）

```python
# 教学示意：pip install trino
from trino.dbapi import connect
cur = connect(host="localhost", port=8080, user="alice",
              catalog="tpch", schema="tiny").cursor()
cur.execute("SELECT nationkey, name FROM nation LIMIT 3")
print(cur.fetchall())
# 生态扩展：pandas 侧有第三方 fastparquet/ADBC 风格取数方案 ⚠️ 具体库名以 PyPI 现状为准
```

官方还提供 `trino-python-client` 的 SQLAlchemy dialect 与 `trino_auth`（LDAP/证书）支持 ⚠️ 细节未逐项抓，仓库 `trinodb/trino-python-client`（同组织下，组织页经 GitHub 可达 ✅ [trinodb](https://github.com/trinodb/trino/releases) 侧证组织活跃）。

### 4. Web UI：引擎的「听诊器」

`http://localhost:8080/ui` —— 查询列表 → 单查询详情：执行计划树、stage 分解、driver/任务时间线、各 stage 输入输出字节数、JSON plan 下载。书把它放在使用章、把调优放在 12 章是同一逻辑：**先认界面，后学读法**。483 起部分历史页面/接口有变（如旧 UI 端点的存续 ⚠️ 未逐项核），入口文档见 client.html 之 apps 节 ✅。

### 5. 执行语义（3.6）：会话即上下文

- 一条连接 = 一个 session：`USE catalog.schema`、`SET SESSION query_max_execution_time='30s'`、`SHOW SESSION` 三件套。
- Trino 对「事务」的支持是**弱**的：查询级原子可见（connector 自定），无跨语句 ACID 常规事务——写侧事务交给表格式/Iceberg（06 章）。
- `EXPLAIN` / `EXPLAIN (TYPE DISTRIBUTED)` 是 SQL 使用与架构（04 章）的桥（✅ [sql/explain.html](https://trino.io/docs/current/sql/explain.html)）。

### 6. 客户端选型速查表（3.1–3.6 收束）

| 你是谁 | 首选 | 次选 | 注意 |
| --- | --- | --- | --- |
| 引擎开发/排障 | CLI + Web UI | 系统表 SQL | CLI 的 `--debug` 与 EXPLAIN 连用 |
| BI 工具（Java） | JDBC 驱动 | ODBC | fetch size 与超时先对齐工具默认 |
| BI 工具（桌面/C++） | ODBC | REST 自研 | DSN 配置与证书链是主要摩擦点 |
| 数据科学/Python | trino-python-client | SQLAlchemy/df 封装 | 大结果集考虑 CTAS 落湖再取 |
| 应用后端 | JDBC/REST API | 池化封装 | 配 plan caching/预处理（9.22） |
| 自动化脚本 | CLI `-f --output-format` | REST 直调 | 别解析交互模式装饰输出 |

选型公理：Trino 所有客户端都收敛到同一 REST 协议（client 文档 API 节 ✅）——差异只在绑定风格，不在能力；因此「换客户端=换工作流」而非「换功能」。

### 7. 一条查询的客户端旅程（衔接 4 章）

`提交 POST /v1/statement` → 拿到 nextUri 轮询 → 状态从 QUEUED/PLANNING/…/FINISHED → 按 token 分批取 result 页（03.5 UI 里的进度条就是这条轮询的可视化）。理解它，UI/JDBC/CLI 三节的所有「怪行为」（假死、首字慢、取消传播）都有统一解释：客户端只是协议的忠实观众（机制在 [04-Trino架构.md](04-Trino架构.md) 展开）。

## 本章一句话与三个动作

一句话：客户端不改变引擎能力，只改变你触碰引擎的姿势。三个跟练动作（配 02 章本地集群）：

1. `trino --server ... --execute "SELECT 1"` —— 打通协议；
2. UI 里点开这条查询，下载 JSON plan —— 打通内省；
3. Python 里 `fetchall()` 同一查询 —— 打通编程面。

三个动作完成，第 3 章的所有小节都已被你亲手摸过一遍；之后的 BI/编排话题（11 章）只是把动作 3 换个调用方。

## 常见误区

- BI 连上就慢：多半是默认 `task.concurrency`/分页行为与 BI 的分面查询模式不合（12 章），而非协议问题。
- Web UI 在生产裸奔：UI 与 REST 共用 8080，默认无鉴权——上生产必须接认证（10 章）。
- JDBC `Properties` 忘设 `SSL=true` 却在 https 端点连不通；证书链问题同因。
- 把 CLI 交互模式输出直接重定向当数据管道：应使用 `--output-format` 与 `-f`（交互模式有装饰噪声）。

## 与其他章/其他书的联系

- 查询内部长什么样 → [04-Trino架构.md](04-Trino架构.md)；UI 的调优读法 → [12-生产环境中的Trino.md](12-生产环境中的Trino.md)。
- BI/可视化侧 Superset 集成在 [11-将Trino与其他工具集成.md](11-将Trino与其他工具集成.md)；ODBC/JDBC 之外还有一层「驱动概念」可对照 [../SQL系列·总索引.md](../SQL系列·总索引.md) 中的 SQL 基础书目。
- 数仓工具链视角（ETL/BI 怎么选端口）配 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md)。

## 核心概念速览（中英对照）

1. **命令行界面** — CLI (trino shell)：官方交互式/脚本化终端。
2. **JDBC 驱动** — JDBC driver：`io.trino.jdbc.TrinoDriver`，BI/Java 标准接入层。
3. **ODBC 驱动** — ODBC driver：非 JVM 语言与桌面 BI 的 C 层接入。
4. **DB-API 客户端** — Python dbapi：PEP-249 风格 `trino.dbapi.connect`。
5. **REST API** — Trino REST protocol：所有客户端最终落到同一 HTTP 协议（client API 文档口径）。
6. **会话** — session：连接级上下文，承载 catalog/schema/属性/事务提示。
7. **会话属性** — session property：`SET SESSION ...` 的查询行为开关。
8. **查询即提交** — query-at-a-time semantics：无多语句事务包，重跑即重查。
9. **Web UI** — web UI：内嵌只读监控台，stage 树与计划入口。
10. **JSON plan** — JSON plan：可下载的分布式计划序列化，调优与复盘素材。
11. **分页** — pagination：JDBC fetch size 与服务端输出缓冲的合体行为。
12. **fat jar 客户端** — shaded jar：自包含依赖的驱动/CLI 分发形态。
13. **认证透传** — client authentication：JDBC/ODBC/CLI 均按 10 章机制带凭据。
14. **方言兼容层** — SQL dialect compatibility：客户端只感知 ANSI 化方言，不感知引擎内部。

## 最新演进与工业实践

- **客户端矩阵现状** ✅：官方 [client.html](https://trino.io/docs/current/client.html)（483）维护 JDBC/ODBC/CLI/Python 全链；JDBC 驱动版本随 Trino 号发布（Maven `io.trino:trino-jdbc`，坐标在 mvnrepository 长期可查 ⚠️ 版本号未逐抓）。
- **ADBC/列式直取**：2024–2026 生态趋势是经 Arrow 类通道（如 Flight SQL/ADBC 方向）做客户端列式取数以甩开行式协议开销；Trino 官方主协议仍是 REST 行式，社区实现推进中（⚠️ 本次未抓到可引用的官方 GA 页，作趋势转述）。
- **Web UI 迭代**：483 的 release notes 每版几乎都有 Web UI/JDBC/CLI 小项（✅ [release-483.html](https://trino.io/docs/current/release/release-483.html) 目录含 Web UI/JDBC/CLI 三节），UI 的 token/认证与旧端点有收紧。
- **工业实践**：BI 侧 Tableau/Superset 连 Trino 的标准姿势 = Trino 前加一层语义层（cube/指标层）已成主流；与 [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md) 中「Spark 出数、BI 读结果」的传统链路对照，Trino 允许 BI 直查湖表。
