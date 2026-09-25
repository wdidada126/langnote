# CSE466 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| "Smashing the Stack for Fun and Profit" (Aleph One) | 1996 | 栈溢出 + shellcode 的原始蓝图 | L3, L5, L8 |
| The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls (Shacham) | 2007 | ROP 的形式化起点：无函数调用的图灵完备控制流 | L9 |
| JITLeak: Just-in-Time String Leaking in JavaScript Engines (Lazar et al.) | 2020 | JIT 优化字符串成泄露/攻击面的代表作 | L11 |
| angr: Symbolic Execution and Program Analysis (Shoshitaishvili et al.) | 2016 | 二进制分析平台 angr 的方法学（CFG/模拟执行） | L7 |
| Efficient Software-Based Fault Isolation (Wahbe et al.) | 1993 | 纯软件沙箱隔离，SFI 是 seccomp 前思想源 | L4, L14 |
| Capsicum: Practical Capabilities for UNIX (Watson et al.) | 2010 | 能力模型落地 FreeBSD，限制提权爆炸半径 | L14 |
| House of Orange: A New glibc Heap Exploitation Technique | 2016 | 无泄露下劫持 top chunk 的堆利用里程碑 | L10 |
| 格式化字符串漏洞原始披露文档 (2000) | 2000 | printf 家族变成任意读写原语 | L10 |
| 内核提权技术文章谱系："Writing Kernel Exploits" (Phrack) 及 KernelCTF 生态 | 2006+ | commit_creds/modprobe_path 等提权原语教学化 | L12 |
| kAFL: Hardware Goes Back to (Software) Debugging | 2017 | 利用 PT 硬件虚拟化的内核 greybox fuzzing | L12, L13 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| HyperCanary: Detecting All Buffer Overflows in the Heap | IEEE S&P 2021 | 硬件 tag 支持下的堆溢出全检测实验 | L10, L14 |
| JITpoking: Bypassing CfGuard for JavaScript in Firefox | 2022 | JIT 读原语绕过 Firefox 类型防护 | L11 |
| StackWarp: Breaking Intel Stack Engine | 2023 | 微结构缓冲干扰导致跨特权数据注入 | L12, L13 |
| GhostWrite: (GPU 驱动层) 无写内存破坏 | USENIX Sec 2024 | 驱动 DMA 路径成为通用内存破坏原语 | L12 |
| ret2page: A New Page-Face — 利用页缓存侧信道削弱 Linux 内核 ASLR | 2022 | 新型泄露原语挑战内核缓解假设 | L10, L12 |
| syzbot/Continuous Kernel Fuzzing 效果测量与 CVE 归因研究 | 2021–2025 | Syzkaller 生态产出的量化评估 | L12, L13 |
| DARPA AIxCC 自动 pwn/修补系统报告 | 2024–2025 | 自动发现与自动修复真实代码库漏洞的新范式 | L13, L14 |

## 知识点在开源项目中的应用

> 按要求映射 pwn.college / CTF / Syzkaller 生态。

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| 滥用与 IPC（L1–L2） | pwn.college、linPEAS、pspy | dojo 关卡；本地枚举工具 |
| Shellcode（L3–L4） | pwntools（shellcode 模板/编码器）、shellcoder、libc-database | 生成-汇编-验证与 libc gadget 基座 |
| 逆向（L5–L7） | Ghidra、radare2/rizin、pwndbg/GEF、angr | 反汇编/符号执行混合分析 |
| ROP/控制流劫持（L8–L9） | ROPgadget、ropper、one_gadget、angr | gadget 挖掘与链构造 |
| 堆与内存错误（L10） | how2heap (shellphish)、glibc 源码、checksec | 分配器利用教学靶与加固检测 |
| JIT 攻击（L11） | Fuzzilli、BrowserFuzzingFoundation | JS 引擎结构化 fuzz 与利用研究基座 |
| 内核（L12–L13） | Syzkaller（fuzzer + syzbot 公共实例）、kAFL、KernelCTF / kernel-exploit-factory | 内核 fuzz/提权靶场 |
| 沙箱与竞态（L13–L14） | gVisor、seccomp（systemd/nspawn 配置）、raceforge 风格竞态脚本 | 生产级沙箱与竞态工具链 |
| CTF 生态 | CTFd、picoCTF、DEF CON CTF（公开 final 靶与题解包） | 赛制练习与赛后研读 |
