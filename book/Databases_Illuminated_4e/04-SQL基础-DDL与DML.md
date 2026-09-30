# 04 SQL 基础：DDL 与 DML

> 单元性质：⚠️ 主题重构。对应教材通行"SQL: Introduction / Data Definition & Manipulation"单元。深度对照：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)；中文应试对照：../数据库系统概论.md 第 3 章；SQLite 方言专册：[../The_Definitive_Guide_to_SQLite_2e/03-SQL基础.md](../The_Definitive_Guide_to_SQLite_2e/03-SQL基础.md)。

## 1. SQL 的四翼与本单元边界

DDL（CREATE/ALTER/DROP）、DML（INSERT/UPDATE/DELETE）、DQL（SELECT）、DCL（GRANT/REVOKE，本册在 12 章）。教材式学习法：一切语法都回答两个问题——**对模式做什么**（DDL）与**对实例做什么**（DML/DQL）。SQL 是声明式语言：标准只约定语义，方言（dialect）差异交给引擎——本目录实测用 SQLite 3.45.3 与 DuckDB 1.5.5（环境见 00 第五节）。

## 2. DDL：建表就是装订契约

- **CREATE TABLE**：列定义 + 表级约束；数据类型选标准族（INTEGER/REAL/TEXT/DECIMAL/DATE），SQLite 的亲和性（affinity）与 DuckDB 的严格静态类型是两极（../Using_SQLite/06-SQLite数据类型.md）。
- **约束位置学**：列级（CHECK(salary >= 0)）与表级（PRIMARY KEY(dept_id)）——教材强调"何时必须表级"：复合键、跨列 CHECK。
- 日期与时间：标准 SQL 的 DATE/TIME/TIMESTAMP 在 SQLite 中并不存在独立存储类型（以 TEXT/REAL/INTEGER 亲和存之），DuckDB 则有完整 DATE/TIMESTAMP 族——🔧 exp4 的 sales 表以 `day INTEGER`（20200101 形态代理日期）落库，正是为绕开这一方言裂口的刻意选择，跨引擎对照教学请优先读 ../Using_SQLite/06-SQLite数据类型.md。
- **ALTER 的现实**：标准说可改一切；SQLite 直到 3.35+ 才支持 DROP COLUMN，改类型仍需建新表搬数据（⚠️ 版本细节以其 changelog 为准）；DuckDB 的 ALTER 支持面更宽但无跨会话系统目录锁。
- **DROP 的三种姿势**：DELETE（行）/DROP COLUMN（结构）/DROP TABLE（对象），级联破坏性由 RESTRICT/CASCADE 语义决定。

## 3. 🔧 exp1：约束违约的实录语料（DDL+DML 一体两面）

方法：`D:\develops\tmp\dbwave_w7_dbill\exp1_ddl_dml.py`，教学库三表（department/instructor/course），instructor.dept_id 外键 `ON DELETE SET NULL`，salary CHECK >=0，credits CHECK BETWEEN 1 AND 6，逐条试探：

| 试探 | 🔧 实测输出（SQLite 3.45.3） |
|---|---|
| 重复主键 INSERT | `UNIQUE constraint failed: department.dept_id` |
| 插入 dept_id=99（不存在） | `FOREIGN KEY constraint failed` |
| 插入 salary=-5 | `CHECK constraint failed: salary >= 0` |
| DELETE 被引部门（SET NULL） | Bob 的 dept_id → None，部门删除成功 |
| UPDATE instructor SET salary*1.1 WHERE dept_id=1 | rowcount=2（Alice/Carol 命中） |

教学结论：① SQLite 对 PRIMARY KEY 违约报的是 **UNIQUE** 约束错（PK 由唯一索引实现，见 07 章 exp4 的 index_list）；② 外键须 `PRAGMA foreign_keys=ON` 才执法——教材默认行为与引擎默认不一致的头号现场。

## 4. DML：三动词的细节分层

- **INSERT**：值表/默认值/多行批量（executemany 才是应用常态）；SQLite 的 `INTEGER PRIMARY KEY` 自动充当 ROWID 别名——隐式自增的方言彩蛋 ⚠️ 非标准行为。
- **UPDATE**：`SET salary = salary * 1.1` 的右侧先于左侧求值；**缺 WHERE 是全表**——教材的"死刑句"警告在本目录实测为 rowcount 直读。
- **DELETE**：无行条件即清空；不回退 AUTOINCREMENT 计数器（方言细节 ⚠️）。
- **TRUNCATE 不存在于 SQLite 标准面**：DELETE 全表+VACUUM 是替代姿势（../Using_SQLite/07-建表约束与Pragmas.md）。

## 5. DQL 入门骨架：SELECT—FROM—WHERE

逻辑求值序 FROM→WHERE→SELECT 与书写序相反；谓词比较覆盖 =,<>,LIKE,GLOB(In 方言),IS NULL,BETWEEN,IN。教材的"元组变量"即 SQL 别名（FROM instructor AS i）。ORDER BY 只属查询层不属关系层——关系无序（03 章）的再次体现。

## 6. 数据装载与导出（实践翼）

Python `sqlite3.executemany` + CSV 流式装载；DuckDB `read_csv_auto` 一步建表（🔧 exp5 用 `range(1000000)` 直接造百万行演示）。教材附录传统上用 MySQL/Access 演示导入向导 ⚠️ 具体附录不可证；本目录以脚本替代。

## 7. 与概念6/王珊的写法差异速记

- 概念6 用 university 示例（student/instructor/takes/course）——本目录 exp1 三表即其骨架简化。
- 王珊册把"数据更新+数据查询"合并为"SQL 的 DML"一大节，考试表述以它为准；本书（及本目录）按 DDL/DML/DQL 三分，便于挂 🔧 实验。

## 8. 常见错误清单

1. WHERE 里写 `col = NULL`（03 章三值逻辑）。
2. 忘开 `PRAGMA foreign_keys` 就断定"外键没起作用"。
3. UPDATE 忘 WHERE 后直接 COMMIT（09 章 ROLLBACK 是唯一后悔药；🔧 exp3 实测回滚保住了 v=10）。
4. 把 `DROP COLUMN` 当成跨引擎可用（SQLite 版本线）。
5. 用行级 INSERT 循环而不用 executemany——性能差一个数量级（🔧 exp4 装载 30 万行即批量法）。

## 9. 小结

至此获得"把模式与实例都写对"的能力。下一单元把 SELECT 推进到连接/嵌套/聚合的完整表达力（05），再往后才是"把表设计对"（06）。

## 10. 补充：exp1 逐行讲解（可直接上机复现）

脚本 `D:\develops\tmp\dbwave_w7_dbill\exp1_ddl_dml.py`（🔧 2026-10-01，SQLite 3.45.3/Python 3.13.2）。关键行逐条：

```python
con.execute('PRAGMA foreign_keys=ON')      # 外键执法开关，忘开=白建
... REFERENCES department(dept_id) ON DELETE SET NULL  # 违约处置=置空
con.executemany('INSERT INTO instructor(name,dept_id,salary) VALUES(?,?,?)', [...])  # 占位符批量
```

观察点排序：① 先跑"好路径"（三表插入成功、commit）；② 再逐条触发三类违约，把报错原文抄写归类；③ 最后做破坏性实验（DELETE 被引行）看 SET NULL 生效。教学价值：**报错文本是约束存在性的证据**——学生第一次建立"约束=可执行对象"的直觉。

## 11. 补充表格：DDL 对象清单（教材口径→本目录可测性）

| 对象 | 用途 | SQLite 可测 | DuckDB 可测 |
|---|---|---|---|
| TABLE/VIEW | 基本结构 | ✅ | ✅ |
| INDEX | 07 章 | ✅ | 部分（自动 ART 索引为主 ⚠️） |
| TRIGGER | 过程性约束 | ✅ | ❌（无用户触发器） |
| SEQUENCE | 生成器 | 自增 ROWID 替代 | ✅ |
| DOMAIN | 03 章域 | ❌ | ❌ |
| SCHEMA | 命名空间 | ATTACH 近似 | ✅ |

这张"功能矩阵"本身就是教材 DDL 章最好的补充读物：标准语法的每个对象都有引擎投票它是否活着。

## 12. 自测五问（含参考答案要点）

1. 为什么 INSERT 一条 CHECK 违约行时报错文本带约束表达式？（引擎把 CHECK 原样入目录，便于定位——自描述原则。）
2. `DELETE FROM t` 与 `DROP TABLE t` 差异三点？（行级 DML 可回滚 vs 结构级 DDL；索引/权限/依赖随表消失；外键引用方变悬挂被拒或级联。）
3. SQLite 里 `PRAGMA foreign_keys` 是连接级还是库级？（连接级——新连接要重设，应用池初始化的常见事故点。）
4. UPDATE 加别名 `UPDATE t SET ... WHERE EXISTS(...)` 合法吗？（合法：WHERE 可含子查询，但 SET 左侧不可用别名引用外关系——方言差异小。）
5. DDL 在事务里能回滚吗？（SQLite/DuckDB 支持事务性 DDL；MySQL 家族隐式提交 ⚠️ 转述——"方言雷区"首选案例。）

## 13. 延伸阅读与复现清单

- 完整复跑：`python D:\develops\tmp\dbwave_w7_dbill\exp1_ddl_dml.py`（🔧 无外部依赖，标准库即可）。
- SQLite 方言边界：../Using_SQLite/07-建表约束与Pragmas.md（约束与 PRAGMA 的权威中文笔记）。
- 类型系统两极：../Using_SQLite/06-SQLite数据类型.md ↔ DuckDB 文档的类型表。
- 服务器家族对照（教材原教旨语法）：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md) 的 university 示例建表清单。

## 核心概念速览（中英对照）

- **DDL / DML / DQL / DCL** — 四翼：定义/改动/查询/控制
- **CREATE TABLE** — 建表：列+约束的契约装订
- **table-level vs column-level constraint** — 表级/列级约束：复合键必须表级
- **CHECK constraint** — 检查约束：域内合法性谓词
- **DEFAULT** — 默认值：缺省列填充
- **ALTER TABLE** — 改表：方言支持面差异最大的 DDL
- **DROP (DELETE/TRUNCATE 之辨)** — 删除三个层级：行/列/表
- **executemany** — 批量插入：应用侧 DML 正姿
- **WHERE 谓词族** — 谓词：=/<>/LIKE/BETWEEN/IN/IS NULL
- **ORDER BY 非关系算子** — 排序属查询层：关系本身无序
- **type affinity / static typing** — 类型亲和 vs 严格类型：SQLite 与 DuckDB 两极
- **INTEGER PRIMARY KEY ≡ ROWID** — SQLite 彩蛋：隐式自增别名
- **read_csv_auto** — DuckDB 自动装载：脚本化 ETL 入口

## 最新演进与工业实践

- **SQLite 现状（3.45–3.5x，2024–2026）**：RETURNING（3.35+）成为教材 INSERT 章节新宠；JSON 函数（05/14 章用到）稳定化；STRICT 表收紧动态类型 ⚠️ 逐版本行为以 sqlite.org 变更日志为准，本目录未逐版实测。
- **DuckDB 作为教材第二引擎**：1.x 线以 `range()`、`read_csv_auto`、友好错误信息著称，与 SQLite 组成"事务+分析"双演示面（本目录 exp2/exp5 即双跑对照）。
- **dbt 时代的基础 SQL**：SELECT/INSERT 讨论延伸至模型层 `ref()` 物化，但语法地基仍是本单元四翼（可参 ../Analytics_Engineering_with_SQL_and_dbt 目录）。
- **工业习惯**：生产迁移一律走版本化脚本（Flyway/Liquibase 思路），教材的"直接 ALTER"在生产被禁止——与 12 章变更管控呼应。
