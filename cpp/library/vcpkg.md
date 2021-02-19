# vcpkg

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
    Install-Package vcpkg.D.vcpkg -Source "D:\vcpkg\scripts\buildsystems"




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
用Visual Studio 打开一个工程或解决方案。右键点击需要设置的工程，选择“管理NuGet程序包”。在右上角的“程序包源”中选择刚刚设置的“vcpkg”。这样在“浏览”选项卡中就可以看到“vcpkg.H.Repos.vcpkg”。点击最右侧的“安装”。这样就可以集成到某个工程了。


