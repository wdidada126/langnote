# Spring Cloud



## spring cloud作用



springmvc开发http接口

spring boot starter web快速开发http接口



sping cloud 一整套企业级服务

微服务http调用 分布式追踪，注册中心，配置中心，分布式事务 网关

国内 阿里 腾讯 华为 卖云服务的，都有一套基于spring cloud的框架



之前是netfix主导的



腾讯云 阿里云都有类似的微服务框架


 Spring Cloud
 Finchley
Spring Cloud	Spring Boot
Angel版本	兼容Spring Boot 1.2.x
Brixton版本	兼容Spring Boot 1.3.x，也兼容Spring Boot 1.4.x
Camden版本	兼容Spring Boot 1.4.x，也兼容Spring Boot 1.5.x
Dalston版本、Edgware版本	兼容Spring Boot 1.5.x，不兼容Spring Boot 2.0.x
Finchley版本	兼容Spring Boot 2.0.x，不兼容Spring Boot 1.5.x
Greenwich版本	兼容Spring Boot 2.1.x
Hoxtonl版本	兼容Spring Boot 2.2.x

SpringBoot与SpringCloud的版本对应详细版
https://blog.csdn.net/qq32933432/article/details/89375630



史上最简单的SpringCloud教程 | 第二篇: 服务消费者（rest+ribbon）

https://blog.csdn.net/forezp/article/details/69788938




从Alibaba提供Spring Alibaba来看，国内在Spring使用上还是很强大的



BeanDefinitionParserDelegate dbpd;
DefaultDocumentLoader defaultDocumentLoader;

new project how to integert to Spring Cloud?



spring



xml文件定义${}变量，如何替换掉



aoutconfig maven插件是生成properties插件



从Alibaba提供Spring Alibaba来看，国内在Spring使用上还是很强大的



BeanDefinitionParserDelegate dbpd;
DefaultDocumentLoader defaultDocumentLoader;

`BeanDefinitionParserDelegate`是Spring框架内部的一个关键类，用于解析和处理XML配置文件中的bean定义。

它的主要作用如下：

1. 解析bean定义：`BeanDefinitionParserDelegate`负责解析XML配置文件中的bean定义，并将其转换为Spring框架内部的数据结构，即`BeanDefinition`对象。它会根据配置文件中的元素和属性，构建相应的`BeanDefinition`对象，包括bean的名称、类型、属性、依赖关系等信息。

2. 处理命名空间：Spring框架支持使用命名空间扩展XML配置文件的功能，而`BeanDefinitionParserDelegate`负责处理这些命名空间。它会根据不同的命名空间，调用相应的处理器来解析和处理扩展元素。

3. 处理属性值：`BeanDefinitionParserDelegate`会处理配置文件中bean的属性值，包括字面值、引用值、占位符等。它会根据配置文件中的不同写法，将属性值解析为相应的对象，如字符串、引用、表达式等。

4. 处理嵌套标签：`BeanDefinitionParserDelegate`支持处理XML配置文件中的嵌套标签，如构造函数参数、集合属性、内部bean等。它会递归地解析和处理这些嵌套标签，确保bean定义的完整性和准确性。

总的来说，`BeanDefinitionParserDelegate`在Spring框架的XML配置文件解析过程中扮演了重要的角色，负责解析和处理bean定义的各个方面，将配置文件转化为Spring框架内部可操作的数据结构。它为Spring的IoC容器提供了必要的元数据信息，以便正确地创建和管理应用程序中的bean实例。


`DefaultDocumentLoader`是Spring框架中用于加载和解析XML文档的默认实现类。

它的主要作用如下：

1. 加载XML文档：`DefaultDocumentLoader`负责加载XML文档并创建对应的`Document`对象。它使用JAXP（Java API for XML Processing）提供的API，通过解析器将XML文档转换为DOM（Document Object Model）树结构。

2. 解析XML文档：一旦XML文档加载完成，`DefaultDocumentLoader`会对文档进行解析，将其转换为内部的表示形式。它会识别XML中的元素、属性、命名空间等，并将其映射为Spring框架内部的数据结构，如`BeanDefinition`、`PropertyValue`等。

3. 处理命名空间：`DefaultDocumentLoader`还负责处理XML文档中的命名空间。它会解析文档中的命名空间声明，并注册相应的命名空间处理器，以便在解析过程中处理扩展的XML元素。

4. 处理DTD和Schema验证：如果XML文档定义了DTD（Document Type Definition）或Schema验证，`DefaultDocumentLoader`会根据相应的规范进行验证。它会检查XML文档的结构和内容，确保其符合定义的规则和约束。

总的来说，`DefaultDocumentLoader`是Spring框架中负责加载和解析XML文档的核心组件。它将XML文档转换为Spring框架内部可操作的数据结构，为后续的处理过程提供必要的元数据信息。通过`DefaultDocumentLoader`，Spring能够有效地读取和理解XML配置文件，实现IoC容器的构建和配置。


new project how to integert to Spring Cloud?



spring



xml文件定义${}变量，如何替换掉
spel表达式


aoutconfig maven插件是生成properties插件

## 源代码



https://cloud.spring.io/



[spring-cloud/spring-cloud-commons: Common classes used in different Spring Cloud implementations (github.com)](https://github.com/spring-cloud/spring-cloud-commons)



v2.2.5.RELEASE



spring-cloud-commons

spring-cloud-commons-dependencies

spring-cloud-context
spring-cloud-netflix-archaius
spring-cloud-netflix-ribbon
spring-cloud-starter

spring-cloud-starter-loadbalancer

spring-cloud-loadbalancer







https://github.com/alibaba/spring-cloud-alibaba



https://github.com/spring-cloud/spring-cloud-config



https://github.com/spring-cloud/spring-cloud-openfeign



v2.2.5.RELEASE



maven构建的



spring-cloud-openfeign-core api doc网址？

https://docs.spring.io/spring-cloud-openfeign/docs/3.1.8/reference/html/



spring-cloud-openfeign-dependencies



```xml
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot-dependencies.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring.cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>com.alibaba.cloud</groupId>
                <artifactId>spring-cloud-alibaba-dependencies</artifactId>
                <version>${spring-cloud-alibaba.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
```





## 源代码分包解析




spring-cloud-commons

spring-cloud-commons-dependencies

spring-cloud-context

BootstrapPropertySource<T>
org.springframework.cloud.bootstrap.config.BootstrapPropertySource 

spring-cloud-netflix-archaius
spring-cloud-netflix-ribbon
spring-cloud-starter

spring-cloud-starter-loadbalancer

spring-cloud-loadbalancer