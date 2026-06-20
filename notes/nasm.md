# nasm

nasm

masm

linux as工具

## 源代码编译
https://www.nasm.us/
win或者rpm系列linux，可以直接下载编译好的

https://github.com/netwide-assembler/nasm

以下是关于NASM汇编语言的经典和实用书籍推荐，涵盖从入门到精通的各个阶段：

一、经典必读（系统性学习）

1. 《汇编语言（基于x86处理器）》

• 作者：Kip R. Irvine

• 特点：非常经典的汇编语言教材，使用MASM、TASM和NASM多种汇编器进行讲解，内容系统全面

• 相关章节：NASM语法差异、x86指令集、系统调用等

2. 《x86汇编语言：从实模式到保护模式》

• 作者：李忠、王晓波、余洁

• 特点：国人编写的优秀教材，从基础到高级循序渐进，适合中文读者

• NASM相关：书中示例代码主要基于NASM汇编器

3. 《Professional Assembly Language》

• 作者：Richard Blum

• 特点：面向有一定编程经验的读者，重点讲解Linux下的汇编编程

• NASM应用：使用NASM作为主要汇编器，涵盖系统调用、高级技巧

二、NASM专项书籍

4. 《The Art of Assembly Language》

• 作者：Randall Hyde

• 特点：汇编语言的"圣经级"著作，虽然主要使用HLA，但对理解NASM有重要参考价值

• 在线资源：有大量NASM相关的在线章节和示例

5. 《汇编语言程序设计》

• 作者：Richard Detmer

• 特点：专门针对NASM汇编器，从基础语法到高级应用全面覆盖

• 实践性强：每章都有丰富的NASM示例代码

三、在线资源和官方文档

6. NASM官方手册

• 网址：https://www.nasm.us/doc/

• 特点：最权威的参考资料，包含完整的指令说明、语法规范、宏系统等

• 必读章节：

  • Chapter 2: Running NASM

  • Chapter 3: The NASM Language

  • Chapter 4: The NASM Preprocessor

7. Linux汇编语言开发指南

• 网址：多个在线教程和PDF资源

• 特点：专注于Linux系统下的NASM编程，包含系统调用、ELF格式等

四、实践导向书籍

8. 《低层程序设计》

• 作者：Jonathan Bartlett

• 特点：从C语言到汇编的过渡，大量使用NASM进行实例演示

• 项目驱动：通过实际项目学习汇编编程

9. 《x86-64 汇编语言编程》

• 作者：Ed Jorgensen

• 特点：免费开源教材，专注于64位汇编，使用NASM和GCC

• 在线获取：可从官网免费下载PDF版本

五、学习路径建议

阶段1：基础语法（1-2周）

; 基础NASM语法示例
section .data
    msg db 'Hello, World!', 0xA
    len equ $ - msg

section .text
    global _start

_start:
    ; write系统调用
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, msg        ; 消息地址
    mov edx, len        ; 消息长度
    int 0x80
    
    ; exit系统调用
    mov eax, 1          ; sys_exit
    xor ebx, ebx        ; 退出码0
    int 0x80

推荐书籍：《汇编语言（基于x86处理器）》前几章 + NASM官方手册第3章

阶段2：高级特性（2-3周）

• 宏系统：%macro, %endmacro

• 条件汇编：%if, %ifdef  

• 重复块：%rep, %endrep

• 结构体和记录

推荐书籍：NASM官方手册第4章 + 《Professional Assembly Language》

阶段3：系统编程（3-4周）

; 文件操作示例
section .data
    filename db 'test.txt', 0
    buffer times 100 db 0

section .text
global _start

_start:
    ; 打开文件
    mov eax, 5          ; sys_open
    mov ebx, filename
    mov ecx, 0          ; O_RDONLY
    int 0x80


推荐书籍：《Linux汇编语言开发指南》 + 实践项目

六、重点学习内容

1. NASM特有语法

; 数据定义
db 0x12        ; 定义字节
dw 0x1234      ; 定义字
dd 0x12345678  ; 定义双字
dq 0x123456789ABCDEF0 ; 定义四字

; 标签和变量
my_var: dd 42          ; 标签定义变量
mov eax, [my_var]      ; 使用变量

; 段定义
section .data          ; 数据段
section .bss           ; 未初始化数据段  
section .text          ; 代码段

2. 宏和条件汇编

; 宏定义
%macro syscall 1
    mov eax, %1
    int 0x80
%endmacro

; 条件编译
%ifdef DEBUG
    ; 调试代码
%endif

3. 与GCC的交互

; 调用C函数
extern printf
section .data
    fmt db "Result: %d", 10, 0

section .text
global main
main:
    push dword 42
    push fmt
    call printf
    add esp, 8
    ret

七、实用学习建议
1. 边学边练

# 编译和链接NASM程序
nasm -f elf32 program.asm -o program.o
ld -m elf_i386 program.o -o program
./program

2. 使用调试器

# 使用GDB调试NASM程序
gdb ./program
(gdb) layout asm
(gdb) break _start
(gdb) run

3. 参考项目结构

asm_project/
├── src/
│   ├── main.asm
│   ├── io.asm
│   └── math.asm
├── include/
│   └── macros.inc
├── Makefile
└── README.md

总结推荐
学习阶段 推荐书籍 重点内容
入门 《汇编语言（基于x86处理器）》 基础语法、指令集
进阶 NASM官方手册 + 《Professional Assembly Language》 宏系统、高级特性
精通 实践项目 + 在线资源 系统编程、性能优化
最佳组合：以《汇编语言（基于x86处理器）》为理论基础，配合NASM官方手册作为语法参考，通过实际项目加深理解。

开始学习时建议从简单的Hello World程序入手，逐步深入到文件操作、系统调用等复杂功能。
