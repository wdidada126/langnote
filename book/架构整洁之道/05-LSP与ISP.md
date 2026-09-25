# 第 9 章 LSP：里氏替换原则 与 第 10 章 ISP：接口隔离原则

> **一句话**：LSP 是「继承能不能用」的判定器，ISP 是「接口该多宽」的度量衡——两者都不只是类设计问题，一旦越过包边界，就变成**架构上的可替换性**问题。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| Ch9 继承的使用指导 | 继承里的抽象方法该由谁实现 | 继承是「实现复用」+「类型契约」，只有后者才值得关注 |
| Ch9 正方形/长方形问题 | 数学上的正方形不是 LSP 满足的长方形 | 契约必须由**你定义的规则**决定，而不是领域直觉 |
| Ch9 LSP 与软件架构 | 违反 LSP 会导致运行时类型无法互相替换 | 架构层：接口的实现必须可无歧义地互换 |
| Ch9 违反 LSP 的案例 | 平台库里的 bug（Stack 继承 Vector 之类） | 用「能编译但会出错」的替换，代价由调用方承担 |
| Ch9 本章小结 | LSP 是抽象是否有用的前提 | 抽象若不可替换，等于没有抽象 |
| Ch10 ISP 与编程语言 | 语言是否支持「选择性可见」 | Java abstract class vs interface 的差别在这里 |
| Ch10 ISP 与软件架构 | 胖接口强迫依赖不需要的东西 | 架构层：**不要让内核模块依赖外层才用的方法** |
| Ch10 本章小结 | 拆接口是低成本、高杠杆的架构动作 | 每拆一个接口，就多一处「不会触发重编译」的解耦 |

---

## 核心精讲

**教学示意，不参与构建、不编译、不运行。**

**LSP：判断「能不能替换」看的是你自己定的契约。**

```java
// 反例（示意）：正方形"是"长方形，但宽度一改高度不变 -> 契约破裂
abstract class Rectangle {
    protected int w, h;
    public void setW(int w) { this.w = w; }
    public void setH(int h) { this.h = h; }
    public abstract int area();
}
class Square extends Rectangle {
    public void setW(int w) { super.setW(w); super.setH(w); }  // 强制同步
    public void setH(int h) { super.setH(h); super.setW(h); }
}
```

```java
// 正例方向：把"可变尺寸"与"等边形状"拆成两个正交的抽象
interface Shape { int area(); }
interface Resizable { void resize(int w, int h); }
```

**ISP：窄接口让「用不到的方法」不再成为依赖。**

```java
// 反例：一个"万能"持久化接口，让领域层被迫依赖它不需要的方法
interface SuperRepository {
    void save(Object o);
    byte[] exportBinary();        // 只有运维要用
    void scheduleReindex();       // 只有搜索要用
}

// 正例方向：按调用方需要的形状拆开，内核只依赖真正会用的那一个
interface Saver { void save(Order o); }
interface AdminOps { byte[] exportBinary(); void scheduleReindex(); }
```

> 架构层面的翻译：LSP 问「这两个实现能不能互换」，ISP 问「调用方凭什么要依赖整个模块」。**ISP 是本书里最便宜的解耦手段**——不需要新增目录、不需要框架，只需要把接口按「谁在用」切窄。

---

## 版本演进

| 时期 | 事件 | 与本章的关系 |
| --- | --- | --- |
| 1987 | Liskov，《Data Abstraction and Hierarchy》 | LSP 的原始出处（在 OOPSLA 1987 的 keynote 里提出） |
| 1994 | Martin 把 LSP 写进 *Agile Software Development* | 从类型系统话题转为设计原则 |
| 2000s | 语言机制演进：Java 8 默认方法、Go 的隐式接口、Rust 的 trait | ISP 的「窄接口」在这些语言里成本更低 |
| 2017 | 本书把 LSP 从类级提升到架构级 | 「可替换的实现」成了依赖方向讨论的 synonyms（同义词） |
| 2020 年代 | 「不要为框架实现写接口」的实践共识 | 框架定义的接口往往违反 ISP，导致领域层被污染 |
| 2020 年代 | DDD 战术设计复兴，`Repository` 接口回归「只暴露用例需要的方法」 | ISP 与聚合边界结合，见 `13-展示器与谦卑对象及不完全边界.md` |

---

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| *Data Abstraction and Hierarchy*, Liskov | OOPSLA'87 Keynote Address（1987） | LSP 的原始提出，注意是 OOPSLA 会议 key note，不是 CACM 论文 |
| *The Liskov Substitution Principle*, Martin | clean-code.com 博客（*The Principles of OOD* 系列） | 把 LSP 转成软件工程原则 |
| *The Interface Segregation Principle*, Martin | clean-code.com 博客 | ISP 原文；「胖接口导致脂肪依赖」 |
| *The Single Responsibility Principle*（同系列） | clean-code.com 博客 | SRP 与 ISP 共同强调「按变更原因切分」 |
| *On the Criteria To Be Used in Decomposing Systems into Modules*, Parnas | CACM，1971 | 「隐藏决策」与「窄接口」同源 |
| *Domain-Driven Design*, Evans | Addison-Wesley，2003 | 仓储接口只暴露聚合所需，是 ISP 在领域层的实例 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：**接口「窄而多」被语言机制进一步强化**（Go 的隐式接口、Rust 的 trait、TypeScript 的结构类型），同时框架作者与架构师之间的「接口归属」冲突成为公开讨论：究竟是框架定义接口，还是应用定义端口。

| 仓库 | star（2026-09-25 `gh api` 实测） | 说明 |
| --- | --- | --- |
| `golang/go` | **138994** | 隐式接口：`io.Reader`/`io.Writer` 是 ISP 最干净的工业实例 |
| `rust-lang/rust` | **119150** | trait 取代继承，天然避免 LSP 陷阱（不需要 LSP 也满足替换） |
| `TNG/ArchUnit` | **3843** | 可写规则「领域包不得依赖某类标记接口的包」，落地 ISP 的架构约束 |
| `sverweij/dependency-cruiser` | **7218** | JS/TS 侧：结构类型下 ISP 依然可检（用依赖图看胖依赖） |

---

## 常见误区与本书需修正之处

| 误区 | 表现 | 修正 |
| --- | --- | --- |
| 🔧 用「is-a」判断继承合法性 | `Square extends Rectangle` | 用**你自己的契约**判断：调用方期望的行为满足吗 |
| 把 LSP 当成类型系统的细节 | 争论泛型协变逆变 | 关心的是「这个抽象是否真的能被替换」 |
| 🔧 把框架接口当自己的接口用 | 领域层实现 `CrudRepository` | 在应用侧定义端口，框架侧实现适配器（Ch22–23） |
| ISP 被读成「接口越多越好」 | 每个类一套私有接口 | 按**调用方**切，而不是按类名切 |
| 认为拆接口一定能解耦 | 拆了接口但两个实现仍在同一包 | 配合包边界与依赖方向才有效（`08-组件耦合.md`） |
| LSP/ISP 只影响单测 | 以为可以永不替换实现 | 可替换性正是「保持可选项」的核心机制（Ch15） |

---

## 与其他章 / 其他书的联系

- **本目录**：`03-面向对象编程与函数式编程.md`（Ch5，多态与继承的背景）、`04-SRP与OCP.md`（Ch7–8）、`06-DIP：依赖反转原则.md`（Ch11，DIP 与 LSP 的合力）、`07-组件与组件聚合.md`（Ch12–13，包级可见性）、`15-服务、嵌入式与实现细节.md`（Ch32，框架接口 « 应用端口）。
- **`book/设计模式GoF/`**：`concepts/依赖倒置.md`、`02-创建型模式.md`（抽象工厂与 DIP 配合）；`05-策略、状态、模板方法与访客.md`里的模板方法涉及继承契约，可直接对照 LSP。
- **`book/代码整洁之道*`（仓库内 `book/C++代码整洁之道.md`）**：Clean Code 关于「继承层级过深」的提醒与 LSP 同源。
- **`book/重构*`（仓库内暂无）**：「以委托取代继承」「提炼接口」是 Ch9–10 的重构版手法。
- **`book/代码大全（第2版）*`**（仓库内暂无）：接口/耦合章节提供 ISP 的术语对照。
- **`book/企业应用架构模式.md`**：Gateway、Mapper 模式里「接口只暴露用例方法」，是 ISP 在企业应用里的原型。
