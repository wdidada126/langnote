# MIT 6.031: Software Construction 软件构建

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | MIT 6.031 / 6.031J Software Construction（软件构建） |
| 学校 | Massachusetts Institute of Technology（EECS，与 6.005 同源继承） |
| 主讲 | Rob Miller 等课程授课组（课程教材由授课组共同编写，最新届仍由 Rob Miller 主持） |
| 教材 | 课程自写在线教材/notes《Software Construction》（web.mit.edu/6.031/…/notes），无外部纸质教材 |
| csdiy 路径 | https://csdiy.wiki/软件工程/6031/ （页面更新 2024-05-14） |
| 最新期次 | 课程网站 Latest（Spring 2024 及之后的最新一届），另有 Spring 2022 / 2021 / 2016（2016 春起开源全部作业代码框架） |
| 先修/语言/难度 | 先修掌握至少一门编程语言；语言 Java；难度 🌟🌟🌟🌟；预计学时 100 小时 |
| 状态 | 骨架 |

## 为什么学

- 目标极其明确：**写出高质量代码**，课程对"高质量"的三条定义（照录设计者原话，避免翻译曲解）：
  - *Safe from bugs* — 正确性（现在行为对）与防御性（将来行为也对）。
  - *Easy to understand* — 代码要能和未来读者沟通，那个读者可能就是几个月后的你自己。
  - *Ready for change* — 软件必然变化，好设计让改动不必推倒重写。
- 自建教材把细节讲到"如何写注释与函数 Specification、如何设计抽象数据类型、如何做并行编程"，是少数**把 ADT 与规约讲透**的课。
- 作业全部在精心设计的 Java 项目中练习这些模式：4 个编程作业 + 1 个 Project，2016 春季起代码框架完全开源，可离线自做。
- 与算法课互补：6.006/CS61B 教你让程序"快"，6.031 教你让程序"活得久、改得动"。
- 后半程的服务端与 Web 安全章节（SQL 注入、XSS、CSRF、认证与会话）是普通算法课完全没有的工程必备知识。

## 先修与知识联系

- 先修：至少一门语言的系统经验；Java 语法课内以 Java 11/17 速成方式补齐（也可先读 ../MIT6.092 与 CS106B 建立对象概念）。
- 建议先修/并行：CS61B 或 6.006（有真实数据结构可实现，才体会得到抽象与不变式的价值）；CSAPP/CS110（理解并发与内存模型）。
- 后继：CS169（把单人的好代码放大成团队的交付流程）、CMU 17-803（用实证方法度量"什么叫好代码"）、CS186/15-445（服务端与存储工程）、6.1600/6.858（安全纵深）。
- 与课程外知识：Liskov 替换原则、Parnas 信息隐藏是 6.031 全部设计章节的理论地基；JUnit/Gradle/Git 与"必学工具"章节重合。

## 最新年份讲义章节目录（Latest 版，按课程 notes 顺序整理为 24 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：软件构建与"高质量"三目标、课程工具链（Java/Gradle/Git） | notes §Introduction；syllabus |
| L2 | Java 速成与代码阅读：类、接口、异常、集合与 Eclipse/IDE 工作流 | notes §Java in 6.031 |
| L3 | 版本控制与协作：Git 分支、GitLab 工作流、提交粒度 | notes §Git + 必学工具 Git 章 |
| L4 | 代码审查 Code Review：检查什么、如何写评语、审查清单 | notes §Code Review；Bacchelli & Bird (2013) |
| L5 | 单元测试：JUnit、测试金字塔、等价类划分与覆盖度量 | notes §Unit Testing；HW1 发布 |
| L6 | 规格 Specification：PRE/POST/RET/TERMINATES 与契约式思维 | notes §Specifications；HW1 |
| L7 | 测试策略：测试派生、属性测试与随机化测试（JUnit QuickTheories） | notes §Test Derivation/Strategy |
| L8 | 抽象数据类型 ADT：抽象函数 AF、表示不变式 RI、安全表示暴露 | notes §Abstract Data Types；HW2 发布 |
| L9 | 不可变类型：final、缓存/记忆化与不可变带来的并发安全 | notes §Immutable Types |
| L10 | 接口与实现分离：Java interface、封装层次与包设计 | notes §Interfaces & Abstraction |
| L11 | 泛型与类型参数：通配符、上下界与不变性 | notes §Generics |
| L12 | 子类型与替换原则：协变/逆变、行为子类型、LSP 与继承 vs 组合 | notes §Subtyping & Generics；HW3 发布 |
| L13 | 可变 ADT：观察者/变更者、表示共享、观察者模式与失效风险 | notes §Mutable ADTs |
| L14 | 面向对象设计原则：职责分配、分层（layering）、DIP/SRP/OCP | notes §Object-Oriented Design |
| L15 | 设计模式实战：策略/工厂/装饰/组合在课程项目中的用法与滥用信号 | notes §Design Patterns；经典 GoF 选读 |
| L16 | 并发基础：线程、竞态、原子性与线程安全规格 | notes §Concurrency；HW4 发布 |
| L17 | 锁与死锁：互斥、锁顺序、Guarded Object 模式、不变式保护 | notes §Thread Safety |
| L18 | 更高层次并行：ExecutorService、线程池、并行流与不可变数据共享 | notes §Concurrent Programming |
| L19 | 性能与正确性权衡：记忆化、缓存失效、避免过早优化 | notes §Memoization/Performance |
| L20 | 服务端与 Web 服务：HTTP、REST API 设计、无状态服务与 JSON | notes §Web Services；Project 发布 |
| L21 | 客户端与服务端交互：单页应用、表单与客户端校验的边界 | notes §Client-Side Web Apps |
| L22 | Web 安全 I：注入（SQL/命令）、XSS、输出编码与 CSP | notes §Web Security；HW/Quiz |
| L23 | Web 安全 II：CSRF、认证与会话、口令存储、访问控制与日志 | notes §Authentication & Access Control |
| L24 | 综合复习与项目交付：质量三目标回归检查、代码复审与重构 | notes §Review；Project 截止 |

> 说明：6.031 各学期讲次合并方式略有差异（如泛型与子类型有时并为一讲），但**规格 → ADT → 子类型 → 并发 → Web/安全**的骨架稳定；本表以 Latest 版 notes 顺序为准。

## 课程资源（摘自 csdiy）

- 课程网站：latest / Spring 2022 / Spring 2021 / Spring 2016
- 课程视频：无（课程以自读 notes + 作业为主，强调阅读与动手）
- 课程教材：课程网站 notes（在线教材）
- 课程作业：4 个编程作业 + 1 个 Project（2016 春起作业代码框架全部开源）
- 社区资源：PKUFlyingPig/MIT6.031-software-construction；pengzhangzhi/self-taught-CS 笔记
