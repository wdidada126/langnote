/* pgtbl.c — 两级页表 + TLB + 缺页 + CoW（L04/L10/L11 的可运行教材） */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pgtbl.h"

unsigned char ram[NFRAMES][PGSIZE];
unsigned int frame_ref[NFRAMES];
int frame_free[NFRAMES];                 /* 1 = 空闲 */
unsigned int g_last_fault;
int g_flush_on_map = 1;                  /* 0 = 模拟"忘了 sfence.vma" */

static TlbEnt tlb[TLB_N];

#define PTE(ep)  ((ep) & ~0xFFFu)         /* 帧物理地址 */
#define PPF(ep)  ((ep) >> PGSHIFT)        /* 帧号 */
#define MK(PPN, perm) (((PPN) << PGSHIFT) | (perm))

/* 页表也存在 ram[] 里：目录/表各占一帧（1024 个 32 位项） */
static unsigned int *tbl_of(int f) { return (unsigned int *)ram[f]; }

void pm_init(void)
{
    int i;
    for (i = 0; i < NFRAMES; i++) { frame_free[i] = 1; frame_ref[i] = 0; }
    memset(tlb, 0, sizeof tlb);
}

int pm_alloc_frame(void)
{
    int i;
    for (i = 0; i < NFRAMES; i++)
        if (frame_free[i]) { frame_free[i] = 0; frame_ref[i] = 1; return i; }
    return -1;
}

void pm_free_frame(int f)
{
    if (f < 0 || f >= NFRAMES || frame_free[f]) return;
    if (--frame_ref[f] == 0) frame_free[f] = 1;
}

Proc *proc_create(void)
{
    Proc *p = (Proc *)calloc(1, sizeof *p);
    int f = pm_alloc_frame();
    if (f < 0) return 0;
    memset(ram[f], 0, PGSIZE);
    p->root = (unsigned int)f;
    return p;
}

/* 找到/创建 PTE 所在槽位；walk 计 3 次内存访问（目录项+表页+PTE 视作两次） */
static unsigned int *pte_slot(Proc *p, unsigned int va, int alloc, int *st)
{
    unsigned int *dir = tbl_of((int)p->root);
    unsigned int de = dir[PDX(va)];
    unsigned int *tab;
    if (!(de & PTE_V)) {
        int f;
        if (!alloc) { *st = FAULT_UNMAPPED; return 0; }
        f = pm_alloc_frame();
        if (f < 0) { *st = FAULT_NOMEM; return 0; }
        memset(ram[f], 0, PGSIZE);
        dir[PDX(va)] = MK((unsigned int)f, PTE_V);
        p->n_walk += 2;
        de = dir[PDX(va)];
    }
    tab = tbl_of(PPF(de));
    p->n_walk += 2;
    *st = FAULT_NONE;
    return &tab[PTX(va)];
}

int pt_map(Proc *p, unsigned int va, unsigned int f, unsigned int perm)
{
    int st; unsigned int *ep = pte_slot(p, va, 1, &st);
    if (!ep) return st;
    frame_ref[f]++;
    *ep = MK(f, PTE_V | perm);
    if (g_flush_on_map) tlb_flush_all();  /* sfence.vma：改了映射必刷 */
    return 0;
}

void pt_unmap(Proc *p, unsigned int va)
{
    int st; unsigned int *ep = pte_slot(p, va, 0, &st);
    if (ep && (*ep & PTE_V)) {
        pm_free_frame((int)PPF(*ep));
        *ep = 0;
        p->n_mapped--;
        tlb_flush_all();
    }
}

int pt_walk(Proc *p, unsigned int va, unsigned int *pa, unsigned int *perm)
{
    int st; unsigned int *ep = pte_slot(p, va, 0, &st);
    if (!ep || !(*ep & PTE_V)) { g_last_fault = FAULT_UNMAPPED; return FAULT_UNMAPPED; }
    if (pa) *pa = PTE(*ep);
    if (perm) *perm = *ep & 0xFFFu;
    return FAULT_NONE;
}

void tlb_flush_all(void)
{
    int i; for (i = 0; i < TLB_N; i++) tlb[i].valid = 0;
}

/* 实验用：只失效一项——"忘刷"演示 */
void tlb_flush_noop(void) { /* 什么都不做：保留陈旧条目 */ }

static TlbEnt *tlb_find(unsigned int vpn)
{
    TlbEnt *e = &tlb[vpn % TLB_N];
    if (e->valid && e->vpn == vpn) return e;
    return 0;
}

static void tlb_fill(unsigned int vpn, unsigned int pa, unsigned int perm)
{
    TlbEnt *e = &tlb[vpn % TLB_N];
    (void)e; (void)vpn; (void)pa; (void)perm;
}

/* 真正带统计的 translate：hit/walk/demand-map/CoW 全路径 */
int tlb_translate(Proc *p, unsigned int va, int write, unsigned int *pa)
{
    unsigned int vpn = va >> PGSHIFT;
    TlbEnt *e = tlb_find(vpn);
    unsigned int ep_perm;
    int st; unsigned int *ep;

    p->n_translate++;
    if (e) {                              /* TLB hit：也要复查写权限（CoW 位在 perm 里） */
        if (write && !(e->perm & PTE_W)) goto slow;
        if (!write && !(e->perm & PTE_R)) goto slow;
        p->n_tlb_hit++;
        *pa = e->pa | PGOFF(va);
        return FAULT_NONE;
    }
    p->n_tlb_miss++;
slow:
    ep = pte_slot(p, va, 0, &st);
    if (!ep || !(*ep & PTE_V)) {          /* demand paging：缺页补一页 */
        int f = pm_alloc_frame();
        p->n_fault++;
        g_last_fault = FAULT_UNMAPPED;
        if (f < 0) return FAULT_NOMEM;
        memset(ram[f], 0, PGSIZE);
        return (pt_map(p, va, (unsigned int)f, PTE_R | PTE_W | PTE_U),
                tlb_translate(p, va, write, pa));
    }
    ep_perm = *ep & 0xFFFu;
    if (write && !(ep_perm & PTE_W)) {
        if (ep_perm & PTE_C) {            /* CoW：copy-on-fault */
            p->n_cow_copy++;
            if (frame_ref[PPF(*ep)] > 1) {
                int nf = pm_alloc_frame();
                if (nf < 0) return FAULT_NOMEM;
                memcpy(ram[nf], ram[PPF(*ep)], PGSIZE);
                frame_ref[PPF(*ep)]--;    /* 手动减一：下面 pt_unmap 还会再减，先拆弹 */
                frame_free[nf] = 0; frame_ref[nf] = 1;
                *ep = MK((unsigned int)nf, PTE_V | PTE_R | PTE_W | PTE_U);
            } else {                       /* 唯一持有者：直接转正 */
                *ep = MK(PPF(*ep), PTE_V | PTE_R | PTE_W | PTE_U);
            }
            tlb_flush_all();
            return tlb_translate(p, va, write, pa);
        }
        g_last_fault = FAULT_PERM;
        return FAULT_PERM;
    }
    *pa = PTE(*ep) | PGOFF(va);
    e = &tlb[vpn % TLB_N];                /* 回填 TLB */
    e->valid = 1; e->vpn = vpn; e->pa = PTE(*ep); e->perm = ep_perm;
    return FAULT_NONE;
}

int sys_store(Proc *p, unsigned int va, unsigned char data)
{
    unsigned int pa; int st = tlb_translate(p, va, 1, &pa);
    if (st) return st;
    ram[pa >> PGSHIFT][pa & (PGSIZE - 1)] = data;
    return 0;
}

int sys_load(Proc *p, unsigned int va, unsigned char *data)
{
    unsigned int pa; int st = tlb_translate(p, va, 0, &pa);
    if (st) return st;
    *data = ram[pa >> PGSHIFT][pa & (PGSIZE - 1)];
    return 0;
}

/* fork：遍历父页表，把可写页双方降为只读+C，只读文本页直接共享 */
Proc *proc_fork_cow(Proc *p)
{
    Proc *c = proc_create();
    unsigned int *pdir = tbl_of((int)p->root), *cdr;
    int i, j, st;
    if (!c) return 0;
    cdr = tbl_of((int)c->root);
    for (i = 0; i < 1024; i++) {
        unsigned int *ptab;
        if (!(pdir[i] & PTE_V)) continue;
        st = 0; (void)st;
        ptab = tbl_of(PPF(pdir[i]));
        { int f = pm_alloc_frame(); if (f < 0) return c; /* 简化：目录页不够就返回 */
          memset(ram[f], 0, PGSIZE);
          cdr[i] = MK((unsigned int)f, PTE_V); }
        { unsigned int *ctab = tbl_of(PPF(cdr[i]));
          for (j = 0; j < 1024; j++) {
              unsigned int ep = ptab[j];
              unsigned int perm;
              if (!(ep & PTE_V)) continue;
              perm = ep & 0xFFFu;
              frame_ref[PPF(ep)]++;
              if (perm & PTE_W) {          /* 可写 → 双方只读 + CoW 标记 */
                  perm = (perm & ~PTE_W) | PTE_C;
                  ptab[j] = MK(PPF(ep), PTE_V | perm);
              }
              ctab[j] = MK(PPF(ep), PTE_V | perm);
              c->n_mapped++;
          } }
    }
    tlb_flush_all();
    return c;
}

void pgtbl_stats(Proc *p, const char *tag)
{
    printf("[pgtbl %s] translate=%ld tlb-hit=%ld miss=%ld (%.1f%% hit) "
           "walk-accesses=%ld faults=%ld cow-copy=%ld\n",
           tag, p->n_translate, p->n_tlb_hit, p->n_tlb_miss,
           100.0 * (double)p->n_tlb_hit / (double)(p->n_translate + 1),
           p->n_walk, p->n_fault, p->n_cow_copy);
}
