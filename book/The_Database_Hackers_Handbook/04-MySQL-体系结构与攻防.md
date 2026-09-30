# 04 · MySQL：体系结构与攻防（原版 Part VI / Ch17–20）

> 覆盖中文版目录第 17–20 章（✅ 目录逐字）：MySQL体系结构 / MySQL：发现、攻击和防御 /
> MySQL：深入网络 / 保护MySQL。版本基线 MySQL 4.1/5.0 时代；小节为主题重构 ⚠️。
> 正面结构知识可回链 [00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)。

## 1. Ch17 MySQL 体系结构（安全切片）

- **单进程多线程 + 插件式存储引擎**（MyISAM 时代，InnoDB 尚为可选引擎）：
  进程沦陷即全部库沦陷，无实例隔离（对照 DB2 两级模型，见 [03-DB2-发现攻击与防御.md](03-DB2-发现攻击与防御.md)）。
- **认证与授权双层**：`mysql.user` 的 user@host 粒度 + 全局/库/表级权限；
  4.1 口令哈希为 **160-bit SHA1 截半**（两 8 字节 DES 块混合），离线还原成本低 ⚠️ 转述。
- **默认安装的裸面**：匿名账户（空 user@host）、root 空口令惯例、test 库人人可写——
  书中"发现"章的第一靶。
- **网络面**：3306/TCP；协议握手携带版本串与加盐 scramble（明文协议，可中间人）。
- **UDF 与数据目录**：`mysql.func` 注册可加载任意 .so/.dll（FILE 权限+可写插件目录），
  是 4.x/5.0 最凶的"库→主机"跳板（Kevin Wall 系公开研究 ⚠️ 作者归属未逐章核验）。

## 2. Ch18 发现、攻击与防御（Web 时代语境）

- **发现**：端口+`mysql --version`/SELECT VERSION() 指纹；`information_schema`（5.0 起）
  让元数据侦察从猜表名变成查字典——本书强调注入语境下"schema 自举"效率跃升。
- **注入路径**（Web 应用层展开见 [白帽子讲Web安全.md](../白帽子讲Web安全.md)）：联合查询回显、
  `information_schema` 拖库、`load_file()/INTO OUTFILE` 读写主机文件（需 FILE 权限+
  secure_file_priv 未设，5.7 后收紧 ⚠️ 演进注）、写 webshell/计划任务。
- **叠加查询**：MySQL C API `mysql_real_query` 默认单语句；开启
  `CLIENT_MULTI_STATEMENTS` 后叠加生效——同一引擎两种安全姿态，书中作为
  驱动配置攻击面的范例 ⚠️ 转述（与 SQLite 🔧 E1b"驱动级拒叠"构成跨语言对照）。
- **UDF 提权三部曲**：上传恶意库（需 FILE+可写目录）→ `CREATE FUNCTION` 注册 →
  执行系统命令；书中给出完整攻击链示例。
- **防御**：最小权限（撤 FILE/SUPER/GRANT OPTION）、禁匿名、`--skip-grant-tables`
  绝不上生产、`老库口令全换` 的迁移策略。

## 3. Ch19 MySQL：深入网络

- **协议画像**：握手明文、auth switch 机制尚未出现（4.x 固定 scramble），
  版本/能力位在 banner 里全说；扫描器可无凭证枚举能力。
- **DoS 面**：`max_connections` 耗尽 + `connect(0)` 类畸形报文（5.0 前解析脆弱期 ⚠️）、
  `mysql_proc` 旧协议多包处理错误。
- **中间人**：无 TLS 强制的默认安装下，嗅探即拿全量 SQL（含语句里的敏感参数）。

## 4. Ch20 保护 MySQL（加固清单重构）

- 安装即加固：`mysql_secure_installation` 的四个"删除"（匿名/test/root 远程/重载）
  在书中已成雏形建议（该脚本为后来版本正式化 ⚠️ 演进注）。
- 账户策略：口令复杂度（5.7 validate_password 插件前身是外规 ⚠️）、
  登录失败锁定、root@localhost 唯一化。
- 权限策略：应用账户按库/表授；审计（企业版 audit log / 通用 query log 轮转）。
- 网络策略：bind-address=127.0.0.1 起步、TLS 强制（`REQUIRE SSL`）、
  skip-networking 单机部署。
- 升级窗口：4.1→5.0 的认证哈希兼容期问题（新旧哈希并存的降档风险 ⚠️ 转述）。

## 5. 🔧 类比锚（SQLite，非本书 MySQL 行为）

- **注入**：🔧 E1 全链路演示（拼接→全表外带→参数化封堵），结论与本章"参数化第一"一致；
  但 SQLite **无 FILE/load_file/OUTFILE 面**（无网络服务、单文件），
  "注入→读主机文件→webshell"的 MySQL 链在 SQLite 语境不存在——标非本书行为。
- **叠加语句**：🔧 E1c Python sqlite3 驱动直接拒多语句（ProgrammingError），
  比 MySQL "取决于客户端能力位"更强地默认安全。
- **匿名账户** ↔ SQLite **无认证概念**：文件到手即全权（🔧 E2/E3），
  相当于"人人都是 root@%"的极端形态——嵌入式场景安全重心整体移向 OS 与密钥层。

## 6. 与系列其他 MySQL 笔记的分工

| 议题 | 归谁 |
|---|---|
| 存储引擎/锁/日志正面机制 | [00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)、[MySQL运维内参.md](../MySQL运维内参.md) |
| 性能与容量运维 | `../Efficient_MySQL_Performance`（目录版） |
| 注入的 Web 上下文 | [白帽子讲Web安全.md](../白帽子讲Web安全.md) |
| 引擎攻击面（本章） | 认证哈希/UDF/FILE/网络默认姿态 |

## 7. 注入进阶阶梯（书中 MySQL 章的 payload 演化线 ⚠️ 重构）

1. **回显探测**：`' UNION SELECT 1,2,3 --` 定列数与字符列位；
2. **版本与身份**：`VERSION()`/`USER()` 回显——判断可否走后续台阶；
3. **字典自举**：5.0 起 `information_schema.tables/columns` 拖结构（4.1 时代
   只能猜表名，书中对比了两种年代的注入成本）；
4. **数据外带**：按库拖 `mysql.user`（拿哈希）与业务表；
5. **文件台阶**：FILE 权限在则 `load_file('/etc/passwd')` 探针 →
   `INTO OUTFILE` 写码；
6. **主机台阶**：UDF 上传注册三部曲（见 Ch18 节）→ 命令执行；
7. **痕迹管理**：slow log/general log 重定位（`--log` 篡改面 ⚠️ 转述）规避审计。

> 该阶梯与 [白帽子讲Web安全.md](../白帽子讲Web安全.md) 应用层叙述互为表里：MySQL 章解释"为什么
> 每一步都可行"，Web 安全章解释"注入点从哪来"。

## 8. 年代校准卡（读本章先对齐）

| 书中语境（2005，4.1/5.0） | 今天的状态（8.x/9.x ⚠️ 概括） |
|---|---|
| 匿名账户+test 库默认存在 | 安装器强制清除；8.0 无匿名 |
| SHA1 截半弱哈希 | caching_sha2_password 默认 |
| OUTFILE 靠 FILE 权限自律 | secure_file_priv 默认目录约束 |
| 叠加取决于客户端能力位 | 驱动默认多为单语句 |
| TLS 可选、明文常态 | 云托管默认 TLS 强制 |
| UDF 提权流行 | 托管实例 FILE 不可得，链断裂 |

## 核心概念速览（中英对照）

- **user@host 授权** — Account-level grant：MySQL 以"用户+来源主机"为权限主体
- **匿名账户** — Anonymous user（空 user）：默认安装裸面之首，后被安装器清除
- **SHA1 截半哈希** — 4.1 password hash：两 DES 块混合的弱形态，可离线还原
- **information_schema** — 元数据字典：5.0 起的 schema 自举侦察面
- **INTO OUTFILE / load_file** — 文件读写语句：FILE 权限越界出库通道
- **secure_file_priv** — 文件路径白名单：上述通道后来的收口配置（演进 ⚠️）
- **UDF 注入** — User-Defined Function hijack：mysql.func+恶意库=主机执行
- **CLIENT_MULTI_STATEMENTS** — 多语句能力位：驱动配置决定叠加是否可行
- **max_connections 耗尽** — 连接洪水：彼时最常见 MySQL DoS 形态
- **REQUIRE SSL** — 连接级 TLS 强制：明文嗅探议题的修复开关
- **mysql_secure_installation** — 安装加固脚本：书中建议的后来正式化
- **query log 轮转** — General log audit-lite：企业审计缺位时代的监控替代

## 最新演进与工业实践

- 版本演进：5.0→5.5（InnoDB 默认）→5.7（secure_file_priv 默认、validate_password）→
  8.0（caching_sha2_password、SQL 防火墙类能力靠企业版/代理层 ⚠️ 概括）——
  本章弱哈希/匿名账户/OUTFILE 三大裸面在现代默认安装中全部收口。
- MariaDB 分支接管部分开源部署（本 repo [MariaDB原理与实现.md](../MariaDB原理与实现.md)、`../Migrating_to_MariaDB` 有正面叙述）。
- 工业实践：注入对策已平台化——预编译语句为 ORM 默认、WAF/RASP 补位、
  数据外带告警（DLP）；UDF 提权在云托管实例（RDS 类）中因 FILE 权限不可得而消失，
  攻击叙事转向凭证泄露与滥用（对照 [00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)）。
- 开源工具：sqlmap 的 MySQL 方言最完备（联合/布尔盲注/报错/时间四道），
  mitmproxy+MySQL 明文协议复现仍可做实验 ⚠️ 本环境未实做。
- 论文线：SQL 注入检测（AST/污点）与绕过研究长盛，可经 [db.md](../../db/db.md) 论文索引溯源。
