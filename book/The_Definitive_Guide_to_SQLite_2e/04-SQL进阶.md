# 04 · Advanced SQL for SQLite（SQL 进阶）

> 原书第 4 章（Crossref 章题 ✅：`..._4` "Advanced SQL for SQLite"）。小节划分 ⚠️ 推定。
> 🔧 环境同册；E4 输出在 `exp_out.txt`。

## 1. 本章在 2010 年的语境

"进阶"在 2010 年的含义与今天不同：那时没有 UPSERT/RETURNING/CTE/窗口函数，所以本章的
技术含量集中在**用有限的原语组合出完整应用语义**：

1. **触发器工程学**：BEFORE/AFTER × INSERT/UPDATE/DELETE × FOR EACH ROW，`NEW/OLD` 记录、
   `RAISE(ABORT|FAIL|IGNORE, msg)` 三档中止语义——2010 的"存储过程穷人版"，书里用它实现
   审计、派生列、复杂约束。递归触发默认关闭（`recursive_triggers` PRAGMA 控制；pragma.html
   ✅ 抓到 "Support for recursive triggers was added in version 3.6."——特性与本书同期）。
2. **视图**：普通视图只读，可写视图 = INSTEAD OF 触发器（🔧 E3）；物化视图不存在，"视图+索引"
   靠手工汇总表。
3. **子查询与连接**：EXISTS vs IN 的优化器命运、相关子查询、`FROM` 子查询物化。
4. **全文检索 FTS3**（2010 现状：FTS3 已在，FTS4 于 3.7.3 进入 changelog ✅ first-mention，
   FTS5 要等 3.9.0 ✅ changelog 原句 "Added Full Text Search version 5 (FTS5) to the amalgamation"）。
5. **日期时间与格式化**：无 DATE 类型、六枚时间修饰符靠 `strftime` 一族函数（今天仍然如此）。

## 2. 精读要点（重构）

- `RAISE(ABORT)` 回滚**当前语句**、`ROLLBACK` 关键词回滚**整个事务**——书中此处有专门对比表
  （⚠️ 表未核验；语义 ✅ 与 lang_create_TRIGGER 现行文档一致）。
- 触发器内改 NEW 值仅 BEFORE 行触发器可为——2026 文档原样保留该规则。
- FTS3/4 的 `MATCH` 是"字符串谓词"，与 `LIKE` 的成本结构完全不同（倒排 vs 扫描）。
- 本章最大的时代眼泪：**用 `INSERT OR REPLACE` 模拟 upsert 的整套仪式**——今天一行
  `ON CONFLICT ... DO UPDATE` 终结（但语义差异必须实测钉死，见 E4）。

## 3. 🔧 实测（E4）：OR REPLACE vs UPSERT 的 rowid 语义分叉

| 观察 | 数字/结果 |
| --- | --- |
| `INSERT OR REPLACE`（ supplying id=1 撞唯一键） | 旧行**被删后重插**：本例恰好 rowid 仍=1，n=9；count=2。**若不提供 rowid，新行换 rowid，外键/依赖全断**（书的隐性坑 ✅ 语义实测） |
| 真 UPSERT：`ON CONFLICT(word) DO UPDATE SET n=n+100` | `(1,'alpha',109)`——原地 UPDATE，无删插 |
| UPSERT + `RETURNING id,v` | 一步拿回 `[(1,'x',1)]`，无需二次 SELECT |
| 窗口函数 `rank() OVER (ORDER BY v DESC)` | `[('x',1)]` 直接可用（3.25.0+） |
| FTS5 vs LIKE（5000 行英文语料，MATCH/LIKE 同词 'sqlite'） | MATCH **0.6 ms** vs LIKE **1.8 ms**（约 3×；本机数据量小，姊妹册 20 万行版为 15×——比值随规模扩大 ✅ 交叉印证） |
| rtree 矩形查询 | 命中 `[(1,)]` |
| `json_extract('{"a":{"b":42}}','$.a.b')` | `(42,)`，无需任何扩展加载 |
| `pow(2,10)`（3.35.0 数学函数，需编译旗标） | `(1024.0,)`——CPython 发行版已开旗标 ✅ |
| 生成列 `b INT GENERATED ALWAYS AS (a*2) VIRTUAL` | 插入 a=7 读出 `[(7,14)]` |

## 4. 2010 语境 vs 2026 现状对位

| 本书设定（3.6.x） | 2026 现状 | 锚点 |
| --- | --- | --- |
| FTS3 是"新玩具" | FTS3/FTS4/FTS5 三代并存、出厂内置（🔧 module_list 10 模块含 fts5/fts5vocab） | FTS5 3.9.0 ✅ changelog；FTS4 3.7.x ✅ first-mention |
| upsert 仪式 = INSERT OR REPLACE + 触发器补救 | `ON CONFLICT DO UPDATE/NOTHING` 一等语法 | 3.24.0 ✅ [lang_upsert.html](https://www.sqlite.org/lang_upsert.html) "History ...added with version 3.24.0 (2018-06-04)" |
| DML 后二次查询取回值 | RETURNING 子句 | 3.35.0 ✅ changelog 原句；[lang_returning.html](https://www.sqlite.org/lang_returning.html) ✅200 |
| 排名/累计靠临时表+相关子查询 | 窗口函数（含帧规范） | 3.25.0 ✅ changelog |
| 时间戳格式化 = 唯一选择 | 仍是 `strftime` 家族 + 新增 `unixepoch()/timediff()/to_unixsubsec` 等便捷函数 ⚠️（3.42+ 增强，未逐条核验） | — |
| 前缀索引/表达式索引受限 | 表达式索引一直可用（CREATE INDEX ON t(expr)）；3.9.0 起部分索引（WHERE 子句）✅ changelog first-mention "partial indices" 语境 ⚠️ 措辞 | — |

## 5. 常见误区

1. 把 `INSERT OR REPLACE` 当 UPSERT ⇒ 它是 DELETE+INSERT 原子操作：BEFORE DELETE 触发器会
   跑、外键级联会触发、rowid 会变（E4 第一行）。迁移到 `DO UPDATE` 前必须审计触发器。
2. 忘记 `PRAGMA foreign_keys=OFF` 默认 ⇒ 触发器里的"约束补偿"其实在裸奔（姊妹册 07 章同题）。
3. FTS 表当普通表 JOIN ⇒ `MATCH` 只能在虚表侧；`fts5vocab` 才是字典式访问入口。
4. 对 recursive_triggers 的恐惧过头 ⇒ 默认 OFF 是兼容行为（pragma.html ✅ "added in 3.6."），
   开启后注意 TERMINATE 条件。

## 6. 互链

- 触发器/视图理论面：[../数据库系统概念6/04-中级SQL.md](../数据库系统概念6/04-中级SQL.md)。
- FTS5 深潜（20 万行版实验）：[../Using_SQLite/10-扩展虚拟表与时间旅行.md](../Using_SQLite/10-扩展虚拟表与时间旅行.md)。
- 分析型 SQL（窗口/CTE 的列存对照物）：[../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)。
- 册内：UPSERT/RETURNING 在应用层的姿势见 [08-语言绑定.md](08-语言绑定.md)；执行计划在 [11-内部机制与新特性.md](11-内部机制与新特性.md)。

## 7. 触发器决策表（书时代"穷人版存储过程"的设计图纸）

| 你要做什么 | 触发器选型 | 关键注意 |
| --- | --- | --- |
| 补 CHECK 做不了的约束 | BEFORE + `RAISE(ABORT,'msg')` | 回滚当前语句，事务还在（⚠️ 语义 ✅ 文档） |
| 审计历史表 | AFTER INSERT/UPDATE/DELETE | NEW/OLD 行镜像；bulk 下每行触发（🔧 total_changes 含转发） |
| 派生列/汇总表 | BEFORE UPDATE/INSERT 改 NEW | 只有 BEFORE 行触发可改 NEW（03 章伏笔） |
| 视图可写 | INSTEAD OF（唯一解） | 🔧 E3 实证 |
| 防级联递归 | 默认 recursive_triggers=OFF | ✅ pragma.html "added in 3.6." 同期特性 |
| 假 upsert 修复 | 弃用 OR REPLACE → UPSERT | 🔧 E4：删插换 rowid 实证 |

## 8. FTS5 一课通（把 2010 的 FTS3 例子搬到 2026 跑）

```sql
CREATE VIRTUAL TABLE f USING fts5(body, tokenize='unicode61');  -- 分词器可指定 ⚠️ E4 用默认
INSERT INTO f VALUES('sqlite database engine number 1'), ...;    -- 🔧 5000 行
SELECT count(*) FROM f WHERE f MATCH 'sqlite';                   -- 🔧 0.6 ms
SELECT count(*) FROM f WHERE body LIKE '%sqlite%';               -- 🔧 1.8 ms（比值随规模升）
SELECT * FROM f WHERE f MATCH 'engine NEAR/3 number';            -- 短语/邻近语法 ⚠️ 通识
SELECT * FROM f('sqlite') JOIN f USING rowid;                    -- bm25() 排序 ⚠️ 未实测
```

## 9. 本章自检卡（一问一答）

1. Q：OR REPLACE 和 UPSERT 的本质差异？ A：删+插 vs 原地改（🔧 rowid 与触发器行为分叉）。
2. Q：`DO UPDATE` 里能引用新值吗？ A：`excluded.` 前缀（🔧 E4 用法）。
3. Q：RETURNING 能用在哪？ A：INSERT/UPDATE/DELETE 三 DML（✅ changelog 原句）。
4. Q：`rank() over ()` 无 ORDER BY？ A：合法，全行并列 rank=1（⚠️ 帧规则以 lang_window 页为准）。
5. Q：FTS 表能做普通列谓词吗？ A：可以但退化为扫描；MATCH 才走倒排。
6. Q：递归触发器默认？ A：OFF（✅）。
7. Q：触发器里能 SELECT 别的表吗？ A：能；但别在钩子里改本表引发递归（07 章重入告诫同源）。
8. Q：2010 怎么模拟"部分索引"？ A：表达式索引 + CASE 手工；3.8.0 起原生 WHERE 子句 ⚠️。
9. Q：json 字段查询 2010 方案？ A：外部函数/自解析；2026 一列 `json_extract`（🔧 42）。
10. Q：视图 + 触发器组合的坑？ A：INSTEAD OF 触发器不校验 NEW 列存在性，静默错配 ⚠️。

## 核心概念速览（中英对照）

- **行触发器** — FOR EACH ROW trigger：SQLite 只有行级，无语句级。
- **RAISE(ABORT/FAIL/IGNORE)** — 触发器内三档错误语义：回滚语句/保留先前/仅跳过本行。
- **INSERT OR REPLACE** — 删插语义的"假 upsert"：rowid 与触发器行为皆与 DO UPDATE 不同（🔧 E4）。
- **UPSERT** — `ON CONFLICT DO UPDATE/NOTHING`：3.24.0 起的 PostgreSQL 式正解 ✅。
- **RETURNING** — DML 返回受影响值：3.35.0 ✅。
- **窗口函数** — window function：rank/row_number/帧，3.25.0 ✅。
- **FTS5** — 全文检索虚表：3.9.0 编入 amalgamation ✅；MATCH 谓词 3×/15× 两级实测。
- **fts5vocab** — FTS5 词表视图模块：出厂即有（🔧 module_list）。
- **rtree** — R 树空间虚表：矩形谓词命中（🔧 E4）。
- **json_extract** — 路径取值：3.38 起内置（🔧 免加载直用）。
- **生成列（VIRTUAL/STORED）** — generated column：3.31.0（🔧 7→14）。
- **部分索引** — partial index：CREATE INDEX ... WHERE，3.8.0 起 ⚠️ 通识。
- **recursive_triggers** — 递归触发开关：默认 OFF，特性与本书同期（✅ pragma.html）。
- **表达式索引** — expression index：函数索引的 SQLite 形态，老特性。
- **穷人版存储过程** — trigger-as-procedure：2010 本章的真实主题。

## 最新演进与工业实践

- 本章是"2010 仪式→2026 一行"密度最高的章：upsert 仪式（3 段 SQL+触发器）→ 3.24.0；取回值
  仪式 → 3.35.0 RETURNING；排名仪式 → 3.25.0 窗口；JSON 文档桥接 → 3.38.0 内置 + `->`/`->>`
  操作符 ⚠️（3.38 引入，未逐条核验）；全文检索 FTS3→FTS5（3.9.0 ✅）。
- 2026 应用层通行组合拳：`INSERT ... ON CONFLICT DO UPDATE ... RETURNING` + STRICT 表 +
  CHECK，把当年"触发器工程学"的三成功能交还给声明层（趋势转述 ⚠️）。
- FTS5 的 trigram/unicode61 混合、`spellfix1` 等外部扩展生态繁荣（⚠️ 转述）；官方内置面维持
  fts3/4/5 + rtree + json 不动（🔧 module_list 证据）。
- 取证：本文件全部 ✅ 版本句出自 sqlite.org changes.html 抓取件与各专页 200 校验（清单见 00）。
