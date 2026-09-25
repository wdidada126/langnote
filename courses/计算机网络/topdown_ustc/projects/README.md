# USTC 计算机网络（自顶向下）配套项目计划（projects/README.md）

> 课程无硬核编程作业（原版 Kurose lab 以抓包为主）。本表用「小项目」补齐动手能力；本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| Ch1 概述 / Ch2 HTTP | Python | 极简 HTTP/1.0 服务器 + 浏览器实测 | `python http_server.py 8080` |
| Ch2 DNS | Python | 手写递归 DNS 解析器（socket + 报文打包） | `python dns_resolver.py <domain>` |
| Ch2 Socket/UDP | C | UDP 聊天/文件传输（丢包注入观察） | `gcc -o udp_chat udp_chat.c && ./udp_chat` |
| Ch3 TCP 可靠传输 | Python | 停等/GBN 协议模拟器（信道丢包模型） | `python rdt_sim.py` |
| Ch3 拥塞控制 | Python | AIMD/慢启动窗口演化仿真 + matplotlib | `python tcp_cong_sim.py` |
| Ch4 子网/CIDR | Python | 子网计算器 + 最长前缀匹配路由查找 | `python subnet_calc.py` |
| Ch4 路由算法 | Python/Go | Dijkstra(LS) 与 Bellman-Ford(DV) 收敛对比 | `python routing_sim.py` |
| Ch5 以太网/交换 | Python | 学习型交换机 + STP 破环模拟 | `python switch_sim.py` |
| Ch6 无线 | Python | CSMA/CD vs CSMA/CA 吞吐仿真 | `python csma_sim.py` |
| 全程 抓包 lab | Wireshark | 各层协议抓包分析（对应官方 labs） | Wireshark GUI / `tshark` |

环境约定：Python ≥3.10 + requirements.txt；C 用 gcc；Go 用 go modules；本轮只写不编译，集中编译由用户稍后统一执行。
