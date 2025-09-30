# rust
https://rustcc.cn/

## rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup toolchain list -v
rustup install 1.80.0
rustup default 1.80.0


https://github.com/rust-lang/rust/releases

rustup self update
info: checking for self-update
  rustup unchanged - 1.27.1

rustc --version

在Rust中，并没有直接称为"override"或"overwrite"的函数重写机制，如同在面向对象编程（OOP）语言（如Java或C++）中那样。Rust是一门多范式编程语言，它支持面向对象的特性（通过结构体和trait），但更倾向于使用组合而非继承来构建复杂的系统。

然而，Rust通过使用trait（接口）和泛型来模拟类似的行为。如果你想要实现类似函数重写的功能，你可以通过定义一个trait，然后在不同的结构体上实现这个trait的同名方法。这样，虽然这不是严格意义上的"重写"（因为Rust中没有继承），但你可以根据结构体类型调用不同的实现，实现类似的效果。

下面是一个简单的例子，展示了如何在Rust中模拟函数重写：

rust
trait Animal {  
    fn make_sound(&self) -> String;  
}  
  
struct Dog {}  
  
impl Animal for Dog {  
    fn make_sound(&self) -> String {  
        "Woof!".to_string()  
    }  
}  
  
struct Cat {}  
  
impl Animal for Cat {  
    fn make_sound(&self) -> String {  
        "Meow!".to_string()  
    }  
}  
  
fn main() {  
    let dog = Dog{};  
    let cat = Cat{};  
  
    println!("Dog says: {}", dog.make_sound()); // 输出: Dog says: Woof!  
    println!("Cat says: {}", cat.make_sound()); // 输出: Cat says: Meow!  
}
在这个例子中，Animal trait定义了一个make_sound方法，而Dog和Cat结构体分别实现了这个方法。虽然这不是传统意义上的重写（因为Rust没有继承），但我们通过为不同的结构体实现同一个trait方法，实现了类似的效果。

需要注意的是，Rust的这种做法与OOP中的继承和多态有相似之处，但它更加灵活和强大，因为它不依赖于继承的层次结构。此外，Rust的类型系统（如泛型、trait和生命周期）提供了额外的安全性和表达力，使得开发者能够编写出既安全又高效的代码。

在某种意义上，Rust的trait可以被视为类似于C++中的interface，但它们之间存在一些关键差异。

相似之处
抽象接口：Rust的trait和C++的interface都提供了一种定义一组方法的接口的方式，这些方法将由实现它们的类型来具体实现。
多态：两者都支持多态，即你可以通过接口的引用来操作实现了该接口的不同类型的对象。
关键差异
默认实现：Rust的trait可以包含带有默认实现的方法，这意味着当你为一个类型实现这个trait时，你可以选择覆盖这些方法或简单地继承默认实现。C++的interface直到C++11（通过纯虚函数）和C++20（通过concept和可能的requires子句，但这不是真正的接口实现）之前，一直不支持方法的默认实现。
静态解析类型（SRT） vs 动态多态：Rust的trait方法通常是静态解析的，这意味着在编译时就知道调用哪个实现。这有助于减少运行时开销并提高性能。然而，Rust也支持通过动态分发（如使用Box<dyn Trait>）来实现动态多态。C++的接口则默认是动态多态的，通过虚函数表（vtable）实现。
与泛型的结合：Rust的trait与泛型紧密结合，可以定义泛型trait并为特定的类型参数集合实现它。这使得Rust能够以非常灵活和强大的方式编写泛型代码。C++虽然也支持模板和接口，但它们的结合不如Rust那样无缝。
语言设计哲学：Rust和C++在设计哲学上有很大不同。Rust更加关注内存安全和并发编程，而C++则更侧重于性能优化和与C的兼容性。这种差异反映在它们如何处理接口（或traits）的方式上。
多重继承：C++支持多重继承，包括从多个接口继承。Rust不支持多重继承，但你可以通过组合多个trait（使用+操作符，尽管这通常用于trait bounds而非在类型上直接应用）来模拟类似的行为。然而，Rust中的组合方式通常更加明确和安全。
总之，虽然Rust的trait在概念上与C++的interface有相似之处，但它们在实现、用途和与语言其他部分的集成方面存在显著差异。在Rust中，trait不仅仅是接口，它们还是Rust类型系统中的一个关键部分，支持泛型编程、类型安全和强大的抽象能力。

ownership也是rust的一大卖点
在Rust中，所有权（ownership）是其内存安全特性中的一个核心概念。它帮助Rust编译器在编译时自动管理内存，避免了如悬挂指针（dangling pointers）、内存泄漏和缓冲区溢出等常见问题。通过所有权系统，Rust确保了每个值在任一时刻都只有一个所有者，当所有者离开作用域时，其拥有的值将被自动清理。

下面是一个简单的Rust代码例子，展示了所有权的基本工作原理：

```rust
fn main() {  
    // 创建一个字符串并分配内存  
    let s1 = String::from("hello");  
  
    // s1 现在拥有这块内存  
    // 通过 move 语义（这里实际上是隐式的），我们将所有权从 s1 转移给 s2  
    let s2 = s1;  
  
    // s1 不再拥有这块内存，此时尝试使用 s1 会导致编译错误  
    // println!("{}", s1); // 这行代码会报错，因为 s1 不再拥有它的数据  
  
    // 当 s2 离开作用域时，其拥有的字符串会被自动清理  
    // 注意，这里 s2 实际上在 main 函数的末尾离开作用域  
    println!("{}", s2); // 输出: hello  
  
    // 字符串切片（string slice）不拥有数据，它们只是指向某个字符串的一部分  
    let s = String::from("world");  
    // 字符串切片 s3 指向 s 中的数据，但不拥有它  
    let s3 = &s[0..5];  
  
    // s3 仅仅是一个借用的视图，s 仍然拥有数据  
    // 当 s 离开作用域时，其拥有的字符串会被自动清理，但这不影响 s3 的有效性（只要 s 在 s3 使用期间存活）  
    println!("{}", s3); // 输出: world  
}
```
在这个例子中，我们创建了两个String类型的变量s1和s2。当我们将s1的值赋给s2时，Rust通过所有权机制确保了s1不再拥有那个字符串数据，而s2则成为了新的所有者。尝试在转移所有权后使用s1将会导致编译错误，因为Rust的编译器能够确保不会有悬挂指针或双重释放的问题。

接着，我们展示了字符串切片（&str类型），它是对字符串的一个部分视图的引用，但不拥有所引用的数据。字符串切片通过与原字符串共享内存的方式来工作，但它们的生命周期受限于它们所引用的数据。在这个例子中，s3是对s的一个切片，它依赖于s的存在来保持有效。

这些特性共同构成了Rust强大的内存安全机制，使得开发者能够在享受高性能的同时，也能避免常见的内存错误。


rust写的coreutils
https://github.com/uutils/coreutils

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

```
cargo tree
axum-web-app v0.1.0 (D:\git\github\axum-web-app)
|-- ammonia v3.3.0
|   |-- html5ever v0.26.0
|   |   |-- log v0.4.25
|   |   |-- mac v0.1.1
|   |   `-- markup5ever v0.11.0
|   |       |-- log v0.4.25
|   |       |-- phf v0.10.1
|   |       |   `-- phf_shared v0.10.0
|   |       |       `-- siphasher v0.3.11
|   |       |-- string_cache v0.8.8
|   |       |   |-- new_debug_unreachable v1.0.6
|   |       |   |-- parking_lot v0.12.3
|   |       |   |   |-- lock_api v0.4.12
|   |       |   |   |   `-- scopeguard v1.2.0
|   |       |   |   |   [build-dependencies]
|   |       |   |   |   `-- autocfg v1.4.0
|   |       |   |   `-- parking_lot_core v0.9.10
|   |       |   |       |-- cfg-if v1.0.0
|   |       |   |       |-- smallvec v1.13.2
|   |       |   |       `-- windows-targets v0.52.6
|   |       |   |           `-- windows_x86_64_msvc v0.52.6
|   |       |   |-- phf_shared v0.11.3
|   |       |   |   `-- siphasher v1.0.1
|   |       |   |-- precomputed-hash v0.1.1
|   |       |   `-- serde v1.0.217
|   |       |       `-- serde_derive v1.0.217 (proc-macro)
|   |       |           |-- proc-macro2 v1.0.93
|   |       |           |   `-- unicode-ident v1.0.16
|   |       |           |-- quote v1.0.38
|   |       |           |   `-- proc-macro2 v1.0.93 (*)
|   |       |           `-- syn v2.0.98
|   |       |               |-- proc-macro2 v1.0.93 (*)
|   |       |               |-- quote v1.0.38 (*)
|   |       |               `-- unicode-ident v1.0.16
|   |       `-- tendril v0.4.3
|   |           |-- futf v0.1.5
|   |           |   |-- mac v0.1.1
|   |           |   `-- new_debug_unreachable v1.0.6
|   |           |-- mac v0.1.1
|   |           `-- utf-8 v0.7.6
|   |       [build-dependencies]
|   |       |-- phf_codegen v0.10.0
|   |       |   |-- phf_generator v0.10.0
|   |       |   |   |-- phf_shared v0.10.0
|   |       |   |   |   `-- siphasher v0.3.11
|   |       |   |   `-- rand v0.8.5
|   |       |   |       |-- rand_chacha v0.3.1
|   |       |   |       |   |-- ppv-lite86 v0.2.20
|   |       |   |       |   |   `-- zerocopy v0.7.35
|   |       |   |       |   |       |-- byteorder v1.5.0
|   |       |   |       |   |       `-- zerocopy-derive v0.7.35 (proc-macro)
|   |       |   |       |   |           |-- proc-macro2 v1.0.93 (*)
|   |       |   |       |   |           |-- quote v1.0.38 (*)
|   |       |   |       |   |           `-- syn v2.0.98 (*)
|   |       |   |       |   `-- rand_core v0.6.4
|   |       |   |       |       `-- getrandom v0.2.15
|   |       |   |       |           `-- cfg-if v1.0.0
|   |       |   |       `-- rand_core v0.6.4 (*)
|   |       |   `-- phf_shared v0.10.0 (*)
|   |       `-- string_cache_codegen v0.5.3
|   |           |-- phf_generator v0.11.3
|   |           |   |-- phf_shared v0.11.3 (*)
|   |           |   `-- rand v0.8.5 (*)
|   |           |-- phf_shared v0.11.3 (*)
|   |           |-- proc-macro2 v1.0.93 (*)
|   |           `-- quote v1.0.38 (*)
|   |   [build-dependencies]
|   |   |-- proc-macro2 v1.0.93 (*)
|   |   |-- quote v1.0.38 (*)
|   |   `-- syn v1.0.109
|   |       |-- proc-macro2 v1.0.93 (*)
|   |       |-- quote v1.0.38 (*)
|   |       `-- unicode-ident v1.0.16
|   |-- maplit v1.0.2
|   |-- once_cell v1.20.3
|   |-- tendril v0.4.3 (*)
|   `-- url v2.5.4
|       |-- form_urlencoded v1.2.1
|       |   `-- percent-encoding v2.3.1
|       |-- idna v1.0.3
|       |   |-- idna_adapter v1.2.0
|       |   |   |-- icu_normalizer v1.5.0
|       |   |   |   |-- displaydoc v0.2.5 (proc-macro)
|       |   |   |   |   |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |   |-- quote v1.0.38 (*)
|       |   |   |   |   `-- syn v2.0.98 (*)
|       |   |   |   |-- icu_collections v1.5.0
|       |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |-- yoke v0.7.5
|       |   |   |   |   |   |-- stable_deref_trait v1.2.0
|       |   |   |   |   |   |-- yoke-derive v0.7.5 (proc-macro)
|       |   |   |   |   |   |   |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |   |   |   |-- quote v1.0.38 (*)
|       |   |   |   |   |   |   |-- syn v2.0.98 (*)
|       |   |   |   |   |   |   `-- synstructure v0.13.1
|       |   |   |   |   |   |       |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |   |   |       |-- quote v1.0.38 (*)
|       |   |   |   |   |   |       `-- syn v2.0.98 (*)
|       |   |   |   |   |   `-- zerofrom v0.1.5
|       |   |   |   |   |       `-- zerofrom-derive v0.1.5 (proc-macro)
|       |   |   |   |   |           |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |   |           |-- quote v1.0.38 (*)
|       |   |   |   |   |           |-- syn v2.0.98 (*)
|       |   |   |   |   |           `-- synstructure v0.13.1 (*)
|       |   |   |   |   |-- zerofrom v0.1.5 (*)
|       |   |   |   |   `-- zerovec v0.10.4
|       |   |   |   |       |-- yoke v0.7.5 (*)
|       |   |   |   |       |-- zerofrom v0.1.5 (*)
|       |   |   |   |       `-- zerovec-derive v0.10.3 (proc-macro)
|       |   |   |   |           |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |           |-- quote v1.0.38 (*)
|       |   |   |   |           `-- syn v2.0.98 (*)
|       |   |   |   |-- icu_normalizer_data v1.5.0
|       |   |   |   |-- icu_properties v1.5.1
|       |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |-- icu_collections v1.5.0 (*)
|       |   |   |   |   |-- icu_locid_transform v1.5.0
|       |   |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |   |-- icu_locid v1.5.0
|       |   |   |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |   |   |-- litemap v0.7.4
|       |   |   |   |   |   |   |-- tinystr v0.7.6
|       |   |   |   |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   |   |   |   |   |-- writeable v0.5.5
|       |   |   |   |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   |   |   |   |-- icu_locid_transform_data v1.5.0
|       |   |   |   |   |   |-- icu_provider v1.5.0
|       |   |   |   |   |   |   |-- displaydoc v0.2.5 (proc-macro) (*)
|       |   |   |   |   |   |   |-- icu_locid v1.5.0 (*)
|       |   |   |   |   |   |   |-- icu_provider_macros v1.5.0 (proc-macro)
|       |   |   |   |   |   |   |   |-- proc-macro2 v1.0.93 (*)
|       |   |   |   |   |   |   |   |-- quote v1.0.38 (*)
|       |   |   |   |   |   |   |   `-- syn v2.0.98 (*)
|       |   |   |   |   |   |   |-- stable_deref_trait v1.2.0
|       |   |   |   |   |   |   |-- tinystr v0.7.6 (*)
|       |   |   |   |   |   |   |-- writeable v0.5.5
|       |   |   |   |   |   |   |-- yoke v0.7.5 (*)
|       |   |   |   |   |   |   |-- zerofrom v0.1.5 (*)
|       |   |   |   |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   |   |   |   |-- tinystr v0.7.6 (*)
|       |   |   |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   |   |   |-- icu_properties_data v1.5.0
|       |   |   |   |   |-- icu_provider v1.5.0 (*)
|       |   |   |   |   |-- tinystr v0.7.6 (*)
|       |   |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   |   |-- icu_provider v1.5.0 (*)
|       |   |   |   |-- smallvec v1.13.2
|       |   |   |   |-- utf16_iter v1.0.5
|       |   |   |   |-- utf8_iter v1.0.4
|       |   |   |   |-- write16 v1.0.0
|       |   |   |   `-- zerovec v0.10.4 (*)
|       |   |   `-- icu_properties v1.5.1 (*)
|       |   |-- smallvec v1.13.2
|       |   `-- utf8_iter v1.0.4
|       `-- percent-encoding v2.3.1
|-- axum v0.5.17
|   |-- async-trait v0.1.86 (proc-macro)
|   |   |-- proc-macro2 v1.0.93 (*)
|   |   |-- quote v1.0.38 (*)
|   |   `-- syn v2.0.98 (*)
|   |-- axum-core v0.2.9
|   |   |-- async-trait v0.1.86 (proc-macro) (*)
|   |   |-- bytes v1.10.0
|   |   |-- futures-util v0.3.31
|   |   |   |-- futures-core v0.3.31
|   |   |   |-- futures-sink v0.3.31
|   |   |   |-- futures-task v0.3.31
|   |   |   |-- pin-project-lite v0.2.16
|   |   |   `-- pin-utils v0.1.0
|   |   |-- http v0.2.12
|   |   |   |-- bytes v1.10.0
|   |   |   |-- fnv v1.0.7
|   |   |   `-- itoa v1.0.14
|   |   |-- http-body v0.4.6
|   |   |   |-- bytes v1.10.0
|   |   |   |-- http v0.2.12 (*)
|   |   |   `-- pin-project-lite v0.2.16
|   |   |-- mime v0.3.17
|   |   |-- tower-layer v0.3.3
|   |   `-- tower-service v0.3.3
|   |-- bitflags v1.3.2
|   |-- bytes v1.10.0
|   |-- futures-util v0.3.31 (*)
|   |-- http v0.2.12 (*)
|   |-- http-body v0.4.6 (*)
|   |-- hyper v0.14.32
|   |   |-- bytes v1.10.0
|   |   |-- futures-channel v0.3.31
|   |   |   `-- futures-core v0.3.31
|   |   |-- futures-core v0.3.31
|   |   |-- futures-util v0.3.31 (*)
|   |   |-- h2 v0.3.26
|   |   |   |-- bytes v1.10.0
|   |   |   |-- fnv v1.0.7
|   |   |   |-- futures-core v0.3.31
|   |   |   |-- futures-sink v0.3.31
|   |   |   |-- futures-util v0.3.31 (*)
|   |   |   |-- http v0.2.12 (*)
|   |   |   |-- indexmap v2.7.1
|   |   |   |   |-- equivalent v1.0.2
|   |   |   |   `-- hashbrown v0.15.2
|   |   |   |-- slab v0.4.9
|   |   |   |   [build-dependencies]
|   |   |   |   `-- autocfg v1.4.0
|   |   |   |-- tokio v1.43.0
|   |   |   |   |-- bytes v1.10.0
|   |   |   |   |-- mio v1.0.3
|   |   |   |   |   `-- windows-sys v0.52.0
|   |   |   |   |       `-- windows-targets v0.52.6 (*)
|   |   |   |   |-- parking_lot v0.12.3 (*)
|   |   |   |   |-- pin-project-lite v0.2.16
|   |   |   |   |-- socket2 v0.5.8
|   |   |   |   |   `-- windows-sys v0.52.0 (*)
|   |   |   |   |-- tokio-macros v2.5.0 (proc-macro)
|   |   |   |   |   |-- proc-macro2 v1.0.93 (*)
|   |   |   |   |   |-- quote v1.0.38 (*)
|   |   |   |   |   `-- syn v2.0.98 (*)
|   |   |   |   `-- windows-sys v0.52.0 (*)
|   |   |   |-- tokio-util v0.7.13
|   |   |   |   |-- bytes v1.10.0
|   |   |   |   |-- futures-core v0.3.31
|   |   |   |   |-- futures-sink v0.3.31
|   |   |   |   |-- pin-project-lite v0.2.16
|   |   |   |   `-- tokio v1.43.0 (*)
|   |   |   `-- tracing v0.1.41
|   |   |       |-- log v0.4.25
|   |   |       |-- pin-project-lite v0.2.16
|   |   |       |-- tracing-attributes v0.1.28 (proc-macro)
|   |   |       |   |-- proc-macro2 v1.0.93 (*)
|   |   |       |   |-- quote v1.0.38 (*)
|   |   |       |   `-- syn v2.0.98 (*)
|   |   |       `-- tracing-core v0.1.33
|   |   |           `-- once_cell v1.20.3
|   |   |-- http v0.2.12 (*)
|   |   |-- http-body v0.4.6 (*)
|   |   |-- httparse v1.10.0
|   |   |-- httpdate v1.0.3
|   |   |-- itoa v1.0.14
|   |   |-- pin-project-lite v0.2.16
|   |   |-- socket2 v0.5.8 (*)
|   |   |-- tokio v1.43.0 (*)
|   |   |-- tower-service v0.3.3
|   |   |-- tracing v0.1.41 (*)
|   |   `-- want v0.3.1
|   |       `-- try-lock v0.2.5
|   |-- itoa v1.0.14
|   |-- matchit v0.5.0
|   |-- memchr v2.7.4
|   |-- mime v0.3.17
|   |-- percent-encoding v2.3.1
|   |-- pin-project-lite v0.2.16
|   |-- serde v1.0.217 (*)
|   |-- serde_json v1.0.138
|   |   |-- itoa v1.0.14
|   |   |-- memchr v2.7.4
|   |   |-- ryu v1.0.19
|   |   `-- serde v1.0.217 (*)
|   |-- serde_urlencoded v0.7.1
|   |   |-- form_urlencoded v1.2.1 (*)
|   |   |-- itoa v1.0.14
|   |   |-- ryu v1.0.19
|   |   `-- serde v1.0.217 (*)
|   |-- sync_wrapper v0.1.2
|   |-- tokio v1.43.0 (*)
|   |-- tower v0.4.13
|   |   |-- futures-core v0.3.31
|   |   |-- futures-util v0.3.31 (*)
|   |   |-- pin-project v1.1.9
|   |   |   `-- pin-project-internal v1.1.9 (proc-macro)
|   |   |       |-- proc-macro2 v1.0.93 (*)
|   |   |       |-- quote v1.0.38 (*)
|   |   |       `-- syn v2.0.98 (*)
|   |   |-- pin-project-lite v0.2.16
|   |   |-- tokio v1.43.0 (*)
|   |   |-- tower-layer v0.3.3
|   |   |-- tower-service v0.3.3
|   |   `-- tracing v0.1.41 (*)
|   |-- tower-http v0.3.5
|   |   |-- bitflags v1.3.2
|   |   |-- bytes v1.10.0
|   |   |-- futures-core v0.3.31
|   |   |-- futures-util v0.3.31 (*)
|   |   |-- http v0.2.12 (*)
|   |   |-- http-body v0.4.6 (*)
|   |   |-- http-range-header v0.3.1
|   |   |-- pin-project-lite v0.2.16
|   |   |-- tower v0.4.13 (*)
|   |   |-- tower-layer v0.3.3
|   |   `-- tower-service v0.3.3
|   |-- tower-layer v0.3.3
|   `-- tower-service v0.3.3
|-- chrono v0.4.39
|   |-- num-traits v0.2.19
|   |   [build-dependencies]
|   |   `-- autocfg v1.4.0
|   `-- windows-targets v0.52.6 (*)
|-- config v0.11.0
|   |-- lazy_static v1.5.0
|   |-- nom v5.1.3
|   |   |-- lexical-core v0.7.6
|   |   |   |-- arrayvec v0.5.2
|   |   |   |-- bitflags v1.3.2
|   |   |   |-- cfg-if v1.0.0
|   |   |   |-- ryu v1.0.19
|   |   |   `-- static_assertions v1.1.0
|   |   `-- memchr v2.7.4
|   |   [build-dependencies]
|   |   `-- version_check v0.9.5
|   |-- rust-ini v0.13.0
|   |-- serde v1.0.217 (*)
|   |-- serde-hjson v0.9.1
|   |   |-- lazy_static v1.5.0
|   |   |-- num-traits v0.1.43
|   |   |   `-- num-traits v0.2.19 (*)
|   |   |-- regex v1.11.1
|   |   |   |-- aho-corasick v1.1.3
|   |   |   |   `-- memchr v2.7.4
|   |   |   |-- memchr v2.7.4
|   |   |   |-- regex-automata v0.4.9
|   |   |   |   |-- aho-corasick v1.1.3 (*)
|   |   |   |   |-- memchr v2.7.4
|   |   |   |   `-- regex-syntax v0.8.5
|   |   |   `-- regex-syntax v0.8.5
|   |   `-- serde v0.8.23
|   |-- serde_json v1.0.138 (*)
|   |-- toml v0.5.11
|   |   `-- serde v1.0.217 (*)
|   `-- yaml-rust v0.4.5
|       `-- linked-hash-map v0.5.6
|-- redis v0.23.3
|   |-- async-trait v0.1.86 (proc-macro) (*)
|   |-- bytes v1.10.0
|   |-- combine v4.6.7
|   |   |-- bytes v1.10.0
|   |   |-- futures-core v0.3.31
|   |   |-- memchr v2.7.4
|   |   |-- pin-project-lite v0.2.16
|   |   |-- tokio v1.43.0 (*)
|   |   `-- tokio-util v0.7.13 (*)
|   |-- futures-util v0.3.31 (*)
|   |-- itoa v1.0.14
|   |-- percent-encoding v2.3.1
|   |-- pin-project-lite v0.2.16
|   |-- ryu v1.0.19
|   |-- sha1_smol v1.0.1
|   |-- socket2 v0.4.10
|   |   `-- winapi v0.3.9
|   |-- tokio v1.43.0 (*)
|   |-- tokio-util v0.7.13 (*)
|   `-- url v2.5.4 (*)
|-- reqwest v0.11.27
|   |-- base64 v0.21.7
|   |-- bytes v1.10.0
|   |-- encoding_rs v0.8.35
|   |   `-- cfg-if v1.0.0
|   |-- futures-core v0.3.31
|   |-- futures-util v0.3.31 (*)
|   |-- h2 v0.3.26 (*)
|   |-- http v0.2.12 (*)
|   |-- http-body v0.4.6 (*)
|   |-- hyper v0.14.32 (*)
|   |-- hyper-tls v0.5.0
|   |   |-- bytes v1.10.0
|   |   |-- hyper v0.14.32 (*)
|   |   |-- native-tls v0.2.13
|   |   |   `-- schannel v0.1.27
|   |   |       `-- windows-sys v0.59.0
|   |   |           `-- windows-targets v0.52.6 (*)
|   |   |-- tokio v1.43.0 (*)
|   |   `-- tokio-native-tls v0.3.1
|   |       |-- native-tls v0.2.13 (*)
|   |       `-- tokio v1.43.0 (*)
|   |-- ipnet v2.11.0
|   |-- log v0.4.25
|   |-- mime v0.3.17
|   |-- native-tls v0.2.13 (*)
|   |-- once_cell v1.20.3
|   |-- percent-encoding v2.3.1
|   |-- pin-project-lite v0.2.16
|   |-- rustls-pemfile v1.0.4
|   |   `-- base64 v0.21.7
|   |-- serde v1.0.217 (*)
|   |-- serde_json v1.0.138 (*)
|   |-- serde_urlencoded v0.7.1 (*)
|   |-- sync_wrapper v0.1.2
|   |-- tokio v1.43.0 (*)
|   |-- tokio-native-tls v0.3.1 (*)
|   |-- tower-service v0.3.3
|   |-- url v2.5.4 (*)
|   `-- winreg v0.50.0
|       |-- cfg-if v1.0.0
|       `-- windows-sys v0.48.0
|           `-- windows-targets v0.48.5
|               `-- windows_x86_64_msvc v0.48.5
|-- serde v1.0.217 (*)
|-- serde_json v1.0.138 (*)
|-- tokio v1.43.0 (*)
|-- tower v0.4.13 (*)
|-- tower-http v0.3.5 (*)
|-- tracing v0.1.41 (*)
|-- tracing-appender v0.2.3
|   |-- crossbeam-channel v0.5.14
|   |   `-- crossbeam-utils v0.8.21
|   |-- thiserror v1.0.69
|   |   `-- thiserror-impl v1.0.69 (proc-macro)
|   |       |-- proc-macro2 v1.0.93 (*)
|   |       |-- quote v1.0.38 (*)
|   |       `-- syn v2.0.98 (*)
|   |-- time v0.3.37
|   |   |-- deranged v0.3.11
|   |   |   `-- powerfmt v0.2.0
|   |   |-- itoa v1.0.14
|   |   |-- num-conv v0.1.0
|   |   |-- powerfmt v0.2.0
|   |   `-- time-core v0.1.2
|   `-- tracing-subscriber v0.3.19
|       |-- matchers v0.1.0
|       |   `-- regex-automata v0.1.10
|       |       `-- regex-syntax v0.6.29
|       |-- nu-ansi-term v0.46.0
|       |   |-- overload v0.1.1
|       |   `-- winapi v0.3.9
|       |-- once_cell v1.20.3
|       |-- regex v1.11.1 (*)
|       |-- sharded-slab v0.1.7
|       |   `-- lazy_static v1.5.0
|       |-- smallvec v1.13.2
|       |-- thread_local v1.1.8
|       |   |-- cfg-if v1.0.0
|       |   `-- once_cell v1.20.3
|       |-- tracing v0.1.41 (*)
|       |-- tracing-core v0.1.33 (*)
|       `-- tracing-log v0.2.0
|           |-- log v0.4.25
|           |-- once_cell v1.20.3
|           `-- tracing-core v0.1.33 (*)
|-- tracing-subscriber v0.3.19 (*)
`-- uuid v1.13.1
    `-- getrandom v0.3.1
        |-- cfg-if v1.0.0
        `-- windows-targets v0.52.6 (*)
[dev-dependencies]
|-- config v0.11.0 (*)
`-- tokio v1.43.0 (*)
```


