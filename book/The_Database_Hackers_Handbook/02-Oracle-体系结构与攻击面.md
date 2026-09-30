# 02 · Oracle：体系结构与攻击面（原版 Part II / Ch2–5）

> 覆盖中文版目录第 2–5 章（✅ 目录逐字）：Oracle体系结构 / 攻击Oracle /
> Oracle：深入网络 / 保护Oracle。小节为老书降级主题重构 ⚠️；版本基线 Oracle 9i/10g。
> Litchfield 系 Oracle 研究的公开论文与漏洞公告为主要旁证源（⚠️ 转述）。

## 1. Ch2 Oracle 体系结构（安全视角重讲）

正面结构叙述可对照 [00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)
与 [00-总览与阅读地图.md](../Oracle_Performance_Tuning_2e/00-总览与阅读地图.md)；本书只取"哪里能被碰"：

- **进程与内存**：专用/共享服务器模式下服务器进程（shadow process）继承会话权限；
  PGA 中的会话数据若可被同主机低权进程读取，即信息泄露面 ⚠️ 转述。
- **监听器 Listener（TNS，默认 1521）**：独立的 LISTENER 进程，先于数据库认证
  暴露在网络——这是 Oracle 攻击面最独特之处（先打监听，再打库）。
- **数据字典与 SYS/SYSTEM**：`SYS.SYSUSER$`（9i 时代口令哈希所在基表）可读性
  决定离线破解可行性；`ANY` 系系统权限的语义陷阱（如 `SELECT ANY TABLE` 不含字典但
  `SELECT ANY DICTIONARY` 含）。
- **PL/SQL 引擎与编译代码**：存储过程/函数/包以定义者权限（definer's rights）
  默认执行，是本书 Oracle 攻击章的绝对主轴。
- **外部接口**：EXTERNAL TABLES（10g）、Java in Oracle（JVM）、UTL_FILE/UTL_HTTP/
  DBMS_LDAP、外部过程代理 extproc——每一条都是出库通道。

## 2. Ch3 攻击 Oracle（语句与授权模型滥用）

- **口令哈希离线破解**：9i/10g 使用 DES 基一次性哈希且大小写不敏感，
  字典还原极快；11g 才引入 SHA-1 加盐（演进注）。⚠️ 转述自该书体系公开同源材料。
- **默认账户面**：SCOTT/HR/PM/OUTLN/MDSYS/CTXSYS/DBSNMP/ORACLE/ORDPLUGINS…
  数百个随库创建账户，多数版本默认口令或口令即用户名；枚举即入口 ⚠️ 转述。
- **PL/SQL 注入（本书招牌贡献）**：以定义者权限执行的包若动态拼接 SQL，
  低权调用者可把参数"喂"成任意语句——典型如 `AUTHID CURRENT_USER` 缺失的 SYS 包。
  Litchfield 团队 2003–2004 批量报告的多枚 CVE 即此类（⚠️ 未逐号核 CVE ID）。
  与 Web 注入的本质差异：这里的"用户输入"进入了**高权限上下文**，注入即提权。
- **取巧授权面**：`GRANT ANY ROLE`/`GRANT ANY PRIVilege` 被误授给非 DBA 包属主；
  公共同义词（PUBLIC SYNONYM）劫持：攻击者在自身 schema 建同名对象+公共同义词歧义，
  诱导高权过程执行攻击者代码（与 SQL Server 的 dbo 公用角色滥用同型，见 `05` 章）。
- **extproc 滥用**：外部过程调用经由监听器派生子进程，早期默认配置下
  `tnsnames` 指向的攻击者可控库可实现主机命令执行 ⚠️ 转述。

## 3. Ch4 Oracle：深入网络（协议层）

- **TNS 协议画像**：明文；支持版本/服务/环境（OSENV）字段协商——握手即泄露
  版本与主机环境，为指纹与针对型利用供给情报。
- **监听器未认证操作**：旧版 `SET PASSWORD` 缺省即无口令监听，远程可
  `SET CURRENT_LOG_DIRECTORY`、注册伪造服务、查询状态（tnsping/lsnrctl 与
  手工 TNS 报文等效）；"监听器即无认证 RPC 面"是本章论断 ⚠️ 转述。
- **TNS 拒绝服务与缓冲溢出史**：监听器解析报文的多起溢出（含 iSQL*Plus、
  Enterprise Manager DB Control 8080/1158 HTTP 口）说明**非 SQL 通道**同样致命。
- **EM/iSQL*Plus Web 层**：DB Control 默认 HTTP、弱口令可直登管理控制台——
  与 [白帽子讲Web安全.md](../白帽子讲Web安全.md) 的"管理后台暴露"议题相连。

## 4. Ch5 保护 Oracle（加固清单重构）

- 监听器：设口令、`ADMIN_RESTRICTIONS_<name>=ON`、只绑内网 IP、关闭未用服务注册。
- 账户：删/锁默认示例账户，口令策略走 PROFILE（复杂度/锁定/有效期）。
- 授权：审计 `DBA_ROLE_PRIVS`/`DBA_SYS_PRIVS` 中 ANY 类权限与 DBA 持有者；
  新写包一律 `AUTHID CURRENT_USER` 或严格白名单动态 SQL（绑定变量）。
- 字典与文件：限制对 `SYS` 基表直接 SELECT；UTL_FILE 目录对象白名单化。
- 审计与监控：`audit_trail`、FGA 细粒度审计、登录失败与特权使用告警；
  与波内 #61 [Oracle_Security 总览](../Oracle_Security/00-总览与阅读地图.md)
  （防御端，含[审计体系](../Oracle_Security/05-审计体系与跟踪文件.md)、
  [加密与数据保护](../Oracle_Security/07-加密混淆与数据保护.md)）构成攻防双线。
- 补丁：季度 CPU（Critical Patch Update）机制自 2005-01 起施行——本书出版同年，
  书中"补丁管理是首要防御"的论断由此制度化 ✅ 机制时间线为通识。

## 5. 🔧 类比锚（SQLite，非本书 Oracle 行为）

- **口令哈希可导出性**：⚠️ 无类比——SQLite 库文件本身可整体拷贝，比 9i 字典表
  泄露更彻底（见 [08-SQLite安全实验与跨引擎防御对照.md](08-SQLite安全实验与跨引擎防御对照.md) E3：明文即落盘）。
- **同义词歧义** ↔ SQLite ATTACH 多库命名空间：🔧 E6 实测——不限定名默认先解析
  `main`，但表缺失时**落透**到已挂载库（E6e 取到攻击库行），构成与公共同义词
  同型的"命名空间歧义"最小演示（详见 [08-SQLite安全实验与跨引擎防御对照.md](08-SQLite安全实验与跨引擎防御对照.md)）。
- **最小权限内核编译** ↔ SQLite 默认编译禁用扩展加载（🔧 E4 `not authorized`），
  对应 extproc"默认关"的加固哲学。

## 6. 跨引擎回看（Oracle 议题在他书中的镜像）

| Oracle 议题 | 镜像 |
|---|---|
| 定义者权限注入 | SQL Server 存储过程拼接（`05` 章）、MySQL EVENT/TRIGGER 期权限（⚠️） |
| 监听器未认证 RPC | SQL Server 1434/UDP（`05` 章）、DB2 的 DRDA 端口枚举（`03` 章） |
| 默认账户海 | MySQL 匿名用户（`04` 章）、PG 的 postgres 超级用户与 trust 认证（`06` 章） |
| CPU 季度补丁 | MS 月度 Patch Tuesday 文化圈对照（`05` 章） |

## 7. 本章攻击面速查（按可达性排序）

| # | 攻击面 | 前置条件 | 章节出处 | 书中标级 ⚠️ 推定 |
|---|---|---|---|---|
| 1 | 监听器未认证操作 | 1521 可达+无口令 | Ch4 | 高危·先于一切认证 |
| 2 | 默认账户弱口令 | 服务/SID 可知 | Ch3 | 高危·枚举即得 |
| 3 | SYS 包 PL/SQL 注入 | 任意合法低权账户 | Ch3 | 高危·注入即提权 |
| 4 | 字典表口令哈希导出 | 本地/低权可读面 | Ch3 | 中危·离线破解 |
| 5 | extproc 子进程滥用 | 可注册 tnsnames | Ch3 | 中危·出库一跳 |
| 6 | EM/iSQL*Plus Web 口 | 8080/HTTP 可达 | Ch4 | 中危·管理面暴露 |
| 7 | 公共同义词歧义 | 可建对象+包属主大意 | Ch3 | 低概率高影响 |

## 8. 与姊妹书 The Oracle Hacker's Handbook 的内容分界

- 本书（2005）：Oracle 占 Part II 一章群（Ch2–5），广度优先，TNS/监听器章
  已含原型方法；
- Oracle HH（2007，Litchfield/Heurtel/Minto ✅ Google Books 元数据核到）：
  把 Ch3/Ch4 扩展为全书（审计绕过/连接池滥用/OS 融合攻击深化）；
- 阅读策略：本目录 `02` 读"面"；波内防御深读走 #61
  [Oracle_Security](../Oracle_Security/00-总览与阅读地图.md)（已落盘实链 ✅），
  Oracle HH 谱系本身在系列内暂无专册。

## 核心概念速览（中英对照）

- **监听器** — Oracle Listener/TNS Listener：1521 上先于数据库的未认证网络面
- **TNS 协议** — Transparent Network Substrate：Oracle 私有会话协议，握手即泄露情报
- **定义者权限** — Definer's Rights：PL/SQL 以包属主权限执行的默认模型，注入即提权
- **调用者权限** — Invoker's Rights（AUTHID CURRENT_USER）：对定义者权限陷阱的修复开关
- **公共同义词劫持** — Public Synonym Hijack：命名空间歧义诱导高权代码执行
- **ANY 权限** — SELECT/INSERT/UPDATE ANY TABLE 等：语义宽泛的系统权限雷区
- **extproc** — External Procedure Agent：经监听器派生外部进程的经典出库通道
- **UTL_FILE/UTL_HTTP/DBMS_LDAP** — 内置网络/文件包：库内向外的受控通道与滥用面
- **FGA** — Fine Grained Auditing：Oracle 细粒度审计，防御端核心抓手
- **CPU 补丁** — Critical Patch Update：2005-01 起的季度安全补丁节奏
- **DB Control** — Oracle Enterprise Manager Database Control：默认 HTTP 管理口 ⚠️ 端口号版本相关
- **口令哈希 DES 一次性** — 9i/10g 口令存储形态：可离线字典还原的根因
- **加固清单** — Hardening checklist：账户/权限/监听/审计四位一体的防御重构

## 最新演进与工业实践

- 版本演进：11g（12 位加盐 SHA-1 + 大小写敏感）、12c（统一审计、口令验证函数、
  容器 PDB 隔离）、19c/23ai（角色与最小权限继续收紧）——本书所列多数默认账户/弱哈希
  问题在现版本默认安装中已消除或缓解 ⚠️ 转述，未逐条核版本矩阵。
- 工业实践：生产库监听器仅内网+ADMIN_RESTRICTIONS、口令策略集中化、
  DBA 权限分离（安全管理员/审计员角色）为主流基线；审计产品（Imperva 类）
  与 Oracle Data Safe（云）承接本书"监控"章的诉求。
- PL/SQL 注入的当代形态：绑定变量与 DBMS_ASSERT 白名单进入编码规范；
  SQL 注入检测论文线（如盲注时序信道）可回溯至 Litchfield 此后对时间攻击的公开研究 ⚠️。
- 与 #61 [Oracle_Security](../Oracle_Security/00-总览与阅读地图.md) 双线：
  该书防御体系论（VPD/标签安全/加密）与本章"保护 Oracle"构成互补，实链已挂 ✅。
- 开源近邻：sqlmap 对 Oracle 方言的支持、ociel/tnscmd 类协议工具延续本章攻击面叙事。
