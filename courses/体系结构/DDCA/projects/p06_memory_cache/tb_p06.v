// p06/tb_p06.v —— 2 路组相联 cache 模型 testbench：冲突缺失/LRU/写直达 可观测
// 期望输出：P06: ALL TESTS PASSED
// 主存初始化性质：backing[w]=w*4 ⇒ 字地址 a（未写前）读出值 == a，方便对拍。

`timescale 1ns/1ps

module tb_p06;
    integer errors = 0;
    reg clk = 0, rst_n;
    always #5 clk = ~clk;

    reg        req, we;
    reg  [7:0] addr;
    reg  [31:0] wdata;
    wire [31:0] rdata;
    wire       hit;
    wire [15:0] hit_cnt, miss_cnt;

    cache #(.AW(8), .OFFW(1), .IDXW(2), .WAYS(2)) dut (
        .clk(clk), .rst_n(rst_n), .req(req), .we(we),
        .addr(addr), .wdata(wdata), .rdata(rdata),
        .hit(hit), .hit_cnt(hit_cnt), .miss_cnt(miss_cnt));

    reg [31:0] rdata_obs;

    // 一次访问：负沿驱动 → 正沿前采样 hit/数据 → 下个负沿撤销
    task access(input [7:0] a, input w, input [31:0] wd,
                input exp_hit, input [31:0] exp_data, input chk_data);
        begin
            @(negedge clk);
            addr = a; req = 1; we = w; wdata = wd;
            #4;
            if (hit !== exp_hit) begin
                errors = errors + 1;
                $display("FAIL @%h hit=%b exp=%b", a, hit, exp_hit);
            end
            rdata_obs = rdata;
            @(negedge clk);
            req = 0; we = 0;
            if (chk_data && rdata_obs !== exp_data) begin
                errors = errors + 1;
                $display("FAIL @%h data=%0d exp=%0d", a, rdata_obs, exp_data);
            end
        end
    endtask

    initial begin
        rst_n = 0; req = 0; we = 0; addr = 0; wdata = 0;
        repeat (2) @(negedge clk);
        rst_n = 1;

        // ---- set 0 上的 2 路 LRU 剧情（tag 互不相同，全落 set 0）----
        // 0x00 M | 0x20 M | 0x00 H | 0x20 H | 0x40 M(逐出LRU=0x00) | 0x20 H | 0x00 M
        access(8'h00, 1'b0, 32'h0, 1'b0, 32'h00, 1);
        access(8'h20, 1'b0, 32'h0, 1'b0, 32'h20, 1);
        access(8'h00, 1'b0, 32'h0, 1'b1, 32'h00, 1);
        access(8'h20, 1'b0, 32'h0, 1'b1, 32'h20, 1);
        access(8'h40, 1'b0, 32'h0, 1'b0, 32'h40, 1);
        access(8'h20, 1'b0, 32'h0, 1'b1, 32'h20, 1);
        access(8'h00, 1'b0, 32'h0, 1'b0, 32'h00, 1);

        if (hit_cnt !== 16'd3 || miss_cnt !== 16'd4) begin
            errors = errors + 1;
            $display("FAIL counters h=%0d m=%0d exp 3/4", hit_cnt, miss_cnt);
        end

        // ---- 不同 set（0x08 → set1）与 set0 无冲突 ----
        access(8'h08, 1'b0, 32'h0, 1'b0, 32'h08, 1);   // set1 首次：miss
        access(8'h08, 1'b0, 32'h0, 1'b1, 32'h08, 1);   // 再访问：hit

        // ---- 写直达 + 写分配：写 0x84=1234，回读 hit 且值正确 ----
        access(8'h84, 1'b1, 32'd1234, 1'b0, 32'h0, 0); // miss（分配并写）
        access(8'h84, 1'b0, 32'h0,    1'b1, 32'd1234, 1);

        if (hit_cnt !== 16'd5 || miss_cnt !== 16'd6) begin
            errors = errors + 1;
            $display("FAIL final counters h=%0d m=%0d exp 5/6", hit_cnt, miss_cnt);
        end
        // 主存应已收到写（write-through 证据）
        if (dut.backing[8'h84 >> 2] !== 32'd1234) begin
            errors = errors + 1; $display("FAIL backing not updated");
        end

        if (errors == 0)
            $display("P06: ALL TESTS PASSED");
        else
            $display("P06: %0d ERRORS", errors);
        $finish;
    end
endmodule
