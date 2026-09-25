// p05/riscv_single.v —— RV32I 子集单周期 CPU（本课全项目的"总装车间"）
// 对应讲义：notes/L08.md（ISA）、notes/L09.md（单周期 datapath/控制单元/指令周期）
//
// 支持指令（自定义扩展 halt = custom-0 编码，仅仿真用）：
//   lui/addi/andi/ori/xori/slli/srli
//   add/sub/and/or/xor/sll/srl/slt/sltu
//   lw/sw
//   beq/bne
//   jal
//   halt
// x0 硬连线 0；DMEM 基址 0x1000；PC 自 0 起。
// 结构就是 L09 §1.2 的图：PC→imem→译码→RF→ALU→dmem→写回 mux。

`default_nettype none

module riscv_single #(
    parameter IMEM_FILE  = "prog.mem",
    parameter IMEM_WORDS = 256,
    parameter DMEM_BASE  = 32'h0000_1000,
    parameter DMEM_WORDS = 64
) (
    input  wire clk,
    input  wire rst_n,
    output reg  halt
);
    // ================= 取指 =================
    reg  [31:0] pc;
    wire [31:0] instr;
    wire [31:0] next_pc;

    imem #(.FILE(IMEM_FILE), .WORDS(IMEM_WORDS)) u_imem (
        .addr(pc), .rdata(instr));

    // ================= 译码字段 =================
    wire [6:0] op  = instr[6:0];
    wire [2:0] f3  = instr[14:12];
    wire [6:0] f7  = instr[31:25];
    wire [4:0] rd  = instr[11:7];
    wire [4:0] rs1 = instr[19:15];
    wire [4:0] rs2 = instr[24:20];

    wire [31:0] immI = {{20{instr[31]}}, instr[31:20]};
    wire [31:0] immS = {{20{instr[31]}}, instr[11:7], instr[30:25]};
    wire [31:0] immB = {{19{instr[31]}}, instr[31], instr[7],
                        instr[30:25], instr[11:8], 1'b0};
    wire [31:0] immJ = {{11{instr[31]}}, instr[31], instr[19:12],
                        instr[20], instr[30:21], 1'b0};
    wire [31:0] immU = {instr[31:12], 12'b0};

    // ================= 控制信号（主译码器 = L09 §1.3 那张表）=================
    reg        reg_write, mem_read, mem_write, alu_src;
    reg [2:0]  imm_sel;     // 0=I 1=S 2=B 3=J 4=U 5=0
    reg [3:0]  alu_op;      // 见下方 ALU 编码
    reg [1:0]  wb_sel;      // 0=ALU 1=DMEM 2=PC+4
    reg        branch, jump;

    always @(*) begin
        reg_write = 1'b0; mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b0;
        imm_sel   = 3'd0; alu_op    = 4'd0; wb_sel = 2'd0;
        branch    = 1'b0; jump      = 1'b0;

        case (op)
            7'h37: begin // LUI：x0 + immU（rs1 字段为 0）
                reg_write = 1'b1; alu_src = 1'b1; imm_sel = 3'd4; alu_op = 4'd0;
            end
            7'h13: begin // OP-IMM
                reg_write = 1'b1; alu_src = 1'b1; imm_sel = 3'd0;
                case (f3)
                    3'b000: alu_op = 4'd0;              // addi
                    3'b111: alu_op = 4'd2;              // andi
                    3'b110: alu_op = 4'd3;              // ori
                    3'b100: alu_op = 4'd4;              // xori
                    3'b001: alu_op = 4'd5;              // slli
                    3'b101: alu_op = 4'd6;              // srli（srai 未实现：按 srl 处理，勿在程序中使用）
                    default: begin alu_op = 4'd0; reg_write = 1'b0; end
                endcase
            end
            7'h33: begin // OP-REG
                reg_write = 1'b1; imm_sel = 3'd5;
                case (f3)
                    3'b000: alu_op = f7[5] ? 4'd1 : 4'd0; // sub/add
                    3'b111: alu_op = 4'd2;                // and
                    3'b110: alu_op = 4'd3;                // or
                    3'b100: alu_op = 4'd4;                // xor
                    3'b001: alu_op = 4'd5;                // sll
                    3'b101: alu_op = 4'd6;                // srl（srai 未实现：勿使用）
                    3'b010: alu_op = 4'd7;                // slt
                    3'b011: alu_op = 4'd8;                // sltu
                    default: begin alu_op = 4'd0; reg_write = 1'b0; end
                endcase
            end
            7'h03: begin // LOAD lw
                reg_write = 1'b1; mem_read = 1'b1; alu_src = 1'b1;
                imm_sel = 3'd0; alu_op = 4'd0; wb_sel = 2'd1;
            end
            7'h23: begin // STORE sw
                mem_write = 1'b1; alu_src = 1'b1; imm_sel = 3'd1; alu_op = 4'd0;
            end
            7'h63: begin // BRANCH beq/bne
                branch = 1'b1; imm_sel = 3'd2; alu_op = 4'd0;
            end
            7'h6f: begin // JAL
                jump = 1'b1; reg_write = 1'b1; imm_sel = 3'd3; wb_sel = 2'd2;
            end
            7'h2f: begin // halt（custom-0，仿真专用）
                // 无副作用；halt 标志在时序块置位
            end
            default: ; // nop
        endcase
    end

    // ================= 寄存器堆（32×32，组合读/同步写，x0 恒零）=================
    reg [31:0] rf [0:31];
    integer    i;
    initial for (i = 0; i < 32; i = i + 1) rf[i] = 32'h0;

    wire [31:0] rdata1 = (rs1 == 5'd0) ? 32'h0 : rf[rs1];
    wire [31:0] rdata2 = (rs2 == 5'd0) ? 32'h0 : rf[rs2];

    wire [31:0] wb_data = (wb_sel == 2'd1) ? dm_rdata :
                          (wb_sel == 2'd2) ? (pc + 32'd4) : alu_result;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < 32; i = i + 1) rf[i] <= 32'h0;
        end else if (reg_write && (rd != 5'd0)) begin
            rf[rd] <= wb_data;
        end
    end

    // ================= ALU =================
    // 0 add 1 sub 2 and 3 or 4 xor 5 sll 6 srl 7 slt 8 sltu 15 直通b
    wire [31:0] imm = (imm_sel == 3'd0) ? immI :
                      (imm_sel == 3'd1) ? immS :
                      (imm_sel == 3'd2) ? immB :
                      (imm_sel == 3'd3) ? immJ :
                      (imm_sel == 3'd4) ? immU : 32'h0;

    wire [31:0] b_in = alu_src ? imm : rdata2;
    wire [31:0] alu_result;
    wire        alu_eq = (rdata1 == rdata2);   // beq/bne 用（不走 ALU 减法器，见 L09 §1.2）

    assign alu_result =
        (alu_op == 4'd0)  ? (rdata1 + b_in)   :
        (alu_op == 4'd1)  ? (rdata1 - b_in)   :
        (alu_op == 4'd2)  ? (rdata1 & b_in)   :
        (alu_op == 4'd3)  ? (rdata1 | b_in)   :
        (alu_op == 4'd4)  ? (rdata1 ^ b_in)   :
        (alu_op == 4'd5)  ? (rdata1 << b_in)  :
        (alu_op == 4'd6)  ? (rdata1 >> b_in)  :
        (alu_op == 4'd7)  ? {31'b0, $signed(rdata1) < $signed(b_in)}  :
        (alu_op == 4'd8)  ? {31'b0, rdata1 < b_in} :
        (alu_op == 4'd15) ? b_in : 32'h0;

    // ================= 访存 =================
    wire [31:0] dm_addr   = alu_result;          // lw/sw 的地址 = rs1+imm（ALU 复用）
    wire [31:0] dm_rdata;                        // dmem 组合读回（前向声明引用 OK）

    // ================= PC 更新 =================
    wire branch_taken = branch && ((f3 == 3'b000) ? alu_eq :
                                   (f3 == 3'b001) ? ~alu_eq : 1'b0);
    assign next_pc = jump         ? (pc + immJ) :
                     branch_taken ? (pc + immB) : (pc + 32'd4);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)     pc   <= 32'h0;
        else if (!halt) pc   <= next_pc;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) halt <= 1'b0;
        else if (op == 7'h2f && instr[6:0] == 7'h2f) halt <= 1'b1;
    end

    dmem #(.BASE(DMEM_BASE), .WORDS(DMEM_WORDS)) u_dmem (
        .clk(clk), .wen(mem_write), .addr(dm_addr),
        .wdata(rdata2), .rdata(dm_rdata));

endmodule

`default_nettype wire
