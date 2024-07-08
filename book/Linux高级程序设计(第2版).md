# Linux高级程序设计(第2版)
c语言的，不是c++的
https://gitee.com/edidada/linuxadvancec

本书以Linux操作系统（内核为2.6版本）为开发平台、GCC 4.0/GDB 6.3为开发调试环境，详细介绍了Linux系统下编程环境及编程工具、文件管理（文件类型、ANSI以及POSIX标准下文件读写操作）、进程管理（创建、退出、执行、等待、属性控制）、进程间通信（管道、消息队列、共享内存）、进程间同步机制（信号量）、进程间异步机制（信号）、线程管理（创建、退出、取消等以及属性控制）、线程间同步（互斥锁、读写锁、条件变量）以及网络基本编程、高级应用等内容。

本书内容丰富、紧扣应用，适合从事Linux下C应用编程的人员阅读，也适合从事嵌入式Linux开发的人员阅读。

pdf windows电脑上有
ppt和代码 Linux高级程序设计2资源.zip
豆瓣评价，有一些负面的信息，可以参考。

杨宗德

https://book.douban.com/subject/2364656/
第二版 2008年
9787115171696

2012年第三版
https://book.douban.com/subject/20273594/

介绍linux环境下c应用程序编程的

文件操作
进程/线程通信


涉及到系统编程的，没有使用图形工具

没有教学生写类似学生管理系统之类的东西

没有用开源库 libevent

libpng libjpeg只是简单的介绍了下 math库 pthread

工具比较经典，但是不使用，工业界使用的图形工具 vs qt clion eclipse netbeans
介绍了vi vim sourceinsight gcc g++
autotools -> bazel cmake vcpkg meson conan xmake

make ->ninja

apt yum安装开发库也没介绍

#### Chap. 1 Linux c开发环境

c 头文件

glibc 库函数

c语言没有为常见的操作，如：输入输出、内存管理、字符串操作等提供内置的支持。这些功能一般由标准的库函数来支持。
coreutils 库也没有介绍
CP命令的源代码是包含在coreutils里的，上gnu网站看看： http://www.gnu.org/software/coreutils/coreutils.html

gnu有介绍

man

info

tar

expand

grep

find

个人补充：
sed
cat
cp
ls
mv
ssh
scp

#### Chap. 2 Linux c语言开发工具
2.3 Make工具与Makefile文件
2.6Autoconf/Automake自动化工具
make

gdb lldb

gcc

vim/source insight  /免费的VSCode装完clangd等插件，吊打SI

#### Chap. 3 Linux进程存储管理 跟Chap7对比
3.1 elf文件接口

testlinuxlibcrypt是可执行文件

```
size testlinuxlibcrypt
text    data     bss     dec     hex filename
2470     656       8    3134     c3e testlinuxlibcrypt
```

3.2 linux进程结构
QQ 运行两个，有些区域是共用的

静态分配:编译器在处理程序源代码时分配。
动态分配:程序在执行时调用malloc()库函数申请分配。

extern 

mcheck
https://www.cnblogs.com/cyssmile/p/14003900.html
mcheck是GNU C库提供的一种用于检测C程序内存一致性的工具，常被用于调试内存相关的问题，如内存泄漏、双重释放和内存越界等问题。
在使用mcheck时，需要在程序中包含mcheck.h头文件，以便获得与内存调试相关的函数和类型定义。例如，可以使用MCHECK_DISABLED、MCHECK_OK、MCHECK_FREE等枚举类型来表示不同的内存状态。为了启用mcheck的检测功能，需要调用mcheck()或mcheck_pedantic()函数，并传入一个错误处理函数，这个错误处理函数将在检测到内存异常时被调用。
在编译使用mcheck的程序时，需要确保编译器和链接器能够找到并正确处理mcheck.h头文件以及相关函数。通常情况下，这需要使用支持GNU C库的编译器，并在编译命令中加入相应的选项，如-g用于生成调试信息。
总的来说，通过包含mcheck.h头文件并在代码中正确使用mcheck提供的API，可以有效检测C程序中的内存问题。结合正确的编译选项和运行时环境设置，能够最大化利用mcheck工具的功能，帮助开发者定位并解决内存泄露、越界等棘手问题。

Valgrind
见md文件

ansi c内存控制api
malloc()
free()

#### Chap. 4 ansi c文件管理
fopen()
fwrite()
rewind()
fclose()
fgetc()
fputs()

注意头文件和库文件
#### Chap. 5 posix c文件管理 POSIX文件及目录管理
getcwd()
open()
fcntl()
write()
close()
creat()
lseek()
mmap()
munmap()

注意头文件和库文件

#### Chap. 6 普通文件管理 普通文件．连接文件及目录文件属性管理
chmod
unlink
#include<utime.h>
#include<time.h>

time
ctime
utime

#### Chap. 7 Linux进程管理与程序开发
signal
wait
fork
vfork

#### #### Chap. 8 进程间通信——管道和信号

popen

epoll是linux 2007年开始支持的

##### 8.2进程管理及控制

111111111 fork()函数可以创建一个新的进程

// come from /usr/include/unistd.h

extern __pid_t fork(void)

__pid_t int
成功，在父进程中返回子进程pid
在子进程中返回0
失败，在父进程中返回 -1，错误原因存储在errorno中

[PCB](http://blog.csdn.net/wyzxg/article/details/4024340)

缓冲区是在用户空间，根据第4章的相关内容，子进程会复制父进程所有用户空间的

#### Chap. 9 SystemV进程间通信


#### Chap. 10 多线程编程
- 10.1线程基本概念与线程操作
- 10.2线程属性控制
- 10.3线程调度策略

#### Chap. 11 线程同步机制
- 11.1互斥锁通信机制 mutex
- 11.2条件变量通信机制 condictionvariable
- 11.3读写锁通信机制 readwriteLock
- 11.4线程与信号 


#### 11.1互斥锁通信机制 mutex


初始化互斥锁
阻塞申请互斥锁
释放互斥锁
非阻塞申请互斥锁
销毁互斥锁
功能
互斥锁基本操作函数
pthread_mutex_init
pthread_mutex_lock
pthread_mutex_unlock
pthread_mutex_trylock
pthread_mutex_destroy

互斥锁（Mutex）是一种用于多线程编程中保护共享资源的工具。在C语言中，可以使用POSIX线程库中的`pthread_mutex_t`类型和相关函数来操作互斥锁。以下是互斥锁的基本操作函数及其功能：

1. 初始化互斥锁：`pthread_mutex_init`函数用于初始化一个互斥锁。它需要一个指向`pthread_mutex_t`类型的指针和一个互斥属性对象。通常，我们使用默认的属性对象`PTHREAD_MUTEX_DEFAULT`。

```c
#include <pthread.h>

pthread_mutex_t mutex;
int result = pthread_mutex_init(&mutex, NULL);
if (result != 0) {
    // 处理错误
}
```

2. 阻塞申请互斥锁：`pthread_mutex_lock`函数用于阻塞地申请互斥锁。如果互斥锁已经被其他线程锁定，当前线程将等待直到互斥锁被释放。

```c
int result = pthread_mutex_lock(&mutex);
if (result != 0) {
    // 处理错误
}
```

3. 释放互斥锁：`pthread_mutex_unlock`函数用于释放互斥锁，允许其他线程获取该锁。

```c
int result = pthread_mutex_unlock(&mutex);
if (result != 0) {
    // 处理错误
}
```

4. 非阻塞申请互斥锁：`pthread_mutex_trylock`函数尝试非阻塞地申请互斥锁。如果互斥锁已经被其他线程锁定，函数将立即返回并设置错误码为EBUSY。

```c
int result = pthread_mutex_trylock(&mutex);
if (result == EBUSY) {
    // 互斥锁已被锁定，无法获取
} else if (result != 0) {
    // 处理其他错误
}
```

5. 销毁互斥锁：`pthread_mutex_destroy`函数用于销毁一个已经初始化的互斥锁。在销毁之后，互斥锁不能再被使用。

```c
int result = pthread_mutex_destroy(&mutex);
if (result != 0) {
    // 处理错误
}
```
#### 11.2条件变量通信机制 condictionvariable

初始化条件变量
阻塞等待条件变量
通知等待该条件变量的第1个线程
在指定的时间之内阻塞等待条件变量
通知等待该条件变量的所有线程
销毁条件变量状态


pthread_cond_init
pthread_cond_wait
pthread_cond_signal
pthread_cond_timedwait
pthread_cond_broadcast
pthread_cond_destroy

- pthread_condattr_init
- pthread_condattr_destroy
- pthread_condattr_setpshared
- pthread_condattr_getclock
- pthread_condattr_setclock


#### 11.3读写锁通信机制 readwriteLock


初始化读写锁
阻塞申请读锁
非阻塞申请读锁
阻塞申请写锁
非阻塞中请写锁
释放锁(无论是读锁还是写锁)
销毁读写锁

pthread_rwlock_init
pthread_rwlock_rdlock
pthread_rwlock_tryrdlock
pthread_rwlock_wrlock
pthread_rwlock_trywrlock
pthread_rwlock_unlock
pthread_rwlock_destroy

https://www.man7.org/linux/man-pages/man3/pthread_rwlock_init.3p.html

- 11.4线程与信号 

OS中会介绍三种互斥算法，即锁，条件变量，信号量




- pthread_spin_init
- pthread_spin_destroy
- pthread_spin_lock
- pthread_spin_trylock
- pthread_spin_unlock


- pthread_barrier_init
- pthread_barrier_destroy
- pthread_barrier_wait
- pthread_barrierattr_init
- pthread_barrierattr_destroy
- pthread_barrierattr_getpshared
- pthread_barrierattr_setpshared


- pthread_key_create
- pthread_key_delete
- pthread_getspecific
- pthread_setspecific

#### Chap. 12 socket网络编程

#### Chap. 13 网络编程工具

tcpdump
lsof
netstat

#### Chap. 14 网络编程高级应用

select poll epoll

本章就TCP、UDP网络编程高级应用进行详细介绍，主要包括非阻塞I/O处理、多路复用、信号驱动以及UDP广播和组播通信、原始套接口等内容。

- 第1节主要介绍1/0阻塞与非阻塞操作的基本应用，即解决在读写操作时，如果没有可操作数据，操作进程将一直阻塞的问题，
- 第2节主要介绍socket多路复用技术，即使用select函数实现某个进程阻塞于多个socket文件描述符的情况，从而提高应用效率。
- 第3节主要介绍socket信号驱动，首先对各I/0类型进行比较然后重点介绍UDP对SIGIO信号的处理。
- 第4节主要介绍UDP广播与组播通信，即在局域网内，使用UDP实现一点对多点同时传送数据的应用。
- 第5节主要介绍原始套接口基本应用，即如何自己构建IP数据包头，TCP 数据包头。

sockaddr_in 结构体是在网络编程中用于表示IPv4地址和端口号的一个结构体，它定义在特定的头文件中。具体来说，sockaddr_in 结构体通常定义在 <netinet/in.h> 头文件中。然而，在某些情况下，<arpa/inet.h> 头文件也可能包含对 sockaddr_in 的定义，这主要取决于操作系统和编译环境。

头文件信息
主要头文件：<netinet/in.h>
这个头文件是网络编程中非常核心的一个，它包含了多种与Internet地址族相关的结构体和函数声明，如sockaddr_in、in_addr结构体，以及inet_aton、inet_ntoa等函数。
辅助头文件：<arpa/inet.h>
这个头文件也提供了网络编程中常用的函数，如字节序转换函数htonl、htons、ntohl、ntohs，以及inet_addr、inet_ntoa等地址转换函数。虽然它不直接定义sockaddr_in结构体，但在处理网络字节序和地址转换时非常有用，因此常常与<netinet/in.h>一起被包含在网络编程的代码中。
使用建议
在进行网络编程时，如果需要使用sockaddr_in结构体，建议首先包含<netinet/in.h>头文件。如果还需要进行字节序转换或地址转换等操作，可以再包含<arpa/inet.h>头文件。

示例代码
以下是一个简单的示例，展示了如何在C或C++程序中使用sockaddr_in结构体：

```c
#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
#include <netinet/in.h> // 包含sockaddr_in定义  
#include <arpa/inet.h>  // 包含inet_addr和htons等函数声明  
  
int main() {  
    struct sockaddr_in server_addr;  
  
    // 初始化server_addr  
    memset(&server_addr, 0, sizeof(server_addr)); // 清除结构体内存  
    server_addr.sin_family = AF_INET; // 设置地址族为IPv4  
    server_addr.sin_port = htons(8080); // 设置端口号，注意转换为网络字节序  
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // 设置IP地址  
  
    // ... 其他网络编程代码 ...  
  
    return 0;  
}
```
在这个示例中，我们首先包含了<netinet/in.h>和<arpa/inet.h>头文件，以便使用sockaddr_in结构体和相关函数。然后，我们创建了一个sockaddr_in类型的变量server_addr，并使用memset函数将其内存初始化为0。接着，我们设置了server_addr的地址族、端口号和IP地址。注意，端口号需要使用htons函数转换为网络字节序。


## sockaddr

struct sockaddr_in server_address;
(struct sockaddr *)&server_address

struct sockaddr_in 和 struct sockaddr 在网络编程中都扮演着重要的角色，它们之间存在特定的关系。

结构体定义：
struct sockaddr 是一个通用的套接字地址结构体，它主要用于存储套接字地址信息。这个结构体是抽象的，不直接包含IP地址和端口号等具体信息，而是提供了一个通用的接口来访问这些信息。
struct sockaddr_in 是一个基于struct sockaddr的扩展结构体，它专门用于存储IPv4地址和端口号信息。sockaddr_in结构体包含了sockaddr结构体作为它的第一个成员，这使得sockaddr_in结构体可以强制转换为sockaddr结构体类型。
关系：
struct sockaddr_in是struct sockaddr的一个具体实现，专门用于IPv4地址。由于sockaddr_in包含了sockaddr作为它的第一个成员，因此可以将sockaddr_in结构体的地址强制转换为sockaddr结构体的指针，而不会破坏内存布局。
类型转换：
在网络编程中，经常需要将struct sockaddr_in类型的变量转换为struct sockaddr类型的指针。这是因为一些套接字函数（如bind、connect等）的参数是struct sockaddr类型的指针，而不是struct sockaddr_in类型的指针。通过强制类型转换，我们可以将这些函数用于IPv4地址。
示例：
```c
struct sockaddr_in server_address;  
// ... 初始化server_address ...  
struct sockaddr *sock_addr = (struct sockaddr *)&server_address;
```
在这个示例中，我们创建了一个struct sockaddr_in类型的变量server_address，并将其地址强制转换为struct sockaddr类型的指针sock_addr。这样，我们就可以将sock_addr传递给需要struct sockaddr类型指针的套接字函数了。

