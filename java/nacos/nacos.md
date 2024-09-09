# nacos

屹通用2.2.3

配置中心竞品
super-diamond
https://github.com/melin/super-diamond
截止2023年，5年没更新了

nacos有配置文件，debug的时候配置文件在哪儿？

Spring cloud alibaba nacos，默认dataID nacos-service.properties修改成自定义值

如果你想将Spring Cloud Alibaba Nacos中默认的 `dataId`（即 `nacos-service.properties`）修改为自定义的值，你可以在 `bootstrap.properties`或 `bootstrap.yml`文件中配置 `spring.cloud.nacos.config.prefix`和 `spring.cloud.nacos.config.file-extension`属性。

具体来说，你可以将 `spring.cloud.nacos.config.prefix`设置为你想要的 `dataId`前缀，将 `spring.cloud.nacos.config.file-extension`设置为你想要的扩展名。例如，你可以在 `bootstrap.yml`中添加以下配置：

```
spring:
  cloud:
    nacos:
      config:
        prefix: my-service-config
        file-extension: properties
```

在这个配置中，`prefix`属性指定了 `dataId`的前缀为 `my-service-config`，`file-extension`属性指定了 `dataId`的扩展名为 `properties`。这将会使Spring Cloud Alibaba Nacos使用 `my-service-config.properties`作为服务的元数据信息文件。

需要注意的是，如果你修改了 `dataId`，你需要在Nacos控制台上创建对应的配置文件，并将服务的元数据信息保存到这个文件中。例如，如果你将 `dataId`修改为 `my-service-config.properties`，那么你需要在Nacos控制台上创建一个名为 `my-service-config.properties`的配置文件，并将服务的元数据信息保存到这个文件中。

总之，如果你想将Spring Cloud Alibaba Nacos中默认的 `dataId`修改为自定义的值，你可以在 `bootstrap.properties`或 `bootstrap.yml`文件中配置 `spring.cloud.nacos.config.prefix`和 `spring.cloud.nacos.config.file-extension`属性。需要注意的是，如果你修改了 `dataId`，你需要在Nacos控制台上创建对应的配置文件，并将服务的元数据信息保存到这个文件中。

注意，nacos配置中心的设置，在applicaion.yml中设置不生效，在在 `bootstrap.properties`或 `bootstrap.yml`中设置才生效
注意，nacos配置中心的设置，在applicaion.yml中设置不生效，在在`bootstrap.properties`或`bootstrap.yml`中设置才生效

默认端口号：8848

https://gitee.com/edidada/nacos-config-example

https://gitee.com/edidada/springcloudnacosdemo

https://gitee.com/edidada/testnacosclient

## 官网

https://nacos.io/zh-cn/

## windows启动nacos server

startup.cmd

source code
https://github.com/alibaba/nacos
https://gitter.im/alibaba/nacos

https://github.com/edidada/nacos.git

1.4.2
cd C:\Users\admin\Documents\GitHub\nacos
git checkout 1.4.2

mvn -Prelease-nacos -Dmaven.test.skip=true install -U
```shell
Error:  Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:3.2.2:repackage (default) on project nacos-console: Execution default of goal org.springframework.boot:spring-boot-maven-plugin:3.2.2:repackage failed: Unable to load the mojo 'repackage' in the plugin 'org.springframework.boot:spring-boot-maven-plugin:3.2.2' due to an API incompatibility: org.codehaus.plexus.component.repository.exception.ComponentLookupException: org/springframework/boot/maven/RepackageMojo has been compiled by a more recent version of the Java Runtime (class file version 61.0), this version of the Java Runtime only recognizes class file versions up to 55.0
```

Java写的项目

用了jraft

nacos client版本需要跟nacos server版本相同？
对
困扰了我一天
nacos github上有版本兼容性相关的描述？

https://blog.csdn.net/ljl19930522/article/details/124746908
D：（nacos解压的盘符）

（nacos中bin文件的目录）
（cluster是集群启动）

```powshell
chcp 65001
cd F:\nacos-server-2.2.0\bin
./startup.cmd -m standalone
```

1.41最低要求java8

quanyi健康用nacos 1.40

Windows 10电脑，nacos数据源配置成mysql的

[windows下安装nacos](https://blog.csdn.net/q15102780705/article/details/102571353)

Tomcat started on port(s): 8848 (http) with context path '/nacos'

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

## nacos library

```xml
    <dependency>
      <groupId>com.alibaba.nacos</groupId>
      <artifactId>nacos-client</artifactId>
      <version>1.4.2</version>
    </dependency>
```

endpoint 是啥？
服务发现的

docker pull nacos/nacos-server:1.4.0
docker run -d -p 8848:8848 -e MODE=standalone -e PREFER_HOST_MODE=hostname --name nacos nacos/nacos-server:1.4.0

## nacos api

服务注册&发现和配置管理
服务注册
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'

服务发现
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'

发布配置
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"

获取配置
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"

nacos/v1/cs/
nacos/v1/ns/
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

http://192.168.56.1:8848/nacos

用户名密码默认都是：nacos 不是admin

最近几年，各种新的高效序列化方式层出不穷，不断刷新序列化性能的上限，最典型的包括：
专门针对Java语言的：Kryo，FST等等
跨语言的：Protostuff，ProtoBuf，Thrift，Avro，MsgPack等等

### nacos源码解析

com.alibaba.cloud.nacos.NacosConfigManager

如何发起http请求，如何接收nacos server的推送
push pull？

Nacos 配置中心支持push和pull两种方式来获取配置。

Pull模式：客户端主动从Nacos服务器拉取配置信息。在这种模式下，客户端需要周期性地轮询Nacos服务器，以便及时得到配置变化。
Push模式：Nacos服务器将配置信息推送给客户端，客户端需要开启一个长连接并订阅指定的配置集，一旦配置发生变化，Nacos服务器会立即推送变更信息给客户端。这种模式下客户端只需要在启动时订阅一次，就可以实现实时更新配置。
推荐使用push模式，因为它能够及时地将配置变化推送给客户端，避免了客户端轮询带来的网络和服务器资源浪费。

如何查看nacos是pull还是push

如果你想要查看你的Java Nacos程序是采用的哪种模式，可以检查你的程序代码中注册监听器的方式。如果使用了 @NacosConfigListener 注解，则是采用了 push 模式。如果是通过轮询访问 Nacos 配置中心的 HTTP 接口或者使用 Nacos 客户端 SDK 进行轮询，则是采用了 pull 模式。

spring-cloud-alibaba-nacos-config程序是push还是pull
spring-cloud-alibaba-nacos-config程序是通过pull方式获取配置的。Nacos配置中心的服务端源码主要在nacos-config项目的ConfigController类，服务端的逻辑要比客户端稍复杂一些，处理长轮询，服务端对外提供的监听接口地址 /v1/cs/configs/listener，这个方法内容不多，顺着 doPollingConfig 往下看。
https://developer.aliyun.com/article/785050

Nacos配置中心的服务端源码主要在nacos-config项目的ConfigController类，服务端的逻辑要比客户端稍复杂一些，这里我们重点看下。

com.alibaba.nacos.client.config.NacosConfigService

private final AtomicReference<Map<String, CacheData>> cacheMap = new AtomicReference<Map<String, CacheData>>(new HashMap<>());

获取配置

Nacos获取配置数据的逻辑比较简单，先取本地快照文件中的配置，如果本地文件不存在或者内容为空，则再通过HTTP请求从远端拉取对应dataId配置数据，并保存到本地快照中，请求默认重试3次，超时时间3s。
com.alibaba.nacos.client.config.NacosConfigService#getConfig

spring-cloud-alibaba-nacos-config程序默认访问的dataid和group
spring-cloud-alibaba-nacos-config程序默认访问的dataid和group是由spring.application.name和spring.cloud.nacos.config.group组成的。如果没有明确指定spring.cloud.nacos.config.group配置的情况下，默认使用的是DEFAULT_GROUP。
https://developer.aliyun.com/article/897341

spring.cloud.nacos.config.name作用是指定要读取的配置文件的Data ID，如果没有指定读取的dataid，那么默认是读取的是微服务名相同的.yml配置节的信息。

支持profile粒度的配置
spring-cloud-starter-alibaba-nacos-config 在加载配置的时候，不仅仅加载了以 dataid 为 {spring.application.name}.{file-extension:properties} 为前缀的基础配置，还加载了dataid为 {spring.application.name}-{profile}.{file-extension:properties} 的基础配置。在日常开发中如果遇到多套环境下的不同配置，可以通过Spring 提供的 {spring.profiles.active} 这个配置项来配置。
spring.profiles.active=develop
profile 的配置文件 大于 默认配置的文件。 并且形成互补
支持自定义 namespace 的配置
用于进行租户粒度的配置隔离。不同的命名空间下，可以存在相同的 Group 或 Data ID 的配置。Namespace 的常用场景之一是不同环境的配置的区分隔离，例如开发测试环境和生产环境的资源（如配置、服务）隔离等。
在没有明确指定${spring.cloud.nacos.config.namespace}配置的情况下， 默认使用的是 Nacos 上 Public 这个namespae。如果需要使用自定义的命名空间，可以通过以下配置来实现：
spring.cloud.nacos.config.namespace=b3404bc0-d7dc-4855-b519-570ed34b62d7
支持自定义 Group 的配置
Group是组织配置的维度之一。通过一个有意义的字符串（如 Buy 或 Trade ）对配置集进行分组，从而区分 Data ID 相同的配置集。当您在 Nacos 上创建一个配置时，如果未填写配置分组的名称，则配置分组的名称默认采用DEFAULT_GROUP 。
配置分组的常见场景：不同的应用或组件使用了相同的配置类型，如 database_url 配置和MQ_topic 配置。
在没有明确指定 ${spring.cloud.nacos.config.group} 配置的情况下， 默认使用的是 DEFAULT_GROUP 。如果需要自定义自己的 Group，可以通过以下配置来实现：
spring.cloud.nacos.config.group=DEVELOP_GROUP
支持自定义扩展的 Data Id 配置
Data ID 是组织划分配置的维度之一。Data ID 通常用于组织划分系统的配置集。一个系统或者应用可以包含多个配置集，每个配置集都可以被一个有意义的名称标识。Data ID 通常采用类 Java 包（如 com.taobao.tc.refund.log.level）的命名规则保证全局唯一性。此命名规则非强制。
通过自定义扩展的 Data Id 配置，既可以解决多个应用间配置共享的问题，又可以支持一个应用有多个配置文件。
spring.application.name=opensource-service-provider
spring.cloud.nacos.config.server-addr=127.0.0.1:8848

## config external configuration

### 1、Data Id 在默认的组 DEFAULT_GROUP,不支持配置的动态刷新

spring.cloud.nacos.config.extension-configs[0].data-id=ext-config-common01.properties

### 2、Data Id 不在默认的组，不支持动态刷新

spring.cloud.nacos.config.extension-configs[1].data-id=ext-config-common02.properties
spring.cloud.nacos.config.extension-configs[1].group=GLOBALE_GROUP

### 3、Data Id 既不在默认的组，也支持动态刷新

spring.cloud.nacos.config.extension-configs[2].data-id=ext-config-common03.properties
spring.cloud.nacos.config.extension-configs[2].group=REFRESH_GROUP
spring.cloud.nacos.config.extension-configs[2].refresh=true
可以看到:
• 通过 spring.cloud.nacos.config.extension-configs[n].data-id 的配置方式来支持多个 Data Id 的配置。
• 通过 spring.cloud.nacos.config.extension-configs[n].group 的配置方式自定义 Data Id 所在的组，不明确配置的话，默认是 DEFAULT_GROUP。
• 通过 spring.cloud.nacos.config.extension-configs[n].refresh 的配置方式来控制该 Data Id 在配置变更时，是否支持应用中可动态刷新， 感知到最新的配置值。默认是不支持的。
多个 Data Id 同时配置时，它的优先级关系是 spring.cloud.nacos.config.extension-configs[n].data-id 其中 n 的值越大，优先级越高。
spring.cloud.nacos.config.extension-configs[n].data-id 的值必须带文件扩展名，文件扩展名既可支持 properties，又可以支持 yaml/yml。
此时 spring.cloud.nacos.config.file-extension 的配置对自定义扩展配置的 Data Id 文件扩展名没有影响。
通过自定义扩展的 Data Id 配置，既可以解决多个应用间配置共享的问题，又可以支持一个应用有多个配置文件。
通过自定义扩展的 Data Id 配置，既可以解决多个应用间配置共享的问题，又可以支持一个应用有多个配置文件。
为了更加清晰的在多个应用间配置共享的 Data Id ，你可以通过以下的方式来配置：

### 配置支持共享的 Data Id

spring.cloud.nacos.config.shared-configs[0].data-id=common.yaml

### 配置 Data Id 所在分组，缺省默认 DEFAULT_GROUP

spring.cloud.nacos.config.shared-configs[0].group=GROUP_APP1

### 配置Data Id 在配置变更时，是否动态刷新，缺省默认 false

spring.cloud.nacos.config.shared-configs[0].refresh=true
可以看到：
通过 spring.cloud.nacos.config.shared-configs[n].data-id 来支持多个共享 Data Id 的配置。
通过 spring.cloud.nacos.config.shared-configs[n].group 来配置自定义 Data Id 所在的组，不明确配置的话，默认是 DEFAULT_GROUP。
通过 spring.cloud.nacos.config.shared-configs[n].refresh 来控制该Data Id在配置变更时，是否支持应用中动态刷新，默认false。
配置的优先级
Spring Cloud Alibaba Nacos Config 目前提供了三种配置能力从 Nacos 拉取相关的配置。
• A: 通过 spring.cloud.nacos.config.shared-configs[n].data-id 支持多个共享 Data Id 的配置
• B: 通过 spring.cloud.nacos.config.extension-configs[n].data-id 的方式支持多个扩展 Data Id 的配置
• C: 通过内部相关规则(应用名、应用名+ Profile )自动生成相关的 Data Id 配置
当三种方式共同使用时，他们的一个优先级关系是:A < B < C
完全关闭配置
通过设置 spring.cloud.nacos.config.enabled = false 来完全关闭 Spring Cloud Nacos Config

spring.cloud.nacos.config项目配置使用properties还是yml根据什么配置项
在Spring Cloud Alibaba Nacos中，Nacos Config除了支持.properties格式以外，也支持yaml格式。在客户端配置中，可以在bootstrap.properties文件中使用spring.cloud.nacos.config.file-extension属性声明从配置中心中读取的配置文件格式。该配置的缺省值为properties，即默认是读取properties格式的配置文件

nacos的dataId invalid报错如何解决
Nacos的dataId invalid报错可能是由于dataId不合法，例如包含了特殊字符或者长度超过了限制。另外，也有可能是由于Nacos server没有正确地配置。

=mytest不行
测试程序

```java
import com.alibaba.nacos.client.config.utils.ParamUtils;

public class ParamUtilsMain {
    public static void main(String[] args) {
        boolean isvalid = ParamUtils.isValid("mytest");
        System.out.println(isvalid);
    }
}
```

Nacos支持CP+AP模式，即Nacos可以根据配置识别为CP模式或AP模式，默认是AP模式。如果注册Nacos的client节点注册时ephemeral=true，那么Nacos集群对这个client节点的效果就是AP，采用distro协议实现；而注册Nacos的client节点注册时ephemeral=false，那么Nacos集群对这个节点的效果就是CP的，采用raft协议实现。根据client注册时的属性，AP，CP同时混合存在，只是对不同的client节点效果不同。Nacos可以很好的解决不同场景的业务需求。
协议介绍
distro协议
1、阿里自研发
2、保证cp，保证最终一致性。

Nacos 每个节点是平等的都可以处理写请求，同时把新数据同步到其他节点。
每个节点只负责部分数据，定时发送自己负责数据的校验值到其他节点来保持数据一致性。
每个节点独立处理读请求，及时从本地发出响应。

nacos配置单个文件的

### nacos server源代码解析

http接口

- /v1/cs  com.alibaba.nacos.config.server.controller.ConfigController#publishConfig
- /v1/auth/users/login?username=nacos

## docker部署nacos集群
