# 05 · 编译与使用 SQLite 库（Compiling and Using the SQLite Library）⚠️ 章号推定

> 主题锚定：把 SQLite 当 C 库嵌进程序——open/prepare/step/finalize 主循环、绑定与列取、
> 错误码体系、资源与内存管理、运行期配置。官方依据：
> [capi3ref.html](https://sqlite.org/capi3ref.html) ✅、
> [rescode.html](https://sqlite.org/rescode.html) ✅、
> [c3ref/changes.html](https://sqlite.org/c3ref/changes.html) ✅（均 curl 200）。
> 🔧 本会话不编译 C（零安装纪律），改用"语义探针"：所有 C API 结论以 Python 绑定
> 与 CLI 3.50.6 的等价行为实测呈现，并明确标注哪些是转述。

## 1. 主循环：prepare_v2 是全书最重要的一句

```c
sqlite3 *db;  sqlite3_open("app.db", &db);          // 或 open_v2 + flags
sqlite3_stmt *st;
sqlite3_prepare_v2(db, "SELECT id, name FROM t WHERE id=?", -1, &st, NULL);
sqlite3_bind_int(st, 1, 42);
while (sqlite3_step(st) == SQLITE_ROW)
    printf("%d %s\n", sqlite3_column_int(st, 0), sqlite3_column_text(st, 1));
sqlite3_finalize(st);
```

- `prepare_v2`（取代老式 `prepare`）把**执行失败也交给 SQL 层报告**（老 API 会把
  模式变更伪造成 SQLITE_SCHEMA 错误码地狱）——书中专段警告过的坑，2026 新代码
  已无理由踩（官方三件套：prepare_v2 / step / finalize，[capi3ref](https://sqlite.org/capi3ref.html) ✅）。
- `sqlite3_exec()` 是"只要结果不要行"的便捷壳；回调式 `get_table()` 是更老的糖。
- 绑定参数索引从 **1** 开始；列索引从 **0** 开始——书中吐槽过的不对称，API 冻结永不改。

## 2. 错误码：返回码 + 扩展码两层

[rescode.html](https://sqlite.org/rescode.html) ✅ 要点：

| 码 | 名 | 语义（对应🔧观察） |
| --- | --- | --- |
| 0 | SQLITE_OK | 成功 |
| 100 | SQLITE_ROW | step 出了一行（不是错误） |
| 101 | SQLITE_DONE | step 无更多行 |
| 5 | SQLITE_BUSY | 锁被占，**可重试**（🔧 Python `e.sqlite_errorcode==5` 实测） |
| 6 | SQLITE_LOCKED | 同连接内表级冲突 |
| 8 | SQLITE_READONLY | 只读访问被写 |
| 19 | SQLITE_MISMATCH | STRICT 表类型不符（🔧 CLI 报错尾注 `(19)` 实测） |
| 1 | SQLITE_ERROR | 一般错误/语法（🔧 实测 errorname='SQLITE_ERROR'） |

- 扩展码 `sqlite3_extended_result_codes()` 把 5 拆成 BUSY_SNAPSHOT/BUSY_DEADLOCK 等；
  书中"只判 BUSY 会错过细因"的建议 → 2026 语言绑定直接给 `errorname`（04 章🔧）。

## 3. 运行期配置：dbconfig 与 pragma 的分界

- `sqlite3_db_config()`：DEFENSIVE（禁止改 sqlite_* 内部表）、SQLITE_DBCONFIG_MAINDBNAME、
  ENABLE_LOAD_EXTENSION、TRUSTED_SCHEMA 等**连接级安全/行为开关**；
- 🔧 CLI 3.50.6 `.dbconfig` 输出 `attach_create on / defensive on / dqs_ddl on` 等条目——
  C 层配置面在 shell 可见，是核对嵌入配置的快捷通道。
- 编译期宏（02 章）→ 连接期 dbconfig → 会话期 PRAGMA，三层开关管同一批行为，
  排障顺序也按这三层走。

## 4. 内存与资源：三种 allocator 哲学

书中"malloc 全家桶"三选：内建 slab（可设上限、可测用量）、系统 malloc、自定义
`sqlite3_malloc` 替身；🔧 本机 CPython 构建用 `SYSTEM_MALLOC`（compile_options 可见）。
- `sqlite3_memory_used/highwater`（当未用系统分配器时）给出内存量；
- `PRAGMA cache_size=-KB` 是页缓存的会话级旋钮——**这是 C 库唯一"越大越快"的常规杠杆**。

## 5. 🔧 实测一：cache_size 的页面缓存效应

方法：21.6 MB 库（10 万行 × 约 216 B，表 5,280 页），30,000 次随机主键点查；
分别在 `PRAGMA cache_size=-64`（64 KB ≈ 16 页）、`-8192`（8 MB）下计时；再用小缓存复测。

结果（🔧，同一进程内顺序执行）：

| 次序 | 配置 | 耗时 |
| --- | --- | --- |
| 1 | cache_size=-64 KB（冷，页几乎不复用） | **8.608 s** |
| 2 | cache_size=-8192 KB | **0.995 s**（8.6×） |
| 3 | 再次 -64 KB | **0.940 s** |

解读：**SQLite 不绕过 OS 文件缓存**——第 3 轮小缓存依旧快，因为页缓存在内核 page cache
里；-64 KB 的 8.6 s 是"缓存行 churn + 首读磁盘"的合成成本。对嵌入式选型含义：
容量规划里 SQLite 的工作集 = 页缓存 + OS 缓存两层，基准测试要区分冷/热（呼应
[../Database_Reliability_Engineering/02-容量性能与成本.md](../Database_Reliability_Engineering/02-容量性能与成本.md)
的容量四步法——那里同样用 SQLite 做基线实验）。

## 6. 🔧 实测二：连接、变更计数与 ATTACH

- `changes()`/`total_changes`：单条 `INSERT('y'),('z')` 后 Python `total_changes` 从 1 → 3（🔧），
  对应 `sqlite3_changes()` "最近一条 DML 影响行数"（[c3ref/changes.html](https://sqlite.org/c3ref/changes.html) ✅）；
- `last_insert_rowid()`=1（🔧）；
- ATTACH 至第 11 库报 `too many attached databases - max 10`（🔧，与 compile_options
  `MAX_ATTACHED=10` 对账成功）——C 程序里多租户"一进程多库"的默认天花板就是 10+主库。

## 7. 多文件库组合：ATTACH 的正确姿势与边界

书中 ATTACH 用例（跨文件 JOIN、临时库、归档合并）今天仍常用，但注意：
- ATTACH 后的事务是**单写者跨全部附件**的全局事务——attach 越多，锁面越大；
- 3.53 起 `attach_create/attach_write` 可经 dbconfig 收紧（🔧 CLI 默认 `attach_create on`）；
  ⚠️ 细粒度"只附加只读"要靠 URI 文件名 `?mode=ro` + `-readonly` 组合。

## 8. 本章带走三条

1. 嵌入 = prepare/step/finalize 循环 + 错误码纪律；其余 API 都是这三件套的展开。
2. BUSY 是"设计点"不是"故障"：写重试循环（或信任 busy_timeout），锁语义见 08 章。
3. 页缓存与 OS 缓存双层结构决定性能表象（🔧 8.6 s → 1.0 s 实验）；测试报告里必须写明冷热。

## 核心概念速览（中英对照）

- **预备语句** — prepared statement（sqlite3_stmt*）：编译后的 SQL 执行对象，可反复 step
- **步进** — sqlite3_step：执行一步，返回 SQLITE_ROW / SQLITE_DONE / 错误码
- **终结** — sqlite3_finalize：释放语句对象，退出前必调
- **绑定参数** — bind parameters：`?` 占位符，索引从 1 起，天然免疫 SQL 注入
- **列取值** — column accessors：sqlite3_column_*，索引从 0 起，类型自辨
- **SQLITE_ROW/DONE** — 步进哨兵码：100/101，"非错误的成功"最易误判
- **扩展错误码** — extended result codes：主码 8 位 + 子码，BUSY_* 细分
- **db_config** — 连接级配置：DEFENSIVE/TRUSTED_SCHEMA/ENABLE_LOAD_EXTENSION 等
- **页缓存** — page cache：`cache_size` 控制的 LRU 页缓冲，单位页(负值=KB)
- **slab 分配器** — builtin allocator：sqlite3_malloc 家族，可设上限与高水位
- **ATTACH** — 附加库：把第二文件挂进同一连接命名空间，上限 MAX_ATTACHED
- **URI 文件名** — URI filename：`file:db.sqlite?mode=ro` 打开选项内嵌写法
- **changes()** — 变更计数：最近 DML 影响行数，多语言绑定同名暴露

## 最新演进与工业实践

- **capi3ref 命名冻结**：C API 自 3.x 起承诺稳定（官方入口
  [c3ref/intro.html](https://sqlite.org/c3ref/intro.html) ✅ curl 200 实测）；2026 年仍无任何破坏性
  C API 变更，这是嵌入式供应链长期锁版的基础。
- **TRUSTED_SCHEMA/DEFENSIVE 是安全线新增**（3.26/3.27 时代，⚠️ 具体版本号引自
  [pragma.html](https://sqlite.org/pragma.html) 页内说明而非 changelog 逐条核验）：
  防"恶意库文件借 schema 执行代码"——书中威胁模型在 2026 已有专职开关。
- **Python 绑定把错误码枚举化**（🔧 errorcode/errorname 实测）+ CLI 报错尾注码（🔧 `(19)`），
  "可编程处理 SQLITE_*" 从 C 专属变成全栈能力。
- **与 MySQL 对照**：InnoDB 的连接=线程、错误=errno 表；SQLite 的连接=纯句柄、
  错误=码族且大半可重试——存储引擎视角对读
  [../Understanding_MySQL_Internals/06-基于线程的请求处理.md](../Understanding_MySQL_Internals/06-基于线程的请求处理.md)。
- **取证清单（本章）**：capi3ref.html ✅、rescode.html ✅、c3ref/changes.html ✅、
  c3ref/busy_timeout.html ✅、pragma.html ✅（curl 200，2026-09-27）；
  🔧 实验见 `exp_a_out.txt`（EXP5/EXP5b 段）与本会话 `.dbconfig` CLI 记录。
  ⚠️ C 代码未在本会话实际编译运行（零安装纪律），代码骨架为官方文档转述。
