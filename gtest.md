# gtest

## install
conan
vcpkg install gtest

## api
## namespace
testing
### GTest api

- GTEST_API_
- TEST
- EXPECT_EQ


```c
testing::InitGoogleTest(&argc, argv);
```

```c
RUN_ALL_TESTS()
```

### vcpkg安装的库
头文件在vcpkg/installed/x64-linux/include

[wdidada@10-23-29-39 include]$ cd gtest/
[wdidada@10-23-29-39 gtest]$ ls
gtest-death-test.h  gtest-message.h     gtest-printers.h  gtest-test-part.h
gtest.h             gtest-param-test.h  gtest_prod.h      gtest-typed-test.h
gtest-matchers.h    gtest_pred_impl.h   gtest-spi.h       internal
[wdidada@10-23-29-39 gtest]$ pwd


```
The package gtest is compatible with built-in CMake targets:

    enable_testing()

    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)

    add_test(AllTestsInMain main)
```

## 官方doc
https://github.com/google/googletest/blob/main/docs/samples.md
googletest github 仓库

docs文件夹

md文件

支持Linux Mac Windows平台

cmake配置gtest，是另外的可执行文件
类比JUnit，也是另外的main函数

```
The package gtest is compatible with built-in CMake targets:

    enable_testing()

    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)

    add_test(AllTestsInMain main)
```


## link
```
target_link_libraries(example libgtest.a)
```

```
target_link_libraries(example gtest_main)
```

c 单元测试 gtest

https://blog.csdn.net/u014775175/article/details/65643698


你遇到的这个 GoogleTest 1.10.0 编译错误 是 经典的 `-Werror=maybe-uninitialized` 警告被升级为错误，发生在 `gtest-death-test.cc` 中的 `StackGrowsDown()` 函数：

```cpp
int dummy;  // 未初始化
StackLowerThanAddress(&dummy, &result);  // 警告：dummy 未初始化
```

虽然逻辑上 `dummy` 只取地址，不访问值，但 GCC 11+（Ubuntu 22.04 默认） 会触发 `-Wmaybe-uninitialized`，而 GoogleTest 默认开启 `-Werror`，导致 编译失败。



## 终极解决方案（3 种，任选其一）



### 方案 1：【推荐】关闭 `-Werror`（最简单、最安全）

> 不影响测试功能，只关闭“警告变错误”

#### 修改 `googletest/CMakeLists.txt`（或外层 CMake）

在 `add_library(gtest ...)` 之前 移除或覆盖 `-Werror`：

```cmake
# 找到这行（通常在 googletest/CMakeLists.txt）
# string(REPLACE "-Werror" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

# 或者直接加：
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wno-error=maybe-uninitialized)
endif()
```

#### 或者在 外部 CMake 中传入：

```bash
cmake .. -DGTEST_HAS_PTHREAD=0 -DCMAKE_CXX_FLAGS="-Wno-error=maybe-uninitialized"
```



### 方案 2：初始化 `dummy` 变量（精准修复）

> 直接修改 GoogleTest 源码（不推荐长期维护，但可行）

编辑文件：
```
/home/runner/.../googletest/googletest/src/gtest-death-test.cc
```

找到第 1299 行：

```cpp
int dummy;  // 修改为：
int dummy = 0;
```

> 这样 GCC 就不会警告了，逻辑不变。



### 方案 3：【升级 GoogleTest】使用 1.11.0+ 或 1.14.0（推荐）

> 1.10.0 是 2020 年版本，已知在 GCC 11+ 有此问题  
> 1.14.0（2023）已修复此警告

```bash
# 删除旧版本
rm -rf googletest

# 下载 1.14.0
wget https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
tar -xzf v1.14.0.tar.gz
mv googletest-1.14.0 googletest
```

然后正常编译：

```bash
mkdir build && cd build
cmake .. -DGTEST_HAS_PTHREAD=0
make -j$(nproc)
```

## 一键修复脚本（推荐方案 1 + 清理）

```bash
# 进入项目根目录
cd /home/runner/work/github_codespaces_compile/github_codespaces_compile/cpp/googletest/linux/1_10_0

# 清理旧构建
rm -rf build
mkdir build && cd build

# 编译时关闭 -Werror
cmake .. \
    -DGTEST_HAS_PTHREAD=0 \
    -DCMAKE_CXX_FLAGS="-Wno-error=maybe-uninitialized"

make -j$(nproc)
```

## 为什么不能忽略？

| 选项 | 是否有效 |
|||
| `-Wno-maybe-uninitialized` | 无效（因为 `-Werror` 覆盖） |
| `-Werror=maybe-uninitialized` | 更糟 |
| `-Wno-error=maybe-uninitialized` | 正确 |

## 验证成功

```bash
./googletest/googlemock/gtest/samples/sample1_unittest
# 输出： [==========] Running 6 tests...
#         [  PASSED  ] 6 tests.
```



## 总结：你现在应该怎么做？

| 目标 | 命令 |
|||
| 快速通过编译 | `cmake .. -DCMAKE_CXX_FLAGS="-Wno-error=maybe-uninitialized"` |
| 长期稳定 | 升级到 GoogleTest 1.14.0 |
| 不改外部 CMake | 修改 `googletest/CMakeLists.txt` 加 `add_compile_options(-Wno-error=maybe-uninitialized)` |

我推荐你直接运行这个：

```bash
cd build
rm -rf *
cmake .. -DCMAKE_CXX_FLAGS="-Wno-error=maybe-uninitialized"
make -j$(nproc)
```

3 分钟内编译成功！

需要我给你 打好补丁的 GoogleTest 1.10.0 压缩包 或 1.14.0 一键脚本，我立刻发你！


```shell
/usr/local/include/gtest/gtest-printers.h:959:29: error: ‘nullopt_t’ is not a member of ‘std’; did you mean ‘nullptr_t’?
  959 | class UniversalPrinter<std::nullopt_t> {
      | ^~~~~~~~~
      | nullptr_t
/usr/local/include/gtest/gtest-printers.h:959:29: error: ‘nullopt_t’ is not a member of ‘std’; did you mean ‘nullptr_t’?
  959 | class UniversalPrinter<std::nullopt_t> {
      | ^~~~~~~~~
      | nullptr_t
/usr/local/include/gtest/gtest-printers.h:959:38: error: template argument 1 is invalid
  959 | class UniversalPrinter<std::nullopt_t> {
      | ^
/usr/local/include/gtest/gtest-printers.h:966:29: error: ‘variant’ is not a member of ‘std’
  966 | class UniversalPrinter<std::variant<T...>> {
      | ^~~~~~~
/usr/local/include/gtest/gtest-printers.h:966:29: note: ‘std::variant’ is only available from C++17 onwards
/usr/local/include/gtest/gtest-printers.h:966:29: error: ‘variant’ is not a member of ‘std’
/usr/local/include/gtest/gtest-printers.h:966:29: note: ‘std::variant’ is only available from C++17 onwards
/usr/local/include/gtest/gtest-printers.h:966:38: error: expected parameter pack before ‘...’
  966 | class UniversalPrinter<std::variant<T...>> {
      | ^~~
/usr/local/include/gtest/gtest-printers.h:966:38: error: template argument 1 is invalid
/usr/local/include/gtest/gtest-printers.h:966:41: error: expected unqualified-id before ‘>’ token
  966 | class UniversalPrinter<std::variant<T...>> {
      | ^~
In file included from /usr/local/include/gtest/gtest.h:67,
                 from /home/runner/work/miniob_2021_final/miniob_2021_final/unitest/bitmap_test.cpp:17:
/usr/local/include/gtest/gtest-param-test.h:483:56: error: missing template arguments before ‘(’ token
  483 | typename StdFunction = decltype(std::function(std::declval<Func>()))>
      | ^
/usr/local/include/gtest/gtest-param-test.h:493:56: error: missing template arguments before ‘(’ token
  493 | typename StdFunction = decltype(std::function(std::declval<Func>()))>
      | ^
gmake[2]: * [unitest/CMakeFiles/bitmap_test.dir/build.make:79: unitest/CMakeFiles/bitmap_test.dir/bitmap_test.cpp.o] Error 1
gmake[1]: * [CMakeFiles/Makefile2:427: unitest/CMakeFiles/bitmap_test.dir/all] Error 2
gmake: * [Makefile:136: all] Error 2 gtest最新版，ubuntu22，编译miniob报错，
```

你遇到的这个错误 非常典型，是 GoogleTest 版本与 C++ 标准不匹配 导致的：

```
error: ‘nullopt_t’ is not a member of ‘std’
error: ‘variant’ is not a member of ‘std’
note: ‘std::variant’ is only available from C++17 onwards
```



## 根本原因

| 项目 | 说明 |
|||
| 你使用的 GoogleTest | 最新版（1.14.0+），从 1.12.0 开始 默认要求 C++17 |
| MiniOB 项目 | 默认 C++11（CMakeLists.txt 中未设置 `cxx_standard 17`） |
| Ubuntu 22.04 默认 g++ | 支持 C++17，但 必须手动开启 |

> GoogleTest 1.14.0+ 必须用 `-std=c++17` 编译，否则 `std::nullopt_t`、`std::variant` 无法识别！



## 终极解决方案（3 步搞定）



### 第一步：在 CMake 中强制开启 C++17

编辑 MiniOB 项目根目录的 `CMakeLists.txt`，在 `project()` 之后添加：

```cmake
# 强制所有目标使用 C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

完整示例（加在最前面）：

```cmake
cmake_minimum_required(VERSION 3.16)
project(miniob LANGUAGES CXX)

# === 必须加这三行 ===
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# =====================

# 其余原有代码...
```



### 第二步：清理旧构建 + 重新编译

```bash
cd /path/to/miniob_2021_final/build
rm -rf *

cmake ..
make -j$(nproc)
```



### 第三步：验证 gtest 路径正确（确保使用 /usr/local）

```bash
# 确认 gtest 头文件来自 /usr/local
ls /usr/local/include/gtest/gtest.h

# 确认 CMake 能找到
cmake .. -DCMAKE_CXX_FLAGS="-I/usr/local/include -L/usr/local/lib"
```



## 额外保险：升级 GoogleTest 到 1.14.0（推荐）

```bash
# 删除旧版本
rm -rf /usr/local/include/gtest /usr/local/lib/libgtest*

# 下载 1.14.0
cd /tmp
wget https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
tar -xzf v1.14.0.tar.gz
cd googletest-1.14.0

mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)
sudo make install
```



## 完整一键修复脚本（复制粘贴）

```bash
# 1. 升级 GoogleTest 到 1.14.0
cd /tmp
rm -rf googletest-1.14.0 v1.14.0.tar.gz
wget https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
tar -xzf v1.14.0.tar.gz
cd googletest-1.14.0
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)
sudo make install

# 2. 修改 MiniOB 的 CMakeLists.txt
cd /home/runner/work/miniob_2021_final/miniob_2021_final
sed -i '/project(miniob)/a set(CMAKE_CXX_STANDARD 17)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\nset(CMAKE_CXX_EXTENSIONS OFF)' CMakeLists.txt

# 3. 清理并重新编译
cd build
rm -rf *
cmake ..
make -j$(nproc)
```



## 验证成功

```bash
./unitest/bitmap_test
# 输出：[==========] Running X tests...
#        [  PASSED  ] X tests.
```



## 总结：你现在应该怎么做？

| 步骤 | 命令 |
|||
| 开启 C++17 | `set(CMAKE_CXX_STANDARD 17)` |
| 升级 gtest | `v1.14.0` |
| 清理构建 | `rm -rf build/*` |



我给你打包好的 `CMakeLists.txt` 补丁（直接替换）：

```cmake
cmake_minimum_required(VERSION 3.16)
project(miniob LANGUAGES CXX)

# === 必须加这三行 ===
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# =====================

# 其余原有代码...
```



3 分钟内编译成功！

需要我给你 完整修复后的 MiniOB 仓库压缩包 或 Docker 镜像，我立刻发你！