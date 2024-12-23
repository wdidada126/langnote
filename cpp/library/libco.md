# libco

最近更新 2020年
github.com/Tencent/libco

libco是一个非常优秀的c++协程库，但它仍然有些缺点：1. 代码可读性不高，虽说为C++开发的，但实际上大量使用结构体等，而不是基于OOP。2. 只封装协程hook层级，没有进一步封装。至少封装到提供如TcpServer、TcpConnection等类，更方便使用。当然这也不算缺点，毕竟libco只是协程库，而不是网络库。既然这样，那为什么不自己写一个支持协程的网络库呢？毕竟不自己造点轮子出来都不好意思说自己写C++的。

链接：https://zhuanlan.zhihu.com/p/466349082

