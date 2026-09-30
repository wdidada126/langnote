# 01 关系模型与 SQL 基础（⚠️ 推定重构章 · 对应原书"Part I"主题域）

> 章名与章号为 ⚠️ 主题重构（见 [00 §二降级声明](00-总览与阅读地图.md)）；本章承载 Oracle Essentials 系列历来开篇的"DBMS→关系模型→SQL"三件套。Oracle 行为一律 ⚠️ 转述；🔧 均为 SQLite/DuckDB 类比实测，非 Oracle。

## 1. 本章在全书中的位置

- 导游册的第一段：先建立"数据库管理系统是什么、关系模型给了什么承诺、SQL 是哪种方言"的公共语言，后面的存储/实例/工具章全部使用这套词汇。
- 本系列立场：这一章是全书**最能与开源引擎互相印证**的一章——SQL 标准是共同地基，故 🔧 实验密度高。
- 阅读时长定位：本目录把原书"开篇一揽子"拆成厚薄最均匀的一章，为 02/03 的硬核分层图预留术语。
- 与盘上中文册的起点差异：[Oracle_11g管理与编程基础.md](../Oracle_11g管理与编程基础.md) 从安装讲起，导游册从"为什么需要 DBMS"讲起——两种开篇哲学在此分岔。

## 2. DBMS：从文件系统到数据库管理系统（⚠️ 转述）

- 传统动机四件套：数据独立性（物理/逻辑两层）、并发控制、恢复能力、声明式查询；导游册会用"电子表格/文件堆 vs DBMS"的对照讲。
- DBMS 组件鸟瞰：存储管理器 + 查询处理器 + 事务管理器 + 目录（dictionary/catalog）——本书 02/03/04/05 章即按此骨架展开。
- 事务 ACID 四性在第一章只点名，落点分散到后章：持久性→02/03 章 redo，隔离性→05 章一致性读，原子性→回滚段（02 章 UNDO）。
- 数据库管理员的职能边界（开发者视角 vs DBA 视角）是本系列一贯的"给开发人员看的 DBA 书"定位来源 ⚠️。
- 三级模式/两级映射（外模式-概念模式-内模式）在导游册里通常只出现一张图，但它是"数据独立性"承诺的机制注脚（本目录补讲）。
- 🔧 一句话反例感：用裸文件+CSV 做"转账"要自己处理半写损坏；SQLite 单文件库开 WAL 后崩溃可恢复（见 [09 章 T15](09-高可用集群与Oracle产品版图.md)）——"恢复能力"承诺的最小可测形态。

## 3. Oracle 谱系与企业级特征（⚠️ 转述）

- 版本线：Oracle V2→V6→V7（SQL 声明式主流化）→8/8i→9i→10g/11g→12c→…；"g/c"后缀含义（grid/cloud）成书于 12c 时代的册子通常会解释 ⚠️。
- 导游册会强调的"Oracle 与众不同"清单（都是后续章的预告）：表空间分层（02 章）、SGA/后台进程（03 章）、Net Services 连接模型（04 章）、字典+动态视图双目录（05 章）、数据仓库血统（07/08 章）、RAC 共享磁盘集群（09 章）。
- ⚠️ 作者/副标题存疑（11g vs 12c，见 00 §一），故本章不声称"书中如何描述某一具体版本"。

## 4. 关系模型要点（通用知识 ⚠️ 转述 + 🔧 印证）

- 关系=元组集合（无序、无重复承诺）；域=原子类型；键=超键/候选键/外键的约束链。
- 关系代数八操作（选/投/并/差/积/连接/除/重命名）是 SQL 查询优化的形式基础——这正是 [Cost_Based_Oracle_Fundamentals/00](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md) 全册的工作语言。
- 🔧 **类比实验 A：SQLite 并不强制"关系纯度"**（非 Oracle 行为）。Python：
  `sqlite3.connect(":memory:")` 后 `CREATE TABLE t(a INTEGER); INSERT INTO t VALUES('text')` 成功——SQLite 动态类型亲和性允许违例；Oracle 的强类型检查（⚠️ 转述：ORA-00932 类）是"承诺更硬"的一侧。
- 🔧 **类比实验 B：DuckDB 接近声明式集合语义**（非 Oracle 行为）：`SELECT DISTINCT` 实测返回纯去重集合；目录层关系性可用 information_schema 查询复现（exp2.py G3.3）。

## 5. ANSI/ISO SQL 与 Oracle SQL 方言（⚠️ 转述）

- 标准演进（SQL-87/92/99/2003/2011/2016）与"所有商用引擎都只是符合子集"是导游册的标准口径 ⚠️。
- 方言差异清单（Oracle 侧 ⚠️ 转述，SQLite/DuckDB 侧 🔧）：
  - 行数限制：Oracle `FETCH FIRST n ROWS ONLY`（12c 起）/此前 ROWNUM；🔧 SQLite 原生 `LIMIT`，DuckDB 两者皆通——本次实测 DuckDB `range(50000)` 集合生成 + 聚合输出（exp2.py G5.2，31.2ms）。
  - 连接语法：ANSI `JOIN...ON` vs 旧式 `(+)` 外连接方言 ⚠️；🔧 SQLite/DuckDB 均只走 ANSI JOIN（G5.2 星型查询 USING(store_id) 实测通过）。
  - 伪列/序列：Oracle SEQUENCE+NEXTVAL 模型 ⚠️；🔧 SQLite 用 `INTEGER PRIMARY KEY` 自增别名 rowid，DuckDB 有 `generate_series()`——两种"代替代序"设计对照。
- PL/SQL 一句话定位：过程化扩展（游标/异常/包），与 SQLite 无存储过程（🔧 只有触发器子集）形成纵深差。

## 6. 🔧 实验最小复现代码（SQLite 3.45.3 / DuckDB 1.5.5；非 Oracle）

```python
import sqlite3
s = sqlite3.connect(":memory:")
s.execute("CREATE TABLE t(a INTEGER)")
s.execute("INSERT INTO t VALUES('text')")     # 🔧 成功：类型亲和性违例
s.execute("PRAGMA table_info(t)").fetchall()  # 🔧 目录里类型仍记 INTEGER

import duckdb
d = duckdb.connect()
d.execute("SELECT r FROM range(10) tbl(r) LIMIT 3").fetchall()  # 🔧 集合生成+限制
```

- 观察 1：SQLite 的"记录类型≠声明类型"是"域约束弱化"的活标本；Oracle 同类插入预期报类型错 ⚠️ 转述。
- 观察 2：DuckDB `range()` 表函数一步生成序列集；Oracle 谱系里对应物是 `ROWNUM`/`CONNECT BY LEVEL`/12c `FETCH FIRST` ⚠️。
- 观察 3：两开源引擎都没有本书 05 章那种"静态字典+动态性能视图"双目录纵深——差距到 05 章才拉开。

## 7. 为什么导游册要把 SQL 放在开头（本目录解读）

- 后文一切"结构"话题都靠 SQL 表达：表空间=CREATE TABLESPACE 语句背后（02 章）、字典=SELECT * FROM DBA_*（05 章）、并行=ALTER...PARALLEL（08 章）。
- 对已读 [#23 CBOF](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md) 的读者：本章是其"基数估算→物理代价"链条的最上游；关系代数改写（[CBOF/09-查询变换.md](../Cost_Based_Oracle_Fundamentals/09-查询变换.md)）的每条规则都源自此处代数。
- 对性能线：SQL 方言/绑定变量习惯直接决定 [#42 TOP 12 解析章](../Troubleshooting_Oracle_Performance_2e/12-解析.md) 的硬解析风暴与否 ⚠️。

## 8. 本章一页结构（背这页=带走本章）

- DBMS 四承诺：独立性 / 并发 / 恢复 / 声明式。
- 关系纯度阶梯：数学关系 → SQL 表（允许序与重复的实用妥协）→ 方言细节。
- Oracle 独特叙事预告位：表空间(02)、SGA/进程(03)、连接(04)、双目录(05)、工具(06)、仓库(07/08)、集群(09)。
- 标准 vs 方言三战场：行数限制 / 连接语法 / 序列与伪列。
- 附加战场两条：类型系统强弱（🔧 亲和性反例）与过程语言有无（PL/SQL vs 无）。
- 动线建议：本章读完接 [02 章](02-物理存储结构与表空间.md)；SQL 纵深去 [SQL系列·总索引](../SQL系列·总索引.md)。

## 9. 自测（能复述=过关）

1. 说出 DBMS 相对文件系统的四条根本承诺，并各给一个 Oracle/SQLite 实现深浅差异。
2. 关系代数八操作里，哪三个是优化器重写的主力？各自在 SQL 中对应什么子句？
3. Oracle 行数限制语法 11g/12c 差异是什么？🔧 SQLite/DuckDB 各用什么？
4. "所有引擎只符合 SQL 标准子集"——各举 SQLite 与 DuckDB 的一个不符合点（SQLite：外键默认不强制；DuckDB：存储过程缺位 ⚠️ 转述级）。
5. 🔧 实验 A 里插入成功的根本原因是什么？Oracle 预期行为（⚠️）为何不同？
6. 本章哪些结论来自 🔧、哪些来自 ⚠️？混用会犯什么错？
7. 把"导游册预告位"七个括号里的章号默写一遍，并各配一个关键词。

## 10. 本章互链登记（写前已验目标存在）

- → [00 §三谱系表](00-总览与阅读地图.md)：Oracle 线六册分工与本波兄弟登记。
- → [#23 CBOF 00](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)、[CBOF/09 查询变换](../Cost_Based_Oracle_Fundamentals/09-查询变换.md)。
- → [#42 TOP/12 解析](../Troubleshooting_Oracle_Performance_2e/12-解析.md)。
- → [SQL系列·总索引](../SQL系列·总索引.md)：SQL 方言纵深各册。
- → [论文线 db.md](../../db/db.md)：关系模型与 SQL 标准化史（Codd 谱系按该线索引，⚠️ DOI 未校验不引）。

## 核心概念速览（中英对照）

- **DBMS** — Database Management System：以并发/恢复/独立性换取文件堆自由度的系统软件。
- **数据独立性** — Data Independence：应用不因物理/逻辑结构变更而重写。
- **三级模式** — Three-Schema Architecture：外/概念/内模式+两级映射的独立性机制。
- **关系** — Relation：无序、不重复的元组集合，表的数学原型。
- **域/原子性** — Domain：列取值集合与其类型约束。
- **候选键** — Candidate Key：极小超键；选一个做主键。
- **外键** — Foreign Key：跨关系引用完整性约束。
- **关系代数** — Relational Algebra：查询优化重写规则的形式语言。
- **方言** — Dialect：SQL 标准之上各引擎的非兼容增量（ROWNUM/亲和类型等）。
- **PL/SQL** — Procedural Language/SQL：Oracle 过程化扩展（⚠️ 本书语境转述）。
- **类型亲和性** — Type Affinity：SQLite 特有的"尽力而为"类型制度（🔧 实测项）。
- **导游册** — Guided Tour Book：本书体裁——广度优先、单章即地图一格。
- **ACID** — Atomicity/Consistency/Isolation/Durability：事务四承诺，后章各自落地。
- **rowid** — SQLite 自增别名：🔧 无序列引擎对 Oracle SEQUENCE 的替代形态。
- **选择度** — Selectivity：谓词过滤比例的度量词，[02 章](02-物理存储结构与表空间.md)起高频。
- **声明式** — Declarative：说"要什么"不说"怎么拿"——SQL 的第一承诺。

## 最新演进与工业实践

- **SQL 标准现状**：SQL:2016 之后工业主流引擎（含 Oracle 19c/23ai）的差异化战场已移向 JSON 半结构化、向量检索、细粒度权限；本书"方言清单"式讲法在 2020 年代多被各引擎 compatibility mode 吸收 ⚠️ 转述。
- **23ai 增量**：JSON 关系表双格式、AIVector 类型等进入 Oracle 主线 ⚠️ 转述（docs.oracle.com 本次无法 curl 校验，故只述不引 URL）；在盘 [Pro_Oracle_23ai_Administration](../Pro_Oracle_23ai_Administration/00-总览与阅读地图.md) 已覆盖操作侧。
- **开源对照（🔧 现行）**：SQLite 以"嵌入式 SQL 子集+强兼容承诺"成为事实基准；DuckDB 走"分析方言全家桶"路线——两者与 Oracle 的差距仍主要在过程语言、目录纵深与企业权限 ⚠️。
- **教学实践**：2024–2026 数据库课程普遍用 SQLite/DuckDB 讲关系代数与 SQL（零运维），本书第一章的课堂职能已被开源引擎接管；Oracle 独有叙事收缩到体系结构/集群/多租户 ⚠️ 类比。
- **论文线**：关系模型史与 SQL 标准化史按 [../../db/db.md](../../db/db.md) 索引检索；本波网络受限，未做 Crossref 校验，凡涉论文仅给检索方向、不给 DOI ⚠️。
