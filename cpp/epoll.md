# epoll

epoll API 是 Linux 系统特有的一个接口，用于高效地处理大量并发网络连接中的 I/O 事件。它允许开发者监控多个文件描述符（通常是套接字），以查看是否有 I/O 操作（如读、写、异常等）可以进行。以下是 epoll API 的详细解析：

一、epoll 的基本概念
epoll 实例：通过 epoll_create 或 epoll_create1 创建的，对应于内核中的一个数据结构，用于管理监控的文件描述符集合。
兴趣列表（Interest List）：内核中用于存储用户注册的要监控的文件描述符集。
就绪列表（Ready List）：内核中用于存储已经准备好进行 I/O 操作的文件描述符集合，它是兴趣列表的子集。
二、epoll 的工作模式
epoll 支持两种工作模式：

水平触发（Level Triggered, LT）：默认模式。只要某个文件描述符处于就绪状态，每次调用 epoll_wait 都会报告该事件。
边缘触发（Edge Triggered, ET）：仅当文件描述符状态发生改变时才触发事件，避免了不必要的重复唤醒。
三、epoll 的主要 API
epoll_create(int size)
创建一个新的 epoll 实例。
参数 size 在 Linux 内核 2.6.8 及以后版本中已被弃用，但仍需传入一个大于 0 的值以保持兼容性。
返回值：成功时返回新的 epoll 文件描述符，失败时返回 -1 并设置 errno。
epoll_create1(int flags)
是 epoll_create 的扩展，提供了更多的控制选项。
参数 flags 可以是 EPOLL_CLOEXEC（创建的文件描述符在 exec 后会关闭）等。
返回值与 epoll_create 相同。
*epoll_ctl(int epfd, int op, int fd, struct epoll_event event)
控制 epoll 实例上的文件描述符。
epfd 是 epoll 文件描述符。
op 是操作类型，包括 EPOLL_CTL_ADD（添加文件描述符）、EPOLL_CTL_MOD（修改文件描述符的监听事件）、EPOLL_CTL_DEL（删除文件描述符）。
fd 是要操作的文件描述符。
event 是指向 epoll_event 结构体的指针，用于指定感兴趣的事件类型和附加数据。
返回值：成功时返回 0，失败时返回 -1 并设置 errno。
*epoll_wait(int epfd, struct epoll_event events, int maxevents, int timeout)
等待 epoll 实例上的事件。
epfd 是 epoll 文件描述符。
events 是用于存储发生事件的 epoll_event 结构体数组。
maxevents 是 events 数组的最大长度。
timeout 是等待时间（毫秒），-1 表示无限期等待，0 表示立即返回。
返回值：成功时返回发生事件的数量，可能为 0（无事件发生且超时未到）或 -1（发生错误）。
四、epoll_event 结构体
epoll_event 结构体用于定义感兴趣的事件类型和对应的文件描述符，其定义如下：

c
struct epoll_event {  
    uint32_t  events;   /* Epoll events */  
    epoll_data_t data;  /* User data variable */  
};  
  
union epoll_data {  
    void        *ptr;  
    int          fd;  
    uint32_t     u32;  
    uint64_t     u64;  
};
其中，events 是一个位掩码，用于指定感兴趣的事件类型（如 EPOLLIN、EPOLLOUT 等），data 是一个联合体，用于存储用户定义的附加数据或文件描述符。

五、总结
epoll API 通过其高效的事件通知机制，显著提高了大规模并发网络编程的性能。它利用内核内部的数据结构来维护就绪事件列表，避免了传统轮询造成的效率损失，并减少了用户空间与内核空间之间的数据拷贝操作。在实际应用中，epoll 常用于构建高性能、可伸缩的网络服务器。