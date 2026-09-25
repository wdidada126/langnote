# Stanford CS110: Principles of Computer Systems 计算机系统原理

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | CS110: Principles of Computer Systems |
| 所属学校 | 斯坦福大学（Stanford） |
| 主讲 | Nick Troccoli（CS106B 原班教学团队延续开设） |
| 教材 | Computer Systems: A Programmer's Perspective 3/E（与 CSAPP 同教材，CS110 是其 Stanford 式进阶实践版） |
| csdiy 路径 | /计算机系统基础/CS110/ |
| 最新期次 | 每年滚动开课（csdiy 收录 winter20 站点与 spring19 视频，最新届见 cs110.stanford.edu） |
| 先修要求 | 编程基础、Unix、GDB、Valgrind（即 CS106B 水平）；语言 C/C++；难度 🌟🌟🌟🌟🌟；预计学时 150 小时 |
| 状态 | 骨架已建，正文待填充 |

## 为什么学

- 站在 CS106B（数据结构）与 CSAPP（系统概览）之上，专攻「设计大型系统、跨机器软件与并行计算」，是把 CSAPP 知识真正用起来的课。
- 每周 lab + 递进式项目：围绕同一套项目逐步加功能（mini malloc、Web Server、Shell、多线程/分布式 MapReduce），答案公开便于自查。
- 与 CSAPP 互补：CSAPP 讲「系统是什么」，CS110 讲「怎么用系统构件搭真实软件」；作业均配完整测试框架，自学友好度高。

## 先修与知识联系

| 方向 | 关联 |
| --- | --- |
| 先修 | CS106B/CS61B（C++/数据结构）、CS50/CS61A、Unix 工具链、GDB/Valgrind |
| 平行 | CSAPP（同教材；15-213 覆盖理论面，CS110 覆盖工程实践面） |
| 后续 | 6.S081/CS162（OS 内核）、CS244（网络）、CS149/6.824（并行与分布式） |
| 项目联系 | HTTP Server → CS144 Proxy Lab；线程池 → 15445；MapReduce → 6.824 |

## 最新年份讲义章节目录表（20 讲骨架，对应官网 lecture 排课主题）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：系统视角与程序构建全流程 | CSAPP Ch.1 |
| L2 | 程序到机器：编译、链接与加载全景回顾 | CSAPP Ch.7（复习） |
| L3 | 静态库与动态库、dlopen 与插件架构 | CSAPP Ch.7.10 |
| L4 | 内存映射：mmap 与文件/内存统一视图 | CS110 mmap 讲义 |
| L5 | 堆与动态内存：设计并实现 mini malloc | CSAPP Ch.9.9 |
| L6 | 文件与文件描述符：open/read/write 语义 | CSAPP Ch.10 |
| L7 | 系统级 I/O、标准 I/O 与缓冲策略 | CSAPP Ch.10.4–10.8 |
| L8 | 进程：fork/exec/wait 与进程生命周期 | CSAPP Ch.8.2–8.4 |
| L9 | 信号与异常控制流 | CSAPP Ch.8.5 |
| L10 | 管道与进程间通信（pipe/dup2） | CSAPP Ch.8.9 |
| L11 | 套接字与网络编程基础 | CSAPP Ch.11 |
| L12 | HTTP 协议与单连接 Web Server | RFC 9112 节选 |
| L13 | 并发 Web Server：进程/线程池模型 | 线程池设计讲义 |
| L14 | 线程 API 与共享数据竞争 | CSAPP Ch.12.3–12.5 |
| L15 | 锁、条件变量与生产者-消费者 | CSAPP Ch.12.6–12.7 |
| L16 | 信号量与同步设计模式 | CSAPP Ch.12.7 |
| L17 | 线程安全数据结构与原子操作 | CS110 并发讲义 |
| L18 | 事件驱动：select/poll 与 Reactor 模式 | Kegel "C10K" 文档 |
| L19 | 分布式入门：多机 MapReduce 与 RPC | Dean & Ghemawat, MapReduce (OSDI 2004) |
| L20 | 课程总结：系统权衡与设计原则复盘 | 全部讲义回顾 |

## 课程资源（摘自 csdiy）

- 课程网站：winter20 版；课程视频：spring19（B 站有搬运）
- 课程作业：7 labs + 8 assignments，参见课程网站
- 资源汇总：xuzheng465/Stanford_CS110（全部资源与作业实现）
