# CSE466 学习要点提纲（骨架）

> 每模块/讲 3–5 条要点；不记录具体题解，只沉淀技术概念与通用方法论。

## L1 Program Misuse
- 不挖 bug 也能赢：解释器、编辑器、包管理器的「合法功能」提权路径枚举。
- 文件描述符、/proc、进程信号是本地信息收集的主干道。
- 环境审计思维：先画信任图（谁以什么权限跑什么）。

## L2 Program Interaction
- IPC 滥用：管道、unix socket、共享内存的鉴权盲区。
- 竞态雏形：TOCTOU 检查（为 L13 埋点）。
- 守护进程与计划任务：长期运行实体的攻击面。

## L3 Shellcoding
- 约束下写码：无 \x00、位置无关（PIC）、自定位（call-pop）。
- syscall ABI 手搓 exit/execve 最小 shellcode。
- 编码技巧：alpha32/xor 编码器绕过字符集过滤。

## L4 Shellcode 防御
- W^X/NX 如何终结「数据页直接执行」。
- 可执行内存的现实来源：JIT、mmap(PROT_EXEC) 滥用。
- 防御栈视角：seccomp + 沙箱限制执行语义。

## L5 函数帧与栈布局
- prologue/epilogue、saved rbp、返回地址的字节级心智模型。
- 栈上局部变量排布与 canary 位置。
- 用「读栈图」代替「猜」：逆向 pwn 题的第一步。

## L6 静态逆向
- Ghidra/IDA：交叉引用、函数识别、类型重建工作流。
- 识别编译器产物：-O2 后的循环/字符串混淆观感。
- 静态定位危险函数（system/execve/strcpy）作攻击面锚点。

## L7 动态逆向
- pwndbg/GEF 速查表：telescope、vmmap、hijack-flow。
- 断点策略：malloc/free 边界、one-gadget 距离测量。
- strace/ltrace 先看行为再看指令。

## L8 控制流劫持基础
- ret2syscall：寄存器约束达成 execve。
- ret2plt/ret2libc：借现成 PLT 与 one-gadget。
- 泄露先行：无信息泄露则 ASLR 不可越（leak→base→hijack 三段式）。

## L9 ROP 与栈迁移
- gadget 搜索与调用约定对齐（pop rdi; ret 链）。
- 栈迁移/pivot：ROP 链溢出短缓冲时的续命术。
- ret2csu/sigreturn(ROP) 等高级控制流技术谱系。

## L10 内存错误：格式化字符串与堆
- fmt string：任意读写原语（%n、偏移泄露）。
- glibc 堆：tcache/fastbin 的 free-list 投毒思路（House 家族概念）。
- UAF 与类型混淆：现代浏览器/内核漏洞的主流根因。

## L11 JIT 与现代执行体
- JIT spray：把编译器变成 shellcode 生成器。
- 浏览器 pwn 分层：渲染进程→沙箱逃逸→内核提权的链条观。
- WASM/托管语言环境下的新攻击面。

## L12 内核模块与提权
- 内核态调试环境：QEMU + kdump + 符号表。
- 模块即攻击面：copy_from_user 校验缺失、modprobe_path、commit_creds 原语。
- 缓解对照：SMEP/SMAP/KASLR 与用户态 payload 布局。
- 与 Syzkaller/kAFL 生态的衔接点。

## L13 System Exploitation 与竞态
- 本地提权链整合：从容器逃逸到 root 的路径设计。
- race condition 工具化：raceforge 思路、时间窗口放大与 CPU 亲和。
- UFFD/内核对象生命周期竞态（概念级）。

## L14 Sandboxing 与综合
- 沙箱三件套：seccomp-bpf、namespace、capabilities 组合语义。
- 已知绕过研究观感：内核接口攻击面收缩史。
- 期末 CTF 方法论：题面→假设→链设计→时间预算。
