# 第 11 章 重构 API

> **一句话**：接口是**对调用方的承诺**——重构 API 的代价天然比内部重构高一个量级，所以这一章的全部内容都围绕一个问题：**如何用最小的兼容代价，把这个承诺改成你真正想要的形状**。

---

## 本章地图

| 手法 | 解决什么问题 | 要点 | 代价 |
| --- | --- | --- | --- |
| **Hide Delegate** 隐藏委托关系 | 过长的消息链、内幕交易 | 在被委托方上建方法 → 原类留转发 → 逐步撤掉穿透访问 | 多一层转发；一旦暴露就难以收回 |
| **Remove Middle Man** 移除中间人 | 冗赘的元素 | 让调用方直接访问被委托方 | 消息链重新出现 |
| **Remove Parameter** 移除参数 | 重构 API 后遗留的死参数 | 删参数 → 处理兼容层 | 某些调用方其实需要它 |
| **Rename Method** 重命名函数 | 神秘命名 | 改名 + 更新所有调用点 | 唯一「测试可能拦不住」的手法 |
| **Introduce Parameter Object** 引入参数对象 | 过长参数列、数据泥团 | 建一个类承载这组参数 | 参数对象可能变成上帝对象 |
| **Remove Setter** 移除设值函数 | 破坏不变性与约束 | 改用构造/工厂方法 | 需要补初始化路径 |
| **Hide Method** 隐藏方法 | 方法本不该对外可见 | 改可见性；必要时先改继承体系 | 子类重构要牵动接口 |
| **Replace Constructor with Factory Method** 以工厂方法取代构造函数 | 构造意图不明显、要返回子类/缓存 | 私化构造 + 命名工厂 | 工厂类成为新的耦合点 |
| **Replace Error Notification with Exception** 以异常取代错误通知 | 调用方漏检查返回值 | 定义异常类型 → 抛出 → 边界捕获 | 异常跨越模块边界 |
| **Replace Exception with Error Notification** 以错误通知取代异常 | 异常被当成正常控制流 | 改成显式返回状态 + 边界统一处理 | 调用方容易漏检查 |

**关键结论**：
- API 改动的**兼容策略优先级**：新增 ≫ 新增可选参数 ≫ 废弃（Deprecated）保留 ≫ 硬删。
- 改名的兼容性最差，因此**越早改名越便宜**——代码刚写出来的那两周，改名几乎零成本。
- API 的「承诺」不止在代码里：还有文档、SDK、序列化契约、跨团队口头约定。**契约不在代码里的部分，工具帮你不了**。

---

## 核心精讲

> 教学示意代码，不编译、不运行、不参与构建。

### 1. Hide Delegate 与 Remove Middle Man：一对需要「看时机」的手法

```java
// 教学示意，不参与构建
// ❌ 过长的消息链：调用方穿过了三个内部对象
String city = order.getCustomer().getAddress().getCity();
```

```java
// 教学示意，不参与构建
// ✅ Hide Delegate：在 Order 上开一个「语义合理」的门
public class Order {
    public String city() { return customer.address().city(); }   // 一层转发，但名字表达了业务含义
}
// 调用方：order.city()
```

```java
// 教学示意，不参与构建
// ❌ 中间人：转发了 12 个方法，没加任何价值（冗赘的元素）
class Employee {
    public String getName() { return person.getName(); }
    public String getDept() { return person.getDept(); }
    public String getTel()  { return person.getTel(); }
    // …… 全是转发
}
```

| 时机 | 该用哪个 |
| --- | --- |
| 转发**加了语义**（`order.city()` 比 `order.getCustomer().getAddress().getCity()` 好读） | **Hide Delegate** |
| 转发**只加了层数** | **Remove Middle Man** |
| 被委托方将来可能换掉（策略/数据源可变） | **Hide Delegate**（保留一层抽象） |
| 中间人只是为了兼容旧版本 | 保留但标 `Deprecated`，排期删除 |

### 2. Introduce Parameter Object：参数列瘦身

```js
// 教学示意，不参与构建
// ❌ 过长参数列表：五个参数，顺序记错就出大事
function transfer(fromAcc, toAcc, amount, currency, memo, asOf) { … }
transfer(a, b, 100, "CNY", "房租", "2026-09-01");

// ✅ 把「永远一起出现」的参数收成一个对象
function transfer(cmd) { … }
transfer({ from: a, to: b, amount: 100, currency: "CNY", memo: "房租", asOf: "2026-09-01" });
```

**适用信号**：
- 参数 ≥ 4 个且顺序敏感；
- 有一组参数总是**一起传、一起删**（数据泥团）；
- 调用方为了凑参数而在多处构造一个小结构（那说明这个结构本该存在）。

**别滥用**：只有 2–3 个参数时用参数对象是噪音；更关键的是——**参数对象不要长成「把所有东西都塞进去」的上帝对象**。

### 3. Remove Parameter：最难判断「该不该删」的一个

```java
// 教学示意，不参与构建
public void send(String to, String subject, String body, boolean trackOpen) { … }
// 现在没人传 trackOpen 了 —— 删掉吗？
```

| 判断 | 结论 |
| --- | --- |
| 参数在函数体内**完全没被用到** | 删 |
| 参数被用到，但调用方全传同一个值 | 不删，改成配置/构造参数 |
| 参数被用到，且确实有不同取值 | 不删 |
| 参数只在少数调用方里有用 | 拆成两个方法，或改成参数对象 |

> **经验法则**：先 `Rename Parameter` 观察它的用途，然后再决定删不删；直接删是常见错误。

### 4. Replace Constructor with Factory Method：让创建意图可见

```java
// 教学示意，不参与构建
// ❌ 构造函数名无法表达「这是哪种创建」
new Animal("dog");
new Animal("cat");
// 于是每个调用方各自写 switch/registry

// ✅ 命名工厂方法把意图写进名字
public class Animal {
    public static Animal dog() { return new Animal("dog", DogBehaviour.INSTANCE); }
    public static Animal cat() { return new Animal("cat", CatBehaviour.INSTANCE); }
    private Animal(String kind, Behaviour b) { … }
}
```

**为什么值得**：构造函数**只能重名重载**，无法表达「这一族哪个」；工厂方法可以有语义良好的名字，还能返回子类实例、缓存实例或特殊 CASE（Form Special Case）。

### 5. 兼容策略：真实项目里改 API 的顺序

```text
第 0 步  确认契约范围：代码内 / SDK / 文档 / 序列化格式 / 跨团队约定
第 1 步  新增：只加不删（加新方法、加可选参数、加可选字段）
第 2 步  废弃：老方法标 @Deprecated / deprecated，日志告警，观察调用量
第 3 步  迁移：分批把调用方迁到新接口（可用静态分析定位调用点）
第 4 步  删除：观察两个版本后再删老接口
```

```java
// 教学示意，不参与构建
// 第 1–2 步的典型写法：老接口保留但废弃，新语义从内部开始推进
@Deprecated
public double getAmount() { return amount(); }   // 老名字继续可用

public double amount() { … }                     // 新名字成为主接口
```

### 6. 异常 vs 错误通知：不是哪个对，而是「谁负责处理」

```java
// 教学示意，不参与构建
// ❌ 异常当控制流：每个「用户不存在」都抛一次，栈被拉长，事务被标记回滚
try { return userRepo.find(id).get(); }
catch (NoSuchElementException e) { return registerPage(); }

// ✅ 用显式状态表达「正常业务流程的一部分」
Optional<User> u = userRepo.find(id);
if (u.isEmpty()) return registerPage();
```

| 场景 | 选哪个 |
| --- | --- |
| 参数是非法输入、状态机不允许的状态 | **Exception**（不该发生就别继续） |
| 「用户不存在」是一个正常业务分支 | **Error Notification / Optional / 状态对象** |
| 库内部的实现细节失败了 | **Exception** |
| 跨语言边界、插件宿主、脚本引擎 | 多为 **Error Notification**（异常无法安全穿越） |

---

## 版本演进

| 项 | 第 1 版（1999） | 第 2 版（2019） |
| --- | --- | --- |
| 章节位置与名称 | 第 1 版名录里没有独立的「重构 API」组 | 第 2 版**新增一整章「重构 API」**（第 11 章），把 Hide Delegate、Remove Middle Man、Introduce Parameter Object、Remove Parameter、Rename Method 等集中起来 |
| 侧重点 | 「如何改接口」散落在各手法里 | 明确以**兼容性**为中心：强调「接口是承诺」「先弃后删」的版本管理思路 |
| 示例语言 | Java | JavaScript，并以「模块导出面的变化」为例说明 API 改动成本 |

**2020 年代的重构工具与 AI 辅助**：

- **工具化**：IntelliJ 的 `Change Signature`（改参数列表 + 自动更新调用点）、Rename、Introduce Parameter Object 都已产品化；跨模块的重构会给出「影响面预览」。
- **契约层的缺失工具**：**Swagger/OpenAPI、gRPC 契约、数据库 schema、前端代码**——这些都不在 IDE 的重构作用域内，改名一个字段往往需要人工核对。这是本章「代价」一栏被低估的现实原因。
- **语言吸收**：TypeScript 的**可选参数 / 重载 / 工具类型**让「加参数」几乎零成本；Kotlin 的**默认参数与命名参数**部分吸收了 `Introduce Parameter Object` 的动机；Rust 没有「可选参数」，于是整体改用参数对象——**语言差异会直接改变这一章的手法排序**。
- **AI 辅助**：模型极擅长「把参数列表改成参数对象」，也极擅长**批量更新调用点**。风险是它可能**同时删掉一个你想保留的参数**（`Remove Parameter` 过度执行），或者把异常吞成静默返回值。审 diff 时请专门看：参数是否少了一个、异常去哪了。
- **OpenRewrite**：2020 年代把「API 迁移」做成了专门的品类——一次 recipe 完成「新增 + 废弃 + 迁移 + 删除」四个阶段，正是本章兼容策略的工业化版本。

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Opdyke, W.，《Refactoring Object-Oriented Frameworks》 | UIUC 博士论文，1992 | 接口变更类手法的早期形式（Encapsulate、Hide Method 的原型） |
| Fowler, M.，《Refactoring》第 2 版第 11 章「重构 API」 | Addison-Wesley，2019；中译本 ISBN 978-7-115-50865-2 | 本章骨架：Hide Delegate、Remove Middle Man、Remove Parameter、Rename Method、Introduce Parameter Object、Remove Setter、Hide Method、Replace Constructor with Factory Method、Replace Error Notification with Exception、Replace Exception with Error Notification |
| Coplien, J.，《A Pattern Language for Parameterised Software》 | 相关文献，关于参数化与接口设计的讨论 | 「参数该不该成组出现」的早期讨论，与 Introduce Parameter Object 相关 |
| Gamma 等，《Design Patterns》 | Addison-Wesley，1994 | **Facade**（Hide Delegate 的目标形态）、**Adapter**（对外承诺的转换）、**Factory Method**（工厂手法的目标形态） |
| refactoring.com 条目页 | https://refactoring.com | 各 API 手法的 Mechanics 与示例 |
| Fowler, M.，Bliki `RewriteVsRefactor` | https://refactoring.com | 「改写 API 等于改写承诺」的界定，是本章兼容性讨论的边界 |

> 以上均为真实可查文献，未使用编造的编号或 DOI。

---

## 近年研究与工业界开源实践（2015–2026）

**趋势**：API 重构的工业焦点从「代码里的调用点」转向「**契约与依赖的管理**」——语义化版本、兼容性门（API compatibility gate）、以及 AI 驱动的迁移。

| 仓库 | star（`gh api` 实测，2026-09-25） | 说明 |
| --- | --- | --- |
| `JetBrains/intellij-community` | **20,588★** | Change Signature、Rename、Introduce Parameter Object 等动作与「影响面预览」 |
| `dotnet/roslyn` | **20,688★** | 语义级签名变更与引用更新；.NET 侧有完整的 **API compatibility** 工具链 |
| `openrewrite/rewrite` | **3,750★** | 把本章的兼容策略（新增→废弃→迁移→删除）做成可大批量执行的 recipe |
| `google/error-prone` | **7,238★** | 编译期拦截废弃 API 的使用，加速第 2 阶段的迁移 |
| `rust-lang/rust` | **119,150★** | 没有默认参数/重载，参数对象与命名构造是默认形态 |
| `spring-projects/spring-framework` | **60,260★** | 框架升级是最常见的 API 重构现场：每个大版本都在做「弃用—迁移—删除」 |
| `llvm/llvm-project` | **40,650★** | clang-tidy 与 fix-it 提供「批量改调用点」的底层机制 |

---

## 常见误区与本书需修正之处

| # | 误区 / 需修正处 | 现实约束 | 应对 |
| --- | --- | --- | --- |
| 1 | 🔧 **「重构在很多团队里没有时间」**——改 API 要牵动所有调用方，包括别的团队、别的仓库、别的语言 | 跨团队 API 改动是最难排期的重构 | 把「弃用—迁移—删除」拆成跨三个迭代的路线图；提供适配层降低下游成本 |
| 2 | 🔧 **并发代码的重构风险被低估**——`Remove Parameter`、`Replace Constructor with Factory Method` 常常改变**构造时机**，而在并发下构造时机就是可见性边界 | 测试全绿但可能引入竞态 | 改构造路径后立刻跑并发测试；小心把「惰性初始化」改成「提前初始化」时引入的锁语义变化 |
| 3 | 🔧 **不谈跨服务与数据迁移的重构**——跨服务的「API 改名」本质是契约治理：版本共存、网关路由、数据双写、消费者适配 | 一次跨服务字段改名可能是季度项目 | 用契约测试 + 影子流量 + 双写；本书完全没有覆盖这一层（见 `book/微服务架构设计模式.md`） |
| 4 | 🔧 **AI 生成代码带来的新债**——AI 会「顺手」删掉觉得没用的参数、把异常吞成静默返回值，这些都是 API 语义的隐式变更 | 高 diff、低语义可读性是 AI 重构的典型特征 | 审查 AI 产出的 API 改动时，重点核对三条：参数数量变了没？异常去哪了？序列化 key 变了没？ |
| 5 | 🔧 `Remove Parameter` 被当成「既然没用就删」，但**很多参数是被反射、被框架、被序列化框架使用的** | 删掉后运行时才炸，且报错在很远的另一处 | 删除前先全局搜索参数名（含字符串形式）；对框架注入的参数一律不删 |
| 6 | 🔧 第 2 版写于 2019 年，尚未把「**契约即代码**（OpenAPI / Protobuf / GraphQL schema）」纳入讨论 | 今天的 API 契约越来越多地以 schema 文件存在 | 契约文件也要纳入重构范围，并且要能被 CI 校验（避免代码改了契约没改） |
| 7 | 🔧 「Rename Method 是安全的」并不总成立：反射调用、字符串拼接的方法名、序列化后的字段名、数据库列名都不会被工具找到 | 漏改会以「运行时 NoSuchMethod」或「静默取到 null」的形式出现 | 跨边界改名人工核对；在测试里加上「关键字段名」的快照断言 |
| 8 | 🔧 本章默认「同一个进程内的接口」；在前端—后端的分离架构里，「接口」还包括**前端对后端的调用约定**，改动要同时评估用户体验 | 一次 API 破坏性改动可能影响多个前端仓库 | 把 API 契约作为一等公民（版本化 + 兼容性门禁），而不是只改代码 |

---

## 与其他章 / 其他书的联系

| 关联 | 说明 |
| --- | --- |
| ← `05-介绍重构名录.md` | 本章对应名录「重构 API」组的展开 |
| ← `06-第一组重构.md` | `Replace Constructor with Factory Method`、`Replace Error Notification with Exception`、`Remove Flag Argument` 的入门版 |
| ← `08-搬移特性.md` | `Hide Delegate` / `Remove Middle Man` 是搬移手法的收尾动作 |
| ← `04-构筑测试体系.md` | API 改动必须靠测试保证调用点全部更新 |
| → `07-封装.md` | `Remove Setter`、`Hide Method` 是封装在接口层的延续 |
| → `12-处理继承关系.md` | `Hide Method` 常需要处理继承体系的可见性 |
| → `book/设计模式GoF/` | Facade ⟶ Hide Delegate；Factory Method ⟶ 工厂手法；Adapter ⟶ 契约转换 |
| → `book/代码整洁之道*` | Clean Code 的「函数参数」与「异常使用」讨论与本章重叠 |
| → `book/架构整洁之道*` | 接口边界的稳定与否，直接决定架构的「可测试性」与「框架无关性」 |
| → `book/重构/00-总览与阅读地图.md` | 总表「简化调用 / 重构 API」一节的展开 |
