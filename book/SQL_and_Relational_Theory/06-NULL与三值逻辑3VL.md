# 06 NULL 与三值逻辑 3VL

> ⚠️ 原书归属推定：Part II NULL 专题。NULL 是 SQL 对关系模型最严重的偏离之一。
> 本文件讲清 **3VL 的真值表、UNKNOWN 在 WHERE/JOIN/聚合里的归宿**，以及为什么它是「陷阱制造机」。
> 所有 SQL/代数式为 🔧 自拟教学示意，非书中原文。

## 核心概念速览（中英对照）

- **缺失值** — missing value：某元组在本应有值的属性上「没有已知值」，SQL 用 NULL 表示。
- **NULL** — null：不是值，而是一个「值缺失」的标记；比较它得 UNKNOWN。
- **三值逻辑** — 3VL (three-valued logic)：真值取 {TRUE, FALSE, UNKNOWN}。
- **UNKNOWN** — unknown：含 NULL 的比较/运算的结果，既非真也非假。
- **IS NULL** — is-null 谓词：3VL 体系外唯一能可靠探测 NULL 的构造（返回二值）。
- **归约（保留条件）** — filtering on TRUE：WHERE 只保留结果为 TRUE 的行，UNKNOWN/FALSE 都丢。
- **UNKNOWN 传播** — unknown propagation：任一子表达式 UNKNOWN，AND/OR 可能整体 UNKNOWN。
- **聚合忽略 NULL** — NULL-ignoring aggregates：COUNT(*) 计所有，其余聚合跳过 NULL——口径不一致之源。
- **NOT IN 陷阱** — NOT IN with NULL：子查询含 NULL 使 `NOT IN` 恒 UNKNOWN，结果为空。
- **二值 vs 三值** — 2VL vs 3VL：关系模型坚持 2VL；SQL 混入 3VL 导致等价式失效。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 NULL 的三个谎言 | 它不是 0、不是空串、不是值 | 它是「无已知值」的标记 |
| 6.2 3VL 真值表 | AND/OR/NOT 加 UNKNOWN | 排中律、双重否定被削弱 |
| 6.3 WHERE 只认真 | UNKNOWN 也丢 | 「过滤」语义与直觉不符 |
| 6.4 NOT IN / <> 的坍缩 | 子查询含 NULL→空结果 | 高频生产事故 |
| 6.5 聚合的 NULL 口径 | COUNT(*) vs COUNT(col) vs SUM | 分母不一致致百分比错 |
| 6.6 外连接补 NULL | JOIN 产生人造 NULL（07/09 续） | 混淆「真缺失」与「没匹配上」 |

## 核心精讲

### 6.1 NULL 不是值，是标记

SQL 把 NULL 塞进「值」的世界，于是所有比较运算必须回答「和未知比，结果是什么」。答案不能是真/假，只能是 **UNKNOWN**。Date 的立场：**在一个真正的关系模型里没有 NULL 容身之地**——每个属性在每个元组上都该有确定值；「不知道」应通过建模解决（07 章），而不是给个标记让逻辑三值化。

### 6.2 3VL 真值表（记住 UNKNOWN 是关键）

🔧 用 U 表示 UNKNOWN：

```text
AND ： T∧T=T  T∧F=F  T∧U=U  F∧*=F  U∧U=U
OR  ： T∨*=T  F∨F=F  F∨U=U  U∨U=U
NOT ： ¬T=F  ¬F=T  ¬U=U
```

要点：
- `F ∧ U = F`（假压过未知）、`T ∨ U = T`（真压过未知）——直觉对。
- 但 `T ∧ U = U`、`F ∨ U = U`——未知「污染」了本可判定的式子。
- **排中律崩了**：`U ∨ ¬U = U ∨ U = U`，不再是 TRUE。
- 双重否定：`¬¬U = U`，看似保留，但 `WHERE X OR NOT X` 对 `X=NULL` 的行返回 UNKNOWN → **该行被过滤掉**。这违反「恒真式应保留所有行」的直觉。

### 6.3 WHERE 只保留 TRUE

SQL 规定：`WHERE` 保留使条件为 TRUE 的行，**FALSE 和 UNKNOWN 都丢**。这就是 05.5 里德摩根/双重否定在 SQL 里翻车的落地机制。

🔧 经典：

```sql
-- 表 S 有一行 STATUS = NULL
SELECT * FROM S WHERE STATUS > 20;    -- 该行不出现（UNKNOWN）
SELECT * FROM S WHERE STATUS <= 20;   -- 该行也不出现（UNKNOWN）
-- 两次的并 ≠ 全表！少了那行 NULL。要它，得：
SELECT * FROM S WHERE STATUS > 20 OR STATUS <= 20 OR STATUS IS NULL;
```

「>20」和「<=20」在二值下互补，在 3VL 下**中间漏了一条缝**（NULL）。生产上「两个互补查询计数相加 ≠ 总数」就是这条缝。

### 6.4 NOT IN 与 <> 的坍缩（最危险）

🔧 需求：「找没被任何订单引用的客户」。

```sql
-- ❌ 危险：若 Order.CustID 里有一个 NULL
SELECT * FROM Customer WHERE CustID NOT IN (SELECT CustID FROM Order);
```

`NOT IN (…含 NULL…)` 展开为 `CustID<>v1 AND CustID<>v2 AND … AND CustID<>NULL`。最后一项是 UNKNOWN，整个 AND 变 UNKNOWN → **该行被丢** → 结果常常是空集。这不是「查不到匹配」，是「什么都查不到」。

代数视角（02 章）：这本质是**差集** `Customer − π CustID(Order)`，除法/差在集合语义里根本没有 UNKNOWN 问题。Date 的告诫：能用 `NOT EXISTS`（相关子查询，按行判断存在性）替代 `NOT IN`，避开 NULL 坍缩：

```sql
-- ✅ 用 NOT EXISTS 规避 NULL
SELECT * FROM Customer c WHERE NOT EXISTS (SELECT 1 FROM Order o WHERE o.CustID = c.CustID);
```

`o.CustID = c.CustID` 遇 NULL 得 UNKNOWN，`WHERE` 丢该比较行——这里反而正确（NULL 的订单本来就不引用任何具体客户）。**同一个 UNKNOWN 行为，在两种写法里一个致命一个无害**，这就是必须懂 3VL 的原因。

### 6.5 聚合的 NULL 口径不一致

🔧 表 `S(SNO, STATUS)`，其中 2 行 STATUS 为 NULL，共 10 行：

| 表达式 | 计什么 | 结果 |
| --- | --- | --- |
| `COUNT(*)` | 所有元组 | 10 |
| `COUNT(STATUS)` | 非 NULL 的 STATUS | 8 |
| `SUM(STATUS)` / `AVG(STATUS)` | 跳过 NULL 求和/求均 | 基于 8 |
| `AVG` 手工写成 `SUM(*)/COUNT(*)` | 分母用 10 | **偏低** |

经典 bug：算「平均状态」用 `SUM(STATUS)/COUNT(*)` → 分母混入 NULL 行，均值被稀释。**要么统一 `COUNT(col)`，要么先把 NULL 建模成真实值（07）**。Date：3VL 让聚合语义「看起来自然其实处处要对齐分母」。

### 6.6 外连接「补 NULL」：人造的未知

`LEFT JOIN` 右表没匹配时，用 NULL **填充**右表列（07/09 章展开）。问题：填进去的 NULL 与「右表本来就有个真缺失的 NULL」**无法区分**。于是：

```sql
-- 🔧 自拟
SELECT * FROM S LEFT JOIN SP ON S.SNO = SP.SNO WHERE SP.QTY IS NULL;
```

这行返回的是「既包括没供货的供应商，也包括供货但 QTY 恰好为 NULL 的供应商」——两类语义混在一起。这是「LEFT JOIN 误用 + NULL」的组合拳，详见 07、09。

## 常见误区

| # | 误区 | 纠正视角 |
| --- | --- | --- |
| 1 | `WHERE col <> 'x'` 会带上 NULL 行 | UNKNOWN→被丢；NULL 行两头都不在（6.3） |
| 2 | `NOT IN 子查询` 安全 | 子查询含 NULL → 结果空（6.4） |
| 3 | `COUNT(*)=COUNT(col)` | 有 NULL 时不等，均值/比例随之错（6.5） |
| 4 | `WHERE X OR NOT X` 全保留 | X 为 NULL 时 UNKNOWN，被丢（6.2） |
| 5 | LEFT JOIN 的 NULL=真缺值 | 是人造填充，与真 NULL 混淆（6.6/07） |

## 与其他章 / 其他书的联系

- ← `05`：3VL 破坏双重否定/排中律，正是 AND-OR-NOT 的失效边界。
- → `07`：用 Placeholder/分解消除缺失值，回归 2VL。
- → `08`：NULL 外键与参照完整性的特例规则。
- → `09`：LEFT JOIN + NULL 的聚合/分组连锁坑。
- → [../mysql/mysql是怎样运行的.md](../mysql/mysql是怎样运行的.md)、[../mysql/15-连接查询.md](../mysql/15-连接查询.md)：MySQL 对 NULL 的实际求值/排序/索引口径。

## 文献与文档

- C.J. Date, *SQL and Relational Theory*, 3rd ed. —— 对 NULL/3VL 的持续批评（章号 ⚠️ 推定）。
- E. F. Codd, *Does SQL Have Any Future?* 及 Codd 1970 —— Codd 本人也主张「应给缺失值一个 better 机制」（互链精读 1970）。
- ISO/IEC SQL 标准：NULL 与 `<empty>` 的区分、`IS NULL` 谓词。
