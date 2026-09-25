# CS168 配套项目计划（projects/README.md）

> 本轮只列计划不写代码；语言遵循课程官方 Python，另加自选练习。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L01–L03（寻址/链路/IP） | Python | Traceroute 探测工具：TTL 超时解析路径、统计逐跳 RTT（官方 Project 1） | `python traceroute.py <host>` + pytest |
| L04–L06（路由） | Python | 域内路由模拟器：实现 DV 与 LS 两种算法并对拍收敛（官方 Project 2） | `python router_sim.py --topo topo.json` |
| L07–L09（TCP） | Python | 迷你可靠传输：滑动窗口+超时重传+AIMD 拥塞窗口仿真（官方 Project 3） | `python tcp_mini.py` + matplotlib 出图 |
| L09（拥塞控制） | Python | CUBIC vs BBR 行为对比 notebook：不同 RTT/丢包下吞吐-时延曲线 | `jupyter lab` / `python plot_cubic_bbr.py` |
| L10–L11（DNS/HTTP） | Python | 手写 DNS 递归解析器 + HTTP/1.1 并发抓取器 | `python dns_probe.py`、`python http_fetch.py` |
| L12（TLS/端到端） | Go | 简易 TLS echo server：观察握手与证书链 | `go build && ./tlsecho` |
| L13（数据中心） | Python | Clos 拓扑 + ECMP 路径模拟：哈希选择链路 | `python ecmp_sim.py` |
| L14（无线） | C | CSMA/CA 冲突模拟器（Aloha 对比） | `gcc -O2 -o csma csma.c && ./csma` |

环境约定：Python ≥3.10，虚拟环境 + `requirements.txt`；每个项目独立目录、独立 build/run 脚本；本轮只写不编译，集中编译由用户稍后统一执行。
