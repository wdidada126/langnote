// p04/tb_p04.v —— 序列检测器 + 交通灯 testbench
// 期望输出：P04: ALL TESTS PASSED
// 运行：./build.sh 或 build.bat（需 iverilog）

`timescale 1ns/1ps

module tb_p04;
    integer errors = 0;
    integer i, n;
    reg clk = 0;
    reg rst_n;
    always #5 clk = ~clk;

    // ---------- 序列检测器 ----------
    reg  din;
    wire hit;
    seq_detect_1011 u_seq (.clk(clk), .rst_n(rst_n), .din(din), .hit(hit));

    // ---------- 交通灯 ----------
    reg  tick;
    reg  walk;
    wire red, yel, grn;
    traffic_light #(.T_G(3'd5), .T_Y(3'd2), .T_R(3'd6)) u_tl (
        .clk(clk), .rst_n(rst_n), .tick(tick), .walk_req(walk),
        .red(red), .yellow(yel), .green(grn));

    task one_second;      // 给交通灯一拍 tick；对 seq 不驱动 din
        begin
            @(negedge clk); tick = 1'b1;
            @(negedge clk); tick = 1'b0;
        end
    endtask

    initial begin
        rst_n = 0; din = 0; tick = 0; walk = 0;
        @(negedge clk); rst_n = 1;

        // ================= 1) 序列检测器 =================
        // 流:   1 0 1 1 0 1 1 0 0 1 0 1 1
        // hit:  0 0 0 1 0 0 1 0 0 0 0 0 1   (重叠式：第 3、6、12 拍)
        begin : seq_test
            // Verilog-2005：块内声明不允许带初始化，先声明再顺序赋值
            reg [12:0] bits;
            reg [12:0] expct;
            bits  = 13'b1011011001011;                   // bit12 先发
            expct = 13'b0001001000001;
            for (n = 0; n < 13; n = n + 1) begin
                @(negedge clk);
                din = bits[12-n];      // 负沿送数：本拍 Mealy 输出由(旧状态,新输入)决定
                #1;
                if (hit !== expct[12-n]) begin
                    errors = errors + 1;
                    $display("FAIL seq t=%0d din=%b hit=%b exp=%b", n, din, hit, expct[12-n]);
                end
            end
        end
        din = 0;

        // ================= 2) 交通灯：完整周期（无请求）=================
        // 上电红 6s → 绿 5s → 黄 2s → 红 6s
        walk = 0;
        for (i = 0; i < 6; i = i + 1) begin
            if (red !== 1'b1 || grn || yel) begin
                errors = errors + 1; $display("FAIL tl red@%0d r=%b g=%b y=%b", i, red, grn, yel);
            end
            one_second;
        end
        for (i = 0; i < 5; i = i + 1) begin
            if (grn !== 1'b1 || red || yel) begin
                errors = errors + 1; $display("FAIL tl green@%0d", i);
            end
            one_second;
        end
        for (i = 0; i < 2; i = i + 1) begin
            if (yel !== 1'b1 || red || grn) begin
                errors = errors + 1; $display("FAIL tl yel@%0d", i);
            end
            one_second;
        end
        if (red !== 1'b1) begin errors = errors + 1; $display("FAIL tl back2red"); end

        // ================= 3) 行人请求：红灯提前放行 =================
        // 当前红灯 cnt=0。置 walk=1，最早第 3 拍放行（cnt>=2），不得晚于第 6 拍。
        walk = 1; n = 0;
        while (!grn && n < 10) begin one_second; n = n + 1; end
        if (!grn) begin errors = errors + 1; $display("FAIL walk never green"); end
        if (n < 3 || n > 6) begin errors = errors + 1; $display("FAIL walk early n=%0d", n); end
        walk = 0;

        // 放行后照常：绿 5 拍 → 黄 2 拍 → 红（转入绿的那拍未计绿时长，需完整 5 拍）
        for (i = 0; i < 5; i = i + 1) begin
            if (!grn) begin errors = errors + 1; $display("FAIL walk grn@%0d", i); end
            one_second;
        end
        for (i = 0; i < 2; i = i + 1) begin
            if (!yel) begin errors = errors + 1; $display("FAIL walk yel@%0d", i); end
            one_second;
        end
        if (!red) begin errors = errors + 1; $display("FAIL walk red phase"); end

        if (errors == 0)
            $display("P04: ALL TESTS PASSED");
        else
            $display("P04: %0d ERRORS", errors);
        $finish;
    end
endmodule
