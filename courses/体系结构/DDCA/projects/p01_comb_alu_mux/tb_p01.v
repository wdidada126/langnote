// p01/tb_p01.v —— p01 组合逻辑 testbench：真值表穷举 + 自动判定
// 对应讲义：notes/L02.md §1.2（组合逻辑验证 = 2^n 行全检）
//           notes/L04.md §1.3（TB 三件套：激励/检查/pass-fail 判定）
// 运行：见 build.sh / build.bat（需要安装 iverilog）

`timescale 1ns/1ps

module tb_p01;
    integer errors = 0;

    // ---- mux2 / mux4 ----
    reg  [7:0] d0, d1;
    reg        s;
    wire [7:0] y2;
    mux2 #(.W(8)) u_mux2 (.d0(d0), .d1(d1), .s(s), .y(y2));

    reg [3:0][7:0] dd;
    reg [1:0] sel2;
    wire [7:0] y4;
    mux4 #(.W(8)) u_mux4 (.d0(dd[0]), .d1(dd[1]), .d2(dd[2]), .d3(dd[3]),
                          .sel(sel2), .y(y4));

    // ---- decoder ----
    reg  [1:0] addr;
    reg        en;
    wire [3:0] sel;
    decoder2to4 u_dec (.addr(addr), .en(en), .sel(sel));

    // ---- ALU ----
    reg  [3:0] aa, bb;
    reg  [2:0] f;
    wire [3:0] yy;
    wire       zz;
    alu4 u_alu (.a(aa), .b(bb), .funct(f), .y(yy), .zero(zz));

    reg [3:0] exp;

    initial begin
        // 1) mux2：8 位数据抽样 + 双选择值
        d0 = 8'hA5; d1 = 8'h3C;
        for (s = 0; s <= 1; s = s + 1) begin
            #1;
            if (y2 !== (s ? d1 : d0)) begin
                errors = errors + 1;
                $display("FAIL mux2 s=%b y=%h", s, y2);
            end
        end

        // 2) mux4：4 个选择值
        dd[0] = 8'h11; dd[1] = 8'h22; dd[2] = 8'h33; dd[3] = 8'h44;
        for (sel2 = 0; sel2 <= 3; sel2 = sel2 + 1) begin
            #1;
            if (y4 !== dd[sel2]) begin
                errors = errors + 1;
                $display("FAIL mux4 sel=%b y=%h exp=%h", sel2, y4, dd[sel2]);
            end
        end

        // 3) decoder：4 地址 × 2 使能 = 8 向量穷举
        for (en = 0; en <= 1; en = en + 1)
            for (addr = 0; addr <= 3; addr = addr + 1) begin
                #1;
                if (sel !== (en ? (4'b1 << addr) : 4'b0)) begin
                    errors = errors + 1;
                    $display("FAIL dec addr=%b en=%b sel=%b", addr, en, sel);
                end
            end

        // 4) ALU：穷举 16×16×8 = 2048 向量，对照行为级期望
        for (f = 0; f <= 7; f = f + 1)
            for (aa = 0; aa <= 15; aa = aa + 1)
                for (bb = 0; bb <= 15; bb = bb + 1) begin
                    #0.1;
                    case (f)
                        3'b000:  exp = aa + bb;
                        3'b001:  exp = aa - bb;
                        3'b010:  exp = aa & bb;
                        3'b011:  exp = aa | bb;
                        3'b100:  exp = aa ^ bb;
                        3'b101:  exp = (bb >= 4) ? 4'b0 : (aa << bb);
                        3'b110:  exp = (bb >= 4) ? 4'b0 : (aa >> bb);
                        3'b111:  exp = {3'b0, (aa < bb)};
                        default: exp = 4'b0;
                    endcase
                    if (yy !== exp) begin
                        errors = errors + 1;
                        $display("FAIL alu f=%b a=%h b=%h y=%h exp=%h", f, aa, bb, yy, exp);
                    end
                    if (zz !== (exp == 4'b0)) errors = errors + 1;
                end

        if (errors == 0)
            $display("P01: ALL TESTS PASSED");
        else
            $display("P01: %0d ERRORS", errors);
        $finish;
    end
endmodule
