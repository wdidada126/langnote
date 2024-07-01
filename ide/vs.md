# visual studio


```shell
cmake -B build_64 -S . -G "Visual Studio 17 2022" -A x64 -DCMAKE_TOOLCHAIN_FILE="D:\git\github\vcpkg\scripts\buildsystems\vcpkg.cmake"
cmake -B build_32 -S . -G "Visual Studio 17 2022" -A x32 -DCMAKE_TOOLCHAIN_FILE="D:\git\github\vcpkg\scripts\buildsystems\vcpkg.cmake"
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



vs如何查看c#源代码

msvc-160
2019

msvc-170
2022

visual studio 2022 如何查看c#标准库代码
F12
https://docs.microsoft.com/zh-cn/dotnet/standard/library

Vs code团队负责人：Erich Gamma . JUnit作者之一，《设计模式》作者之一， Eclipse 架构师。2011 加入微软，在瑞士苏黎世组建团队开发基于 web 技术的编辑器，也就是后来的 monaco-editor。VSCode 开发团队从 10 来个人开始，早期成员大多有 Eclipse 开发团队的背景。

VS可以连接远程服务器调试，还要啥Clion啊

测试了下，远程服务器新安装库，在本地vs上提示找不到头文件

使用VS编写Linux程序，可以将VS连接到Linux上，却出现了VS IDE中找不到
#include <sys/socket.h>这类系统头文件的情况，可以将Linux中 /usr/include/ 目录 手动拷贝到windows的
C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\VC\Linux\include\usr\ 位置

https://blog.csdn.net/weixin_43327696/article/details/106463764

D:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VC\Linux\include\usr\include


vs配置头文件和库目录
https://blog.csdn.net/y24283648/article/details/109517407


https://blog.csdn.net/weixin_44144762/article/details/127467173

MSVC没有完整支持20年前的C99标准。你看下是否适合吧。MSVC实现的标准C功能有：完整的C94（C89 + 后续宽字符支持）不完整的C99语核（缺复合字面量、非常量长度数组、T[static N]函数参数等）少数C11中标准化的扩展（如匿名struct/union成员）C99标准库包含于C++的C11标准库部分（有少量缺失）与C11标准略有区别的_s系列函数基本上还是不要把MSVC当成用C开发的东西了。如果需要VS的话可以考虑Visual Studio + Clang 。

vla
https://en.wikipedia.org/wiki/Variable-length_array


visual studio linux c++ 开发

个人使用的话，推荐微软Visual Studio 2022社区版，安装时把C++ 跨平台开发相关选项勾上，会自动安装MSVC、Clang和GCC三种编译器，开发Windows应用时使用MSVC，开发Linux/安卓/iOS平台应用时视情况选择Clang或GCC。

测试可用：
Visual Studio 2022 Professional
TD244-P4NB7-YQ6XK-Y8MMM-YWV2J

Visual Studio 2022 Enterprise
VHF9H-NXBBB-638P6-6JHCY-88JWH

clang-tools:可视化C ++中的继承关系的工具

VS2019怎么设置启动项?
在解决方案管理器中，右键点击项目，然后在弹出菜单中选择“设为启动项目”。
