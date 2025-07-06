# abi

名字修饰（name decoration），也称为名字重整、名字改编（name mangling），是现代计算机程序设计语言的编译器用于解决由于程序实体的名字必须唯一而导致的问题的一种技术。

https://www.cnblogs.com/ToTigerMountain/articles/18024548

使用extern ”C“关键字可以强制C++不做名字修饰，事实库函数通常都是这么写的

您说得非常对。在 C++ 中使用 `extern "C"` 关键字可以强制编译器不对链接的符号名进行 name mangling(名字修饰)。这在与 C 语言进行交互时非常有用。

下面是一个具体的例子:

假设我们有一个 C 语言函数 `add(int a, int b)` 定义在 `mymath.h` 头文件中:

```c
// mymath.h
#ifndef MYMATH_H
#define MYMATH_H

int add(int a, int b);

#endif
```

在 C++ 代码中使用这个 C 函数时,我们可以用 `extern "C"` 包裹函数声明,这样就可以避免 C++ 编译器对函数名进行修饰:

```cpp
// main.cpp
#include <iostream>
#include "mymath.h"

extern "C" {
    int add(int a, int b);
}

int main() {
    int result = add(3, 4);
    std::cout << "3 + 4 = " << result << std::endl;
    return 0;
}
```

在这个例子中,`add()` 函数是一个纯 C 函数,没有经过 C++ 的名字修饰。如果不使用 `extern "C"`,C++ 编译器会将 `add()` 函数名修饰成诸如 `_Z3addii` 之类的形式,这样在链接时就会找不到对应的符号。

`extern "C"` 的作用就是告诉 C++ 编译器,后面的声明/定义是 C 语言风格的,不需要进行 name mangling。这在使用 C 语言库函数时非常有用。

事实上,大部分标准 C 库函数,如 `printf()`、`malloc()` 等,其声明都是使用 `extern "C"` 进行包裹的,这样 C++ 程序就可以直接调用这些 C 语言函数了。

是的,关于 C/C++ ABI (Application Binary Interface)的详细介绍和教程,网上有很多不错的资源:

1. ABI 介绍 - GNU 文档
   - 链接: https://gcc.gnu.org/onlinedocs/gcc/C-Implementation.html#C-Implementation
   - 这是 GNU 编译器集合 (GCC) 的官方文档,其中详细介绍了 C 语言的 ABI 实现细节,包括数据类型、函数调用约定等。

2. C++ ABI 规范
   - 链接: https://itanium-cxx-abi.github.io/cxx-abi/
   - 这是 C++ ABI 的官方规范,由 Itanium C++ ABI 工作组维护。涵盖了类、异常处理、名字修饰等 C++ 特有的ABI 内容。

3. ABI 教程 - IBM developerWorks
   - 链接: https://developer.ibm.com/articles/l-abigen/
   - IBM 的这篇文章全面地介绍了什么是 ABI,以及如何使用 abigen 工具分析 ABI。对初学者很有帮助。

4. ABI 差异分析 - Red Hat
   - 链接: https://access.redhat.com/articles/1320623
   - Red Hat 的这篇文章深入探讨了不同 ABI 版本之间的差异,以及如何处理 ABI 兼容性问题。

5. ABI 最佳实践 - Stackoverflow
   - 链接: https://stackoverflow.com/questions/2171175/what-is-the-c-c-abi-and-why-should-i-care
   - Stackoverflow 上的这个帖子总结了 ABI 的重要性以及使用 ABI 的最佳实践。

这些资源涵盖了 C/C++ ABI 的方方面面,从基本概念到实际应用,都有很好的介绍。希望对你理解 ABI 有所帮助。如果还有其他问题,欢迎继续询问。


 一些实现C++ ABI的实践参考
除了C Style API，如果需要实现C++ ABI，我们应该如何着手？

避免在接口处使用虚函数与Pimpl

文章说明了C++虚函数的弊端，以及COM通过继承的方式拓展接口的弊端，表扬了Linux Kernel通过系统调用的方式保持接口的不变性，并说明了Pimpl方式实现接口的好处。 并说明了非虚函数的健壮性： virtual function 是 bind-by-vtable-offset，而 non-virtual function 是 bind-by-name。 最后，作者提供了一个推荐做法：

使用Pimpl包装实现，将实现代码完全转移到so中，二进制随着库升级自动变更；
class内的API不使用虚函数，可以灵活在新版本中添加新的函数；
D-Pointer

类似于Pimpl，D-Pointer也是将实现细节完全隐藏在库内的接口设计方式。Qt因此而具有非常好的ABI兼容性，即使我们将使用底版本（比如Qt4.5）编译的App，也能在高版本（比如Qt4.6）库中正确运行。

d-pointer的思想是，在导出类中保存一个私有类/数据结构的指针，这个私有的类的子类可以自由的变更，而不会对APP产生副作用，对于APP来说，d-pointer只是一个指针，导出类的大小没有变化，所以不存在ABI问题。

上面提到的私有类的子类，虽然可以在内部自由变化，但是我们需要将这个d-pointer转换到其对应的子类，以及相互转换。这时，Qt内部就提供了便捷的宏（Q_D和Q_Q。Q_DECLARE_PRIVATE和Q_DECLARE_PUBLIC）来完成这个事情。


ABI Compliance Checker
git clone https://github.com/lvc/abi-compliance-checker.git

https://lvc.github.io/abi-compliance-checker/


Android SDK则使用了libabigail对kernel进行ABI兼容性检查。

ABI Compliance Checker 主页后面提供了很多非常有价值的参考文章，介绍了ABI兼容性和如何实现ABI兼容性。

ABI Compliance Checker的使用有两种方法，一种是源码编译，另一种是在linux上直接通过apt-get 安装工具。

sudo apt update -y
sudo apt install vtable-dumper abi-dumper abi-compliance-checker -y

时隔5年之后，我终于又用起来conan了。没选择vcpkg是因为我随便选了一个。这次效果就好很多，安装顺利，使用方便，但是编译的包会出现段错误。经过各种排查，才发现是默认GCC ABI用的是旧的，新版本的GCC需要使用stdlibc++11。修改之后就很顺畅。
您遇到的段错误可能与GCC的ABI（Application Binary Interface）变化有关。以下是相关情况和解决方法的详细说明：
#### 段错误情况
1. GCC ABI变更
   - 自GCC 5.1版本起，引入了C++11 ABI的新实现，通过`-D_GLIBCXX_USE_CXX11_ABI`选项控制。
   - 旧版GCC（如GCC 4.x）默认使用旧的C++03 ABI。
   - 新版本的GCC（如GCC 5.x及以上）默认使用C++11 ABI，除非显式指定`-D_GLIBCXX_USE_CXX11_ABI=0`。
2. ABI不兼容导致段错误
   - 库与代码ABI不一致：如果您的代码使用了新ABI编译，但链接的库是旧ABI编译的，或反之，会导致运行时错误，如段错误。
   - 类型不匹配：新旧ABI中`std::string`等类型的内部实现不同，传递这些类型时可能出现内存访问错误。
#### 查看GCC的ABI
1. 查看GCC版本
   - 使用命令`gcc --version`或`g++ --version`查看GCC版本。
   - 版本号影响默认的ABI选择。
2. 检查ABI选项
   - 编译命令：查看编译时的命令是否包含`-D_GLIBCXX_USE_CXX11_ABI`选项。
   - Conan配置文件：在Conan的`conanfile.txt`或`conanfile.py`中，检查`settings.compiler.libcxx`设置。
3. 查看已编译库的ABI
   - 使用`readelf`命令查看库的符号表：
     ```bash
     readelf -p .comment <lib-name>
     ```
   - 搜索`GLIBCXX`关键字，确认使用的ABI版本。
#### 解决方法
1. 统一ABI选项
   - 在编译代码和依赖库时，确保使用相同的`-D_GLIBCXX_USE_CXX11_ABI`选项。
   - 例如，在CMake中设置：
     ```cmake
     add_compile_options(-D_GLIBCXX_USE_CXX11_ABI=1)
     ```
2. 指定GCC版本
   - 使用Conan指定GCC版本和ABI选项：
     ```python
     # conanfile.txt
     [requires]
     mylib/1.0@user/channel
     compiler=gcc/9.3
     compiler.libcxx=libstdc++11
     ```
3. 修改Conan配置文件
   - 在Conan的`profile`文件中设置ABI选项：
     ```ini
     # ~/.conan/profiles/default
     [settings]
     compiler=gcc
     compiler.version=9
     compiler.libcxx=libstdc++11
     ```
4. 检查依赖库
   - 确保所有依赖库都使用相同的ABI编译。
通过以上方法，您可以解决因GCC ABI不兼容导致的段错误问题，确保代码和库的兼容性。
大多数项目在初期时候，变化方向不明确，因此系统内部结构是不稳定的。在中期结构稳定后，可能又缺乏演进式设计和重构能力，对软件结构的划分未必能保证低耦合。如果当大多数变更都需要跨越多个包的时候，采用包管理这种隔离性强的方式，反而会增大协作沟通成本，降低效率。幸运的是，conan提供了editable mode package和workspace的特性(RUST的cargo也提供了这个特性)，来让多包协作的修改变得稍微容易一些。
许多编程语言都把包管理器作为一个抓手，围绕着包开发来打造贯穿整个开发过程的最佳实践和辅助工具。包管理的引入会将原有的软件模块团队的交付终点，从仅仅将代码合入到代码库，延长到了需要保证构建、测试、打包和发布成功，并且满足包版本的发布契约（验收测试和契约测试），从而真正意义上的使能团队独立流水线，推动了团队的devops能力。
作者：MagicBowen链接：https://www.jianshu.com/p/5de358c1c007來源：简书简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
