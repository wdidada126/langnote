# projects —— 《自顶向下方法》配套 Python 项目（标准库，无第三方依赖）

> 本轮约定：代码**只写不编译**；每个 run.sh/run.bat 内置 `python -m py_compile` 语法自检，首次运行请先执行它。
> 语言：Python 3.8+（`socket / threading / zlib / struct / heapq / json / argparse` 全部标准库）。

| 项目 | 对应章节/讲次 | 内容 | 入口 |
| --- | --- | --- | --- |
| ch2_http_server | §2.2/§2.4，第 5/7 讲 | 多线程 HTTP/1.1 GET 服务器：请求解析、简易路由（/hello /time /count）、/static + 304 协商缓存 | `http_server.py` |
| ch2_dns_query | §2.3，第 6 讲 | 手工构造/解析 DNS 报文（A/NS/CNAME/AAAA），0xC0 压缩指针处理；与 `getaddrinfo` 对比 | `dns_query.py` |
| ch3_arq | §3.4，第 10 讲 | 停等 / GBN / SR 在模拟损伤信道（丢失+比特错+ACK 丢失）上的轮次模拟与利用率对比 | `arq_sim.py` |
| ch3_chat | §2.4/§3.2/§3.3，第 7/9 讲 | 群聊双版本：TCP（每连接一线程、行框架）vs UDP（二元组分用、应用层 seq+ACK 停等重传） | `chat_tcp.py` / `chat_udp.py` |
| ch3_congestion | §3.6，第 12 讲 | AIMD / Reno（慢启动+快恢复+超时）窗口演化模拟，纯文本位图绘图；双流公平性 | `congestion_sim.py` |
| ch4_router_sim | §4.3/§5.1，第 14/16/17 讲 | 最长前缀匹配 FIB（二进制 trie）+ Dijkstra 链路状态 + 距离向量 Bellman-Ford（计数到无穷与毒性逆转对比） | `router_sim.py` |
| ch5_ethernet_sim | §6.2/§6.4，第 20/21 讲 | 以太网帧构造与 FCS、小多项式 CRC 长除法手算、交换机自学习/泛洪/老化 | `ethernet_sim.py` |

## 通用运行方式

```bash
# Linux / macOS
cd ch3_arq && ./run.sh            # 先 py_compile 自检再运行
python3 arq_sim.py                # 直接跑亦可
```

```bat
:: Windows
cd ch3_arq && run.bat
py arq_sim.py
```

多进程/多终端类项目（http_server、chat）见各自 README 的"运行"一节——服务端一个终端、客户端 N 个终端。

## 与官方 Lab 的关系

- 官方 Wireshark lab 是"观察真实协议"；本目录项目是"重造协议骨架"——两者互补：
  先跑模拟理解状态机，再用 Wireshark 对照真实内核实现（Linux TCP / BIND / Nginx）。
- 想做硬核实现级训练：用本项目 `ch3_arq`/`ch3_congestion` 的思路进入 **CS144**（C++ 完整 TCP/IP 栈），
  用 `ch4_router_sim` 进入 **CS168/DPDK/VPP**；用 `ch2_http_server` 进入 **CSAPP**（C socket + tiny）。
