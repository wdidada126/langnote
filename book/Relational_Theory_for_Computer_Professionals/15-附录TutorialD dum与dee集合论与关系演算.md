# 附录 A–E　Tutorial D 语法、TABLE_DUM/TABLE_DEE、集合论与关系演算

> 译本 p185–215｜五个附录标题 ✅ 实抓自译本目录：A Tutorial D 语法 / B TABLE_DUM 和 TABLE_DEE / C 集合论 / D 关系演算 / E 进阶阅读指南。附录 B 的英文写法 `TABLE_DUM`/`TABLE_DEE` 是作者固定记号，不算回译；其余英文标题 ⚠️ 回译。
> 本文件是**精读重构**：附录正文/条目清单未能逐字取得，凡依作者公开体系（TTM/教程传统）转述处一律 ⚠️；Tutorial D 代码一律标 ⚠️ 示意，不声称是原书代码；SQL 对照处用本机 Python `sqlite3`（3.45.3）实测标 🔧（**验证的是 SQL 行为，不是 Tutorial D 行为**）。
> 各附录的"落点章"：A→第 2/4/5/7 章语法汇总；B→第 4/6 章比较与断言；C→第 2 章头/体；D→第 4/5 章算子；E→全书延伸。

## 附录地图

| 附录 | 讲了什么 | 一句话结论 |
| --- | --- | --- |
| A Tutorial D 语法 | 第 2–9 章零散使用的记号集中成一页速查 | Tutorial D 不是新理论，是**前文全部公设的可书写形式** |
| B TABLE_DUM 和 TABLE_DEE | 两个零度关系常量及其定律 | 布尔值必须能装进关系层次，否则"一切皆关系"是半吊子 |
| C 集合论 | 本书真正用到的集合论最小机器 | 头无序、体去重、外延相等——三个决定全在这页纸上 |
| D 关系演算 | 元组演算/论域演算与代数的等价 | SQL 的 WHERE 形正是元组演算的语法糖，**丢安全限定的那部分** |
| E 进阶阅读指南 | 书目 | 通往 TTM 与三部曲其余两本的门口 |

## 核心精讲

### 1. 附录 A：Tutorial D 语法脉络

作者把语法按"类型 → 变量 → 查询 → 更新 → 数据库级"五层给出。速查表（⚠️ 依第 2–9 章与前两本教程书的公开形态汇总，**不保证逐字**）：

| 层 | 记号（⚠️ 示意） | 出处章 |
| --- | --- | --- |
| 类型 | `TUPLE {SN SNO, STATUS INTEGER}`、`RELATION { ... }`（类型产生器） | 第 2、7 章 |
| 域 | `DOMAIN SN DOMAIN IS STRING ...`（命名类型 + 可选谓词） | 第 7、13 章对照 |
| 声明 | `VAR S RELATION {SN SNO, STATUS INTEGER, CITY NAME} KEY {SN};` | 第 2 章 |
| 查询算子 | `WHERE p`（σ）、`{ X }`（π）、`RENAME`（ρ）、`TIMES`（×）、`MINUS`（−）、`AND`/`OR`/`NOT`（关系级逻辑）、`PLUS`（广义并）、`DIVIDED BY`（÷）、`MATCHING BY`/`NOT MATCHING BY`（半/反半联接）、`EXTEND`、`SUMMARIZE ... ADD 聚集` | 第 4、5 章 |
| 更新 | `S := <关系表达式>`；`INSERT`/`DELETE`/`UPDATE` 为其派生缩写 | 第 4、7 章 |
| 数据库级 | `CONSTRAINT 名字 : <必须为真的谓词>`、`ASSERTION`、`VIEW`、`TRANSACTION START/COMMIT/ABORT` | 第 6、8 章 |

一组连贯示例（S/P/SP 例库，⚠️ 示意）：

```
-- 声明 + 查询 + 约束，三种句子各给一行
VAR S RELATION {SN SN#, STATUS INTEGER, CITY CITY#} KEY {SN} ;
Q : S WHERE CITY = 'Paris' { SN } ;
CONSTRAINT s_status_nonneg : ( S WHERE STATUS < 0 ) IS_EMPTY ;
```

三条语法原则，正是前几章公设的书写形式：**每个查询构造都是返回关系的表达式**（闭包，第 4 章）；**赋值是唯一的更新原语**（第 7 章 7.5）；**类型在定义时强制**（第 7 章 7.2，🔧 反例见 07 的 typeof 混住）。SQL 对照与逐条差异不在本文件展开——那是本目录第三部分（→ [10-SQL基本表.md](10-SQL基本表.md) ～ [14-SQL与关系模型.md](14-SQL与关系模型.md) 的偏差清单）的分工；语法层的另一半可执行讲法见 [../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md](../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md)（Tutorial Dees，同谱系的教学方言）。

### 2. 附录 B：TABLE_DUM 与 TABLE_DEE——把布尔值装进关系层次

**定义**（这是零度关系的通行定义，⚠️ 转述附录 B 立场）：

| 常量 | 度 | 元组 | 基数 | 直觉 |
| --- | --- | --- | --- | --- |
| `TABLE_DEE`（dee） | 0 | 恰含一个 0 元组 `()` | 1 | **关系层次的 TRUE** |
| `TABLE_DUM`（dum） | 0 | 不含元组 | 0 | **关系层次的 FALSE** |

**为什么非要这两个常量**：模型说"数据库里的一切都是关系"。可查询语言里必然出现"存在/为空/必须为真"这类**命题**。如果布尔值不是关系，表达式系统就被劈成两半：算子（关系进关系出）与谓词（关系进布尔出）之间没有回程通道。`IS_EMPTY(r)` 是"关系→布尔"的出口，`dee/dum` 是"布尔→关系"的入口——**有了双向翻译，断言才能写成关系等式**，第 6 章的"约束 = 反例关系为空"才在形式上闭合。

**定律**（⚠️ 依附录 B 的一贯表述转述；可推导的给出理由）：

- `r TIMES TABLE_DEE = r`：乘积基数相乘，`|r| × 1 = |r|`，度加 0 ⇒ 恒等。dee 是 TIMES 的**幺元**。
- `r TIMES TABLE_DUM = r 的头上的零基数关系`：`|r| × 0 = 0` ⇒ dum 是 TIMES 的**零元**（"r 的恒假改写"）。
- **AND（关系合取）以 dee 为幺元：`r AND TABLE_DEE = r`**；OR/PLUS（广义析取）以 dum 为幺元：`r PLUS TABLE_DUM = r`。两条互为对偶。⚠️ `AND`/`PLUS` 在头不同时的精确定义（经乘积/广义并构造）此处不逐字转写，以 TTM 附录原文为准——本笔记只用到幺元/零元这两条可推导的形态。
- **零度投影是布尔→关系的桥**：把 r 投影到空头，得 `dee`（若 r 非空）或 `dum`（若 r 为空）。于是"存在反例"这件事第一次成为一个**关系值**，可以被 `=`、`MINUS` 继续运算。

**断言出口（接第 6 章）**：6.2 那条 `ASSERT` 的等式形态 `（反例表达式） = TABLE_DUM`，严格读需要一个隐含步骤——先把反例关系零度投影再与 dum 比较；直接对度非零的关系写 `= TABLE_DUM` 在"同头才许比较"的语法下类型不通 ⚠️（本文件的一个诚实脚注：06 中该式标了示意，此处把机制讲透；更保险的写法是 `IS_EMPTY`）。

🔧 SQL 侧：零度关系整个缺位（SQLite 3.45.3，方法=直接查询）：

```sql
SELECT 1;              -- -> [(1,)]  列名 expr_0：这是一度一元关系，不是 dee
SELECT 1 WHERE 0;      -- -> []      同理，它也不是 dum，只是"空的一度关系"
SELECT EXISTS (SELECT 1 FROM S WHERE CITY='Paris');  -- -> [(1,)]
```

`EXISTS` 返回**整数** 0/1（D6/D6b/D6c）：布尔值不在 SQL 的类型系统里，也不在关系的层次里——它被逐出了模型，只能在谓词位置（WHERE/HAVING）当临时工。这就是第 14 章清单里"没有零度关系"一条的实测证据。

### 3. 附录 C：够用的集合论

附录 C 不是集合论教程，而是把前文反复赖账的几个"集合事实"集中交代。本目录视角下真正承重的三条：

| 集合论事实 | 模型结论 | 在 SQL 里塌掉的样子（🔧 见 01/02/14） |
| --- | --- | --- |
| 头是**属性名的集合**：无序 | 交换列序是同一关系 | `UNION` 按位置不按名字（D2）；`SELECT *` 按位置消费 |
| 体是**元组的集合**：外延公理 ⇒ 无重复 | 两个相同元组只算一个 | 表允许重复行（D1）；靠 rowid 物理位置区分不可区分的元组（D1c） |
| 集合相等 = 含同一批元素 | `r1 = r2` 是良定义的关系比较 | 比较运算符不对表可用，只能双向 EXCEPT 绕（D10e） |

袋语义（bag）与集合的分野在这里定调：**不是数学上不允许袋，而是模型的公设选了集合**，SQL 为性能默认袋又拒绝承认（第 14 章 #1）。⚠️ 附录是否涉及序偶的形式定义（Kuratowski 编码等）无法从目录确认，本笔记按"关系模型最小必需"重构，不声称覆盖。

### 4. 附录 D：关系演算——元组式与论域式

**两种演算**（学院口径，与 [../数据库系统概念6/06-形式化关系查询语言.md](../数据库系统概念6/06-形式化关系查询语言.md) 一致）：

- **元组关系演算**（Codd 1971/1972 ⚠️ 年份口径）：`{ t | P(t) }`，变量 t 遍历**元组**，P 是由 `∧ ∨ ¬ ∃ ∀` 构成的谓词公式。
- **论域（域）关系演算**：`{ <x1, ..., xn> | P(x1, ..., xn) }`，变量直接遍历**域中的值**。表达力与元组演算等价，书写更"扁平"。
- SQL 的 `SELECT ... WHERE` 形就是元组演算的直接语法借用：`WHERE` 里放谓词，`SELECT` 里放投影。**关系代数是程序性的（怎么算），演算是描述性的（要什么）**——附录 D 在本书的功能是给出"每个代数算子的等价声明式形式"这块判据。

**算子 ↔ 演算模板对照**（05 章欠的那张表）：

| 代数算子 | 演算模板 | SQL 近似（🔧 本目录已测） |
| --- | --- | --- |
| `r WHERE p`（σ） | `{ t ∈ r | p(t) }` | `SELECT * FROM r WHERE p` |
| `r { X }`（π） | `{ t | ∃u (u ∈ r ∧ t 是 u 在 X 上的限制) }` | 必须补 DISTINCT（D4） |
| `UNION` / `MINUS` | `∨` / `∧ ¬` | UNION / EXCEPT（D4c） |
| `TIMES`（×） | `∃u ∃v (u∈r1 ∧ v∈r2 ∧ t 是 u,v 拼接)` | CROSS JOIN（D4b） |
| `MATCHING BY`（半联接） | `{ t ∈ r | ∃u (u ∈ s ∧ t(X) = u(X)) }` | `WHERE EXISTS (...)`（D5b） |
| `NOT MATCHING BY` | `{ t ∈ r | ¬∃u (u ∈ s ∧ t(X) = u(X)) }` | `WHERE NOT EXISTS (...)`（D5c） |
| `DIVIDED BY`（÷） | `{ t | ∀u (u ∈ s → tu ∈ r) }` ≡ 双重否定 `¬∃u (u∈s ∧ tu∉r)` | 双 NOT EXISTS（D5d；漏 DISTINCT 即退化袋语义，D5e） |
| `IS_EMPTY r` | `¬∃t (t ∈ r)` | `COUNT(*) = 0`（绕道整数，见 B 节 🔧） |

**安全性**：无限域上 `{ t | ¬(t ∈ r) }` 有无穷多解，不可计算。演算必须加"安全"限定（可判定等价的系统化论述见 Chandra & Harel《Computable queries for relational data bases》，✅ DOI 10.1016/0022-0000(80)90032-x 过 Crossref；⚠️ Crossref 日期字段为 1980-10，常见引年为 1985，以 Crossref 记录为准但两者并存说明）。本书第 7 章的算子安全性公设是同一要求的代数版本：**结果永远有限且良定义**。关系演算在工业里没有直接产品，但它是 SQL 子查询语义的裁判语言——第 11/12 章每问一遍"这个子句求值是关系还是表"，用的就是这个裁判。

### 5. 附录 E：进阶阅读指南

⚠️ 具体条目未取得，按作者谱系的重构：出口是《The Third Manifesto》（Tutorial D 的完整规范来源）、《An Introduction to Relational Database Theory》（理论版全集）、同作者《SQL and Relational Theory》（本目录已建：[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)）与 Codd 原论文（repo 精读笔记：[../../paper/doi_10.1145_362384.362685/00-精读笔记.md](../../paper/doi_10.1145_362384.362685/00-精读笔记.md)）。设计向续读：#8《Database Design and Relational Theory》目录版 [../Database_Design_and_Relational_Theory/00-总览与阅读地图.md](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md)。动手向：用代码实现附录 A/B 的算子与 dum/dee（[../BuildYourOwnDatabaseFromScratch.md](../BuildYourOwnDatabaseFromScratch.md)、[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)）。

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「dum/dee 是理论玩具」 | 它们检验表达系统是否闭合：没有"布尔→关系"回程，断言就只能活在 SQL 的整数值里（🔧 D6c） |
| 「dee = 只有一行的表，dum = 空表」 | 是**零度**关系：dee 的那一行没有列。`SELECT 1` 不配当 dee（🔧 D6） |
| 「附录是补遗，可跳过」 | 附录 B 是第 6 章断言形式的机关所在；附录 D 是第 4/5 章算子的声明式孪生 |
| 「演算 vs 代数是两种查询语言之争」 | Codd 定理：安全演算 ≡ 代数。差别在书写范式，不在能力（无限域上另谈，见安全性） |
| 「SQL 子查询 = 关系演算」 | 形似神异：3VL 让谓词不是真值函数（06/13 章），袋语义让"集合构造括号"不成立 |
| 「Tutorial D 语法背下来就行」 | 语法只是五层公设的书写；背记号不背闭包性，等于没读附录 A |

## 与其他章 / 其他书的联系

- 附录 A 语法 ↔ 各算子正文：[04-关系运算符Ⅰ.md](04-关系运算符Ⅰ.md)、[05-关系运算符Ⅱ.md](05-关系运算符Ⅱ.md)；类型与赋值公设：[07-关系模型.md](07-关系模型.md)。
- 附录 B ↔ 断言的等式写法：[06-约束和断言.md](06-约束和断言.md)；`IS_EMPTY` 的出场：[04-关系运算符Ⅰ.md](04-关系运算符Ⅰ.md)。
- 附录 C ↔ 头/体与值/变量分离：[02-关系和关系变量.md](02-关系和关系变量.md)、[10-SQL基本表.md](10-SQL基本表.md)；偏离总账：[14-SQL与关系模型.md](14-SQL与关系模型.md)。
- 附录 D ↔ 半联接/除法的算子定义：[05-关系运算符Ⅱ.md](05-关系运算符Ⅱ.md)；SQL 侧逐子句问"求值是关系还是表"：[11-SQL操作符Ⅰ.md](11-SQL操作符Ⅰ.md)、[12-SQL运算符Ⅱ.md](12-SQL运算符Ⅱ.md)。
- 学院口径的演算（记号更形式化、例题更多）：[../数据库系统概念6/06-形式化关系查询语言.md](../数据库系统概念6/06-形式化关系查询语言.md)。
- 可执行的教学方言（Tutorial Dees）与关系代数纠偏：[../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md](../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md)、[../SQL_and_Relational_Theory/02-关系代数与封闭性.md](../SQL_and_Relational_Theory/02-关系代数与封闭性.md)。
- 关系模型与元组演算的原始出处：[../../paper/doi_10.1145_362384.362685/00-精读笔记.md](../../paper/doi_10.1145_362384.362685/00-精读笔记.md)。
- 设计续读（范式与依赖的操作性步骤）：[../Database_Design_and_Relational_Theory/00-总览与阅读地图.md](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **TABLE_DEE（dee）** — zero-degree relation, one tuple：零度一元关系，关系层次的 TRUE
- **TABLE_DUM（dum）** — zero-degree relation, no tuple：零度零元关系，关系层次的 FALSE
- **零度投影** — projection on empty heading：把 r 折成 dee（非空）或 dum（空），布尔与关系的双向翻译桥
- **幺元/零元定律** — identity/annihilator laws：`r TIMES DEE = r`、`r AND DEE = r`、`r PLUS DUM = r`、`r TIMES DUM = 恒假关系`
- **断言的关系等式形态** — assertion as relation equation：约束 = "反例关系是 dum"（→ 06 章）
- **元组关系演算** — tuple relational calculus：`{ t | P(t) }`，变量遍历元组；SQL WHERE 的祖先
- **论域关系演算** — domain relational calculus：变量直接遍历域值，与元组演算等价
- **Codd 等价定理** — Codd's theorem：安全范围演算 ≡ 关系代数
- **安全性** — safety / range safety：无限域上的演算表达式必须有限且可判定（→ 07 章算子安全性公设）
- **外延公理** — axiom of extensionality：头无序、体去重、比较只看成员——附录 C 的三根承重柱
- **广义并 PLUS** — generalized union：允许头不同的关系析取，以 dum 为幺元（⚠️ 转述形态）
- **Tutorial D 五层结构** — five-layer syntax：类型/声明/查询/更新/数据库级，速查见附录 A

## 最新演进与工业实践

- **Tutorial D 谱系的当代实现**：作者的参考实现 Rel（⚠️ 其仓库地址本次未能核实可达，不附链）之外，开源可核的是 **TclRAL**——Andrew Mangogna 用 Tcl 实现的关系代数核心（Tutorial D 方言），主页本次 `curl -sI` 200：https://sourceforge.net/projects/tclral/ 与 http://tclral.sourceforge.net/ ✅；其 Python 封装 PyRAL 仓库 API 可达（https://api.github.com/repos/modelint/PyRAL ✅ 200，2026-05 仍有提交）。github.com 网页直读本机超时（curl 000），故以上以 API/SourceForge 口径标 ✅。
- **dateanddarwen 系站点可达性实测（2026-09）**：https://www.thedailydarwen.com/ 与 http://www.thirdmanifesto.com/ 本次均 curl 000（不可达）⚠️——TTM 旧官方站已下线，作者的公开写作现挂在 Darwen 的 https://www.dbdebunk.com/ （本次 200 ✅，Blogger 站，含论文索引页 /p/papers_3.html）。引用 TTM 附录原文时注意**原站不可达，需走检索缓存或纸质版** ⚠️。
- **演算/集合论在教科书与工业里的位置**：元组演算与 SQL 的对应仍是数据库教科书标配章（对照：../数据库系统概念6/ 的 06 章文件 ✅ 在盘）；工业产品没有直接暴露演算接口，但安全演算 ≡ 代数的等价性被查询优化器继承——代数树是 IR，声明式输入是用户接口（另见 [../Readings_in_Database_Systems/07-查询优化.md](../Readings_in_Database_Systems/07-查询优化.md)）。形式化源头：Chandra & Harel《Computable queries for relational data bases》，JCSS，✅ https://api.crossref.org/works/10.1016/0022-0000(80)90032-x （Crossref 200）。
- **SQL 标准进展与附录主题的关系（⚠️ 转述）**：SQL:2016/2023 两轮补的是 JSON 与属性图查询（SQL/PGQ），后续轮次（常称 SQL:2024/2025）方向仍是嵌套与图；**附录 B/C 关心的三件事——零度关系、集合去重、值/变量分离——一条都不在议程上**。ISO 官方页本次不可读（www.iso.org 返回 403 反爬），不附标准页链接；历史文本用公开镜像 SQL-1992（前轮 200 实抓，50794 行）：https://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt ⚠️ 仅作"当年就没有零度关系"的反证。
- **社区方言**：Tutorial D 风格的教学实现持续零星出现（本次 API 200 ✅：https://api.github.com/repos/k1complete/initiald 、https://api.github.com/repos/moerkb/core.relational ），共同点是**都不实现 RVA 与断言的完整层次**——附录 B 的布尔回装仍是这类语言最常被省略的一块，恰可自测对模型闭合性的理解。
- **一键复现**：本文件 🔧 证据全部出自 `D:\develops\tmp\dbwave_rtcp\rg_sqlite_demo.py`（输出 `demos.txt`）的 D1/D1c/D2/D4/D4b/D4c/D5b/D5c/D5d/D5e/D6/D6b/D6c/D10e 段（**SQL 行为，非 Tutorial D**）；repo 内零非 md 产物。
