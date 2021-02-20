# grpc
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





2005年开源的

HTTP/2 based RPC
high performance RPC framework


grpc为什么用http2，不用tcp，甚至是quic


grpc与spring
grpc-client-spring-boot-starter
grpc-server-spring-boot-starter

https://blog.csdn.net/qq_25112523/article/details/84889951


[grpctest](bitbucket.org/sandisks/grpctest)



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

