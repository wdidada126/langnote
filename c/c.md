# c
ANSI C (C89/C90)  C99 C11 C17 C23
## c cppreference
https://en.cppreference.com/w/c/header.html

Ubuntu 22.04
头文件位置: 在Ubuntu 22.04中，<assert.h> 通常位于 /usr/include/assert.h。这是GCC编译器默认搜索的标准头文件之一。
库文件位置: C标准库(libc)的库文件一般位于 /usr/lib/x86_64-linux-gnu/（对于64位系统）。例如，glibc的主库文件可能是 libc.so.6。不过，请注意，<assert.h> 相关的功能是编译时包含的，并且链接时自动引用标准C库，因此你可能不会直接看到与assert.h对应的特定库文件。

## define LIBETPAN_EXPORT

在libetpan库中，LIBETPAN_EXPORT宏通常用于控制库函数和变量的导出行为，特别是在构建动态链接库（DLL）或共享对象（.so文件）时。这个宏的定义取决于编译环境（如操作系统和编译器）以及是否希望库函数对外部可见。
在Windows平台上，当使用Microsoft Visual Studio或其他支持DLL的编译器时，LIBETPAN_EXPORT可能会被定义为__declspec(dllexport)，这告诉编译器这些函数或变量应该从DLL中导出，以便其他程序（即DLL的客户端）可以链接到并使用它们。
在Unix-like系统（如Linux或macOS）上，当构建共享对象时，通常不需要在源代码中显式指定导出哪些函数或变量，因为默认情况下，所有非静态的函数和变量都是可见的。然而，为了跨平台兼容性和明确性，libetpan可能会定义LIBETPAN_EXPORT为一个空宏（例如#define LIBETPAN_EXPORT），或者在某些特定情况下（如果库需要更精细的控制导出哪些符号），它可能会使用编译器特定的属性或标记。
不过，在实际的libetpan源代码中，LIBETPAN_EXPORT的确切定义可能会根据库的版本和构建配置而有所不同。如果你正在查看libetpan的源代码或与之相关的文档，并且遇到了LIBETPAN_EXPORT，最好的做法是查看它在你所使用的构建环境中是如何被定义的。
对于大多数使用libetpan的开发者来说，除非你在构建自己的libetpan版本或需要深入了解库的导出机制，否则通常不需要直接关心LIBETPAN_EXPORT宏。你只需要确保在链接你的程序时正确地指定了libetpan库，就可以使用它提供的函数和类型了。
最后，如果你是在编写一个需要被其他程序链接的库，并且希望控制哪些符号被导出，那么了解和使用像__declspec(dllexport)（在Windows上）或GCC的__attribute__((visibility("default")))（在Unix-like系统上）这样的特性将会非常有用。但是，这通常是在编写库的内部实现时需要考虑的高级话题。



extern 

ANSI C
c89/90
99
11
17
23

c_version.png

清华大学 
C89的时候引入void，const，函数原型和函数声明，
C99引入bool，inline，for声明，long long，单行注释，
C11引入原子操作

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

cmake判断操作系统类型，也是类似的设计

c语言 内存模型

https://blog.csdn.net/csdn1571167656/article/details/50273403

## c
裸机程序，
c程序运行平台
Linux
Redis
nginx

complier gcc gdb

各种操作系统都提供了c api
glibc

ansi c
posix c

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

链接器和加载器 (豆瓣)  这本书很薄的，一个星期足够看完几次了。看完之后就可以理解你遇到的问题了：为什么不同版本的 g++ 的编译衍生产品混在会有大麻烦。

## 著名开源库 项目
Linux


### list map
tbox里面有

在C语言标准库中，并没有直接类似于其他高级语言中（如Python的list或map）那样的内置数据结构。C语言是一种相对底层的语言，其标准库主要提供了一些基础的函数和数据类型，用于实现数据的存储和操作，但并不包含复杂的数据结构如list或map。

然而，C语言提供了足够的基础元素（如数组、指针、结构体等），允许开发者自己实现类似list和map这样的数据结构。例如：

链表（Linked List）：链表可以通过结构体和指针在C语言中实现，每个节点包含数据和指向下一个节点的指针。通过动态分配内存，链表可以灵活地添加或删除节点，模拟出类似list的行为。
哈希表（Hash Table）：虽然C标准库中没有直接提供哈希表的实现，但开发者可以使用数组、链表和哈希函数等组合起来，手动实现一个哈希表。哈希表能够提供快速的插入、删除和查找操作，类似于map的功能。
需要注意的是，由于C语言标准库中没有直接提供这些复杂的数据结构，因此在使用时需要自己编写相应的代码来管理内存和逻辑。这既提供了灵活性，也要求开发者对内存管理有深入的理解。

总结来说，C语言标准库中没有直接类似于list或map的内置数据结构，但提供了足够的工具和元素来允许开发者自己实现这些数据结构。


在C语言中，由于标准库并未直接提供类似于其他高级语言中list和map这样的复杂数据结构，一些开源库便应运而生，以提供这些功能。以下是一些实现了list和map等数据结构的C语言开源库：

1. GLib
概述：GLib是GNOME项目的一个基础库，它提供了许多常用的数据结构和工具函数。这些数据结构包括链表、哈希表、队列、双向链表等，非常适合在C语言项目中使用。
特点：GLib的数据结构设计得既高效又易用，可以与其他C语言库和应用程序无缝集成。
应用：广泛应用于GNOME项目及其相关应用程序中，也适合其他需要高效数据结构的C语言项目。
2. uthash
概述：uthash是一个轻量级的哈希表实现，专为C语言程序设计。它提供了简单易用的API，可以方便地将数据结构与哈希表相关联。
特点：uthash的哈希表实现非常灵活，支持动态扩展和收缩，且内存管理高效。
应用：适合需要快速查找、插入和删除操作的应用程序，如缓存系统、索引构建等。
3. TinyCThread
注意：虽然TinyCThread主要提供线程相关功能，但它与数据结构的直接实现关系不大。但提到多线程时，通常意味着需要在多个线程之间共享和访问数据结构，因此在此提及。
概述：TinyCThread是一个小型的C线程库，提供了简单的线程创建、互斥锁、条件变量等功能。
特点：TinyCThread简单易用，且与平台兼容性好，可以方便地集成到C语言项目中以实现多线程编程。
4. Melon
概述：Melon是一个无依赖且开箱即用的开源C语言库，它提供了包括双向链表在内的多种数据结构实现。
特点：Melon的双向链表实现非常灵活，支持不同的使用场景，并且提供了详细的文档和示例代码。
应用：适合需要频繁插入和删除操作的应用程序，如实时数据处理、游戏开发等。
5. 其他库
除了上述提到的库外，还有一些其他的C语言开源库也提供了类似list和map的数据结构实现，如BSD的queue.h（提供了简单的链表和队列实现）、以及一些专门的哈希表库如uthash的变种或类似实现等。这些库各有特点，开发者可以根据具体需求选择合适的库来使用。

总结
在C语言中实现list和map等数据结构通常需要借助开源库或自己编写代码。上述提到的GLib、uthash、Melon等开源库都是不错的选择，它们提供了高效、易用的数据结构实现，并且可以与C语言项目无缝集成。开发者可以根据项目需求和个人喜好选择合适的库来使用。

### 气象

在气象领域，使用C、C++和Python语言进行数据处理、模型模拟和可视化分析是非常常见的。这些语言各自拥有强大的库和工具集，适用于气象数据的处理和分析。以下是一些在气象领域常用的库和工具：

C/C++
NetCDF (Network Common Data Form)
NetCDF是一种用于存储和分发科学数据的文件格式，广泛用于气象、海洋学等领域。C和C++都有NetCDF的库，允许你读写这种格式的文件。
官网：Unidata NetCDF
HDF5 (Hierarchical Data Format version 5)
HDF5是另一种用于存储和组织大量数据的文件格式，支持复杂的数据类型。气象数据经常以HDF5格式存储。
官网：HDF Group
ECCODES
ECCODES是欧洲中期天气预报中心（ECMWF）提供的一套库，用于解码和编码GRIB（General Regularly-distributed Information in Binary form）和BUFR（Binary Universal Form for the Representation of meteorological data）气象数据。
官网：ECCODES
Python
Python因其简洁的语法和丰富的库生态系统，在气象数据处理和分析中非常受欢迎。以下是一些常用的库：

NumPy
NumPy是Python的一个库，提供了大量的数学函数操作，特别是针对大型多维数组和矩阵。它是许多其他科学计算库的基础。
官网：NumPy
SciPy
SciPy是建立在NumPy之上的一个开源库，提供了更多的数学算法和函数，包括统计、优化、积分、插值、FFT、信号处理、线性代数等。
官网：SciPy
Matplotlib
Matplotlib是Python的一个绘图库，提供了类似于MATLAB的绘图系统。它非常适合生成高质量的图表，用于数据可视化。
官网：Matplotlib
Pandas
Pandas是一个强大的数据分析和操作库，提供了快速、灵活和表达式丰富的数据结构，旨在使“关系”或“标签”数据的处理工作变得既简单又直观。
官网：Pandas
xarray
xarray是一个用于N维数组数据的Python库，特别是针对气象和海洋科学中的大型数据集。它建立在NumPy和Pandas之上，提供了多维数组的高性能接口。
官网：xarray
MetPy
MetPy是一个专注于气象学的Python包，它利用NumPy、SciPy、matplotlib和Pandas等库，为气象数据的处理和分析提供了便利的工具。
官网：MetPy
Cartopy
Cartopy是一个Python包，用于地图的绘制和地理数据处理。它基于matplotlib，提供了广泛的地图投影、坐标系统和地图边界绘制功能。
官网：Cartopy
使用这些库和工具，你可以高效地处理和分析气象数据，进行模型模拟，以及制作专业的数据可视化图表。


### c win head file

C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\ucrt

## C 语言综合笔记（截至 2026-08）

### 标准、实现与平台 API 的边界

C 是一门小而底层的语言标准；实际项目同时依赖编译器、C 标准库、ABI、操作系统和第三方库。`<stdio.h>`、`<stdint.h>`、`<stdlib.h>` 属于 ISO C 标准库；`<pthread.h>`、`<unistd.h>`、`<sys/socket.h>` 通常属于 POSIX/Unix；Win32 API、glibc 扩展、MSVC CRT 则是平台/实现特有能力。可移植代码必须把这些层次分开，不能把“Linux 上能编译”当成标准 C 保证。

当前 C 标准为 C23，即 ISO/IEC 9899:2024；C17（ISO/IEC 9899:2018）基本是对 C11 的缺陷修正，并没有旧文所列的大量新语言/库特性。C11 才引入 `_Generic`、原子类型、`_Thread_local`、`<threads.h>` 等；C23 引入或标准化了 `nullptr`、`true`/`false` 关键字、属性、`_BitInt`、`#embed`、`#warning` 等能力。实际采用前必须检查目标 GCC/Clang/MSVC、libc 和嵌入式工具链的支持，使用 feature-test macro 或配置探测，而不是只按标准名称开启编译选项。

官方/参考入口：

- WG14 C 标准主页：https://open-std.org/jtc1/sc22/wg14/
- C23 项目状态：https://www9.open-std.org/JTC1/SC22/WG14/www/projects.html
- C23 特性参考：https://en.cppreference.com/w/c/23

| 层次 | 例子 | 工程含义 |
| --- | --- | --- |
| ISO C | `malloc`、`qsort`、`stdio` | 最广可移植性，但能力有限。 |
| POSIX | 文件描述符、socket、pthread、`poll` | Unix/Linux/macOS 常用，需要处理平台差异。 |
| libc/编译器扩展 | glibc、musl、GCC attributes、MSVC intrinsics | 性能/功能强，但要封装和声明兼容边界。 |
| 硬件/裸机 | MMIO、ISR、启动代码 | 需要 volatile、内存屏障、链接脚本和芯片手册。 |

### 对象、指针、生命周期与未定义行为

C 给的是地址和字节，不是自动资源管理。数组在大多数表达式中衰变为指针，指针不携带长度、所有权或有效期；函数参数中的 `T a[]` 本质上也是 `T *a`。设计接口时必须把长度、容量、所有权、可空性、编码和失败语义写入名称、类型、注释与测试。

```c
/* dst 至少有 cap 字节；返回 0 成功，-1 表示空间不足。 */
int copy_text(char *dst, size_t cap, const char *src) {
    if (cap == 0) return -1;
    int n = snprintf(dst, cap, "%s", src);
    return n >= 0 && (size_t)n < cap ? 0 : -1;
}
```

高风险错误包括：越界读写、use-after-free、double free、返回栈变量地址、未初始化读取、整数截断/符号转换、`printf` 格式与实参不匹配、无效指针算术、错误的对齐/严格别名假设、signed overflow、data race。它们很多属于 undefined behavior（UB），并非“偶尔崩溃”而是编译器可基于其不会发生而重排或删除代码。优化级别、架构、编译器或一次无关改动都可能改变表现。

安全规则：

1. 用 `size_t` 表示对象大小/索引，用固定宽度整数表达协议和磁盘格式；所有外部长度先做上界检查。
2. 初始化每个对象；释放后不再使用，必要时让拥有者指针置空，但不要把置空误认为消除了别名悬垂。
3. 避免 `strcpy`、`strcat`、`sprintf` 和不检查截断的复制；`strncpy` 也不保证 NUL 结尾。优先显式长度与 `snprintf`/受审计封装。
4. `const` 表示不经该接口修改，`restrict` 是优化承诺，`volatile` 不是线程同步原语；不要用它修复竞态。
5. 对网络、文件、环境变量、FFI 输入先校验，再解析；任何长度乘法先检查溢出。

### 错误处理、资源释放与 API 设计

C 没有异常和析构，常用约定是 `0` 成功、非零错误码，或返回值加 `errno`；库 API 应统一错误模型，避免调用方既要读返回值又要猜全局状态。错误信息用可检查枚举/错误码，日志附带操作、路径、fd、长度等上下文但不泄露密钥。

多资源初始化可采用单一 `cleanup:` 标签，清理按反序执行。这不是滥用 `goto`，而是 C 中保持失败路径完整、避免重复和泄漏的常见模式。

```c
int process(const char *path) {
    FILE *f = NULL;
    char *buf = NULL;
    int rc = -1;

    f = fopen(path, "rb");
    if (f == NULL) goto cleanup;
    buf = malloc(BUFSIZ);
    if (buf == NULL) goto cleanup;
    /* 使用 f 和 buf，任何失败转到 cleanup。 */
    rc = 0;
cleanup:
    free(buf);
    if (f != NULL) fclose(f);
    return rc;
}
```

库边界应导出稳定的 C ABI：头文件使用 include guard、`extern "C"` 兼容 C++、可见性宏、明确结构体所有权和 allocator 归属。不要跨不同 CRT/allocator 分配与释放同一对象；跨 DLL/so 接口优先由“创建方提供 destroy 函数”，避免调用方 `free` 不同运行时分配的内存。

### 并发与内存模型

C11 提供 `<stdatomic.h>` 与 `<threads.h>`，但许多系统项目仍用 pthread/平台线程。没有同步的并发读写是 data race，也是 UB。mutex、condition variable、原子操作和线程创建/join 定义了 happens-before；`volatile` 只适用于某些 MMIO/信号相关场景，不能保证原子性、互斥或跨核可见性。

| 需求 | 合适工具 | 常见错误 |
| --- | --- | --- |
| 复合共享状态 | mutex | 只把一个 flag 声明为 volatile。 |
| 单一计数/状态转换 | C11 atomics | 用普通 `++` 并发累加。 |
| 条件等待 | mutex + condition variable | 不在循环中检查谓词，忽略虚假唤醒。 |
| 硬件寄存器 | `volatile` + 平台屏障/手册 | 把 volatile 当通用线程安全机制。 |

原子内存序和 lock-free 只在 profile 证明 mutex 成为瓶颈且团队能证明正确性时使用；大多数业务代码使用默认顺序一致原子或 mutex 更可维护。线程退出不自动回收其访问过的对象，所有权、join、取消和队列关闭仍需设计。

### 编译、链接、测试与安全工具

建议将警告视为错误并持续构建：GCC/Clang 可从 `-Wall -Wextra -Wpedantic -Werror` 起步，再按项目添加转换、格式和阴影警告。调试使用 `-g -O0` 或适当优化；发布使用明确 `-O2`/`-O3` 并保留符号文件。静态库只是对象文件归档，动态库涉及符号可见性、SONAME、rpath、加载器搜索路径和 ABI 兼容，不能只看头文件能否编译。

测试与诊断组合：单元/集成测试、fuzz、静态分析（clang-tidy、cppcheck 等）、AddressSanitizer、UndefinedBehaviorSanitizer、LeakSanitizer、ThreadSanitizer、Valgrind（适合特定平台/场景）、gdb/lldb、`perf`。Sanitizer 要在 CI 和预发布压测覆盖真实路径；它们不能证明没有漏洞，但能把很多潜伏内存错误提前变成可定位报告。

学习顺序：C 对象模型和声明 -> 指针/数组/字符串/整数 -> 生命周期/错误路径 -> 编译、链接、ELF/PE -> POSIX I/O、进程、线程和 socket -> sanitizer、调试和性能分析。仓库中的 [C11](c11.md)、[C23](c23.md)、[glibc](glibc.md)、[未定义行为](c_ub.md)、[lld](lld.md) 可进一步阅读。掌握 C 的标志不是能手写链表，而是能清楚说明每块内存谁分配谁释放、每个长度如何校验、每个线程如何同步以及失败路径如何回收。
