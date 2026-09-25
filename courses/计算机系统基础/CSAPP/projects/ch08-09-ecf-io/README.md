# ch08-09-ecf-io —— 异常控制流与系统级 I/O

**关联讲次**：L14（进程/fork/wait）、L15（信号/Shell）、L18（Unix I/O）。
对应官方 **Shell Lab** 与 CSAPP Ch.10 的健壮 I/O 主题。

## 内容

| 文件 | 说明 |
| --- | --- |
| `src/mini_shell.c` | Shell 骨架：fork/execvp/waitpid、`&` 后台、SIGCHLD 收割、Ctrl-C/Ctrl-Z 进程组语义；Windows 退化为 `_system` 顺序执行版 |
| `src/robust_copy.c` | `cp` 迷你版：Rio 风格短读/短写/EINTR 处理，POSIX 与 Windows CRT 双通道 |

## 构建运行

```sh
./build.sh          # 生成 bin/mini_shell bin/cp_like
./bin/cp_like src/mini_shell.c /tmp/t.c && diff src/mini_shell.c /tmp/t.c
```
```bat
build.bat           :: vcvarsall x64 环境；生成 bin\mini_shell.exe bin\cp_like.exe
```

## 骨架故意"未完成"的地方（留给读者=Shell Lab 的坑）

1. **作业表/fg/bg 命令**：需要记录 pid↔命令行，并用 `kill(0-pid, SIG...)`
   向前台进程组发信号（注意负 pid = 进程组，L15）。
2. **SIGTSTP/SIGINT 竞态**：`Ctrl-C` 恰好发生在 fork 之前 → 骨架在父进程
   安装 handler、子进程 `SIG_DFL`，这是最小正确姿势；完整解法用
   `sigsuspend` 等待标志位（见 L15 笔记）。
3. **SIGCHLD 合并**：handler 里 `while(waitpid(-1,NULL,WNOHANG)>0)`，
   绝不能用 `wait()`（L14 僵尸 → L15 竞态的连环坑）。
4. `SA_RESTART` 的选择：加了它 fgets 不被 EINTR 打断——学习期建议注释掉
   观察 `read: interrupted system call`。

## Ch.9/10 延伸：epoll 与 IOCP 双平台设计说明

`robust_copy` 是**阻塞 I/O**。要写并发服务器（Proxy Lab），两大平台模型：

```
Linux (select → poll → epoll)          Windows (IOCP)
- epoll_create1 注册兴趣事件表          - CreateIoCompletionPort 把句柄挂到端口
- epoll_ctl 增删改 (fd, EPOLLIN...)     - 读写用 WSARecv/ReadFileEx 且 overlapped=异步提交
- epoll_wait 一次返回"全部就绪 fd"       - GetQueuedCompletionStatus 收割"已完成包"
- 水平触发 LT / 边沿触发 ET(需一次读干净)  - 真·完成端口：完成即通知，无需再关心就绪
- O_NONBLOCK + 重试 EAGAIN 是标配         - fd≈HANDLE：ReadFile/WriteFile/TransmitFile
共同点：单线程事件循环即可服务上万连接；
差异点：epoll"就绪才干活"(reactor)，IOCP"干完活才通知"(proactor)。
libuv 在 Windows 用 IOCP、在 POSIX 用 epoll，是两套语义的统一层（见 L20）。
```

骨架建议：在 mini_shell 的事件版（tsh）上先加 `select` 管理 stdin+SIGCHLD
self-pipe，再换 `epoll`；Windows 侧同理用 `WSAEventSelect` 过渡到 IOCP。

## 观察命令

```sh
strace -f -e trace=process ./bin/mini_shell     # 看 fork/exec/wait 序列
ls -l /proc/self/fd                             # 看 fd 三层表（L18）
echo $$ ; kill %1                               # 作业控制手感（L15）
```
