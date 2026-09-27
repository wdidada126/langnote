# 08 · 第 9 章 Migration to the Architected Environment + 第 10 章 The Data Warehouse and the Web

> 两章同属「怎么走到目标环境 + 新环境里的新数据源」主题，合并一文件（映射见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。章题小节题 ✅ 官方 Contents PDF；正文为**精读重构**。英文原书约 269–304 页。

## A 部分 · 第 9 章：迁移到架构化环境

### 9.1 为什么是「迁移」而不是「新建」

前两章给了目标（架构化环境+仓库分层），本章回答**从蜘蛛网到目标态的工程路径**。Inmon 反复强调：没人能推倒重建企业数据环境，只能**逐主题增量迁移**——这句话是他对「big bang 项目」的终身宣战，也是他与「敏捷重写」派（金氏迭代的通俗版）差异最小的地方：都反对大爆炸，分歧在增量单位是**主题域**（Inmon）还是**业务过程集市**（Kimball，[../数据仓库工具箱3.md](../数据仓库工具箱3.md) 实施章）。

### 9.2 一种迁移方案（✅ A Migration Plan，中译 9.1「一种迁移方案」）

官方小节即路线图 ⚠️（各步展开依 Inmon 通说重建）：

1. 选**高价值低风险**的先行主题（不是最容易的，也不是最想要的）；
2. 建最小架构化骨架：staging+一个主题的原子层+一份元数据——**地基按全书标准建，哪怕只住一间房**；
3. 以原子层派生首个集市/报表，兑现「从数据到信息」；
4. 反馈循环（✅ The Feedback Loop）：用首轮运营的度量（查询命中率、装载时长、口径争议数）校准下一主题的选择与模型；
5. 逐主题滚雪球，同时**拆蜘蛛网**：每迁入一个主题，即下线该主题的存量抽取管线（下线动作要写进项目计划，否则网拆不掉 ⚠️ 通说）。

### 9.3 战略考量与方法论（✅ Strategic Considerations / Methodology and Migration / A Data-Driven Development Methodology / Data-Driven Methodology / System Development Life Cycles / A Philosophical Observation）

- **数据驱动开发（DDDM）**：先定数据资产与口径，再排应用需求——对「需求拉动一切」的 SDLC 传统的正面挑衅（⚠️ 通说：其 DDDM 文章 1990s 末已发表，本章收编）。
- **SDLC 定位**：Inmon 不反对 SDLC，反对把它当**唯一**生命周期：仓库环境是运营态（接第 1 章 monitoring），项目只是环境增长的脉冲。
- **智者观点（A Philosophical Observation，中译「智者观点」✅）**：迁移成败的第一变量是管理层是否接受「仓库是环境不是项目」；把仓库当项目立项的企业，验收即腐烂开始。
- 2026 对位：这就是 data platform roadmap/平台工程叙事 ⚠️；「环境不是项目」≈ 平台团队常设化、数据产品持续运营。

## B 部分 · 第 10 章：数据仓库和 Web

### 10.1 2005 年的新客人

第 10 章（英文原书 289 页起，含一节支持电子商务环境）处理当时最烫的新事实：**Web 既是需求端也是数据源**。Inmon 的立场延续第 1 章：Web 不会改变仓库的架构，只会改变装载清单。

### 10.2 四个论题（✅ 小节题全实据）

- **Supporting the eBusiness Environment（✅）**：网站是新的「用户」——个性化推荐、点击计费对账等要求仓库**反向供数**（回灌，接第 3 章间接访问三案例之「零售个性化系统」）。⚠️ 对位 2026：reverse ETL 与 feature store 的 2005 雏形。
- **Moving Data from the Web to the Data Warehouse（✅）**：clickstream/服务器日志入仓：粒度=页面事件（比业务事件更细、量级更大 ⚠️）；Inmon 提醒日志的「粒度陷阱」：一次会话可展开数万行，入仓前先定「业务上有意义的最小事件」——第 4 章粒度论在 Web 数据上的复演。
- **Moving Data from the Data Warehouse to the Web（✅）**：仓库算好的客户分群/风险分回写网站；「非易失」纪律下回写只动派生存储，绝不动仓库本体。
- **Web Support（✅）+ 本章与第 14 章 14.7「Web 电子商务接口（粒度管理器）」互见**：高频在线查询走**概要记录/粒度管理器**缓冲，不直穿原子层——现代特征服务（低延迟读层）的架构学祖先 ⚠️。

### 10.3 三方方法论对 Web 数据的代际差

| | Inmon（本章） | Kimball 3 版 | 2026 湖仓 |
|---|---|---|---|
| 点击流 | 原子事件入 EDW，粒度受控 | 会话/页面事件事实表，经典「多事实表/累积快照」用例 | 落 lake raw 层，schema-on-read 后按需建模 |
| 分歧 | 「先定粒度再谈分析」 | 「先出一个会话分析集市」 | 「先存下来」——Inmon 最反对的姿势 |

对照读物：[../The_Data_Lakehouse/03-结构化文本与物联网数据.md](../The_Data_Lakehouse/03-结构化文本与物联网数据.md)（Inmon 本人在湖仓时代对此的重述）。

## C · 🔧 最小演示（DuckDB，可复现）

「Web 事件入仓的粒度陷阱」：生成会话→事件两层数据（1 会话=20 事件），分别以**会话粒度**与**事件粒度**装载同一张原子表，比较：①集市 sum 对账（🔧 两种粒度下 sum(page_view) 与 sum(event) 需各自定义度量才相等——粒度声明缺失即口径事故的温床）；②行数膨胀 20 倍的存储/扫描差异（列存下事件表压缩后膨胀远低于 20×，🔧 DuckDB/Parquet 实测可复现）。结论：Inmon 的「入仓先声明业务最小事件」在 2026 依然零成本可执行。

---

## 官方目录精读札记（✅ 小节与页码取自 Wiley Contents PDF）

**第 9 章 迁移（p.269–288）**

- **A Migration Plan**（一种迁移方案，p.270）— 先行主题→最小骨架→首集市→滚雪球的路线图
- **The Feedback Loop**（反馈循环，p.278）— 运营度量反哺下一主题选择
- **Strategic Considerations**（策略方面的考虑，p.280）— 预算/政治/时机三维
- **Methodology and Migration**（方法和迁移，p.283）/ **A Data-Driven Development Methodology**（数据驱动的开发方法，p.283）
- **Data-Driven Methodology**（概念，p.286）— 数据资产先行于需求排期
- **System Development Life Cycles**（系统开发生命周期，p.286）— SDLC 是脉冲不是常态
- **A Philosophical Observation**（智者观点，p.286）— 「环境不是项目」的定调句
- **Summary**（小结，p.287）

**第 10 章 Web（p.289–304）**

- （章首无领起小节，正文自 p.289 起，第一个实义小节即：）
- **Supporting the eBusiness Environment**（支持电子商务环境，p.299）— 网站作为新用户（回灌）
- **Moving Data from the Web to the Data Warehouse**（从Web移数据到仓库，p.300）— 点击流粒度陷阱
- **Moving Data from the Data Warehouse to the Web**（从仓库移数据到Web，p.301）— 分群/评分回写
- **Web Support**（对Web的支持，p.302）— 在线读与粒度管理器衔接
- **Summary**（小结，p.302）

## 迁移七步口诀（⚠️ 依 9.1 小节序列重建的通说口诀）

选域（高价值低风险）→ 立架（staging+原子+元数据三件套）→ 出样（首集市兑现）→ 度量（命中率/时长/争议数）→ 校准（反馈调下一域）→ 拆网（迁一域拆一丛管线）→ 循环。

- 每步都必须能独立回答 CFO 之问（接第 15 章微观成本论证）——**工厂是一间车间一间车间盖起来的**，这是 Inmon 对「大爆炸 vs 敏捷」的第三条路 ⚠️ 立场表述。

## 原书口径 → 2026 话语对位速查

| 原书 | 2026（⚠️ 转述） |
|---|---|
| 迁移方案 | data platform roadmap / 洋葱皮渐进替换 |
| 数据驱动开发 DDDM | 数据产品规划、domain ownership 先于用例 |
| 环境非项目 | 平台工程常设团队 |
| 点击流入仓 | 事件采集治理（Snowplow 类）+ raw 层 |
| 回灌 Web | reverse ETL / feature store |
| 在线读仓库 | 物化视图/缓存层/聚合服务 |

## 阅读自测（合卷回答）

1. Inmon 与 Kimball 的增量单位差（主题域 vs 业务过程集市）在第 9 章哪一节最吃紧？（先行主题选择）
2. 为什么「拆网动作」必须写进计划？不写会发生什么可观察症状？
3. 🔧 会话粒度 vs 事件粒度装载：sum 对账在什么定义下才相等？（度量随行/列变）
4. 「SDLC 是脉冲不是常态」与软件工程界 DevOps「持续即常态」冲突吗？对象差在哪？
5. 2005 年 Web 章为何没有「网站是最大数据消费者」的担忧？今天该补哪三问 ⚠️ 立场练习。

---

## 核心概念速览（中英对照）

- **增量迁移** — Migration to the Architected Environment：逐主题把蜘蛛网搬进架构化环境
- **先行主题选择** — Pilot Subject Area：高价值×低风险的启动域
- **最小骨架** — Minimal Architected Skeleton：staging+单主题原子层+元数据的合规地基
- **反馈循环** — Feedback Loop：以运营度量校准迁移节奏的方法
- **拆网动作** — Decommissioning Extracts：迁一主题、下线对应存量抽取管线
- **数据驱动开发** — Data-Driven Development Methodology：数据资产先行的开发观
- **环境非项目** — Environment, Not Project：仓库是常设运营态，项目是脉冲
- **点击流入仓** — Web-to-Warehouse Data：会话/事件日志的粒度受控装载
- **回灌网站** — Warehouse-to-Web Data：分群/评分等派生结果写回在线系统
- **粒度管理器** — Granularity Manager：在线高频读与原子层之间的缓冲机制

## 最新演进与工业实践

- **Reverse ETL 产业化（⚠️ 转述）**：Hightouch 等把「仓库→Web/CRM」做成订阅产品；Inmon 14.7+10.2 的架构位 2026 有独立赛道名。
- **行为数据建模主流化**：Snowplow 类事件治理=「入仓前定粒度」的现代工具化 ⚠️；湖仓侧「先存后模」与本章立场的拉锯见 [../The_Data_Lakehouse/02-数据类型与数据抽象.md](../The_Data_Lakehouse/02-数据类型与数据抽象.md)。
- **平台工程叙事（⚠️）**：「数据平台是环境不是项目」已是平台团队的组织学共识——第 9 章论点的制度化迟到二十年。
- **特征平台承接粒度管理器**：离线/在线双存储+低延迟读层，即「概要记录缓冲原子层」的 ML 版（⚠️ 转述）。
- 🔧 **复现**：上文点击流粒度实验脚本模式（会话×事件两层装载+压缩对比）可与 `proto_edw.py` 并跑，DuckDB 1.5.5。
- **书目实证**：[Wiley 产品页](https://www.wiley.com/en-us/Building+the+Data+Warehouse%2C+4th+Edition-p-9780764599446)、[官方 Contents PDF](https://media.wiley.com/product_data/excerpt/45/07645994/0764599445.pdf)。
