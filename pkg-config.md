# pkg-config

pkg-config --cflags --libs log4cpp
-pthread -I/usr/local/include -L/usr/local/lib -llog4cpp

cmake CMakeLists.txt
maven pom.xml
pkg-config .pc

sudo apt-get install pkg-config

什么是pkg-config
pkg-config是一个linux下的命令，用于获得某一个库/模块的所有编译相关的信息。

例子：

pkg-config opencv –libs –cflags

结果：

-I/usr/include/opencv

/usr/lib/x86_64-linux-gnu/libopencv_calib3d.so

https://www.cnblogs.com/rainsoul/p/10567390.html

pkg-config --cflags --libs libcurl
-I/usr/include/x86_64-linux-gnu -lcurl


file $(which pkg-config)
/usr/bin/pkg-config: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=157ae1758c8097d68ff7c6a1e7bc3b6e2317cc74, for GNU/Linux 3.2.0, stripped

pkg-config 是一个在类 Unix 系统中广泛使用的工具，主要用于在编译和链接程序时获取库的相关信息，比如库的编译参数（如 CFLAGS）和链接参数（如 LDFLAGS）。借助 pkg-config，开发者可以更方便地管理和使用系统中的各种库，避免手动指定库的路径和版本等信息。


在软件开发中，尤其是在构建和配置项目时，`.cmake` 文件和 `.pc` 文件都起着重要作用，但它们的用途、语法和应用场景有所不同，下面详细介绍二者的区别。

### 1. 文件用途
#### `.cmake` 文件
- `.cmake` 文件是 CMake 构建系统使用的脚本文件。CMake 是一个跨平台的开源构建工具，它通过 `.cmake` 文件来描述项目的构建过程，包括源文件、头文件的位置，编译选项，链接选项，依赖库的查找和使用等。
- 可以使用 `.cmake` 文件生成不同平台和编译器下的构建文件，如 Unix Makefiles、Visual Studio 项目文件等，从而实现项目的跨平台构建。

#### `.pc` 文件
- `.pc` 文件是 `pkg-config` 工具使用的配置文件，`pkg-config` 是一个在类 Unix 系统中广泛使用的工具，用于在编译和链接程序时获取库的相关信息。
- `.pc` 文件中记录了某个库的元数据，如库的名称、版本、编译参数（`CFLAGS`）、链接参数（`LDFLAGS`）等，帮助开发者方便地找到并使用系统中的库。

### 2. 文件语法
#### `.cmake` 文件
- `.cmake` 文件使用 CMake 特定的语法，由一系列的命令和变量组成。例如：
```cmake
# 设置项目名称和版本
project(MyProject VERSION 1.0)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 添加可执行文件
add_executable(MyExecutable main.cpp)

# 查找并链接依赖库
find_package(SomeLibrary REQUIRED)
target_link_libraries(MyExecutable PRIVATE SomeLibrary::SomeLibrary)
```
- 上述代码中，`project`、`set`、`add_executable`、`find_package` 和 `target_link_libraries` 都是 CMake 命令，用于定义项目、设置编译选项、添加可执行文件、查找依赖库和链接库等操作。

#### `.pc` 文件
- `.pc` 文件使用简单的键值对语法，每个键值对占一行，格式为 `键名: 值`。例如：
```plaintext
prefix=/usr/local
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: SomeLibrary
Description: A sample library
Version: 1.0
Cflags: -I${includedir}
Libs: -L${libdir} -lsomelibrary
```
- 上述代码中，`prefix`、`exec_prefix`、`libdir` 和 `includedir` 定义了库的安装路径，`Name`、`Description` 和 `Version` 是库的基本信息，`Cflags` 和 `Libs` 分别指定了编译和链接时需要的参数。

### 3. 应用场景
#### `.cmake` 文件
- 适用于大型、复杂的项目，尤其是需要跨平台构建的项目。CMake 可以根据 `.cmake` 文件生成不同平台和编译器下的构建文件，方便开发者在不同环境中进行项目的编译和构建。
- 可以集成各种依赖管理工具，如 `FetchContent`、`ExternalProject` 等，方便管理项目的外部依赖。

#### `.pc` 文件
- 主要用于类 Unix 系统中，帮助开发者在编译和链接程序时找到并使用系统中的库。通过 `pkg-config` 工具，可以轻松获取库的编译和链接参数，避免手动指定这些参数带来的麻烦。
- 对于使用传统 Makefile 构建的项目，`.pc` 文件可以很好地与 `pkg-config` 配合，简化项目的构建过程。

### 4. 相互协作
在实际项目中，`.cmake` 文件和 `.pc` 文件可以相互协作。例如，在 CMake 项目中，可以使用 `find_package` 命令结合 `pkg-config` 来查找和使用系统中的库。示例如下：
```cmake
find_package(PkgConfig REQUIRED)
pkg_check_modules(SomeLibrary REQUIRED somelibrary)

add_executable(MyExecutable main.cpp)
target_include_directories(MyExecutable PRIVATE ${SomeLibrary_INCLUDE_DIRS})
target_link_libraries(MyExecutable PRIVATE ${SomeLibrary_LIBRARIES})
```
上述代码中，`find_package(PkgConfig REQUIRED)` 用于查找并启用 `pkg-config`，`pkg_check_modules` 用于通过 `pkg-config` 查找 `somelibrary` 库，并获取其编译和链接参数，然后将这些参数应用到项目中。

综上所述，`.cmake` 文件和 `.pc` 文件在项目构建和配置中各有其独特的用途和优势，开发者可以根据项目的具体需求选择合适的工具和文件。 


`find_package` 和 `pkg_check_modules` 都是在 CMake 构建系统中使用的函数，但它们的来源和用途有所不同。下面为你详细介绍：

### 1. `find_package` 函数
- 函数性质：`find_package` 是 CMake 内置的核心函数，用于查找和加载外部依赖包。它在 CMake 脚本中被广泛使用，目的是帮助开发者在项目里集成第三方库或工具。
- 工作原理：`find_package` 函数会依据指定的包名，在一系列预定义的路径下搜索相应的 CMake 配置文件。这些配置文件的命名通常遵循 `<PackageName>Config.cmake` 或者 `<packagename>-config.cmake` 的格式，也可能是 `<PackageName>Targets.cmake`。当找到合适的配置文件后，CMake 会加载该文件，进而获取依赖包的相关信息，例如包含目录、库文件路径、编译选项等。
- 示例代码：
```cmake
find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
    include_directories(${OpenCV_INCLUDE_DIRS})
    target_link_libraries(YourProject ${OpenCV_LIBS})
endif()
```
在上述示例中，`find_package(OpenCV REQUIRED)` 用于查找 OpenCV 库，若找到则获取其包含目录和库文件信息，并将其应用到项目中。

### 2. `pkg_check_modules` 函数
- 函数性质：`pkg_check_modules` 并非 CMake 的内置函数，它是由 `FindPkgConfig.cmake` 模块提供的。当你调用 `find_package(PkgConfig REQUIRED)` 时，CMake 会加载 `FindPkgConfig.cmake` 模块，从而引入 `pkg_check_modules` 函数。该函数主要用于借助 `pkg-config` 工具来查找和使用系统中的库。
- 工作原理：`pkg_check_modules` 函数会调用 `pkg-config` 工具，依据指定的库名查找对应的 `.pc` 文件，进而获取库的元数据，如编译参数（`CFLAGS`）、链接参数（`LDFLAGS`）等。
- 示例代码：
```cmake
find_package(PkgConfig REQUIRED)
pkg_check_modules(SomeLibrary REQUIRED somelibrary)
if(SomeLibrary_FOUND)
    include_directories(${SomeLibrary_INCLUDE_DIRS})
    target_link_libraries(YourProject ${SomeLibrary_LIBRARIES})
endif()
```
在这个示例中，`find_package(PkgConfig REQUIRED)` 加载 `FindPkgConfig.cmake` 模块，`pkg_check_modules(SomeLibrary REQUIRED somelibrary)` 通过 `pkg-config` 查找 `somelibrary` 库的信息，若找到则将其包含目录和库文件信息应用到项目中。

综上所述，`find_package` 是 CMake 内置函数，而 `pkg_check_modules` 是由 `FindPkgConfig.cmake` 模块提供的函数，二者都用于在 CMake 项目中查找和使用外部依赖。 


cmake安装之后有FindPkgConfig.cmake文件



wdidada@LAPTOP-wdidada:~$ which cmake
/home/wdidada/cmake-3.30.1-linux-x86_64/bin/cmake
wdidada@LAPTOP-wdidada:~$ cd ~/cmake-3.30.1-linux-x86_64/
wdidada@LAPTOP-wdidada:~/cmake-3.30.1-linux-x86_64$ find . -name "FindPkgConfig.cmake"
./share/cmake-3.30/Modules/FindPkgConfig.cmake

