/*
 * p06/cache_sim.c —— 缓存映射模拟器（C 辅助，对应 notes/L13.md）
 *
 * 编译（需要 gcc，iverilog 只跑 Verilog 部分）：
 *   gcc -O2 -o cache_sim cache_sim.c        Windows: gcc 同理（MinGW-w64），或 cc
 *   ./cache_sim
 *
 * 模拟三种配置（同一 4KB 地址空间、块大小可变）：
 *   直接映射 E=1 / 2 路组相联 / 4 路组相联（LRU）
 * trace 三种：顺序扫描(stride=4B) / 大步长(stride=组数×块长，制造冲突) / 随机。
 * 输出命中率矩阵——亲手复现 L13 §1.2 的"冲突失效"与 §1.5 的 AMAT 账。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CACHE_BYTES   256      /* 数据容量：256B，8 个字/块的倍数便于演示 */
#define WORD_BYTES    4

typedef struct {
    int n_sets, ways, line_words;
    int valid[64][8];
    unsigned tag[64][8];
    int lru_age[64][8];        /* 越大越久未用（LRU 时间戳） */
    long hits, misses;
} Cache;

static void cache_init(Cache *c, int ways, int line_words)
{
    c->ways = ways;
    c->line_words = line_words;
    c->n_sets = (CACHE_BYTES / WORD_BYTES) / (ways * line_words);
    memset(c->valid, 0, sizeof c->valid);
    c->hits = c->misses = 0;
}

static int cache_access(Cache *c, unsigned byte_addr, int write)
{
    unsigned wa = byte_addr / WORD_BYTES;
    int line_word = wa % c->line_words;
    int set  = (wa / c->line_words) % c->n_sets;
    unsigned tag = wa / ((unsigned)c->line_words * c->n_sets);
    int w;
    (void)line_word; (void)write;

    for (w = 0; w < c->ways; w++) {
        if (c->valid[set][w] && c->tag[set][w] == tag) {
            c->hits++;
            c->lru_age[set][w] = 0;
            return 1;
        }
    }
    c->misses++;
    /* LRU victim */
    int victim = 0, oldest = -1;
    for (w = 0; w < c->ways; w++) {
        if (!c->valid[set][w]) { victim = w; oldest = 1 << 30; break; }
        if (c->lru_age[set][w] > oldest) { oldest = c->lru_age[set][w]; victim = w; }
    }
    c->valid[set][victim] = 1;
    c->tag[set][victim] = tag;
    c->lru_age[set][victim] = 0;
    for (w = 0; w < c->ways; w++) if (w != victim || !oldest) c->lru_age[set][w]++;
    return 0;
}

static void run_trace(const char *name, Cache *c, const unsigned *trace, int n)
{
    for (int i = 0; i < n; i++) cache_access(c, trace[i], 0);
    printf("  %-12s E=%d: 命中率 %5.1f%%  (%ld hits / %ld)\n",
           name, c->ways, 100.0 * c->hits / (c->hits + c->misses),
           c->hits, c->hits + c->misses);
}

int main(void)
{
    enum { N = 4096 };
    static unsigned t_seq[N], t_stride[N], t_rand[N];

    for (int i = 0; i < N; i++) {
        t_seq[i]     = (unsigned)(i % (CACHE_BYTES / WORD_BYTES)) * WORD_BYTES;   /* 顺序循环 */
        t_stride[i]  = (unsigned)(((i * 8) % (CACHE_BYTES / WORD_BYTES)) * WORD_BYTES); /* 步长 8 字=32B：直接映射颠簸配置 */
        t_rand[i]    = (unsigned)(rand() % (CACHE_BYTES / WORD_BYTES)) * WORD_BYTES;
    }

    printf("== 256B 数据容量、块=2字(8B)：冲突缺失的对照实验 ==\n");
    struct { int ways; const char *nm; } cfg[] = {{1, "直接映射"}, {2, "2路LRU"}, {4, "4路LRU"}};
    for (unsigned ci = 0; ci < sizeof cfg / sizeof cfg[0]; ci++) {
        Cache c;
        cache_init(&c, cfg[ci].ways, 2);
        run_trace("顺序 stride=4B", &c, t_seq, N);
        cache_init(&c, cfg[ci].ways, 2);
        run_trace("大步长 stride=32B", &c, t_stride, N);
        cache_init(&c, cfg[ci].ways, 2);
        run_trace("随机", &c, t_rand, N);
        printf("----\n");
    }
    printf("观察：步长=组数×块长时直接映射命中率暴跌，组相联靠多 way 吸收冲突。\n");
    printf("延伸：改 line_words 复现“块变大→空间局部性↑但缺失代价↑”的曲线（L13 §1.5）。\n");
    return 0;
}
