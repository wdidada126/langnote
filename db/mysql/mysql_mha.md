# mysql mha


mha4mysql-manager
https://github.com/yoshinorim/mha4mysql-manager



https://www.cnblogs.com/--smile/p/11475380.html

MHA（Master High Availability）目前在 MySQL 高可用方面是一个相对成熟的解决方案，它由日本 DeNA 公司的 youshimaton（现就职于 Facebook 公司）开发，是一套优秀的作为 MySQL 高可用性环境下故障切换和主从提升的高可用软件。
在 MySQL 故障切换过程中，MHA 能做到在0~30秒之内自动完成数据库的故障切换操作，并且在进行故障切换的过程中，MHA 能在最大程度上保证数据的一致性，以达到真正意义上的高可用。
该软件由两部分组成：MHA Manager（管理节点）和 MHA Node（数据节点）。MHA Manager 可以单独部署在一台独立的机器上管理多个 master-slave 集群，也可以部署在一台 slave 节点上。MHA Node 运行在每台 MySQL 服务器上，MHA Manager 会定时探测集群中的 master 节点，当 master 出现故障时，它可以自动将最新数据的 slave 提升为新的 master，然后将所有其他的 slave 重新指向新的 master。整个故障转移过程对应用程序完全透明。
在 MHA 自动故障切换过程中，MHA 试图从宕机的主服务器上保存二进制日志，最大程度的保证数据的不丢失，但这并不总是可行的。例如，如果主服务器硬件故障或无法通过ssh访问，MHA 没法保存二进制日志，只进行故障转移而丢失了最新的数据。使用 MySQL 5.5 的半同步复制，可以大大降低数据丢失的风险。MHA 可以与半同步复制结合起来。如果只有一个 slave 已经收到了最新的二进制日志，MHA 可以将最新的二进制日志应用于其他所有的 slave 服务器上，因此可以保证所有节点的数据一致性。
目前 MHA 主要支持一主多从的架构，要搭建 MHA,要求一个复制集群中必须最少有三台数据库服务器，一主二从，即一台充当 master，一台充当备用 master，另外一台充当从库，因为至少需要三台服务器，出于机器成本的考虑，淘宝也在该基础上进行了改造，目前淘宝TMHA已经支持一主一从。
