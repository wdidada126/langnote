# protoc

要使用 `protoc` 命令生成 `auth.grpc.pb.cc` 文件，通常需要通过以下步骤来实现：

1. 安装 `protoc` 和 gRPC 插件:
   - 确保已安装 Protocol Buffers 编译器（`protoc`）和 gRPC 插件。
   - 安装方式（根据你的操作系统选择）：
     - Linux:
       ```bash
       sudo apt-get install -y protobuf-compiler
       ```
     - macOS:
       ```bash
       brew install protobuf
       brew install grpc
       ```
     - Windows: 可以通过下载预编译的二进制文件来安装。

2. 命令行生成 `.cc` 文件:
   - 使用以下命令生成 `auth.grpc.pb.cc` 和 `auth.grpc.pb.h` 文件：
     ```bash
     protoc --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` auth.proto
     ```

3. 生成 `.pb.cc` 和 `.pb.h` 文件:
   - 你通常还需要生成 Protocol Buffers 的 `.cc` 和 `.h` 文件，使用以下命令：
     ```bash
     protoc --cpp_out=. auth.proto
     ```

### 整合命令
可以将上述步骤整合为一个命令，一次性生成所有需要的文件：
```bash
protoc --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` auth.proto
```

### 解释：
- `--cpp_out=.`: 指定生成 `.pb.cc` 和 `.pb.h` 文件的输出目录（当前目录）。
- `--grpc_out=.`: 指定生成 gRPC 代码的输出目录（当前目录）。
- `--plugin=protoc-gen-grpc=`which grpc_cpp_plugin``: 告诉 `protoc` 使用 gRPC 插件来生成 gRPC 代码。

执行上述命令后，你应该会在当前目录下看到生成的 `auth.pb.cc`、`auth.pb.h`、`auth.grpc.pb.cc` 和 `auth.grpc.pb.h` 文件。




