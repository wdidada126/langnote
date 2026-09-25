# CS110 讲义骨架（notes/outline.md）

> 每讲 3–5 条要点，骨架级；正文学习时逐条展开。

## L1 课程导论：系统视角与程序构建全流程
- 计算机系统 = 硬件 + 操作系统 + 运行时库 + 你的程序，四层协作执行一条语句。
- 源码到可执行文件的四个阶段：预处理、编译、汇编、链接。
- 「系统思维」：性能与正确性往往由抽象层边界的行为决定。
- 课程项目地图：mini malloc → Web Server → Shell → MapReduce。

## L2 程序到机器：编译、链接与加载全景回顾
- 目标文件（.o/ELF）三类：可重定位、可执行、共享对象。
- 符号解析与重定位：链接器如何 patch 地址。
- 加载时内核建立 mm_struct 与初始栈/堆布局。
- 复习 CSAPP Ch.7，为 dlopen 与 malloc 讲次铺垫。

## L3 静态库与动态库、dlopen 与插件架构
- .a 是 ar 打包的目标文件集合，链接时拷贝所需成员。
- .so 通过 PIC + GOT/PLT 实现位置无关与延迟绑定。
- dlopen/dlsym 把「链接」从构建期搬到运行期，支撑插件架构。
- 权衡：动态库省内存易升级，但版本漂移（DLL hell）风险高。

## L4 内存映射：mmap 与文件/内存统一视图
- mmap 把文件页直接映射进地址空间，read/write 变页错误驱动。
- MAP_SHARED 与 MAP_PRIVATE（写时复制）语义差异。
- 用 mmap 做匿名大内存分配，绕过内核堆拷贝路径。
- 项目：给 mini malloc 换用 mmap 管理超页（arena）。

## L5 堆与动态内存：设计并实现 mini malloc
- malloc/free 契约：任意顺序分配释放、碎片控制、对齐保证。
- 空闲链表 + first fit/best fit；边界标记（boundary tags）合并。
- 元数据开销 vs 内部碎片 vs 外部碎片的三角权衡。
- 常见 bug：double free、use-after-free、越界写坏元数据（Valgrind 复现）。

## L6 文件与文件描述符：open/read/write 语义
- fd 是进程级整数句柄，指向系统级 open file table 表项。
- 三张表模型：fd 表 → 打开文件表（偏移/状态标志）→ v-node 表。
- open 标志（O_APPEND/O_TRUNC/O_CREAT）与权限位、umask。
- 原子性：O_APPEND 写偏移更新的竞态意义。

## L7 系统级 I/O、标准 I/O 与缓冲策略
- printf 与 write 之间隔着用户态缓冲，fflush/setvbuf 控制时机。
- 行缓冲/全缓冲/无缓冲三模式及适用场景（终端 vs 文件 vs 管道）。
- 减少系统调用次数是 I/O 优化的第一原则。
- 权衡：缓冲区带来的进程异常时数据丢失风险。

## L8 进程：fork/exec/wait 与进程生命周期
- fork 复制地址空间（现代实现为 CoW），返回双子值。
- exec 家族替换镜像但保留 fd 与环境，构成 shell 启动程序的原语。
- wait 回收状态；孤儿与僵尸进程及 SIGCHLD 处理。
- 项目：Shell 的 fork+exec+wait 主循环。

## L9 信号与异常控制流
- 信号是内核向进程递送的软件中断，默认处置可捕获/忽略。
- 异步信号安全与信号掩码：handler 内只能调有限函数。
- SIGINT/SIGTSTP/SIGCHLD/SIGPIPE 的 shell 语义。
- 竞态：kill 与 sigprocmask 的顺序问题及 sigaction 解决法。

## L10 管道与进程间通信
- pipe 提供内核环形缓冲，dup2 重定向实现 `ls | wc -l`。
- 管道读端阻塞与 EOF：所有写端关闭才见 EOF。
- SIGPIPE 与 write 到已关闭读端。
- IPC 全景：管道/Unix socket/共享内存的拷贝次数对比。

## L11 套接字与网络编程基础
- socket/bind/listen/accept/connect 到一条 TCP 连接。
- 地址族与网络字节序（大端），getaddrinfo 解析。
- 客户端一行代码背后：三次握手与内核队列。
- 项目：Web Server 的 listen/accept 骨架。

## L12 HTTP 协议与单连接 Web Server
- 请求/响应报文结构：方法、URI、头部、状态码。
- 文本协议解析：按行读、空行结束、Content-Length。
- 静态文件服务：MIME 类型、404/403 语义、路径穿越防御。
- 每次连接一个请求的朴素模型及其性能瓶颈。

## L13 并发 Web Server：进程/线程池模型
- fork-per-request 与 thread-per-request 的开销剖析。
- 线程池 + 任务队列把「连接建立」与「请求处理」解耦。
- 共享日志/缓存需要锁；accept 竞争与惊群初探。
- 权衡：隔离性（进程）vs 轻量共享（线程）。

## L14 线程 API 与共享数据竞争
- pthread_create/pthread_join；同一地址空间内多控制流。
- 竞争条件：read-modify-write 非原子导致计数错误。
- 数据竞争 vs 竞态条件（时序 bug）的区分。
- Valgrind/heapcheck 与线程调试工具（Helgrind/TSan）。

## L15 锁、条件变量与生产者-消费者
- 互斥锁保护临界区；死锁四条件与锁序约定。
- 条件变量必须配合 while 谓词循环防虚假唤醒。
- 生产者-消费者有界缓冲：本课程的核心同步范式。
- 锁粒度：粗锁简单、细锁高并发但易错。

## L16 信号量与同步设计模式
- 信号量计数语义：P/V 解耦「互斥」与「顺序」。
- 读者-写者、屏障、流水线等模式。
- 用信号量实现互斥锁与条件变量的思路。
- 何时选无锁结构：延迟敏感场景导引。

## L17 线程安全数据结构与原子操作
- 线程安全哈希表/队列的分段锁设计。
- 原子指令 CAS/FAA 与内存序（relaxed/acquire/release）初步。
- 锁 vs 原子：单字操作用原子，多字段不变量用锁。
- 为 MapReduce Worker 池准备并发容器。

## L18 事件驱动：select/poll 与 Reactor 模式
- 单线程多路复用：就绪表 + 非阻塞状态机。
- select 的 fd 集上限与 O(n) 轮询，poll/epoll 改进方向。
- Reactor 与 thread-per-request 的资源模型对比（C10K）。
- 权衡：事件驱动复杂度高但无切换开销。

## L19 分布式入门：多机 MapReduce 与 RPC
- 跨机通信回到 socket：序列化与 RPC 抽象。
- MapReduce 分而治之：分片、shuffle、聚合容错。
- Master/Worker 心跳与任务重派发。
- 与 6.824 的分工：本课给使用级直觉，6.824 给实现级深度。

## L20 课程总结：系统权衡与设计原则复盘
- 贯穿主线：抽象、缓存、并发三板斧在每层重现。
- 权衡清单：拷贝次数、锁粒度、缓冲深度、进程 vs 线程 vs 事件。
- 系统 debug 方法论：strace/lldb/core dump/Valgrind 组合拳。
- 通往 CS140/6.S081/CS149/CS244 的知识地图。
