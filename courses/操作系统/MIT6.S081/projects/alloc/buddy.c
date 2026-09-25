/* buddy.c — 伙伴系统分配器（对应 L19：Linux mm/page_alloc.c 的最小模型）
 * 规则：size → order = ceil(log2(size/unit))；大伙伴劈半（split），
 * 释放时若同 order 伙伴空闲则合并（merge）。
 * 外碎片≈0，代价是 2 的幂凑整带来的内部碎片（平均 ~25%）。 */
#include <stdlib.h>
#include <stdio.h>
#include "alloc.h"

static int fls_order(long n) /* ceil(log2(n)) */
{
    int o = 0; long v = 1;
    while (v < n) { v <<= 1; o++; }
    return o;
}

int bd_init(Buddy *b, void *mem, size_t unit, int maxorder)
{
    long nb;
    if (maxorder < 1 || maxorder > BUDDY_MAXORDER) return -1;
    nb = 1L << maxorder;
    b->base = (unsigned char *)mem;
    b->unit = unit;
    b->maxorder = maxorder;
    b->nblocks = nb;
    b->order = (int *)malloc(sizeof(int) * (size_t)nb);
    b->inuse = (int *)malloc(sizeof(int) * (size_t)nb);
    b->free_next = (int *)malloc(sizeof(int) * (size_t)nb);
    b->free_prev = (int *)malloc(sizeof(int) * (size_t)nb);
    if (!b->order || !b->inuse || !b->free_next || !b->free_prev) return -1;
    { long i; for (i = 0; i < nb; i++) { b->order[i] = -1; b->inuse[i] = 0;
        b->free_next[i] = b->free_prev[i] = -1; } }
    { int o; for (o = 0; o <= maxorder; o++) b->free_head[o] = -1; }
    /* 整堆是一个 order=maxorder 的空闲块 */
    b->order[0] = maxorder;
    b->free_head[maxorder] = 0;
    b->pages_requested = b->pages_consumed = 0;
    b->n_alloc = b->n_free = b->n_fail = b->n_split = b->n_merge = 0;
    return 0;
}

void bd_destroy(Buddy *b)
{
    free(b->order); free(b->inuse); free(b->free_next); free(b->free_prev);
    b->order = 0;
}

static void list_add(Buddy *b, int o, int idx)
{
    b->free_prev[idx] = -1;
    b->free_next[idx] = b->free_head[o];
    if (b->free_head[o] >= 0) b->free_prev[b->free_head[o]] = idx;
    b->free_head[o] = idx;
}

static void list_del(Buddy *b, int o, int idx)
{
    if (b->free_prev[idx] >= 0) b->free_next[b->free_prev[idx]] = b->free_next[idx];
    else b->free_head[o] = b->free_next[idx];
    if (b->free_next[idx] >= 0) b->free_prev[b->free_next[idx]] = b->free_prev[idx];
    b->free_prev[idx] = b->free_next[idx] = -1;
}

int bd_free_units(Buddy *b, int order)
{
    int cnt = 0, i = b->free_head[order];
    while (i >= 0) { cnt++; i = b->free_next[i]; }
    return cnt;
}

void *bd_alloc(Buddy *b, size_t size)
{
    long need;
    int o, k, idx;
    if (size == 0) return 0;
    need = (long)((size + b->unit - 1) / b->unit);
    o = fls_order(need);
    k = o;
    while (k <= b->maxorder && b->free_head[k] < 0) k++;
    if (k > b->maxorder) { b->n_fail++; return 0; }
    /* 从 order k 一路劈到 order o */
    while (k > o) {
        idx = b->free_head[k];
        list_del(b, k, idx);
        b->order[idx] = k - 1;
        b->order[idx + (1 << (k - 1))] = k - 1; /* 后半块空闲 */
        list_add(b, k - 1, idx + (1 << (k - 1)));
        list_add(b, k - 1, idx);
        b->n_split++;
        k--;
    }
    idx = b->free_head[o];
    list_del(b, o, idx);
    b->inuse[idx] = 1;
    b->order[idx] = o;
    b->n_alloc++;
    b->pages_requested += need;
    b->pages_consumed += 1L << o;
    return b->base + (size_t)idx * b->unit;
}

void bd_free(Buddy *b, void *p)
{
    size_t off = (unsigned char *)p - b->base;
    int idx = (int)(off / b->unit);
    int o;
    if (off % b->unit || idx < 0 || idx >= b->nblocks || !b->inuse[idx]) {
        printf("buddy: bad free %p\n", p); return;
    }
    o = b->order[idx];
    b->inuse[idx] = 0;
    while (o < b->maxorder) {
        int buddy = idx ^ (1 << o);
        if (buddy >= b->nblocks || b->inuse[buddy] || b->order[buddy] != o ||
            b->free_head[o] < 0) break;
        /* 伙伴必须在空闲链上才能合并 */
        { int i = b->free_head[o], found = 0;
          while (i >= 0) { if (i == buddy) { found = 1; break; } i = b->free_next[i]; }
          if (!found) break;
          list_del(b, o, buddy); }
        idx = idx & ~(int)((1u << (o + 1)) - 1); /* 合并后块的起始 */
        b->order[idx] = o + 1;
        o++;
        b->n_merge++;
    }
    b->order[idx] = o;
    list_add(b, o, idx);
    b->n_free++;
}

void bd_report(Buddy *b, const char *tag)
{
    printf("[buddy %s] alloc=%ld free=%ld fail=%ld split=%ld merge=%ld "
           "internal-frag=%.1f%% (consumed %ld / requested %ld units)\n",
           tag, b->n_alloc, b->n_free, b->n_fail, b->n_split, b->n_merge,
           b->pages_requested ? 100.0 * (double)(b->pages_consumed - b->pages_requested)
                              / (double)b->pages_consumed : 0.0,
           b->pages_consumed, b->pages_requested);
}
