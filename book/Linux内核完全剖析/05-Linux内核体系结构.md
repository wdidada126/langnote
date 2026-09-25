# 第 5 章 Linux 内核体系结构

> **本章地图**：Linux 内核的「设计模式」（单体内核 vs 微内核的取舍）→ 内核源代码的**目录树结构**（`boot/`、`fs/`、`include/`、`init/`、`kernel/`、`lib/`、`mm/`、`tools/`）→ Makefile 与编译组织（顶层 Makefile → `Image` 的 `cat` 拼接）→ 内核编制结构（各子系统的头文件与包含关系）。
>
> 一句话结论：**0.11 的目录树是「教科书级别的 1/10 缩微模型」**——它小到可以整体记住，大到包含了现代内核的全部子系统划分。把这张图背下来，你就拥有了一份读任何版本内核的「目录地图」。

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 内核设计模式 | 单体内核、层次化、可移植层 | Linux 是**单体内核**，但内部有清晰的层次与接口边界 |
| 目录树结构（0.11） | 8 个目录 + 顶层 Makefile | 与今天内核的子系统目录几乎一一对应 |
| Makefile 与编译 | 顶层规则、`boot`/`kernel`/`mm`/`fs` 的编译单元 | 0.11 无 Kbuild，靠手写规则与脚本拼 Image |
| 内核编制结构 | 头文件分层、包含关系 | `include/linux/`、`include/asm/`、`include/sys/` 三层 |

## 核心精讲

### 5.1 设计模式：Linux 为什么是「单体内核」

```text
; 教学示意：单体内核的层次（自底向上）
;   ┌────────────────────────────────────────┐
;   │  应用程序（shell / ls / cat）           │ 用户态
;   ├────────────────────────────────────────┤
;   │  系统调用接口（int 0x80 / sys_table）   │ 内核边界
;   ├────────────────────────────────────────┤
;   │  进程调度  |  内存管理  |  文件系统      │ 内核态（同一地址空间）
;   │  sched.c   |  memory.c |  buffer/minix │
;   ├────────────────────────────────────────┤
;   │  设备驱动（hd.c / console.c / tty_io.c）│
;   ├────────────────────────────────────────┤
;   │  arch/i386 层（head.s / system_call.s）│ 硬件抽象
;   └────────────────────────────────────────┘
```

| 维度 | 单体内核（Linux） | 微内核（MINIX/早期 Mach） |
| --- | --- | --- |
| 性能 | 快（无跨地址空间调用） | 慢（IPC 开销） |
| 可维护 | 差（全局耦合） | 好（服务独立） |
| 0.11 的体现 | 驱动与内核同地址空间，一个 bug 全盘崩溃 | MINIX 把文件服务/进程服务放在用户态 |
| 🔧 现代折中 | 内核内加**可加载模块**与**子系统接口边界** | L4 系微内核 + 用户态服务 |

> 结论：Linux 选择了「单体内核 + 严格内部接口 + 模块（后期）」，这是工程上的取舍，不是理论上的败北。

### 5.2 0.11 目录树（**本章最有价值的图**）

```text
; 教学示意：Linux 0.11/0.12 源码树（顶层 9 项）
;   linux/
;   ├── boot/       bootsect.s  setup.s  head.s        （引导，实模式→保护模式）
;   ├── fs/         buffer.c  inode.c  file_table.c  namei.c  minix_fs/…
;   ├── include/    linux/ asm/ sys/                   （三层头文件）
;   ├── init/       main.c  Version.c                  （内核初始化，非引导）
;   ├── kernel/     sched.c  fork.c  signal.c  sys.c  exit.c  trap.c
;   │               mm/  blk_drv/  chr_drv/  math/     （子目录）
;   ├── lib/        open.c  strings.c  vsprintf.c      （内核公共函数）
;   ├── mm/         memory.c  page.s                   （分页与缺页）
;   ├── tools/      build.c                            （生成 Image 的构建工具）
;   └── Makefile    （及子 Makefile）
```

| 目录 | 体量（0.11） | 🔧 现在对应 |
| --- | --- | --- |
| `boot/` | 3 个汇编码文件 | `arch/x86/boot/`（含 `head_64.S`） |
| `fs/` | minix 文件系统 + buffer 层 | `fs/`（ext4/fuse/overlayfs…）+ `fs/buffer.c` 已弱化 |
| `include/` | linux/asm/sys 三层 | `include/` + `arch/*/include/`（**已拆开**） |
| `init/` | main.c / Version.c | `init/main.c`（`start_kernel()`） |
| `kernel/` | 调度/进程/信号/系统调用 | `kernel/` + `kernel/sched/`（CFS 独立成一树） |
| `lib/` | vsprintf/strings | `lib/`（rbtree、string、crypto） |
| `mm/` | memory.c/page.s | `mm/`（SLUB、mmap、shmem…） |
| `tools/` | build.c | `scripts/` + `tools/`（perf、selftests） |

### 5.3 Makefile 与编译组织

```makefile
# 教学示意，不代表可编译运行：0.11 顶层 Makefile 骨架
AS_ROOT = as86
CC      = gcc -m32
CFLAGS  = -Wall -O2 -fstrength-reduce -fomit-frame-pointer

Image: boot/bootsect boot/setup system
	cat boot/bootsect boot/setup system > Image

boot/bootsect: boot/bootsect.s
	$(AS_ROOT) -o boot/bootsect.o boot/bootsect.s
	ld86 -s -o boot/bootsect boot/bootsect.o

system: head.o kernel.o mm.o fs.o
	ld -e _start -o system head.o kernel.o ...
```

> 关键认知：**`cat bootsect + setup + system > Image` 就是 0.11 的「打包」**，没有 ELF 入口概念——入口地址由 `bootsect` 里那段固定搬运代码决定。
> 🔧 现代是 `Kbuild`：`make vmlinux && make modules && make bzImage`，`scripts/link-vmlinux.sh` 负责链接，`objtool` 做校验。

### 5.4 内核编制结构与头文件分层

```text
; 教学示意：包含关系（0.11）
;   include/linux/*.h   ← 内核公共定义（sched.h / fs.h / mm.h …）
;   include/asm/*.h     ← 与 CPU 相关（system.h 里的 in/out、lidt、cr0）
;   include/sys/*.h     ← 面向应用的系统调用原型（_syscallN 宏）
```

> `_syscall0`…`_syscall3` 宏是 0.11 生成系统调用包装的「元编程」手段，展开后就是几行 `mov %eax, ...; int $0x80`——这是理解 `08` 章 `system_call.s` 的关键。

### 5.2 目录树速记法（读现代内核的地图）

把 0.11 的目录名与今天的内核目录**并排放**，能立刻定位「一个新东西挂在哪个目录」：

| 0.11 目录 | 0.11 职责 | 现代内核对应目录 | 现代新增职责 |
| --- | --- | --- | --- |
| `boot/` | 引导三件套 | `arch/x86/boot/` | 含 `efistub`、压缩与解压缩 |
| `include/`（三层） | 头文件 | `include/` + `arch/*/include/` | asm 头文件按架构拆分 |
| `kernel/` | 调度/进程/信号/syscall | `kernel/` + `kernel/sched/` | 调度器独立成子系统 |
| `mm/` | 分页与缺页 | `mm/` | slab/slub、mempool、folio |
| `fs/` | minix 文件系统 | `fs/` | ext4/btrfs/fuse/overlayfs |
| `kernel/blk_drv/` | 块设备驱动入口 | `block/` | blk-mq 多层队列 |
| `kernel/chr_drv/` | 字符设备入口 | `drivers/char/` + `drivers/tty/` | 现代设备模型 |
| `kernel/math/` | 387 仿真 | `arch/x86/math-emu/`（已弱化） | — |
| — | — | 🔧 新增 `net/`、`crypto/`、`security/`、`virt/`、`certs/`、`samples/`、`rust/` | 协议栈、加密、LSM、KVM、证书、范例、Rust |

> **用法建议**：读现代内核时，先在 0.11 目录里找到「同类文件」，再去 `torvalds/linux` 里找今天的目录。例如：想看调度，先看本书 `08-内核代码.md` 的 `sched.c`，再去读 `kernel/sched/fair.c`。

### 5.3 目录树之外：内核的「虚拟文件系统接口清单」

0.11 的内核对外只暴露四类接口，这与今天的 `Documentation/` 目录划分几乎一致：

| 接口类型 | 0.11 的入口 | 用户态看到的形态 |
| --- | --- | --- |
| 进程 | `fork/execve/wait4/exit` | shell 的 `&`、脚本执行 |
| 文件 | `open/read/write/close/lseek` | `cat`/`ls` 等命令 |
| 设备 | `open` + `read/write/ioctl`（字符/块） | `/dev/*` 节点 |
| 内存 | `brk/mmap`（0.12 起更完整） | 堆分配与共享映射 |

> 结论：**系统调用就是内核的「目录树索引」**；每读一个子系统，先问一遍「它对应用户态哪个命令」，定位会快很多。

### 5.4 内核「编制结构」的三条层次规则

1. **与硬件无关的代码放全局目录，相关的放 `arch/`**：`mm/` 通用 vs `arch/i386/mm/`。
2. **头文件按「通用 / CPU 相关 / 系统调用」分层**：0.11 是 `include/linux`、`include/asm`、`include/sys`；🔧 现代是 `include/linux`、`arch/x86/include/asm`、`include/uapi`。
3. **构建规则随代码走**：0.11 每目录一个 Makefile；🔧 现代是 `Kconfig` 决定要不要编译，`Kbuild` 决定编什么。

## 版本演进

| 年份 | 结构变化 |
| --- | --- |
| 1991–1992 | 0.11/0.12：上表结构，8 目录 |
| 1996 | 2.0：`drivers/` 成为一等公民，SMP 支持 |
| 2001 | 2.4：`net/` 独立化，`Documentation/` 制度化 |
| 2002 | 2.5：**Kbuild**、`.config`、`obj-y/obj-m`、`init/Kconfig` |
| 2005 | 2.6：模块签名、`sysfs`、`kobject` 体系落地 |
| 2011 | 3.0：`arch/` 与 `include/` 分离完成（asm 头文件迁入各 arch） |
| 2015+ | 🔧 `certs/`、`crypto/`、`security/`、`virt/`（KVM）、`samples/` 等新顶层目录出现 |
| 2021+ | 🔧 `rust/` 顶层目录、Rust 支持逐步主线化 |

## 经典论文与原始文献

| 文献 | 出处 | 与本主题的关联 |
| --- | --- | --- |
| Bovet & Cesati, *Understanding the Linux Kernel*（3rd ed.） | O'Reilly，2005 | 对 0.11→2.6 内核结构的权威展开 |
| Love, *Linux Kernel Development*（3rd ed.） | 2010 | 以 2.6/3.x 讲内核架构与子系统 |
| Corbet, Rubini & Kroah-Hartman, *Linux Device Drivers*（3rd ed.） | O'Reilly，2005 | 设备与驱动的架构视角 |
| *The Linux Kernel Documentation*（kernel.org/doc） | 持续更新 | 🔧 一手结构说明（`process/`、`driver-api/`，分中文版） |
| Torvalds, *Linux Kernel Module Programming Guide* | 社区文档 | 🔧 模块与内核边界的实操说明 |
| Tanenbaum & Woodhams, *Operating Systems Design and Implementation*（MINIX） | 1997 第2版 | 微内核对照物，用于本节的取舍讨论 |

## 近年研究与工业界开源实践（2015–2026）

- **`torvalds/linux`（**250112★**，2026-09-25 实测）** 的顶层目录已从上表演化为二十余项，`drivers/` 占比过半，是当前架构讨论的唯一现实对象。
- **子系统的「官方仓库」概念**：如 `torvalds/linux-net-queue`、`torvalds/linux-mm`（维护者 tree），`libbpf/libbpf`（**2758★**）把 eBPF 库独立成树，说明「内核 API 外化」的趋势。
- **可复现的迷你内核环境**：`cirosantilli/linux-kernel-module-cheat`（**4515★**）用一个仓库覆盖 QEMU + GDB + 模块 + 内核调试全流程，是本章「目录树」的现代等价实验工具。
- **Rust 主线化**：`Rust-for-Linux/linux`（**4413★**）与 `fishinabarrel/linux-kernel-module-rust`（**1336★**）展示了内核语言边界的现状。
- **构建可复现性**：`buildroot/buildroot`（**3656★**）与 `systemd/systemd`（**16746★**）是「内核 + 用户空间」现代组合的具体落地，读它们的目录组织能反推内核架构的演进方向。

## 常见误区与本书需修正之处

| # | 说法/写法 | 修正与补充 |
| --- | --- | --- |
| 1 | 「Linux 是微内核」 | 明确是**单体内核**；仅有部分功能（如 FUSE、部分文件系统）运行在用户态 |
| 2 | 「0.11 的目录树就是现在内核的目录树」 | 🔧 大致对应但差异巨大：`include/asm` 已拆分、`kernel/sched` 独立、新增 `crypto/`、`security/`、`virt/`、`rust/`、`certs/` 等 |
| 3 | 「Makefile 学一遍就行」 | 🔧 现代是 Kbuild + `.config` + Kconfig 三件套，手写 Makefile 已不是主流 |
| 4 | 「`cat` 拼 Image 很落后」 | 它恰恰是理解「引导扇区必须落在 `0x7C00`」「system 必须在 `0x10000` 起」的关键 |
| 5 | 🔧 「本书讲的就是 Linux 架构」 | 本书讲的是 1992 年的架构；现代架构请读 *Linux Kernel Development* 与 `Documentation/` |
| 6 | 🔧 缺现代内容 | 建议补：kobject/device model、模块机制、tracepoint、kunit、rust-for-linux |

## 与其他章 / 其他书的联系

- **上游依赖**：`04-80x86保护模式及其编程.md`（GDT/LDT 在内核数据结构的落点）、`03-内核编程语言与环境.md`（目录里的 `.s`/`.c` 用什么工具编）。
- **下游主体**：`06-引导启动程序.md`（`boot/`）、`07-初始化程序.md`（`init/main.c`）、`08-内核代码.md`（`kernel/`）、`13-内存管理.md`（`mm/`）、`12-文件系统.md`（`fs/`）。
- **其他章名录**：`09-块设备驱动程序.md`、`10-字符设备驱动程序.md`、`14-头文件.md`、`11-数学协处理器.md` 都是本目录树的直接展开。
- **跨书**：`book/LinuxUnix设计思想.md`（Unix/Kernel 的设计哲学对照，`tools/build.c` 这类「小工具」的思路同源）；`book/操作系统_原理与实现2.md`（架构层对照）；`book/深入理解Linux网络.md`、`book/深入理解MySQL核心技术.md`（同一「目录树 + 子系统」读法在其它软件上的应用）；`book/程序员的自我修养链接装载与库.md`（`lib/` 与链接的关系）。
