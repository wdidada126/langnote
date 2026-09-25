#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch3_chat TCP 版 —— 《自顶向下方法》§2.4/§3.5 配套：房间式群聊服务器 + 客户端（每连接一线程）。

协议（行文本，'\n' 结尾 = 应用层消息边界，对照 §2.1 字节流粘包条目）：
  上线首条 : /nick <名字>
  普通消息 : 任意文本 -> 广播给房间内其他人（带昵称前缀）
  私聊     : /msg <名字> <文本>
  退出     : /quit
服务端 TCP：accept 后的 socket 即"连接"（四元组区分，§3.2 分用）；FIN 关闭处理半死连接。
"""

import argparse
import socket
import threading

HOST, PORT = "127.0.0.1", 9000


# ---------------- 服务端 ----------------

class Room:
    def __init__(self):
        self.lock = threading.Lock()
        self.clients = {}          # conn -> nick

    def add(self, conn, nick):
        with self.lock:
            self.clients[conn] = nick

    def remove(self, conn):
        with self.lock:
            return self.clients.pop(conn, None)

    def snapshot(self):
        with self.lock:
            return list(self.clients.items())

    def broadcast(self, text, exclude=None):
        for conn, _ in self.snapshot():
            if conn is exclude:
                continue
            try:
                conn.sendall((text + "\n").encode("utf-8"))
            except OSError:
                pass  # 关闭将在 handler 的 recv 异常路径处理


def handler(conn, addr, room):
    conn.settimeout(300)  # 演示用的空闲踢出（对照 TCP 保活/NAT 超时，§3.5/§4.4）
    nick = None
    try:
        buf = b""
        while True:
            chunk = conn.recv(2048)
            if not chunk:
                break                       # 对端 FIN -> EOF
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                text = line.decode("utf-8", "replace").strip()
                if not text:
                    continue
                if nick is None:
                    if text.startswith("/nick "):
                        nick = text[6:].strip()[:16] or addr[0]
                        room.add(conn, nick)
                        conn.sendall("*** 你已加入，房间广播：{} 上线\n".format(nick).encode("utf-8"))
                        room.broadcast("*** {} 上线".format(nick), exclude=conn)
                    else:
                        conn.sendall("*** 请先发送 /nick <名字>\n".encode("utf-8"))
                elif text == "/quit":
                    raise EOFError()
                elif text.startswith("/msg "):
                    _, target, rest = (text.split(" ", 2) + ["", ""])[:3]
                    hit = [(c, n) for c, n in room.snapshot() if n == target]
                    if hit and rest:
                        hit[0][0].sendall("*** [私聊 {}] {}".format(nick, rest).encode("utf-8"))
                        conn.sendall("*** [-> {}] {}".format(target, rest).encode("utf-8"))
                else:
                    room.broadcast("{}: {}".format(nick, text), exclude=conn)
    except (EOFError, socket.timeout, ConnectionResetError, OSError):
        pass
    finally:
        left = room.remove(conn)
        if left:
            room.broadcast("*** {} 离开".format(left))
        conn.close()
        print("[tcp] {} 断开".format(addr))


def run_server(port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, port))
    srv.listen(16)
    print("chat-tcp server on {}:{} （Ctrl-C 退出）".format(HOST, port))
    room = Room()
    try:
        while True:
            conn, addr = srv.accept()
            print("[tcp] {} 接入".format(addr))
            threading.Thread(target=handler, args=(conn, addr, room), daemon=True).start()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        srv.close()


# ---------------- 客户端 ----------------

def reader(sock):
    while True:
        try:
            data = sock.recv(2048)
        except OSError:
            break
        if not data:
            print("\n[服务器已关闭连接]")
            break
        # 注意：TCP 短读常见（§2.1 字节流），生产应累积缓冲按行切分；此处直显
        print(data.decode("utf-8", "replace"), end="")


def run_client(host, port, name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))                # 触发三次握手（§3.5）
    print("已连接，输入即聊天；/msg 某人 内容；/quit 退出")
    s.sendall(("/nick " + name + "\n").encode("utf-8"))
    t = threading.Thread(target=reader, args=(s,), daemon=True)
    t.start()
    try:
        while True:
            line = input("")
            s.sendall((line + "\n").encode("utf-8"))
            if line.strip() == "/quit":
                break
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description="TCP group chat (topdown §2.4/§3.5)")
    ap.add_argument("--server", action="store_true")
    ap.add_argument("--host", default=HOST)
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--name", default="guest")
    a = ap.parse_args()
    if a.server:
        run_server(a.port)
    else:
        run_client(a.host, a.port, a.name)


if __name__ == "__main__":
    main()
