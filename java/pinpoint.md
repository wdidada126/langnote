# pinpoint

架构
HBase (用于存储数据)
Pinpoint Collector (信息的收集者，部署在tomcat中)
Pinpoint Web (提供WEB_UI界面，部署在tomcat中)
Pinpoint Agent (附加到 java 应用来做采样)

韩国人开发的

*Naver*公司(*Naver* Corporation)是一家韩国互联网内容服务运营商

http://naver.github.io/pinpoint/ 这个网页不存在了

https://www.oschina.net/p/pinpoint
Pinpoint 应用性能管理工具

Java 开发的 编程语言
https://github.com/pinpoint-apm/pinpoint

中文资料：https://legacy.gitbook.com/book/skyao/learning-pinpoint/details

[pinpoint插件开发之二：从零开始新建一个插件](https://blog.csdn.net/boling_cavalry/article/details/78568073)

[Pinpoint 插件开发](https://juejin.im/post/5b0a4afaf265da0dd110cce5)

公司是基于pinpoint开发的监控系统

[pinpoint](https://github.com/naver/pinpoint)

APM, (Application Performance Management) tool for large-scale distributed systems written in Java. 

Java程序启动参数 agent 非侵入

现在支持php

部署pinpoint节点步骤：

明确节点host，全为linux系统

pinpoint部署应用名	ip
mbp-launch	172.22.186.128
通过性能跳板机
在/tools目录下建立目录pp-agent: mkdir pp-agent
上传agent的jar包，jar包在跳板机 D:\pp-agent
解压jar包：unzip pinpoint-agent-1.7.2-SNAPSHOT.zip
在/tools/jetty/bin/env.sh文件添加下面的参数（agentId唯一、applicationName选应用名）：-javaagent:/tools/pp-agent/pinpoint-bootstrap-1.7.2-SNAPSHOT.jar -Dpinpoint.agentId=pp201803131837 -Dpinpoint.applicationName=mbp-launch
重启jetty: sh /tools/jetty/bin/jetty.sh restart 



[全链路监控工具-Pinpoint之插件开发](https://www.sohu.com/a/200888410_659464)



[pinpoint 插件开发实战](https://blog.csdn.net/devotedwife/article/details/81877210)



https://blog.csdn.net/zgliang88/article/details/83279557



dapper

https://bigbully.github.io/Dapper-translation/





Dapper, a Large-Scale Distributed Systems Tracing Infrastructure



https://research.google/pubs/pub36356/

https://skyao.gitbooks.io/learning-pinpoint/

https://github.com/olivere/dapper

windows

C:\Users\edidada\Downloads\learning-pinpoint.pdf