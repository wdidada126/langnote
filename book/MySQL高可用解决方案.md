# MySQL高可用解决方案

https://book.douban.com/subject/36096579/

徐轶韬，甲骨文公司MySQL解决方案首席工程师。为中国金融、政府、航空运输等行业的MySQL用户提供相关产品的售前咨询、企业级产品介绍、解决方案服务，以及推广和普及MySQL数据库在社区的使用。公众号“MySQL解决方案工程师”的运营者和内容作者。“3306π”开源软件社区活动出品人，“墨天轮”社区2020年度十大突出贡献人物。

本书对MySQL官方提供的高可用解决方案逐一进行介绍，详细阐述每种方案的原理、架构、优缺点及适用场景，并配合演示说明，帮助读者快速理解相关内容。与其他MySQL高可用相关图书不同，本书专注于MySQL官方团队提供的解决方案，包括MySQL主从复制、MySQL ReplicaSet、组复制、InnoDB Cluster及InnoDB ClusterSet等相关内容。此外，本书还介绍了MySQL 8.0的部分内容，包括文档存储、MySQL Shell及MySQL Router等。附录部分介绍了企业版监控、企业版备份等MySQL官方工具，以及克隆插件和虚拟机环境VirtualBox，使读者可以更加全面地了解MySQL的生态和工具。通过本书，MySQL数据库开发人员、MySQL数据库管理人员和架构师可以了解MySQL当前全部的产品特性和高可用解决方案，获知每种方案的详细内容，并能够将高可用解决方案灵活运用到实际的生产解决方案中。本书面向的读者对象包括MySQL的初学者、数据库架构师、DBA、相关软件开发人员，以及组织内部的IT负责人。



## 第1章 高可用介绍 1
1.1　高可用的概念 1
1.1.1　可靠性 3
1.1.2　恢复 4
1.1.3 冗余 5
1.1.4 容错 5
1.1.5 可伸缩性 6
1.2　MySQL高可用 7
1.2.1　MySQL高可用选项 7
1.2.2　MySQL高可用的实现 8
1.2.3　MySQL高可用带来的挑战 9

## 第2章 MySQL高可用的演进 10

2.1 主从复制 11
2.1.1 主从复制的优点 11
2.1.2 主从复制的缺点 12
2.1.3 主从复制的方法概述 12
2.1.4 主从复制的类型概述 13
2.1.5 主从复制适用的高可用要求 13
2.2 组复制 14
2.2.1 组复制实现的理论 14
2.2.2 组复制的优点 15
2.2.3 组复制的要求 16
2.2.4 组复制的缺点和限制 17
2.2.5 组复制满足的高可用要求 17
2.3 InnoDB Cluster 18
2.3.1 InnoDB Cluster的构成 19
2.3.2 InnoDB Cluster的要求和限制 19
2.3.3 InnoDB Cluster满足的高可用要求 20
2.4 InnoDB ReplicaSet 20
2.4.1 InnoDB ReplicaSet的构成 21
2.4.2 InnoDB ReplicaSet的使用限制 22
2.4.3 InnoDB ReplicaSet满足的高可用要求 23
2.5 InnoDB ClusterSet 23
2.5.1 InnoDB ClusterSet的要求和限制 24
2.5.2 InnoDB ClusterSet满足的高可用要求 25
2.6 NDB Cluster 25
2.6.1 NDB Cluster的架构 26
2.6.2 NDB Cluster的数据节点和高可用性 27
2.6.3 NDB Cluster适用的场景和要求 28

## 第3章 主从复制与InnoDB ReplicaSet 30

3.1 主从复制与InnoDB ReplicaSet入门 31
3.1.1　主从复制的原理 31
3.1.2　主从复制的类型 32
3.1.3　主从复制的应用场景 35
3.1.4　InnoDB ReplicaSet的基础知识 37
3.2　主从复制功能的演示 38
3.2.1 配置主从复制的步骤 38
3.2.2　使用GTID进行复制 57
3.2.3　配置半同步复制 63
3.3 InnoDB ReplicaSet演示 67
3.3.1　直接配置InnoDB ReplicaSet 71
3.3.2　采用现有的复制配置InnoDB ReplicaSet 80
3.3.3　InnoDB ReplicaSet与MySQL Router 83
3.3.4　使用InnoDB ReplicaSet 88

## 第4章 组复制 92
4.1　什么是组复制 92
4.1.1　概念和术语 93
4.1.2　组复制使用的技术 95
4.1.3　组复制的架构及功能 95
4.1.4　组复制的特征及使用场景 98
4.2　组复制的模式 99
4.2.1　单主模式 99
4.2.2　多主模式 101
4.3　组复制的通信系统与成员管理 104
4.3.1　组复制的通信过程 104
4.3.2　组复制达成一致及认证的过程 105
4.3.3　事务的整体顺序传递 107
4.3.4　组成员关系管理 108
4.4　组复制的监控与管理 109
4.4.1　故障检测机制 109
4.4.2　组复制监控 111
4.4.3　改变组复制模式 119
4.5　组复制的事务一致性 124
4.5.1　组复制的一致性相关事件 124
4.5.2　一致性级别的影响 126
4.6　组复制的分布式恢复 130
4.6.1　组复制的分布式恢复过程 130
4.6.2　组复制的分布式恢复方法 131
4.7　组复制的搭建及操作演示 132
4.7.1　组复制的要求 132
4.7.2　本地搭建组复制 134
4.7.3　组复制的操作 143
4.7.4　组复制的安全性 156
4.7.5　组复制的升级 162
4.8　组复制的优化 169
4.8.1　组通信线程（GCT） 169
4.8.2　消息压缩 170
4.8.3　流量控制 171
4.8.4　消息片段化 174
4.8.5　通信引擎缓存管理 175
4.8.6　故障检测和网络分区的响应 177
4.9　组复制的限制 183
4.9.1　组复制的功能性限制 183
4.9.2　组复制的事务大小限制 185
## 第5章 MySQL Shell 187
5.1　MySQL Shell概述 187
5.1.1　MySQL Shell的特性 188
5.1.2　MySQL 8.0的新特性 190
5.2　MySQL Shell的安装方法 194
5.2.1　安装MySQL Shell 194
5.2.2　在macOS上安装MySQL Shell 196
5.2.3　在Linux上安装MySQL Shell 199
5.3　如何使用MySQL Shell 199
5.3.1　MySQL Shell的命令与选项 200
5.3.2 MySQL Shell入门 204
5.3.3　使用MySQL Shell 210
5.4　在MySQL Shell中使用SQL对数据库进行操作 229
5.4.1　关系型数据库基础 230
5.4.2　使用MySQL的语句和函数 233
5.4.3　使用Python管理数据库 248
5.5　在MySQL Shell中使用NoSQL对文档存储进行操作 261
5.5.1　MySQL中的JSON文档 264
5.5.2　路径表达式 269
5.5.3　JSON函数 273
## 第6章 MySQL Router 283
6.1　MySQL Router概述 284
6.2　MySQL Router的安装 285
6.2.1　Windows下的MySQL Installer 286
6.2.2　在其他操作系统下安装MySQL Router 289
6.3　部署与配置 289
6.3.1　基本连接路由 290
6.3.2　路由器演示 291
6.3.3　配置路由器 294
6.4　路由器应用程序 301
6.4.1　启动路由器 302
6.4.2　使用路由器日志 302
## 第7章 InnoDB Cluster 304
7.1　InnoDB Cluster概述 304
7.2　ACID特性 305
7.3　组件 308
7.3.1　组复制 308
7.3.2　MySQL Shell 309
7.3.3　X DevAPI 310
7.3.4　AdminAPI 310
7.3.5　MySQL Router 311
7.4　安装InnoDB Cluster 311
7.4.1 在Windows上安装MySQL 313
7.4.2　利用Sandbox部署InnoDB Cluster 319
## 第8章 使用AdminAPI部署InnoDB Cluster 325
8.1　dba类 326
8.2　cluster类 329
8.3　InnoDB Cluster部署演示 330
8.3.1　部署全新的InnoDB Cluster 331
8.3.2　将组复制转换为InnoDB Cluster 338
8.4　InnoDB Cluster与MySQL Router 343
8.4.1　配置MySQL Router 343
8.4.2　AdminAPI与MySQL Router 346
## 第9章 InnoDB Cluster管理与优化 348
9.1　集群的监视 348
9.1.1　使用Cluster.describe()方法监视集群 349
9.1.2　使用Cluster.status()方法检查集群的状态 350
9.1.3　监视恢复操作 357
9.1.4　查看InnoDB Cluster和组复制的通信协议 359
9.2　集群的使用 360
9.2.1　检查实例配置 361
9.2.2　添加和删除实例 362
9.2.3　解散集群 363
9.2.4　改变集群拓扑 364
9.3　集群配置 366
9.3.1　集群的配置选项 366
9.3.2　配置选举过程 367
9.3.3　配置故障转移一致性 367
9.3.4　配置实例自动重新加入 368
9.3.5　配置并行复制应用 369
9.3.6　集群的安全性 371
9.4　集群的升级 372
9.4.1　MySQL Router滚动升级 373
9.4.2　更新InnoDB Cluster的元数据 373
9.5　集群的故障排除 374
9.5.1　将实例重新加入集群 374
9.5.2　从丢失仲裁中恢复集群 375
9.5.3　在成员宕机后重新启动集群 376
9.5.4　重新扫描集群 377
9.6　使用集群的限制与技巧 378
9.6.1　使用集群的限制 378
9.6.2　使用集群的技巧 379
## 第10章 InnoDB ClusterSet 382
10.1　InnoDB ClusterSet概述 382
10.2　部署InnoDB ClusterSet 384
10.3　InnoDB ClusterSet的状态与拓扑 394
10.3.1　InnoDB ClusterSet的状态 394
10.3.2　InnoDB ClusterSet的拓扑 399
10.4　InnoDB ClusterSet与MySQL Router 401
10.4.1　ClusterSet使用路由器时的注意事项 401
10.4.2　ClusterSet使用路由器的配置步骤 401
10.5　InnoDB ClusterSet的主动切换与故障转移 408
10.5.1　InnoDB ClusterSet执行主动切换的过程 408
10.5.2　InnoDB ClusterSet的故障转移 415
10.6　InnoDB ClusterSet的要求与限制 423
10.6.1　InnoDB ClusterSet的要求 423
10.6.2　InnoDB ClusterSet的限制 424
## 第11章 MySQL的相关软件与工具 425
11.1　MySQL产品的生命周期 425
11.2　MySQL的高级功能 427
11.2.1　企业版备份 427
11.2.2　企业版监控 432
11.2.3　MySQL TDE (Transparent Data Encryption) 437
11.3　MySQL Workbench 446
11.3.1　MySQL Workbench的下载 446
11.3.2　MySQL Workbench的功能及使用 447
11.4　MySQL的克隆插件 451
11.4.1　安装克隆插件 452
11.4.2　克隆数据 453
11.4.3　复制使用克隆插件 454
11.5　关于VirtualBox 457