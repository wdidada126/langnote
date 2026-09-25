#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p05 简易汇编器：RV32I 子集 -> .mem（每行一个 32 位字，$readmemh 十六进制格式）
用法:  python asm2mem.py prog.s prog.mem
支持:  lui addi andi ori xori slli srli add sub and or xor sll srl slt sltu
       lw sw（形式: rd, off(rs1)）beq bne jal halt；伪指令 mv rd,rs
约定:  寄存器 x0..x31；立即数十进制或 0x 十六进制；标签在行首 "name:"。
对应讲义: notes/L08.md §1.4（"汇编->机器码 = 译码器的逆运算"——本脚本就是迷你汇编器）
"""
import re

REG = re.compile(r'^x([0-9]|[12][0-9]|3[01])$')


def pr(tok):
    t = tok.strip()
    m = REG.match(t)
    if not m:
        raise ValueError('bad register: %r' % tok)
    return int(m.group(1))


def pi(tok):
    t = tok.strip().lower()
    return int(t, 16) if t.startswith('0x') else int(t, 10)


def fields(v, lo, width):
    """取 v 二进制补码表示的第 lo..lo+width-1 位"""
    return (v >> lo) & ((1 << width) - 1)


def split_args(s):
    return [a for a in re.split(r'[,()\s]+', s.strip()) if a != '']


def encode(mnem, args, labels, addr):
    """一条指令 -> 32 位字；branch/jal 的目标标签必须已在 labels{名:字节地址}"""
    if mnem == 'halt':
        return 0x2F                                   # custom-0，仿真用停机
    if mnem == 'mv':
        return encode('addi', [args[0], args[1], '0'], labels, addr)
    if mnem == 'lui':
        rd, imm = pr(args[0]), pi(args[1])
        return ((imm & 0xFFFFF) << 12) | (rd << 7) | 0x37
    if mnem in ('addi', 'andi', 'ori', 'xori', 'slli', 'srli'):
        rd, rs, imm = pr(args[0]), pr(args[1]), pi(args[2])
        f3 = {'addi': 0, 'slli': 1, 'srli': 5, 'xori': 4, 'ori': 6, 'andi': 7}[mnem]
        if mnem in ('slli', 'srli'):
            if not 0 <= imm <= 31:
                raise ValueError('shamt out of range: %d' % imm)
            imm12 = (0x20 if mnem == 'srli' else 0) << 5 | imm
        else:
            imm12 = fields(imm, 0, 12)
        return (imm12 << 20) | (rs << 15) | (f3 << 12) | (rd << 7) | 0x13
    if mnem in ('add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'slt', 'sltu'):
        if mnem in ('sll', 'srl') and len(args) == 3 and not REG.match(args[2].strip()):
            # 便利写法：sll/srl 第三操作数给立即数时自动按 slli/srli 编码
            return encode(mnem + 'i', args, labels, addr)
        rd, rs1, rs2 = pr(args[0]), pr(args[1]), pr(args[2])
        f3 = {'add': 0, 'sub': 0, 'slt': 2, 'sltu': 3, 'xor': 4, 'sll': 1,
              'srl': 5, 'or': 6, 'and': 7}[mnem]
        f7 = 0x20 if mnem == 'sub' else 0
        return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | 0x33
    if mnem in ('lw', 'sw'):
        # 解析后 split_args 已把 "0(x6)" 拆成 ['0','x6']
        if len(args) != 3:
            raise ValueError('lw/sw 需要形式: r, off(rs1)')
        r, off, rs1 = pr(args[0]), pi(args[1]), pr(args[2])
        if mnem == 'lw':
            return (fields(off, 0, 12) << 20) | (rs1 << 15) | (2 << 12) | (r << 7) | 0x03
        return (fields(off, 5, 7) << 25) | (r << 20) | (rs1 << 15) | \
               (2 << 12) | (fields(off, 0, 5) << 7) | 0x23
    if mnem in ('beq', 'bne'):
        rs1, rs2, lbl = pr(args[0]), pr(args[1]), args[2].strip()
        off = labels[lbl] - addr
        f3 = 0 if mnem == 'beq' else 1
        return (fields(off, 12, 1) << 31) | (fields(off, 5, 6) << 25) | \
               (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
               (fields(off, 1, 4) << 8) | (fields(off, 11, 1) << 7) | 0x63
    if mnem == 'jal':
        rd, lbl = pr(args[0]), args[1].strip()
        off = labels[lbl] - addr
        return (fields(off, 20, 1) << 31) | (fields(off, 1, 10) << 21) | \
               (fields(off, 11, 1) << 20) | (fields(off, 12, 8) << 12) | \
               (rd << 7) | 0x6F
    raise ValueError('unknown mnemonic: %s' % mnem)


def assemble(lines):
    labels = {}
    items = []
    pc = 0
    for raw in lines:
        line = re.split(r'#|//|;', raw)[0].strip()
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
    words = []
    for mnem, args, addr in items:
        words.append('%08x' % (encode(mnem, args, labels, addr) & 0xFFFFFFFF))
    return words, labels


def main():
    import sys
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, 'r', encoding='utf-8') as f:
        words, labels = assemble(f.readlines())
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words) + '\n')
    print('%s -> %s: %d words, labels=%s' %
          (src, dst, len(words), {k: hex(v) for k, v in sorted(labels.items(), key=lambda kv: kv[1])}))


if __name__ == '__main__':
    main()
