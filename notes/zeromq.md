# zeromq

https://zeromq.org/

https://github.com/zeromq

https://github.com/zeromq/jeromq
Pure Java ZeroMQ


https://github.com/zeromq/cppzmq
Header-only C++ binding for libzmq



要在 Ubuntu 22.04 上安装 ZeroMQ（`zmq.hpp` 头文件），可以按照以下步骤进行：

### 使用 `apt` 包管理器安装 ZeroMQ

1. **更新软件包列表**：

   在终端中执行以下命令来更新本地软件包列表：

   ```bash
   sudo apt update
   ```

2. **安装 ZeroMQ 库和开发文件**：

   安装 ZeroMQ 的库文件和开发文件，包括 `zmq.hpp` 头文件：

   ```bash
   sudo apt install libzmq3-dev
   ```

   这条命令会安装 ZeroMQ 库的开发包，包括 `zmq.hpp` 头文件和编译所需的其他文件。

### 验证安装

安装完成后，你可以验证 ZeroMQ 是否成功安装。可以通过以下命令查看安装的版本：

```bash
dpkg -s libzmq3-dev | grep Version
```

如果安装成功，会显示安装的版本号。

### 注意事项

- 如果你的 Ubuntu 22.04 系统已经添加了非默认的软件源或者自定义了软件源列表，可能需要先更新软件源信息（`sudo apt update`）来确保能够找到并安装 `libzmq3-dev`。
- 如果你需要使用 CMake 进行编译，安装了 `libzmq3-dev` 后，CMake 可以自动找到并配置 ZeroMQ 库的位置。

按照上述步骤安装 ZeroMQ 库和头文件后，你应该可以在编程时包含 `<zmq.hpp>` 头文件并使用 ZeroMQ 库了。
