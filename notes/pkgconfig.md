# pkgconfig

## 问题定位  
```
Could NOT find PkgConfig (missing: PKG_CONFIG_EXECUTABLE)
```
**根本原因**：系统里 **没有装 `pkg-config`（或 `pkgconf`）**，`find_package(PkgConfig REQUIRED)` 找不到可执行文件。

---

## 一键解决（CentOS 7 / Rocky 8 / AlmaLinux / Ubuntu / Debian 通用）

```bash
# 1. 安装 pkg-config（CentOS 7 / Rocky 8 / AlmaLinux）
sudo yum install -y pkgconfig        # CentOS 7、Rocky 8、AlmaLinux
# 或者
sudo dnf install -y pkgconf          # Rocky 8/9、AlmaLinux（推荐）

# 2. 验证
pkg-config --version
# 应该输出类似：0.27.1  或  1.8.1
```

> **Ubuntu / Debian**  
> ```bash
> sudo apt update
> sudo apt install -y pkg-config
> ```

---

## 完整编译流程（miniob-2024）

```bash
# 1. 安装必备依赖
sudo yum install -y epel-release
sudo yum install -y pkgconfig gtest-devel libevent-devel \
                    gcc gcc-c++ make cmake3 git

# 2. （可选）解决 clang-format 警告
sudo yum install -y llvm-toolset-7-clang
echo "source /opt/rh/llvm-toolset-7/enable" >> ~/.bashrc
source ~/.bashrc

# 3. 重新配置项目
cd /home/wdidada/miniob-2024
rm -rf build && mkdir build && cd build

# 关键：让 CMake 能找到系统包
cmake3 .. -DCMAKE_PREFIX_PATH=/usr
make -j$(nproc)
```

---

## 验证 `pkg-config` 已可用

```bash
$ which pkg-config
/usr/bin/pkg-config

$ pkg-config --modversion gtest
1.8.1

$ pkg-config --libs gtest
-lgtest -lpthread
```

---

## 常见坑 & 快速排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `pkg-config: command not found` | 没装 `pkgconfig` | `yum install pkgconfig` |
| `pkg-config` 找不到 `gtest.pc` | 没装 `gtest-devel` | `yum install gtest-devel` |
| `PKG_CONFIG_EXECUTABLE` 仍为空 | CMake 缓存旧 | 删除 `build` 目录重新 `cmake` |
| `libevent` 仍报错 | 同理 | `yum install libevent-devel` |

---

## 最终 `CMakeLists.txt` 片段（推荐写法）

```cmake
cmake_minimum_required(VERSION 3.10)
project(miniob)

# ---------- 1. PkgConfig ----------
find_package(PkgConfig REQUIRED)

# ---------- 2. libevent ----------
pkg_check_modules(LIBEVENT REQUIRED libevent)
add_library(Libevent::Libevent UNKNOWN IMPORTED)
set_target_properties(Libevent::Libevent PROPERTIES
    IMPORTED_LOCATION             "${LIBEVENT_LDFLAGS}"
    INTERFACE_INCLUDE_DIRECTORIES "${LIBEVENT_INCLUDE_DIRS}"
    INTERFACE_COMPILE_OPTIONS     "${LIBEVENT_CFLAGS_OTHER}"
)

# ---------- 3. GTest ----------
pkg_check_modules(GTEST REQUIRED gtest)
add_library(GTest::gtest UNKNOWN IMPORTED)
set_target_properties(GTest::gtest PROPERTIES
    IMPORTED_LOCATION             "${GTEST_LDFLAGS}"
    INTERFACE_INCLUDE_DIRECTORIES "${GTEST_INCLUDE_DIRS}"
    INTERFACE_COMPILE_OPTIONS     "${GTEST_CFLAGS_OTHER}"
)

add_library(GTest::Main UNKNOWN IMPORTED)
set_target_properties(GTest::Main PROPERTIES
    IMPORTED_LOCATION             "${GTEST_LDFLAGS}"
    INTERFACE_LINK_LIBRARIES      "GTest::gtest"
)

# ---------- 4. 你的目标 ----------
add_executable(vacuous_trx_test
    ../src/observer/storage/trx/vacuous_trx.cpp
    vacuous_trx_test.cpp
)
target_link_libraries(vacuous_trx_test
    Libevent::Libevent
    GTest::gtest
    GTest::Main
    pthread
)

enable_testing()
include(GoogleTest)
gtest_discover_tests(vacuous_trx_test)
```

---

**搞定！**  
现在 `pkg-config` 已安装，`libevent`、`gtest` 都能通过 `pkg_check_modules` 找到，`cmake` 再也不会报 `PKG_CONFIG_EXECUTABLE` 错误。

> **下一步**：`make && ctest` 跑单元测试，或 `./observer` 启动数据库。

需要我写一个 `vacuous_trx_test.cpp` 示例？直接说！

这是一个非常棒的问题，它触及了 C/C++ 生态中几个核心工具的关系。我们来逐一拆解。

核心答案

pkg-config 并不是 Linux Only 的工具，但它确实在类 Unix 系统（如 Linux, macOS, *BSD）上最为流行和普及。理论上，它也可以在 Windows 上使用，但通常需要配合 MSYS2、Cygwin 或 vcpkg 等环境，并且远不如在 Linux 上那么常见。

一、pkg-config 解决了哪些问题？

pkg-config 的核心使命是解决 C/C++ 库的依赖管理和编译参数传递 的难题。

想象一下没有 pkg-config 的场景：

假设你的程序需要链接一个第三方库，比如 libcurl。在编译时，你需要告诉编译器：
1.  头文件路径在哪里？ (-I 选项)
2.  库文件在哪里？ (-L 选项)
3.  具体要链接哪个库？ (-l 选项)

你的编译命令可能会长得像这样：
gcc -o my_program my_program.c -I/usr/local/include -L/usr/local/lib -lcurl -lssl -lcrypto -lz


这带来了几个问题：
•   命令冗长易错：你必须手动写出所有复杂的路径和依赖。

•   版本和路径不统一：不同系统、不同包管理器安装的库，路径可能不同（/usr/lib, /usr/local/lib, /opt/homebrew/lib）。

•   传递性依赖：libcurl 本身可能依赖 libssl, libcrypto, libz。你必须手动找出并填写所有这些依赖库，非常麻烦。

•   交叉编译困难：为其他平台编译时，路径完全不同。

pkg-config 的解决方案：

pkg-config 为每个已安装的库维护一个后缀名为 .pc 的元数据文件。这个文件里明确定义了该库的编译和链接参数。

例如，libcurl 的 curl.pc 文件内容可能如下：
prefix=/usr/local
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: libcurl
Description: Library for transferring data with URLs
Version: 7.68.0
Libs: -L${libdir} -lcurl -lssl -lcrypto -lz
Cflags: -I${includedir}


现在，你只需要使用 pkg-config 来生成这些参数：
gcc -o my_program my_program.c `pkg-config --cflags --libs curl`


pkg-config 的优势：
1.  简化命令：一行命令替代一长串参数。
2.  自动化依赖解析：自动处理传递性依赖。如果你 libA 依赖 libB，那么查询 libA 时，libB 的参数也会自动包含进来。
3.  路径透明：无论库安装在哪里，pkg-config 都能通过 .pc 文件找到正确的路径。
4.  版本管理：可以查询库的版本，便于条件编译。

二、pkg-config 与 Make, CMake, xmake 的关系

这几个工具扮演着不同的角色，它们的关系是 协作 而非 竞争。下图清晰地展示了它们在现代C/C++项目构建中的层级关系：
flowchart TD
    A[“项目构建系统<br>（Make / CMake / xmake）”] --> B[“调用 pkg-config”]
    B --> C[“读取 .pc 文件”]
    C --> D[“返回编译链接参数<br>（--cflags, --libs）”]
    D --> E[“构建系统使用这些参数<br>调用编译器(gcc/clang)”]


角色分析

工具 角色定位 与 pkg-config 的关系

pkg-config 库信息查询工具 它是信息的提供者。它本身不编译代码，只负责回答“如何编译和链接某个库？”这个问题。

Make 老牌构建工具 Make 规则中的 gcc 命令需要复杂的参数。这时，可以在 Makefile 的规则中使用  `pkg-config ...`  来动态获取参数。Make 是 pkg-config 的调用者。

CMake 跨平台构建系统生成器 CMake 有自己强大的查找包模块。它内部封装了类似 pkg-config 的功能（如 find_package）。但为了兼容性，它也提供了 FindPkgConfig 模块，允许你直接在 CMakeLists.txt 中调用 pkg-config 来获取库信息。

xmake 现代跨平台构建工具 xmake 的设计更加一体化。它内置了包管理功能，可以自动处理依赖。但它同样支持与 pkg-config 集成，你可以使用 add_requires("pkg-config::curl") 这样的语法来直接利用系统上通过 pkg-config 管理的库。

举例说明

1. 在 Makefile 中：
# 使用 pkg-config 获取编译和链接标志
CFLAGS += `pkg-config --cflags glib-2.0`
LIBS += `pkg-config --libs glib-2.0`

my_program: my_program.c
    $(CC) -o $@ $< $(CFLAGS) $(LIBS)

2. 在 CMakeLists.txt 中：
# 查找 pkg-config 工具
find_package(PkgConfig REQUIRED)

# 使用 pkg-config 查找 glib-2.0
pkg_check_modules(GLIB2 REQUIRED glib-2.0)

# 将 flags 添加到目标
include_directories(${GLIB2_INCLUDE_DIRS})
target_link_libraries(my_program ${GLIB2_LIBRARIES})


3. 在 xmake.lua 中：
-- 直接使用系统的 pkg-config 信息
add_requires("pkg-config::glib-2.0")

target("my_program")
    add_packages("pkg-config::glib-2.0")


总结

•   pkg-config：是一个专注于解决库依赖信息查询的辅助工具。它本质上是库（如 OpenGL, GTK, libcurl）和构建系统（如 Make, CMake）之间的翻译官。

•   Make / CMake / xmake：是构建系统，负责管理整个项目的编译、链接规则和文件依赖关系。它们是项目的总指挥。

•   关系：构建系统（总指挥）在需要知道如何链接一个库时，会去调用 pkg-config（翻译官）获取指令，然后将这些指令传递给编译器（工人）去执行。

因此，pkg-config 是 Unix/Linux 下 C/C++ 开发生态中一个不可或缺的、承上启下的关键组件。

这是一个非常深入的问题，触及了现代构建系统的核心工作流程。Make 和 Ninja 本身并不知道 pkg-config 是什么，它们只是“构建引擎”。调用 pkg-config 的实际上是构建系统的配置文件生成器（如 autotools、CMake、Meson）或在 Makefile 中直接编写的规则。

简单来说，流程是这样的：
构建系统生成器（如CMake） -> 生成构建脚本（Makefile或Ninja文件） -> 构建引擎（Make或Ninja）执行脚本

下图清晰地展示了这一完整的工作流程：
flowchart TD
    A[“开发者编写构建配置<br>（如 CMakeLists.txt）”] --> B

    subgraph B [配置阶段]
        B1[“构建系统生成器<br>（如 CMake, Meson）”]
        B1 --> B2[“调用 pkg-config<br>查询依赖库参数”]
        B2 --> B3[“生成构建脚本<br>（Makefile 或 .ninja 文件）”]
    end

    B3 --> C[“构建脚本中包含<br>由 pkg-config 生成的<br>完整编译链接命令”]

    C --> D{构建引擎执行}
    D --> E1[“Make<br>读取 Makefile”]
    D --> E2[“Ninja<br>读取 .ninja 文件”]

    E1 --> F[“调用编译器<br>（gcc/clang）”]
    E2 --> F


下面我们分情况详细说明。

情况一：Make 如何调用 pkg-config？

Make 通过直接在 Makefile 中使用 反引号 或 $(shell ...) 函数来执行 pkg-config 命令，并将其返回的字符串作为变量使用。

示例1：直接在规则中使用

# 一个非常简单的 Makefile
my_program: main.c
    gcc -o my_program main.c `pkg-config --cflags --libs gtk+-3.0`

在这个例子中，当 Make 执行这条规则时，它会先运行反引号内的命令 pkg-config --cflags --libs gtk+-3.0，然后用这个命令的输出结果（例如 -pthread -I/usr/include/gtk-3.0 ... -lgtk-3.0）替换掉整个反引号部分，最后再执行完整的 gcc 命令。

示例2：使用变量（更规范的做法）

# 定义变量，保存 pkg-config 的输出
CFLAGS = `pkg-config --cflags gtk+-3.0`
LIBS = `pkg-config --libs gtk+-3.0`

my_program: main.c
    gcc -o my_program main.c $(CFLAGS) $(LIBS)

或者使用 $(shell ...) 函数，这在 GNU Make 中更通用：
CFLAGS = $(shell pkg-config --cflags gtk+-3.0)
LIBS = $(shell pkg-config --libs gtk+-3.0)

my_program: main.c
    gcc -o my_program main.c $(CFLAGS) $(LIBS)


关键点：对于 Make 来说，pkg-config 的调用发生在 Makefile 被解析的阶段。也就是说，在你运行 make 命令的瞬间，pkg-config 就已经被执行了，它的输出被填充到 CFLAGS 和 LIBS 变量中。

情况二：Ninja 如何调用 pkg-config？

Ninja 的设计哲学是“追求构建速度”，它本身不包含任何复杂的语法（如条件判断、shell 命令）。因此，你几乎永远不会在 .ninja 构建文件中看到直接调用 pkg-config 的指令。

那么 Ninja 是如何获得 pkg-config 提供的信息的呢？

答案是：通过更高级的构建系统生成器，如 CMake、Meson、Autotools。

这些生成器的工作流程是：
1.  配置阶段：当你运行 cmake /path/to/source 或 meson setup builddir 时，生成器会启动。
2.  调用 pkg-config：在配置阶段，CMake/Meson 会读取项目配置文件（如 CMakeLists.txt），并根据配置执行 pkg-config 命令来探测系统上是否存在所需的库，并获取其编译标志。
3.  生成构建文件：CMake/Meson 将获取到的所有信息（包括从 pkg-config 得到的完整路径和链接参数）直接硬编码到生成的 build.ninja（或 Makefile）文件中。

示例：从 CMakeLists.txt 到 build.ninja

假设有一个 CMakeLists.txt 文件：
cmake_minimum_required(VERSION 3.10)
project(MyProject)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK3 REQUIRED gtk+-3.0)

add_executable(my_program main.c)
target_link_libraries(my_program ${GTK3_LIBRARIES})
target_include_directories(my_program PRIVATE ${GTK3_INCLUDE_DIRS})
target_compile_options(my_program PRIVATE ${GTK3_CFLAGS_OTHER})


当你使用 -G Ninja 选项运行 CMake 时：
mkdir build && cd build
cmake -G Ninja .. # 配置阶段

在配置阶段，CMake 会调用 pkg-config，然后生成一个 build.ninja 文件。在这个文件中，你会看到类似这样的内容（已简化）：
# build.ninja (由 CMake 生成)
rule C_COMPILER
  command = gcc $CFLAGS $INCLUDES $FLAGS -o $out -c $in

rule LINK_EXECUTABLE
  command = gcc $LINK_FLAGS $in -o $out $LIBRARIES

# pkg-config 的结果被直接硬编码在这里！
build main.c.o: C_COMPILER ../main.c
  INCLUDES = -I/usr/include/gtk-3.0 -I/usr/include/pango-1.0 ... # 来自 pkg-config --cflags
  FLAGS = -pthread # 来自 pkg-config --cflags

build my_program: LINK_EXECUTABLE main.c.o
  LIBRARIES = -lgtk-3.0 -lgdk-3.0 -lpangocairo-1.0 ... # 来自 pkg-config --libs

然后，当你运行 ninja 命令时，它只是简单地执行 build.ninja 文件中已经写死的命令，不会再调用 pkg-config。

总结对比

特性 Make Ninja

调用方式 在 Makefile 中直接使用  `pkg-config ...`  或 $(shell pkg-config ...) 不直接调用，由高级生成器（CMake, Meson）在配置阶段调用。

调用时机 构建时（每次运行 make 时都会解析并执行）。 配置时（仅在运行 cmake/meson 时调用一次，结果被硬编码）。

灵活性 高，可以方便地在 Makefile 中编写逻辑。 低，Ninja 文件是静态的，但生成它的工具（CMake）非常灵活。

构建速度 相对较慢，因为每次都可能要调用外部命令并重新解析。 极快，因为所有依赖和命令都是预先计算好并写死的，没有冗余计算。

因此，Ninja 的高性能部分正是源于它将 pkg-config 这类“配置工作”提前到了生成阶段，构建阶段只做最纯粹的编译和链接操作。
