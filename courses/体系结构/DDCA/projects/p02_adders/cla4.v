// p02/cla4.v —— 4 位超前进位加法器（Carry-Lookahead Adder）
// 对应讲义：notes/L03.md §1.1 —— P = a xor b（传播），G = a & b（生成）
//   c1 = G0 + P0·c0
//   c2 = G1 + P1·G0 + P1·P0·c0
//   c3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·c0
//   c4 = G3 + P3·G2 + P3·P2·G1 + P3·P2·P1·G0 + P3·P2·P1·P0·c0
// 进位在 2~3 级门内并行产生 ⇒ 关键路径 O(log N)（组间级联时）
// 与 rca 对照：本文件用 assign 直写布尔式，让"面积换速度"看得见。

`default_nettype none

module cla4 (
    input  wire [3:0] a, b,
    input  wire       cin,
    output wire [3:0] s,
    output wire       cout
);
    wire [3:0] p, g;
    wire [4:0] c;

    assign p = a ^ b;
    assign g = a & b;
    assign c[0] = cin;

    assign c[1] = g[0] | (p[0] & c[0]);
    assign c[2] = g[1] | (p[1] & g[0]) | (p[1] & p[0] & c[0]);
    assign c[3] = g[2] | (p[2] & g[1]) | (p[2] & p[1] & g[0])
                | (p[2] & p[1] & p[0] & c[0]);
    assign c[4] = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1])
                | (p[3] & p[2] & p[1] & g[0])
                | (p[3] & p[2] & p[1] & p[0] & c[0]);

    // 和位 = 传播位 xor 本位进位输入（S = P ^ C[i]，与全加器语义等价）
    assign s = p ^ c[3:0];

    assign cout = c[4];
endmodule

`default_nettype wire
