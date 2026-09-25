# 第 11 章 DIP：依赖反转原则

> **一句话**：DIP 是全书把「原则」变成「机制」的那一步——**低层细节要定义高层需要的接口，高层策略拥有抽象，具体实现由外层注入**。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| Ch11 稳定的抽象层 | 哪些抽象值得放在内层 | 抽象越靠内，越接近「业务语言」，越稳定 |
| Ch11 工厂模式 | 谁来负责创建对象 | 用工厂/装配把 `new` 挡在边界外 |
| Ch11 具体实现组件 | 具体实现由外层提供 | 具体实现可以单独部署、单独替换 |
| Ch11 本章小结 | DIP 的三条操作手册 | 高层不依赖低层；低层依赖高层声明的接口；具体实现在边界外 |

---

## 核心精讲

**教学示意，不参与构建、不编译、不运行。**

**DIP 的四条可操作规则**（原文的三个要点 + 工程补充）：

1. 高层策略不要依赖低层细节，**两者都依赖抽象**；
2. 抽象不要依赖具体实现细节，**具体实现类依赖抽象**；
3. 具体实现组件放在边界之外（外层 / 部署单元 / 插件目录）；
4. 对象的创建走工厂或装配，而不在业务代码里 `new`。

```java
// ---------- 内层：策略 + 抽象（不认识任何具体存储） ----------
public interface OrderRepository {           // 抽象归内层的"用例"所有
    Order findById(OrderId id);
    void save(Order order);
}

public final class PlaceOrder {              // 用例：唯一一处变化点
    private final OrderRepository repo;
    public PlaceOrder(OrderRepository repo) { this.repo = repo; }   // 构造注入

    public void execute(PlaceOrderRequest req) {
        Order o = Order.place(req);                 // 业务规则（Entities）
        repo.save(o);
    }
}
```

```java
// ---------- 外层：具体实现（可单独替换、可单独部署） ----------
public final class JdbcOrderRepository implements OrderRepository {
    public Order findById(OrderId id) { /* SQL 细节在这里 */ return null; }
    public void save(Order order)    { /* SQL 细节在这里 */ }
}
```

```java
// ---------- 装配点：Main 组件（Ch26）或框架容器 ----------
public final class Main {
    public static void main(String[] args) {
        OrderRepository repo = new JdbcOrderRepository();   // 唯一的耦合点
        new PlaceOrder(repo).execute(PlaceOrderRequest.of("o-1"));
    }
}
```

**为什么「接口归调用方所有」这件事重要**（这是 DIP 最常见被抄错的地方）：

| 归属方 | 接口名字 | 后果 |
| --- | --- | --- |
| 被依赖方（存储框架）定义 | `JdbcRepository`、带 `save/update/delete` 的 `CrudRepository` | 领域层被迫依赖框架类型，换 ORM 要改业务代码 |
| 调用方（用例层）定义 | `OrderRepository`（方法按用例裁剪） | 存储换掉时只改实现，业务代码不动 |

---

## 版本演进

| 时期 | 事件 | 与本章的关系 |
| --- | --- | --- |
| 1994 | Martin，《A Pattern Language for Tailor-Made Applications》（C++ Report） | 「控制反转」与「依赖注入」早期形态 |
| 1996 | Martin 的 C++ Report 专栏正式提出 DIP | 命名与论证的出处 |
| 2002 | *Agile Software Development* 收录 DIP | 进入 SOLID 组合 |
| 2004 | Spring 框架让「依赖注入」成为主流实践 | DIP 从理念变成「一行注解」——但也因此被大量误用 |
| 2017 | 本书 Ch11 + Ch22：DIP 被写成「依赖关系规则」 | 与同心圆分层绑定，成为整洁架构的地基 |
| 2018 之后 | 「依赖注入容器是架构负债」的讨论 | 容器把装配成本移出业务代码，但也把耦合移进了 XML/注解 |
| 2020 年代 | DDD 战术设计复兴：`Repository` 接口回到「只暴露聚合需要」 | 对 DIP 的一次回归：接口要窄（ISP）且归调用方所有 |
| 2020 年代 | Go 的隐式接口 + 显式构造；Rust 的 `Box<dyn Trait>` | DIP 在这些语言里不需要容器也能干净实现 |

---

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| *The Dependency Inversion Principle*, Martin | clean-code.com 博客（*The Principles of OOD* 系列）；亦见 C++ Report 1996 专栏 | DIP 的母本 |
| *The Principles of OOD*（整系列） | clean-code.com 博客 | SRP/OCP/LSP/ISP/DIP 的原始连载 |
| *Pattern of Enterprise Application Architecture*, Martin | Addison-Wesley，2002 | Domain Model / Data Mapper / Registry，Ch11 的工程形态（中译本笔记见 `book/企业应用架构模式.md`） |
| *Domain-Driven Design*, Evans | Addison-Wesley，2003 | 仓储抽象的位置与聚合边界 |
| *Inversion of Control* 相关讨论 | Martin Fowler 对 PicoContainer 的整理（2004） | 把 DIP 与 IoC 容器的关系讲清楚 |
| *How Do Committees Invent?*, Conway | Datamation，1968 | 说明「谁定义接口」往往由组织结构决定，而不是技术优劣 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：**「要不要用 DI 容器」不再重要，「装配点在哪」才重要**。工业界共识正在从「框架提供容器」转向「应用代码显式装配（Composition Root）」，以减少注解驱动的隐式耦合。

| 仓库 | star（2026-09-25 `gh api` 实测） | 说明 |
| --- | --- | --- |
| `spring-projects/spring-framework` | **60260** | DI 容器的工业标准，也是「隐式耦合」的争议来源 |
| `spring-projects/spring-boot` | **81497** | 自动配置让装配极简，也把框架决策推到了最内层 |
| `golang/go` | **138994** | 显式构造 + 隐式接口：无容器也能 DIP，装配写在 `main`/`cmd` 里 |
| `rust-lang/rust` | **119150** | `Box<dyn Trait>` + 生命周期，配合显式装配实现零成本抽象与依赖反转 |
| `TNG/ArchUnit` | **3843** | 校验「内层不得依赖外层」这类 DIP 规则的机器化手段 |

---

## 常见误区与本书需修正之处

| 误区 | 表现 | 修正 |
| --- | --- | --- |
| 🔧 「所有依赖都指向内部」在实践中代价高昂 | 连 `Logger`、`Clock`、`Money` 都要在内层定义接口 | 只对**有真实替换动机**的边界做抽象；其余用具体类并允许内层直用 |
| 🔧 用框架提供的 `CrudRepository` 当领域接口 | 领域层 `import org.springframework.data...` | 在用例层定义自己的窄接口，外层实现（Ch22–23 的网关） |
| 把 DIP 理解成「到处加接口」 | 每个类一套接口 | 抽象数量 = 需要反转的依赖数量 |
| 认为 DI 容器等于 DIP | 满屏注解，装配逻辑不可读 | 保持一个明确的 Composition Root（Ch26 的 `Main` 组件） |
| 忘记「具体实现组件」的部署含义 | 实现与内核打进同一个包，物理上无法替换 | 具体实现放外层包 / 独立部署单元（`08-组件耦合.md`、Ch18） |
| 把 DIP 当成架构的最终目标 | 依赖方向对了，但层与层的职责仍然混乱 | DIP 是手段；目标是 Ch15 的「保持可选项」 |

---

## 与其他章 / 其他书的联系

- **本目录**：`00-总览与阅读地图.md`（同心圆与四条依赖规则）、`04-SRP与OCP.md`、`05-LSP与ISP.md`（接口归属）、`07-组件与组件聚合.md`（`REP` 与 DIP 的包级对应）、`12-尖叫的软件架构与整洁架构.md`（Ch22 的依赖关系规则）、`14-层次与边界Main及测试边界.md`（Ch26 `Main` 组件、Ch28 测试专用 API）。
- **`book/设计模式GoF/`**：`concepts/依赖倒置.md` 是本条目的直接对照；`06-模式的代价与反模式.md` 讨论「抽象何时是过度设计」。
- **`book/代码整洁之道*`（仓库内 `book/C++代码整洁之道.md`）**：Clean Code 的「依赖注入」一节与本章同一观点，只是粒度在类级。
- **`book/重构*`（仓库内暂无）**：「以工厂方法取代直接构造」「引入接口」是 DIP 的重构手法。
- **`book/代码大全（第2版）*`**（仓库内暂无）：耦合与内聚的度量，可与 DIP 的规则互相校验。
- **`book/企业应用架构模式.md`**：P of EAA 的 Dependency Injection 模式原文，与 Ch11 的一步步对照。
