# Linux高级程序设计(第2版)

https://gitee.com/edidada/linuxadvancec

本书以Linux操作系统（内核为2.6版本）为开发平台、GCC 4.0/GDB 6.3为开发调试环境，详细介绍了Linux系统下编程环境及编程工具、文件管理（文件类型、ANSI以及POSIX标准下文件读写操作）、进程管理（创建、退出、执行、等待、属性控制）、进程间通信（管道、消息队列、共享内存）、进程间同步机制（信号量）、进程间异步机制（信号）、线程管理（创建、退出、取消等以及属性控制）、线程间同步（互斥锁、读写锁、条件变量）以及网络基本编程、高级应用等内容。

本书内容丰富、紧扣应用，适合从事Linux下C应用编程的人员阅读，也适合从事嵌入式Linux开发的人员阅读。


pdf windows电脑上有
ppt和代码 Linux高级程序设计2资源.zip
豆瓣评价，有一些负面的信息，可以参考。

杨宗德

https://book.douban.com/subject/2364656/
第二版 2008年
2012年第三版

介绍linux环境下c应用程序编程的

文件操作
进程/线程通信


涉及到系统编程的，没有使用图形工具

没有教学生写类似学生管理系统之类的东西

没有用开源库 libevent

libpng libjpeg只是简单的介绍了下

工具比较经典，但是不使用，工业界使用的图形工具 qt clion eclipse netbeans

autotools -> bazel cmake vcpkg meson conan xmake

make ->ninja



apt yum安装开发库也没介绍



#### Chap. 1 Linux c开发环境

c 头文件

glibc 库函数

c语言没有为常见的操作，如：输入输出、内存管理、字符串操作等提供内置的支持。这些功能一般由标准的库函数来支持。





man

info



tar

expand

grep

find





#### Chap. 2 Linux c语言开发工具

make

gdb

gcc

vim/source insight  /免费的VSCode装完clangd等插件，吊打SI





Chap. 3 进程存储管理 跟Chap7对比
mcheck
https://www.cnblogs.com/cyssmile/p/14003900.html
Valgrind
见md文件

Chap. 4 ansi c文件管理

Chap. 5 posix c文件管理

Chap. 6 普通文件管理

Chap. 7 进程管理与开发



#### Chap. 8



epoll是linux 2007年开始支持的





8.2进程管理及控制

111111111 fork()函数可以创建一个新的进程

// come from /usr/include/unistd.h

extern __pid_t fork(void)

__pid_t int
成功，在父进程中返回子进程pid
在子进程中返回0
失败，在父进程中返回 -1，错误原因存储在errorno中



[PCB](http://blog.csdn.net/wyzxg/article/details/4024340)

缓冲区是在用户空间，根据第4章的相关内容，子进程会复制父进程所有用户空间的

#### Chap. 9



Chap. 10 多线程编程

Chap. 11 线程同步机制

- 
- 
- 

Chap. 12 socket

Chap. 13 网络编程工具

tcpdump

lsof

netstat



Chap. 14