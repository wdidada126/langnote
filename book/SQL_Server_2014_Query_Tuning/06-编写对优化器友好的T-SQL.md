# 06 编写对优化器友好的 T-SQL（⚠️ 推定重建章·语言卷判决线）

> 状态声明：主题簇重建章。盘上根文件 [../Microsoft_SQL_Server_2008技术内幕.md](../Microsoft_SQL_Server_2008技术内幕.md) 经波4 #56 判决：其实体为 **Ben-Gan《T-SQL Fundamentals》语言卷**（douban 4047293；书根同存 2012 版源码包 55349_TSQLFundamentals2012.zip），并非内核/调优卷——因此「怎么写 T-SQL」的语言层深度归那条谱系，本章只承接**调优视角的写法后果**，避免同题并档。

## 6.1 语句形态→计划形态的因果表（本章主件）

| 写法 | 优化器看到的 | 计划后果 | 处方 |
|---|---|---|---|
| `YEAR(d)=2014` | 列侧函数 | 扫描+计算标量 | 半开区间（05 §5.3） |
| `WHERE a=@p OR b=@q` 跨列 | 难折的连接替代 | Expensive-OR/扫描 | UNION ALL 去重语义改写 |
| `NOT IN (子查询)` 可空列 | 需 Assert 语义 | 保守反连接 | `NOT EXISTS` |
| 标量 UDF 逐行调用 | 不透明黑盒 | 抑制内联（2014 时代表达式 ⚠️）| 内联表值函数 iTVF / 直接展开 |
| 游标/WHILE 循环 | RBAR 行循环 | N 次往返 | 集合式 UPDATE/窗口函数（语言卷军规互见上注根文件） |
| `SELECT *` | 宽列投影 | 覆盖失败、回表、网络税 | 列裁剪是调优第一义务 |
| 函数包裹连接键 | 类型/序不可用 | 连接退化为扫描哈希 | 列侧裸键+类型钉死 |
| 三段式 `WHERE` 大杂烩 | 无法拆解 | 选择性相乘雪崩 | 分段索引+过滤统计（02） |

## 6.2 参数化：语句「长相」决定一切下游（转述 ⚠️）

- 字面量 SQL（ORM 直接拼串）→ 计划缓存污染（高速编译/CPU 税、缓存驱逐）；**参数化 SQL 才有资格谈计划复用与嗅探**（07 章对象）。
- 简单参数化 vs 强制参数化：默认仅安全形态被简单参数化（模板化入缓存）；`sp_executesql`/类型化参数让优化器看见「参数」而非值——优化时按**统计快照+参数无关**估计（嗅探发生在执行时刻用实际值重估/复用，两条路径读 07）。
- ORM 侧义务清单：参数带显式类型与长度（长度不匹配即隐式转换温床）；分页统一 `OFFSET/FETCH`（2012+）替代 ROW_NUMBER 嵌套方言；批操作以 TVP（2008+）替代逐行 RPC——机制侧 TVP 的 tempdb 系统在 [../Pro_SQL_Server_Internals/08-XML与临时表.md](../Pro_SQL_Server_Internals/08-XML与临时表.md) 谱系有对位讨论。
- 动态 SQL：`sp_executesql` 内层参数化是正解；字符串拼接 SQL 在调优上等于「自断缓存」（与 07 章 ad-hoc 膨胀互证；安全面不属本目录，登记 [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md) 同款跨引擎立场——仅示意，非强制链）。

## 6.3 中间结果物化：把搜索空间剪断的艺术 ⚠️

- 临时表/表变量（2014 时代语境）：表变量**无统计、估计恒为 1 行族**（经典口径），大表变量参与连接是计划灾难高发区；临时表有统计但受创建时机影响（02 陷阱）。
- 「>16 表/巨型 CTE → 物化分步」的原理在 01 §1.2：每一步把子语句拉回穷举档，代价是多一次编译+tempdb IO——调优账要两头算。
- CTE 非物化屏障：内联展开，复杂引用多次=重复展开；「用 CTE 强制物化」是常见谣言 ⚠️ 转述。
- `#temp` 与索引：对大中间集在临时表上建索引常胜过对基表加索引（不污染生产写放大，05 §5.4）。

## 6.4 集合语义的等价改写库（示例示意，⚠️ 非原书代码）

- 运行总计：自连接/游标 → 窗口 `SUM() OVER(ORDER BY ... ROWS UNBOUNDED PRECEDING)`（2012+，帧默认行含并列注意语义）。
- Top-N 分组：相关子查询计数 → `ROW_NUMBER()/RANK()` + 过滤。
- 间隙与岛屿：NOT EXISTS 自证 → LAG/LEAD + 累计和。
- 除法/全包含：双 NOT EXISTS 或 GROUP/HAVING COUNT 比对（计划形态差异读 04 §4.2）。
- 去重删除：`ROW_NUMBER()... WHERE rn>1` 直删 vs 先物化再删——大表上后者可避免锁升级与日志尖峰（11 章）。
以上与 Ben-Gan 语言卷（根文件判决线）的「集合思维军规」同源，此处只记「改写→计划」映射，不重复其推导。

## 6.5 反模式博物馆（各一条判读信号）

1. `sp_executesql` 参数长度大于列宽 → CONVERT_IMPLICIT 上键列（03 XML 警告）。
2. 每行调用标量 UDF 的 UPDATE 巨表 → 实际计划 CPU 全在 Compute Scalar（iTVF 化处方）。
3. WHERE 里对列做 `RTRIM()` → 持久化列/改写双出口。
4. `ORDER BY (SELECT NULL)` 式技巧绕过 TOP 语法 → 优化器视为无保证形态，计划随版本漂移。
5. 隐式事务+大 DELETE 分批 → 改 `WHERE` 分段+循环（日志增长与锁升级，11 章联动）。
6. `IN (@list)` 字符串拆分函数包裹 → 拆列后列侧函数化（回 6.1）。

## 6.6 🔧 本机类比：同义改写的计划差（非本书引擎行为）

SQLite 3.45.3（orders 50 万行，索引态同 05 G1/G2）：
```
写法 A: SELECT ... WHERE cust=1234 AND status IN ('A','B')
  → SEARCH ... USING INDEX (cust=? AND status IN(?,?))   -- 分段 Seek
写法 B: 把 status='A' 包进 CASE: WHERE cust=1234 AND CASE WHEN status='A' THEN 1 ELSE 0 END=1
  → SEARCH ... USING INDEX (cust=?)，status 退化为残余过滤
```
- 演示要点：**同一逻辑谓词，列侧被表达式包裹即从 Seek 键序跌落为残差**——与 6.1 表第一行、05 §5.3 同构；SQLite 用一行 EXPLAIN 就能让学员「看见」SARGability，SQL Server 的对应物是 CONVERT_IMPLICIT/Compute Scalar 判读。
- 方法：`EXPLAIN QUERY PLAN` 直读；数据同上 🔧 组，复现脚本在 tmp/dbwave_w5_sstune。

## 6.7 本章检查清单

- [ ] 能默写 8 行「写法→后果→处方」表。
- [ ] 能解释简单/强制参数化与 sp_executesql 的缓存关系。
- [ ] 知道 2014 时代表变量的估计缺陷及其后续修复（演进节）。
- [ ] 能给 4 类集合改写的计划形态差异。
- [ ] 会用 🔧 写法 A/B 演示列侧包裹的代价。

## 6.8 改写工坊：十条 before/after 速判（示意 ⚠️）

1. `WHERE dt >= '20140101' AND dt < '20150101'` ⇚ `YEAR(dt)=2014`：半开区间换 Seek。
2. `NOT EXISTS` ⇚ 可空列 `NOT IN`：去 Assert。
3. iTVF ⇚ 标量 UDF 进 SELECT 列：黑盒入树。
4. `OFFSET 1000 ROWS FETCH 20 NEXT` ⇚ `ROW_NUMBER` 双嵌套：计划一阶化。
5. `GROUP BY` 预聚合再连 ⇚ 明细直连大表：行数砍在连接前。
6. `UNION ALL 两支` ⇚ 跨列大 `OR`：各自 Seek。
7. `UPDATE t SET ... FROM 联接` ⇚ 逐行游标：集合化。
8. TVP 批入参 ⇚ 循环单行 INSERT：RPC 归一。
9. 列裁剪的显式投影 ⇚ `SELECT *`：覆盖可能性回升。
10. `#temp` 分步 ⇚ 16+ 表巨连接：搜索空间剪断（6.3）。

## 6.9 一页口诀

> 列要裸、类型要对、区间要半开；
> 行要成集、数要参数、值要嗅得对；
> 中间结果物化是刀、表变量估一是坑；
> 写法先行，索引随后，提示最后。

## 6.10 与语言卷的分工备忘

- 集合思维/窗口推导/传统 SQL 军规 → 根文件判决线（00 §3 第三行）与 Ben-Gan 谱系。
- 本章只管「写法落进优化器后的形态」，两层引用互不重复。

### 附 6-A：自测快问（答案均在本章上文）

1. 写法→后果→处方表任选四行默写。
2. 简单/强制参数化与 sp_executesql 的缓存关系？
3. 2014 时代表变量为什么是计划灾难高发区？
4. CTE 是不是物化屏障？为什么？
5. 大中间集建索引为什么优先 #temp 而非基表？
6. 🔧 写法 A/B 演示的核心概念是哪一个？
7. 标量 UDF 与 iTVF 的调优差在 2019 后如何变化？
8. 本章与 Ben-Gan 语言卷的分工线划在哪？

## 核心概念速览（中英对照）

- **参数化查询** — Parameterized Query：模板化 SQL 以复用计划。
- **简单参数化** — Simple Parameterization：引擎自动模板化安全语句。
- **强制参数化** — Forced Parameterization：数据库级把所有字面量模板化。
- **sp_executesql** — 带类型化参数的动态执行入口。
- **标量 UDF** — Scalar UDF：逐行黑盒，2014 时代优化抑制者。
- **内联表值函数** — Inline TVF：可展开为子表达式的「参数化视图」。
- **TVP** — Table-Valued Parameter：集合入参，替代逐行 RPC。
- **物化屏障** — Materialization Barrier：强制中间结果落盘的语句形态。
- **窗口函数** — Window Functions：OVER 族，替代自连接/游标模式。
- **残余过滤** — Residual Predicate：无法进 Seek 键序、逐行判定的谓词。
- **RBAR** — Row-By-Agonizing-Row：游标式行循环反模式统称。
- **半开区间** — Half-Open Range：`>=起点 AND <终点` 的日期谓词标准形。

## 最新演进与工业实践

- **标量 UDF 内联（2019 兼容级 150+）**：6.1/6.5 的「黑盒抑制」在 IQP 时代被大幅拆除，但确定性/副作用仍阻断内联。✅ intelligent-query-processing 页。
- **内联表变量（2019）与延迟编译（2019）/记忆化（2022）**：6.3 的表变量恒估缺陷成为官方修复对象；升级后「老写法不再天然危险」，但 6.2 的参数化义务永存。⚠️ 转述。
- **ORM 生态**：EF/Dapper 等默认参数化+类型钉死程度决定生产计划质量；「先抓缓存再看 ORM 生成 SQL」是 .NET 栈常规调优循环 ⚠️ 生态转述。
- **跨引擎同题**：MySQL 侧对位材料（同样以「写法→索引可用性」为主线）见 [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md) 与 [../Understanding_MySQL_Internals/09-解析器与优化器.md](../Understanding_MySQL_Internals/09-解析器与优化器.md)；PG 侧 SARGability 语义差异登记在飞兄弟 Learn_PostgreSQL_2e（波5，勿链只登记）。
- **教学法**：6.6 的 A/B 一行式实验被各引擎工作坊通用化（DuckDB `EXPLAIN` 亦可复现），低成本建立「谓词位置决定访问路径」直觉 🔧 经验推广。
