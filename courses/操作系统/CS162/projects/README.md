# CS162 配套项目计划（projects/README.md）

> 主干为官方 Pintos 3 Project + 6 Homework（C/Rust 双版本，Docker 跨平台环境）。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L5 基础与进程 | C (Pintos) | Project1 User Programs：参数解析、进程系统调用（含 25 年新增 fork）、文件 syscall | Docker 实验镜像内 `make -C pintos/threads`，`check-pintos` 本地测试 |
| L3–L7 同步与调度 | C (Pintos) | Project2 Threads：timer_sleep 非忙等、严格优先级调度器（优先级继承）、迷你 pthread 库 | 同上，`make check` 逐 project 评测 |
| L8–L10 内存 | C (Pintos) | Project3 Virtual Memory：用户程序换页与 mmap | 同上 |
| L11–L15 文件系统 | C (Pintos) | Project4 File Systems：buffer cache、可扩容文件、子目录 | 同上 |
| L1 热身 | C | Homework-List：Pintos 内置双向链表封装与单测 | `gcc -std=gnu99 -o list-test list.c test.c` |
| L5/L13 Shell | C 或 Rust | Homework-Shell：支持管道/重定向/信号的 Unix shell | `make`（自带 Makefile）；Rust 版 `cargo build --release` |
| L16 HTTP | C 或 Rust | Homework-HTTP：GET 静态服务器（与 CS110/CS144 互认） | `gcc -pthread`；Rust 版 `cargo run` |
| L8 内存 | C | Homework-Memory：sbrk/malloc/free 与并发压力测试 | `gcc -O2 -pthread -no-pie`（对齐课程测试脚本） |
| L17–L18 分布式 | Go（可选 C/Rust） | Homework-MapReduce：可容忍失败的 MapReduce（含 RPC 子任务；可与 6.824 lab 互换） | Go: `go build ./... && go test ./...` |
