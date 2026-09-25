# 第 25 章 层次与边界、第 26 章 Main 组件、第 28 章 测试边界

> **一句话**：本章讲「边界与层次如何对应」以及两个收口的地方——`Main` 组件是唯一允许知道「具体是什么」的地方，而测试是系统里的**第二用户**，它的成本必须被架构考虑进去。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| Ch25 基于文本的冒险游戏：Hunt The Wumpus | 一个完整小系统的层次与边界 | 用最小例子看清全貌 |
| Ch25 可否采用整洁架构 | 该架构在这个规模下是否划算 | 本书罕见地直接讨论「不值得」 |
| Ch25 交汇数据流 / 数据流的分割 | 数据在边界之间的两种走法 | 读模型与写模型可分别设计 |
| Ch25 本章小结 | 边界与层次不必一一对应 | 同层可以有多个边界 |
| Ch26 最细节化的部分 | `Main` 负责一切「具体」的装配 | 装配点集中在一处 |
| Ch26 本章小结 | 依赖注入、配置、启动流程都在 `Main` 里 | 业务代码里不出现具体类的构造 |
| Ch28 测试也是一种系统组件 | 测试有与生产代码同等的地位 | 测试也是架构的使用者 |
| Ch28 可测试性设计 | 依赖方向带来可测性 | 最内层可纯内存测试 |
| Ch28 测试专用 API | 为测试提供的受控入口 | 有时值得为测试留一个小口 |
| Ch28 本章小结 | 测试成本是架构成本的一部分 | 用测试金字塔约束端到端规模 |

---

## 核心精讲

**教学示意，不参与构建、不编译、不运行。**

**`Main` 组件作为「唯一的具体知识持有者」**：

```java
// ---------- 业务代码：不认识任何具体产品 ----------
public interface ClockPort { Instant now(); }        // 内层端口

public final class Report {
    private final ClockPort clock;
    public Report(ClockPort c) { this.clock = c; }
    public String today() { return clock.now().toString(); }
}

// ---------- Main：唯一 new 出具体实现的地方（Ch26） ----------
public final class Main {
    public static void main(String[] args) {
        ClockPort clock = new SystemClock();              // 具体在这里出现
        new Report(clock).today();                         // 业务代码始终不知道
    }
}
```

**Hunt The Wumpus 的层次/边界映射（Ch25 的教学例子）**：

```text
   边界 A（玩家输入）     边界 B（地图与渲染）
        |                        |
   [Controller]  <-->  [ Use Cases ]  <-->  [ Entities ]
        |                                        ^
   [Player Adapter]                              |
        +---- 跨边界只传简单文本/坐标 ----------+
```

**测试专用 API（Ch28）**：什么时候值得为测试开一个口子。

| 场景 | 做法 | 代价 |
| --- | --- | --- |
| 端到端测试太慢 | 提供「跳过 UI、直接调用例」的入口 | 多一层 API 需要维护 |
| 时间/随机的不确定性 | 注入 `ClockPort`、随机数种子 | 抽象成本（与 Ch11 一致） |
| 数据库不可用 | 用内存实现或测试替身 | 与真实行为可能有偏差 |
| 🔧 为方便测试把业务逻辑搬进测试框架 | 测试里 `mock` 掉一半业务 | 测试通过但系统不通过 |

> Ch25 的「可否采用整洁架构」是全书难得的一次自我限定：**在很小的系统里，那些层可能不值得**。这与 12 章的常见误区相互呼应。

---

## 版本演进

| 时期 | 事件 | 与本章的关系 |
| --- | --- | --- |
| 1979 | Parnas 关于「隐藏层级」与渐进式细化 | 层次与实现细节分离的思想源头 |
| 2002 | P of EAA：Composition Root（依赖注入的根） | `Main` 组件的前身 |
| 2013 | Fowler，《Inversion of Control Containers and the Dependency Injection pattern》 | Composition Root 的正式说法 |
| 2017 | 本书 Ch25–26：层次、边界与 `Main` 组件成章 | 把装配点写成架构元素 |
| 2018 | 中译本 | 「Main 组件」成为中文里的常用词 |
| 2020 年代 | 「Composition Root 应该在 Main，而不是框架启动时」成为主流观点 | 与 Spring Boot 的自动装配形成对照 |
| 2020 年代 | 测试策略：测试金字塔 + 契约测试 + 快照测试 | Ch28「端到端测试规模」的落地工具 |
| 2020 年代 | 「可测试性」成为架构评审的常规项 | 与 Ch22 的可测试性主张合流 |
| 2024–2026 | AI 生成的集成测试激增，测试专用 API 的价值上升 | 测试作为系统组件的地位更突出 |

---

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| *Inversion of Control Containers and the Dependency Injection pattern*, Fowler | martinfowler.com，2004 | Composition Root 的权威描述 |
| *On the Criteria To Be Used in Decomposing Systems into Modules*, Parnas | CACM，1971 | 层次分解与隐藏细节 |
| *Pattern of Enterprise Application Architecture*, Martin | Addison-Wesley，2002 | Registry、Composition Root 与初始化的模式化 |
| *The Principles of OOD*（DIP 篇），Martin | clean-code.com 博客 | `Main` 组件里做装配的依据 |
| *How Do Committees Invent?*, Conway | Datamation，1968 | 测试组织与开发组织的结构同构 |
| *Designing Object-Oriented C++ Applications Using the Booch Method*, Martin | Prentice Hall，1995 | 「静态模型/动态模型」与层次划分的早期讨论 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：**「装配点集中化」从理念变成可审计的规范**——用显式 `main`/`cmd`、无容器架构、以及构建级的可见性控制来实现；同时测试成本被视为架构债的主要来源之一。

| 仓库 | star（2026-09-25 `gh api` 实测） | 说明 |
| --- | --- | --- |
| `golang/go` | **138994** | 无框架时 `cmd/` + `internal/` 天然就是 Composition Root |
| `rust-lang/rust` | **119150** | `main.rs` 显式装配 + `Box<dyn Trait>`，无 DI 容器也能完成依赖反转 |
| `spring-projects/spring-framework` | **60260** | 容器接管装配；争议点在于「容器是不是 Composition Root」 |
| `pytest-dev/pytest` | **14534** | Ch28 的工程形态：分层 fixture 让集成测试按需启用 |
| `bazelbuild/bazel` | **25880** | 用测试目标粒度限制端到端测试规模 |

---

## 常见误区与本书需修正之处

| 误区 | 表现 | 修正 |
| --- | --- | --- |
| 🔧 把「层次对应边界」当成一对一的规则 | 每一个层都必须有一个独立部署单元 | 同层可以有多个边界；边界强度可以不同（`10`、`18` 章） |
| 把 `Main` 当成「随便放主函数的类」 | 装配逻辑散落在 Spring 配置、`@PostConstruct`、静态块 | 装配集中在一处，其它地方不出现具体类构造 |
| 认为 `Main` 只负责打印欢迎语 | 配置解析、数据库连接池、迁移脚本都在业务代码里 | `Main` 是「系统成为一个系统的地方」 |
| 🔧 为测试大量增加测试专用 API | 生产代码里多出一堆仅供测试的类 | 只在确实划算时开口子，并对这些类做明确的可见性限制 |
| 认为端到端测试越少越好 | 把集成测试当负担删掉 | Ch28 主张的是「合理规模」；删掉的是重复的、不稳定的那部分 |
| 测试专用 API 泄露到生产语义 | 测试入口被用来「绕过校验」 | 口子只暴露必要的受控行为 |
| `Main` 组件里塞进太多，成了上帝对象 | 一个文件 2000 行装所有装配 | 拆成若干装配 DSL/配置对象，主题仍是「集中」 |
| 认为「可测试性」只是测试团队的事 | 架构评审不测可测性 | 内层不依赖框架 = 单测不需要容器，这是架构的直接收益 |

---

## 与其他章 / 其他书的联系

- **本目录**：`06-DIP：依赖反转原则.md`（Ch11，工厂与装配）、`12-尖叫的软件架构与整洁架构.md`（Ch22）、`13-展示器与谦卑对象及不完全边界.md`（Ch23–24）、`15-服务、嵌入式与实现细节.md`（Ch27、Ch29–32，`Main` 在嵌入式与框架处的变形）。
- **`book/设计模式GoF/`**：`02-创建型模式.md`（工厂与构造方式）、`06-模式的代价与反模式.md`（测试专用 API 的滥用）。
- **`book/代码整洁之道*`（仓库内 `book/C++代码整洁之道.md`）**：Clean Code 关于「构造与使用分离」的讨论。
- **`book/企业应用架构模式.md`**：Composition Root 与 Registry 模式的更早版本。
- **`book/重构*`（仓库内暂无）**：「引入测试替身」「拆分构造函数」是本章手法。
- **`book/代码大全（第2版）*`**（仓库内暂无）：其「测试策略」「集成节奏」一章与 Ch28 高度互补。
