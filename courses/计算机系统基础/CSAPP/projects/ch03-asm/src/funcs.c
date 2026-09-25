/*
 * ch03-asm —— CSAPP Ch.3 机器级程序：小型 C 函数集
 * 关联讲次：L04(操作数/算术) L05(控制流) L06(过程/栈帧) L07(结构/对齐)
 *
 * 用法（Linux）:  gcc -Og -std=c99 -Wall -c src/funcs.c && objdump -d src/funcs.o
 * 用法（Windows）: cl /O2 /Fafuncs.asm src\funcs.c   （/Fa 输出 .asm 清单）
 * 逐函数注释里给出 x86-64 (System V ABI, -Og) 下的"预期汇编要点"，
 * 对照反汇编逐条验证即是Bomb Lab 的逆向训练。
 */
#include "funcs.h"
#include <stdio.h>
#include <string.h>

/* L04：最简单的寄存器参数 → lea/add。
 * 预期: movl %edi, %eax; addl %esi, %eax; ret  （或 lea (%rdi,%rsi), %eax） */
int add(int a, int b)
{
    return a + b;
}

/* L04：7 个参数 → 前 6 个走 rdi/rsi/rdx/rcx/r8/r9，第 7 个在栈上 8(%rsp)（call 压返回地址后为 16(%rsp)）。
 * 预期: subq $N,%rsp 开栈放第 7 参；加法用 lea 组合；结果 %eax */
long scale7(long a, long b, long c, long d, long e, long f, long g)
{
    return a + 2*b + 4*c + g;
}

/* L05：三目 → 可能编译成 cmov（无分支）。
 * 预期: cmpl $10, %edi; cmovl/cmovge 组合，或直接 setl+算术 */
int pick(int x)
{
    return x < 10 ? 1 : 2;
}

/* L05：while 规范化为 do-while + guard。
 * 预期: 先 testle/cmpl 判空(n<=0 直接返回 0)，循环体 addq+cmpq+jl */
long sum_to_n(long n)
{
    long s = 0, i;
    for (i = 1; i <= n; i++)
        s += i;
    return s;
}

/* L06：递归 → 帧链。callee-saved 的 rbx/rbp 或本地保存 n。
 * 预期: 保存返回地址与 n；测试 n==0；递归调用后 imulq %rbx, %rax */
long rfact(long n)
{
    return n <= 1 ? 1 : n * rfact(n - 1);
}

/* L07：结构访问 = 基址 + 编译期偏移；double b 因 8 对齐被垫到偏移 8。
 * 预期: movl (%rdi), %eax → 加 1；movsd 8(%rdi) 读 double；movb 16(%rdi) */
int bump(struct rec *r)
{
    r->a += 1;
    r->b *= 2.0;
    r->c = (char)(r->a & 0x7F);
    return (int)sizeof(struct rec);      /* 运行期常量：24（8 对齐） */
}

/* L07/Ch3.9：行主序二维数组 A[i][j] = *(A + i*stride + j)：
 * 外层指针 A 存的是"第 i 行的行首地址"，寻址需两次解引用。
 * 预期: movq (%rdi,%rsi,8), %rax; 再对 %eax 按 4 倍偏移读取 */
int row_sum(int **A, long i, long n)   /* A: n×n 行指针数组 */
{
    long j;
    int s = 0;
    for (j = 0; j < n; j++)
        s += A[i][j];
    return s;
}

/* L06：xor-swap 展示指针=内存操作数：movl (%rdi),%eax / (%rsi),%ecx 交替异或回写 */
void xor_swap(int *p, int *q)
{
    if (p != q) {
        *p ^= *q;
        *q ^= *p;
        *p ^= *q;
    }
}

/* 自驱动 main：打印各函数结果，防止链接器裁剪并给出可见输出 */
int main(void)
{
    struct rec r;
    int row0[3] = {1, 2, 3};
    int row1[3] = {10, 20, 30};
    int *A[2] = { row0, row1 };

    memset(&r, 0, sizeof r);
    r.a = 41; r.b = 0.5; r.c = 'z';

    printf("add(2,3)      = %d\n", add(2, 3));
    printf("scale7        = %ld\n", scale7(1, 1, 1, 1, 1, 1, 1));
    printf("pick(5)/pick(50) = %d/%d\n", pick(5), pick(50));
    printf("sum_to_n(100) = %ld\n", sum_to_n(100));
    printf("rfact(5)      = %ld\n", rfact(5));
    printf("bump: a=%d b=%.1f c=%c sizeof=%d\n", r.a + 1, r.b * 2, (char)('a' + 1), (int)sizeof(struct rec));
    bump(&r);
    printf("after bump: a=%d b=%.1f\n", r.a, r.b);
    printf("row_sum(A,1,3) = %d\n", row_sum(A, 1, 3));
    {
        int x = 7, y = 9;
        xor_swap(&x, &y);
        printf("xor_swap -> x=%d y=%d\n", x, y);
    }
    return 0;
}
