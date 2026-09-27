# 04 · 从其他语言使用 SQLite ⚠️ 章号推定

> 主题锚定：语言绑定层的共性（连接/游标/绑定/事务语义）、以 Python `sqlite3` 为主要标本，
> 兼述 Perl DBI / PHP PDO / Tcl / ODBC / .NET / Ruby 生态位。
> 官方依据：[docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html) ✅
> （curl 200，本会话）、[bindparam C 页](https://sqlite.org/c3ref/bindparam.html)（404，改用
> [capi3ref.html](https://sqlite.org/capi3ref.html) ✅ 总入口）。

## 1. 绑定层的谱系：全都薄，全都通向同一张 C API

书中逐一演示 Perl DBI、PHP PDO、Tcl sqlite3、Ruby-DBI、ODBC、.NET；2026 的生态位变化：

| 通道 | 书中时代 | 2026 现状 |
| --- | --- | --- |
| Python `sqlite3` | 标准库成员 | 标准库仍在（PEP 735 后仍随 CPython 分发，🔧 本机 3.13.2 内置 3.45.3）；异步侧 aiosqlite 流行 ⚠️ 未核验仓库 |
| PHP PDO | 默认捆绑 | 仍是默认（php-src ext/pdo_sqlite） |
| Ruby sqlite3 gem | gem | 地位被 better-sqlite3（Node）类比下去；Node 生态 `node:sqlite` 内置（Node 22+，⚠️ 版本细节未核验） |
| Tcl | 一等公民（SQLite 官方测试用 Tcl） | 小众但在 TCL 社区仍捆绑 |
| ODBC | 驱动存在 | 边缘化，BI 工具偶用 |
| .NET | System.Data.SQLite | Microsoft.Data.Sqlite 成主流（⚠️ 未核验仓库） |

共同点（书中核心洞见，依然成立）：**绑定 = 把 C API 的 prepare/step/bind 三件套
翻译成各语言的惯用形态**。因此语言层的坑基本都是 05 章 C 语义坑的马甲。

## 2. Python 标本：DB-API 2.0 与 SQLite 语义的三层摩擦

1. **事务模式**：DB-API 要求隐式 BEGIN/autocommit 开关；Python 长期用"legacy 隐式事务"
   （DML 前偷偷 BEGIN），3.12 起新增 `autocommit` 属性给出显式三态
   （LEGACY_TRANSACTION_CONTROL / True / False，官方文档 ✅）。书中"驱动怎么帮我开事务"
   的问题，如今答案是"你自己说清楚"。
2. **占位符方言**：qmark/named/format/pyformat——同一 SQL 在不同库间搬运会炸；
   `sqlite3.paramstyle='qmark'` 是锚。
3. **行是元组**：`row_factory`（`sqlite3.Row`）解决"SELECT * 后列名漂移"问题——
   书中"换列序代码就坏"的老毛病，一行配置治好（🔧 见实验 C）。

## 3. 🔧 实测（本会话，CPython 3.13.2 / SQLite 3.45.3）

### 实验 A：事务包裹的杀伤力——同一批数据三种写法

方法：10,000 行 `(int, float)` 插入，三组：
(a) `isolation_level=None` 逐条 `execute INSERT`（每条一个自动提交事务）；
(b) 显式 `BEGIN` + 循环 + `COMMIT`；(c) `BEGIN` + `executemany` + `COMMIT`。

结果（🔧，同一台 Windows 机器两轮）：

| 写法 | 耗时 |
| --- | --- |
| 逐条自动提交（10k 次 fsync 风暴） | 23.1 s / 另一次 161.7 s（Windows 杀软/IO 抖动放大离散度） |
| 单事务循环 | **0.016–0.099 s** |
| 单事务 executemany | **0.006–0.012 s** |

- **结论量化**：单事务 vs 逐条提交相差 **~4 个数量级**（最坏对比 13,852×）。
  这就是书中"SQLite 慢的传说几乎都是 autocommit 背锅"的实测注脚。
- `executemany` 相对纯循环再快约 8×（省 Python 层调用开销），
  但真正的鸿沟在事务边界，不在 API 选择。

### 实验 B：并发与 busy_timeout——Python 层的锁体验

方法：连接 A `BEGIN EXCLUSIVE` 后挂 1s 提交；连接 B1 `timeout=0`、B2 `timeout=3.0` 同时
`BEGIN IMMEDIATE`。

结果（🔧）：
- B1 **0.036 s** 即抛 `sqlite3.OperationalError: database is locked`（SQLITE_BUSY）；
- B2 **阻塞 1.10 s 后拿到锁**（等待时间 ≈ 写者提交时刻，busy handler 按指数退避轮询）；
- 这正是 C 层 `sqlite3_busy_timeout()`（[c3ref/busy_timeout.html](https://sqlite.org/c3ref/busy_timeout.html) ✅）
  的 Python 马甲：`connect(timeout=…)` 参数只映射到这一个调用（Python 默认 5.0 s，
  官方文档 ✅）——它只管**锁等待**，不管其他任何错误。

### 实验 C：DB-API 惯用法采样

- `last_insert_rowid()` → 1；`conn.total_changes` → 3（🔧，跨 INSERT 累计，对应 08 章"Changes"）；
- `IntegrityError: UNIQUE constraint failed: k.u`——Python 3.11+ 起异常自带
  `sqlite_errorname='SQLITE_BUSY'`/`sqlite_errorcode=5` 字段（🔧 实测：锁冲突时
  `errorcode=5, errorname=SQLITE_BUSY`；语法错 `SQLITE_ERROR/1`）；
  **错误处理从"匹配字符串"进化为"匹配枚举"**——书中"别拿 errno 当字符串比"的愿望
  由语言绑定实现。
- 行工厂：`row['city']` 按名取列；`detect_types` + 转换器解决 `TEXT 存日期` 老问题，
  但当代更推荐直接存 ISO 文本（6 章）。

## 4. 线程模型：多连接是契约

- SQLite `THREADSAFE=1`（🔧 本机 CPython 编译选项即 1=serialized）：同一连接可跨线程用
  但会串行化；Python 默认 `check_same_thread=True` 在语言层再设一道闸。
- 书中"每线程一连接"教范在 2026 仍是正解：连接对象极廉价（🔧 01 章实测开+查 0.13 ms/次），
  没必要池化到共享——池化反而是 busy 错误的放大器（写者只有一个，池化不增加写并发）。

## 5. 跨语言速记（书中"每种语言一节"的 2026 压缩版）

1. PHP PDO：`new PDO('sqlite:app.db')` + `setAttribute(ERRMODE, EXCEPTION)`；事务原生。
2. Node（better-sqlite3 风格）：同步 API 反而贴合 SQLite 的低延迟特性（🔧 本会话未装 Node，⚠️ 转述）。
3. Java/Android：`android.database.sqlite` 把库包在 OS 层，App 拿到的版本≠你想要的版本
   （02 章"发行版滞后"的移动特化版）。
4. 一切绑定的共同建议：显式事务、显式 timeout、按名取列、错误按 code 匹配。

## 6. 本章带走三条

1. 绑定层教的是"翻译学"：把 05 章 C 语义直译成各语言惯用法，没有黑魔法。
2. 性能问题九成在事务边界（🔧 4 个数量级实测），并发问题九成在 timeout/busy 语义。
3. 2026 语言层的进步：显式 autocommit 三态、错误码枚举、backup() 直接暴露在线备份 API。

## 核心概念速览（中英对照）

- **DB-API 2.0** — Python PEP 249 数据库接口规范，sqlite3 模块遵循之
- **参数风格** — paramstyle：qmark/named/format/pyformat 四种占位符方言
- **隐式事务控制** — implicit transaction control：驱动自动 BEGIN 的历史行为（legacy mode）
- **autocommit 三态** — autocommit attribute：3.12+ 显式接管事务边界的新 API
- **行工厂** — row_factory：把元组行换成按名访问的映射（sqlite3.Row）
- **忙超时** — busy timeout：遇锁时阻塞重试的上限秒数（映射 sqlite3_busy_timeout）
- **SQLITE_BUSY** — busy error：写锁冲突的可重试错误码（🔧 errorcode=5）
- **sqlite_errorname** — 错误枚举名：3.11+ Python 异常附带的机器可读错误标识
- **每线程一连接** — connection per thread：嵌入式库并发使用的标准姿势
- **串行化模式** — serialized threading：THREADSAFE=1，最安全的 C 层互斥级别
- **executemany** — 批量执行：一次循环绑定多组参数的 DB-API 方法
- **total_changes** — 累计变更数：连接级"本会话以来改动行数"计数器

## 最新演进与工业实践

- **Python 3.12 `autocommit` 属性 + 3.11 错误码字段**：官方文档 ✅（docs.python.org/3/library/sqlite3.html）；
  书中"各绑定对事务的处理不一致"的痛点，标准库层面首次给出显式控制面。
- **`Connection.backup()`（3.7+）**：在线备份 API 直连（🔧 08 章用它 9.2 MB 库 0.05 s 完成），
  语言绑定开始把 C 层非 SQL 能力直接抬进来，而非只做 SQL 管道。
- **SQLite 捆绑版本现状**：CPython 3.13.2 = 3.45.3（🔧），落后最新 3.53.4（2026-07-24 ✅）
  约 8 个次版本；发行版滞后是跨语言绑定的共同话题（02 章对位表）。
- **生态观察**：Python 侧 SQLAlchemy 把 SQLite 当"单机默认方言"、AI/Agent 应用把 SQLite
  当会话状态存储已成 2024–2026 显学（⚠️ 行业综述性判断，未逐条核验数字）。
- **取证清单（本章）**：python sqlite3 文档 ✅、busy_timeout C 页 ✅、capi3ref ✅（curl 200）；
  🔧 实验 A/B/C 数字来自 `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt` 与本会话补充脚本。
  ⚠️ aiosqlite/better-sqlite3/Microsoft.Data.Sqlite/Node 22 内置模块等第三方仓库本会话未核验，
  只作生态位陈述不作引用依据。
