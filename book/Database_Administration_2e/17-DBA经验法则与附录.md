# 17 DBA 经验法则与附录（Chapter 24: DBA Rules of Thumb，pp.735–752；Appendix A–E，pp.753–792；Bibliography p.793 / Glossary p.819 / Index p.853）

> 对应原书第 24 章与全部附录 ✅（12 条规则与小节名、附录 A–E 及其二级小节实抓自 InformIT 官方 TOC；多章归拢，映射表见
> [00-总览与阅读地图.md](00-总览与阅读地图.md)）。正文为主题级精读重构；厂商名录为 2012 口径 ⚠️ 历史文档转述。

## 一、第 24 章：DBA 经验法则（全书终章，12 条 ✅ 逐条实录）

TOC 的 12 个小节即 12 条法则 ✅，每条后注其在全书的展开位置（页码均实抓）：

1. **Write Down Everything（p.735）**——留痕是审计、交接、复盘的原料；展开于第 2 章规程（p.92）、第 7 章变更（p.243）。
2. **Keep Everything（p.736）**——历史版本/旧数据/日志能不删就不删；与第 15 章保留归档（p.498）、第 13 章时态（p.444）同构。
3. **Automate!（p.737）**——重复第三次即写脚本/买工具；第 23 章工具品类（p.699）是其采购面。
4. **Share Your Knowledge（p.739）**——文档+内训+结对，拒绝知识单点；第 2 章 DBMS Education（p.103）的组织面。
5. **Analyze, Simplify, and Focus（p.741）**——先量化的再动刀，砍掉不增值的动作；第 9–12 章性能方法论的格言版。
6. **Don't Panic!（p.742）**——事故按预案走，预案靠演练（第 16/17 章 p.516/p.563 ✅）。
7. **Measure Twice, Cut Once（p.743）**——不可逆操作前二次核量；容量与变更的通用纪律（p.608 规划节 ⚠️ 呼应推定）。
8. **Understand the Business, Not Just the Technology（p.743）**——DBA 的判断力来自业务账（宕机成本 p.271、合规语言 p.483 均是业务件）。
9. **Don't Become a Hermit（p.745）**——走出机房：与开发/审计/业务共建（第 6 章评审 p.227、第 15 章协作 p.486）。
10. **Use All of the Resources at Your Disposal（p.745）**——厂商支持/用户组/社区/文献都是武器（附录 B/C/D 即资源地图 ✅）。
11. **Keep Up-to-Date（p.746）**——版本、补丁、知识三条时间线都不许脱期（第 2 章升级 p.82、第 14 章补丁 p.480）。
12. **Invest in Yourself（p.747）**——认证、社群、写作（第 1 章 p.56 的职业闭环）。
- Summary p.748；**Final Exam（p.748）**✅：全书收官的综合自测，教材规格的最后一块 ⚠️ 结构实抓。
- 解读（⚠️ 推定）：12 条中**技术含量最高的是「Automate!」，含金量最高的是「Understand the Business」**——
  前者决定你的时间去向，后者决定你的谈判筹码；这正是 2026 年 DBRE/平台工程叙事里保留的两项 ⚠️ 对照结论。

## 二、附录 A：数据库基础（Appendix A: Database Fundamentals，p.753）

- What Is a Database?（p.753）/ Why Use a DBMS?（p.754）✅：面向新入行的地基两页——文件系统的痛点清单
  （冗余、一致性、并发、恢复缺位）与 DBMS 承诺的对照 ⚠️ 重构；Summary p.759。
- 对本 repo 读者的替换读物：这两页的所有论点在 [../数据库系统概念6/00-总览与阅读地图.md](../数据库系统概念6/00-总览与阅读地图.md) 第 1 章有更严格版本 ⚠️ 对照。

## 三、附录 B/C：厂商与工具生态（p.761 / p.769，2012 名录）

- **B The DBMS Vendors（p.761）**✅ 的分级框架至今有分析价值：The Big Three（p.762，2012 口径指 Oracle/IBM DB2/微软 SQL Server ⚠️ 名录以原文为准、
  未直接核字）、Second Tier（p.763，Sybase/PostgreSQL 阵营等 ⚠️ 待核验）、Other Significant Players（p.763）、
  **Open-Source DBMS Offerings（p.764）**、Nonrelational（p.765）/NoSQL Vendors（p.765）、Object-Oriented（p.766）、PC-Based（p.766）。
  八档结构与 2026 现实的错位：Big Three 之一（DB2）收缩、开源三柱（PG/MySQL/MariaDB）上位、NoSQL 并入多模、OO/PC-Based 两档消亡 ⚠️ 对照评述。
- **C DBA Tool Vendors（p.769）**✅：The Major（p.769）/Other（p.770）/Data Modeling Tool Vendors（p.771）/Repository Vendors（p.772）/
  Data Movement and Business Intelligence Vendors（p.773）——分类骨架与第 23 章品类矩阵一致；名录按「历史文档」读，不作现行选型依据 ⚠️。
- 中文替代资源图谱可接 [../数据库系列·总索引.md](../数据库系列·总索引.md) 的分层阅读路线。

## 四、附录 D/E：网络资源与岗位样本（p.775 / p.785）

- **D DBA Web Resources（p.775）**✅：Usenet Newsgroups（p.775）/Mailing Lists（p.776）/Websites, Blogs, and Portals（p.778）——
  三档即 2012 的知识流通拓扑；其现代对应物：新闻组→Stack Overflow/引擎官方论坛，邮件列表→Slack/Discord/邮件订阅，博客门户→云厂商技术博客与 ⚠️ 趋势转述。
- **E Sample DBA Job Posting（p.785）**✅：一页真实 JD（Job Posting p.785）供第 1 章「Evaluating a DBA Job Offer（p.14）」做反向核查——
  职责/资格/薪项结构 ⚠️ 重构；JD 读法在 2026 仍成立：**岗位要求是组织 DBA 成熟度的自白书** ⚠️ 结论推定。

## 五、Bibliography（p.793）/ Glossary（p.819）/ Index（p.853）✅

- Bibliography 按主题分节（TOC 实抓 ✅）：Database Management and Database Systems（793）、Data Administration/Data Modeling/Database Design（799）、
  Database Security, Protection, and Compliance（802）、Data Warehousing（804）、SQL（805）、Object Orientation（807）、Operating Systems（807）、
  Related Topics（808），再到分引擎书目：DB2（812）、IMS（813）、MySQL（813）、Oracle（814）、SQL Server（815）、Sybase（816）、Other（817）——
  **书目结构本身就是作者知识版图的 X 光片**：管理学科居中、引擎为用，IMS 单列暴露大型机血统 ⚠️ 结构实抓/评述推定。
- Glossary/Index 为检部件，不另作笔记；Glossary 术语已在各章「核心概念速览」覆盖 ⚠️ 覆盖度不承诺逐条对齐。

## 6. 精读要点备忘（重构）

1. 终章 17 页 ✅ 没有一条新技术——全书压轴是**职业素养清单**，与第 1 章「管理学科」首尾咬合：这是本书与所有「XX 天 DBA 实战」的根本分界 ⚠️ 推定。
2. 附录 B/C/D 的「名录会过期、**分类框架不过期**」读法，可推广到一切带附录的技术书 ⚠️ 方法论结论。
3. Final Exam（p.748）建议真做：它跨 24 章出题，等于全书的知识点连通性测试 ⚠️ 结构实抓/用法推定。

## 7. 十二条自测评分表（⚠️ 重构；每条三档，自查或团队互评用）

| # | 法则 | 0 分表现 | 1 分表现 | 2 分表现 |
| --- | --- | --- | --- | --- |
| 1 | Write Down Everything | 口口相传 | 有 wiki | 版本化+可审计检索 |
| 2 | Keep Everything | 随手 DROP | 保留脚本 | 历史表+保留政策联动 ⚠️ |
| 3 | Automate! | 手工点鼠标 | 脚本半自动 | 流水线+告警闭环 |
| 4 | Share Your Knowledge | 单点英雄 | 文档齐全 | 轮值+评审+内训制度 |
| 5 | Analyze, Simplify, Focus | 见问题就调 | 先测量后动 | 有优先级账与放弃清单 |
| 6 | Don't Panic! | 事故现搜手册 | 手册存在 | 年度演练验证过手册 |
| 7 | Measure Twice, Cut Once | 直接执行 | 双人复核 | 复核进流程强制点 |
| 8 | Understand the Business | 只懂技术 | 知道系统服务谁 | 能用宕机成本谈判 ⚠️ p.271 联动 |
| 9 | Don't Become a Hermit | 独来独往 | 参会评审 | 跨团队共建流程 |
| 10 | Use All Resources | 孤军 | 会用厂商支持 | 社区/文献/同业网络常备 |
| 11 | Keep Up-to-Date | 版本补丁双脱 | 按季跟进 | 有 EOL 台账与升级日历 |
| 12 | Invest in Yourself | 被动培训 | 认证跟进 | 写作/分享反哺社区 |

- 用法（⚠️ 推定）：对照第 1 章 p.14「评估雇主」——团队均分低的组织，个人分数天花板也低 ⚠️ 结论重构。

## 8. 附录使用法与版本谱系注记

- **A（p.753）**：给新同事的第一小时读物；进阶直读 [../数据库系统概念6/00-总览与阅读地图.md](../数据库系统概念6/00-总览与阅读地图.md)。
- **B/C（p.761/p.769）**：当「分类框架教材」读而非名录读；2026 名录重建：关系双强+PG、开源多模、云数仓与湖仓四层 ⚠️ 转述，
  深读入口本 repo 均有：[../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)、
  [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)、
  [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)（存在已验证）。
- **D（p.775）**：三档知识渠道的史前史；当代渠道权重见 [16] 号文件演进节 ⚠️ 内部承接。
- **E（p.785）**：配合 [01-DBA是什么.md](01-DBA是什么.md) 的 p.14 小节做双向评估练习 ⚠️ 用法推定。
- **版本谱系**：1e（2007，Michael W. Rees 署名 ⚠️ 待核验）→ **2e（2012-10-11，Craig S. Mullins，本笔记对象 ✅）**→ 3e（2021 前后，⚠️ 待核验）；
  2e 相对 1e 为**换作者重写**，引用时严禁混用两版章号——本目录全部页码仅对 2e 有效 ✅。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 经验法则 | Rules of Thumb | 无需形式化即可执行的职业判断集 |
| 事事留痕 | Write Down Everything | 一切操作/决定成文可回放 |
| 保留一切 | Keep Everything | 删除是例外，保留是默认 ⚠️ 与合规删除权并读 |
| 自动化 | Automate! | 重复劳动的脚本化/工具化 |
| 知识共享 | Share Your Knowledge | 反单点化的组织免疫机制 |
| 业务理解 | Understand the Business | 技术决策以业务账定价 |
| 资源利用 | Use All Resources | 厂商支持/社区/文献的武装自己 |
| DBMS 厂商分级 | The Big Three/Second Tier | 2012 市场份额式的厂商分类法 ⚠️ 历史口径 |
| 开源 DBMS | Open-Source DBMS Offerings | 附录 B 单列的开源阵营档 |
| NoSQL 厂商 | NoSQL DBMS Vendors | 2012 热潮名录档 ⚠️ 历史口径 |
| 岗位样本 | Sample DBA Job Posting | 反向评估雇主的 JD 模板 |
| 主题书目 | Bibliography by Topic | 按 14 个主题域组织的全书书单 ⚠️ 分节实抓 |

## 最新演进与工业实践

1. **12 法则的当代映射**：Write/Keep/Automate 汇入 GitOps 与可观测性（对接 [05](05-设计评审与变更管理.md)/[16](16-元数据管理与DBA工具.md) 号文件所列工具链）；
   Invest in Yourself/Keep Up-to-Date 汇入云认证与引擎年报节奏；**唯「Don't Panic!」的制度化形态变了**——从个人素养变成
   事故管理（incident management）职能与值班轮转，见 [../Database_Reliability_Engineering/00-总览与阅读地图.md](../Database_Reliability_Engineering/00-总览与阅读地图.md)（存在已验证）⚠️ 对照。
2. **附录 B 名录的 2024–2026 重排**：关系引擎「Big Three」收缩为 Oracle/微软两强加 PostgreSQL 事实第三 ⚠️ 转述（市场份额无单一权威口径，标存疑）；
   开源侧 MariaDB/PG 文档为权威入口（https://www.postgresql.org/docs/current/ 本目录引用页均 ✅200）；NoSQL 档在 2026 的深读
   对口本 repo：[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)、
   [../从Lucene到Elasticsearch.md](../从Lucene到Elasticsearch.md)、[../cassandra实战.md](../cassandra实战.md)（均存在已验证；辨析：目录版 [#89](../Expert_Apache_Cassandra_Administration/00-总览与阅读地图.md)/[#98](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md) 已落盘，见 00 义务登记闭环）。
3. **经典论文锚点**：附录 B 提到的关系/DBMS 史可用红宝书线补时间轴——[../Readings_in_Database_Systems/00-总览与阅读地图.md](../Readings_in_Database_Systems/00-总览与阅读地图.md) 与论文索引
   [../../db/db.md](../../db/db.md)；开源阵营史前史可读 INGRES 设计论文（ACM TODS 1976，DOI `10.1145/320473.320476` ✅ Crossref 200）⚠️ 史料转述。
4. **JD 的反向核查升级**：2026 年读 JD 新增三问——平台工程还是值班文化？SLO 归谁？schema 变更走什么流水线？（对应
   [01-DBA是什么.md](01-DBA是什么.md) 的岗位演进节闭环）⚠️ 实践转述。
