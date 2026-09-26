# 09 发行（Release）版调试（对应原书第 9 章）

> 对应原书第 9 章「发行（Release）版调试」（✅ 章名双源核实）。节级目录（⚠️ 据豆瓣阅读电子书页 TOC）：
> 9.1 在VC中调试发行版、9.2 在gdb中调试发行版。豆瓣第 2 版页摘要示意为
> 「VC 去优化测试与保留优化调试、gdb 提取符号与调试版映射」（✅ 摘要级，细节未逐字核对）。
> 本章实测密度第三：`-O2` 调试的全部假象均为本机 gdb 17.1 + g++ 15.2 真实会话。

## 核心概念速览（中英对照）

- **发行版调试** — release debugging：在优化过（内联/重排/删除）的二进制上重建源码级现场。
- **as-if 规则** — 优化的合同：只要可观测行为等价，编译器可任意改写——「行号还在，程序已不是你的程序」。
- **序列点** — sequence points：优化后源码行↔指令的映射表；DWARF `.debug_line` 的**非单调**产物。
- **`-g` + `-O2` 共存** — 现代默认姿势：优化版二进制照样带调试信息，代价是变量可读性打折而非归零。
- **optimized out** — 变量彻底消失：位置表达式为空；`<optimized out>`/`value has been optimized out` 字样的真义。
- **@entry 值** — gdb 的「入参快照」：x86-64 SysV ABI 下寄存器存过即不可复得，gdb 按 DWARF 参数位置标 `n@entry=11`（本机实测）。
- **帧指针省略** — omit frame pointer（`-fomit-frame-pointer`，x86-64 默认开）：rbp 链断，回溯转依赖 `.eh_frame` CFI——Release 回溯的另一半答案（第 8 章）。
- **分离调试信息** — split debug info：`objcopy --only-keep-debug`/`--strip-debug`+`--add-gnu-debuglink`，或 `-gsplit-dwarf`(.dwo)；发行版「裸二进制+符号包」的标准工艺。
- **build-id** — ELF 内容哈希（`readelf -n`）：exe 与其符号包的关联键；debuginfod 的寻址单位。
- **符号提取与映射** — 原书 9.2 主线 ⚠️：从「调试版抽符号、发行版当目标」到「addr2line 离线翻译」，本质都是 build-id 匹配问题的不同包装。
- **PDB 匹配** — Windows 版：exe/dll 与 .pdb 的签名（GUID+age）一致才符号化——build-id 的私有格式同位体。
- **地址→行** — `addr2line`/`llvm-addr2line`：一行命令的离线符号化；崩溃日志方案（第 8 章 Crashpad）的原子操作。

## 动机：为什么「Release 才复现」不是玄学

三重机制叠加出「Debug 正常、Release 崩」的全部案例：

1. **优化暴露 UB**：未初始化值在 Debug 恰好是 0，Release 里寄存器复用后是垃圾；严格别名/溢出假设让
   侥幸代码当场变鬼（UB 清单见 [../cppprime.md](../cppprime.md) 相关讨论与 cppreference）；
2. **时序改变**：优化+内联改变竞态窗口（第 4 章）；assert 被 `NDEBUG` 删掉后，本该被拦的非法调用走得更深；
3. **现场退化**：真正的 bug 也许两个版本都在，只是 Debug 里 gdb 看得见、Release 里看不见——
   本章 90% 的篇幅是第 3 类：**信息问题，不是行为问题**。

## 机制：`-O2 -g` 的现场到底还剩什么（全部本机实测）

### 实验一：行号漂移与寄存器变量（opt.exe = wp.c 加 -g -O2）

```text
🔧 gdb -batch -x cmd6.gdb ./wp_O2.exe   # 脚本: start; next; next; p i; p sum; stepi; x/3i $pc; bt

Thread 1 hit Temporary breakpoint 1, main () at wp.c:2
2	int main(void) {
6	        sum += arr[i];          ← next 一次直接从第 2 行跳到第 6 行：第 3/4 行的初始化被向量化/折叠
$1 = 0                            ← p i：此刻读到的是寄存器实况(ebx)，语义已不属于「i==0 那一瞬」
$2 = 0
=> 0x...2885 <main()+53>:	lea 0x1774(%rip),%rcx
   0x...288c <main()+60>:	mov %ebx,%edx        ← 源码里的 i/sum 们活在 ebx 里
```

判读纪律：**Release 的「停在哪一行」是近似值，「x 的值」可能是别的变量的尸体**。
`disassemble /m`（源码/汇编交错）是唯一的诚实视图——编译器不骗人，行号表会。

### 实验二：变量到底会不会 optimized out（opt2.exe）

```text
🔧 break opt2.c:4; run; info locals; p i; p s
sumto (n=n@entry=11) at opt2.c:4
i = 1        ← 出乎很多人意料：GCC 15 -O2 下循环变量仍可显示
s = 1
```

**诚实结论（本机实测推翻常见教条）**：现代 GCC + DWARF **位置表达式/位置列表**让简单循环在 -O2 下
常常仍可观测（循环被高斯公式替换后反而无处可寻——本例 gcc 未替换）；真正消失的是**被完全吸收的中间量**
与**死代码删除路径上的行**。`x@entry=21` 这类 `@entry` 标注则提醒：参数在寄存器里被踩过后，
显示的是入口残值而非当前值——**「可读」与「可信」是两回事**，这是第 9 章的核心判断。

### 实验三：发行版的最小可调试构建

Windows/MSVC 侧（原书 9.1 路线的 2026 版 ⚠️ 原书细节未核对）：
`/O2 /Zi /Fd:out.pdb /link /PDBSTRIPPED`（发行丢 PDB、事故后按签名找回）；
「去优化测试」（/Od 复现对照）与「保留优化调试」（本笔记实验三）是原书点名的两种姿势（✅ 摘要级）。

Linux 侧符号工艺链（可逐环实操）🔧：

```bash
🔧 g++ -O2 -g -g1 prog.cpp -o prog            # -g1: 只留行号/函数级——生产常用折中
🔧 readelf -n prog | grep 'Build ID'          # 指纹
🔧 objcopy --only-keep-debug prog prog.debug  # 符号抽出（体积大但只此一份，进符号库）
🔧 strip --strip-debug prog                   # 发行用瘦身版
🔧 objcopy --add-gnu-debuglink=prog.debug prog  # 缝回指针
🔧 gdb ./prog                                 # 自动尝试加载 prog.debug
```

addr2line 离线翻译（本机实测，第 1 章同款）：
`addr2line -e wp.exe 0x140001440 → main / wp.c:2`。崩溃日志里 `module+offset` 的批量还原即
`addr2line -f -i -e exe addrs...`（`-i` 展开内联链——内联帧在 DWARF 里是子程序条目，
`info line *0x...`/`bt` 会显示 `inlined` 字样）。

## 权衡：生产环境该留多少调试能力

| 档位 | 构建 | 事后能力 | 体积/攻击面 |
| --- | --- | --- | --- |
| 裸发行 | -O2，strip | 只有地址；崩溃栈靠 `dladdr`+偏移 | 最小 |
| +build-id | 同上，保留 note | 符号包按指纹可寻 | +几十字节 |
| +调试符号分离 | -O2 -g1，strip 主件 | gdb 载 core 自动补符号 | 符号包 GB 级，离线管 |
| -gsplit-dwarf | 编译期就分家(.dwo) | 同+.dwo 缺失只丢细节 | 构建增量最优 |
| ASan 影子发行 | -O2 -fsanitize=address | 第 6 章全套 | 2~3 倍减速，灰度/金丝雀专用 |

2026 实践基线：**生产二进制 strip+build-id，符号包进 debuginfod/内部符号库，崩溃管线全自动符号化**——
「发行版不可调」在基建健全的组织已是历史问题；没基建的小团队从「表格第 3 行」起步最划算。

## 相邻概念对比

- vs 第 8 章：第 8 章管「现场怎么来」，本章管「现场能不能读懂」；同一份 core，符号匹配失败时两章内容互为表里。
- vs 第 10 章：`disassemble /m` 读机器码是本章的日常工具，第 10 章把它升格为「没有源码也能调」的正道
  （无源码补丁/破解向 ⚠️ 原书 10 章小节含此内容）。
- VS 的「Just My Code/优化代码」开关族解决的是**噪音过滤**（系统帧折叠），不解决**信息缺失**——
  别把设置面板当时间机器。

## 最新演进与工业实践

- **`-gsplit-dwarf`+`debuginfod` 合流**：发行版把 DWARF 切到 .dwo/debuginfod 服务端（dnf/debuginfod、
  elfutils），开发者侧 `gdb prog core` 首次自动 HTTP 拉符号（`accept-deletion` 提示）——
  「符号服务器」在 Linux 完成对 Windows 20 年前生态的追赶（第 2 章呼应）。
- **LLVM 侧**：`llvm-addr2line --inlines`、`llvm-dwarfdump`、`llvm-symbolizer` 速度/正确性全面压制 binutils
  对应物；Android 平台崩溃服务（`ndk-stack`/`llvm-symbolizer` 管线）是移动端默认形态。
- **Minidump 化日志**：不产整 core，只发「栈+寄存器+模块表」的 Crashpad 式小包（第 8 章），符号化在服务端
  ——发行版调试从「调试器会话」变成「数据流水线」，本章技能成为管线的最后一环。
- **MSVC 新趋势**：`/debug:fastlink`（PDB 增量巨型但链接快）+ 公共存储符号服务器；
  VS2022 的「IntelliTrace 现场快照」在 Enterprise 侧提供 Release 的 limited 历史调试 ⚠️ 支持范围凭记忆。
- **静态前移对照**：Release-only 鬼 bug 的终局解法常是**别在 Release 调**——`-O1/-Og` 二分、
  编译选项 bisect（`-fno-...` 逐个关回）比硬读 `disassemble /m` 更快；`-fno-omit-frame-pointer`
  保留回溯能力是性价比最高的一项（第 8 章 CFI 兜底之外的双保险）。

## 互链

- 在线断点/单步母章：[03-Linux下gdb调试基本功能.md](03-Linux下gdb调试基本功能.md)
- assert 消失与优化扰动：[02-VisualC++调试基本功能.md](02-VisualC++调试基本功能.md)、[04-多线程死锁调试.md](04-多线程死锁调试.md)
- 无 PDB 的 .dll/.so 栈：[05-调试动态库.md](05-调试动态库.md)
- ASan 在 -O2 上仍是第一推荐：[06-内存检查.md](06-内存检查.md)
- core/dmp 的符号化失败面：[08-转储文件调试分析.md](08-转储文件调试分析.md)
- 反汇编与无源码调试正道：[10-调试高级话题.md](10-调试高级话题.md)
- 对象在内存里的真实布局（读裸字节的前提）：[../深度探索C++对象模型.md](../深度探索C++对象模型.md)
- UB 与优化合同的语言侧：[../cppprime.md](../cppprime.md)
- 总索引：[../C++系列·总索引.md](../C++系列·总索引.md)、单文件：[../C++代码调试的艺术.md](../C++代码调试的艺术.md)
