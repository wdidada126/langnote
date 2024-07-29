# rust

std

Primitive Types
Modules
Macros
Keywords

基本类型 模块 宏 关键字

https://doc.rust-lang.org/std/index.html

https://zhuanlan.zhihu.com/p/149548652

命令行执行：
rustup doc

file:///Users/ibqo/.rustup/toolchains/stable-x86_64-apple-darwin/share/doc/rust/html/index.html

/Users/ibqo/.rustup/toolchains/stable-x86_64-apple-darwin/lib/rustlib/src/rust/library

ls
alloc				rtstartup
backtrace			rustc-std-workspace-alloc
core				rustc-std-workspace-core
panic_abort			rustc-std-workspace-std
panic_unwind			std
portable-simd			stdarch
proc_macro			test
profiler_builtins		unwind


https://github.com/shadowsocks/shadowsocks-rust

https://github.com/helix-editor/helix

本书为《Programming Rust - Fast, Safe Systems Development》第2版的个人中文翻译，仅供学习和交流使用，如有侵权请联系作者删除
https://github.com/MeouSker77/ProgrammingRust

脱离标准库 Rust可以写OS

https://github.com/Svetlitski/fcp

git clone -b v0.2.1 https://github.com/Svetlitski/fcp.git

Rust ubuntu 16

Struct
impl
err

?

cloudwego字节跳动开源Rust框架
https://github.com/cloudwego/volo

「Rust日报」2019每周精选 • 第九期

rust
base64编码

rust写os

美国弗吉尼亚大学计算机OS课程的作业便要求是用Rust语言来完成的。在不带运行时的情况下Rust内存管理虽然是自动的但并不依赖垃圾收集器，这也是本文后续要介绍的。

### 从零开始写 OS

超级详细的 rust OS 编写教程，作者是清华大学陈渝教授的学生

https://learningos.github.io/rcore_step_by_step_webdoc/

rustup update

实验楼rust教程

print相关函数
format
宏

- [kafka-rust](https://github.com/edidada/kafka-rust)
- [Rocket0.4.2](https://github.com/edidada/Rocket0.4.2)
- [testiron](https://github.com/edidada/testiron)
- ### [testrustspin](https://github.com/edidada/testrustspin)

https://learnku.com/docs/cargo-book/2018/specifying-dependencies/4773

你配置的是cargo的源，不是rustup的源

### 路线图

http Rocket
log  ？ std::log是api，env_log实现
mysql ？libmysql 绑定c
json ?

`rustup override set nightly`

[rust : rustup切换stable、nightly](https://blog.csdn.net/wowotuo/article/details/90743180)

rust windows，kafka-rust，使用openssl的c库，交叉编译
vcpkg

环境变量设置OPENSSL_DIR=D:\vcpkg\installed\x64-windows-static

ide智能提示
rust-analyzer

Rust开发操作系统
不链接libc
面向的平台不是已知的

Rust没有class，用fleid引用父类对象来实现？

[iron repo](https://github.com/iron/iron/)

[iron](http://ironframework.io/)

[iron doc](https://docs.rs/iron/0.6.0/iron/)

```shell
/home/edidada/.cargo/bin/cargo run --color=always --package iron --bin iron
error: There are multiple `iron` packages in your project, and the specification `iron` is ambiguous.
Please re-run this command with `-p <spec>` where `<spec>` is one of the following:
  iron:0.6.0
  iron:0.1.0

Process finished with exit code 101
```

/home/edidada/.cargo/bin/cargo run --color=always --package iron --bin iron

开发ide

- Clion 带插件
- idea 带插件 比Clion更好
- eclipse


  标准库
  三方库

从LLVM bitcode生成Rust可执行文件

```shell
rls --version
error: 'rls.exe' is not installed for the toolchain 'stable-x86_64-pc-windows-msvc'
To install, run `rustup component add rls --toolchain stable-x86_64-pc-windows-msvc`

C:\Users\edidada>rustup component add rls --toolchain stable-x86_64-pc-windows-msvc
error: toolchain 'stable-x86_64-pc-windows-msvc' does not contain component 'rls' for target 'x86_64-pc-windows-msvc'

C:\Users\edidada>rustup update

rustc --version --verbose

rls --version
rls 1.34.0 (0d6f53e 2019-02-14)
```

跨文件调用

mod

LLVM确实提供了所有功能，因此了解不执行的功能非常有用。
例如，LLVM不会解析语言的语法。许多工具已经可以完成这项工作，例如lex/yacc，flex/bison和ANTLR。无论如何，解析都是要与编译分离的，因此LLVM不会尝试解决任何这些也就不足为奇了。
LLVM还没有直接解决围绕给定语言的更广泛的软件文化。安装编译器的二进制文件，在安装中管理软件包以及升级工具链-您需要自己完成。
最后，也是最重要的一点，LLVM仍然有一些语言的通用部分，而它们并未提供原语。许多语言都有某种方式的垃圾回收内存管理，既可以作为管理内存的主要方式，也可以作为RAII之类的策略（C ++和Rust使用）的辅助。LLVM并没有为您提供垃圾收集器机制，但是它确实提供了 通过允许用元数据标记代码来实现垃圾收集的工具，从而使编写垃圾收集器变得更加容易。

https://docs.rs/releases

https://doc.rust-lang.org/nightly/nightly-rustc/rustc/hir/index.html

https://rustforce.net/article?id=beae65c6-b723-420a-a2fc-dc9b935e2da9

Compiling autocfg v0.1.7
error[E0658]: use of unstable library feature 'alloc': this library is unlikely to be stabilized in its current form or name (see issue #27783)
  --> C:\Users\edidada\.cargo\registry\src\mirrors.ustc.edu.cn-61ef6e0cd06fb9b8\smallvec-1.0.0\lib.rs:38:1

[awesome-rust](https://github.com/rust-unofficial/awesome-rust)

http-client     hyper

http-server	[Rocket](https://github.com/SergioBenitez/Rocket)

将错误信息输出到标准错误而不是标准输出

想起来还有个ripgrep，性能很好的命令行正则表达式搜索工具，已被atom和vscode集成为默认搜索工具。

deno

马上Facebook libra 再助攻一把

Tikv servo

我上次还见谁把 rust 的 unicode 支持吹得无人能及来着，可能他就没听说过 swift 和 perl

Rust 语言层面对 unicode 的支持也只是比较基础的东西，吹那么高干啥

 RustFest 2018大会上Alex Crichton 和 David Tolnay两位大佬

rust

ll

ml ir

optimize

为了和现有的生态系统良好地集成，Rust 支持非常方便且零成本的 FFI 机制，兼容 C-ABI，并且从语言架构层面上将 Rust 语言分成 Safe Rust 和 Unsafe Rust 两部分。其中 Unsafe Rust 专门和外部系统打交道，比如操作系统内核。

百度开源的 brpc 框架新增 Rust 语言支持

http://smallcultfollowing.com/babysteps/blog/2015/12/18/rayon-data-parallelism-in-rust/

Rayon: data parallelism in Rust

https://github.com/rustcc/awesome-rust

https://github.com/rajasekarv/vega

# Rayon: data parallelism in Rust

安装Windows环境
https://www.cnblogs.com/qq67579722/p/12897819.html

### Rust toolschan

- stable-x86_64-pc-windows-msvc
- stable-x86_64-pc-windows-gnu updated

国内代理

下载库文件设置位置，不能放c盘

C:\Users\edidada\.rustup
2G多的磁盘占用

 'cargo'
 'clippy'
 'llvm-tools-preview'
 'rls'
 'rust-analysis'
 'rust-docs'
 'rust-src'
 'rust-std'
 'rustc'
 'rustfmt'

info: latest update on 2024-07-25, rust version 1.80.0 (051478957 2024-07-21)

在Windows上安装Rust的特定版本（非最新版本），你可以通过Rust的官方安装器rustup来实现。rustup是Rust的官方安装和版本管理工具，允许你安装、更新、卸载Rust编译器和相关的工具链。以下是通过rustup安装Rust特定版本的步骤：

1. 下载并运行Rust安装器
访问Rust的官方网站https://www.rust-lang.org/zh-CN/。
在页面中找到Rust安装器的下载链接，通常是在“安装”或“获取Rust”部分。点击下载适用于Windows的安装器rustup-init.exe。
2. 运行安装器并安装Rust
双击下载的rustup-init.exe文件启动安装程序。
在安装过程中，你会被询问是否要修改安装选项。默认情况下，rustup会安装Rust的最新稳定版本。但是，你可以通过自定义安装选项来安装特定版本。
要安装特定版本，你可能需要在安装程序提示你选择安装类型时选择“自定义安装”（通常是通过输入2然后回车）。
接下来，在询问你要安装哪个工具链时，你可以输入具体的版本号，如stable-YYYY-MM-DD（其中YYYY-MM-DD是发布日期），或者如果你知道具体的版本号（如1.59.0），你可以尝试直接输入该版本号（但请注意，直接输入具体版本号可能不是所有情况都支持，通常更常见的是通过发布日期来指定）。
如果直接输入版本号不可行，你可能需要在安装完Rust后，使用rustup命令行工具来切换或安装特定版本。
3. 使用rustup安装或切换特定版本
如果安装程序没有直接提供安装特定版本的选项，你可以在安装Rust后，通过rustup命令行工具来安装或切换到特定版本。打开命令行工具（如cmd或PowerShell），然后执行以下命令：

查看可安装的Rust版本：
```bash
rustup toolchain list available
```
安装特定版本的Rust（以1.59.0为例）：
```bash
rustup toolchain install 1.59.0
```
切换到特定版本的Rust作为默认版本（以1.59.0为例）：
```bash
rustup default 1.59.0
```
请注意，由于Rust的版本和安装程序可能会更新，上述步骤中的具体命令和选项可能会有所不同。因此，建议参考rustup的官方文档或rustup命令行工具的帮助信息来获取最准确的信息。

此外，如果你在中国大陆地区，可能会遇到下载速度较慢的问题。为了加速下载过程，你可以考虑配置Rust的国内镜像源，如清华大学开源软件镜像站、中国科学技术大学镜像站等。具体配置方法可以在Rust的官方文档或相关社区中找到。

## 标准库
Rust标准库是Rust语言的核心组成部分，提供了一组稳定且可靠的API，用于构建Rust程序。Rust标准库主要分为三个主要部分：core、alloc和std。以下是对这三个部分内容的详细概述：

1. Core库
概述：Core库是Rust的核心库，它不依赖于任何外部的分配器，因此适用于任何环境，包括内核级别的开发。Core库是与硬件CPU架构无关的可移植库，包含了Rust语言的基础类型和基本功能。
主要内容：
编译器内置固有（intrinsic）函数：包括内存操作函数、数学函数、位操作函数、原子变量操作函数等，这些函数通常与CPU硬件架构紧密相关，且一般需要使用汇编代码来提供最佳性能。
基本特征（Trait）：如运算符（OPS）Trait、编译器Marker Trait、迭代器（Iterator）Trait、类型转换Trait等。
Option/Result类型：这些类型虽然不是编译器的内嵌类型，但它们是Rust中不可或缺的语法组成部分。
基本数据类型：包括整数类型、浮点类型、布尔类型、字符类型和单元类型，对这些类型实现了基本特征及一些特有函数。
数组、切片及Range类型：提供了对这些类型的基本特征及一些特有函数的实现。
内存操作：包括alloc模块、mem模块、ptr模块，Rust中大部分的不安全（unsafe）语法都与这些模块相关。
字符串及格式化：对字符串类型实现了基本特征及一些特有函数，包括格式化功能。
内部可变性类型：如UnSafeCell<T>、Cell<T>、RefCell<T>等，实现了对这些类型的基本特征及一些特有函数。
其他：还包括FFI（Foreign Function Interface）、时间、异步库等内容。
2. Alloc库
概述：Alloc库提供了动态内存分配的能力，它依赖于Core库。Alloc库的所有类型都基于堆内存，包括智能指针类型、集合类型、容器类型等。
主要内容：
内存申请与释放：通过Allocator Trait及其实现者Global单元类型进行。
基础智能指针类型：如Box<T>、Rc<T>。
动态数组智能指针类型：如RawVec<T>、Vec<T>。
字符串智能指针类型：如String。
并发安全基础智能指针类型：如Arc<T>。
集合类型：如LinkedList<T>、VecQueue<T>、BTreeSet<T>、BTreeMap<T>等。
3. Std库
概述：Std库是建立在Core和Alloc之上的标准库，提供了大多数Rust程序所需的功能，包括文件I/O、错误处理、集合类型等。Std库只适用于用户态编程。
主要内容：
对Core库及Alloc库的内容进行映射：提供了对这两个库内容的封装和扩展。
进程管理与进程间通信：实现了进程管理及相关通信功能。
线程管理：包括线程间临界区/互斥锁、消息通信等线程相关内容。
文件、目录及OS环境：提供了文件、目录操作及OS环境相关的函数和类型。
输入、输出：实现了输入、输出相关的功能。
网络通信：提供了网络通信相关的函数和类型。
综上所述，Rust标准库通过Core、Alloc和Std三个主要部分，为Rust程序提供了丰富且强大的功能支持。这些库的设计和实现都是基于Rust语言的设计目标和现代编程语言的特征，确保了Rust程序的高效性、安全性和可移植性。
## 关键字

## oo还是fp

