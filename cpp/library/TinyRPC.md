# TinyRPC
只用 10 行代码搭建一个高性能 RPC 服务 -- TinyRPC 框架应用篇
https://zhuanlan.zhihu.com/p/522778736
C++实现的协程异步 RPC 框架 TinyRPC（一）-- 协程封装
https://zhuanlan.zhihu.com/p/466349082

C++实现的协程异步 RPC 框架 TinyRPC（二）-- 协程Hook
https://zhuanlan.zhihu.com/p/474353906
C++实现的协程异步 RPC 框架 TinyRPC（三）-- 时间轮处理无效的 TCP 连接
https://zhuanlan.zhihu.com/p/505034474
C++实现的协程异步 RPC 框架 TinyRPC（四）-- Reactor 实现
https://zhuanlan.zhihu.com/p/503323714

C++实现的协程异步 RPC 框架 TinyRPC（五）-- TcpServer 实现
https://zhuanlan.zhihu.com/p/523947909

C++实现的协程异步 RPC 框架 TinyRPC（六）-- TcpConnection 实现
https://zhuanlan.zhihu.com/p/524517895

C++实现的协程异步 RPC 框架 TinyRPC（七）-- 编解码与事件分发
https://zhuanlan.zhihu.com/p/557082478

https://github.com/edidada/rocket-cpp

https://github.com/Gooddbird/tinyrpc


wrk -c 1000 -t 8 -d 30 --latency 'http://127.0.0.1:19999/qps?id=1'
Running 30s test @ http://127.0.0.1:19999/qps?id=1