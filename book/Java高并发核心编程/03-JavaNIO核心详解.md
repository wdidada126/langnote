# 第 3 章 Java NIO 核心详解（卷1）

> `Buffer`/`Channel`/`Selector` 三件套、`ByteBuffer` 读写模式、直接缓冲区（`DirectByteBuffer`）、`epoll` 多路复用、 SelectionKey 事件。本书把 JDK NIO 与底层 `epoll` 打通，其他并发书多略过。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| Buffer | capacity/limit/position/mark |
| Channel | SocketChannel/ServerSocketChannel |
| Selector | 多路复用、SelectionKey 事件 |
| 直接缓冲 | DirectByteBuffer（堆外，零拷贝友好） |

## 二、核心精讲

### 2.1 🔧 `ByteBuffer` 读写模式切换
- `flip()` 切读（limit=position, position=0）；`clear()`/`compact()` 切写（🔧 `compact` 保留未读数据，断连重发场景用；`clear` 清空重来）。

### 2.2 直接缓冲区
- `ByteBuffer.allocateDirect` 在堆外（不受 GC 管理、零拷贝友好），但分配/回收贵（🔧 Netty `PooledByteBuf` 池化直接内存；注意 `-XX:MaxDirectMemorySize` 上限 + 监控，避免堆外 OOM）。

### 2.3 Selector 与 epoll
- 一个 `Selector` 监视多 fd；Linux 底层 `epoll`（`EPOLLIN/EPOLLOUT`），`selectedKeys` 是「就绪集合」非「全部」（🔧 JDK NIO 的 `epoll` 空转 bug（JDK 6/早期7）曾用 `Selector.wakeup` 重建规避，JDK 8+ 已修）。

## 三、版本演进 / 论文 / 前沿

- 论文/文献：`epoll` (Linux 2.6)、`kqueue`(BSD)；JDK 1.4 引入 NIO。
- 工业界：Netty 在 NIO 之上封装（规避 JDK NIO API 繁琐 + bug）；Grizzly（GlassFish）。
- 开源 stars（2026-09）：netty 34k / tomcat 8k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "NIO 直接缓冲随便用" | 堆外 OOM；要池化 |
| 2 | "flip/clear 混淆" | 断点续传用 compact |
| 3 | "Selector 监视全部 key" | 只返回就绪的 |
| 4 | "手搓 NIO 服务" | 用 Netty，别造轮子 |
