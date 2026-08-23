# liburing

### liburing库简介

liburing是一个开源的C语言库（也有Python绑定），它为Linux内核的io_uring（一个高效的异步I/O接口）提供用户空间的辅助工具和简化接口。io_uring是 Linux内核（从 5.1 版本起引入）的一个高性能异步I/O框架，旨在减少系统调用开销，支持批量提交和完成操作，特别适合高并发场景如网络服务器、文件系统和数据库。

#### 主要功能与优势
- 核心作用：
  - 帮助开发者设置和拆除 io_uring 实例（setup/teardown）。
  - 提供简化的 API，避免直接处理复杂的内核接口（如 ring buffer 管理）。
  - 支持缓冲 I/O（buffered）和直接 I/O（O_DIRECT），适用于文件、网络等 I/O 操作。
- 优势：
  - 高性能：相比传统 epoll 或 select，io_uring 可减少 90%+ 的系统调用，支持零拷贝和多路复用。
  - 易用性：隐藏底层细节，适合不熟悉内核的开发者；包含回归测试套件，用于验证内核 io_uring 支持。
  - 兼容性：不绑定特定内核版本（支持 5.11 及更早），但最佳在 5.17+ 内核上运行。
- 适用场景：高吞吐服务器（如 Nginx 替代）、数据库（如 RocksDB 集成）、文件系统（如 3FS 项目中用于异步存储）。
- 限制：仅限 Linux；需要内核支持 io_uring（export 模块）。

#### GitHub 地址
- 官方仓库：https://github.com/axboe/liburing
  - 作者：Jens Axboe（Linux 内核 io_uring 主要开发者）。
  - 星标：超过 2.5k。
  - 最新版本：2.6（2024 年更新），支持更多测试和绑定。
  - 安装示例：`git clone https://github.com/axboe/liburing && cd liburing && make && sudo make install`。

#### 其他资源
- Python 绑定：https://pypi.org/project/liburing/（Cython 包装，便于 Python 开发者）。
- 文档：仓库 README 及 https://unixism.net/loti/tutorial/（教程）。
- 内核背景：io_uring 论文 https://kernel.dk/io_uring.pdf。

CMake 集成 liburing

在你的 `CMakeLists.txt` 中，你可以像这样查找并链接 `liburing` 库。一个通用的查找脚本可以长这样：

```cmake
# 在你的 CMakeLists.txt 中
find_package(LibUring REQUIRED)

# 链接到你的目标
target_link_libraries(your_target PRIVATE ${LIBURING_LIBRARIES})
target_include_directories(your_target PRIVATE ${LIBURING_INCLUDE_DIRS})
```
