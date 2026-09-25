# 第 7 章 SRP：单一职责原则 与 第 8 章 OCP：开闭原则

> **一句话**：SRP 说「一个模块只因一个原因而变」，OCP 说「加功能要扩展而不是改源码」——两者的落点都是同一件事：**控制依赖方向，让变化只打在一个地方**。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| Ch7 反面案例 1：意外的复用 | 一个被别处复用的模块，被无辜地改动 | 「复用」与「耦合」是同一个决定的两面 |
| Ch7 反面案例 2：代码合并 | 两个人为了互不相干的原因改同一个文件 | 合并冲突 = SRP 失守的报警器 |
| Ch7 解决方案 / 本章小结 | 单一职责的判据是「变化的轴」 | 职责 = **变更原因**，不是「功能数量」 |
| Ch8 思想实验 | 一个由第三方控制的程序，如何做到不改源码加功能 | 信息隐藏 + 依赖倒置 + 合成/聚合 |
| Ch8 依赖方向的控制 | 依赖必须指向抽象 | OCP 的架构版翻译 |
| Ch8 信息隐藏 | 模块藏住自己的决策 | 隐藏的「决策」越多，可替换性越强 |
| Ch8 本章小结 | OCP 与「对扩展开放、对修改关闭」的边界 | 开放是有代价的：只对**预测到的**扩展点开放 |

---

## 核心精讲

**教学示意，不参与构建、不编译、不运行。**

**Ch7：SRP 的判据是「变更原因」，不是「代码多少」。**

```java
// 反例：一个 Employee 类同时承担三种变更原因（DTO/持久化/薪资规则）
class Employee {                 // 示意：三类变化挤在一个类里
    String name; BigDecimal salary;   // 可能因 UI 变
    void insert() { ... }             // 可能因 DB 变
    BigDecimal calcPay() { ... }      // 可能因财务规则变
}
```

```java
// 正例方向：按"变更原因"切分
record EmployeeDTO(String name, BigDecimal salary) {}                 // UI/边界用
interface EmployeeGateway { void save(Employee e); }                  // 存储抽象（Ch30）
final class PayCalculator { BigDecimal calc(Employee e) { ... } }     // 规则
```

**Ch8：OCP 的技术骨架（用合成替代继承，用抽象替代具体实现）。**

```java
// 抽象在"内"，具体在外：依赖方向向内
public interface DiscountRule {
    boolean matches(Request req);
    BigDecimal discount(Request req);
}

// 外层装配；新增一种折扣 = 新增一个类，不改旧代码
public final class DiscountEngine {
    private final List<DiscountRule> rules;
    public DiscountEngine(List<DiscountRule> rules) { this.rules = List.copyOf(rules); }
}

// 依赖倒置的另一种常见写法：把"具体组件"交给 Main / 工厂（Ch11、Ch26 会展开）
// 示意：不要在引擎内部 new 出具体规则
```

> 一个容易忽略的细节：OCP 的「开」是**局部的**。对所有点都开放的系统等于没有稳定的抽象；真正可维护的做法是只对**已经观察到、且确定会发生**的变化点开放（这也正是本书 Ch24「不完全边界」的伏笔）。

---

## 版本演进

| 时期 | 事件 | 与本章的关系 |
| --- | --- | --- |
| 1994 | Martin，《*Adaptive Object Model*》系列文章 | 「元数据驱动 + 规则集中」的思想，OCP 在配置化方向的尝试 |
| 1996 | Martin 在 C++ Report 的专栏首提 DIP | Ch8 里「依赖方向」的技术依据 |
| 2002 | *Agile Software Development, Principles, Patterns, and Practices* | 以书的形式把 SOLID 讲了一遍（博客在前，书在后） |
| 2008 前后 | *The Principles of OOD*（clean-code.com） | SRP/OCP/LSP/ISP/DIP 五篇成文，Ch7–Ch11 逐条对应 |
| 2017 | 本书把 SOLID 从「类级原则」提升为「**架构级**原则」 | 关键转变：SRP 不只管一个类，它管**组件**与**层** |
| 2020 年代批评 | 「为 OCP 而 OCP」的抽象税被反复点名 | 修正：抽象只对**可预见的、有预算的**变化点开放 |
| 2020 年代 | 配置/规则引擎与「策略即数据」成为主流，OCP 在实践里退化为「少改旧代码」 | 从「必须开闭」到「尽量开闭」 |

---

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| *The Single Responsibility Principle*, Martin | clean-code.com 博客（*The Principles of OOD* 系列） | SRP 的原文定义与两个反例（意外的复用、代码合并） |
| *The Open-Closed Principle*, Martin | clean-code.com 博客 | Ch8 思想实验的原始版本 |
| *The Dependency Inversion Principle*, Martin | clean-code.com 博客；C++ Report 专栏 | 「高层策略不应依赖低层细节」的提出 |
| *On the Criteria To Be Used in Decomposing Systems into Modules*, Parnas | CACM，1971 | 信息隐藏的奠基：隐藏「可能变化的决策」，正是 SRP/OCP 的共同动机 |
| *Designing Data-Intensive Applications*（相关讨论） | O'Reilly，2017 | 补充：分布式系统里「不修改」的代价更高（见第 15 章） |
| *Pattern of Enterprise Application Architecture* | Addison-Wesley，2002 | P of EAA 的 Domain Model / Data Mapper 是 Ch8 抽象的工程形态 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：**OCP 的「扩展点」正在从代码层下沉到配置与数据层**（策略注册、插件、规则引擎），同时「抽象税」的反思让团队开始要求「扩展点必须有删除路径」——即新增的类必须能被撤回。

| 仓库 | star（2026-09-25 `gh api` 实测） | 说明 |
| --- | --- | --- |
| `TNG/ArchUnit` | **3843** | 把 SRP 落成规则：例如「同一包内不得同时出现 `Controller` 与 `Repository`」 |
| `sverweij/dependency-cruiser` | **7218** | JS/TS 侧用依赖规则约束「扩展点的依赖方向」 |
| `spring-projects/spring-framework` | **60260** | `@Conditional` / `BeanPostProcessor` 是 OCP 的工业化实现，也是抽象税的来源 |
| `bazelbuild/bazel` | **25880** | 用构建期依赖图强制「新增实现必须显式声明依赖」 |

```java
// ArchUnit 规则示意（教学示意，不参与构建）
// @ArchTest
// static final ArchRule 单一职责 = classes()
//     .that().resideInAPackage("..domain..")
//     .should().onlyDependOnClassesThat().resideInAPackage("..domain..", "..usecases..");
```

---

## 常见误区与本书需修正之处

| 误区 | 表现 | 修正 |
| --- | --- | --- |
| 🔧 「一个类一个职责」被读成「一个类做一件事」 | 按动词切类，产生大量 Pipeline 类 | 按**变更原因**切；需求方变了才算换了原因 |
| 把 OCP 理解成「永远不改旧代码」 | 任何改动都先想办法加个扩展点 | 只对**已观测到**的变化开放；没观测到就先写死（Ch24 的不完全边界） |
| 认为「信息隐藏 = 全 private」 | 把所有字段藏起来却靠 getter 全暴露 | 隐藏的是**决策**，不是可见性；暴露只读视图即可 |
| 🔧 抽象税：为每个扩展点造接口+工厂 | 三个实现用五个接口，删掉两个没人敢删 | 要求每个抽象都有「被替换的真实案例」，否则删除 |
| SRP 只讲究代码组织，与包无关 | 类切得很干净，包里仍然混着三层 | 本书明确：SRP 与包组织同构，见 `07-组件与组件聚合.md` |
| 认为 OCP 就是「用继承扩展」 | 大量 `BaseXxx` 抽象类 | 优先组合 + 抽象接口；继承受 LSP 强约束（见 `05-LSP与ISP.md`） |

---

## 与其他章 / 其他书的联系

- **本目录**：`05-LSP与ISP.md`（Ch9–10，OCP 的契约面）、`06-DIP：依赖反转原则.md`（Ch11，OCP 的实现机制）、`07-组件与组件聚合.md`（Ch12–13，SRP 在包级的实现）、`13-展示器与谦卑对象及不完全边界.md`（Ch24，OCP 的「半途而废」方案）。
- **`book/设计模式GoF/`**：`concepts/依赖倒置.md` 与 `01-引言与模式系统.md` 可直接对照；`05-策略、状态、模板方法与访客.md` 是 OCP 的模式化形态。
- **`book/代码整洁之道*`（仓库内 `book/C++代码整洁之道.md`）**：Clean Code 的「类应该尽量小」是 SRP 在类级的表达。
- **`book/重构*`（仓库内暂无；`book/大话重构.md` 为解读）**：「提炼类」「以策略取代条件逻辑」正是 Ch7–8 的手法。
- **`book/代码大全（第2版）*`**（仓库内暂无）：「表里如一」「耦合度量」可与 SRP 互相印证。
- **`book/企业应用架构模式.md`**：其中 Data Mapper、Plugin 等模式是 OCP 在 2002 年的工程形态。
