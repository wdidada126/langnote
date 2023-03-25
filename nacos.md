# nacos



https://nacos.io/zh-cn/

windows



startup.cmd


https://blog.csdn.net/ljl19930522/article/details/124746908
 D：（nacos解压的盘符）
                                        cd D:\Java\nacos\bin   （nacos中bin文件的目录）
                                        startup.cmd -m standalone  （cluster是集群启动）
————————————————
版权声明：本文为CSDN博主「维涅斯」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ljl19930522/article/details/124746908

[windows下安装nacos](https://blog.csdn.net/q15102780705/article/details/102571353)



```shell
2020-04-29 16:51:22,579 INFO Exposing 2 endpoint(s) beneath base path '/actuator'

2020-04-29 16:51:22,653 INFO Initializing ExecutorService 'taskScheduler'

2020-04-29 16:51:22,865 INFO Tomcat started on port(s): 8848 (http) with context path '/nacos'

2020-04-29 16:51:22,897 INFO Nacos logs files: D:\nacos-server-1.2.1\nacos\logs\

2020-04-29 16:51:22,906 INFO Nacos conf files: D:\nacos-server-1.2.1\nacos\conf\

2020-04-29 16:51:22,907 INFO Nacos data files: D:\nacos-server-1.2.1\nacos\data\

2020-04-29 16:51:22,908 INFO Nacos started successfully in stand alone mode.

2020-04-29 16:51:23,128 INFO Initializing Servlet 'dispatcherServlet'

2020-04-29 16:51:23,165 INFO Completed initialization in 20 ms
```


### nacos api

服务注册&发现和配置管理
服务注册
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'

服务发现
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'

发布配置
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"

获取配置
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"

name service
config service

startup.cmd -m standalone



nacos 分布式部署 如何解决分布式一致性问题

Nacos如何实现Raft算法与Raft协议原理详解
https://blog.csdn.net/qq_34820803/article/details/107978204


https://my.oschina.net/u/3232343/blog/4347715

spring-cloud-starter-alibaba-nacos-config
spring-cloud-starter-alibaba-nacos-discovery

通过 Nacos Server 和 spring-cloud-starter-alibaba-nacos-config 实现配置的动态变更。
通过 Nacos Server 和 spring-cloud-starter-alibaba-nacos-discovery 实现服务的注册与发现。


通过 Nacos Server 和 nacos-config-spring-boot-starter 实现配置的动态变更；
通过 Nacos Server 和 nacos-discovery-spring-boot-starter 实现服务的注册与发现。




最近几年，各种新的高效序列化方式层出不穷，不断刷新序列化性能的上限，最典型的包括：

专门针对Java语言的：Kryo，FST等等
跨语言的：Protostuff，ProtoBuf，Thrift，Avro，MsgPack等等



ldap
https://docs.spring.io/spring-ldap/docs/1.3.2.RELEASE/reference/html/

