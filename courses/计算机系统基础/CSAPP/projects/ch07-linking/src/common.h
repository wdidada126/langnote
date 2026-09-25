#ifndef COMMON_H
#define COMMON_H

/* vec.c */
int vec_addn(const int *v, int n);

/* weakdemo.c / strongdef.c —— L12 符号解析演示 */
extern int shared_counter;   /* 唯一定义：strongdef.c(强) / weakdemo.c(暂定义,弱) */
int  weak_show(void);

/* foo.c / bar.c —— 静态库链接顺序演示 */
int foo(void);               /* foo 依赖 bar */
int bar(void);

#endif
