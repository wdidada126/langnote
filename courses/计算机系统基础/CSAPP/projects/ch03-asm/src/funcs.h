#ifndef FUNCS_H
#define FUNCS_H

/* struct rec：short 之后需 6 字节填充使 double 落到 8 对齐（L07） */
struct rec {
    int    a;    /* 偏移 0  */
    double b;    /* 偏移 8  */
    char   c;    /* 偏移 16 */
};               /* sizeof = 24（尾部再垫 7） */

int   add(int a, int b);
long  scale7(long a, long b, long c, long d, long e, long f, long g);
int   pick(int x);
long  sum_to_n(long n);
long  rfact(long n);
int   bump(struct rec *r);
int   row_sum(int **A, long i, long n);
void  xor_swap(int *p, int *q);

#endif
