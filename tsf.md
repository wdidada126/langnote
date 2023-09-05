# tsf


# 分布式事务 DTF

分布式事务（Distributed Transaction Framework，DTF）是腾讯云自主研发的高性能、高可用的分布式事务中间件，用于提供分布式的场景中，特别是微服务架构下的事务一致性服务。分布式事务 DTF 拥抱 Spring Cloud、Spring Boot 开发框架

https://cloud.tencent.com/document/product/1224/45969#.E4.B8.8E-tsf-.E7.BB.93.E5.90.88.E4.BD.BF.E7.94.A8
TCC 模式 Spring Boot 开发
TCC 模式 Spring Free 开发
FMT 模式 Spring Boot 开发
Saga 模式 Spring Boot 开发
Saga 模式 Spring Free 开发


@EnableTsf

@EnableDtf

工作流 金融

不是用的hystrix
dubbo-hystrix

自研的？也有可能使用k8s的
限流 每秒多少次
熔断 集群 实例 接口

在ECS实例上部署应用。每个ECS实例上只能部署一个应用。

用户可通过两种方式更新代码中的配置信息：使用配置类@ConfigurationProperties和@Value注解。@Value比较适用于配置比较少的场景，而@ConfigurationProperties则更适用于有较多配置的情况。
用户也可以动态更新应用配置文件（如 application.yml）中的配置，如动态更改 redis 的地址或者鉴权功能开关等。


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


虚拟机部署
容器部署
容器部署需要使用docker
需要设置docker账户密码
用户名系统提供了100002010298
密码设置成5Edidada


登录腾讯云docker registry
sudo docker login --username=100002010298  ccr.ccs.tencentyun.com

从registry拉取镜像
sudo docker pull ccr.ccs.tencentyun.com/tsf_100002010298/register:[tag]


将镜像推送到registry
sudo docker login --username=100002010298  ccr.ccs.tencentyun.com
sudo docker tag [ImageId] ccr.ccs.tencentyun.com/tsf_100002010298/register:[tag]
sudo docker push ccr.ccs.tencentyun.com/tsf_100002010298/register:[tag]


git@github.com/edidada/SpringEurekaDockerDemo


docker tag 05358ed3a675 ccr.ccs.tencentyun.com/tsf_100002010298/register:0.0.1-SNAPSHOT
docker push ccr.ccs.tencentyun.com/tsf_100002010298/register:0.0.1-SNAPSHOT

docker push edidada/spring-cloud-eureka:0.0.2



将镜像推送到registry

复制sudo docker login --username=100002010298 ccr.ccs.tencentyun.com复制sudo docker tag [ImageId] ccr.ccs.tencentyun.com/tsf_100002010298/edidadaspringcloudeureka:[tag]复制sudo docker push ccr.ccs.tencentyun.com/tsf_100002010298/edidadaspringcloudeureka:[tag]
其中[ImageId]请根据您的实际镜像ID信息进行填写，[tag]请根据您的镜像版本信息进行填写


一个是docker login
version
tag 别名
imageid
containid
push/pull
跟git对比


docker tag 1f6277a9518e ccr.ccs.tencentyun.com/tsf_100002010298/edidadaspringcloudeureka:0.0.2
docker push ccr.ccs.tencentyun.com/tsf_100002010298/edidadaspringcloudeureka:0.0.2


docker tag b21522bdfabc ccr.ccs.tencentyun.com/tsf_100002010298/customer:0.0.1-SNAPSHOT
docker push ccr.ccs.tencentyun.com/tsf_100002010298/customer:0.0.1-SNAPSHOT


### sdk

https://cloud.tencent.com/document/product/649/20231


### demo

https://github.com/tencentyun/tsf-simple-demo



如果您希望使用 TSF 文件配置 功能，则需要在 Dockerfile 中增加文件配置组件 tsf-consul-template-docker.tar.gz（下载地址），然后在 CMD 启动命令中启动该组件。

```shell
FROM centos:7
RUN echo "ip_resolve=4" >> /etc/yum.conf
RUN yum update -y && yum install -y java-1.8.0-openjdk
# 设置时区。这对于日志、调用链等功能能否在 TSF 控制台被检索到非常重要。
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
ENV workdir /app/
# 下面的 jar 包可替换为您的 Spring Cloud 应用 jar包，注意这个 jar 包要和您的 dockerfile 位于同一级目录
ENV jar provider-demo-0.0.1-SNAPSHOT.jar
COPY ${jar} ${workdir}
WORKDIR ${workdir}
# tsf-consul-template-docker 用于文件配置功能，如不需要可注释掉该行
ADD tsf-consul-template-docker.tar.gz /root/
# JAVA_OPTS 环境变量的值为部署组的 JVM 启动参数，在运行时 bash 替换。使用 exec 以使 Java 程序可以接收 SIGTERM 信号。
CMD ["sh", "-ec", "sh /root/tsf-consul-template-docker/script/start.sh; exec java ${JAVA_OPTS} -jar ${jar}"]
```

    <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
    </plugin>

fastjar


.tsf/discovery/目录
provider-demo.cache文件

```shell
{
  "statusCode" : 200,
  "statusMessage" : "OK",
  "content" : [ {
    "node" : {
      "id" : "050cc805-dae5-b71e-5383-f9fb266967b1",
      "node" : "Wdidada",
      "address" : "127.0.0.1",
      "datacenter" : "dc1",
      "taggedAddresses" : {
        "lan" : "127.0.0.1",
        "lan_ipv4" : "127.0.0.1",
        "wan" : "127.0.0.1",
        "wan_ipv4" : "127.0.0.1"
      },
      "meta" : {
        "consul-network-segment" : ""
      },
      "createIndex" : 11,
      "modifyIndex" : 12
    },
    "service" : {
      "id" : "provider-demo-18081",
      "service" : "provider-demo",
      "tags" : [ "secure=false" ],
      "address" : "192.168.137.1",
      "meta" : {
        "TSF_APPLICATION_ID" : "",
        "TSF_GROUP_ID" : "",
        "TSF_INSTNACE_ID" : "",
        "TSF_PROG_VERSION" : "",
        "TSF_REGION" : "",
        "TSF_SDK_VERSION" : "1.23.0-Greenwich-RELEASE",
        "TSF_ZONE" : ""
      },
      "port" : 18081,
      "enableTagOverride" : false,
      "createIndex" : 19,
      "modifyIndex" : 19
    },
    "checks" : [ {
      "node" : "Wdidada",
      "checkId" : "serfHealth",
      "name" : "Serf Health Status",
      "status" : "PASSING",
      "notes" : "",
      "output" : "Agent alive and reachable",
      "serviceId" : "",
      "serviceName" : "",
      "serviceTags" : [ ],
      "createIndex" : 11,
      "modifyIndex" : 11
    }, {
      "node" : "Wdidada",
      "checkId" : "service:provider-demo-18081",
      "name" : "Service 'provider-demo' check",
      "status" : "PASSING",
      "notes" : "",
      "output" : "",
      "serviceId" : "provider-demo-18081",
      "serviceName" : "provider-demo",
      "serviceTags" : [ "secure=false" ],
      "createIndex" : 19,
      "modifyIndex" : 98
    } ]
  } ],
  "consulIndex" : 98,
  "consulKnownLeader" : true,
  "consulLastContact" : 0,
  "updateTime" : 1618819465772
}
```


腾讯云TSF(Tencent Serverless Framework)支持的配置中心主要有:

1. TSF CONFIG:TSF框架自带的配置中心

基于TSF的配置组件,可以非常方便地管理服务的配置。

2. Apollo: 阿波罗配置中心

阿波罗配置中心是专门用于分布式系统的配置中心,与TSF框架天然集成。

3. Cloud Config: 腾讯云配置中心

腾讯云提供的云上配置中心服务。

TSF可将Cloud Config与应用无缝对接。

4. 使用其他第三方配置中心

TSF支持以插件的形式,集成其他配置中心,比如:

- Nacos 
- Spring Cloud Config 
- HashiCorp Consul
通过TSF插件机制,可以使用第三方配置中心。

这几种配置中心在TSF中的优缺点:

- TSF CONFIG:
  - 优点:内置,易用
  - 缺点:管理功能较一般

- Apollo:
  - 优点:功能全面丰富
  - 缺点:需要额外安装和部署

- Cloud Config:
  - 优点:与腾讯云其他产品集成好
  - 缺点:需要付费使用  
总的来说,腾讯云TSF主要支持三种配置中心,以及通过插件实现的其他第三方配置中心。

希望上述内容能为你解读TSF支持的配置中心!如还有其他疑问,欢迎继续补充。
