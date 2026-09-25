# 第 10 章 CALL 和 RET 指令

> **一句话**：`call` 就是「把返回地址压栈，然后跳过去」，`ret` 是它的逆；把这两条与 `SS:SP` 组合起来，才第一次有了**栈帧**与**函数**，也才第一次需要认真回答「参数怎么传、现场怎么保」。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 `ret` 和 `retf` | 返回 | `ret` = `pop IP`；`retf` = `pop IP; pop CS` |
| 10.2 `call` 指令 | 调用 | `call` = `push 返回地址; jmp 目标` |
| 10.3 依据位移的 `call` | `call s` / `call near s` | 位移同样有 short/near 之分 |
| 10.4 目的地址在指令中的 `call` | `call far ptr s` | 压入 CS 与 IP |
| 10.5 目的地址在寄存器中的 `call` | `call ax` | 引出 C++ 虚函数的间接调用 |
| 10.6 目的地址在内存中的 `call` | `call word ptr [bx]` | 引出 C 的 `*_self` 回调表 |
| 10.7 `call`/`ret` 的配合使用 | 现场保存与恢复 | **函数的两条铁律**：不改应改的、栈必须平衡 |
| 10.8 `mul` 指令 | 乘法：`AX = AX × op` | 与 `call` 一起构成完整子程序 |
| 10.9 模块化程序设计 | 把功能封装成子程序 | 接口 = 入口参数 + 出口参数 |
| 10.10 参数和结果传递的问题 | 约定优于规则 | 寄存器传递的约定必须双方遵守 |
| 10.11 批量数据的传递 | 首地址 + 长度 | 用寄存器存「指针」 |
| 10.12 寄存器冲突的问题 | 谁保存谁 | callee-saved vs caller-saved 的原型 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建，不编译不运行**。

### 1) 栈帧是怎么长出来的（10.1–10.7）

```asm
; 教学示意，不参与构建
code segment
start:
    mov ax, 1000h
    mov ss, ax
    mov sp, 0100h            ; 设好栈

    call sub1                ; ① push 返回地址（call 的下一条指令偏移）
                             ;    → sp ← sp-2，ss:[sp] ← 返回偏移
                             ;    ② IP ← sub1

    mov ax, 4c00h
    int 21h

sub1:                        ; 子程序入口
    push bp                  ; 保存旧的 bp（现场）
    mov  bp, sp              ; bp 指向当前栈顶 —— 帧指针建立
    sub  sp, 4               ; 为局部变量留出 4 字节

    mov  ax, [bp+4]          ; 取参数（参数在返回地址之上）
    add  ax, [bp+6]
    mov  [bp-2], ax          ; 局部变量

    mov  sp, bp              ; 释放局部变量（等同 add sp,4）
    pop  bp                  ; 恢复旧的 bp
    ret                      ; pop IP → 回到 call 的下一条
code ends
end start
```

**栈帧图**

```text
高地址
 │  参数 2          ← [bp+6]
 │  参数 1          ← [bp+4]
 │  返回地址        ← [bp+2]（call 压入的 IP）
 │  旧的 BP         ← [bp]   （push bp 之后、mov bp,sp 之前）
 │  局部变量        ← [bp-2]
低地址 ← SP/BP
```

> 三条必须刻在脑子里的规则：
> 1. **进入子程序时栈上已经有了返回地址**，所以参数从 `[bp+4]` 开始（16 位），32/64 位下是 `[rbp+8]`。
> 2. **返回时栈必须完全平衡**：`ret` 会 pop IP，若你多 pop 或少 push，程序立刻飞掉。
> 3. 保存现场用 `push` 而不是「存到全局变量」——因为递归要求每次调用有独立现场。

### 2) `call`/`ret` 的机器级分解（10.2 / 10.7）

```asm
; 教学示意，不参与构建
; call near s   ≡   push IP的下一个 ; jmp near s
; ret           ≡   pop IP

; 远调用的情形：
call far ptr s  ≡   push CS ; push IP ; jmp far ptr s
retf            ≡   pop IP ; pop CS
```

### 3) 参数传递与结果（10.10 / 10.11）

```asm
; 教学示意，不参与构建
; 约定：AX 传结果，DS:SI 指向首地址，CX 传长度（"首地址 + 长度"范式）
mov ax, data
mov ds, ax
mov si, 0
mov cx, 5
call sum_words                ; 结果在 AX

sum_words:
    push bp
    mov bp, sp
    push cx                   ; 寄存器冲突：cx 正好是循环计数
    xor ax, ax
    mov bx, 0
s:  add ax, [si+bx]           ; 用 si 当指针
    add bx, 2
    loop s
    pop cx                    ; 恢复现场
    pop bp
    ret
```

### 4) `mul`（10.8）

```asm
; 教学示意，不参与构建
; mul 与 div 对称：被乘数隐含在 AL/AX（或 DX:AX）
mul byte ptr [bx]   ; AX = AL * op         （8 位乘法）
mul word ptr [bx]   ; DX:AX = AX * op      （16 位乘法）
```

### 5) 寄存器冲突与保存约定（10.12）

| 约定 | 谁负责保存 | 对应 x86-64 |
| --- | --- | --- |
| caller-saved（调用者保存） | 调用前自己 push | `rax, rcx, rdx, rsi, rdi, r8, r9, xmm0-15` |
| callee-saved（被调用者保存） | 函数入口 push，出口 pop | `rbx, rbp, r12-r15` |
| 共用约定 | 谁都不能破坏的 | 栈指针 `rsp` 必须与进入时一致 |

> 这正是 System V AMD64 ABI 的另一半。**本书教你用 MASM 自定义约定，ABI 是「被写进规范、被所有编译器遵守」的同一种约定。**

---

## 版本演进

| 年份 | 事件 | 关联 |
| --- | --- | --- |
| 1978 | 8086 已有 `call/ret`，但**没有**栈帧的硬件约定 | 帧指针全靠程序员手工维护 |
| 1985 | 80386：32 位 `call/ret`，`ebp` 作为标准帧指针 | 栈帧从约定变为事实标准 |
| 1990s | 编译器的 `-fomit-frame-pointer` | 帧指针让位于寄存器窗口 |
| 2003 | x86-64：`rsp` 16 字节对齐要求 + callee-saved 清单固定 | 函数接口规范化，跨语言 ABI 成为可能 |
| 2010s | CET / Shadow Stack 把返回地址保护交给硬件 | 面向 ROP 攻击的「ret」加固 |
| 2026 | Rust/Go/JIT 大量生成 x86-64 汇编 | 手写 `call/ret` 的场景集中在 JIT、补丁、内核 |

> 值得注意：**`call/ret` 这条指令串联了本书全部三条主线**——栈（Ch2/Ch3）、转移（Ch9）、标志与中断（Ch11/Ch12）。它是理解「函数调用 = 栈操作」的最小样本。

---

## 经典论文与原始文献

| 论文 / 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Intel 8086 Family User's Manual | Intel，1978 | `CALL/RET/RETF` 的压栈顺序定义 |
| Intel 386 Programmer's Reference Manual | Intel，1985 | 32 位栈帧与 `ebp` 的常规用法 |
| Intel SDM Vol.2 — `CALL`/`RET`；Vol.1 §6.3 — x86-64 栈规则 | Intel 在线发行版 | 包括「`call` 后 `rsp` 对齐 16 字节」的硬性要求 |
| AMD64 ABI（hjl-tools/x86-psABI 草案） | https://github.com/hjl-tools/x86-psABI | callee-saved 清单与栈对齐的**规范文本** |
| Agner Fog, *Optimizing Assembly*（"Calling Conventions" 一章） | https://www.agner.org/optimize/ | 各代 CPU 的调用约定与跳转表优化 |
| Bauman, *Return-Oriented Programming* / CVE 系列 | USENIX Security 论文体系 | 为什么返回地址保护（CET）值得做，以及它为什么被绕过 |
| Wikibooks *X86 Assembly* — Calling Conventions | https://en.wikibooks.org/wiki/X86_Assembly | 各类调用约定的自由教材 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：JIT（V8/Ruby/Java/Cranelift）与 FFI 让「手写 call/ret 规范」变成生成器的责任；同时 ABI 兼容成了跨语言互操作的关键。

| 仓库 / 项目 | star | 说明 |
| --- | --- | --- |
| `llvm/llvm-project` | 40,648★（实测） | `fastcc`/`coldcc`/`preserves-all`；`llc` 生成的 ABI 合规调用序列 |
| `rust-lang/rust` | 119,149★（实测） | `extern "C"` 与 `#[no_mangle]` 的 ABI 契约；`core::arch::asm!` |
| `gcc-mirror/gcc` | 11,261★（实测） | `-fomit-frame-pointer`、`-maccumulate-outgoing-args` 等 ABI 行为 |
| `torvalds/linux` | 250,106★（实测） | `arch/x86/` 的调用序列与 `-fno-omit-frame-pointer` 内核约定 |
| `hjl-tools/x86-psABI` | 396★（实测） | 规范本身；任何跨语言 ABI 问题的最终答案 |
| `openssl/openssl` | 30,844★（实测） | `OPENSSL_ia32asm` 调用约定与常量时间控制流 |
| `sqlite/sqlite` | 10,540★（实测） | `sqlite3_step` 的 C 与汇编混合接口 |

> 实测方式：`gh api repos/OWNER/REPO --jq '.stargazers_count'`，日期 **2026-09-25**。

---

## 常见误区与本书需修正之处

| # | 误区 / 待修正 | 说明 |
| --- | --- | --- |
| 1 | 🔧 「参数在 `[bp+0]`」 | 进入子程序时返回地址已经压栈，返回值/参数是 `[bp+2]`（IP）与 **`[bp+4]`**（第一个 16 位参数）。差 2 字节是汇编函数最常见的 bug。 |
| 2 | 🔧 「`ret` 之前不用管栈」 | `ret` 要 pop IP。如果函数里少 pop 一次或多 pop 一次，栈就失衡，返回地址会读错——症状是「莫名其妙跳到错误的地方」而不是崩溃提示。 |
| 3 | 🔧 「用全局寄存器传参数就行，约定随意」 | 约定随意意味着**你换一个编译器、或让 C 也调用它，就会全盘崩**。这就是 ABI 存在的理由；跨语言必须遵守 `hjl-tools/x86-psABI` 或 Microsoft x64。 |
| 4 | 🔧 「`call far ptr` 只是写法不同」 | 它是**同时改 CS 与 IP** 的远调用，栈上多压一个段值。在 32/64 位扁平模型里已不存在。 |
| 5 | 🔧 「递归函数需要特殊处理」 | 不需要特殊指令，但需要「现场保存到栈上」——正是 10.12 的要求。**不保存现场的函数无法递归**。 |
| 6 | 🔧 「x86-64 上手写 asm 也有 `[bp+4]`」 | 64 位下帧指针可省略、参数主要走寄存器（`rdi/rsi/...`）、还要满足 16 字节对齐。书里那套 `[bp+4]` 是实模式专属。 |
| 7 | 🔧 「手写汇编函数一定更灵活更快」 | 在 x86-64 上手写函数最容易输的地方恰恰是**参数命名的灵活性**（编译器能跨函数优化，手写函数被隔离在一个 translation unit 里）。 |
| 8 | 「`mul` 与 `div` 对称所以也一样快」 | `mul` 延迟远小于 `div`；`div` 在 x86 上可以贵到 30–90 周期，是除法慢的根源。 |

---

## 与其他章 / 其他书的联系

- 前承：`08-转移指令的原理.md`（`call` = push + jmp）；`05-包含多个段的程序.md` 的独立栈段是前提。
- 后承：`10-标志寄存器.md` 的 `cmp`/条件转移是子程序里 if/else 的实现基础；`11-内中断与int指令.md` 的中断过程本质也是「push 标志 + push CS/IP + 跳中断例程」。
- 与 `book/程序员的自我修养链接装载与库.md` 强相关：栈帧的进一步发展是栈回溯（unwind），是异常/崩溃分析的基础。
- 与 `book/链接器和加载器.md` 相关：跨目标文件的 `call` 需要重定位（CALL 分支的 `R_X86_64_PLT32`）。
- 与 `book/深入理解计算机系统/`（CSAPP 第 3、7 章）对照：过程抽象与动态链接的当代版本。
- 与 `book/计算机程序的构造和解释（原书第2版）/` 对照：它用间接求值解释「过程」的语义，能解释为什么栈帧是必要的。
