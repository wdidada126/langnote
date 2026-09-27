# 第 13 章　SQL 约束（SQL Constraints ⚠️ 回译）

> 译本 p169–176｜小节（✅ 实抓）：13.1 数据库约束 / 13.2 类型约束 / 13.3 练习 / 13.4 答案。
> 第 6 章讲的是「约束**应该**是什么」（谓词、断言、声明式）；这一章是「SQL **实际**给了什么」。
> 一句话结论：**标准里有断言，产品把它砍掉了；剩下的约束家族还依赖会话开关，所以"没开开关"就等于"没约束"。**

## 本章地图

| 模型里的东西（第 6 章） | SQL 里的对应物 | 支持状况 | 🔧 实测证据（A 系列，SQLite 3.45.3） |
| --- | --- | --- | --- |
| 关系变量断言（元组级谓词） | 列级/表级 `CHECK` | 有，但禁子查询、且 UNKNOWN 视为通过 | A6 / A7 / A8 |
| 数据库断言（跨关系谓词） | `CREATE ASSERTION`（SQL:1999） | 标准有，产品普遍没有 | A9：`near "ASSERTION": syntax error` |
| 域（类型 + 约束） | `CREATE DOMAIN`（标准） | SQLite 无 | 「CREATE DOMAIN」→ `near "DOMAIN": syntax error` |
| 候选码（平等的一组码） | `PRIMARY KEY` / `UNIQUE` | 语法有，语义不平等 | A11：只有 autoindex，另加隐藏 `rowid` |
| 外码 / 包含依赖 | `FOREIGN KEY ... REFERENCES` | 有，但默认关闭 | A1–A4、A12–A14 |
| 约束的求值时点 | `DEFERRABLE / INITIALLY DEFERRED` | SQLite 有可用实现 | A15 / A16 |
| 「类型只限制取值」 | 声明类型 = affinity | 形同虚设 | A5：一列混 text/real/null/integer |

## 核心精讲

### 1. 13.1 数据库约束：SQL 给的是「五种声明 + 一个开关」

标准在表定义里能写的东西不多：`NOT NULL`、`UNIQUE`、`PRIMARY KEY`、`FOREIGN KEY`、`CHECK`（加上 13.2 的 `DOMAIN`）。作者在第 6 章已经铺好判据——**一条声明是否算约束，看它是否在数据库状态每次变化时被 DBMS 自己求值并强制**。用这条判据看 SQL：

**① 外键：默认不生效**（🔧 A1/A2）

```sql
PRAGMA foreign_keys;                     -- -> [(0,)]     默认关闭
CREATE TABLE SP_off (SN TEXT REFERENCES S(SN), PN TEXT, QTY INTEGER);
INSERT INTO SP_off VALUES ('S9','P9',1); -- 被接受：REFERENCES 此时等同注释
SELECT COUNT(*) AS bad_rows FROM SP_off WHERE SN NOT IN (SELECT SN FROM S);  -- -> [(1,)]
```

**② 开关打开后也不追认历史脏行**（🔧 A3/A4）：非法新行被拒（`FOREIGN KEY constraint failed`），但已有的 `S9` 行仍在；只有事后跑 `PRAGMA foreign_key_check;` → `[('SP_off', 1, 'S', 0)]` 才看得见。完整性依赖会话状态 + 需要人工体检 ⇒ 这在模型意义上就是「没有约束」。

**③ `CHECK` 只能表达元组级断言，且 NULL 会漏**（🔧 A6/A7）

```sql
CREATE TABLE T_nullchk (V INTEGER CHECK (V > 0));
INSERT INTO T_nullchk VALUES (NULL);     -- 被接受！CHECK 返回 UNKNOWN 不阻止写入
INSERT INTO T_nullchk VALUES (-1);       -- !! CHECK constraint failed: V > 0
```

第 6 章说「断言是谓词，谓词必须有真值」；SQL 的 `CHECK` 却把「真值不是 True」和「真值是 False」区分对待——只有 False 才拒。这与 `WHERE` 把 UNKNOWN 当假（🔧 D8b）恰好相反，两处口径不一致是 3VL 的又一次泄漏（→ 第 14 章清单）。

**④ 跨关系的东西一律写不进 `CHECK`**（🔧 A8/A9）

```sql
-- 想让"只有已存在的供应商才能出现在 T_assert"
CREATE TABLE T_assert (SN TEXT PRIMARY KEY CHECK (EXISTS (SELECT 1 FROM S WHERE S.SN = T_assert.SN)));
-- !! OperationalError: subqueries prohibited in CHECK constraints
CREATE ASSERTION city_max_2 CHECK ((SELECT COUNT(*) FROM S WHERE CITY='Paris') <= 2);
-- !! OperationalError: near "ASSERTION": syntax error
```

于是第 6 章的「断言」在产品里只剩一条出路：触发器（🔧 A10）——`CREATE TRIGGER ... WHEN (SELECT COUNT(*) FROM S WHERE CITY = NEW.CITY) > 2 BEGIN SELECT RAISE(ABORT, ...); END` 实测 S4 通过、S5 被拒。代价是把声明式规则改写成过程式代码：它只在「走 SQL 写入路径」时成立，批量导入、直接改文件、以后换个引擎都能绕过。

**⑤ 参照动作：模型不管"怎么补救"，SQL 必须管**（🔧 A13/A14）

```sql
CREATE TABLE T_cas (SN TEXT REFERENCES S2(SN) ON DELETE CASCADE, PN TEXT);
-- 插入 2 个子行 -> children_before [(2,)]
DELETE FROM S2 WHERE SN = 'S1';          -- CASCADE
-- children_after  -> [(0,)]
```

而无 `CASCADE` 时（🔧 A14）删父行直接 `FOREIGN KEY constraint failed`，父行仍在（`parent_rows [(4,)]`、`child_rows [(1,)]`）——整条语句回滚。`ON DELETE SET NULL`/`SET DEFAULT` 同样是产品发明：它们都在**修改数据来迁就错误的删除**，而不是拒绝违反约束的状态（⚠️ 转述：`SET NULL` 还要求被引用列可为 NULL，否则行为随产品而异）。

**⑥ 匹配语义只有 SIMPLE**（🔧 A12）：复合外码 `(C1,C2)` 引用 `S2p(SN,PN)`，插入 `('S1',NULL)`、`(NULL,'P1')`、`('S9',NULL)` 三条全部被接受，只有 `('S9','P9')` 被拒 ⇒ 任一组件为 NULL 就整行跳过检查（SQL 的 SIMPLE 匹配）。标准的 `MATCH FULL`（要么全 NULL 要么全非 NULL）在 SQLite 无处声明。这就是「外码是包含依赖」在含 NULL 时的破口——第 3 章的包含依赖定义要求**逐元组成立**，SIMPLE 匹配把它放宽成了**逐非空元组成立**。

**⑦ 候选码被降级成"一个 PK + 若干唯一索引"**（🔧 A11）：`pragma_index_list('S')` → `[('sqlite_autoindex_S_1', 'pk', 0)]`；两张 `UNIQUE` 列的表得到两条 origin 同为 `u` 的 autoindex，引擎不给它们任何"码"的地位，同时又额外提供隐藏 `rowid` 作为真实元组身份（→ 第 2 章 D1c/D3c）。第 3 章的判据「码是关系必须有的性质」在这里彻底落空：`CREATE TABLE no_key (A INTEGER, B INTEGER)` 合法（🔧 D7f，插两条相同行 → `[(2,)]`）。

**⑧ 唯一真正对上了模型的东西：可延后约束**（🔧 A15/A16）

```sql
CREATE TABLE T_def (SN TEXT REFERENCES S(SN) DEFERRABLE INITIALLY DEFERRED);
BEGIN; INSERT INTO T_def VALUES ('S99');     -- 事务内不报错
COMMIT;   -- !! IntegrityError: FOREIGN KEY constraint failed
SELECT COUNT(*) FROM T_def;                  -- -> [(1,)]  ← 陷阱！
ROLLBACK; SELECT COUNT(*) FROM T_def;        -- -> [(0,)]
```

`DEFERRABLE INITIALLY DEFERRED` 让约束在**事务边界**求值，这正是第 6/8 章说的「约束限制的是状态，事务是状态转移的单位」——标准给了语法，多数产品没给实现，SQLite 给了。但注意实测的坑：**COMMIT 被拒后事务并没有自动关闭**，脏行在同一连接里仍然可见，必须显式 `ROLLBACK`。这提醒一句工程口径：延迟约束失败时不要假定"事务已经干净地结束了"。

### 2. 13.2 类型约束：整个领域在产品里近乎缺席

第 7 章的类型公设说：每个属性有一个**域（类型）**，元组分量必须是该类型的值，域可以带自己的约束（"状态 ∈ 0..100"）。SQL 侧的现实：

- **声明类型不是类型约束**。🔧 A5：`CREATE TABLE T_typ (ST INTEGER)` 后插入 `'abc'`、`3.14`、`NULL`、`42` 全部成功，`typeof(ST)` → `[('abc','text'), ('3.14','real'), (None,'null'), (42,'integer')]`；甚至 `SELECT MIN(ST)` → `[(3.14,)]`——跨类型比较用的是 SQLite 的类型排序（null < integer/real < text < blob），不是任何"整数上的序"。这就是 SQLite 文档所说的 affinity（⚠️ 术语出处见 https://www.sqlite.org/datatype3.html ✅）。
- **`DOMAIN` 不存在**：🔧 `CREATE DOMAIN D_STATUS AS INTEGER CHECK (VALUE >= 0 AND VALUE <= 100)` → `near "DOMAIN": syntax error`。于是"类型 + 约束"无法一次声明、多处复用，只能把同一串 `CHECK` 抄在每张表上（PostgreSQL 实现了 `CREATE DOMAIN`，⚠️ 转述：https://www.postgresql.org/docs/current/sql-createdomain.html ✅）。
- **带约束的类型必须有秩序，而"相等"随列而变**（🔧 A20）：`A TEXT COLLATE NOCASE` 与 `B TEXT` 存同一个值 `'s1'`，`WHERE A='S1'` → 1 行、`WHERE B='S1'` → 0 行 ⇒ `=` 不是全域统一的比较运算符，属性带着自己的等价关系。关系模型里这属于"类型的成分"，SQL 里属于"列的选项"。
- **约束的时点/范围**（🔧 A18 vs A17）：SQLite 没有 `EXCLUDE BY`（`near "D": syntax error`），但**部分唯一索引**能表达"每个城市最多一个 status=99"：`CREATE UNIQUE INDEX u_worst ON T_pu (CITY) WHERE STATUS = 99` → 第二条 Paris/99 被 `UNIQUE constraint failed: T_pu.CITY` 拒掉，而 Paris/10 仍然允许。约束在产品实现层就是索引的化身——这个事实决定了「能不能表达」经常取决于「有没有一种索引形状」。
- **视图上的检查（WITH CHECK OPTION）缺席**：🔧 `CREATE VIEW V_hi AS ... WITH CHECK OPTION` → `near "WITH": syntax error`，所以"通过受约束的视图写入"这条标准路径也不通（⚠️ PostgreSQL 支持，见其文档）。
- **能用的补充手段**：生成列 + `CHECK`（🔧 A19 类测试）——`CREATE TABLE T_gen (..., S INTEGER GENERATED ALWAYS AS (A+B) VIRTUAL, CHECK (S <= 10))`：插入 `(6,7)` 被 `CHECK constraint failed: S <= 10` 拒，插入 `(4,5)` 通过，且 `UPDATE T_gen SET S=1` → `cannot UPDATE generated column "S"`。这是"派生值不可写 + 派生值可约束"的少见完整组合，比视图 + CHECK OPTION 更硬。
- **`DEFAULT` 是占位值，不是缺失值**（🔧）：`STATUS INTEGER DEFAULT 0` 下省略列得到 `0`（`typeof` = `integer`），显式写 `NULL` 得到 `null`。第 7 章反对"用某个域内值冒充未知"，`DEFAULT` 正是这种冒充的语法化入口。
- **事后体检**：`PRAGMA integrity_check;` → `[('ok',)]`（🔧）——产品把"库是否自洽"做成了一个命令，而不是一个不变式。

### 3. 把 13.1 + 13.2 叠回第 6 章

| 第 6 章的判据 | SQL 现实 |
| --- | --- |
| 约束是谓词，声明式 | 只有元组级谓词可声明（`CHECK`）；跨关系谓词必须写成触发器 |
| 约束限制状态空间，不限过程 | 求值时点可被会话开关、SIMPLE 匹配、NULL 放过三处绕开 |
| 约束在每次状态转移后仍成立 | 可延后约束终于做到了事务边界成立（🔧 A15），但历史脏行不追认（🔧 A3/A4） |
| 类型是第一等公民 | 类型只是列属性；`DOMAIN` 缺席，affinity 使声明不成立 |

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「写了 `REFERENCES` 就有参照完整性」 | 🔧 默认 `PRAGMA foreign_keys = 0`，且开关打开不追认存量脏行 |
| 「`CHECK` 里返回 UNKNOWN 会拦下来」 | 🔧 不拦：NULL 直接通过，必须再写 `NOT NULL` |
| 「约束只能建表时声明」 | SQLite 没有 `ALTER TABLE ... ADD CONSTRAINT`（PostgreSQL 有 `ADD CONSTRAINT ... NOT VALID`，⚠️ 转述），改约束常要重建表 |
| 「`ON DELETE CASCADE` 是模型要求的」 | 模型只要求「不允许违规状态」；CASCADE/SET NULL 是产品的**自动改数据**策略，可能把删除扩散成静默数据丢失 |
| 「UNIQUE 列就是候选码」 | 🔧 引擎只看到 autoindex，还另给 `rowid` 当真实身份；码的"最小性"也不被检查 |
| 「声明了 `INTEGER` 就是整数域」 | 🔧 affinity：同列可存 text/real/null，`MIN()` 用类型序而不是数值序 |
| 「延迟约束失败＝事务回滚干净了」 | 🔧 A16：`COMMIT` 被拒后事务仍开着，脏行本连接内可见，需要显式 `ROLLBACK` |
| 「有断言需求就上 dbt/期望框架」 | 那是**事后检测**；本章的差别在于「写入时由 DBMS 拒绝」（→ 第 12 章末、第 14 章） |

## 与其他章 / 其他书的联系

- 约束的应然定义（谓词、断言、约束 vs 断言的层次）：[06-约束和断言.md](06-约束和断言.md)；码/外码/包含依赖：[03-码外码和相关概念.md](03-码外码和相关概念.md)。
- 类型公设、域、关系类型产生器：[07-关系模型.md](07-关系模型.md)；NULL 与 3VL 的语义：[11-SQL操作符Ⅰ.md](11-SQL操作符Ⅰ.md)；聚集/断言在 SQL 里的替身：[12-SQL运算符Ⅱ.md](12-SQL运算符Ⅱ.md)；求值时点与事务：[08-事务.md](08-事务.md)；本章偏离项的汇总：[14-SQL与关系模型.md](14-SQL与关系模型.md)。
- SQL 侧「约束的声明式力量」的可操作版本（怎么写才不被 NULL 反噬）：[../SQL_and_Relational_Theory/10-约束的声明式力量.md](../SQL_and_Relational_Theory/10-约束的声明式力量.md)、[../SQL_and_Relational_Theory/08-外键与参照完整性.md](../SQL_and_Relational_Theory/08-外键与参照完整性.md)。
- 学院口径的约束小节（`CHECK`/断言/域）：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)、[../数据库系统概念6/08-关系数据库设计.md](../数据库系统概念6/08-关系数据库设计.md)。
- 同一引擎的产品手册视角（外键开关、affinity、部分索引的真实语义）：同波 [#87 `Using_SQLite`](../Using_SQLite/00-总览与阅读地图.md)（已落盘，波尾闭环；见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 登记）。
- 物理层为什么"约束=索引"：[../Database_Internals/01-简介与概览.md](../Database_Internals/01-简介与概览.md)。

## 核心概念速览（中英对照）

- **数据库约束** — database constraint：限制关系变量/数据库**允许的值**的谓词（第 6 章口径）
- **表级 / 列级约束** — table / column constraint：`CHECK` 的两种书写位置，求值都是元组级
- **`CHECK`** — check constraint：唯一的元组级断言替身；禁子查询、UNKNOWN 放过 🔧
- **断言** — assertion（`CREATE ASSERTION`，SQL:1999）：跨关系谓词，产品普遍缺席 🔧
- **域** — domain（`CREATE DOMAIN`）：类型 + 约束的可复用单元；SQLite 无语法 🔧
- **类型亲和** — type affinity：SQLite 声明类型只是"倾向"，不构成域约束 🔧
- **候选码 vs 主码** — candidate key vs primary key：SQL 只给一个 PK + 若干唯一索引，不承认码的平等地位 🔧 A11
- **包含依赖** — inclusion dependency：外码的模型本质；被 SIMPLE 匹配放宽 🔧 A12
- **SIMPLE / FULL / PARTIAL 匹配** — `MATCH` 子句：含 NULL 的外码行是否参与检查；SQLite 只有 SIMPLE 🔧
- **参照动作** — `ON DELETE/UPDATE CASCADE / SET NULL / RESTRICT`：产品的自动补救策略，非模型概念 🔧 A13/A14
- **可延后约束** — `DEFERRABLE INITIALLY DEFERRED`：在事务边界求值的约束，最接近模型的机制 🔧 A15
- **部分唯一索引** — partial unique index：用索引形状补约束表达力 🔧 A18
- **生成列** — generated column：派生值不可写且可参与 `CHECK` 🔧
- **`WITH CHECK OPTION`** — 视图写入的谓词检查：SQLite 不支持 🔧
- **`PRAGMA foreign_key_check` / `integrity_check`** — 事后体检：把不变式降级为命令 🔧

## 最新演进与工业实践

- **SQLite（本机 🔧 3.45.3）**：外键仍是编译期默认 + 连接期开关（https://www.sqlite.org/foreignkeys.html ✅），`CHECK` 仍禁子查询，无 `ASSERTION`/`DOMAIN`/`WITH CHECK OPTION`/`EXCLUDE`；3.45 一线的稳定能力是生成列、部分唯一索引（https://www.sqlite.org/partialindex.html ✅）、`DEFERRABLE`。表文档见 https://www.sqlite.org/lang_createtable.html ✅。⚠️ 本章未实测更新的 3.5x 版本。
- **PostgreSQL（⚠️ 转述，本机未装）**：约束家族最完整的一侧——`CHECK`（含 `NO INHERIT`）、`UNIQUE`、`PRIMARY KEY`、`FOREIGN KEY ... MATCH FULL/PARTIAL/SIMPLE`、`EXCLUDE USING gist/spgist`（跨行区间不重叠）、`NOT VALID` + `VALIDATE CONSTRAINT`（先建后验，避免长锁）、`CREATE DOMAIN`、`WITH CHECK OPTION`、约束名与 `pg_constraint` 系统目录（https://www.postgresql.org/docs/current/ddl-constraints.html ✅、https://www.postgresql.org/docs/current/sql-createdomain.html ✅）。`EXCLUDE` 正是 12.4.2「通用限制」在**有限形状**上的部分实现，但仍不是任意谓词。
- **MySQL / InnoDB（⚠️ 转述）**：`CHECK` 到 8.0.16 才真正强制（8.0.16 之前解析后忽略），无 `ASSERTION`、无 `DOMAIN`（https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html ）；参照动作齐全但 `MATCH FULL/PARTIAL` 支持有限。这类"同名不同义"正是第 14 章要按产品分列的原因。
- **断言需求的外移（工业实践）**：跨表/跨行规则今天常见三种落点——① 库内触发器或 `EXCLUDE`；② 建模层的 dbt tests / Great Expectation 类期望（**写入后检测**）；③ 应用层 + 单一写入口（第 10 章批评的"程序系统"回潮）。判据仍是第 6 章那条：**是否每次状态转移都被 DBMS 强制**。
- **给工程的一条硬规矩（来自 🔧）**：把 `PRAGMA foreign_keys = ON` 写进连接初始化并在集成测试里断言之，否则 SQLite 库里的"外键"只是文档；同理，任何使用延迟约束的路径都要处理 `COMMIT` 失败后事务仍开着的状态（🔧 A16）。
- **深浅分工**：本章只做"SQL 给了哪几种约束、各自漏在哪"；**在 SQL 里把这些约束用对**（NULL 反噬、外键误删、唯一性与并发的写法）见 [../SQL_and_Relational_Theory/10-约束的声明式力量.md](../SQL_and_Relational_Theory/10-约束的声明式力量.md)；**按模型做设计**（码/范式/分解）在 Date 三部曲的方法论层——同波 [#8 `Database_Design_and_Relational_Theory`](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md)（已落盘；见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 的互链义务登记，波尾闭环）。
