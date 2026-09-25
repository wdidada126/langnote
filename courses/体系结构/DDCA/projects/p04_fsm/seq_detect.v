// p04/seq_detect.v —— "1011" 序列检测器（重叠式，Mealy 型，三段式 FSM）
// 对应讲义：notes/L06.md §1.2（经典例题）
// 输入流 ...101011... 中末位 1 到来当拍 hit=1，且允许重叠：
//   匹配 1011 后，串尾 "1" 仍是新序列的前缀 ⇒ 状态回 S_1（失败回退边，KMP 雏形）。
// 三段式：段1 状态寄存器 / 段2 次态组合 / 段3 输出（Mealy：输出与次态同表）。

`default_nettype none

module seq_detect_1011 (
    input  wire clk,
    input  wire rst_n,
    input  wire din,
    output reg  hit      // Mealy 输出：与 din 同拍有效
);
    localparam S_IDLE = 2'd0;  // 无前缀匹配
    localparam S_1    = 2'd1;  // 已匹配 "1"
    localparam S_10   = 2'd2;  // 已匹配 "10"
    localparam S_101  = 2'd3;  // 已匹配 "101"

    reg [1:0] state, next;

    // 段1：状态寄存器
    always @(posedge clk or negedge rst_n)
        if (!rst_n) state <= S_IDLE;
        else        state <= next;

    // 段2+3：次态与 Mealy 输出
    always @(*) begin
        next = state;
        hit  = 1'b0;
        case (state)
            S_IDLE:  if (din) next = S_1;              // 输入 0：留在空闲
            S_1:     if (!din) next = S_10;            // 再来 1：仍以"1"结尾，保持
            S_10:    if (din)  next = S_101;
                     else      next = S_IDLE;          // "100" 没有任何前缀后缀
            S_101:   if (din) begin next = S_1; hit = 1'b1; end
                     else      next = S_10;            // "1010" 最长前缀后缀 = "10"
            default: next = S_IDLE;                    // 未用编码回安全态（L06 §4）
        endcase
    end
endmodule

`default_nettype wire
