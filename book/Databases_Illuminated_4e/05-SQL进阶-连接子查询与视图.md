# 05 SQL 进阶：连接、子查询与视图

> 单元性质：⚠️ 主题重构。对应教材通行"More SQL / Advanced SQL"单元。深度对照：[../数据库系统概念6/04-中级SQL.md](../数据库系统概念6/04-中级SQL.md) 与 [../数据库系统概念6/05-高级SQL.md](../数据库系统概念6/05-高级SQL.md)；方言实操两册：[../DuckDB_in_Action/03-执行SQL查询.md](../DuckDB_in_Action/03-执行SQL查询.md)、[../The_Definitive_Guide_to_SQLite_2e/04-SQL进阶.md](../The_Definitive_Guide_to_SQLite_2e/04-SQL进阶.md)。

## 1. 连接（JOIN）的语义几何

INNER = 笛卡尔积+谓词；LEFT/RIGHT/FULL 保留侧补 NULL；CROSS 无谓词积；NATURAL 按同名列合并（教材警告：schema 一改即碎，工业禁用）。本质是把"外键方向"（03 章）变成"遍历方向"：teach→department 顺 FK 走，department→teach 逆 FK 走。

🔧 **exp2 实录（双引擎同题）**：`teach LEFT JOIN department`，SQLite 与 DuckDB 输出逐行一致：`[('Alice','CS'), ('Bob','Math'), ('Carol','CS'), ('Dan','(none)')]`——Dan 的部门列为 NULL，靠 COALESCE 显示兜底。外连接补 NULL 的教科书定义在两个不同架构引擎上可复现。

## 2. 聚合与分组

GROUP BY 把"表"折成"组"；聚合族 COUNT/SUM/AVG/MIN/MAX + HAVING 对组再过滤；**WHERE 行级、HAVING 组级**是考试与工程双重高频点。SELECT 列表在标准 SQL 必须"分组键或聚合"（SQLite 方言宽容允许裸列 ⚠️，DuckDB 报错严格——两引擎对比即活教材）。

🔧 exp2：`GROUP BY student HAVING AVG(grade)>80` 双引擎同解 `[('Alice', 88.5)]`（Carol 均分 77、Bob 78 被滤掉——学生手工验算的好靶子）。

## 3. 子查询光谱

标量子查询（SELECT 列位置）、行子查询（IN/=ANY）、表子查询（FROM 里的派生表/内联视图）、EXISTS 半连接、相关子查询（逐行求值的"内层参数化"）。教材三大坑：**NOT IN 遇 NULL**（03 章 UNKNOWN 传播→整条件 UNKNOWN→空结果，改 NOT EXISTS 免疫）、标量子查询必须单行（卡迪诺违例报运行时错）、相关子查询性能退化（优化器视引擎改写能力，08 章）。

🔧 exp2：`WITH top AS (...)` CTE 与相关等价写法（`e.grade = t.m`）双路同解 `[('Alice','C102'), ('Bob','C101'), ('Carol','C101')]`——"每学生最高分课"题型的两种翻译。

## 4. 窗口函数：分析翼的入口

OVER(PARTITION BY ... ORDER BY ... [frame]) + 排名族（ROW_NUMBER/RANK/DENSE_RANK）与位移族（LAG/LEAD）。教材定位：不折叠行的聚合。DuckDB 额外给 **QUALIFY** 子句直接过滤窗口结果。

🔧 exp2：`RANK() OVER(PARTITION BY student ORDER BY grade DESC)` SQLite 全表出 5 行名次；DuckDB `QUALIFY r=1` 一步取每人最好成绩——同一题在"标准 SQL 写法"与"方言糖"间的对照。

## 5. 视图（VIEW）：命名查询与逻辑独立性兑现

视图=存储的查询定义；更新视图受"可合并性"限制（多数引擎只允许键保全视图更新）。01 章三级模式的外部层在此落地；02 章 EER 之外，视图也是隐藏 NULL 补齐与列裁剪的工具。安全用途（行级裁剪给不同角色）归 12 章材料化。

## 6. 集合运算与 CASE

UNION（去重）/UNION ALL（保重保序成本）、INTERSECT、EXCEPT（SQLite/DuckDB 均支持；方言名差 ⚠️ MINUS=Oracle 系）。CASE 表达式是"行内 if-else"，透视（PIVOT）的原料；DuckDB 有原生 PIVOT/UNPIVOT 语法（🔧 实测语法可用——但若不先对枢轴值做聚合，它会把其余全部列当行组做枢轴，输出瞬间爆炸；教材侧仍以 CASE 手工透视为通用技能）。

## 7. 嵌入式 SQL 与现代接口

教材传统章节 EXEC SQL + 游标（DECLARE/FETCH/CLOSE）+ 宿主语言（C/COBOL）；现代对应：Python DB-API（PEP 249）的 cursor/参数绑定——🔧 exp1–exp5 全程即"嵌入式"实操（sqlite3/duckdb 包）。存储过程/函数一节在 SQLite 方言缺位（可用自定义函数注册替代）、DuckDB 无用户存储过程 ⚠️——教材通用叙述在嵌入式引擎上"测不出来"本身就是对照知识点。

## 8. 常见错误清单

1. LEFT JOIN 的过滤条件写进 WHERE（把保留侧 NULL 行滤光，语义退化为 INNER）——应写 ON 或 HAVING。
2. HAVING 里放行级谓词（能用 WHERE 就别进 HAVING，优化器感激你）。
3. NOT IN + 可空子查询列。
4. SELECT 裸列依赖 SQLite 方言宽容——换引擎即碎。
5. 窗口函数用在 WHERE（不允许，需 CTE/子查询中继）。

## 9. 小结

表达力闭环：单表（04）→多表+组+窗口（本单元）→可命名复用（视图）。SQL 技能树到此可支撑 06 章的"设计好不好"与 08 章的"跑得快不快"讨论。

## 10. 补充：JOIN 谓词位置实验（exp2 的引申，5 分钟可复现）

在同套三表上跑三种写法并比对行数（🔧 方法：`dbwave_w7_dbill\exp2_sql_advanced.py` 增补三行即可）：

```sql
-- A 正确：过滤放 ON（保留侧语义不破坏）
SELECT t.name,d.dept_name FROM teach t LEFT JOIN department d ON t.dept_id=d.dept_id AND d.dept_id<3;
-- B 陷阱：同谓词挪到 WHERE → 退化为 INNER（NULL 行被滤光）
... WHERE d.dept_id<3;
-- C 补救：WHERE 里放行级过滤但补 OR d.dept_id IS NULL
```

教学结论：LEFT JOIN 的 ON 是"连接条件"，WHERE 是"连接后过滤"——一句话背下来不如一次行数对比。外连接的另一半代价在 08 章：优化器对左侧驱动的改写自由度更低。

## 11. 补充：视图更新性的直觉判据

可更新视图≈"每个目标行能唯一还原为基表操作"：单表+投影/选择的视图多数可更新（WITH CHECK OPTION 防"看窗外"）；带 JOIN/聚合/DISTINCT/GROUP 的视图基本只读。教材 DEFINER/INVOKER 权限语义在 12 章展开；🔧 SQLite/DuckDB 对可更新视图的支持面窄（SQLite 仅简单视图可直更，复杂需 INSTEAD OF 触发器）——**"用触发器伪造可更新视图"是本单元最好的高阶练习**（与 07 索引章无冲突，可课后跑）。

## 12. 自测五问

1. `COUNT(*)` 与 `COUNT(col)` 在含 NULL 组的差异？（前者计行、后者跳 NULL——03 章 NULL 语义的聚合面。）
2. RANK 与 DENSE_RANK 对并列的不同跳号？（RANK 跳、DENSE 不跳、ROW_NUMBER 强拆——给序列 (90,90,85) 各写一遍。）
3. 为什么 HAVING 里放 `AVG(grade)>80` 合法而 `grade>80` 不合法（标准 SQL）？（组内无单行 grade 可指；SQLite 方言宽容见 2 节警告。）
4. NOT EXISTS 与 NOT IN 对空表/含 NULL 的四种组合结果？（空表：两者全放行；NULL：IN 变 UNKNOWN、NOT IN 恒不真——画真值表。）
5. CTE 何时退化为"内联宏"而非"物化缓冲"？（SQLite 3.35 前默认物化、后默认复用策略变；DuckDB 优化器可内联——方言细节 ⚠️ 以版本线为准，考点是"两种语义都合法"。）

## 13. 窗口函数进阶三题（可跑，SQLite/DuckDB 双解）

1. **运行合计**：`SUM(amt) OVER(PARTITION BY student ORDER BY day)` —— 累计 GPA/账单原型。
2. **同比/环比**：`LAG(grade,1) OVER(PARTITION BY student ORDER BY day)` 求相邻差值；注意 LAG 跳不出"缺日"陷阱（补日历表再 JOIN——06 章"日期不是维度表"的教训）。
3. **组内 Top-K**：`ROW_NUMBER() ... WHERE rn<=2` 需外套查询（SQLite）或 QUALIFY（DuckDB，🔧 exp2 已实测）——**方言糖的差异恰好暴露"逻辑上先窗口后过滤"的求值序**。

三题共用 exp2 数据集，改三行 SQL 即得课堂全套；求值序板书建议：FROM→WHERE→GROUP→HAVING→窗口→QUALIFY/WHERE(外)→ORDER→LIMIT。

## 14. 子查询→连接的改写直觉表

| 子查询形态 | 等价改写 | 注意 |
|---|---|---|
| `WHERE x IN (SELECT ...)` | 半连接 JOIN+DISTINCT | 去重防放大 |
| `WHERE (SELECT MAX..)` 标量 | 聚合 JOIN 或窗口 | 空输入时标量为 NULL |
| `EXISTS(相关)` | 半连接 | 短路语义保留 |
| `NOT IN(可空)` | `NOT EXISTS` | NULL 免疫改写（本单元头号戒律） |
| `SELECT (相关标量) FROM..` | LEFT JOIN 聚合 | 一对多变多列聚合 |

优化器做不做这些改写因引擎而异（08 章 unnesting），但**人会改写=面试与调优双得分**。

## 核心概念速览（中英对照）

- **INNER/LEFT/RIGHT/FULL JOIN** — 内/左/右/全外连接：保留侧+NULL 补齐
- **NATURAL JOIN** — 自然连接：同名列自动合并，工业禁用
- **CROSS JOIN** — 交叉连接：无谓词笛卡尔积
- **GROUP BY / HAVING** — 分组/组级过滤：行级与组级的分界
- **aggregate function** — 聚合函数：折叠组为单值（COUNT/SUM/AVG/MIN/MAX）
- **correlated subquery** — 相关子查询：逐行参数化内层
- **EXISTS / NOT EXISTS** — 半连接谓词：NULL 免疫的安全写法
- **derived table / inline view** — 派生表：FROM 位置的子查询
- **CTE (WITH)** — 公用表表达式：命名、可复用、可读性枢纽
- **window function** — 窗口函数：不折叠行的聚合/排名
- **ROW_NUMBER / RANK / DENSE_RANK** — 排名三兄弟：跳号与并列之辨
- **QUALIFY** — DuckDB 方言：窗口结果直滤糖
- **VIEW** — 视图：存储查询、外部层落地
- **UNION / INTERSECT / EXCEPT** — 集合三运算：去重与保重（ALL）
- **CASE expression** — 条件表达式：行内分支与透视原料
- **cursor / DB-API** — 游标/数据库接口：嵌入式 SQL 的今昔两副面孔

## 最新演进与工业实践

- **窗口函数已是工业 SQL 默认武库**：dbt/仓内分析模型大量依赖 LAG/RANK；教材"advanced"定语在 2024–2026 已名不副实——面试与代码评审视其为基本功。
- **DuckDB 方言扩散**：QUALIFY、PIVOT、`range()`、`read_csv_auto` 等被多家引擎跟进借鉴（DuckDB_in_Action 04 章有同题演练）。
- **SQLite JSON+窗口双能力**：3.25+ 窗口、3.38+ 物化生成列，教材附录若还写"SQLite 不支持窗口函数"已过时 ⚠️ 以版本线为准。
- **向量检索新翼**：2024–2026 各引擎以向量类型/索引扩展 SQL（pgvector、SQLite 向量扩展、DuckDB 社区扩展），把"相似查询"纳入 SELECT 语法——传统教材未及的新增面，可作课堂讨论题 ⚠️ 生态碎片化注意甄别。
