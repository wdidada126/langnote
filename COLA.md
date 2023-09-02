# COLA

阿里开源的Cola框架的代码托管在GitHub上，地址为：https://github.com/alibaba/cola

Cola框架包括COLA微服务框架、COLA应用性能管理、COLA分布式事务中间件三个部分，主要适用于互联网和电商等高性能、高并发的场景。COLA微服务框架基于Spring Boot和Spring Cloud开发，支持快速搭建微服务应用；COLA应用性能管理提供分布式追踪、性能分析等功能，帮助开发者定位系统中的性能瓶颈；COLA分布式事务中间件基于TCC两阶段事务和可靠消息最终一致性协议，保证分布式事务的完整性。

阿里开源架构Cola4.0的项目
阿里高级技术专家谈开源DDD框架:COLA4.1,分离架构和组件(下)
cola 领域建模
基于COLA架构进行领域建模时，主要步骤包括：

<dependency>  
    <groupId>org.springframework.cloud</groupId>  
    <artifactId>spring-cloud-cola</artifactId>  
    <version>2.2.6.RELEASE</version>  
</dependency>

创建COLA微服务项目：可以选择使用Maven，并选择COLA项目模板来创建新的微服务项目。
定义领域模型：在领域建模中，需要先确定聚合根和实体，然后创建对应的领域模型。例如，在货物运输系统中，可以创建Voyage（航线）和CarrierMovement（运输过程）等实体类。
实现领域模型：在COLA框架中，可以使用Spring Boot和Spring Cloud等开发工具进行开发，包括适配层、应用层、领域层和基础设施层的代码开发。
防腐层设计：COLA 4.0引入了防腐层（ACL）的设计，用于防止领域模型被污染。
领域事件：COLA框架还支持领域事件，可以在领域模型发生变化时发布消息，实现异步通信和事件驱动架构。
通过以上步骤，基于COLA架构进行领域建模可以构建出复杂业务应用系统。



```
mvn archetype:generate  -DgroupId=cn.wdidada.cola -DartifactId=demo -Dversion=1.0.0-SNAPSHOT -Dpackage=cn.wdidada.cola.demo -DarchetypeArtifactId=cola-framework-archetype-web -DarchetypeGroupId=com.alibaba.cola -DarchetypeVersion=2.0.0
```



