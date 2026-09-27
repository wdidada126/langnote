# 02 · 构建与安装 SQLite（Building and Installing SQLite）⚠️ 章号推定

> 主题锚定：amalgamation 单文件源码、编译选项体系、各 OS/发行版如何"自带 SQLite"。
> 官方依据：[compile.html](https://sqlite.org/compile.html) ✅、
> [testing.html](https://sqlite.org/testing.html) ✅、
> [download.html](https://sqlite.org/download.html) ✅（3.53.4，2026-07-24）。

## 1. Amalgamation：为什么官方只给你一个 .c 文件

从 sqlite.org 下载页拿到的是 **amalgamation**——把上百个 .c 按依赖顺序合成
一个约 8 个数量级行数的 `sqlite3.c`（+ 头文件 `sqlite3.h`）。官方理由：

- 编译更快、优化器可见性更好（单 TU 全量内联）、依赖自包含（除 libm/libdl 外零第三方）；
- 用户"构建 SQLite"实际上只是"带着若干 `-D` 宏编译一个 C 文件"。

书中 3.8 时代的流程（`./configure && make`）在 2026 依旧成立——官方 tarball 仍附
autotools 脚手架；但主流集成路径早已是**把 amalgamation 拷进你的工程**。
质量侧的配套是 tcltest 测试框架与 100% 语句覆盖率要求（[testing.html](https://sqlite.org/testing.html) ✅），
这是"一个 C 文件敢当全球默认数据库"的底气。

## 2. 编译选项：一张控制"发行版人格"的开关面板

SQLite 没有 my.cnf，行为差异全部前移到**编译期宏**（[compile.html](https://sqlite.org/compile.html) ✅）。
关键族群：

| 族群 | 宏 | 效果 |
| --- | --- | --- |
| 功能开关 | `SQLITE_ENABLE_FTS4/FTS5`、`ENABLE_RTREE`、`ENABLE_JSON1`（旧名；3.38 起默认内置，`SQLITE_OMIT_JSON` 可关） | 决定虚拟表/全文检索在不在 |
| 并发/内存 | `THREADSAFE`（0/1/2）、`MALLOC`、`MAX_HEAP_SIZE` | 线程模型与分配器 |
| 默认运行值 | `DEFAULT_PAGE_SIZE`、`DEFAULT_SYNCHRONOUS`、`DEFAULT_CACHE_SIZE`、`DEFAULT_WAL_AUTOCHECKPOINT`、`DEFAULT_WAL_SYNCHRONOUS`（均见 compile.html ✅） | 写进库的"出厂默认" |
| 裁剪 | `SQLITE_OMIT_*`（如 OMIT_AUTOINIT、OMIT_LOAD_EXTENSION） | 嵌入式瘦身 |
| 安全 | `SQLITE_DBCONFIG_DEFAULTS`、`SECURE_DELETE`、`MAX_ATTACHED` | 行为护栏 |

书中场景"编译你自己的 SQLite"在 2026 的典型翻版：**为语言运行时/发行版打包 SQLite**——
每个 Python/PHP/Android/浏览器构建都是一次"选项矩阵"选择。

## 3. 平台安装图（书中按 OS 分节 → 2026 口径）

- **Linux**：发行版自带 libsqlite3；CLI 常需单装 `sqlite3` 包；升级看发行版而非 sqlite.org。
- **macOS**：系统自带一个"被苹果打过补丁的"版本（历史上以 `libsqlite0` 名义锁版本），
  自己 `brew install sqlite` 常不在 PATH——书里"PATH 里有俩 sqlite3"的坑原样存在。
- **Windows**：官方给预编译 zip（exe + dll）；语言运行时各自内置（见下节实测）。
- **Android/iOS**：系统分区内置 sqlite3 CLI 与库（🔧 本会话直接用了 Android platform-tools
  里那颗 3.50.6 的 CLI）；App 端通过各自 API 层（Android `android.database.sqlite`）访问，
  **升级库版本 = 升级 OS/绑定库**，App 无法自带系统那份。
- **源码**：`tarball → configure/make/make install`，或把 amalgamation 丢进构建系统。

## 4. 🔧 实测：同一颗"SQLite"在不同发行里是两个物种

环境：本机 CPython 3.13.2（内置 SQLite **3.45.3**，MSVC 构建）
vs Android platform-tools CLI（SQLite **3.50.6**，clang 构建，32 位）。

### 实验 A：`PRAGMA compile_options` 全量对比

CPython 内置构建列出 **43 项**，节选（🔧 原文输出）：

```
COMPILER=msvc-1942, DEFAULT_PAGE_SIZE=4096, DEFAULT_SYNCHRONOUS=2,
DEFAULT_WAL_AUTOCHECKPOINT=1000, ENABLE_FTS3, ENABLE_FTS4, ENABLE_FTS5,
ENABLE_MATH_FUNCTIONS, ENABLE_RTREE, MUTEX_W32, SYSTEM_MALLOC,
THREADSAFE=1, MAX_ATTACHED=10, MAX_VARIABLE_NUMBER=32766, OMIT_AUTOINIT, TEMP_STORE=1
```

解读：CPython 开了 FTS5/rtree/数学函数（`SQLITE_ENABLE_MATH_FUNCTIONS` 是 3.35+ 的新开关——
发行版跟进速度的样本）；`SYSTEM_MALLOC` + `MUTEX_W32` 说明用 OS 分配器与 Windows 临界区。

而 3.50.6 CLI 上 `PRAGMA compile_options` **返回空**（🔧 实测；`page_size`、`function_list`
等常规 pragma 正常）——Android 构建未记录/未开启该自省项。**同一个 SQL 版本域内的两颗
SQLite，自省能力都不同**；跨发行版排障时"先跑 compile_options"的习惯要加一句"如果它返回空"。

### 实验 B：功能可见性验证（构建选项 → SQL 能力）

- `SELECT name FROM pragma_module_list` → **11 个模块**（含 `fts5`、`fts4`、`rtree`、
  `json_each/json_tree`）（🔧）——ENABLE_* 宏与 OMIT_JSON 的最终落点在此可枚举；
- `SELECT json_extract('{"a":42}','$.a')` → 42（🔧，无需任何加载步骤 = 3.38 内置化的本机验证）；
- `SELECT sqlite_version()` → 3.45.3（Python）vs `--version` → 3.50.6（CLI）：
  **两文件同机共存**，正是本节"PATH 里有几个 sqlite3"的现代版：答案通常不止一个，
  而且版本、选项、甚至是否支持 STRICT 都不同。

### 实验 C：`SQLITE_MAX_ATTACHED=10` 的实锤

方法：Python 循环 `ATTACH DATABASE` 11 个库。
结果：第 **11 个失败**：`too many attached databases - max 10`（🔧），
与 compile_options 里的 `MAX_ATTACHED=10` 完全对应——**编译宏在运行期错误信息里现形**。

## 5. 升级与共存纪律（书中运维视角的延伸）

1. 嵌入式产品里"SQLite 版本"= **你链接的那份**，不是官网站上那份；SBOM 要写实际版本号
   （🔧 `SELECT sqlite_version();` 是唯一可信通道）。
2. 文件格式总体向后兼容（format 3 从未破坏），但**新特性会设版本门**：老版本打不开
   用了新格式/新语法的库（[stricttables.html](https://sqlite.org/stricttables.html) ✅ 明言：
   低版本遇到 STRICT 关键字会拒库）——升级前查
   [changes.html](https://sqlite.org/changes.html) ✅ 的版本门与"向后兼容承诺"。
3. 语言运行时绑定的版本滞后是常态：本机 Python 3.13 = 3.45.3（2024-04 线）比最新
   3.53.4 落后 8 个次版本——对位清单见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 基线总表。

## 6. 本章带走三条

1. "构建 SQLite"在当代更多是"选择一颗别人构建好的 SQLite"——选的是**选项矩阵**，不是源码。
2. compile_options 是发行版指纹；跨环境行为不一致时先 diff 它（🔧 空返回也是信息）。
3. 单机多版本共存是嵌入式世界的常态而非事故，脚本要用显式路径 + `sqlite_version()` 断言。

## 核心概念速览（中英对照）

- **聚合码** — amalgamation：官方发布的单文件 C 源码合并产物（sqlite3.c）
- **编译期选项** — compile-time option：`-DSQLITE_*` 宏，构建期决定行为与功能
- **自省 PRAGMA** — introspection pragma：`compile_options`/`module_list` 等查询自身配置的 PRAGMA
- **TRANSLATION UNIT（TU）** — 编译单元：amalgamation 将全部代码并入单一 TU 以利内联
- **tcltest 框架** — TclTest harness：SQLite 官方测试套件，追求语句级 100% 覆盖
- **功能裁剪** — feature omission：`SQLITE_OMIT_*` 系列宏用于嵌入式瘦身
- **默认值宏** — default value options：`DEFAULT_PAGE_SIZE` 等"出厂默认"
- **线程安全级别** — threadsafe mode：`THREADSAFE` 0 非安全/1 串行化/2 多线程
- **系统分配器** — system malloc：`SQLITE_SYSTEM_MALLOC`，用 libc 分配替代内建 slab
- **发行版滞后** — bundled version lag：语言/OS 自带 SQLite 落后官方版本的现象
- **SBOM 版本断言** — version assertion：以 `sqlite_version()` 为准记录实际依赖版本
- **ATTACH 上限** — max attached：`SQLITE_MAX_ATTACHED`，默认 10（🔧 实测撞墙点）
- **版本门** — version gate：新库特性（如 STRICT）使旧引擎拒开新库的兼容机制

## 最新演进与工业实践

- **3.53.4（2026-07-24）为当前发布**：[download.html](https://sqlite.org/download.html)、
  [releaselog/3_53_4.html](https://sqlite.org/releaselog/3_53_4.html) 均实抓 200 ✅；
  发布节奏保持"季度级"，changelog 2026 年多条修复注明"来自 AIs 的问题报告"（changes.html ✅ 原文
  "mostly coming from AIs"）——AI 时代上游质量工程的直读样本。
- **构建即供应链**：Android（AOSP `external/sqlite`）、Chromium、Firefox、Python（PEP 依赖链）、
  PHP 均各自捆绑源码构建；工业实践上主流做法是把 sqlite.org tarball 进私有制品库并固化
  compile_options 基线（🔧 本章实验 A 即"指纹对比法"）。
- **JSON1 内置化改写依赖表**：3.38.0（2022-02-22）起 JSON 函数默认在核心
  （[json1.html](https://sqlite.org/json1.html) ✅），书中"要不要编译 JSON1"的问题
  变成"要不要 `-DSQLITE_OMIT_JSON` 裁掉它"。
- **`SQLITE_ENABLE_MATH_FUNCTIONS`**（3.35.0 起；🔧 本机 CPython 已开）补上了书中
  "只有 5 个内置数学函数"的短板对位。
- **取证清单（本章）**：compile.html ✅、testing.html ✅、download.html ✅、changes.html ✅、
  releaselog/3_53_4.html ✅（curl 200，2026-09-27）；🔧 实验脚本
  `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt`（EXP2/EXP5b 段）。
  ⚠️ size.html 已 404（实测），历史体积数字不作为依据；书中 configure 步骤细节按官方
  build 文档口径转述。
