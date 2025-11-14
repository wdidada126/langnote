# llvm
主要还是企业的推动，基中最大的是苹果和谷歌。苹果发起了建立在llvm后端之上的clang前端项目。同时也给llvm社区大量的捐款和贡献代码，让llvm项目从此起飞。苹果发起clang项目的原因是之前的xcode集成的GCC编译器非常难以适应xcode的需求，苹果期望在xcode前端构建非常复杂的代码分析和性能分析工具，但是GCC主要还是因适配Linux系统而设计的编译器，同时因为GPL协议让苹果把编译器部分代码集成到接口与IDE进行对接过程中会遇到严重的协议问题，因此苹果发起了clang项目同时组织了大量的研发力量对整个llvm社区提供代码，可以查看当时的社区邮件，cfe社区可以说是因苹果而兴起。之后谷歌深度参与进来，谷歌的贡献主要在后端和系统特性的加入，比如并行优化器，运行时动态profile的xray等等。目前从架构上看llvm体系远比GCC现代得多，整个Linux和BSD的内核和工具编译都在逐渐切换到llvm上。

在macOS和FreeBSD系统中，C标准库的实现有所不同，但它们都遵循C标准，提供了标准C库的功能。

macOS系统
在macOS系统中，C标准库的实现通常与Xcode开发环境紧密相关。Xcode是Apple提供的集成开发环境（IDE），它包括了Clang编译器和LLVM工具链，以及针对macOS优化的C/C++标准库。对于C标准库，macOS使用的是基于LLVM项目的一部分，特别是与Clang编译器紧密集成的C标准库实现。然而，具体实现细节可能因macOS版本而异，且Apple可能会使用自己的定制版本来优化性能和兼容性。

FreeBSD系统
在FreeBSD系统中，C标准库的实现通常是GNU C Library（glibc）的一个替代品，因为glibc主要是为基于GNU/Linux的系统设计的。FreeBSD使用自己的C标准库实现，如libc，它提供了与标准C库兼容的API，但针对FreeBSD系统进行了优化。libc是FreeBSD操作系统的基础组件之一，它提供了广泛的系统调用接口和C标准库函数，支持FreeBSD系统的稳定运行和应用程序的开发。

总结
macOS：使用基于LLVM项目的C标准库实现，与Xcode开发环境紧密集成。
FreeBSD：使用自己的C标准库实现，如libc，针对FreeBSD系统进行了优化。
需要注意的是，虽然这些系统使用不同的C标准库实现，但它们都遵循C标准，提供了标准C库的功能，因此开发者可以编写可移植的C语言程序，并在这些系统上进行编译和运行。然而，在实际开发中，可能还需要注意不同系统之间的细微差别，如系统调用、线程库、网络库等方面的差异，以确保程序的兼容性和稳定性。


Clang（一个C/C++/Objective-C编译器）、LLVM（编译器和工具链技术的核心库）、LLDB（一个调试器）、libclc（OpenCL的C库）、libcxx（一个C++标准库）、libcxxabi（一个C++ ABI库）、libunwind（一个用于确定函数调用关系的库）、lld（一个链接器）等。

https://github.com/llvm/llvm-project/blob/d76a1233f7d7923d056a53cfa6f89735e9cda86e/libcxx/include/__memory/shared_ptr.h#L833


clang是前端

谷歌跟苹果在维护
苹果是因为oc

谷歌因为提案没进去，所以没有向以前投入资源

非常希望在有生之年能看懂v8
回复: 易读不是大部分项目的追求……
不过，话说回来，LLVM的libc++可读性是相当好的，至少比GCC和MSVC的标准库实现容易理解多了。

brew install llvm

If you need to have llvm first in your PATH, run:
  echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> /Users/ibqo/.bash_profile

For compilers to find llvm you may need to set:
  export LDFLAGS="-L/usr/local/opt/llvm/lib"
  export CPPFLAGS="-I/usr/local/opt/llvm/include"

LLVM编译器实战教程 第二版

一步步掌握LLVM
https://www.zhihu.com/column/c_1250484713606819840

Swift官方就是用llvm，在LLVM IR上面也有一层SIR的东西。毕竟两个的爹都是Apple。感觉llvm以后要一统江湖啊，原先每个编译器企业自己做技术栈，以后估计都要整合到llvm的框架里了。

http://releases.llvm.org/8.0.0/docs/CMake.html

mac

```shell
/Users/ibqo/mybuilddir
cmake -version
cmake --build .
cmake -DLLVM_BUILD_EXAMPLES=ON ../llvm-8.0.0.src

$ cmake -DCMAKE_INSTALL_PREFIX=/usr/local/llvm -P cmake_install.cmake
```

编译

带example

归功于整个AI产业吧，目前AI芯片需要大量编译器背景的人，同时AI框架也是很多采用LLVM，需要有编译器背景的人。另外，在安全，区块链，数据库等很多行业都开始采用LLVM，所以这是做编译器，尤其是LLVM的人，很好的一个时机
知乎 蓝色 阿里巴巴

llvm支持的后端有：

添加后端

https://www.zhihu.com/question/315440674/answer/683641589

LLVM从一个学术研究项目进化成C、C++和Objective C编译器的通用后端。成功的关键是性能和适应能力，两者都得益于LLVM独特的设计和实现。
传统的编译器架构为：
Source Code -> [ Frontend & Optimizer & Backend ] -> Machine Code
对比，LLVM的架构为：
Source Code @ x -> [ x Frontend ] -> [ LLVM Optimizer @ IR ] -> [ LLVM m Backend ] -> Machine Code @ m
其中，x为C/C++, Objcect C等多种语言；m为x86，PowerPC，ARM等多种CPU架构。

不同的前端后端使用统一的中间代码LLVM Intermediate Representation (LLVM IR)
优化阶段是一个通用的阶段，它针对的是统一的LLVM IR，和具体语言无关；
扩展性好：如果需要支持一种新的编程语言，那么只需要实现一个新的前端；如果需要支持一种新的硬件设备，那么只需要实现一个新的后端


## 源代码

llvm-project
https://github.com/llvm/llvm-project


https://libcxx.llvm.org/BuildingLibcxx.html

git clone https://gitcode.com/pollyduan/llvm-project.git

https://gitcode.com/pollyduan/llvm-project/overview

### 源代码编译

git clone -b llvmorg-17.0.6 https://gitcode.com/pollyduan/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm
make -j5

## releases/version/版本

https://releases.llvm.org/

版本号 发布日期
4 November 2025: LLVM 21.1.5
21.1.0 2025-08-26
20.1.0 2025-03-04
19.1.1 2024-10-01
19.1.0 2024-09-17
19.1.0-rc1 2024-07-26
18.1.8 2024-06-20
18.1.7 2024-06-06
18.1.6 2024-05-18
18.1.5 2024-05-02
18.1.4 2024-04-17
18.1.3 2024-04-04
18.1.2 2024-03-19
18.1.1 2024-03-08
18.1.0 2024-03-05
17.0.6 2023-11-28
17.0.5 2023-11-14
17.0.4 2023-10-31
17.0.3 2023-10-17
17.0.2 2023-10-03
17.0.1 2023-09-09
16.0.6 2023-06-13
16.0.5 2023-06-02
16.0.4 2023-05-16
16.0.3 2023-05-03
16.0.2 2023-04-19
16.0.1 2023-04-05
16.0.0 2023-03-17
15.0.7 2023-01-12
15.0.6 2022-11-29
15.0.5 2022-11-16
15.0.4 2022-11-02
15.0.3 2022-10-18
15.0.2 2022-10-04
15.0.1 2022-09-20
15.0.0 2022-09-06
14.0.6 2022-06-24
14.0.5 2022-06-10
14.0.4 2022-05-24
14.0.3 2022-04-29
14.0.2 2022-04-26
14.0.1 2022-04-12
14.0.0 2022-03-25
13.0.1 2022-02-07
13.0.0 2021-10-04
12.0.1 2021-07-08
12.0.0 2021-04-14
11.1.0 2021-02-25
11.0.1 2021-01-14
11.0.0 2020-10-12
10.0.1 2020-08-06
10.0.0 2020-03-24
9.0.1 2019-12-20
9.0.0 2019-09-19
8.0.1 2019-07-19
7.1.0 2019-05-10
8.0.0 2019-03-20
7.0.1 2018-12-21
7.0.0 2018-09-19
6.0.1 2018-07-05
5.0.2 2018-05-16
6.0.0 2018-03-08
5.0.1 2017-12-21
5.0.0 2017-09-07
4.0.1 2017-07-04
4.0.0 2017-03-13
3.9.1 2016-12-23
3.9.0 2016-09-02
3.8.1 2016-07-11
3.8.0 2016-03-08
3.7.1 2016-01-05
3.7.0 2015-09-01
3.6.2 2015-07-16
3.6.1 2015-05-26
3.5.2 2015-04-02
3.6.0 2015-02-27
3.5.1 2015-01-20
3.5.0 2014-09-03
3.4.2 2014-06-19
3.4.1 2014-05-07
3.4 2014-01-02
3.3 2013-06-17
3.2 2012-12-20
3.1 2012-05-22
3.0 2011-12-01
2.9 2011-04-06
2.8 2010-10-05
2.7 2010-04-27
2.6 2009-10-23
2.5 2009-03-02
2.4 2008-11-09
2.3 2008-06-09
2.2 2008-02-11
2.1 2007-09-26
2.0 2007-05-23
1.9 2006-11-19
1.8 2006-08-09
1.7 2006-04-20
1.6 2005-11-08
1.5 2005-05-18
1.4 2004-12-09
1.3 2004-08-13
1.2 2004-03-19
1.1 2003-12-17
1.0 2003-10-24