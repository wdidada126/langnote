// p03/tb_p03.v —— 触发器/使能寄存器/计数器/寄存器堆 testbench
// 期望输出：P03: ALL TESTS PASSED
// 运行：./build.sh 或 build.bat（需 iverilog）

`timescale 1ns/1ps

module tb_p03;
    integer errors = 0;
    reg clk = 0;
    reg rst_n;
    always #5 clk = ~clk;   // 100 MHz 时钟

    // ---- dff ----
    reg  d;
    wire q;
    dff u_dff (.clk(clk), .rst_n(rst_n), .d(d), .q(q));

    // ---- reg_en ----
    reg         ren;
    reg  [7:0]  rd;
    wire [7:0]  rq;
    reg_en #(.N(8)) u_reg (.clk(clk), .rst_n(rst_n), .en(ren), .d(rd), .q(rq));

    // ---- counter 模10 ----
    reg         cen;
    wire [3:0]  cq;
    wire        crol;
    counter #(.N(4), .MODUL(10)) u_cnt (.clk(clk), .rst_n(rst_n), .en(cen), .q(cq), .rollover(crol));

    // ---- regfile ----
    reg         rfwen;
    reg  [4:0]  rfwaddr, rfr0, rfr1;
    reg  [31:0] rfwdata;
    wire [31:0] rfrd0, rfrd1;
    regfile u_rf (.clk(clk), .rst_n(rst_n),
                  .wen(rfwen), .waddr(rfwaddr), .wdata(rfwdata),
                  .raddr0(rfr0), .raddr1(rfr1), .rdata0(rfrd0), .rdata1(rfrd1));

    task tick;            // 运行一个完整时钟周期
        begin @(posedge clk); @(posedge clk); #1; end
    endtask

    initial begin
        rst_n = 0; d = 0; ren = 0; rd = 0; cen = 0;
        rfwen = 0; rfwaddr = 0; rfwdata = 0; rfr0 = 0; rfr1 = 1;
        #3; rst_n = 1; #3;

        // 1) dff：d=1 后下一个沿 q 变 1；保持 d=0 两拍观察异步复位
        d = 1; tick;
        if (q !== 1'b1) begin errors = errors + 1; $display("FAIL dff set"); end
        d = 0; tick;
        if (q !== 1'b0) begin errors = errors + 1; $display("FAIL dff clr"); end
        rst_n = 0; #1;
        if (q !== 1'b0) errors = errors + 1;   // 复位期间保持 0
        rst_n = 1; #1;

        // 2) reg_en：装载/保持
        rd = 8'h5A; ren = 1; tick;
        if (rq !== 8'h5A) begin errors = errors + 1; $display("FAIL reg load %h", rq); end
        rd = 8'hFF; ren = 0; tick;
        if (rq !== 8'h5A) begin errors = errors + 1; $display("FAIL reg hold %h", rq); end

        // 3) counter 模 10：从 0 走到 9 后归零且 rollover 恰一拍
        cen = 1;
        begin : cnt_test
            integer n;
            for (n = 0; n < 10; n = n + 1) begin
                if (cq !== n[3:0]) begin
                    errors = errors + 1;
                    $display("FAIL cnt t=%0d q=%0d", n, cq);
                end
                if (crol !== (n == 9)) begin
                    errors = errors + 1;
                    $display("FAIL rollover t=%0d", n);
                end
                tick;
            end
        end
        if (cq !== 4'd0) begin errors = errors + 1; $display("FAIL cnt wrap"); end
        cen = 0;

        // 4) regfile：写 x5=32'hCAFE、x6=32'hBEEF；x0 恒零；组合读即时更新
        rfwaddr = 5'd5; rfwdata = 32'hCAFE_0001; rfwen = 1; tick; rfwen = 0;
        rfwaddr = 5'd6; rfwdata = 32'hBEEF_0002; rfwen = 1; tick; rfwen = 0;
        rfwaddr = 5'd0; rfwdata = 32'hDEAD_BEEF; rfwen = 1; tick; rfwen = 0;
        #1;
        rfr0 = 5'd5; rfr1 = 5'd6;
        if (rfrd0 !== 32'hCAFE_0001 || rfrd1 !== 32'hBEEF_0002) begin
            errors = errors + 1; $display("FAIL rf read");
        end
        rfr0 = 5'd0;
        if (rfrd0 !== 32'h0) begin errors = errors + 1; $display("FAIL x0 not zero"); end
        // 复位测试
        rst_n = 0; #2; rst_n = 1; #1;
        rfr0 = 5'd5;
        if (rfrd0 !== 32'h0) begin errors = errors + 1; $display("FAIL rf rst"); end

        if (errors == 0)
            $display("P03: ALL TESTS PASSED");
        else
            $display("P03: %0d ERRORS", errors);
        $finish;
    end
endmodule
