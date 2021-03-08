# cpp


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

