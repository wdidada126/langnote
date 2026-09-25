// p05/imem.v —— 指令存储器：组合读，上电 $readmemh 加载 .mem 程序
// 对应讲义：notes/L09.md §1.2（IMem 是单周期 datapath 的第一个黑盒）
// 地址约定：PC 从 0 开始，字对齐（addr[1:0] 忽略）。

`default_nettype none

module imem #(
    parameter FILE   = "prog.mem",
    parameter WORDS  = 256
) (
    input  wire [31:0] addr,
    output wire [31:0] rdata
);
    reg [31:0] mem [0:WORDS-1];
    integer i;   // Verilog-2005：声明须放模块级（initial 无名块内不允许变量声明）

    initial begin
        for (i = 0; i < WORDS; i = i + 1) mem[i] = 32'h0000_0013; // nop: addi x0,x0,0
        $readmemh(FILE, mem);
    end

    assign rdata = mem[addr[$clog2(WORDS)+1:2]];
endmodule

`default_nettype wire
