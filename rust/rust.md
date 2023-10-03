# rust

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

[awesome-rust]( https://github.com/rust-unofficial/awesome-rust)

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
