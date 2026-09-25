/* main.c — first-fit vs buddy 正确性 / 碎片 / 性能三重演示（L04/L19）
 * 1) 确定性伪随机混合负载 + 存活区间互不重叠校验（写标记、回读校验）；
 * 2) 交错释放制造空洞：first-fit 外碎片 vs buddy 内碎片的量化对比；
 * 3) clock() 计时吞吐对比。只写不编译交付；build.sh/build.bat 已备。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "alloc.h"

#define HEAP_BYTES (1u << 20)          /* 1 MiB 静态堆 */
static unsigned char heap_firstfit[HEAP_BYTES];
static unsigned char heap_buddy[HEAP_BYTES];

/* 简单 LCG：跨平台、可复现 */
static unsigned int seed = 12345u;
static unsigned int rnd(void) { seed = seed * 1103515245u + 12345u; return seed >> 8; }

#define MAXLIVE 512
typedef struct { void *p; size_t n; unsigned int tag; } Live;
static Live live[MAXLIVE];
static char overlap_flag;

static void note_live(int slot, void *p, size_t n, unsigned int tag)
{ live[slot].p = p; live[slot].n = n; live[slot].tag = tag; }

/* 填充可校验的图案 */
static void stamp(unsigned char *p, size_t n, unsigned int tag)
{ size_t i; for (i = 0; i < n; i++) p[i] = (unsigned char)(tag + i); }

static int verify(unsigned char *p, size_t n, unsigned int tag)
{ size_t i; for (i = 0; i < n; i++) if (p[i] != (unsigned char)(tag + i)) return 0; return 1; }

static int overlaps(int slot, void *p, size_t n)
{
    int i;
    unsigned char *a = (unsigned char *)p, *b = a + n;
    for (i = 0; i < MAXLIVE; i++) {
        if (!live[i].p) continue;
        if (a < (unsigned char *)live[i].p + live[i].n &&
            (unsigned char *)live[i].p < b) return 1;
    }
    return 0;
}

typedef struct { const char *name;
    int (*init)(void); void *(*alloc)(size_t); void (*free_)(void *);
    void (*report)(const char *); } Alloc;

static FirstFit FF; static Buddy BD; static int use_buddy;

static void *ffa(size_t n) { return ff_alloc(&FF, n); }
static void  fff(void *p)   { ff_free(&FF, p); }
static void  ffr(const char *t) { ff_report(&FF, t); }
static void *bda(size_t n) { return bd_alloc(&BD, n); }
static void  bdf(void *p)  { bd_free(&BD, p); }
static void  bdr(const char *t) { bd_report(&BD, t); }
static int inits(void) { use_buddy = 0; return ff_init(&FF, heap_firstfit, HEAP_BYTES); }
static int initb(void) { use_buddy = 1; return bd_init(&BD, heap_buddy, 64, 14); }

static void run_workload(const char *tag)
{
    Alloc A; int i; seed = 999u;
    memset(live, 0, sizeof live);
    A.name = use_buddy ? "buddy" : "firstfit";
    A.alloc = use_buddy ? bda : ffa;
    A.free_ = use_buddy ? bdf : fff;
    (void)A.name; (void)tag;
    for (i = 0; i < 60000; i++) {
        unsigned int r = rnd();
        if (r & 1) { /* 50% 分配：挑一个空闲槽位 */
            size_t n = 8 + (r % 500);
            int slot = (int)(r % MAXLIVE);
            if (live[slot].p == 0) {
                void *p = A.alloc(n);
                if (p) {
                    if (overlaps(slot, p, n)) { overlap_flag = 1; printf("OVERLAP BUG!\n"); }
                    note_live(slot, p, n, r);
                    stamp((unsigned char *)p, n > 64 ? 64 : n, r); /* 只标前 64B */
                }
            }
        } else {
            int slot = (int)(r % MAXLIVE);
            if (live[slot].p) {
                unsigned int tag = live[slot].tag; size_t n = live[slot].n;
                void *p = live[slot].p;
                if (!verify((unsigned char *)p, n > 64 ? 64 : n, tag)) {
                    overlap_flag = 1; printf("CORRUPTION at %p\n", p);
                }
                live[slot].p = 0;
                A.free_(p);
            }
        }
    }
    /* 收尾释放全部存活块 */
    for (i = 0; i < MAXLIVE; i++)
        if (live[i].p) { A.free_(live[i].p); live[i].p = 0; }
    if (use_buddy) bdr(tag); else ffr(tag);
    printf("  overlap/corruption seen: %s\n\n", overlap_flag ? "YES" : "no");
}

static void frag_demo(void)
{
    void *keep[64], *tmp;
    size_t small = 64 * 1024 / 64; /* 每块 1KB（buddy 正好一个 order-4 块） */
    int i;
    puts("== 碎片实验：分配 64 块 1KB，释放偶数号，再申请大块 ==");
    use_buddy = 0; ff_init(&FF, heap_firstfit, HEAP_BYTES);
    use_buddy = 1; bd_init(&BD, heap_buddy, 64, 14);
    for (i = 0; i < 64; i++) { keep[i] = ff_alloc(&FF, small); }
    for (i = 0; i < 64; i += 2) ff_free(&FF, keep[i]);
    tmp = ff_alloc(&FF, 32 * 1024);
    printf("firstfit: largest-free=%zuB, alloc 32KB %s（棋盘空洞=外碎片）\n",
           ff_largest_free(&FF), tmp ? "OK" : "FAIL");
    if (tmp) ff_free(&FF, tmp);
    for (i = 0; i < 64; i++) { keep[i] = bd_alloc(&BD, small); }
    for (i = 0; i < 64; i += 2) bd_free(&BD, keep[i]);
    tmp = bd_alloc(&BD, 32 * 1024);
    printf("buddy  : alloc 32KB %s（交错占用同样阻断合并——这正是 slab 按对象分桶的动机）\n",
           tmp ? "OK" : "FAIL");
    if (tmp) bd_free(&BD, tmp);
    for (i = 1; i < 64; i += 2) bd_free(&BD, keep[i]); /* 全清：伙伴一路合并 */
    tmp = bd_alloc(&BD, 32 * 1024);
    printf("buddy  : 全部释放后 alloc 32KB %s（order 一路 merge 回升，外碎片可自愈）\n",
           tmp ? "OK" : "FAIL");
    if (tmp) bd_free(&BD, tmp);
    bd_report(&BD, "after-frag");
    puts("");
}

static void bench(void)
{
    clock_t t0; long i; seed = 7u;
    puts("== 吞吐基准（100k 次 alloc，size 8..1000B 随机，立即 free） ==");
    ff_init(&FF, heap_firstfit, HEAP_BYTES);
    t0 = clock();
    for (i = 0; i < 100000; i++) { void *p = ff_alloc(&FF, 8 + rnd() % 993); if (p) ff_free(&FF, p); }
    printf("firstfit: %.3f s (avg search steps=%.1f)\n", (double)(clock() - t0) / CLOCKS_PER_SEC,
           (double)FF.search_steps / (double)(FF.n_alloc + 1));
    bd_init(&BD, heap_buddy, 64, 14);
    t0 = clock();
    for (i = 0; i < 100000; i++) { void *p = bd_alloc(&BD, 8 + rnd() % 993); if (p) bd_free(&BD, p); }
    printf("buddy   : %.3f s\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    bd_report(&BD, "bench");
}

int main(void)
{
    puts("alloc demo — 6.1810 L04/L19: first-fit vs buddy");
    if (inits() == 0) run_workload("mixed workload");
    if (initb() == 0) run_workload("mixed workload");
    frag_demo();
    bench();
    puts("done.");
    return 0;
}
