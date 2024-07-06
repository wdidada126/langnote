# grpc

最近在研究gRPC,主要想用他来替代传统的HTTP通讯，以提升server间的通讯效率，中间也接触到了JSON-RPC，都有现成的库做支持，但考虑到最后，还是决定用gRPC，主要还是行业内，他还是主流，虽然有些学习成本，但熟悉之后倒还好，其他的方案毕竟没有接触过，不知道会遇到什么坑。

https://github.com/grpc/grpc/

https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protobuf-cpp-3.19.4.zip

windows
vcpkg install grpc
1.48.0

grpc命名空间详解

https://grpc.github.io/grpc/cpp/dir_9da1417219d37d29f30953e77a197f19.html


头文件
https://grpc.github.io/grpc/cpp/files.html

protobuf传输协议

云原生大量使用


```shell
ls /root/vcpkg/installed/x64-linux/tools/grpc
grpc_cpp_plugin  grpc_csharp_plugin  grpc_node_plugin  grpc_objective_c_plugin  grpc_php_plugin  grpc_python_plugin  grpc_ruby_plugin
```

```shell
/root/vcpkg/packages/protobuf_x64-linux/tools/protobuf/protoc --version
libprotoc 3.10.0
```

```shell
ls /root/vcpkg/packages/grpc_x64-linux/lib
libaddress_sorting.a  libgrpc.a    libgrpc_cronet.a       libgrpc++_error_details.a  libgrpcpp_channelz.a    libgrpc_unsecure.a
libgpr.a              libgrpc++.a  libgrpc_csharp_ext.so  libgrpc_plugin_support.a   libgrpc++_reflection.a  libgrpc++_unsecure.a
```

```shell
find_package(gRPC CONFIG REQUIRED)
    # Note: 8 target(s) were omitted.
    target_link_libraries(main PRIVATE gRPC::gpr gRPC::grpc gRPC::grpc++ gRPC::grpc_cronet)
```

vcpkg install grpc

Feb 26, 2015年开源的
Feb 26, 2015 -> release-0_5_0
Apr 8, 2015 -> release-0_6_0
https://github.com/grpc/grpc/releases?page=28


HTTP/2 based RPC
high performance RPC framework


grpc为什么用http2，不用tcp，甚至是quic
go也支持http2

grpc与spring
grpc-client-spring-boot-starter
grpc-server-spring-boot-starter

[springboot 集成 grpc 和 protobuf（二） | 在实际项目中使用 grpc 和 protobuf](https://blog.csdn.net/qq_25112523/article/details/84889951)


- [grpctest example](bitbucket.org/sandisks/grpctest)
- [spring grpc java](https://github.com/edidada/grpc-springboot-lin)
- [grpc-cpp-vcpkg](https://gitee.com/edidada/grpc-cpp-vcpkg)
- [testcppgrcpconan](https://gitee.com/edidada/testcppgrcpconan)

gprc java go c++互相调用



https://www.grpc.io/docs/quickstart/cpp/

```sh
export MY_INSTALL_DIR=$HOME/.local
mkdir -p $MY_INSTALL_DIR
export PATH="$PATH:$MY_INSTALL_DIR/bin"
cmake --version
sudo apt install -y build-essential autoconf libtool pkg-config
git clone --recurse-submodules -b v1.28.1 https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build
cd cmake/build
cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
      ../..
make -j
make install
```

cmake 加参数DBUILD_SHARED_LIBS=ON



```sh
cd examples/cpp/helloworld
mkdir -p cmake/build
cmake -DCMAKE_PREFIX_PATH=$MY_INSTALL_DIR ../..
```

20200525不行，换travis去编译

编译让ci/cd工具去

## api doc

### java

https://grpc.io/docs/what-is-grpc/core-concepts/


For detailed information about the gRPC C++ API, including tutorials, best practices, and reference material, you can visit the official gRPC documentation. Here are some useful links:

1. [gRPC C++ API Reference](https://grpc.io/docs/languages/cpp/): This section provides comprehensive details about the gRPC API for C++, including various tutorials and best practices.
2. [gRPC C++ Quick Start](https://grpc.io/docs/languages/cpp/quickstart/): A guide to quickly get started with gRPC in C++.
3. [gRPC C++ Tutorials](https://grpc.io/docs/languages/cpp/basics/): Tutorials covering the basics and advanced topics in gRPC for C++.
4. [gRPC Best Practices for C++](https://grpc.io/docs/languages/cpp/best-practices/): Recommendations for using gRPC effectively in C++ applications.

These resources will help you understand how to implement and use gRPC in your C++ projects.

https://grpc.io/docs/languages/cpp/


https://grpc.github.io/grpc/cpp/

### grpc java
https://grpc.github.io/grpc-java/javadoc/

### grpc go

https://grpc.io/docs/languages/go/api/
