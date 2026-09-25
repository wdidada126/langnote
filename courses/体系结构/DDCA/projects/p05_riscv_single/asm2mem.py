#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p05 简易汇编器：RV32I 子集 -> .mem（每行一个字，$readmemh 格式）
用法:  python asm2mem.py prog.s prog.mem
支持:  lui addi andi ori xori slli srli add sub and or xor sll srl slt sltu
       lw sw beq bne jal halt ；伪指令 mv rd,rs
约定:  寄存器写 x0..x31；立即数十进制/0x 十六进制；标签在行首 "name:"。
对应讲义: notes/L08.md §1.4（指令->机器码 = 译码器的逆运算）
"""
import sys, re

REG = re.compile(r'^x(\d{1,2})$')

def parse_reg(tok):
    t = tok.strip()
    m = REG.match(t)
    if not m:
        raise ValueError('bad register: %r' % tok)
    r = int(m.group(1))
    if r > 31:
        raise ValueError('reg out of range: %s' % t)
    return r

def parse_imm(tok):
    t = tok.strip().lower()
    return int(t, 16) if t.startswith('0x') else int(t, 10)

def split_args(s):
    return [a for a in re.split(r'[,()\s]+', s.strip()) if a != '']

def field(v, lo, width):
    """取 v 的 [lo, lo+width) 位（用于拆分 B/J 立即数）"""
    return (v >> lo) & ((1 << width) - 1)

def s_field(v, bits):
    """把立即数按补码截成 bits 位再放入指令（符号位自然对齐）"""
    return v & ((1 << bits) - 1)

class Asm:
    def __init__(self):
        self.passno = 0
        self.out = []
        self.pc = 0

    def emit(self, w, line):
        if self.passno == 1:
            self.out.append('%08x' % (w & 0xFFFFFFFF))
        self.pc += 4

M = Asm()

def encode(mnem, args, labels, addr, expand_only=False):
    """返回指令字；branch/jal 需要 labels 已解析"""
    def reg_or_label(t):
        ts = t.strip()
        if ts in labels:
            return labels[ts]
        return parse_reg(ts)

    if mnem == 'halt':
        return 0x2F  # custom-0, 全 0 操作数
    if mnem == 'lui':
        rd, imm = parse_reg(args[0]), parse_imm(args[1])
        return (imm & 0xFFFFF) << 12 | rd << 7 | 0x37
    if mnem == 'mv':
        rd, rs = parse_reg(args[0]), parse_reg(args[1])
        return rd << 7 | 0x13 | rs << 15  # addi rd, rs, 0
    if mnem in ('addi', 'andi', 'ori', 'xori', 'slli', 'srli'):
        rd, rs, imm = parse_reg(args[0]), parse_reg(args[1]), parse_imm(args[2])
        f3 = {'addi': 0, 'andi': 6, 'ori': 4, 'xori': 4, 'slli': 1, 'srli': 5}[mnem]
        if mnem == 'xori': f3 = 4
        if mnem in ('slli', 'srli'):
            if imm > 31: raise ValueError('shamt too big')
            imm12 = (0 if mnem == 'slli' else 0x20) << 5 | imm
            return imm12 << 20 | rs << 15 | f3 << 12 | rd << 7 | 0x13
        return s_field(imm, 12) << 20 | rs << 15 | f3 << 12 | rd << 7 | 0x13
    if mnem in ('add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'slt', 'sltu'):
        rd, rs1, rs2 = map(parse_reg, args[:3])
        f3 = {'add': 0, 'sub': 0, 'and': 7, 'or': 6, 'xor': 4, 'sll': 1,
              'srl': 5, 'slt': 2, 'sltu': 3}[mnem]
        f7 = {'add': 0, 'sub': 0x20, 'and': 0, 'or': 0, 'xor': 0, 'sll': 0,
              'srl': 0, 'slt': 0, 'sltu': 0}[mnem]
        return f7 << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | rd << 7 | 0x33
    if mnem in ('lw', 'sw'):
        m = re.match(r'^(\w+)\s*,\s*(-?\w+|0x[0-9a-fA-F]+)\((\w+)\)$',
                     ','.join(args).replace(' ', ''))
        if not m:
            raise ValueError('lw/sw 需要形式 rd, off(rs1)')
        rd_rs2, off, rs1 = parse_reg(m.group(1)), parse_imm(m.group(2)), parse_reg(m.group(3))
        if mnem == 'lw':
            return s_field(off, 12) << 20 | rs1 << 15 | 2 << 12 | rd_rs2 << 7 | 0x03
        return (s_field(off, 12) >> 5) << 25 | rd_rs2 << 20 | rs1 << 15 | 2 << 12 | \
               (s_field(off, 12) & 0x1F) << 7 | 0x23
    if mnem in ('beq', 'bne'):
        rs1, rs2, lbl = parse_reg(args[0]), parse_reg(args[1]), args[2].strip()
        if lbl not in labels:
            raise KeyError('undefined label %s' % lbl)
        off = labels[lbl] - addr
        f3 = 0 if mnem == 'beq' else 1
        w = (s_field(off, 13) >> 12) << 31 | (s_field(off, 12) >> 5) << 25 | \
            rs2 << 20 | rs1 << 15 | f3 << 12 | ((s_field(off, 12) >> 1) & 0xF) << 8 | \
            ((s_field(off, 12) >> 11) & 1) << 7 | 0x63
        return w
    if mnem == 'jal':
        rd, lbl = parse_reg(args[0]), args[1].strip()
        if lbl not in labels:
            raise KeyError('undefined label %s' % lbl)
        off = labels[lbl] - addr
        return (s_field(off, 21) >> 20) << 31 | (s_field(off, 20) >> 1) << 21 | \
               ((s_field(off, 11) >> 10) & 1) << 20 | (s_field(off, 12) >> 12) << 12 | \
               rd << 7 | 0x6F
    raise ValueError('unknown mnemonic: %s' % mnem)


def assemble(src_lines):
    M.out = []
    labels, pc = {}, 0
    items = []
    for raw in src_lines:
        line = re.split(r'#|//', raw)[0].strip()
        if not line:
            continue
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m:
            labels[m.group(1)] = pc
            line = m.group(2).strip()
            if not line:
                continue
        mnem, _, rest = line.partition(' ')
        items.append((mnem.lower(), split_args(rest), pc))
        pc += 4

    for mnem, args, addr in items:
        if mnem == 'mv':
            mnem, args = 'addi', [args[0], args[1], '0']
        w = encode(mnem, args, labels, addr)
        M.out.append('%08x' % (w & 0xFFFFFFFF))
    return labels


def main():
    if len(sys.argv) != 4 or sys.argv[1] != '-':
        pass
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, 'r', encoding='utf-8') as f:
        labels = assemble(f.readlines())
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(M.out) + '\n')
    print('assembled %d words -> %s; labels: %s' %
          (len(M.out), dst, {k: hex(v) for k, v in sorted(labels.items(), key=lambda kv: kv[1])}))


if __name__ == '__main__':
    main()
