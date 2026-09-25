# 10 · PL/SQL 高级特性与工程化

> **本章地图**：**子程序与参数模式**（`IN`/`OUT`/`IN OUT`、`NOCOPY`）→ **包（PACKAGE）**（规范体分离、重载、包状态、`PACKAGE BODY` 依赖）→ **子程序重载的规则与陷阱**（参数类型 vs 参数模式）→ **自治事务**（`#PRAGMA AUTONOMOUS_TRANSACTION`）→ **批量绑定 `BULK COLLECT` / `FORALL` / `SAVE EXCEPTIONS`**→ **pipelined 表函数与 `TABLE()`**→ **依赖与失效**（编译期依赖、对象失效、`ALTER ... COMPILE`）→ **动态 SQL 与 `DBMS_SQL`**→ **性能工程**（`%NOTFOUND` vs `FETCH` 计数、减少上下文切换）→ **编码规范**（命名、注释、异常分层、版本管理）→ **工程化现实**（测试、迁移、PL/SQL 资产处置）。

## 一、核心精讲

> 以下 SQL/PL-SQL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 子程序：Procedure / Function / 参数模式

| 模式 | 含义 | 常见用途 |
| --- | --- | --- |
| `IN` | 只读输入，默认 | 99% 场景 |
| `OUT` | 只写输出 | 返回单值；**注意 OUT 参数在函数体内必须先初始化才能引用** |
| `IN OUT` | 可读写 | 需要双向时 |
| **`NOCOPY`** | 提示"用引用传递"（大 LOB/集合时避免复制） | **只是提示，不是保证**；对 `OUT`/`IN OUT` 的集合与 LOB 有效 |

```sql
-- 教学示意，不参与构建
CREATE OR REPLACE PROCEDURE add_emp (
  p_empno  IN  emp.empno%TYPE,
  p_ename  IN  emp.ename%TYPE,
  p_sal    IN  emp.sal%TYPE DEFAULT 0,
  p_msg    OUT VARCHAR2
) IS
BEGIN
  INSERT INTO emp(empno, ename, sal) VALUES (p_empno, p_ename, p_sal);
  p_msg := 'inserted ' || SQL%ROWCOUNT;
EXCEPTION
  WHEN DUP_VAL_ON_INDEX THEN
    p_msg := 'duplicated';
END add_emp;
/
```

> **`DEFAULT` 让参数有默认值，是"不破坏已有调用"的唯一办法**——在老程序上新增参数时，用 `DEFAULT` 而不是要求所有调用方都改。

### 1.2 包：为什么要用包

```
PACKAGE 规范（PACKAGE，公开接口）
   ├─ 子程序声明、变量/类型/游标声明
   └─ 被 GRANT 的对象（权限只给规范）
          ↓ 实现
PACKAGE BODY（PACKAGE BODY，私有实现）
   └─ 具体的代码，外部看不见
```

包的价值有三条，按重要性排序：

1. **状态保留**：包里的**包级变量（package variable）在整个会话里存活**。这是缓存（如"缓存字典表"）的经典实现；
2. **一次加载多次调用**：首次调用加载整个包到 PGA，后续调用零解析成本；
3. **命名空间与重载**：把相关逻辑收在一个命名空间下。

**代价（必须知道）**：包状态一旦发生不一致，只能 **`ALTER PACKAGE ... COMPILE` 或让包失效**来"重置"，因为包是"整包重启"的。生产上"某个包的状态坏了"的处理方式就是**重新编译让会话下次进来时重新初始化**。

### 1.3 重载：规则比想象中严

**只有"参数类型不同"才能重载；"参数模式不同"不能重载。** 下面这两对都是**编译错误**（教学示意，不参与构建）：

```sql
-- 错误 1：只改参数模式（教学示意，不参与构建）
PACKAGE p IS
  PROCEDURE f(p VARCHAR2);
  PROCEDURE f(p OUT VARCHAR2);   -- ORA-01755: declared procedure needs FOR syntax? 其实报的是重载不合法
END p;

-- 正确：参数类型不同（教学示意，不参与构建）
PACKAGE p IS
  PROCEDURE f(p VARCHAR2);
  PROCEDURE f(p NUMBER);         -- 合法
END p;
```

**调用时的歧义**：如果实参是 `NULL` 或父类型/子类型混用（如 `INTEGER` 传 `NUMBER`），Oracle 可能报"有歧义"（`PLS-00307`）。经验做法：**传入时显式转换类型**。

### 1.4 自治事务：用对是宝，用错是灾难

```sql
-- 教学示意，不参与构建
CREATE OR REPLACE PROCEDURE log_audit (
  p_action VARCHAR2, p_detail VARCHAR2
) IS
PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
  INSERT INTO audit_log(action, detail, at) VALUES (p_action, p_detail, SYSDATE);
  COMMIT;                       -- 注意：自治事务必须自己提交/回滚
END log_audit;
/
```

三条规则：

1. **自治事务看不到主事务的未提交数据**——所以"先写日志再改业务，主事务回滚了日志还在"是对的（日志已独立提交）；
2. **必须在自治程序里显式 `COMMIT`/`ROLLBACK`**，否则会抛 `ORA-06558`；
3. **嵌套深度有限**（默认最多 4 层左右，由 `_max_autonomous_transaction_depth` 控制），且**递归调用自治事务极易导致死锁**；
4. **典型误用**：为了"让日志不回滚"而把**业务写入**也放进自治事务——这等于破坏了原子性。

### 1.5 批量绑定：把 N 次 SQL 合成 1 次

```sql
-- 反例（教学示意，不参与构建）：N 次 INSERT → N 次上下文切换 + N 次 redo
FOR i IN 1 .. ids.COUNT LOOP
  INSERT INTO t(id, val) VALUES (ids(i), vals(i));
END LOOP;

-- 正解：FORALL（教学示意，不参与构建）
FORALL i IN 1 .. ids.COUNT
  INSERT INTO t(id, val) VALUES (ids(i), vals(i));

-- 正解：BULK COLLECT + LIMIT（内存安全，教学示意，不参与构建）
DECLARE
  CURSOR c IS SELECT * FROM big_src WHERE flag = 1;
  TYPE tt IS TABLE OF c%ROWTYPE;
  l_batch tt;
BEGIN
  OPEN c;
  LOOP
    FETCH c BULK COLLECT INTO l_batch LIMIT 5000;   -- 必须配 LIMIT
    EXIT WHEN l_batch.COUNT = 0;
    FORALL i IN 1 .. l_batch.COUNT
      INSERT INTO big_tgt VALUES l_batch(i);
    COMMIT;
  END LOOP;
  CLOSE c;
END;
/
```

**`SAVE EXCEPTIONS`**：`FORALL ... SAVE EXCEPTIONS` 让"某几条失败"不中断整批，失败信息累积在 `SQL%BULK_EXCEPTIONS` 里。**这是大批量数据修补的标准姿势**——否则第一条报错就整批回滚，等于白干。

```sql
-- 教学示意，不参与构建
BEGIN
  FORALL i IN 1 .. ids.COUNT SAVE EXCEPTIONS
    INSERT INTO t(id) VALUES (ids(i));
EXCEPTION
  WHEN OTHERS THEN
    FOR j IN 1 .. SQL%BULK_EXCEPTIONS.COUNT LOOP
      DBMS_OUTPUT.PUT_LINE('err at ' || SQL%BULK_EXCEPTIONS(j).ERROR_CODE);
    END LOOP;
END;
/
```

### 1.6 pipelined 表函数：把 PL/SQL 结果当表用

```sql
-- 教学示意，不参与构建
CREATE OR REPLACE FUNCTION f_get_emps(p_dept NUMBER)
RETURN SYS_REFCURSOR ... -- 不推荐
/

-- 正确形态：pipelined table function
CREATE OR REPLACE FUNCTION f_emps(p_dept NUMBER)
RETURN SYS.ODCIVARCHAR2LIST PIPELINED IS
  CURSOR c IS SELECT ename FROM emp WHERE deptno = p_dept;
  l_name VARCHAR2(30);
BEGIN
  FOR r IN c LOOP
    PIPE ROW (r.ename);              -- 边算边吐，不占满内存
  END LOOP;
  RETURN;
END;
/

-- 在 SQL 里当表用
SELECT * FROM TABLE(f_emps(20));     -- 可被 CBO 优化、可 JOIN、可并行
```

与"返回 `SYS_REFCURSOR`"的对比是本章的实用结论：

| 方式 | 能否在 SQL 里 JOIN | 能否并行 | 内存 |
| --- | --- | --- | --- |
| 返回 `SYS_REFCURSOR` | ❌ | ❌ | 客户端自行取 |
| **pipelined 表函数** | ✅ | ✅ | 流式，可控 |
| 建临时表再插 | ✅（但要写盘，且要清理） | 一般 | 高 |

### 1.7 依赖与失效：为什么一个表加列会让一堆程序挂掉

- PL/SQL 程序是**在编译期做名字解析**的，所以它依赖具体表/列；
- 一旦被依赖的对象结构变了（加了列、改了类型），依赖它的**程序会变成 `INVALID`**；下次调用时 Oracle 会**自动重编译**——若失败则报错；
- **`UTL_RECOMP`** 是批量重编译的工具（10g 起）；
- 生产上"给一张大表加一列，然后全库开始报错"就是这个机制。

```sql
-- 教学示意，不参与构建
SELECT object_name, status FROM user_objects WHERE status = 'INVALID';
ALTER PROCEDURE my_proc COMPILE;
-- 批量重编译（以 SYS 运行）
-- SELECT utl_recomp.recomp_parallel('SCHEMA_NAME', 8) FROM dual;
```

### 1.8 编码规范（工程化的落点）

| 项 | 建议 |
| --- | --- |
| 命名 | 前缀区分类型：`v_` 变量、`c_` 常量、`p_` 参数、`t_` 类型、`sp_` 过程、`fn_` 函数、`pkg_` 包；业务表用业务前缀 |
| 异常 | **分层处理**：底层 `RAISE` 抛原始异常，上层转成业务异常（`RAISE_APPLICATION_ERROR`）并记日志 |
| 事务边界 | **不在被库函数里 `COMMIT`**——让最外层决定事务边界，否则"调用了我一个函数，结果我的事务被提交了" |
| SQL 写法 | 绑定变量、不用 `SELECT *`、不用 `NOCOPY` 之外的"大对象复制" |
| 注释 | 每个过程头部写"做什么、参数含义、修改历史（谁/何时/为什么）" |
| 版本管理 | **包规范与包体都要纳入版本库**，且**部署顺序是"先改规范还是先改体"必须走流程**（见 1.9） |
| 幂等 | 数据修补类程序**必须可重复执行**（先删后插 / 用 MERGE / 加唯一约束） |

## 二、版本演进

| 版本 | PL/SQL 高级特性变化 |
| --- | --- |
| 10g | `UTL_RECOMP`；`DBMS_PARALLEL_EXECUTE`（把大任务切片并行跑——**大批量数据修补的标配**） |
| 11g | 编译期优化（"编译更快、运行更快"）；`SIMILAR` 集合运算符 |
| 12c | 12.1：Pipelined 表函数与并行更紧密结合；12.2：`WITH FUNCTION` 内联 PL/SQL、更强的编译时检查 |
| 19c | 持续 PRC 与 PL/SQL 表操作优化；**自动索引**会与 PL/SQL 内的 SQL 交互 |
| 23c | JSON Relational Duality 让"JSON 文档 ↔ 关系表"双向映射，PL/SQL 也提供 JSON 处理函数 |

🔧 **2026 年必须补的四条**：
1. **`DBMS_PARALLEL_EXECUTE` + `DBMS_Scheduler` 才是大表批量更新的现代组合**（比"一个大事务 `UPDATE` 5000 万行"安全得多：切片、可断点续跑、可并行），本书时代的做法是"写个匿名块循环提交"。
2. **PL/SQL 与自动索引（19c/23c）的交互**：自动索引可能在你的 PL/SQL 里建出意料之外的索引，需要显式监控。
3. **PL/SQL 单元测试**：`UTL_UNITTEST` / `SQL Developer 的 Unit Test` / `utPLSQL`（开源）是 2020 年代才普及的做法；PL/SQL 曾经的"不可测试"正在被工具链解决。
4. **PL/SQL 资产迁移**：见 [`09`](09-PLSQL编程基础.md) 的"驱动生态换血"与本节 1.9。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Stonebraker《Procedure Logic for DBMS: A Paradigm for Extending a Relational System》 | IEEE Data Engineering Bulletin 1985 | **通用理论，非 Oracle 专属**：数据库内嵌过程化语言的开山思路 |
| Lampson & Redell《An Object-Oriented System》（或更贴切的：面向"封装与模块化"的经典系统论文） | 1980 年代 | **通用理论，非 Oracle 专属**：包（规范 + 实现）这一"模块化封装"范式 |
| Oracle《PL/SQL Language Reference》"PACKAGE / Overloading / Bulk Binds / Autonomous Transactions" | Oracle 官方文档（非论文） | 本章全部语法的权威描述 |
| Oracle《PL/SQL Packages and Types Reference》（`DBMS_PARALLEL_EXECUTE`、`DBMS_UTILITY`、`UTL_RECOMP` 等） | Oracle 官方文档（非论文） | 工程化工具的权威描述 |

> 说明：包、重载、批量绑定都是**产品实现**；其背后是"过程化扩展关系库"与"模块化封装"的通用思想（明**不是 Oracle 专属论文**）。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：**过程化逻辑的迁移与等价重写**、**数据库内 UDF 的向量化执行**（DuckDB/Velox 的 `CREATE MACRO`、PG 的 PL/vector），以及**PL/SQL 到 SQL 的自动化转换**（用 LLM 辅助把 Pl/SQL 翻译成 Java/Go）在 2023 年后成为国内"去 Oracle"项目里的热点课题。
- **工业界**：
  - 🔧 **`utPLSQL`（开源单元测试框架）** 在 2018 年后普及，是"PL/SQL 可以被测试"这件事的主流答案；
  - 🔧 **`oracle/python-oracledb`（star 实测 ≈453）** 支持 **PL/SQL 块执行与绑定数组（`setinputsizes` / `bindarraysize`）**，一条语句把整批数据送进 PL/SQL，是"批量绑定"在客户端侧的对应能力；
  - 🔧 **中间件与池化**：`alibaba/Druid`（star 实测 ≈28178）与 Oracle **UCP / DRCP** 配合，让"PL/SQL 包状态"不再绑定在独占会话上（DRCP 共享会话内存，见 [`13`](13-高并发系统的架构与设计.md)）；
  - 🔧 `debezium/debezium`（star 实测 ≈13152）：捕获 PL/SQL 产生的 DML；但由于 PL/SQL 内部中间状态不可见，**重逻辑的 PL/SQL 系统在 CDC 场景里先天吃亏**，这是迁移决策的一手输入。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "`NOCOPY` 保证引用传递" | 只是**提示**；Oracle 在异常回滚等场景下可能仍复制 | PL/SQL 终极指南（参数章） |
| 2 | "参数模式不同也能重载" | **不能**，只有类型不同才能重载；调用还可能歧义 | PL/SQL 终极指南（子程序章） |
| 3 | "包状态坏了重启实例就好" | 不需要重启实例，`ALTER PACKAGE ... COMPILE` 或让它失效即可让下次调用重新初始化 | 全部 9 本 |
| 4 | "`FORALL` 一样快到飞起" | 若集合本身就很大且**没有 `LIMIT`**，PGA 也会爆；`FORALL` 只解决上下文切换数量 | PL/SQL 终极指南（批绑定章） |
| 5 | "`FORALL` 中某条失败就整批回滚" | 默认如此；要"部分成功"必须加 **`SAVE EXCEPTIONS`** | PL/SQL 终极指南（批绑定章） |
| 6 | "自治事务可以读主事务已改的数据" | **不能**；它完全隔离 | PL/SQL 终极指南（自治事务章） |
| 7 | "大批量更新就在一个事务里跑完" | undo/redo 爆炸、回滚代价高、长事务阻塞 purge；现代做法是 **分批提交 + `DBMS_PARALLEL_EXECUTE`** | 全部 9 本（成书早于 2015 的居多） |
| 8 | "程序失效让 DBA 去修就行" | 失效是**设计缺陷的表现**（紧耦合）；加列前应先看有多少依赖对象（`dba_dependencies`） | 全部 9 本 |
| 9 | 🔧 "PL/SQL 逻辑要长期留在数据库里" | 2026 年主流是**外移**（结算/报表/风控逻辑迁到服务层）；PL/SQL 难测试难版本化，是迁移成本大头 | 🔧 全部 9 本未涉及 PL/SQL 资产的迁移策略 |
| 10 | 🔧 "PL/SQL 不可测试，没办法" | `utPLSQL` 等框架已成熟，2020 年代起是标准做法 | 🔧 全部 9 本 |
| 11 | 🔧 "触发器 + 自治事务 = 完美审计方案" | 触发器影响 DML 性能、行为难预测；现代方案是 **CDC（Debezium/GoldenGate）+ 独立审计表** | 🔧 PL/SQL 终极指南与 PL/SQL 实例精解都把触发器当重点章 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`09-PLSQL编程基础.md`](09-PLSQL编程基础.md)（本章是它的延续：从"会写"到"工程化"）
- **下一章**：[`11-RAC与高可用.md`](11-RAC与高可用.md)（包状态在多节点 RAC 下**不共享**，是 RAC 上 PL/SQL 设计的关键约束）
- **强相关**：[`06-SQL执行计划与CBO.md`](06-SQL执行计划与CBO.md)（pipelined 表函数在 SQL 里就是个函数扫描；批量绑定改变了 redo/undo 的量级）
- **强相关**：[`11-RAC与高可用.md`](11-RAC与高可用.md)——**RAC 每个实例各自一份包状态**（不共享），DRCP 的共享会话也可能把"逻辑会话"的 PL/SQL 状态复用给别人，这是 RAC/DRCP 上 PL/SQL 设计的关键约束
- **强相关**：[`13-高并发系统的架构与设计.md`](13-高并发系统的架构与设计.md)（`SERIALLY_REUSABLE`、池化与 PL/SQL 会话内存）
- **其他书**：《Oracle 12c PL/SQL程序设计终极指南》开发篇（第 11–17 章）与高级篇（第 18–22 章）是本章的主支撑；《Oracle PL/SQL实例精解》用"练习驱动"的方式补充了游标与触发器；《DBA攻坚指南》第 2 章讲"业务高峰期不要编译对象"（`library cache pin/lock`），正好是本章"依赖与失效"的运维副作用。
