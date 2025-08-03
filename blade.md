# blade

https://github.com/blade-build/blade-build

doc

https://github.com/blade-build/blade-build/tree/master/doc

Blade is a powerful build system from Tencent, supports many mainstream programming languages, such as C/C++, java, scala, python, protobuf...

http://google-engtools.blogspot.hk/2011/08/build-in-cloud-how-build-system-works.html

# example
https://github.com/blade-build/blade-build/tree/master/example/quick-start

Blade 运行时需要以下依赖：

Linux 或 Mac 操作系统
Python v2.7+
Ninja v1.8+
Blade还能和以下软件协作：

ccache v3.1+
distcc
Blade 编译项目时可能需要到：

gcc v4.0+
jdk v1.6+
scala v2.10+
swig v2.0+ (required for swig_library)
flex v2.5+ (required for lex_yacc)
bison v2.1+ (required for lex_yacc)

Blade 本身并不直接提供依赖下载功能，但它可以通过以下几种方式间接实现依赖库的获取：

外部依赖 (External Dependencies)：Blade 允许你在 BUILD 文件中定义外部依赖，例如通过 cc_library 或 cc_binary 规则中的 deps 字段引用其他库。这些外部库可以是：
本地库：位于项目目录之外的库，通过路径引用。
系统库：如 libpthread 等，由系统提供。
通过包管理器安装的库：你需要先使用系统包管理器（如 apt, yum, brew）或 C++ 专用包管理器（如 vcpkg, conan）安装这些库，然后 Blade 在构建时链接它们。
集成包管理器：虽然 Blade 本身不内置包管理功能，但你可以将 Blade 与外部的 C++ 包管理器（如 vcpkg 或 conan）结合使用。通常的做法是：
使用 vcpkg/conan 下载并安装项目所需的第三方库。
在 Blade 的构建配置中，指定这些库的头文件路径（include_dirs）和库文件路径（link_all_symbols 或通过 linkopts）。
Blade 在构建时会链接这些已下载的库。
源码依赖 (Source Dependencies)：Blade 的强大之处在于它支持将其他开源项目作为源码依赖直接包含在你的项目中。你可以：
使用 git submodule 或直接复制源码的方式将第三方库的源代码纳入你的项目目录。
为这些第三方库编写相应的 BUILD 文件（或使用它们自带的构建文件，如果支持）。
然后在你的主项目 BUILD 文件中通过 deps 直接引用这些源码库。Blade 会负责编译这些依赖库的源码，并将其链接到你的目标中。
总结：

Blade 本身不直接下载依赖库（不像 npm install 或 pip install 那样一键下载所有依赖）。它更侧重于声明和管理依赖关系。要获取依赖库，通常需要：

手动下载源码并集成到项目中（Blade 管理编译）。
使用外部包管理器（如 vcpkg, conan）先下载安装库，再让 Blade 链接。
依赖系统包管理器安装的库。
因此，虽然 Blade 不是“下载器”，但它通过清晰的依赖声明和构建规则，使得管理（包括需要下载的）依赖库变得非常方便和可靠。你项目的 BUILD 文件清晰地定义了所有依赖，结合外部工具或源码集成，就能实现依赖的获取和构建。

