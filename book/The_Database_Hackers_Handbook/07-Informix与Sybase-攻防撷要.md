# 07 · Informix 与 Sybase ASE：攻防撷要（原版 Part IV–V / Ch10–16）

> 覆盖中文版目录第 10–16 章（✅ 目录逐字）：Informix体系结构 / Informix：发现、攻击和防御 /
> 保护Informix / Sybase体系结构 / Sybase：发现、攻击和防御 / Sybase：深入网络 / 保护Sybase。
> 两引擎在本 repo 系列中无正面专册 ⚠️，本章全依该书体系公开同源材料降级重构（⚠️ 转述为主），
> 小节号一律不虚构。版本基线 Informix 9/10、Sybase ASE 12.5/15。

## 1. Ch10–12 Informix 切片

- **体系结构（安全视角）**：实例由 ONCONFIG 定义，运行时以 `ONLISTEN/oninit`
  进程族呈现；默认服务端口 1526（INFORMIXSERVER 注册惯例 ⚠️），
  共享内存段权限与 `$INFORMIXDIR` 写权限是本地攻击面。
- **发现**：环境指纹即目标画像：`INFORMIXDIR`/`INFORMIXSERVER`/`ONCONFIG`
  三变量在主机与网络上双双泄露（banner/配置文件可读），扫描器可无凭证勾勒拓扑。
- **攻击面要点**：
  - 认证依赖连接串明文口令时代早，嗅探=拿凭证 ⚠️；
  - `sysauth`/`sysrolemembers` 目录表与 DBA 角色单轨，对象授权粒度粗（10.x 前）；
  - 外部例程与 BLD（加载例程）通道：向库注册 C 例程即主机代码执行，
    与四引擎"扩展点"总题一致（见 [08-SQLite安全实验与跨引擎防御对照.md](08-SQLite安全实验与跨引擎防御对照.md) 对照表）。
  - 直接 SQL 注入面：SQLAPI/ESQL 字符串拼接同构。
- **防御**：ONCONFIG 权限收敛（600 级）、审计钩子（`auditing` 配置 + 专用告警管道）、
  网络隔离（只允监听机暴露）、补丁（IBM 系 IBM Security Response ⚠️ 制度名转述）。

## 2. Ch13–16 Sybase ASE 切片

- **体系结构（安全视角）**：ASE 单实例多库；接口层默认 5000/TCP（历史惯例 ⚠️）；
  `sa`（system administrator）账户 + 过程执行语言（ISQL/`sqsh` 客户端生态）。
- **Sybase 的"原罪"**：早期安装 `sa` 空口令且无强制策略——本书将其与 SQL Server 2000
  sa 空口令并列为"两大默认裸奔"（⚠️ 转述）。SQL Server 与 Sybase 同源血缘使大量
  议题同构：
  - **扩展存储过程族**（xp_*）：命令执行/注册表/服务控制，与 `05` 章完全同谱系；
  - **角色模型**：srvrole（sysadmin/security/processadmin/diskoperator）+
    库角色，提权链与 SQL Server db_owner→sysadmin 同型；
  - **口令哈希**：sysprocesses/syslogins 可读面（版本相关 ⚠️）供离线破解；
  - **审计**：sp_auditoption 家族（`audit` 表位于 master），书中评价"默认全关"。
- **Ch15 深入网络**：TDS 方言双分支（Sybase TDS 与 MS TDS 分家 ⚠️ 史实概括），
  登录包解析历史溢出、OOB（出带）经由 DNS/HTTP 类存储过程的案例与 `05` 章共享
  同一"扩展点外联"主题。
- **Ch16 保护 ASE**：sa 强口令+改名策略争议、xp_* 删除/禁列、
  模块授权 EXEC ROLE（15.x 的 granular privileges ⚠️ 演进注）、
  审计全开+集中转储、补丁滚动。

## 3. 为什么仍要读这两部（任务未点名引擎的价值）

- 任务硬要求 2 点名 SQL Server/Oracle/MySQL/DB2/PostgreSQL 五引擎；
  Informix/Sybase 为原版实有分部（✅ 目录），不写即目录映射不完整。
- 概念复利：Sybase≈SQL Server 的前史与旁支，读 ASE 的 xp_* 与角色链，
  反能看清 `05` 章议题的血缘；Informix 的"环境指纹"是嵌入式/配置驱动型
  系统攻击面的早期范本——与 SQLite 的"文件即一切"（🔧 E2/E3）同属
  "无网络服务的攻击面"教学组。
- 当代余量：Informix 并入 HCL/IBM 产品线、ASE 在金融存量系统存续 ⚠️ 概括，
  两章的审计与扩展点治理清单仍有迁移价值。

## 4. 🔧 类比锚（SQLite，非本书这两引擎行为）

- **环境指纹泄露** ↔ SQLite **无进程可指纹**：目标情报只剩库文件与页格式，
  🔧 E6d `PRAGMA database_list` 把"我能看到什么"的最小集合直接打印。
- **sa 空口令** ↔ SQLite **无口令**：文件可读即全库可读（🔧 E3a 明文断言 True），
  是"默认裸奔"的极限对照——SQLite 的对策不在库内而在 OS/加密层（🔧 E5a 只读 URI、
  `08` 章加密讨论）。
- **xp_* 禁列加固** ↔ SQLite **编译期裁剪**：不编入即不可用（🔧 E4a not authorized），
  比"装完再关"更彻底。

## 5. 取证缺口声明

- Informix/Sybase 两分部的小节级结构、示例版本号、具体 CVE 对应关系均不可达
  （⚠️ 老书降级）；本章所有技术条目为"该书体系同源论文/公告"级转述，
  不可作为操作手册引用。
- 中文编译本对这 7 章的删节比例未知 ⚠️。

## 6. Sybase ASE ↔ SQL Server 对照表（读 `05` 章后的回收表）

| 议题 | Sybase ASE 形态 | SQL Server 形态（`05` 章） | 共同教训 |
|---|---|---|---|
| 空口令原罪 | sa 默认空口令（早期安装 ⚠️） | 2000 混合认证 sa 弱口令 | 出厂配置即攻击面 |
| 命令执行面 | xp_cmdshell 同族 xp_* | xp_cmdshell/sp_OACreate | 扩展点默认关 |
| 角色提权 | srvrole 四特权角色 | 服务器/库双层角色 | 角色语义审计 |
| 口令哈希 | syslogins 可读面 ⚠️ | 哈希导出案例 | 字典表访问控制 |
| 协议溢出 | 自有 TDS 分支登录包 ⚠️ | MS TDS/1434 双溢出史 | 解析器=隐形门 |
| 审计默认值 | sp_auditoption 全关 ⚠️ | 2000 默认跟踪缺位 | 默认不留痕=合规债 |

## 7. 两分部一页纸摘要（应试/评审两用）

- Informix 三句话：环境指纹即目标画像；认证外包给连接串明文时代；
  扩展点（BLD/C 例程）治理与审计钩子是仅有的两把防御锁。
- Sybase 三句话：与 SQL Server 同源共生，攻防素材可互换复用；
  空 sa 与 xp_* 是"默认裸奔+一键出库"的教科书组合；
  15.x 的细粒度权限/模块授权是书成之后的补救演进 ⚠️。
- 评审提示：若你的存量系统仍含 ASE/Informix，先查"扩展点+空口令+审计开关"
  三件套，再谈高级威胁建模。

## 核心概念速览（中英对照）

- **ONCONFIG/INFORMIXSERVER** — Informix 配置与环境指纹：主机侧目标画像来源
- **BLD/外部例程** — Loadable routines：Informix 的出库执行通道
- **auditing 钩子** — Informix audit hooks：告警管道式早期审计
- **ASE** — Adaptive Server Enterprise：Sybase 旗舰，SQL Server 血缘旁支
- **sa 账户** — System administrator（Sybase）：空口令原罪载体
- **xp_*** — 扩展存储过程族：Sybase/SQL Server 共享的命令执行谱系
- **srvrole** — 服务器角色：sysadmin/security/processadmin 提权面
- **sp_auditoption** — 审计开关族：默认关闭的合规债
- **TDS 方言分家** — TDS fork：Sybase/MS 协议差异与溢出史双轨
- **granular privileges** — 细粒度权限（15.x ⚠️）：模块授权演进注
- **环境指纹** — Environment fingerprinting：无凭证情报收集总称
- **编译期裁剪** — Compile-time trimming：SQLite 式彻底加固范式（🔧 类比）
- **同源血缘** — Shared lineage：Sybase/SQL Server 攻防素材可互换的谱系原因
- **默认裸奔** — Insecure defaults：空 sa/弱 sa 与扩展点全开的出厂状态合称
- **三件套评审** — Extension-point/empty-password/audit-switch triage：
  存量 ASE/Informix 系统的最小安全检查集

## 最新演进与工业实践

- 谱系终局：Sybase ASE 历经 SAP 收购（2010）更名 SAP ASE，补丁与
  SAP Security Notes 体系接续书中"滚动补丁"建议；Informix 转售 HCL（2017），
  版本号 HCL Informix 14 ⚠️ 概括。两者均已退出主流安全研究视野。
- 教学价值转移：书中"扩展点治理"议题在当代以 SQLite 扩展白名单、PostgreSQL
  扩展供应链安全、SQL Server 功能开关等新形态延续（分见 `06`/`05`/`08` 章）。
- 开源近邻：sqsh（Sybase 客户端遗产）、isql/odbc 通用面；研究侧 ASE/Informix
  漏洞公告存档于各厂商 PSIRT，引用须逐条回核（⚠️ 本目录未代核）。
- 与系列的关系：本 repo 无 ASE/Informix 正面册，本章即系列内唯一切片；
  数据库系列索引见 [数据库系列·总索引.md](../数据库系列·总索引.md)。
