# Linux高性能服务器编程

https://book.douban.com/subject/24722611/

作者: 游双
出版社: 机械工业出版社
出版年: 2013-5-1
页数: 360
定价: CNY 69.00
装帧: 平装
丛书: 华章科技·实战系列
ISBN: 9787111425199

https://github.com/edidada/LinuxServerCodesYouShuang

# 使用 CMake 配置项目并指定 Ninja 生成器
cmake -G "Ninja" ..

poll
epoll
lt
gt模式？

libevent c库
基本都是c，linux c api
参考代码是cpp后缀的
mingw编译不了，有linux os api

源码
G:\Linux高性能服务器编程清晰PDF+源码\LinuxServerCodes

第一篇 TCPIP协议详解
第二篇 深入解析高性能服务器编程
第三篇 高性能服务器优化与监测

第一篇 TCPIP协议详解
第1章 TCPIP协议族
1.1 TCPIP协议族体系结构以及主要协议
1.1.1 数据链路层
1.1.2 网络层
1.1.3 传输层
1.1.4 应用层
1.2 封装
1.3 分用
1.4 测试网络
1.5 ARP协议工作原理
1.5.1 以太网ARP请求应答报文详解
1.5.2 ARP高速缓存的查看和修改
1.5.3 使用tcpdump观察ARP通信过程
1.6 DNS工作原理
1.6.1 DNS查询和应答报文详解
1.6.2 Linux下访问DNS服务
1.6.3 使用tcpdump观察DNS通信过程
1.7 socket和TCPIP协议族的关系

第2章 IP协议详解
2.1 IP服务的特点
2.2 IPv4头部结构
2.2.1 IPv4头部结构
2.2.2 使用tcpdump观察IPv4头部结构
2.3 IP分片
2.4 IP路由
2.4.1 IP模块工作流程
2.4.2 路由机制
2.4.3 路由表更新
2.5 IP转发
2.6 重定向
2.6.1 ICMP重定向报文
2.6.2 主机重定向实例
2.7 IPv6头部结构
2.7.1 IPv6固定头部结构
2.7.2 IPv6扩展头部

第3章 TCP协议详解
3.1 TCP服务的特点
3.2 TCP头部结构
3.2.1 TCP固定头部结构
3.2.2 TCP头部选项
3.2.3 使用tcpdump观察TCP头部信息
3.3 TCP连接的建立和关闭
3.3.1 使用tcpdump观察TCP连接的建立和关闭
3.3.2 半关闭状态
3.3.3 连接超时
3.4 TCP状态转移
3.4.1 TCP状态转移总图
3.4.2 TIME_WAIT状态
3.5 复位报文段
3.5.1 访问不存在的端口
3.5.2 异常终止连接
3.5.3 处理半打开连接
3.6 TCP交互数据流
3.7 TCP成块数据流
3.8 带外数据
3.9 TCP超时重传
3.10 拥塞控制
3.10.1 拥塞控制概述
3.10.2 慢启动和拥塞避免
3.10.3 快速重传和快速恢复

第4章 TCPIP通信案例：访问Internet上的Web服务器
4.1 实例总图
4.2 部署代理服务器
4.2.1 HTTP代理服务器的工作原理
4.2.2 部署squid代理服务器
4.3 使用tcpdump抓取传输数据包
4.4 访问DNS服务器
4.5 本地名称查询
4.6 HTTP通信
4.6.1 HTTP请求
4.6.2 HTTP应答
4.7 实例总结

第二篇 深入解析高性能服务器编程
第5章 Linux网络编程基础API
5.1 socket地址API
5.1.1 主机字节序和网络字节序
5.1.2 通用socket地址
5.1.3 专用socket地址
5.1.4 IP地址转换函数
5.2 创建socket
5.3 命名socket
5.4 监听socket
5.5 接受连接
5.6 发起连接
5.7 关闭连接
5.8 数据读写
5.8.1 TCP数据读写
5.8.2 UDP数据读写
5.8.3 通用数据读写函数
5.9 带外标记
5.10 地址信息函数
5.11 socket选项
5.11.1 SO_REUSEADDR选项
5.11.2 SO_RCVBUF和SO_SNDBUF选项
5.11.3 SO_RCVLOWAT和SO_SNDLOWAT选项
5.11.4 SO_LINGER选项
5.12 网络信息API
5.12.1 gethostbyname和gethostbyaddr
5.12.2 getservbyname和getservbyport
5.12.3 getaddrinfo
5.12.4 getnameinfo

第6章 高级IO函数
6.1 pipe函数
6.2 dup函数和dup2函数
6.3 readv函数和writev函数
6.4 sendfile函数
6.5 mmap函数和munmap函数
6.6 splice函数
6.7 tee函数
6.8 fcntl函数

第7章 Linux服务器程序规范
7.1 日志
7.1.1 Linux系统日志
7.1.2 syslog函数
7.2 用户信息
7.2.1 UID、EUID、GID和EGID
7.2.2 切换用户
7.3 进程间关系
7.3.1 进程组
7.3.2 会话
7.3.3 用ps命令查看进程关系
7.4 系统资源限制
7.5 改变工作目录和根目录
7.6 服务器程序后台化
第8章 高性能服务器程序框架
8.1 服务器模型
8.1.1 CS模型
8.1.2 P2P模型
8.2 服务器编程框架
8.3 IO模型
8.4 两种高效的事件处理模式
8.4.1 Reactor模式
8.4.2 Proactor模式
8.4.3 模拟Proactor模式
8.5 两种高效的并发模式
8.5.1 半同步半异步模式
8.5.2 领导者追随者模式
8.6 有限状态机
8.7 提高服务器性能的其他建议
8.7.1 池
8.7.2 数据复制
8.7.3 上下文切换和锁

第9章 IO复用
9.1 select系统调用
9.1.1 select API
9.1.2 文件描述符就绪条件
9.1.3 处理带外数据
9.2 poll系统调用
9.3 epoll系列系统调用
9.3.1 内核事件表
9.3.2 epoll_wait函数
9.3.3 LT和ET模式
9.3.4 EPOLLONESHOT事件
9.4 三组IO复用函数的比较
9.5 IO复用的高级应用一：非阻塞connect
9.6 IO复用的高级应用二：聊天室程序
9.6.1 客户端
9.6.2 服务器
9.7 IO复用的高级应用三：同时处理TCP和UDP服务
9.8 超级服务xinetd
9.8.1 xinetd配置文件
9.8.2 xinetd工作流程
第10章 信号
10.1 Linux信号概述
10.1.1 发送信号
10.1.2 信号处理方式
10.1.3 Linux信号
10.1.4 中断系统调用
10.2 信号函数
10.2.1 signal系统调用
10.2.2 sigaction系统调用
10.3 信号集
10.3.1 信号集函数
10.3.2 进程信号掩码
10.3.3 被挂起的信号
10.4 统一事件源
10.5 网络编程相关信号
10.5.1 SIGHUP
10.5.2 SIGPIPE
10.5.3 SIGURG

第11章 定时器
11.1 socket选项SO_RCVTIMEO和SO_SNDTIMEO
11.2 SIGALRM信号
11.2.1 基于升序链表的定时器
11.2.2 处理非活动连接
11.3 IO复用系统调用的超时参数
11.4 高性能定时器
11.4.1 时间轮
11.4.2 时间堆

第12章 高性能IO框架库Libevent
12.1 IO框架库概述
12.2 Libevent源码分析
12.2.1 一个实例
12.2.2 源代码组织结构
12.2.3 event结构体
12.2.4 往注册事件队列中添加事件处理器
12.2.5 往事件多路分发器中注册事件
12.2.6 eventop结构体
12.2.7 event_base结构体
12.2.8 事件循环

第13章 多进程编程
13.1 fork系统调用
13.2 exec系列系统调用
13.3 处理僵尸进程
13.4 管道
13.5 信号量
13.5.1 信号量原语
13.5.2 semget系统调用
13.5.3 semop系统调用
13.5.4 semctl系统调用
13.5.5 特殊键值IPC_PRIVATE
13.6 共享内存
13.6.1 shmget系统调用
13.6.2 shmat和shmdt系统调用
13.6.3 shmctl系统调用
13.6.4 共享内存的POSIX方法
13.6.5 共享内存实例
13.7 消息队列
13.7.1 msgget系统调用
13.7.2 msgsnd系统调用
13.7.3 msgrcv系统调用
13.7.4 msgctl系统调用
13.8 IPC命令
13.9 在进程间传递文件描述符

第14章 多线程编程
14.1 Linux线程概述
14.1.1 线程模型
14.1.2 Linux线程库
14.2 创建线程和结束线程
14.3 线程属性
14.4 POSIX信号量
14.5 互斥锁
14.5.1 互斥锁基础API
14.5.2 互斥锁属性
14.5.3 死锁举例
14.6 条件变量
14.7 线程同步机制包装类
14.8 多线程环境
14.8.1 可重入函数
14.8.2 线程和进程
14.8.3 线程和信号
第15章 进程池和线程池
15.1 进程池和线程池概述
15.2 处理多客户
15.3 半同步半异步进程池实现
15.4 用进程池实现的简单CGI服务器
15.5 半同步半反应堆线程池实现
15.6 用线程池实现的简单Web服务器
15.6.1 http_conn类
15.6.2 main函数

第三篇 高性能服务器优化与监测
第16章 服务器调制、调试和测试
16.1 最大文件描述符数
16.2 调整内核参数
16.2.1 procsysfs目录下的部分文件
16.2.2 procsysnet目录下的部分文件
16.3 gdb调试
16.3.1 用gdb调试多进程程序
16.3.2 用gdb调试多线程程序
16.4 压力测试

第17章 系统监测工具
17.1 tcpdump
17.2 lsof
17.3 nc
17.4 strace
17.5 netstat
17.6 vmstat
17.7 ifstat
17.8 mpstat

## 笔记
## 第一篇 TCPIP协议详解

### 第1章 TCPIP协议族
#### 1.1 TCPIP协议族体系结构以及主要协议
1.1.1 数据链路层
1.1.2 网络层
1.1.3 传输层
1.1.4 应用层
1.2 封装
1.3 分用
1.4 测试网络
1.5 ARP协议工作原理
1.5.1 以太网ARP请求应答报文详解
1.5.2 ARP高速缓存的查看和修改
1.5.3 使用tcpdump观察ARP通信过程
1.6 DNS工作原理
1.6.1 DNS查询和应答报文详解
1.6.2 Linux下访问DNS服务
1.6.3 使用tcpdump观察DNS通信过程
1.7 socket和TCPIP协议族的关系



### 第2章 IP协议详解
2.1 IP服务的特点
2.2 IPv4头部结构
2.2.1 IPv4头部结构
2.2.2 使用tcpdump观察IPv4头部结构
2.3 IP分片
2.4 IP路由
2.4.1 IP模块工作流程
2.4.2 路由机制
2.4.3 路由表更新
2.5 IP转发
2.6 重定向
2.6.1 ICMP重定向报文
2.6.2 主机重定向实例
2.7 IPv6头部结构
2.7.1 IPv6固定头部结构
2.7.2 IPv6扩展头部

### 第3章 TCP协议详解
3.1 TCP服务的特点
3.2 TCP头部结构
3.2.1 TCP固定头部结构
3.2.2 TCP头部选项
3.2.3 使用tcpdump观察TCP头部信息
3.3 TCP连接的建立和关闭
3.3.1 使用tcpdump观察TCP连接的建立和关闭
3.3.2 半关闭状态
3.3.3 连接超时
3.4 TCP状态转移
3.4.1 TCP状态转移总图
3.4.2 TIME_WAIT状态
3.5 复位报文段
3.5.1 访问不存在的端口
3.5.2 异常终止连接
3.5.3 处理半打开连接
3.6 TCP交互数据流
3.7 TCP成块数据流
3.8 带外数据
3.9 TCP超时重传
3.10 拥塞控制
3.10.1 拥塞控制概述
3.10.2 慢启动和拥塞避免
3.10.3 快速重传和快速恢复

### 第4章 TCPIP通信案例：访问Internet上的Web服务器
4.1 实例总图
4.2 部署代理服务器
4.2.1 HTTP代理服务器的工作原理
4.2.2 部署squid代理服务器
4.3 使用tcpdump抓取传输数据包
4.4 访问DNS服务器
4.5 本地名称查询
4.6 HTTP通信
4.6.1 HTTP请求
4.6.2 HTTP应答
4.7 实例总结

## 第二篇 深入解析高性能服务器编程
### 第5章 Linux网络编程基础API
5.1 socket地址API
5.1.1 主机字节序和网络字节序
5.1.2 通用socket地址
5.1.3 专用socket地址
5.1.4 IP地址转换函数
5.2 创建socket
5.3 命名socket
5.4 监听socket
5.5 接受连接
5.6 发起连接
5.7 关闭连接
5.8 数据读写
5.8.1 TCP数据读写
5.8.2 UDP数据读写
5.8.3 通用数据读写函数
5.9 带外标记
5.10 地址信息函数
5.11 socket选项
5.11.1 SO_REUSEADDR选项
5.11.2 SO_RCVBUF和SO_SNDBUF选项
5.11.3 SO_RCVLOWAT和SO_SNDLOWAT选项
5.11.4 SO_LINGER选项
5.12 网络信息API
5.12.1 gethostbyname和gethostbyaddr
5.12.2 getservbyname和getservbyport
5.12.3 getaddrinfo
5.12.4 getnameinfo

Java程序是大端

socket对应多个协议

IP地址转换函数
inet_addr()
inet_aton()
inet_ntoa()

在 C/C++ 网络编程中，处理 IP 地址时经常需要用到一些标准库函数来进行 IP地址字符串与网络字节序整数之间的转换。以下是三个常用的函数：

- `inet_addr()`
- `inet_aton()`
- `inet_ntoa()`

它们都定义在 `<arpa/inet.h>`（Linux/macOS）或 `<winsock2.h>`（Windows）中。

---

## 📌 1. `inet_addr()`

### ✅ 功能：
将 IPv4 地址字符串（如 `"192.168.1.1"`）转换为一个 32 位的网络字节序整数（`in_addr_t` 类型）。

### ⚠️ 注意：
- 已被标记为 过时（obsolete），建议使用 `inet_aton()`。
- 返回值类型是 `in_addr_t`，失败返回 `INADDR_NONE`。

### 🔧 示例：

```c
#include <stdio.h>
#include <arpa/inet.h>

int main() {
    const char* ip_str = "192.168.0.1";
    in_addr_t ip_num = inet_addr(ip_str);

    if (ip_num == INADDR_NONE) {
        printf("Invalid IP address\n");
    } else {
        printf("inet_addr(\"%s\") = %u (network byte order)\n", ip_str, (unsigned int)ip_num);
    }

    return 0;
}
```

### 输出示例：

```
inet_addr("192.168.0.1") = 3232235521 (network byte order)
```

---

## 📌 2. `inet_aton()`

### ✅ 功能：
将 IPv4 地址字符串转换为二进制形式，并存储到 `struct in_addr` 中。

### 🟡 推荐使用：
比 `inet_addr()` 更安全，支持 CIDR 表示法和错误检查。

### 🔧 示例：

```c
#include <stdio.h>
#include <arpa/inet.h>

int main() {
    const char* ip_str = "192.168.0.1";
    struct in_addr ip;

    if (inet_aton(ip_str, &ip) == 0) {
        printf("Invalid IP address\n");
    } else {
        printf("inet_aton(\"%s\") -> s_addr = %u\n", ip_str, ip.s_addr);
    }

    return 0;
}
```

### 输出示例：

```
inet_aton("192.168.0.1") -> s_addr = 3232235521
```

---

## 📌 3. `inet_ntoa()`

### ✅ 功能：
将 `struct in_addr` 类型的网络地址转换回点分十进制的 IP 字符串（例如 `"192.168.0.1"`）。

### ⚠️ 注意：
- 是 非线程安全 的（返回的是内部静态缓冲区），多线程下应使用 `inet_ntop()` 替代。
- 只适用于 IPv4。

### 🔧 示例：

```c
#include <stdio.h>
#include <arpa/inet.h>

int main() {
    struct in_addr ip;
    inet_aton("192.168.0.1", &ip); // 先转成 in_addr

    char* ip_str = inet_ntoa(ip);
    printf("inet_ntoa(s_addr=%u) = %s\n", ip.s_addr, ip_str);

    return 0;
}
```

### 输出示例：

```
inet_ntoa(s_addr=3232235521) = 192.168.0.1
```

---

## 🆕 更现代的替代方案：`inet_pton()` 和 `inet_ntop()`

这些函数支持 IPv6，且线程安全。

### 示例（IPv4）：

```c
#include <stdio.h>
#include <arpa/inet.h>

int main() {
    const char* ip_str = "192.168.0.1";
    struct in_addr ip;

    // 字符串转结构体
    if (inet_pton(AF_INET, ip_str, &ip) <= 0) {
        printf("Invalid IP\n");
        return 1;
    }

    // 结构体转字符串
    char output[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &ip, output, INET_ADDRSTRLEN);

    printf("inet_pton(\"%s\") -> s_addr = %u\n", ip_str, ip.s_addr);
    printf("inet_ntop(s_addr=%u) = %s\n", ip.s_addr, output);

    return 0;
}
```

---

## ✅ 总结对比表：

| 函数名称       | 功能                             | 是否线程安全 | 支持 IPv6 | 备注 |
|----------------|----------------------------------|---------------|------------|------|
| `inet_addr()`  | IP字符串 ➜ `in_addr_t`           | ❌             | ❌         | 已废弃 |
| `inet_aton()`  | IP字符串 ➜ `struct in_addr`      | ✅             | ❌         | 推荐使用 |
| `inet_ntoa()`  | `struct in_addr` ➜ IP字符串      | ❌             | ❌         | 非线程安全 |
| `inet_pton()`  | IP字符串 ➜ `struct in_addr`/IPv6 | ✅             | ✅         | 最推荐 |
| `inet_ntop()`  | `struct in_addr` ➜ IP字符串      | ✅             | ✅         | 最推荐 |

---

如果你希望我帮你：

- ✅ 实现 IPv6 地址的转换示例
- ✅ 封装为 C++ 类或函数模板
- ✅ 对比不同平台（Linux vs Windows）下的用法差异


网络编程三大步:
int sock = socket( PF_INET, SOCK_STREAM, 0 );
int ret = bind( sock, ( struct sockaddr* )&address, sizeof( address ) );
ret = listen( sock, backlog );
accept()
conneected()
close()

socketaddr()
socketaddr_storage()
socketaddr_up()
socketaddr_in()
socketaddr_in6()

AF
PF Unix协议
v4协议
v6协议

### 第6章 高级IO函数
6.1 pipe函数
6.2 dup函数和dup2函数
6.3 readv函数和writev函数
6.4 sendfile函数
6.5 mmap函数和munmap函数
6.6 splice函数
6.7 tee函数
6.8 fcntl函数

pipe()
实现管道，进程通信

dup()
dup2()
readv()
writev()
sendfile()
进程之间发送数据
零拷贝
内核缓冲区
用户缓冲区

mmap()
申请一段内存
nummap()
释放上述申请的内存

splice()
tee()
fcntl()

参考
linux_api.md

### 第7章 Linux服务器程序规范
7.1 日志
7.1.1 Linux系统日志
7.1.2 syslog函数
7.2 用户信息
7.2.1 UID、EUID、GID和EGID
7.2.2 切换用户
7.3 进程间关系
7.3.1 进程组
7.3.2 会话
7.3.3 用ps命令查看进程关系
7.4 系统资源限制
7.5 改变工作目录和根目录
7.6 服务器程序后台化

### 第8章 高性能服务器程序框架
8.1 服务器模型
8.1.1 CS模型
8.1.2 P2P模型
8.2 服务器编程框架
8.3 IO模型
8.4 两种高效的事件处理模式
8.4.1 Reactor模式
8.4.2 Proactor模式
8.4.3 模拟Proactor模式
8.5 两种高效的并发模式
8.5.1 半同步半异步模式
8.5.2 领导者追随者模式
8.6 有限状态机
8.7 提高服务器性能的其他建议
8.7.1 池
8.7.2 数据复制
8.7.3 上下文切换和锁

### 第9章 IO复用
9.1 select系统调用
9.1.1 select API
9.1.2 文件描述符就绪条件
9.1.3 处理带外数据
9.2 poll系统调用
9.3 epoll系列系统调用
9.3.1 内核事件表
9.3.2 epoll_wait函数
9.3.3 LT和ET模式
9.3.4 EPOLLONESHOT事件
9.4 三组IO复用函数的比较
9.5 IO复用的高级应用一：非阻塞connect
9.6 IO复用的高级应用二：聊天室程序
9.6.1 客户端
9.6.2 服务器
9.7 IO复用的高级应用三：同时处理TCP和UDP服务
9.8 超级服务xinetd
9.8.1 xinetd配置文件
9.8.2 xinetd工作流程

### 第10章 信号
10.1 Linux信号概述
10.1.1 发送信号
10.1.2 信号处理方式
10.1.3 Linux信号
10.1.4 中断系统调用
10.2 信号函数
10.2.1 signal系统调用
10.2.2 sigaction系统调用
10.3 信号集
10.3.1 信号集函数
10.3.2 进程信号掩码
10.3.3 被挂起的信号
10.4 统一事件源
10.5 网络编程相关信号
10.5.1 SIGHUP
10.5.2 SIGPIPE
10.5.3 SIGURG

### 第11章 定时器
11.1 socket选项SO_RCVTIMEO和SO_SNDTIMEO
11.2 SIGALRM信号
11.2.1 基于升序链表的定时器
11.2.2 处理非活动连接
11.3 IO复用系统调用的超时参数
11.4 高性能定时器
11.4.1 时间轮
11.4.2 时间堆

### 第12章 高性能IO框架库Libevent
12.1 IO框架库概述
12.2 Libevent源码分析
12.2.1 一个实例
12.2.2 源代码组织结构
12.2.3 event结构体
12.2.4 往注册事件队列中添加事件处理器
12.2.5 往事件多路分发器中注册事件
12.2.6 eventop结构体
12.2.7 event_base结构体
12.2.8 事件循环

### 第13章 多进程编程
13.1 fork系统调用
13.2 exec系列系统调用
13.3 处理僵尸进程
13.4 管道
13.5 信号量
13.5.1 信号量原语
13.5.2 semget系统调用
13.5.3 semop系统调用
13.5.4 semctl系统调用
13.5.5 特殊键值IPC_PRIVATE
13.6 共享内存
13.6.1 shmget系统调用
13.6.2 shmat和shmdt系统调用
13.6.3 shmctl系统调用
13.6.4 共享内存的POSIX方法
13.6.5 共享内存实例
13.7 消息队列
13.7.1 msgget系统调用
13.7.2 msgsnd系统调用
13.7.3 msgrcv系统调用
13.7.4 msgctl系统调用
13.8 IPC命令
13.9 在进程间传递文件描述符

### 第14章 多线程编程
14.1 Linux线程概述
14.1.1 线程模型
14.1.2 Linux线程库
14.2 创建线程和结束线程
14.3 线程属性
14.4 POSIX信号量
14.5 互斥锁
14.5.1 互斥锁基础API
14.5.2 互斥锁属性
14.5.3 死锁举例
14.6 条件变量
14.7 线程同步机制包装类
14.8 多线程环境
14.8.1 可重入函数
14.8.2 线程和进程
14.8.3 线程和信号

### 第15章 进程池和线程池
15.1 进程池和线程池概述
15.2 处理多客户
15.3 半同步半异步进程池实现
15.4 用进程池实现的简单CGI服务器
15.5 半同步半反应堆线程池实现
15.6 用线程池实现的简单Web服务器
15.6.1 http_conn类
15.6.2 main函数

## 第三篇 高性能服务器优化与监测
### 第16章 服务器调制、调试和测试
16.1 最大文件描述符数
16.2 调整内核参数
16.2.1 procsysfs目录下的部分文件
16.2.2 procsysnet目录下的部分文件
16.3 gdb调试
16.3.1 用gdb调试多进程程序
16.3.2 用gdb调试多线程程序
16.4 压力测试

### 第17章 系统监测工具
17.1 tcpdump
17.2 lsof
17.3 nc
17.4 strace
17.5 netstat
17.6 vmstat
17.7 ifstat
17.8 mpstat


非阻塞write没有一次写对  陈硕 知乎上有说法 两次
