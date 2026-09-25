#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch3_chat UDP 版 —— 《自顶向下方法》§2.4/§3.3 配套：无连接群聊（服务端一个 socket 收所有人）。

与 TCP 版的关键差异（本项目的教学目标）：
  * 分用规则：UDP socket 由 (dstIP, dstPort) 二元组标识 —— 服务器只 bind 一次、
    任何来源的数据报都进同一 socket，用 recvfrom/sendto 区分对端（§3.2）。
  * 消息边界：一个数据报=一条消息，天然无粘包；但可能丢失——本项目刻意加
    应用层 seq+ACK（停等式）演示"谁为可靠性买单"（§3.3/§3.4）。
  * 无连接：服务器不感知"断开"，用 (addr -> 最后活动时间) 的 GC 代替 FIN。
"""

import argparse
import json
import socket
import threading
import time

HOST, PORT = "127.0.0.1", 9001
RETRY, TIMEOUT = 3, 1.0


# ---------------- 报文格式（JSON 文本，一报一消息）----------------
# {"t":"msg","seq":n,"nick":"x","text":"..."}   消息
# {"t":"ack","seq":n}                            对 msg 的确认
# 发方：发送 -> 等 ack 1s -> 重传，最多 3 次 -> 打印"发送失败(丢包)"


def server_loop(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, port))                      # 不需要 listen/accept！
    print("chat-udp server on {}:{} （Ctrl-C 退出）".format(HOST, port))
    roster = {}                                # addr -> (nick, last_seen)
    lock = threading.Lock()

    def gc():
        now = time.time()
        with lock:
            gone = [a for a, (_, t) in roster.items() if now - t > 120]
            for a in gone:
                roster.pop(a)

    def recv_loop():
        while True:
            data, addr = s.recvfrom(4096)     # 任意来源 -> 同一 socket（二元组分用）
            try:
                m = json.loads(data.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            if m.get("t") != "msg":
                continue
            with lock:
                roster[addr] = (m.get("nick", addr[0]), time.time())
                peers = [a for a, (n, t) in roster.items() if a != addr]
                nicks = {a: n for a, (n, t) in roster.items()}
            s.sendto(json.dumps({"t": "ack", "seq": m.get("seq")}).encode("utf-8"), addr)
            line = "*** {}: {}".format(m.get("nick"), m.get("text"))
            for p in peers:
                try:
                    s.sendto(line.encode("utf-8"), p)   # 转发（尽力而为，不重传——广播消息教学简化）
                except OSError:
                    pass
            gc()
    try:
        recv_loop()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        s.close()


def client_loop(host, port, nick):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, 0))                          # 本地端口，让 ACK/广播有明确目的
    seq = 0
    print("UDP 模式：每条消息带序号，1s 无 ACK 重传（最多 3 次）。Ctrl-C 退出。")
    # 说明：单线程"发送-等待确认"循环即可同时收广播与 ACK，
    # 避免与后台线程争抢同一 socket（真实应用才做双线程/异步，见 §2.4 与 CSAPP 11 章）。
    while True:
        try:
            line = input("")
        except (EOFError, KeyboardInterrupt):
            break
        seq += 1
        pkt = json.dumps({"t": "msg", "seq": seq, "nick": nick, "text": line}).encode("utf-8")
        ok = False
        for attempt in range(RETRY):
            s.sendto(pkt, (host, port))
            s.settimeout(TIMEOUT)
            try:
                data, _ = s.recvfrom(4096)
                txt = data.decode("utf-8", "replace")
                try:
                    m = json.loads(txt)
                    if m.get("t") == "ack" and m.get("seq") == seq:
                        ok = True
                        break
                    print(txt)
                except ValueError:
                    print(txt)                 # 别人的广播（纯文本）
            except socket.timeout:
                continue
            finally:
                s.settimeout(None)
        if not ok:
            print("*** 本条消息在 {} 次重传后仍未确认（§3.4 的痛）".format(RETRY))
    s.close()


def main():
    ap = argparse.ArgumentParser(description="UDP group chat (topdown §2.4/§3.3)")
    ap.add_argument("--server", action="store_true")
    ap.add_argument("--host", default=HOST)
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--name", default="guest")
    a = ap.parse_args()
    if a.server:
        server_loop(a.port)
    else:
        client_loop(a.host, a.port, a.name)


if __name__ == "__main__":
    main()
