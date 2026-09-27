# 12 · 附录：SQL 基础与物理层 primer（第 12 章 The Basics of SQL, pp.261-277 + 在线 Bonus 两章 + 尾部材料）

> 本章文件为**精读重构**，非原书文本。章题与页区间 ✅ Crossref 实抓（"The Basics of SQL" 261-277；"Query Optimization and Plan Selection" Bonus3-Bonus24；"A Simple Performance Model for Databases" Bonus25-Bonus28；三条记录均无 author 字段 ⚠️）。本章把全书"最后三块地基"收进一个文件：SQL 速成、I/O 粗算、优化器入门——它们共同构成通往物理设计的引桥。

## 一、第 12 章《SQL 基础》：建模者视角的 SQL 速成

- **定位**：不是 SQL 教程大全，而是"读懂第 5 章映射产物"所需的最小语言集——DDL（CREATE TABLE/约束）、DML 四件套、JOIN 代数直觉、GROUP BY 聚合、视图与授权点到 ⚠️（小节划分未实抓）。
- **特色讲法（书脉口径重构 ⚠️）**：每个 SQL 构造都回挂 ER 语义——`NOT NULL`=全参与、`REFERENCES`=联系的键落点、`CHECK`=业务规则的最后防线、`PRIMARY KEY`=实体唯一性承诺。**"SQL 是 ER 的机器方言"**是本章的存在理由。
- 与 repo 分工：语法纵深与引擎行为差异在 [../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md) 与 [../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)、[../数据库系统概念6/04-中级SQL.md](../数据库系统概念6/04-中级SQL.md)、[../数据库系统概念6/05-高级SQL.md](../数据库系统概念6/05-高级SQL.md)；本目录不重讲语法。
- 🔧 **SQLite 3.45.3 实测要点**（demo3.py 及追加验证）：
  1. FK 默认**不强制**，须 `PRAGMA foreign_keys=ON`（开启后非法引用插入抛 `FOREIGN KEY constraint failed` ✅ 实测）；
  2. `CHECK` 约束建表即生效，与 PG/SQL Server 一致 ✅；
  3. JSON1 扩展 `json_each()` 可用（08/09 文件"嵌套拍平"演示成立 ✅ 实测），本机内建版本 3.45.3（`sqlite3.sqlite_version`）。

## 二、在线 Bonus：《查询优化与计划选择》（Bonus3-Bonus24）

- **性质**：物理设计引桥章——同作者群的 Physical Database Design 书第 3 章的教科书缩进版（[../Physical_Database_Design/03-查询优化与计划选择.md](../Physical_Database_Design/03-查询优化与计划选择.md)），两册同源，读其一可跳其二 ⚠️ 同源关系按作者群与章题推断。
- **内容骨架（重构 ⚠️）**：逻辑等价变换（谓词下推/投影提前）→ 连接顺序与算法（NLJ/索引 NLJ/排序归并/哈希 join）→ 索引如何改变计划空间 → 统计与选择率粗算 → "设计者为什么要懂优化器"：**你建的每个键/外键/范式决策，最终都由优化器用代价复读**。
- 对建模读者的三条直用结论：
  1. 桥接表两端无索引 → M:N 查询走全扫（第 5 章 R7 的物理尾巴）；
  2. 反范式省 JOIN 的收益要用"计划是否真被换掉"验证，不看直觉（第 7 章账本的方法论）；
  3. 选择率估算依赖数据分布——模式再对也怕统计谎报（PDD 第 10 章抽样问题的预告）。

## 三、在线 Bonus：《简单数据库性能模型》（Bonus25-Bonus28）

- 4 页极简 I/O 账：行宽×行数估页数、聚簇因子概念、随机 vs 顺序 I/O 单价差——为 Bonus 优化章提供代价单位 ⚠️ 公式细节未实抓，按 PDD 附录 A（同题同名，页 371-374）同谱系转述。
- 2026 视角：SSD 时代"随机/顺序单价差"收窄但**放大为缓冲池命中率与预取粒度问题**，模型的"以页为账本单位"思想不变（[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 存储层展开）。

## 四、尾部材料一览（Preface ix-xii / References 279-284 / Exercises 285-290 / Solutions 291-293 / Glossary 295-300 / Index 301-304，均 ✅ 实抓）

- **Preface**（⚠️ 未实抓文本）：书脉惯例是声明"面向高年级/研究生与从业者，最小先修=一门 SQL"；5e 前言应含对 Chen 1980 第 1 版的致敬句——此句**未核实，不引用**。
- **Exercises+Solutions**：本目录各章"易错点与自测"即参照该体系编写；
- **Glossary**：与本目录各文件"核心概念速览"互补——中英对照表可当它的中文镜像用。

## 五、全书收束：从概念到物理的完整链条（00→12 的终点图）

```
需求(4) ─ ER/UML(2,3) ─ 映射(5) ─ 质检(6) ─ 案例(7) ─ 扩展(8,9,10) ─ 工具(11)
                                                        │
                                        SQL 方言(12) + 优化器/代价(Bonus)
                                                        │
                                              →→→ 物理设计（交给 PDD 书系）
```

**自测五问**：① 用 ER 词汇解释四种 SQL 约束；② 为什么 FK 不建索引是"设计正确、物理欠账"的典型；③ 选择率如何把建模决策变成计划差异；④ I/O 模型里"页"的替身在现代引擎中是什么；⑤ 本书止于哪一步、下一本书从哪步开始。

## 补充一、SQL 速成三遍法（本章给自学者开的路）

- 第一遍·能跑（约 6 小时）：SELECT/WHERE/JOIN/GROUP BY/DDL 约束五件套，用第 7 章 DDL 骨架灌 100 行假数据，写 20 条查询；
- 第二遍·能审（约 10 小时）：子查询↔连接等价改写、NULL 三值逻辑陷阱（`<>` 漏 NULL、NOT IN 含 NULL 全空）、聚合过滤 HAVING vs WHERE 的时机——每条陷阱各造一个反例数据验证；
- 第三遍·能省（约 10 小时）：`EXPLAIN QUERY PLAN`（SQLite）逐条回看第一遍查询：全扫/索引/物化临时表三种计划各认出十次；把"第 5 章哪条规则导致这条 JOIN"讲成口头禅；
- 判据：能把任意一条查询改写成"ER 路径叙述"（从哪个实体出发、沿哪条联系、什么谓词过滤）即出师。

## 补充二、优化器五问（Bonus 章读后自测，答案都在本文件第二节）

1. 谓词下推改变结果吗？改变的是哪张中间表的基数估计？
2. 为什么"小表驱动大表"在有索引 NLJ 时代仍是口语正确、机理含糊？
3. 排序归并连接吃的两大成本是什么？哈希连接替代了其中哪一个？
4. 统计过期时优化器最先选错哪类计划？举"桥表无索引→嵌套全扫"为例；
5. 反范式省掉一跳 JOIN，什么情况下计划层根本没变？（连接消除未触发/谓词仍需回表）

## 补充三、I/O 账本的现代重算（把 Bonus 模型搬进 2026 硬件）

- 原模型三量：行宽×行数→页数；随机 I/O 单价 ≫ 顺序 I/O；缓冲池命中率是折减系数 ⚠️ 框架转述；
- 当代换轴：NVMe 使随机/顺序单价差从百倍收敛到个位数倍，但**页带宽与 CPU 解码成本**接管瓶颈——向量化引擎（DuckDB/ClickHouse）的账本单位是"列块+SIMD"，不是"页"（[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 同题）；
- 不变式仍有两条：**统计质量决定计划质量**；**模式的 JOIN 拓扑决定计划空间形状**——逻辑设计对物理层的这两条因果链没有因硬件换代而松弛；
- 🔧 复算演示法：同一聚合查询在 SQLite 行存与（若本机已 pip 装 duckdb）列存上对比耗时与 `EXPLAIN`，记录"扫描字节数"差异来源——数字随机器浮动，只引用数量级与机理，不引用绝对值。

## 补充四、尾部材料的再利用建议

- Glossary（295-300）与本目录 12×「核心概念速览」互为中英镜像——复习时遮住一栏默写另一栏；
- Exercises+Solutions（285-293）：设计题优先重做，语法题可跳；
- References（279-284）：ER 谱系早期文献可整体导入 [../../db/db.md](../../db/db.md) 论文线做批量 DOI 校验。

## 补充五、SQL 基础章的"建模者错题本"（重构 ⚠️ 通用清单）

- `NOT IN (子查询含 NULL)` → 结果恒空：三值逻辑第一课，反连接请改 `NOT EXISTS` 或 LEFT JOIN…IS NULL；
- `COUNT(col)` vs `COUNT(*)`：前者跳过 NULL——参与约束没写 NOT NULL 时，计数口径悄悄变了；
- `GROUP BY` 后 SELECT 非分组列：不同方言宽严不一（SQLite 放行、PG 报错）——**方言宽容≠语义正确**；
- 隐式类型转换杀死索引：字符串列配数字谓词——第 5 章"列类型选择"的物理侧利息；
- `ORDER BY` 依赖插入序：没有显式排序就没有顺序承诺（"上次查询都对"是最贵的误解）；
- DDL 的注释即文档：列注释/表注释字段（COMMENT）是第 11 章数据字典的最小投入。

## 补充六、本章一页总结（兼全书收束）

- 第 12 章+Bonus 三件套的本质：**把"逻辑设计正确"升级为"在真实引擎上成立"**——SQL 是表达层，优化器是裁判层，I/O 模型是账本层；
- 建模者学这三样的深度标尺：能读懂自家系统 Top 20 查询的执行计划、能对一条慢查询说出"模式责任还是物理责任"、能估算一次反范式化的存储与一致性成本——三问过线即可出本书；
- 全书终点回到第 1 章起点：**语义在概念层立约，在逻辑层翻译，在物理层结账**——本书教会前两步，结账请持本目录互链表去 Physical_Database_Design 与索引笔记的柜台。

### 本文件实测环境备忘（可复跑）

- 环境：Windows + Python 3.13（内置 sqlite3 链接库版本 3.45.3）；
- 步骤：`python D:\develops\tmp\dbwave_dmd5e\demo3.py` 一次跑完全部六项断言，逐行打印结果；
- 追加单测（可选两分钟）：
  `python -c "import sqlite3;d=sqlite3.connect(':memory:');d.execute('CREATE TABLE t(x CHECK(x>0))');print([d.execute('INSERT INTO t VALUES(-1)'] and 'no' or 'x')"` ——观察 IntegrityError 即 CHECK 生效 ✅；
  `python -c "import sqlite3;d=sqlite3.connect(':memory:');print(d.execute(\"select value from json_each('[1,2,3]')\").fetchall())"` ——json_each 可用 ✅；
- 注意：以上两处为演示级引号嵌套，实际复跑建议落成临时 .py（照旧写 `D:\develops\tmp\`，repo 零产物）。

## 核心概念速览（中英对照）

1. **DDL 四约束** — primary key/foreign key/check/not null：ER 语义的 SQL 方言
2. **等价变换** — logical equivalence：谓词下推等不改结果的改写
3. **连接算法** — join algorithms (NLJ/merge/hash)：计划空间的执行底座
4. **聚簇因子** — clustering factor：键序与物理序的贴合度
5. **选择率** — selectivity：谓词过滤比例的估计量
6. **统计信息** — statistics：优化器代价输入，数据的"体检表"
7. **I/O 成本模型** — I/O cost model：以页为单位的粗算框架
8. **顺序/随机 I/O** — sequential/random I/O：两种访问形态的单价差
9. **缓冲池** — buffer pool：SSD 时代性能账的真正主角
10. **PRAGMA foreign_keys** — SQLite 外键开关：默认关闭的方言差异
11. **引桥章** — primer chapter：为下游专书铺路的附录材料
12. **计划验证** — plan verification：用执行计划复核反范式直觉的手法

## 最新演进与工业实践

- **优化器入门的现状（2024-2026）**：教科书四算子框架仍成立；工业增量在——扩展统计（多列相关性）、自适应连接（Oracle SQL Plan Directives、SQL Server 自适应连接 ⚠️ 转述）、向量化+代价模型学习（Neo/Lucy 系 learned optimizer 研究，论文线 [../../db/db.md](../../db/db.md) 有 learned index/optimizer 条目可接）。
- **SQL 标准演进**：SQL:1999 之后 SQL:2003 窗口、SQL:2016 行属性、SQL:2023 图查询（MATCH）陆续落地——本章的"最小 SQL 集"今天对应 PG/SQLite 文档入门链 ✅ https://www.postgresql.org/docs/current/ddl.html 、✅ https://www.sqlite.org/lang_createindex.html（curl 200）。
- **SQLite 的教学地位上升**：作为"零安装参考实现"，本章内容 + 🔧 demo 组合被 2020s 课程普遍采用 ⚠️ 趋势口径；Python 3.13 内建 sqlite3 链路全通（本机实测环境）。
- **波内兄弟衔接**：[#87《Using SQLite》](../Using_SQLite/00-总览与阅读地图.md)、[#134《DuckDB: Up and Running》](../DuckDB_Up_and_Running/00-总览与阅读地图.md)（均已落盘，00 第十节义务波尾闭环）——它们的向量化执行正是"简单 I/O 模型"该被重写的地方。
- 🔧 **全部实测汇总**（本机 Python 3.13 + SQLite 3.45.3，脚本 `D:\develops\tmp\dbwave_dmd5e\demo3.py`）：桥接表+FK 拦截 ✅；有损分解 (s,g)+(c,g) 自然连接得 5 行 vs 原 3 行（2 个增广元组）✅；无损分解 (s,c)+(c,g) 重建 0 缺 0 增 ✅；弱实体 FK+CASCADE 孤儿拦截 ✅；`json_each()` 可用性 ✅；`PRAGMA foreign_keys` 默认 OFF 行为差异 ✅。
