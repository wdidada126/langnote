# 12 · Appendix A: Client APIs for DuckDB（附录 A：DuckDB 客户端 API）

> 覆盖原书附录 A。目录来源：✅ Manning 官方 TOC 实抓。附录把"进程内"落到工程细节：官方客户端矩阵、**并发一言**、批量导入姿势、以及 Java JDBC 全流程示例。

## 内容规格（小节地图，✅ 实抓）

- **A.1 Officially supported languages**：C/C++、Java(JDBC)、Node、Python、R、Go(C API 绑定)、.NET、Wasm、Swift/Kotlin(社区上升官方)——一个内核（libduckdb）多语言壳。
- **A.2 A word on concurrency**：**进程内多线程并发友好**（一库多连接、并行只读/写事务隔离），**跨进程不行**（数据库目录一次只归一个进程）；多读扩展走"各自开只读副本/文件直查"。
- **A.3 Use cases**：嵌入式分析库的正确姿势（应用自带分析层）。
- **A.4 Importing large amounts of data**：appender/COPY/批量 DataFrame，反对逐行 INSERT。
- **A.5 Using DuckDB from Java via the JDBC Driver**：A.5.1 一般用法（`DriverManager.getConnection("jdbc:duckdb:")`、jar 依赖）；A.5.2 多线程多连接；A.5.3 以 DuckDB 为 Java 的数据处理工具；A.5.4 大批量插入（PreparedStatement.addBatch / appender via C API / Arrow JNI）。
- **A.6 Additional connection options**：`?access_mode=read_only`、`?threads=N`、config dict（Python）等 URL/config 参数。

## 核心技术清单

- libduckdb 共享内核：各语言客户端只是 ABI 封装。
- JDBC 驱动自带原生库（平台 artifact），连接串即配置面。
- 连接模型：一个数据库实例(进程) : N 连接 : M 游标；同进程写并发受 MVCC+锁粒度限制。
- 跨进程互斥：文件锁强制；`read_only` 也不能绕过（实测，见下）。
- 批量通道优先级：`COPY` ≫ `appender`/DataFrame 直灌 ≫ `executemany` 逐行。
- A.6 配置参数：`access_mode`、`threads`、`memory_limit`、`enable_external_access` 等。

## 🔧 实测（并发与导入，数字惊人）

1. **跨进程互斥（A.2 核心论断）**：进程 A 持有 `conc.duckdb`（含写入间隙的 sleep），进程 B 无论读写、即便 `read_only=True` 均 **IOException**：`Cannot open file ... File is already open in python.exe (PID 30924)`——OS 级文件锁，Windows/Linux 一致行为（Linux 未验，⚠️ 推断）。多进程"读扩展"的正确做法：各自打开**只读 Parquet 文件**（实测两进程并读 `big.parquet` 正常）。
2. **A.4 批量导入三档对比**（1.5.5 / Python，100 万行 {INT,VARCHAR,DOUBLE}）：
   - `executemany("INSERT ... VALUES (?,?,?)")` 1M 行：**270 s**（实测，逐行事务/绑定开销的灾难样本）；
   - 注册 DataFrame + `INSERT INTO t BY NAME SELECT * FROM tmp`：**0.13 s**；
   - `con.append("t", df)`：**0.12 s**；
   - CTAS 10M 行落盘（01 章）：3.31 s。→ 逐行 INSERT 与批量路径差 **~2000 倍**。
3. ⚠️ JDBC（A.5）未本机实测（未起 Java 工程；`java` 在本机存在，JDK 依赖 duckdb jarm 未下载）；转述官方文档姿势。
4. 连接参数：`duckdb.connect("bench.duckdb", read_only=True)` ✅；config 字典 `duckdb.connect(config={"threads":4})` 未逐一验（⚠️）。

## 易错点与陷阱

- **"DuckDB 支持并发"的误读**：支持的是**一个进程内**的并发连接；把它当 MySQL 那样"多应用共连一库"是架构级错误——需要共享层时上 MotherDuck（07 章）或 DuckLake 目录（11 章）。
- **Web 框架 worker 模型冲突**：Gunicorn/uWSGI 每 worker 一进程各开库 → 第一个写者赢、其余 IOException（实测锁行为）。解法：预 fork 前只读、或数据改 Parquet、或外部服务化。
- **`executemany` 不是批处理**：名字骗人，仍是逐行执行；Java 侧 `addBatch/executeBatch` 同理只能救网络往返救不了逐行解析（A.5.4 的教训移植）。
- **跨语言类型映射暗坑**：JDBC 的 DECIMAL→BigDecimal、LIST/STRUCT 在 JDBC 无原生映射需转 JSON 字符串（⚠️ 转述，版本敏感）。
- **客户端版本与文件版本**：客户端落后于写入端大版本会拒开库文件——升级要全语言客户端同步。
- `read_only=True` 的库文件仍需**独占**（见实测 1）：设计"多进程共享只读快照"就每人各留一份文件/直接读 Parquet。

## 关键连接选项速查（A.6 主题）

| 选项 | 形态 | 说明 |
| --- | --- | --- |
| 路径 | `duckdb.connect()` / `"x.db"` / `":memory:"` | 内存/文件 |
| `read_only=True` | Python / JDBC `access_mode=read_only` | 仍进程独占（实测） |
| `config={"threads":4,"memory_limit":"8GB"}` | Python | 会话默认值一次配齐 |
| `?access_mode=READ_ONLY` | JDBC URL 参数 | `jdbc:duckdb:path.db?access_mode=READ_ONLY` |
| `enable_external_access=false` | 锁定环境 | 禁扩展/网络（安全基线） |
| `allow_unsigned_extensions` | 信任开关 | 社区扩展前提 |
| `custom_user_agent` | 遥测标注 | 发行版可标记来源 |
| `extension_directory` / `storage_version` | 布局 | 容器镜像缓存策略 |
| 多连接 | `con.cursor()` | 进程内并发载体 |
| 结果出口 | `fetch*`/`df()`/`to_arrow_table()` | 语言而异 |

## 本章实测复现（并发与导入两个硬结论）

```python
# --- A.2 并发：两进程实验（本机真实输出，Windows 11）---
# 进程 A：c = duckdb.connect("conc.duckdb"); ...创建 5M 行后 sleep(3) 再 INSERT
# 进程 B：duckdb.connect("conc.duckdb", read_only=True)
#   -> _duckdb.IOException: Cannot open file "conc.duckdb":
#      另一个程序正在使用此文件，进程无法访问。 File is already open in python.exe (PID 30924)
# 判读：库文件进程级独占；"多进程只读扩展"须改用 Parquet（并读实测正常）。

# --- A.4 导入三档（100 万行 {INT,VARCHAR,DOUBLE}）---
con.executemany("INSERT INTO t VALUES (?,?,?)", rows)   # 1M 行: 270 s  ← 反模式
con.register("tmp", df); con.execute("INSERT INTO t BY NAME SELECT * FROM tmp")  # 0.13 s
con.append("t", df)                                     # 0.12 s（appender 族）
# 比值 ~2000x：任何"逐行 INSERT"评审意见都该引用这组数。
```

⚠️ JDBC（A.5）未本机跑（未下载驱动 jar；`java` 在 PATH）——姿势转述自官方文档入口 ✅ https://duckdb.org/docs/stable/clients/overview 。

## 与其他章/本书的互链

- 并发限制的云解法 → [07-云端DuckDB与MotherDuck.md](07-云端DuckDB与MotherDuck.md)
- 并发限制的应用解法 → [09-构建与部署数据应用.md](09-构建与部署数据应用.md)
- appender/COPY 的规模化样本 → [10-大数据集性能考量.md](10-大数据集性能考量.md)
- 语言无关的 API 心智（Python 篇）→ [06-融入Python生态.md](06-融入Python生态.md)

## 思考题（合上笔记再答）

1. "一个 DuckDB 实例 = 一个进程"，那 Web 多 worker 的三种正确姿势？（worker 只读 Parquet/快照文件、连接池收敛到单进程网关、或干脆上 MotherDuck 共享层）
2. JDBC `addBatch` 能拯救 A.5.4 的插入性能吗？为什么？（不能——仍逐行 SQL 解析/物化；正解是 appender/COPY/Arrow 批量通道，参照 2000× 实测差）
3. 为什么"客户端版本对齐引擎大版本"在 DuckDB 比在 MySQL 更重要？（瘦客户端厚内核，但各语言绑定随 core release 出 wheel/jar，跨大版本文件/ABI 兼容承诺有限——升级要全矩阵同动）

## 2026 视角补注

- 客户端矩阵继续扩张（Go/Rust 经 C API、Swift/Kotlin 上升），官方 overview 页是唯一权威清单 ✅。
- Java 生态把 DuckDB 用作"嵌入式数据加工器"（批处理/数据校验/测试夹具），A.5 整节在 2026 年反而更像"主菜预演"。
- 并发模型没有变化：DuckDB 官方 FAQ 至今维持"进程内并发/跨进程独占"的口径；本目录用 IOException 实测把它钉死为硬约束——引用本文件即可终结团队内争论。

## 客户端矩阵速记（A.1 主题，2026）

| 语言 | 通道 | 批量写入正解 | 并发要点 |
| --- | --- | --- | --- |
| Python | 原生绑定（wheel） | `append(df)`/COPY | 一连接多 cursor |
| Java | JDBC（自含 native） | Arrow/appender via C API | 多线程多连接 OK |
| R | DBI 驱动 | COPY/dbWrite | 单进程为主 |
| Node/C/C++/Go | libduckdb | appender | 同内核约束 |
| Wasm | 浏览器内 | 小数据 INSERT | 无跨进程概念 |

跨语言公约数：**所有客户端共享同一内核、同一把进程级文件锁、同一种批量导入偏好**——A.2 与 A.4 两节是全矩阵的公共地基。

## 核心概念速览（中英对照）

- **瘦客户端/厚内核** — Fat-core architecture：libduckdb 内核 + 各语言薄封装。
- **JDBC 驱动** — DuckDB JDBC driver：自含原生库的 Java 接入层。
- **进程独占** — Process exclusivity：库文件一次仅一进程可开（实测）。
- **连接:游标模型** — Connection/cursor：同实例多连接共享事务与目录。
- **MVCC** — 多版本并发控制：进程内读写不互阻的机制。
- **appender** — 高速行批写接口：绕过 SQL 解析直入行组。
- **批语句** — addBatch/executeBatch：JDBC 批处理，仍逐行物化。
- **access_mode** — 连接配置：read_only / read_write。
- **原生库捆绑** — Bundled native lib：jar/wheel 内带平台二进制。
- **Wasm 客户端** — 浏览器内同内核运行（11 章"去中心化"一环）。

## 最新演进与工业实践

- **客户端矩阵现状（2026）**：官方文档入口 ✅ https://duckdb.org/docs/stable/clients/overview ；R/Swift/Kotlin 等由社区→官方通道持续推进（定性）。
- **JDBC 侧**：驱动发布节奏跟 DuckDB core release 走（GitHub releases ✅ v1.5.5/2026-07-22 含各语言 artifact）；Arrow JDBC 扩展（A.5.4 的 Java 大批量终解）已入官方仓库（⚠️ 未逐项 curl，标转述）。
- **服务端化趋势**：社区出现把 DuckDB 包成 HTTP/SQL 网关（"quack 式"客户端/服务试验）缓解跨进程限制——但官方立场仍是"嵌入式 + 共享存储"（⚠️ 定性判读，以 DuckLake/MotherDuck 为官方路线）。
- **工程守则**：本目录量化结论可直接入团队规范——"DuckDB 导入禁用行级循环；跨进程共享一律走 Parquet/DuckLake/MotherDuck"（依据 = 实测 270 s vs 0.12 s、IOException 复现记录）。
