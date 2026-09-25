#include "common.h"

/* liba 侧：foo 依赖 bar。若归档顺序把 libb 放前、liba 放后，
 * 链接器处理 libb 时 bar 无人引用 → 丢弃 → 最终未定义符号 foo/bar。 */
int foo(void)
{
    return bar() + 1;   /* 期望 43 */
}
