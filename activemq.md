# activemq

./apache-activemq-5.12.2/bin/activemq console   windows版本好像不行，mac行

[官方下载地址](http://activemq.apache.org/download.html)

### 安装启动
- 第一步：把ActiveMQ 的压缩包上传到Linux系统
- 第二步：解压缩
- 第三步：启动
```
使用bin目录下的activemq命令启动：
[root@localhost bin]# ./activemq start
关闭：
[root@localhost bin]# ./activemq stop
查看状态：
[root@localhost bin]# ./activemq status

进入管理后台：http://IP:8161/admin
用户名：admin
密码：admin
```

登录用户名密码可在 `conf/jetty-realm.properties` 文件中修改



Tasks provided by the sysv init script:
    kill            - terminate instance in a drastic way by sending SIGKILL
    restart         - stop running instance (if there is one), start new instance
    console         - start broker in foreground, useful for debugging purposes
    status          - check if activemq process is running


编程语言java
https://github.com/apache/activemq

https://activemq.apache.org/maven/apidocs/
https://activemq.apache.org/components/classic/documentation
https://activemq.apache.org/


activemq-cpp


2019年 ActiveMQ-CPP v3.9.5 Released


git clone https://gitbox.apache.org/repos/asf/activemq-cpp.git
cd activemq-cpp
git checkout tags/3.9.5

http://127.0.0.1:8161/


61616

activeMQ默认配置下启动会启动8161和61616两个端口，其中8161是mq自带的管理后台的端口，61616是mq服务默认端口 。
8161是后台管理系统，61616是给java用的tcp端口。

https://blog.csdn.net/u010994966/article/details/77895374


### jar包依赖

geronimo-jms_1.1_spec

没有依赖jsm-api这个jar包

Apache Geronimo所带jar包
Apache Geronimo是Apache软件基金会的开放源码J2EE服务器
Apache Geronimo is an open source server runtime that integrates the best open source projects to create Java/OSGi server runtime



### jsm api

- ObjectMessage
- TextMessage


Queue createQueue(String queueName)
Topic createTopic(String topicName)

activemq topic queue区别

Topic用于消息订阅 pub sub,属于一对多;Queue用于消息处理,属于一对一。


ActiveMQ的Queue与Topic区别.png
