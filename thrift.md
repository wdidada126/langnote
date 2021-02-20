# thrift



Idea Maven 插件

https://blog.csdn.net/u010900754/article/details/80172671





Apache Thrift 小米 谢龙使用





.thrift文件
.thrift语法

thrift支持Rust了

generator代码的

github.com/edidada/thrifttest

facebook
The Apache Thrift software framework, for scalable cross-language services development, combines a software stack with a code generation engine to build services that work efficiently and seamlessly between C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml and Delphi and other languages.

Apache Thrift v0.13.0

[thrift官网](https://thrift.apache.org/)

<dependency>
  <groupId>org.apache.thrift</groupId>
  <artifactId>libthrift</artifactId>
  <version>0.13.0</version>
</dependency>

[thrift repo](https://github.com/apache/thrift)


```shell
vcpkg install thrift
Your feedback is important to improve Vcpkg! Please take 3 minutes to complete our survey by running: vcpkg contact --survey
The following packages will be built and installed:
    thrift[core]:x64-osx
Starting package 1/1: thrift:x64-osx
Building package thrift[core]:x64-osx...
-- Using cached /Users/ibqo/vcpkg/downloads/apache-thrift-acdd4226c210336e9e15eb812e5932a645fcd5ce.tar.gz
-- Using source at /Users/ibqo/vcpkg/buildtrees/thrift/src/a645fcd5ce-616856a2c8
-- Configuring x64-osx-dbg
-- Configuring x64-osx-rel
-- Building x64-osx-dbg
CMake Error at scripts/cmake/vcpkg_execute_build_process.cmake:136 (message):
    Command failed: /Users/ibqo/vcpkg/downloads/tools/cmake-3.14.0-osx/cmake-3.14.0-Darwin-x86_64/CMake.app/Contents/bin/cmake --build . --config Debug --target install -- -v
    Working Directory: /Users/ibqo/vcpkg/buildtrees/thrift/x64-osx-dbg
    See logs for more information:
      /Users/ibqo/vcpkg/buildtrees/thrift/install-x64-osx-dbg-out.log

Call Stack (most recent call first):
  scripts/cmake/vcpkg_build_cmake.cmake:91 (vcpkg_execute_build_process)
  scripts/cmake/vcpkg_install_cmake.cmake:24 (vcpkg_build_cmake)
  ports/thrift/portfile.cmake:45 (vcpkg_install_cmake)
  scripts/ports.cmake:94 (include)


Error: Building package thrift:x64-osx failed with: BUILD_FAILED
Please ensure you're using the latest portfiles with `.\vcpkg update`, then
submit an issue at https://github.com/Microsoft/vcpkg/issues including:
  Package: thrift:x64-osx
  Vcpkg version: 2019.09.12-unknownhash

Additionally, attach any relevant sections from the log files above.
```


thrifty.yy:1.7-14: syntax error, unexpected identifier



.yy

Thrift使用了开源的flex和Bison进行词法语法分析（具体见thrift.ll和thrift.yy）

Thrift 框架介绍
http://blog.sina.com.cn/s/blog_72995dcc0101gn82.html


c++ 之 std::move 原理实现与用法总结
https://blog.csdn.net/p942005405/article/details/84644069
