#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch3_arq —— 《自顶向下方法》§3.4 配套：在模拟损伤信道上运行 停等 / GBN / SR 三种 ARQ。

知识点对照：
  * rdt1.0→3.0 三件套：校验和（CRC 判错）、序号、超时重传（含"重发上次 ACK"的 rdt2.2 技巧）
  * 停等利用率 vs 流水线：同样的信道损伤，轮数与发送次数差异即 §3.4 效率讨论
  * GBN：累积确认、接收窗=1、超时回退整窗（go-back-N）
  * SR：独立确认、接收缓冲乱序、base 只推进到首个空洞
信道模型（教学简化，README 详述）：
  - 以"轮"为时间步：发送在第 r 轮 -> 第 r+1 轮到接收方；ACK 第 r+2 轮回到发送方（RTT=2 轮）。
  - 每个报文独立判：丢失 p_loss / 比特错 p_err（表现为 CRC 校验失败）；ACK 丢失 p_ack。
  - 不产生乱序（乱序留给习题：把发送顺序打乱即可自行扩展）。
仅用标准库：zlib, random, struct。
"""

import random
import struct
import zlib

SEQ_MOD = 1 << 16


def make_pkt(seq, payload):
    """返回 (seq, payload, crc)；crc 基于 seq+payload 计算。"""
    crc = zlib.crc32(struct.pack("!II", seq, payload)) & 0xFFFFFFFF
    return (seq, payload, crc)


def crc_ok(pkt):
    seq, payload, crc = pkt
    return crc == (zlib.crc32(struct.pack("!II", seq, payload)) & 0xFFFFFFFF)


class Channel:
    def __init__(self, p_loss=0.10, p_err=0.05, p_ack=0.10):
        self.p_loss, self.p_err, self.p_ack = p_loss, p_err, p_ack

    def pass_data(self, pkt):
        r = random.random()
        if r < self.p_loss:
            return None                                   # 整包丢失
        if r < self.p_loss + self.p_err:                  # 比特错：篡改 crc 字段
            seq, payload, crc = pkt
            return (seq, payload, crc ^ 0x1)
        return pkt

    def pass_ack(self, ack):
        return None if random.random() < self.p_ack else ack


def run(kind, N, ch, w=4, timeout=3, seed=0, limit=10000):
    random.seed(seed)
    dataq = []           # (arrive_round, pkt) 在途数据
    ackq = []            # (arrive_round, ack_num) 在途 ACK
    state = {
        "base": 0,           # 发送方：最早未确认序号
        "nextseq": 0,        # 发送方：下一个新消息序号
        "sent": {},          # seq -> 最近发送轮
        "rx_expect": 0,      # 接收方（GBN）唯一期望 / （停等）期望 seq 翻转
        "rx_buf": {},        # SR 接收缓冲 seq -> payload
        "rx_lastack": None,  # 接收方上次回过的 ACK（重复时报文错/乱序的"重发 ACK"）
        "acked": set(),      # SR 已确认集合
        "delivered": 0,      # 已交付应用的消息数
        "tx": 0,             # 数据报文发送总次数
        "round": 0,
    }

    def to_rx(pkt):
        dataq.append((state["round"] + 1, pkt))

    def to_tx(ack):
        ackq.append((state["round"] + 1, ack))

    while state["delivered"] < N and state["round"] < limit:
        state["round"] += 1
        r = state["round"]

        # ---------- 1) 数据到达接收方 ----------
        arrived = [p for (ra, p) in dataq if ra == r]
        dataq[:] = [(ra, p) for (ra, p) in dataq if ra != r]
        for pkt in sorted(arrived, key=lambda p: p[0]):
            ok = crc_ok(pkt)
            if kind == "stopwait":
                exp = state["rx_expect"] % SEQ_MOD
                if ok:
                    if pkt[0] == exp:
                        state["delivered"] += 1
                        state["rx_expect"] += 1
                        state["rx_lastack"] = pkt[0]
                        to_tx(pkt[0])                      # 正确：ACK 该 seq
                    else:
                        # 重复包：丢弃但重发上次 ACK（rdt2.2/3.0）
                        if state["rx_lastack"] is not None:
                            to_tx(state["rx_lastack"])
                        else:
                            to_tx((exp - 1) % SEQ_MOD)
                # CRC 错：不回 ACK，让发方超时（也可回 NAK，等价）
            elif kind == "gbn":
                exp = state["rx_expect"] % SEQ_MOD
                if ok and pkt[0] == exp:
                    state["delivered"] += 1
                    state["rx_expect"] += 1
                    state["rx_lastack"] = pkt[0]
                    to_tx(pkt[0])                          # 累积确认（此处=最后交付号）
                elif not ok:
                    if state["rx_lastack"] is not None:
                        to_tx(state["rx_lastack"])         # 等价"重发上次 ACK"
                # 乱序包直接丢弃（GBN 接收窗=1），不回 ACK——发方超时回退
            elif kind == "sr":
                if ok:
                    state["rx_buf"][pkt[0]] = pkt[1]
                    to_tx(pkt[0])                          # 独立确认

        # ---------- 2) ACK 回到发送方 ----------
        acks = [a for (ra, a) in ackq if ra == r]
        ackq[:] = [(ra, a) for (ra, a) in ackq if ra != r]
        for a in acks:
            if kind == "stopwait":
                if state["base"] % SEQ_MOD == a:
                    state["base"] += 1
                    state["nextseq"] = state["base"]
                    state["sent"].pop(state["base"] - 1, None)
            elif kind == "gbn":
                for s in list(state["sent"]):
                    if s <= a:
                        state["sent"].pop(s)
                state["base"] = max(state["base"], a + 1)
                state["nextseq"] = max(state["nextseq"], state["base"])
            elif kind == "sr":
                state["acked"].add(a)
                while state["delivered"] < state["nextseq"] and \
                        state["delivered"] % SEQ_MOD in state["acked"]:
                    seq_d = state["delivered"] % SEQ_MOD
                    state["rx_buf"].pop(seq_d, None)
                    state["sent"].pop(state["delivered"], None)
                    state["delivered"] += 1
                state["base"] = state["delivered"]

        # ---------- 3) 发送方决定本轮发什么 ----------
        if kind == "stopwait":
            b = state["base"]
            if b < N:
                if b not in state["sent"]:
                    state["sent"][b] = r
                    state["tx"] += 1
                    to_rx(make_pkt(b % SEQ_MOD, b))
                elif r - state["sent"][b] >= timeout:
                    state["sent"][b] = r
                    state["tx"] += 1
                    to_rx(make_pkt(b % SEQ_MOD, b))
        elif kind == "gbn":
            b = state["base"]
            if b in state["sent"] and r - state["sent"][b] >= timeout:
                for s in range(b, min(b + w, N)):          # 回退：整窗重发
                    state["sent"][s] = r
                    state["tx"] += 1
                    to_rx(make_pkt(s % SEQ_MOD, s))
            else:
                for s in range(b, min(b + w, N)):
                    if s >= state["nextseq"]:
                        state["nextseq"] = s + 1
                        state["sent"][s] = r
                        state["tx"] += 1
                        to_rx(make_pkt(s % SEQ_MOD, s))
                        break                              # 每轮最多补一个新包（保守管道）
        elif kind == "sr":
            for s in range(state["base"], min(state["base"] + w, N)):
                if s in state["acked"]:
                    continue
                if s not in state["sent"] or r - state["sent"][s] >= timeout:
                    state["sent"][s] = r
                    state["tx"] += 1
                    to_rx(make_pkt(s % SEQ_MOD, s))
    rounds = state["round"]
    return rounds, state["tx"], state["delivered"]


def bar(frac, width=24):
    n = int(round(frac * width))
    return "[{}{}] {:.0%}".format("#" * n, "." * (width - n), frac)


def main():
    N = 20
    chp = dict(p_loss=0.10, p_err=0.05, p_ack=0.10)
    print("信道 p_loss={} p_err={} p_ack={}, 消息数 N={}".format(chp["p_loss"], chp["p_err"], chp["p_ack"], N))
    print("{:<16} {:>6} {:>7} {:>9} {:>10}  {}".format("协议", "轮数", "发送", "信道利用率", "交付速率", "对比停等"))
    results = {}
    for kind, w, label in (("stopwait", 1, "停等(rdt3.0)"), ("gbn", 4, "GBN(w=4)"), ("sr", 4, "SR(w=4)")):
        rounds, tx, got = run(kind, N, Channel(**chp), w=w, seed=42)
        results[kind] = rounds
        eff = got / tx if tx else 0.0
        speed = got / rounds * N
        rel = results["stopwait"] / rounds if rounds else 0.0
        print("{:<16} {:>6} {:>7} {:>9.2f} {:>7.2f}/RTT {}  x{:.1f}".format(
            label, rounds, tx, eff, N / max(1, rounds / 2), bar(min(1.0, speed / (2 * N))), rel))
    print("\n读图要点：")
    print("  * 轮数≈完成时间：流水线协议显著更短（§3.4 停等利用率公式的仿真验证）。")
    print("  * 信道利用率=有效交付/发送次数：GBN 因回退重发整窗最低，SR 最高。")
    print("  * 把 p_err 升到 0.3 再跑：观察 GBN/SR 差距进一步拉开（乱序/错误密集时 SR 胜出）。")


if __name__ == "__main__":
    main()
