/* alloc.h — 迷你内核分配器公共接口（对应 6.1810 L04/L19）
 * 宿主可移植 C：不依赖 OS 线程，只在静态堆数组上模拟 first-fit 与 buddy。 */
#ifndef MINIALLOC_H
#define MINIALLOC_H

#include <stddef.h>

/* ---------- first-fit：块头 + 按地址有序的空闲链，含伙伴合并 ---------- */
typedef struct FBHeader {
    size_t size;            /* 数据区大小（含头对齐后的可用字节） */
    int    used;
    struct FBHeader *next;  /* 按地址有序串联全部块 */
} FBHeader;

typedef struct FirstFit {
    unsigned char *base;
    size_t cap;
    FBHeader *head;
    /* 统计 */
    long n_alloc, n_free, n_fail;
    long long search_steps;  /* first-fit 查找走过的块数：碎片代价的度量 */
} FirstFit;

int   ff_init(FirstFit *a, void *mem, size_t cap);
void *ff_alloc(FirstFit *a, size_t size);
void  ff_free(FirstFit *a, void *p);
size_t ff_largest_free(FirstFit *a);
void  ff_report(FirstFit *a, const char *tag);

/* ---------- buddy：内核帧分配器（Linux page_alloc 的最小模型） ----------
 * 最小粒度 unit；总容量必须恰好为 unit << maxorder。 */
#define BUDDY_MAXORDER 14

typedef struct Buddy {
    unsigned char *base;
    size_t unit;
    int    maxorder;
    long   nblocks;          /* unit 块总数 = 1L << maxorder */
    int   *order;            /* 每 unit 块起始处的 order 标记（-1 未定） */
    int   *inuse;            /* 1 = 已分配 */
    int    free_head[BUDDY_MAXORDER + 1]; /* 每 order 一条空闲链（索引表） */
    int   *free_next, *free_prev;         /* 空闲链节点数组（按块索引） */
    long   pages_requested;               /* 请求字节折算 unit 总数 */
    long   pages_consumed;                /* 实际上盘 unit 总数（含凑整） */
} Buddy;

int   bd_init(Buddy *b, void *mem, size_t unit, int maxorder);
void  bd_destroy(Buddy *b);
void *bd_alloc(Buddy *b, size_t size);          /* 向上取整到 2^k * unit */
void  bd_free(Buddy *b, void *p);
int   bd_free_units(Buddy *b, int order);        /* 该 order 空闲块数（碎片实验用） */
void  bd_report(Buddy *b, const char *tag);

#endif /* MINIALLOC_H */
