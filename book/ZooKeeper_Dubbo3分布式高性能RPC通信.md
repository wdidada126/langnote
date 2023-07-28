ZooKeeper_Dubbo3分布式高性能RPC通信

9787301333921

2022-10-01

本教程详细介绍了ZooKeeper + Dubbo 3联合开发时的高频实战技能，包含ZooKeeper的数据模型、Watch观察者机制、服务器角色、领导选举、ZAB协议、ZooKeeper架构、节点类型、ZooKeeper运用场景、搭建单机和主从环境、常用的Command命令、ACL授权、配额等高频使用技术点。在Dubbo 3章节中详细介绍了单体/水平集群/垂直集群/SOA架构的发展历程、CAP理论、Dubbo特性、RPC原理、Dubbo中的五大核心组件、直连提供者、隐式参数、服务分组、多版本、启动时检查、令牌验证、超时和线程池大小、Nacos注册中心、服务提供者集群、集群容错、负载均衡等实用技能。


第 1 章 ZooKeeper核心理论 1
1.1 ZooKeeper的介绍 2
1.2 ZooKeeper的数据模型和Watch观察
机制 3
1.3 ZooKeeper中的角色：Leader领导者/
Follower跟随者 6
1.4 ZooKeeper为什么要进行选举 6
1.5 Paxos算法和ZAB协议简介 7
1.6 ZooKeeper选举的算法 7
1.7 为什么建议服务器个数为奇数 9
1.8 ZooKeeper的特点 10
1.9 使用ZooKeeper的架构 10
1.10 znode节点类型 12
1.11 ZooKeeper的运用场景 13
1.12 ZooKeeper的五点保证 13
1.13 简单的API 13
第 2 章 搭建ZooKeeper单机运行
环境 14
2.1 下载ZooKeeper 15
2.2 创建zoo.cfg配置文件 16
2.3 核心配置选项tickTime、dataDir、
clientPort的解释 18
2.4 启动ZooKeeper服务 18
2.5 连接ZooKeeper服务 20
2.6 停止ZooKeeper服务 21
2.7 查看ZooKeeper服务状态 21
2.8 查看ZooKeeper所有命令 22
2.9 使用create命令创建znode节点 23
2.10 使用ls命令查看所有子节点 25
2.11 使用get命令查看节点对应的值 26
2.12 使用set命令对节点设置新值 27
2.13 使用delete命令删除节点 29
第 3 章 搭建ZooKeeper主从运行
环境 31
3.1 配置选项initLimit和syncLimit的
解释 32
3.2 创建myid文件及更改cfg配置文件 33
3.3 启动每个ZooKeeper实例 35
3.4 向Leader中存数据及从Follower中取
数据 36
3.5 获取ZooKeeper实例的角色 37
3.6 命令sync的使用 38
第 4 章 ZooKeeper常见命令和Curator
的使用 39
4.1 命令create [-s] [-e] [-c] [-t ttl] path
[data] [acl]和get [-s] [-w] path的
使用 40
4.2 命令deleteall的使用 57
4.3 命令close的使用 59
4.4 命令connect host:port的使用 60
4.5 命令getAcl [-s] path的使用与验证
方式 61
4.6 设置认证方式与授权 64
4.7 命令quit的使用 77
4.8 配额的使用 77
4.9 命令history的使用 84
4.10 命令redo cmdno的使用 84
4.11 命令set [-s] [-v version] path data的
使用：根据version实现乐观锁 85
4.12 命令delete [-v version] path的使用：
根据version版本号删除 88
4.13 命令get [-s] [-w] path的使用：使用
watch监控数据变化 90
4.14 命令printwatches on|off的使用 92
4.15 命令ls [-s] [-w] [-R] path的使用：
使用-w参数只监控子节点变化 93
4.16 命令ls [-s] [-w] [-R] path的使用：
使用-R参数取出所有子和子孙节点 96
4.17 命令ls [-s] [-w] [-R] path的使用：
使用-s参数取出节点的状态数据 96
4.18 命令stat [-w] path的使用 98
4.19 命令removewatches path [-c|-d|-a] [-l]
的使用 99
4.20 自实现递归watch的效果 103
4.21 命令whoami的使用 107
4.22 命令version的使用 107
4.23 命令getAllChildrenNumber path的
使用 107
4.24 命令getEphemerals path的使用 108
第 5 章 软件技术架构的发展 109
5.1 单体架构 110
5.2 水平集群架构 111
5.3 垂直集群架构 112
5.4 SOA架构 113
5.5 微服务架构 115
5.6 CAP理论 117
第 6 章 Dubbo介绍 120
6.1 Dubbo介绍 121
6.2 使用服务注册和服务发现的必要性 130
第 7 章 Dubbo实战技能 132
7.1 创建my-parent父模块 133
7.2 创建my-api模块 136
7.3 使用ZooKeeper作为注册中心实现RPC
通信 139
7.4 直连提供者 150
7.5 隐式参数 157
7.6 服务分组 164
7.7 多版本 172
7.8 启动时检查 180
7.9 令牌验证 189
7.10 超时和线程池大小 197
7.11 Nacos
介绍 208
7.12 搭建Nacos单机运行环境 211
7.13 使用Nacos作为注册中心实现RPC
通信 215
7.14 结合ZooKeeper注册中心集群 222
第 8 章 Dubbo高级技能 229
8.1 服务提供者集群 230
8.2 集群容错 237
8.3 负载均衡 263
