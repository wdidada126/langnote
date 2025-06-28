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
