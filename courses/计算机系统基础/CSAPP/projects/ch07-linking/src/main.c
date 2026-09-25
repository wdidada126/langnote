#include <stdio.h>
#include "common.h"

/* 链接规则 2/3（CSAPP 图 7-10）演示入口。
 * 默认构建里只链 weakdemo.o：int shared_counter; 暂定义 → 打印 0。
 * 实验（见 README"实验①"）：把 strongdef.o（int shared_counter=100;）
 * 一起链入 ——
 *   gcc -fcommon（老行为）：强胜弱 → 打印 100；
 *   gcc -fno-common（GCC≥10 默认）：直接 multiple definition 链接错误。
 * 两种结果都值得亲眼看到：前者是 CSAPP 的规则，后者是现代工具链的收紧。
 */
int main(void)
{
    int v[5] = { 1, 2, 3, 4, 5 };

    printf("vec_addn(1..5) = %d   (来自静态库 libvec.a/.lib)\n", vec_addn(v, 5));
    printf("shared_counter = %d   (暂定义未初始化 → .bss，默认 0)\n", weak_show());
    printf("foo()          = %d   (liba 依赖 libb：链接顺序即拓扑序)\n", foo());

    printf("\n观察: nm obj/main.o | grep shared ; readelf -S obj/weakdemo.o (bss)\n");
    printf("     objdump -d bin/static_demo | grep -A5 '<main>'\n");
    return 0;
}
