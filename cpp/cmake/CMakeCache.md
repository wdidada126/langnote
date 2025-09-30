# CMakeCache

缓存变量：全局有效，存储在 CMakeCache.txt 文件中，跨 CMake 运行持久化。
CMake 在首次配置项目时，会在构建目录的根目录下生成 CMakeCache.txt 文件。这个文件本质上是一个持久化的配置文件，用于存储各种变量及其值，确保在多次运行 CMake 时这些信息得以保留，从而避免重复检测和计算，提高配置效率。

下面是一个 CMakeCache.txt 文件可能包含的主要内容，为了让你能快速了解，我先把它们整理在表格里：

类别 示例变量名 作用说明
CMake自身信息与配置 CMAKE_VERSION CMake 的版本号。
CMAKE_GENERATOR 使用的生成器（如 "Unix Makefiles", "Visual Studio 17 2022"）。
CMAKE_BUILD_TYPE 构建类型（如 Debug, Release）。
项目信息 PROJECT_NAME 项目的名称。
PROJECT_VERSION 项目的版本号。
安装路径 CMAKE_INSTALL_PREFIX 安装根目录（如 /usr/local）。
编译器与工具链 CMAKE_C_COMPILER C 编译器的完整路径。
CMAKE_CXX_COMPILER C++ 编译器的完整路径。
CMAKE_MAKE_PROGRAM 构建工具路径（如 make 或 ninja）。
系统检测结果 CMAKE_SYSTEM_NAME 目标操作系统的名称（如 Linux, Windows）。
CMAKE_SYSTEM_VERSION 目标操作系统的版本。
项目特定选项 BUILD_SHARED_LIBS 全局控制库的构建类型（ON 为动态库，OFF 为静态库）。
BUILD_TESTING 是否构建测试目标。
MY_PROJECT_USE_FEATURE_X (示例) 项目中通过 option() 命令定义的定制化开关选项。

CMakeCache.txt 的格式
这个文件的内容通常遵循以下格式：
# 这是注释
变量名:类型=值

例如：
//Path to a program.
CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/g++

//Build type (Debug, Release, RelWithDebInfo, MinSizeRel)
CMAKE_BUILD_TYPE:STRING=Debug

//Install path prefix.
CMAKE_INSTALL_PREFIX:PATH=/usr/local

每一条目通常包含：
•   变量名：如 CMAKE_INSTALL_PREFIX。
•   类型：常见的有 STRING、BOOL、PATH、FILEPATH、INTERNAL 等。类型主要用于 GUI 工具（如 cmake-gui）如何展示和编辑该变量。
•   值：变量的实际设置值。
•   描述（可选）：以 // 开头的注释行，说明该变量的用途。

 操作 CMakeCache.txt

•   查看内容：你可以直接在文本编辑器中打开 CMakeCache.txt 文件查看，或在命令行中使用 cmake -L 或 cmake -LAH 命令列出缓存变量（-LAH 会显示所有变量，包括帮助信息）。

•   修改变量：

    ◦   推荐方式：通过命令行参数 -D 重新运行 CMake（例如 cmake -DCMAKE_BUILD_TYPE=Release .），或使用交互式工具 ccmake 或图形化工具 cmake-gui。

    ◦   直接编辑文件：虽然技术上可行，但一般不推荐直接手动编辑 CMakeCache.txt 文件，因为格式错误或不当修改可能导致配置不一致或失败。CMake 在设计上期望通过其提供的界面或命令行参数来管理缓存。

•   重置缓存：如果配置出现问题，或想完全重新开始，最彻底的方法是删除整个构建目录（因为构建目录中可能还有其他基于初始缓存生成的中间文件）。你也可以只删除 CMakeCache.txt 文件，然后重新运行 cmake，这将触发完整的重新检测和配置。

主要特点与注意事项
•   持久化：CMakeCache.txt 中的值会在多次 CMake 运行之间保留，除非你显式删除它们或使用 -U 选项。
•   用户配置与自动检测：该文件同时包含了用户设置的选项（如通过 -D 传递的）和 CMake 自动检测系统得到的信息（如编译器路径、系统特性等）。
•   变量优先级与覆盖：在 CMakeLists.txt 中，如果存在与缓存变量同名的普通变量，普通变量会遮盖（Shadow）缓存变量。这意味着在当前作用域内，${VAR} 会取普通变量的值。要强制访问缓存变量，需使用 $CACHE{VAR} 语法。使用 set(... CACHE ... FORCE) 可以强制覆盖缓存变量的值。
•   跨项目/目录移动警告：由于 CMakeCache.txt 中包含大量绝对路径，它通常不能直接复制到另一个构建目录或另一台机器上使用，否则很可能因路径错误导致问题。

希望这些信息能帮助你更好地理解和使用 CMakeCache.txt。如果你有更多关于 CMake 的问题，我很乐意继续为你解答。