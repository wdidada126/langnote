# CMake

## cmake判断操作系统
#### 检查操作系统类型


```shell
if(UNIX AND NOT APPLE)
    # Linux
    include_directories("/usr/include/mysql")

    # 添加 libmysqlclient.so 所在的目录到链接器的搜索路径
    link_directories(/usr/lib/x86_64-linux-gnu)
    target_link_libraries(yishengAttendanceData
            mysqlclient
    )

    # UNIX platforms excluding macOS
    message(STATUS "This is a Unix-like system but not macOS")

    # Check for specific distributions
    if(EXISTS "/etc/os-release")
        file(READ "/etc/os-release" OS_RELEASE_CONTENT)
        string(FIND "${OS_RELEASE_CONTENT}" "ID=ubuntu" UBUNTU_FOUND)
        string(FIND "${OS_RELEASE_CONTENT}" "ID=debian" DEBIAN_FOUND)
        string(FIND "${OS_RELEASE_CONTENT}" "ID=centos" CENTOS_FOUND)

        if(NOT ${UBUNTU_FOUND} EQUAL -1)
            message(STATUS "Running on Ubuntu")
        elseif(NOT ${DEBIAN_FOUND} EQUAL -1)
            message(STATUS "Running on Debian")
        elseif(NOT ${CENTOS_FOUND} EQUAL -1)
            message(STATUS "Running on CentOS")
        else()
            message(STATUS "Running on an unknown Unix-like system")
        endif()
    else()
        message(WARNING "Unable to detect Linux distribution: /etc/os-release not found")
    endif()
elseif(APPLE)
    message(STATUS "This is macOS")
elseif(WIN32)
    # Windows
    include_directories(
            #        ${PROJECT_SOURCE_DIR}/include
            #        "D:/git/github/vcpkg/installed/x86-windows/include/sqlpp11/mysql"
            "D:/mysql-connector-c-6.1.11-win32/include"
    )
    target_link_libraries(yishengAttendanceData "D:/mysql-connector-c-6.1.11-win32/lib/libmysql.lib")
else()
    message(FATAL_ERROR "Unsupported operating system")
endif()
```


## win cmake 生成.sln

```shell
cmake -B build_64 -S . -G "Visual Studio 17 2022" -A x64 -DCMAKE_TOOLCHAIN_FILE=D:\git\github\vcpkg\scripts\buildsystems\vcpkg.cmake
cmake -B build_32 -S . -G "Visual Studio 17 2022" -A x32 -DCMAKE_TOOLCHAIN_FILE=D:\git\github\vcpkg\scripts\buildsystems\vcpkg.cmake
```

在 CMake 中设置构建类型为 Debug 或 Release，可以通过以下几种方式来实现：

### 方法 1: 使用命令行选项

你可以在配置 CMake 时通过命令行选项 `-DCMAKE_BUILD_TYPE` 来指定构建类型：

```bash
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . --config Debug
```

或者：

```bash
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release
```

### 方法 2: 在 `CMakeLists.txt` 文件中设置默认构建类型

你可以在 `CMakeLists.txt` 文件中添加默认的构建类型：

```cmake
# Set default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()
```

### 方法 3: 使用 CMake 的预设功能

CMake 3.19 及以上版本支持使用预设来设置构建配置。在项目根目录下创建一个 `CMakePresets.json` 文件：

```json
{
  "version": 3,
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 19,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "default",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}"
    },
    {
      "name": "debug",
      "inherits": "default",
      "description": "Configure for Debug build",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "release",
      "inherits": "default",
      "description": "Configure for Release build",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ]
}
```

然后使用预设进行配置和构建：

```bash
cmake --preset debug
cmake --build build/debug
```

或：

```bash
cmake --preset release
cmake --build build/release
```

### 方法 4: 使用 CMake GUI

如果你使用的是 CMake GUI，可以在配置过程中选择构建类型。配置过程中，在“CMake Options”中添加 `CMAKE_BUILD_TYPE` 并设置为 `Debug` 或 `Release`。

### 总结

通过这些方法，你可以轻松地在 CMake 中设置构建类型为 Debug 或 Release。选择合适的方法取决于你的工作流程和项目需求。


## .pc cmake
.pc cmake生成
pkg-config介绍 通常我们在写程序时需要依赖一些库以及头文件，比如我今天用到的opencv，但库的安装位置可能不同，这时就需要一个工具能够管理并能搜索这些库的路径（头文件路径/include，库文件路径 /lib）。 pkg-config 就是通过库提供的一个 .pc 文件获得库的各种必要信息的，包括版本信息、编译和连接需要的参数等。通过 pkg-config 提供的参数(–cflags, –libs)，将所需信息提取出来供编译和连接使用。这样，不管库文件安装在哪，通过库对应的.pc文件就可以准确定位。 它提供的主要功能有：
 <1> 检查库的版本号。如果所需库的版本不满足要求，打印出错误信息，避免连接错误版本的库文件。
 <2> 获得编译预处理参数，如宏定义，头文件的路径。
 <3> 获得编译参数，如库及其依赖的其他库的位置，文件名及其他一些连接参数。
 <4> 自动加入所依赖的其他库的设置。


知乎存在的逻辑
提高交流的频率，效率
不是严肃出版物，科普，通俗介绍性的文字
包括的范围更大
推荐，方便读者查阅资料

分类，有标签，标签之间有包括关系

非法集资，大部分是合法注册(只批条，不监管?)，有公众人物站台(包括明星，专家，官员)，甚至有地方国资入股(0元购，斐讯，联壁，华夏万家金服，松江国资委)，部分官员的家属在里边工作(盛晓春系盛亚飞的女儿)，请问一句已提示风险，就轻飘飘的过去了，您觉得合适吗？


自己写redis


JAVA自己的数据结构到redis网络协议，再到redis内存。


cmake学习材料
intel tbb    Intel Thread Building Blocks (TBB)
https://github.com/oneapi-src/oneTBB/tree/v2021.7.0


if (NOT DEFINED BUILD_SHARED_LIBS)
    set(BUILD_SHARED_LIBS ON)
endif()



set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
project(zeno VERSION 1.0.0 LANGUAGES C CXX)



【【公开课】现代CMake高级教程（持续更新中）-哔哩哔哩】 https://b23.tv/GUFOCko
课件：https://github.com/parallel101/course
作业：https://github.com/parallel101/hw11（还在准备中）

set_target_properties()
target_include_directories()

cmake install()函数用法
https://blog.csdn.net/weixin_42398658/article/details/121672529
https://zhuanlan.zhihu.com/p/102955723

make 2>&1 | tee out.txt把所有输出都定向到文件同时保留屏幕显示
sudo make install 2>&1 | tee out.txt

muduo doc使用doxygen
doxygen用法？

windows支持posix

posix 标准定义了一套操作系统必须实现的api，这样的话，当你写的代码只使用了posix标准定义的接口时，那么你的代码相对于所有支持posix标准的操作系统来说，都是可移植的，最多重新编译一下就可以使用。
至于为什么Windows也要支持他？应该是为了使用符合posix标准的应用程序吧，实现了posix标准，就意味着很多只有在Linux、Unix、MAC 等操作系统的应用程序都可以在Windows下使用了。
更多的应用，就代表着更多的用户，你懂的。

github查看当前登录用户有哪些codepace

https://edidada-zany-happiness-jw6qv69vrjhpq45.github.dev/

git clone https://github.com/grpc/grpc
cd grpc/
git checkout v1.48.0
git submodule update --init
mkdir -p cmake/build
cd cmake/build
cmake ../..
make

undefined reference to xxx某个函数
怎么知道这个函数是那个库里面的？
怎么知道.cc文件被打包进哪个so文件里面

make怎么打包成库文件 g++怎么打包库文件

mvn package


leveldb需要snappy
https://www.oschina.net/p/snappy?hmsr=aladdin1e1
https://src.fedoraproject.org/repo/pkgs/snappy/

git remote set-url origin https://gitee.com/edidada/testrust.git


其实nevovim + spavevim撸也还行

apue unp
陈硕

C++服务器开发精髓
https://book.douban.com/subject/35491437/

https://book.douban.com/subject/25900403/

https://gitee.com/edidada/unix-linux-program
https://gitee.com/edidada/essential_cpp_code

ansic
fopen

posix
fnctl.h open

进程 fork
线程 pthread_create

人世间
电视剧

真没必要这么麻烦，再穷逼现在组个e5洋垃圾1200元就有16c32t的规格，多线程性能堪比10900k，编程完全没有任何压力甚至绰绰有余

https://www.linuxquestions.org/questions/linux-general-1/ubuntu-20-04-blocking-google-signin-4175688411/

回形针也是理中客，混乱博物馆更是搞科普的，其背后都有境外反华势力参与。
回形针是被自媒体曝光的，插图事件也是网络舆论发酵才引发关注的，塔里木盆地教科书的事件更是持续了十几年。
渗透和控制已经非常严重了，情报系统可能已经失能。网络平台不可能不受此影响，它们完全可以通过后台操作使拥有反华背景的自媒体成为主流。
美国过去几十年通过各种渠道引导、操控我国国民认只，整个文学影视界全面亲美，不可能错过网络时代。
睡前消息极有可能跟意林回形针一样，参考消息主持人长的很像台湾人。

CatalyzeX chrome插件

https://www.zhihu.com/answer/2779480241

严店中学旁边就是百大周谷堆

https://github.com/Kr328/ClashForAndroid

企业级ssd

企业级，航天级 民用的，不一样
你一说话，别人就默认你是在为自己谋利


答主可能没有实际操作过向各大平台申请信息披露吧，我向抖音、微信、小红书都申请过，前两个都明确告知需要法院调查令，小红书是因为不强制要求实名制，他们也没有对方的个人信息

武汉地铁我参与建设很多条线，还是比较有发言权的...
5.6k能上车地铁房不一定值得，位置真的太偏了，举个例子，21号线（阳逻线）武生院到金台这一段，价格不高，但是完全不推荐。
低价上车可能只有四新白沙洲这种没啥上涨空间，自住凑合的区域。

学习c++最新版本特性，不一定要装编译器，有线上编译环境

工业软件市场太小，就算做出来也未必有人会买账，欧特克多厉害，几乎算是工业软件里的一哥了，一年营收也就接近30亿美元


业务开发
技术应用
两个方向

整理资料，定期复习，repo

gcc是编译c的，我却在mac上用gcc编译c++代码，报错了

sonic是开源的，推荐sonic无可厚非啊。在字节跑路前用sonic优化过项目下发端的代码，对于计算密集型服务性能确实有一定提升，不过我负责的项目优化后没图中那么明显，印象中图中的项目还同时用了tango？

cmake需要手动新建CMakefile.txt吗？

mvn init

pom.xml设置jdk版本
.cmake文件

设置变量
pom.xml properries节点
cmakefile.txt
生命式
set

pom.xml一堆插件，cmake有插件吗？

conanfile.py
xmake.lua

https://blog.csdn.net/Gabriel576282253/article/details/104826413

减少重复造轮子，开源Java微信小程序商城 (前后台开源) 。快速搭建一个属于自己的微信小程序商城。QQ交流群：66502035、870579539、151602347欢迎大家进群交流技术。



```cmake
add_library (spongechecks STATIC send_equivalence_checker.cc tcp_fsm_test_harness.cc byte_stream_test_harness.cc network_interface_test_harness.cc)

macro (add_test_exec exec_name)
    add_executable ("${exec_name}" "${exec_name}.cc")
    target_link_libraries ("${exec_name}" spongechecks ${ARGN})
    target_link_libraries ("${exec_name}" sponge ${ARGN})
endmacro (add_test_exec)

add_test_exec (tcp_parser ${LIBPCAP})
add_test_exec (ipv4_parser ${LIBPCAP})
add_test_exec (fsm_active_close)
add_test_exec (fsm_passive_close)
```

https://vimeo.com/kitware

CMakeLists.txt

引用target_link_libraries()
zlib::zlib
qt
grpc:grpc
等等符号，由什么定？

在 CMakeLists.txt 文件中，引用到的符号（例如 `target_link_libraries()` 中的库名）通常由以下几个因素决定：
1. 库的名称: 该符号是指要链接的库的名称。库的名称通常由库的开发人员或项目的文档指定。例如，对于常见的库，如 zlib、Qt 和 gRPC，您可以在它们的官方文档或文档中找到相应的库名称。
2. 导入目标名称: 在 CMake 中，当使用 `find_package()` 命令查找并导入库时，会创建一个导入目标。导入目标的名称通常与库的名称相关联，但也可以在 CMakeLists.txt 文件中进行自定义。在 `target_link_libraries()` 中引用库时，可以使用导入目标的名称来指定要链接的库。
   例如，对于 `zlib` 库，您可能会使用 `find_package(ZLIB REQUIRED)` 来查找并导入库，然后使用 `target_link_libraries(your_target_name PRIVATE ZLIB::ZLIB)` 将 `your_target_name` 与导入目标 `ZLIB::ZLIB` 进行链接。
3. 库的别名: 在某些情况下，库可能会定义一个别名，用于更简洁地引用该库。例如，在 Qt 中，库通常定义了一个别名 `Qt::<module>`，其中 `<module>` 是 Qt 库的模块名称。您可以使用这些别名来链接库。
   例如，对于 Qt 的 Core 模块，您可以使用 `target_link_libraries(your_target_name PRIVATE Qt::Core)` 来链接 Core 模块。
总之，这些符号的使用方式是由库的开发人员定义的，并且通常在库的文档中有所描述。您需要根据库的名称、导入目标名称或别名来引用相应的库，并在 CMakeLists.txt 文件中使用 `target_link_libraries()` 命令将其与目标进行链接。


SQLite3Targets.cmake
ZLIBTargets.cmake
Qt6Targets.cmake

xxxTargets.cmake文件里面有

CMake preset是一个用于指定构建系统配置的JSON文件。CMake支持两个主要的配置文件：CMakePresets.json和CMakeUserPresets.json。
CMakePresets.json文件旨在指定项目范围的构建细节，它位于项目的根目录中。这个文件可以用来定义构建目标、构建类型（如Debug或Release）、构建工具链等。它还可以包含预设（presets），这些预设是一组配置选项的组合，可以方便地用于不同的构建场景。
CMakeUserPresets.json文件则旨在让开发人员自定义他们自己的本地构建细节。这个文件也位于项目的根目录中，并且可以包含用户定义的预设。这些预设可以覆盖CMakePresets.json中的相应设置，以满足开发人员的个性化需求。
在CMake中，预设可以通过命令行参数`--preset`来指定，也可以在构建工具的用户界面中选择。当指定了一个预设后，CMake会根据该预设中的配置选项来生成构建文件，并使用这些文件来构建项目。
此外，CMake还支持在预设中包含其他预设文件，这可以通过在include字段中指定其他预设文件的路径来实现。需要注意的是，CMakeUserPresets.json隐式包含CMakePresets.json，且禁止循环包含。
总的来说，CMake preset是一种方便的方式来管理和共享构建系统配置，它可以提高构建过程的效率和灵活性。

opencv是cmake组织的

cmake核心概念，target install()的时候用

llvm clang也是用cmake
lwip是cmake组织的

```
wget --no-check-certificate https://github.com/Kitware/CMake/releases/download/v3.27.9/cmake-3.27.9-linux-x86_64.tar.gz
tar -xvf cmake-3.27.9-linux-x86_64.tar.gz > /dev/null
mv cmake-3.27.9-linux-x86_64 cmake-install
pwd_path=$(pwd)
PATH=${pwd_path}/cmake-install:${pwd_path}/cmake-install/bin:$PATH
cmake --version
```
property
分类
项目
文件夹
目标
https://cmake.org/cmake/help/v3.20/manual/cmake-properties.7.html

CMAKE_C_KNOWN_FEATURES

## Command
Scripting Command
Project Command
CTest Command

判断
if()
endif

message()
get_target_property()

get_target_property(_aliased Upstream::lib1 ALIASED_TARGET)
if(_aliased)
  message(STATUS "The name Upstream::lib1 is an ALIAS for ${_aliased}.")
endif()

target_compile_definitions()
DEBUG_BUILD

`target_compile_definitions()`是CMake中的一个命令，它的主要作用是向特定的目标（例如程序、库等）的编译器添加编译定义。这些定义在编译过程中会被“输出”到生成的C源码中。

该命令的基本语法格式如下：
```cmake
target_compile_definitions(<target> <INTERFACE|PUBLIC|PRIVATE> [items1...] [<INTERFACE|PUBLIC|PRIVATE> [items2...] ...])
```
其中，`<target>`参数代表需要添加定义的目标，这个目标通常是由诸如`add_executable`或`add_library`之类的CMake命令创建的，需要注意的是，这个命名的目标不能是一个ALIAS target。而`<INTERFACE|PUBLIC|PRIVATE>`参数则用于指定这些定义的作用范围，可以是接口(INTERFACE)，公共(PUBLIC)或私有(PRIVATE)。最后的`[items1...] [<INTERFACE|PUBLIC|PRIVATE> [items2...] ...]`则是需要添加的具体编译定义项。

## CMake Generators
cmake -G
make
ninja
vs
Green Hills MULTI
Xcode

##  variable
分类
Control the Build
Languages
CTest

https://cmake.org/cmake/help/v3.16/manual/cmake-env-variables.7.html
CMAKE_MODULE_PATH

## package 分享包给其他项目引用

cmake 模块module
gcc
qt
wxWidgets
cuda啥的
android
Fortran
Dart
include(AndroidTestUtilities)  -> android_add_test_data()


configure_package_config_file()
<PackageName>Config.cmake
set_and_check()
check_required_components()

write_basic_package_version_file()

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/FooConfigVersion.cmake
  VERSION 1.2.3
  COMPATIBILITY SameMajorVersion)



```shell
mkdir temp
cd temp
wget -O cmake.tar.gz https://cmake.org/files/v3.24/cmake-3.24.4-linux-x86_64.tar.gz
tar zxvf cmake.tar.gz -C ./
export PATH=${{github.workspace}}/temp/cmake-3.24.4-linux-x86_64/bin:$PATH
```
export PATH=/cmake-3.24.4-linux-x86_64/bin:$PATH

export PATH=/home/wdidada/cmake-3.24.4-linux-x86_64/bin:$PATH

cmake 3.18.0不支持vs 2022
cmake 3.21开始，支持vs 2022
https://cmake.org/cmake/help/v3.18/manual/cmake-generators.7.html
CMake Error: Could not create named generator Visual Studio 17 2022

https://blog.csdn.net/weixin_49486457/article/details/125763660


cmake -G "MinGW Makefiles" ..      
CMake Error: Error: generator : MinGW Makefiles
Does not match the generator used previously: Ninja
Either remove the CMakeCache.txt file and CMakeFiles directory or choose a different binary directory.



## cmake使用的例子

SQLiteCpp

```cmake
file(GLOB files "*.cpp")
foreach(file ${files})
    get_filename_component(file_basename ${file} NAME_WE)
    add_executable(${file_basename} ${file})
    # note: sqlite3 already linked in top-level CMakeLists
    target_link_libraries(${file_basename} PRIVATE SQLite3)
endforeach()
```

## cmake与vcpkg conan conan2集成
conan
提供cmake函数
conan_basic_setup()

cmake是如何支持多profile的

CMake支持多profile的方式是通过配置文件（如CMakeLists.txt）中的条件判断语句来实现的。

例如，假设有test、dev、uat和prod四个环境，每个环境中都有不同的变量设置。可以在CMakeLists.txt文件中使用if语句来判断当前所处的环境，然后设置相应的变量值。

以下是一个示例：

```cmake
# 判断当前环境
if(ENV{ENV_TYPE} STREQUAL "test")
    # 设置test环境的变量值
    set(VAR1 "value1")
    set(VAR2 "value2")
elseif(ENV{ENV_TYPE} STREQUAL "dev")
    # 设置dev环境的变量值
    set(VAR1 "value3")
    set(VAR2 "value4")
elseif(ENV{ENV_TYPE} STREQUAL "uat")
    # 设置uat环境的变量值
    set(VAR1 "value5")
    set(VAR2 "value6")
elseif(ENV{ENV_TYPE} STREQUAL "prod")
    # 设置prod环境的变量值
    set(VAR1 "value7")
    set(VAR2 "value8")
else()
    # 如果环境类型不是test、dev、uat或prod，则输出错误信息并退出
    message(FATAL_ERROR "Invalid environment type: ${ENV{ENV_TYPE}}")
endif()
```

在执行CMake时，可以通过设置`ENV{ENV_TYPE}`环境变量来指定当前所处的环境。例如，如果要使用test环境，可以执行以下命令：

```bash
export ENV_TYPE=test && cmake ..
```

cmake脚本判断不同的c++编译器版本，os版本

在CMakeLists.txt文件中，可以使用`CMAKE_CXX_COMPILER_VERSION`变量来获取当前使用的C++编译器版本。同时，可以使用`CMAKE_SYSTEM_NAME`和`CMAKE_SYSTEM_VERSION`变量来获取操作系统的名称和版本。

以下是一个示例：

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject)

# 获取C++编译器版本
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    message("使用GCC编译器")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message("使用Clang编译器")
else()
    message("使用其他编译器")
endif()

# 获取操作系统名称和版本
message("操作系统： ${CMAKE_SYSTEM_NAME}")
message("操作系统版本： ${CMAKE_SYSTEM_VERSION}")
```

这个脚本首先检查C++编译器的类型，然后输出相应的信息。接下来，它输出操作系统的名称和版本。

sudo yum install cmake3 -y

`include(FetchContent)` 是 CMake 中的一条指令，用于包含 FetchContent 模块。FetchContent 模块是 CMake 3.11 版本引入的功能，用于在构建过程中自动下载和构建依赖项。
`FetchContent_Declare` 是 FetchContent 模块提供的命令之一，用于声明要下载的依赖项。在你的示例中，它声明了一个名为 "Poco" 的依赖项，并指定了其下载地址为 https://github.com/pocoproject/poco/archive/refs/tags/poco-1.10.1-release.zip。
`FetchContent_MakeAvailable` 是 FetchContent 模块提供的另一个命令，用于下载和构建声明的依赖项，并使其可用于当前的 CMake 构建过程。在你的示例中，它将下载并构建名为 "Poco" 的依赖项，并将其添加到当前的 CMake 构建中，以供你的项目使用。
使用 FetchContent 模块可以方便地管理和自动下载依赖项，而无需手动下载和配置它们。这对于简化项目的构建过程和确保依赖项的一致性非常有用。

mkdir build && cd build && cmake .. && cmake --build . -j6
对于 cmake 3.13+ 也可以使用如下命令进行编译:
cmake -B build && cmake --build build -j6

cmake支持c#吗？
CMake 3.8版本开始支持生成Visual Studio C#项目，因此CMake支持C#。默认情况下，它将.csproj文件中的语言版本（" LangVersion"）设置为版本3。此外，CMake现在还可能支持C、C++、Fortran、Objective C和CUDA。

modern cmake
配置期运行命令
编译器运行命令 add_custom_command

https://cliutils.gitlab.io/modern-cmake/
https://github.com/onqtam/awesome-cmake
https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1

cmake 太折磨了，喜欢xmake或者scons这种用已有脚本语言的模式

https://github.com/parallel101/course/blob/master/11/01_source/00/CMakeLists.txt

### cmake

cmake总文档
https://cmake.org/cmake/help/v3.25/genindex.html

project(Snappy VERSION 1.1.8 LANGUAGES C CXX)

option()

https://cmake.org/cmake/help/latest/command/option.html

CMake之Option使用简介
https://blog.csdn.net/lhl_blog/article/details/123553686

message()
https://cmake.org/cmake/help/latest/command/message.html

include(TestBigEndian)
test_big_endian(SNAPPY_IS_BIG_ENDIAN)

include(CheckIncludeFile)
check_include_file("byteswap.h" HAVE_BYTESWAP_H)

include(CheckLibraryExists)
check_library_exists(z zlibVersion "" HAVE_LIBZ)

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("/arch:AVX" HAVE_VISUAL_STUDIO_ARCH_AVX)

https://cmake.org/cmake/help/latest/command/include.html

cmake变量
CMAKE_CXX_FLAGS

${PROJECT_VERSION}

${PROJECT_VERSION_MAJOR}

${PROJECT_SOURCE_DIR}

${PROJECT_BINARY_DIR}

${PROJECT_SOURCE_DIR}

https://cmake.org/cmake/help/v3.25/variable/PROJECT_BINARY_DIR.html#variable:PROJECT_BINARY_DIR

grpc使用cmake
grpc_build_log.txt

```shell
wdidada@wdidada-E550:~/CLionProjects/snappy-1.1.8/cmake-build-release$ sudo make install
[sudo] wdidada 的密码： 
[ 62%] Built target snappy
[100%] Built target snappy_unittest
Install the project...
-- Install configuration: "Release"
-- Installing: /usr/local/lib/libsnappy.a
-- Installing: /usr/local/include/snappy-c.h
-- Installing: /usr/local/include/snappy-sinksource.h
-- Installing: /usr/local/include/snappy.h
-- Installing: /usr/local/include/snappy-stubs-public.h
-- Installing: /usr/local/lib/cmake/Snappy/SnappyTargets.cmake
-- Installing: /usr/local/lib/cmake/Snappy/SnappyTargets-release.cmake
-- Installing: /usr/local/lib/cmake/Snappy/SnappyConfig.cmake
-- Installing: /usr/local/lib/cmake/Snappy/SnappyConfigVersion.cmake
```
cmake -B build -S

cmake --install
cmake --build

cmake 2
cmake 3 现代cmake

### cmake指令伴随一个项目的生命周期
Generate a Project Buildsystem
 cmake [<options>] <path-to-source | path-to-existing-build>
 cmake [<options>] -S <path-to-source> -B <path-to-build>

Build a Project
 cmake --build <dir> [<options>] [-- <build-tool-options>]

Install a Project
 cmake --install <dir> [<options>]

Open a Project
 cmake --open <dir>

Run a Script
 cmake [-D <var>=<value>]... -P <cmake-script-file>

Run a Command-Line Tool
 cmake -E <command> [<options>]

Run the Find-Package Tool
 cmake --find-package [<options>]

Run a Workflow Preset
 cmake --workflow [<options>]

View Help
 cmake --help[-<topic>]

cmake -S ./sample -B ./binary -G "Ninja" -A x64

### 内置环境变量
CMAKE_CPP_FLAGS
CMAKE_CXX_FLAGS

为了让下游能够方便的使用我们发布的库，我们通常会提供两种配置之一： Find模块或CONFIG模块。
对于find模块(Find<PACKAGE_NAME>.cmake)来说，它并不能根据库的更新来被动升级，所以经常会出现一些bug。而使用cmake导出的CONFIG模块更加合适。
在这篇教程中，我将展示将库导出为CONFIG模块的各个函数及用法。
https://zhuanlan.zhihu.com/p/488700798
https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html#id6

CMake 导出库的头文件GenerateExportHeader
https://www.cnblogs.com/fortunely/p/16297277.html
https://cmake.org/cmake/help/v3.0/module/GenerateExportHeader.html
generate_export_header()
install()  虽然cmake提供了export函数，但是现在已经被 install(EXPORT) 所替代。在这里我只讲解后者。

当然，还可以添加其他关键字例如：

SHARED 声明该库仅被作为动态库生成
STATIC 声明该库仅被作为静态库生成
OBJECT 声明该target仅生成中间binary文件，以供其他target使用
INTERFACE 声明该库仅是一个接口而并没有属于自己的binary
ALIAS 声明该库仅是其他库的别名
IMPORTED 声明该库不需要构建，而是已被导入具体配置。此方式一般存在于依赖提供的配置中。
上述关键字只能在 add_library 中被声明。

```cmake
# Install
############################################################

# Binaries
install(TARGETS cmake_examples_inst_bin
        DESTINATION bin)

# Library
# Note: may not work on windows
install(TARGETS cmake_examples_inst
        LIBRARY DESTINATION lib)

# Header files
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/
        DESTINATION include)

# Config
install(FILES cmake-examples.conf
        DESTINATION etc)
```

```shell
cmake --install cmake-build-debug
-- Install configuration: "Debug"
-- Installing: /usr/local/bin/cmake_examples_inst_bin
-- Installing: /usr/local/lib/libcmake_examples_inst.dylib
-- Up-to-date: /usr/local/include
-- Installing: /usr/local/include/Hello.h
-- Installing: /usr/local/etc/cmake-examples.conf
```


SET(EXECUTABLE_OUTPUT_PATH "${PROJECT_SOURCE_DIR}/lib")


例子
https://gitee.com/edidada/cmake_library_install

brpc
cmake组织

新近文件夹，新建CMakeFile.txt

```shell
ibqodembp:~ ibqo$ cmake -h
Usage

  cmake [options] <path-to-source>
  cmake [options] <path-to-existing-build>
  cmake [options] -S <path-to-source> -B <path-to-build>

Specify a source directory to (re-)generate a build system for it in the
current working directory.  Specify an existing build directory to
re-generate its build system.

Options
  -S <path-to-source>          = Explicitly specify a source directory.
  -B <path-to-build>           = Explicitly specify a build directory.
  -C <initial-cache>           = Pre-load a script to populate the cache.
  -D <var>[:<type>]=<value>    = Create or update a cmake cache entry.
  -U <globbing_expr>           = Remove matching entries from CMake cache.
  -G <generator-name>          = Specify a build system generator.
  -T <toolset-name>            = Specify toolset name if supported by
                                 generator.
  -A <platform-name>           = Specify platform name if supported by
                                 generator.
  --toolchain <file>           = Specify toolchain file
                                 [CMAKE_TOOLCHAIN_FILE].
  --install-prefix <directory> = Specify install directory
                                 [CMAKE_INSTALL_PREFIX].
  -Wdev                        = Enable developer warnings.
  -Wno-dev                     = Suppress developer warnings.
  -Werror=dev                  = Make developer warnings errors.
  -Wno-error=dev               = Make developer warnings not errors.
  -Wdeprecated                 = Enable deprecation warnings.
  -Wno-deprecated              = Suppress deprecation warnings.
  -Werror=deprecated           = Make deprecated macro and function warnings
                                 errors.
  -Wno-error=deprecated        = Make deprecated macro and function warnings
                                 not errors.
  --preset <preset>,--preset=<preset>
                               = Specify a configure preset.
  --list-presets               = List available presets.
  -E                           = CMake command mode.
  -L[A][H]                     = List non-advanced cached variables.
  --build <dir>                = Build a CMake-generated project binary tree.
  --install <dir>              = Install a CMake-generated project binary
                                 tree.
  --open <dir>                 = Open generated project in the associated
                                 application.
  -N                           = View mode only.
  -P <file>                    = Process script mode.
  --find-package               = Legacy pkg-config like mode.  Do not use.
  --graphviz=[file]            = Generate graphviz of dependencies, see
                                 CMakeGraphVizOptions.cmake for more.
  --system-information [file]  = Dump information about this system.
  --log-level=<ERROR|WARNING|NOTICE|STATUS|VERBOSE|DEBUG|TRACE>
                               = Set the verbosity of messages from CMake
                                 files.  --loglevel is also accepted for
                                 backward compatibility reasons.
  --log-context                = Prepend log messages with context, if given
  --debug-trycompile           = Do not delete the try_compile build tree.
                                 Only useful on one try_compile at a time.
  --debug-output               = Put cmake in a debug mode.
  --debug-find                 = Put cmake find in a debug mode.
  --trace                      = Put cmake in trace mode.
  --trace-expand               = Put cmake in trace mode with variable
                                 expansion.
  --trace-format=<human|json-v1>
                               = Set the output format of the trace.
  --trace-source=<file>        = Trace only this CMake file/module.  Multiple
                                 options allowed.
  --trace-redirect=<file>      = Redirect trace output to a file instead of
                                 stderr.
  --warn-uninitialized         = Warn about uninitialized values.
  --no-warn-unused-cli         = Don't warn about command line options.
  --check-system-vars          = Find problems with variable usage in system
                                 files.
  --profiling-format=<fmt>     = Output data for profiling CMake scripts.
                                 Supported formats: google-trace
  --profiling-output=<file>    = Select an output path for the profiling data
                                 enabled through --profiling-format.
  --help,-help,-usage,-h,-H,/? = Print usage information and exit.
  --version,-version,/V [<f>]  = Print version number and exit.
  --help-full [<f>]            = Print all help manuals and exit.
  --help-manual <man> [<f>]    = Print one help manual and exit.
  --help-manual-list [<f>]     = List help manuals available and exit.
  --help-command <cmd> [<f>]   = Print help for one command and exit.
  --help-command-list [<f>]    = List commands with help available and exit.
  --help-commands [<f>]        = Print cmake-commands manual and exit.
  --help-module <mod> [<f>]    = Print help for one module and exit.
  --help-module-list [<f>]     = List modules with help available and exit.
  --help-modules [<f>]         = Print cmake-modules manual and exit.
  --help-policy <cmp> [<f>]    = Print help for one policy and exit.
  --help-policy-list [<f>]     = List policies with help available and exit.
  --help-policies [<f>]        = Print cmake-policies manual and exit.
  --help-property <prop> [<f>] = Print help for one property and exit.
  --help-property-list [<f>]   = List properties with help available and
                                 exit.
  --help-properties [<f>]      = Print cmake-properties manual and exit.
  --help-variable var [<f>]    = Print help for one variable and exit.
  --help-variable-list [<f>]   = List variables with help available and exit.
  --help-variables [<f>]       = Print cmake-variables manual and exit.

Generators

The following generators are available on this platform (* marks default):
* Unix Makefiles               = Generates standard UNIX makefiles.
  Ninja                        = Generates build.ninja files.
  Ninja Multi-Config           = Generates build-<Config>.ninja files.
  Xcode                        = Generate Xcode project files.
  CodeBlocks - Ninja           = Generates CodeBlocks project files.
  CodeBlocks - Unix Makefiles  = Generates CodeBlocks project files.
  CodeLite - Ninja             = Generates CodeLite project files.
  CodeLite - Unix Makefiles    = Generates CodeLite project files.
  Eclipse CDT4 - Ninja         = Generates Eclipse CDT 4.0 project files.
  Eclipse CDT4 - Unix Makefiles= Generates Eclipse CDT 4.0 project files.
  Kate - Ninja                 = Generates Kate project files.
  Kate - Unix Makefiles        = Generates Kate project files.
  Sublime Text 2 - Ninja       = Generates Sublime Text 2 project files.
  Sublime Text 2 - Unix Makefiles
                               = Generates Sublime Text 2 project files.
```

作者：SynTimes https://www.bilibili.com/read/cv15986541/
出处：bilibili

### 创建新项目

cmake引用conan管理的库

https://gitee.com/edidada/cmake_library_install
https://cmake.org/cmake/help/v3.16/manual/cmake-buildsystem.7.html



学习cmake的材料
https://gitee.com/edidada/test-open-xlsx
test-open-xlsx/ OpenXLSX / CMakeLists.txt 
 

### 使用cmake组织的开源项目

- mysql


https://github.com/edidada/mysql-5.6.26/blob/master/CMakeLists.txt

### cmake命令

aux_source_directory 命令
aux_source_directory(<dir> <variable>)

add_subdirectory
add_executable
target_link_libraries
option


让 CMake 支持 gdb 的设置也很容易，只需要指定 Debug 模式下开启 -g 选项：



cmake 中文互联网有一堆老版本cmake的教程

查找三方库
find() 错
find_package() 对

[CMakeList.txt在大型文件应用（SLAM常用库添加依赖项）](https://zhuanlan.zhihu.com/p/149191302)


```
gcc test.c -g
```


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



https://github.com/BrightXiaoHan/CMakeTutorial

cmakefiles.txt如何配置



添加子文件夹的函数时
add_subdirectory
不是 add_includexxx

-DCMAKE_TOOLCHAIN_FILE=/Users/ibqo/vcpkg/scripts/buildsystems/vcpkg.cmake

`cmake -DCMAKE_TOOLCHAIN_FILE=/home/wdidada/vcpkg/scripts/buildsystems/vcpkg.cmake ..`

-DCMAKE_TOOLCHAIN_FILE

CMAKE_TOOLCHAIN_FILE
absolute or relative path to a cmake script which sets up all the toolchain related variables mentioned above

CMAKE给交叉编译预留了一个变量CMAKE_TOOLCHAIN_FILE，它定义了一个.cmake文件的路径，该文件里面设置了一系列CMAKE变量和属性，比如C_COMPILER，CXX_COMPILER等。.cmake文件的好处是一次编写多次使用，不同平台架构的交叉编译工具链可以编写一个独立的toolchain.cmake文件，而工程的CMakeLists.txt可以编写为通用格式，对工具链不可见。cmake脚本可以如下形式：

cmake -DCMAKE_TOOLCHAIN_FILE=./toolchains/ndk64-toolchain.cmake .. && make
cmake -DCMAKE_TOOLCHAIN_FILE=./toolchain/ndk32-toolchain.cmake .. && make
toolchain.cmake demo
set(CMAKE_SYSTEM_NAME Android)
set(CMAKE_ANDROID_API 21)
set(CMAKE_ANDROID_ARCH_ABI aarch64)
set(CMAKE_ANDROID_STL_TYPE gnustl_static)
set(TOOLCHAIN_PATH /opt/sdk/android-aarch64)# 
set(ANDROID_LIB_PATH ${TOOLCHAIN_PATH}/sysroot/usr/lib)
set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/aarch64-linux-android-gcc)
set(CMAKE_C_FLAGS "-D__ANDROID_API__=21  -fno-exceptions -O2 -fpie -fpic -fPIE -fPIC -pie -lm -Wl,-llog" CACHE STRING "" FORCE)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/aarch64-linux-android-g++)set(CMAKE_CXX_FLAGS 



cmake 添加头文件目录
https://www.cnblogs.com/binbinjx/p/5626916.html
添加头文件目录INCLUDE_DIRECTORIES
语法：
include_directories([AFTER|BEFORE] [SYSTEM] dir1 [dir2 ...])
它相当于g++选项中的-I参数的作用，也相当于环境变量中增加路径到CPLUS_INCLUDE_PATH变量的作用。

include_directories(../../../thirdparty/comm/include)


- 多文件夹 maven也支持
- 设定名称 版本 是库还是程序
- 引用依赖 find
- 执行本地命令 protoc maven是通过插件实现的

cmake新建一个项目，mysqlclient pthread

libmysqlclient.so.20
vertx-core-3.8.5.jar

pom.xml
CMakeLists.txt

project(cmaketest VERSION 1.0.0 LANGUAGES C CXX)

maven标记一个项目groupId architect artifactId version

设置版本号

https://blog.csdn.net/lianshaohua/article/details/107980612

`include_directories(mylib1name PUBLIC include)`

.h .cc/.cpp分开的 

rpmbuild spec CMake 创建项目的rpm 包

https://blog.csdn.net/henry860916/article/details/50443574

https://blog.csdn.net/wudongxu/article/details/6804536

CMake中包含的三个工具（cmake cpack ctest）

cpack

ctest ctest连接gtest boost.test

rpm

deb

包



类比maven

jar 本质是一压缩格式，winrar可以打开

war



aar


=======
cmake module模块
```shell
cmake --help-module-list
AddFileDependencies
AndroidTestUtilities
BundleUtilities
CMakeAddFortranSubdirectory
CMakeBackwardCompatibilityCXX
CMakeDependentOption
CMakeDetermineVSServicePack
CMakeExpandImportedTargets
CMakeFindDependencyMacro
CMakeFindFrameworks
CMakeFindPackageMode
CMakeForceCompiler
CMakeGraphVizOptions
CMakePackageConfigHelpers
CMakeParseArguments
CMakePrintHelpers
CMakePrintSystemInformation
CMakePushCheckState
CMakeVerifyManifest
CPack
CPackArchive
CPackBundle
CPackComponent
CPackCygwin
CPackDMG
CPackDeb
CPackFreeBSD
CPackIFW
CPackIFWConfigureFile
CPackNSIS
CPackNuGet
CPackPackageMaker
CPackProductBuild
CPackRPM
CPackWIX
CSharpUtilities
CTest
CTestCoverageCollectGCOV
CTestScriptMode
CTestUseLaunchers
CheckCCompilerFlag
CheckCSourceCompiles
CheckCSourceRuns
CheckCXXCompilerFlag
CheckCXXSourceCompiles
CheckCXXSourceRuns
CheckCXXSymbolExists
CheckFortranCompilerFlag
CheckFortranFunctionExists
CheckFortranSourceCompiles
CheckFortranSourceRuns
CheckFunctionExists
CheckIPOSupported
CheckIncludeFile
CheckIncludeFileCXX
CheckIncludeFiles
CheckLanguage
CheckLibraryExists
CheckOBJCCompilerFlag
CheckOBJCSourceCompiles
CheckOBJCSourceRuns
CheckOBJCXXCompilerFlag
CheckOBJCXXSourceCompiles
CheckOBJCXXSourceRuns
CheckPIESupported
CheckPrototypeDefinition
CheckStructHasMember
CheckSymbolExists
CheckTypeSize
CheckVariableExists
Dart
DeployQt4
Documentation
ExternalData
ExternalProject
FeatureSummary
FetchContent
FindALSA
FindASPELL
FindAVIFile
FindArmadillo
FindBISON
FindBLAS
FindBZip2
FindBacktrace
FindBoost
FindBullet
FindCABLE
FindCUDA
FindCURL
FindCVS
FindCoin3D
FindCups
FindCurses
FindCxxTest
FindCygwin
FindDCMTK
FindDart
FindDevIL
FindDoxygen
FindEXPAT
FindEnvModules
FindFLEX
FindFLTK
FindFLTK2
FindFontconfig
FindFreetype
FindGCCXML
FindGDAL
FindGIF
FindGLEW
FindGLUT
FindGSL
FindGTK
FindGTK2
FindGTest
FindGettext
FindGit
FindGnuTLS
FindGnuplot
FindHDF5
FindHSPELL
FindHTMLHelp
FindHg
FindICU
FindITK
FindIce
FindIconv
FindIcotool
FindImageMagick
FindIntl
FindJNI
FindJPEG
FindJasper
FindJava
FindKDE3
FindKDE4
FindLAPACK
FindLATEX
FindLTTngUST
FindLibArchive
FindLibLZMA
FindLibXml2
FindLibXslt
FindLibinput
FindLua
FindLua50
FindLua51
FindMFC
FindMPEG
FindMPEG2
FindMPI
FindMatlab
FindMotif
FindODBC
FindOpenACC
FindOpenAL
FindOpenCL
FindOpenGL
FindOpenMP
FindOpenSSL
FindOpenSceneGraph
FindOpenThreads
FindPHP4
FindPNG
FindPackageHandleStandardArgs
FindPackageMessage
FindPatch
FindPerl
FindPerlLibs
FindPhysFS
FindPike
FindPkgConfig
FindPostgreSQL
FindProducer
FindProtobuf
FindPython
FindPython2
FindPython3
FindPythonInterp
FindPythonLibs
FindQt
FindQt3
FindQt4
FindQuickTime
FindRTI
FindRuby
FindSDL
FindSDL_image
FindSDL_mixer
FindSDL_net
FindSDL_sound
FindSDL_ttf
FindSQLite3
FindSWIG
FindSelfPackers
FindSquish
FindSubversion
FindTCL
FindTIFF
FindTclStub
FindTclsh
FindThreads
FindUnixCommands
FindVTK
FindVulkan
FindWget
FindWish
FindX11
FindXCTest
FindXMLRPC
FindXalanC
FindXercesC
FindZLIB
Findosg
FindosgAnimation
FindosgDB
FindosgFX
FindosgGA
FindosgIntrospection
FindosgManipulator
FindosgParticle
FindosgPresentation
FindosgProducer
FindosgQt
FindosgShadow
FindosgSim
FindosgTerrain
FindosgText
FindosgUtil
FindosgViewer
FindosgVolume
FindosgWidget
Findosg_functions
FindwxWidgets
FindwxWindows
FortranCInterface
GNUInstallDirs
GenerateExportHeader
GetPrerequisites
GoogleTest
InstallRequiredSystemLibraries
MacroAddFileDependencies
ProcessorCount
SelectLibraryConfigurations
SquishTestScript
TestBigEndian
TestCXXAcceptsFlag
TestForANSIForScope
TestForANSIStreamHeaders
TestForSSTREAM
TestForSTDNamespace
UseEcos
UseJava
UseJavaClassFilelist
UseJavaSymlinks
UsePkgConfig
UseSWIG
Use_wxWindows
UsewxWidgets
WriteBasicConfigVersionFile
WriteCompilerDetectionHeade
```

```shell
cmake --help-module FindSQLite3
FindSQLite3
-----------

Find the SQLite libraries, v3

IMPORTED targets
^^^^^^^^^^^^^^^^

This module defines the following ``IMPORTED`` target:

``SQLite::SQLite3``

Result variables
^^^^^^^^^^^^^^^^

This module will set the following variables if found:

``SQLite3_INCLUDE_DIRS``
  where to find sqlite3.h, etc.
``SQLite3_LIBRARIES``
  the libraries to link against to use SQLite3.
``SQLite3_VERSION``
  version of the SQLite3 library found
``SQLite3_FOUND``
  TRUE if found
```

cmake find_package()
https://blog.csdn.net/haluoluo211/article/details/80559341

.cmake文件

E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-linux-dbg\cmake_install.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\Export\share\protobuf\protobuf-targets.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\Export\share\protobuf\protobuf-targets-debug.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-targets.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-config-version.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-options.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-module.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-config.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeSystem.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeCXXCompiler.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeCCompiler.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\cmake_install.cmake
>>>>>>> 6faa5abd105d9ac215af4c26599be94f269ae80a



add_test(NAME uuid_generator COMMAND uuid_generator)

理论上只需要find_package()就可以引入一个三方库
没有最佳实践
没有资金支持


在 gRPC 的 CMakeLists.txt 文件中，c-ares 的 find_package 模式为 CONFIG（find_package(c-ares CONFIG) ），关于 find_package() 模式的解释如下：
find_package()包括module模式和config模式。
在module模式下，CMake搜索所有名为Find<package>.cmake的文件，这些文件的路径由变量由安装CMake时指定的CMAKE_MODULE_PATH变量指定。如果查找到了该文件，它会被CMake读取并被处理。如果没有找到文件，则进入config模式。
Config 模式，继续搜索<Name>config.cmake 或<low-case-name>config.cmake文件，这两个文件是安装库自动安装的。



- cpack

- ctest



https://blog.csdn.net/wlhwaii/article/details/88026673



[add thread pthread](https://www.zhihu.com/question/37189523)



CMake

参考mysql项目源码，同一个cmake项目，可以有多个可执行文件

cpp不支持module

CmakeList.txt也可以有多个
maven pom.xml也可以有多个





cmake入门

核心观点：**Learning by Doing.** 

边做边学，由浅入深，以问题驱动自己去做。比如

1.如何使用CMake创建一个可执行程序

2.如何创建一个动态库／静态库，如何配合第三方库

3.如何支持不同平台不同编译器以及其参数，如何用CMake组织多层目录的项目

4.如何自定义CMake Target

5.如何使用CMake调用外部工具等等。

学习也不用想着100%都知道了才能开始做，这对于CMake这样的工具是更加不可取的做法。无论如何，推荐一个材料叫CMake实践，搜索这个名字"CMake实践 PDF"就会出来相应的pdf。

而CMake的好处在于什么呢？一个巨大的好处就在于你不用去折腾平台了，Windows你需要创建Visual Studio项目文件，还是如何？Linux创建Makefile？OS X创建Xcode项目文件？编译选项呢？实际上大部分你的配置都会是一样的，使用CMake会给你很好的项目维护性，也会降低你的维护成本。

抽象

定义cmakefile.txt



 `CMAKE_INSTALL_PREFIX`  

https://packages.ubuntu.com/eoan/all/rapidjson-dev/filelist 



```
/usr/lib/cmake/RapidJSON/RapidJSONConfig.cmake
/usr/lib/cmake/RapidJSON/RapidJSONConfigVersion.cmake
```



cmake修改文件 复制文件 获取git信息

 https://blog.csdn.net/qq_38410730/article/details/103741579 



find_package
是寻找
packageConfig.cmake
cpacage_config.cmake

[cmake_root not set module not speic](https://blog.csdn.net/lichen18848950451/article/details/79912265)



cmake可以多模块编译

gn

xmake支持cuda



参考moduo的cmakelists.txt

leveldb



[muduo](https://github.com/chenshuo/muduo/blob/master/CMakeLists.txt)





 list(APPEND CXX_FLAGS "-Wno-null-dereference") 



`**CMD#51: list** `列表操作命令。

```
  　　list(LENGTH <list> <output variable>)
  　　list(GET <list> <element index> [<element index> ...] <output variable>)
  　　list(APPEND <list> <element> [<element> ...])
  　　list(FIND <list> <value> <output variable>)
  　　list(INSERT <list> <element_index> <element> [<element> ...])
  　　list(REMOVE_ITEM <list> <value> [<value> ...])
  　　list(REMOVE_AT <list> <index> [<index> ...])
  　　list(REMOVE_DUPLICATES <list>)
  　　list(REVERSE <list>)
  　　list(SORT <list>)
```

　　使用LENGTH选项时，该命令会返回给定list的长度。

　　使用GET选项时，该命令返回list中所有被index索引的元素构成的list。

　　使用APPEND选项时，该命令将会在该list之后追加若干元素。

　　使用FIND选项时，该命令将返回list中指定的元素的索引；若果未找到，返回-1。

　　使用INSERT选项时，该命令将在list中指定的位置插入若干元素。

　　使用REMOVE_AT和REMOVE_ITEM选项将会从list中删除一些元素。它们之间的区别是：REMOVE_ITEM删除的是指定的项，而REMOVE_AT删除的是在指定索引处的项。

　　使用REMOVE_DUPLICATES选项时，该命令将删除list中的重复项。

　　使用REVERSE选项时，该命令将把list的内容就地前后倒换。

　　使用SORT选项时，该命令将按字母序对list总的内容就地排序。

　　注意：在CMake中，一个list是一个由封号;分割的一组字符串。使用set命令可以创建一个list。例如，set(var a b c d e)命令将会创建一个list：a;b;c;d;e；而set(var "a b c d e")命令创建的只是一个字符串，或者说是只有一个项的list。

　　当使用指定索引的命令格式时，如果<element index>是大于等于0的数，<element index>是从list第一个项开始的序号，list的第一项的索引是0。如果<element index>小于等于-1，这个索引是从结尾开始的逆向索引，其中-1表示的是list的最后一项。当使用负数索引时，注意它们不是从0开始！-0与0等价，它指向list的第一个成员。



[CMake 手册详解](https://blog.csdn.net/jiayizhenzhenyijia/article/details/98851886)



 find_package(CURL) 

if(CURL_FOUND)
  message(STATUS "found curl")
endif()


find_path(CARES_INCLUDE_DIR ares.h)
find_library(CARES_LIBRARY NAMES cares)


if(CARES_INCLUDE_DIR AND CARES_LIBRARY)
  message(STATUS "found cares")
endif()


[caffe的CMakeList.txt注释](https://blog.csdn.net/fuzi2012/article/details/72454532/)



 CMAKE_BUILD_TYPE 



[cmake 常用变量、常用环境变量、常用语法总结](https://blog.csdn.net/bytxl/article/details/50634868)



cmake:环境变量(environment variable)读写和if判断



[cmake语法-STREQUAL](https://blog.csdn.net/10km/article/details/51769633)



cmake语法-STREQUAL

 **STREQUAL** 用于比较字符串，相同返回 **true** 。 



### option

 option(MUDUO_BUILD_EXAMPLES "Build Muduo examples" ON) 



[CMake----if与option使用小记](https://www.cnblogs.com/rickyk/p/3872568.html)





- [cmaketest](https://github.com/edidada/cmaketest)
- 



cmake .."-DCMAKE_TOOLCHAIN_FILE=D:\vcpkg-master\vcpkg\scripts\buildsystems\vcpkg.cmake" -G"Visual Studio 14"

https://blog.csdn.net/kasteluo/article/details/81384746


cmake --check-system-vars

cmake 库有多个，顺序是？

CmakeLists.txt 
.cmake文件 作用

[cmake手册 私人撰写](https://chenxiaowei.gitbook.io/cmake-cookbook/4.0-chinese/4.4-chinese)

# README

.a 可以用压缩工具打开

.so库文件如何设置

https://blog.csdn.net/ktigerhero3

[大型项目CMakeLIsts.txt的编写规范](https://blog.csdn.net/dongfang1984/article/details/55105537)

[多目录工程的CmakeLists.txt编写](https://blog.csdn.net/ktigerhero3/article/details/70313350)

### cmake
生成makefile ninja.build之类的文件
Generator支持多种
不同操作系统支持的generator不同


[cmakelists.txt+添加子文件夹的cmakelists.txt](https://blog.csdn.net/u012258999/article/details/87161613)

```shell script
project(mainproject VERSION 1.0.0 LANGUAGES C CXX)
```
cmake是版本2.8时报错


```shell script
/home/edidada/cmake-3.14.7-Linux-x86_64/bin/cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -G "CodeBlocks - Unix Makefiles" /home/edidada/CLionProjects/cmaketest
CMake Warning (dev) at anotherproject/CMakeLists.txt:2 (project):
  Policy CMP0048 is not set: project() command manages VERSION variables.
  Run "cmake --help-policy CMP0048" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The following variable(s) would be set to empty:

    PROJECT_VERSION
    PROJECT_VERSION_MAJOR
    PROJECT_VERSION_MINOR
    PROJECT_VERSION_PATCH
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Configuring done
-- Generating done
-- Build files have been written to: /home/edidada/CLionProjects/cmaketest/cmake-build-debug

[Finished]

```

一种是用了的，设置cmake的版本为3.8
一种是`cmake_policy(SET CMP0048 NEW)`


[cmake 添加头文件目录，链接动态、静态库](https://www.cnblogs.com/binbinjx/p/5626916.html)

maven中也可以设置java版本
cmake中可以设置gcc g++版本

[cmake中使用c++11](https://blog.csdn.net/sohu_2011/article/details/51276884)


不添加c++11直接运行报错

```shell script
====================[ Build | stdarray | Debug ]================================
/home/edidada/cmake-3.14.7-Linux-x86_64/bin/cmake --build /home/edidada/CLionProjects/testc11/cmake-build-debug --target stdarray -- -j 2
Scanning dependencies of target stdarray
[ 50%] Building CXX object CMakeFiles/stdarray.dir/stdarray.cpp.o
In file included from /usr/include/c++/5/array:35:0,
                 from /home/edidada/CLionProjects/testc11/stdarray.cpp:5:
/usr/include/c++/5/bits/c++0x_warning.h:32:2: error: #error This file requires compiler and library support for the ISO C++ 2011 standard. This support must be enabled with the -std=c++11 or -std=gnu++11 compiler options.
 #error This file requires compiler and library support \
  ^
/home/edidada/CLionProjects/testc11/stdarray.cpp: In function ‘int main()’:
/home/edidada/CLionProjects/testc11/stdarray.cpp:10:5: error: ‘array’ is not a member of ‘std’
     std::array<int, 3> a1{ {1,2,3} };  // double-braces required
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:10:16: error: expected primary-expression before ‘int’
     std::array<int, 3> a1{ {1,2,3} };  // double-braces required
                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:11:5: error: ‘array’ is not a member of ‘std’
     std::array<int, 3> a2 = {1, 2, 3}; // except after =
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:11:16: error: expected primary-expression before ‘int’
     std::array<int, 3> a2 = {1, 2, 3}; // except after =
                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:5: error: ‘array’ is not a member of ‘std’
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:27: error: expected primary-expression before ‘,’ token
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                           ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:32: error: ‘a3’ was not declared in this scope
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:63: warning: extended initializer lists only available with -std=c++11 or -std=gnu++11
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                                                               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:15:15: error: ‘a1’ was not declared in this scope
     std::sort(a1.begin(), a1.end());
               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:16:23: error: ‘a2’ was not declared in this scope
     std::reverse_copy(a2.begin(), a2.end(), 
                       ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:22:15: error: ISO C++ forbids declaration of ‘s’ with no type [-fpermissive]
     for(auto& s: a3)
               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:22:18: warning: range-based ‘for’ loops only available with -std=c++11 or -std=gnu++11
     for(auto& s: a3)
                  ^
make[3]: *** [CMakeFiles/stdarray.dir/stdarray.cpp.o] Error 1
make[2]: *** [CMakeFiles/stdarray.dir/all] Error 2
make[1]: *** [CMakeFiles/stdarray.dir/rule] Error 2
make: *** [stdarray] Error 2
```



```

"D:\Program Files\CMake\bin\cmake.exe" ..  -A x64 -DCMAKE_TOOLCHAIN_FILE="D:\vcpkg\scripts\buildsystems\vcpkg.cmake"
-- Building for: Visual Studio 16 2019
-- The C compiler identification is MSVC 19.23.28106.4
-- The CXX compiler identification is MSVC 19.23.28106.4
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found ZLIB: optimized;D:/vcpkg/installed/x64-windows/lib/zlib.lib;debug;D:/vcpkg/installed/x64-windows/debug/lib/zlibd.lib (found version "1.2.11")
-- Found OpenSSL: D:/vcpkg/installed/x64-windows/debug/lib/libeay32.lib (found version "1.0.2s")
CMake Error at D:/vcpkg/scripts/buildsystems/vcpkg.cmake:263 (_find_package):
  Found package configuration file:

    D:/vcpkg/installed/x64-windows/share/poco/PocoConfig.cmake

  but it set Poco_FOUND to FALSE so package "Poco" is considered to be NOT
  FOUND.  Reason given by package:

  The Poco package requires at least one component

Call Stack (most recent call first):
  CMakeLists.txt:31 (find_package)


-- Configuring incomplete, errors occurred!
See also "D:/visual studio 2015/Projects/CMakeWindowsCppRestSdk/cmmm/CMakeFiles/CMakeOutput.log".

D:\visual studio 2015\Projects\CMakeWindowsCppRestSdk\cmmm>subl D:/vcpkg/installed/x64-windows/share/poco/PocoConfig.cmake

```




-A x64
设置64bit架构
默认是32bit

https://blog.csdn.net/linuxheik/article/details/74626996

CMakeWindowsCppRestSdk项目

cpprestsdk没例子
cpp-netlib
Poco
这两个报错


```
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)
# 项目信息
project (Demo3)
# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
aux_source_directory(. DIR_SRCS)
# 添加头文件路径
include_directories("${PROJECT_SOURCE_DIR}/math")
# 添加 math 子目录
add_subdirectory(math)
# 指定生成目标
add_executable(Demo main.c)
# 添加链接库
target_link_libraries(Demo MathFunctions)

```


```

add_library(archive archive.cpp zip.cpp lzma.cpp)
add_executable(zipapp zipapp.cpp)
target_link_libraries(zipapp archive)

```

- SHARED
- STATIC
- MODULE
- OBJECT


https://www.kancloud.cn/itfanr/cmake-practice/82989

1，CMAKE_BINARY_DIR PROJECT_BINARY_DIR _BINARY_DIR

这三个变量指代的内容是一致的，如果是in source 编译，指得就是工程顶层目录，如果是out-of-source 编译，指的是工程编译发生的目录。PROJECT_BINARY_DIR 跟其他指令稍有区别，现在，你可以理解为他们是一致的。


cmake-build-debug

vs支持cmake

参考mysql项目源码，同一个cmake项目，可以有多个可执行文件

CmakeList.txt也可以有多个

多module

add_subdirectory

[CMake多模块的构建方式](http://www.leadroyal.cn/?p=781)

需要看文档和实践

module

maven pom.xml也可以有多个

https://docs.microsoft.com//cpp/build/cmake-projects-in-visual-studio?view=vs-2019



多看官方文档



生成makefile文件的

跨平台



Clion支持

`include(TestBigEndian)`
TestBigEndian.cmake

[find_package与CMake如何查找链接库详解](https://blog.csdn.net/bytxl/article/details/50637277)

cmake有哪些内置的模块?

https://github.com/Kitware/CMake/tree/master/Modules

FindZLIB.cmake
Findosg.cmake
TestBigEndian.cmake
CheckIncludeFile.cmake
CheckLibraryExists.cmake

`check_library_exists`

[c++ - 使用CMAKE，如何使用CHECK_LIBRARY_EXISTS检查C++库](https://www.ojit.com/article/1713263)





cmake target_link_libraries private public



add_library STATIC SHARED



cmake添加变量

```
cmake -DOPENSSL_ROOT_DIR=/usr/include/openssl -DOPENSSL_LIBRARIES=/usr/local/ssl/lib
```



## 

[cmake 安装和测试](https://www.hahack.com/codes/cmake/)



定制安装规则
首先先在 math/CMakeLists.txt 文件里添加下面两行：


###### 指定 MathFunctions 库的安装路径
install (TARGETS MathFunctions DESTINATION bin)
install (FILES MathFunctions.h DESTINATION include)
指明 MathFunctions 库的安装路径。之后同样修改根目录的 CMakeLists 文件，在末尾添加下面几行：

###### 指定安装路径
install (TARGETS Demo DESTINATION bin)
install (FILES "${PROJECT_BINARY_DIR}/config.h"
         DESTINATION include)
通过上面的定制，生成的 Demo 文件和 MathFunctions 函数库 libMathFunctions.o 文件将会被复制到 /usr/local/bin 中，而 MathFunctions.h 和生成的 config.h 文件则会被复制到 /usr/local/include 中。我们可以验证一下（顺带一提的是，这里的 /usr/local/ 是默认安装到的根目录，可以通过修改 CMAKE_INSTALL_PREFIX 变量的值来指定这些文件应该拷贝到哪个根目录）：


[ehome@xman Demo5]$ sudo make install
[ 50%] Built target MathFunctions
[100%] Built target Demo
Install the project...
-- Install configuration: ""
-- Installing: /usr/local/bin/Demo
-- Installing: /usr/local/include/config.h
-- Installing: /usr/local/bin/libMathFunctions.a
-- Up-to-date: /usr/local/include/MathFunctions.h
[ehome@xman Demo5]$ ls /usr/local/bin
Demo  libMathFunctions.a
[ehome@xman Demo5]$ ls /usr/local/include
config.h  MathFunctions.h
为工程添加测试
添加测试同样很简单。CMake 提供了一个称为 CTest 的测试工具。我们要做的只是在项目根目录的 CMakeLists 文件中调用一系列的 add_test 命令。


###### 启用测试
enable_testing()

###### 测试程序是否成功运行
add_test (test_run Demo 5 2)

###### 测试帮助信息是否可以正常提示
add_test (test_usage Demo)
set_tests_properties (test_usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage: .* base exponent")

###### 测试 5 的平方
add_test (test_5_2 Demo 5 2)

set_tests_properties (test_5_2
 PROPERTIES PASS_REGULAR_EXPRESSION "is 25")

###### 测试 10 的 5 次方
add_test (test_10_5 Demo 10 5)

set_tests_properties (test_10_5
 PROPERTIES PASS_REGULAR_EXPRESSION "is 100000")

###### 测试 2 的 10 次方
add_test (test_2_10 Demo 2 10)

set_tests_properties (test_2_10
 PROPERTIES PASS_REGULAR_EXPRESSION "is 1024")
上面的代码包含了四个测试。第一个测试 test_run 用来测试程序是否成功运行并返回 0 值。剩下的三个测试分别用来测试 5 的 平方、10 的 5 次方、2 的 10 次方是否都能得到正确的结果。其中 PASS_REGULAR_EXPRESSION 用来测试输出是否包含后面跟着的字符串。

让我们看看测试的结果：


[ehome@xman Demo5]$ make test
Running tests...
Test project /home/ehome/Documents/programming/C/power/Demo5
    Start 1: test_run
1/4 Test #1: test_run .........................   Passed    0.00 sec
    Start 2: test_5_2
2/4 Test #2: test_5_2 .........................   Passed    0.00 sec
    Start 3: test_10_5
3/4 Test #3: test_10_5 ........................   Passed    0.00 sec
    Start 4: test_2_10
4/4 Test #4: test_2_10 ........................   Passed    0.00 sec

100% tests passed, 0 tests failed out of 4

Total Test time (real) =   0.01 sec
如果要测试更多的输入数据，像上面那样一个个写测试用例未免太繁琐。这时可以通过编写宏来实现：

###### 定义一个宏，用来简化测试工作
macro (do_test arg1 arg2 result)
  add_test (test_${arg1}_${arg2} Demo ${arg1} ${arg2})
  set_tests_properties (test_${arg1}_${arg2}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result})
endmacro (do_test)

使用该宏进行一系列的数据测试
do_test (5 2 "is 25")
do_test (10 5 "is 100000")
do_test (2 10 "is 1024")
关于 CTest 的更详细的用法可以通过 man 1 ctest 参考 CTest 的文档。

支持 gdb
让 CMake 支持 gdb 的设置也很容易，只需要指定 Debug 模式下开启 -g 选项：

set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
之后可以直接对生成的程序使用 gdb 来调试。

