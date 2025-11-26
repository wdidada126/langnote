# asm

《architecture patterns with python》，作者是某个欧洲家具转运公司的，不是啥大厂，但业务逻辑也够复杂。这本书结合实战例子讲了 DDD，这就明白的多了。也讲了 TDD，事件驱动设计等等。这书最好的是讲了这些花里胡哨的概念怎么能落地，究竟怎么帮助了他们。咱们写代码最终也是为了解决问题，把东西落地，并不是为了“我们用了 XXX，这很 cooooool”。所以很值得一看

非常优秀的开源课程项目专门教授汇编语言和计算机体系结构
1. CS61C - Great Ideas in Computer Architecture (Berkeley)
• 课程：计算机体系结构的伟大思想
• 特点：从C语言到RISC-V汇编，再到硬件实现
• 项目：实现类MIPS处理器的模拟器
• 资源：完整的课程视频、讲义、作业
• GitHub: https://github.com/ucb-cs61c

2. Nand2Tetris (希伯来大学)
• 课程：从与非门到俄罗斯方块
• 特点：从最基础的逻辑门开始，逐步构建完整的计算机系统
• 内容：
  • 硬件：CPU、内存、机器语言
  • 软件：汇编器、虚拟机、编译器
• 网站: http://www.nand2tetris.org/
• 书籍: 《计算机系统要素》

3. CSAPP (CMU 15-213)
• 课程：计算机系统导论
• 特点：深入的x86-64汇编和系统编程
• 著名实验：
  • Data Lab：位操作
  • Bomb Lab：反汇编破解
  • Attack Lab：缓冲区溢出攻击
• 书籍: 《深入理解计算机系统》

4. 6.004 (MIT)
• 课程：计算结构
• 特点：从数字逻辑到指令集架构
• 使用：Beta处理器架构（类RISC）
• 资源: https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/

5. Stanford CS107 / CS107E
• CS107：计算机组成与系统
• CS107E：嵌入式系统的计算机组成（基于Raspberry Pi）
• 特点：直接在硬件上编写汇编，理解计算机启动过程

6. RISC-V 相关课程
Berkeley CS61C (新版)
• 使用RISC-V代替MIPS
• 更现代的指令集架构

MIT 6.191
• 基于RISC-V的数字集成电路
• 从算法到硬件实现
推荐学习路径
初学者路线
Nand2Tetris → CS61C → CSAPP
实践导向路线
CS107E (树莓派实践) → 6.004 → 专业项目
特色对比

课程 架构 难度 实践性 现代性
CS61C MIPS/RISC-V 中等 ⭐⭐⭐⭐ ⭐⭐⭐⭐
Nand2Tetris HACK 入门 ⭐⭐⭐⭐ ⭐⭐⭐
CSAPP x86-64 较高 ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐
6.004 Beta 较高 ⭐⭐⭐ ⭐⭐

获取方式

1. edX/Coursera：CS61C、Nand2Tetris有正式MOOC
2. 大学开放课程：MIT OCW、Stanford Engineering Everywhere
3. GitHub：搜索课程代码 + "solution"或"notes"
4. 课程官网：直接访问大学课程页面

这些课程都提供了完整的视频讲座、讲义、作业和实验项目，非常适合系统学习汇编语言和计算机体系结构！

## source code
musl 有汇编

## doc
NASM汇编语言编译器

https://www.nasm.us/

开源

https://blog.csdn.net/liigo/article/details/80680929

Microsoft Macro Assembler 8.0 (MASM) 

Microsoft Macro Assembler 8.0 (MASM) 是一个利用x86汇编语言程序并产生相应的二进制文件的工具。用MASM生成的汇编语言程序可以使用Visual C++ 2005 Express版进行编辑和调试。本软件包需要在计算机上先行安装Visual C++ 2005 Express版。

javap查看字节码

jclasslib IDEA插件

hsdis/使用hsdis查看jit生成的汇编代码

查看Java代码对应的汇编指令

https://blog.csdn.net/xiaojia1100/article/details/105387566

-server -Xcomp -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly -XX:CompileCommand=compileonly,*App.main  

是JVM直接提供的，在JVM里需要使用插件的方式，Kenai项目则提供了这个插件
下载：https://kenai.com/projects/base-hsdis/downloads https://github.com/liuzhengyang/hsdis
找到对应的指令集，操作系统所对应的so文件下载，好像不支持windows

https://blog.csdn.net/raintungli/article/details/9832783

Clion怎么查看反编译的汇编代码

https://github.com/lurumdare/awesome-asm

Mac OS X版本的sublime text 3安装汇编语言语法支持

/Users/${user}/Library/Application Support/Sublime Text 3/Packages

https://blog.csdn.net/qq_43678568/article/details/84071366

汇编语言的编程艺术(第2版)

VSCode + 插件（x86 and x86_64 Assembly）

现代的CPU/GPU把指令再分解成微指令

操作系统用到的汇编其实和CPU密切相关，什么实模式、保护模式， GDT, LDT，数据段，代码段......这些Intel CPU的概念如果没搞明白， 根本不可能读懂操作系统的启动过程。

什么是寄存器

程序在内存和CPU中是怎么折腾的

CPU是如何访问内存的

程序的分段

机器层面如何实现函数调用（理解缓冲区溢出攻击的基础）

中断及其处理

冯诺依曼计算机 图灵机

有了这些知识，肯定对冯诺依曼计算机有了深刻认识。

而这些知识又构成了操作系统的基础， 有了这些基础，理解进程/线程的概念，同步和互斥，以及他们的实现就非常容易，还有虚拟内存、文件系统、 I/O 等等。

并不是说必须学了汇编才能理解操作系统，而是说看问题的深度不一样。  有了汇编的保驾护航， 你可以在头脑中建立起一个有更多细节，更多实现的计算机， 那些概念不是模糊的，而是清晰的、鲜活的。

操作系统的运行原理， 绝对是程序员受益一生的知识。 比如说后端编程，不了解OS的进程、线程、 页面缓存，文件系统，I/O  就去大谈如何实现一个高并发、大数据量的网站简直就是笑话。

再比如对JVM的学习， 如果你懂得汇编， 看到JVM的字节码、看到栈帧就会觉得很亲切，只需要把基于寄存器的计算方式转换成基于栈的计算方式就可以了。

我们的计算机知识就像一座金字塔，  底层是数学， 上面是数字电路，然后是汇编，再往上是操作系统、网络，数据库、高级编程语言、框架等等

求伯君竟然用汇编写出了WPS！ Ken Thompson、Dennis Ritchie 居然用汇编写出操作系统Unix！

在某些情况下，你除了汇编没有别的选择——
CPU，时钟，以及内存尚未初始化的时候
当你需要切换CPU的工作模式的时候
当你需要直接操作协处理器的时候

对操作系统和计算机结构的理解，比如中断啊系统调用

汇编仅在优化的地方或者bootloader里面写写

俄罗斯方块 汇编写

https://github.com/jmechner/Prince-of-Persia-Apple-II

data

text

段

当年学C++时，对this指针不解，拿起ollydbg逆之，原来是这货在ECX里面，指向了类对象的数据成员，懂了以后，将某游戏的某C++对象内存dump下来， mov ecx,object; call object.method ,将某游戏爆出翔。
后来又学到虚函数，这又是什么鬼？ 老规矩，逆之，原来内存里面有一张虚函数表，这张表就如同一张的地图，指名实际要调用的函数，正是因为这张表，在sizeof(object)时，变大了。

看完上面，有没有感受到这种属性加成？你可以省去大量的谷歌，百度时间。

还有，可以分析编译器的智商程度，比如strlen,编译器竟然聪明到用
`repne scas BYTE PTR[EDI]`

巧妙实现，当时就给跪了。

https://www.zhihu.com/question/23088538/answer/295173568

树莓派汇编器

as

CentOS7写汇编并编译运行汇编代码

https://blog.csdn.net/chunxiaqiudong5/article/details/95937826

单片机

嵌入式

为何 x86 汇编会有两种语法，Intel 和 AT&T

Intel 语法是 Intel 自己发明的

貌似是 AT&T 想要定义一个跨平台的汇编语法，所以就无视 Intel 语法强制采用自家的语法了

能跑在对方的cpu上吗？