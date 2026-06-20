# tvm

*TVM*是一个用于深度学习系统的编译器堆栈。它旨在缩小以生产力为中心的深度学习框架与以性能和效率为中心的硬件后端之间的差距。

知乎 蓝色

https://github.com/apache/tvm

## 编程语言
python
c++

## 协议
apache

## 版本version
Apache TVM v0.22.0

## 编译源代码
https://tvm.apache.org/docs/install/from_source.html


TVM 深度集成了 LLVM 的多个核心模块，主要作为其可移植的后端代码生成器。以下是具体使用的功能模块：

1. 目标代码生成 (LLVM CodeGen)
主要用途：生成高性能目标代码

// TVM 使用 LLVM IRBuilder 生成代码
llvm::IRBuilder<> builder(context);
llvm::Function* func = ...;
builder.SetInsertPoint(...);

// 将 TVM 表达式转换为 LLVM IR
llvm::Value* llvm_value = codegen.VisitExpr(tvm_expr);

2. LLVM IR 中间表示
TVM 生成 LLVM IR，LLVM 负责优化和代码生成

; 生成的 LLVM IR 示例
define @vector_add(float* %A, float* %B, float* %C, i32 %n) {
entry:
  %i = phi i32 [0, %entry], [%i.next, %loop]
  %a_ptr = getelementptr float, float* %A, i32 %i
  %a = load float, float* %a_ptr
  %b_ptr = getelementptr float, float* %B, i32 %i
  %b = load float, float* %b_ptr
  %sum = fadd float %a, %b
  store float %sum, float* %C
  br label %loop
}


3. 目标平台支持 (Target Support)

利用 LLVM 的多目标支持

# TVM 中使用 LLVM 目标
target = tvm.target.Target("llvm -mcpu=skylake -mattr=+avx512f")
# 或者
target = tvm.target.Target("llvm -mtriple=aarch64-linux-gnu")


支持的架构：
• x86, x86-64

• ARM, AArch64

• PowerPC

• RISC-V

• NVIDIA GPU (通过 NVPTX)

• AMD GPU (通过 AMDGPU)

4. 自动向量化 (Auto-Vectorization)
利用 LLVM 的自动向量化优化
// TVM 生成可向量化的循环
for (int i = 0; i < n; i += 4) {
    // LLVM 会将其向量化为 <4 x float> 操作
    C[i] = A[i] + B[i];
}


5. 循环优化 (Loop Optimization)

使用 LLVM 的循环优化通道
• 循环展开 (Loop Unrolling)
• 循环融合 (Loop Fusion)
• 循环分发 (Loop Distribution)
• 循环向量化 (Loop Vectorization)

6. 内存优化

利用 LLVM 的内存优化

; LLVM 优化内存访问模式
%arrayidx = getelementptr i32, i32* %A, i64 %index
load i32, i32* %arrayidx


7. 目标特定优化

使用 LLVM 的目标特定 intrinsics

; 使用架构特定的 intrinsics
call <8 x float> @llvm.x86.avx.sqrt.ps(<8 x float> %a)


8. TVM 中的具体实现模块

Runtime 模块

// tvm/src/codegen/llvm/llvm_module.cc
class LLVMModuleNode : public runtime::ModuleNode {
    std::unique_ptr<llvm::Module> module_;
    std::unique_ptr<llvm::LLVMContext> context_;
    std::unique_ptr<llvm::ExecutionEngine> engine_;
};


CodeGen 模块

// tvm/src/codegen/llvm/codegen_llvm.cc
class CodeGenLLVM : public ExprFunctor<llvm::Value*(const PrimExpr&)> {
    llvm::IRBuilder<> builder_;
    llvm::Module* module_;
    llvm::LLVMContext* ctx_;
};

9. TVM调用LLVM的流程

# Python 层调用流程
def build_with_llvm(mod, target):
    # 1. TVM 计算图优化
    mod = relay.transform.OptimizeOnExpr(mod)
    
    # 2. 生成 LLVM IR
    with tvm.transform.PassContext(opt_level=3):
        lib = relay.build(mod, target="llvm")
    
    # 3. LLVM 优化并生成机器码
    return lib

# 使用示例
mod = tvm.IRModule.from_expr(expr)
lib = build_with_llvm(mod, "llvm")


10. 性能优化特性

TVM 利用的 LLVM 优化级别

# 对应 LLVM 的优化级别
with tvm.transform.PassContext(opt_level=0):  # -O0
with tvm.transform.PassContext(opt_level=1):  # -O1  
with tvm.transform.PassContext(opt_level=2):  # -O2
with tvm.transform.PassContext(opt_level=3):  # -O3

总结
TVM 使用 LLVM 的核心模块：
模块 用途 TVM 中的重要性
IR 生成 生成优化过的中间表示 ⭐⭐⭐⭐⭐
目标代码生成 架构特定的机器码生成 ⭐⭐⭐⭐⭐
向量化优化 SIMD 指令自动生成 ⭐⭐⭐⭐
循环优化 循环结构优化 ⭐⭐⭐⭐
内存优化 内存访问模式优化 ⭐⭐⭐
多目标支持 跨架构可移植性 ⭐⭐⭐⭐⭐

关键价值：TVM 专注于高层计算图优化和调度优化，将低层机器代码生成委托给成熟的LLVM后端，实现了可移植的高性能代码生成。
AI/大数据领域的"算子" 是指在数据流图上执行的基本计算操作单元。让我用通俗易懂的方式解释：