# tinycc
TCC 的全称是 Tiny C Compiler，有时也写作 TinyCC。顾名思义，它的最大特点就是“小”和“快”。
什么是 TCC？
TCC 是一个轻量级、高速的 C 语言编译器。它由法国程序员 Fabrice Bellard 开发（这位大神还开发了 FFmpeg、QEMU 等著名软件）。TCC 遵循 ISO C99 标准，同时也包含了一些 GNU C 的扩展。
TCC 的核心特点
1.  极其小巧
    ◦   完整的 TCC 可执行文件只有几百 KB，而 GCC 或 Clang 则动辄几十甚至上百 MB。
    ◦   它的源代码也非常简洁，易于理解和修改。
2.  编译速度极快
    ◦   TCC 被公认为世界上最快的 C 编译器之一。它的编译速度通常比 GCC 快数倍甚至一个数量级。
    ◦   之所以快，是因为它设计简单，没有进行复杂的优化处理，直接生成代码。
3.  无需链接器
    ◦   传统的编译流程是：预处理器 -> 编译器 -> 汇编器 -> 链接器。
    ◦   TCC 将这几个步骤全部集成在一起，可以直接从 C 源代码生成可执行文件或内存中的代码，跳过了生成 .o 目标文件再链接的步骤，这大大提升了速度。
4.  内存编译与执行
    ◦   这是 TCC 最独特的功能之一。它可以将 C 源代码直接编译并加载到内存中执行，而无需先生成磁盘上的可执行文件。
    ◦   这使得 TCC 可以像一个脚本解释器一样使用，实现 C 脚本 的功能。
        #!/usr/bin/tcc -run
        #include <stdio.h>
        int main() {
            printf("Hello, World!\n");
            return 0;
        }
        
        上面的代码可以直接像 Shell 或 Python 脚本一样运行。

5.  支持安全的沙盒编译
    ◦   TCC 包含一个可选的边界检查功能，可以检测数组越界等内存错误，提高了代码的安全性。

6.  可生成动态库
    ◦   尽管简单，但 TCC 功能完整，它支持编译生成动态链接库（.so 或 .dll）和静态库。

TCC 的局限性

TCC 的优势来自于其简洁的设计，这也带来了相应的局限性：

1.  优化能力很弱
    ◦   TCC 的主要目标是快速编译，而不是生成运行速度最快的代码。它只做了一些非常基础的优化。

    ◦   因此，由 TCC 编译产生的可执行文件，其运行速度通常远慢于 GCC 或 Clang 带 -O2 优化选项编译的程序。不适合用于对性能要求极高的生产环境发布。

2.  语言标准支持滞后
    ◦   TCC 完全支持 C99 和大部分 C89 标准，但对新的 C11 和 C17 标准支持不完整或尚未支持。如果你需要使用新的语言特性（如 _Generic, _Atomic），TCC 可能无法编译。

3.  平台支持相对有限
    ◦   虽然支持 x86, x86-64, ARM 等主流架构，但其支持和活跃度远不如 GCC 和 Clang。

TCC 的主要用途

鉴于以上特点，TCC 非常适合以下场景：

•   快速开发和原型验证：当你需要快速编译和测试一段代码时，TCC 的极速编译能极大提升效率。

•   C 脚本：将 C 语言当作脚本语言来使用，用于系统管理、自动化任务等。

•   教学和学习：由于其代码简洁，TCC 本身是学习编译器设计的优秀范例。用它来学习 C 语言，编译反馈非常迅速。

•   嵌入式或资源受限环境：在磁盘空间和内存都非常有限的环境中（如旧电脑、微型嵌入式系统），TCC 的小体积是巨大优势。

•   引导其他编译器：在构建一个全新的操作系统或交叉编译工具链时，可以先使用小巧的 TCC 编译出一个功能完整的 GCC 或 Clang。

获取与使用 TCC

•   官方网站：http://download.savannah.gnu.org/releases/tinycc/

•   GitHub 仓库：https://github.com/TinyCC/tinycc

在大多数 Linux 发行版中，可以直接通过包管理器安装：
# Debian/Ubuntu
sudo apt install tcc

# Arch Linux
sudo pacman -S tcc

# Fedora
sudo dnf install tcc


Windows 和 macOS 也有对应的预编译版本。

基本用法与 GCC 类似，非常简单：
# 编译并链接 hello.c，生成可执行文件 a.out (Linux/Unix) 或 a.exe (Windows)
tcc hello.c

# 指定输出文件名
tcc -o hello hello.c

# 直接编译并立即执行（不生成磁盘文件）
tcc -run hello.c


总结

特性 TCC GCC / Clang

核心目标 编译速度、小巧 代码优化、标准支持

编译速度 极快 较慢

代码性能 较差 优秀（开启优化后）

可执行文件大小 很小 较大

标准支持 C99 C11, C17, C23 等最新标准

适用场景 快速测试、脚本、教学、资源受限环境 生产环境、高性能计算、大型项目

总而言之，TCC 是一个独特而强大的工具，它在“快速编译”这个细分领域做到了极致。它不是要取代 GCC 或 Clang，而是作为一个有益的补充，在特定的场景下发挥着不可替代的作用。

##  编程语言
c

## 源代码
https://github.com/TinyCC/tinycc

## 手动编译源代码

git clone https://github.com/TinyCC/tinycc.git
cd tinycc
git checkout release_0_9_27
./configure
make
make test
make install

c/tinycc/linux/0_9_27
get_c_tinycc_linux_0_9_27.sh