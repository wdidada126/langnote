#include <stdio.h>
#include <string.h>
#include <limits.h>
#include "bits.h"

static int fails = 0;

static unsigned f2u(float f)          /* float → 位模式（memcpy 型双关，良定义） */
{
    unsigned u;
    memcpy(&u, &f, sizeof u);
    return u;
}
static float u2f(unsigned u)
{
    float f;
    memcpy(&f, &u, sizeof f);
    return f;
}

static void check_i(const char *name, long long got, long long want)
{
    if (got == want) {
        printf("[ OK ] %-14s = %lld\n", name, got);
    } else {
        printf("[FAIL] %-14s = %lld (want %lld)\n", name, got, want);
        fails++;
    }
}
static void check_f(const char *name, unsigned got, unsigned want)
{
    printf("[ %s ] %-16s got=0x%08X want=0x%08X (%.7g vs %.7g)\n",
           got == want ? "OK" : "FAIL", name, got, want,
           (double)u2f(got), (double)u2f(want));
    if (got != want) fails++;
}

int main(void)
{
    /* --- 整数/位运算 --- */
    check_i("bit_and(6,3)",   bit_and(6, 3), 6 & 3);
    check_i("bit_and(MIN,1)", bit_and(INT_MIN, 1), 0);
    check_i("bit_count(0xF)", bit_count(0xF), 4);
    check_i("bit_count(-1)",  bit_count(-1), 32);
    check_i("bang(0)",  bang(0),  1);
    check_i("bang(5)",  bang(5),  0);
    check_i("bang(INT_MIN)", bang(INT_MIN), 0);
    check_i("sat_add(2e9-1,1)", sat_add(2000000000, 1), 2000000001);
    check_i("sat_add(INT_MAX,1)", sat_add(INT_MAX, 1), INT_MAX);
    check_i("sat_add(INT_MIN,-1)", sat_add(INT_MIN, -1), INT_MIN);
    check_i("is_positive(1)",  is_positive(1),  1);
    check_i("is_positive(0)",  is_positive(0),  0);
    check_i("is_positive(INT_MIN)", is_positive(INT_MIN), 0);

    /* --- 浮点位级操作（对照真机算术） --- */
    check_f("float_neg(2.0)",  float_neg(f2u(2.0f)),  f2u(-2.0f));
    check_f("float_abs(-3.5)", float_abs(f2u(-3.5f)), f2u(3.5f));
    check_f("float_twice(1.0)",    float_twice(f2u(1.0f)),  f2u(2.0f));
    check_f("float_twice(-0.25)",  float_twice(f2u(-0.25f)), f2u(-0.5f));
    /* 最小非规格化 2^-149 翻倍 = 最小规格化 2^-126 的前半: 0x00400000 → 0x00800000 */
    check_f("twice(2^-149)", float_twice(0x00000001u), 0x00000002u);
    check_f("twice(2^-127)", float_twice(0x00400000u), 0x00800000u);
    /* 最大有限 float 0x7F7FFFFF ×2 → +Inf 0x7F800000 */
    check_f("twice(MAXF)",   float_twice(0x7F7FFFFFu), 0x7F800000u);
    check_i("twice(+0)==+0", float_twice(0x00000000u) == 0x00000000u, 1);
    check_i("neg(NaN)=NaN",  float_neg(0x7FC00000u) == 0x7FC00000u, 1);

    printf("%s (%d failures)\n", fails ? "RESULT: SOME TESTS FAILED" : "RESULT: ALL PASSED", fails);
    return fails != 0;
}
