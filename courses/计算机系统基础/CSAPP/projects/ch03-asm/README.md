# ch03-asm —— 机器级程序：C → x86-64 对照练习集

**关联讲次**：L04（寄存器/操作数/算术）、L05（控制流）、L06（过程/栈帧）、L07（结构/对齐）。

## 内容

`src/funcs.h` + `src/funcs.c`：8 个小函数，每个函数头部注释给出
**预期汇编要点**（AT&T 语法，gcc `-Og` System V ABI）。本项目的玩法：

1. 先自己预测每个函数的汇编；
2. 反汇编对照；
3. 解释每一处不一致。

```sh
# Linux/macOS
gcc -Og -std=c99 -Wall -Wextra -c src/funcs.c -o bin/funcs.o
objdump -d bin/funcs.o | less
./build.sh            # 编译+运行+自动尝试反汇编
```

```bat
:: Windows（需 vcvarsall x64 环境）
build.bat             :: 生成 funcs.asm 清单 + 可执行
cl /O2 /Fe:bin\funcs.exe src\funcs.c /Fabin\funcs.asm
dumpbin /disasm bin\funcs.obj   :: 或用 /Fa 清单
```

## 观察清单（对应讲次）

| 函数 | 观察点 | 讲次 |
| --- | --- | --- |
| `add` | 参数在 `%edi/%esi`，返回值 `%eax` | L04 |
| `scale7` | 第 7 参在栈上；`lea` 当廉价 ALU | L04 |
| `pick` | `-Og/-O2` 下是否用 `cmov` 消灭分支 | L05 |
| `sum_to_n` | for→guard+do-while 的 `jmp` 进测试 | L05 |
| `rfact` | 帧上保存 n；`imulq` 收尾；call/ret | L06 |
| `bump` | 偏移 0/8/16 与 `sizeof=24`（padding） | L07 |
| `row_sum` | 双重解引用：行指针 + 4 倍标度 | L07 |
| `xor_swap` | 内存操作数读写序、`(%rdi)` 别名 | L04/06 |

> 注意：MSVC 用 Microsoft x64 调用约定（前 4 参 rcx/rdx/r8/r9，且返回 double 用 xmm0），
> 与 gcc 注释有差异——这本身就是 L06"调用约定"的活教材。
