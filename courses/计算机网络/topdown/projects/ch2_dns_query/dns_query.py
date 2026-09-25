#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_dns_query —— 《自顶向下方法》§2.3 配套：手工构造/解析 DNS 报文的 A 记录查询器。

知识点对照：
  * DNS 报文头 12 字节：ID/FLAGS/QDCOUNT/ANCOUNT/NSCOUNT/ARCOUNT（§2.3, Fig.2.10）
  * QNAME 的 (len, label...) + 0x00 编码；回答段的 0xC0 压缩指针（本文件核心难点）
  * RR 四元组 (name, type, value, ttl)：A/AAAA/NS/CNAME
  * UDP 53 vs getaddrinfo（libc 完整客户端：hosts/NSS/缓存/多记录）对比计时
仅用标准库：socket, struct, time, random, sys, argparse。
"""

import argparse
import random
import socket
import struct
import time

TYPE_A, TYPE_NS, TYPE_CNAME, TYPE_AAAA = 1, 2, 5, 28
TYPE_NAME = {TYPE_A: "A", TYPE_NS: "NS", TYPE_CNAME: "CNAME", TYPE_AAAA: "AAAA"}


def encode_name(name):
    """www.example.com -> 3 'www' 7 'example' 3 'com' 0"""
    out = b""
    for label in name.rstrip(".").split("."):
        b = label.encode("ascii")
        if len(b) > 63:
            raise ValueError("label too long")
        out += bytes([len(b)]) + b
    return out + b"\x00"


def build_query(name, qtype=TYPE_A, rd=True):
    tid = random.randint(0, 0xFFFF)
    flags = 0x0100 if rd else 0x0000          # QR=0, RD
    header = struct.pack("!HHHHHH", tid, flags, 1, 0, 0, 0)
    q = encode_name(name) + struct.pack("!HH", qtype, 1)  # QTYPE, IN
    return tid, header + q


def parse_name(msg, off):
    """返回 (name, 新的偏移)；处理 0xC0 压缩指针（RFC 1035 §4.1.4）。"""
    labels = []
    jumped = False
    end = off
    while True:
        ln = msg[off]
        if ln == 0:
            off += 1
            if not jumped:
                end = off
            break
        if ln & 0xC0 == 0xC0:                 # 指针：高 2 位为 1
            ptr = struct.unpack("!H", msg[off:off + 2])[0] & 0x3FFF
            if not jumped:
                end = off + 2
            jumped, off = True, ptr
            continue
        labels.append(msg[off + 1:off + 1 + ln].decode("ascii", "replace"))
        off += 1 + ln
    return ".".join(labels), end


def parse_response(msg):
    tid, flags, qd, an, ns, ar = struct.unpack("!HHHHHH", msg[:12])
    rcode = flags & 0xF
    off = 12
    for _ in range(qd):                        # 问题段：name + type/class
        _, off = parse_name(msg, off)
        off += 4
    records = []
    for cnt, section in ((an, "ANSWER"), (ns, "AUTHORITY"), (ar, "ADDITIONAL")):
        for _ in range(cnt):
            name, off = parse_name(msg, off)
            rtype, rclass, ttl, rdlen = struct.unpack("!HHIH", msg[off:off + 10])
            off += 10
            rdata = msg[off:off + rdlen]
            off += rdlen
            if rtype == TYPE_A:
                val = socket.inet_ntoa(rdata)
            elif rtype == TYPE_AAAA:
                val = socket.inet_ntop(socket.AF_INET6, rdata)
            elif rtype in (TYPE_NS, TYPE_CNAME):
                val, _ = parse_name(msg, off - rdlen)
            else:
                val = rdata.hex()
            records.append((section, name, TYPE_NAME.get(rtype, "T{}".format(rtype)), val, ttl))
    return tid, rcode, records


def dns_query(name, server="8.8.8.8", qtype=TYPE_A, timeout=3.0):
    tid, pkt = build_query(name, qtype)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    t0 = time.perf_counter()
    try:
        s.sendto(pkt, (server, 53))
        data, _ = s.recvfrom(4096)
    finally:
        s.close()
    dt = (time.perf_counter() - t0) * 1000
    got_tid, rcode, records = parse_response(data)
    assert got_tid == tid, "transaction ID mismatch: possible spoofing (cf. §2.3 attacks)"
    return rcode, records, dt


def main():
    ap = argparse.ArgumentParser(description="manual DNS A/NS/CNAME query")
    ap.add_argument("name", nargs="?", default="www.google.com")
    ap.add_argument("--server", default="8.8.8.8")
    ap.add_argument("--type", default="A", choices=["A", "NS", "CNAME", "AAAA"])
    args = ap.parse_args()

    qtype = {"A": TYPE_A, "NS": TYPE_NS, "CNAME": TYPE_CNAME, "AAAA": TYPE_AAAA}[args.type]
    print("== 手工 DNS 查询 {} {} via {} ==" .format(args.type, args.name, args.server))
    try:
        rcode, records, ms = dns_query(args.name, args.server, qtype)
        print("rcode={}  time={:.1f}ms".format(rcode, ms))
        for sec, name, t, val, ttl in records:
            print("  [{:<9}] {}  {}  ttl={:<6} -> {}".format(sec, name, t, ttl, val))
    except Exception as e:  # noqa: BLE001
        print("手工查询失败:", e)

    # 对比：libc 的 getaddrinfo（含 hosts 文件、NSS、缓存、IPv4/6 排序——远不止一次 DNS）
    t0 = time.perf_counter()
    try:
        infos = socket.getaddrinfo(args.name, None, type=socket.SOCK_STREAM)
        ips = sorted({i[4][0] for i in infos})
        dt2 = (time.perf_counter() - t0) * 1000
        print("== getaddrinfo 对比：{:.1f}ms, {} 个连接级地址 {}".format(dt2, len(ips), ips[:4]))
    except Exception as e:  # noqa: BLE001
        print("getaddrinfo 失败:", e)
    print("说明：两者差异 = 'DNS 协议查询' 与 '完整名字解析服务' 的差异（§2.3 + 笔记第 6/7 讲）。")


if __name__ == "__main__":
    main()
