#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_http_server —— 《自顶向下方法》§2.2 配套：多线程 HTTP/1.1 GET 服务器 + 简易路由。

知识点对照：
  * HTTP 请求行/头部解析（教材 Fig.2.6/2.9 语法）
  * 响应状态行 + Content-Type/Content-Length/Connection 头
  * 304 条件请求（If-Modified-Since 简化演示）
  * 每连接一线程并发模型（§2.4 socket + §2.1 C/S）
仅用标准库：socket, threading, os, time, mimetypes, urllib.parse。
"""

import os
import re
import socket
import threading
import mimetypes
import time
from urllib.parse import urlparse, unquote

HOST, PORT = "127.0.0.1", 8000
WWW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")
MAX_BODY = 4096  # 本 demo 只读请求头，限制读取量防内存问题

STATUS_TEXT = {
    200: "OK", 304: "Not Modified", 400: "Bad Request",
    404: "Not Found", 405: "Method Not Allowed", 500: "Internal Server Error",
}

_counter = {"n": 0}
_counter_lock = threading.Lock()


# ---------- 简易路由表：路径 -> handler(query, headers) -> (status, body_bytes, extra_headers) ----------

def route_index(query, headers):
    html = (b"<html><body><h1>topdown ch2 http server</h1>"
            b"<ul><li><a href='/hello?name=world'>/hello</a></li>"
            b"<li><a href='/time'>/time</a></li>"
            b"<li><a href='/count'>/count</a></li>"
            b"<li><a href='/static/index.html'>/static/...</a></li></ul></body></html>")
    return 200, html, {"Content-Type": "text/html; charset=utf-8"}


def route_hello(query, headers):
    name = unquote(query.get("name", ["anonymous"])[0])
    body = "Hello, {}!\n".format(name).encode("utf-8")
    return 200, body, {"Content-Type": "text/plain; charset=utf-8"}


def route_time(query, headers):
    body = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()).encode()
    return 200, body, {"Content-Type": "text/plain",
                       "Cache-Control": "no-store"}


def route_count(query, headers):
    with _counter_lock:
        _counter["n"] += 1
        n = _counter["n"]
    body = "requests served: {}\n".format(n).encode()
    return 200, body, {"Content-Type": "text/plain", "Cache-Control": "no-store"}


ROUTES = {
    "/": route_index,
    "/hello": route_hello,
    "/time": route_time,
    "/count": route_count,
}


def handler_static(query, headers, path):
    rel = unquote(path[len("/static/"):])
    safe = os.path.normpath(rel).lstrip("/\\")
    full = os.path.join(WWW_DIR, safe)
    if not os.path.abspath(full).startswith(os.path.abspath(WWW_DIR) + os.sep):
        return 400, b"path traversal rejected\n", {"Content-Type": "text/plain"}
    if not os.path.isfile(full):
        return 404, b"not found\n", {"Content-Type": "text/plain"}
    mtime = int(os.path.getmtime(full))
    last_mod = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(mtime))
    ims = headers.get("if-modified-since")
    if ims == last_mod:  # 简化版协商缓存（教材 §2.2.1 conditional GET）
        return 304, b"", {"Last-Modified": last_mod}
    with open(full, "rb") as f:
        data = f.read()
    ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
    return 200, data, {"Content-Type": ctype, "Last-Modified": last_mod}


# ---------- 请求解析 ----------

def recv_until_headers(conn):
    """循环读直到 '\r\n\r\n'（TCP 字节流无边界：必须自己判框架，§2.1/§3.5）。"""
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = conn.recv(4096)
        if not chunk:
            break
        buf += chunk
        if len(buf) > 64 * 1024:
            raise ValueError("header too large")
    return buf


def parse_request(raw):
    head, _, rest = raw.partition(b"\r\n\r\n")
    lines = head.decode("latin-1").split("\r\n")
    method, target, version = lines[0].split(" ", 2)
    headers = {}
    for ln in lines[1:]:
        if ":" in ln:
            k, v = ln.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return method, target, version, headers, rest


def build_response(status, body, extra_headers, version="HTTP/1.1"):
    h = dict(extra_headers)
    h.setdefault("Content-Type", "text/plain")
    h["Content-Length"] = str(len(body))
    h["Server"] = "topdown-demo/1.0"
    h["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    lines = ["{} {} {}".format(version, status, STATUS_TEXT.get(status, ""))]
    lines += ["{}: {}".format(k, v) for k, v in h.items()]
    return ("\r\n".join(lines) + "\r\n\r\n").encode("latin-1") + body


# ---------- 连接处理 ----------

def handle_client(conn, addr):
    conn.settimeout(10)
    try:
        raw = recv_until_headers(conn)
        if not raw:
            return
        method, target, version, headers, _rest = parse_request(raw)
        parsed = urlparse(target)
        path = parsed.path
        query = {}
        for k, v in re.findall(r"([^=&]+)=?([^=&]*)", parsed.query):
            if v:
                query.setdefault(k, []).append(v)
        print("[{}] {} {} ({})".format(addr[0], method, target,
                                       headers.get("host", "-")))
        if method == "GET":
            if path in ROUTES:
                status, body, hdrs = ROUTES[path](query, headers)
            elif path.startswith("/static/"):
                status, body, hdrs = handler_static(query, headers, path)
            else:
                status, body, hdrs = 404, b"no such route\n", {}
        elif method == "HEAD":
            status, body, hdrs = 200, b"", {}
            hdrs = dict(hdrs)
        elif method in ("POST", "PUT", "DELETE"):
            status, body, hdrs = 405, b"this demo only serves GET/HEAD\n", {}
        else:
            status, body, hdrs = 400, b"bad request\n", {}
        close = headers.get("connection", "").lower() == "close" or version == "HTTP/1.0"
        if status == 304:
            resp = build_response(status, b"", hdrs)
        else:
            resp = build_response(status, body, hdrs)
        conn.sendall(resp)
        if not close:
            # 教学简化：demo 不实现持久连接循环，直接关闭并带 keep-alive 提示
            pass
    except Exception as e:  # noqa: BLE001  演示服务器：记录即可
        try:
            conn.sendall(build_response(500, str(e).encode(), {}))
        except Exception:
            pass
    finally:
        conn.close()


def main():
    os.makedirs(WWW_DIR, exist_ok=True)
    sample = os.path.join(WWW_DIR, "index.html")
    if not os.path.exists(sample):
        with open(sample, "w", encoding="utf-8") as f:
            f.write("<h1>static index</h1><p>try /static/index.html</p>\n")
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(16)
    print("listening on http://{}:{}  (Ctrl-C to stop)".format(HOST, PORT))
    try:
        while True:
            conn, addr = srv.accept()   # 已完成三次握手（§3.5）
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
