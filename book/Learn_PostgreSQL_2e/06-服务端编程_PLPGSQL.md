# 06 · 服务端编程：PL/pgSQL 与函数/过程（原书第 7 章）

> 对应原书 Ch7 *Server Side Programming*（✅ 章题）。
> 实证 ✅：`CHAPTER_07/code/chapter7.sql`（9.4KB 实抓）——`CREATE OR REPLACE FUNCTION`×16、`plpgsql`×12、`RAISE`×2、`SECURITY DEFINER`×1：本章以 PL/pgSQL 函数为中心，兼及过程与安全定义符。
> 权威 ✅ https://www.postgresql.org/docs/current/plpgsql.html 、https://www.postgresql.org/docs/current/plpgsql-control-structures.html 。

## 1. 函数 vs 过程：SQL 与 PL 两层语言（⚠️+✅）

- 四象限骨架（✅ https://www.postgresql.org/docs/current/sql-createfunction.html 与 https://www.postgresql.org/docs/current/sql-createprocedure.html 均 200 已验）：
  - `LANGUAGE sql`：简单委托/表达式包装，无控制流；
  - `LANGUAGE plpgsql`：块结构、变量、IF/LOOP、异常——本章主场；
  - 函数 `RETURNS ...` 可嵌表达式；过程 `CREATE PROCEDURE`+`CALL`（PG 11+）可在体内 `COMMIT/ROLLBACK` ⚠️。
- PL/pgSQL 是**扩展而非内建语言**（⚠️+✅ plpgsql.html 开篇"extension"定性）——此身份直连 Ch12 扩展生态（[09-扩展生态.md](09-扩展生态.md)）：同机制、同目录。
- 书风格示例多为 forumdb 业务函数（标题规范化、计数联动一类 ⚠️ 重构推断），`RAISE NOTICE/EXCEPTION` 承担调试输出（✅ 实证×2）。

## 2. 参数、返回与集合值函数（⚠️+✅）

- 参数模式：`IN/OUT/INOUT/VARIADIC`（✅ sql-createfunction 页）。
- 集合出口三式：
  - `RETURNS TABLE(a int, b text)` + `RETURN QUERY SELECT ...`（SRF 当表查）；
  - `RETURNS SETOF`；
  - 多态 `anyelement/anyarray`（通用工具函数）⚠️+✅ https://www.postgresql.org/docs/current/functions-srf.html （200 已验）。
- 美元引用 `$$ ... $$` 免转义（✅ plpgsql.html）；`$tag$` 嵌套。

## 3. 易变性契约与 SECURITY DEFINER（本章技术深水区 ⚠️+✅）

- `IMMUTABLE / STABLE / VOLATILE` 是给优化器的契约：
  - IMMUTABLE 才可进表达式索引/生成列（→ [03-基础语句_DDL与DML.md](03-基础语句_DDL与DML.md) 第 5 节、[10-查询调优索引与性能.md](10-查询调优索引与性能.md) 表达式索引）；
  - 误标=静默腐蚀物化视图与索引 ⚠️+✅（sql-createfunction 页警告段）。
- `SECURITY DEFINER`×1（✅ 实证）：体内外动作一律以**函数属主**权限执行——提级利器：
  - 铁律一：体内第一行 `SET search_path = pg_catalog, ...`（防对象名劫持）⚠️；
  - 铁律二：最小属主（别拿超管当函数属主）⚠️；
  - 官方安全 FAQ ✅ https://www.postgresql.org/support/security/ （200 已验）。
- `STRICT`（NULL 短路）与 `PARALLEL SAFE/UNSAFE` 点到 ⚠️+✅ sql-createfunction。

## 4. 异常块与"没有自治事务"（⚠️+✅）

- `BEGIN ... EXCEPTION WHEN others THEN ... END` 子块=隐式保存点：**捕获即回滚子块全部写入**，热路径高代价 ⚠️+✅（plpgsql-control-structures.html ✅200）。
- PG 无 Oracle 式自治事务 ⚠️：日志表独立提交的惯用替代=
  - 拆成独立连接/dblink 通道（⚠️）或
  - 过程+外层循环逐条 CALL 提交（PG 11+ 正解 ⚠️+✅ sql-createprocedure）。
- `SQLSTATE`/`GET DIAGNOSTICS` 错误采集 ⚠️+✅。

## 5. 🔧 类比实测：嵌入式引擎的"服务端"能走多远（duck5.out / sq 系 🔧，非 PostgreSQL 行为）

**DuckDB 1.5.5：有宏、无 PL——**

```text
> CREATE MACRO add4(x) AS x+4        # 成功（表达式级宏）
> SELECT add4(3)                     -> [(7,)]
> CREATE FUNCTION f() RETURNS INT AS $$ SELECT 9 $$ LANGUAGE plpgsql
  Parser Error: syntax error at or near "RETURNS"     # 拒绝 PG 式过程语言
```

**Python sqlite3 3.45.3：函数活在宿主进程里——**

```python
>>> sc.create_function("tri", 1, lambda x: x*3)
>>> sc.execute("SELECT tri(7)").fetchone()   # (21,)
>>> sc.execute("CREATE FUNCTION ...")         # near "FUNCTION": syntax error
```

三层结论 ⚠️：
1. DuckDB 宏=参数化表达式视图，无游标/异常/控制流；
2. SQLite UDF 生命周期=连接（跨会话不可见、不可 GRANT）；
3. PG 函数是**目录对象**（pg_proc）：持久、可授权、可 SECURITY DEFINER——"服务端编程"一词只在 PG 成立（✅ plpgsql.html）。

## 6. 与其他册分工

- 管理册的服务端视角：[../Mastering_PostgreSQL_Administration/04-服务器管理_模式用户与权限.md](../Mastering_PostgreSQL_Administration/04-服务器管理_模式用户与权限.md)；
- 配方册函数/自动化：[../PostgreSQL_16_Administration_Cookbook/02-表数据与psql自动化.md](../PostgreSQL_16_Administration_Cookbook/02-表数据与psql自动化.md)；
- SECURITY DEFINER 完整权限图 → [08-安全权限与事务MVCC.md](08-安全权限与事务MVCC.md)；触发器=特殊 PL 函数 → [07-触发器规则与分区.md](07-触发器规则与分区.md)。

## 7. 本章自测（重构版；题目自拟 ⚠️）

1. **问**：函数与过程的 PG 分界？**答**：过程可 CALL、可体内管事务（PG 11+）；函数可嵌表达式。
2. **问**：IMMUTABLE 乱标会怎样？**答**：表达式索引/物化视图被错误结果污染且不自愈 ⚠️。
3. **问**：SECURITY DEFINER 两大护身符？**答**：锁 search_path + 小权限属主 ⚠️。
4. **问**：EXCEPTION 块为何昂贵？**答**：每捕获=一次隐式回滚到保存点。
5. **问**：想要"函数里偷偷提交"怎么办？**答**：PG 无自治事务——外层过程逐条 CALL 提交 ⚠️。

## 8. PL/pgSQL 调试与性能实务（⚠️ 书外延伸+✅ 文档锚点）

- **RAISE 级别族**（✅ https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html ）：`DEBUG/LOG/INFO/NOTICE/WARNING/EXCEPTION` 六级——`NOTICE` 默认回客户端、`WARNING` 进日志+客户端、`EXCEPTION` 中止事务 ⚠️。
- **GET DIAGNOSTICS**（✅ plpgsql-control-structures 页）：`GET DIAGNOSTICS cnt = ROW_COUNT;` 取上一条语句影响行数——审计/批量操作反馈必备。
- **动态 SQL**：`EXECUTE format('SELECT * FROM %I WHERE id=$1', tbl_name) USING rec.id;`——`%I` 标识符引用自动加引号防注入（✅ plpgsql 动态命令节）。
- **性能守则** ⚠️：
  - PL/pgSQL 函数体首次执行后**编译为字节码**缓存在 `pg_proc.prosrc` 解析后的计划中——但每会话独立编译（不跨会话共享 ⚠️）；
  - 避免在循环内做单行 SELECT——改用 `FOR rec IN SELECT ... LOOP`（✅ 游标 FOR 循环）减少往返；
  - `PERFORM` 丢弃结果执行语句（替代 `SELECT ... INTO` 弃值 ⚠️+✅）。

## 9. 游标与集合操作的精细控制（⚠️+✅）

- **显式游标**（✅ plpgsql-control-structures 页 cursors 节）：`OPEN cur FOR SELECT ...; LOOP FETCH cur INTO rec; ... END LOOP; CLOSE cur;`——大数据集逐行处理。
- **游标变量与 refcursor**：函数返回 `refcursor`，调用方在事务内 `FETCH`——分页/流式导出惯用法 ⚠️。
- **RETURN QUERY vs RETURN NEXT**：前者一次返回整个查询结果集、后者逐行拼装——大数据集 RETURN NEXT 可控内存但代码更长 ⚠️。
- 🔧 DuckDB 1.5.5 无游标概念（🔧 非 PostgreSQL 行为）；SQLite 宿主 API 有 `sqlite3_step` 逐行取但 SQL 层无游标语句（🔧）。

## 10. 过程的事务控制细节（PG 11+ ⚠️+✅）

- `CREATE PROCEDURE` 体内可用 `COMMIT/ROLLBACK`（✅ sql-createprocedure 页）——函数内**不允许**（函数整体在一个事务里）。
- 事务控制限制 ⚠️：
  - 不能在 `DO` 块内 COMMIT（`DO` 走函数规则 ⚠️）；
  - 过程内 COMMIT 后当前事务结束、新隐式事务开始——后续语句在新事务里；
  - 异常处理块（`EXCEPTION`）内**不可** COMMIT/ROLLBACK ⚠️+✅。
- 调用语法：`CALL proc_name(args);`（不是 `SELECT` ⚠️——新手常犯错误）。

## 核心概念速览（中英对照）

1. **PL/pgSQL** — 过程语言扩展：块/变量/控制流/异常。
2. **函数/过程** — function vs procedure：返回值可嵌 vs CALL+事务。
3. **美元引用** — dollar quoting：$$ 包裹体。
4. **RETURNS TABLE / RETURN QUERY** — 集合返回函数（SRF）。
5. **易变性** — volatility：IMMUTABLE/STABLE/VOLATILE 优化器契约。
6. **SECURITY DEFINER** — 属主身份执行：提级面+护栏两件套 ⚠️。
7. **SECURITY INVOKER** — 默认调用者身份：最小权限基线。
8. **异常块** — EXCEPTION section：捕获即回滚子块。
9. **自治事务之无** — no autonomous transaction：以过程外提替代。
10. **VARIADIC/STRICT** — 可变参/NULL 短路修饰。
11. **pg_proc** — 函数目录：持久对象的身份证。
12. **MACRO** — DuckDB 宏：嵌入式的"服务端编程"下限 🔧。

## 最新演进与工业实践

- **版本增量** ⚠️+✅：PG 11 过程+事务控制是分水岭（同批引入 `PIPE ROW` 集合拼装）；12-16 打磨 PL 细节（调用栈行号、foreach 数组等 ✅ plpgsql-control-structures 持续演进）；17/18 无破坏性语言变更（✅ release 17.0/18.0 页通读转述 ⚠️）。
- **多语言矩阵**：PL/Python、PL/V8、PL/Rust 经扩展体系接入（→ [09-扩展生态.md](09-扩展生态.md)）；生产常见=PL/pgSQL 干 DBA 活、外部语言只留给算法段 ⚠️。
- **安全审计**：DEFINER+可变 search_path 是教科书提级链；CI 静态扫（pgllint 类 ⚠️）+评审清单两条腿。
- **架构边界共识** ⚠️：2020s 社区主流"业务逻辑上移应用层，PL 只留批量维护/DDL 编排"——本书"服务端编程"章今日读法是**运维自动化 DSL** 而非应用架构。
