# Stanford CS242 — 逐讲要点骨架

> 骨架级要点；填充时对照课程笔记与作业 README 展开。

## L1 课程导论
- PL 教育的双痛点：纯理论课"学不会用"，系统课"用而不明"。
- 本课程主张：以系统编程问题反向引入理论概念。
- 工具链：OCaml（dune/opam）+ Rust（cargo）双语言贯穿。
- 评价方式：8 次作业 + 1 个大作业，全部有本地测试。

## L2 JSON 形式化与证明
- 语法（grammars）→ 语义（judgments）→ 类型（well-typedness）三段式。
- 归纳定义与规则式推理：数学归纳/结构归纳起手式。
- 证明"形式化不是装饰"：确定性、规范化等性质。
- HW1 用 Lean 或纸笔证明，取决于当期版本。

## L3 Lambda 演算
- 词法/对象级变量、α-等价、β-规约；替换的定义与捕获避免。
- 规范化策略与 Church-Rosser 直觉。
- 编码一切：Booleans/Naturals/Rec（Y 组合子）。
- 与 L5 解释器实现直接挂钩。

## L4 OCaml 函数式编程
- 代数数据类型 + 模式匹配 = 语法树即数据类型。
- 高阶函数、递归与尾递归；不可变优先风格。
- dune 工程结构与 utop 调试。
- 为后续所有 HW 建立手感。

## L5 类型检查器与解释器（经典作业）
- 从 λ→ 到多类型（unit/bool/integer/pair/function）。
- 进度保持（progress）+ 类型可靠（preservation）= 类型安全。
- 求值策略：call-by-value 与惰性扩展。
- 报错信息设计：检查器的可用性也是工程。

## L6 WebAssembly
- 栈式虚拟机模型、模块/函数表/内存对象；binary/text 格式。
- 类型系统如何保证运行时安全（无 trap 的控制流）。
- 与 JS 边界交互与沙箱语义。
- HW：读/解析/执行 Wasm 字节码子集。

## L7 线性类型与 Rust 所有权
- 线性/相关类型：变量恰用一次→资源管理自动化。
- move/borrow/lifetime：Rust 是线性类型的工程化子集。
- Drop 检查与"use after free"在编译期消失的原理。
- HW：给迷你语言实现所有权检查器。

## L8 Rust 异步
- Future/poll/waker：异步的状态机本质。
- async/await 语法脱糖；Send/Sync 自动派生。
- 与所有权交叉的坑：自引用 Future、Pin。
- HW：手写 executor + channel 用例。

## L9 类型化状态机与会话类型
- 把协议写进类型："没发握手就调 API 不能通过编译"。
- 会话类型：双向消息协议的类型对偶性。
- Rust typestate 惯用法：PhantomData/泛型参数进结构体。
- HW：session-typed TCP 库设计。

## L10 大作业工作坊 I（形式化验证线）
- Lean：定理证明器工作流与 Mathlib 生态。
- F*：验证文件系统正确性（可对照 fstar-examples）。
- 选型指导：验证线 vs 系统线的个人取舍。

## L11 大作业工作坊 II（系统实现线）
- Rust 实现 Read-Log-Update：并发数据结构验证思维。
- OCaml 迷你深度学习框架：函数式自动微分（AD）+ 类型驱动设计。
- 两条线的共同点：用类型消灭一类运行时 bug。

## L12 总结与迁移图谱
- 复盘：L2-L5 理论→L6-L9 系统→L10-L11 综合的"接地"路径。
- 一图流：每个理论概念对应它防住的真实 bug 类别。
- 后续路线：CS242 深读清单（TAPL 余下章节/程序分析/PL 顶会入门）。
