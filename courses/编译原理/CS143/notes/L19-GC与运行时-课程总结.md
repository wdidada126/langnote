# L19 GC 与运行时支持：课程总结

> 讲次：CS143 L19 ｜ 阅读：龙书 ch7.5 + Aiken GC 讲义 ｜ 收官讲：把 L11/L18 欠下的"堆的债"还清

## 核心概念

### 引用计数（RC）
```
inc/dec 伴随每条 MOVE/参数传递/赋值——编译器的"簿记税"。
优点：增量、实时、无暂停、实现直观（CPython 至今混合使用）。
缺点：循环垃圾必须靠额外机制（周期扫描/weak 表）；缓存行争用（多线程 dec 同一头）——
计数器放对象头 = 伪共享，现代系统把计数分散或延迟批量处理（WebKit/Swift 的 side-table）。
```

### 标记-清除家族（追踪式 GC）
- Mark-Sweep：从根集 DFS 标记可达 → 清扫未标记。碎片化 → 引出 Mark-Compact（3 指针拷贝式整理）。
- Mark-Release / 增量写屏障：三色抽象（白=待探、灰=在界、黑=已完成）——**写屏障代码是编译器在 L15/L18 发射的**：赋值 `x = y` 后插 `barrier(x, y)` 维护"黑不指白"不变式。
- Copying（Cheney 2-space）：无碎片、分配=p 指针 bump；代价=空闲减半 + 对象移动需要"更新全部引用"——句柄/间接指针方案。
- 分代假说：大部分对象早死 → 年轻代小、复制廉价；年老代标记整理为主。G1/ZGC/Shenandoah =  Region 化增量并发整理的工程史。
- 精确 vs 保守 GC：COOL 保守（把栈上所有字当指针，靠类型标签校验）——**精确 GC 要求编译器为每点发射"指针掩码/元数据"**（L11 的 CFI 同族义务）。

### 运行时库清单（PA5 的 hidden dependencies）
- 字符串拼接/比较/substr/int2str（COOL 的 String 方法全部是运行时调用）。
- IO：out_string/out_int；abort；`new` 分配器；GC hooks。
- 这些函数在 COOL 运行时以 `.cl` 库源码形式提供（cool-runtime）——学生第一次体会"编译器与运行时 ABI"：名字 mangling、隐藏参数（self/classinfo）都必须在两侧一致。

### 课程总结视角：你刚刚亲手造过的东西
- 阶段流水线（L1）、DFA 词法器（L3-4）、bison+AST（L5-8）、SDD/属性（L9）、符号表类型检查（L10）、帧布局与调用约定（L11）、IR+翻译模式（L12-13）、数据流（L14）、指令选择与调度（L15）、着色（L16）、SSA 与优化族（L17）、特征表派发（L18）、GC（L19）。
- 一句话：**编译器 = 在"保留语义合同"约束下对程序做的保序重写**。

## 与前后讲的联系
- 收束：L11 帧=GC 根；L18 对象头=标记依据；L15-L16=发射屏障的预算；L14=逃逸分析（堆/栈分配决策的数据流应用）。
- PA5 之后无 PA，但课程论文/考试覆盖全部——本讲建议回头重做 HW4/HW5 自查。

## 跨课程联系
- **6.S081**：内核无 GC（引用计数 kfree 纪律）；用户态 ASLR/COW fork 与 copying GC 的"移动+重映射"共享页表技巧。
- **CS149/MIT6.824**：并行/增量 GC = 并发标记的着色不变式（Dijkstra 三色 ≈ 分布式快照 Chandy-Lamport）——两门课在同一个不动点上会师。
- **CS229/MLC 类比**：训练框架的显存管理（张量生命周期 + 释放时机 ≈ 静态 GC 插入：Hooper&Cooper "memory retention" 问题）；`torch.no_grad`/in-place 改写影响 autograd 图的存活 ≈ 写屏障语义。
- **CSAPP**：malloc/free 用户态分配器与 GC 的分工（C 手动、Java 托管）；dlmalloc 的 bins 思想与分代回收同构。
- **CS3110/CS242**：OCaml/Haskell 的 GC 是"函数式语言性能叙事"的主角——与 COOL 保守栈扫对照最见设计取舍。

## 开源项目中的应用
- **Boehm-Demers-Weiser GC（libgc）**：保守标记清扫，COOL 运行时可直接挂它——"最接近课堂的工业 GC"。
- **CPython**：RC + 分代循环垃圾回收器（gc module 的收集阈值即调参接口）。
- **Go runtime**：三色并发标记 + 写屏障（Dijkstra+Yuasa 混合），`GOGC`/`GOMEMLIMIT` 暴露 GC 调优——现代并发 GC 的最佳入门读物（官方 blog）。
- **V8**：Orinoco 年轻/年老双空间 + 增量起始标记；`performance.measureUserAgentSpecificMemory` 之类 API 让 GC 可观测。
- **Rust**：零 GC 路线——所有权系统把"收集期"提前到编译期（逃逸分析失败 ⇒ 编译错误而非堆分配）；`bumpalo`/arena 提供无收集替代——与 GC 互为镜像的设计空间。
- **Z3**：AST 大规模驻留场景用引用计数 + 延迟删除栈（avoid 递归析构爆栈）——RC 工程细节的漂亮案例。

## 延伸阅读
- 龙书 ch7.5；Jones, Hosking & Moss, "The Garbage Collection Handbook: The Art of Automatic Memory Management"（标准参考）。
- Boehm & Weiser 1988 "Garbage collection in an uncooperative environment"（保守 GC 原文）；Go 官方博客 GC 系列（"Visualizing, simplifying, and uniting GC metrics" 等）；CPython GC 设计备忘（python-dev 存档，Mark Shannon）。
- 并发标记正确性：Dijkstra On-line cycle detection 1978 → Yuasa 色变 1990 → Go/Shenandoah 工程实践（论文列表见 GC Handbook 第 10 章）。

## 自测问题
1. 给 `while(true){ new String(...) }`（无引用保存）：RC、保守标记、分代复制各如何回收？停顿画像是什么？
2. 写出三色不变式被"无屏障赋值"破坏的具体交错序列（并发标记 + mutator 改引用）。
3. COOL 为什么能保守？若做精确 GC，编译器必须为帧额外发射什么、在哪些点更新？（衔接 L11 的 CFI）
4. Rust 无 GC 的代价与收益各是什么？`bumpalo` 适合什么形状的程序、泄漏如何兜底？
5. 课程 19 讲里，哪三处"编译器义务"最终都由运行时元数据兑现？（提示：GC roots、CFI、typeID）
