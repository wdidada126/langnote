# TDSQL

全面解析腾讯数据库TDSQL架构
https://www.jianshu.com/p/c41a19525c7b
系统由三个模块组成：Scheduler、Agent、网关，三个模块的交互都是通过ZooKeeper完成，极大简化了各个节点之间的通信机制，相对于第二代HOLD的开发简单了很多。

