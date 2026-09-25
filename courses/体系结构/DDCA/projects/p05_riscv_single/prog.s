# p05 演示程序（RV32I 子集，由 asm2mem.py 汇编为 prog.mem）
# 期望终值见 tb_p05.v 断言表：
#   x5=20 x6=0x1000 x7=7 x8=17 x9=3 x10=2 x11=15 x12=13
#   x13=20 x14=1 x15=64 x16=0 x17=15
        addi x5, x0, 10        # x5  = 10
        lui  x6, 1             # x6  = 0x1000（DMEM 基址）
        addi x7, x0, 7         # x7  = 7
        add  x8, x5, x7        # x8  = 17
        sub  x9, x5, x7        # x9  = 3
        and  x10, x5, x7       # x10 = 1010 & 0111 = 0010 = 2
        or   x11, x5, x7       # x11 = 1111 = 15
        xor  x12, x5, x7       # x12 = 1101 = 13
        sw   x8, 0(x6)         # dmem[0x1000] = 17
        sw   x9, 4(x6)         # dmem[0x1004] = 3
        lw   x13, 0(x6)        # x13 = 17
        add  x13, x13, x9      # x13 = 20（load->use 数据通路全链路）
        addi x14, x0, 0
        beq  x13, x0, Lskip    # 20!=0：不跳转（测"未跳转"路径）
        addi x14, x14, 1       # x14 = 1
Lskip:
        jal  x15, Ldone        # 链接跳转：x15 = 本条 PC+4 = 64
        addi x14, x14, 100     # 被跳过
Ldone:
        sll  x5, x5, 2         # x5  = 40
        srl  x5, x5, 1         # x5  = 20
        addi x16, x0, 5
        addi x17, x0, 0
Lloop:
        add  x17, x17, x16     # 累加 5+4+3+2+1 = 15
        addi x16, x16, -1
        bne  x16, x0, Lloop    # 向后分支（测负偏移编码）
        halt                   # 停机（custom-0，仅仿真）
