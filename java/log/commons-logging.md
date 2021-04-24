# commons-logging


common-io.PNG

Sprig日志库
core jar包pom.xml
org.apache.commons.logging.LogFactory
Spring是使用commons log，Log4j的



https://blog.csdn.net/aselidy/article/details/84721601

导入链接桥
<!-- Apache Commons Logging Bridge -->
<dependency>
<groupId>org.apache.logging.log4j</groupId>
<artifactId>log4j-jcl</artifactId>
<version>2.3</version>
</dependency>



additivity="false" 如果不配上，消息会被打印两遍，这个功能一般用不上，因此配置为false

