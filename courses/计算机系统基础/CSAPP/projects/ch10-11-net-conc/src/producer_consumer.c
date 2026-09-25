/*
 * producer_consumer.c —— 有界缓冲区生产者/消费者（L20 / CSAPP 12.4-12.5）
 * 讲点：共享计数器、互斥、条件变量、虚假唤醒、while-vs-if。
 *
 * 跨平台同步原语：
 *   POSIX   : pthread_mutex + pthread_cond
 *   Windows : SRWLOCK(互斥) + CONDITION_VARIABLE
 * 为让"同一份逻辑代码"在两个平台编译，这里封一层极简 API。
 * 主线程当生产者，spawn 一个消费者线程，生产 N 个、消费 N 个后校验一致。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
  #include <windows.h>
  typedef HANDLE           thread_t;
  typedef SRWLOCK          lock_t;
  typedef CONDITION_VARIABLE cond_t;

  static void lock_init(lock_t *l)    { InitializeSRWLock(l); }
  static void lock_p(lock_t *l)       { AcquireSRWLockExclusive(l); }
  static void lock_v(lock_t *l)       { ReleaseSRWLockExclusive(l); }
  static void cond_init(cond_t *c)    { InitializeConditionVariable(c); }
  static void cond_wait(cond_t *c, lock_t *l) {
      SleepConditionVariableSRW(c, l, INFINITE, 0);   /* 可能虚假唤醒 */
  }
  static void cond_signal(cond_t *c)  { WakeConditionVariable(c); }
  static void cond_broadcast(cond_t *c){ WakeAllConditionVariable(c); }
  static thread_t thr_create(unsigned (*fn)(void*), void *arg) {
      DWORD id;
      return CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)fn, arg, 0, &id);
  }
  static void thr_join(thread_t t)    { WaitForSingleObject(t, INFINITE); CloseHandle(t); }
#else
  #include <pthread.h>
  #include <semaphore.h>
  #include <unistd.h>
  typedef pthread_t        thread_t;
  typedef pthread_mutex_t  lock_t;
  typedef pthread_cond_t   cond_t;

  static void lock_init(lock_t *l)    { pthread_mutex_init(l, NULL); }
  static void lock_p(lock_t *l)       { pthread_mutex_lock(l); }
  static void lock_v(lock_t *l)       { pthread_mutex_unlock(l); }
  static void cond_init(cond_t *c)    { pthread_cond_init(c, NULL); }
  static void cond_wait(cond_t *c, lock_t *l) { pthread_cond_wait(c, l); }
  static void cond_signal(cond_t *c)  { pthread_cond_signal(c); }
  static void cond_broadcast(cond_t *c){ pthread_cond_broadcast(c); }
  static thread_t thr_create(void *(*fn)(void*), void *arg) {
      thread_t t; pthread_create(&t, NULL, (void*(*)(void*))fn, arg); return t;
  }
  static void thr_join(thread_t t)    { pthread_join(t, NULL); }
#endif

#define N 16                 /* 生产/消费总数 */
#define SLOT 4               /* 有界缓冲区容量 */

typedef struct {
    int   buf[SLOT];
    int   count;             /* 当前元素数 —— 被 buf_mtx 保护的共享状态 */
    int   in, out;
    int   finished;          /* 生产者置位：不再生产 */
    lock_t mtx;
    cond_t not_full;
    cond_t not_empty;
    long consumer_sum;
} shared_t;

/* 消费者：等待非空 → 取一个 → 累加 */
#ifdef _WIN32
static unsigned consumer(void *arg)
#else
static void *consumer(void *arg)
#endif
{
    shared_t *s = (shared_t *)arg;
    int got;
    for (;;) {
        lock_p(&s->mtx);
        /* while（不是 if）！防虚假唤醒 + 防多消费者争用（L20） */
        while (s->count == 0 && !s->finished)
            cond_wait(&s->not_empty, &s->mtx);
        if (s->count == 0 && s->finished) { lock_v(&s->mtx); break; }
        got = s->buf[s->out];
        s->out = (s->out + 1) % SLOT;
        s->count--;
        s->consumer_sum += got;
        cond_signal(&s->not_full);          /* 腾空一格 → 唤醒生产者 */
        lock_v(&s->mtx);
    }
#ifdef _WIN32
    return 0;
#else
    return NULL;
#endif
}

int main(void)
{
    shared_t s;
    thread_t t;
    int i, produced_sum = 0;

    memset(&s, 0, sizeof s);
    lock_init(&s.mtx);
    cond_init(&s.not_full);
    cond_init(&s.not_empty);

    t = thr_create(
#ifdef _WIN32
        (unsigned (*)(void*))consumer,
#else
        (void *(*)(void*))consumer,
#endif
        &s);

    /* 主线程当生产者 */
    for (i = 1; i <= N; i++) {
        lock_p(&s.mtx);
        while (s.count == SLOT)             /* 缓冲区满 → 等 not_full */
            cond_wait(&s.not_full, &s.mtx);
        s.buf[s.in] = i;
        s.in = (s.in + 1) % SLOT;
        s.count++;
        produced_sum += i;
        printf("[prod] put %2d (count=%d)\n", i, s.count);
        cond_signal(&s.not_empty);          /* 有新货 → 唤醒消费者 */
        lock_v(&s.mtx);
    }

    lock_p(&s.mtx);
    s.finished = 1;
    cond_broadcast(&s.not_empty);           /* 让消费者看到结束标志 */
    lock_v(&s.mtx);

    thr_join(t);

    printf("produced_sum=%d consumer_sum=%ld  %s\n",
           produced_sum, s.consumer_sum,
           produced_sum == s.consumer_sum ? "MATCH ✓" : "MISMATCH ✗");
    return produced_sum == s.consumer_sum ? 0 : 1;
}
