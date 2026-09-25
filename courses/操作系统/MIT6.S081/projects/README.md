# projects — 6.1810/6.S081 配套动手项目

六个纯 C 项目：不依赖 RISC-V 工具链、不需要 QEMU，全部是"内核机制的宿主模拟器"，
可在 Linux/macOS（gcc/clang）与 Windows（MSVC Developer Command Prompt）双平台构建。
统一约定：每个目录含 `build.sh`（cc/gcc）与 `build.bat`（cl），运行演示入口 `main.c`。

## 讲次 → 项目 → 知识点

| 项目 | 主要对应讲次 | 覆盖知识点 | 内核原型 |
| --- | --- | --- | --- |
| `alloc/` | L04, L19（辅助 L10） | first-fit 外碎片、buddy 劈半/合并与内部碎片、分配器两层化（帧+对象）、吞吐与碎片量化 | xv6 `ulib.c malloc`、`kalloc.c`；Linux `page_alloc.c` |
| `pgtbl/` | L04, L10, L11 | 两级页表 walk、TLB 命中与 `sfence.vma` 一致性（含"忘刷"实验）、demand paging 缺页自愈、CoW fork（引用计数 + 写缺页复制） | xv6 `vm.c: walk/mappages`；lab-cow `duppage/uvmfault` |
| `sched/` | L01, L02（对照 OSTEP MLFQ） | 多级反馈队列：降级/保级/boost/指数时间片；周转/响应时间；与 RR、FIFO 基线对比 | xv6 `proc.c scheduler()`（裸 RR 反例） |
| `minifs/` | L06, L07, L08, L09, L14 | 块位图/inode/目录/namei、缓冲缓存、三段式 redo 日志、两种崩溃时机的重放/回滚验证、批提交（fssched 思路） | xv6 `fs.c/bio.c/log.c`；lab-fs |
| `locking/` | L02, L15 | test-and-set 自旋锁 + 指数退避 + acquire/release 栅栏、mutex vs spin 吞吐差、epoch-RCU 读端零争用与 grace period 安全回收、use-after-free 反例 | xv6 `spinlock.c`；lab-lock；lab-thread |
| `mini_shell/` | L05, L20（服务 L01） | fork/exec/wait、fd 语义、管道链与 EOF、重定向、`cd` 为何必须内建、fd 泄漏(CLOEXEC)经典坑 | xv6 `user/sh.c`；lab-shell（POSIX + Win32 双后端） |

## 快速开始

```sh
cd alloc     && ./build.sh
cd pgtbl     && ./build.sh
cd sched     && ./build.sh
cd minifs    && ./build.sh
cd locking   && ./build.sh    # 需要 -pthread（Windows 走 build.bat 用 Win32 线程）
cd mini_shell && ./build.sh   # 交互式，不自动运行
```
Windows：在 Developer Command Prompt 中逐个 `build.bat`。

## 学习顺序建议
L04→alloc → pgtbl；L10/L11 复习后再看 pgtbl 的缺页/CoW 实验；
L02→locking 的锁部分；L15→locking 的 RCU 部分；
L06–L09→minifs；L01/L02 调度线→sched；L05/L20→mini_shell。

每个项目的 README 内含"机制↔xv6 函数"对照表与刻意留下的练习（间接块、引用计数、后台 `&` 等）。
