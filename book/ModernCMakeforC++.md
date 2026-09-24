# Modern CMake for C++

https://book.douban.com/subject/37000914/

作者: Rafał Świdziński
出版社: Packt Publishing
副标题: Effortlessly build cutting-edge C++ code and deliver high-quality solutions
出版年: 2024-5-28
页数: 502
定价: USD 51.86
装帧: 平装
ISBN: 9781805121800

内容比较新 (2024 年中) 偏向实用，适合入门有个全局基本概念； cons: 对 cmake 自身进行扩展讲的比较浅，对大型项目来说还是差点意思 

这本书是在Amazon上看到的，然后有豆友找我说想让我翻译这本书，所以想办法找到了这本书的电子版。
这本书和之前译的《 CMake Best Practices 》《CMake Cookbook》，《  Professional CMake 》不同。
这本书更加注重于项目内部的种种事情，并且对一些软件工程的原则和C++都有介绍。并且，对于在其他书中都大书特书的 超级构建 ，这本书的作者认为这是没有必要的，这种观点可能是想让相应的工程更加的纯粹，而不需要被各种所使用到的其他库所污染。可以看出作者是一个非常追求优雅的人。

中文翻译
https://github.com/xiaoweiChen/Modern-CMake-for-Cpp/releases

Modern-CMake-for-C++.pdf

## source code

https://github.com/PacktPublishing/Modern-CMake-for-Cpp

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2024-01
> 一些构建工具的发展，为C/C++的代码复用引入了更好的方式。例如CMake从3.0版本开始被称之为“Modern CMake”，是因为它引入了target的概念，以及基于target建立起了构建的依赖可见性和传播控制机制。这些都更好的支持了代码在构建上的模块化，号称“everything is a (self-contained) target”。另外，借助CMake的ExternalProject和find_package特性，使得我们可以从指定的http或者git分支下载、构建、安装和引用代码库。由于CMake的广泛流行，目前这已经成为C/C++开源社区的事实标准。关于Modern CMake的用法和最佳实践，可以看看这篇文章：《Modern CMake最佳实践》。

