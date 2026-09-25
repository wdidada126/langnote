// p02/tb_p02.v —— 加法器 testbench：RCA vs CLA 对照 + 穷举校验
// 期望输出：P02: ALL TESTS PASSED
// 运行：./build.sh 或 build.bat（需 iverilog）

`timescale 1ns/1ps

module tb_p02;
    integer errors = 0;
    integer i, j, k;
    reg  [3:0] a4, b4;
    reg        cin;
    wire [3:0] s_rca, s_cla;
    wire       co_rca, co_cla;
    reg  [4:0] exp5;

    rca  #(.N(4)) u_rca (.a(a4), .b(b4), .cin(cin), .s(s_rca), .cout(co_rca));
    cla4          u_cla (.a(a4), .b(b4), .cin(cin), .s(s_cla), .cout(co_cla));

    // 8 位 RCA 抽查（对照行为级 a+b+cin）
    reg  [7:0] a8, b8;
    reg        cin8;
    wire [7:0] s8;
    wire       co8;
    reg  [8:0] exp8;
    rca #(.N(8)) u_rca8 (.a(a8), .b(b8), .cin(cin8), .s(s8), .cout(co8));

    initial begin
        // 1) 4 位：穷举 16*16*2 = 512 向量，两个 DUT 同时比对期望
        for (i = 0; i < 16; i = i + 1)
            for (j = 0; j < 16; j = j + 1)
                for (k = 0; k < 2; k = k + 1) begin
                    a4 = i[3:0]; b4 = j[3:0]; cin = k[0];
                    #0.1;
                    exp5   = {1'b0, a4} + {1'b0, b4} + {1'b0, cin};
                    if ({co_rca, s_rca} !== exp5[4:0]) begin
                        errors = errors + 1;
                        $display("FAIL rca a=%h b=%h ci=%b got=%b exp=%b",
                                 a4, b4, cin, {co_rca, s_rca}, exp5);
                    end
                    if ({co_cla, s_cla} !== exp5[4:0]) begin
                        errors = errors + 1;
                        $display("FAIL cla a=%h b=%h ci=%b got=%b exp=%b",
                                 a4, b4, cin, {co_cla, s_cla}, exp5);
                    end
                    if (s_rca !== s_cla || co_rca !== co_cla) begin
                        errors = errors + 1;
                        $display("FAIL rca!=cla a=%h b=%h", a4, b4);
                    end
                end

        // 2) 8 位：随机 200 向量抽查
        for (i = 0; i < 200; i = i + 1) begin
            a8 = $random; b8 = $random; cin8 = $random;
            #0.1;
            exp8 = {1'b0, a8} + {1'b0, b8} + cin8;
            if ({co8, s8} !== exp8) begin
                errors = errors + 1;
                $display("FAIL rca8 a=%h b=%h ci=%b", a8, b8, cin8);
            end
        end

        if (errors == 0)
            $display("P02: ALL TESTS PASSED");
        else
            $display("P02: %0d ERRORS", errors);
        $finish;
    end
endmodule
