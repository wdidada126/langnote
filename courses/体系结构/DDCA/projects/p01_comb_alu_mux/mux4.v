// p01/mux4.v —— 4 选 1 多路选择器（结构化：用 3 个 mux2 拼装）
// 对应讲义：notes/L03.md §1.3 —— "层次化设计方法学"第一次实践
// 2 位选择信号 sel：sel[0] 控制第一级，sel[1] 控制第二级

`default_nettype none

module mux4 #(
    parameter W = 1
) (
    input  wire [W-1:0] d0, d1, d2, d3,
    input  wire [1:0]   sel,
    output wire [W-1:0] y
);
    wire [W-1:0] a, b;

    mux2 #(.W(W)) u_m0 (.d0(d0), .d1(d1), .s(sel[0]), .y(a));
    mux2 #(.W(W)) u_m1 (.d0(d2), .d1(d3), .s(sel[0]), .y(b));
    mux2 #(.W(W)) u_m2 (.d0(a),  .d1(b),  .s(sel[1]), .y(y));
endmodule

`default_nettype wire
