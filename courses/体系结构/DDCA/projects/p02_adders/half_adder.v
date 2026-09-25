// p02/half_adder.v —— 半加器：两位相加，无低位进位输入
// 对应讲义：notes/L03.md §1.1；H&H Fig.3.2
// S = A xor B, C = A and B

`default_nettype none

module half_adder (
    input  wire a, b,
    output wire s, c
);
    assign s = a ^ b;
    assign c = a & b;
endmodule

`default_nettype wire
