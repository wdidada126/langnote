/* main.c — 多级反馈队列（MLFQ）调度器模拟，附 RR 与 FIFO 基线
 * 对应讲次：L01（进程抽象）/L02（控制流与上下文切换）；规则取自 OSTEP MLFQ 章。
 * 单核事件驱动，按 tick 推进；确定性 LCG 生成混合负载（交互型/计算型）。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NPROC   8
#define NLEVEL  5
#define BASEQ   1        /* 最高级时间片 = 1 tick，下一级别 ×2 */
#define BOOST   200      /* 优先级刷新周期 */
#define MAXT    8000
#define NSLOT   8        /* 每进程 CPU/IO 段数上限 */

enum { MLFQ, RR, FIFO };
enum { ST_NEW, ST_READY, ST_RUN, ST_IO, ST_DONE };

typedef struct {
    int id, arrival, prio;
    int cpuburst[NSLOT], ioburst[NSLOT], nseg, seg;
    int state, io_left, cpu_left, slice_left;
    int first_run, finish;
} Proc;

static Proc P[NPROC];
static char gantt[MAXT + 2];

static unsigned int seed = 2024u;
static unsigned int rnd(unsigned int m)
{
    seed = seed * 1103515245u + 12345u;
    return (seed >> 10) % m;
}

static void mkload(int i)
{
    int s, n = 3 + (int)rnd(4);
    P[i].id = i;
    P[i].arrival = (int)rnd(50);
    P[i].nseg = n;
    for (s = 0; s < n; s++) {
        if (i % 2 == 0) {  /* 交互型：短 CPU 段 + 长 IO，期待低延迟 */
            P[i].cpuburst[s] = 1 + (int)rnd(4);
            P[i].ioburst[s]  = 5 + (int)rnd(20);
        } else {           /* 计算型：长 CPU 段，吞吐来源 */
            P[i].cpuburst[s] = 30 + (int)rnd(60);
            P[i].ioburst[s]  = 1 + (int)rnd(3);
        }
    }
    P[i].prio = 0; P[i].seg = 0; P[i].state = ST_NEW;
    P[i].io_left = P[i].cpu_left = P[i].slice_left = 0;
    P[i].first_run = P[i].finish = -1;
}

/* ---- 每级一条循环数组就绪队列 ---- */
typedef struct { int ring[NLEVEL][64]; int head[NLEVEL], tail[NLEVEL]; } ReadyQ;

static void qpush(ReadyQ *q, int lvl, int id)
{
    q->ring[lvl][q->tail[lvl] % 64] = id;
    q->tail[lvl]++;
}
static int qpop(ReadyQ *q, int lvl)
{
    int v;
    if (q->head[lvl] == q->tail[lvl]) return -1;
    v = q->ring[lvl][q->head[lvl] % 64];
    q->head[lvl]++;
    return v;
}
static int qnonempty(ReadyQ *q)
{
    int l;
    for (l = 0; l < NLEVEL; l++) if (q->head[l] != q->tail[l]) return 1;
    return 0;
}

static double run(int mode)
{
    ReadyQ q;
    int t, cur = -1, i;
    long turn = 0, resp = 0, ndone = 0;
    memset(&q, 0, sizeof q);
    memset(gantt, '.', sizeof(gantt) - 1);

    /* RR 与 FIFO 都只有第 0 级有意义；FIFO 时间片"无限大"（跑满当前 CPU 段） */
    for (t = 0; t < MAXT && ndone < NPROC; t++) {
        for (i = 0; i < NPROC; i++) {
            if (P[i].state == ST_NEW && P[i].arrival == t) {
                P[i].state = ST_READY;
                qpush(&q, P[i].prio, i);
            }
            if (P[i].state == ST_IO) {
                if (--P[i].io_left <= 0) { P[i].state = ST_READY; qpush(&q, P[i].prio, i); }
            }
        }
        if (mode == MLFQ && t && t % BOOST == 0) {   /* 全体拉回最高级 */
            int l, id;
            ReadyQ nq; memset(&nq, 0, sizeof nq);
            for (l = 0; l < NLEVEL; l++)
                while ((id = qpop(&q, l)) >= 0) { P[id].prio = 0; qpush(&nq, 0, id); }
            q = nq;
            if (cur >= 0) P[cur].prio = 0;
        }
        if (cur < 0 && qnonempty(&q)) {
            int l;
            for (l = 0; l < NLEVEL; l++) { cur = qpop(&q, l); if (cur >= 0) break; }
            if (cur >= 0) {
                P[cur].state = ST_RUN;
                if (P[cur].first_run < 0) P[cur].first_run = t;
                P[cur].cpu_left = P[cur].cpuburst[P[cur].seg];
                P[cur].slice_left = (mode == FIFO) ? 1 << 20
                                    : (mode == RR) ? 4 : (BASEQ << P[cur].prio);
            }
        }
        if (cur >= 0) {
            gantt[t] = (char)('0' + P[cur].id);
            P[cur].cpu_left--;
            P[cur].slice_left--;
            if (P[cur].cpu_left <= 0) {           /* 当前 CPU 段跑完 → IO 或结束（主动让出：不降级） */
                P[cur].seg++;
                if (P[cur].seg >= P[cur].nseg) {
                    P[cur].state = ST_DONE; P[cur].finish = t;
                    ndone++;
                } else {
                    P[cur].state = ST_IO; P[cur].io_left = P[cur].ioburst[P[cur].seg];
                }
                cur = -1;
            } else if (P[cur].slice_left <= 0) {  /* 用满时间片 → 降级（MLFQ 规则） */
                if (mode == MLFQ && P[cur].prio < NLEVEL - 1) P[cur].prio++;
                P[cur].state = ST_READY;
                qpush(&q, (mode == MLFQ) ? P[cur].prio : 0, cur);
                cur = -1;
            }
        }
    }
    for (i = 0; i < NPROC; i++)
        if (P[i].state == ST_DONE) {
            turn += P[i].finish - P[i].arrival;
            resp += P[i].first_run - P[i].arrival;
        }
    printf("  gantt[0..110]: %.110s\n", gantt);
    printf("  avg turnaround=%.1f avg response=%.1f done=%ld/%d\n",
           (double)turn / (double)(ndone + 1), (double)resp / (double)(ndone + 1),
           (long)ndone, NPROC);
    return (double)turn / (double)(ndone + 1);
}

int main(void)
{
    int i;
    puts("sched demo — MLFQ vs RR vs FIFO（6.1810 L01/L02 配套）");
    for (i = 0; i < NPROC; i++) mkload(i);
    puts("== MLFQ（5 级，指数时间片 + boost） ==");
    seed = 2024u; run(MLFQ);
    for (i = 0; i < NPROC; i++) mkload(i);
    puts("== RR（单队列，片长 4） ==");
    run(RR);
    for (i = 0; i < NPROC; i++) mkload(i);
    puts("== FIFO（非抢占，跑满 CPU 段） ==");
    run(FIFO);
    puts("解读：交互型进程(偶数号)的 response 在 MLFQ 下显著低于 RR/FIFO——");
    puts("      代价是计算型进程被降级、周转上升；把 BOOST 调大再观察饥饿现象。");
    return 0;
}
