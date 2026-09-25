// p04/traffic_light.v —— 交通灯控制器（Moore 型 FSM + 秒计数器）
// 对应讲义：notes/L06.md §1.2 例题（G→Y→R 循环 + 行人请求）；Basys 3 Lab 4 的仿真版
// 设计说明（先状态图后代码的示范）：
//   状态：S_G(T_G 秒) → S_Y(T_Y 秒) → S_R(T_R 秒，可被 walk_req 提前到 ≥2s 放行)
//   done = tick && (cnt == 时长-1)；异步输入 walk_req 在 TB/顶层先双 FF 同步（L05 §4）。
//   输出为 Moore：只由 state 译码。

`default_nettype none

module traffic_light #(
    parameter T_G = 3'd5,
    parameter T_Y = 3'd2,
    parameter T_R = 3'd6
) (
    input  wire clk,
    input  wire rst_n,
    input  wire tick,      // 每秒一个宽脉冲（1 拍）
    input  wire walk_req,  // 已同步的行人请求电平
    output reg  red,
    output reg  yellow,
    output reg  green
);
    localparam [1:0] S_G = 2'd0, S_Y = 2'd1, S_R = 2'd2;

    reg [1:0] state;
    reg [2:0] cnt;

    wire [2:0] dur = (state == S_G) ? T_G :
                     (state == S_Y) ? T_Y : T_R;
    wire       at_last = (cnt == dur - 2'd1);
    wire       done    = tick && at_last;
    wire       early   = tick && (state == S_R) && walk_req && (cnt >= 3'd2);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_R;             // 上电安全态：红
            cnt   <= 3'd0;
        end else if (done || early) begin
            cnt   <= 3'd0;
            case (state)
                S_G:   state <= S_Y;
                S_Y:   state <= S_R;
                S_R:   state <= S_G;
                default: state <= S_R;   // 未用编码回安全态
            endcase
        end else if (tick) begin
            cnt <= cnt + 1'b1;
        end
    end

    // Moore 输出（组合译码；打一拍寄存版见 README 延伸实验）
    always @(*) begin
        {red, yellow, green} = 3'b000;
        case (state)
            S_G:     green  = 1'b1;
            S_Y:     yellow = 1'b1;
            S_R:     red    = 1'b1;
            default: red    = 1'b1;
        endcase
    end
endmodule

`default_nettype wire
