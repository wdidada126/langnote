# ch3_chat —— 群聊双版本：TCP 与 UDP 同题对照

## 对应章节

- 教材：§2.4（用 TCP/UDP 编程）、§3.2（复用/分用）、§3.3（UDP）、§3.4（可靠原理→UDP 版自带停等重传）
- 笔记：`notes/ch2-04-sockets.md`（第 7 讲）、`notes/ch3-01-transport-udp.md`（第 9 讲）

## 协议要点（两版本共用一套"行文本/JSON 消息"语法，便于对照）

| 维度 | chat_tcp.py | chat_udp.py |
| --- | --- | --- |
| 连接 | listen/accept；四元组区分连接（§3.2） | bind 一个 socket；二元组收所有来源（§3.2） |
| 消息边界 | 无！按 `\n` 手动切分（粘包处理，§2.1） | 一报一消息，天然有边界（§3.3） |
| 可靠性 | TCP 保证 | 应用层 seq+ACK+3 次重传（§3.4 停等 ARQ） |
| 断开 | FIN/EOF 感知，广播"离开" | 无连接——靠 120s 活动时间 GC |
| 并发 | 每连接一线程 | 单 socket 收主循环 |

## 运行

```
# 服务端（任选一版，开两个终端对比）
python chat_tcp.py --server
python chat_udp.py --server

# 客户端（每个用户一个终端）
python chat_tcp.py --name alice
python chat_tcp.py --host 127.0.0.1 --name bob
python chat_udp.py --name carol

# 一键（含 py_compile 自检，默认起 TCP 服务端）
./run.sh            # run.sh server|client <name> 可指定角色
run.bat server
```

## 实验建议

1. 同时开两版服务端+客户端，`tcpdump -i lo port 9000 or port 9001`（或 Wireshark）对比：
   TCP 流里看到握手/ACK 噪音但应用只管写字节；UDP 里每消息一个数据报+你的应用层 ack 报文。
2. 在 UDP 客户端把 `TIMEOUT` 改 0.01 观察"假超时重传风暴"（第 11 讲 RTO 估计的动机）。
3. 思考：TCP 版如何把广播从"遍历所有 socket"优化成事件循环？（练习：selectors 重写）
