#include <stdio.h>

/* 动态库导出函数（L13）。Linux: libdyn.so；Windows: dyn.dll。
 * 构建见 Makefile / build.bat 的 dyn 目标。 */
void dyn_greet(const char *who)
{
    printf("[libdyn] hello %s —— 本消息来自运行期装载的共享库\n", who);
}
