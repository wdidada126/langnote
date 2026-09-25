/* firstfit.c — first-fit 空闲链分配器（对应 L04 的 ulib.c malloc / L19）
 * 机制：每个块 = [头|数据]，全堆一条按地址有序的链表；
 * free 时与地址相邻的空闲块双向合并，控制外碎片。 */
#include <string.h>
#include <stdio.h>
#include "alloc.h"

#define FF_MIN    16u
#define FF_ALIGN  16u
#define roundup(x, a) (((size_t)(x) + (a) - 1) & ~((size_t)(a) - 1))
#define HSIZE     roundup(sizeof(FBHeader), FF_ALIGN)

static FBHeader *hdr(void *datap)
{
    return (FBHeader *)((unsigned char *)datap - HSIZE);
}

int ff_init(FirstFit *a, void *mem, size_t cap)
{
    FBHeader *h;
    if (cap < HSIZE * 4) return -1;
    cap = (cap / FF_ALIGN) * FF_ALIGN;
    a->base = (unsigned char *)mem;
    a->cap = cap;
    h = (FBHeader *)mem;
    h->size = cap;
    h->used = 0;
    h->next = 0;
    a->head = h;
    a->n_alloc = a->n_free = a->n_fail = 0;
    a->search_steps = 0;
    return 0;
}

void *ff_alloc(FirstFit *a, size_t size)
{
    FBHeader *h, *cand = 0;
    size_t need = roundup(size + FF_MIN, FF_ALIGN);
    for (h = a->head; h; h = h->next) {
        a->search_steps++;
        if (!h->used && h->size >= HSIZE + need) { cand = h; break; }
    }
    if (!cand) { a->n_fail++; return 0; }
    /* 足够大就劈出一个新空闲尾块 */
    if (cand->size >= HSIZE + need + HSIZE + FF_MIN) {
        FBHeader *tail = (FBHeader *)((unsigned char *)cand + need);
        tail->size = cand->size - need;
        tail->used = 0;
        tail->next = cand->next;
        cand->next = tail;
        cand->size = need;
    }
    cand->used = 1;
    a->n_alloc++;
    return (unsigned char *)cand + HSIZE;
}

void ff_free(FirstFit *a, void *p)
{
    FBHeader *h, *prev;
    if (!p) return;
    h = hdr(p);
    h->used = 0;
    /* 与后继合并 */
    if (h->next && !h->next->used) {
        h->size += h->next->size;
        h->next = h->next->next;
    }
    /* 与前驱合并（表短，线性找前驱即可） */
    prev = 0;
    for (h = a->head; h; prev = h, h = h->next)
        if (!h->used && h->next && !h->next->used) {
            h->size += h->next->size;
            h->next = h->next->next;
            a->n_free++;
            return;
        }
    a->n_free++;
}

size_t ff_largest_free(FirstFit *a)
{
    FBHeader *h; size_t best = 0;
    for (h = a->head; h; h = h->next)
        if (!h->used && h->size > best) best = h->size;
    return best > HSIZE ? best - HSIZE : 0;
}

void ff_report(FirstFit *a, const char *tag)
{
    long blocks = 0, freeb = 0; size_t freeb_bytes = 0; FBHeader *h;
    for (h = a->head; h; h = h->next) {
        blocks++;
        if (!h->used) { freeb++; freeb_bytes += h->size; }
    }
    printf("[firstfit %s] alloc=%ld free=%ld fail=%ld blocks=%ld freeblocks=%ld "
           "freepct=%.1f%% avg_search=%.1f\n",
           tag, a->n_alloc, a->n_free, a->n_fail, blocks, freeb,
           100.0 * (double)freeb_bytes / (double)a->cap,
           a->n_alloc ? (double)a->search_steps / (double)a->n_alloc : 0.0);
}
