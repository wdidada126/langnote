# 03 · 命令行 Shell 的配置与使用 ⚠️ 章号推定

> 主题锚定：`sqlite3` CLI 的调用方式、点命令（dot-commands）体系、输出模式、
> 脚本化与数据导入导出。官方依据：[cli.html](https://sqlite.org/cli.html) ✅（curl 200）。
> 🔧 本章实验在**本机 Android platform-tools 的 sqlite3 3.50.6（32 位，clang-22 构建）**上完成，
> 它是本系列可用的"现代 CLI 样本"，与书中 3.8 时代 Shell 对照。

## 1. Shell 是什么：SQL 的"瑞士军刀前台"

```
sqlite3 [选项] 数据库文件 ["SQL或点命令"] ...
```

- 不带文件参数进交互模式；带 SQL 字符串则执行即退出（书中同款）；
- **argv 里混点命令**是后加能力（🔧 3.50.6 实测：`sqlite3 :memory: "PRAGMA journal_mode;" ".version"`
  正常输出两行）——书中年代点命令只能从 stdin/脚本喂，这直接改变了单行管道写法；
- `-batch`（不读 rc 文件）、`-csv`、`-json`、`-readonly`、`--safe`（3.37 起禁副作用点命令，
  [changes.html](https://sqlite.org/changes.html) ✅ 实抓 "--safe command-line option that disables
  dot-commands and SQL statements that might cause side-effects"）等启动开关。

Shell 的定位与书中一致：**不是生产服务组件，而是原型、验证、救火、ETL 小活的界面**。
"先能用 shell 复现，再写进代码"的调试路径在 2026 仍是嵌入式排障第一课。

## 2. 点命令：小写字母支配的"第二语法"

点命令不属于 SQL，是 CLI 自身配置（官方全表 [cli.html](https://sqlite.org/cli.html) ✅）。
书中必讲核心集（3.8 起就有）：

| 命令 | 用途 | 一句话提醒 |
| --- | --- | --- |
| `.help [PATTERN]` | 列表/检索 | 3.50.6 🔧 实测 **61 个**点命令（书中约 30 个量级，⚠️ 凭记忆估） |
| `.schema / .tables / .dump / .restore` | 自省与搬迁 | `.dump` 是"文本化全库"，跨版本迁移的保险绳 |
| `.import --csv FILE TABLE` | CSV 入库 | 3.32 起有 `--csv/--ascii/--skip`（changes.html ✅ 原文实证） |
| `.mode list\|csv\|column\|html\|insert` | 输出格式 | 3.33.0（2020-08-14）新增 "box"、"json"、"markdown"、"table" 四种输出模式（changes.html ✅ 原文实证）；🔧 本机 3.50.6 box 正常 |
| `.headers on/off` | 列名开关 | 管道给脚本时永远 off，给人看时永远 on |
| `.output FILE / stdout` | 重定向 | `.output` 走 CLI，不受 shell 引号语法管 |
| `.read FILE` | 执行 SQL 脚本 | 与 `.output` 搭配 = 手工报表流水线 |
| `.timer on` | 逐条计时 | 书中"性能初检"手法，🔧 依旧好用 |
| `.backup FILE` | **在线备份** | 底层即 sqlite3_backup API（08 章实验互证；书中未及，属现代补位） |

**双引号革命（3.32.0，2020-05-22 ✅ changes.html 语境）**：点命令参数支持带空格
路径与转义，书中"点命令参数怎么引"的老问题基本消失。

## 3. 交互体验的现代化（对位书中 readline/编辑行小节）

- 3.50.6 🔧 `--help` 风格输出与彩色 box 表格仍是一身 POSIX 气质；新增
  `.echo`、`.once`、`.csv` 快捷、`-json` 启动模式，把 CLI 变成 JSON 管道节点
  （`sqlite3 -json app.db 'select ...' | jq ...`）——**2026 年 CLI 的新身份是"JSON 数据前端"**，
  书中只会 `| sed` 的年代没有这条路。
- `.param init` 🔧 实测：把 SQL 里的 `:x` 绑定成 shell 变量（`.param set :x 7; SELECT :x;` → 7），
  写多语句脚本不再需要 sed 拼串。

## 4. 🔧 实测（本会话，sqlite3 3.50.6，Windows）

### 实验 A：CSV 批量入库 + 查询（ETL 小活全链路）

方法：Python 造 200,000 行 CSV（id,city,pop，5 城市随机）；
`sqlite3 cli.db ".import --csv cli_data.csv t"`；`.mode box` 聚合查询。

结果：
- 导入耗时 **372 ms**（单进程 CLI、默认回滚日志模式、无索引；⚠️ 其内部事务批处理
  策略未在本会话核验，仅以结果计时为准）；
- 库文件 **5,713,920 B**（约 5.7 MB，20 万行 ×3 列）；
- 聚合查询 `GROUP BY city ORDER BY n DESC`（表扫全量）在 box 模式下 <1s 返回；
- `.mode insert` 立刻给出 `INSERT INTO "table" VALUES('42','Eburgh','8332830');`
  —— 数据回搬（re-export）一行命令，书中同款用法在 2026 依旧顺手。

对照认知：**"百万行以下别谈导入性能"**——5.7 MB 库、亚秒级全流程，
这是嵌入式 ETL 与"MySQL 需要先建实例"的本质差别。

### 实验 B：现代输出模式 = 人类可读 + 机器可解析双轨

- `.mode box`：Unicode 框线表格（🔧 输出 3 行城市统计，边框对齐）；
- `.mode line`：单行记录竖排（`id = 42` 三行式）；
- `.mode insert`：生成可回放的 INSERT；
- 启动级 `-json`（官方页有述 ✅）：整库查询直接吐 JSON 数组。

### 实验 C：点命令即程序配置

- `.dbconfig`（🔧 列出 `attach_create on / defensive on / dqs_ddl on` 等运行期配置，
  对应 C 库 DBCONFIG 族，见 05 章）——Shell 已能自省**库层**开关，书中只有 pragma；
- `.backup cli_copy.db`：在线备份 5.7 MB 库成功（🔧 产物 5,722,112 B）；
  与 08 章 Python `Connection.backup()` 实验同族 API。

### 实验 D：STRICT 表错误信息带错误码（CLI 现代化彩蛋）

🔧 `INSERT INTO st VALUES('abc')` →
`Error: stepping, cannot store TEXT value in INTEGER column st.x (19)`——
**尾号 (19) = SQLITE_MISMATCH**（[rescode.html](https://sqlite.org/rescode.html) ✅）；
3.8 时代 CLI 只给文字，现在错误码直接可断言（05 章错误码体系的前台呈现）。

## 5. 常见坑（书中"注意"小节的 2026 复述）

1. **引号地狱**：外层 shell 与内层 SQL/点命令两层转义；argv 点命令支持后，
   写 `"SELECT ..."` 外层用单引号包裹是最稳姿势（Windows cmd 例外，⚠️ 平台差异大）。
2. **`.import` 的首行语义随目标而变**：🔧 实测——表不存在时自动建表并把 CSV 首行
   当列名（导入后 `count(*)` 恰为 200,000，不含表头）；表已存在时首行会当数据插入，
   需要 `--skip 1`（3.32+ ✅）或去掉表头。
3. **每个 CLI 调用是一个新进程**：管道里多条语句若跨进程则事务上下文丢失；
   批量场景用 `.read` 或单进程 argv 串。

## 6. 本章带走三条

1. Shell 是嵌入式数据库的"听诊器"：`.schema/.dump/.timer/.dbconfig` 覆盖 90% 的第一现场侦查。
2. CLI 现代化的红利：argv 点命令 + `-json` + `.param` + 错误码尾注，让 sqlite3 成了
   当代脚本管道里最轻的结构化数据前端。
3. `.import`/`.mode insert`/`.backup` 三件套 = 最小 ETL + 最小迁移 + 最小备份，全在一条命令内。

## 核心概念速览（中英对照）

- **点命令** — dot-command：CLI 自有指令，以句点开头，不属于 SQL 标准语法
- **输出模式** — output mode：`.mode` 家族（list/csv/box/table/insert/json/html）
- **批模式** — batch mode：`-batch` 跳过用户 rc 文件，保证脚本可复现
- **只读旗标** — readonly flag：`-readonly`/`--readonly`，防手滑的护栏
- **安全模式** — safe mode：`--safe`（3.37+）禁用有副作用的语句与点命令
- **在线备份命令** — backup dot-command：`.backup` 调 sqlite3_backup 系列 API
- **计时器** — timer：`.timer on` 逐条打印 rusr/sysusr 等四元组
- **导入 CSV** — import：`.import --csv [--skip N] f.tbl table` 自动建表或按列匹配
- **参数绑定（CLI 侧）** — .param：shell 变量映射到 SQL 绑定参数（`:x`）
- **rc 文件** — sqliterc：用户级启动配置（每次连接自动执行）
- **SQL 日志** — echo：`.echo on` 打印即将执行的每条约等价于 -x 调试
- **转储/恢复** — dump/restore：文本 SQL 全库导出（跨格式版本最稳通道）

## 最新演进与工业实践

- **CLI 版本对位**：书 = 3.8 内置 shell；本会话 🔧 = **3.50.6**（2025-09-22，
  `sqlite3 --version` 实抓）；最新 **3.53.4**（2026-07-24 ✅ download.html）。
  十年间点命令从约 30（⚠️ 书中清单未核）到 61（🔧 实测 `.help` 计数）。
- **JSON 一等公民**：3.33.0 新增 "json" 等四种输出模式（[changes.html](https://sqlite.org/changes.html) ✅ 原文实证），
  配合 JSON 内置化（3.38）后 CLI 与 REST/k8s 工具链无缝；工业实践中常见
  "sqlite3 -json 出监控数据 + jq 后处理"的轻量运维脚本模式。
- **`.import` 生态位**：数据科学侧常把 SQLite CLI 当 duckdb 之前的"零安装 csv→sql"跳板；
  与 [#134 DuckDB UAR·02 数据导入](../DuckDB_Up_and_Running/02-数据导入DuckDB.md) 形成对位（波尾已闭环；DuckDB 的 `read_csv` 是同一需求的列存版本，
  可先看 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)）。
- **取证清单（本章）**：cli.html ✅、rescode.html ✅、changes.html ✅（curl 200 实测 2026-09-27）；
  🔧 原始输出存 `D:\develops\tmp\dbwave_usqlite\`（cli.db/cli_out.txt 及会话记录）。
  ⚠️ 书中 3.8 shell 的点命令精确条数与老 .help 文案无法复现，未作数字引用。
