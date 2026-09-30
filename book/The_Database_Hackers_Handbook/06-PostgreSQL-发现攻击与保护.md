# 06 · PostgreSQL：发现、攻击与保护（原版 Part VIII / Ch24–26 + 附录 A–C）

> 覆盖中文版目录第 24–26 章（✅ 目录逐字）：PostgreSQL体系结构 / PostgreSQL：发现与攻击 /
> 保护PostgreSQL。版本基线 PostgreSQL 8.0/8.1 时代；小节为主题重构 ⚠️。
> 附录 A–C 章题未核到 ⚠️（推测为工具/参考类），本文件以"附录观感"节做降级处理。
> 正面知识回链 [02-用户与连接管理.md](../Learn_PostgreSQL_2e/02-用户与连接管理.md)、
> [03-安全与权限.md](../PostgreSQL_16_Administration_Cookbook/03-安全与权限.md)。

## 1. Ch24 PostgreSQL 体系结构（安全切片）

- **多进程模型**：postmaster 派生 backend，每连接一进程；权限上下文=OS 用户
  `postgres` 加后端能力，无 SQL Server 式"服务账户天板"议题，但共享内存/段
  权限是主机本地面 ⚠️ 转述。
- **认证在库外**：`pg_hba.conf` 决定 host/user/db/method（trust/md5/crypt/
  password/krb/ident）——书中头号发现：**方法错配**（trust 或 password 明文
  远程放行）比口令强度更致命。
- **角色模型**：8.1 前后从"用户=数据库内 ACL"向 rolsuper/rolcreaterole 等
  属性化角色过渡（⚠️ 版本节点为通识补充）；SUPERUSER 全库单轨，无 MySQL 式
  user@host 多态。
- **目录表可读性**：`pg_shadow` 早期对普通用户可读（口令哈希外泄面），
  8.1 起收紧为仅超级用户（✅ 该修复为 PG 官方史实，⚠️ 具体小节号书中不可核）。
- **网络面**：5432/TCP 默认仅本地（`listen_addresses` 老版本默认不接远程，
  反而是书中"发现"章的难点——先要开到远程才有得打 ⚠️ 版本口径）。

## 2. Ch25 发现与攻击

- **发现**：远程未认证时探测面窄；一旦 `trust`/`password` 暴露，nmap 脚本级
  枚举库/角色即可长驱直入。
- **COPY 通道**：`COPY ... TO/FROM`（早期 server-side 文件读写仅需超级用户，
  `COPY TO/FROM PROGRAM` 为后来物 ⚠️ 演进注）——PG 方言的"FILE 权限"议题，
  对照 [04-MySQL-体系结构与攻防.md](04-MySQL-体系结构与攻防.md) 的 OUTFILE。
- **外部语言出库**：`plperu/plpythonu`（untrusted PL）直接 OS 调用；书中演示
  高权下经 PL 命令执行与读配置（pg_hba/data 目录全路径经 `SHOW` 泄露）。
- **叠加查询**：libpq 的 `PQexec` 允许分号多语句（书中与 SQL Server 叠加
  同列，✅ 该驱动行为为 libpq 史实）——与 🔧 E1b（Python sqlite3 拒叠）形成
  "客户端决定论"的另一极标本。
- **UDF 与 C 语言函数**：`CREATE FUNCTION ... LANGUAGE C` 加载 $PG/lib 下 .so，
  权限校验弱期存在路径注入面 ⚠️ 转述。
- **DoS 面**：autovacuum/锁等待滥用、连接洪水（无默认连接池时代）。

## 3. Ch26 保护 PostgreSQL

- pg_hba 纪律：远程一律 scram/md5+TLS，禁 trust/password 明文；默认
  `listen_addresses=localhost` 保持。
- 角色最小化：撤 createrole/createdb/superuser；按库授权而非全局。
- 语言白名单：不装不用的 untrusted PL；`security_definer` 函数审计（对照
  Oracle 定义者权限，见 [02-Oracle-体系结构与攻击面.md](02-Oracle-体系结构与攻击面.md)）。
- 目录表加固：pg_shadow/pg_auth 可读性核查（8.1 后默认已好 ⚠️）。
- 审计：syslog/logging collector 集中化、log_statement 分级（书中时代
  pGpSQL/审计插件尚幼，现代 pgAudit 承接 ⚠️ 演进注）。
- 补丁与升级窗口：小版本安全发布节奏延续至今（✅ 制度史实）。

## 4. 附录 A–C 观感（降级声明）

- ⚠️ 附录章题未在任何可达源核到；依同年代技术书惯例推测为工具清单/参考书目类，
  本目录不虚构其内容。
- 若后续 O'Reilly 平台可达，应回填附录目录并勘误本文件。

## 5. 🔧 类比锚（SQLite，非本书 PostgreSQL 行为）

- **pg_hba 的"方法错配"** ↔ SQLite 无认证层可言：🔧 E2a 库文件模式 0o666
  （Windows 名义值）说明 SQLite 的"pg_hba"就是文件系统 ACL+URI 参数——
  🔧 E5a `mode=ro` 写被拒（attempt to write a readonly database）是其
  "一行 pg_hba"的最小等价。
- **叠加语句** ↔ 🔧 E1b：libpq 放行 vs sqlite3 拒止，驱动层差异标本对。
- **pg_shadow 可读=哈希外泄** ↔ 🔧 E3a：SQLite 整库明文直读（原始文件含
  `4111-1111-1111-1111` 断言 True），静态加密缺位的极限形态。
- **命名空间歧义**（安全议题跨引擎通用） ↔ 🔧 E6e ATTACH 落透（见 `02` 章）。

## 6. pg_hba 方法风险矩阵（书中语境 ⚠️ 重构）

| 方法 | 口令传输形态 | 网络嗅探风险 | 书中评级 ⚠️ |
|---|---|---|---|
| trust | 无口令 | — | 高危·远程禁用 |
| password | 明文 | 全暴露 | 高危·远程禁用 |
| crypt | DES 截断哈希 | 可重放/破解 | 中危 |
| md5 | 加盐 MD5 | 离线破解成本存在 | 彼时基线（现代 scram 替代） |
| krb5/证书类 | 票据/双向认证 | 低 | 推荐 |

> 现代落地版对照：[03-安全与权限.md](../PostgreSQL_16_Administration_Cookbook/03-安全与权限.md)
> 的 scram-sha-256+TLS 配方即本章的"今天的正确答案"。

## 7. 发现→攻击→防御 三步清单

发现：端口/库/角色枚举（需 hba 允许某种连接）→ `SELECT version()` 指纹 →
`SHOW data_directory` 等配置读取（登录后）。
攻击：错配入口（trust/明文）→ 超级用户会话 → 台阶：
读 `pg_hba`/私钥文件、装 untrusted PL、server-side COPY 读写盘、
C 函数注册（$PG/lib 白名单外 ⚠️）。
防御：hba 收紧+TLS、角色审计（rolsuper/createrole 清单）、
语言与扩展安装管控（现代扩展白名单 `allow_in_place_tablespaces`/loader 类 ⚠️ 演进）、
日志集中（pgAudit 承接）、小版本滚动。

## 核心概念速览（中英对照）

- **pg_hba.conf** — 主机基线认证配置：方法错配即远程裸奔，PG 安全第一开关
- **trust 认证** — 免口令放行：书中列举的最危险默认错配
- **md5/scram** — 口令哈希认证演进：scram 为 9.6 引入（⚠️ 演进注）
- **pg_shadow** — 旧口令目录表：早期普读面，8.1 收紧的标志性修复
- **超级用户单轨** — rolsuper：无 user@host 多态的全库最高权
- **COPY 服务端文件** — server-side COPY：PG 方言的 FILE 权限议题
- **COPY ... PROGRAM** — 命令执行通道：后来版本的显式高危开关（⚠️ 演进注）
- **untrusted PL** — plperu/plpythonu：出库执行 OS 命令的语言级扩展点
- **PQexec 多语句** — libpq 叠加放行：与 sqlite3 拒叠构成驱动层对照
- **security_definer** — SECURITY DEFINER 函数：PG 版定义者权限陷阱与审计对象
- **log_statement** — 语句级日志：审计缺位时代的监控基线
- **listen_addresses** — 远程监听开关：PG 默认本地=书中"先要打得着"前提
- **附录降级** — Appendix downgrade：未核到即不虚构的取证纪律

## 最新演进与工业实践

- 版本演进：8.x→9.x（流复制/SCRAM 前夜）→10（ scram 预告、分区）→14+（SCRAM 默认趋势）
  →16/17（现代默认已基本封死本章多数错配路径 ⚠️ 概括）；仓库内现代落地见
  [03-安全与权限.md](../PostgreSQL_16_Administration_Cookbook/03-安全与权限.md) 与
  [02-用户与连接管理.md](../Learn_PostgreSQL_2e/02-用户与连接管理.md)。
- 工业实践：托管化（RDS/Cloud SQL/Neon 类）把 pg_hba 转译为云安全组+IAM；
  审计走 pgAudit+日志平台（对照 [00-总览与阅读地图.md](../Database_Reliability_Engineering/00-总览与阅读地图.md)
  的保障框架）。
- 攻击面位移：引擎本体溢出少见，现实事件集中在应用注入（Postgres 方言报错回显）、
  扩展供应链（恶意/失维扩展）与云凭证滥用；COPY PROGRAM 滥用仍是托管实例内
  越权叙事常客 ⚠️ 概括。
- 开源近邻：pgbadger（日志）、pgtune（性能）、SQL 注入工具 sqlmap 的 PG 方言
  （报错/时间信道）。
