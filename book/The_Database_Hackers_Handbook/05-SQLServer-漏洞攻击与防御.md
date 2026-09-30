# 05 · SQL Server：漏洞、攻击与防御（原版 Part VII / Ch21–23）

> 覆盖中文版目录第 21–23 章（✅ 目录逐字）：Microsoft SQL Server体系结构 /
> SQL Server：漏洞、攻击和防御 / 保护SQL Server。版本基线 SQL Server 2000/2005。
> 本章素材与 Chris Anley 2001–2004 公开论文高度同源（⚠️ 分章作者归属未官方核验，
> 但其 SQL Server 攻击研究者身份 ✅ 公知）。正面机制回链
> [00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)、[01-体系结构与SQLOS.md](../SQL_Server_2012_Internals/01-体系结构与SQLOS.md)。

## 1. Ch21 SQL Server 体系结构（安全切片）

- **服务形态**：`sqlservr.exe`（1433/TCP 默认）+ `SQLBrowser`（1434/UDP 解析）+
  SQL Agent/SSIS 等兄弟服务；服务账户权限=主机提权天花板（LocalSystem 惯例部署是书中头号批评点）。
- **认证双轨**：Windows 认证与混合认证（sa）；2000 时代 sa 可空口令、
  且弱口令策略使"猜 sa"成为最廉价入口。
- **角色与权限**：服务器角色（sysadmin/securityadmin…）→数据库角色（db_owner/db_accessadmin…）→
  模块签名（EXECUTE AS 为 2005 新物 ⚠️ 演进注）；书中演示"低登录+db_owner=准 sysadmin"
  的多条路径。
- **扩展存储过程面**：`xp_cmdshell`（命令执行）、`sp_OACreate` 系（OLE Automation）、
  `xp_reg*`（注册表）、`sp_makewebtask`（HTTP 出网）——"库转主机"的四件套。
- **TDS 协议**：登录包/查询包结构、加密可选；解析器历史上多个溢出（1434 即其兄弟）。

## 2. Ch22 漏洞与攻击（Anley 模型主干）

- **叠加查询注入（本书最著名贡献之一）**：SQL Server 的批量语句与动态执行使
  `'; shutdown --` 式叠加直接改写控制流；Anley 论文将其系统化为"语境攻击"⚠️ 转述。
- **二级注入（second-order）**：输入入库时安全、出库拼接时爆发——书中以账户名/
  客户名为例，强调"校验点与危险点分离"的架构病。
- **口令哈希与离线破解**：2000 时代哈希可被本地/链接服务器途径导出，案例库成熟。
- **提权路径集**：`sp_addsrvrolemember`（借 db_owner 上下文）、Agent 作业伪装
  （job 以高权跑任意步）、链接服务器横向（Linked Servers 凭证复用）、
  公共服务账户劫持（服务改名/配置权限）。
- **协议层**：MS02-039（1434 解析溢出）→ **SQL Slammer**（2003-01，376 字节报文打穿全球）
  ——本章把"蠕虫只需一个 UDP 端口"作为攻防成本不对称的终极教材。
- **数据外带信道**：错误消息回显、DNS（xp_dirtree 类触发外连）与时间侧信道
  （书中后段与 Litchfield 后续时间攻击研究的接口 ⚠️）。

## 3. Ch23 保护 SQL Server（加固清单重构）

- 安装面：Windows 认证模式优先、sa 强口令且仅审计期启用、命名实例隐藏（`HideInstance`）。
- 服务面：虚拟服务账户低权化（LocalSystem 禁令）、Browser 服务按需、端口白名单。
- 语句面：参数化/存储过程白名单；动态 SQL 的 `QUOTENAME` 纪律；应用错误信息收敛
  （避免哈希/结构回显）。
- 功能面：不用的扩展组件彻底移除（2005 Surface Area Configuration 工具将
  xp_cmdshell/OLE 自动化为可勾选开关 ✅ 制度史实）；`sp_configure 'show advanced options'` 管控。
- 监控面：默认跟踪（2008 才正式化 ⚠️ 演进注）、登录审计、Agent 作业审计、
  Windows 审核联动；补丁与 Slammer 教训=自动更新策略。

## 4. 🔧 类比锚（SQLite，非本书 SQL Server 行为）

- **叠加查询** ↔ 🔧 E1b：Python sqlite3 在 `execute()` 层直接拒多语句
  （ProgrammingError），说明"叠加是否可行"很大程度取决于**驱动/客户端**而非引擎文本；
  SQL Server 的 ODBC/DB-Library 路径则放行批语句——跨引擎差异标本。
- **xp_cmdshell 开关化** ↔ 🔧 E4：SQLite 默认编译 `load_extension` 返回
  not authorized——同为"出厂即关的扩展点"，但 SQLite 是编译期而非配置期开关。
- **服务账户即天板** ↔ SQLite **无守护进程**：嵌入式部署的提权链被整体拆除，
  主机面仅剩文件权限（🔧 E2/E3），与"把攻击面从进程缩小到字节"对照。

## 5. 与系列 SQL Server 笔记的分工

| 议题 | 归谁 |
|---|---|
| 页/索引/统计正面内部 | [00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md) |
| SQLOS/日志恢复 | [01-体系结构与SQLOS.md](../SQL_Server_2012_Internals/01-体系结构与SQLOS.md) |
| 索引性能 | [00-总览与阅读地图.md](../Expert_Performance_Indexing_SQL_Server_2019/00-总览与阅读地图.md) |
| T-SQL 语言 | [Microsoft_SQL_Server_2008技术内幕.md](../Microsoft_SQL_Server_2008技术内幕.md)（辨析：与 #35 不同书，见其 00） |
| 2008→2022 管理演进 | 波内 #35 [SQL_Server_2008_Internals](../SQL_Server_2008_Internals/00-总览与阅读地图.md)、#68 [SQL_Server_Advanced_Troubleshooting](../SQL_Server_Advanced_Troubleshooting/00-总览与阅读地图.md)、#71 [SQL_Server_2022_Administration_Inside_Out](../SQL_Server_2022_Administration_Inside_Out/00-总览与阅读地图.md)（已落盘实链 ✅） |

## 6. Anley 论文 → 本章映射（素材谱系 ⚠️ 对应关系为推定）

| 论文/公开研究（2001–2004） | 本章落点 | 概念沉淀 |
|---|---|---|
| "The SQL Server Hacker's Handbook" 系长文 | Ch22 主干 | 语境攻击总纲 |
| 叠加查询与动态执行滥用 | Ch22 首节 | 注入即控制流改写 |
| 扩展存储过程安全（xp_cmdshell/sp_OA*） | Ch21/Ch23 | 扩展点治理 |
| 提权路径百科（db_owner→sysadmin） | Ch22 | 角色语义漏洞 |
| Slammer 后续分析（1434 蠕虫学） | Ch22 协议层 | 攻击成本不对称 |

## 7. 提权路径速查（书中例型重构 ⚠️ 伪 SQL 示意）

1. `db_owner` 会话内：改密他人高权账户/建作业 → `sysadmin` 面；
2. 拼接动态 SQL：`EXEC('... WHERE name=''' + @in + '''')` → 叠加 `;shutdown--`；
3. 二级注入：注册表/账户名入库（安全）→ 报表拼接出库（引爆）；
4. Agent 代理：低权借作业步骤以包属主身份跑命令；
5. 链接服务器：A 实例凭证复用到 B 实例横移；
6. 服务账户：sqlservr 改名/配置权限 → 主机 SYSTEM 跳板。

> 与 Oracle 的"定义者权限注入"（[02-Oracle-体系结构与攻击面.md](02-Oracle-体系结构与攻击面.md)）同为
> "信任上下文错位"的两个方言实现；SQLite 语境两者皆不存在（🔧 E1b/E4a，
> 见 [08-SQLite安全实验与跨引擎防御对照.md](08-SQLite安全实验与跨引擎防御对照.md)）。

## 核心概念速览（中英对照）

- **叠加查询** — Stacked/Chained queries：注入点携带分号批语句改写控制流
- **二级注入** — Second-order injection：入库安全、出库拼接爆发的延迟引爆型
- **动态 SQL** — Dynamic SQL（EXEC 批）：注入的语句级温床，QUOTENAME 纪律对象
- **xp_cmdshell** — 扩展存储过程命令执行：库转主机头号牌，2005 后开关化
- **OLE Automation** — sp_OACreate 家族：组件库对象创建的另一主机跳板
- **db_owner** — 数据库角色：准 sysadmin 提权路径的起点
- **链接服务器** — Linked Servers：跨实例凭证复用与横向移动面
- **SQL Agent 作业伪装** — Job step takeover：高权调度器滥用
- **1434/SQLBrowser** — 解析服务：Slammer 载体，UDP banner/版本枚举面
- **TDS** — Tabular Data Stream：专有会话协议，溢出史与嗅探面
- **Surface Area Configuration** — 面积配置器（2005）：扩展点勾选式加固雏形
- **语境攻击** — Context attacks（Anley 术语）：跨语境数据/代码信任错位总称 ⚠️ 术语转述
- **HideInstance** — 命名实例隐藏：响应抑制类缓解

## 最新演进与工业实践

- 版本演进：2005（SAC）→2008（策略管理/审计基础）→2017 起 `xp_cmdshell` 默认关、
  SQL Server on Linux 改变服务账户叙事→2022 智能查询处理与治理工具化 ⚠️ 概括；
  Azure SQL 把"监听器/补丁"议题整体云端化（对照 [00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)）。
- Slammer 遗产：蠕虫级数据库攻击成为安全经济学教科书案例（"376 字节打瘫全球"），
  驱动了自动补丁与资产清点合规（PCIDSS 数据库条款 ⚠️ 版本口径）。
- 当代攻击面位移：引擎溢出大幅减少，转向链接/服务账户、备份介质、SSMS/AD 凭证、
  以及注入+ORM 误配；检测端 MS Defender for SQL、Query Store 异常基线承接审计。
- 开源近邻：mssql-cli、Impacket MSSQL 枚举、sqlmap；研究面 Anley 此后转向
  大数据/机器学习安全（Google 任职期论文 ⚠️ 未核链）。
- 阅读建议：本章与 `02` 章对读可见"扩展点治理"（xp_cmdshell/extproc/UDF/外部例程）
  是四引擎共同的头号主机化风险，该主题在 [08-SQLite安全实验与跨引擎防御对照.md](08-SQLite安全实验与跨引擎防御对照.md)
  以 🔧 E4 收束。
