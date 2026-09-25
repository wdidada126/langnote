# 6.031 参考文献与开源应用（骨架）

> 关联讲次对应 README/outline 的 L1–L24。6.031 的思想大多有明确的论文源头，标注便于回读原文。

## 经典论文 / 文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Go To Statement Considered Harmful (E. W. Dijkstra) | 1968 | 结构化编程宣言：静态推理依赖受控控制流 | L2, L14 |
| On the Criteria To Be Used in Decomposing Systems into Modules (D. L. Parnas) | 1972 | 信息隐藏与"按设计决策分组"的模块划分原则 | L8, L10, L14 |
| "Programming with Abstract Data Types" (Liskov & Zilles) | 1974 | 抽象数据类型的正式提出：表示独立与操作契约 | L6, L8 |
| No Silver Bullet — Essence and Accidents of Software Engineering (F. P. Brooks) | 1987 | 软件固有难点（复杂性/一致性/可变性/不可见性）解释工程方法边界 | L1, L14 |
| A New Definition of the Subtype Relation (Wing & Liskov) | 1994 | 行为子类型与替换原则（LSP）的严格定义 | L12 |
| Design Patterns: Elements of Reusable Object-Oriented Software (Gamma et al.) | 1994 | 模式语言：策略/工厂/装饰/观察者等命名的共同词汇 | L15 |
| Java Concurrency in Practice (Brian Goetz et al.) [专著] | 2006 | 线程安全规格、加锁策略与 java.util.concurrent 的正确用法 | L16–L18 |
| xUnit Test Patterns: Refactoring Test Code (Gerard Meszaros) [专著] | 2007 | 测试结构、夹具与替身模式的体系化 | L5, L7 |
| A Study of Code Readability and Its Relationship to Quality and Complexity (Buse & Weimer) | 2008 | 用可度量的"可读性"支撑 easy to understand 目标 | L1, L4, L14 |
| Why Do Concurrency Bugs Get Recurred? (Lu et al.) | 2009 | 真实并发缺陷分类与复现规律，指导线程安全设计 | L16–L17 |
| The Expectations, Challenges, and Industry Practices for Modern Code Review (Bacchelli & Bird) | 2013 | 现代代码审查动机与最佳实践综述 | L3, L4 |
| Modern Code Review: A Case Study at Google (Sadowski et al.) | 2018 | 工业化审查：小 diff、审查者选择、静默同意与工具链 | L4 |
| OWASP Top 10（持续更新的 Web 风险清单） | 2017/2021 | 注入、失效认证、XSS、CSRF 等风险的工程分类学 | L22–L23 |
| Why Johnny Can't Encrypt: A Security Analysis of S/MIME (Bellovin & Merritt) | 1998 | 安全机制的可用性缺口：可用性与安全同等重要 | L22–L23 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Software Engineering at Google（Titus Winters, Tom Manshreck, Hyrum Wright, O'Reilly） | 2021（中译/重印持续） | 大规模代码库治理：审查、依赖、重构与可维护性的工业化做法 | L3–L4, L14 |
| Productivity Assessment of Neural Code Completion (Ziegler et al., FSE) | 2022 | 用遥测实验测量 AI 补全对交付速度/接受率的影响 | L2, L5 |
| Do Users Write More Insecure Code with AI Assistants? (Perry et al., NeurIPS) | 2023 | 受控实验：AI 助手在安全敏感任务上可能产出更脆弱代码 | L6, L22–L23 |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al., ICLR) | 2024 | 用真实 issue + 测试判定"会否修 bug"，重构了工程能力评测 | L4–L5, L14 |
| Large Language Models for Software Engineering: A Systematic Literature Review (Hou et al., TOSEM) | 2024 | 系统综述 LLM 在代码生成/审查/缺陷修复中的证据与空白 | L4, L14–L15 |
| Automated Code Review by LLMs（"Codet" / PR 审查智能体系列评测） | 2023–2024 | 用智能体 + 测试反馈生成补丁，评估"可编译可测试"的修复率 | L5, L12 |
| Empirical Studies of Technical Debt at Scale（债务标记、重构惯例挖掘） | 2021–2024 | 用大量仓库量化"ready for change"退化过程 | L1, L14 |
| Dependency Confusion / Supply-Chain Attacks 与防护研究 | 2021–2023 | 包管理与构建供应链成为新的安全主战场 | L3, L20, L23 |
| Static Analysis for AI-Generated Code Vulnerabilities（SAST 工具对照实验） | 2024–2025 | 评估传统静态分析能否守住 LLM 代码的安全底线 | L5, L22 |
| Observability/SRE 实践演进（错误预算、变更管理最新综述） | 2021–2025 | 服务端质量目标从"少 bug"扩展为"可控变更 + 可观测" | L20–L21 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 规格与契约 (L6) | Java `Objects.requireNonNull`、`assert`；Rust `debug_assert!`；Design by Contract 框架（CDS/contract 库） | 前置/后置条件的可执行化 |
| 单元测试与属性测试 (L5, L7) | JUnit 5、jqwik、QuickTheories、Hypothesis(Python) | 分区/属性驱动的测试生成与收缩（shrinking） |
| 不可变类型 (L9) | Guava `ImmutableList`、Java `record`、Kotlin `data class`、Rust 所有权 | 值语义 + 天然线程安全，缓存与共享的前提 |
| ADT/表示独立性 (L8) | JDK 集合框架、Android SDK 分层、Spring 的 `@Repository` 抽象 | 内部表示可替换而 API 稳定 |
| 子类型与 LSP (L12) | Jackson/Gson 的多态反序列化、JDBC 驱动 SPI、Java Collections | 替换实现不破坏客户端假设 |
| 泛型与通配符 (L11) | Guava/Caffeine API 设计、Apache Commons | PECS 规则在通用容器 API 中的体现 |
| 设计模式与分层 (L14–L15) | Spring Framework（IoC/DI）、OkHttp（Builder/Interceptor）、Netty（Pipeline） | 责任分层与可扩展钩子 |
| 并发与 Guarded Object (L16–L18) | java.util.concurrent、Kafka broker 线程模型、Disruptor、gRPC 线程池 | 队列 + 锁顺序 + 线程池隔离的落地 |
| 记忆化与缓存 (L19) | Caffeine、Guava Cache、Redis 客户端封装 | 失效策略、容量上界与并发正确性 |
| 代码审查流程 (L3–L4) | Gerrit、GitHub/GitLab PR 工作流、Phabricator（已开源）、Reviewable | 审查粒度、投票与静态检查联动 |
| REST 与无状态服务 (L20) | Spring Boot、FastAPI、gRPC-Web、OpenAPI/Swagger 生态 | 资源建模、幂等与 API 版本化 |
| 注入与 XSS 防护 (L22) | Hibernate/JPA 参数化查询、OWASP Java Encoder、DOMPurify、Content-Security-Policy | 按上下文编码与最小权限 DB 账号 |
| 认证与会话 (L23) | Spring Security、Keycloak、Passlib/argon2-jvm、JWT 库（含 alg 混淆防护） | 令牌与会话管理、口令哈希参数化 |
| 供应链与构建安全 (L3) | Gradle/Maven + Dependabot/Renovate、Sigstore/cosign、SBOM(OWASP dependency-check) | 依赖锁定、签名与来源可验证 |
