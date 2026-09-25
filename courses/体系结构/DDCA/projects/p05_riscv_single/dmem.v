// p05/dmem.v —— 数据存储器：同步写、组合读；基址 DMEM_BASE，越界读 0/写丢弃
// 对应讲义：notes/L09.md §1.2；notes/L07.md §4（"读同拍变"的简化模型声明）

`default_nettype none

module dmem #(
    parameter BASE  = 32'h0000_1000,
    parameter WORDS = 64
) (
    input  wire        clk,
    input  wire        wen,        // 字节写使能（本模型整字写）
    input  wire [31:0] addr,
    input  wire [31:0] wdata,
    output wire [31:0] rdata
);
    reg [31:0] mem [0:WORDS-1];

    wire        word_ok = (addr[1:0] == 2'b00);
    wire [31:0] off     = addr - BASE;
    wire        in_rng  = word_ok && (addr >= BASE) && (off < (WORDS*4));
    wire [$clog2(WORDS)-1:0] idx = off[$clog2(WORDS)+1:2];

    always @(posedge clk)
        if (wen && in_rng) mem[idx] <= wdata;

    assign rdata = in_rng ? mem[idx] : 32'h0;
endmodule

`default_nettype wire
