/*
 * matrix.c —— Cache 友好遍历与分块矩阵乘 benchmark
 * 关联讲次：L10（存储层次/缓存）、L09（循环变换）、L11（展开与向量化收益观察）
 *
 * 三组实验，全部用同一份 64×64 双精度块（≈32KB/矩阵，接近常见 L1 32KB）：
 *   A. 遍历顺序：行优先 vs 列优先 —— 空间局部性 / 缓存颠簸
 *   B. 矩阵乘：ijk 朴素 vs 分块(tiling) —— 数据复用与工作集
 *   C. 步长扫描：stride 遍历 —— 组冲突（cache set conflict）
 * 结果正确性在 B 中与朴素实现逐元素比对，防止"快但错"。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "perf_util.h"

/* ---------- 工具 ---------- */
static double *alloc_matrix(int n)
{
    double *m = (double *)malloc((size_t)n * (size_t)n * sizeof(double));
    int i, j;
    if (!m) { fprintf(stderr, "malloc failed\n"); exit(1); }
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            m[(size_t)i * n + j] = (double)((i * 37 + j * 11) % 13) * 0.25 + 1.0;
    return m;
}

/* volatile 累加器：阻止编译器把测量循环整体优化掉（L09 的"死代码消除"） */
static volatile double g_sink;
static void sink(double v) { g_sink = v; }

/* ---------- A. 遍历顺序 ---------- */
static double sum_row_major(const double *m, int n)
{
    double s = 0.0;
    int i, j;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            s += m[(size_t)i * n + j];
    return s;
}

static double sum_col_major(const double *m, int n)
{
    double s = 0.0;
    int i, j;
    for (j = 0; j < n; j++)
        for (i = 0; i < n; i++)
            s += m[(size_t)i * n + j];      /* 每次跨一整行 → 空间局部性尽失 */
    return s;
}

static void bench_traversal(int n, int reps)
{
    double *m = alloc_matrix(n);
    double t, best_r = 1e30, best_c = 1e30;
    int k;
    for (k = 0; k < reps; k++) {
        TIME_IT(sink(sum_row_major(m, n)), t);
        if (t < best_r) best_r = t;
        TIME_IT(sink(sum_col_major(m, n)), t);
        if (t < best_c) best_c = t;
    }
    printf("[A] n=%-5d 行优先 %8.4fs (%6.2f ns/元素) | 列优先 %8.4fs (%6.2f ns/元素) | 慢 %.1fx\n",
           n, best_r, best_r * 1e9 / ((double)n * n),
           best_c, best_c * 1e9 / ((double)n * n), best_c / best_r);
    free(m);
}

/* ---------- B. 矩阵乘：朴素 ijk vs 分块 ---------- */
static void mul_naive(const double *a, const double *b, double *c, int n)
{
    int i, j, k;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++) {
            double s = 0.0;
            for (k = 0; k < n; k++)
                s += a[(size_t)i * n + k] * b[(size_t)k * n + j];
            c[(size_t)i * n + j] = s;
        }
}

#define TILE 32
static void mul_blocked(const double *a, const double *b, double *c, int n)
{
    int i0, j0, k0, i, j, k;
    for (i0 = 0; i0 < n; i0 += TILE)
        for (j0 = 0; j0 < n; j0 += TILE)
            for (k0 = 0; k0 < n; k0 += TILE) {
                int ie = i0 + TILE < n ? i0 + TILE : n;
                int je = j0 + TILE < n ? j0 + TILE : n;
                int ke = k0 + TILE < n ? k0 + TILE : n;
                for (i = i0; i < ie; i++)
                    for (j = j0; j < je; j++) {
                        double s = c[(size_t)i * n + j];
                        for (k = k0; k < ke; k++)
                            s += a[(size_t)i * n + k] * b[(size_t)k * n + j];
                        c[(size_t)i * n + j] = s;
                    }
            }
}

static int mul_equal(const double *x, const double *y, int n, double tol)
{
    int i;
    for (i = 0; i < n * n; i++)
        if (x[i] - y[i] > tol || y[i] - x[i] > tol)  /* 不用 fabs 以免依赖 <math.h> -lm */
            return 0;
    return 1;
}

static void bench_mul(int n)
{
    double *a = alloc_matrix(n), *b = alloc_matrix(n);
    double *c1 = (double *)calloc((size_t)n * n, sizeof(double));
    double *c2 = (double *)calloc((size_t)n * n, sizeof(double));
    double t, tn = 1e30, tb = 1e30;
    double flops = 2.0 * (double)n * (double)n * (double)n;
    int k;

    for (k = 0; k < 2; k++) {
        TIME_IT(mul_naive(a, b, c1, n), t);
        if (t < tn) tn = t;
        memset(c2, 0, (size_t)n * n * sizeof(double));
        TIME_IT(mul_blocked(a, b, c2, n), t);
        if (t < tb) tb = t;
    }
    printf("[B] n=%-5d 朴素 %7.4fs (%6.2f GFLOP/s) | 分块(TILE=%d) %7.4fs (%6.2f GFLOP/s) | 正确性 %s\n",
           n, tn, flops / tn / 1e9, TILE, tb, flops / tb / 1e9,
           mul_equal(c1, c2, n, 1e-6) ? "OK" : "MISMATCH");
    free(a); free(b); free(c1); free(c2);
}

/* ---------- C. 步长扫描 ---------- */
static double stride_scan(const double *m, int n, int stride, int touches)
{
    double s = 0.0;
    long idx = 0;
    int k;
    for (k = 0; k < touches; k++) {
        s += m[(size_t)idx];
        idx += stride;
        if (idx >= (long)n * n) idx = 0;
    }
    return s;
}

static void bench_stride(int n, int touches)
{
    double *m = alloc_matrix(n);
    int strides[] = {1, 2, 4, 8, 16, 32, 64, 128, 256};
    size_t s;
    printf("[C] n=%d, %d 次随机跳跃累加，单位 ns/访存（数值跳变=组冲突/未命中）\n", n, touches);
    for (s = 0; s < sizeof(strides) / sizeof(strides[0]); s++) {
        double t, best = 1e30;
        int rep;
        for (rep = 0; rep < 3; rep++) {
            TIME_IT(sink(stride_scan(m, n, strides[s], touches)), t);
            if (t < best) best = t;
        }
        printf("    stride=%4d -> %7.2f ns/访存\n", strides[s], best * 1e9 / touches);
    }
    free(m);
}

/* ---------- main ---------- */
int main(void)
{
    printf("=== CSAPP Ch.6 存储层次 / Ch.5 优化 实验台 ===\n");
    printf("提示: 用 -O1/-O2 对比；观察 A 的行列差、B 的分块加速、C 的 stride 曲线\n\n");

    bench_traversal(512, 3);
    bench_traversal(1024, 2);

    bench_mul(128);
    bench_mul(256);
    bench_mul(512);

    bench_stride(512, 200000);

    printf("\n(累加器最终值 %g —— 仅为防止优化而写)\n", g_sink);
    return 0;
}
