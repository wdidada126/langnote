// p03/reg_en.v —— 带使能加载的 N 位寄存器（dff 的阵列 + 反馈 Mux）
// 对应讲义：notes/L05.md §1.4 —— "n 位寄存器 = n 个 DFF + 使能 Mux"
// L09/L10 中所有 datapath 寄存器（MDR/IR/NPC...）都是这个模板的实例。

`default_nettype none

module reg_en #(
    parameter N = 8
) (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         en,     // 高：装载 d；低：保持
    input  wire [N-1:0] d,
    output wire [N-1:0] q
);
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : g_dff
            dff u_dff (
                .clk(clk), .rst_n(rst_n),
                .d(en ? d[i] : q[i]),   // 使能 Mux：反馈保持旧值
                .q(q[i])
            );
        end
    endgenerate
endmodule

`default_nettype wire
