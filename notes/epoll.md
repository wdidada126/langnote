# epoll

select，poll，epoll本质上都是同步I/O，因为他们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的，而异步I/O则无需自己负责进行读写，异步I/O的实现会负责把数据从内核拷贝到用户空间。

我们先看一下epoll和select和poll的调用接口上的不同，select和poll都只提供了一个函数——select或者poll函数。而epoll提供了三个函数，epoll_create,epoll_ctl和epoll_wait
- epoll_create是创建一个epoll句柄；
- epoll_ctl是注册要监听的事件类型；
- epoll_wait则是等待事件的产生。
- epoll_data
- epoll_event

epoll_create1
epoll_data_t
epoll_pwait
epoll_pwait2

linux_api.md

你问得非常精准！这是 Linux 高性能 I/O 多路复用的核心机制 —— epoll 的完整图谱。我们来系统性地、逐个详解 `epoll` 的所有关键函数和结构体，从入门到进阶，彻底搞懂它。

---

## 一、epoll 三大核心函数（基础三件套）

### 1. `epoll_create` / `epoll_create1`：创建 epoll 实例

#### `int epoll_create(int size);`
- 作用：创建一个 epoll 实例，返回一个文件描述符（`epoll_fd`）。
- 参数 `size`：仅作提示（Linux 2.6.8 后已忽略），表示你预计监听多少个 fd。
- 返回值：成功返回 epoll 句柄（非负整数），失败返回 -1。

> ⚠️ 已被弃用，推荐使用 `epoll_create1`。

---

#### ✅ `int epoll_create1(int flags);`（推荐）

- `flags` 可选值：
  - `0`：默认行为，等价于 `epoll_create()`
  - `EPOLL_CLOEXEC`：设置 `FD_CLOEXEC` 标志，进程 `exec` 时自动关闭该 fd（防泄漏，强烈推荐！）

```c
int epoll_fd = epoll_create1(EPOLL_CLOEXEC);
if (epoll_fd == -1) {
    perror("epoll_create1");
    exit(1);
}
```

> ✅ 最佳实践：永远用 `epoll_create1(EPOLL_CLOEXEC)`

---

### 2. `int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);`

#### 作用：
向 `epoll_fd` 对应的实例中添加、修改或删除对某个 `fd` 的监听。

#### 参数详解：

| 参数 | 说明 |
|------|------|
| `epfd` | `epoll_create1` 返回的句柄 |
| `op` | 操作类型：`EPOLL_CTL_ADD`, `EPOLL_CTL_MOD`, `EPOLL_CTL_DEL` |
| `fd` | 要监听的文件描述符（如 socket） |
| `event` | 指向 `struct epoll_event` 的指针，描述监听事件和附加数据 |

#### 示例：监听 socket 可读事件

```c
struct epoll_event ev;
ev.events = EPOLLIN;           // 监听“可读”
ev.data.fd = sockfd;           // 绑定 sockfd

int ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, sockfd, &ev);
if (ret == -1) {
    perror("epoll_ctl");
    exit(1);
}
```

---

### 3. `int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);`

#### 作用：
阻塞等待，直到有事件发生，将就绪的事件填充到 `events` 数组中。

#### 参数：

| 参数 | 说明 |
|------|------|
| `epfd` | epoll 句柄 |
| `events` | 用户提供的数组，用于存放就绪事件 |
| `maxevents` | 数组大小（最大返回事件数） |
| `timeout` | 超时时间（毫秒）：<br> `-1`：永久阻塞<br> `0`：立即返回（轮询）<br> `>0`：最多等待 timeout 毫秒 |

#### 返回值：
- `>0`：就绪事件数量
- `0`：超时
- `-1`：出错（如被信号中断）

#### 示例：

```c
struct epoll_event events[1024];
int nfds = epoll_wait(epoll_fd, events, 1024, -1);
for (int i = 0; i < nfds; ++i) {
    if (events[i].events & EPOLLIN) {
        read(events[i].data.fd, buf, sizeof(buf));
    }
}
```

---

## 二、核心结构体详解

### `struct epoll_event` 定义（`<sys/epoll.h>`）

```c
typedef union epoll_data {
    void    *ptr;
    int      fd;
    uint32_t u32;
    uint64_t u64;
} epoll_data_t;

struct epoll_event {
    uint32_t     events;    // Epoll events (EPOLLIN, EPOLLOUT, etc.)
    epoll_data_t data;      // User data variable
};
```

---

### `epoll_data_t` 详解：事件的“上下文携带者”

`data` 字段是一个 union，你可以用它携带任何你想在事件触发时获取的信息。

#### 常见用法：

| 用法 | 示例 | 说明 |
|------|------|------|
| `data.fd` | `ev.data.fd = sockfd;` | 最简单，直接存 fd |
| `data.ptr` | `ev.data.ptr = &conn;` | 存指向连接上下文的指针（最灵活） |
| `data.u32/u64` | `ev.data.u32 = conn_id;` | 存 ID、状态码等 |

#### 高级用法：携带连接上下文

```c
struct Connection {
    int fd;
    char buffer[1024];
    void (*on_read)(struct Connection*);
};

struct epoll_event ev;
ev.events = EPOLLIN;
ev.data.ptr = conn_ctx;  // 指向 Connection 结构体

// 在 epoll_wait 触发后：
struct Connection* conn = (struct Connection*)events[i].data.ptr;
conn->on_read(conn);  // 直接调用处理函数
```

> ✅ 这是高性能服务器的常见设计模式：事件触发 → 直接拿到上下文 → 无需查表。

---

### `events` 字段详解：监听哪些事件？

| 事件 | 说明 |
|------|------|
| `EPOLLIN` | 对应 `POLLIN`，数据可读（socket 有数据到达） |
| `EPOLLOUT` | 对应 `POLLOUT`，可写（socket 发送缓冲区有空间） |
| `EPOLLERR` | 错误发生（总是被监听，无需显式设置） |
| `EPOLLHUP` | 对端关闭连接（挂起） |
| `EPOLLRDHUP` | 对端关闭写端（TCP 连接关闭写方向） |
| `EPOLLET` | 边缘触发（Edge Triggered） 模式（默认是水平触发 LT） |
| `EPOLLONESHOT` | 事件只触发一次，需重新 `epoll_ctl` 重新启用 |

#### ⚡ ET 模式 vs LT 模式

| 模式 | 行为 | 性能 | 使用难度 |
|------|------|------|---------|
| LT（水平触发） | 只要条件满足（如可读），就一直通知 | 稍低 | 简单 |
| ET（边缘触发） | 只在状态变化时通知一次（如从不可读→可读） | 高 | 复杂（必须一次性读完） |

> ET 模式必须配合非阻塞I/O，否则可能阻塞在 `read()`。

---

## ⏱ 三、进阶函数：带信号处理的等待

### `int epoll_pwait(int epfd, struct epoll_event *events, int maxevents, int timeout, const sigset_t *sigmask);`

#### 作用：
原子地：临时用 `sigmask` 替换当前线程的信号掩码 → 调用 `epoll_wait` → 恢复原信号掩码。

#### 为什么需要它？

想象你用 `sigprocmask` 手动屏蔽信号，再调 `epoll_wait`：

```c
sigset_t set, oldset;
sigemptyset(&set);
sigaddset(&set, SIGINT);
pthread_sigmask(SIG_BLOCK, &set, &oldset);

n = epoll_wait(epfd, events, max, timeout);  //  原子性问题！

pthread_sigmask(SIG_SETMASK, &oldset, NULL);
```

如果 `epoll_wait` 前后有信号到达，可能丢失。而 `epoll_pwait` 是原子操作，确保安全。

#### 示例：

```c
sigset_t sigmask;
sigemptyset(&sigmask);
sigaddset(&sigmask, SIGINT);

int n = epoll_pwait(epoll_fd, events, 1024, -1, &sigmask);
// 等价于：屏蔽 SIGINT → epoll_wait → 恢复
```

---

### `int epoll_pwait2(int epfd, struct epoll_event *events, int maxevents, int timeout, const struct __kernel_timespec *timeout_ts, const sigset_t *sigmask);`

#### 作用：
`epoll_pwait` 的纳秒级精度版本，支持更精确的超时控制。

- `timeout` 参数是 `struct __kernel_timespec*`，支持秒 + 纳秒。
- 其他行为与 `epoll_pwait` 完全相同。

#### 适用场景：
- 高精度定时任务
- 实时系统

```c
struct __kernel_timespec ts = {
    .tv_sec = 1,
    .tv_nsec = 500000000  // 1.5 秒
};

epoll_pwait2(epfd, events, max, -1, &ts, &sigmask);
```

>  注意：`__kernel_timespec` 是内核结构体，用户态通常用 `struct timespec`。


##  四、总结：epoll 家族全景图

| 函数/结构 | 作用 | 是否推荐 |
|----------|------|---------|
| `epoll_create(size)` | 创建 epoll 实例 | ❌ 已弃用 |
| `epoll_create1(flags)` | 创建 epoll 实例（支持 `CLOEXEC`） |  强烈推荐 |
| `epoll_ctl()` | 增删改监听事件 |  必用 |
| `epoll_wait()` | 等待事件（基本版） |  常用 |
| `epoll_pwait()` | 等待事件 + 安全信号处理 |  多线程/信号安全场景 |
| `epoll_pwait2()` | `epoll_pwait` + 纳秒精度 |  高精度需求 |
| `epoll_event.data.fd` | 携带 fd |  简单场景 |
| `epoll_event.data.ptr` | 携带上下文指针 |  高性能服务器推荐 |
| `EPOLLET` | 边缘触发模式 |  高并发推荐（配非阻塞 I/O） |


##  五、最佳实践建议

1. 永远使用 `epoll_create1(EPOLL_CLOEXEC)`
2. ET 模式 + 非阻塞 I/O 是高性能标配
3. 用 `data.ptr` 携带连接上下文，避免查表
4. 多线程中用 `epoll_pwait` 避免信号竞争
5. 注意 `EPOLLONESHOT` 和 `EPOLLET` 的组合使用



如果你想看：
- 一个基于 `epoll ET + nonblock` 的迷你 HTTP 服务器
- `epoll` 与 `select`/`poll` 的性能对比
- `epoll` 内核实现原理（红黑树 + 就绪链表）

我可以继续深入，带你从应用到底层彻底打通！

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

##  一、什么是 `epoll`？

`epoll` 是 Linux 提供的一种 I/O 多路复用机制，适用于高并发网络服务器开发（如 Nginx、Redis 等）。它通过监听多个 socket 或文件描述符的状态变化来触发事件回调。

##  二、`enum EPOLL_EVENTS` 各枚举值详解 15个 14个使用，1个废弃
in out 2
rd wr 4 band norm  RD NROM RD BAND,WR NROM WR BAND
pri MSG(废弃) ERROR 3
WAREUP 1
ONSHOT 1
HUP RDHUP 2
et
EXCLUSIVE


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

##  三、常见组合使用方式

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

##  四、如何使用这些事件？

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

##  五、边缘触发 vs 水平触发（ET vs LT）

| 特性 | 水平触发（LT，默认） | 边缘触发（ET，需设置 `EPOLLET`） |
|------|------------------|----------------------------|
| 触发时机 | 只要处于就绪状态就会一直通知 | 只在状态变化时通知一次 |
| 性能 | 适合低并发场景 | 更适合高并发，效率更高 |
| 注意事项 | 不需要立即处理完所有数据 | 必须一次性读完或写完数据（否则可能无法再次触发） |

##  六、总结表格

| 枚举值 | 是否常用 | 用途说明 |
|--------|----------|----------|
| `EPOLLIN` |  常用 | 可读事件 |
| `EPOLLOUT` |  常用 | 可写事件 |
| `EPOLLET` |  常用 | 边缘触发模式 |
| `EPOLLONESHOT` |  多线程常用 | 保证事件只触发一次 |
| `EPOLLRDHUP` |  推荐搭配 | 检测对端关闭连接 |
| `EPOLLERR / EPOLLHUP` |  必须处理 | 错误或连接中断 |
| `EPOLLEXCLUSIVE` | ⚠️ 高级用法 | 防止“惊群”现象 |
| `EPOLLWAKEUP` | ❌ 很少用 | 嵌入式系统防止休眠 |

##  七、建议阅读和实践

你可以尝试以下实验：

1. 写一个基于 `epoll` 的 TCP 服务器，支持多个客户端连接。
2. 使用 `EPOLLET` 实现非阻塞读写。
3. 添加 `EPOLLONESHOT` 支持多线程安全处理。
4. 添加信号处理模块，实现优雅退出。
5. 扩展成 HTTP 服务器，支持 GET/POST 请求解析。


是否需要我封装成模块化结构？比如：

- `epoll_server.c/h`：主逻辑
- `connection_pool.c/h`：连接池管理
- `http_parser.c/h`：HTTP 解析器
