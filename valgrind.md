# valgrind

Valgrind 是一个用于构建动态分析工具的仪器框架。 Valgrind 工具可以自动检测许多内存管理和线程错误，并对程序进行详细剖析。 目前，Valgrind 发行版包括七种高质量工具：一个内存错误检测器、两个线程错误检测器、一个高速缓存和分支预测剖析器、一个生成调用图的高速缓存和分支预测剖析器以及两个不同的堆剖析器。 它还包括一个实验性的 SimPoint 基本块向量生成器。 它可在以下平台上运行 X86/Linux、AMD64/Linux、ARM/Linux、ARM64/Linux、PPC32/Linux、PPC64/Linux、PPC64LE/Linux、S390X/Linux、MIPS32/Linux、MIPS64/Linux、X86/Solaris、AMD64/Solaris、ARM/Android（2.3.x 及更高版本）、ARM64/Android、X86/Android（4.0 及更高版本）、MIPS32/Android、X86/FreeBSD、AMD64/FreeBSD、ARM64/FreeBSD、X86/Darwin 和 AMD64/Darwin (Mac OS X 10.12)。

## 官网
https://valgrind.org/

[内存、性能问题分析的利器](https://blog.csdn.net/breaksoftware/article/details/79429330)

## 版本

valgrind 3.4.1
valgrind 3.4.0
valgrind 3.3.1
valgrind 3.3.0
valgrind 3.2.3
valgrind 3.2.2
valgrind 3.2.1
valgrind 3.2.0
valgrind 3.1.1
valgrind 3.1.0
valgrind 3.0.1
valgrind 3.0.0
valgrind 2.4.1
valgrind 2.2.0
valgrind 2.1.2
valgrind 2.1.1
valgrind 2.1.0
valgrind 2.0.0
valgrind 1.9.6

## 安装

git clone https://sourceware.org/git/valgrind.git
cd valgrind
./autogen.sh
./configure
make


sudo apt install -y valgrind valgrind-dbg valgrind-mpi

valgrind --leak-check=full --track-origins=yes ./my_program


Valgrind 允许你将输出或报错信息保存到文件中，而不是直接显示在终端上。这在你需要稍后分析输出或在不方便查看终端输出的环境中运行 Valgrind 时非常有用。

要将 Valgrind 的输出保存到文件中，你可以使用重定向操作符（>）或 --log-file 选项。以下是两种方法的示例：

使用重定向操作符
在 Unix-like 系统中，你可以使用重定向操作符 > 将 Valgrind 的输出重定向到文件中。例如：

bash
valgrind --leak-check=full ./your_program > valgrind_output.txt
但是，请注意，这种方法只会将标准输出（stdout）重定向到文件中，而 Valgrind 的错误和警告信息（包括内存泄露报告）通常是通过标准错误（stderr）输出的。为了同时捕获标准输出和标准错误，你可以使用 &>（在某些 shell 中是 2>&1）：

bash
valgrind --leak-check=full ./your_program &> valgrind_output.txt  
# 或者  
valgrind --leak-check=full ./your_program 2>&1 > valgrind_output.txt
注意：&> 是 Bash 和一些其他 shell 的语法糖，用于同时重定向标准输出和标准错误。如果你使用的是较旧的 shell 或脚本需要在不同的环境中运行，最好使用 2>&1。

使用 --log-file 选项
Valgrind 提供了 --log-file 选项，允许你指定一个文件来保存其输出。使用此选项时，Valgrind 会将所有输出（包括标准输出和标准错误）写入指定的文件，而不会在终端上显示任何内容。例如：

bash
valgrind --leak-check=full --log-file=valgrind_output.txt ./your_program
这种方法更加直接和方便，特别是当你只关心将 Valgrind 的输出保存到文件时。

总结
使用重定向操作符（&> 或 2>&1 >）可以捕获 Valgrind 的标准输出和标准错误。
使用 --log-file 选项可以将 Valgrind 的所有输出保存到指定的文件中，而不会在终端上显示任何内容。
根据你的具体需求选择合适的方法。


blog_rest_valgrind_output.txt

valgrind_output.txt