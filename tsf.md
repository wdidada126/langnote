# tsf

https://github.com/tencentyun/qcloud-documents


ps -aux | grep java
root     18892 73.8 13.1 2659196 247892 ?      Sl   09:26   0:25 java -Xshare:off -Xloggc:/data/tsf_apm/monitor/jvm-metrics/gclog.log -XX:+PrintGCDateStamps -XX:+PrintGCDetails -verbose:gc -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=8 -XX:GCLogFileSize=50M -javaagent:/root/tsf-agent/common/jvm-monitor/TencentCloudJvmMonitor-RELEASE.jar=hascontroller=true -Xms128m -Xmx512m -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=512m -jar /root/tsf-agent/repo/1254811207/application-apl3rkgv/20210414092315/spring-cloud-eureka-0.0.1.jar


新建集群不收费 普通版 专业版 铂金版
导入主机，需要自行购买


### FatJar
https://cloud.tencent.com/document/product/649/16934
FatJar 是一种可执行的 Jar 包（Executable Jar）。FatJar 和普通的 Jar 不同在于它包含了依赖的 Jar 包。

添加 FatJar 打包方式
在工程的 pom.xml 文件中添加插件：

<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
打包 FatJar 文件
添加完插件后，在工程的主目录下，使用 maven 命令 mvn clean package 进行打包，即可在 target 目录下找到打包好的 FatJar 文件。


### 推荐yaml配置格式

http://www.bejson.com/validators/yaml_editor/



腾讯云tsf是一款二次开发的框架
TSF 目前支持 Spring Cloud Edgware、Spring Cloud Finchley、Spring Cloud Greenwich 三个版本。Spring Cloud 、Spring Boot 及 TSF SDK 版本之间的关系如下表所示。
Spring Cloud	Spring Boot
Hoxton	2.2.x
Greenwich	2.1.x
Finchley	2.0.x
Edgware	1.5.x


#### tsf 长期维护 SDK 版本
SDK 版本号	新增特性
1.23.x	
新增 spring cloud gateway 微服务网关，链路追踪和调用监控
微服务网关路径重写配置和微信小程序登录插件
调用链支持 RocketMQ
1.21.x	
支持服务熔断
支持服务容错
支持全链路灰度发布
1.18.x	
支持微服务网关（zuul1 版）SDK，基于此 SDK 二次研发，无缝集成 TSF 平台服务治理能力
增加 swagger-ui 依赖包
调用链支持 MySQL JDBC、Redis、MongoDB、CMQ、Kafka
支持全局命名空间
新增自定义日志配置需要的 Converter 和 Layout 类，支持用户使用自定义 logback\log4j\log4j2 日志配置
1.12.x	
支持服务限流
支持服务路由
支持服务鉴权
支持分布式配置
支持调用链