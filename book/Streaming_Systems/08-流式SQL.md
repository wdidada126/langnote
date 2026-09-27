# 第 8 章 流式SQL（Streaming SQL）

> 对应原书 Part II 第 8 章（英文原题 *Streaming SQL*；中译「流式SQL」）。
> 小节目录 ✅ oreilly.com.cn 实抓：8.1 什么是流式SQL / 8.2 回顾：流和表的偏好 /
> 8.3 展望：迈向健壮的流式SQL / 8.4 小结。
> 本文件为精读重构。本章回答一个历史性问题：**SQL 生来就在表上，凭什么能在流上活？**

## 章定位与中心论题

第 6 章的对偶性给了许可证：**流 = 表 + 时间取向**。于是"流式 SQL"不是新语言，
而是**给经典查询补上 Where/When/How 三个缺省参数**：
传统 SQL 隐含"在全表快照上、现在执行、结果一次性返回"；流式 SQL 把这三个隐含值显式化，
其余语法**一字不改**。本章同时是全书四问框架与关系代数的一次会师。

## 逐节精读重构

### 8.1 什么是流式SQL

- 先纠正一个常见误读："SQL over streams" 不等于"把流当字符串表查"；
  正统定义（重构表述）：**对动态表（第 6 章）求值的连续查询（continuous query）**，
  输入随 changelog 演化，输出是持续更新的表或再次展开为流。
- 静态语义守恒律：一条合法 SQL 在**任意快照**上应当给出该快照的正确答案——
  流式执行只是"增量地维持这个答案"。这句话把 6.5 的"物化视图"论断翻译成 SQL 方言。
- 历史脉络 ⚠️：连续查询研究（1990s TELEGRAPH/CQ、NiagaraCQ 一系）早已写下该语义，
  本书的贡献是把它们与水位线/窗口模型接上——**SQL 不需要为流重造，只需要补全**。

### 8.2 回顾：流和表的偏好

- 把第 6 章四象限落到 SQL 习惯上：
  - `GROUP BY` 无窗口 = 全表聚合（What + 全局 Where）；
  - 窗口函数 `OVER (PARTITION BY ... ORDER BY ...)` = 每行对"移动前缀"求聚合 = **逐元素快照**；
  - `GROUP BY TUMBLE/HOP/SESSION(...)` = 把 Where 显式化；
  - 关键观察（本章文眼）：**标准 SQL 只有 Where 没有 When/How**——
    窗口聚合默认"最后全量出一次"，即批的 When。这正是健壮化要补的缺口。
- 输入偏好问题：同一物理数据，声明为表（读快照）还是流（读 changelog），
  决定查询是"一次性"还是"永动"——语法相同、语义取向不同（6.4 的用户侧再现）。

### 8.3 展望：迈向健壮的流式SQL

- 健壮 = 乱序/迟到/纠错都**留在语言语义内**，而不是靠运维旋钮兜底。路线图三件（⚠️ 转述原书展望）：
  1. **允许声明 When**：何时可发布中间答案（触发）、允许迟到多久；
  2. **允许声明 How**：修正以回撤（retract/upsert）流入下游——输出从"表"变"带符号流"；
  3. **元语言统一**：把水位线来源（事件属性声明 `WATERMARK FOR ts AS ...`）纳入 DDL。
- 作者对时态表的讨论（⚠️ 转述，为第 9 章铺垫）：`FOR SYSTEM_TIME AS OF` 类语法
  让"表"在 JOIN 中带时间维度——批 SQL 语法长出时间参数是健壮化的关键一步。
- 现实注脚（本目录补记）：Beam SQL 方言（✅ https://beam.apache.org/documentation/programming-guide/ 之 SQL 扩展 ⚠️）
  与 Flink SQL（动态表+撤回流+窗口 TVF ✅ 文档线见下演进节）走的恰是 8.3 路线图，
  "预测被原书语言层命中"是本章值得骄傲的读法。

### 8.4 小结

流式 SQL 的难点从来不是语法而是**时间参数的显式化**；
SQL 的声明式气质反而使它成为四问框架最好的用户界面——第 9 章将验证这一点。

## 🔧 概念演示一：Over 聚合 = "逐元素快照"语义的批式显影（DuckDB，非真流引擎）

```sql
with t(ts, k, amt) as (values (1,'a',10),(2,'a',5),(3,'b',7),(4,'a',-10),(5,'b',3))
select ts, k, amt,
       sum(amt) over (partition by k order by ts
                      range between 2 preceding and current row) as running_2
from t order by k, ts;
```

🔧 实测输出：

```text
ts=1 k=a amt=10  running_2=10
ts=2 k=a amt=5   running_2=15
ts=4 k=a amt=-10 running_2=-5    （ts=1 滑出 RANGE 2 之后）
ts=3 k=b amt=7   running_2=7
ts=5 k=b amt=3   running_2=10
```

解读：每一行输出都是"**截至该行时刻的局部表答案**"——8.2 所谓"逐元素快照"。
注意 `amt=-10`：删除以带符号值进入聚合，正是 8.3 第 2 件（回撤思想）在语法夹缝里的可用形态。

## 🔧 概念演示二：无界流上的"健壮聚合"= 快照 + 修正（承接第 6 章演示 C）

把 changelog 按任意时刻折叠成表（第 6 章 SQL 复用），即可模拟"结果表随迟到不断被修正"：
`at t=4: a=15` → `at t=6: a=15`（a 不再变）、`b: 20→0`。
批 SQL 能表达**快照序列**（每 t 一次全量重算），但表达不了"只重发差异"（retract stream）——
该缺口即 8.3 路线图第 2 件，Flink 以 `+U/-U` 行种类在**引擎层**补齐 ⚠️（转述）。

## 与相关书目的衔接

- [../Trino_The_Definitive_Guide_2e/09-高级SQL特性.md](../Trino_The_Definitive_Guide_2e/09-高级SQL特性.md)：
  有界世界的窗口函数/over 聚合权威讲法——8.2 的每种"批习惯"都能在此找到原型；
- [../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md](../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md)：
  8.3 路线图的 Flink 实现全档（动态表、撤回流、窗口 TVF）；
- [../SQL系列·总索引.md](../SQL系列·总索引.md)：SQL 语言谱系入口；
- [../设计数据密集型应用.md](../设计数据密集型应用.md)：物化视图维护 = 连续查询的单机形态。

## 核心概念速览（中英对照）

- **流式SQL** — streaming SQL：对动态表求值的连续查询，SQL 语义按快照守恒
- **连续查询** — continuous query：永不下班的查询（1990s 概念，本书复活）
- **动态表** — dynamic table：随 changelog 演化的表，流式 SQL 的操作对象
- **逐元素快照** — per-element snapshot：over 聚合的语义本质
- **回撤流** — retract stream：带 +U/-U 的输出流，How 的 SQL 化
- **upsert** — 按键合并输出：retract 的工程近亲（幂等 sink 的通道）
- **窗口 TVF** — window table-valued function：`TUMBLE/HOP/SESSION()` 把 Where 写进 FROM
- **WATERMARK FOR** — 事件属性声明：把第 3 章推断参数纳入 DDL
- **FOR SYSTEM_TIME AS OF** — 时态连接语法：表长出时间维度的标志（第 9 章主场）
- **语法守恒律** — semantics preservation：任何快照上结果与批查询一致
- **触发/迟到的语言化** — declaring when/how：8.3 未竟路线图（各引擎仍未标准化 ⚠️）

## 最新演进与工业实践

- **Flink SQL 文档线已到 2.x** ✅：Flink 2.3 中文文档含「窗口聚合 / Over 聚合 / 窗口关联 /
  去重 / Top-N / 模式检测 / 时态表 / Materialized Table」完整家族
  （✅ https://nightlies.apache.org/flink/flink-docs-release-2.3/zh/release-notes/flink-2.0/ 页面导航实证，200）——
  8.2/8.3 展望的语法清单大部分已成文；**唯独"触发与累积模式"仍未进入标准 SQL 语法**（Flink 用
  allowedLateness 等表选项近似 ⚠️），8.3 路线图第 1 件仍开放。
- **物化表**（MT）✅ 存在性实证见上导航；其定位正是"流式 SQL 的产品化封装"：用户声明查询与新鲜度，
  引擎生成 continuous query 与刷新调度（细节 ⚠️ 转述，见第 6 章演进节同款说明）。
- **湖仓 SQL 的合流**：Iceberg/Delta 的 time-travel + incremental query 让批 SQL 引擎（Trino/Spark）
  也能"顺着快照序列看流" ⚠️（对照 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)
  与 [../Trino_The_Definitive_Guide_2e/06-连接器.md](../Trino_The_Definitive_Guide_2e/06-连接器.md)）——
  8.2 的"输入偏好"问题在存储层获得了新选项。
- **增量计算复兴（2023–2026）** ⚠️：以 DBSP 为理论基底的新一代增量/连续查询系统（Materialize、
  Feldera、Path、risingwave 一系）持续升温；其论文未在本会话完成 Crossref 校验，
  此处仅列名词不作引用断言——但方向与 8.3 完全同路：**SQL 的流式健壮化是进行时**。
