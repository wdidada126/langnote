#include "bits.h"
#include <limits.h>

/* x & y == ~(~x | ~y)（德摩根）。全部 int 位运算，无溢出风险。 */
int bit_and(int x, int y)
{
    return ~((~x) | (~y));
}

/* 经典分治 popcount：先 2 位分组，再 4/8/16/32。unsigned 保证逻辑右移。 */
int bit_count(int x)
{
    unsigned u = (unsigned)x;
    u = (u & 0x55555555u) + ((u >> 1) & 0x55555555u);
    u = (u & 0x33333333u) + ((u >> 2) & 0x33333333u);
    u = (u & 0x0F0F0F0Fu) + ((u >> 4) & 0x0F0F0F0Fu);
    u = u + (u >> 8);
    u = u + (u >> 16);
    return (int)(u & 0x3Fu);
}

/* bang：对 x != 0，(unsigned)x | (-x 的位模式) 必使最高位为 1；x == 0 时为 0。
 * 用 ~x+1 构造 -x 的位模式（unsigned 域无 UB），右移用逻辑移保证确定性。 */
int bang(int x)
{
    unsigned ux = (unsigned)x;
    unsigned neg = (~ux) + 1u;               /* 模 2^32 的 -x */
    unsigned t = ux | neg;                   /* x==0 ? 0 : MSB=1 */
    return (int)((t >> 31) ^ 1u);
}

/* 饱和加法：用 long long 精确判定（宽类型无溢出），再钳位。 */
int sat_add(int x, int y)
{
    long long s = (long long)x + (long long)y;
    if (s > INT_MAX) return INT_MAX;
    if (s < INT_MIN) return INT_MIN;
    return (int)s;
}

/* x>0 ⇔ 符号位为 0 且非零。复用 bang，避免有符号右移的实现定义行为。 */
int is_positive(int x)
{
    unsigned sb = ((unsigned)x) >> 31;       /* 1 = 负数（含 INT_MIN） */
    unsigned nz = 1u - (unsigned)bang(x);    /* 1 = 非零 */
    return (int)((1u - sb) & nz);
}

/* ---- 浮点位级操作：uf 即 float 的位模式（由 main 端 memcpy 得到） ---- */

unsigned float_neg(unsigned uf)
{
    /* exp=0xFF 且 frac!=0 → NaN，须原样返回。无符号序下 NaN 恰在高位区。 */
    if (uf > 0x7F800000u)
        return uf;
    return uf ^ 0x80000000u;
}

unsigned float_abs(unsigned uf)
{
    unsigned mag = uf & 0x7FFFFFFFu;             /* 清符号位（bit31），保留数值位 */
    if (mag > 0x7F800000u)                       /* 只看数值位判 NaN，两个 NaN 区间都保持 */
        return uf;
    return mag;
}

/* uf * 2：
 *   +Inf / NaN     → 原样
 *   exp==0xFF 有限大 → 溢出变 +Inf? (exp 域内不再自增) 这里按 IEEE: Inf
 *   规格化          → exp+1（若 +1 后为 0xFF → Inf）
 *   非规格化(frac!=0) → frac<<1（可能进入规格化：frac 最高位为 1 时自动进位）
 *   ±0             → 原样
 */
unsigned float_twice(unsigned uf)
{
    unsigned sign = uf & 0x80000000u;
    unsigned exp = uf & 0x7F800000u;
    unsigned frac = uf & 0x007FFFFFu;

    if (exp == 0x7F800000u)                  /* Inf 与 NaN 原样 */
        return uf;
    if (exp == 0u) {                         /* 0 或非规格化 */
        if (frac == 0u) return uf;
        return sign | (frac << 1);           /* 若进规格化，bit23 自然为 1 */
    }
    if (exp == 0x7F000000u)                  /* 最大规格化 ×2 → Inf */
        return sign | 0x7F800000u;
    return sign | (exp + 0x00800000u) | frac;
}
