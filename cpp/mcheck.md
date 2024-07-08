# mcheck

#include <mcheck.h>

https://www.man7.org/linux/man-pages/man3/mcheck.3.html

## mtrace

## 简介
mcheck是GNU C库提供的一种用于检测C程序内存一致性的工具，常被用于调试内存相关的问题，如内存泄漏、双重释放和内存越界等问题。
在使用mcheck时，需要在程序中包含mcheck.h头文件，以便获得与内存调试相关的函数和类型定义。例如，可以使用MCHECK_DISABLED、MCHECK_OK、MCHECK_FREE等枚举类型来表示不同的内存状态。为了启用mcheck的检测功能，需要调用mcheck()或mcheck_pedantic()函数，并传入一个错误处理函数，这个错误处理函数将在检测到内存异常时被调用。
在编译使用mcheck的程序时，需要确保编译器和链接器能够找到并正确处理mcheck.h头文件以及相关函数。通常情况下，这需要使用支持GNU C库的编译器，并在编译命令中加入相应的选项，如-g用于生成调试信息。
总的来说，通过包含mcheck.h头文件并在代码中正确使用mcheck提供的API，可以有效检测C程序中的内存问题。结合正确的编译选项和运行时环境设置，能够最大化利用mcheck工具的功能，帮助开发者定位并解决内存泄露、越界等棘手问题。
