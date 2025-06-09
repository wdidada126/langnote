# epoll

select，poll，epoll本质上都是同步I/O，因为他们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的，而异步I/O则无需自己负责进行读写，异步I/O的实现会负责把数据从内核拷贝到用户空间。

我们先看一下epoll和select和poll的调用接口上的不同，select和poll都只提供了一个函数——select或者poll函数。而epoll提供了三个函数，epoll_create,epoll_ctl和epoll_wait，epoll_create是创建一个epoll句柄；epoll_ctl是注册要监听的事件类型；epoll_wait则是等待事件的产生。

[select、poll、epoll之间的区别总结](https://www.cnblogs.com/Anker/p/3265058.html)

[epoll使用详解（精髓）](https://www.cnblogs.com/fnlingnzb-learner/p/5835573.html)

有例子

https://gitee.com/edidada/epollhttp

<sys/sysctl.h>
Linux 特有的系统头文件，用于访问内核参数（如 /proc/sys/ 下的内容）

sudo apt update
sudo apt install build-essential libssl-dev linux-libc-dev -y
sudo apt install linux-headers-$(uname -r) -y
sudo apt install libc6-dev -y

```c
enum EPOLL_EVENTS
  {
    EPOLLIN = 0x001,
#define EPOLLIN EPOLLIN
    EPOLLPRI = 0x002,
#define EPOLLPRI EPOLLPRI
    EPOLLOUT = 0x004,
#define EPOLLOUT EPOLLOUT
    EPOLLRDNORM = 0x040,
#define EPOLLRDNORM EPOLLRDNORM
    EPOLLRDBAND = 0x080,
#define EPOLLRDBAND EPOLLRDBAND
    EPOLLWRNORM = 0x100,
#define EPOLLWRNORM EPOLLWRNORM
    EPOLLWRBAND = 0x200,
#define EPOLLWRBAND EPOLLWRBAND
    EPOLLMSG = 0x400,
#define EPOLLMSG EPOLLMSG
    EPOLLERR = 0x008,
#define EPOLLERR EPOLLERR
    EPOLLHUP = 0x010,
#define EPOLLHUP EPOLLHUP
    EPOLLRDHUP = 0x2000,
#define EPOLLRDHUP EPOLLRDHUP
    EPOLLEXCLUSIVE = 1u << 28,
#define EPOLLEXCLUSIVE EPOLLEXCLUSIVE
    EPOLLWAKEUP = 1u << 29,
#define EPOLLWAKEUP EPOLLWAKEUP
    EPOLLONESHOT = 1u << 30,
#define EPOLLONESHOT EPOLLONESHOT
    EPOLLET = 1u << 31
#define EPOLLET EPOLLET
  };
```

你列出的这段代码是 Linux 中 `epoll` 事件机制的核心枚举值定义，位于 `<sys/epoll.h>` 头文件中。这些枚举值用于描述 文件描述符在 epoll 监听时的状态或事件类型。

---

## 🧠 一、什么是 `epoll`？

`epoll` 是 Linux 提供的一种 I/O 多路复用机制，适用于高并发网络服务器开发（如 Nginx、Redis 等）。它通过监听多个 socket 或文件描述符的状态变化来触发事件回调。

---

## ✅ 二、`enum EPOLL_EVENTS` 各枚举值详解 15个 14个使用，1个废弃
in out 2
rrww 4
pri and 2

et

| 枚举值 | 十六进制 | 描述 |
|--------|----------|------|
| `EPOLLIN` | `0x001` | 表示对应的文件描述符可以读（包括对端关闭连接） |
| `EPOLLPRI` | `0x002` | 表示有紧急数据可读（带外 OOB 数据） |
| `EPOLLOUT` | `0x004` | 表示对应的文件描述符可以写 |
| `EPOLLRDNORM` | `0x040` | 表示有普通数据可读（与 `EPOLLIN` 类似） |
| `EPOLLRDBAND` | `0x080` | 表示有优先级较高的数据（带宽数据）可读 |
| `EPOLLWRNORM` | `0x100` | 表示普通数据可以写（与 `EPOLLOUT` 类似） |
| `EPOLLWRBAND` | `0x200` | 表示优先级高的数据可以写 |
| `EPOLLMSG` | `0x400` | 忽略，POSIX 已废弃 |
| `EPOLLERR` | `0x008` | 文件描述符发生错误（只在 `epoll_wait` 返回时出现） |
| `EPOLLHUP` | `0x010` | 文件描述符被挂起（断开连接等） |
| `EPOLLRDHUP` | `0x2000` | 对端关闭了连接，或者关闭了写端（常用于检测对方关闭） |
| `EPOLLEXCLUSIVE` | `1u << 28` | 设置独占唤醒模式（防止“惊群”问题） |
| `EPOLLWAKEUP` | `1u << 29` | 防止系统进入休眠状态（用于嵌入式设备） |
| `EPOLLONESHOT` | `1u << 30` | 只监听一次事件，之后必须重新添加 |
| `EPOLLET` | `1u << 31` | 边缘触发（Edge Triggered），只在状态变化时通知 |

---

## 🔍 三、常见组合使用方式

### 1. `EPOLLIN | EPOLLET`
- 表示监听 可读事件，并且采用 边缘触发 模式（只触发一次，直到下一次状态变化）。
- 常用于高性能服务器中，避免重复通知浪费资源。

### 2. `EPOLLOUT | EPOLLET`
- 表示监听 可写事件，且为边缘触发。
- 当 socket 缓冲区有空间写入数据时会触发一次。

### 3. `EPOLLIN | EPOLLRDHUP`
- 推荐组合：监听可读，并检测对端是否关闭连接。
- 适用于 TCP 通信中判断客户端是否断开。

### 4. `EPOLLIN | EPOLLET | EPOLLONESHOT`
- 表示监听可读、边缘触发、仅触发一次。
- 多线程环境下常用，确保一个事件只被一个线程处理。

---

## 🛠️ 四、如何使用这些事件？

```c
struct epoll_event event;
event.events = EPOLLIN | EPOLLET;  // 监听可读 + 边缘触发
event.data.fd = client_fd;

epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &event);
```

然后使用 `epoll_wait()` 等待事件：

```c
struct epoll_event events[MAX_EVENTS];
int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);

for (int i = 0; i < nfds; ++i)
{
    if (events[i].events & EPOLLIN)
    {
        // 处理可读事件
    }
    else if (events[i].events & EPOLLOUT)
    {
        // 处理可写事件
    }
    else if (events[i].events & EPOLLERR || events[i].events & EPOLLHUP)
    {
        // 处理错误或连接关闭
        close(events[i].data.fd);
    }
}
```

---

## 📌 五、边缘触发 vs 水平触发（ET vs LT）

| 特性 | 水平触发（LT，默认） | 边缘触发（ET，需设置 `EPOLLET`） |
|------|------------------|----------------------------|
| 触发时机 | 只要处于就绪状态就会一直通知 | 只在状态变化时通知一次 |
| 性能 | 适合低并发场景 | 更适合高并发，效率更高 |
| 注意事项 | 不需要立即处理完所有数据 | 必须一次性读完或写完数据（否则可能无法再次触发） |

---

## ✅ 六、总结表格

| 枚举值 | 是否常用 | 用途说明 |
|--------|----------|----------|
| `EPOLLIN` | ✅ 常用 | 可读事件 |
| `EPOLLOUT` | ✅ 常用 | 可写事件 |
| `EPOLLET` | ✅ 常用 | 边缘触发模式 |
| `EPOLLONESHOT` | ✅ 多线程常用 | 保证事件只触发一次 |
| `EPOLLRDHUP` | ✅ 推荐搭配 | 检测对端关闭连接 |
| `EPOLLERR / EPOLLHUP` | ✅ 必须处理 | 错误或连接中断 |
| `EPOLLEXCLUSIVE` | ⚠️ 高级用法 | 防止“惊群”现象 |
| `EPOLLWAKEUP` | ❌ 很少用 | 嵌入式系统防止休眠 |

---

## 🧪 七、建议阅读和实践

你可以尝试以下实验：

1. 写一个基于 `epoll` 的 TCP 服务器，支持多个客户端连接。
2. 使用 `EPOLLET` 实现非阻塞读写。
3. 添加 `EPOLLONESHOT` 支持多线程安全处理。
4. 添加信号处理模块，实现优雅退出。
5. 扩展成 HTTP 服务器，支持 GET/POST 请求解析。

---

如果你希望我帮你写一个完整的 epoll 示例程序，包含事件分发、连接管理、数据收发、多线程支持等功能，请告诉我！

是否需要我封装成模块化结构？比如：

- `epoll_server.c/h`：主逻辑
- `connection_pool.c/h`：连接池管理
- `http_parser.c/h`：HTTP 解析器
