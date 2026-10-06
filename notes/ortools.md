# ortools

https://github.com/google/or-tools

https://gitee.com/edidada/cumcm-paper-and-source-code
CUMCM-Paper-And-SourceCode/2019C机场出租车/queueing_system_ortools.py

Google OR-Tools库是一个用于解决组合优化问题的强大工具套件。它集合了各种先进的优化算法，旨在解决各种类型的优化问题，如线性规划、整数规划、车辆路径规划以及图论算法等。
OR-Tools的核心算法是用C++编写的，因此它具有跨平台性，并且可以在不同的操作系统和硬件平台上使用。同时，它也支持Python、Java和C#等编程语言的调用，这使得开发者可以根据自己的技术栈选择适合的编程语言来解决问题。
OR-Tools提供了统一的接口，用于多种线性规划和混合整数规划求解，包括CBC、CLP、GLOP、GLPK、Gurobi、CPLEX和SCIP等求解器。这使得用户可以根据自己的需求选择合适的求解器来解决问题。
此外，OR-Tools还提供了图算法、经典旅行推销员问题和车辆路径问题的算法，以及经典装箱和背包算法等。这些算法和工具可以帮助用户解决各种复杂的优化问题。
OR-Tools是一个开源且开放的软件套件，用户可以免费使用并查看其源代码。它还支持第三方求解器的接入，如CPLEX等商用求解器以及SCIP等开源求解器，这使得用户可以根据需要选择更高级的求解器。
总的来说，Google OR-Tools库是一个功能强大、灵活且易于使用的优化工具套件，它可以帮助开发者高效地解决各种复杂的优化问题。无论你是运筹学专家还是初学者，都可以从OR-Tools中找到适合自己的解决方案。

## java

https://developers.google.com/optimization/install/java/pkg_windows?hl=zh-cn

  <dependency>
    <groupId>com.google.ortools</groupId>
    <artifactId>ortools-java</artifactId>
    <version>9.8.3296</version>
    <type>jar</type>
    <scope>compile</scope>
  </dependency>

直接查询libc和libc++的具体文件版本
对于更直接地查看文件级别的版本信息，你可以使用otool和install_name_tool命令：
查看动态库的安装名称和路径：
otool -L /usr/lib/libc.dylib
或者对于C++：
otool -L /usr/lib/libc++.dylib

查看动态库的版本：

install_name_tool -dump /usr/lib/libc.dylib

Python 库：C++ 的封装（Binding）
是的，Python 的 ortools 是一个 Binding（绑定/封装）。
它的源码里直接包含了一个“连接 C++ 层”的模块（ortools.init.python.init）。这意味着你在 Python 里调用的每一个函数，最终都会通过一层接口去执行底层的 C++ 代码。

Java 库：同样是 Wrapper
Java 版也是 封装。官方安装文档特别提醒：Java 版 OR-Tools 库是 “C++ 原生库的封装容器（wrapper）”，所以安装时必须先装好 C++ 的运行库（Microsoft Visual C++ Redistributable）。Java 代码通过 JNI（Java Native Interface）来调用 C++ 核心，比如你在 Java 代码里调用的 mainJNI 类，就是在负责这种跨语言交互