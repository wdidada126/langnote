// p02/full_adder.v —— 全加器（结构化：两个半加器 + 或门）
// 对应讲义：notes/L03.md §1.1
// S = a xor b xor cin ; Cout = ab + cin(a xor b)

`default_nettype none

module full_adder (
    input  wire a, b, cin,
    output wire s, cout
);
    wire s1, c1, c2;

    half_adder u_ha1 (.a(a),     .b(b),    .s(s1), .c(c1));
    half_adder u_ha2 (.a(s1),    .b(cin),  .s(s),  .c(c2));
    or         u_or  (cout, c1, c2);
endmodule

`default_nettype wire
