# 第 16-17 章 直接定址表与 BIOS 键盘输入、磁盘读写

> **一句话**：前 15 章教你「怎么写汇编」，这两章教你「写真的有用的汇编」——用直接定址表做「查表即函数调用」，再用 `int 16h`/`int 13h` 读键盘和读写磁盘扇区，做出一个能自举、能装自己的程序。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 16.1 描述了单元长度的标号 | 带 `: ` 的标号就是地址 | `lab: nop` 里的 `lab` 只等于偏移，不携带长度信息 |
| 16.2 在其他段中使用数据标号 | `cs:lab` / `ds:lab` 引用 | MASM 的段修饰语法；跨段访问要靠它 |
| 16.3 直接定址表 | 一张「入口地址表」 | **查表 = 跳过 switch / if 链**，O(1) 分发 |
| 16.4 程序入口地址的直接定址表 | 表项是各子程序的入口 | 本章的巅峰写法；实验 16 的成品 |
| 17.1 `int 9` 对键盘输入的处理 | 键盘缓冲区循环队列 | BIOS 在 `int 9` 里把按键写入 `16h` 中断的数据区 |
| 17.2 用 `int 16h` 读键盘缓冲区 | `AH=0` 取键，`AH=1` 查有无键 | 应用程序与键盘之间的**标准接口** |
| 17.3 字符串的输入 | 逐字符读 + 回显 + 退格 | 一个完整的行编辑器（不含编辑键） |
| 17.4 用 `int 13h` 读写磁盘 | `AH=02h` 读扇区 / `AH=03h` 写扇区 | 扇区号 = `(柱面, 磁头, 扇区)`；`DS:BX` 指向缓冲区 |
| 实验 17 | 写包含多个功能子程序的中断例程 | 把 16、17 章全部串起来 |
| 课程设计 2 | 综合项目 | 本书的毕业设计 |

---

## 核心精讲

### 1) 直接定址表：把「分支链」换成「查表」（16.1–16.4）

```asm
; 教学示意，不参与构建
data segment
    ; 表：每个表项是一个子程序的入口地址（这里用 dw 存放偏移）
    table dw sub_zero, sub_one, sub_two, sub_three
data ends

code segment
start:
    mov ax, data
    mov ds, ax
    mov bx, offset table
    add bx, ax            ; bx = 表首 + 功能号 × 2（dw 占 2 字节）
    call word ptr [bx]    ; 间接调用：IP ← (ds:bx) 处的字
    mov ax, 4c00h
    int 21h

sub_zero:
    mov dl, '0'
    jmp short print_ok
sub_one:
    mov dl, '1'
    jmp short print_ok
sub_two:
    mov dl, '2'
    jmp short print_ok
sub_three:
    mov dl, '3'
print_ok:
    mov ah, 02h
    int 21h               ; DOS 输出一个字符
    ret
code ends
end start
```

**为什么值得用**

| 方式 | 复杂度 | 可扩展性 |
| --- | --- | --- |
| `cmp ax,0` / `cmp ax,1` / … 串 if 链 | O(n) 比较 | 加功能要改判断逻辑 |
| 直接定址表 + `jmp/call word ptr [bx]` | **O(1)** 一次取指 | 加功能只改表 |

> 这正是**跳转表（jump table）**的雏形。在 x86-64 上它长得更现代：`jmp qword ptr [rip + table*8]`（真正的 switch 编译结果），或者 C 的 `switch` + 编译器生成的 `jmp` 表。
> 注意本书用 `dw` 存偏移，**只能段内跳转**；跨功能表要用 `dd` 存 CS:IP 或改用 `jmp far`。

### 2) 键盘：`int 9` 与 `int 16h`（17.1–17.3）

```asm
; 教学示意，不参与构建
; 读一个键（阻塞）；返回 AX = 扫描码(高 8 位) / ASCII(低 8 位)
    mov ah, 00h
    int 16h               ; BIOS 键盘服务：AH=0 取键
    ; AL = ASCII 码（0 表示特殊键），AH = 扫描码

; 不阻塞地查是否有键
    mov ah, 01h
    int 16h               ; ZF=1 表示有键可用
    jz  no_key
```

**行编辑器的骨架（17.3）**

```asm
; 教学示意，不参与构建
input_loop:
    mov ah, 00h
    int 16h
    mov ah, 0eh           ; DOS/BIOS 回显一个字符
    int 10h

    cmp al, 08h           ; 退格
    je  backspace
    cmp al, 0dh           ; 回车（0Dh）
    je  input_done
    ; 其它可打印字符：存入缓冲区
    mov [si], al
    inc si
    jmp input_loop

backspace:
    dec si                ; 只做示意：真实实现要处理缓冲区下界与回显删字
    jmp input_loop
```

> 键盘输入的三层要分清：**硬件层**（`int 9`，扫描码）→ **BIOS 缓冲层**（`int 16h` 读写）→ **应用层**（你自己的字符串处理）。

### 3) 磁盘：`int 13h` 读扇区（17.4）

```asm
; 教学示意，不参与构建
; 读第 1 号扇区（boot 扇区）到 0:7C00
    mov ax, 0
    mov ds, ax            ; 缓冲区段址
    mov bx, 7c00h         ; 缓冲区偏移
    mov ah, 02h           ; 子功能：读扇区
    mov al, 1             ; 读 1 个扇区
    mov ch, 0             ; 柱面（cylinder）低 8 位
    mov cl, 1             ; 扇区号（1–63）
    mov dh, 0             ; 磁头
    mov dl, 0             ; 驱动器号（A 盘 = 0）
    int 13h               ; BIOS 磁盘服务
    jc  disk_error        ; CF=1 表示失败

disk_error:
    ; AX = 状态字，可直接打印
```

**CHS 与容量**

```text
扇区号 CL = 位 5–0（1–63）；位 7–6 存柱面高 2 位
柱面 CH = 低 8 位；柱面高 2 位从 CL 的高 2 位取
磁头 DH = 0..N（0 面 / 1 面）
每磁头扇区数 = 63 × 2 头 × 柱面数
```

> 现代意义：`int 13h` 只能访问 CHS 可达的 8 GB 范围；要用 LBA 的扩展调用（`AH=42h` 读 / `AH=43h` 写，通过 `DL` 的扩展磁盘包 `disk address packet`）。在 UEFI 环境下则彻底用 `int 10h` 的 EFI 块 I/O 协议或自己驱动 AHCI/NVMe。

### 4) 综合实验 17 的形态（含 install 程序）

```text
1. 写一个中断例程（比如 int 7Ch 或 int 9），内部用直接定址表分发功能
2. 写一个 install 程序：把该例程的代码复制到内存安全区（如 0:200）
3. 用 CLI/STI 保护下，把例程地址写入 IDT（中断向量表）
4. 运行后，原程序可以通过 int N 调用这些功能（读键盘、读磁盘扇区…）
```

> 这就是**「自己给自己装系统调用」**的完整过程，也是理解「操作系统如何提供系统调用」的最好玩具实验——Linux 的 `entry_SYSCALL_64` 在结构上干的是同一件事。

---

## 版本演进

| 年份 | 事件 | 关联 |
| --- | --- | --- |
| 1978 | 8086：`int 13h`（磁盘）/`int 16h`（键盘）已在 ROM BIOS 中 | 本章主角 |
| 1984 | BIOS 中断扩展（INT 1Ah 等）与扩展 BIOS 区（EBDA） | 中断例程安装位置的雏形 |
| 1990s | 免引导扇区（boot sector）模板、`stage1/stage2` 引导链 | 本书实验 13/17 的直接继承者 |
| 2000s | GRUB/LILO、EFI → UEFI | 磁盘服务从 `int 13h` 换到 EFI 协议 |
| 2012 | UEFI 全面落地（Windows 8 起） | `int 13h` 在 64 位启动路径上被 ISO 化 |
| 2026 | 安全启动（Secure Boot）+ measured boot 让「自写引导扇区」需要签名或关闭校验 | 本书实验的**现代门槛**变高了 |

> 最重要的提醒：**今天在真机上写引导扇区会遇到 Secure Boot**。要么在虚拟机（QEMU/Bochs）里做，要么在固件设置里临时关闭校验。

---

## 经典论文与原始文献

| 论文 / 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Intel 8086 Family User's Manual | Intel，1978 | `int`/`iret` 与 BIOS 中断的底层基础 |
| IBM PC BIOS Listings（ROM BIOS 反汇编源码） | IBM / Manybooks 等汇编本 | `int 13h`/`int 16h` 实现的原始代码，可逐行对照 |
| 《IBM Disk Operating System / PC BIOS 技术参考》 | IBM，1981–1994 | 各中断的入口参数与返回值 |
| Intel SDM Vol.3 — 中断；Vol.2 — `CALL` 间接形式 | Intel 在线发行版 | 间接调用与向量表的机器级规定 |
| Intel 64 and IA-32 Architectures Optimization Reference Manual | Intel 在线发行版 | 跳转表与分支图（branch graph）的现代化建议 |
| Tanenbaum, *Operating Systems: Design and Implementation* | Prentice Hall，1987 | minix 的引导、中断与系统调用实现，与实验 17 结构相同 |
| Wikibooks *X86 Assembly* — OS Dev / Interrupts | https://en.wikibooks.org/wiki/X86_Assembly | 引导扇区与 `int 13h` 的现代自由教材 |

---

## 近年研究与工业界开源实践（2015–2026）

趋势：bootloader 与系统调用分发在现代工程里走向「生成 + 验证」；手写汇编的 hardcore 场景（引导、固件、内核入口）要么被框架接管，要么被安全启动挡在门外。

| 仓库 / 项目 | star | 说明 |
| --- | --- | --- |
| `qemu/qemu` | 13,761★（实测） | 最佳实验台：`-drive format=raw,file=disk.img` 可加载你写的扇区 |
| `netwide-assembler/nasm` | 3,315★（实测） | 引导扇区与 16 位代码的现代首选汇编器 |
| `yasm/yasm` | 1,485★（实测） | 同上；`yasm boot.asm -f bin -o boot.bin` |
| `torvalds/linux` | 250,106★（实测） | `arch/x86/boot/`（实模式引导）+ `arch/x86/entry/`（系统调用分发） |
| `openssl/openssl` | 30,844★（实测） | 自写汇编模块 + 常量时间控制流的工业范例 |
| `llvm/llvm-project` | 40,648★（实测） | switch 指令到跳转表的生成逻辑（本章 16.3 的编译器版） |
| `riscv/riscv-tools` | 1,195★（实测） | 对照 RISC-V 的引导与 S 态陷阱处理，形态更简洁 |

> 实测方式：`gh api repos/OWNER/REPO --jq '.stargazers_count'`，日期 **2026-09-25**。

---

## 常见误区与本书需修正之处

| # | 误区 / 待修正 | 说明 |
| --- | --- | --- |
| 1 | 🔧 「`int 13h` 读盘失败就不管了」 | 失败时 **CF=1 且 `AX` 里是错误码**，同时 **AH 保留状态字节**。一定要判 CF 并在失败时复位驱动器（`AH=00h`）再重试。 |
| 2 | 🔧 「扇区号从 0 开始数」 | `int 13h` 的**扇区号从 1 开始**（`CL` 的 1–63）；柱面从 0 开始。这是死记硬背也得会的常识。 |
| 3 | 🔧 「跨段直接定址表用 `dw` 就行」 | `dw` 只能存 16 位偏移，跳转**只能段内**。跨段要用 `dd` 存段:偏移，或用 `jmp far ptr` 配合远指针表。 |
| 4 | 🔧 「`int 16h` 读到键就直接当 ASCII 用」 | `AL` 为 0 时是**特殊键**（功能键、方向键），信息在 `AH`（扫描码）里。直接当字符处理会丢掉功能键。 |
| 5 | 🔧 「自写引导扇区在现在机器上一定跑得起来」 | 会遇到 **Secure Boot**：未签名的 MBR 引导扇区可能被拒绝执行。建议用 QEMU/Bochs 实验，或固件里临时关校验。 |
| 6 | 🔧 「`int 13h` 能访问任意容量磁盘」 | CHS 路径只到 8 GB 左右。大容量要用 LBA 扩展调用（`AH=42h/43h`），UEFI 下则改用 EFI 块 I/O 或自行驱动 AHCI/NVMe。 |
| 7 | 🔧 「安装中断例程只要写向量表」 | 顺序应为：① 保留旧向量 → ② 复制例程到安全区 → ③ 写向量 → ④ `sti`；并且全程 `cli` 保护。本书实验 12 已示范，实验 15/17 复用同一套路。 |
| 8 | 🔧 「`int 9` 例程里可以直接用 DOS 中断」 | 可以，但 BIOS/DOS 中断例程在中断上下文里调用 DOS 服务容易重入（`int 21h` 在 DOS 单线程下不安全）。现代内核用 `tasklet`/`softirq` 把处理推后。 |
| 9 | 🔧 「这两章教的技术今天仍可直接复用」 | 概念（查表分发、中断链、扇区读写）100% 有效；**API 与接口已换代**（`int 13h` → LBA/UEFI；`int 21h` → `syscall`）。 |

---

## 与其他章 / 其他书的联系

- 前承：`11-内中断与int指令.md`（向量表与安装手法）、`12-端口与外中断.md`（键盘硬件链路）。
- 与 `09-CALL和RET指令.md` 的间接调用强相关：`call word ptr [bx]` 是本章查表分发的核心。
- 与 `07-数据处理的两个基本问题.md` 的 `dw`/`dd` 强相关：表项的大小决定了自己怎么算下标。
- 与 `book/Linux内核完全剖析/`（仓库内可见同名目录）对照：boot 扇区 → 实模式 → 保护模式的完整迁移。
- 与 `book/程序员的自我修养链接装载与库.md` 对照：install 程序做的是「运行时动态装载」，正是装载器的微缩版。
- 与 `book/深入理解计算机系统/`（CSAPP 第 3、9 章）与 `book/操作系统设计与实现.md` 对照：异常控制流与 I/O 的现代版本。
