# 09 重复行、DISTINCT 与集合语义：bag 偏离的代价

> ⚠️ 原书归属推定：Part III 语义纠偏章。SQL 默认工作在**多重集（bag）**而非**集合（set）**语义上，
> 这是它对关系模型最 pervasive 的偏离。本文件系统排雷：重复行、DISTINCT、GROUP BY、UNION ALL、LEFT JOIN。
> 所有 SQL/代数式为 🔧 自拟教学示意，非书中原文。

## 核心概念速览（中英对照）

- **袋 / 多重集** — bag / multiset：允许元素重复的集合；SQL 表默认在此语义。
- **集合语义** — set semantics：关系模型所在，无重复（03）。
- **DISTINCT** — 去重开关，把 bag 折回 set。
- **ALL** — 保留重复的开关，如 `UNION ALL`、`COUNT(ALL col)`。
- **GROUP BY** — 分组；每组折叠为一行，重复在此「被利用」。
- **HAVING** — 对分组结果的限制（谓词），区别于 WHERE 对分组前的限制。
- **UNION vs UNION ALL** — 并（去重）vs 带重复的并；前者才等价关系 ∪。
- **LEFT JOIN** — 左外连接；右表无匹配则补 NULL（06.6/08.4）。
- **COUNT 陷阱** — count pitfall：`COUNT(*)` 把 JOIN 复制出的重复行也计入。
- **幂等性** — idempotence：集合去重后同操作再施加不变；bag 无此性质。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 set vs bag：一处根基偏离 | SQL 表=多重集，关系=集合 | 重复行是 bag 产物，非模型产物 |
| 9.2 DISTINCT 何时是「纠正」 | 投影天然去重（02.3） | 漏 DISTINCT=语义错，不止冗余 |
| 9.3 GROUP BY 的隐藏 DISTINCT | 分组即按键去重 | 组数=候选键投影的基数 |
| 9.4 UNION ALL 何时正当 | 性能 vs 语义 | 需要保重复（如计数明细）才用 ALL |
| 9.5 LEFT JOIN + COUNT 事故 | 外连接复制/补 NULL | 经典「计数偏大/偏小」双坑 |
| 9.6 用代数校准 | π/∪/− 都是集合算子 | 把 SQL 结果映射回关系即现原形 |

## 核心精讲

### 9.1 SQL 的根基偏离：表是 bag

03 章说关系里无重复元组；SQL 却说「表可以有两行一模一样」。原因是 SQL 选择了**多重集语义**——每一「行」有重数（multiplicity），可以是 2、3……。这不是模型的性质，而是实现/标准的妥协（性能：去重有代价）。代价是：**几乎所有「看起来正确」的 SQL，都要额外操心重复**。

🔧 一个 relvar 没设主键，于是能存重复：

```sql
-- 🔧 自拟：无主键
CREATE TABLE T (x INT);
INSERT INTO T VALUES (1),(1),(2);
SELECT * FROM T;          -- 三行：1,1,2（bag）
SELECT DISTINCT * FROM T; -- 两行：1,2（折回 set）
```

关系模型里 `T` 的值只能是 `{1,2}`——两个 1 是同一命题断言两次（04.2）。

### 9.2 DISTINCT：不是「美化」是「纠错」

投影在代数里天然去重（02.3）。所以 `SELECT SNO FROM SPJ` 少了 DISTINCT 时，**它根本不是 `π SNO`**：它返回的是「每个供应记录一行」，一个供应过 5 个零件的供应商出现 5 次。

- 想「有哪些供应商编号参与过供应」→ 必须 `SELECT DISTINCT`。
- 想「供应商—供应次数」→ 用 `GROUP BY SNO`（9.3）。

「忘 DISTINCT」的下游灾难：把重复当成「多实例」去计数、求和，结果成倍膨胀。这是本书点名的头号 bag 事故。

### 9.3 GROUP BY 的隐藏去重 + 位置/别名陷阱

`GROUP BY SNO` 本质是按 `SNO` 把 bag 折叠：组数 = `π SNO` 的基数（因为分组按键唯一，等价于对该键投影去重）。因此：

🔧 「每个城市的供应商数」：

```sql
SELECT CITY, COUNT(*) AS n FROM S GROUP BY CITY;
```

常见坑：
1. **SELECT 里出现非分组列**——SQL 允许（MySQL 关 ONLY_FULL_GROUP_BY）返回**任意一行**的值，破坏函数依赖假设。严格口径：SELECT 非聚合列必须出现在 GROUP BY（或函数依赖于它）。见 [../mysql/14-单表查询.md](../mysql/14-单表查询.md)。
2. **按位置 GROUP BY**（`GROUP BY 1`）——把列位置当语义，而列位置在关系里本无意义（01.2/03.1）；改了 SELECT 列序就静默错分组。
3. **HAVING vs WHERE**：WHERE 在分组前筛元组，HAVING 在分组后筛组。把「先筛再组」和「组后筛」混写，结果不同（04 谓词作用对象不同）。

### 9.4 UNION vs UNION ALL：语义与性能的权衡

- `UNION`（= 关系 ∪，02.1）去重，**幂等**：并上自身不变。
- `UNION ALL` 保留重数，**不是**关系并——它是 bag 并。

🔧 何时必须去重、何时可用 ALL：
- 求「伦敦或巴黎的高状态供应商」（05.3）：语义是集合并 → `UNION`，用 ALL 可能重复计数。
- 求「两批订单合并的完整明细」：本就允许重复（每笔订单一行）→ `UNION ALL` 更快（省排序/哈希去重）。

判断口诀：**问自己「两个输入里会不会有应当合并成一条的相同行」**。会→UNION；各算各的→UNION ALL。Date 会说：只有在 bag 语义世界里才需要纠结 ALL；在关系模型里只有「并」，没有「带重复的并」。

### 9.5 LEFT JOIN + COUNT：双坑

🔧 经典事故：「统计每个供应商的供应笔数，含没供应的」。

```sql
-- 🔧 自拟
SELECT S.SNO, COUNT(SP.PNO) AS n
FROM S LEFT JOIN SP ON S.SNO = SP.SNO
GROUP BY S.SNO;
```

- 用 `COUNT(*)` → 没供应的供应商那组 LEFT JOIN 补出一行（右表全 NULL），`COUNT(*)` 把它算成 **1**（错，应为 0）。正解 `COUNT(SP.PNO)`（跳过补出的 NULL，06.5）得 0。
- 若 SP 里对同一 (SNO) 有重复行（bag 偏离），JOIN 按重数**相乘复制**，计数虚高（9.1）。关系模型里 SPJ 有主键、SP 无重复元组，这种「复制式膨胀」根本不会发生。

这正是任务书点名的「LEFT JOIN 误用」：**把外连接当成「可选匹配 + 计数」时，NULL 填充（06.6）与 bag 复制（9.1）会同时污染结果**。

### 9.6 用代数校准：把结果「折回关系」验真

方法：对可疑 SQL，写出它「本应」对应的关系代数式（π/σ/∪/−/⋈），把 SQL 输出 `DISTINCT` 后与代数结果比对。差异 = bag 偏离惹的祸。

🔧 例：「供应了零件 P1 的供应商，减去供应了 P2 的供应商」：

```text
代数： π_SNO(σ_PNO='P1'(SP))  −  π_SNO(σ_PNO='P2'(SP))
SQL ： SELECT DISTINCT SNO FROM SP WHERE PNO='P1'
       EXCEPT
       SELECT DISTINCT SNO FROM SP WHERE PNO='P2';
```

用 `EXCEPT`（对应集合差 −）而非 `NOT IN`（06.4 的 NULL 陷阱）；加 `DISTINCT`（对应 π 的去重）。两条修正合起来，SQL 才真正等价于那个代数式——这就是全书反复示范的「用关系代数校准 SQL」。

## 常见误区

| # | 误区 | 纠正视角 |
| --- | --- | --- |
| 1 | 「SELECT 列 天然不重复」 | bag 默认留重复，投影要 DISTINCT（9.2） |
| 2 | 「UNION ALL 永远更快更无害」 | 需去重语义时它错，会重复计数（9.4） |
| 3 | 「LEFT JOIN 后 COUNT(*)=匹配数」 | 补出的 NULL 行被计入，偏大（9.5） |
| 4 | 「GROUP BY 位置/别名随便用」 | 位置无语义、别名可致重名歧义；显式列名（9.3） |
| 5 | 「非聚合列不进 GROUP BY 也行」 | 返回任意值、破坏函数依赖（9.3） |
| 6 | 「JOIN 不会凭空造行」 | bag 重数相乘复制，未去重则膨胀（9.1/9.5） |

## 与其他章 / 其他书的联系

- ← `02/03`：π 去重、值语义、封闭性。← `05`：UNION 依赖集合语义。← `06`：NULL 与聚合口径。
- → `10`：主键/唯一约束是把 bag 逼回 set 的声明式手段。
- → `13`：本节多条并入全书误区总表。
- → [../mysql/14-单表查询.md](../mysql/14-单表查询.md)、[../mysql/15-连接查询.md](../mysql/15-连接查询.md)：MySQL 对 GROUP BY 宽松/严格口径、JOIN 算法与行复制。
- → [../../courses/数据库系统/15445/projects/06-mini-sql](../../courses/数据库系统/15445/projects/06-mini-sql)：mini-sql 里 DISTINCT/聚合算子如何显式实现去重。

## 文献与文档

- C.J. Date, *SQL and Relational Theory*, 3rd ed. —— bag vs set、DISTINCT/UNION/外连接系列批评（章号 ⚠️ 推定）。
- E. F. Codd, 1970 —— 关系=集合（无重复）的原始定义（互链精读）。
- SQL 标准：`UNION/EXCEPT/INTERSECT` 及其 `ALL` 变体、`GROUP BY`/`HAVING`。
