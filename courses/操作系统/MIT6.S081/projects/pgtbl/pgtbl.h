/* pgtbl.h — 两级页表 + TLB + 缺页 + CoW 模拟器（对应 6.1810 L04/L10/L11）
 * 32 位地址：PDX(10) | PTX(10) | OFF(12)，页 4KiB；物理内存 = 256 帧静态数组。 */
#ifndef PGTBL_H
#define PGTBL_H

#include <stddef.h>

#define NFRAMES   256                    /* 1 MiB "物理内存" */
#define PGSHIFT   12
#define PGSIZE    (1u << PGSHIFT)
#define PDX(va)   (((va) >> 22) & 0x3FFu)
#define PTX(va)   (((va) >> 12) & 0x3FFu)
#define PGOFF(va) ((va) & 0xFFFu)

/* PTE：30:12 为 PPN，低位权限标志 */
#define PTE_V 0x001u   /* valid */
#define PTE_R 0x002u
#define PTE_W 0x004u
#define PTE_U 0x008u   /* user 可访问 */
#define PTE_C 0x010u   /* 自定义：copy-on-write 候选 */

#define TLB_N    16    /* 直接映射 TLB 项数 */

enum { TLB_MISS = 0, TLB_HIT };
enum { FAULT_NONE = 0, FAULT_UNMAPPED, FAULT_PERM, FAULT_NOMEM };

typedef struct { unsigned int vpn; unsigned int pa; unsigned int perm; int valid; } TlbEnt;

typedef struct {
    unsigned int root;                   /* 页目录所在帧号 */
    unsigned int n_mapped;               /* 已映射用户页数 */
    /* 统计 */
    long n_translate, n_walk, n_tlb_hit, n_tlb_miss, n_fault, n_cow_copy;
} Proc;

extern unsigned char ram[NFRAMES][PGSIZE];
extern unsigned int frame_ref[NFRAMES];
extern int frame_free[NFRAMES];
extern unsigned int g_last_fault;
extern int g_flush_on_map;               /* 1 = 改映射即刷 TLB；0 = 模拟忘发 sfence.vma */

void pm_init(void);
int  pm_alloc_frame(void);               /* 失败返回 -1 */
void pm_free_frame(int f);               /* refcount-- ，归零才真还 */

Proc *proc_create(void);                 /* 分配根页表（一页） */
int  pt_map(Proc *p, unsigned int va, unsigned int f, unsigned int perm);
void pt_unmap(Proc *p, unsigned int va); /* 需 sfence：内部会刷 TLB */
int  pt_walk(Proc *p, unsigned int va, unsigned int *pa, unsigned int *perm);

/* 带 TLB 的翻译：先查表，miss 再 walk */
int  tlb_translate(Proc *p, unsigned int va, int write, unsigned int *pa);
void tlb_flush_all(void);
void tlb_flush_noop(void);               /* 故意"忘刷"，演示陈旧条目 */

/* 访问内存：翻译失败时走缺页处理（demand paging + CoW） */
int  sys_store(Proc *p, unsigned int va, unsigned char data);
int  sys_load(Proc *p, unsigned int va, unsigned char *data);

/* fork：全部可写用户页变只读共享 + C 标记（CoW） */
Proc *proc_fork_cow(Proc *parent);

void pgtbl_stats(Proc *p, const char *tag);

#endif /* PGTBL_H */
