// p03/regfile.v —— 32×32 寄存器堆（RV32I/MIPS 风格：双读口组合，单写口同步）
// 对应讲义：notes/L05.md §1.4；notes/L09.md §1.2（CPU 核心部件）
// 规则（必须在 TB 中验证）：
//   1) 读是组合的：当拍地址当拍数据；
//   2) 写发生在上升沿，且同一沿"读到旧值"（写与读同址时：先读旧后写新）；
//   3) x0/零寄存器恒 0：写忽略、读恒 0（RISC-V 约定）。
// 行为模型用整数数组，iverilog/综合器均可处理（RAM 推断风格）。

`default_nettype none

module regfile #(
    parameter NREG = 32,
    parameter W    = 32,
    parameter AW   = 5
) (
    input  wire             clk,
    input  wire             rst_n,
    // 写口（同步）
    input  wire             wen,
    input  wire [AW-1:0]    waddr,
    input  wire [W-1:0]     wdata,
    // 读口 0/1（组合）
    input  wire [AW-1:0]    raddr0, raddr1,
    output wire [W-1:0]     rdata0, rdata1
);
    reg [W-1:0] rf [0:NREG-1];
    integer i;

    initial for (i = 0; i < NREG; i = i + 1) rf[i] = {W{1'b0}};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < NREG; i = i + 1) rf[i] <= {W{1'b0}};
        end else if (wen && (waddr != {AW{1'b0}})) begin
            rf[waddr] <= wdata;
        end
    end

    assign rdata0 = (raddr0 == {AW{1'b0}}) ? {W{1'b0}} : rf[raddr0];
    assign rdata1 = (raddr1 == {AW{1'b0}}) ? {W{1'b0}} : rf[raddr1];
endmodule

`default_nettype wire
