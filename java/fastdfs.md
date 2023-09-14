# fastdfs
fastdfs源码分析

https://github.com/happyfish100/fastdfs

FastDFS 是一个由 C 语言实现的开源轻量级分布式文件系统，作者余庆(happyfish100)，支持 Linux、FreeBSD、AID 等 Unix 系统，
解决了大数据存储和读写负载均衡等问题，适合存储 4KB~500MB 之间的小文件，如图片网站、短视频网站、文档、app 下载站等，UC、京东、支付宝、迅雷、酷狗等都有使用。

https://www.cnblogs.com/mafly/p/fastdfs.html


fastdfs存储的文件参数有两个，一个group，一个path
https://blog.csdn.net/zollty/article/details/108331055

POSIX通用接口
https://zhuanlan.zhihu.com/p/86827617

跟其他文件系统对比

GFS ceph oss

解决了大容量存储和负载均衡的问题





tracker_server


```java

<dependency>
	<groupId>org.csource</groupId>
	<artifactId>fastdfs</artifactId>
	<version>1.2.4</version>
</dependency>

```


fastdfs可以通过http url的形式下载

FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包括：文件存储、文件同步、文件访问（文件上传、文件下载）等，解决了大容量存储和负载均衡的问题。特别适合以文件为载体的在线服务，如相册网站、视频网站等等。

https://github.com/happyfish100/fastdfs

bfs:支撑Bilibili的小文件存储系统





实际需求：
120天前上传的文件”进行删除操作，以释放空间，请各位知悉。
