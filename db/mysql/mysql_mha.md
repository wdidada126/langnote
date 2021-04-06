# mysql mha


MHA作为MySQL5.7版本下传统复制下的高可用霸主，依旧在MySQL5.7的高可用架构中占据主流地位。

且MHA在MYSQL5.7版本后已经不再更新，这意味着继续使用MHA搭建MySQL8.0的高可用性架构存在不稳定性和不确定性，虽然有人依旧在这么干。

在GTID环境下，MHA随着MySQL8.0版本的推出，慢慢走向没落；
大家开始选择replication-manager或者orchestrator等高可用解决方案。

不足及风险点：
1、failover依赖于外部脚本，比如VIP切换需要自己编写脚本实现
2、MHA启动后只检测主库是否正常，并不检查从库状态及主从延迟
3、需要基于SSH免认证配置，存在一定的安全隐患
4、没有提供从服务器的读负载均衡功能
5、从节点出现宕机等异常并没有能力处理，即没有从库故障转移能力
6、在高可用切换期间，某些场景下可能出现数据丢失的情况，并不保证数据0丢失
7、无法控制RTO恢复时间


mha4mysql-manager
https://github.com/yoshinorim/mha4mysql-manager


https://www.cnblogs.com/xiaolang666/p/13958563.html

https://www.cnblogs.com/--smile/p/11475380.html

MHA（Master High Availability）目前在 MySQL 高可用方面是一个相对成熟的解决方案，它由日本 DeNA 公司的 youshimaton（现就职于 Facebook 公司）开发，是一套优秀的作为 MySQL 高可用性环境下故障切换和主从提升的高可用软件。
在 MySQL 故障切换过程中，MHA 能做到在0~30秒之内自动完成数据库的故障切换操作，并且在进行故障切换的过程中，MHA 能在最大程度上保证数据的一致性，以达到真正意义上的高可用。
该软件由两部分组成：MHA Manager（管理节点）和 MHA Node（数据节点）。MHA Manager 可以单独部署在一台独立的机器上管理多个 master-slave 集群，也可以部署在一台 slave 节点上。MHA Node 运行在每台 MySQL 服务器上，MHA Manager 会定时探测集群中的 master 节点，当 master 出现故障时，它可以自动将最新数据的 slave 提升为新的 master，然后将所有其他的 slave 重新指向新的 master。整个故障转移过程对应用程序完全透明。
在 MHA 自动故障切换过程中，MHA 试图从宕机的主服务器上保存二进制日志，最大程度的保证数据的不丢失，但这并不总是可行的。例如，如果主服务器硬件故障或无法通过ssh访问，MHA 没法保存二进制日志，只进行故障转移而丢失了最新的数据。使用 MySQL 5.5 的半同步复制，可以大大降低数据丢失的风险。MHA 可以与半同步复制结合起来。如果只有一个 slave 已经收到了最新的二进制日志，MHA 可以将最新的二进制日志应用于其他所有的 slave 服务器上，因此可以保证所有节点的数据一致性。
目前 MHA 主要支持一主多从的架构，要搭建 MHA,要求一个复制集群中必须最少有三台数据库服务器，一主二从，即一台充当 master，一台充当备用 master，另外一台充当从库，因为至少需要三台服务器，出于机器成本的考虑，淘宝也在该基础上进行了改造，目前淘宝TMHA已经支持一主一从。
