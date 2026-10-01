# 05 Getting Started with SnowSQL（pp.69–87 ✅ Crossref）

> 章定性：工具面专章——命令行客户端 SnowSQL 的安装、连接、脚本化与 PUT/GET，把 04 章的
> SQL 世界接进 shell/CI。章题/页码 ✅ Crossref `_5`；小节 ⚠️ 推定；命令自拟示意；
> 机制 ⚠️ 转述 + ✅ curl-200 URL；本章无独立 🔧（CLI↔REPL 类比在文中明示非实测）。

## 1. 章节定位与叙事线

SnowSQL 是 Java 写的官方 CLI，2019 时点是"脚本化装载/DDL 批执行/无浏览器环境"的默认答案。
本章叙事：安装（macOS/Linux/Windows 包）→ 连接参数（account/user/私有密钥或密码）→
配置文件 `~/.snowsql/config` 与多连接命名 → 交互 REPL 与点命令 → `-f` 执行 SQL 脚本 / `-q`
静默 / 变量与宏 → `PUT`/`GET` 在本地文件与 stage 间搬运 → 与其它接入方式（JDBC/ODBC/连接器）
的比较收尾 ⚠️ 推定。它承 04（把 COPY 装进夜批 crontab）并启 06（给 Snowpipe 铺 stage 文件）。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 关键物 | 现状锚点（✅ curl-200） |
| --- | --- | --- | --- |
| 1 | 安装与升级 | 平台包/包管理器 | user-guide/snowsql-install-config |
| 2 | 连接与身份 | -a -u -k / config accounts | user-guide/snowsql-config |
| 3 | REPL 与帮助 | `\d`、`!history`、`!quit` | user-guide/snowsql-use |
| 4 | 批执行 | `-f file.sql -v` | user-guide/snowsql |
| 5 | 变量/宏 | `!set`、`&{var}` 插值 | snowsql-use 页 ⚠️ 口径 |
| 6 | PUT/GET | 本地↔内部 stage、压缩并行 | user-guide/snowsql |
| 7 | 输出控制 | CSV/JSON/写文件 | snowsql-use ⚠️ |

## 3. 深读与机制重构

**（a）配置样板（自拟示意，非书中原文）**：

```ini
# ~/.snowsql/config  —— 多环境命名连接
[connections.dev]
accountname = xy12345
username    = etl_svc
dbname      = SALES
warehousename = wh_etl

[connections.prod]
accountname = ab98765
username    = etl_svc
priv_key_path = ~/.ssh/snowflake_rsa
```

```bash
snowsql -c dev -f ./ddl/schema_v12.sql -v            # -v 展开变量回显
snowsql -q -c prod -s "PUT file://./exports/orders_2019_*.csv @mystore auto_compress=true"
snowsql -c prod -f load.sql -D batch=2019-12 -o out.csv  # 变量注入+结果落盘
```

**（b）PUT/GET 的定位**：它们解决"本地文件系统→内部 stage"这一跳（外部 stage 直连 S3 时不需要）；
`auto_compress=true` 顺手 gzip——2019 的装载成本小抄 ⚠️ 转述 ✅
https://docs.snowflake.com/en/user-guide/snowsql。

**（c）脚本化心智**：SnowSQL 的 `!` 命令与变量插值让 DDL 模板化（环境名、批次号），但注意
它是**客户端行为**，服务端只见最终 SQL；这与 07 章任务编排（服务端 TASK）构成"客户侧自动化 vs
平台侧自动化"的分野 ⚠️ 推定。

**（d）接入生态对照（本章收尾语义）**：JDBC/ODBC/Python connector/Kafka connector（06 章）各占
不同位——CLI 占"人+shell"位 ⚠️。工具连接总览在 2026 文档 ✅（Snowsight/连接主题；具体清单
以官方页为准 ⚠️）。

## 4. 🔧 类比实测：REPL 家族对照（SQLite 3.50.6 CLI，系统已装零新装；非 SnowSQL/Snowflake 行为）

`sqlite3` CLI 与 SnowSQL 同属"壳命令 + SQL 双通道"形态；下列为**本地实跑**证据（输出摘要，
实测环境 Git Bash + Android SDK 附带 sqlite3 3.50.6 / python sqlite3 模块 3.45.3）：

```text
sqlite3 demo.db ".read init.sql"      → 建表+插入成功（≈ snowsql -f 批执行）
sqlite3 demo.db ".tables"             → 列出本地目录对象（≈ \d 语义位）
python 中 db.execute(".tables")       → OperationalError: near ".": syntax error
   ——实证"点命令只活在壳通道，不属 SQL 方言本体"，与 SnowSQL ! 命令/元命令边界同型；
     审计侧（QUERY_HISTORY 类账本）只会看到真实 SQL ⚠️ 推论。
差异点：SQLite 无网络跳、无 stage、无凭据——SnowSQL 的 PUT/GET/压缩/重试问题域在此不存在。
```

## 5. 深读问答（自拟）

**Q1：CI 里为什么优先密钥对而非密码？** A：可轮换、可撤销、无交互登录；config 里 priv_key_path
即此姿势 ⚠️（现行最佳实践以官方安全文档为准）。
**Q2：`-f` 脚本失败会怎样？** A：默认逐语句执行、遇错即停并返回非零码 ⚠️ 口径；批装载管道须
自带重试与告警（06/07 章素材）。
**Q3：SnowSQL 与 Web 工作表怎么分工？** A：可审计、可版本化的进 git+CLI；探索性查询进 UI ⚠️。

## 6. 与其他书/章联系

- 前接 04（COPY 的脚本化），后启 06（stage 铺文件）与 07（用户/角色先建好再连）。
- 13 章迁移中"改造存量 SQL 脚本"的技术前提即本章。
- [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：接入层全表参考（波1 ✅）；[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md) ⚠️ 降级册仅辨析（00 §4）。

## 7. 本章检验点

1. 写出多环境命名连接配置并说明 `-c` 的解析顺序。
2. 区分 PUT 的目标类型（内部 stage vs 本地路径误用）。
3. 说出 !set/变量插值与 `USE` 语句两种参数化的差别。
4. 列举至少四种"非 CLI"接入方式及适用位。

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_5`（pp.69–87）；✅ URL（本轮 curl-200）：user-guide/snowsql、
user-guide/snowsql-use、user-guide/snowsql-config、user-guide/snowsql-install-config；
点命令/变量语法细节为 ⚠️ 转述（以官方页现文为准）；§4 为 🔧 本地实测（E8 组，见 00 §6 补注）；
2019 小节顺序 ⚠️ 推定。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 命令行客户端 | SnowSQL (CLI) | 官方 Java CLI，脚本化首选 |
| 命名连接 | named connection | config 文件中一组连接参数 |
| 私有密钥认证 | key-pair auth | 服务账号免密码登录 |
| 点命令/感叹命令 | dot/bang commands | REPL 本地辅助指令族 |
| 变量插值 | variable substitution | !set 与 &{var} 的客户侧模板 |
| PUT/GET | PUT / GET | 本地文件与 stage 双向搬运 |
| 自动压缩 | auto_compress | PUT 顺手 gzip 省传输 |
| 批执行 | -f script mode | 文件即流水线，退出码即信号 |
| 会话仓库 | session warehouse | 连接默认吃哪个仓（03 章） |
| 内部 stage | internal stage | PUT 的落点，仓管存储 |

## 最新演进与工业实践

- **Snowflake CLI（snow CLI）接棒**：2024 起的新一代开源 CLI 承担项目部署/Cortex/SNOWFLAKE
  脚本等新面；SnowSQL 仍在维护但新功能重心转移 ⚠️（本目录未对其 URL 逐一验真，以官方发布
  说明为准）。Git 仓库对象让"SQL 进版本控制"平台原生化 ✅
  https://docs.snowflake.com/en/developer-guide/git/git-overview——本章"CLI+git 目录"土办法的
  官方替代。
- **工作表与 notebooks 扩张**：探索面持续向 Snowsight 集中 ✅（02 章对照卡）；CI 面则出现
  Snowpark Container Services 等新执行位 ⚠️。
- **工业实践**：夜批脚本 2026 的三种形态=托管 TASK（07 章）、外部编排器（Airflow/dagster ⚠️）
  或 SnowSQL 遗留脚本；审计口径统一看 QUERY_HISTORY ✅ account-usage，工具换代之谜在账本
  上不存在 ⚠️ 提示。
- **读本建议**：本章命令族语法以官方三页（snowsql / snowsql-use / snowsql-config ✅）现文为
  唯一权威；书中截图类内容按 2019 史料处理 ⚠️。
