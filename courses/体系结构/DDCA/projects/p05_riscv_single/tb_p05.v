// p05/tb_p05.v —— 单周期 RV32I CPU testbench：加载 prog.mem，跑到 halt，比对寄存器终值
// 期望输出：P05: ALL TESTS PASSED（并打印最终寄存器转储）
// prog.s -> asm2mem.py -> prog.mem（本目录已附生成好的 .mem）
// 对应讲义：notes/L09.md（全链路：取指/译码/执行/访存/写回）

`timescale 1ns/1ps

module tb_p05;
    integer errors = 0;
    integer cycles = 0;
    integer i;
    reg clk = 0;
    reg rst_n;
    always #5 clk = ~clk;

    wire halt;
    riscv_single #(
        .IMEM_FILE("prog.mem"),
        .IMEM_WORDS(256),
        .DMEM_BASE(32'h0000_1000),
        .DMEM_WORDS(64)
    ) dut (
        .clk(clk), .rst_n(rst_n), .halt(halt)
    );

    // 期望终值（prog.s 头部注释即其来源；X = 不检查）
    reg [31:0] exp [0:31];
    reg        chk [0:31];

    initial begin
        for (i = 0; i < 32; i = i + 1) chk[i] = 0;
        exp[5]=32'd20;       chk[5]=1;   // sll/srl 后
        exp[6]=32'h0000_1000; chk[6]=1;  // lui
        exp[7]=32'd7;        chk[7]=1;
        exp[8]=32'd17;       chk[8]=1;   // add
        exp[9]=32'd3;        chk[9]=1;   // sub
        exp[10]=32'd2;       chk[10]=1;  // and
        exp[11]=32'd15;      chk[11]=1;  // or
        exp[12]=32'd13;      chk[12]=1;  // xor
        exp[13]=32'd20;      chk[13]=1;  // sw+lw 全链路
        exp[14]=32'd1;       chk[14]=1;  // beq 未跳 + jal 跳过 +100
        exp[15]=32'd64;      chk[15]=1;  // jal 链接值 PC+4
        exp[16]=32'd0;       chk[16]=1;  // 循环计数
        exp[17]=32'd15;      chk[17]=1;  // 5+4+3+2+1

        rst_n = 0;
        repeat (2) @(negedge clk);
        rst_n = 1;

        // 运行直到 halt（或超时，模拟看门狗——L15 的定时思想）
        while (!halt && cycles < 2000) begin
            @(negedge clk);
            cycles = cycles + 1;
        end
        if (!halt) begin
            errors = errors + 1;
            $display("FAIL: timeout, PC stuck at %h (last instr %h)", dut.pc, dut.instr);
        end

        // 终值比对
        for (i = 0; i < 32; i = i + 1) begin
            if (chk[i] && dut.rf[i] !== exp[i]) begin
                errors = errors + 1;
                $display("FAIL: x%0d = %h, expected %h", i, dut.rf[i], exp[i]);
            end
        end
        // 数据存储器抽查（store 路径）
        if (dut.u_dmem.mem[0] !== 32'd17) begin
            errors = errors + 1; $display("FAIL: dmem[0]=%0d exp 17", dut.u_dmem.mem[0]);
        end

        // 转储（方便对照 riscv-isa-sim / Spike 输出）
        $display("---- final register file (halted after %0d cycles) ----", cycles);
        for (i = 0; i < 32; i = i + 1)
            $display("x%0d = %08h", i, dut.rf[i]);

        if (errors == 0)
            $display("P05: ALL TESTS PASSED");
        else
            $display("P05: %0d ERRORS", errors);
        $finish;
    end
endmodule
