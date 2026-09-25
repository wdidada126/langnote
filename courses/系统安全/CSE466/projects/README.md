# CSE466 配套项目计划

> 原则：模块 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> pwn.college challenge 在线且不可复刻；以下为同知识点的自制靶题 + 利用/防御双向工程，全部作用于本地/Docker 自有环境，笔记不问题解。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| L1–L2 滥用与 IPC | C + Python | 含 unix socket 鉴权缺失的守护进程靶 + 交互滥用脚本 | `make daemon`，`python client_abuse.py`（Docker） |
| L3–L4 Shellcode | x86-64 asm + C | 手搓 execve shellcode（无坏字符约束检查器）+ mmap 可执行对照 demo | `nasm sc.S && make sc`，验证脚本 `python check_sc.py` |
| L5–L7 逆向练习册 | C + Python | 10 个「读反汇编答问题」小函数集（Ghidra 脚本批处理导出） | `make rev-book`（gcc -O0/-O2 双版本） |
| L8 控制流劫持 | C + Python | 自制 ret2sys/ret2libc 双靶 + pwntools 模板脚本 | `make ctTargets`，`python pwn_*.py` |
| L9 ROP/栈迁移 | C + Python | gadget 受限的二进制（自制 Ropper 统计脚本）+ pivot 靶 | `make roplab`，`ROPgadget --binary` 记录 |
| L10 堆与格式化字符串 | C + Python | tcache 投毒教学靶（打印分配器状态）+ fmt 任意读写靶 | `make heap fmt`（Ubuntu 22.04 glibc 固定版 Dockerfile） |
| L11 JIT 面 | JS + Python | SpiderMonkey debug shell 最小 repro 清单 + Fuzzilli 运行配置 | Fuzzilli 官方镜像 compose 文件（本轮只写配置） |
| L12–L13 内核与竞态 | C (kernel module) + QEMU | 故意含 unchecked copy_from_user 的 toy 内核模块 + QEMU 调试环境 + 竞态放大脚本 | `make kmod`（内核头 + Kbuild），`qemu/run.sh` |
| L14 沙箱综合 | C + Seccomp BPF | 给自制 shell 服务套 seccomp+namespace 双层沙箱 + 逃逸审计清单 | `make sandbox`（libseccomp） |
| 综合 | Python | 迷你「本地 CTF」组卷器：串联上述靶生成多旗挑战环境 | `python organizer.py serve`（docker compose） |

## 目录约定（后续填充）

```
projects/
  01_ipc_daemon/  02_shellcode/  03_rev_workbook/  04_cfi_targets/
  05_rop/  06_heap_fmt/  07_jit/  08_kernel_qemu/  09_sandbox/  10_localctf/
```

内核/QEMU 相关一律附 Dockerfile + Linux 内核构建脚本（只写不跑）；Windows 宿主通过 WSL2 运行，说明统一写在各项目 README。
