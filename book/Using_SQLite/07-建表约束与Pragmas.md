# 07 · 建表、约束与 PRAGMA（Table Creation, Constraints, and Pragmas）⚠️ 章号推定

> 主题锚定：CREATE TABLE 语法面、约束（PK/UNIQUE/NOT NULL/CHECK/FK）、外键默认关闭的
> 著名设计、PRAGMA 体系。官方依据：[lang_createtable.html](https://sqlite.org/lang_createtable.html) ✅、
> [pragma.html](https://sqlite.org/pragma.html) ✅、[lang_altertable.html](https://sqlite.org/lang_altertable.html) ✅、
> [foreignkeys.html](https://sqlite.org/foreignkeys.html)（本会话未单独抓取，机制以 🔧 实测 +
> lang_createtable ✅ 内文交叉印证）。

## 1. 建表语法：比标准 SQL 宽，比想象中窄

```sql
CREATE [TEMP] TABLE name (
  coltype-decls..., table-constraints...
) [WITHOUT ROWID] [STRICT];          -- STRICT 为 3.37+（✅ stricttables.html）
```

- 列约束六种：PRIMARY KEY / NOT NULL / UNIQUE / CHECK / REFERENCES / COLLATE；
  表约束同族可跨列（`UNIQUE(a,b)`）。🔧 本机（3.45.3）对 CHECK/NOT NULL/UNIQUE 常规执行无异常，
  与书中一致；
- **约束的执行力是分层配置的**——本节第 3 点外键是最大的一层"默认不执法"。

## 2. ALTER TABLE：书中最痛的限制，已大幅松绑（对位表放第 5 节）

3.8 时代只有 `RENAME TABLE` 与 `ADD COLUMN`（且不能加 NOT NULL 无默认、UNIQUE、
PK、REFERENCES 列）；"改一列 = 建新表搬数据" 是官方推荐流程（
[lang_altertable.html](https://sqlite.org/lang_altertable.html) ✅ 至今保留
"17 steps" 手工重建指南——官方文档转述其仍存在）。书中据此大讲
"表迁移仪式"，这些内容今天读作**心法**而非必做操作。

## 3. 外键：声明容易，执法要点火（书中头号警告）

`REFERENCES` 语法 3.6.x 起解析，但 **`PRAGMA foreign_keys` 默认 OFF**：

🔧 实测（Python，:memory:）：
1. `PRAGMA foreign_keys` → `(0,)`（默认关，亲验）；
2. 建 `parent(id)`/`child(pid REFERENCES parent)`，插孤儿行 `child(999)` **成功**（亲验，rows=1）；
3. `PRAGMA foreign_keys=ON` 后再插 `child(998)` →
   `IntegrityError: FOREIGN KEY constraint failed`（亲验）。

补充语义（官方转述，✅ lang_createtable 约束小节有述）：
- 这是**每连接**开关，不是库属性——连接池里漏一个就漏一个执法者；
- 3.6.19 起支持（历史版本叙事，⚠️ 引自官方 foreignkeys 页，未逐字核）；
- 2026 工程实践：把 `PRAGMA foreign_keys=ON` 写进连接初始化模板（Python 3.12 起
  可用 `connection.set_trace` 之外的位置是驱动初始化参数；各绑定多提供
  `init_command` 式钩子——⚠️ 具体绑定名未核验）。

## 4. PRAGMA 体系：SQLite 的"第二配置面"

三类（[pragma.html](https://sqlite.org/pragma.html) ✅）：

| 类别 | 例 | 语义 |
| --- | --- | --- |
| 查询式（get/set） | `page_size`、`journal_mode`、`foreign_keys`、`cache_size`、`synchronous`、`auto_vacuum`、`busy_timeout` | SELECT 形态读，赋值形态写；部分持久进库头、部分仅连接级 |
| 动作式 | `incremental_vacuum(N)`、`wal_checkpoint(TRUNCATE)`、`optimize`（FTS） | 执行维护任务（09 章🔧） |
| 表式（pragma 虚表） | `table_info`、**`table_xinfo`**、`index_list`、`function_list`、`module_list`、`database_list` | 以表形态自省——🔧 `pragma_module_list` 实测可 SELECT |

**`table_info` vs `table_xinfo` 🔧 实测**（含生成列的表 `g(a,b,t VIRTUAL,h STORED)`）：
- `table_info(g)` 只返回 a、b（**隐藏生成列**）；
- `table_xinfo(g)` 多返回 t、h，hidden 标志 2/3（0=普通，2=VIRTUAL 生成列，3=STORED）。
书中没有这组对（3.8 无生成列），2026 做 schema 审计**必须用 xinfo**，否则代码会
"看不见"一半列。

## 5. 3.8 → 2026 建表能力对位（逐条 ✅ changelog/官方页）

| 能力 | 书中（3.8.x） | 现状 | 取证与本机验证 |
| --- | --- | --- | --- |
| 列重命名 | 不支持 | `RENAME COLUMN` | 3.25.0（2018-09-15）✅ changes.html 原文；3.37 起带 CHECK/生成列的 ADD COLUMN 放宽 ✅ |
| 约束重命名 | 不支持 | `RENAME CONSTRAINT` | 3.37 系列增强（✅ changes.html STRICT 同节有述；引用前按节复核） |
| CHECK 强度 | 存在但历史坎坷 | 完整支持 + CLI `.dbconfig defensive` 保护 sqlite_* 内部表 | 🔧 CLI `.dbconfig` 输出 defensive on（05 章） |
| STRICT 表 | 无 | 每表可选严格类型 | 3.37.0 ✅ stricttables.html；🔧 本机 3.45.3/3.50.6 双端可用 |
| 生成列 | 无 | `GENERATED ALWAYS AS … VIRTUAL/STORED` | 3.31.0 ✅ changes.html；🔧 计算值 (2,3)→t=5,h=6、UPDATE 被拒 |
| 索引内表达式 | 无独立语法 | 表达式索引可用（`CREATE INDEX ON t(lower(x))`）⚠️ 本机未专项实测 | lang_createtable/index 页口径 |
| `defer_foreign_keys` | 无 | 会话级延迟外键检查 | pragma 列表 ✅（3.8.0 前已存在但书中未提，⚠️ 版本叙事从略） |

## 6. 🔧 实测二：STRICT 表的行为边界

方法（Python 3.45.3）：
`CREATE TABLE st(id INTEGER PRIMARY KEY, name TEXT NOT NULL, n REAL, any1 ANY) STRICT`。

结果（🔧 原文）：
- **`NUMERIC` 不是合法 STRICT 类型**：`CREATE TABLE ...(n NUMERIC) STRICT` →
  `unknown datatype for ...: "NUMERIC"`（亲验报错）——迁移旧 schema 必须先把
  声明清洗成 INT/INTEGER/REAL/TEXT/BLOB/ANY；
- 文本 `'2'` 进 INTEGER 列**成功**（无损整数字面文本允许转换——官方规则实锤：
  strict 拒绝的是"有损/不可能"的值）；
- `'notreal'` 进 REAL 列 → `cannot store TEXT value in REAL column st.n`
  （IntegrityError，亲验）；CLI 端同操作报错**尾附错误码 (19)**（🔧 03 章实验 D）；
- `ANY` 列原样保 TEXT 值：`typeof(any1)`='text'（亲验）。

## 7. 设计守则（由本章实验反推）

1. 新库三件套：`STRICT` + `foreign_keys=ON`（连接级）+ 命名约束（便于将来 RENAME/诊断）；
2. 老库体检：用 `pragma_table_info/table_xinfo` 生成"实际执法状态报告"（FK 声明了没开、
   列类型词表是否 STRICT 兼容）；
3. 与系列互链：表迁移心法在 MySQL 语境是 Online DDL 问题
   （[../高性能mysql.md](../高性能mysql.md)、[../Database_Reliability_Engineering/05-无停机变更.md](../Database_Reliability_Engineering/05-无停机变更.md)），
   SQLite 因为"库=文件"而把同一流程简化成 17 步手工重建——两相对照是
   "运维复杂度来自并发可用性需求而非 SQL 语法"的最佳案例。

## 核心概念速览（中英对照）

- **表约束** — table constraint：列/表两级的声明式完整性规则六家族
- **外键开关** — foreign_keys pragma：连接级执法开关，默认 OFF
- **延迟外键** — defer_foreign_keys：本事务末尾统一检查 FK 的会话开关
- **CHECK** — check constraint：行级谓词执法（3.8 起基本完备）
- **命名约束** — named constraint：给约束起名以支持 RENAME CONSTRAINT（3.37+）
- **WITHOUT ROWID** — 索引组织表声明：以主键 B 树代替 rowid 组织
- **STRICT** — 严格表声明：存储类强制一致，类型词表六枚
- **PRAGMA** — 引擎私有指令面：get/set、action、table-valued 三形态
- **table_xinfo** — 扩展列自省：显示 table_info 隐藏的生成列（hidden 2/3）
- **defensive** — dbconfig 护栏：拒写 sqlite_* 内部表（3.26+ 概念）
- **表重建** — table rebuild：改列限制的官方手工流程（17 步）
- **连接初始化** — connection init：把每连接 pragma 固化为模板的工程实践

## 最新演进与工业实践

- **ALTER TABLE 现代化**：3.25.0 RENAME COLUMN（✅ changes.html 精确定位）之后，
  3.37 起 ADD COLUMN 对 CHECK/NOT NULL-生成列放宽（✅ lang_altertable 同页可查）；
  官方文档至今保留表重建指南（lang_altertable ✅），复杂变更仍推荐
  "新表 + 触发器同步 + 改名"的 expand-contract，与
  [../Database_Reliability_Engineering/05-无停机变更.md](../Database_Reliability_Engineering/05-无停机变更.md)
  同构。
- **STRICT 的采用现状**：官方明言 STRICT 是"prescriptive style"、每表可选
  （✅ stricttables.html 首段用语），新项目默认 STRICT + 老库维持 legacy 是社区主流建议
  （⚠️ 综述性判断）。
- **生成列 + STRICT 组合**：`n REAL GENERATED ALWAYS AS (...) STORED` 在 STRICT 表内
  同样受类型一致执法（⚠️ 官方规则口径，本会话未做交叉专项实验）。
- **取证清单（本章）**：lang_createtable.html ✅、pragma.html ✅、lang_altertable.html ✅、
  stricttables.html ✅、changes.html ✅（curl 200，2026-09-27）；
  🔧 实验全部来自 `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt`（EXP7 段）。
  ⚠️ foreignkeys.html 专页未抓，FK 历史版本叙事按官方惯例待核。
