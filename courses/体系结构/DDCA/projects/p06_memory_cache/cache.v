// p06/cache.v —— 2 路组相联读/写直达 cache 行为模型（含缺失统计）
// 对应讲义：notes/L13.md §1.2 地址三段论（tag | set | block offset）、§1.3 LRU、§1.4 写策略
// 默认参数 AW=8, OFFW=1, IDXW=2 ⇒ 字地址 6 位 = tag(3) + set(2) + 块内字(1)。
// 命中 = 组内各路 tag 并行比较 OR（CAM 思想，L13 §1.2）；数据输出 = way Mux（L03）。
// 教学简化：单拍命中/缺失（真机缺失要总线等待状态，见 L10 §1.4/L13 的 stall）。

`default_nettype none

module cache #(
    parameter AW   = 8,               // 字节地址宽
    parameter OFFW = 1,               // 块内字偏移位数（log2(每块字数)）
    parameter IDXW = 2,               // 组号位数
    parameter WAYS = 2                // 本模型固定 2 路（改 1 即直接映射做对照）
) (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         req,
    input  wire         we,
    input  wire [AW-1:0] addr,
    input  wire [31:0]  wdata,
    output wire [31:0]  rdata,
    output wire         hit,
    output reg  [15:0]  hit_cnt,
    output reg  [15:0]  miss_cnt
);
    localparam TAGW  = AW - OFFW - IDXW - 2;         // tag 位数（字节地址低 2 位不参与划分）
    localparam LINES = (1 << OFFW);
    localparam SETS  = (1 << IDXW);
    localparam WORDS = SETS * WAYS * LINES;         // cache 总字数
    localparam BWORDS = (1 << (AW - 2));            // 主存字数

    // ----- 地址划分（L13 §1.2）-----
    wire [IDXW-1:0]  set_i = addr[OFFW+IDXW+1:OFFW+2];
    wire [OFFW-1:0]  line_w = addr[OFFW+1:2];
    wire [AW-OFFW-IDXW-3:0] tag_i = addr[AW-1:OFFW+IDXW+2];

    // ----- 存储体（平坦索引 = {set,way,line_word}）-----
    reg [31:0] data_arr  [0:WORDS-1];
    reg [31:0] backing   [0:BWORDS-1];               // 模拟主存（读缺时填行）
    reg        valid     [0:SETS*WAYS-1];
    reg [27:0] tags      [0:SETS*WAYS-1];            // tag 用固定宽度存，简化声明
    reg        lru       [0:SETS-1];                 // 2 路：victim 指针

    integer w;
    initial begin
        for (w = 0; w < SETS*WAYS; w = w + 1) begin
            valid[w] = 1'b0; tags[w] = 28'h0;
        end
        for (w = 0; w < SETS; w = w + 1)   lru[w]   = 1'b0;
        for (w = 0; w < WORDS; w = w + 1)  data_arr[w] = 32'h0;
        for (w = 0; w < BWORDS; w = w + 1) backing[w]  = w * 32'd4;   // 可预测数据：mem[wa]=4*wa
    end

    // ----- 命中判定：组内并行 tag 比较（CAM 思想，L13 §1.2/§1.3）-----
    wire [WAYS-1:0] way_hit;
    genvar g;
    generate
        for (g = 0; g < WAYS; g = g + 1) begin : g_cmp
            assign way_hit[g] = valid[set_i*WAYS+g] &&
                                (tags[set_i*WAYS+g] == {{4{1'b0}}, tag_i});
        end
    endgenerate
    assign hit = req && (|way_hit);

    // ----- 读出 Mux（L03 的 Mux 第 N 次出场）-----
    reg [31:0] muxed;
    integer k;
    always @(*) begin
        muxed = 32'h0;
        for (k = 0; k < WAYS; k = k + 1)
            if (way_hit[k]) muxed = data_arr[(set_i*WAYS+k)*LINES + line_w];
        if (!hit) muxed = backing[{addr[AW-1:2]}];   // 缺失直读主存
    end
    assign rdata = muxed;

    // ----- 更新：写直达 + 缺失写分配 + LRU 推进 -----
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            hit_cnt  <= 16'd0;
            miss_cnt <= 16'd0;
        end else if (req) begin
            if (hit) begin
                hit_cnt <= hit_cnt + 16'd1;
                lru[set_i] <= way_hit[0] ? 1'b1 : 1'b0;          // 命中路设为最近
                if (we)
                    data_arr[(set_i*WAYS + (way_hit[0] ? 0 : 1))*LINES + line_w] <= wdata;
            end else begin
                miss_cnt <= miss_cnt + 16'd1;
                // victim = lru 指向的 way
                tags[set_i*WAYS + lru[set_i]]  <= {{4{1'b0}}, tag_i};
                valid[set_i*WAYS + lru[set_i]] <= 1'b1;
                // 整行填（block fill，空间局部性的来源）
                begin : fill
                    integer j; integer base;
                    base = (set_i*WAYS + lru[set_i]) * LINES;
                    for (j = 0; j < LINES; j = j + 1)
                        data_arr[base + j] <=
                            backing[{addr[AW-1:OFFW+2], {OFFW{1'b0}}} + j];
                end
                if (we) begin
                    // 写分配：刚填的块里也要写本字
                    data_arr[(set_i*WAYS + lru[set_i])*LINES + line_w] <= wdata;
                end
                lru[set_i] <= ~lru[set_i];
            end
            if (we) backing[addr[AW-1:2]] <= wdata;  // 写直达到主存
        end
    end
endmodule

`default_nettype wire
