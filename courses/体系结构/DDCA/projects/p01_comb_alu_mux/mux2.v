// p01/mux2.v —— 2 选 1 多路选择器（参数化位宽）
// 对应讲义：notes/L03.md §1.3；H&H Ch.2.7
// 说明：Mux 是"可编程连线"，FPGA 的 LUT 本质就是 Mux+SRAM（notes/L04.md §1.4）

`default_nettype none

module mux2 #(
    parameter W = 1
) (
    input  wire [W-1:0] d0,   // s=0 时选中
    input  wire [W-1:0] d1,   // s=1 时选中
    input  wire         s,    // 选择信号
    output wire [W-1:0] y
);
    assign y = s ? d1 : d0;
endmodule

`default_nettype wire
