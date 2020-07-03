---
title: Hadoop+hbase+zookeeper整合
date: 2017-06-24 09:51:12
tags: CSDN迁移
---
  ### Hadoop+hbase+zookeeper整合

 
#### 各软件版本介绍

 hadoop 2.7.3   
 hbase 1.2.4   
 zookeeper 3.4.9

 
#### hadoop安装

 关于hadoop的安装可以参考我的两篇blog:   
 [http://blog.csdn.net/zhumingyuan111/article/details/53149642](http://blog.csdn.net/zhumingyuan111/article/details/53149642)   
 [http://blog.csdn.net/zhumingyuan111/article/details/73161098](http://blog.csdn.net/zhumingyuan111/article/details/73161098)

 
#### zookeeper安装

 下载zookeeper文件 zookeeper-3.4.9.tar.gz   
 解压到制定目录 

 
```
tar -zxvf  zookeeper-3.4.9.tar.gz -C /usr/local/zookeeper
```
 环境变量配置

 
```
export ZOOKEEPER_HOME=/usr/local/zookeeper
export PATH=$ZOOKEEPER_HOME/bin:$PATH
```
 配置zookeeper实例   
 在路径：/usr/local/zookeeper/conf

 
```
cp zoo_sample.cfg zoo.cfg
cp zoo_sample.cfg zoo1.cfg
cp zoo_sample.cfg zoo2.cfg
```
 我在一台电脑上开启三个zk实例，下面给出配置文件内容   
 zoo.cfg

 
```
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper/zookeeperdir/zookeeper-data
dataLogDir=/usr/local/zookeeper/zookeeperdir/logs
clientPort=2181
server.1=127.0.0.1:2888:3888
server.2=127.0.0.1:2889:3889
server.3=127.0.0.1:2890:3890                                                             
```
 zoo1.cfg

 
```
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper/zookeeperdir/zookeeper-data1
dataLogDir=/usr/local/zookeeper/zookeeperdir/logs
clientPort=2182
server.1=127.0.0.1:2888:3888
server.2=127.0.0.1:2889:3889
server.3=127.0.0.1:2890:3890
```
 zoo2.cfg

 
```
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper/zookeeperdir/zookeeper-data2
dataLogDir=/usr/local/zookeeper/zookeeperdir/logs
clientPort=2183
server.1=127.0.0.1:2888:3888
server.2=127.0.0.1:2889:3889
server.3=127.0.0.1:2890:3890
```
 
##### 参数解释：

 
```
   tickTime：心跳检测的时间间隔（毫秒），缺省：2000
   clientPort：其他应用（比如solr）访问ZooKeeper的端口，缺省：2181
    initLimit：初次同步的阶段（followers连接到leader的阶段），允许的时长（tick数量），缺省：10
    syncLimit：允许followers同步到ZooKeeper的时长（tick数量），缺省：5
    dataDir：数据（比如所管理的配置文件）的存放路径，初始时应该为空
    dataLogDir：zk 日志文件的存储路径
    server.X：X是ensemble中一个服务器的id，后面指定该server的hostname、第一个端口号用于ZooKeeper之间的通信、第二个端口用于和其他应用之间的通信
```
 创建dataDir目录，并在该目录下创建myid文件：   
 在/usr/local/zookeeper/路径下：

 
```
mkdir zookeeperdir
cd zookeeperdir
mkdir zookeeper-data
mkdir zookeeper-data1
mkdir zookeeper-data2
echo "1" > zookeeper-data/myid
echo "2" > zookeeper-data1/myid
echo "3" > zookeeper-data2/myid
```
 
##### 启动zookeeper

 在%ZOOKEEPER_HOME%/bin下：

 
```
zkServer.sh start zoo.cfg
zkServer.sh start zoo1.cfg
zkServer.sh start zoo2.cfg
```
 出现类似的日志信息，则表示启动成功

 
```
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
```
 jps 查看zookeeper的进程   
 ![这里写图片描述](https://img-blog.csdn.net/20170624102323492?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
##### 查看zookeeper状态

 
```
zkServer.sh status zoo.cfg
zkServer.sh status zoo1.cfg
zkServer.sh status zoo2.cfg
```
 出现类似以下的日志则表明启动成功

 
```
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo1.cfg
Mode: leader
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Mode: follower
```
 我们可以看到有一个节点是leader角色,其余的follower角色

 
### hbase安装

 下载hbase安装包，hbase-1.2.4-bin.tar.gz   
 解压并重命名： `tar -zxvf  hbase-1.2.4-bin.tar.gz -C /usr/local/hbase` 

 
#### 配置hbase 环境变量

 
```
export HBASE_HOME=/usr/local/hbase
export PATH=${HBASE_HOME}/bin:$PATH
```
 
#### 修改$HBASE_HOME/conf/hbase-env.sh

 
```
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_111
export HBASE_CLASSPATH=/usr/local/hadoop
export HBASE_MANAGES_ZK=false
```
 
##### 修改$HBASE_HOME/conf/hbase-site.xml

 
```
<configuration>
        <property>
                <name>hbase.rootdir</name>
                <value>hdfs://localhost:9000/hbase</value>
        </property>
        <property>
                <name>hbase.cluster.distributed</name>
                <value>true</value>
        </property>
        <property>
                <name>dfs.replication</name>
                <value>1</value>
        </property>
        <property>
                <name>hbase.zookeeper.quorum</name>
                <value>127.0.0.1</value>
        </property>

        <property>
                <name>zookeeper.session.timeout</name>
                <value>60000</value>
        </property>
</configuration>
```
 注意：hbase.rootdir值是根据%HADOOP_HOME%/etc/hadoop下配置文件core-site.xml中fs.default.name的值加上/hbase.

 
#### 启动hbase

 在启动hbase 之前确定已经启动了hadoop和zookeeper.   
 在%HBASE_HOME%/bin下

 
```
./start-hbase.sh
```
 jps查看进程

 
```
12337 ResourceManager
11809 NameNode
12945 HMaster
12465 NodeManager
13461 Jps
11941 DataNode
13078 HRegionServer
12168 SecondaryNameNode
10924 QuorumPeerMain
10878 QuorumPeerMain
10815 QuorumPeerMain
```
 进入hbase命令行模式

 
```
./hbase shell
```
 接下来可以简单见表测试一下

 
```
建表
create 'hbase_test','id','name','age';
插入数据
put 'hbase_test','1','id:123','bejing'
查看数据
scan 'hbase_test'
```
 
### 遇到的问题总结

 zookeeper 无法成功启动：有一次突然出现zk无法启动，日志中报错：unable to load database on disk 和java.io.IOException: Unreasonable length = 1048583   
 网上查找的解决方案是把dataDir下version-2文件夹下的所有文夹删除，但是似乎还没有解决，后来把dataLogDir下version-2文件夹下的所有文件删除之后问题解决了。

   
  