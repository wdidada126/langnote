# zk

- testcurator
- distarch
- ZooKeeper





- ClientSingleWatch
- CuratorFrameworkDemo



ZooKeeper这个github仓库是md文件



org.apache.zookeeper.KeeperException$ConnectionLossException



https://blog.csdn.net/u011534095/article/details/48421119



[zk命令行客户端](https://www.cnblogs.com/leesf456/p/6022357.html)

[zk客户端](https://blog.csdn.net/yelllowcong/article/details/78230026)

[Zookeeper使用命令行](https://www.cnblogs.com/leesf456/p/6022357.html)

zk面试题

[zook docker安装](https://blog.csdn.net/qq_37495786/article/details/83280467)


zk客户端
cursor

zk分布式

zk监控时间，一旦发生时间，会把相应信息推送给客户端





zk是apache开源项目

使用场景：hadoop

利用ZooKeeper搭建Hadoop的HA集群

https://www.cnblogs.com/qingyunzong/p/8634335.html



HDFS的NameNode的HA,

YARN的ResourceManager的HA

https://www.linuxidc.com/Linux/2017-11/148906.htm









Zookeeper 有4种节点属性，持久化节点PERSISTENT,临时节点EPHEMERAL，持久化时序节点PERSISTENT_SEQUENTIAL，临时时序节点EPHEMERAL_SEQUENTIAL



zkServer





https://blog.csdn.net/qq_27529917/article/details/80614274

zkCli  -timeout 5000 -r -server 172.17.45.14:2181

zkCli  -timeout 5000 -r -server 127.0.0.1:2181





```shell
ZooKeeper -server host:port cmd args
        stat path [watch]
        set path data [version]
        ls path [watch]
        delquota [-n|-b] path
        ls2 path [watch]
        setAcl path acl
        setquota -n|-b val path
        history
        redo cmdno
        printwatches on|off
        delete path [version]
        sync path
        listquota path
        rmr path
        get path [watch]
        create [-s] [-e] path data acl
        addauth scheme auth
        quit
        getAcl path
        close
        connect host:port






ls /
create /node_01 mydata
# Node already exists: /node_01

create -e /node_02

create -s -e /node_03

create -s /node_04 data

 stat /node_01 
cZxid = 0x2f
ctime = Sat Nov 12 15:54:05 CST 2016
mZxid = 0x2f
mtime = Sat Nov 12 15:54:05 CST 2016
pZxid = 0x2f
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 6
numChildren = 0

ls /node_01
ls2 /node_01

set /node_01 data_1
get /node_01
set /node_01 data_02

delete path [version]

rmr node_01
```





[Apache curator-recipes代码范例](https://blog.csdn.net/wangmuming/article/details/38234247)

创建节点 赋值数据
更改数据
判断节点是否存在

获取数据

删除数据
删除节点

创建子节点
递归创建多级子节点
获取子节点列表

zk数据存储方式



测试zk主动推送数据



`zkCli -server 172.17.45.14:2181 ls /`





[zk server 历史](https://blog.csdn.net/gaoshan12345678910/article/details/67638657#commentBox)



```
Exception in thread "main" org.apache.zookeeper.KeeperException$ConnectionLossException: KeeperErrorCode = ConnectionLoss for /
```





[远程主机强迫关闭了一个现有的连接](https://blog.csdn.net/weixin_39816332/article/details/83239307)





https://blog.csdn.net/mayp1/article/details/52137327



https://cwiki.apache.org/confluence/display/zookeeper/zab



https://www.zhihu.com/question/389403695/answer/1171102356





[什么样的系统 ](https://www.zhihu.com/question/384102981/answer/1119478764)





zk book



- [ZooKeeper:分布式过程协同技术详解 : 分布式过程协同技术详解](https://book.douban.com/subject/26766807/)

- [从Paxos到Zookeeper : 分布式一致性原理与实践](https://book.douban.com/subject/26292004/)



- [Netty、Redis、Zookeeper高并发实战](https://book.douban.com/subject/34801361/)

