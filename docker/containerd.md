# containerd 



docker 对容器的管理和操作基本都是通过 containerd 完成的

https://www.cnblogs.com/sparkdev/p/9063042.html





Containerd 的技术方向和目标

- 简洁的基于 gRPC 的 API 和 client library
- 完整的 OCI 支持(runtime 和 image spec)
- 同时具备稳定性和高性能的定义良好的容器核心功能
- 一个解耦的系统(让 image、filesystem、runtime 解耦合)，实现插件式的扩展和重用