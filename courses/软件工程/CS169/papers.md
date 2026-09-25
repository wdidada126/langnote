# CS169 参考文献与开源应用（骨架）

> 关联讲次对应 README/outline 的 L1–L14。这门课的"论文"一半来自敏捷/DevOps 实证研究，一半来自工业系统论文。

## 经典论文 / 文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Manifesto for Agile Software Development（Beck 等 17 人） | 2001 | 敏捷四条价值观与十二条原则，全课的方法论起点 | L1–L2 |
| Extreme Programming Explained: Embrace Change (Kent Beck) [专著] | 2000 | 把价值观落到实践：结对、TDD、小.release、持续集成 | L2, L6–L7 |
| Get Ready for Agile Methods, with Care (Boehm & Turner, IEEE Computer) | 2002 | 五维度对照：何时该敏捷、何时该计划驱动，破除教条 | L1–L2, L8 |
| Agile and Adaptive Software Development: A Review of Research in Extreme Programming (Cockburn & Williams) | 2000 | 系统整理 XP 的实证证据与未证实之处 | L7 |
| Independent and Pair Programmers: When Is a Pair Better Than Two? (Williams & Kerner, SIGCSE) | 2000 | 结对设计的产出质量更高、耗时略长但缺陷更少 | L7 |
| A Controlled Experiment of Test-Driven Development (George & Williams, IEEE Software) | 2004 | TDD 显著降低功能开发缺陷密度，且总工时相近 | L6, L9 |
| Analysis of the Test-Driven Development Approach (Nagappan et al., IEEE TSE) | 2008 | 微软产品实证：缺陷率下降 40–90%，交付时间略增 | L6, L9 |
| 12-Factor App (Adam Wiggins / Heroku) [在线文献] | 2011 | SaaS 应用构建与发布的十二项工程约束，云平台时代基线 | L4, L9 |
| MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, OSDI) | 2004 | 以简单编程模型换取可扩展性与容错 | L11–L12 |
| Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al.) | 2007 | 一致性/可用性权衡与最终一致实践，NoSQL 时代的源头 | L12 |
| Architecture Strategies for Catching the Long Tail (Chong & Carraro, Microsoft) | 2006 | SaaS 多租户三种隔离策略的成本/弹性权衡 | L14 |
| Continuous Delivery: Reliable Software Releases (Humble & Farley) [专著] | 2010 | 把"随时可发布"变成工程能力：流水线 + 环境即代码 | L9 |
| Expectations, Challenges, and Industry Practices for Modern Code Review (Bacchelli & Bird) | 2013 | 现代代码审查的动机、瓶颈与改进清单 | L7 |
| Refactoring: Improving the Design of Existing Code (Fowler) [专著] | 1999/2018 | 坏味道目录与可执行重构手法，支撑 L10 的术语体系 | L10 |
| OWASP Top 10（Web 应用安全风险清单） | 2010–2021 各版 | 注入/失效认证/XSS/越权的分类学与防护要点 | L13 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| What is DevOps? A Systematic Literature Review and Classification (Smite 等) | 2021（扩展版持续更新） | 把 DevOps 定义为 CALRE 五能力，给敏捷之外提供可测量框架 | L2, L9 |
| Productivity Assessment of Neural Code Completion (Ziegler et al., FSE) | 2022 | 用遥测与接受率量化 AI 补全对开发速度的真实影响 | L5–L7 |
| DevOps and Software Engineering Research Roadmap (Fagerholm 等) | 2022 | 给出流水线/实践/组织三层的研究问题清单 | L9, L14 |
| Do Users Write More Insecure Code with AI Assistants? (Perry et al., NeurIPS) | 2023 | 受控实验显示 AI 助手会拉高安全敏感任务的不安全代码比例 | L13 |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al., ICLR) | 2024 | 真实 issue + CI 测试判定，成为"软件工程能力"的新基准 | L6, L9 |
| Large Language Models for Software Engineering: A Systematic Literature Review (Hou et al., TOSEM) | 2024 | 综述 LLM 在评审/测试/修复/文档上的证据与缺口 | L7, L10 |
| 云端 FinOps 与可持续性研究系列（能耗/成本感知的调度与部署） | 2021–2024 | 把成本与碳排变成一等指标，纳入发布决策 | L11, L14 |
| Platform Engineering / Internal Developer Platform 实践与综述 | 2022–2025 | 以"黄金路径"降低认知负担，CI/CD 组织形态的最新演化 | L4, L9 |
| Continuous AI/LLM-assisted Code Review 与门禁工具评估 | 2023–2025 | 自动评审意见的有用性/信噪比量化，人机协同审查流程 | L7 |
| Site Reliability 与 SLO 驱动的变更管理最新实证（事故复盘、错误预算） | 2021–2025 | 用错误预算把"可靠性 vs 速度"变成可协商的资源分配 | L11, L14 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 敏捷看板与 GitHub Flow (L3) | GitLab、GitHub Actions、Project boards | 短分支、MR/PR 门禁、看板与里程碑一体化 |
| 12-Factor 与云部署 (L4) | Fly.io、Render、Dokku、Caprover、Docker/K8s | Procfile/镜像化构建、配置注入、无状态进程 |
| Rails 约定与 MVC (L5) | Rails、JHipster、Laravel、Django | 脚手架、迁移、资源路由与"约定优于配置" |
| TDD 与测试金字塔 (L6) | RSpec、Minitest、Cypress/Playwright、pytest | 单元/请求/端到端分层与并行执行 |
| 结对与代码审查 (L7) | Gerrit、Reviewable、Codacy、Danger、CodeRabbit | 审查门禁、静态检查前置、机器人评审建议 |
| 估点与流动度量 (L8) | Linear、Jira + 燃尽/CFD 插件、GitDevil/Axis 类度量工具 | 速度、周期时间与 WIP 限制的可视化 |
| CI/CD 与灰度发布 (L9) | GitHub Actions、GitLab CI、Argo Rollouts、Flagger、Sentry | 流水线、金丝雀/蓝绿发布、错误率自动回滚 |
| 重构与设计模式 (L10) | RuboCop、Brakeman、SonarQube、Refactoring.nvim | 坏味道检测、风格与静态分析纳入流水线 |
| 性能与后台任务 (L11) | Sidekiq、Resque、Solid Queue、Redis、Prometheus + Grafana | 队列削峰、指标采集、慢查询与火焰图分析 |
| NoSQL 与分片 (L12) | MongoDB、Cassandra、ScyllaDB、DynamoDB（LocalStack 模拟） | 文档/宽列模型、分片键选择与一致性配置 |
| 安全与隐私 (L13) | Devise、OmniAuth、Doorkeeper、Brakeman、OWASP ZAP、Certbot | 认证/授权中间件、依赖与静态安全扫描 |
| 运营指标与 A/B (L14) | Mixpanel/Amplitude 开源替代（PostHog）、GrowthBook、Statsig 类 | 事件流分析、实验分流与统计显著性判定 |
| 多租户与成本 (L14) | PostgreSQL RLS、Citus、Kubernetes 配额/命名空间 | 数据隔离与噪声邻居治理、成本分摊 |
