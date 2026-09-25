// p02/rca.v —— 行波进位加法器（Ripple Carry Adder），参数化位宽
// 对应讲义：notes/L03.md §1.1 —— 关键路径 = N 级全加器串联 ≈ O(N)
// generate 语句：H&H App.B 推荐的可综合循环展开写法

`default_nettype none

module rca #(
    parameter N = 4
) (
    input  wire [N-1:0] a, b,
    input  wire         cin,
    output wire [N-1:0] s,
    output wire         cout
);
    wire [N:0] c;
    assign c[0] = cin;

    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : g_fa
            full_adder u_fa (
                .a(a[i]), .b(b[i]), .cin(c[i]),
                .s(s[i]), .cout(c[i+1])
            );
        end
    endgenerate

    assign cout = c[N];
endmodule

`default_nettype wire
