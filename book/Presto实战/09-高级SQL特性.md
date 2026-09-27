# 09 高级 SQL 特性

> 原书第 9 章（中译本 p.148–173）。定位：函数族+近似计算+窗口+lambda+地理空间——Presto 表达力的富矿。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 9.1–9.9 函数总览与标量/数学 | 函数命名空间（scalar/aggregation/window）与发现方式 | `SHOW FUNCTIONS LIKE '%...%'` 是手册 |
| 9.3–9.6 布尔/逻辑/BETWEEN/IS NULL | 三值逻辑细节 | NULL 传播规则决定谓词形态 |
| 9.10–9.13 字符串/映射/Unicode/正则 | regexp_extract 族、format 族 | 日志清洗主力工具 |
| 9.14 解嵌套 | UNNEST 展开 ARRAY/MAP | 嵌套→行的枢纽 |
| 9.15 JSON | json_extract(_scalar)/json_format | 弱结构数据的逃生舱 |
| 9.16 日期时间 | 时区敏感的函数族 | 交互式报表最常翻车区 |
| 9.17 直方图 | `histogram(col)` → MAP 频次图 | 探索式分析的"一页纸分布" |
| 9.18 聚合：映射/近似 | approx_distinct(HLL)、approx_percentile(T-Digest) | 大数据统计的内存换精度范式 |
| 9.19 窗函数 | OVER 分区/排序/帧 | 排名、同环比、滑动统计 |
| 9.20 lambda | transform/filter/reduce/zip_with 内的高阶函数 | SQL 里的函数式编程 |
| 9.21 地理空间 | GeoSPARQL…不，是 S2/geometric 函数族 | 原生类型 LINEAR_RING/POLYGON + 空间 Join |
| 9.22 Prepared Statement | PREPARE/EXECUTE/DEALLOCATE | 参数化省解析、护计划 |

## 精讲

### 1. 近似聚合是引擎性格（9.18.2）
- `approx_distinct(x)`：HyperLogLog，误差上界可调（标准误差参数），O(1) 内存；
- `approx_percentile(x, 0.99)`：T-Digest/QDigest（⚠️ 具体实现名按版本），百分位秒出；
- 交互式场景的正确姿势：**探索用近似、出报表用精确**——同一个 SQL 里把两族并排写，
  既省内存又给业务"误差可感"的沟通锚点。
**方法**（🔧 概念验证可用本机 Python `datasketch`/`tdigest` 复现 HLL/T-Digest 误差曲线；
Presto 本体结论为转述 ⚠️）：同一列分别跑 `count(DISTINCT x)` 与 `approx_distinct(x)`，
在集群内存监控（12.3/jmx）里对比驻留——"为什么大集群敢开高并发"的答案就在此。

### 2. UNNEST + lambda：嵌套类型的两段舞（9.14+9.20）
```sql
-- 事件数组展开并按阈值过滤计数（示意）
SELECT u.uid, tag
FROM   logs l, UNNEST(l.tags) AS u(tag)
WHERE  cardinality(filter(l.scores, s -> s > 0.9)) > 3;
```
- `UNNEST` 把一行数组变多行（cross apply 语义）；
- `transform/filter/reduce` 在**不展行**的前提下就地加工数组——
  比"展开→聚合回去"省一次 Exchange，是 4.9 局部聚合思想在表达式层的复刻。

### 3. 直方图与探索闭环（9.17）
`SELECT histogram(event_type) FROM big_table` 一行返回 `MAP<值,计数>`，
配合 `CARDINALITY`/解嵌套可当"迷你数据画像"；书中用它引入第 4 章的统计信息（ANALYZE 产的
频次分布是同一件事的两种视角：**用户探索 vs 优化器消费**）。

### 4. 地理空间不是彩蛋（9.21）
`POINT`/`LINESTRING`/`POLYGON` 原生类型 + `spatial_contains`/S2 索引类函数，
使"轨迹×围栏"这类 Join 可在一句 SQL 完成；该族与 Presto 的 TPCH z3 扩展、S2 Geometry 库绑定
（⚠️ 函数名以版本手册核对）。repo 视角：这是"表达式丰富度=护城河"论的极致样本。

### 5. Prepared Statement 的工程价值（9.22）
`PREPARE p AS SELECT ... WHERE id = ?; EXECUTE p USING 42;`
- 省重复解析/分析开销（协调器带宽，5.10 呼应）；
- JDBC 侧 `PreparedStatement` 映射到此机制 ⚠️ 版本相关；BI 网关层复用计划的关键。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| approx_distinct 是"不精确的 count distinct"所以低人一等 | 它是用**有界误差换常数内存**的正确工具；精确族在小基数用，近似族在大基数用 |
| UNNEST 随便放 FROM 里不影响计划 | 展开倍率×数据量的乘爆常见；先 filter 数组再 UNNEST 是肌肉记忆 |
| lambda 只是语法糖 | 就地加工避免重分布，是性能写法不是风格写法 |
| 时间函数无时区问题 | `now()/current_timestamp` 与会话时区联动；跨源对账必须钉死时区 |

## 与其他章/其他笔记的联系
- 类型地基 → [08-在Presto中使用SQL.md](08-在Presto中使用SQL.md) 8.9；
- 执行形态（为何这些写法省 Exchange）→ [04-Presto的架构.md](04-Presto的架构.md)；
- SQL 模式与方言通识 → [../SQL系列·总索引.md](../SQL系列·总索引.md)、[../SQL反模式.md](../SQL反模式.md)；
- JSON/弱结构处理对照 → [../nosql精粹.md](../nosql精粹.md)。

## 本章小结与行动清单

三句话带走：
1. 函数面分三层：标量（行内）/聚合（跨行，两阶段执行）/窗口（帧内跨行），
   写 SQL 前先问"我的语义在哪层"——跨层改写（窗口→自连接）是性能事故高发区；
2. 近似家族（HLL/T-Digest）与直方图把"统计学"变成 SQL 一等公民：交互式分析的默认姿势是
   **近似探索、精确出账、误差入报表脚注**；
3. UNNEST×lambda×高层数组函数构成的嵌套处理组合拳，决定了你能不能把 JSON/数组日志直接当表用——
   这是 Presto 方言相对多数 BI SQL 的代差优势。

团队函数规范落地清单：
- [ ] 高基数去重统一 `approx_distinct`（误差参数团队定版，如 0.01）并写进代码模板；
- [ ] 百分位类指标一律 `approx_percentile`，禁止 `ORDER BY` 全量排序取中位数的土法；
- [ ] 时间列查询强制会话时区声明（08 章类型坑的制度化）；
- [ ] 复杂表达式优先 lambda 就地加工，展行仅用于最终输出形态需要；
- [ ] `SHOW FUNCTIONS LIKE` 纳入新人 onboarding（手册意识）。

自测：
- [ ] `count(DISTINCT)` 在什么基数下开始伤集群？近似族的误差如何向业务方交代？
- [ ] 为什么 `transform/filter` 能省一次 Exchange？（4.9 局部思想表达式层复刻）

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 标量函数 | Scalar Function | 行内一对一变换 |
| 聚合函数 | Aggregation Function | 多行归一（含两阶段执行形态） |
| 窗函数 | Window Function | 分区帧上的排名/滑动聚合 |
| HyperLogLog | HLL | 基数估计算法，approx_distinct 内核 |
| T-Digest | T-Digest | 分位数草图算法，approx_percentile 内核 |
| 直方图函数 | histogram() | 聚合产出值→频次 MAP 的探索工具 |
| UNNEST | UNNEST | 集合列展开为行 |
| 基数 | Cardinality | 数组/集合长度（cardinality() 函数） |
| Lambda 表达式 | Lambda in SQL | transform/filter/reduce 等的高阶参数 |
| JSON 抽取 | json_extract / _scalar | JSONPath 取值（结构/标量两式） |
| 正则提取 | regexp_extract | 字符串模式捕获组提取 |
| 时区敏感函数 | Timezone-aware Functions | now/at time zone 族 |
| 地理空间类型 | Geospatial Types | POINT/POLYGON 等原生类型与空间谓词 |
| S2 索引 | S2 Geometry | 球面空间索引库（空间 Join 加速器） |
| PREPARE/EXECUTE | Prepared Statement | 参数化语句复用计划 |

## 最新演进与工业实践

- **近似计算家族扩张（2024–2026）**：两条线持续新增/调整 sketch 与统计函数
  （Reservoir/Digest 族、kll_sketch 等在 Trino 的引入 ⚠️ 以 Release Notes 核对）；
  函数手册入口：[github.com/prestodb/presto](https://github.com/prestodb/presto) ✅ 内 docs 与
  Trino SQL 文档（经 [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅ 导航）。
- **原生执行改写性能常数**：Velox 把大量标量/聚合函数以向量化 C++ 重实现，
  本章"表达式丰富度 vs 速度"的老权衡被部分刷新（函数支持覆盖面对照以官方 issue/文档为准）——
  [github.com/facebookincubator/velox](https://github.com/facebookincubator/velox) ✅，论文 DOI
  [10.14778/3554821.3554829](https://doi.org/10.14778/3554821.3554829) ✅（VLDB 2022），条目互见 [../../db/db.md](../../db/db.md)。
- **湖格式吸收 JSON/半结构**：Iceberg v3 对 variant/几何类型的推进使"Presto 侧逃生舱"前移到存储侧 ⚠️（以
  [iceberg.apache.org/spec/](https://iceberg.apache.org/spec/) ✅ 为准；互链
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)）。
- **国内印证**：美团文章即展示过交互式分析中近似函数与采样策略的取舍（同链接
  [tech.meituan.com Presto 实践](https://tech.meituan.com/2014-06-16/presto.html) ✅）；
  B 站 Adhoc/DQC 高频使用 window+CTE 组合控制扫描收敛（[dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅）。
- **学习资源**：官方函数手册的"按族浏览 + LIKE 搜索"工作流（`SHOW FUNCTIONS LIKE`）在两条线文档均保留；
  本书该节给出的"函数即目录"心智在 2026 年仍是上手最快路径。
