# triton

https://github.com/JonathanSalwan/Triton

Triton is a Dynamic Binary Analysis (DBA) framework. It provides internal components like a Dynamic Symbolic Execution (DSE) engine, a dynamic taint engine, AST representations of the x86, x86-64, ARM32 and AArch64 Instructions Set Architecture (ISA), SMT simplification passes, an SMT solver interface and, the last but not least, Python bindings.

部署运行你感兴趣的模型镜像
Triton 基于 python 的 DSL，面向 GPU 体系特点，自动分析和实施神经网路计算的分块，triton 既是语言，也是编译器。

1 triton 的定位
TVM、XLA，能实现从模型到硬件的端到端的优化：

起点是深度学习模型，之后模型被转换成计算图，即一种数据结构，用于表示模型中的所有操作和他们之间的数据依赖关系。
在图表示的基础上，编译器应用多种优化策略来提高性能，例如合并操作，消除冗余
优化后的计算图会被转换成一系列的内核，kernel，是实际执行计算的代码
最终，将 kernel 部署到目标设备上执行
但是多数情况下，TVM/XLA 生成的代码性能不如供应商算子库。
triton 通过提供领域特定的语言和编译器，直接面向底层的 kernel 开发和编译优化问题，使得开发者能够以更高抽象层次编写高效的 GPU kernel，从而提升性能。
