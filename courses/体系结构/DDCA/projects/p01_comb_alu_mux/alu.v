// p01/alu.v —— 4 位 ALU：8 种操作 + Zero 标志
// 对应讲义：notes/L03.md §1.4（"同一结构，功能由选择线编码表决定"）
// 也是 notes/L09.md 单周期 CPU 中 ALU 部件的最小原型
//
// funct[2:0] 编码：
//   000 add  001 sub  010 and  011 or
//   100 xor  101 sll  110 srl  111 slt(无符号比较，1/0)
// 注意：case 内是有符号还是无符号要显式声明（$signed/$unsigned），
// 这是 notes/L07.md 补码算术在 HDL 里的落点。

`default_nettype none

module alu4 (
    input  wire [3:0] a,
    input  wire [3:0] b,
    input  wire [2:0] funct,
    output reg  [3:0] y,
    output wire       zero
);
    always @(*) begin
        case (funct)
            3'b000:  y = a + b;
            3'b001:  y = a - b;
            3'b010:  y = a & b;
            3'b011:  y = a | b;
            3'b100:  y = a ^ b;
            3'b101:  y = a << b;            // 移位量超过位宽时结果为 0（Verilog 语义）
            3'b110:  y = a >> b;
            3'b111:  y = {3'b0, (a < b)};   // 无符号置slt
            default: y = 4'b0;
        endcase
    end

    assign zero = (y == 4'b0);
endmodule

`default_nettype wire
