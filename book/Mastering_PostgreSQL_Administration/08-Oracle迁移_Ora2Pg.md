# 08 · Oracle→PostgreSQL 数据迁移：Ora2Pg（原书第 8 章）

> 对应原书章：**Ch.8 Data Migration from Oracle to PostgreSQL Using Ora2Pg**（✅ Crossref DOI `..._8`）。
> 官方摘要原句（✅）："This chapter explores the motives for migrating an Oracle database to a PostgreSQL
> database and explains the different migration methods and various tools available to migrate an Oracle
> database to a PostgreSQL database either within on-premises or to a cloud environment."
> 口径声明：章题与摘要 ✅ 实抓；正文为按 Ora2Pg 官方文档与社区实践口径的精读重构 ⚠️ 转述
> （本机无 Oracle/PG，两端均不装不跑）；🔧 节用 DuckDB/SQLite 实跑**方言语法差异**，非两端引擎结论。

## 本章地图

| 主题 | 你能做到 | 关键对象/参数/命令 |
| --- | --- | --- |
| 迁移动机与范围 | 写得出立项理由与边界清单 | 许可成本、生态位、或云厂商托管 PG 的 TCO 口径 ⚠️ |
| 评估先行 | 用工具量化"能不能迁、多难" | `ora2pg -t SHOW_REPORT --estimate_cst`、PLSQL 复杂度报告 ⚠️ |
| 类型对译 | 建字段映射表并处理暗坑 | NUMBER→numeric、DATE→timestamp、''与 NULL 语义差 ⚠️ |
| Ora2Pg 实操 | 配 conf 跑完 DDL/数据/代码三段 | SCHEMA/TARGET/TYPE/JOBS、EXPORT_* 开关族 ⚠️ |
| 兼容层取舍 | 决定上不上 orafce/改写 | orafce 扩展、包→schema、(+)/ROWNUM 批量改写 ⚠️ |
| 校验与收尾 | 迁移后可信 | 行数/校验和/抽样比对、权限与统计重建 ⚠️ |

## 核心精讲（⚠️ 文档转述重构）

### 1. 路线图谱

去 O 的四段式：**评估 → 结构迁移 → 数据迁移 → 代码/应用适配**；停机窗口大的走
Ora2Pg 一次性装载，窗口小的走"初始装载 + 增量追平"（与 09 章 GoldenGate 或逻辑复制衔接）。
Ora2Pg（✅ https://github.com/darold/ora2pg 与 https://ora2pg.darold.net/ 实抓 200）是 Perl 实现的
开源主力：直连 Oracle（DBD::Oracle）+ PG（DBD::Pg），产 DDL、装载数据、导出 PL/SQL 转 PL/pgSQL，
并给复杂度评估报告——"报告先行"是它的杀手锏（人日估算字段 --estimate_cst ⚠️）。

### 2. 类型对译主表（高频 30 行里的前 10 行）

| Oracle | PostgreSQL | 坑注 |
| --- | --- | --- |
| NUMBER（无精度） | numeric | 大表性能敏感处建议落 numeric(38) 或分拆 int/bigint ⚠️ |
| NUMBER(p) | numeric(p) / integer / bigint | Ora2Pg 按精度自动降型可配 ⚠️ |
| VARCHAR2 / CHAR | varchar / char；`NATIONAL` 前缀同理 | BYTE vs CHAR 语义（长度按字节/字符）要人工复核 ⚠️ |
| DATE | timestamp(0) | Oracle DATE 带时分秒！映射成 date 即丢时间，最常见低级错 |
| TIMESTAMP(6) WITH LOCAL TIME ZONE | timestamptz | 会话时区语义差异列入应用回归用例 |
| CLOB / BLOB | text / bytea | >1996B 走 PG TOAST（03 章），LOB 定位器 API 无对偶，应用必改 ⚠️ |
| RAW | bytea | hex 编解码格式不同（`DEADBEEF`→`\xdeadbeef`）⚠️ |
| ROWID | 无对偶 | 用主键改造"rowid 游标"写法，应用层硬伤 ⚠️ |
| SEQUENCE.NEXTVAL | nextval('seq')（10+ 亦支持 a.nextval ⚠️） | start/increment/cache 对齐，迁移期防重号 |
| 空字符串 '' | ≡ NULL（PG 区分 ''与 NULL） | **语义级头号坑**：所有 `where col is null`/`nvl(col)` 行为回归必测 |

其余（INTERVAL YEAR TO MONTH、XMLTYPE、对象类型、BFILE…）逐表进项目映射文档 ⚠️。

### 3. Ora2Pg 实操骨架（⚠️ 转述）

```conf
# ora2pg.conf 最小可用集
ORACLE_SCHEMA "HR"
ORACLE_DSN   "dbi:Oracle:host=oh;sid=ORCL"
USER / PSWD（低权只读账号，04 章治理口径）
TYPE TABLE,VIEW,MATERIALIZED VIEW,SEQUENCE,INDEX,TRIGGER,PROCEDURE,FUNCTION,PACKAGE,DATA
DEFAULT_SCHEMA app            # 04 章：专用模式承接
JOBS 4                         # 表级并行装载
DISABLE_SEQUENCE / TRIGGERS / FOREIGN_KEYS 1   # 装载期关约束，尾声重建
```

流程：`ora2pg -c ora2pg.conf -t TABLE -s`（先出 DDL 审）→ `ora2pg -t PREVIEW` 抽数据 →
`ora2pg -t LOAD_DATA -b TABLE`（COPY 快速通道，03 章 TOAST/8K 页侧的装载友好性）→
`-t FUNCTION -t PACKAGE` 代码转换 + **人工 diff**（Ora2Pg 转换率非 100%，PACKAGE→schema 化是
主要手工区）。全程幂等重跑靠 `-b` 分项与目录产物。

### 4. 对象与代码级暗坑清单

- **标识符大小写**：Oracle 非引号标识符折叠大写，PG 折叠小写 → 迁移后 `SELECT "Emp"."Id"` 满屏引号。
  社区主流：**统一折叠小写**（Ora2Pg 默认转小写），应用 SQL 同步清洗 ⚠️。
- **(+)** 外连接 → ANSI JOIN；**ROWNUM** 分页 → LIMIT/OFFSET（且 Oracle 12c 的 OFFSET/FETCH 与 PG
  语法近似可直译）；**CONNECT BY** → WITH RECURSIVE；**DECODE** → CASE；**SYSDATE** → now()（时区！）；
  **MERGE** → PG15+ 原生 MERGE（老脚本用 ON CONFLICT 重写）⚠️。
- 包/自治事务/Oracle 特有系统视图（V$、DBA_*）无对偶：orafce 兼容扩展可救急但别当架构 ⚠️。
- 序列"当前值"对齐：`SELECT setval('s', max(id))` 收尾必做 ⚠️。

### 5. 🔧 本机概念演示：方言墙真实存在（DuckDB/SQLite，非 PG 结论）

方法：Python 3.13.2 + **DuckDB 1.5.5** / **sqlite3 3.45.3** 实跑对照（脚本存盘
`D:\develops\tmp\dbwave_w3_pgadmin\demo.py`）：

```
SELECT NVL(NULL,'d')  → DuckDB: Catalog Error: Scalar Function with name nvl does not exist!
                       → SQLite: no such function: NVL
SELECT COALESCE(NULL,'d') → [('d',)]        # 同义改写即通行
SELECT current_date                           → 2026-09-27（对位 Oracle SYSDATE 概念）
LIMIT 2 / CASE WHEN…END                       → 均通过（对位 ROWNUM / DECODE 的现代写法）
```

**概念结论**（✅ 方法论）：同一语义在不同引擎常只认一种拼写——**迁移工程的核心工作量正是这张
"同义算子映射表"**，且映射有方向性（COALESCE 通行、NVL 专有）。Ora2Pg 的转换器、兼容性扩展
（orace 类）与应用改写都是在为这张表的不同列买单。数字属 DuckDB/SQLite，Oracle/PG 两端未实测 ⚠️。

## 常见坑与判读

| 现象 | 第一判读 | 取证动作（⚠️ 转述） |
| --- | --- | --- |
| 迁完行数对不上 | 装载中途报错跳过/字符集丢行 | Ora2Pg 日志 ERROR 计数 + 两端 count(*) 分组比对 |
| 空串条件全错 | Oracle ''=NULL 语义差 | 全局 grep nvl/is null/='' 用例回归（第 2 节头号坑） |
| 日期列时间部分消失 | DATE→date 误映射 | 映射表复核 + timestamp(0) 重导 ⚠️ |
| 序列主键冲突 | 序列当前值未对齐 | setval 对齐 max(id) 后重放增量 |
| 应用报关系不存在 | 大小写折叠差异 | 统一小写策略；检查引号标识符残留 |
| 切换后突发慢 | 统计信息缺失 | ANALYZE 全库（06 章）；PG17 前统计不随 pg_upgrade 走 |

## 与其他章 / 其他笔记的联系

- 本册：03 章（bytea/TOAST 存储侧后果）；04 章（对译表是本章前置；角色映射承接权限重建）；
  05 章（迁移窗口内的备份链不断）；06 章（迁后统计/膨胀治理）；09 章（增量追平通道）；
  10 章（PG17 装载与逻辑复制改进对迁移的增益）。
- [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)：
  系列"另一源端"的内部结构参照位（SQL Server 迁移语境时反查）。
- [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)：
  去 O 落地选 MySQL 路线时的姊妹对照（同为 Oracle 迁出目标的坑谱系）。
- [../PostgreSQL_16_Administration_Cookbook/07-复制高可用与升级.md](../PostgreSQL_16_Administration_Cookbook/07-复制高可用与升级.md)：
  逻辑复制通道与升级链食谱版。
- [../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 核心概念速览（中英对照）

1. **去 O** — Oracle exit/migration：以成本与自主可控为动机的整库换引擎工程。
2. **复杂度评估** — migration assessment report：Ora2Pg 的对象计分与人日估算，立项第一产出物。
3. **类型映射表** — data type mapping：字段级对译清单，DATE/'' 两个高频暗坑在此闭环。
4. **Ora2Pg**：Perl 栈的 Oracle→PG 开源迁移主力（DDL/数据/PLSQL/报告四合一）。
5. **兼容层** — orafce 类扩展：函数/包语义垫片，救急不上架构。
6. **折叠大小写** — identifier case folding：两端非引号标识符折叠方向相反，统一小写是主流解法。
7. **LOBI 定位器** — LOB locator：Oracle 流式读写 API，PG bytea/text 无对偶，应用必改。
8. **自治事务** — autonomous transaction：PG 无对偶语义，改造需重新设计（通常拆 outbox 表）。
9. **空串≡NULL**：Oracle 特有语义，迁移回归测试第一优先。
10. **装载关约束** — disable triggers/FK during load：Ora2Pg 并行装载的事务安全前置。
11. **增量追平** — delta sync：初始装载后靠日志/触发通道补差，衔接 09 章。
12. **切换演练** — cutover rehearsal：影子库双跑 + 校验和比对，迁移验收的硬门槛。

## 最新演进与工业实践

- **Ora2Pg 现状**：官方仓库持续维护（✅ https://github.com/darold/ora2pg 实抓 200，2026-09-27），
  近年增强集中在 PG17 目标端语法兼容与装载并行度；Oracle 端对新版本客户端的适配跟随 DBD::Oracle ⚠️ 转述。
- **PG15+ MERGE / PG17 逻辑改进**：Oracle 迁移包的"最后一段路"（增量同步）在 PG17 的可运维性提升
  （见 09/10 章演进节）✅ 入口 https://www.postgresql.org/docs/release/17.0/ 实抓 200。
- **托管去 O**：云厂商迁移服务（DMS/SCC 类）与 AWS/Blob 生态把 Ora2Pg 包成托管流水线；
  核心知识（映射表/暗坑清单）不变，只是执行位从本地脚本搬到控制台 ⚠️ 转述。
- **社区方法论**：评估→试点→双跑的三段式成为主流；"兼容层比例"作为技术债指标被显式管理
  （orafce 使用量入架构评审）⚠️ 转述。
- **缺口诚实登记 ⚠️**：原书第 8 章实操用的版本（Ora2Pg v2x 具体小版本、截图 UI）与是否含 AWS SCT
  对照未获样章，不臆写。
