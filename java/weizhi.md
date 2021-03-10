# weizhi

c++ std

std::set
std::deque


cmake例子
https://blog.csdn.net/listener51/article/details/78004266
https://blog.csdn.net/dbzhang800/article/details/6314073

C++中的默认函数与default和delete用法
https://blog.csdn.net/u012333003/article/details/25299939
https://blog.csdn.net/u010591680/article/details/71101737
https://blog.csdn.net/FX677588/article/details/74615470


https://github.com/schuhschuh/gflags
gflags
https://gflags.github.io/gflags/#cmake
http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2017/1009/8575.html
GitHub代码浏览插件
https://juejin.im/entry/597025d9518825419f7b65ba

http://yifeng.studio/2017/09/06/recommended-extension-tools-about-github/

https://blog.csdn.net/breaksoftware/article/details/51020803
gtest源码分析
https://www.ibm.com/developerworks/cn/aix/library/au-googletestingframework.html

https://blog.csdn.net/breaksoftware/article/details/50917733

https://www.cnblogs.com/liyuan989/p/4136099.html

virtual bool IsPrime(int n) const = 0;
c++ virtual function        const = 0;
https://blog.csdn.net/qq_29003347/article/details/78420236


https://www.gnu.org/software/gdb/documentation/
https://blog.csdn.net/eroswang/article/details/2425242
GDB文档 比较详细的GDB用法说明
http://sourceware.org/gdb/current/onlinedocs/

CMake是个一个开源的跨平台自动化建构系统，用来管理软件建置的程序，并不相依于某特定编译器。并可支持多层目录、多个应用程序与多个库。 它用配置文件控制建构过程（build process）的方式和Unix的make相似，只是CMake的配置文件取名为CMakeLists.txt。CMake并不直接建构出最终的软件，而是产生标准的建构档（如Unix的Makefile或Windows Visual C++的projects/workspaces），然后再依一般的建构方式使用。这使得熟悉某个集成开发环境（IDE）的开发者可以用标准的方式建构他的软件，这种可以使用各平台的原生建构系统的能力是CMake和SCons等其他类似系统的区别之处。 CMake配置文件(CMakeLists.txt)可设置源代码或目标程序库的路径、产生适配器（wrapper）、还可以用任意的顺序建构可执行文件。CMake支持in-place建构（二进档和源代码在同一个目录树中）和out-of-place建构（二进档在别的目录里），因此可以很容易从同一个源代码目录树中建构出多个二进档。CMake也支持静态与动态程序库的建构。

“CMake”这个名字是"Cross platform Make"的缩写。虽然名字中含有"make"，但是CMake和Unix上常见的“make”系统是分开的，而且更为高端。 它可与原生建置环境结合使用，例如：make、苹果的Xcode与微软的Visual Studio。

qmake是一个协助简化跨平台进行项目开发的构建过程的工具程序，Qt附带的工具之一 。qmake能够自动生成Makefile、Microsoft Visual Studio 项目文件 和 xcode 项目文件。不管源代码是否是用Qt写的，都能使用qmake，因此qmake能用于很多软件的构建过程。

手写Makefile是比较困难而且容易出错，尤其在进行跨平台开发时必须针对不同平台分别撰写Makefile，会增加跨平台开发复杂性与困难度。qmake会根据项目文件（.pro）里面的信息自动生成适合平台的 Makefile。开发者能够自行撰写项目文件或是由qmake本身产生。qmake包含额外的功能来方便 Qt 开发，如自动的包含moc 和 uic 的编译规则。

SCons，一种软件开发工具程序，功能类似于UNIX上的make、autoconf与automake工具。它是一个开放源代码计划，采用MIT许可，原作者是史蒂芬·奈特（Steven Knight），使用Python语言开发。第一个正式版本在2010年3月23日发布。



```shell
cmake/linux/bin/cmake --helpUsage
  cmake [options] <path-to-source>
  cmake [options] <path-to-existing-build>
  cmake [options] -S <path-to-source> -B <path-to-build>
Specify a source directory to (re-)generate a build system for it in the
current working directory. Specify an existing build directory to
re-generate its build system.
Options
  -S <path-to-source> = Explicitly specify a source directory.
  -B <path-to-build> = Explicitly specify a build directory.
  -C <initial-cache> = Pre-load a script to populate the cache.
  -D <var>[:<type>]=<value> = Create or update a cmake cache entry.
  -U <globbing_expr> = Remove matching entries from CMake cache.
  -G <generator-name> = Specify a build system generator.
  -T <toolset-name> = Specify toolset name if supported by
                                 generator.
  -A <platform-name> = Specify platform name if supported by
                                 generator.
  -Wdev = Enable developer warnings.
  -Wno-dev = Suppress developer warnings.
  -Werror=dev = Make developer warnings errors.
  -Wno-error=dev = Make developer warnings not errors.
  -Wdeprecated = Enable deprecation warnings.
  -Wno-deprecated = Suppress deprecation warnings.
  -Werror=deprecated = Make deprecated macro and function warnings
                                 errors.
  -Wno-error=deprecated = Make deprecated macro and function warnings
                                 not errors.
  -E = CMake command mode.
  -L[A][H] = List non-advanced cached variables.
  --build <dir> = Build a CMake-generated project binary tree.
  --open <dir> = Open generated project in the associated
                                 application.
  -N = View mode only.
  -P <file> = Process script mode.
  --find-package = Run in pkg-config like mode.
  --graphviz=[file] = Generate graphviz of dependencies, see
                                 CMakeGraphVizOptions.cmake for more.
  --system-information [file] = Dump information about this system.
  --debug-trycompile = Do not delete the try_compile build tree.
                                 Only useful on one try_compile at a time.
  --debug-output = Put cmake in a debug mode.
  --trace = Put cmake in trace mode.
  --trace-expand = Put cmake in trace mode with variable
                                 expansion.
  --trace-source=<file> = Trace only this CMake file/module. Multiple
                                 options allowed.
  --warn-uninitialized = Warn about uninitialized values.
  --warn-unused-vars = Warn about unused variables.
  --no-warn-unused-cli = Don't warn about command line options.
  --check-system-vars = Find problems with variable usage in system
                                 files.
  --help,-help,-usage,-h,-H,/? = Print usage information and exit.
  --version,-version,/V [<f>] = Print version number and exit.
  --help-full [<f>] = Print all help manuals and exit.
  --help-manual <man> [<f>] = Print one help manual and exit.
  --help-manual-list [<f>] = List help manuals available and exit.
  --help-command <cmd> [<f>] = Print help for one command and exit.
  --help-command-list [<f>] = List commands with help available and exit.
  --help-commands [<f>] = Print cmake-commands manual and exit.
  --help-module <mod> [<f>] = Print help for one module and exit.
  --help-module-list [<f>] = List modules with help available and exit.
  --help-modules [<f>] = Print cmake-modules manual and exit.
  --help-policy <cmp> [<f>] = Print help for one policy and exit.
  --help-policy-list [<f>] = List policies with help available and exit.
  --help-policies [<f>] = Print cmake-policies manual and exit.
  --help-property <prop> [<f>] = Print help for one property and exit.
  --help-property-list [<f>] = List properties with help available and
                                 exit.
  --help-properties [<f>] = Print cmake-properties manual and exit.
  --help-variable var [<f>] = Print help for one variable and exit.
  --help-variable-list [<f>] = List variables with help available and exit.
  --help-variables [<f>] = Print cmake-variables manual and exit.
Generators
The following generators are available on this platform:
  Unix Makefiles = Generates standard UNIX makefiles.
  Ninja = Generates build.ninja files.
  Watcom WMake = Generates Watcom WMake makefiles.
  CodeBlocks - Ninja = Generates CodeBlocks project files.
  CodeBlocks - Unix Makefiles = Generates CodeBlocks project files.
  CodeLite - Ninja = Generates CodeLite project files.
  CodeLite - Unix Makefiles = Generates CodeLite project files.
  Sublime Text 2 - Ninja = Generates Sublime Text 2 project files.
  Sublime Text 2 - Unix Makefiles
                               = Generates Sublime Text 2 project files.
  Kate - Ninja = Generates Kate project files.
  Kate - Unix Makefiles = Generates Kate project files.
  Eclipse CDT4 - Ninja = Generates Eclipse CDT 4.0 project files.
  Eclipse CDT4 - Unix Makefiles= Generates Eclipse CDT 4.0 project files.
```
采用eclipse gdb来搭建调试qemu源码的环境
https://my.oschina.net/tantexian/blog/648887


glibc
http://www.gnu.org/software/libc/manual/pdf/libc.pdf

https://www.cnblogs.com/likui360/p/6029484.html
MySQL源码分析：源码文件结构及主要数据结构

https://github.com/oracle/graal
graal
GraalVM: Run Programs Faster Anywhere
如何用CLion 导入android 系统项目的代码
https://blog.csdn.net/Imbak/article/details/78288876
Android NDK开发(一)  入门
https://www.jianshu.com/p/0261e6cceb3e
使用CLion在MacOS、Linux上编译C++代码
https://www.cnblogs.com/conorpai/p/6425048.html


ODB  C++ 数据库操作库
入门介绍
https://blog.csdn.net/machuanfei_c/article/details/82428422
例子调试
cmake 组织 edidada的github上

https://blog.csdn.net/u012927281/article/details/51289608
使用gdb调试glibc

https://blog.csdn.net/logic_lai/article/details/80403361
linux mysql gui client
https://www.cnblogs.com/terrytian88/p/5820159.html
C++笔记——c++中#pragma的用法
https://blog.csdn.net/mao_hui_fei/article/details/78150143

提醒一下：IPv6 不关交换机什么事。

MediaTek MT7621
7621 简称
https://en.cppreference.com/w/cpp/preprocessor/impl

#pragma c++

https://cloud.tencent.com/developer/article/1054231
clion g++  添加参数


20190201笔记
离线安装rpm包
进入下载包的目录，离线安装rpm包
rpm -ivh *.rpm
Centos 7
odb 源码安装 失败
rpm包安装 成功
sudo yum install centos-release-scl
sudo yum install devtoolset-5-gcc*
使用devtoolset升级GCC版本




如果你想要用apt-get命令来安装一个软件,但是你只知道大概有几个字母,那么,你可以用下面的命令来进行查询,看下跟这个字母有关的软件都有哪些,它会给你把列表列出来:
sudo apt-cache search all | grep gcc

person.sql是自动生成的建立表的sql语句
其他三个是操作数据库支持的代码
上述命令 --generate-query选项是生成数据查询支持的代码,--generate-schema选项是生成创建数据表相关的代码

ldconfig
https://git.codesynthesis.com/cgit/odb/
ODB源码
https://blog.csdn.net/Windeal/column/info/windeal-apue
APUE学习笔记
使用devtoolset升级GCC版本


https://blog.csdn.net/windeal3203/article/details/71438861
https://www.cnblogs.com/binbinjx/p/5603362.html

cmake 强制链接静态库

https://www.codesynthesis.com/products/odb/
ODB: C++ Object-Relational Mapping (ORM)
https://www.codesynthesis.com/products/odb/download.xhtml


https://blog.csdn.net/x_r_su/article/details/52927768
cmake 添加头文件，库文件，链接库文件

https://blog.csdn.net/tangcaijun/article/details/42110319
Crypto++学习总结---MD5 AES
https://blog.csdn.net/wangweitingaabbcc/article/details/11152531

Crypto++ 看编译器
The current version of Crypto++ supports the following compilers:

Visual Studio 2003 - 2017
GCC 3.3 - 9.0
Apple Clang 4.3 - 9.0
LLVM Clang 2.9 - 7.0
C++Builder 2013
Intel C++ Compiler 9 - 16.0
Sun Studio 12u1 - 12.6
IBM XL C/C++ 10.0 - 13.1

Crypto++ 编译 centos 7

https://www.cryptopp.com/

https://www.cryptopp.com/wiki/User_Guide:_Introduction

https://github.com/weidai11/cryptopp
https://www.cryptopp.com/wiki/Linux
https://www.cryptopp.com/wiki/Compiling#Crypto.2B.2B_5.6.5
    
https://www.cryptopp.com/wiki/CMake

https://github.com/noloader/cryptopp-cmake

https://github.com/noloader/cryptopp-cmake/blob/master/CMakeLists.txt

参考：https://blog.csdn.net/tgbtgb/article/details/52495589

https://github.com/weidai11/cryptopp/tree/CRYPTOPP_5_6_5

https://www.cryptopp.com/wiki/Linux

命令行
git tag CRYPTOPP_5_6_5

make libcryptopp.a libcryptopp.so cryptest.exe 

 ls .so .a *.exe 

make install PREFIX=/usr/local


编译到时候添加编译库

静态库： 在编译参数直径添加libcryptopp.a的实际路径。比如： 
/usr/local/lib/libcryptopp.a 
动态库：在编译参数直径添加 -lcryptopp

https://www.cnblogs.com/conw/p/5938113.html
https://www.jianshu.com/p/1821fc597b25
基于CLion的GTest测试工程简单示例
自己的代码 https://github.com/edidada/GTest-CLion-example
成功

https://www.cnblogs.com/yangai/p/6863670.html
https://www.cnblogs.com/james6176/p/3222671.html
c++ 字符串
https://www.cnblogs.com/nzbbody/p/3504199.html


The C++ Standard Library - A Tutorial and Reference - 2nd Edition
http://www.cppstdlib.com/

https://blog.csdn.net/Cyang_liu/article/details/65449457
c++ 中mutable的用法

std::make_shared
https://zh.cppreference.com/w/cpp/memory/shared_ptr/make_shared
https://blog.csdn.net/wangshubo1989/article/details/50374914
实战c++中的vector系列--vector的遍历

std::vector
http://www.cplusplus.com/reference/vector/vector/

std::move
https://zh.cppreference.com/w/cpp/utility/move

curl 模拟 GET\POST 请求，以及 curl post 上传文件
curl localhost:9999/api/daizhige/article -X POST -d "title=comewords&content=articleContent"

https://www.cnblogs.com/lidabo/archive/2012/12/06/2804252.html
c++数据类型万能转换器boost::lexical_cast

https://en.cppreference.com/w/cpp/thread/lock_guard
lock_guard  c++
clion快捷键
https://blog.csdn.net/fengbingchun/article/details/73521630

https://blog.csdn.net/wd2014610/article/details/79637503?utm_source=blogxgwz7

https://blog.csdn.net/firetreeSF/article/details/53468515

https://baike.baidu.com/item/%23pragma%20once

https://blog.csdn.net/chlele0105/article/details/23691147

https://blog.csdn.net/zhangbiao1981/article/details/4128209

Libevent使用例子，从简单到复杂
http://www.cnblogs.com/wainiwann/p/7096245.html


https://www.jetbrains.com/help/clion/cmakelists-txt-file.html
可以定义变量

virtual c++含义
virtual c++含义
虚拟函数 父类生命
可以类比Java的抽象函数？
子类实现
https://blog.csdn.net/ring0hx/article/details/1605254
reinterpret_cast是C++里的强制类型转换符。

https://baike.baidu.com/item/reinterpret_cast/9303204

https://pocoproject.org/pro/docs/00153-RemotingNGTutorialPart4.html
https://github.com/pocoproject/sandbox/blob/master/JSON/testsuite/src/JSONTest.cpp
https://blog.csdn.net/fengyishang/article/details/45220823




