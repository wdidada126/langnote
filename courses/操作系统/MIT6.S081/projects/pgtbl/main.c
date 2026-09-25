/* main.c — 地址翻译 / TLB / 缺页 / CoW 综合演示（6.1810 L04/L10/L11） */
#include <stdio.h>
#include <stdlib.h>
#include "pgtbl.h"

static unsigned int seed = 42u;
static unsigned int rnd(void) { seed = seed * 1103515245u + 12345u; return seed >> 10; }

#define USTACK 0x0FFFF000u
#define TEXT   0x00001000u

static void demand_paging_demo(void)
{
    Proc *p = proc_create();
    unsigned int va;
    unsigned char d;
    int i;
    puts("== demand paging：首次触碰即缺页补一页 ==");
    for (i = 0; i < 40; i++) {
        va = TEXT + (unsigned int)i * PGSIZE;      /* 顺序触碰 40 页 */
        sys_store(p, va, (unsigned char)(i + 1));
        sys_store(p, va + 4, (unsigned char)i);
    }
    /* 每页内部连写 8 次：制造 TLB 命中 */
    for (i = 0; i < 8; i++) {
        sys_store(p, TEXT + 4 * (unsigned)i, (unsigned char)i);
    }
    pgtbl_stats(p, "demand+local");
    sys_load(p, TEXT, &d);
    printf("  readback TEXT[0]=%u (expect 1)\n", d);
    (void)USTACK; free(p);
}

static void tlb_demo(void)
{
    Proc *p = proc_create();
    int f0 = pm_alloc_frame(), f1 = pm_alloc_frame();
    unsigned int va = TEXT;
    unsigned char d;
    puts("== TLB 一致性：改映射后\"忘刷 sfence\"会读到陈旧物理页 ==");
    ram[f0][0] = 0xAA; ram[f1][0] = 0x55;
    pt_map(p, va, (unsigned)f0, PTE_R | PTE_W | PTE_U);
    sys_load(p, va, &d);
    printf("  第一次翻译 -> PA 帧%d, 值 0x%02X\n", f0, d);

    g_flush_on_map = 0;                            /* 假装没执行 sfence.vma */
    pt_map(p, va, (unsigned)f1, PTE_R | PTE_W | PTE_U); /* 换底层帧但不刷 TLB */
    sys_load(p, va, &d);
    printf("  换映射+不刷 -> 值 0x%02X（陈旧：仍来自帧%d）\n", d, f0);

    g_flush_on_map = 1;
    pt_map(p, va, (unsigned)f1, PTE_R | PTE_W | PTE_U); /* 正常应伴随 sfence */
    sys_load(p, va, &d);
    printf("  换映射+刷   -> 值 0x%02X（正确：来自帧%d）\n", d, f1);
    free(p);
}

static void cow_demo(void)
{
    Proc *parent = proc_create();
    Proc *child;
    unsigned int va = TEXT;
    unsigned char d;
    int i;
    puts("== Copy-on-Write fork ==");
    sys_store(parent, va, 10);                     /* 分配一页并写 */
    sys_store(parent, va + 100, 20);
    child = proc_fork_cow(parent);                 /* 双方变只读+共享 */
    sys_load(child, va, &d);
    printf("  子进程读共享页 -> %u\n", d);
    sys_store(child, va, 99);                      /* 子进程写 -> 触发 CoW 复制 */
    sys_load(parent, va, &d);
    printf("  写后父进程仍读到 %u（子进程已私有化那页）\n", d);
    sys_load(child, va, &d);
    printf("  子进程读到 %u（新副本）\n", d);

    for (i = 0; i < 30; i++) {                     /* 制造更多可写页 */
        unsigned int v = TEXT + (unsigned)i * PGSIZE;
        sys_store(parent, v, (unsigned char)i);
    }
    { Proc *c2 = proc_fork_cow(parent);
      int k;
      for (k = 0; k < 15; k++) sys_store(c2, TEXT + (unsigned)k * PGSIZE, (unsigned char)k);
      pgtbl_stats(parent, "parent(after 2 forks)");
      pgtbl_stats(c2,     "child (wrote 15 pages)");
      free(c2); }
    free(child); free(parent);
}

int main(void)
{
    puts("pgtbl demo — 6.1810 L04/L10/L11: page table, TLB, fault, CoW");
    pm_init();
    demand_paging_demo();
    tlb_demo();
    cow_demo();
    puts("done.");
    return 0;
}
