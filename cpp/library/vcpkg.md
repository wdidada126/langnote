# vcpkg

库作者如何添加自己的库到本地的vcpkg

spdlog

vcpkg编译下载的库报错，解决思路：
编译器版本，支持c++14? c++17?

vcpkg search apache
rbmq的cpp库


`cmake -DCMAKE_TOOLCHAIN_FILE=/root/vcpkg/scripts/buildsystems/vcpkg.cmake ..`


CMake给交叉编译预留了一个很好的变量即CMAKE_TOOLCHAIN_FILE,它定义了一个文件的路径，这个文件即toolChain,里面set了一系列你需要改变的变量和属性，包括C_COMPILER,CXX_COMPILER。CMake为了不让用户每次交叉编译都要重新输入这些命令，因此它带来toolChain机制，简而言之就是一个cmake脚本，内嵌了你需要改变以及需要set的所有交叉环境的设置。

这里面也牵扯了一些相关的变量设置,在这里我通过自己的项目，简单介绍下几个比较重要的：

set(CMAKE_ASM_COMPILER ccmips)

set(CMAKE_SYSTEM_NAME Generic)

set(UNIX True CACHE BOOL "Archiver")

set(CMAKE_C_COMPILER ccmips)
set(CMAKE_CXX_COMPILER c++mips)

set(CMAKE_AR armips CACHE FILEPATH "Archiver")
set(CMAKE_RANLIB ranlibmips CACHE FILEPATH "Archiver")
set(CMAKE_LINKER ldmips CACHE FILEPATH "Archiver")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_MODE_LIBRARY ONLY)

add_compile_options(-mno-branch-likely -mips64 -nostdinc -mabi=n32 -mgp64 -EL -fno-builtin -fno-zero-initialized-in-bss -fno-common -Wall -G8 -MD  -O2 -G 8 -D_VSB_CONFIG_FILE="${CONFIG_H}/lib_smp/h/config/vsbConfig.h" )

#精简后好的
add_definitions(-DCPU=_DELTA_MIPSI64 -DINET -DTOOL_FAMILY=gnu -DTOOL=gnule -D_CORETEK_KERNEL -D_CORETEK_MIPS_N32_ABI -DMIPSEL -D_WRS_LIB_BUILD  -DWRS_IPNET -D_WRS_CONFIG_SMP)

add_link_options(-EL)
CMAKE_SYSTEM_NAME:

即你目标机target所在的操作系统名称，比如ARM或者Linux你就需要写"Linux",如果Windows平台你就写"Windows",如果你的嵌入式平台没有相关OS你即需要写成"Generic",只有当CMAKE_SYSTEM_NAME这个变量被设置了，CMake才认为此时正在交叉编译，它会额外设置一个变量CMAKE_CROSSCOMPILING为TRUE.

CMAKE_C_COMPILER

顾名思义，即C语言编译器，这里可以将变量设置成完整路径或者文件名，设置成完整路径有一个好处就是CMake会去这个路径下去寻找编译相关的其他工具比如linker,binutils等，如果你写的文件名带有arm-elf等等前缀，CMake会识别到并且去寻找相关的交叉编译器。

CMAKE_CXX_COMPILER

同上，此时代表的是C++编译器。

CMAKE_FIND_ROOT_PATH

代表了一系列的相关文件夹路径的根路径的变更，比如你设置了/opt/arm/,所有的Find_xxx.cmake都会优先根据这个路径下的/usr/lib,/lib等进行查找，然后才会去你自己的/usr/lib和/lib进行查找，如果你有一些库是不被包含在/opt/arm里面的，你也可以显示指定多个值给CMAKE_FIND_ROOT_PATH

CMAKE_FIND_ROOT_PATH_MODE_PROGRAM:

对FIND_PROGRAM()起作用，有三种取值，NEVER,ONLY,BOTH,第一个表示不在你CMAKE_FIND_ROOT_PATH下进行查找，第二个表示只在这个路径下查找，第三个表示先查找这个路径，再查找全局路径，对于这个变量来说，一般都是调用宿主机的程序，所以一般都设置成NEVER.

CMAKE_FIND_ROOT_PATH_MODE_LIBRARY

对FIND_LIBRARY()起作用，表示在链接的时候的库的相关选项，因此这里需要设置成ONLY来保证我们的库是在交叉环境中找的.

CMAKE_FIND_ROOT_PATH_MODE_INCLUDE:

对FIND_PATH()和FIND_FILE()起作用，一般来说也是ONLY,如果你想改变，一般也是在相关的FIND命令中增加option来改变局部设置，有NO_CMAKE_FIND_ROOT_PATH,ONLY_CMAKE_FIND_ROOT_PATH,BOTH_CMAKE_FIND_ROOT_PATH

add_compile_options

添加编译时的参数

add_definitions

添加编译时的宏

add_link_options

添加链接参数

作者：罗蓁蓁
链接：https://www.jianshu.com/p/03a0ba0578ad
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

C++ ORM框架:SQLPP11教程 使用vcpkg
https://blog.csdn.net/linyilong3/article/details/100853675
vcpkg install sqlpp11-connector-sqlite3
vcpkg install sqlpp11

wget https://github.com/boostorg/asio/archive/boost-1.71.0.tar.gz -O boostorg-asio-boost-1.71.0.tar.gz



wget https://sqlite.org/2019/sqlite-amalgamation-3300100.zip -O sqlite-amalgamation-3300100.zip

wangle
folly
sqlite3
fizz
libsodium



Could not locate cached archive: /root/.cache/vcpkg/archives/6c/6cf9e157da02ea725983db2111fe9a1953d65400.zip
-- Downloading https://github.com/pocoproject/poco/archive/3fc3e5f5b8462f7666952b43381383a79b8b5d92.tar.gz...

  Package: poco:x64-linux
  Vcpkg version: 2020.06.15-unknownhash

  Package: poco:x64-linux
  Vcpkg version: 2019.09.12-unknownhash



vcpkg mingw
https://blog.csdn.net/weixin_40448140/article/details/109111042

vcpkg 打包成rpm deb
windows mac c/c++库格式



vcpkg 2020-11这个tag，缓存在
/root/.cache/vcpkg/archives/cb/

vcpkg 2019版本，缓存在

vcpkg下载github上面的源码包

自定义c++库，vcpkg如何处理
自定义rust go库，cargo等如何处理

Starting package 30/84: boost-mpl:x64-linux
Building package boost-mpl[core]:x64-linux...
Could not locate cached archive: /root/.cache/vcpkg/archives/cb/cb5e93e30070ece9c8c294d8ed275fc74689c054.zip
-- Downloading https://github.com/boostorg/mpl/archive/boost-1.73.0.tar.gz...

mac thrift失败

centos 7 gcc7 folley失败





```shell
./vcpkg/vcpkg install gtest
The following packages will be built and installed:
    gtest[core]:x64-osx
Starting package 1/1: gtest:x64-osx
Building package gtest[core]:x64-osx...
-- Using cached /Users/ibqo/vcpkg/downloads/google-googletest-cd17fa2abda2a2e4111cdabd62a87aea16835014.tar.gz
-- Using source at /Users/ibqo/vcpkg/buildtrees/gtest/src/ea16835014-2505ff1bf1
-- Configuring x64-osx-dbg
-- Configuring x64-osx-rel
-- Building x64-osx-dbg
-- Building x64-osx-rel
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest_main.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-all.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-death-test.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-filepath.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-internal-inl.h
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-matchers.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-port.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-printers.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-test-part.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/src/gtest-typed-test.cc
-- Installing: /Users/ibqo/vcpkg/packages/gtest_x64-osx/share/gtest/copyright
-- Performing post-build validation
The following files are placed in
/Users/ibqo/vcpkg/packages/gtest_x64-osx:
```





如果你指的是已有的库需要指定特定版本，请使用. /vcpkg x-history <portname> 来查看当前查询的库的更新记录。并根据版本号选择离下个版本最近的修正版，获取commit Id。再根据commit Id使用git reset命令回退版本至你指定的版本。

最后build就完事啦！



要是能vcpkg install curl(1.3)[openssl(1.0.2k),sspi] 就牛逼了，或者指定commitid
未来不是没有可能。不过兼容性问题很麻烦。





vcpkg查看库依赖

./vcpkg/vcpkg depend-info grpc
openssl-unix:
c-ares:
openssl: openssl-unix
protobuf:
zlib:
grpc: c-ares, openssl, protobuf, zlib





编译代码的选项在哪儿？



triplets/x64-osx.cmake

```shell
set(VCPKG_TARGET_ARCHITECTURE x64)
set(VCPKG_CRT_LINKAGE dynamic)
set(VCPKG_LIBRARY_LINKAGE static)

set(VCPKG_CMAKE_SYSTEM_NAME Darwin)

```

编译成.a静态库

可以编译成动态库吗？

VCPKG_LIBRARY_LINKAGE dynamic









同一个主机，使用同一个编译器gccg++去编译源代码

go

rust都是这样干的



mac平台



zstd_1.4.0-1_x64-osx.list

installed/vcpkg/info/zstd_1.4.0-1_x64-osx.list

installed/x64-osx/



zstd_1.4.0-1_x64-osx.list内容见zstd_1.4.0-1_x64-osx.list文件



centos平台



zstd_1.4.0-1_x64-linux.list

```shell
x64-linux/
x64-linux/debug/
x64-linux/debug/lib/
x64-linux/debug/lib/libzstdd.a
x64-linux/debug/lib/pkgconfig/
x64-linux/debug/lib/pkgconfig/libzstd.pc
x64-linux/include/
x64-linux/include/cover.h
x64-linux/include/zbuff.h
x64-linux/include/zdict.h
x64-linux/include/zstd.h
x64-linux/include/zstd_errors.h
x64-linux/lib/
x64-linux/lib/libzstd.a
x64-linux/lib/pkgconfig/
x64-linux/lib/pkgconfig/libzstd.pc
x64-linux/share/
x64-linux/share/zstd/
x64-linux/share/zstd/COPYING
x64-linux/share/zstd/LICENSE
x64-linux/share/zstd/copyright
x64-linux/share/zstd/vcpkg_abi_info.txt

```





编译好的库文件在packages




`wget https://github.com/boostorg/math/archive/boost-1.71.0.tar.gz -O /Users/ibqo/vcpkg/downloads/boostorg-math-boost-1.71.0.tar.gz`



vcpkg 编译结果 packages/zstd_x64-linux/lib/lizstd.a





vcpkg install 流程

下载源代码到downloads/temp

解压

编译




vcpkg install opencv

wget https://github.com/glennrp/libpng/archive/v1.6.37.tar.gz

放到/root/vcpkg/downloads/temp/glennrp-libpng-v1.6.37.tar.gz





最新版要求gcc 7版本以上

```shell
./bootstrap-vcpkg.sh 
Downloading ninja...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   619  100   619    0     0    148      0  0:00:04  0:00:04 --:--:--   148
100 77854  100 77854    0     0  12509      0  0:00:06  0:00:06 --:--:--  137k
Downloading ninja... done.
Extracting ninja...
Extracting ninja... done.
CXX (g++) is too old; please install a newer compiler such as g++-7.
On Ubuntu try the following:
  sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
  sudo apt-get update -y
  sudo apt-get install g++-7 -y
On CentOS try the following:
  sudo yum install centos-release-scl -y
  sudo yum install devtoolset-7 -y
  scl enable devtoolset-7 bash
```


如何用brew apt yum安装vcpkg

自己打包vcpkg deb rpm包

cpack





Vcpkg新增库简易指南

看vcpkg下的doc文件，有例子



https://www.jianshu.com/p/9b72a57499c6





### Vcpkg的优点

- 自动下载开源库源代码
- 源码包的缓存管理和版本管理，可以升级版本
- 轻松编译
- 依赖关系检查（比如编译libcurl，会自动下载zlib、openssl进行编译）
- 无缝集成Visual Studio，不需要设置库文件、头文件的所在目录，自动集成。
- Visual Studio全平台支持，不仅支持Debug/Release、x86/x64编译，还支持UWP、ARM平台的编译。



https://docs.microsoft.com/zh-cn/cpp/build/vcpkg?



安装时，忽略下载cmake，ninja

在该目录下创建downloads,将自行下载的压缩包放入该目录下

```
sudo cp ninja-linux-1.8.2.zip /usr/local/vcpkg/downloads
sudo cp cmake-3.14.0-Linux-x86_64.tar.gz /usr/local/vcpkg/downloads
```

https://blog.csdn.net/cyh5272/article/details/103214932

vcpkg install xxx 安装开源库到本地

cmake配置 clion
find_package()

build


vcpkg支持vs
qtcreator
eclipse

自己写的库，如何支持vcpkg



-DCMAKE-BUILD-TYPE=Debug

-DCMAKE-BUILD-TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake
同时安装32bit和64bit

`vcpkg install cpprestsdk cpprestsdk:x64-windows`
`vcpkg install libxml2 libxml2:x64-windows`
`vcpkg install wangle wangle:x64-windows`
`vcpkg install boost-test:x64-osx`

vcpkg install cpp-netlib cpp-netlib:x64-windows

Boost.Test

`vcpkg install boost-test boost-test:x64-windows`

```
The package libxml2 is compatible with built-in CMake targets:

    find_package(LibXml2 REQUIRED)
    target_include_directories(main PRIVATE ${LIBXML2_INCLUDE_DIR})
    target_link_libraries(main PRIVATE ${LIBXML2_LIBRARIES})

The package libxml2 is compatible with built-in CMake targets:

    find_package(LibXml2 REQUIRED)
    target_include_directories(main PRIVATE ${LIBXML2_INCLUDE_DIR})
    target_link_libraries(main PRIVATE ${LIBXML2_LIBRARIES})
    
```



类似的工具：mac平台brew，linux的apt pkg yum
vcpkg 支持linux Widnows Mac


xxx-dev



https://github.com/microsoft/vcpkg/issues/9386

我用过的的Linux包管理器都不能做到这个，除非源管理者将不同版本的软件视作不同的软件，比如libpng12和libpng16、Gtk2和Gtk3。

windows安装会假死

Vcpkg仅支持Visual Studio 2015 update 3及以上版本（包括Visual Studio 2017），究其原因，很可能和c++11的支持度以及集成原理有关系。
目前Vcpkg编译静态库，默认只支持MT模式。

mac安装vcpkg
https://blog.csdn.net/jia_gushuai/article/details/85597347



- downloads  下载的源码
- buildtrees 安装后展开


计算机架构
vcpkg.exe help triplet
Available architecture triplets:
  arm-uwp
  arm-windows
  arm64-uwp
  arm64-windows
  x64-linux
  x64-osx
  x64-uwp
  x64-windows
  x64-windows-static
  x86-uwp
  x86-windows
  x86-windows-static




vcpkg integrate project
Created nupkg: D:\vcpkg\scripts\buildsystems\vcpkg.D.vcpkg.1.0.0.nupkg

With a project open, go to Tools->NuGet Package Manager->Package Manager Console and paste:
 




vcpkg integrate install
Applied user-wide integration for this vcpkg root.

All MSBuild C++ projects can now #include any installed libraries.
Linking will be handled automatically.
Installing new libraries will make them instantly available.

CMake projects should use: "-DCMAKE_TOOLCHAIN_FILE=D:/vcpkg/scripts/buildsystems/vcpkg.cmake"

通过powershell下载cpprestsdk:x64-windows失败，手动下载brotli-1.0.7.tar.gz放在$vcpkg/downloads下失败，因为正确的文件名称是google-brotli-v1.0.7.tar.gz
https://github.com/microsoft/vcpkg/issues/9485

-- Using cached D:/vcpkg/downloads/google-glog-v0.4.0.tar.gz
-- Using source at D:/vcpkg/buildtrees/glog/src/v0.4.0-46ccbc49a4







# vckpg

···

vcpkg install gtest
The following packages will be built and installed:
    gtest[core]:x86-windows
Starting package 1/1: gtest:x86-windows
Building package gtest[core]:x86-windows...
Warning: The following VS instances are excluded because the English language pack is unavailable.
    D:\Program Files\Microsoft Visual Studio\2019\Professional
Please install the English language pack.
Could not locate a complete toolset.
The following paths were examined:
    C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat
    D:\Program Files\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvarsall.bat
    D:\Program Files\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.23.28105\bin\HostX86\x86\dumpbin.exe

···


https://github.com/Microsoft/vcpkg/issues/3842


···

The package gtest is compatible with built-in CMake targets:

    enable_testing()
    
    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)
    
    add_test(AllTestsInMain main)

···


[Visual Studio开源库集成器Vcpkg全教程--利用Vcpkg轻松集成开源第三方库](https://blog.csdn.net/cjmqas/article/details/79282847)


`vckpg search`

4. Vcpkg和Visual Studio的集成
   4.1. 什么是集成？
   上面我们已经安装了一些第三方库，那如何使用呢？常规情况下，我们需要设置include目录、lib目录等，会有很多工作量。Vcpkg提供了一套机制，可以全自动的适配目录，而开发者不需要关心已安装的库的目录在哪里，也不需要设置。这是Vcpkg的一大优势。
   4.2. 集成到全局
   “集成到全局”适用于Visual Studio开发环境和msbuild命令行。执行命令：
   vcpkg integrate install
   当出现“Applied user-wide integration for this vcpkg root.”字样的时候，说明已经集成成功。这时候可以在任意的工程中使用安装好的第三方库。
   4.3. 移除全局集成
   移除全局集成只要执行下列命令即可：
   vcpkg integrate remove
   4.4. 集成到工程
   上面已经可以集成到全局，为什么还要“集成到工程”呢？因为在大部分情况下，我们不希望集成到全局，毕竟有很多第三方库我们希望自定义处理一下，或者干脆不想集成第三方库。那么集成到工程是最灵活的处理方式。也是工程级项目推荐的处理方式。
   “集成到工程”是整个vcpkg中最复杂的一项，它需要利用Visual Studio 中的nuget插件来实现。我们接下来一步一步来说。
   4.4.1. 生成配置
   执行命令
   vcpkg integrate project
   这时候会在“\scripts\buildsystems”目录下，生成nuget配置文件.
   其中是指vcpkg实际所在目录。
   4.4.2. 基本配置
   打开Visual Studio，点击菜单“工具->NuGet包管理器->程序包管理器设置”，进入设置界面，点击“程序包源”。

点击“加号”增加一个源。修改源的名字为vcpkg。在“源”的选项中点击右侧的”…”选择vcpkg目录下的“scripts\buildsystems”目录，然后点击右侧的“更新按钮”。
点击“确定”，关闭设置对话框。
到此，全局性的设置已经完成，以后不必再重复设置了。
4.4.3. 工程配置
用Visual Studio打开一个工程或解决方案。右键点击需要设置的工程，选择“管理NuGet程序包”。在右上角的“程序包源”中选择刚刚设置的“vcpkg”。这样在“浏览”选项卡中就可以看到“vcpkg.H.Repos.vcpkg”。点击最右侧的“安装”。这样就可以集成到某个工程了。



