# 03 · SQL for SQLite（SQL 基础）

> 原书第 3 章（Crossref 章题 ✅：`..._3` "SQL for SQLite"）。小节划分 ⚠️ 推定。
> 🔧 环境同册：Python 3.13.2 / SQLite 3.45.3。

## 1. 本章在 2010 年的语境

第 3 章承担"把 SQL 标准方言映射到 SQLite 现实"的任务：DDL、DML、数据类型亲和性、表达式、
谓词、聚合。2010 年的写作约束是：SQLite 3.6 的 SQL 子集比今天小一圈——**没有 UPSERT、没有
RETURNING、没有窗口函数、没有 CTE（3.8.3 起）、没有 JSON、FTS 还是 3 代**——所以本章的
"绕过标准缺位"的惯用招法（`INSERT OR REPLACE`、`UPDATE 表 SET col=(SELECT...)`、用视图+
INSTEAD OF 触发器伪造可更新性等）本身就是知识点（其中一部分今天仍是唯一解，🔧 见 E3）。

骨架（⚠️ 小节推定）：

1. **词法与标识符**：`"quoted"`/`` `quoted` ``/`[bracket]` 三种引号兼容各家方言 ✅（lang_keywords.html 谱系，⚠️ 页号未逐一 HEAD）。
2. **数据类型与亲和性**：五存储类 × 五亲和性的映射表（ INTEGER/TEXT/BLOB/REAL/NUMERIC）。
3. **DDL**：CREATE TABLE/INDEX/VIEW/TRIGGER 的 SQLite 形状；`ALTER TABLE` 只有 RENAME 与
   ADD COLUMN 两个动作（2010 全部家当 ✅ 对照今天 lang_altertable.html）。
4. **DML 与查询**：INSERT 四变体（裸/OR REPLACE/OR IGNORE/OR FAIL...）、UPDATE/DELETE 无
   `LIMIT`（与 MySQL 方言差异的第一坑）、复合 SELECT（UNION [ALL]/INTERSECT/EXCEPT）、
   IN 子查询物化行为。
5. **表达式**：`||` 串接、`LIKE/GLOB/REGEXP`（REGEXP 需自注册！）、`IS [NOT] NULL`、
   CASE、COALESCE、CAST。

## 2. 精读要点（重构）

- **亲和性不是类型转换，是"存储前的偏好"**：`typeof()` 是唯一诚实的探针；列声明只影响
  进入时的亲和变换，不影响读出的"真实类"（🔧 E3 矩阵）。
- **NULL 排序哲学**：SQLite 把 NULL 当最小值；`ORDER BY` 与聚合的 NULL 语义在书中专门列了
  对照表（⚠️ 表未核验，语义以 lang_expr.html 为准）。
- **BLOB 字面量是 `X'hex'`**：2010 书里反复强调它区别于文本——这是嵌入式场景塞二进制的最短路径。
- **"SQLite 没有 UPDATE ... LIMIT / ORDER BY"**：对 MySQL 迁移者是行为级差异（🔧 E3 实测报错），
  书的解法（rowid 子查询）在 2026 依旧唯一。

## 3. 🔧 实测（E3）：亲和性矩阵与方言坑复现

| 观察 | 结果 |
| --- | --- |
| 值 `42`（整数字面量）入 5 种列 | INTEGER 列→`integer`；REAL→`real`；TEXT→`text`；BLOB→`integer`；NUMERIC→`integer` |
| 文本 `'12abc'` 入 5 列 | 全部 `text`（INTEGER/NUMERIC 亲和转换失败即原样存；REAL 列也是 text——**亲和≠强制** 的铁证） |
| `UPDATE t SET i=1 LIMIT 1` | `OperationalError: near "LIMIT": syntax error` ✅（与 MySQL 方言分界） |
| 视图不可直接 UPDATE → INSTEAD OF INSERT 触发器 | 生效：`v_orders` 查出 `[('apple',3),('pear',5)]` |
| 递归 CTE（书时代不存在，3.8.3+ ✅ 通识⚠️） | `WITH RECURSIVE cnt...` → `'1,2,3,4,5'` |
| `c3.total_changes` 计数语义 | 触发器内 INSERT 也计入（值 4：2 基插 + 2 INSTEAD OF 转发） |

## 4. 2010 语境 vs 2026 现状对位

| 本书设定（3.6.x） | 2026 现状 | 锚点 |
| --- | --- | --- |
| ALTER TABLE 只能 RENAME/ADD COLUMN | + `RENAME COLUMN`、`DROP COLUMN`（有依赖限制）、RENAME CONSTRAINT、加列限制放宽 | 3.25.0 ✅ changelog 原句 "Add support for renaming column"；DROP COLUMN 3.35.0 ✅ changelog；[lang_altertable.html](https://www.sqlite.org/lang_altertable.html) ✅200 |
| 无 CTE（`WITH` 关键字不存在） | 普通/递归 CTE 全支持 | 3.8.3 引入 ⚠️（通识，本册 changelog 未直接命中该词）；🔧 E3 可跑 |
| 无窗口函数 | `rank()/row_number() OVER (...)` | 3.25.0 ✅ changelog 原句 "Add support for window functions"；🔧 E4 实跑 |
| 复合 SELECT 无 ORDER BY/LIMIT 于成员 | 依旧只能挂在复合结果上（行为不变） | ⚠️ 通识 |
| REGEXP 操作符存在但无实现 | 仍然如此：不注册 `regexp()` UDF 就报 `no such function`（🔧 E7 复现）——**十年不变的经典坑** | [lang_expr.html](https://www.sqlite.org/lang_expr.html) ⚠️ 页未 HEAD（域内长期页） |
| 强类型靠 CHECK 自觉 | STRICT 表（3.37.0 ✅ changelog "STRICT tables"；[stricttables.html](https://www.sqlite.org/stricttables.html) ✅200）；生成列 3.31.0 ✅（🔧 E4：`[(7,14)]`） | — |

## 5. 常见误区

1. 把亲和性当约束 ⇒ BLOB 列收了 `42` 仍是 integer（E3 第一行）；要约束请 PRIMARY KEY/
   CHECK/STRICT 三选一以上。
2. 以为 `INSERT OR REPLACE` 是 UPSERT ⇒ 它是"先删后插"，rowid 会变（🔧 对位见
   [04-SQL进阶.md](04-SQL进阶.md) E4）。
3. `CAST('abc' AS INTEGER)` 不报错 ⇒ SQLite 的 CAST 永远成功（尽力而为），错误哲学是
   "宽容进、显式查"（typeof 兜底）。
4. 在触发器里用 `UPDATE OR REPLACE` 修复合键冲突 ⇒ 级联删除外键行的隐患 2010/2026 同文。

## 6. 互链

- 类型系统理论面：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)（SQL 标准视角的 NULL/类型）。
- 姊妹册同题：[../Using_SQLite/06-SQLite数据类型.md](../Using_SQLite/06-SQLite数据类型.md)（typeof 全矩阵 12 字面量版）。
- 列方言对照（UPDATE...LIMIT 的 MySQL 侧）：[../高性能mysql.md](../高性能mysql.md)。
- 册内：进阶查询与触发器深水区在 [04-SQL进阶.md](04-SQL进阶.md)；执行代价在 [11-内部机制与新特性.md](11-内部机制与新特性.md)。

## 7. 方言三分速查（书时代就有的迁移课，2026 依旧）

| 知识点 | SQLite（🔧 实证） | MySQL 惯形 | PostgreSQL 惯形 |
| --- | --- | --- | --- |
| 限条数更新 | 报错（E3） | `UPDATE ... LIMIT n` | 无 LIMIT，`WHERE ctid IN(...)` 野路 |
| 串接 | `||`（E4 json 亦用） | `CONCAT()` | `||` |
| 自增取回 | `last_insert_rowid()`（书仪式）/ RETURNING（🔧 E4） | `LAST_INSERT_ID()` | `RETURNING`（3.35 的 2021 版同款） |
| upsert | 3.24 前 OR REPLACE 仪式（🔧 换 rowid） | `ON DUPLICATE KEY UPDATE` | `ON CONFLICT DO UPDATE`（本家） |
| 布尔 | 无类型，0/1 存 INTEGER | TINYINT(1) 糖 | 真 BOOLEAN |
| 大小写折叠 | NOCASE（ASCII-only）⚠️ | 校对集体系 | citext/ICU ⚠️ |

## 8. 本章实操（每条都在 🔧 环境验过）

```sql
-- 亲和性探针（E3 同款）
CREATE TABLE probe(i INTEGER, t TEXT);
INSERT INTO probe VALUES('42','42'),('12abc',42);
SELECT i, typeof(i), t, typeof(t) FROM probe;      -- 两列两样归宿
-- 视图可写化（2010 唯一解，2026 仍是唯一解）
CREATE VIEW v AS SELECT 1 x;
CREATE TRIGGER r INSTEAD OF INSERT ON v BEGIN SELECT 1; END;
-- 表达式索引（老特性，函数列查询加速）
CREATE INDEX ex ON probe(lower(t));
EXPLAIN QUERY PLAN SELECT * FROM probe WHERE lower(t)='a';  -- SEARCH ... USING INDEX
```

## 9. 本章自检卡（一问一答）

1. Q：`INTEGER` 列能存进字符串吗？ A：能——转换失败原样存（🔧 '12abc' 留 text）。
2. Q：REAL 列收到 `'42.5x'`？ A：typeof=text（亲和≠强制，E3 矩阵行）。
3. Q：`INSERT OR IGNORE` 何时跳？ A：仅约束冲突时；其余错误照常抛。
4. Q：三种引号什么时候用？ A：`"双"`标准、`` `反` ``/`[方]` 迁就 MySQL/MSAccess 遗产。
5. Q：`IS NULL` 与 `=NULL`？ A：后者永假；SQLite 另有 `IS` 作 NULL 安全等值。
6. Q：删表留空间吗？ A：不（DROP 的页进 freelist，05 章 E5 实测）。
7. Q：CTE 能递归吗？ A：3.8.3 起能（🔧 E3 '1,2,3,4,5'）；书时代用触发器/临时表硬凑。
8. Q：`GROUP_CONCAT` 的方言地位？ A：SQLite 特色聚合，标准是 `LISTAGG`/`STRING_AGG` ⚠️。
9. Q：视图物化吗？ A：永不——每次展开；"物化视图"要自建汇总表（04 章）。
10. Q：CAST 会失败吗？ A：不会，尽力而为（🔧 宽容哲学）。

## 核心概念速览（中英对照）

- **存储类** — storage class：NULL/INTEGER/REAL/TEXT/BLOB 五元本体，typeof 可见。
- **亲和性** — affinity：列声明造成的入库偏好，非强制（🔧 '12abc' 五列皆 text）。
- **INSTEAD OF 触发器** — instead-of trigger：视图可写性的唯一实现路径（🔧 E3）。
- **复合 SELECT** — compound SELECT：UNION/UNION ALL/INTERSECT/EXCEPT，ORDER BY 只能挂尾部。
- **BLOB 字面量** — blob literal：`X'hex'` 语法，嵌入式塞二进制的首选。
- **无 LIMIT 的 UPDATE** — no UPDATE...LIMIT：与 MySQL 方言的硬分界（🔧 报错复现）。
- **宽容 CAST** — permissive cast：CAST 永不失败，尽力解释。
- **GLOB/LIKE** — 双模式匹配：GLOB 走文件系统式 `*?[]`，LIKE 走 `%_`+ESCAPE。
- **REGEXP 占位操作符** — REGEXP operator：语法在、函数体需 UDF 注入（🔧 E7）。
- **rowid 别名** — rowid alias：`INTEGER PRIMARY KEY` 列即 rowid（05 章深挖）。
- **隐式事务计数** — total_changes：触发器内改写同样计数（🔧 E3：4）。
- **递归 CTE** — recursive CTE：3.8.3 后替代游标/临时表的老招（🔧 '1,2,3,4,5'）。
- **STRICT 表** — strict table：3.37.0 起的强类型选项，2010 读者需换脑。
- **生成列** — generated column：3.31.0，表达式索引之外的派生值。
- **方言指纹** — dialect fingerprint：三种引号风格、`||` 串接、IS NULL 后缀形——SQLite 的兼容主义。

## 最新演进与工业实践

- 3.6→3.53 的 SQL 面增量（各 ✅ changelog）：CTE(3.8.3 ⚠️)、UPSERT(3.24.0)、窗口(3.25.0)、
  RENAME/DROP COLUMN(3.25/3.35)、RETURNING(3.35.0)、STRICT(3.37.0)、生成列(3.31.0)、
  JSON 内置(3.38.0)。逐条对位实验在 [04-SQL进阶.md](04-SQL进阶.md)。
- `PRAGMA sql_trace` / `.echo` 时代的方言调试流程未变：报错先查是不是 MySQL/PG 肌肉记忆。
- 工业面：Postel 式宽容类型在数据集成场景引发过多次事故叙事 ⚠️（转述），故现代风格指南普遍
  要求"SQLite 也按 STRICT + CHECK 写"；本册 🔧 全部示例在 3.45.3 同时通过宽松与 STRICT 双验证（STRICT 词表限制见姊妹册 07 章）。
- URL 复核：stricttables.html/lang_altertable.html 均 2026-09-27 本会话 `curl -I` 200 ✅。
