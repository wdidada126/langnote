# CS110L 讲义要点（骨架，按 Spring 2020 slides 主题）

## L1 导论：为什么 Rust
- C/C++ 内存错误（泄漏/UAF/double free）在系统软件中的代价。
- Rust 目标：零成本抽象 + 编译期内存安全，无 GC。
- cargo/rustc 工具链与课程项目结构。

## L2 Rust 基础语法
- 表达式为中心的语言；绑定与可变性 (`mut`)。
- 基本类型、元组、数组与切片。
- 函数与模块可见性 (`pub`)。

## L3 所有权与借用
- 移动语义默认化：每个值有唯一 owner。
- 借用规则：多个 `&T` 或一个 `&mut T`，编译器强制。
- 生命周期标注初探；对照 C++ 引用悬垂问题。

## L4 Trait 与泛型
- Trait 作为接口/约束；单态化与 dyn 动态分发的取舍。
- 常用标准 trait：Display、From、Iterator。
- Operator overloading  via traits。

## L5 数据结构与错误处理
- Vec/HashMap、Option/Result 消灭 null。
- `?` 操作符与错误传播；Lab 测试驱动。

## L6 闭包与迭代器
- 三种捕获环境（&、&mut、move）。
- 迭代器适配器惰性求值；对照 C++ STL 与 Java Stream。

## L7 智能指针与内部可变性
- Box/Rc/RefCell/Cell；Rc<RefCell<T>> 组合模式。
- 与 C++ shared_ptr 的对照及循环引用问题。
- Deref/Drop trait。

## L8 线程与并发基础
- `thread::spawn` + join；Send/Sync 类型级线程安全。
- mpsc 消息传递 vs Mutex 共享内存。
- Project1：ptrace 实现迷你 debugger（断点/单步/寄存器）。

## L9 Futures 与异步
- Future trait、poll/waker 模型；async/await 语法。
- 与 epoll 事件循环的对应关系。

## L10 并发范式对比
- 进程/线程/异步 I/O/actor 的隔离性与扩展性权衡。
- Project2：负载均衡器多方案实现与压测比较。
