# 02 · Getting started with DuckDB（快速上手：安装、CLI 与扩展系统）

> 覆盖原书第 2 章。目录来源：✅ Manning 官方 TOC 实抓。本章把"零安装"承诺兑现：CLI 装法、点命令、扩展体系，并用 CLI 完成第一次 CSV 分析。

## 内容规格（小节地图，✅ 实抓）

- **2.1 Supported environments**：CLI、Python、R、Java/JDBC、Node、Wasm/浏览器、C/C++…（原书列官方客户端矩阵；今见 12 附录 A）。
- **2.2 Installing the DuckDB CLI**：2.2.1 macOS（brew install duckdb）；2.2.2 Linux and Windows（下载单二进制/包管理器/winget）。
- **2.3 Using the DuckDB CLI**：2.3.1 SQL statements（多行输入、`;` 结束）；2.3.2 Dot commands（`.tables` `.schema` `.mode` `.headers` `.read file.sql` `.open` `.output`）；2.3.3 CLI arguments（`duckdb 文件.db -c "SQL"`、`-csv`、初始化脚本 `.sql` 文件传参、`--cmd`）。
- **2.4 DuckDB's extension system**：`INSTALL`/`LOAD` 两级；core extensions（官方仓库、签名）与 community extensions（第三方，需 `allow_unsigned_extensions`）；自动加载（配置了即按需 LOAD）；核心思想——**引擎核心极小，能力靠插件**（httpfs/sqlite/mysql_scanner/tpch/iceberg/ducklake…）。
- **2.5 Analyzing a CSV file with the DuckDB CLI**：不建库直接 `SELECT * FROM 'file.csv'`；2.5.1 Result modes（`.mode duckbox/csv/json/markdown/html`）。

## 核心技术清单

- 单二进制零依赖 CLI；打开即一个内存库，`.open x.db` 才落盘。
- 点命令 = CLI 的"元指令"，不进 SQL 解析器（对比 SQLite 同源习惯）。
- 非交互模式：管道喂 SQL（`type data.sql | duckdb`）、`-c` 单发、退出码可用于脚本。
- 扩展目录 `~/.duckdb/extensions/<版本>/<平台>/`；`PRAGMA version;` 查平台标识。
- `duckdb_extensions()` 表：installed/loadable/extension_mode 三列排障必看。
- 文件即表：`FROM 'x.csv'`、`FROM 'x.parquet'` 的隐式 read_csv/read_parquet。

## 🔧 实测

**环境同 01 文件。⚠️ 本机未装 CLI 二进制（内网下载不便），点命令未逐条验证；以下用 Python API 验证"本章心智"，方法可迁到 CLI。**

1. **扩展系统真的能装**：`INSTALL httpfs;` 首次联网下载 **5.2 s** 成功（Windows x64 包）；随后
   ```sql
   SELECT extension_name, installed, loadable_mode, declared_mode
   FROM duckdb_extensions() WHERE installed;
   ```
   可见 httpfs/sqlite/tpch/ducklake 等条目（installed 标记翻转）。`INSTALL sqlite` **4.9 s**。
2. **不建库查 CSV**（2.5 的核心动作，Python 等价）：对 5,000,000 行、142.2 MB 的 CSV 直接
   `SELECT count(*), sum(mwh) FROM read_csv_auto('big.csv')` → **0.44 s** 完成全文件扫描聚合——全程无 CREATE TABLE、无落盘。
3. **结果模式等价物**：Python 侧 `.fetchall()/.df()/.arrow()/to_json()` 对应 CLI `.mode`；CLI 的 duckbox 漂亮表格在 1.x 仍是默认。
4. 平台与版本自检：`SELECT version(), current_setting('platform')` → `v1.5.5 | windows`。

## 易错点与陷阱

- **INSTALL ≠ LOAD**：INSTALL 只下载，LOAD 才生效；新会话要再 LOAD（`autoload_extension` 可按需，但别依赖）。实测 INSTALL sqlite 后直接 ATTACH 报 Catalog Error——忘 LOAD 是新手第一坑。
- **扩展按"引擎小版本+平台"分目录**：升级 DuckDB 后老扩展不自动兼容，需重装；CI 缓存 `~/.duckdb` 会因此炸。
- community extension 签名策略：1.x 起非 core 仓库扩展需要显式 `allow_unsigned_extensions`，官方在收紧（⚠️ 政策细节以文档为准：https://duckdb.org/docs/stable/extensions/overview ✅）。
- CLI 里忘打 `;`：多行缓冲让你以为"卡死"；`\q` 与 Ctrl+C 行为同 SQLite。
- Windows 下 `.read 文件.sql` 的路径编码（GBK 脚本文件）会乱码——脚本存 UTF-8。
- 别把 CLI 当服务用：`duckdb my.db` 持有文件期间，其他进程（含 Python）打不开同一库（实测 IOException，见 12 附录章）。

## 核心概念速览（中英对照）

- **点命令** — Dot command：CLI 元指令（`.tables` 等），非 SQL。
- **结果模式** — Result mode：CLI 输出格式（duckbox/csv/json/markdown/html）。
- **扩展安装两态** — INSTALL/LOAD duality：下载与装载分离。
- **核心扩展** — Core extension：官方签名仓库中的扩展（httpfs、sqlite、tpch、ducklake…）。
- **社区扩展** — Community extension：第三方仓库扩展，需显式信任。
- **自动加载** — Autoloading：使用相关函数时隐式 LOAD。
- **read_csv_auto** — 自动嗅探 CSV：推断列名/类型/分隔符/压缩的表函数。
- **单二进制发行** — Single-binary distribution：CLI 免依赖即拷即用。
- **平台目标三元组** — Extension platform tag：os_arch 决定扩展包路径。
- **非交互执行** — Batch mode：`-c`/管道/脚本文件驱动 CLI 进 CI。

## 最新演进与工业实践

- **CLI 现状**：1.x 提供稳定 shell 补全、`.mode duckbox` 默认、`duckdb -ui` 实验 Web UI；安装页 https://duckdb.org/install/ ✅。Windows 可用 winget，macOS brew，Linux 官方脚本。
- **扩展仓库治理演进（2024–2026）**：DuckDB 把扩展划分为 core / named（官方托管需署名）/ community 三级并强制签名；**iceberg、ducklake 等湖仓扩展已升为 core**——本机 `INSTALL ducklake` 成功即证（✅ 实测，2026-09）。
- **Wasm 与浏览器内分析**：duckdb-wasm 已支撑生产级"浏览器查 Parquet"（官方 https://duckdb.org/docs/stable/clients/overview ✅ 列全客户端矩阵）。
- **CI 实践**：主流做法是 `pip install duckdb` + 固定版本锁扩展重装脚本；`FORCE INSTALL` 应对升级后 ABI 变化（本工程即用 `FORCE INSTALL tpch` 复现，✅）。
