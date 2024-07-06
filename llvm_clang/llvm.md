# llvm

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
