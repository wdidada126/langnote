# CS144 配套项目计划（projects/README.md）

> 本轮只列计划不写代码。官方作业即 8 个 checkpoint（CP0–CP7）+ Labs，语言 C++17；下表的「小项目」为课程 checkpoint 主线 + 自选加深练习。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L01–L02 环境热身（CP0） | C++ | webget：用内核 socket 写基础网络爬虫 | `make webget`（官方 Makefile）|
| L10 字节流抽象（CP0.5） | C++ | StreamReassembler：内存受限的可靠字节流 | `make check_lab0` + `make lab0` |
| L11–L12 TCP 接收端（CP1） | C++ | TCPRcvr：重组/去重/输出界 | `make check_lab1` |
| L12 TCP 发送端（CP2） | C++ | TCPSndr：重传定时器 + 指数退避 + 窗口取 min | `make check_lab2` |
| L12–L13 全双工 TCP（CP3） | C++ | 与工业实现互操作的完整 TCP peer | `make check_tcp` |
| L15 端到端集成（CP4） | C++ | TCPMinnowSocket 替换内核 socket 跑 webget + 数据分析 | `make minnowshell` + Python matplotlib |
| L09 网络接口/ARP（CP5） | C++ | NetworkInterface + ARP 抹平 IP/Ethernet 沟 | `make check_lab5` |
| L06–L07 IP 路由器（CP6） | C++ | IPRouter：最长前缀匹配转发 | `make check_lab6` |
| L16 端到端互联（CP7） | C++ | 经中继服务器两端自建栈实时通信 | `make run_router` + endtoend |
| L13–L14 拥塞控制（自选） | C++ | 在 CP2 上实现 CUBIC 并对比 BBR 行为 | 独立测试 `ctest -R cubic` |
| L17 NAT/中间盒（自选） | Python | conntrack 行为观察小脚本 | `python nat_watch.py` |

环境约定：C++17，CMake/Make 双支持，依赖 libpcap/uv；官方仓库每年清空，建议先 fork。本轮只写不编译，集中编译由用户稍后统一执行。
