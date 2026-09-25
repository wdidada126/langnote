# CS220 讲义要点（骨架，按 2025 版 slides 主题）

## L1 导论：Programming Principles 指什么
- 不是"Rust 语法课"：以原理视角（抽象、类型安全、语义）重学编程。
- 课程结构：slides + Rust Book 自学 + 大量带测试的 homework。

## L2 Rust 基础
- 绑定/mut、阴影 (shadowing)、表达式语义。
- 函数、类型系统基本面貌；cargo 工作流。

## L3 枚举与代数数据类型
- Option/Result 消灭 null；sum × product types 的代数观点。
- 模式匹配穷尽性与解构 (destructuring)。

## L4 Trait 与泛型
- trait bound、默认实现、对象安全。
- 单态化 vs dyn：抽象的运行时成本。

## L5 所有权与借用
- move 默认、Copy trait 的例外；借用检查规则。
- 用 homework 反复训练"编译器对话"能力。

## L6 生命周期
- 函数/结构体上的生命周期参数；'static 误区。
- 生命周期是类型系统的一部分而非 GC。

## L7 闭包与迭代器
- Fn/FnMut/FnOnce 与捕获类别。
- 迭代器组合子写声明式代码；性能与手写循环对比。

## L8 智能指针
- Box/Rc/RefCell；为什么 Rust 需要显式别名可变控制。
- 图/树结构与循环引用破解 (Weak)。

## L9 错误与测试
- Result 组合子链、自定义错误类型。
- cargo test/基准；作业均以测试为验收。

## L10 并发基础
- 线程与 mpsc；Send/Sync 如何在类型层面阻止数据竞争。
- Mutex<T> + Arc 的惯用组合，为 cs431 铺路。

## L11 unsafe 与扩展（若当期开设）
- unsafe 的契约：正确性责任转移给程序员。
- 宏与元编程初览。
