# jms

### jms
ActiveMQ "Classic"  JMS 1.1
ActiveMQ Artemis    JMS 2.0

https://gitee.com/edidada/testjmsbyactivemq
gitee repo

https://github.com/shuaicong/activemq

JMS

JMS即Java消息服务（Java Message Service）应用程序接口

https://www.cnblogs.com/JonaLin/p/11506013.html



https://www.oracle.com/technetwork/java/jms/index.html


https://mvnrepository.com/artifact/javax.jms/javax.jms-api/2.0.1

```xml
<dependency>
    <groupId>javax.jms</groupId>
    <artifactId>jms</artifactId>
    <version>1.1</version>
</dependency>
```


```xml
    <!-- Java JMS 原生API -->
    <dependency>
        <groupId>javax.jms</groupId>
        <artifactId>javax.jms-api</artifactId>
        <version>2.0</version>
    </dependency>
```

activemq
IBM WebSphere MQ

https://docs.oracle.com/javaee/6/tutorial/doc/bncdr.html
https://docs.oracle.com/javaee/7/api/javax/jms/package-summary.html


https://www.cnblogs.com/alter888/p/8974919.html


rocketmq支持jms
jboss支持jms？对


JBoss本身支持JMS(通过JNDI公布)，只需要在deploy/jms里配置相应xml文件，把Topic/Queue/ConnectionFactory配好即可，默认Jboss启动会在1099端口监听JMS消息。

https://blog.csdn.net/leimengyuanlian/article/details/46701305

官网
https://access.redhat.com/documentation/zh-cn/jboss_enterprise_application_platform/6.2/html/administration_and_configuration_guide/configure_jms_address_settings



### api

import javax.jms.Connection;
import javax.jms.JMSException;
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;


TextMessage (javax.jms)
    ActiveMQTextMessage (org.apache.activemq.command)
StreamMessage (javax.jms)
    ActiveMQStreamMessage (org.apache.activemq.command)
MapMessage (javax.jms)
    ActiveMQMapMessage (org.apache.activemq.command)
ObjectMessage (javax.jms)
    ActiveMQObjectMessage (org.apache.activemq.command)
BytesMessage (javax.jms)
    ActiveMQBytesMessage (org.apache.activemq.command)
Message (org.apache.activemq)
    BlobMessage (org.apache.activemq)
        ActiveMQBlobMessage (org.apache.activemq.command)
    ActiveMQMessage (org.apache.activemq.command)
        ActiveMQBytesMessage (org.apache.activemq.command)
        ActiveMQObjectMessage (org.apache.activemq.command)
        ActiveMQMapMessage (org.apache.activemq.command)
        ActiveMQStreamMessage (org.apache.activemq.command)
        ActiveMQBlobMessage (org.apache.activemq.command)
        ActiveMQTextMessage (org.apache.activemq.command)



### activemq jar包依赖

geronimo-jms_1.1_spec

没有依赖jsm-api这个jar包

Apache Geronimo所带jar包
Apache Geronimo是Apache软件基金会的开放源码J2EE服务器
Apache Geronimo is an open source server runtime that integrates the best open source projects to create Java/OSGi server runtime