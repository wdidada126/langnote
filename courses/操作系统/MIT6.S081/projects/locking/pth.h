/* pth.h — 极小线程/原子兼容层：POSIX 用 pthread，Windows 用 Win32。
 * 为 projects/locking 服务；教学用，不追求无锁库级别的严谨（见 README 声明）。 */
#ifndef PTH_H
#define PTH_H

#include <stdlib.h>

#if defined(_WIN32)

#include <windows.h>

typedef HANDLE pth_t;
typedef struct { void (*fn)(void *); void *arg; } pth_box;

static DWORD WINAPI pth_win_start(void *arg)
{
    pth_box *b = (pth_box *)arg;
    b->fn(b->arg);
    free(b);
    return 0;
}
static int pth_create(pth_t *t, void (*fn)(void *), void *arg)
{
    pth_box *b = (pth_box *)malloc(sizeof *b);
    b->fn = fn; b->arg = arg;
    *t = CreateThread(0, 0, pth_win_start, b, 0, 0);
    return *t ? 0 : -1;
}
static void pth_join(pth_t t) { WaitForSingleObject(t, INFINITE); CloseHandle(t); }
static void pth_yield(void) { SwitchToThread(); }
static void pth_sleep_ms(unsigned ms) { Sleep(ms); }

static long atomic_inc(long *p) { return InterlockedIncrement(p); }
static long atomic_dec(long *p) { return InterlockedDecrement(p); }
static long atomic_add(long *p, long v) { return InterlockedExchangeAdd(p, v) + v; }
static long atomic_read(const long *p) { return *(volatile long *)p; }
static void *atomic_ptr_read(void *const *p) { return *(void *volatile *)(p); }
static void atomic_ptr_store(void **p, void *v)
{ MemoryBarrier(); *(void *volatile *)p = v; MemoryBarrier(); }
static int atomic_xchg(int *p, int v)
{ return (int)InterlockedExchange((volatile LONG *)p, (LONG)v); }
static void barrier(void) { MemoryBarrier(); }

typedef CRITICAL_SECTION pth_mutex;
static void pth_mutex_init(pth_mutex *m) { InitializeCriticalSection(m); }
static void pth_mutex_lock(pth_mutex *m) { EnterCriticalSection(m); }
static void pth_mutex_unlock(pth_mutex *m) { LeaveCriticalSection(m); }

#else /* POSIX */

#include <pthread.h>
#include <unistd.h>

typedef pthread_t pth_t;
typedef struct { void (*fn)(void *); void *arg; } pth_box;

static void *pth_trampoline(void *arg)
{
    pth_box *b = (pth_box *)arg;
    b->fn(b->arg);
    free(b);
    return 0;
}
static int pth_create(pth_t *t, void (*fn)(void *), void *arg)
{
    pth_box *b = (pth_box *)malloc(sizeof *b);
    b->fn = fn; b->arg = arg;
    return pthread_create(t, 0, pth_trampoline, b);
}
static void pth_join(pth_t t) { void *x; pthread_join(t, &x); }
static void pth_yield(void) { sched_yield(); }
static void pth_sleep_ms(unsigned ms) { usleep(ms * 1000u); }

static long atomic_inc(long *p) { return __sync_add_and_fetch(p, 1); }
static long atomic_dec(long *p) { return __sync_add_and_fetch(p, -1); }
static long atomic_add(long *p, long v) { return __sync_add_and_fetch(p, v); }
static long atomic_read(const long *p) { return *(volatile long *)p; }
static void *atomic_ptr_read(void *const *p) { return *(void *volatile *)p; }
static void atomic_ptr_store(void **p, void *v)
{ __sync_synchronize(); *(void *volatile *)p = v; __sync_synchronize(); }
static int atomic_xchg(int *p, int v)
{ return (int)__sync_lock_test_and_set((volatile int *)p, v); }
static void barrier(void) { __sync_synchronize(); }

typedef pthread_mutex_t pth_mutex;
static void pth_mutex_init(pth_mutex *m) { pthread_mutex_init(m, 0); }
static void pth_mutex_lock(pth_mutex *m) { pthread_mutex_lock(m); }
static void pth_mutex_unlock(pth_mutex *m) { pthread_mutex_unlock(m); }

#endif /* _WIN32 */

/* 自旋锁：acquire/release 语义按 xv6 spinlock.c —— 换到手 = 之前别人
 * 释放锁时的写对我可见（barrier 教学近似，xv6 用 __sync 组合+fence）。 */
typedef struct { volatile int locked; } spinlock_t;

static void spin_init(spinlock_t *l) { l->locked = 0; }
static void spin_acquire(spinlock_t *l)
{
    int backoff = 1;
    while (atomic_xchg((int *)&l->locked, 1) == 1) {
        int i;
        for (i = 0; i < backoff; i++) pth_yield();     /* 指数退避，减少 cacheline 争用 */
        if (backoff < 256) backoff <<= 1;
    }
    barrier();                                          /* acquire 栅栏 */
}
static void spin_release(spinlock_t *l)
{
    barrier();                                          /* release 栅栏 */
    atomic_xchg((int *)&l->locked, 0);
}

#endif /* PTH_H */
