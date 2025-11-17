# clang warn
## apple clang
这是一个很好的问题！确实存在多个 Clang 版本，这主要是由于不同的发布渠道和定制需求。让我详细解释：

1. 两个 Clang 的来源

1.1 LLVM 官方 Clang

# LLVM 官方发布的 Clang
clang version 5.0.0 (tags/RELEASE_500/final)
Target: x86_64-unknown-linux-gnu
Thread model: posix


特点：
• 上游版本：来自 LLVM 官方项目

• 功能完整：包含所有标准功能

• 更新及时：跟随 LLVM 发布周期

• 跨平台：支持所有主流操作系统

1.2 Apple Clang

# Apple 定制的 Clang
Apple clang version 9.0.0 (clang-900.0.39.2)
Target: x86_64-apple-darwin17.3.0
Thread model: posix


特点：
• Apple 定制：基于 LLVM Clang 但深度定制

• macOS 集成：与 Xcode 和 macOS 深度集成

• 版本滞后：通常比上游版本旧

• Apple 特定功能：包含 macOS/iOS 特定扩展

2. 版本差异的原因

2.1 发布周期不同


时间线示例：
2017年9月: LLVM Clang 5.0 发布
2017年12月: Apple Clang 9.0 发布（基于 Clang 4.0）


Apple Clang 版本号策略：
• 使用独立的版本号体系

• 数字通常比对应的上游版本大

• 反映在 Xcode 中的版本

2.2 对应关系表

Apple Clang 版本 基于的 LLVM Clang Xcode 版本 发布时间

Apple Clang 9.0 Clang 4.0 Xcode 9.0 2017年9月

Apple Clang 9.1 Clang 5.0 Xcode 9.3 2018年3月

Apple Clang 10.0 Clang 6.0 Xcode 10.0 2018年9月

Apple Clang 11.0 Clang 8.0 Xcode 11.0 2019年9月

3. 功能差异

3.1 标准支持差异

// LLVM Clang 5.0 可能支持 C++17 的更多特性
#include <variant>
#include <optional>

// Apple Clang 9.0 可能缺少某些新特性
// 可能不支持 std::variant 或需要特殊标志


3.2 Apple 特定扩展

// 只有 Apple Clang 支持的特性
#import <Foundation/Foundation.h>  // Objective-C
@import UIKit;                     // 模块导入

// Apple 特定的属性
__attribute__((availability(macosx, introduced=10.13)))
void appleSpecificAPI();


3.3 诊断信息差异

// LLVM Clang 可能有更详细的错误信息
error: no matching function for call to 'foo'

// Apple Clang 可能有不同的诊断格式
No viable conversion from 'int' to 'string'


4. 如何检查和管理多个 Clang

4.1 查看系统上的 Clang

# 查看所有可用的 Clang
which -a clang
which -a clang++

# 查看版本信息
clang --version
/usr/bin/clang --version  # Apple Clang
/usr/local/bin/clang --version  # 可能安装的 LLVM Clang


4.2 macOS 上的典型布局

# Apple 系统 Clang（随 Xcode 安装）
/usr/bin/clang
/usr/bin/clang++

# 手动安装的 LLVM Clang（通过 Homebrew 等）
/usr/local/opt/llvm/bin/clang
/usr/local/bin/clang


4.3 使用 Homebrew 管理多个版本

# 安装最新 LLVM Clang
brew install llvm

# 链接到 PATH
echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.zshrc

# 验证版本
clang --version  # 现在使用 LLVM Clang


5. 实际影响和选择建议

5.1 编译标志差异

# LLVM Clang 5.0 可能支持
clang -std=c++17 -stdlib=libc++ main.cpp

# Apple Clang 9.0 可能需要不同标志
clang -std=c++1z -stdlib=libc++ main.cpp


5.2 库依赖差异

# CMake 中需要处理版本差异
cmake_minimum_required(VERSION 3.10)
project(MyProject)

# 检查 Clang 版本
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 5.0)
        set(HAVE_CXX17 true)
    elseif(APPLE AND CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 9.0)
        # Apple Clang 9.0 基于 Clang 4.0，C++17 支持有限
        set(HAVE_CXX17 false)
    endif()
endif()


5.3 跨平台开发建议

# 更好的跨平台 CMake 配置
set(CMAKE_CXX_STANDARD 14)  # 使用广泛支持的 C++14
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 根据编译器能力设置特性
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag("-std=c++17" HAS_CXX17)
if(HAS_CXX17)
    target_compile_options(my_target PRIVATE -std=c++17)
endif()


6. 具体技术差异

6.1 默认标准库

# LLVM Clang 通常使用 libc++
clang -stdlib=libc++

# Apple Clang 强制使用 libc++（macOS）
# 无法选择其他标准库


6.2 目标平台支持

# LLVM Clang 支持更多目标
clang -target x86_64-pc-linux-gnu
clang -target aarch64-linux-gnu

# Apple Clang 主要针对 Apple 平台
clang -target x86_64-apple-macosx10.13
clang -target arm64-apple-ios11.0


6.3 调试信息格式

# LLVM Clang 默认 DWARF
clang -g main.cpp

# Apple Clang 使用特殊的调试格式
clang -g -fdebug-info-for-profiling main.cpp


7. 如何选择使用哪个 Clang

7.1 开发环境设置

# 在 ~/.zshrc 或 ~/.bashrc 中设置
# 优先使用 Homebrew 安装的 LLVM Clang
export PATH="/usr/local/opt/llvm/bin:$PATH"
export CC=clang
export CXX=clang++

# 或者明确指定
export CC=/usr/local/opt/llvm/bin/clang
export CXX=/usr/local/opt/llvm/bin/clang++


7.2 项目特定配置

# Makefile 示例
ifeq ($(shell uname),Darwin)
    # macOS 使用系统 Clang 或指定路径
    ifeq ($(shell which /usr/local/opt/llvm/bin/clang),)
        CC = clang
    else
        CC = /usr/local/opt/llvm/bin/clang
    endif
else
    CC = clang
endif


8. 总结

为什么有两个 Clang？

1. 发布渠道不同：
   • LLVM Clang：上游官方版本

   • Apple Clang：Apple 定制版本

2. 目标平台不同：
   • LLVM Clang：跨平台通用

   • Apple Clang：专注于 Apple 生态系统

3. 功能集差异：
   • LLVM Clang：标准功能完整

   • Apple Clang：包含 Apple 特定扩展

选择建议：
• macOS 开发：通常使用 Apple Clang（Xcode 集成）

• 跨平台项目：考虑使用 LLVM Clang

• 需要最新特性：安装 LLVM Clang

• 生产环境：匹配目标平台的编译器版本

理解这些差异有助于在不同环境中做出正确的编译器选择。
## doc
apt search clang

```shell
clang/bionic-updates 1:6.0-41~exp5~ubuntu1 amd64
  C, C++ and Objective-C compiler (LLVM based)

clang-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  C, C++ and Objective-C compiler

clang-10-doc/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 all
  C, C++ and Objective-C compiler - Documentation

clang-10-examples/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  Clang examples

clang-3.9/bionic 1:3.9.1-19ubuntu1 amd64
  C, C++ and Objective-C compiler (LLVM based)

clang-3.9-doc/bionic 1:3.9.1-19ubuntu1 all
  C, C++ and Objective-C compiler (LLVM based) - Documentation

clang-3.9-examples/bionic 1:3.9.1-19ubuntu1 amd64
  Clang examples

clang-4.0/bionic 1:4.0.1-10 amd64
  C, C++ and Objective-C compiler

clang-4.0-doc/bionic 1:4.0.1-10 all
  C, C++ and Objective-C compiler - Documentation

clang-4.0-examples/bionic 1:4.0.1-10 amd64
  Clang examples

clang-5.0/bionic 1:5.0.1-4 amd64
  C, C++ and Objective-C compiler

clang-5.0-doc/bionic 1:5.0.1-4 all
  C, C++ and Objective-C compiler - Documentation

clang-5.0-examples/bionic 1:5.0.1-4 amd64
  Clang examples

clang-6.0/bionic 1:6.0-1ubuntu2 amd64
  C, C++ and Objective-C compiler

clang-6.0-doc/bionic 1:6.0-1ubuntu2 all
  C, C++ and Objective-C compiler - Documentation

clang-6.0-examples/bionic 1:6.0-1ubuntu2 amd64
  Clang examples

clang-7/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  C, C++ and Objective-C compiler

clang-7-doc/bionic-updates 1:7-3~ubuntu0.18.04.1 all
  C, C++ and Objective-C compiler - Documentation

clang-7-examples/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  Clang examples

clang-8/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  C, C++ and Objective-C compiler

clang-8-doc/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 all
  C, C++ and Objective-C compiler - Documentation

clang-8-examples/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  Clang examples

clang-9/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  C, C++ and Objective-C compiler

clang-9-doc/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 all
  C, C++ and Objective-C compiler - Documentation

clang-9-examples/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  Clang examples

clang-format/bionic-updates 1:6.0-41~exp5~ubuntu1 amd64
  Tool to format C/C++/Obj-C code

clang-format-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  Tool to format C/C++/Obj-C code

clang-format-3.9/bionic 1:3.9.1-19ubuntu1 amd64
  Tool to format C/C++/Obj-C code

clang-format-4.0/bionic 1:4.0.1-10 amd64
  Tool to format C/C++/Obj-C code

clang-format-5.0/bionic 1:5.0.1-4 amd64
  Tool to format C/C++/Obj-C code

clang-format-6.0/bionic 1:6.0-1ubuntu2 amd64
  Tool to format C/C++/Obj-C code

clang-format-7/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  Tool to format C/C++/Obj-C code

clang-format-8/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  Tool to format C/C++/Obj-C code

clang-format-9/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  Tool to format C/C++/Obj-C code

clang-tidy/bionic-updates 1:6.0-41~exp5~ubuntu1 amd64
  clang-based C++ linter tool

clang-tidy-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  clang-based C++ linter tool

clang-tidy-3.9/bionic 1:3.9.1-19ubuntu1 amd64
  clang-based C++ linter tool

clang-tidy-4.0/bionic 1:4.0.1-10 amd64
  clang-based C++ linter tool

clang-tidy-5.0/bionic 1:5.0.1-4 amd64
  clang-based C++ linter tool

clang-tidy-6.0/bionic 1:6.0-1ubuntu2 amd64
  clang-based C++ linter tool

clang-tidy-7/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  clang-based C++ linter tool

clang-tidy-8/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  clang-based C++ linter tool

clang-tidy-9/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  clang-based C++ linter tool

clang-tools/bionic-updates 1:6.0-41~exp5~ubuntu1 amd64
  clang-based tools

clang-tools-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  clang-based tools for C/C++ developments

clang-tools-4.0/bionic 1:4.0.1-10 amd64
  clang-based tools for C/C++ developments

clang-tools-5.0/bionic 1:5.0.1-4 amd64
  clang-based tools for C/C++ developments

clang-tools-6.0/bionic 1:6.0-1ubuntu2 amd64
  clang-based tools for C/C++ developments

clang-tools-7/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  clang-based tools for C/C++ developments

clang-tools-8/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  clang-based tools for C/C++ developments

clang-tools-9/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  clang-based tools for C/C++ developments

clangd-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  Language server that provides IDE-like features to editors

clangd-9/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  Language server that provides IDE-like features to editors

elpa-irony/bionic 1.2.0-4 all
  Emacs C/C++ minor mode powered by libclang

irony-server/bionic 1.2.0-4 amd64
  Emacs C/C++ minor mode powered by libclang (server)

libclang-10-dev/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  Clang library - Development package

libclang-3.9-dev/bionic 1:3.9.1-19ubuntu1 amd64
  clang library - Development package

libclang-4.0-dev/bionic 1:4.0.1-10 amd64
  clang library - Development package

libclang-5.0-dev/bionic 1:5.0.1-4 amd64
  clang library - Development package

libclang-6.0-dev/bionic 1:6.0-1ubuntu2 amd64
  clang library - Development package

libclang-7-dev/bionic-updates 1:7-3~ubuntu0.18.04.1 amd64
  clang library - Development package

libclang-8-dev/bionic-updates,bionic-security 1:8-3~ubuntu18.04.2 amd64
  Clang library - Development package

libclang-9-dev/bionic-updates,bionic-security 1:9-2~ubuntu18.04.2 amd64
  Clang library - Development package

libclang-common-10-dev/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  Clang library - Common development package

libclang-common-3.9-dev/bionic 1:3.9.1-19ubuntu1 amd64
  clang library - Common development package

libclang-common-4.0-dev/bionic 1:4.0.1-10 amd64
  clang library - Common development package

libclang-common-5.0-dev/bionic 1:5.0.1-4 amd64
  clang library - Common development package

libclang-common-6.0-dev/bionic 1:6.0-1ubuntu2 amd64
  clang library - Common development package
```

Clang daemon: Version of clion-clangd is 30, but expected version is 37

clang

clang++

```
clang -v
Apple clang version 11.0.0 (clang-1100.0.33.16)
Target: x86_64-apple-darwin19.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin

clang -v
clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/7
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/7.3.0
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/8
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7.3.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/8
Selected GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/8
Candidate multilib: .;@m64
Selected multilib: .;@m64
```

.clang-format

clang-format命令行工具，Clion支持

## 编译源码

cmake
make
zlib
python

```shell
git clone -b llvmorg-17.0.6 https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm
make -j5
cd bin
ls
```

```shell
ls
FileCheck                    clang-scan-deps          llvm-diff                       llvm-min-tblgen                llvm-strings
UnicodeNameMappingGenerator  clang-tblgen             llvm-dis                        llvm-ml                        llvm-strip
amdgpu-arch                  count                    llvm-dlang-demangle-fuzzer      llvm-modextract                llvm-symbolizer
analyze-build                diagtool                 llvm-dlltool                    llvm-mt                        llvm-tapi-diff
apinotes-test                dsymutil                 llvm-dwarfdump                  llvm-nm                        llvm-tblgen
arcmt-test                   intercept-build          llvm-dwarfutil                  llvm-objcopy                   llvm-tli-checker
bugpoint                     llc                      llvm-dwp                        llvm-objdump                   llvm-undname
c-arcmt-test                 lli                      llvm-exegesis                   llvm-opt-fuzzer                llvm-windres
c-index-test                 lli-child-target         llvm-extract                    llvm-opt-report                llvm-xray
clang                        llvm-PerfectShuffle      llvm-gsymutil                   llvm-otool                     llvm-yaml-numeric-parser-fuzzer
clang++                      llvm-addr2line           llvm-ifs                        llvm-pdbutil                   llvm-yaml-parser-fuzzer
clang-17                     llvm-ar                  llvm-install-name-tool          llvm-profdata                  not
clang-ast-dump               llvm-as                  llvm-isel-fuzzer                llvm-profgen                   nvptx-arch
clang-check                  llvm-bcanalyzer          llvm-itanium-demangle-fuzzer    llvm-ranlib                    obj2yaml
clang-cl                     llvm-bitcode-strip       llvm-jitlink                    llvm-rc                        opt
clang-cpp                    llvm-c-test              llvm-jitlink-executor           llvm-readelf                   sancov
clang-diff                   llvm-cat                 llvm-lib                        llvm-readobj                   sanstats
clang-extdef-mapping         llvm-cfi-verify          llvm-libtool-darwin             llvm-reduce                    scan-build
clang-format                 llvm-config              llvm-link                       llvm-remark-size-diff          scan-build-py
clang-fuzzer-dictionary      llvm-cov                 llvm-lipo                       llvm-remarkutil                scan-view
clang-import-test            llvm-cvtres              llvm-lit                        llvm-rtdyld                    split-file
clang-linker-wrapper         llvm-cxxdump             llvm-locstats                   llvm-rust-demangle-fuzzer      verify-uselistorder
clang-offload-bundler        llvm-cxxfilt             llvm-lto                        llvm-sim                       yaml-bench
clang-offload-packager       llvm-cxxmap              llvm-lto2                       llvm-size                      yaml2obj
clang-refactor               llvm-debuginfo-analyzer  llvm-mc                         llvm-special-case-list-fuzzer
clang-rename                 llvm-debuginfod          llvm-mca                        llvm-split
clang-repl                   llvm-debuginfod-find     llvm-microsoft-demangle-fuzzer  llvm-stress
```

## 社区

https://discord.com/invite/xS7Z362

https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm

## releases/version/版本
通 llvm.md
