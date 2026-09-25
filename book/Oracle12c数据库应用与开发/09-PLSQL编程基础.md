# 09 · PL/SQL 编程基础

> **本章地图**：**PL/SQL 是什么**（过程化语言嵌在 SQL 里，由 **PL/SQL 引擎**执行，与 SQL 引擎的交互代价是核心成本）→ **块结构**（声明段 / 可执行段 / 异常段，`DECLARE ... BEGIN ... EXCEPTION ... END;`）→ **变量与类型**（标量 / 复合 / 参照 / LOB；`%TYPE` 与 `%ROWTYPE`；绑定变量 `:new.x`）→ **PL/SQL 类型体系**（12c 起的布尔标量、`SUBTYPE`、以及 12c 的 `BOOLEAN` 在 SQL 里可用的边界）→ **流程控制**（`IF`/`CASE`/`LOOP` 三族）→ **游标三态**（隐式游标 / 显式游标 / `REF CURSOR`）→ **集合与记录**（索引表、嵌套表、VARRAY；`records`、`TABLE()` 函数）→ **动态 SQL**（`EXECUTE IMMEDIATE` 与 `DBMS_SQL`）→ **异常**（预定义 / 非预定义 / 自定义，`PRAGMA EXCEPTION_INIT`、`RAISE_APPLICATION_ERROR`）→ **`PRAGMA`** 家族（`AUTONOMOUS_TRANSACTION`、`SERIALLY_REUSABLE`、`AUTOMATIC_DML`）。

## 一、核心精讲

> 以下 SQL/PL-SQL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 为什么 PL/SQL 慢：引擎边界

```
┌──────────────────────────────────────────────┐
│  PL/SQL 引擎（在 PGA 里，-process 内）          │
│   ├─ 执行过程化语句（赋值、分支、循环）          │
│   ├─ 执行 SQL 语句  →  调用 SQL 引擎            │  ← 每次跨边界都有开销
│   └─ SQL 引擎执行完后把结果返回给 PL/SQL 引擎    │
└──────────────────────────────────────────────┘
```

**关键认知**：PL/SQL 快在"批量、少次数的 SQL"，慢在"一条一条跑 SQL"。所以：

- **在 PL/SQL 循环里执行 `INSERT`**（每次一次上下文切换）→ 慢；
- **一条 SQL 处理一整批**（`UPDATE ... WHERE` 一次扫一遍）→ 快；
- 折中方案就是 `[`10`](10-PLSQL高级与工程化.md) 里的 **`BULK COLLECT` + `FORALL`**——把"N 次 SQL"合成"1 次 SQL + 1 次绑定"。

### 1.2 块结构（教学示意，不参与构建）

```sql
DECLARE
  v_empno   emp.empno%TYPE   := 7369;      -- %TYPE：跟随列类型
  v_ename   emp.ename%TYPE;
  v_total   NUMBER(10,2)     := 0;
  c_tax     CONSTANT NUMBER  := 0.06;
  TYPE emp_rec IS RECORD (                  -- 自定义记录类型
    empno  emp.empno%TYPE,
    ename  emp.ename%TYPE,
    sal    emp.sal%TYPE);
  r_emp emp_rec;
BEGIN
  SELECT ename INTO v_ename FROM emp WHERE empno = v_empno;
  SELECT SUM(sal) INTO v_total FROM emp WHERE deptno = 20;
  DBMS_OUTPUT.PUT_LINE(v_ename || ' total=' || v_total);
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('no such emp');
  WHEN OTHERS THEN
    IF SQLCODE = -20001 THEN NULL; END IF;
    RAISE;                                   -- 不要吞掉异常
END;
/
```

四条硬规则：

1. **`SELECT ... INTO` 必须返回且仅返回一行**——零行报 `NO_DATA_FOUND`，多行报 `TOO_MANY_ROWS`；
2. **`EXCEPTION WHEN OTHERS` 里至少要 `RAISE` 或记录日志**，否则异常被静默吞掉，故障无从追溯（这是生产上最常见的"程序没报错但数据错了"）；
3. **`COMMIT`/`ROLLBACK` 可以在 PL/SQL 里显式写**，但要意识到它影响的是**整个会话事务**（见 [`04`](04-事务与redo-undo-归档.md)）；
4. **`PRAGMA AUTONOMOUS_TRANSACTION`** 让这段代码在一坨独立的事务里跑——最常用于**记录日志**（主事务回滚时日志仍在）。代价是它**不能再访问主事务未提交的更改**。

### 1.3 变量与类型

| 类别 | 例子 | 说明 |
| --- | --- | --- |
| **标量** | `NUMBER`、`VARCHAR2`、`DATE`、`BOOLEAN`、`CLOB` | 12c 起 `BOOLEAN` 可用于更多地方（但仍不能作为 SQL 表达式的一部分直接用在 SQL 语句里，**直到 23c 才更通用**） |
| **复合** | `RECORD`、`TABLE`（嵌套表）、`VARRAY`、`INDEX BY`（索引表/关联数组） | 索引表是 PL/SQL 里最常用、最接近"字典"的结构 |
| **参照** | `%TYPE`、`%ROWTYPE`、游标变量（`REF CURSOR`） | **强烈建议用 `%TYPE`**，列类型变了不用改代码 |
| **LOB** | `CLOB`/`BLOB`/`NCLOB` | 大对象，注意 `DBMS_LOB` 的操作是独立的 SQL 操作 |

**绑定变量与 `:new` / `:old`**：触发器里 `:new.col` / `:old.col` 就是**绑定变量**的形式；在 PL/SQL 里写 `WHERE` 条件时应该用**绑定变量**（`:v`）而不是字面量拼接，否则共享池里会出现 `version_count` 爆炸（见 [`06`](06-SQL执行计划与CBO.md)）。

### 1.4 流程控制（教学示意，不参与构建）

```sql
-- 条件：CASE 是标准写法，DECODE 是 Oracle 专有（迁移友好性上 CASE 更好）
CASE v_job
  WHEN 'CLERK'   THEN v_pay := v_sal * 1.1
  WHEN 'SALESMAN' THEN v_pay := v_sal * 1.2
  ELSE v_pay := v_sal
END CASE;

-- 循环三族
FOR i IN 1..10 LOOP NULL; END LOOP;               -- 数值 FOR
FOR r IN (SELECT * FROM emp WHERE deptno = 20) LOOP  -- 游标 FOR（内部自动 OPEN/FETCH/CLOSE）
  NULL;
END LOOP;
WHILE v_count < 100 LOOP v_count := v_count + 1; END LOOP;
<<outer>>
FOR i IN 1..5 LOOP
  FOR j IN 1..5 LOOP
    CONTINUE outer WHEN i = j;                    -- 标签 + CONTINUE
  END LOOP;
END LOOP;
```

> **游标 FOR 循环是 PL/SQL 里最重要的语法糖**：它在内部把 `OPEN` / `FETCH ... INTO` / `CLOSE` 三件事做掉，而且**在循环体里 DML 同一张表时要小心**（游标 FOR 默认 `FOR UPDATE` 的语义，可能锁住整批行）。

### 1.5 游标三态

| 类型 | 谁管理 | 典型写法 | 注意 |
| --- | --- | --- | --- |
| **隐式游标** | Oracle | `SELECT ... INTO`；`SQL%ROWCOUNT`、`SQL%NOTFOUND` | 只在单值/单行查询里用；DML 后的 `SQL%ROWCOUNT` 很常用 |
| **显式游标** | 开发者 | `CURSOR c IS ...; OPEN c; FETCH c INTO x; CLOSE c;` | 必须 `CLOSE`，或用游标 FOR |
| **REF CURSOR（游标变量）** | 开发者 | `SYS_REFCURSOR` / 自定义 `REF CURSOR` 类型 | 可被返回给客户端；**`OPEN ... FOR` 动态 SQL** 时尤其有用 |

教学示意，不参与构建：

```sql
DECLARE
  TYPE c_emp IS REF CURSOR RETURN emp%ROWTYPE;   -- 强类型 REF CURSOR
  v_cur  c_emp;
  v_row  emp%ROWTYPE;
BEGIN
  OPEN v_cur FOR SELECT * FROM emp WHERE deptno = 20;
  FETCH v_cur INTO v_row;
  CLOSE v_cur;
END;
/
```

### 1.6 集合与记录：把"循环里跑 SQL"改掉

| 集合类型 | 索引 | 是否有序 | 能否在 SQL 里用 |
| --- | --- | --- | --- |
| **索引表（INDEX BY）** | `BINARY_INTEGER`/`VARCHAR2` 键 | 无序 | ❌（只能 PL/SQL 内）。12c 起可用 `TABLE()`？——**索引表不能直接在 SQL 里用** |
| **嵌套表（NESTED TABLE）** | 从 1 开始 | 有序 | ✅（可作表列、可被 `TABLE()` 展开） |
| **VARRAY** | 从 1 开始 | 有序 | ✅（有上限，适合"固定个数的列表"） |
| **集合（嵌套表）作参数** | —— | —— | ✅ 可传给 SQL，配合 `TABLE()` |

教学示意，不参与构建：

```sql
DECLARE
  TYPE emp_tab IS TABLE OF emp%ROWTYPE INDEX BY PLS_INTEGER;
  l_emps emp_tab;
  l_rec  emp%ROWTYPE;
BEGIN
  SELECT * BULK COLLECT INTO l_emps FROM emp WHERE deptno = 20;  -- 一次拿回一批
  FOR i IN 1 .. l_emps.COUNT LOOP
    DBMS_OUTPUT.PUT_LINE(l_emps(i).ename);
  END LOOP;
END;
/
-- 嵌套表/集合在 SQL 里展开（教学示意，不参与构建）
SELECT * FROM TABLE(l_ids);
```

> **注意 `BULK COLLECT` 的无限增长风险**：`SELECT ... BULK COLLECT INTO` 不设上限，可能一次把几千万行读进 PGA 导致 **PGA 耗尽 / ORA-04031**。必须配 `LIMIT`（见 [`10`](10-PLSQL高级与工程化.md)）。

### 1.7 动态 SQL：`EXECUTE IMMEDIATE` vs `DBMS_SQL`

```sql
-- 简单动态 SQL（教学示意，不参与构建）
DECLARE
  v_sql  VARCHAR2(200);
  v_cnt  NUMBER;
BEGIN
  v_sql := 'SELECT COUNT(*) FROM ' || USER || '.emp WHERE deptno = :d';
  EXECUTE IMMEDIATE v_sql INTO v_cnt USING 20;
  DBMS_OUTPUT.PUT_LINE('cnt=' || v_cnt);
END;
/
```

三条铁律：

1. **绝不拼接用户输入**（SQL 注入）；绑定变量 `:d` 用 `USING` 传；
2. **绑定变量的数量与顺序必须与 SQL 中的占位符一致**；返回多行要用 `BULK COLLECT INTO`；
3. **`DBMS_SQL` 只用于"列数/类型在编译期未知"的复杂场景**（如三思笔记里常见的数据泵导出封装），日常用 `EXECUTE IMMEDIATE` 就够了。

### 1.8 异常与 PRAGMA

| 异常类别 | 例子 | 处理 |
| --- | --- | --- |
| **预定义异常** | `NO_DATA_FOUND`、`TOO_MANY_ROWS`、`ZERO_DIVIDE`、`INVALID_NUMBER` | 直接 `WHEN no_data_found THEN` |
| **非预定义（ORA-xxxx）** | `ORA-01555 snapshot too old` | 用 `PRAGMA EXCEPTION_INIT(e, -1555)` 绑定后处理 |
| **自定义（应用异常）** | `ORA-20001` 起 | `RAISE_APPLICATION_ERROR(-20001, 'msg')` |

```sql
DECLARE
  e_low_sal EXCEPTION;                        -- 自定义异常声明
  PRAGMA EXCEPTION_INIT(e_low_sal, -20001);   -- 绑定到 ORA-20001
BEGIN
  IF 1 = 0 THEN RAISE_APPLICATION_ERROR(-20001, 'salary too low'); END IF;
EXCEPTION
  WHEN e_low_sal THEN DBMS_OUTPUT.PUT_LINE('caught app error');
END;
/
```

**PRAGMA 家族速查**：

| PRAGMA | 作用 |
| --- | --- |
| `AUTONOMOUS_TRANSACTION` | 这段程序在**独立事务**里跑（日志场景） |
| `SERIALLY_REUSABLE` | 包状态放在临时段，不占 PGA（高并发下省内存） |
| `AUTOMATIC_DML` | 让 SQL 语句对自表自动 DML（12c 触发器场景） |
| `EXCEPTION_INIT` | 把 ORA-xxxx 绑到具名异常 |
| `INLINE` / `RESTRICT_REFERENCES`（旧） | 优化与 purity 声明 |

## 二、版本演进

| 版本 | PL/SQL 相关变化 |
| --- | --- |
| 11g | `CONNECT BY`  enhancements、PL/SQL 的 `SIMILAR` 集合运算符；`DBMS_UTILITY` |
| 12c | 12.1 起：`BOOLEAN` 在更多地方可用（但不能直接用于 SQL 表达式）；**`WITH` 子句里的 PL/SQL 函数（12c 起支持 `WITH FUNCTION` 内联）**；`EXECUTE IMMEDIATE` 增强；**PL/SQL 的"易用性"大幅增强**（`FETCH ... INTO` 可直接 `BULK`）；12.2 起 PL/SQL 与 SQL 的边界更模糊 |
| 12.2 | PL/SQL 的 `CASE`/`NULLS` 处理改进；**`DBMS_PROFILER`** 等工具链完善 |
| 19c | **持续 PRC** 与 PL/SQL 表操作；PL/SQL 与 In-Memory 的交互 |
| 21c/23c | **JSON 与 PL/SQL 融合**、AI 向量类型、自治事务改进 |

🔧 **2026 年必须补的四条**：
1. **`cx_Oracle` → `oracle/python-oracledb`（star 实测 453）**：Python 生态已换血，Python-OracleDB 支持 **AQE（异步）、语句级回调、以及"不依赖 Oracle Client 的 Thin 模式"**——Thin 模式极大简化了容器化部署；
2. **`REST-enabled SQL` 与 `ORDS`（Oracle REST Data Services）**：2026 年给 PL/SQL 与_JSON_ 提供 HTTP 接口的主流方式，替代了大量"为了调 Oracle 而开 ODP.NET/JDBC 端口"的做法；
3. **PL/SQL 的"存算分离"压力**：大量企业把报表逻辑从 PL/SQL 迁到应用/数仓层（结算、风控逻辑外移），因为 PL/SQL 难测试、难版本化、难被异构团队复用；
4. **`SERIALLY_REUSABLE` 与 PGA 的关系**在容器化与高并发下比 2015 年更重要（共享 server 与 DRCP 场景见 [`13`](13-高并发系统的架构与设计.md)）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Stonebraker《Procedure Logic for DBMS: A Paradigm for Extending a Relational System》 | IEEE Data Engineering Bulletin 1985 | **通用理论，非 Oracle 专属**：数据库内嵌过程化语言的开山之作（Ingres/EGP），PL/SQL 的思想谱系 |
| Atkinson 等《An Introduction to Object-Oriented Database Systems》 | 1989（书/论文） | **通用理论，非 Oracle 专属**：对象与集合类型，PL/SQL 的 `RECORD`/集合类型的思想来源 |
| Date & Darwen《Foundation for Future Database Systems: The Fourth-Generation Language (4GL)》 | 1989 | **通用理论，非 Oracle 专属**：对"过程化扩展 SQL"的批评与替代方案 |
| Oracle《PL/SQL Language Reference》（Release 12.x/19c） | Oracle 官方文档（非论文） | 块结构、类型、游标、异常、PRAGMA 的权威描述 |
| Oracle《PL/SQL 语言参考》中关于 `AUTONOMOUS_TRANSACTION` 的说明 | Oracle 官方文档（非论文） | 自治事务的权威描述 |

> 说明：PL/SQL 是**产品实现**，其学术源头是"数据库内嵌过程化语言"这一研究方向（Stonebraker 1985 等）。上述为**通用理论，非 Oracle 专属论文**；具体语法行为以 Oracle 官方文档为准。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：**数据库内嵌编程语言的可测试性与隔离性**研究（如 PL/SQL 的 pure 函数、可序列化副作用），以及**把过程化逻辑下推到向量化执行引擎**（Velox/DuckDB 的 UDF、PG 的 PL/pgSQL 与 PL/vector）。
- **工业界**：
  - 🔧 **驱动生态换血**：`oracle/python-oracledb`（star 实测 ≈453）取代 `cx_Oracle`；`oracle/node-oracledb`（star 实测 ≈2368）同步演进。Thin 模式让"不用装 Oracle Client"成为默认选项，极大降低容器镜像体积。
  - 🔧 **连接与池化**：`alibaba/Druid`（star 实测 ≈28178）是最常见的 Java 连接池，能把 PL/SQL 里的慢 SQL 暴露给应用侧；Oracle 自己的 **UCP** 与 **DRCP** 是 Oracle 侧的池化方案（见 [`13`](13-高并发系统的架构与设计.md)）。
  - 🔧 **从 PL/SQL 迁出的趋势**：国内金融行业"去 IOE / 去 Oracle"过程中，PL/SQL 资产（几千个存储过程）是迁移成本的大头。经验做法：**先做调用关系分析（依赖图）→ 分类（可被 SQL 替代 / 需要改写为 Java/Go 服务 / 保留在数据库）→ 分批下线**，而不是一次性重写。
  - 🔧 **CDC 与 PL/SQL**：`debezium/debezium`（≈13152★）的 Oracle 连接器能捕获"应用侧的变更"，但**捕获不到 PL/SQL 内部的中间状态**——这决定了 PL/SQL 重逻辑的系统在做实时同步时天然吃亏。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "PL/SQL 执行 SQL 和直接在 SQL*Plus 里执行一样" | 每次跨"PL/SQL 引擎 ↔ SQL 引擎"都有开销；**循环里跑 SQL 是最贵写法** | PL/SQL 终极指南（第 21 章性能优化）、PL/SQL 实例精解 |
| 2 | "`EXCEPTION WHEN OTHERS` 里什么都不做就没事了" | 异常被静默吞掉，是"数据错了但程序没报"的头号原因；至少要 `RAISE` 或写日志 | PL/SQL 实例精解（错误处理章） |
| 3 | "`SELECT ... INTO` 没查到数据返回 NULL 而已" | 抛 **`NO_DATA_FOUND`**；查到多行抛 **`TOO_MANY_ROWS`**，二者都要处理 | PL/SQL 终极指南（第 10 章错误处理） |
| 4 | "`BULK COLLECT` 会自动限制数量" | **不会**。不配 `LIMIT` 可能撑爆 PGA（`ORA-04031`） | PL/SQL 终极指南（第 17 章批绑定） |
| 5 | "动态 SQL 拼接字符串方便" |  SQL 注入 + 硬解析风暴；必须用绑定变量 | PL/SQL 实例精解（动态 SQL 章） |
| 6 | "自治事务可以读主事务未提交的数据" | **不能**——它看不到主事务的任何未提交更改；这是它用于"日志"的原因，也是它的限制 | PL/SQL 终极指南（自治事务章） |
| 7 | "游标 FOR 循环里改同一张表没问题" | 游标会锁定已取出的行（`FOR UPDATE` 语义），大结果集下会长期持锁 | 全部 9 本 |
| 8 | 🔧 "`cx_Oracle` 还是 Python 连 Oracle 的标准方式" | 已被 **`oracle/python-oracledb`** 取代，支持 Thin 模式（无需 Oracle Client） | 🔧 PL/SQL 相关书（成书 2009–2018）与全部 9 本均未覆盖驱动换血 |
| 9 | 🔧 "PL/SQL 里的逻辑不需要迁走" | 2026 年主流方向是**把结算/报表类逻辑外移**，因为 PL/SQL 难测试、难版本化；迁移时的成本大头就是这些资产 | 🔧 全部 9 本未涉及"PL/SQL 资产迁移" |
| 10 | 🔧 "触发器是做审计/同步的最方便方式" | 触发器难以预测、影响 DML 性能、且**在 RAC/ DG 下行为不一致**；现代做法是 CDC（Debezium/GoldenGate） | 🔧 PL/SQL 终极指南与 PL/SQL 实例精解都把触发器当重点章，但未评估替代方案 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`08-常见SQL误区与最佳实践.md`](08-常见SQL误区与最佳实践.md)（"循环里跑 SQL"这一反模式在 PL/SQL 里最常见，本章 1.1/1.6 与 [`10`](10-PLSQL高级与工程化.md) 讲解法）
- **下一章**：[`10-PLSQL高级与工程化.md`](10-PLSQL高级与工程化.md)（本章讲"怎么写"，下一章讲"怎么写成大工程"：包、重载、批绑定、pipelined 表函数）
- **强相关**：[`06-SQL执行计划与CBO.md`](06-SQL执行计划与CBO.md)（PL/SQL 里的 SQL 也会走 CBO；`version_count` 与绑定变量是共享池问题的来源）
- **强相关**：[`04-事务与redo-undo-归档.md`](04-事务与redo-undo-归档.md)（`COMMIT`/`ROLLBACK` 在 PL/SQL 里的会话级含义，以及自治事务）
- **强相关**：[`13-高并发系统的架构与设计.md`](13-高并发系统的架构与设计.md)（`SERIALLY_REUSABLE`、连接池与 PL/SQL 会话内存的关系）
- **其他书**：《Oracle 12c PL/SQL程序设计终极指南》是本套里 PL/SQL 的主支撑（三篇 22 章，开发篇第 11–17 章讲子程序/包/依赖/触发器/集合/动态 SQL/批绑定）；《Oracle PL/SQL实例精解》是教程式补充，"概念 + 示例 + 练习"的写法适合打基础。
