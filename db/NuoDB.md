# NuoDB

NuoDB Dassault Systèmes 分布式弹性 SQL 数据库连续可用 + 动态伸缩 + 云友好被收购后仍在维护云/多云企业应用、高可用

NuoDB 是否开源？

否，NuoDB 不是开源数据库。

- NuoDB 是一个商业闭源（proprietary）的分布式 SQL 数据库，由 Dassault Systèmes（达索系统）拥有和维护。
- 虽然早期（2010s）有过 Community Edition（社区版），限制为最多 3 个 Transaction Engine + 1 个 Storage Manager，但它不是完全开源（源代码不公开在 GitHub 上供自由修改/分发）。
- 2026年现状：核心引擎和产品仍是闭源商业软件，没有转为 Apache/MIT 等开源许可。GitHub 上 nuodb 组织只有辅助工具（如 metrics collector、Docker compose、迁移工具等），没有核心数据库源码。
- 它被归类为企业级分布式 SQL 数据库，强调云原生、弹性扩展和连续可用性，主要面向付费企业用户（按使用付费或订阅模式）。

官方网址：
- 主页：https://www.3ds.com/nuodb-distributed-sql-database （Dassault Systèmes 下的 NuoDB 页面）
- 文档：https://doc.nuodb.com/nuodb/latest/ （最新 release notes 和功能介绍）
- GitHub 组织（辅助项目）：https://github.com/nuodb （无核心代码）
- 控制平面文档（Control Plane）：https://nuodb.github.io/nuodb-cp-docs （部署相关）

如果你想用开源替代品，推荐 CockroachDB、YugabyteDB 或 TiDB（这些都是开源的分布式 SQL 数据库，支持 PostgreSQL/MySQL 协议）。需要我帮你对比 NuoDB 和这些开源选项的差异吗？

NuoDB 是美国的数据库公司。

- 起源国家：美国（United States）。
- 成立时间：2008 年开始开发（原名 NimbusDB），2010 年正式注册成立（incorporated）。
- 总部所在地：马萨诸塞州剑桥市（Cambridge, Massachusetts），位于波士顿大都市区。这是其从创立到被收购前的核心总部位置（地址曾包括 CambridgePark Drive 和 Wyman St 等）。
- 创始人：Barry S. Morris 和 Jim Starkey（两位都是美国数据库领域的资深人士，Starkey 有 DEC、Interbase、MySQL 等背景）。
- 当前状态：2020 年 11 月被法国公司 Dassault Systèmes（达索系统，总部在法国 Velizy-Villacoublay）完全收购（之前已持有部分股权）。收购后，NuoDB 作为 Dassault Systèmes 的子公司/技术资产继续运营，但其技术根基和早期发展完全在美国。

简单说：NuoDB 起源于美国（硅谷之外的东海岸波士顿科技生态），是典型的美国初创数据库公司，后来被法国企业收购。

如果你对 NuoDB 的技术细节（如其独特弹性架构）或与 Dassault Systèmes 的整合感兴趣，可以继续问！
