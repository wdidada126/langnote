/*
 * perf_util.h —— 最小性能测量脚手架（L09/L10 方法论）
 * 跨平台单调时钟：POSIX clock_gettime / Win32 QueryPerformanceCounter。
 */
#ifndef PERF_UTIL_H
#define PERF_UTIL_H

#include <stdint.h>

#if defined(_WIN32)
#include <windows.h>
static double now_sec(void)
{
    LARGE_INTEGER freq, t;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&t);
    return (double)t.QuadPart / (double)freq.QuadPart;
}
#else
#include <time.h>
static double now_sec(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + 1e-9 * (double)ts.tv_nsec;
}
#endif

/* 计时宏：结果写入 out_sec（秒）。多次采样取最小值是稳健做法。 */
#define TIME_IT(stmt, out_sec)                \
    do {                                      \
        double _t0 = now_sec();               \
        stmt;                                 \
        (out_sec) = now_sec() - _t0;          \
    } while (0)

#endif /* PERF_UTIL_H */
