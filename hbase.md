# hbase

作者：向磊
链接：https://www.zhihu.com/question/39859266/answer/83676259
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

纠正一个理解错误，hbase不是oltp，作为一个NoSQL，他顶多是olp, 没有transaction。而且仅在rowkey上支持索引。在性能上不如memcached和redis，但是持久化存储方面比内存NoSQL强啊。作为文档型NoSQL在分布式存储上比mongo做sharding和MapReduce分析方便多了啊。当然最重要的原因是这样，设想你要存储用户的地址和喜好，这当然可以做成结构化SQL。但是用户把家搬到上海了，那么以前在北京的地址要update覆盖掉吗，我们要计算分析用户的整个人生周期的活动记录和喜好，来推测他的行为，收入，知识层次，信用，道德水准之类的，当然他的相关历史行为是不能被丢弃的。所以hbase可以很好的适应这样的场景。这只是简单的举个例子，mongo在小规模下也可以适应这种场景，不过随着数据增长，会涉及到sharding和gridfs让人痛苦的要命。当然以上场景也可以用其他工具，比如Cassandra，但是hbase和accumulo是跟hdfs以及mapreduce,Spark等结合的最好的，不但可以方便地存，更可以方便地算，这才是用hbase重要的原因吧。当然hbase不是银弹，不能解决所有问题，所以才会有那么多其他的NoSQL和SQL。---------补充你的补充提问的补充回答1.当然会有数据分析的需求，放了N多数据，如果只是为了存着，成本太高了。hbase依赖于hdfs存储，就我目前的认知范围，还不知道怎么在没有hadoop的情况下安装hbase。2.用户生命周期数据为何要存成日志，难道不需要获取了吗，每次网页申请获取一个用户数据都要跑一遍MR计算吗？另外，hbase是可以update的。只不过机制跟sql完全不同。3.事实上，hbase适合大数据量的查询，但并不适合大范围的查询，他就是put，get kv对，海量数据下跑类似select一样的检索scan一遍全表？

Caused by: java.io.FileNotFoundException: HADOOP_HOME and hadoop.home.dir are unset.


https://blog.csdn.net/qq_35590459/article/details/102540091

https://github.com/xnnre/winutils


http://127.0.0.1:16010/master-status

1 set set JAVA_HOME=D:\Program Files\Java\jdk1.8.0_171(注意是反斜线路径是自己的jdk安装路径)

2 set HBASE_MANAGES_ZK=false;


打开新的cmd命令常窗口,将目录定位到hbase的bin目录下输入:hbase shell进入hbase shell命令模式


hadoop三个进程master zk 
hbase类似数据库
hbase可以基于zk
hbase可以基于本地文件系统或者hdfs
https://apachecn.gitee.io/hbase-doc-zh/#/docs/2

