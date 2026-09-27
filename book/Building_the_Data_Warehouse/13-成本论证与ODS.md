# 13 · 第 15 章 Cost-Justification and Return on Investment + 第 16 章 The Data Warehouse and the ODS

> 两章合并（商业论证 + 近实时伴侣架构，映射见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。章题小节题 ✅ 官方 Contents PDF；正文为**精读重构**。英文原书约 413–442 页。

## A 部分 · 第 15 章：成本论证与投资回报

### 15.1 先破「抄对手」论证（✅ Copying the Competition）

Inmon 讽刺开篇：当年最流行的建仓理由是客户讲标里的「对手有我也要有」——他称之为**恐惧驱动**而非价值驱动（⚠️ 措辞重建）；随后给严肃版：ROI 论证要在**立项前**做，宏观微观两层。

### 15.2 宏观与微观论证（✅ The Macro Level / A Micro Level Cost-Justification）

- 宏观=企业级：把「信息获取总成本」（程序员抽取工时+口径争议决策损耗+数据不可用错失窗口）整体与建仓 TCO 对账；
- 微观=场景级：为每个主题/应用单独立项算账，**拒绝「全有或全无」**——这与第 9 章「逐主题增量」互锁：每步都能自证回报，工厂才能持续拿到预算 ⚠️ 通说。
- **Information from the Legacy Environment（✅ + 中译 15.4.1–15.4.6 六小段）**：旧环境取数的真实成本清单（新信息的成本/用数仓收集信息/成本比较/建仓/完整情况图/得到数据的障碍）——核心是**机会成本**：取不到的分析=隐损失，Inmon 要求把它计入资产负债表外 ⚠️。

### 15.3 数据的时间价值与集成信息的价值（✅ The Time Value of Data / The Speed of Information / Integrated Information / The Value of Historical Data / Historical Data and CRM）

- **时间价值/信息速度（✅）**：同一信息，实时决策价值≫月报；「仓库=慢数据」的批评被他反转为「仓库是历史数据增值库，快数据另有 ODS（下节）」；
- **历史数据的价值 ✅**：客户关系的长期曲线（CRM 案例 ✅ 中译 15.6.2）——**留存历史是资产不是负债**，为第 2 章「不删史」与第 12 章「归档」做财务背书；
- 2026 对位 ⚠️：FinOps 与「数据 ROI 度量」（data product P&L）是本章的制度化后代；湖仓时代「存历史几乎免费」削弱了「为留存付成本」的论证需求，但「证明数据资产价值」的 CFO 考题永在。

## B 部分 · 第 16 章：数据仓库和 ODS

### 16.1 ODS 定位：互补结构（✅ Complementary Structures）

ODS（Operational Data Store，操作型数据存储）=仓库的**近实时伴侣**：当前值、细到事务、短保留、可更新 ⚠️（与 EDW 的「历史/只追加/长保留」互补）。Inmon 对 ODS 的态度历来克制：它不是仓库替代品，是**时效性需求的泄压阀**（防止用户逼 EDW 做 24×7）。

### 16.2 六个机制（✅ 小节题全实据）

- **Updates in the ODS（✅）**：ODS 允许更新（区别于 EDW 非易失）——代价是其历史由「变更日志/时间分片」兜底；
- **Historical Data and the ODS / Profile Records（✅）**：ODS 不留长史，要史去 EDW；档案记录在 ODS 侧给当前横截面；
- **Different Classes of ODS（✅ 中译 16.2「不同种类的ODS」）**：按集成度与刷新频率分档 ⚠️ 通说；
- **Database Design — A Hybrid Approach / Drawn to Proportion（✅）**：ODS 设计=规范化+适度反规范化的混合，「按比例绘制」=按访问比例定冗余度；
- **Transaction Integrity in the ODS（✅）**：跨源当前值要在 ODS 内达成事务一致（它的「操作型」姓氏来源）；
- **Time Slicing the ODS Day（✅）**：把一天切多片装载，缩短时效窗口——批处理时代对「实时」的最大让步；对位 2026：CDC 连续化后此节变「微批间隔设定」。

### 16.3 多个 ODS、Web 与案例（✅ Multiple ODS / ODS and the Web Environment / An Example of an ODS）

- 多 ODS 的边界问题（全局 ODS vs 域 ODS）与第 6 章分布式仓库同构 ⚠️ 推定；
- **ODS 与 Web（✅）**：网站「当前库存/当前积分」类读需求的最优宿主；
- 与三方关系：Kimball 把 ODS 划在体系外（工具箱3 术语表位 ⚠️）；DV 社区把 ODS 视作一种 staging 变体（[../Data_Vault_2_0/08-物理数仓设计.md](../Data_Vault_2_0/08-物理数仓设计.md) 的装载分层可类比 ⚠️）；现代云仓的「近实时层/增量物化视图」事实上接管 ODS 职能 ⚠️（[../大数据之路.md](../大数据之路.md) 的 ODS→DWD 命名直接继承了这一层概念的中国化 ✅）。

### 16.4 🔧 最小 ODS 演示（DuckDB，可复现）

在同库内并建两张表对照：`edw_atomic`（只追加，含有效区间）与 `ods_current`（MERGE upsert 当前态）；同一源变更序列重放后：①EDW 可查任意历史时点（🔧 `WHERE ord_date` 区间过滤+valid 区间），②ODS 只答「现在是什么」（主键 upsert 后旧值消失，需自带日志表才不丢史——印证 16.2「更新代价=另留日志」）。结论（🔧 本机）：互补结构成立的关键是**别拿 ODS 当历史库、别拿 EDW 扛 24×7 点查**——Inmon 两章（14/16）的分工纪律在 5 行 SQL 里可见。

---

## 官方目录精读札记（✅ 小节与页码取自 Wiley Contents PDF）

**第 15 章 成本论证与 ROI（p.413–428）**

- **Copying the Competition**（应对竞争，p.413）— 恐惧驱动立项的讽刺开篇
- **The Macro Level of Cost-Justification**（宏观上的成本论证，p.414）— 信息获取总成本 vs 建仓 TCO
- **A Micro Level Cost-Justification**（微观上的成本论证，p.415）— 逐主题自证回报
- **Information from the Legacy Environment**（来自遗留环境的信息，p.418）— 旧环境取数真账
- **The Cost of New Information**（新信息的成本，p.419）/ **Gathering Information with a Data Warehouse**（用数据仓库收集信息，p.419）/ **Comparing the Costs**（成本比较，p.420）
- **Building the Data Warehouse**（建立数据仓库，p.420）/ **A Complete Picture**（完整的情况图，p.421）
- **Information Frustration**（得到数据的障碍，p.422）— 取不到数的决策损耗入账
- **The Time Value of Data**（数据的时间价值，p.422）/ **The Speed of Information**（信息速度，p.423）
- **Integrated Information**（集成的信息，p.424）/ **The Value of Historical Data**（历史数据的价值，p.425）/ **Historical Data and CRM**（历史数据和客户关系模型，p.426）
- **Summary**（小结，p.426）

**第 16 章 ODS（p.429–442）**

- **Complementary Structures**（互补的结构，p.430）— ODS 管现在、EDW 管历史
- **Updates in the ODS**（ODS 中的更新，p.430）— 可更新的特权与代价
- **Historical Data and the ODS**（历史数据与 ODS，p.431）— 要史去 EDW
- **Profile Records**（概要记录，p.432）— 当前横截面在 ODS 侧
- **Different Classes of ODS**（不同种类的 ODS，p.434）— 按集成度×刷新率分档
- **Database Design — A Hybrid Approach**（混合式数据库设计，p.435）/ **Drawn to Proportion**（按比例画图，p.436）— 冗余度=访问比
- **Transaction Integrity in the ODS**（ODS 中的事务集成，p.437）— 当前值强一致
- **Time Slicing the ODS Day**（对 ODS 处理日进行分片，p.438）— 日内多批的时效妥协
- **Multiple ODS**（多个 ODS，p.439）/ **ODS and the Web Environment**（ODS 和网络环境，p.439）/ **An Example of an ODS**（ODS 的一个例子，p.440）
- **Summary**（小结，p.441）

## ROI 论证模板（把本章压成一页 ⚠️ 重建自两章骨架）

1. 基线：旧环境取数成本（工时+争议+放弃的分析）；
2. 对照：建仓 TCO 全账（第 12 章账法）；
3. 增益：时间价值曲线（信息速度差×决策频度）+ 历史资产增值（CRM 曲线）；
4. 拆单：逐主题微观回报承诺（第 9 章每车间自证）；
5. 复审：使用监控器数据回填（第 12 章裁判）——闭环。

## 本章论证链复原（⚠️ 依 ✅ 小节序列重建的推理骨架）

1. 立项前先算账：「对手有我也要有」不算论证 → 宏观总账 + 微观逐主题账（p.413–417 ✅）；
2. 账本要补记表外项：旧环境取不到的分析（信息挫败）与时间价值/历史资产是隐损益（p.418–426 ✅）；
3. 时效需求会逼 EDW 破戒（非易失/批窗口）→ 用 ODS 做泄压阀，现态/历史立双契约（p.430 ✅）；
4. ODS 特权（可更新）必附代价（日志兜底、混合设计、事务一致、时间分片）（p.430–441 ✅）。
两章一钱一闸：第 15 章保证工厂拿得到预算，第 16 章保证工厂不被时效需求改造成操作库。

## 阅读自测（合卷回答）

1. 「微观论证」为什么是工厂模式的生命线？（预算流依赖车间自证）
2. ODS 允许更新，其"历史"靠什么兜底？与 EDW 时戳覆盖的本质差？（日志外置 vs 内建）
3. 🔧 双表实验里 upsert 丢史演示对应本章哪节警告？
4. 时间分片装载在 CDC 时代还剩什么形态？（微批间隔/水位线 ⚠️）
5. 湖仓「现态物化视图+时间旅行」是否让 ODS 这个独立编制过时？两方各引哪节自证？

---

## 核心概念速览（中英对照）

- **成本论证** — Cost-Justification：立项前的宏/微双层价值证明
- **微观论证** — Micro Level Justification：逐主题自证回报以维持预算流
- **机会成本入账** — Cost of New Information：旧环境取不到的分析计为隐损失
- **数据时间价值** — Time Value of Data：信息价值随新鲜度衰减的定价观
- **历史数据资产** — Value of Historical Data：留存=资产，CRM 曲线是其财务证词
- **操作型数据存储** — ODS：当前值、可更新、短保留的仓库伴侣
- **互补结构** — Complementary Structures：ODS 管现在、EDW 管历史的分工
- **按比例混合设计** — Hybrid, Drawn to Proportion：按访问比定冗余度的 ODS 设计法
- **事务一致当前值** — Transaction Integrity in ODS：跨源当前态的强一致要求
- **时间分片装载** — Time Slicing the Day：日内多批次缩短时效的批处理妥协
- **多 ODS 边界** — Multiple ODS：全局与域级 ODS 的分布同构问题

## 最新演进与工业实践

- **FinOps/数据 ROI 度量（⚠️ 转述）**：第 15 章的制度化后代；云账单归因让「微观成本论证」可按 query/团队粒度做实（[docs.snowflake.com/en/](https://docs.snowflake.com/en/)）。
- **实时化吸收 ODS（⚠️）**：Flink CDC+OLAP（Doris/Doris 类，[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)）与仓内增量物化视图把「当前值层」并入主平台，ODS 作为独立产品名淡出，但其**语义分工**（现态/历史双契约）完整存活 ⚠️。
- **湖仓 medallion 的 silver 层≈ODS 职能**（[../The_Data_Lakehouse/07-数据需要的层次.md](../The_Data_Lakehouse/07-数据需要的层次.md) 的层级论与其对位）；OneData 的 ODS 贴源层命名即该概念的中文制度化（[../大数据之路.md](../大数据之路.md)）。
- **dbt incremental + snapshot 表**在转换层复刻「EDW 时变/ODS 现态」双契约 ⚠️（[getdbt.com](https://www.getdbt.com/) 200）。
- 🔧 **复现入口**：`proto_edw.py` 的 upsert/append 双表实验（DuckDB 1.5.5）。
- **书目实证**：[Wiley 产品页](https://www.wiley.com/en-us/Building+the+Data+Warehouse%2C+4th+Edition-p-9780764599446)、[官方 Contents PDF](https://media.wiley.com/product_data/excerpt/45/07645994/0764599445.pdf)。
