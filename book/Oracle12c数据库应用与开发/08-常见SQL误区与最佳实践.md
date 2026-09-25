# 08 · 常见 SQL 误区与最佳实践

> **本章地图**：**隐式类型转换**（最隐蔽的索引杀手）→ **NULL 的六个陷阱**（`NULL` 与 `''`、`NOT IN`、`NOT EXISTS`、`NULL = NULL`、`NULL` 与聚合、分组与排序）→ **`NOT IN` vs `NOT EXISTS` vs `LEFT JOIN ... IS NULL`** 三者的语义与性能差异 → **函数导致索引失效** → **行列转换**（`DECODE`/`CASE` 与 `PIVOT`/`UNPIVOT`/`MODEL`）→ **`DUAL` 表的正确用法**（还有 12c 的 `dual` 优化与 `FIRST_ROWS`）→ **`MERGE` 的陷阱**→ **性能反模式清单**（`SELECT *`、`HAVING` 里过滤、`ROWNUM` 与排序、`DISTINCT`、`OR` 展开、循环里跑 SQL、无谓的 `COMMIT`）→ **`sqlldr` 直接路径导入的注意点**。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 隐式类型转换：一条最常见的"明明有索引却不走"

```sql
-- 列 phone_no 是 VARCHAR2(20)，但谓词传了数字（教学示意，不参与构建）
CREATE INDEX idx_emp_phone ON emp (phone_no);
SELECT * FROM emp WHERE phone_no = 13800001111;
-- Oracle 实际执行的是： TO_NUMBER(phone_no) = 13800001111
-- → 索引失效，退化成全表扫描
```

**规则（记住这一条就够）**：**Oracle 遇到类型不匹配时，会把"字符列"转成"数字列"，而不是反过来。** 后果有三：

1. **索引失效**；
2. **`NLS_DATE_FORMAT` 等会话设置会影响日期列的转换结果**——同一段代码在不同会话里结果不同；
3. **能成功反而更危险**：`TO_NUMBER('138...abc')` 会抛 `ORA-01722`。

对策：**在应用层就把类型定义好**，让 `PreparedStatement.setLong()` 写上数字，让 `WHERE` 里出现的是字符串字面量 `'138...'`。

### 1.2 NULL 的六个陷阱

| # | 写法 | 结果 | 为什么 |
| --- | --- | --- | --- |
| 1 | `WHERE col = NULL` | **零行** | `NULL` 参与任何比较都是 **UNKNOWN**，不是 TRUE/FALSE |
| 2 | `WHERE col <> 'A'`（col 有 NULL） | **漏掉 NULL 行** | `NULL <> 'A'` 是 UNKNOWN，该行被过滤掉 |
| 3 | `WHERE col IN ('A', NULL)` | **零行** | `IN` 的语义等价 `OR`，UNKNOWN 参与 OR 后仍是 UNKNOWN |
| 4 | `NOT IN` **子查询结果里有 NULL** | **零行**（这是最著名的坑） | `NOT IN` 等价于 `NOT(... OR ... OR ...)`,里面只要有一个 NULL 就整条变 UNKNOWN（详见 1.3） |
| 5 | `MAX(col)` / `SUM(col)` | **NULL**（不是 0） | 聚合函数跳过 NULL；`MAX` 全 NULL 则返回 NULL |
| 6 | `GROUP BY col` / `ORDER BY col` | `NULL` 被**归为一组**、排序时 **NULL 最后** | Oracle 默认 `NULLS LAST` |

教学示意，不参与构建：

```sql
-- 正确写法：用 NOT EXISTS 或加 IS NOT NULL（教学示意，不参与构建）
SELECT * FROM dept d
WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.deptno = d.deptno);

SELECT * FROM dept d
WHERE d.deptno NOT IN (SELECT deptno FROM emp WHERE deptno IS NOT NULL);
```

### 1.3 `NOT IN` / `NOT EXISTS` / `LEFT JOIN ... IS NULL` 的三角关系

| 写法 | 有 NULL 时 | 通常执行方式 | 适用场景 |
| --- | --- | --- | --- |
| `col NOT IN (subq)` | **返回零行**（灾难） | 转 `ANTI JOIN` | 确信子查询无 NULL |
| `NOT EXISTS (subq)` | 安全 | `ANTI JOIN` / `HASH JOIN ANTI` | **默认首选** |
| `LEFT JOIN ... WHERE 右表主键 IS NULL` | 安全 | `ANTI JOIN` | 需要保留语义清晰时 |
| `col IN (subq)` | 有 NULL 也安全（`IN` 只看是否命中） | `SEMI JOIN` | 正向筛选 |

**记忆口诀**：**`NOT` 打头的一律想到 `NULL`；`IN` 可以，`NOT IN` 要加 `IS NOT NULL` 兜底。**

### 1.4 函数导致索引失效：五种形态

```sql
-- 1) 显式函数（教学示意，不参与构建）
SELECT * FROM emp WHERE TO_CHAR(hiredate,'YYYY') = '1981';   -- 除非建函数索引
-- 2) 隐式函数：隐式类型转换（见 1.1）
SELECT * FROM emp WHERE eno = 7369;                          -- eno 是 VARCHAR2
-- 3) 运算：让谓词不再是"列 = 常数"
SELECT * FROM emp WHERE sal * 12 > 100000;                   -- 改写为 sal > 100000/12 可走索引
-- 4) 拼接
SELECT * FROM emp WHERE ename || '' = 'SMITH';               -- 无意义但足以毁掉索引
-- 5) 三思：用了 UPPER 就想大写检索，应建 UPPER(ename) 上的函数索引或虚拟列索引
```

**改写原则**：**把运算移到"常数的那一侧"**，或者**在表达式上建索引**（见 [`05`](05-索引与约束.md) 1.4）。

### 1.5 行列转换（PIVOT / UNPIVOT / 传统写法）

```sql
-- 12c 起的原生 PIVOT（教学示意，不参与构建）
SELECT * FROM (
  SELECT deptno, job, sal FROM emp
)
PIVOT ( SUM(sal) FOR job IN ('CLERK' AS clerk, 'SALESMAN' AS salesman) )
ORDER BY deptno;

-- 更早版本（以及任何版本都可用的）DECODE/CONDITIONAL AGG 写法
SELECT deptno,
       SUM(DECODE(job,'CLERK',sal,0))     AS clerk,
       SUM(DECODE(job,'SALESMAN',sal,0))  AS salesman
FROM emp GROUP BY deptno;

-- UNPIVOT：把列转成行
SELECT deptno, job, sal FROM (
  SELECT deptno, SUM(DECODE(job,'CLERK',sal,0)) AS clerk FROM emp GROUP BY deptno
) UNPIVOT (sal FOR job IN (clerk));
```

> 传统 `DECODE` 写法的好处是**兼容所有版本**，`PIVOT` 的坏处是 11g 之前不可用。跨版本迁移时这条很实际。

### 1.6 `DUAL` 表的正确用法

- `DUAL` 是一个只有一行一列的**伪表**，用于 `SELECT sysdate FROM dual`、`SELECT 1+1 FROM dual`；
- 12c 起对 `FROM DUAL` 做了优化，但**不要用来替代"临时表"**：在 PL/SQL 里反复 `INSERT INTO dual` 是完全没有意义且浪费的；
- 更现代的做法：`SELECT sysdate FROM sys.dual;` 或（12c 起）在 PL/SQL 里直接 `SELECT ... INTO` 而不用 DUAL；
- 🔧 **迁移提示（重要）**：**MySQL / PostgreSQL 没有 `DUAL` 表**（MySQL 有 `FROM DUAL` 的兼容写法但可选；PG 直接 `SELECT 1` 即可）。从 Oracle 迁到 PG 时，`SELECT 1 FROM dual` 会报错。

### 1.7 `MERGE` 陷阱

```sql
-- 教学示意，不参与构建
MERGE INTO target t
USING (SELECT id, name, amount FROM source) s
ON (t.id = s.id)
WHEN MATCHED THEN UPDATE SET t.name = s.name, t.amount = s.amount + 1
WHEN NOT MATCHED THEN INSERT (id, name, amount) VALUES (s.id, s.name, s.amount);
```

三个坑：

1. **`USING` 子查询有重复键 → `ORA-30926: unable to get a stable set of rows`**；
2. **`WHEN MATCHED` 的 UPDATE 若又更新了 `ON` 里的列，可能触发重扫或报 ORA-30926**；
3. **`MERGE` 是 DDL 式的隐式提交**（某些版本/写法下），会打断你的事务边界——这是"merge 之后我发现前面的插入也没了"的原因之一（见 [`04`](04-事务与redo-undo-归档.md) 的隐式提交）。

### 1.8 性能反模式清单（按出现频率排序）

| 反模式 | 后果 | 替代做法 |
| --- | --- | --- |
| `SELECT *` | 多余字段、LOB 被连带读出、行链接 | 显式列出需要的列 |
| `WHERE` 里对列做函数/运算 | 索引失效 | 改写或建函数索引 |
| `HAVING` 里过滤本可提前的行 | 先聚合再筛，代价放大 | 放进 `WHERE` |
| `DISTINCT` 无意义 | 强制排序/去重 | 确认是否真的需要 |
| `OR` 串联多个范围 | 索引难以使用（12c 起 `OR-expansion` 缓解） | `UNION ALL` 分段 |
| 循环里执行 SQL（PL/SQL 里 `FOR r IN SELECT ... LOOP INSERT ...`） | 上下文切换 × N | `BULK COLLECT` + `FORALL`（见 [`10`](10-PLSQL高级与工程化.md)） |
| 频繁 `COMMIT`（逐行提交） | redo/检查点压力 | 批量提交 |
| `ROWNUM` 与 `ORDER BY` 混用 | **先取行再排序**，结果不符预期 | 子查询里先排序再套 `ROWNUM` |
| `NOT IN` 遇 NULL | 零行 | `NOT EXISTS` |
| 大事务一次提交几十万行 | undo/redo 爆炸、回滚代价高 | 分批 |

```sql
-- ROWNUM 的经典正确写法（教学示意，不参与构建）
SELECT * FROM (
  SELECT * FROM emp ORDER BY sal DESC
) WHERE ROWNUM <= 10;
```

## 二、版本演进

| 版本 | SQL 写法相关变化 |
| --- | --- |
| 11g | `MERGE` 完善；新增 `PIVOT`/`UNPIVOT`  predecessors（`CUBE`/`ROLLUP`/`GROUPING SETS`） |
| 12.1 | **`PIVOT`/`UNPIVOT` GA**；`WITH` 子句的 `SEARCH` / `CYCLE` 语法；`FROM DUAL` 优化 |
| 12.2 | `OR-expansion`、`IN` 列表大小变化；`DISTINCT` 的 `ROWNUM` 处理更稳定 |
| 19c | 持续 PRC 让"更新同一行"的代价变化，对事务型 SQL 写法有影响（见 `14`） |
| 23c | JSON Relational Duality 与 SQL/JSON 语法融合；向量函数进入 SQL 层 |

🔧 **2026 年必须补的三条**：
1. **`ROWNUM` 与 `FETCH FIRST`（12c 起支持 `FETCH FIRST n ROWS ONLY`）**——新代码应该写 `FETCH FIRST`，`ROWNUM` 留给老代码；
2. **多列 `IN`（`IN ((a,b),(c,d))`，12c 起支持）** 与 **多列 `NOT IN`** 的语义细节，跨版本迁移时是新语法点；
3. **`DECODE` 是 Oracle 专有**，`CASE` 是标准 SQL——**新代码一律用 `CASE`**，这样迁移 PG/MySQL 时少一层改造（MySQL 也从不支持 `DECODE`）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Date, Darwen《Foundation for Object/Relational Databases: The Third Manifesto》 | 1996/1999（书） | **通用理论，非 Oracle 专属**：提出"关系模型应当如何约束 SQL 语义"（如 NULL 的处理争议），是 SQL 语义讨论的经典对手文献 |
| Codd《The Relational Model for Database Management: Version 2》 | 1990（书） | **通用理论，非 Oracle 专属**：null 值与三值逻辑的提出 |
| Melton & Simon《SQL:1999 (SQL3)》标准文档 | 1999 | **标准文献**：`CASE`、`MERGE`、`PIVOT` 的标准语义来源 |
| Oracle《Oracle Database SQL Language Reference》"Data Types / Conditional Expressions / Operators" | Oracle 官方文档（非论文） | 隐式类型转换规则、`NULL` 语义、`DECODE` 与 `CASE` 的权威描述 |
| Oracle《Oracle Database SQL Language Reference》"MERGE / PIVOT / UNPIVOT" | Oracle 官方文档（非论文） | 本章 1.5/1.7 的权威描述 |

> 说明：**SQL 的 NULL 语义与三值逻辑是标准与学术议题**（Codd 与 Date 的争论持续了整个 1990 年代），明确**不是 Oracle 专属**。本章的具体语法行为以 Oracle 官方文档为准。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：**SQL 语义等价性验证**（如用等价查询改写验证 `NOT IN` 与 `NOT EXISTS` 是否等价）与 **静态类型推断**（提前发现隐式类型转换）——是"错误检测左移到 IDE/编译器"的研究方向。
- **工业界**：
  - 🔧 **静态分析工具**：SonarQube、SQLFluff、以及 Oracle 自己的 **SQL Quality Dashboard / SQL Developer 的 Analyze** 会把"隐式转换、缺索引的谓词、可聚合的 `HAVING`"报成问题。**在 CI 阶段拦住这些写法**，比上线后再调优便宜一个数量级。
  - 🔧 **ORM 层的隐式转换**：Hibernate/JPA 与 SQLAlchemy 有时会把 `Integer` 绑定到 `VARCHAR` 列上，导致全表扫；**这条在 Java 项目里出现频率极高**，`alibaba/Druid`（star 实测 ≈28178）的慢 SQL 日志是发现它的常用手段。
  - 🔧 **迁移视角**：MySQL 的 `NOT IN` 语义与 Oracle 基本一致，但 **MySQL 没有 `DECODE`、`DUAL` 可选、`ROWNUM` 不存在**（用 `LIMIT`）——Oracle 语法迁出时要建一份"语法对照表"，CN 社区里最常见的迁移踩坑清单就是这一类。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "`WHERE col = NULL` 会报语法错" | 语法合法但**永远返回零行**；要写 `IS NULL` | SQL 应用及误区分析（第 3–6 章） |
| 2 | "`NOT IN` 慢而已，结果是对的" | 子查询结果里**有一个 NULL 就返回零行**，是静默错误 | SQL 应用及误区分析有案例，但未点明"零行"后果 |
| 3 | "`NULL` 和空串是一回事，问题不大" | `''` 会被 Oracle 当 `NULL` 处理，`CONCAT('a','')` 与 `''` 的比较都踩这个坑；但 PostgreSQL **严格区分 `''` 与 `NULL`**，跨库迁移会出错 | 全部 9 本 |
| 4 | "`NULL` 排序时最前" | Oracle **默认 NULLS LAST**；MySQL 在 `ORDER BY ... ASC` 时 NULL 最前——**同 SQL 不同结果** | SQL 应用及误区分析（第 14 章比较了 SQL Server/Oracle 差异，未覆盖 MySQL/PG） |
| 5 | "函数包装列一定不走索引" | 若**建了匹配的函数索引**或**虚拟列**就可以走（见 [`05`](05-索引与约束.md)）；也不排除 CBO 判定全扫更快 | 12c 教材（第 10 章）偏"建了就用"，SQL 优化最佳实践（访问方式章）更准确 |
| 6 | "`MERGE` 有重复行就跳过" | 直接报 **`ORA-30926`**；要先用 `DISTINCT`/`ROW_NUMBER()` 去重 | 全部 9 本 |
| 7 | "隐式类型转换是小事" | 是**最隐蔽的全表扫来源**，且是应用与数据库之间最常见的"沉默故障" | 全部 9 本（SQL 优化最佳实践提到过，但未作为独立条目强调） |
| 8 | 🔧 "`ROWNUM` 是取前 N 行的标准写法" | 12c 起有标准语法 **`FETCH FIRST n ROWS ONLY`**；且 `ROWNUM` 的赋值发生在**行被取回之后**，与 `ORDER BY` 混写必然出错 | 🔧 全部 9 本 |
| 9 | 🔧 "`DECODE` 更好用" | `DECODE` 是 **Oracle 专有**；新代码用标准 `CASE`，可迁移性更好 | 🔧 全部 9 本（DECODE 大量出现在 PL/SQL 书里） |
| 10 | 🔧 "`SELECT 1 FROM dual` 到处都能跑" | **PostgreSQL 没有 `DUAL`**；迁出时要改 `SELECT 1`。反向进来时相反 | 🔧 全部 9 本 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`07-SQL性能诊断与调优实践.md`](07-SQL性能诊断与调优实践.md)（本章的反模式正是 `buffer busy wait` / 全表扫等待事件的**应用侧成因**）
- **下一章**：[`09-PLSQL编程基础.md`](09-PLSQL编程基础.md)（本章的"循环里跑 SQL"反模式在 PL/SQL 里最常见，下一章讲正确写法与 `09` 里的游标）
- **强相关**：[`05-索引与约束.md`](05-索引与约束.md)（函数索引/虚拟列索引与 1.4 联动）
- **强相关**：[`06-SQL执行计划与CBO.md`](06-SQL执行计划与CBO.md)（1.1/1.4 的问题只有读了计划才能确认）
- **强相关**：[`13-高并发系统的架构与设计.md`](13-高并发系统的架构与设计.md)（1.8 的"频繁 COMMIT"与"大事务"在高并发下会被放大成故障）
- **其他书**：《SQL应用及误区分析》是本套里"误区"主题的主支撑（14 章，第 3–6 章增删改查、13 章事务、14 章 SQL Server 与 Oracle 差异对比）；《SQL优化最佳实践》的实战篇提供大量"改写前后计划对比"的实例，可与本章逐条对照验证。
