# cpp


0级：掌握常见C++语法和语言构造，能够顺溜地写清楚各种语言构造（很多小白鼠死在这里）
1级：掌握基本的编程范式：面向过程、面向对象、泛型编程、以及C++11/14支持的函数式编程
2级：清楚编译器在 后面干了什么（compiler under the hood－考验功力的时候到了）
3级：清楚运行时内存模型（memory under the hood）
4级：对经典库（包括但不限于STL, BOOST, Folly）应用熟练，关键原理清晰，掌握设计模式
5级：熟悉至少一个操作系统常用API和内核，调试工具和方法
6级：有清晰的机器和系统模型:CPU, Memery, Cache, GPU, Disk, I/O, Process, Thread, TCP/IP...
7级：有一定系统级应用开发经验，被系统级应用的性能、内存、规模等问题折磨过，并解决过...
8级：从头到尾设计过一个C++库、或框架，并被一定量级的应用使用过
9级：设计并开发过系统级、高性能、大规模的软件系统
10级：成为Bjarne Stroustrup，设计一门语言
https://www.zhihu.com/question/19794858/answer/123988135

https://www.youtube.com/@cppweekly

libxml2

https://www.cnblogs.com/fnlingnzb-learner/p/7040726.html

linux是c语言写的，linux系统调用也是c语言？

Linux编程中C语言头文件位置
https://blog.csdn.net/weixin_43083491/article/details/107867222


Windows中C语言中的头文件一般分为两类，一类是标准库头文件，一类是用户自定义头文件。
1、标准库头文件，不同的编译器都不相同。
Vc6.0一般在安装目录下的\VC98\INCLUDE目录，比如C:\Program Files (x86)\Microsoft Visual Studio\VC98\INCLUDE。
Vs一般在位于$VSPATH\VC\include路径下面。
gcc一般默认在 /usr/include目录下。
2、用户自定义头文件，存储位置有用户自定义。


Mac中
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/bits

1.Linux中一些头文件的作用：

#include <assert.h>       //ANSI C。提供断言，assert(表达式) 
#include <glib.h>           //GCC。GTK，GNOME的基础库，提供很多有用的函数，如有数据结构操作函数 
#include <dirent.h>        //GCC。文件夹操作函数 
#include <ctype.h>        //ANSI C。字符测试函数。isdigit(),islower()等 
#include <errno.h>        //ANSI C。查看错误代码errno是调试程序的一个重要方法 
#include <getopt.h>     //处理命令行参数 
2.linux常用头文件如下：

//POSIX标准定义的头文件 
#include <dirent.h>        //目录项 
#include <fcntl.h>         //文件控制 
#include <fnmatch.h>       //文件名匹配类型 
#include <glob.h>          //路径名模式匹配类型 
#include <grp.h>           //组文件 
#include <netdb.h>         //网络数据库操作 
#include <pwd.h>           //口令文件 
#include <regex.h>           //正则表达式 
#include <tar.h>           //TAR归档值 
#include <termios.h>       //终端I/O 
#include <unistd.h>        //符号常量 
#include <utime.h>         //文件时间 
#include <wordexp.h>       //字符扩展类型 
//————————- 
#include <arpa/inet.h>     //INTERNET定义 
#include <net/if.h>        //套接字本地接口 
#include <netinet/in.h>    //INTERNET地址族 
#include <netinet/tcp.h>   //传输控制协议定义 
//————————- 
#include <sys/mman.h>      //内存管理声明 
#include <sys/select.h>    //Select函数 
#include <sys/socket.h>    //套接字借口 
#include <sys/stat.h>      //文件状态 
#include <sys/times.h>     //进程时间 
#include <sys/types.h>     //基本系统数据类型 
#include <sys/un.h>        //UNIX域套接字定义 
#include <sys/utsname.h>   //系统名 
#include <sys/wait.h>      //进程控制 
//—————————— 
//POSIX定义的XSI扩展头文件 
#include <cpio.h>          //cpio归档值 
#include <dlfcn.h>         //动态链接 
#include <fmtmsg.h>        //消息显示结构 
#include <ftw.h>           //文件树漫游 
#include <iconv.h>         //代码集转换使用程序 
#include <langinfo.h>      //语言信息常量 
#include <libgen.h>        //模式匹配函数定义 
#include <monetary.h>      //货币类型 
#include <ndbm.h>          //数据库操作 
#include <nl_types.h>      //消息类别 
#include <poll.h>          //轮询函数 
#include <search.h>        //搜索表 
#include <strings.h>       //字符串操作 
#include <syslog.h>        //系统出错日志记录 
#include <ucontext.h>      //用户上下文 
#include <ulimit.h>        //用户限制 
#include <utmpx.h>         //用户帐户数据库 
//—————————– 
#include <sys/ipc.h>       //IPC(命名管道) 
#include <sys/msg.h>       //消息队列 
#include <sys/resource.h>  //资源操作 
#include <sys/sem.h>       //信号量 
#include <sys/shm.h>       //共享存储 
#include <sys/statvfs.h>   //文件系统信息 
#include <sys/time.h>      //时间类型 
#include <sys/timeb.h>     //附加的日期和时间定义 
#include <sys/uio.h>       //矢量I/O操作 
//—————————— 
//POSIX定义的可选头文件 
#include <aio.h>           //异步I/O 
#include <mqueue.h>        //消息队列 
#include <pthread.h>       //线程 
#include <sched.h>         //执行调度 
#include <semaphore.h>     //信号量 
#include <spawn.h>         //实时spawn接口 
#include <stropts.h>       //XSI STREAMS接口 
#include <trace.h>         //事件跟踪 
3.C/C++头文件一览：

//C 
#include <assert.h>　　　　//设定插入点 
#include <ctype.h>　　　　 //字符处理 
#include <errno.h>　　　　 //定义错误码 
#include <float.h>　　　　 //浮点数处理 
#include <iso646.h>        //对应各种运算符的宏 
#include <limits.h>　　　　//定义各种数据类型最值的常量 
#include <locale.h>　　　　//定义本地化C函数 
#include <math.h>　　　　　//定义数学函数 
#include <setjmp.h>        //异常处理支持 
#include <signal.h>        //信号机制支持 
#include <stdarg.h>        //不定参数列表支持 
#include <stddef.h>        //常用常量 
#include <stdio.h>　　　　 //定义输入／输出函数 
#include <stdlib.h>　　　　//定义杂项函数及内存分配函数 
#include <string.h>　　　　//字符串处理 
#include <time.h>　　　　　//定义关于时间的函数 
#include <wchar.h>　　　　 //宽字符处理及输入／输出 
#include <wctype.h>　　　　//宽字符分类 
 
//传统C++ 
#include <fstream.h>　　　 //改用<fstream> 
#include <iomanip.h>　　　 //改用<iomainip> 
#include <iostream.h>　　　//改用<iostream> 
#include <strstrea.h>　　　//该类不再支持，改用<sstream>中的stringstream 
//———————————————————————————————— 
 
//标准C++ 
#include <algorithm>　　　 //STL 通用算法 
#include <bitset>　　　　　//STL 位集容器 
#include <cctype>          //字符处理 
#include <cerrno> 　　　　 //定义错误码 
#include <cfloat>　　　　 //浮点数处理 
#include <ciso646>         //对应各种运算符的宏 
#include <climits> 　　　　//定义各种数据类型最值的常量 
#include <clocale> 　　　　//定义本地化函数 
#include <cmath> 　　　　　//定义数学函数 
#include <complex>　　　　 //复数类 
#include <csignal>         //信号机制支持 
#include <csetjmp>         //异常处理支持 
#include <cstdarg>         //不定参数列表支持 
#include <cstddef>         //常用常量 
#include <cstdio> 　　　　 //定义输入／输出函数 
#include <cstdlib> 　　　　//定义杂项函数及内存分配函数 
#include <cstring> 　　　　//字符串处理 
#include <ctime> 　　　　　//定义关于时间的函数 
#include <cwchar> 　　　　 //宽字符处理及输入／输出 
#include <cwctype> 　　　　//宽字符分类 
#include <deque>　　　　　 //STL 双端队列容器 
#include <exception>　　　 //异常处理类 
#include <fstream> 　　　  //文件输入／输出 
#include <functional>　　　//STL 定义运算函数（代替运算符） 
#include <limits> 　　　　 //定义各种数据类型最值常量 
#include <list>　　　　　　//STL 线性列表容器 
#include <locale>          //本地化特定信息 
#include <map>　　　　　　 //STL 映射容器 
#include <memory>          //STL通过分配器进行的内存分配 
#include <new>             //动态内存分配 
#include <numeric>         //STL常用的数字操作 
#include <iomanip> 　　　  //参数化输入／输出 
#include <ios>　　　　　　 //基本输入／输出支持 
#include <iosfwd>　　　　　//输入／输出系统使用的前置声明 
#include <iostream> 　　 　//数据流输入／输出 
#include <istream>　　　　 //基本输入流 
#include <iterator>        //STL迭代器 
#include <ostream>　　　　 //基本输出流 
#include <queue>　　　　　 //STL 队列容器 
#include <set>　　　　　　 //STL 集合容器 
#include <sstream>　　　　 //基于字符串的流 
#include <stack>　　　　　 //STL 堆栈容器 
#include <stdexcept>　　　 //标准异常类 
#include <streambuf>　　　 //底层输入／输出支持 
#include <string>　　　　　//字符串类 
#include <typeinfo>        //运行期间类型信息 
#include <utility>　　　　 //STL 通用模板类 
#include <valarray>        //对包含值的数组的操作 
#include <vector>　　　　　//STL 动态数组容器 
//———————————————————————————————— 
 
//C99增加的部分 
#include <complex.h>　　 //复数处理 
#include <fenv.h>　　　　//浮点环境 
#include <inttypes.h>　　//整数格式转换 
#include <stdbool.h>　　 //布尔环境 
#include <stdint.h>　　　//整型环境 
#include <tgmath.h>　　　//通用类型数学宏 


### msvc标准库
https://learn.microsoft.com/zh-cn/cpp/standard-library/cpp-standard-library-header-files?source=recommendations&view=msvc-170


类别	标头
算法	<algorithm>, <cstdlib>, <numeric>
原子操作	<atomic>11
C 库包装器	<cassert>、<ccomplex>11 a b、<cctype>、<cerrno>、<cfenv>11、<cfloat>、<cinttypes>11、<ciso646>b、<climits>、<clocale>、<cmath>、<csetjmp>、<csignal>、<cstdalign>11 a b、<cstdarg>、<cstdbool>11 a b、<cstddef>、<cstdint>11、<cstdio>、<cstdlib>、<cstring>、<ctgmath>11 a b、<ctime>、<cuchar>11、<cwchar>、<cwctype>
概念	<concepts>20
容器	
序列容器	<array>11、<deque>、<forward_list>11、<list>、<vector>
有序的关联容器	<map>, <set>
无序的关联容器	<unordered_map>11、<unordered_set>11
容器适配器	<queue>, <stack>
容器视图	<span>20
错误和异常处理	<cassert>、<exception>、<stdexcept>、<system_error>11
常规实用工具	<any>17、<bit>20、<bitset>、<cstdlib>、<execution>17、<functional>、<memory>、<memory_resource>17、<optional>17、<ratio>11、<scoped_allocator>11、<tuple>11、<type_traits>11、<typeindex>11、<utility>、<variant>17
I/O 和格式设置	<cinttypes>11、<cstdio>、<filesystem>17、<fstream>、<iomanip>、<ios>、<iosfwd>、<iostream>、<istream>、<ostream>、<sstream>、<streambuf>、<strstream>c、<syncstream>20
迭代器	<iterator>
语言支持	<cfloat>、<climits>、<codecvt>11 a、<compare>20、<contract>20、<coroutine>20、<csetjmp>、<csignal>、<cstdarg>、<cstddef>、<cstdint>11、<cstdlib>、<exception>、<initializer_list>11、<limits>、<new>、<typeinfo>、<version>20
本地化	<clocale>、<codecvt>11 a、<cvt/wbuffer>、<cvt/wstring>、<locale>
数学和数字	<bit>20、<cfenv>11、<cmath>、<complex>、<cstdlib>、<limits>、<numeric>、<random>11、<ratio>11、<valarray>
内存管理	<allocators>、<memory>、<memory_resource>17、<new>、<scoped_allocator>11
多线程处理	<atomic>11、<condition_variable>11、<future>11、<mutex>11、<shared_mutex>14、<thread>11
范围	<ranges>20
正则表达式	<regex>11
字符串和字符数据	<charconv>17、<cctype>、<cstdlib>、<cstring>、<cuchar>11、<cwchar>、<cwctype>、<regex>11、<string>、<string_view>17
时间	<chrono>11、<ctime>


有一本书 c++标准库2
Nicolai M.Josuttis
http://www.josuttis.com/



https://zh.cppreference.com/w/cpp/language/namespace


c++ set使用过后需要delete吗？
new分配的内存在堆上，必须程序员自己用delete，而局部变量和函数参数分配的内存在堆栈上，自动释放，由系统完成。


delete和delete[]的使用规范
对于每个由new操作符号创建的基本数据类型的对象,都需要由一个delete去进行内存回收,这是每个C++程序猿在使用堆时的基本操守。
对于new []操作符动创建的基本数据类型的数组(元素是基本数据类型),只需执行delete[]操作符一次性回收内存。
根据RAII原则，在类的构造函数中由new初始化的指针类型的属性,同时在必须在其解构函数中具有对应的delete操作,这个对于new[]和delete[]也同样使用。

作者：铁甲万能狗
链接：https://www.jianshu.com/p/b87329ceca4d
https://www.cnblogs.com/1zhk/articles/5028743.html
https://www.cnblogs.com/chinsonliu/p/3603168.html

在线编译器
https://coliru.stacked-crooked.com/

### namespace

https://www.cnblogs.com/zhoug2020/p/5972439.html


模板元编程

cpp框架会使用各种cpp语言特性

98年增加stl

融汇 C++ Core Guidelines、SEI CERT、MISRA 等权威规范体系


### 代码检查工具
java snoar

mac命令行编译c cpp代码

gcc c
g++ c++代码

g++ -llibstdc++ 之类的代码，不然报错

问：set list区别

list
封装链表，以链表形式实现，不支持[]运算符。
对随机访问的速度很慢(需要遍历整个链表)，插入数据很快(不需要拷贝和移动数据，只需改变指针的指向)。
新添加的元素，list可以任意加入。
vector
封装数组，使用连续内存存储，支持[]运算符。
对随机访问的速度很快，对头插元素速度很慢，尾插元素速度很快
新添加的元素，vector有一套算法。

protobuf
https://cbs.centos.org/koji/buildinfo?buildID=28989


centos 如何检查动态库是否存在

问：像IDEA 写java项目，关联src.zip一样，源码调试

java se 8 api
https://docs.oracle.com/javase/8/docs/api/index.html

Clion 有所有头文件列表
libstdc++ 7 api
https://gcc.gnu.org/onlinedocs/libstdc++/index.html


按照不同的功能，C++的标准库包含了如下内容：
1，Concepts
C++20新增的。
<concepts>
2，Coroutines
C++20新增的。
<coroutine>
3，Ranges
C++20新增的。
<ranges>
4，工具类
C++17新增了<any> 、<optional>、 <variant>，C++20新增了<compare>、<version>、<source_location>。
<cstdlib>
<csignal>
<csetjmp>
<cstdarg>
<typeinfo>
<typeindex>
<type_traits>
<bitset>
<functional>
<utility>
<ctime>
<chrono>
<cstddef>
<initializer_list>
<tuple>
<any>
<optional>
<variant>
<compare>
<version>
<source_location>
5，容器部分
C++20新增了<span>。
<array>
<vector>
<deque>
<list>
<forward_list>
<set>
<map>
<unordered_set>
<unordered_map>
<stack>
<queue>
<span>
6，iterator
C++20增添了很多iterator类。
<iterator>
7，线程支持
C++20新增了<stop_token>、<semaphore>、<latch>、 <barrier>。
<thread>
<stop_token>
<mutex>
<shared_mutex>
<future>
<condition_variable>
<semaphore>
<latch>
<barrier>
<atomic>
8，通用算法
C++17新增了<execution>。
<algorithm>
<execution>
<algorithm>中包含的算法有：all_of、any_of、none_of、for_each、find、find_if、find_if_not、find_end、find_first_of、adjacent_find、count、count_if、mismatch、equal、is_permutation、search、search_n、copy、copy_n、copy_if、copy_backward、move、move_backward、swap、swap_ranges、iter_swap、transform、replace、replace_if、replace_copy、replace_copy_if、fill、fill_n、generate、generate_n、remove、remove_if、remove_copy、remove_copy_if、unique、unique_copy、reverse、reverse_copy、rotate、rotate_copy、random_shuffle、shuffle、is_partitioned、partition、stable_partition、partition_copy、partition_point、sort、stable_sort、partial_sort、partial_sort_copy、is_sorted、is_sorted_until、nth_element、lower_bound、upper_bound、equal_range、binary_search、merge、inplace_merge、includes、set_union、set_intersection、set_difference、set_symmetric_difference、push_heap、pop_heap、make_heap、sort_heap、is_heap、is_heap_until、min、max、minmax、min_element、max_element、minmax_element、lexicographical_compare、next_permutation、prev_permutation。
9，动态内存和智能指针
C++17新增了memory_resource。
<new>
<memory>
<scoped_allocator>
<memory_resource>
10，字符串
C++17新增了<string_view>、<charconv>，C++20新增了<format>。
<cctype>
<cwctype>
<cstring>
<cwchar>
<cuchar>
<string>
<string_view>
<charconv>
<format>
<regex>
11，本地化
<codecvt>在C++17废弃。
<locale>
<clocale>
<codecvt>
12，stream和io
C++20新增了<syncstream>。
<iosfwd>
<ios>
<istream>
<ostream>
<iostream>
<fstream>
<sstream>
<syncstream>
<strstream>
<iomanip>
<streambuf>
<cstdio>
13，文件系统
C++17新增的。
<filesystem>
14，数值库
C++20新增了<bit>、<numbers>。
<climits>
<cfloat>
<cstdint>
<cinttypes>
<limits>
<cmath>
<complex>
<valarray>
<random>
<numeric>
<ratio>
<cfenv>
<bit>
<numbers>
15，语言特性支持
<exception>
<limits>
<new>
<typeinfo>
16，时间
<chrono>
17，错误和异常处理
<exception>
<stdexcept>
<cassert>
<system_error>
<cerrno>
最后，不是每个系统上的C++编译都使用了标准的C++特性。这里的系统主要是手机操作系统，比如Android。ndk-build可能默认将异常、RTTI等功能停用。




cpp
libstdc++
libstdc++ 库的源码其实就在 gcc 的源码中，gcc源码 有个目录 libstdc++-v3 ,就是它


在GNU/Linux上，我们使用的C++库都是GNU实现的libstdc++（/usr/lib/gcc/x86_64-linux-gnu/9/libstdc++.so、/usr/lib/gcc/x86_64-linux-gnu/9/libstdc++.a）；
在MacOS、iOS上，我们使用的C++库都是LLVM项目实现的libc++（/usr/lib/libc++.dylib）；
在Android上，我们使用的C++库为LLVM的libc++（NDK r18以前还是支持GNU的libstdc++的，在r18上被完全去除）；注意这可不是系统库，你需要将库文件包含在apk中（Android上的系统库是/system/lib/libstdc++.so，这不是GNU的那个，只包含了最小的C++ runtime实现，如new delete等）；


https://zhuanlan.zhihu.com/p/291496862
很重要啊
有哪些库
编译时链接了libstdc++、libm、libgcc_s、libgcc、libc库；
编译时链接了Scrt1.o、crti.o、crtbeginS.o、crtendS.o、crtn.o。


```shell
ldd testjsoncpp 
	linux-vdso.so.1 =>  (0x00007ffcd52f8000)
	libjsoncpp.so.0 => /lib64/libjsoncpp.so.0 (0x00007f4bde499000)
	libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f4bde191000)
	libm.so.6 => /lib64/libm.so.6 (0x00007f4bdde8f000)
	libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007f4bddc79000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f4bdd8ab000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f4bde6d0000)
```

C++库如何被使用

``
```shell
 -m elf_x86_64
 -dynamic-linker /lib64/ld-linux-x86-64.so.2
 -pie
 /usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/Scrt1.o
 /usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/crti.o
 /usr/lib/gcc/x86_64-linux-gnu/9/crtbeginS.o
 -lstdc++
 -lm
 -lgcc_s
 -lgcc
 -lc
 /usr/lib/gcc/x86_64-linux-gnu/9/crtendS.o
 /usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/crtn.o
 ```


```shell
rpm -ql gcc-c++.x86_64 0:4.8.5-44.el7
/usr/bin/c++
/usr/bin/g++
/usr/bin/x86_64-redhat-linux-c++
/usr/bin/x86_64-redhat-linux-g++
/usr/lib/gcc
/usr/lib/gcc/x86_64-redhat-linux
/usr/lib/gcc/x86_64-redhat-linux/4.8.2
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libstdc++.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libstdc++.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libsupc++.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libstdc++.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.5
/usr/libexec/gcc
/usr/libexec/gcc/x86_64-redhat-linux
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/cc1plus
/usr/libexec/gcc/x86_64-redhat-linux/4.8.5
/usr/share/doc/gcc-c++-4.8.5
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1993.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1994.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1995.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1996.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1997.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1998.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-1999.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2000.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2001.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2002.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2003.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2004.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2005.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2006.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2007.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2008.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2009.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2010.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2011.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog-2012.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog.ptr.bz2
/usr/share/doc/gcc-c++-4.8.5/ChangeLog.tree-ssa.bz2
/usr/share/man/man1/g++.1.gz
```


```shell
rpm -ql cpp.x86_64
/usr/bin/cpp
/usr/lib/cpp
/usr/libexec/gcc
/usr/libexec/gcc/x86_64-redhat-linux
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/cc1
/usr/libexec/gcc/x86_64-redhat-linux/4.8.5
/usr/share/info/cpp.info.gz
/usr/share/info/cppinternals.info.gz
/usr/share/locale/be/LC_MESSAGES/cpplib.mo
/usr/share/locale/ca/LC_MESSAGES/cpplib.mo
/usr/share/locale/da/LC_MESSAGES/cpplib.mo
/usr/share/locale/de/LC_MESSAGES/cpplib.mo
/usr/share/locale/el/LC_MESSAGES/cpplib.mo
/usr/share/locale/eo/LC_MESSAGES/cpplib.mo
/usr/share/locale/es/LC_MESSAGES/cpplib.mo
/usr/share/locale/fi/LC_MESSAGES/cpplib.mo
/usr/share/locale/fr/LC_MESSAGES/cpplib.mo
/usr/share/locale/id/LC_MESSAGES/cpplib.mo
/usr/share/locale/ja/LC_MESSAGES/cpplib.mo
/usr/share/locale/nl/LC_MESSAGES/cpplib.mo
/usr/share/locale/pt_BR/LC_MESSAGES/cpplib.mo
/usr/share/locale/ru/LC_MESSAGES/cpplib.mo
/usr/share/locale/sr/LC_MESSAGES/cpplib.mo
/usr/share/locale/sv/LC_MESSAGES/cpplib.mo
/usr/share/locale/tr/LC_MESSAGES/cpplib.mo
/usr/share/locale/uk/LC_MESSAGES/cpplib.mo
/usr/share/locale/vi/LC_MESSAGES/cpplib.mo
/usr/share/locale/zh_CN/LC_MESSAGES/cpplib.mo
/usr/share/locale/zh_TW/LC_MESSAGES/cpplib.mo
/usr/share/man/man1/cpp.1.gz
```

```shell
rpm -ql gcc.x86_64
/usr/bin/c89
/usr/bin/c99
/usr/bin/cc
/usr/bin/gcc
/usr/bin/gcc-ar
/usr/bin/gcc-nm
/usr/bin/gcc-ranlib
/usr/bin/gcov
/usr/bin/x86_64-redhat-linux-gcc
/usr/lib/gcc
/usr/lib/gcc/x86_64-redhat-linux
/usr/lib/gcc/x86_64-redhat-linux/4.8.2
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtbegin.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtbeginS.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtbeginT.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtend.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtendS.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtfastmath.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtprec32.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtprec64.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/crtprec80.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libasan.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libasan.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libasan_preinit.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libatomic.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libatomic.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgcc.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgcc_eh.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgcc_s.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgcov.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgomp.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libgomp.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libitm.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libitm.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libmudflap.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libmudflap.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libmudflapth.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libmudflapth.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libquadmath.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/libquadmath.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtbegin.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtbeginS.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtbeginT.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtend.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtendS.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtfastmath.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtprec32.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtprec64.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/crtprec80.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/adxintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/ammintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/avx2intrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/avxintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/bmi2intrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/bmiintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/bmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/cpuid.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/cross-stdarg.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/emmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/f16cintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/float.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/fma4intrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/fmaintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/fxsrintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/ia32intrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/immintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/iso646.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/limits.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/lwpintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/lzcntintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/mm3dnow.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/mm_malloc.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/mmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/nmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/omp.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/pkuintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/pmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/popcntintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/prfchwintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/rdseedintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/rtmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/smmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdalign.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdarg.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdbool.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stddef.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdfix.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdint-gcc.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdint.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/stdnoreturn.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/syslimits.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/tbmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/tmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/unwind.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/varargs.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/wmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/x86intrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/xmmintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/xopintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/xsaveintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/xsaveoptintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/include/xtestintrin.h
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libasan.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libasan_preinit.o
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libatomic.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libcloog-isl.so.4
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgcc.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgcc_eh.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgcc_s.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgcov.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgomp.a
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgomp.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libgomp.spec
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libitm.spec
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/libtsan.so
/usr/lib/gcc/x86_64-redhat-linux/4.8.2/rpmver
/usr/lib/gcc/x86_64-redhat-linux/4.8.5
/usr/libexec/gcc
/usr/libexec/gcc/x86_64-redhat-linux
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/collect2
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/liblto_plugin.so
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/liblto_plugin.so.0
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/liblto_plugin.so.0.0.0
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/lto-wrapper
/usr/libexec/gcc/x86_64-redhat-linux/4.8.2/lto1
/usr/libexec/gcc/x86_64-redhat-linux/4.8.5
/usr/libexec/getconf
/usr/libexec/getconf/default
/usr/share/doc/gcc-4.8.5
/usr/share/doc/gcc-4.8.5/COPYING
/usr/share/doc/gcc-4.8.5/COPYING.LIB
/usr/share/doc/gcc-4.8.5/COPYING.RUNTIME
/usr/share/doc/gcc-4.8.5/COPYING3
/usr/share/doc/gcc-4.8.5/COPYING3.LIB
/usr/share/doc/gcc-4.8.5/ChangeLog-1997.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-1998.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-1999.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2000.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2001.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2002.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2003.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2004.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2005.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2006.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2007.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2008.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2009.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2010.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2011.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog-2012.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.dataflow.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.graphite.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.lib.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.ptr.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.tree-ssa.bz2
/usr/share/doc/gcc-4.8.5/ChangeLog.tuples.bz2
/usr/share/doc/gcc-4.8.5/README.Portability
/usr/share/info/gcc.info.gz
/usr/share/info/gccgo.info.gz
/usr/share/info/gccinstall.info.gz
/usr/share/info/gccint.info.gz
/usr/share/locale/be/LC_MESSAGES/gcc.mo
/usr/share/locale/da/LC_MESSAGES/gcc.mo
/usr/share/locale/de/LC_MESSAGES/gcc.mo
/usr/share/locale/el/LC_MESSAGES/gcc.mo
/usr/share/locale/es/LC_MESSAGES/gcc.mo
/usr/share/locale/fi/LC_MESSAGES/gcc.mo
/usr/share/locale/fr/LC_MESSAGES/gcc.mo
/usr/share/locale/hr/LC_MESSAGES/gcc.mo
/usr/share/locale/id/LC_MESSAGES/gcc.mo
/usr/share/locale/ja/LC_MESSAGES/gcc.mo
/usr/share/locale/nl/LC_MESSAGES/gcc.mo
/usr/share/locale/ru/LC_MESSAGES/gcc.mo
/usr/share/locale/sr/LC_MESSAGES/gcc.mo
/usr/share/locale/sv/LC_MESSAGES/gcc.mo
/usr/share/locale/tr/LC_MESSAGES/gcc.mo
/usr/share/locale/vi/LC_MESSAGES/gcc.mo
/usr/share/locale/zh_CN/LC_MESSAGES/gcc.mo
/usr/share/locale/zh_TW/LC_MESSAGES/gcc.mo
/usr/share/man/man1/gcc.1.gz
/usr/share/man/man1/gcov.1.gz
```


```shell
rpm -ql devtoolset-7-gcc-c++
/opt/rh/devtoolset-7/root/usr/bin/c++
/opt/rh/devtoolset-7/root/usr/bin/g++
/opt/rh/devtoolset-7/root/usr/bin/x86_64-redhat-linux-c++
/opt/rh/devtoolset-7/root/usr/bin/x86_64-redhat-linux-g++
/opt/rh/devtoolset-7/root/usr/lib/gcc
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libstdc++.a
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libstdc++.so
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libstdc++_nonshared.a
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libstdc++fs.a
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libsupc++.a
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/libstdc++.so
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/libsupc++.a
/opt/rh/devtoolset-7/root/usr/libexec/gcc
/opt/rh/devtoolset-7/root/usr/libexec/gcc/x86_64-redhat-linux
/opt/rh/devtoolset-7/root/usr/libexec/gcc/x86_64-redhat-linux/7
/opt/rh/devtoolset-7/root/usr/libexec/gcc/x86_64-redhat-linux/7/cc1plus
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1993.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1994.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1995.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1996.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1997.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1998.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-1999.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2000.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2001.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2002.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2003.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2004.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2005.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2006.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2007.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2008.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2009.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2010.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2011.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2012.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2013.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2014.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2015.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog-2016.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog.ptr.bz2
/opt/rh/devtoolset-7/root/usr/share/doc/devtoolset-7-gcc-c++-7.3.1/ChangeLog.tree-ssa.bz2
/opt/rh/devtoolset-7/root/usr/share/man/man1/g++.1.gz
```


libstdc 在电脑上的位置
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/32/libstdc++.so
/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/libstdc++.so


cpp开源面试考点
https://github.com/huihut/interview

cpp 内存模型

https://www.cnblogs.com/alexcool/articles/9241548.html

`# define micro`

语法 宏定义 开关




```shell
rpm -pql glibc-2.17-222.el7.x86_64.rpm
/etc/gai.conf
/etc/ld.so.cache
/etc/ld.so.conf
/etc/ld.so.conf.d
/etc/nsswitch.conf
/etc/rpc
```

glibc安装之后才有
/etc/ld.so.cache
/etc/ld.so.conf
/etc/ld.so.conf.d


## 【C++11新特性】 C++11 智能指针之shared_ptr

[【C++11新特性】 C++11 智能指针之shared_ptr](https://mp.weixin.qq.com/s?__biz=MzA4MjU1MDk3Ng==&mid=2451527471&idx=1&sn=b79e69a8fa08d9a50482d26c9f6b8078&chksm=886ffe80bf187796bb0409abd0ef048bc87193ba9446f11a043f53ab72c574dda7ec100cdc07&mpshare=1&scene=1&srcid=&sharer_sharetime=1591591676122&sharer_shareid=656dda2d80ca9f13e1033837a79f6ca7&key=b6ae2d62a5369f54f5a0cbb2a6bead3ec77c45fd47c773dae0babea35dc0ed7ff0813d1178c1d45b8e16e9cc321ec27791bd87156e3abf0a889827db4dda298ee804e2142430d94b0cf9391de123ab00&ascene=1&uin=MjA3Nzg5NzE0MA%3D%3D&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&exportkey=AwjlRNqxJfJZaUx1TDKl%2BHU%3D&pass_ticket=qWSKwVT%2BRmHLU7aWuJRIoMVYvlcSm2qtH0zyYcAdURWIfd7N3Nluuva3nUFbEoF6)





cpp

其实我一点也不关心哪个网络库会进标准，反正我们都用自己的库。
就不要说陈硕了，他自己都不了解asio和ace，他把自己的网络库吹成了宇宙第一网络IO库，asio代码质量非常高，如果他看过asio的代码，他肯定不敢再吹他自己的网络库



https://google.github.io/styleguide/cppguide.html

pg c++访问



redis源码文件夹

Deps应该是depends的英文缩写，即它应该是依赖的库




符号表 linux 如何查看



https://blog.csdn.net/yangyihongyangjiying/article/details/44740045



nm





cpp参考手册

- man
- cppreference

cmake 编译

cmake是生成makfile等

bazel

https://blog.csdn.net/kris_fei/article/details/81982565



##### c++历史

知乎



##### c++编译器

Green Hills Software

不通平台，c++编译器不一样

Android clang

Mac clang

Windows VC





inline表达式，编译器直接展开？



mutable

volatile



[struct和typedef struct](https://www.cnblogs.com/qyaizs/articles/2039101.html)



开源 C++ 库列表

 https://zh.cppreference.com/w/cpp/links/libs 



2018年 微信以cpp为主，编译系统是自己开发的，本地编译，编辑器是vim



cpp template hpp 定义和实现都在头文件



开发库的安装，cpprestsdk为例

With [vcpkg](https://github.com/Microsoft/vcpkg) on Windows

```
PS> vcpkg install cpprestsdk cpprestsdk:x64-windows
```

With [apt-get](https://launchpad.net/ubuntu/+source/casablanca/2.8.0-2build2) on Debian/Ubuntu

```
$ sudo apt-get install libcpprest-dev
```

With [dnf](https://apps.fedoraproject.org/packages/cpprest) on Fedora

```
$ sudo dnf install cpprest-devel
```

With [brew](https://github.com/Homebrew/homebrew-core/blob/master/Formula/cpprestsdk.rb) on OSX

```
$ brew install cpprestsdk
```

With [NuGet](https://www.nuget.org/packages/cpprestsdk.android/) on Windows for Android

```
PM> Install-Package cpprestsdk.android
```

学c linux gcc

其他平台，编译器不行


学习书籍

cpp prime

Unix高性能编程

c++标准库



有一套c++的云编译系统负责编译，然后有一套内部的持续集成系统，发布后将编译产出上传到pass平台部署



### andorid c/c++



```shell script



clang++ -v

clang version 9.0.1 

Target: aarch64-unknown-linux-android

Thread model: posix

InstalledDir: /data/data/com.termux/files/usr/bin


clang -v
clang version 9.0.1 
Target: aarch64-unknown-linux-android
Thread model: posix
InstalledDir: /data/data/com.termux/files/usr/bin
```



感觉C++真心难。指针，函数指针，解指针运算混在一起简直让人头晕。另，设计“通用成员函数指针”，看别人的看了好久才看明白

有关指针我推荐：[C 指针传递变量为什么无法修改变量值？](https://www.zhihu.com/question/41476387/answer/91566794) 学习我这里买的图例理解指针的做法。以及看这个网页里面的PDF文档：[Pointers and Memory](https://link.zhihu.com/?target=http%3A//cslibrary.stanford.edu/102/) C++不是你一个觉得难，但是人生在世，只学容易的岂不是很无趣？



Windows os开发linux系统程序，只有头文件，没有库文件，上传代码到编译服务器去



c/c++/rust

可以对汇编语言进行优化



举例，在编译时，gcc -LDM


[C++开源框架源码分析](https://cloud.tencent.com/developer/user/4235735)



另外在图像处理，音视频开发，网游服务器也很难离开c++ 

 互联网公司按照架构，从前端到后端，其实有多种业务模块： 

作者：John Dooooe


ldconfig -v | grep liblog4cpp.so`

brpc
pistache 都是静态库

brpc prefers static linkages of deps, so that they don't have to be installed on every machine running the app.


大公司，cpp编译器统一的
某公司也是jdk8

`1> 命令行: "cmd.exe" /c ""D:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\2019\PROFESSIONAL\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\CMake\bin\cmake.exe"  -G "Ninja" -DCMAKE_INSTALL_PREFIX:PATH="D:\visual studio 2015\Projects\CMakeProject1\out\install\x64-Debug" -DCMAKE_CXX_COMPILER:FILEPATH="D:/Program Files/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.23.28105/bin/HostX64/x64/cl.exe" -DCMAKE_C_COMPILER:FILEPATH="D:/Program Files/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.23.28105/bin/HostX64/x64/cl.exe"  -DCMAKE_TOOLCHAIN_FILE="D:/vcpkg/scripts/buildsystems/vcpkg.cmake" -DCMAKE_BUILD_TYPE="Debug" -DCMAKE_MAKE_PROGRAM="D:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\2019\PROFESSIONAL\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\Ninja\ninja.exe" "D:\visual studio 2015\Projects\CMakeProject1" 2>&1"`

1）**网页前端+后台，**纯前端的框架本人不擅长，不强答了；以FreeWheel, Airbnb, Grab等公司为例，网站后台一般用golang，ruby on rails；另外还有python（tornado，django）；哦对还有php差点忘了这货；

2）**业务端服务**，比如对接外卖商家的后台服务，推荐系统里一些离线计算服务，不追求极致高性能的场景，一般使用Java；阿里巴巴就是Java为主；

3）**高性能计算服务，**比如推荐系统的推理引擎（inference engine），广告投放引擎等，应对大流量，追求高并发的场景，基本都是c++服务；比如阿里妈妈的广告服务，以及业内很多公司，头条，腾讯，快手，FreeWheel, 微软等，高并发服务都得用到c++；

所以这么一说就简单了，得看你喜欢做哪块的工作，答主本人就是不喜欢业务太多，也不喜欢去做改前端图片文本框这种“low比”工作（no offence 请不要喷我哈哈），所以答主就一直在做广告/推荐引擎c++服务；

随着互联网的发展，其实以上几大块业务都会有越来越大的需求，而且尤其现在AI大潮，高性能c++服务在推荐系统里是非常非常关键的（inference engine），你每次刷到快手广告，每次看到直通车推荐，每次刷脸识别，都要请求到后端高性能c++服务，所以不存在说互联网发展了c++就没有用武之地这种说法。

**貌似 C++ 越来越难找工作了？**

看了上面的回答，我想这里就很明显了，有c++岗位需求的公司，除了上面说的头条，腾讯，快手，还有好多好多公司都在招，以答主最近找工作的经历来看，虽然外界都说现在是互联网寒冬，但是我个人感觉各个公司仍然是非常缺人，至少从我这个c++背景的工程师来看是如此。

我相信，随着技术的发展，以后c++相关岗位的需求，会越来越旺盛，只增不减。



1，项目经历这块，真心喜欢c++的话，可以自己业余做一点c++小项目，尤其如果能在github上面有些贡献那就更好了；

2，练习用c++写面试题，面试时候题解得好 是非常加分的；

3，更进一步的，有空把c++的STL模板库，tcmalloc内存管理机制等都可以去了解了解；

做好以上几点，即使是java背景的候选人，基本上像快手，滴滴等公司，面成功的概率还是比较大的；



 你好，之前的工作语言是C，换工作瞄准了两个方向：1.容器（以golang为主）2.高并发，分布式领域（以c++为主）。请问这种背景下，题主有何建议，针对跨语言方面有哪些是需要着重准备的呢 



1> 命令行: "cmd.exe" /c ""D:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\2019\PROFESSIONAL\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\CMake\bin\cmake.exe"  -G "Ninja" -DCMAKE_INSTALL_PREFIX:PATH="D:\visual studio 2015\Projects\CMakeProject1\out\install\x64-Debug" -DCMAKE_CXX_COMPILER:FILEPATH="D:/Program Files/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.23.28105/bin/HostX64/x64/cl.exe" -DCMAKE_C_COMPILER:FILEPATH="D:/Program Files/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.23.28105/bin/HostX64/x64/cl.exe"  -DCMAKE_TOOLCHAIN_FILE="D:/vcpkg/scripts/buildsystems/vcpkg.cmake" -DCMAKE_BUILD_TYPE="Debug" -DCMAKE_MAKE_PROGRAM="D:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\2019\PROFESSIONAL\COMMON7\IDE\COMMONEXTENSIONS\MICROSOFT\CMAKE\Ninja\ninja.exe" "D:\visual studio 2015\Projects\CMakeProject1" 2>&1"`


vs支持cmake是ninja的

第一阶段：你学会了 C with Classes，然后把各种东西都包装成了 class；

第二阶段：为了实现多态，你学会了继承、虚函数、多继承和虚继承，然后你用这些技术改写了一些代码，实现了代码重用。你觉得很开心，感觉自己减少了代码量，提高了工作效率；
第三阶段：你学会了用抽象类作为接口，发现以前的继承关系太复杂，用接口更清晰，于是把代码都改成了单继承+接口。你觉得很开心，觉得自己设计了很好的架构；
第四阶段：为了实现和使用泛型容器，你学会了模板。你觉得很开心，又进一步提高了代码重用度；
第五阶段：你了解到了动态分派（Dynamic Dispatch）和静态分派（Static Dispatch），于是你把接口都改成了模板。你觉得很开心，不降低抽象程度却提高了代码执行效率；
第六阶段：你学会了异常。你觉得有点不爽，异常虽方便，但异常安全（exception safety）太难做到了；
第七阶段：你学会了移动语义，你觉得很开心，可以用值的形式写出更高效的代码；

第八阶段：你学会了 unique_ptr，shared_ptr。你觉得很开心，妈妈再也不用担心我写出异常不安全的代码了；
第九阶段：你注意到了 Rust 这个语言，然后有意无意地在自己的 C++ 代码中贯彻 Rust 的思想，比如多用移动语义、trait、const；
第十阶段：你学会了模板元编程，SFINAE，并成功地使用不到 30 行代码使编译器输出了 4G 错误信息。然后你用模板实现了一套类型安全的 trait 系统。你觉得很开心，编译器的错误提示终于可以看了；
https://www.zhihu.com/question/62158323/answer/196189709

依赖管理Blaze, 其开源版是Bazel，编译系统Forge

不支持模块化

.a
.so
需要编译

.class -> .jar/.aar跨平台

.lib

vcpkg试图解决这个问题



内存对齐

cmake -makefile

gmake
qmake

gnu的
autogenerator


## cpp linux environment

AutoTools automake eclipse

https://www.cnblogs.com/youxia/p/linux023.html

https://blog.csdn.net/initphp/article/details/43705765





cpp开发，在目标机器上开发，conan不好用，vcpkg在发展中



[开源免费的C/C++网络库(c/c++ sockets library) 七剑下天山](https://blog.csdn.net/weixin_33859844/article/details/85528647)



 图像处理真的是没有第二者，只能用cpp



内存管理机制



 像tcmalloc的机制这种可以简单看一看，另外还可以看看《深入理解计算机系统》第九章：虚拟内存 



 推荐引擎 算法有好多种，看具体场景， xgb / 决策树 也是会用到 





Cpp如何做ci cd 

 

jeikins+gitlab做自动编译部署



##### macros



 https://github.com.cnpmjs.org/solrex/brpc-open-falcon 




[cpp 添加头文件](https://blog.csdn.net/yusiguyuan/article/details/16950547)



`export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/usr/include/libxml2`



 `warning: ISO C++ forbids converting a string constant to ‘char*’ [-Wwrite-strings] `





[string convert]( https://stackoverflow.com/questions/16252455/error-conversion-from-const-char-5-to-non-scalar-type-in-c )

uname -a



 定位头文件



《现在c++实战30讲》



llvm libstdc++写的好点



centos 7 安装高版本gcc

raii
https://blog.csdn.net/GangStudyIT/article/details/80645399
RAII（Resource Acquisition Is Initialization）机制是Bjarne Stroustrup首先提出的，是一种利用对象生命周期来控制程序资源（如内存、文件句柄、网络连接、互斥量等等）的简单技术。
对于RAII概念清楚后，我们就可以理解为智能指针就是RAII的一种体现，智能指针呢，它是利用了类的构造和析构，用一个类来管理资源的申请和释放


rust




内存问题分析的利器——valgraind的memcheck




 https://blog.csdn.net/breaksoftware/article/details/79445591 




 https://blog.csdn.net/jq0123 



 LD_LIBRARY_PATH=:$LD_LIBRARY_PATH:/usr/local/lib
export LD_LIBRARY_PATH 



rest_description



gcc5编译 travis报错



 https://stackoverflow.com/questions/33394934/converting-std-cxx11string-to-stdstring 



libodb-mysql

头文件和库文件不在一个包



cpp 未声明的引用

未定义的引用



https://blog.csdn.net/haluoluo211/article/details/54376947





[CPlusPlusThings](https://github.com/Light-City/CPlusPlusThings)




学习c++

我说的10个小时包括写代码，做习题和做笔记，一天可以写8页笔记左右，很多问题似懂非懂的，写完笔记就清楚了．笔记也没啥用的，写完就可以扔了



张小方

侯捷

勿在浮沙筑高台

It不容一点马虎

记住细节

多看书，多复习



[有哪些值得推荐给C++初学者的国外视频课程](https://www.zhihu.com/question/304609578/answer/545741569)





Bingo招聘

brpc





C++ 如何遍历char *[]



Raii





https://blog.csdn.net/GangStudyIT/article/details/80645399





使用稳定发布版（如 CentOS）的 Linux 用户也需要检查一下，你的 GCC 版本有可能比较老。如果早于 GCC 7 的话，建议你安装一个新版本的 GCC（不需要覆盖系统的 GCC）。比如，对于 CentOS 7，系统安装的 GCC 版本是 4.8，太老，你可以通过安装 centos-release-scl 和 devtoolset-7-gcc-c++ 两个包来获得 GCC 7；随后，可以使用命令 scl enable devtoolset-7 bash 或 . /opt/rh/devtoolset-7/enable 来启用 GCC 7。





[Linux如何使用最新版本gcc scl](https://mp.weixin.qq.com/s/3tvoiz7bcoQ3KZMGIZrJkQ)





老师有没有什么好的C/C++并发方面的书推荐一下，C++ Primer上没有这方面内容。

作者回复: 只有英文的。C++ Concurrency in Action 英文已经出到第二版，口碑不错。但中译本《C++并发编程实战》的翻译则是恶评如潮。





https://github.com/xiaoweiChen/CPP-Concurrency-In-Action-2ed-2019







Cpp patch



C++的代码，部署在centos 7上，自己开发用的电脑如果是ubuntu的话，依赖库怎搞？

开发机 部署机

我现在就发现，我在开发机上编译的库，在部署的机器上还要在编译一次

