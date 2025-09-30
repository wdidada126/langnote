# proactor

Proactor 模式，也称为异步 I/O 模型，与传统的 Reactor 模式不同，它依赖于操作系统能够执行 I/O 操作并在操作完成后通知应用程序的能力。这意味着操作系统需要支持真正的异步 I/O 机制，而不仅仅是基于轮询的非阻塞 I/O。

以下是几种主要的操作系统及其对 Proactor 模式的支持情况：

### 1. Windows 操作系统
- IO Completion Ports (IOCP): Windows 提供了 IOCP，这是一种非常高效的异步 I/O 处理机制，非常适合实现 Proactor 模式。通过使用 IOCP，应用程序可以发起多个 I/O 操作，并在这些操作完成时得到通知，而不需要不断地检查 I/O 的状态。
  
### 2. Linux 操作系统

- Linux AIO: Linux 提供了 `libaio` 库来支持异步 I/O，但它的功能有限，尤其对于网络 I/O 并不完全支持。Linux 上的 AIO 更多的是针对文件系统的操作而非网络 I/O。
- epoll 和 io_uring: 尽管不是传统意义上的 Proactor 实现，但是像 `epoll` 和较新的 `io_uring`（从 Linux 5.1 开始引入）提供了更高效的方式来处理大量并发连接和 I/O 请求。特别是 `io_uring`，它旨在提供一种更加灵活和强大的异步 I/O 解决方案，可以看作是对传统 Linux AIO 的改进和发展，尽管它并不完全等同于 Proactor 模式。

### 3. FreeBSD 和其他类 Unix 系统

- 这些系统通常不直接支持 Proactor 模式的异步 I/O，而是更多地依赖于类似于 Linux 的解决方案，如 kqueue（对于 FreeBSD）。kqueue 提供了一种事件驱动的通知机制，但它并不是为异步 I/O 设计的，而是用于监视多个文件描述符的状态变化。

### 总结

- 最佳支持: Windows 是最典型的支持 Proactor 模式的操作系统，通过 IOCP 提供了原生的异步 I/O 支持。
- 部分支持: 在 Linux 上，虽然有 `libaio` 和 `io_uring`，但它们的应用场景和效果与 Windows 的 IOCP 不同，特别是在网络 I/O 方面。
- 有限或无直接支持: 其他类 Unix 系统，如 FreeBSD，虽然有高效的事件通知机制（如 kqueue），但并不直接支持 Proactor 模式的异步 I/O。

因此，在选择技术栈时，如果您的应用需要利用 Proactor 模式提供的优势（比如高效率的异步 I/O 处理），并且主要运行环境是 Windows，则可以充分利用其 IOCP 功能；而在 Linux 或其他类 Unix 系统上，可能需要考虑采用其他优化策略或者接受一定的局限性。


以下是 Windows IOCP（I/O Completion Ports） 实现 Proactor 模式 的完整代码示例，包含关键步骤和详细注释。IOCP 是 Windows 下高性能异步 I/O 的核心机制，天然支持 Proactor 模式。

1. 核心概念

• Proactor 模式：由操作系统完成 I/O 操作（如读写数据），应用只需处理完成事件。

• IOCP 工作流程：

  1. 创建 I/O 完成端口（CreateIoCompletionPort）。
  2. 将文件句柄（如 Socket）绑定到完成端口。
  3. 发起异步 I/O 操作（如 WSARecv）。
  4. 工作线程通过 GetQueuedCompletionStatus 等待 I/O 完成通知。

2. 完整代码示例（C++）

#include <WinSock2.h>
#include <MSWSock.h>
#include <Windows.h>
#include <iostream>
#pragma comment(lib, "Ws2_32.lib")

#define BUFFER_SIZE 4096

// 自定义的I/O操作上下文结构体
struct IOContext {
    OVERLAPPED overlapped;  // 必须作为第一个成员
    SOCKET socket;
    WSABUF wsaBuf;          // 数据缓冲区
    char buffer[BUFFER_SIZE];
    DWORD bytesTransferred; // 实际传输的字节数
    DWORD flags;            // WSARecv的标志位
};

// 工作线程函数（处理I/O完成事件）
DWORD WINAPI WorkerThread(LPVOID lpParam) {
    HANDLE completionPort = (HANDLE)lpParam;
    IOContext* ioContext = nullptr;
    DWORD bytesTransferred = 0;
    ULONG_PTR completionKey = 0;

    while (true) {
        // 等待I/O操作完成
        BOOL status = GetQueuedCompletionStatus(
            completionPort,
            &bytesTransferred,
            &completionKey,
            (LPOVERLAPPED*)&ioContext,
            INFINITE
        );

        if (!status) {
            DWORD error = GetLastError();
            if (error != ERROR_OPERATION_ABORTED) {
                std::cerr << "GetQueuedCompletionStatus failed: " << error << std::endl;
            }
            continue;
        }

        // 处理完成事件
        if (bytesTransferred == 0) {
            // 连接关闭
            closesocket(ioContext->socket);
            delete ioContext;
            continue;
        }

        // 示例：回显数据
        std::cout << "Received: " << ioContext->buffer << std::endl;
        WSABUF wsaBuf = { bytesTransferred, ioContext->buffer };
        DWORD sendBytes = 0;
        WSASend(ioContext->socket, &wsaBuf, 1, &sendBytes, 0, &ioContext->overlapped, nullptr);
    }
    return 0;
}

int main() {
    // 初始化Winsock
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    // 1. 创建I/O完成端口
    HANDLE completionPort = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, 0, 0);
    if (!completionPort) {
        std::cerr << "CreateIoCompletionPort failed: " << GetLastError() << std::endl;
        return 1;
    }

    // 2. 创建工作线程（通常为CPU核心数*2）
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    for (DWORD i = 0; i < sysInfo.dwNumberOfProcessors * 2; i++) {
        CreateThread(NULL, 0, WorkerThread, completionPort, 0, NULL);
    }

    // 3. 创建监听Socket
    SOCKET listenSocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, WSA_FLAG_OVERLAPPED);
    sockaddr_in serverAddr = { 0 };
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_port = htons(8080);
    bind(listenSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    listen(listenSocket, SOMAXCONN);

    std::cout << "Server started on port 8080..." << std::endl;

    while (true) {
        // 4. 接受新连接
        SOCKET clientSocket = accept(listenSocket, NULL, NULL);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "accept failed: " << WSAGetLastError() << std::endl;
            continue;
        }

        // 5. 将Socket绑定到完成端口
        CreateIoCompletionPort((HANDLE)clientSocket, completionPort, (ULONG_PTR)clientSocket, 0);

        // 6. 发起异步读操作
        IOContext* ioContext = new IOContext();
        ZeroMemory(&ioContext->overlapped, sizeof(OVERLAPPED));
        ioContext->socket = clientSocket;
        ioContext->wsaBuf.buf = ioContext->buffer;
        ioContext->wsaBuf.len = BUFFER_SIZE;
        ioContext->bytesTransferred = 0;
        ioContext->flags = 0;

        DWORD bytesRead = 0;
        int result = WSARecv(
            clientSocket,
            &ioContext->wsaBuf,
            1,
            &bytesRead,
            &ioContext->flags,
            &ioContext->overlapped,
            NULL
        );

        if (result == SOCKET_ERROR && WSAGetLastError() != WSA_IO_PENDING) {
            std::cerr << "WSARecv failed: " << WSAGetLastError() << std::endl;
            delete ioContext;
            closesocket(clientSocket);
        }
    }

    // 清理（实际应用中需处理退出逻辑）
    closesocket(listenSocket);
    CloseHandle(completionPort);
    WSACleanup();
    return 0;
}


3. 关键代码解析

1. I/O 完成端口创建：
   HANDLE completionPort = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, 0, 0);
   

2. 绑定 Socket 到完成端口：
   CreateIoCompletionPort((HANDLE)clientSocket, completionPort, (ULONG_PTR)clientSocket, 0);
   

3. 异步 I/O 操作：
   WSARecv(clientSocket, &ioContext->wsaBuf, 1, &bytesRead, &ioContext->flags, &ioContext->overlapped, NULL);
   

4. 事件处理线程：
   GetQueuedCompletionStatus(completionPort, &bytesTransferred, &completionKey, (LPOVERLAPPED*)&ioContext, INFINITE);
   

4. Proactor 模式 vs. Reactor 模式

特性 Proactor (IOCP) Reactor (epoll/kqueue)

I/O 操作执行者 操作系统内核 应用程序

编程复杂度 高（需管理OVERLAPPED结构） 低（事件就绪后应用自己读写）

适用平台 Windows Linux/macOS

性能 高（零拷贝支持） 高（依赖应用实现）

5. 扩展优化建议

1. 内存池：预分配 IOContext 对象避免频繁 new/delete。
2. 线程池：动态调整工作线程数量（如使用 ThreadPool API）。
3. 错误处理：检查 GetQueuedCompletionStatus 返回的错误码（如 ERROR_NETNAME_DELETED）。

6. 参考文档

• Microsoft Docs: https://learn.microsoft.com/en-us/windows/win32/fileio/i-o-completion-ports

• 《Windows核心编程》第10章（异步I/O与完成端口）

通过此代码，你可以快速理解 Windows 下 Proactor 模式的实现原理，并扩展到实际项目（如高性能服务器开发）。
