# Linux高级程序设计(第2版)



pdf windows电脑上有

豆瓣评价，有一些负面的信息，可以参考。

杨宗德

https://book.douban.com/subject/2364656/



涉及到系统编程的，没有使用图形工具

没有教学生写类似学生管理系统之类的东西

没有用开源库 libevent

libpng libjpeg只是简单的介绍了下

工具比较经典，但是不使用，工业界使用的图形工具 qt clion eclipse netbeans

autotools -> bazel cmake vcpkg meson conan xmake

make ->ninja



apt yum安装开发库也没介绍



#### Chap. 1

c 头文件

glibc 库函数

c语言没有为常见的操作，如：输入输出、内存管理、字符串操作等提供内置的支持。这些功能一般由标准的库函数来支持。





man

info



tar

expand

grep

find





#### Chap. 2 c语言开发环境

make

gdb

gcc

vim/source insight  /免费的VSCode装完clangd等插件，吊打SI





Chap. 3

Chap. 4

Chap. 5

Chap. 6

Chap. 7



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

22222222222222

[PCB](http://blog.csdn.net/wyzxg/article/details/4024340)

缓冲区是在用户空间，根据第4章的相关内容，子进程会复制父进程所有用户空间的

#### Chap. 9



Chap. 10

Chap. 11

Chap. 12

Chap. 13

tcpdump

lsof

netstat



Chap. 14