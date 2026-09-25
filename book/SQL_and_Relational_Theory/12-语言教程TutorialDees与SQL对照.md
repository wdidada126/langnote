# 12 语言教程 Tutorial Dees 与 SQL 对照

> ⚠️ 原书归属推定：附录「语言教程 / Tutorial Dees」。Date 在附录给出一个**教学用的关系语言**
> （他体系里常称 **Tutorial D** 或其变体，本目录依任务书口径称「Tutorial Dees」），用来演示「一个忠于模型的语言长什么样」。
> 本节语法为**示意复述，非逐字原文**；凡具体算子名/关键字以作者一贯的 Rel/Tutorial D 风格 🔧 自拟。

## 核心概念速览（中英对照）

- **Tutorial Dees / Tutorial D** — 作者的教学用关系数据库语言（关系代数 + 更新 + 约束 的可执行写法）。
- **忠于模型的语言** — model-faithful language：语法直接映射关系代数算子，无 bag/无 NULL/无 ORDER BY 副作用。
- **RELS 关系变量声明** — relvar declaration：`RELVAR S ... TUPLE { ... }` 式定义。
- **关系更新算子** — INSERT/DELETE/UPDATE relvar：对 relvar（变量）而非「表」赋值。
- **约束声明断言** — ASSERTION：把任意一阶谓词登记为数据库级约束（10.4 的缺口在此补上）。
- **THE_ 提取算子** — 从 RVA/复合值取成分（11.4，⚠️ 命名依作者风格）。
- **PACK/UNPACK 一等公民** — 语言内置折叠/展开（11.3）。
- **无 UNKNOWN** — 语言坚持 2VL，不提供 NULL（05/06/07 的落地）。
- **SQL ↔ Tutorial D 对照表** — 本文件核心产物。
- **正交性/统一性** — 一切皆表达式，皆可嵌套（02.5 封闭性的语言级保证）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 12.1 为什么作者要自造一门语言 | SQL 的三宗偏离：bag/NULL/序 | 需要个「反面参照」实现 |
| 12.2 relvar 声明 | 类型 + 键 + 约束一起写 | 声明式完整性的原生形态 |
| 12.3 查询：直接写代数 | 表达式即关系，可任意嵌套 | 没有 SELECT 的 bag 陷阱 |
| 12.4 更新：对变量赋值 | INSERT/DELETE 作用 relvar | 承 01.1 值 vs 变量 |
| 12.5 断言与 RVA | ASSERTION/THE_/PACK | 补 SQL 表达力缺口 |
| 12.6 SQL↔D 对照总表 | 逐条映射 | 本文件的主产物 |

## 核心精讲

### 12.1 为什么要自造一门语言

本书绝大部分论证都是「SQL 这样做是错的，模型应那样」。为了让「那样」不只是口号，作者在附录给一门**直接实现关系代数**的教学语言（Tutorial Dees/Tutorial D）。它的每一处设计，都对应本目录前面某章对 SQL 的批评：

- 无 `SELECT` 默认 bag → 投影天然去重（02.3/09）。
- 无 `NULL`/3VL → 谓词全用 AND-OR-NOT 二值（05/06/07）。
- 无 `ORDER BY` 语义 → 关系值不携带序（03）。
- 有 `ASSERTION` → 数据库级声明式约束（10.4）。
- 有 RVA/PACK/UNPACK → 合法嵌套且保封闭性（11）。

### 12.2 relvar 声明（示意）

🔧 依作者一贯风格复述，**非逐字原文**：

```text
-- Tutorial Dees 风格（示意）
TYPE CITY TYPE {CHAR(15)};
VAR S RELATION {
    SNO  SNO_TYPE,
    SNAME TUPLE { SNAME CHAR(20) },   -- 也可 RVA：关系作为属性
    STATUS INTEGER,
    CITY  CITY
  }
  KEY {SNO};                             -- 候选键即唯一性谓词(04.4/08.1)
```

对照 SQL（01、10）：键、域、RVA 全在**一个声明**里、且都是可强制的约束——声明式力量（10.3）在这里是语言原生，不是「额外语法糖」。

### 12.3 查询：直接写关系代数

🔧 「伦敦供应商的编号与状态」：

```text
-- Tutorial Dees（示意）
(S WHERE CITY = 'London') { SNO, STATUS }     -- WHERE=限制σ, {…}=投影π
```

对照代数 `π_{SNO,STATUS}(σ_{CITY='London'}(S))`（02）。要点：

- `{ SNO, STATUS }` 是投影，**天然去重**（09.2）——不会冒出 bag 重复行。
- 整个表达式是**一个关系值**，可放进 `USING`/外层继续 `JOIN`、`UNION`（02.5 封闭性）。
- 没有 `ORDER BY` 的位置：想要有序展示，是「取完关系后、给终端排序」的事（03.3）。

### 12.4 更新：对 relvar 赋值

🔧 「把 S1 的状态改为 30」：

```text
-- 关系赋值/更新（示意）
S := S { ... }        -- 或 UPDATE S WHERE SNO='S1' { STATUS := 30 }
```

明确区分**变量 S** 与**它当前值**（01.1）：`UPDATE`/`INSERT`/`DELETE` 改变 relvar 的值，改变前后都要满足键/参照/断言（10）。对照 SQL `UPDATE S SET ...`——语义相同，但 D 的写法把「这是对变量的值替换」说得毫无歧义，也就不会产生「改主键触发级联」的语义混乱（08.5）。

### 12.5 断言、RVA、PACK/UNPACK

- **ASSERTION**：把任意一阶谓词登记为约束（补 10.4 里 SQL CHECK 的跨表缺口）：

```text
ASSERTION status_sum_le_100 :
  FORALL ( S ) ( ... 关于 S 聚合的谓词 ... ) = TRUE
```

- **RVA + THE_**：把关系当属性值，并用提取算子取成分（11.1/11.4）。
- **PACK/UNPACK**：语言内置，保证嵌套仍可组合、互逆不丢信息（11.3）。

这三样正是「忠于模型的语言」比 SQL 多出来的东西——每一样对应 SQL 的一个已知短板。⚠️ 具体关键字名依作者版本而定，此处为示意。

### 12.6 SQL ↔ Tutorial Dees ↔ 关系代数 对照总表

| 需求 | 关系代数 | SQL | Tutorial Dees（示意） | 关键差异 |
| --- | --- | --- | --- | --- |
| 限制 | `σ_p(R)` | `WHERE p` | `R WHERE p` | SQL 有 3VL，D 坚持 2VL（06） |
| 投影 | `π_X(R)` | `SELECT X` / `SELECT DISTINCT X` | `R { X }` | SQL 需 DISTINCT 才等价，D 天然去重（09） |
| 自然连接 | `R ⋈ S` | `JOIN ON` / `NATURAL JOIN` | `R * S` | SQL 双留键列（02.4），D 合名 |
| 并 | `R ∪ S` | `UNION` / `UNION ALL` | `R union S` | `UNION ALL` 是 bag 并（09.4） |
| 差 | `R − S` | `EXCEPT` / `NOT IN`(危险) | `R minus S` | `NOT IN` 遇 NULL 坍缩（06.4） |
| 改名 | `ρ` | `AS` | `RENAME` | 基本等价 |
| 键 | （模型公理） | `PRIMARY KEY` | `KEY {…}` | 都声明，但产品强制度不一（08/10.3） |
| 数据库级约束 | 一阶谓词 | CHECK(受限)/触发器 | `ASSERTION` | SQL 缺原生跨 relvar 断言（10.4） |
| 排序 | （无此算子） | `ORDER BY`(仅展示) | （展示层） | 关系值无序（03） |
| 缺失值 | （不允许） | `NULL`+3VL | 用 Placeholder/分解 | D 回避 NULL（07） |

## 常见误区

| # | 误区 | 纠正视角 |
| --- | --- | --- |
| 1 | 「Tutorial D 只是玩具语法」 | 它是 SQL 三宗偏离的**反面参照实现**（12.1） |
| 2 | 「SQL 加个 DISTINCT 就等价代数了」 | 还有 3VL/序/bag 聚合需一并处理（12.6） |
| 3 | 「断言=CHECK」 | 断言可跨 relvar、含聚合；CHECK 多限于行内（12.5/10.4） |
| 4 | 「RVA/嵌套是 D 的炫技」 | 它证明嵌套不破坏封闭性（11/12.5） |
| 5 | 「把 D 的算子名当书中原文」 | 本表为示意复述，⚠️ 以作者版本为准 |

## 与其他章 / 其他书的联系

- ← 几乎全部章节：12.6 把 01–11 的偏离逐条对上 D 的写法。
- → `13`：本文件的对照表可直接并入全书误区清单。
- → [../../courses/数据库系统/15445/projects/06-mini-sql](../../courses/数据库系统/15445/projects/06-mini-sql)：mini-sql 用表达式树实现「一切皆关系值、可嵌套」，是封闭性的工程缩影（02.5）。
- → [../../paper/doi_10.1145_362384.362685/00-精读笔记.md](../../paper/doi_10.1145_362384.362685/00-精读笔记.md)：D 是「Codd 关系代数可直接成为查询语言」这一 1970 设想的现代教学实现。

## 文献与文档

- C.J. Date, *SQL and Relational Theory*, 3rd ed. —— 附录语言教程（章号/算子名 ⚠️ 推定，非逐字原文）。
- Date & Darwen, *The Third Manifesto* / *Database Explorations* —— Tutorial D 的规范来源（不引具体编号）。
- E. F. Codd, 1970 —— 关系代数作为可执行查询基础的原典（互链精读）。
