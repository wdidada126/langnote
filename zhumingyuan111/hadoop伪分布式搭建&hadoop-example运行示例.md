---
title: hadoop伪分布式搭建&hadoop-example运行示例
date: 2017-06-13 09:31:46
tags: CSDN迁移
---
  ## hadoop伪分布式搭建

 hadoop 伪分布式实在单击模式的基础上进行的，单击模式可以参考我的另外一片blog : [http://blog.csdn.net/zhumingyuan111/article/details/53149642](http://blog.csdn.net/zhumingyuan111/article/details/53149642)

 
### 配置 ～-site.xml文件

 %HODOOP_HOME%/etc/hadoop/路径下有：core-site.xml,hdfs-site.xml,mapred-site.xml 三个文件，其含义：

  
  * core-site.xml: Hadoop Core的配置项，例如HDFS和MapReduce常用的I/O设置等。 
  * hdfs-site.xml: Hadoop 守护进程的配置项，包括namenode，辅助namenode和datanode等。 
  * mapred-site.xml： MapReduce 守护进程的配置项，包括jobtracker和tasktracker。   
     下面给出三个文夹的配置内容：  core-site.xml 

 
```
<configuration>
   <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
  </property>
  <property>
      <name>hadoop.tmp.dir</name>
      <value>/usr/local-extend/hadoop_hdfs/tmp</value>
  </property>
</configuration>
```
 hdfs-site.xml

 
```
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>1</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:/usr/local/hadoop/hdfs/name</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:/usr/local/hadoop/hdfs/data</value>
        </property>
</configuration>

```
 mapred-site.xml

 
```
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
</configuration>

```
 
### 新建几个文件夹用于存储namenode&datanode&hadoop.tmp.dir

 建立文件夹的位置分别与core-site.xml、hdfs-site.xml中配置一致。   
 /usr/local-extend/hadoop_hdfs/tmp   
 file:/usr/local/hadoop/hdfs/name   
 file:/usr/local/hadoop/hdfs/data

 
```
mkdir /usr/local-extend/hadoop_hdfs/tmp
mkdir /usr/local/hadoop/hdfs
mkdir /usr/local/hadoop/hdfs/name
mkdir /usr/local/hadoop/hdfs/data

```
 
### 格式化HDFS

 主要就是格式化namenode,secondarynamenode,tasktracker   
 在%HADOOP_HOME%/bin下执行：

 
```
hadoop namenode -format
```
 ![这里写图片描述](https://img-blog.csdn.net/20170614082731916?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 ![这里写图片描述](https://img-blog.csdn.net/20170614082802394?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

  
  * 注意如果是第二次格式化，/usr/local/hadoop/hdfs/name 和/usr/local/hadoop/hdfs/data 两个文夹下的VERSION中的cluster要保证一致，否则datanode节点无法启动。
    
     
    ### 启动hadoop
    
     路径%HADOOP_HOME%/sbin
    
     
    ```
    /usr/local/hadoop/sbin$ ./start-all.sh
    ```
     查看hadoop守护进程
    
     
    ```
    /usr/local/hadoop/sbin$ jps
    ```
     出现下图则表示安装成功   
     ![这里写图片描述](https://img-blog.csdn.net/20170614083614742?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
    
      如果安装成功之后，可以访问以下web   
 [http://localhost:50030/](http://localhost:50030/) - Hadoop 管理介面   
 [http://localhost:50060/](http://localhost:50060/) - Hadoop Task Tracker 状态   
 [http://localhost:50070/](http://localhost:50070/) - Hadoop DFS 状态

 此时hadoop已经安装成功，可以对hdfs进行相关操作 

 
```
创建文件夹 ： /usr/local/hadoop/bin$ hdfs dfs -mkdir /usr/tmp/input
存放文件：/usr/local/hadoop/bin$ hdfs dfs -put test.txt /usr/tmp/input
```
 
### 运行hadoop自带的例子

 
```
/usr/local/hadoop/bin$ hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount /usr/tmp/input /usr/tmp/output

```
 ![这里写图片描述](https://img-blog.csdn.net/20170614223311770?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 ![这里写图片描述](https://img-blog.csdn.net/20170614223338043?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
#### 查看输出文件

 
```
/usr/local/hadoop/bin$ hdfs dfs -get /usr/tmp/output
```
 
```
 /usr/local/hadoop/bin$ vim part-r-00000 
```
 ![这里写图片描述](https://img-blog.csdn.net/20170614223641700?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
### 关闭Hadoop的守护进程

 
```
/usr/local/hadoop/sbin$ ./stop-all.sh 
```
 
### 总结

 
```
      以上基本把hadoop伪分布的情况搭建完成，后续在此基础上进行spark的环境搭建。

```
   
  