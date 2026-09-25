# 05 AND-OR-NOT：唯一（且够用）的逻辑操作符

> ⚠️ 原书归属推定：Part II 逻辑章——任务书所称「关系代数唯一操作符 THE AND-OR-NOT」对应作者关于
> 「布尔逻辑只需 AND、OR、NOT 三个原始操作符」的论证。本文件讲**为什么谓词能且只能靠这三样组合**，
> 以及如何用它把复杂 SQL 条件做**保真分解/改写**。所有 SQL/代数式为 🔧 自拟教学示意，非书中原文。

## 核心概念速览（中英对照）

- **唯一操作符（集）** — the one and only (set of) operator：AND、OR、NOT 三者足以表达任意布尔函数。
- **功能完备** — functionally complete：一组联结词能表达所有真值函数。
- **合取** — conjunction（AND）：两谓词同时为真。
- **析取** — disjunction（OR）：至少一个谓词为真。
- **否定** — negation（NOT）：真值翻转。
- **德摩根律** — De Morgan's laws：`NOT(A AND B) ≡ (NOT A) OR (NOT B)`，及其对偶。
- **逻辑等价** — logical equivalence：两谓词对所有代入真值恒同，可安全互相替换。
- **分配律** — distributivity：`A AND (B OR C) ≡ (A AND B) OR (A AND C)`。
- **双重否定** — double negation：`NOT NOT A ≡ A`（仅在二值逻辑成立，3VL 下要当心，见 06）。
- **谓词分解** — predicate decomposition：把一个 WHERE 拆成 AND/OR/NOT 结构以便逐一核对。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 为何三样就够 | 功能完备性、范式(DNF/CNF) | 任何条件都是 AND/OR/NOT 的组合 |
| 5.2 德摩根：最常见的 bug 源 | 否定穿过 AND/OR 要翻转 | SQL `NOT(...)` 写错即漏数据 |
| 5.3 分配律与可推理性 | 把条件拆成子句并集 | 便于证明等价、便于优化 |
| 5.4 分解实战 | 复杂 WHERE 逐步保真改写 | 用代数等价式验证 |
| 5.5 3VL 的破坏预告 | 双重否定/德摩根在 UNKNOWN 下失效 | 逻辑再强也救不了 NULL（06） |

## 核心精讲

### 5.1 三样就够：功能完备

任意布尔函数都能写成「析取范式」（若干 AND 子句用 OR 连起来）或「合取范式」。既然 AND、OR、NOT 能表达全部真值函数，那么**任何 SQL 谓词条件，本质上都是 AND/OR/NOT 的树**。Date 强调这一点，是为了让「改写条件」变成**可证明**的操作，而非凭直觉。

🔧 例：谓词 `x 是伦敦或巴黎的高状态供应商`：

```text
(CITY='London' OR CITY='Paris') AND STATUS > 20
```

它是一棵 AND/OR/NOT 树；你可以用分配律把它展开为 DNF，再逐个子句核对。

### 5.2 德摩根律——SQL 否定写错的第一大源

**定律**：

```text
NOT (A AND B) ≡ (NOT A) OR (NOT B)
NOT (A OR  B) ≡ (NOT A) AND (NOT B)
```

否定穿过 AND 变 OR，穿过 OR 变 AND。手写 SQL 的人最常犯的错就是「否定只分配给第一项，忘了翻转连接词」。

🔧 场景：查「不是（伦敦且高状态）」的供应商。

```sql
-- ❌ 常见错写（德摩根没做对）
SELECT * FROM S WHERE NOT (CITY='London' AND STATUS>20);
-- 若把它「随手」拆成下面这样，就错了：
SELECT * FROM S WHERE NOT CITY='London' AND NOT STATUS>20;   -- 漏行！

-- ✅ 正确的等价展开（AND→OR，各自否定）
SELECT * FROM S WHERE NOT CITY='London' OR NOT STATUS>20;
```

用代数式验证正确性（本书方法论）：

```text
σ ¬(C=L ∧ S>20) (S)  ==  σ (¬C=L ∨ ¬S>20) (S)
```

**这就是「关系代数等价式」作为单元测试的用法**：把两种写法各跑一遍比较，或直接对真值表——德摩根保证二者恒等。

> ⚠️ 提醒：上面对 `NOT (CITY='London')` 的处理在二值逻辑成立。一旦列可能为 NULL，
> `NOT (STATUS>20)` 与 `STATUS<=20` **不再等价**（后者丢 UNKNOWN 行）——见 5.5 与 06 章。

### 5.3 分配律：把 OR 拆成可分别求解的子查询

```text
A AND (B OR C) ≡ (A AND B) OR (A AND C)
```

🔧 用途：把一个难查询拆成两个易查询并起来。求「伦敦或巴黎、且状态>20」的供应商：

```sql
-- 单一谓词
SELECT * FROM S WHERE (CITY='London' OR CITY='Paris') AND STATUS>20;

-- 分配后 = 两个限制再并（UNION 天然去重，等价于关系并 ∪）
SELECT * FROM S WHERE CITY='London' AND STATUS>20
UNION
SELECT * FROM S WHERE CITY='Paris'  AND STATUS>20;
```

代数：`σ_{L∨P ∧ g}(S) = σ_{L∧g}(S) ∪ σ_{P∧g}(S)`。注意必须 `UNION`（去重）而非 `UNION ALL`——因为这里依赖 AND/OR 的**集合**语义；用 `UNION ALL` 会把同时满足两支的元组复制（本例城市互斥所以碰巧没事，但换条件就会暴露，见 09）。

### 5.4 分解实战：复杂条件的保真改写流程

Date 教的不是背定律，而是**流程**：
1. 把 WHERE 写成 AND/OR/NOT 树（谓词分解）。
2. 每一步用一条布尔定律做变换，并写下对应的代数等价式。
3. 对边界值（含 NULL？含空集？含极端比较）核对。

🔧 例：`NOT (A AND (B OR NOT C))`
```text
→ NOT A OR NOT (B OR NOT C)          [德摩根]
→ NOT A OR (NOT B AND NOT NOT C)      [德摩根 + 内部]
→ NOT A OR (NOT B AND C)              [双重否定，二值假设]
```
SQL 里若 A/B/C 任一可能含 NULL，第三步「双重否定」失效，改写会**改变结果**（06 章给出反例）。

### 5.5 AND-OR-NOT 与 3VL 的正面冲突

本章所有等价式的前提是**二值逻辑**：每个命题非真即假，`NOT NOT A ≡ A`。SQL 却用 NULL 引入 UNKNOWN，于是：

| 二值定律 | 在 3VL 下 |
| --- | --- |
| `NOT NOT A ≡ A` | UNKNOWN 的双重否定仍是 UNKNOWN，**看似**成立，但与 `A IS TRUE` 判据背离 |
| 德摩根 | 结构上仍成立，但 UNKNOWN 传播方式让「丢弃」与「保留」的边界偏移 |
| 排中律 `A OR NOT A ≡ TRUE` | 当 A=UNKNOWN 时结果为 UNKNOWN，**不为真**——`WHERE A OR NOT A` 会滤掉该行！ |

这就是全书逻辑部分与 NULL 部分的接缝：**AND-OR-NOT 很美，但它只在没有缺失值时安全**。Date 的处方不是「完善 3VL」，而是「消灭缺失值」（07 章 Placeholder / relvar 分解）。

## 常见误区

| # | 误区 | 纠正视角 |
| --- | --- | --- |
| 1 | `NOT(A AND B)` = `NOT A AND NOT B` | 德摩根要求变 OR；错写漏行 |
| 2 | 拆条件用 `UNION ALL` | AND/OR 语义基于集合，须 `UNION`（去重），见 09 |
| 3 | `NOT (STATUS>20)` = `STATUS<=20` | 3VL 下后者丢 UNKNOWN 行，二者不等价（06） |
| 4 | `X OR NOT X` 恒真可省 | UNKNOWN 时为 UNKNOWN，会误删元组 |
| 5 | 靠直觉改 WHERE | 用代数等价式 + 真值表逐步核对 |

## 与其他章 / 其他书的联系

- ← `04`：谓词的组合即本章的 AND/OR/NOT。
- → `06`：3VL 如何破坏双重否定/排中律。
- → `09`：UNION 去重 vs UNION ALL 的关系论根源。
- → [../../paper/doi_10.1145_362384.362685/00-精读笔记.md](../../paper/doi_10.1145_362384.362685/00-精读笔记.md)：Codd 用谓词表达关系与完整性，本章是其逻辑展开。

## 文献与文档

- 布尔代数 / 命题逻辑（德摩根、分配律、功能完备）—— 经典数理逻辑，非本书独创。
- C.J. Date, *SQL and Relational Theory*, 3rd ed. —— 「the one and only operator: AND-OR-NOT」论证主线（章号 ⚠️ 推定）。
- E. F. Codd, 1970 —— 关系的谓词表达（互链精读）。
