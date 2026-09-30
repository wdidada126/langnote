# 03 权限、角色与 CONNECT 之辩（主题重构章·含实证锚点）

> 本章为**主题重构**，但锚定原书唯一实证结构碎片：O'Reilly 站内页 `ch05s02.html` 标题 **"The CONNECT Role"**（✅ 搜索引擎索引快照，见 00 元数据表）——原书第 5 章第 2 节确在讨论 CONNECT 角色，本章以此为中心展开。Oracle 侧论述 ⚠️ 文档转述；🔧 组为本目录 SQLite 类比实验，**非 Oracle 行为**。

## 3.1 Oracle 授权模型的三层结构

⚠️ 转述（8i/9i，今日骨架未变）：

1. **系统权限**（system privilege）：动作能力，如 `CREATE TABLE`、`SELECT ANY TABLE`，共 100+ 项（`SESSION_PRIVS` 可查）；授予可带 `WITH ADMIN OPTION`（可转授），撤销**不级联**回收已转授部分——与对象权限的关键差异；
2. **对象权限**（object privilege）：对特定对象的访问，如 `SELECT`/`UPDATE`/`REFERENCES`/`DEBUG` 于某表；`WITH GRANT OPTION` 转授，撤销**级联**回收；支持**列级**授予（`GRANT UPDATE(salary) ON emp TO ...`）——细粒度授权在 2001 年已是商用能力（与 04 章视图路线互补）；
3. **角色**（role）：权限的命名集合，用户默认角色激活集受 `SET ROLE`/默认角色控制；预定义角色组：CONNECT/RESOURCE/DBA/PUBLIC 及 9i 起的 `SELECT_CATALOG_ROLE`、`EXECUTE_CATALOG_ROLE`。

三层的语义缝隙正是事故高发区：`ANY` 家族（`SELECT ANY TABLE` 等）让授权者"图省事"一键越过程序属主；`PUBLIC` 是隐式全员角色，出厂若干 `EXECUTE` 于 `UTL_*`/`DBMS_*` 包挂在 PUBLIC 上（`UTL_HTTP`、`DBMS_JOB` 等），构成"人人可用的代码执行面"（⚠️ 同期社区清算通说，各版本清单不同，勿背具体条目）。

## 3.2 CONNECT 角色：一个跨版本的语义漂移标本（✅ 锚点章）

⚠️ 转述版本演化：

| 版本 | CONNECT 实际包含 | 后果 |
|---|---|---|
| ≤6/7 时代 | 一整套建表建视图权限 | "给 CONNECT=能开发"的旧直觉来源 |
| 8i/9i（本书时代） | CREATE SESSION + （兼容遗留）CREATE TABLE/VIEW/CLUSTER 等若干 | 只登录的用户被白送建表空间配额入口 |
| 10g/11g | 收敛到 CREATE SESSION（11g 官方宣布 deprecated 但保留） | 旧脚本报 ORA-01950（无表空间配额）成为迁移保留节目 |
| 现代 | 官方口径：仅作兼容占位，安全基线一律要求改用自建最小角色 | — |

原书 ch05s02 专节清算的即 8i/9i 行的中间态：**"CONNECT"这个命名在语义上已经背叛了它**——名字叫"连接"，发的是"开发者"的权限。本目录提炼的方法论：预定义角色的名字是历史负债，安全评估永远查 `DBA_ROLE_PRIVS`+`ROLE_SYS_PRIVS` 的实际展开，不读角色名。RESOURCE 同理（当年含数十项 ANY/CREATE 权限，⚠️ 具体条目数各版不同，不写死）。

## 3.3 角色设计的工程规范

⚠️ 重构自本册体裁 + 同期通说：

1. **应用角色 vs 管理角色分离**：应用账户只挂业务角色，DBA 操作走命名个人账户（可审计到人）——"共用 sys 登录"是抵赖性崩溃的头号原因（联动 05 章）；
2. **角色嵌套限深**：9i 允许角色含角色，审计展开需递归查询；过深嵌套让"谁最终拿到了什么"不可读；
3. **安全角色**（secure role）：可给角色加口令/加密/会话绑定（`IDENTIFIED BY`/`USING package`），高权限角色不 SET 即不激活——9i 提供但极少被启用，属于"机制有、策略无"清单（01 章呼应）；
4. **默认角色审计**：`DBA_ROLE_PRIVS.DEFAULT_ROLE` 列——权限在授予那一刻并不生效、登录后自动全激活的隐蔽性所在。

## 3.4 🔧 G1：SQLite authorizer——"权限在内核"与"权限在宿主"的结构性对照（非 Oracle 行为）

SQLite **没有**库内用户/GRANT 体系：访问控制由宿主应用注入回调（`Connection.set_authorizer`，Python 3.11+）。实验（🔧 实测，脚本 `D:\develops\tmp\dbwave_w7_orasec\experiments.py`，Python 3.13.2/SQLite 3.45.3）：

```python
def authorizer(action, arg1, arg2, dbname, trigger):
    if action == sqlite3.SQLITE_DROP_TABLE: return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_ATTACH:     return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK
con.set_authorizer(authorizer)
con.execute("DROP TABLE t")            # -> DatabaseError: not authorized
con.execute("ATTACH DATABASE 'x.db' AS x")  # -> not authorized
con.execute("SELECT count(*) FROM t")  # -> 0，正常放行
```

实测输出：`G1 DROP TABLE blocked -> not authorized`、`G1 ATTACH blocked -> not authorized`、SELECT 正常、回调观察到 6 类动作码。

**对照结论**（两侧分别标注）：🔧 SQLite 侧——授权决策点在 VDBE 执行前的每条语句/每个列读，粒度天然到"列"，但**没有持久化授权表**，重启连接即无策略；⚠️ Oracle 侧——GRANT 体系把"谁/对什么/能做什么"持久化进字典、支持转授链与级联回收，代价是 3.1/3.2 的全部复杂性。两者互为镜子：Oracle 的"权限在数据库里"恰是 2001 年这本书存在的理由，而 SQLite 证明"权限也可以根本不在数据库里"——今天的应用层权限网关（代理数据库、REST 层）走的正是后者路线。

## 3.5 ANY 权限与 PUBLIC：两个"省事的灾难"

⚠️ 转述清算：

- `ANY` 家族（`SELECT ANY TABLE` 等）直接穿透一切对象授权设计（含 04 章视图封装——ANY 面前视图不是掩体）；仅审计/备份/导出类系统账户合理持有；现代版本可将角色置于禁用态收权（⚠️ 机制名以官方文档为准，不背细节）；
- 开发者习惯用 DBA 账户跑应用（"先能跑起来再说"），02 章外部认证+RESOURCE+DBA 三者叠加即"免口令全库"组合雷——本书时代第三方渗透报告的最高频条目；
- PUBLIC 收敛运动：安全基线要求把出厂 `EXECUTE ON ... TO PUBLIC` 逐包回收、改用显式业务角色。评估脚本本身是三连字典查询（`DBA_TAB_PRIVS WHERE GRANTEE='PUBLIC'` 等），属 01 章"以视图为证据源"的标准件。

## 3.6 授权体检一页纸（01 章方法论在授权层的实例化）

⚠️ 重构标准件（每行=一条字典查询+一条判据）：

| 查什么 | 视图 | 红牌判据 |
|---|---|---|
| 全员角色面 | `DBA_ROLE_PRIVS` | 非管理账户挂 DBA/RESOURCE |
| 隐式激活面 | 同上 `DEFAULT_ROLE` 列 | 高权角色=Y |
| ANY 持有清单 | `DBA_SYS_PRIVS` | 业务账户含 ANY |
| PUBLIC 对象面 | `DBA_TAB_PRIVS` | GRANTEE=PUBLIC 且含 EXECUTE 于 UTL_/DBMS_ |
| 转授链 | `DBA_TAB_PRIVS` GRANTABLE 列 | 非属主可再转授 |
| 列级例外 | `DBA_COL_PRIVS` | （出现即复核意图，多为合规正确用法） |

判读纪律（本目录提炼）：**先查展开、后看名字**；任何"通过角色间接获得"的 ANY 与 PUBLIC 权限，在报告里必须回填到最终用户粒度（`ROLE_ROLE_PRIVS` 递归）。

## 3.7 本章自测（三问）

1. CONNECT 在 8i/9i 为什么危险、在 11g 后为何改报错 ORA-01950？（3.2 表：语义从"建表免费"到"只剩登录+配额制"）
2. ADMIN OPTION 与 GRANT OPTION 的回收语义差一格在哪？（3.1：不级联 vs 级联）
3. 🔧 G1 里 SQLite 拦 DROP 靠什么、为什么"重启连接即无策略"？（3.4：宿主回调无持久化，恰照出 Oracle 字典账本的存在理由）。

## 3.8 挂点与勘误预防

- 3.2 漂移表 → 08 章 8.1 默认账户体检的"角色附赠"格；00 §八争议①；
- 3.4 权限外置论 → 04 章 G2（判定发生在哪一层）是同一命题的列粒度版本，两实验合看才完整；
- 3.5 PUBLIC → 05 章"权限审计"的主要被审对象；
- ⚠️ 版本敏感声明：本章所有"CONNECT 含 X 权限""RESOURCE 含 N 项"式表述在不同小版本间均有出入，报告引用前先 `ROLE_SYS_PRIVS` 实测——本目录刻意只给语义不给清单，防背错；
- 列级权限（3.1②）→ 04 章 G2：Oracle 的列级是授权语义、SQLite 的列级是回调语义，同粒度两世界；
- 3.6 一页纸 → 08 章 8.9 总单第 3 行的展开件；
- 配额制 ORA-01950（3.2 表 10g/11g 行）→ 迁移项目保留节目，操作侧处置见在盘 12c 册表空间章。

## 核心概念速览（中英对照）

- **系统权限** — system privilege：动作能力（CREATE TABLE 类），ADMIN OPTION 可转授、撤销不级联。
- **对象权限** — object privilege：对具名对象的访问权，GRANT OPTION 撤销级联，支持列级。
- **角色** — role：权限命名集合，可嵌套、可默认激活。
- **CONNECT 角色** — CONNECT role：名义"连接"、旧语义"开发"的漂移标本（✅ 原书 ch05s02 主题）。
- **RESOURCE 角色** — RESOURCE role：与 CONNECT 同案清算的开发者大礼包。
- **ANY 权限家族** — ANY privileges：SELECT/CREATE/DROP ANY ...，跨属主穿透。
- **PUBLIC** — PUBLIC role：全员隐式角色，出厂 EXECUTE 的收容所。
- **WITH ADMIN/GRANT OPTION** — grant option：两条转授链，回收语义不对称。
- **列级权限** — column-level privilege：GRANT UPDATE(col) 的原生细粒度。
- **安全角色** — secure role：口令/包/会话绑定的角色激活门槛。
- **默认角色** — default role：登录后自动激活集，隐蔽扩权面。
- **authorizer 回调** — authorizer callback（🔧）：SQLite 宿主侧语句级 DENY/OK 闸门。
- **权限外置** — externalized authorization：SQLite/代理网关路线 vs Oracle 内建路线的结构对照。
- **抵赖性** — non-repudiation：共用账户直接摧毁，联动审计章。
- **最小角色自建** — custom least-privilege role：基线动作：不读角色名，查权限展开。

## 最新演进与工业实践

- **CONNECT/RESOURCE 终局**：官方长期口径为 deprecated（11g 公告），现代基线（CIS Benchmark、Oracle 官方 Security Guide）一律要求自建最小角色；12c 起新建库 CONNECT 仅剩 CREATE SESSION（⚠️ 通说，可在任意现代版本上验证该差异——但 Oracle 不可在本目录实测，标 ⚠️）。
- **VPD/Label Security/Data Vault**：9i 引入 VPD（dbms_rls 策略函数把 WHERE 子句注入对象访问——04 章接续），后演进为 Database Vault 的"授权之外的授权"（命令规则/领域规则，2005+，⚠️）。当年靠角色纪律解决的部分问题，现代以运行时策略引擎解决。
- **12c 只读账户与 18+ 权限分析**：`DBA_PRIV_USAGE_STATS`/`DBA_USED_PUBPRIVS`/`DBMS_PRIVILITY_CAPTURE`（18c 权限捕获与未用权限撤销建议，⚠️ 特性名以官方文档为准）——把 3.5 的人工清算自动化。
- **23ai 方向**：角色可带 `COMMON` 前缀跨 PDB 管理、默认策略持续收紧（⚠️ 概要转述）。
- **攻方镜像**：#51 DBHH 对 `ANY`/PUBLIC/口令文件路径的利用章与本册 3.1/3.5 一一对位（登记，未落盘不链，见 00 §四）。
- **在盘互参**：授权操作层的现代手感见 [../Oracle12c数据库应用与开发/05-索引与约束.md](../Oracle12c数据库应用与开发/05-索引与约束.md) 邻域的 GRANT 语境（该书以约束/索引为主，权限面在 00 地图内按需跳转）；理论框架见 [../CISSP认证考试指南.md](../CISSP认证考试指南.md) 的 DAC/RBAC 模型节。
- **老代码考古**：`GRANT CONNECT, RESOURCE TO ...` 至今仍在大量建库脚本里存活——迁移项目按 3.6 页流程重做角色设计时，原脚本行保留注释而非删除，是团队考古学的最低成本实践。
