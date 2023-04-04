# activemq

./apache-activemq-5.12.2/bin/activemq console




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

ActiveMQ "Classic"  JMS 1.1
ActiveMQ Artemis    JMS 2.0