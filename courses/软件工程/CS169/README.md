# UCB CS169: Software Engineering 软件工程（Agile SaaS）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | UCB CS169: Software Engineering（敏捷开发与 SaaS 工程实践） |
| 学校 | University of California, Berkeley |
| 主讲 | Armando Fox、David Patterson（课程创设者；edX 版由 Armando Fox 主讲） |
| 教材 | Software as a Service: Web Application Development with Ruby on Rails（Najmi Zafar & Ian Sobel 编写的课程教材草稿，saasbook.info 公开） |
| csdiy 路径 | https://csdiy.wiki/软件工程/CS169/ （页面更新 2022-10-09） |
| 最新期次 | edX「Agile SaaS Development」（CS169 全资料开源版，滚动自定进度）；课程官网 saasbook.info/courses 提供当期 syllabus |
| 先修/语言/难度 | 先修无硬性要求（建议有 CS61B 级别编程经验）；语言 Ruby/JavaScript；难度 🌟🌟🌟🌟；预计学时 100 小时 |
| 状态 | 骨架 |

## 为什么学

- 与"plan & document"式传统软工课不同：这门课**只教今天真正在用的敏捷开发（Agile Development）模式**，并以云平台交付"软件即服务（SaaS）"为唯一主线。
- 全链路实操：从 Ruby/Rails 编码、TDD 与结对，到 CI/CD、性能与可扩展性、NoSQL、后台任务，最后真正把应用部署上线并有真实用户。
- 教材与作业配套极好：以 Rails 逐步搭建一个可运行的 SaaS 应用，练习量大且都有明确验收标准。
- edX 全资料开源（CS169 完整课程自 2012 年起公开），自学可拿到全部视频、作业与评分说明。
- 它是 6.031 的天然后继：6.031 教"一个人写出好代码"，CS169 教"一个团队持续交付可运营的产品"。

## 先修与知识联系

- 先修：一门语言的扎实经验（CS61B/CS106B 级别）；Ruby 语法课内速成，不要求预会 Rails。
- 建议并行/前置：6.031（规格、测试与重构是敏捷实践的技术底座）、CS61B（数据结构，用于性能章节）、必学工具 Git/GitHub/CI 章节。
- 后继与互补：MIT web development / CS142 / Fullstackopen（前端纵深）、6.824/CS149（可扩展性与分布式）、CMU 17-803（用实证方法度量团队与流程有效性）。
- 数据库/网络呼应：ActiveRecord 与索引 → CS186/15-445；缓存与部署 → CS144/topdown、CSAPP IO 与并发。
- 与 6.031 的差别值得记笔记：6.031 关注"代码级正确与可维护"，CS169 关注"流程级可交付与可运营"（估点、迭代、演示、灰度、指标）。

## 最新年份讲义章节目录（按 edX「Agile SaaS Development」/ saasbook 单元顺序整理为 14 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：软件工程在实践中的问题、SaaS 与敏捷宣言 | SaaS Book Ch.1；Agile Manifesto（2001） |
| L2 | 敏捷与 XP 价值观：迭代、增量交付、可持续速度与反馈回路 | SaaS Book Ch.2；Beck《Extreme Programming Explained》选读 |
| L3 | 团队与工具链：Git/GitHub 协作流、Issue 与看板、项目约定 | 必学工具 Git 章 + 课程 GitHub Flow 讲义 |
| L4 | 云端第一次部署：Rails 骨架、Heroku/Fly.io/Railway、Procfile 与 12-Factor | 12-Factor App 全文（在线） |
| L5 | Ruby 与 Rails 核心：MVC、路由、ActiveRecord、迁移与视图 | SaaS Book Ch.4–6 |
| L6 | 测试驱动开发：单元测试、集成测试、fixture 与"测试是设计工具" | SaaS Book Ch.12；George & Williams (2004) |
| L7 | 结对编程与代码审查：驱动/领航、静默期、审查文化与工时影响 | Cockburn & Williams (2000)；Bacchelli & Bird (2013) |
| L8 | 敏捷规划与估点：故事卡片、规划扑克、速度（velocity）与燃尽图 | SaaS Book Ch.3；Cohn《Agile Estimating and Planning》选读 |
| L9 | 持续集成与持续交付：CI 流水线、自动化发布、回滚与特性开关 | SaaS Book Ch.12/Humable & Farley 选读 |
| L10 | 重构与设计模式：坏味道清单、SOLID 在 Rails 里的落地、MVC 的边界 | SaaS Book Ch.7–8；Fowler《Refactoring》选读 |
| L11 | 可扩展性与性能：数据库索引与慢查询、缓存层、后台任务与队列 | SaaS Book Ch.14–15；Dean & Ghemawat (2004) 视角对照 |
| L12 | NoSQL 与数据模型取舍：文档/键值存储、分片、一致性与可用性 | SaaS Book Ch.14；DeCandia et al. Dynamo (2007) |
| L13 | 安全与隐私：认证/授权（OAuth2、会话）、常见 Web 漏洞、数据合规 | SaaS Book Ch.13；OWASP Top 10 |
| L14 | 运营与产品：真实用户监控与指标、A/B 测试、多租户、开源与影响力、结课冲刺 | SaaS Book Ch.9–11 + 课程 capstone 指南 |

> 说明：edX 版把 CS169 内容按教材顺序编为若干模块（每周一个），上表整理为 14 讲，便于逐章写笔记；不同学期会把 L11–L12 合并或把 L14 拆成两讲。原版课程 Heroku 免费额度已于 2022-11 关闭，实践部署可用 Fly.io / Render / Railway 或自建 Docker 替代（笔记中记录迁移经验）。

## 课程资源（摘自 csdiy）

- 课程网站：http://www.saasbook.info/courses
- 课程视频：参见 edX 课程主页（搜索 "Agile SaaS Development"）
- 课程教材：Software as a Service（saasbook.info 提供的课程书籍草稿）
- 课程作业：参见 edx 课程主页（Rails 里程碑作业 + capstone 团队项目）
- 社区资源汇总：PKUFlyingPig/CS169-Software-Engineering
