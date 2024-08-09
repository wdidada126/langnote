# zip

git clone https://github.com/rbock/sqlpp11.git
cd sqlpp11
git checkout 46cffc8398a3a484db3c28573214407825b34a6d
cmake -S . -B build
cmake --build build

CMake 内置变量 `PROJECT_SOURCE_DIR` 和 `CMAKE_SOURCE_DIR` 在 CMake 构建系统中具有不同的作用。它们分别代表着不同的含义：

- `PROJECT_SOURCE_DIR`：这个变量存储了当前项目的顶层源目录的路径。在 CMakeLists.txt 文件中，通常通过这个变量来引用项目的根源代码目录。这对于指定源文件的路径、包含其他 CMake 文件或者设置输出路径等非常有用。

- `CMAKE_SOURCE_DIR`：这个变量存储了执行 cmake 命令时指定的源代码根目录的路径。这个变量通常用于指定 CMakeLists.txt 文件所在的目录。与 `PROJECT_SOURCE_DIR` 不同，`CMAKE_SOURCE_DIR` 可能与项目的源代码目录不同，因为它是在执行 cmake 命令时指定的。

在 CMakeLists.txt 文件中，你可以像下面这样使用这些变量：

```cmake
message(STATUS "Project Source Dir: ${PROJECT_SOURCE_DIR}")
message(STATUS "CMake Source Dir: ${CMAKE_SOURCE_DIR}")
```

这将输出 `PROJECT_SOURCE_DIR` 和 `CMAKE_SOURCE_DIR` 的值，以便你可以查看它们指向的具体目录路径。这些变量对于在 CMake 构建系统中管理项目结构和路径非常有用。