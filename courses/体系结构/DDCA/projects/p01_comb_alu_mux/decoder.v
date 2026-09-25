// p01/decoder.v —— 2-4 译码器（带使能，低有效输出可选：此处高有效）
// 对应讲义：notes/L03.md §1.3；notes/L07.md §1.2（存储阵列行译码的雏形）
// EN=0 时所有输出为 0（三态/片选思想的简化版）

`default_nettype none

module decoder2to4 (
    input  wire [1:0] addr,
    input  wire       en,
    output wire [3:0] sel
);
    assign sel[0] = en & ~addr[1] & ~addr[0];
    assign sel[1] = en & ~addr[1] &  addr[0];
    assign sel[2] = en &  addr[1] & ~addr[0];
    assign sel[3] = en &  addr[1] &  addr[0];
endmodule

`default_nettype wire
