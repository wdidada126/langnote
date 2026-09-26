# 09 · 轻量级 AOP 库与 IoC 容器（原书第 10、11 章）

> 覆盖原书第 10 章（10.1 AOP 介绍 / 10.2 简单实现 / 10.3 轻量级 AOP 框架）与第 11 章
> （11.1–11.7：IoC 概念、对象创建、类型擦除常用方法、Any+闭包、依赖创建、完整容器）。
> 两章共用同一块底座——**用闭包和 Any 把异构对象同构化**，合并为一个文件。
> 大纲形态见 [../深入应用C++11.md](../深入应用C++11.md)；返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **面向切面编程** — AOP (aspect-oriented programming)：把日志/计时/事务等横切逻辑从业务里抽出，织入调用路径。
- **织入** — weaving：运行期用装饰闭包包住原函数（`before → core → after`），C++ 里就是函数的高阶包装。
- **环绕通知** — around advice：切面拿到控制权并能决定原调用是否执行/何时执行——异常安全协议由此而来。
- **控制反转** — IoC (inversion of control)：对象的创建权从调用方上收到容器。
- **依赖注入** — DI (dependency injection)：IoC 的主流实现，构造参数由容器解析供给。
- **注册表/工厂** — registry & factory：`map<string/name, function<T>()>` 形态的创建协议。
- **类型擦除同构化** — type erasure：注册异构服务到同一容器的前提——Any（值擦除）或 function（签名擦除）。
- **Any + 闭包** — 书中 IoC 的双擦除配方：闭包擦掉构造签名，Any 擦掉实例类型。
- **悬垂依赖/单例地狱** — 容器要解决的问题清单：手工 new 的耦合与生命周期失控。
- **bad_any_cast** — `std::any_cast` 的类型不匹配异常，运行期类型协议的双刃剑。

## 一、动机：Java 生态的两件武器，C++ 靠闭包复刻

AOP 与 IoC 在 2015 年的 Java 世界由 Spring 代理字节码生成实现。C++ 没有反射与运行时代理，
但有了 C++11 的 lambda 闭包、`std::function`、可变参数模板与 tuple，祁宇的答案是：
**横切=函数装饰器，注入=类型擦除工厂**。两章代码全部进 cosmos 的 `Aspect.hpp / Ioc.hpp /
Any.hpp / function_traits.hpp`（实测均在该仓库顶层）。

## 二、机制

### 2.1 AOP 的 C++ 形态：高阶函数包住成员函数
```cpp
// 🔧 复刻机制（实测 ch09.cpp）：切面 = before/after 两个闭包 + 原函数
template <class F>
std::function<int(int)> with_log(F&& core, const char* tag) {
    return [core = std::forward<F>(core), tag](int x) {
        std::cout << "[before] " << tag << "\n";
        int r = core(x);                      // 环绕点：异常/短路策略都在此
        std::cout << "[after ] " << tag << "\n";
        return r;
    };
}
```
书中框架版再加注册表（按类型/名字挂切面链）。要点与坑：切面链是 `function` 套 `function`，
**每层一次间接调用**（01 章成本账）；成员函数织入需把 `this` 捕获进闭包，悬垂纪律同观察者模式
（[07 章](07-C++11重思设计模式.md)）。ScopeGuard（[03 章](03-type_traits与可变参数模板.md)）是它的
近亲：AOP 管"进出的额外动作"，ScopeGuard 管"无论如何都要做的退出动作"。

### 2.2 IoC 容器的最小闭包：注册 → 解析 → 组装
注册即把 `[] { return new Service(...); }` 的**结果**塞进 `unordered_map<string, Any>`——
闭包擦掉构造签名，Any 擦掉实例类型；解析时按名取回、`any_cast<T>` 还原；依赖解析则把
"构造函数参数表"当递归问题：用 `tuple + function_traits`（[03 章](03-type_traits与可变参数模板.md)）
从签名拆出每个依赖类型逐个向容器索取。**类型系统承担了 Java 反射注解的活**。

### 2.3 Any 的实现选型（书中自研 vs 后到标准）
自研版（3.3.5 同款）：基类指针 + 模板派生 holder，`type()` 比对 `typeinfo`；
`std::any`（C++17）：单指针 + SBO（libstdc++ 实测 `sizeof(std::any)=16`，容纳平凡小对象免堆分配）。
擦除深度与代价：`any` 比 `function<void()>` 重（存值），比 `variant` 轻（不带封闭类型集检查）。

## 三、权衡与实战提示

- 运行期容器换不来编译期依赖检查：解析失败从"链接期符号缺失"退化为"运行期 bad_any_cast"——
  容器边界要窄（进程装配点），业务内部仍用显式构造。
- AOP 链在热点路径的开销可测量（每层 function 调用 ≈ 间接跳转 + 可能堆分配）；本书"轻量级"
  的限定词是诚实的。
- 循环依赖检测是完整容器的必需件（书 11.6 的解析栈即为此），复刻时不要省。
- 切面要"包住任意签名"就得对每个 arity 写一份 `function` 类型——03 章 function_traits 正是把这件事
  做成通用的零件；书 10.2 的泛化版即此形状。
- IoC 注册表是进程级可变状态：并发注册/解析要锁，且"注册已完成"是隐式时序假设——单测反序装配、
  动态加服务时最容易踩；现代框架用"装配期一次性构建 + 运行期只读"化解。

## 四、相邻概念对比

| 对比 | 差异一句话 |
| --- | --- |
| AOP 织入 vs ScopeGuard | 前者改调用路径，后者改退出路径；异常安全通常两者都要 |
| IoC vs 单例 | 单例=依赖隐式全局获取，IoC=依赖显式装配注入（[07 章](07-C++11重思设计模式.md)的退路） |
| Any 擦除 vs function 擦除 | 擦"值类型" vs 擦"调用签名"；容器常两者叠加 |
| 运行期 DI vs 编译期组装 | 模板/工厂在编译期完成同类工作的对照组（03 章 function_traits 即零件） |
| 装饰器链 vs 中间件栈 | 同一种高阶包装，粒度不同：前者包单个函数，后者包协议边界（HTTP/RPC） |

## 五、实测（🔧 三档：g++ 15.2，gnu++11/17/23，`ch09.cpp`）

```text
gnu++11: OK  [before] square / [after ] square -> 36 / ioc resolved via closure factory
             / "pre-C++17: 无 std::any（书中第11章自研正是补此空缺）"
gnu++17: OK  追加 std::any=42 / sizeof(any)=16 / bad_any_cast caught
gnu++23: OK  同 17
```

- `sizeof(std::any)=16`（两个指针形态）与自研 Any（`void* + 函数指针` 同尺寸）实测对齐——
  书中复刻版与标准版布局同构，替换无痛。
- 装饰闭包 `with_log` 三档一致：AOP 机制**不依赖 14/17 新件**，这正是它 2015 年可行的原因。
- `bad_any_cast caught` 段仅 17/23 档出现，11 档打印"无 std::any"——自研 Any 的解析失败在那个年代
  只能靠错误码或 UB 现场，异常协议本身就是标准化的红利。

## 六、最新演进与工业实践

- **C++17**：`std::any/optional/variant` 入库，书中自研 Any/Optional 的生产理由消失
  （对照 [03 章](03-type_traits与可变参数模板.md) 演进节）；CTAD（P0091R4 实测）让注册宏进一步减少。
- **C++20**：concepts（P0734R0 实测解析）把 `any_cast` 的运行期类型赌局改写成编译期约束的工厂模板；
  ranges 让"注册表遍历装配"写法现代化。
- **DI 生态**：boost.di（编译期注入库）证明另一条路线（零运行期查找）可行但未获标准接纳 ⚠️；
  2026 年工业 C++ 的主流仍是"显式装配 + 少量类型擦除边界"，本书两章的分寸感依然成立。
- **AOP 的日志切面对账（本次任务要求的库血缘项之一）**：Google glog（[google/glog](https://github.com/google/glog)）
  经 GitHub API 实测**已归档**（archived=true，最后 push 2025-05，最新 release v0.7.1/2024-06）；
  其依赖与工具链转向 abseil（[abseil/abseil-cpp](https://github.com/abseil/abseil-cpp)，实测活跃、
  release 20260817.0）——"横切逻辑标准化"如今由 `absl::LogSink` 与各框架中间件承担，
  gtest（独立仓库 googletest，最新 release v1.18.0/2026-08-10 实测）则把测试织入工程流水线。
  本书未用这三个库做案例（案例是 sqlite/rapidjson/TBB/PPL/asio），此处按任务口径给出对账：
  **2015 年"Google 开源四件套"（protobuf/glog/gtest/eigen）已各自迁移或换血，见 [11 章](11-LINQ并行任务与异步网络.md)。**
- **延伸阅读**：[../C++API设计.md](../C++API设计.md)（Reddy）谈接口层的隐式装配代价；
  教程线 [../modern-cpp-tutorial.md](../modern-cpp-tutorial.md)。

## 七、交叉互链

- 大纲：[../深入应用C++11.md](../深入应用C++11.md)；总索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 上游章：[03 章自研 Any/ScopeGuard](03-type_traits与可变参数模板.md)、[04 章 shared_ptr 对象图](04-智能指针与内存管理.md)、[01 章 function 成本账](01-更简洁更现代的C++11.md)
- 下游应用：[10 章消息总线（注册/分发同款底座）](10-消息总线与SQLite封装.md)
- 条款版：[../Effective_Modern_C++/06-lambda表达式.md](../Effective_Modern_C++/06-lambda表达式.md)（闭包即对象）
- 教程线：[../现代C++实战30讲/10-可变模板tuple与类型擦除.md](../现代C++实战30讲/10-可变模板tuple与类型擦除.md)、[../C++代码整洁之道.md](../C++代码整洁之道.md)
- 辨析：[../C++实战.md](../C++实战.md)（课程书无自研容器环节）
