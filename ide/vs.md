# visual studio

cd "C:\Program Files\Microsoft Visual Studio\2022\Enterprise"
PS C:\Program Files\Microsoft Visual Studio\2022\Enterprise> dir


    目录: C:\Program Files\Microsoft Visual Studio\2022\Enterprise


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2025/2/23     11:10                Common7
d-----         2025/2/23     11:14                DIA SDK
d-----         2025/2/23     10:59                dotnet
d-----         2025/2/23     11:11                ImportProjects
d-----         2025/2/23     11:12                JS
d-----         2025/2/23     11:12                Licenses
d-----         2025/2/23     11:01                MSBuild
d-----         2025/2/23     11:14                SDK
d-----         2025/2/23     11:11                Team Tools
d-----         2025/2/23     11:12                TS
d-----         2025/2/23     11:10                VB
d-----         2025/2/23     11:42                VC
d-----         2025/2/23     11:11                VC#
d-----         2025/2/23     11:12                Web
d-----         2025/2/23     11:10                Xml



以下是对这些文件夹作用的简要介绍：
- Common7：通常包含Visual Studio的公共组件和资源，比如一些通用的工具、配置文件、启动相关的文件等，是Visual Studio运行和各种功能实现的基础支持部分。
- DIA SDK：DIA（Debug Interface Access）SDK用于访问调试信息，开发者可以使用它来开发调试工具、分析调试数据等，方便对程序进行调试和故障排查。
- dotnet：与.NET开发相关的文件夹，可能包含.NET运行时、开发工具、库等资源，用于支持.NET应用程序的开发和运行，比如创建.NET框架或.NET Core的项目等。
- ImportProjects：用于存放项目导入相关的文件和配置等内容，可能涉及到从其他格式或平台导入项目时所需的工具和资源，方便将不同类型的项目导入到Visual Studio中进行开发。
- JS：主要用于支持JavaScript开发，可能包含JavaScript语言服务、代码分析工具、调试支持以及相关的项目模板等资源，帮助开发者进行JavaScript相关的项目开发和调试。
- Licenses：存放Visual Studio软件许可证相关的文件和信息，用于验证和管理软件的使用授权，确保软件的合法使用。
- MSBuild：MSBuild是微软的生成系统，这个文件夹包含了MSBuild的相关工具、任务、目标和配置文件等，用于构建、编译和部署各种类型的Visual Studio项目。
- SDK：包含各种软件开发工具包，可能有不同平台、不同技术的SDK，为开发者提供开发特定类型应用所需的库、头文件、工具等资源。
- Team Tools：与团队协作开发相关的工具和资源所在的文件夹，比如可能包含用于版本控制、团队项目管理、代码审查等功能的工具和插件等。
- TS：与TypeScript开发相关，可能包含TypeScript语言服务、编译器、项目模板等资源，用于支持TypeScript项目的开发和编译。
- VB：用于支持Visual Basic语言的开发，包含Visual Basic的编译器、语言服务、项目模板等资源，方便开发者使用Visual Basic进行应用程序开发。
- VC：与C++开发相关，包含Visual C++的编译器、调试器、库文件、项目模板等大量资源，是进行C++语言开发的重要支持文件夹。
- VC#：主要用于支持C#语言的开发，包含C#的编译器、语言服务、项目模板等资源，是开发C#应用程序的关键部分。
- Web：包含与Web开发相关的工具、模板、库等资源，用于支持各种Web应用程序的开发，如ASP.NET应用、HTML/CSS/JavaScript相关的Web项目等。
- Xml：可能包含与XML处理相关的工具、配置文件、模式定义等资源，用于支持XML文档的编辑、验证、解析等操作，在开发中涉及到XML数据处理时会用到这里的相关资源。


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
