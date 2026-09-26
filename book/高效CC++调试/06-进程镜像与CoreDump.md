# 06 进程镜像与Core Dump（原书第 6 章）

> 覆盖《高效C/C++调试》**第 6 章**（6.1 二进制文件格式；6.2 运行期加载和链接；6.3 进程映射表：可执行文件/
> 共享库/线程栈/无名区域/拦截/链接时替换/预先加载代理函数/修改导入导出表/函数手术/核心转储文件格式/
> 核心转储分析工具；6.4 小结，原书 pp.142–170）。目录来源见 [../高效CC++调试.md](../高效CC++调试.md)。
> 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)。

## 核心概念速览（中英对照）

- **进程镜像** — process image：一次运行的全部内存视图：映射的文件段+堆+栈+匿名区，调试与 dump 的共同底图
- **ELF / PE** — Executable and Linkable Format / Portable Executable：Linux/Windows 二进制容器；节表与重定位结构决定加载器行为
- **虚拟内存区域** — VMA / memory mappings：`/proc/pid/maps`（或 Win 模块列表）逐行列出的地址区间及其来源文件
- **位置无关代码** — PIC / PIE：以 RIP 相对寻址+重定位表实现任意加载地址，ASLR 的前提
- **运行期链接** — dynamic linking：加载器解析 `.dynsym`/重定位项，把符号绑定到实际地址（lazy PLT）
- **PLT / GOT** — Procedure Linkage Table / Global Offset Table：函数/数据跨库间接跳转的两级垫片，**劫持与断点的高频目标**
- **拦截** — interposition：同符号多实现时按加载顺序先到先得——LD_PRELOAD 与 LD_DEBUG 的机制基础（6.3.5）
- **链接时替换** — link-time substitution：用 `-Wl,--wrap` 或同名强符号在链接期替换实现（6.3.6）
- **函数手术** — function surgery / detour：运行中改指令流（跳板/hook），调试器断点与热补丁的同一机制（6.3.9）
- **核心转储** — core dump：崩溃瞬间的内存+寄存器快照文件；`ulimit -c` 控制产生，`gdb prog core` 离线复活
- **minidump** — Windows 精简现场（附录 B.2）：可选只含栈/模块/线程，崩溃上报系统的事实标准容器

## 1. 动机：所有离线调试都在一张「地图」上工作

core/PDB/DWARF 三种载体（[01 篇](01-调试符号与调试器.md)）里，现场（core/minidump）就是本章的进程镜像
冻结版。**没有地图就没有取证**：垂直搜索要求判断「这个字是不是合法指针」→ 查它落在哪个映射区；
「变量怎么读都错」→ 符号文件与二进制映射基址不匹配；「崩在陌生 so」→ 无名区域里的 JIT/注入代码。

## 2. 机制

### 2.1 文件→内存：加载器干了什么（6.1/6.2）

ELF：段表（PT_LOAD）→ 每段一个 VMA；.text 只执行、.rodata 只读、.data/.bss 私有写；重定位分
RELA（加载即定）与 PLT/GOT（首调用才定）。PE：节表+DataDirectory 导入表；Windows 加载器以
section 粒度映射，DLL 基址靠重定位修复（ASLR）。两侧差异直接决定：
**GDB 在 Windows 原生环境不提供 `/proc` 视角**——🔧 **已实测**：

```text
(gdb) info proc mappings
Not supported on this target.
```

Windows 侧改用 `info files`、`info sharedlibrary` 或 WinDbg `!address`；WSL2 内跑 Linux 进程则一切照旧。

### 2.2 读懂映射表（6.3.1–6.3.4）

`/proc/pid/maps` 每行：`地址区间 权限 偏移 设备 inode 路径`。四类样本：

1. 可执行文件与其 so：同文件多行（不同权限段），**偏移为 0 的行基址 = 符号文件加载基址**（core 不匹配先查这里）；
2. 线程栈：`[stack]` 仅主线程有名；其余线程栈是「匿名区+guard gap」，从 `pthread_attr_getstackaddr`/
   core 的 NT_THREADS 段找；
3. 无名区域：mmap 匿名（malloc 大块、JIT、SysV 共享内存）——「代码在无名区执行」= 注入/壳/自解压；
4. `[vdso]`/`[vsyscall]`：内核态快速系统调用垫片，回溯里出现属正常。

### 2.3 改变「符号到地址」绑定的五级阶梯（6.3.5–6.3.9）

拦截强度递增、鲁棒性递减——本章最工程化的一节：

| 层级 | 手段 | 生效范围 | 检测难度 |
| --- | --- | --- | --- |
| 预先加载代理（LD_PRELOAD / Windows AppInit、DLL 注入） | 导出同名函数 | 之后所有进程的解析 | 低（maps 可见多出的 so） |
| 链接时替换（--wrap/强符号） | 链接器改写引用 | 单一构建 | 需要构建知识 |
| 修改导入/导出表（IAT patch / GOT overwrite） | 改运行期内存表 | 单进程，可动态开关 | 中（比对文件镜像） |
| 函数手术（inline hook：入口写 jmp） | 改指令流 | 连内部直调都能拦 | 高（反查 .text 与文件差异） |

调试正当用途：给无符号三方库的入口下断（GDB 断 GOT 项）、malloc 失败注入、热修复验证；
恶意用途（rootkit）同源——这也是 1.4.5「内存保护」与本章的交界。🔧 示例（标注命令）：

```text
LD_DEBUG=bindings ./prog                       # 观察每个符号绑定到哪个 so（拦截现场直播）
gdb -ex 'break *puts@plt' -ex run ./prog       # 断 PLT 桩而非实现，看首次/再次调用的分野
```

### 2.4 core 文件：格式与生产策略（6.3.10/6.3.11）

- 结构：ELF 头 + `PT_NOTE`（NT_PRSTATUS 寄存器、NT_FILE 映射表、NT_AUXV）+ `PT_LOAD`（各映射区内存）；
  minidump 同理是「流」容器（附录 B.2）。**core 不含未映射的符号信息**——分析永远要配原始二进制+符号。
- 产生：`ulimit -c unlimited`、`/proc/sys/kernel/core_pattern`（可管道给 systemd-coredump/apport，
  亦是崩溃上报客户端的挂载点，衔接 [11 篇](11-系统级观测与崩溃上报.md)第 13 章）；
- 体积策略：`/proc/pid/coredump_filter` 位掩码决定哪些映射入档——全量 core 动辄数 GB，
  「只留栈+so 头部」的精简模式是服务器场景刚需；
- Windows 对应：WER 自动 minidump、`procdump -ma`、任务管理器「创建转储文件」。

## 3. 权衡

- **完整 core vs 精简 minidump**：完整现场（堆遍历、引用树搜索都依赖堆内容）换磁盘与隐私；
  精简现场（栈+模块表）够定位 80% 崩溃但 [10 篇](10-内存调试工具与CoreAnalyzer.md)的 Core Analyzer 功能全部失效。
  实践分档：日常 minidump，疑难工单升级完整 core。
- **PIE/ASLR 与安全 vs 可复现**：core 分析时基址随机反而利于「发现硬编码地址假设」；关闭 ASLR
  仅用于配合 rr/确定性回放。
- **拦截的层次选择**：LD_PRELOAD 部署最轻但对静态链接与内部调用无效；函数手术最强但一次升级全失效。

## 4. 相邻概念对比

- **进程镜像 vs 程序文件**：文件是「模板」，镜像含运行时决定（复用 so、注入、brk 堆、线程栈）；
  「exe 一样行为不一样」的答案几乎总在镜像差集里。
- **core vs 日志 vs 监控**：core 是深而稀的快照（一崩一具），日志是浅而密的流水，监控是统计聚合；
  第 18 章「日志和监控」与本节构成互补三件套。
- **本章（Linux 为主）vs 附录 B（Windows）**：ELF/PE、core/minidump、maps/模块表一一对映；
  操作版对照见 [../C++代码调试的艺术.md](../C++代码调试的艺术.md) 第 8 章（转储文件分析实操）。

## 最新演进与工业实践

- **debuginfod + core**：发 symbol 的服务同样发 `*.debug`；`gdb -core vmlinux` 时按 Build-ID 自动拉符号，
  容器时代「镜像不带符号、服务器带符号」成为标配（sourceware.org/elfutils/Debuginfod.html，实测 200）。
- **CRIU（checkpoint/restore in userspace）**：把「镜像」整体序列化并可恢复继续跑——core 的「可读」升级为
  「可复活」，用于快速复现长初始化后才出现的 bug。
- **eBPF 观测代替高频 dump**：uprobe 挂到任意函数入口采参数（不开进程、不产生 core），
  bpftrace 一行式常用作「轻量现场」；见 [11 篇](11-系统级观测与崩溃上报.md)。
- **coredumpctl（systemd）**：集中收集/压缩/检索崩溃 core，`coredumpctl gdb <id>` 一条龙，已是主流发行版默认路径。
- **Windows 平台适用性**：本仓库 MinGW 栈调试 minidump 需 WinDbg/CDB（GDB 不吃 minidump）；
  双栈团队统一 Build-ID/GUID+age 校验流程是跨栈事故最少做法。
- **开源仓库逐点对照**：`gdb`（`target core`）、`elfutils`（debuginfod/unstrip）、
  `checkpoint-restore/criu`；minidump/TTD 文档在微软官方站（learn.microsoft.com，前文已实测可达）。

## 互链

- 原书大纲：[../高效CC++调试.md](../高效CC++调试.md)
- 载体三兄弟之「符号」 → [01-调试符号与调试器.md](01-调试符号与调试器.md)；「引用树/垂直搜索」算法 →
  [04-C++对象布局.md](04-C++对象布局.md)；工具化 → [10-内存调试工具与CoreAnalyzer.md](10-内存调试工具与CoreAnalyzer.md)
- 容器里的进程镜像特殊性 → [12-泄漏协程远程容器与预防.md](12-泄漏协程远程容器与预防.md)（第 17 章）
- 服务器进程的部署形态背景 → [../C++服务器开发精髓.md](../C++服务器开发精髓.md)
