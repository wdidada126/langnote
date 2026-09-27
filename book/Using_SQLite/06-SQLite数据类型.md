# 06 · SQLite 数据类型（SQLite Datatypes）⚠️ 章号推定

> 主题锚定：动态类型、五种存储类、声明类型→亲和性（affinity）的映射与六条比较转换规则、
> rowid。官方依据：[datatype3.html](https://sqlite.org/datatype3.html) ✅（curl 200 实测）与
> [lang_createtable.html](https://sqlite.org/lang_createtable.html) ✅；关键分支以 🔧 `typeof` 实测复现。

## 1. 颠覆点：类型属于值，不属于列（的强制约束）

其他 RDBMS："列有类型，值必须服从"。SQLite："**值有存储类，列只有建议**"。
声明的 `INTEGER/VARCHAR/DECIMAL/BLOB...` 只是语法糖，先映射为五种**存储类**之一：

- `NULL`、`INTEGER`、`REAL`、`TEXT`、`BLOB`

再由**列亲和性**（affinity）决定入库前要不要做无损转换：

| 亲和性 | 声明类型名包含（规则大意，官方 datatype3 页） | 行为 |
| --- | --- | --- |
| INTEGER | `INT` | 文本像整数则转整数 |
| TEXT | `CHAR/TEXT/CLOB` | 数值转文本 |
| BLOB | 无声明或 `BLOB` | **原样存入**（"亲和性=无"） |
| REAL | `REAL/FLOA/DOUB` | 尽量转浮点 |
| NUMERIC | `DECIMAL/NUM/MONEY` 等其余 | 整数/浮点间择无损者 |

> 经典陷阱一句版：`'1e3'` 进 INTEGER 列变 1000，进 TEXT 列还是 `'1e3'`；
> `'42abc'` 谁都转不动，原样 TEXT——**转换是尽力而为，不报错**。

## 2. 🔧 实测：typeof 全矩阵（本会话核心实验）

方法：`CREATE TABLE a(i INTEGER, r REAL, x TEXT, n NUMERIC, b BLOB, v VARCHAR(10))`；
把 12 个字面量（`'42'`、`42`、`'42.5'`、`42.5`、`'abc'`、`'1e3'`、`x'4142'`、`' 42 '`、
`'42abc'`、`NULL`、`0`、`'0'`）对**六列全部同值插入**（24 行），再原样读回观察存储结果。

代表性结果（🔧 原文行摘录）：

| 插入值 | i(INTEGER) | r(REAL) | x(TEXT) | n(NUMERIC) | b(BLOB) | v(VARCHAR) |
| --- | --- | --- | --- | --- | --- | --- |
| `'42'` | 42 | 42.0 | '42' | 42 | '42' | '42' |
| `42` | 42 | 42.0 | '42' | 42 | 42 | '42' |
| `'42.5'` | **42.5** | 42.5 | '42.5' | 42.5 | '42.5' | '42.5' |
| `'1e3'` | **1000** | 1000.0 | '1e3' | 1000 | '1e3' | '1e3' |
| `' 42 '` | **42** | 42.0 | ' 42 ' | 42 | ' 42 ' | ' 42 ' |
| `'42abc'` | '42abc' | '42abc' | '42abc' | '42abc' | '42abc' | '42abc' |
| `x'4142'` | b'AB' | b'AB' | b'AB' | b'AB' | b'AB' | b'AB' |
| `0` | 0 | 0.0 | '0' | 0 | 0 | '0' |

观察结论（条条可复测）：

1. **同一输入在同一张表里同时是整数、浮点、文本、字节串**——列名骗不了 `typeof`；
2. `'42.5'` 进 INTEGER 亲和列**保留 REAL 42.5**（无损转不成整，就退 REAL）——
   "INTEGER 列存浮点"合法，书中惊愕点实锤；
3. `' 42 '` 进 i/n 列**去空白成 42**，进 x 列原样——文本→数的转换包含修剪；
4. BLOB 亲和列是**唯一"传真件"**：要"存进去什么出来什么"，声明成 BLOB 或不写类型；
5. `'42abc'` 全体原样：转换失败**静默降级为 TEXT**，不报错（宽松时代的 bug 温床）；
6. `x'4142'` 在所有列保持 b'AB'：BLOB 值无亲和性可对抗它。

另测：`SELECT x, typeof(x) FROM a WHERE x=42` → `('42','text')`——比较时文本 '42'
在 `=42` 谓词下**查询期再转换**（亲和性规则同样作用于表达式，非仅存储）。

## 3. rowid：每表隐藏的"第六存储类"级设施

- 非 `WITHOUT ROWID` 表都有 64 位 `rowid`；`INTEGER PRIMARY KEY` 是它的**别名**
  （🔧 实测：`SELECT id, typeof(id)` → `(1,'integer')`；未显式插入时自动取 max+1）。
- `INTEGER PRIMARY KEY` 必须**逐字**写：`INT PRIMARY KEY`、`INTEGER PRIMARY KEY NOT NULL`
  等变体不会成为 rowid 别名（⚠️ 细节引官方 datatype3/ lang_createtable ✅ 页规则，未逐条实测）。
- 寻址意义：主键查找=rowid 直达 B 树叶页（09 章"Rowid Lookup 最快"的存储层原因；
  对照 [../Understanding_MySQL_Internals/10-存储引擎掠影.md](../Understanding_MySQL_Internals/10-存储引擎掠影.md)
  的聚簇索引视角：InnoDB 把主键做成组织原则，SQLite 把 rowid 做成组织原则，你只能有一个）。

## 4. 比较与排序：类间秩序是硬编码的

官方顺序（NULL 最低，BLOB/TEXT/REAL-INTEGER 分组，数字按值比、文本按 collation 比）：
`NULL < INTEGER/REAL < TEXT < BLOB`。跨类比较前按规则转换（如文本与整数比较时
文本亲和侧数值转数字；规则全表见 datatype3 页，⚠️ 未逐条实测的分支从略）。
🔧 本会话旁证：`WHERE x=42`（x 为 TEXT 亲和且存 '42'）命中——文本侧被转成数值再比。

## 5. 与 MySQL/PG 对照（30 秒表）

| 维度 | SQLite（legacy） | MySQL InnoDB | PostgreSQL |
| --- | --- | --- | --- |
| 类型强制 | 列=建议（亲和性） | 列=法律（宽松模式有隐转） | 列=法律+丰富原生类型 |
| 错误暴露时机 | 静默降级，比较/应用层才炸 | INSERT 即报错（strict mode） | INSERT 即报错 |
| 补救开关（2026） | **STRICT 表**（3.37，见 07 章🔧） | sql_mode=STRICT | 原生即严 |
| 日期/数组/JSON | 文本/数字 + JSON 函数（3.38 内置 ✅） | 原生类型 | 原生类型 |

系列视角：书里"把 VARCHAR(255) 当摆设"的震惊，在 InnoDB 语境是"字符集+长度语义"问题
（[../Understanding_MySQL_Internals/02-MySQL源代码基础.md](../Understanding_MySQL_Internals/02-MySQL源代码基础.md)
里的 charset 讨论）——**两边都没有你直觉里那么"SQL 标准"**。

## 6. 2026 实践准则（由 🔧 矩阵反推）

1. 要可靠性就写 STRICT（或团队规范"每列显式类型 + 入口层校验"）；
2. 需要原样保真的（签名/哈希/二进制）用 BLOB 列 + 应用层编解码（如 base64 文本也远好于
   让 TEXT 亲和列自作主张）；
3. 数值货币用整数最小单位（REAL 的 42.5 教训：二进制浮点入 TEXT 查询会走形）；
4. 迁移审计第一步：`SELECT COUNT(*) ... WHERE typeof(col) != 'expected'` 全表体检。

## 核心概念速览（中英对照）

- **存储类** — storage class：NULL/INTEGER/REAL/TEXT/BLOB 五种值的本体类型
- **亲和性** — affinity：声明类型名映射出的列级"转换偏好"（五档）
- **类型转换规则** — type conversion rules：入库与比较期的尽力而为无损转换
- **动态类型** — dynamic typing：类型属于值而非变量，运行期可混装
- **typeof()** — 运行时类型探针：返回某值当前存储类名
- **rowid** — 行标识：非 WITHOUT ROWID 表隐藏的 64 位整数主键
- **INTEGER PRIMARY KEY** — rowid 别名：逐字声明才生效的整数主键快捷键
- **WITHOUT ROWID** — 索引组织表：以 PK 组织 B 树的表变体（适合窄主键/大量覆盖查询）
- **静默降级** — silent coercion：'42abc' 转不动就存 TEXT，不报错的宽松行为
- **COLLATE** — 排序规则：文本比较/排序的字符序（BINARY/NOCASE/RTRIM + 扩展）
- **BLOB 字面量** — x'HHHH'：十六进制写法，任何亲和性都不得转换它
- **STRICT 表** — strict tables：3.37 起按表强制存储类一致（07 章实测）

## 最新演进与工业实践

- **STRICT 表（3.37.0，2021-11-27 ✅ [stricttables.html](https://sqlite.org/stricttables.html)）**：
  终结"列名欺诈"，但类型词表收窄（仅 INT/INTEGER/REAL/TEXT/BLOB/ANY，🔧 实测 `NUMERIC` 直接
  报 `unknown datatype`——迁移老 schema 要先清洗声明类型）；
- **JSON 的"类型中立"**：3.38 起 JSON 函数内置（✅ json1.html），惯用法是 TEXT 列 +
  `json_valid()` CHECK 约束——文本容器 + 校验器替代原生 JSON 类型（07/10 章实验互证）；
- **生成列（3.31 ✅ changes.html）给"表达式当列"补位**：`n INTEGER GENERATED ALWAYS AS (…) VIRTUAL`
  的类型也走同一亲和性系统（07 章🔧）；
- **行业现状**：SQLite 宽松类型被批十年后，官方给出的答案是"可选 STRICT"而非默认改法——
  兼容性优先的嵌入式社会学样本；对照 [../SQL系列·总索引.md](../SQL系列·总索引.md) 里
  类型系统理论（Date 谱系）的"单一类型模型"讨论，SQLite 是反面教材也是实用主义教材。
- **取证清单（本章）**：datatype3.html ✅、lang_createtable.html ✅、stricttables.html ✅
  （curl 200，2026-09-27；亲和性映射表与比较规则为官方页口径）；🔧 全矩阵与 rowid/比较实测记录见
  `D:\develops\tmp\dbwave_usqlite\exp_a_out.txt`（EXP6 段）。
