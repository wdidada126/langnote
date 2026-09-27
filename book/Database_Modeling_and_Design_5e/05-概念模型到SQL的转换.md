# 05 · 概念模型到 SQL 的转换（第 5 章 Transforming the Conceptual Data Model to SQL, pp.85-108）

> 本章文件为**精读重构**，非原书文本。章题与页区间 ✅ Crossref 实抓；映射规则编号体系（R1/R2…）为本目录重构命名（⚠️ 原书编号以纸质版为准）。本章是全书工程含金量最高的一章：概念层 ER 图在这里"过闸"变成 SQL DDL。

## 一、本章定位

24 页给出一套**可执行的翻译规则表**：每种 ER/UML 构造 → 表、列、主键、外键、CHECK 的落法，以及每条规则背后的存储/维护代价账。Teorey 的讲法从不等式出发："这个联系将来查询是顺向多还是逆向多？"——映射方向因此不是教条而是代价选择。这也是它连接物理设计书系（PDD 第 1/15 章）的枢纽位置。

## 二、基础规则集（重构编号）

| 规则 | ER 构造 | 映射 | 要点 |
|---|---|---|---|
| R1 | 强实体 | 1 表；属性→列；主键→PK | NOT NULL 显式写，别信默认 |
| R2 | 复合属性 | 展平为成员列 | 除非整体读取，否则不存 JSON ⚠️2011 口径 |
| R3 | 多值属性 | 独立 2 列表（PK=引用键+值） | 本质是 M:N 的退化特例 |
| R4 | 派生属性 | 不落库 | 或生成列落库（现代折中，见下节） |
| R5 | 1:1 联系 | 合并进一侧，或独立表 | 合并方向看"哪侧读另一侧更频繁"；可空外键挂稀疏侧 |
| R6 | 1:N 联系 | FK 放 **N 侧**表 | 全参与→NOT NULL；联系带属性→属性随 FK 同表 |
| R7 | M:N 联系 | 独立桥接表 PK=两端 FK 复合 | 联系属性放桥接表；两端都建反向索引 ⚠️物理层 |
| R8 | 三元/多元联系 | 独立表 PK 视约束而定 | "跨边约束"只有独立表能表达——R7 的推广理由 |
| R9 | 弱实体 | 1 表，PK=(识别者FK+局部键)，ON DELETE CASCADE | 级联语义来自存在依赖 |
| R10 | 递归联系 | 同表自 FK + 角色列/表名消歧 | 树形另议（邻接表/闭包表） |

## 三、ISA 三方案（本章的"必考题"）

设 PERSON(id, name, …) 与子类 STUDENT(gpa)、INSTRUCTOR(salary)，`{xor}` 或 overlap，total 或 partial：

| 方案 | 表结构 | 优点 | 代价 |
|---|---|---|---|
| M1 一表全并 | 单表含全部属性 | 无 JOIN；查询最简 | 大量 NULL（稀疏列）；约束靠 CHECK 堆 |
| M2 超类+每子类 | PERSON + STUDENT + INSTRUCTOR 各一表，子表 PK=FK→PERSON | NULL 最少；类型干净；子类可独立演进 | 每次"按人查角色"都要 JOIN；`{xor}` 无法用键表达（要触发器/CHECK） |
| M3 超类+一关系表 | PERSON + BELONGS(role, ref) | 子类可扩展不动 DDL | 引用完整性最弱（多态外键），实务口碑差 |

- 本书决策树（重构转述 ⚠️）：子类少且稳定→M2；子类是"少数派属性"（<20% 行有值）→M1；类型层次会增改→M2 配视图。
- total/partial 决定子表是否配 `PERSON 必有子行` 的守护（触发器/应用/延期）——教科书在此诚实承认：**关系层无法优雅表达全部概念约束**，这正是第 8 章对象关系存在的理由。

## 四、映射的代价账（与物理设计的接缝）

- R6 的 FK 方向决定 JOIN 形态：N 侧挂键→"顺查"便宜、"逆查"需扫 N；与 R7 桥接表对比时，本章已用"每查询平均 I/O"粗算 ⚠️ 例题数字以原书为准。
- 1:1 的合并/分离选择 = PDD 第 15 章"反/合表"决策的概念层镜像（[../Physical_Database_Design/12-数据仓库OLAP与反范式化.md](../Physical_Database_Design/12-数据仓库OLAP与反范式化.md)）。
- 索引不在本章职责内，但 R7 桥接表"两端都要索引"是本章唯一物理暗示——展开见 [../数据库索引设计与优化.md](../数据库索引设计与优化.md)。

## 五、UML 侧的同步映射

类图元素按第 3 章对照表先"ER 化"，再走 R1-R10；关联类（带属性关联）天然走 R7；组合走 R9。本章强调：**两份记法一套规则**，映射表与记法无关——这是"双轨教学"的最终收束。

## 六、易错点与自测

**易错**：① 1:N 把 FK 放 1 侧（一个格子存 N 个值，退化多值）；② 桥接表忘建联系属性（成绩丢了）；③ M2 方案用 `NOT NULL` 强凑 `{xor}`（应为 CHECK/触发器或应用约束）；④ 弱实体局部键当全局 PK；⑤ 级联删除未开（SQLite 默认 FK 不生效 🔧）。

**自测五问**：① R5 何时选"合并"何时"独立表"给出两条判据；② overlap ISA 下 M2 的约束缺口在哪；③ 用 R7 解释"多值属性表"与"桥接表"同构；④ FK 侧放错的性能后果量级估算思路；⑤ 本章哪些规则在文档型数据库里被改写。

## 补充一、映射演练：电商域 12 分钟走完 R1-R10

概念输入：CUSTOMER、PRODUCT（多值标签）、CATEGORY（PRODUCT 多对多分类）、ORDER（含下单客户）、LINE_ITEM（订单内序号+价格快照）、REVIEW（客户评产品，带评分）、VIP/PUBLIC 客户两类（{xor}）、配送地址（客户 1:N）。

| 步 | 构造 | 规则与产物（列要点） |
|---|---|---|
| 1 | CUSTOMER/VIP/PUBLIC | ISA：属性少（积分、折扣率）→ M1 单表 `customer(kind, points, discount)` + CHECK 一致性 |
| 2 | ADDRESS | R6：客户 1:N，FK 进 ADDRESS（NOT NULL=全参与）；地址"区划编码"→ 引 CATEGORY 教训，先建 DISTRICT 表 |
| 3 | TAG（多值） | R3：`product_tag(product_id, tag)` PK 两列 |
| 4 | PRODUCT-CATEGORY | R7：`product_category(product_id, category_id)`；联系属性"主分类标志"落桥表——桥表升格的第一个信号 |
| 5 | ORDER→CUSTOMER | R6：FK 进 ORDER（N 侧），历史价格快照进 LINE_ITEM（SCD1 的 OLTP 正当性） |
| 6 | ORDER-LINE_ITEM | R9：LINE_ITEM 弱实体，PK `(order_id, line_no)` + CASCADE |
| 7 | REVIEW | M:N 带属性 → R7：`review(product_id, customer_id, rating, ...)` PK 前二列（一人一评假设；若允许多评则加时间代理列并登记决策） |
| 8 | 派生列 | "订单总额"不落库（R4）；报表侧物化留给第 10 章/物化视图 |

**自检**：每张表能回答"一行承诺什么"；每个 FK 能回答"参与约束是什么、删父行该怎样"。

## 补充二、映射规则的代价公式（口语版 ⚠️ 重构）

- 空值税：M1 方案每稀疏列 ≈ 扫描/索引体积膨胀 + 语义歧义；
- JOIN 税：桥接表使查询链 +1 跳；用"平均链长×行选择率"估；
- 更新税：冗余列（反范式）= 每次真值变更多 N 处写 + 一致性守卫；
- 三税互兑：读多→买冗余；写多→买范式；两者都多→分区/缓存问题，出逻辑设计域。

## 补充三、现代映射补订（2026 眼光回看 2011 规则表）

- R2 复合属性：JSON 列成为新选项——"整体读写且无独立约束"才嵌套，判据没变、选项变了；
- R4 派生属性：生成列（PG/SQLite/Oracle 各有 ✅）允许"可推导但值得物化"的中间档，但必须声明**单一真相源列**；
- R5 1:1：ORM 懒加载习惯使"分离+FK"成为默认，合并方案需要理由——教科书判据（读写画像）仍有效；
- R7 桥接表：图数据库把"联系一等公民"化——桥表的"反向索引需求"在图库是原生双向遍历（⚠️ 转述）；
- 新增规则位：**事件/审计需求**（谁在何时改过 X）——ER 时代常外包给应用日志，如今建议显式建模（temporal/audit 表，第 7 章决策日志的库内化）。

### 映射决策树（口述版，背下来）

1. 是弱实体吗？→ R9（复合 PK+CASCADE），不是继续；
2. 是 ISA 吗？→ 数子类属性列数与行占比：<20% 且子类少→M1；否则 M2；{xor}/total 落不进 DDL 的部分登记为应用/触发器义务；
3. 是 1:1 吗？→ 读频高侧合并，读频均衡且属性多→独立表+双向 UNIQUE FK；
4. 是 1:N 吗？→ R6，N 侧挂键，全参与加 NOT NULL；
5. 是 M:N/多元/多值吗？→ R7/R8/R3 桥表族，联系属性一律进桥表；
6. 是派生吗？→ R4 不落库，除非报表侧申请物化预算；
7. 每张产出表回答"一行承诺什么"——答不出就回炉。

### 本章一页总结

- 映射是"语义→约束"的守恒翻译：ER 上每一条线、每一个数字，最终都必须以 PK/FK/NOT NULL/CHECK/触发器之一现身，否则就是丢约束；
- 方向选择（FK 挂哪侧、合并还是分开）永远是代价题，不是信仰题；
- DDL 落地只是上半场，**决策日志**（为什么 M1、为什么不合并）决定这张模式三年后还有没有人敢改。

## 核心概念速览（中英对照）

1. **映射规则** — mapping/transformation rules：概念构造→SQL 对象的机械翻译表
2. **外键** — foreign key：表达联系/引用完整性的落库手段
3. **桥接表** — bridge/junction table：M:N 联系的独立关系表
4. **复合主键** — composite primary key：多列联合唯一标识
5. **级联删除** — ON DELETE CASCADE：存在依赖的 DDL 表达
6. **ISA 映射方案** — inheritance mapping (M1/M2/M3)：单表/每子类表/关系表三策略
7. **稀疏列** — sparse columns：M1 方案产生的大面积 NULL 列
8. **多态外键** — polymorphic association：弱完整性引用的反面教材
9. **生成列** — generated/computed column：派生属性"可控落库"的现代折中
10. **可空性设计** — nullability design：NOT NULL 即参与约束的 DDL 化
11. **自关联** — self-referencing FK：递归联系的表结构
12. **代价账** — cost trade-off：映射方向选择的评判标尺

## 最新演进与工业实践

- **ORM 时代**：本章三方案即 Hibernate/EF/SQLAlchemy/Prisma 的 `Inheritance Mapping`（joined/table-per-concrete/single-table）三件套——教科书比工具文档早二十年，术语可互查 ⚠️ 文档转述；SQLAlchemy 官方文档（inheritance 章）是 M2 的活标本（github/rtfd 直连超时 ⚠️ 仅登记）。
- **约束能力升级（2024-2026）**：PG 15+ 的 `MERGE`、表达式生成列与逻辑分区让 R4/R6 的部分触发器需求可声明式解决（✅ https://www.postgresql.org/docs/current/ddl.html 可达）；SQLite 3.45.3 生成列实测可用 🔧。
- 🔧 **SQLite 实测**（本机 3.45.3，脚本 `D:\develops\tmp\dbwave_dmd5e\demo3.py`）：R7 桥接表 `enroll(student_id→student, section_id→section, grade, PK(student_id,section_id))` 建表插 3 行；插入 `student_id=99` → `FOREIGN KEY constraint failed` ✅；要点：必须 `PRAGMA foreign_keys=ON`（默认关闭）——**这是"SQL 标准约束"与"引擎默认行为"的经典落差**，同 DDL 在 PG/SQL Server 默认即生效 ⚠️ 转述。
- **文档模型改写**：R2/R3 在 MongoDB 里以嵌套/数组回归（1:1 合并、1:N 内嵌数组）——映射代价账重算：JOIN 换内嵌、更新代价换读取局部性（[../设计数据密集型应用.md](../设计数据密集型应用.md) 的 schema evolvability 讨论）。
- **与 repo 衔接**：规则背后的"键语义"理论纵深见 [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)（Date 谱系）。
