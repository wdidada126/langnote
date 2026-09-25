# CS110 配套项目计划（projects/README.md）

> 本轮只列计划不写代码；语言与编译方式面向 Linux/macOS POSIX 环境（Windows 下用 WSL）。

| 章节范围 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L3 链接与库 | C | mylinker：手工解析 .o 符号表并静态打包成 mini .a；dlopen 加载 .so 插件计算器 | `gcc -fPIC -shared` + `ar rcs` + `gcc -ldl`，配 Makefile |
| L4–L5 内存 | C | minimalloc：实现 malloc/free/realloc 并通过并发压力与碎片测试；mmap 后端版对比 glibc malloc 吞吐 | `gcc -O2 -pthread`，Makefile `make test` |
| L6–L7 文件与 I/O | C | cat/tail -f 复刻 + 缓冲策略基准（write vs printf vs 手工缓冲） | `gcc -O2`，`strace -c` 采集系统调用数 |
| L8–L10 进程与 IPC | C | mini-shell：管道、重定向、作业控制（SIGCHLD/前台后台） | `gcc -Wall -Wextra`，自带 bats/脚本用例 |
| L11–L13 网络与 Web | C（POSIX sockets） | httpd：thread-per-request → 线程池两版，wrk 压测对比 | `gcc -pthread`，Linux 链接 `-lpthread` |
| L14–L17 并发 | C/C++11 | 线程安全哈希表 + 生产者消费者有界队列；Helgrind/TSan 清干净 | `clang -fsanitize=thread` 与 `g++ -std=c++17 -pthread` |
| L18 事件驱动 | C | reactor-server：单线程 epoll/select 版聊天室，与 L13 线程池版对拍 | `gcc -O2`，Linux 专用 epoll 分支宏控 |
| L19 分布式 | C++ 或 Go | 两机 MapReduce（master/worker + RPC），词频与倒排两个 workload | C++: `g++ -std=c++17 -pthread`；Go: `go build ./...` |
