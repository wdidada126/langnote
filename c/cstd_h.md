# cstd_h

C语言标准库头文件是C语言编程中不可或缺的一部分，它们提供了大量的函数、宏和类型定义，以支持程序的各种功能。以下是一些常见的C语言标准库头文件及其功能的简要说明：

1. 通用头文件
stdio.h：标准输入输出库，包含进行输入输出操作的函数，如printf、scanf等。
stdlib.h：标准库函数，包含内存管理（如malloc、free）、随机数生成、字符串转换等函数。
string.h：字符串处理库，包含字符串操作函数，如strcpy、strcat、strlen等。
math.h：数学库，提供数学计算函数，如三角函数、指数函数、对数函数等。
time.h：时间处理库，提供时间和日期处理函数，如time、localtime、difftime等。
ctype.h：字符处理库，包含字符分类和转换函数，如isalpha、tolower等。
stdbool.h：布尔类型库，定义布尔类型bool以及两个宏true和false。
errno.h：错误处理库，定义全局变量errno，用于表示错误码。
float.h：浮点数处理库，提供与浮点类型相关的常量和宏定义。
limits.h：各种类型变量的最值库，定义各种整数类型的最大值和最小值等。
stdarg.h：可变参数处理库，提供处理可变数量参数的宏和函数。
signal.h：信号处理库，提供信号处理函数，如signal、raise等。
locale.h：本地化库，提供本地化函数，用于处理特定地域的设置。
2. 其他特定头文件
fenv.h：浮点数环境库，提供控制浮点数运算行为的函数和宏。
inttypes.h：整数类型库，定义了一些用于处理整数类型的宏和函数，提供跨平台的整数类型定义。
stdint.h：整型定义库，定义了一系列固定宽度的整数类型，如int8_t、int16_t等。
wchar.h：宽字符处理库，提供宽字符（wchar_t类型）处理函数和宏定义。
wctype.h：宽字符分类库，提供宽字符分类函数，如iswalnum、iswspace等。
3. 注意事项
不同编译器和平台对C语言标准库的支持程度可能有所不同，因此在编写跨平台代码时需要注意兼容性问题。
随着C语言标准的发展（如C99、C11、C17等），标准库头文件也在不断扩展和更新，因此建议查阅最新的C语言标准文档以获取最全面的信息。
以上内容基本涵盖了C语言标准库的主要头文件及其功能。这些头文件是C语言编程中不可或缺的工具，掌握它们对于编写高效、可移植的C语言程序至关重要。


ubuntu20

/usr/include/stdio.h
/usr/include/stdlib.h
/usr/include/string.h
/usr/include/math.h
/usr/include/time.h
/usr/include/ctype.h
/usr/include/errno.h
/usr/include/limits.h
/usr/include/signal.h