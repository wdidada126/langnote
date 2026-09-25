# 07 缺失值的真实语义：「42 与 2」、Placeholder 与分解

> ⚠️ 原书归属推定：Part II NULL 深入章。Date 主张缺失值有**两类**，NULL 一刀切掩盖了这个区别。
> 「42 与 2」是作者用来戳穿 3VL 矛盾的著名口头例子（**其精确编号/原文措辞未在线核实，此处按作者一贯论证复述，标 ⚠️**）。
> 所有 SQL/代数式为 🔧 自拟教学示意，非书中原文。

## 核心概念速览（中英对照）

- **两类缺失值** — two kinds of missing value：IIT（值存在但**未知**）与 N/A（属性**本不适用**）。
- **值存在但未知** — value exists but unknown：如「某人确有个薪资，只是我没记下来」。
- **属性不适用** — attribute not applicable：如「未婚者的配偶姓名」——根本没有这个值。
- **占位符** — Placeholder：在域内挑一个**真实的、约定的**特殊值表示「不适用」，保持二值逻辑。
- **IIT / IIA** — value Is There but unknown / attribute Is Applicable：作者口径的分类标签（⚠️）。
- **relvar 分解** — decomposition：把「可空列」拆到独立 relvar，从根上消灭 NULL。
- **闭世界假设（CWA）** — closed-world assumption：数据库里没有的即视为假；与「未知」冲突时要显式处理。
- **开世界假设（OWA）** — open-world assumption：没记录不代表假，可能只是未知。
- **NULL vs `<empty>`** — null vs empty/default：Codd 后期提出用「默认值」区分两类缺失（SQL 标准未采纳）。
- **3VL 的代价** — cost of 3VL：等价式失效、聚合口径乱、外连接混淆（06 的根因）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 「42 与 2」的直觉 | 两个都写 NULL，语义却天差地别 | 一刀切是错的 |
| 7.2 IIT vs N/A | 存在但未知 / 不适用 | 处置策略应不同 |
| 7.3 Placeholder 方案 | 用域内真实约定值表达 N/A | 回到 2VL，等价式恢复 |
| 7.4 relvar 分解 | 把可选属性拆出去 | 存在性=有没有元组，而非列是否 NULL |
| 7.5 CWA/OWA | 「没有」是假还是未知 | 决定缺失值的正确建模 |

## 核心精讲

### 7.1 「42 与 2」到底在说什么

⚠️（按作者论证复述，非原文编号）核心场景：两个属性都填 NULL，但它们意思完全不同：

- 情形 A：一个员工的**电话号码**——他确实有电话，只是你暂时没录入。这是「值存在但未知」（IIT）。
- 情形 B：一个**未婚者的配偶姓名**——不存在这样一个值。这是「属性不适用」（N/A）。

SQL 让这两种情况都写成 NULL，于是查询、聚合、连接把「一个还没填」与「压根不该填」混为一谈。Date 用一个简单算术把荒谬挑明：

🔧 设某班成绩列里，有人「还没考（未知）」、有人「这门课对他不适用（缺考/免修）」。若两者都记 NULL，再求平均分：

```sql
-- 🔧 自拟
SELECT AVG(SCORE) FROM Exam;   -- 两种 NULL 都被跳过，得到同一个数
```

可真实语义下：「还没考」的人应当**排除在分母外**（等考了再算），而「不适用」的人**本来就不该进这个统计**。用同一个 NULL 无法区分，导致「42 道题对了几道 vs 只有 2 道题能做」这类分母混淆——这正是作者口中「42 与 2」式的笑话：同一个 AVG，两种缺失值给出错误且不可分辨的答案。⚠️ 具体数字与出处未在线核实，机制解释如上。

### 7.2 分类：IIT vs N/A，处置不同

| 类别 | 含义 | 例 | 正确处置 |
| --- | --- | --- | --- |
| 值存在但未知（IIT） | 有确定值，只是当前没掌握 | 待录入的电话 | 允许「未知」语义，补录后替换；参与逻辑时谨慎 |
| 属性不适用（N/A） | 对这个元组该属性无意义 | 未婚者配偶名、免修者分数 | 用**真实域值（Placeholder）**或**分解 relvar**，而非 NULL |

关键：**N/A 完全不需要 NULL**——它可以用一个域内的合法值（如 `SPOUSE_NAME` 域里约定 `'--none--'`）明确表示，从而让所有比较、德摩根、聚合回到二值逻辑正常运作。

### 7.3 Placeholder：用「一个真值」代替 NULL

Placeholder 是在属性的**域内**选定一个约定值来表示「不适用」。因为它是个**真实的域值**，所有 2VL 定律（05 章）继续有效：

🔧 对比：

```sql
-- 用 NULL：查“有配偶的”要用 IS NOT NULL，且与 IIT 混淆
SELECT * FROM Person WHERE Spouse IS NOT NULL;

-- 用 Placeholder '--none--'：条件就是普通二值比较，德摩根/双重否定全部成立
SELECT * FROM Person WHERE Spouse <> '--none--';
```

Placeholder 的代价：域里多了一个「魔法值」，且要 CHECK 约束保证它不与真实数据撞车（10 章）。收益：**逻辑回到干净的 2VL**，摆脱 3VL 的所有陷阱（6.2/6.3）。这是 Date 相对偏好的路线之一。

### 7.4 relvar 分解：把「可选」变成「存在与否」

更彻底的方案：**把带可空属性的信息拆到一个独立 relvar**，让「有没有值」变成「有没有对应元组」——存在性是二值的（有/无），天然没有 UNKNOWN。

🔧 原始（含 NULL 外键坑，见 08）：

```sql
-- 🔧 自拟：员工-部门，部分员工暂无部门
Employee(EmpID, Name, DeptID)   -- DeptID 常为 NULL
```

分解后：

```sql
-- 🔧 自拟
Employee(EmpID, Name)                                    -- 不含可空列
Assignment(EmpID, DeptID)  PRIMARY KEY(EmpID)            -- 有分配才有元组
-- 「暂无部门」= 在 Assignment 里没有该员工元组：存在性判断，二值、干净
SELECT EmpID FROM Employee
WHERE NOT EXISTS (SELECT 1 FROM Assignment a WHERE a.EmpID = Employee.EmpID);
```

这正对应关系模型的「外键所在 relvar 可空性 = 元组存在性」的纯正表达，也回应了 6.4 的 `NOT IN`→`NOT EXISTS` 改写。⚠️ 分解/Placeholder 是否作为独立章标题，第 3 版不可在线确证，此处按作者一贯立场组织。

### 7.5 CWA / OWA：没有记录意味着什么

- **闭世界假设（CWA）**：数据库当作世界的完备清单，「没这条元组」=「该命题为假」。此时「未知」根本不该出现（要么真要么假），NULL 更无立足点。
- **开世界假设（OWA）**：「没这条元组」可能只是「还不知道」。纯关系模型倾向 CWA；一旦引入「未知」就滑向 OWA，而这恰是 NULL/IIT 想表达的东西。

Date 的洞见：**如果你需要表达 OWA 的「未知」，那是应用语义，应该在建模层用显式结构（单独的 relvar、状态列）处理，而不是让 NULL + 3VL 在查询层偷偷替你做逻辑判断**。

## 常见误区

| # | 误区 | 纠正视角 |
| --- | --- | --- |
| 1 | 「NULL 就够了，不必区分缺失类型」 | IIT 与 N/A 语义/处置不同，混用致统计错（7.1） |
| 2 | 「不适用只能 NULL」 | Placeholder（域内真值）可回到 2VL（7.3） |
| 3 | 「可空列就是可选信息」 | 分解 relvar 用元组存在性表达，更干净（7.4） |
| 4 | 「AVG 自动处理缺失」 | 两类 NULL 同被跳过，分母混淆（7.1/6.5） |
| 5 | 「没记录=假」 | 需先定 CWA/OWA；否则未知被当假（7.5） |

## 与其他章 / 其他书的联系

- ← `05`：Placeholder 让德摩根/双重否定重新成立。
- ← `06`：3VL 代价的解药。
- → `08`：NULL 外键的分解式正解。
- → `10`：Placeholder 需要 CHECK/域约束背书。
- → [../../paper/doi_10.1145_362384.362685/00-精读笔记.md](../../paper/doi_10.1145_362384.362685/00-精读笔记.md)：Codd 原文的关系模型对「每个属性都有值」的坚持，是本章立场的源头。

## 文献与文档

- C.J. Date, *SQL and Relational Theory*, 3rd ed. —— 「两类缺失值」「Placeholder」「relvar 分解」立场（具体编号 ⚠️ 未核实）。
- E. F. Codd, 1970 & 后期关于 `<unknown>`/`<inapplicable>` 与默认值的讨论（互链 1970 精读）。
- Date & Darwen, *Foundation for Future Database Systems: The Third Manifesto* —— 反对 NULL、主张断言/约束的体系化论述（不引具体编号）。
