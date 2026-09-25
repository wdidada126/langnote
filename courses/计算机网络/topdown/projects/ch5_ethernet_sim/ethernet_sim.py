#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch5_ethernet_sim —— 《自顶向下方法》Ch6 配套：以太网帧 + CRC 模拟 + 交换机自学习转发表。

知识点对照（笔记第 20/21 讲）：
  * 以太网 II 帧：dst(6) src(6) type(2) payload(46..1500 填充) FCS(4)
  * FCS = CRC-32（反射多项式 0xEDB88320，初值/末异或取反——与 zlib.crc32 同族）
  * 课堂版小多项式 CRC（G(x)=x^3+x+1 → 1011）逐比特除法演示（教材 Fig.6.4 手算过程）
  * 交换机三原则：源 MAC 学习、目的 MAC 查表、未知/广播泛洪；老化计时。
仅用标准库：struct, zlib, time。
"""

import struct
import zlib

BROADCAST = b"\xff" * 6


# ------------------------------------------------ 1. 小多项式 CRC 手算演示（教学用）

def crc_divide(msg_bits, gen_bits):
    """模 2 除法：返回余数 FCS。msg 为 '01' 串，gen 最高位为 1。"""
    g = len(gen_bits)
    padded = msg_bits + "0" * (g - 1)
    rem = list(padded)
    for i in range(len(msg_bits)):
        if rem[i] == "1":
            for j in range(g):
                rem[i + j] = "1" if rem[i + j] != gen_bits[j] else "0"
    return "".join(rem[len(msg_bits):])


def demo_small_crc():
    print("== 1. CRC 手算：M=10100110, G=1011 (x^3+x+1) ==")
    m = "10100110"
    g = "1011"
    fcs = crc_divide(m, g)
    sent = m + fcs
    print("  余数(FCS)={}  实际发送 {} ".format(fcs, sent))
    # 接收端：把 sent 整串再除 G，余 0 => 无错
    print("  接收校验：{} ÷ {} 余 {} => {}".format(sent, g, crc_divide(sent, g), "通过"))
    flipped = sent[:3] + ("1" if sent[3] == "0" else "0") + sent[4:]
    print("  单比特错：{} 余 {} => {}".format(flipped, crc_divide(flipped, g), "检出" if crc_divide(flipped, g) != "000" else "漏检(!)"))
    print("  性质小结：G 含 ≥3 项 ⇒ 所有单/双比特错必检；突发长度<3 必检（§6.2/笔记第 20 讲）。")


# ------------------------------------------------ 2. 以太网帧与 FCS

def mac_bytes(s):
    return bytes(int(b, 16) for b in s.split(":"))


def build_frame(dst, src, ethertype, payload):
    """以太网 II 帧；payload <46 时补零到最小 64B 帧（含 FCS）。"""
    if len(payload) < 46:
        payload = payload + b"\x00" * (46 - len(payload))
    if len(payload) > 1500:
        raise ValueError("payload exceeds MTU: IP should fragment (cf. §4.4), Ethernet never does")
    header = dst + src + struct.pack("!H", ethertype)
    fcs = (~zlib.crc32(header + payload)) & 0xFFFFFFFF     # 标准以太网 FCS 取反
    return header + payload + struct.pack("<I", fcs)


def parse_frame(frame):
    dst, src = frame[:6], frame[6:12]
    ethertype = struct.unpack("!H", frame[12:14])[0]
    body, fcs = frame[14:-4], struct.unpack("<I", frame[-4:])[0]
    calc = (~zlib.crc32(frame[:-4])) & 0xFFFFFFFF
    ok = calc == fcs
    def m(b):
        return ":".join("{:02x}".format(x) for x in b)
    return {"dst": m(dst), "src": m(src), "type": "0x{:04x}".format(ethertype),
            "len": len(frame), "crc_ok": ok, "payload_head": body[:24]}


def demo_frame():
    print("\n== 2. 以太网帧构造 + FCS 校验 ==")
    a = mac_bytes("aa:aa:aa:aa:aa:01")
    b = mac_bytes("bb:bb:bb:bb:bb:02")
    f = build_frame(b, a, 0x0800, b"\x45\x00" + b"hello ip datagram-ish")   # 0x0800=IPv4（§6.4 type 字段）
    info = parse_frame(f)
    print("  帧解析:", info)
    bad = bytearray(f)
    bad[20] ^= 0x01
    print("  翻转 1 字节后：", parse_frame(bytes(bad))["crc_ok"])
    print("  type 0x0800=IPv4, 0x0806=ARP, 0x8100=802.1Q（笔记第 15/21 讲的 type 呼应）")


# ------------------------------------------------ 3. 交换机自学习 + 泛洪

class Switch:
    def __init__(self, nports, aging=300):
        self.ports = {}          # mac -> (port, last_seen)
        self.nports = nports
        self.aging = aging

    def _flood(self, frame, in_port, dst):
        out = [p for p in range(self.nports) if p != in_port]
        self.log(dst, in_port, "泛洪->{}".format(out))
        return {p: frame for p in out}

    def _log(self, dst, in_port, action):
        print("    [sw] in={} dst={} {}".format(in_port, dst, action))

    def learn(self, src, port, now):
        self.ports[src] = (port, now)

    def handle(self, frame, in_port, now=0):
        """收到一帧：学习源 MAC，查目的 MAC——命中单播转发，否则泛洪。"""
        dst, src = frame[:6], frame[6:12]
        self.learn(src, in_port, now)
        if dst == BROADCAST:
            return self._flood(frame, in_port, "broadcast")
        ent = self.ports.get(dst)
        if ent is None:
            return self._flood(frame, in_port, "未知单播")
        port, _ = ent
        if port == in_port:
            self.log(dst, in_port, "同口丢弃(已在同段)")
            return {}
        self.log(dst, in_port, "查表命中->口{}".format(port))
        return {port: frame}


def demo_switch():
    print("\n== 3. 交换机自学习/泛洪/老化 ==")
    sw = Switch(nports=4)
    m = {name: mac_bytes("cc:cc:cc:cc:cc:0{}".format(i + 1))
         for i, name in enumerate(("alice", "bob", "carol"))}
    port_of = {"alice": 0, "bob": 1, "carol": 2}
    print("  ① alice->bob 第一帧：表空 ⇒ 泛洪；同帧学 alice@0")
    sw.handle(build_frame(m["bob"], m["alice"], 0x0800, b"hi"), port_of["alice"])
    print("  ② bob 回复：查 alice@0 命中 ⇒ 单播，不再泛洪")
    sw.handle(build_frame(m["alice"], m["bob"], 0x0800, b"re"), port_of["bob"])
    print("  ③ alice->carol：carol 未知 ⇒ 泛洪（carol 收两份？只给非入口）")
    sw.handle(build_frame(m["carol"], m["alice"], 0x0800, b"hey"), port_of["alice"])
    print("  ④ 广播帧 arp who-has：")
    sw.handle(build_frame(BROADCAST, m["carol"], 0x0806, b"who-has"), port_of["carol"])
    print("  最终 MAC 表：")
    for k, (p, t) in sorted(sw.ports.items()):
        print("    {} -> port {}".format(":".join("{:02x}".format(x) for x in k), p))
    print("  要点：学习靠【源 MAC】，转发靠【目的 MAC】；广播/未知一律泛洪——两棵树合成二层交换（§6.4）。")


def main():
    demo_small_crc()
    demo_frame()
    demo_switch()
    print("\n对照实验：Wireshark 抓任意局域网帧看前导码/FCS；把本文件帧 hex dump 与真实帧比对"
          "（前导码 7B+SFD 不在以太网帧内存里，属于物理层）。")


if __name__ == "__main__":
    main()
