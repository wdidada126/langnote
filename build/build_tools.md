# build_tools

maven是默认
src/main/java下面是java源代码

xmake
xmake.lua
批量添加c源代码文件
批量添加c++源代码文件

cmake
CMakeLists.txt

批量添加src文件夹下面所有cpp cxx cc后缀的文件，如何写？

要在CMake中批量添加`src`文件夹下所有`.cpp`, `.cxx`, `.cc`后缀的文件，您可以使用`file(GLOB ...)`命令来实现。这样可以自动查找并将匹配的文件添加到项目中。

下面是一个示例的`CMakeLists.txt`文件，演示了如何批量添加这些文件：

```cmake
cmake_minimum_required(VERSION 3.0)
project(YourProjectName)

# 添加源文件夹
file(GLOB SOURCES src/*.cpp src/*.cxx src/*.cc)

# 创建可执行文件
add_executable(YourExecutable ${SOURCES})
```

在这个示例中，`file(GLOB SOURCES src/*.cpp src/*.cxx src/*.cc)`会匹配`src`文件夹下所有以`.cpp`, `.cxx`, `.cc`结尾的文件，并将它们存储在`SOURCES`变量中。然后，通过`add_executable`命令将这些源文件添加到可执行文件中。

请注意，使用`file(GLOB ...)`命令来收集源文件有一些限制，例如当项目结构发生变化时可能无法自动检测到新的文件。因此，在实际项目中最好手动列出文件，以确保构建系统的稳定性。

apt/yum/dnf/pkg

