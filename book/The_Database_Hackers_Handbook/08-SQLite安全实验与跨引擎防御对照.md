# 08 · SQLite 安全实验与跨引擎防御对照（🔧 扩展章·非本书内容）

> **声明**：本书（2005 原版）不覆盖 SQLite。本章依波 7 共通规范以本机可跑的
> SQLite 做注入/权限/加密类比实验（🔧 实测 ≥4 组），全部结论**标非本书多引擎行为**，
> 仅用于把 `01`–`07` 章的攻击面/防御概念落到可复现的最小标本。
> 环境：Python 3.13.2 / sqlite3 库 3.45.3 / win32；临时脚本在
> `D:\develops\tmp\dbwave_w7_dbhack\`（repo 内零构建产物）。

## 1. 实验总表（全部 🔧 实测，输出逐字）

| 组 | 主题 | 关键断言/输出（实测逐字） |
|---|---|---|
| E1 | 注入 | E1a 拼接注入外带全表；E1b 叠加语句被驱动拒绝；E1c 参数化归零 |
| E2 | 权限 | E2a 库文件模式即权限边界；E2b 平台注记：无服务端账户概念 |
| E3 | 加密 | E3a 明文断言 True：库文件字节含敏感串；E3b 标准发行无静态加密 |
| E4 | 扩展点 | E4a load_extension → OperationalError: not authorized；E4b 编译选项全可读 |
| E5 | URI 访问控制 | mode=ro 写入被拒：attempt to write a readonly database |
| E6 | 命名空间 | ATTACH 后 main 优先解析（E6c）；表缺失落透到挂载库（E6e） |

## 2. E1 注入组（呼应 `04`/`05` 章语句级攻击主线）

```python
rows = c.execute("SELECT * FROM users WHERE name='%s'" % "bob' OR '1'='1").fetchall()
```
- 🔧 E1a 输出：`[(1, 'alice', 'pw1'), (2, 'bob', 'pw2'), (3, 'carol', 'pw3')]`
  ——一条布尔恒等式把单行查询变成全表外带，与本书"注入即整库暴露"论断同构。
- 🔧 E1b 输出：`ProgrammingError : You can only execute one statement at a time.`
  ——Python sqlite3 驱动层拒绝分号叠加。⚠️ 注意：这是**客户端行为**而非引擎文本层
  禁止；SQL Server/PG（libpq）路径放行叠加（见 [05-SQLServer-漏洞攻击与防御.md](05-SQLServer-漏洞攻击与防御.md)、
  [06-PostgreSQL-发现攻击与保护.md](06-PostgreSQL-发现攻击与保护.md)），"叠加可行性取决于驱动"是本组核心结论。
- 🔧 E1c 输出：`[]`——参数化绑定把同一 payload 当纯字符串匹配，零行返回。
- **非本书行为标注**：SQLite 无网络监听器/无 FILE 语句，MySQL 式"注入→OUTFILE→
  webshell"链（`04` 章）与 SQL Server 式"注入→xp_cmdshell"链（`05` 章）在此
  **不存在**；注入后的爆点只剩数据本身。

## 3. E2/E5 权限组（呼应"认证外包"主线）

- 🔧 E2a 输出：`True 0o666`——库文件创建后权限位由 OS 决定（Windows 上 0o666 为
  名义值，实际由 ACL/所有权承担）；SQLite **库内无 per-user 账户/口令概念**，
  任何能读该文件者即拥有全库读权。这是本书反复讨论的"认证层"在嵌入式形态下的
  整体缺席。
- 🔧 E2b 输出：`os.name = 'nt'` 注记——无服务进程、无服务账户，SQL Server
  "LocalSystem 天板"议题（`05` 章）与 DB2 实例组议题（`03` 章）均无对应物；
  信任边界=文件系统边界。
- 🔧 E5a 输出：`OperationalError : attempt to write a readonly database`
  ——`file:...?mode=ro` URI 参数（✅ 官方文档 https://www.sqlite.org/uri.html
  本会话实抓，mode/immutable/cache 参数表）实现"连接级最小权限"，相当于
  PG pg_hba 的单机微缩版（`06` 章类比锚）。
- **非本书行为标注**：以上权限模型与书中七引擎的账户/角色体系不可互换，
  仅作文档化类比。

## 4. E3 加密组（呼应各章"保护"节的静态数据议题）

- 🔧 E3a 输出：`raw file contains secret: True size: 8192`——插入
  `4111-1111-1111-1111` 后直接对库文件字节做成员断言命中：标准 SQLite
  **无任何静态加密（at-rest/TDE）**，页明文落盘。
- 🔧 E3b 环境注记：`sqlite_version_info = (3, 45, 3)`，官方加密途径只有两条——
  商业 SQLite Encrypted DB 扩展，或第三方 SQLCipher
  （✅ https://www.zetetic.net/sqlcipher/ 本会话实抓可达：开源 AES-256 全库加密）。
- 对照书中引擎：Oracle TDE/SQL Server 2019+ TDE/DB2 加密库均为后来物 ⚠️，
  本书时代该议题以"文件权限+审计"为主防线——E3a 证明该防线对"整文件拷贝"
  场景完全失效，反讽式印证了本书"防御要假设边界已被突破"的总纲。
- **非本书行为标注**：原版无 SQLite 章，本组不映射任何章号，仅补系列空白。

## 5. E4 扩展点组（全书"扩展点治理"总题的最小标本）

- 🔧 E4a 输出：`OperationalError : not authorized`——默认发行未启用扩展加载，
  SQL 层 `load_extension()` 直接拒绝；需宿主代码显式开启
  （✅ https://www.sqlite.org/c3ref/enable_load_extension.html 本会话实抓：
  默认 off，官方并推荐 `SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION` 细粒度配置，
  只放 C-API 而继续封 SQL 入口，明确以防注入面开启为风险场景）。
- 🔧 E4b 输出：`PRAGMA compile_options` 返回 `COMPILER=msvc-1942`、
  `DEFAULT_PAGE_SIZE=4096` 等——运行时配置全量可读（"监控即情报"面，
  `03` 章 DB2 快照类比锚）。
- 跨引擎收束：Oracle extproc（`02`）、DB2 外部例程（`03`）、MySQL UDF（`04`）、
  SQL Server xp_cmdshell（`05`）、PG untrusted PL（`06`）——五引擎"出库通道"
  的共性防御是"默认关+白名单开"；SQLite 把它做到了极致：**编译/宿主层默认关**，
  连配置开关都不给 SQL 会话。

## 6. E6 ATTACH 命名空间组（呼应 `02` 章同义词劫持）

- 🔧 E6a/E6b：两库各有同名表 `cfg`，分别返回 `('role','admin')` 与
  `('role','attacker-planted')`。
- 🔧 E6c：不限定名 `SELECT * FROM cfg` 解析到 `main`（默认搜索序）。
- 🔧 E6e：**表缺失时落透**——`only_in_attach` 未限定查询命中挂载库行
  `[(999,)]`：应用若假设"该表只存在于主库"，即被挂载对象污染逻辑——
  Oracle 公共同义词歧义（[02-Oracle-体系结构与攻击面.md](02-Oracle-体系结构与攻击面.md)）的单机微缩标本。
- 🔧 E6d：`PRAGMA database_list` 打印挂载全集——枚举面自查工具。

## 7. 五引擎防御对照表（本书各"保护"章收拢为一页）

| 防御层 | Oracle（`02`） | DB2（`03`） | MySQL（`04`） | SQL Server（`05`） | PG（`06`） | SQLite 🔧（类比列·非本书） |
|---|---|---|---|---|---|---|
| 认证/入口 | 监听器口令+PROFILE | 禁 OS 信任映射 | 撤匿名/root 远程 | Windows 认证优先 | pg_hba 方法收紧 | 无——OS 文件权限/E5a URI ro |
| 授权最小化 | 撤 ANY 权限/DBA | DB2ADMNS 收窄 | 库表级授 | 角色分层+EXECUTE AS | rolsuper 审慎 | 无库内角色/E2a |
| 扩展点治理 | extproc 白名单 | 外部例程禁建 | UDF 禁+撤 FILE | xp_* 开关化 | untrusted PL 不装 | E4a 编译期默认拒 |
| 语句纪律 | AUTHID/绑定变量 | 动态 SQL 白名单 | 预编译默认 | QUOTENAME/参数化 | 参数化/PQexec 慎叠 | E1c 参数化 |
| 静态数据 | TDE（后补 ⚠️） | 加密库（后补 ⚠️） | 表空间加密（后补 ⚠️） | TDE 2019+（⚠️） | 磁盘加密惯例 | E3a 无——SQLCipher 补 |
| 审计监控 | FGA/统一审计 | db2audit | 企业审计/query log | 默认跟踪/审计 | log_statement/pgAudit | 应用层日志（无库内） |

## 8. 波内安全双线登记（#51 ↔ #61）

- 本目录=双线之"攻"（find→exploit→harden 的引擎切片）；
  [Oracle_Security 总览](../Oracle_Security/00-总览与阅读地图.md)（波内 #61）=双线之"防"
  （体系化防御：VPD/审计/TDE 治理）。
- 写前 ls/Glob 验盘时未落盘，本会话后段复验**已落盘**，实链已挂：防御端加密章
  [07-加密混淆与数据保护](../Oracle_Security/07-加密混淆与数据保护.md) 正好对位
  本章 🔧 E3（SQLite 无静态加密）与 SQLCipher 补位路径；审计端
  [05-审计体系与跟踪文件](../Oracle_Security/05-审计体系与跟踪文件.md) 对位
  第 7 节对照表"审计监控"行。

## 核心概念速览（中英对照）

- **拼接注入** — String-concatenation injection：🔧 E1a 全表外带的成因
- **参数化查询** — Parameterized query：🔧 E1c 归零效果，业界第一对策
- **驱动层拒叠** — Driver-level statement restriction：🔧 E1b ProgrammingError
- **信任边界=文件边界** — Filesystem trust boundary：🔧 E2a SQLite 权限本质
- **URI mode=ro** — 只读连接参数：🔧 E5a 连接级最小权限
- **静态加密缺位** — No at-rest encryption：🔧 E3a 明文落盘实证
- **SQLCipher** — AES-256 全库加密扩展：🔧 E3b 官方路径之外的开源补位
- **编译期最小攻击面** — Compile-time least attack surface：🔧 E4a 扩展默认拒
- **ATTACH 落透** — Attached-DB name fallthrough：🔧 E6e 命名空间歧义微缩标本
- **扩展点治理** — Extension-point governance：五引擎+SQLite 的共同防御总题
- **防御对照表** — Cross-engine hardening matrix：本章第 7 节的一页化收拢
- **安全双线** — Security double track：#51 攻 × #61 防的波内结构

## 最新演进与工业实践

- SQLite 侧（✅ 本会话实抓官方文档两页）：uri.html（3.7.7 引入 URI 参数、
  immutable/nolock/vfs 参数表）与 SQLCipher（zetetic.net，AES-256）构成本章
  实验的现行权威依据；2020s 移动端/IoT/边缘场景使"SQLite 即攻击面"叙事
  兴起（App 逆向取库、浏览器 SQLite 组件 CVE），原书时代无此维度。
- 应用注入防线演进：预编译为各 ORM 默认 → MyBatis `${}` 误用仍年年上榜，
  中文语境续读 [白帽子讲Web安全.md](../白帽子讲Web安全.md)；污点检测/语义等价检测论文经
  [db.md](../../db/db.md) 论文线索取。
- 云与托管时代：七引擎的"监听器/补丁/服务账户"层被平台接管，防御重心
  位移到 IAM/凭证/数据分级，对照 [00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)
  与 [数据安全架构设计与实战.md](../数据安全架构设计与实战.md)。
- 开源与代码仓库：sqlmap（注入自动化）、pgAudit、SQLCipher、SQLite 源码树
  （sqlite.org 发布）为延续本章实验的最小工具集；本书纸质版 2005 后再无
  勘误更新（无第二版），引用务必用"最新演进"各节校准 ⚠️ 判断性陈述。
- 与波内兄弟：#61 [Oracle_Security](../Oracle_Security/00-总览与阅读地图.md) 已落盘、
  双线对照表（攻 8 章 × 防 N 章）实链已挂，波尾在总索引统一登记。
