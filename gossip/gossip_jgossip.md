# jgossip



```shell
member:GossipMember{cluster='gossip_cluster', ipAddress='127.0.0.1', port=60001, id='127.0.0.1:60001', state=JOIN}  state: JOIN
五月 31, 2020 7:53:04 下午 net.lvsq.jgossip.core.GossipManager
信息: Starting gossip! cluster[gossip_cluster] ip[127.0.0.1] port[60001] id[127.0.0.1:60001]
```



##### 实现

gossip 协议有多种实现，这里说一个例子当节点启动时，读配置文件，然后向一个 seed 发送信息，进行信息同步，然后开始没秒都随机选择一个 seed 节点来同步信息
1、随机取一个当前活着的节点，并向它发送同步请求
2、向随机一台不可达的机器发送同步请求
3、如果第一步中所选择的节点不是 seed，或者当前活着的节点数少于 seed 数，则向随意一台 seed 发送同步请求

##### 应用

Cassandra
Cassandra 主要是使用 Gossip 完成三方面的功能：
失败检测
动态负载均衡
去中心化的弹性扩展
Consul





gossip分为客户端和service端？不是，对等节点




一直找不到合适的MySQL监控工具，正好听同事无意中说起，Percona在2016年4月发布了一个监控套件，可以同时对多个MySQL、MongoDB实例进行监控。



memberlist是HashiCorp公司开源的*Gossip*库，这个库被consul（也是HashiCorp公司开源的）所引用。 它是SWIM的一个扩展实现。



![udp](gossip_udp_data.png)

