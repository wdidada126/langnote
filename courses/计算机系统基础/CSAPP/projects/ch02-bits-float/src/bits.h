#ifndef BITS_H
#define BITS_H
/*
 * ch02-bits-float —— CSAPP Ch.2 位级整数/IEEE754 实验
 * 关联讲次：L02(整数/位运算) L03(浮点)；对应官方 Data Lab 风格。
 * 约定：以下函数尽量只用位级操作达成目的（不用 if 的函数标注 "bit-only"），
 *       全部基于 C 的无符号模 2^32 算术，规避未定义行为。
 */
int bit_and(int x, int y);          /* bit-only: x & y，仅用 ~ | */
int bit_count(int x);               /* 二进制 1 的个数 */
int bang(int x);                    /* bit-only: !x（0→1，非0→0） */
int sat_add(int x, int y);          /* 饱和加法：溢出时钳位到 INT_MAX/INT_MIN */
int is_positive(int x);             /* x>0 返回 1，否则 0（注意 INT_MIN 陷阱） */

unsigned float_neg(unsigned uf);    /* 取负；NaN(>0x7F800000) 原样返回 */
unsigned float_abs(unsigned uf);    /* 绝对值；NaN 原样返回 */
unsigned float_twice(unsigned uf);  /* uf*2，处理非规格化/溢出（位级实现） */
#endif
