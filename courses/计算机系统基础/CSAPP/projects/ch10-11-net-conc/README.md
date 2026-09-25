# ch10-11-net-conc —— 网络编程与并发编程（双平台骨架）

**关联讲次**：L19（客户端-服务器/Sockets，Ch.11）、L20（并发编程，Ch.12）。
对应官方 **Proxy Lab** 的三大并发模型主题。

## 内容

| 文件 | 平台 | 说明 |
| --- | --- | --- |
| `src/echo_server.c` | POSIX(pthread) / Windows(Winsock2+CreateThread) | 每连接一线程的回显服务器：getaddrinfo/AI_PASSIVE、bind/listen/accept、SO_REUSEADDR、SIGPIPE→EPIPE、短写重试、fd 泄漏点 |
| `src/echo_client.c` | 同上双平台 | open_clientfd 等价实现；发一行、读回显 |
| `src/producer_consumer.c` | 同上双平台 | 有界缓冲区：mutex+cond（POSIX）/SRWLOCK+CONDITION_VARIABLE（Win），`while` 防虚假唤醒、生产/消费总量校验 |

## 构建运行

```sh
./build.sh                      # gcc -pthread
bin/echo_server 8000 &          # 另开终端
bin/echo_client localhost 8000 hello csapp
bin/producer_consumer
# 压测多客户端（验证并发服务）：
for i in 1 2 3 4 5; do bin/echo_client localhost 8000 "client$i" & done
```
```bat
build.bat        :: vcvarsall x64；自动链接 ws2_32.lib
bin\echo_server 8000
bin\echo_client localhost 8000 hello
```

## 骨架到 Proxy Lab 的路线图

1. **HTTP 解析**：把"echo 原样字节"换成 `rio_readlineb` 解析请求行/头，
   识别 `GET http://host/path` 转发上游或读本地文件（CSAPP 11.5 tiny server）。
2. **三种并发模型**（同一功能，不同写法对照性能）：
   - 进程版：accept 后 `fork`（L14）——隔离最好，最重；
   - 线程版：本仓库 echo_server（L20）——共享状态要小心，但代码"天然并行"；
   - 事件版（单线程）：
     - Linux: `epoll_create1/epoll_ctl/epoll_wait` + `O_NONBLOCK` + 每 fd 状态机；
     - Windows: IOCP——`CreateIoCompletionPort` 挂句柄，`WSARecv` overlapped
       提交，`GetQueuedCompletionStatus` 收割"完成包"（proactor vs epoll 的 reactor）。
     - 或直接上 libevent/libuv 统一两套语义（L20 笔记）。
3. **信号量版生产者-消费者**：把 cond 换成 `sem_t empty/full + mutex`
   （Windows `CreateSemaphore`），体会"计数信号量 vs 条件变量"两种表达。
4. **线程安全自查**（CSAPP 12.7 分类）：`printf` 在多线程下是否安全？
   `ctime`/`gethostbyname` 这类"返回静态缓冲区"的函数为什么禁止在服务器用？

## 观察点

- 服务器不处理 SIGPIPE 时：客户端先关 → 服务器 write 收到信号猝死（POSIX）。
- Windows 上 recv/send 错误码用 `WSAGetLastError()`（errno 是另一套！）。
- `SO_REUSEADDR`：服务器重启立刻 bind 失败 = TIME_WAIT 端口占用（L12 的
  "内核网络栈状态"在 API 上的投影）。
- 把 `cond_wait` 的 `while` 改成 `if`：多数时候仍"对"，偶发 MISMATCH——
  这就是竞态 bug 的难缠之处（L15/L20 主题）。
