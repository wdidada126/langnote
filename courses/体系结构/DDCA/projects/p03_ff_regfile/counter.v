// p03/counter.v —— 同步模 N 计数器（含使能与滚过标志）
// 对应讲义：notes/L05.md §1.5；也是 notes/L06.md "最小 FSM"（状态=计数值）
// 关键路径 = 加法器 + 比较器 + D 建立：L11 段平衡分析的第一个素材。

`default_nettype none

module counter #(
    parameter N     = 8,
    parameter MODUL = 16
) (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         en,
    output reg  [N-1:0] q,
    output wire         rollover   // 本拍 +en 后回到 0：模 MODUL 的"溢出脉冲"
);
    assign rollover = en && (q == MODUL - 1);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)          q <= {N{1'b0}};
        else if (en)         q <= rollover ? {N{1'b0}} : q + 1'b1;
        // en=0 隐式保持：时序块允许（FF 使能 Mux），不是 latch
    end
endmodule

`default_nettype wire
