#include "common.h"

/* 暂定义(tentative definition)：C89 语义下等价于未初始化全局，
 * 老 gcc(-fcommon) 按"弱符号"处理 —— CSAPP 规则 3 的温床。
 * GCC≥10 默认 -fno-common： Tentative 变强定义，与 strongdef.o 同链会报
 * multiple definition（现代收紧，见 README 实验①）。 */
int shared_counter;

int weak_show(void)
{
    return shared_counter;   /* -fcommon 且链入 strongdef.o 时读到 100 */
}
