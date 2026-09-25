/* main.c — 自旋锁 / 互斥锁 / epoch 式 RCU 三合一演示（6.1810 L02/L15）
 * 共享数据：一条按 key 有序的链表；4 读线程狂找 key，2 写线程插入/删除。
 * 三种保护模式对比：
 *   MUTEX  —— 全部操作进大锁（正确但读者互相排队）
 *   SPIN   —— xv6 spinlock 风格（短临界区更快，读者仍有争用）
 *   RCU    —— 读端零指令级争用；写端原地改链，退役节点等 grace period 再 free
 * 声明：教学用"够用即可"的内存序（见 pth.h），不等同 liburcu 级别的生产实现。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "pth.h"

#define NREADER 4
#define NWRITER 2
#define READS   60000
#define WRITES  2000

typedef struct Node { struct Node *next; int key; } Node;

static Node list_head = { 0, -1 };       /* 哨兵：key=-1 */

enum { MODE_MUTEX, MODE_SPIN, MODE_RCU };
static int mode;

static pth_mutex bigm;
static spinlock_t wlk;                   /* 只保护写者之间（RCU 模式） */

static long n_reads, n_writes, n_hit;    /* 原子访问见 atomic_inc */

/* ---------- epoch RCU 核心（lab-thread / Linux Tree RCU 的最小模型） ---------- */
#define MAXT 16
static volatile long g_epoch = 1;
static volatile long tstate[MAXT];       /* -1 = 静默态，否则=进入读临界区时的 epoch */
static int n_threads_total;

static void rcu_read_lock(int tid)
{
    long e;
    do {
        e = atomic_read((long *)&g_epoch);
        if (e == -1) { pth_yield(); continue; }
        tstate[tid] = e;
        barrier();
        if (atomic_read((long *)&g_epoch) == e) return;  /* 期间被推进则重试 */
    } while (1);
}
static void rcu_read_unlock(int tid) { barrier(); tstate[tid] = -1; }

/* 写者：推进 epoch；非阻塞探测 grace；到期的退役节点才 free */
typedef struct { Node *node; long e; } Retired;
static Retired retired[WRITES * NWRITER + 8];
static int nretired;
static spinlock_t rlk;
static long reclaimed, still_waiting;

static void retire(Node *n)
{
    spin_acquire(&rlk);
    if (nretired < (int)(sizeof retired / sizeof retired[0])) {
        retired[nretired].node = n;
        retired[nretired].e = atomic_read((long *)&g_epoch);
        nretired++;
    }
    spin_release(&rlk);
}

static int grace_period_done(long target)
{
    int i;
    for (i = 0; i < n_threads_total; i++) {
        long s = tstate[i];
        if (s != -1 && s < target) return 0;   /* 仍有旧读者 */
    }
    return 1;
}

static void try_reclaim(void)
{
    int i, freed;
    spin_acquire(&rlk);
    do {
        freed = 0;
        for (i = 0; i < nretired; i++) {
            if (grace_period_done(retired[i].e)) {
                Node *n = retired[i].node;
                retired[i] = retired[nretired - 1];
                nretired--;
                free(n);
                reclaimed++;
                freed = 1;
                break;
            }
        }
    } while (freed);
    still_waiting = nretired;
    spin_release(&rlk);
}

static void advance_epoch(void)
{
    long e = atomic_read((long *)&g_epoch);
    barrier();
    g_epoch = e + 1;                      /* 写者之间由 wlk 串行化，安全 */
    barrier();
}

/* ---------- 链表操作 ---------- */
static int list_contains(int key)
{
    Node *x;
    for (x = list_head.next; x && x->key < key; x = x->next) ;
    return x && x->key == key;
}

static void reader_loop(void *arg)
{
    int tid = (int)(size_t)arg;
    int i, k;
    unsigned s = (unsigned)tid * 2654435761u;
    for (i = 0; i < READS; i++) {
        s = s * 1103515245u + 12345u;
        k = (int)((s >> 8) % 1000);
        if (mode == MODE_RCU) {
            rcu_read_lock(tid);
            if (list_contains(k)) atomic_inc(&n_hit);
            rcu_read_unlock(tid);
        } else if (mode == MODE_SPIN) {
            spin_acquire(&wlk);
            if (list_contains(k)) atomic_inc(&n_hit);
            spin_release(&wlk);
        } else {
            pth_mutex_lock(&bigm);
            if (list_contains(k)) atomic_inc(&n_hit);
            pth_mutex_unlock(&bigm);
        }
        atomic_inc(&n_reads);
    }
}

static void ins(int key)
{
    Node *pred = &list_head, *x = list_head.next, *n;
    while (x && x->key < key) { pred = x; x = x->next; }
    if (x && x->key == key) return;
    n = (Node *)malloc(sizeof *n);
    n->key = key;
    n->next = pred->next;
    barrier();
    pred->next = n;                      /* 发布：RCU 语义靠写者锁+屏障 */
    barrier();
}

static int del(int key)
{
    Node *pred = &list_head, *x = list_head.next;
    while (x && x->key < key) { pred = x; x = x->next; }
    if (!x || x->key != key) return 0;
    pred->next = x->next;                /* 原地摘链：旧读者仍可能拿着 x —— 绝不 free */
    barrier();
    if (mode == MODE_RCU) retire(x);
    else free(x);
    return 1;
}

static void writer_loop(void *arg)
{
    int tid = (int)(size_t)arg;
    int i, k;
    unsigned s = 12345u + (unsigned)tid * 97u;
    for (i = 0; i < WRITES; i++) {
        s = s * 1103515245u + 12345u;
        k = (int)((s >> 8) % 1000);
        if (mode == MODE_RCU) {
            spin_acquire(&wlk);          /* 只排写者 */
            advance_epoch();             /* 新 epoch：旧读者终将退出 */
            if (i & 1) del(k); else ins(k);
            atomic_inc(&n_writes);
            spin_release(&wlk);
            try_reclaim();               /* 回收 grace 到期的退役节点 */
            if ((i & 63) == 0) pth_sleep_ms(1);
        } else if (mode == MODE_SPIN) {
            spin_acquire(&wlk);
            if (i & 1) del(k); else ins(k);
            atomic_inc(&n_writes);
            spin_release(&wlk);
        } else {
            pth_mutex_lock(&bigm);
            if (i & 1) del(k); else ins(k);
            atomic_inc(&n_writes);
            pth_mutex_unlock(&bigm);
        }
    }
}

static int list_sane(void)
{
    Node *x = &list_head;
    int last = -2;
    while (x) {
        if (x->key <= last) return 0;
        last = x->key;
        x = x->next;
    }
    return 1;
}

static void clear_list(void)
{
    Node *x = list_head.next;
    while (x) { Node *t = x->next; free(x); x = t; }
    list_head.next = 0;
}

static void run(int m, const char *tag)
{
    pth_t tr[MAXT];
    int i, n = NREADER + NWRITER;
    double t0;
    mode = m;
    n_threads_total = n;
    { int j; for (j = 0; j < MAXT; j++) tstate[j] = -1; }
    n_reads = n_writes = n_hit = reclaimed = still_waiting = 0;
    nretired = 0;
    g_epoch = 1;
    pth_mutex_init(&bigm);
    spin_init(&wlk);
    spin_init(&rlk);
    clear_list();
    for (i = 0; i < NWRITER; i++) ins(i * 37 % 1000); /* 预填几个 key */
    t0 = (double)clock();
    for (i = 0; i < n; i++)
        pth_create(&tr[i], i < NREADER ? reader_loop : writer_loop, (void *)(size_t)i);
    for (i = 0; i < n; i++) pth_join(tr[i]);
    t0 = (double)(clock() - t0) / CLOCKS_PER_SEC;
    try_reclaim();
    printf("[%8s] reads=%ld writes=%ld hits=%ld time=%.2fs "
           "reclaimed=%ld pending=%ld list=%s\n",
           tag, n_reads, n_writes, n_hit, t0, reclaimed, still_waiting,
           list_sane() ? "OK" : "BROKEN");
    clear_list();
}

int main(void)
{
    puts("locking demo — 6.1810 L02/L15: mutex vs spinlock vs epoch-RCU");
    puts("（计时用 clock()，跨线程 CPU 时间仅作参考——重点是量级与正确性）");
    run(MODE_MUTEX, "mutex");
    run(MODE_SPIN, "spin");
    run(MODE_RCU, "rcu");
    puts("观察：RCU 读端不加锁不计数 → 读吞吐最高；退役节点在 grace 后才回收；");
    puts("把 del() 里 retire(x) 换成 free(x) 重跑（勿在生产模仿），通常很快段错误——");
    puts("这就是 RCU 的存在理由：难的不是更新，是安全回收。");
    return 0;
}
