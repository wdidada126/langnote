# thrift

.thrift
https://thrift.apache.org/docs/idl.html

idea maven thrift
https://blog.csdn.net/weixin_38370441/article/details/121007996

protobuf插件 自动下载可执行工具
thirft需要自己下载

滴滴用thrift
benchmark-thrift
thrift-mock
https://github.com/didi/thrift-mock
https://github.com/didi/benchmark-thrift

benchmark-thrift 是一款测试Thrift应用程序性能的工具，开箱即用，高效简单。
thrift-mock 是一款轻量级的 Java 测试工具，用来模拟 thrift 服务。通过它可以轻松的将依赖的 thrift 服务接口进行 mock，获得指定的接口返回，从而极大的提升了联调、测试阶段的开发效率。

Mac vcpkg install thrift

需要flex

bison

yum install flex bison -y

bison 2.3不行，版本太低

java demo
https://github.com/edidada/ThriftRpcDemo.git 

thrift-0.14.0.exe  

Idea Maven 插件

https://blog.csdn.net/u010900754/article/details/80172671

Apache Thrift 小米 谢龙使用

java maven构建
重新构建了下，知道了具体原因，才想起还需要配置thrift.exe windows环境
去官网http://thrift.apache.org/download 下载thrift.exe,然后设置环境变量的 path 变量，把thrift.exe 所在目录加上就行
最后打开cmd 验证是否成功：thrift -version
输出版本号信息代表设置成功
Thrift version 0.9.3
然后重启IDEA开发工具，重新构建就成功了　


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

Apache Thrift 是一个开源的跨语言 RPC (Remote Procedure Call) 框架，支持高效的数据序列化和多种编程语言。下面是一个入门示例，展示如何使用 Thrift 定义一个简单的服务，并在 C++ 中实现和调用该服务。

### 步骤概览

1. 安装 Thrift。
2. 定义 Thrift 接口文件（.thrift 文件）。
3. 生成代码。
4. 编写服务器和客户端代码。
5. 运行服务器和客户端。

### 1. 安装 Thrift

在不同的操作系统上安装 Thrift 的方式可能有所不同。以下是在 Ubuntu 上的安装示例：

```bash
sudo apt-get update
sudo apt-get install thrift-compiler
```

在其他操作系统上，请参考 [Thrift 官方安装文档](https://thrift.apache.org/docs/BuildingFromSource) 进行安装。

### 2. 定义 Thrift 接口文件

创建一个名为 `example.thrift` 的文件，定义一个简单的计算服务：

```thrift
namespace cpp example

service Calculator {
  i32 add(1: i32 num1, 2: i32 num2),
  i32 subtract(1: i32 num1, 2: i32 num2)
}
```

### 3. 生成代码

使用 Thrift 编译器生成 C++ 代码：

```bash
thrift --gen cpp example.thrift
```

这会生成 `gen-cpp` 目录，包含以下文件：
- `example_types.h` 和 `example_types.cpp`
- `example_constants.h` 和 `example_constants.cpp`
- `Calculator.h` 和 `Calculator.cpp`

### 4. 编写服务器和客户端代码

#### 服务器代码 (`server.cpp`)

```cpp
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TServer.h>
#include <thrift/server/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include "gen-cpp/Calculator.h"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::server;
using namespace ::apache::thrift::transport;

class CalculatorHandler : public CalculatorIf {
public:
  CalculatorHandler() {}

  int32_t add(const int32_t num1, const int32_t num2) override {
    return num1 + num2;
  }

  int32_t subtract(const int32_t num1, const int32_t num2) override {
    return num1 - num2;
  }
};

int main() {
  int port = 9090;
  ::std::shared_ptr<CalculatorHandler> handler(new CalculatorHandler());
  ::std::shared_ptr<TProcessor> processor(new CalculatorProcessor(handler));
  ::std::shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  ::std::shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  ::std::shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}
```

#### 客户端代码 (`client.cpp`)

```cpp
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include "gen-cpp/Calculator.h"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;

int main() {
  ::std::shared_ptr<TTransport> socket(new TSocket("localhost", 9090));
  ::std::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
  ::std::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
  CalculatorClient client(protocol);

  try {
    transport->open();
    int32_t sum = client.add(1, 1);
    printf("1 + 1 = %d\n", sum);
    int32_t difference = client.subtract(5, 3);
    printf("5 - 3 = %d\n", difference);
    transport->close();
  } catch (TException& tx) {
    printf("ERROR: %s\n", tx.what());
  }

  return 0;
}
```

### 5. 运行服务器和客户端

首先，编译服务器和客户端代码：

```bash
g++ -std=c++11 -o server server.cpp gen-cpp/Calculator.cpp gen-cpp/example_constants.cpp gen-cpp/example_types.cpp -lthrift
g++ -std=c++11 -o client client.cpp gen-cpp/Calculator.cpp gen-cpp/example_constants.cpp gen-cpp/example_types.cpp -lthrift
```

然后，启动服务器：

```bash
./server
```

在另一个终端窗口中，运行客户端：

```bash
./client
```

你应该会看到以下输出：

```
1 + 1 = 2
5 - 3 = 2
```

### 参考资料

- [Apache Thrift 官方文档](https://thrift.apache.org/docs/)
- [Thrift GitHub 仓库](https://github.com/apache/thrift)

