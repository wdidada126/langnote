// p03/dff.v —— 上升沿 D 触发器（异步低有效复位）
// 对应讲义：notes/L05.md §1.2；H&H Fig.5.16
// 注意复位在敏感表：异步复位。同步复位写法把 if(rst) 放进 else 之前且敏感表只留 clk。

`default_nettype none

module dff (
    input  wire clk,
    input  wire rst_n,   // 异步复位，低有效
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 1'b0;
        else        q <= d;
    end
endmodule

`default_nettype wire
