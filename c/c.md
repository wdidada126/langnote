# c


大一C语言怎么快速入门
https://www.zhihu.com/question/273547272/answer/1992791314


C/C++跨平台的的预编译宏
https://blog.csdn.net/earbao/article/details/53307432

```c
#ifdef _WIN32
   //define something for Windows (32-bit and 64-bit, this part is common)
   #ifdef _WIN64
      //define something for Windows (64-bit only)
   #endif
#elif __APPLE__
    #include "TargetConditionals.h"
    #if TARGET_IPHONE_SIMULATOR
         // iOS Simulator
    #elif TARGET_OS_IPHONE
        // iOS device
    #elif TARGET_OS_MAC
        // Other kinds of Mac OS
    #else
    #   error "Unknown Apple platform"
    #endif
#elif __linux__
    // linux
#elif __unix__ // all unices not caught above
    // Unix
#elif defined(_POSIX_VERSION)
    // POSIX
#else
#   error "Unknown compiler"
#endif
```

c语言 内存模型

https://blog.csdn.net/csdn1571167656/article/details/50273403



ANSI C
c89/90





# c

c程序运行平台
Linux
complier gcc gdb





各种操作系统都提供了c api



动态链接

静态链接



假设你新开发一个操作系统NewOS

需要开放api，你会选择c



c适合嵌入式系统

cpp一般不用于开发http

c写驱动



串口通信



V大
如何学习tcp，从定时器开始



linxu c api

 https://wizardforcel.gitbooks.io/linux-c-api-ref/content/ 





问:对了，c语言标准库在windows上也是每个版本有一个自己的？

答:链接器和加载器 (豆瓣)  这本书很薄的，一个星期足够看完几次了。看完之后就可以理解你遇到的问题了：为什么不同版本的 g++ 的编译衍生产品混在会有大麻烦。

