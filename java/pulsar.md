# pulsar

是的，Apache Pulsar是一个分布式的消息和流处理平台，与传统的消息队列系统不同，Pulsar采用了存储和计算分离的架构。

在传统的消息队列系统中，存储和计算通常是耦合在一起的。消息被写入队列后，存储和计算都在同一个节点上进行处理。这种架构在规模较小的系统中效果良好，但在大规模系统中可能会面临扩展性和性能的挑战。

Pulsar通过将存储和计算分离，实现了更高的可扩展性和灵活性。消息被写入持久化的存储层（称为存储服务），而计算逻辑（如消费者）则可以从存储服务中读取消息进行处理。存储服务可以横向扩展以处理大规模的数据量，而计算节点可以根据需要进行动态伸缩。

这种分离的架构带来了一些好处：
- 可以独立扩展存储和计算能力，根据需求分别进行优化和调整。
- 存储和计算节点可以部署在不同的硬件或云环境中，提供更大的灵活性和弹性。
- 可以实现多租户的架构，不同的租户可以共享相同的存储服务而独立进行计算。
总体而言，Pulsar的存储和计算分离架构为构建大规模、高可扩展性的消息和流处理系统提供了更好的基础。

https://pulsar.apache.org/

https://github.com/apache/pulsar

Java写的

## 版本

3.0.0 2023.04发布

pulsar-2.2.0                2018-10-23 22:58  
pulsar-2.2.1                2018-12-24 20:13  
pulsar-2.3.0                2019-02-21 05:04  
pulsar-2.3.1                2019-04-13 00:53  
pulsar-2.3.2                2019-05-30 18:41  
pulsar-2.4.0                2019-07-02 08:35  
pulsar-2.4.1                2019-09-03 06:15  
pulsar-2.4.2                2019-12-04 05:13  
pulsar-2.5.0                2020-01-15 10:37  
pulsar-2.5.1                2020-04-20 07:51  
pulsar-2.5.2                2020-05-18 23:36  
pulsar-2.6.0                2020-07-03 04:10  
pulsar-2.6.1                2020-11-05 18:51  
pulsar-2.6.2                2020-11-09 05:32  
pulsar-2.6.3                2021-01-21 03:44  
pulsar-2.6.4                2021-06-02 17:03  
pulsar-2.7.0                2020-11-30 13:44  
pulsar-2.7.1                2021-03-16 02:42  
pulsar-2.7.2                2021-05-10 09:45  
pulsar-2.7.3                2021-08-02 13:45  
pulsar-2.7.4                2021-12-24 02:38  
pulsar-2.7.5                2022-09-01 12:20  
pulsar-2.8.0                2021-06-15 09:30  
pulsar-2.8.1                2021-09-07 13:33  
pulsar-2.8.2                2021-12-29 08:13  
pulsar-2.8.3                2022-06-17 11:41  
pulsar-2.8.4                2022-09-02 09:02  
pulsar-2.9.0                2021-11-25 11:23  
pulsar-2.9.1                2022-06-17 11:42  
pulsar-2.9.2                2022-06-17 11:40  
pulsar-2.9.3                2022-07-18 02:38  
pulsar-2.9.4                2022-12-29 07:39  
pulsar-2.9.5                2023-04-21 02:31  

pulsar-2.10.0               2022-06-17 11:39  
pulsar-2.10.1               2022-06-28 15:43  
pulsar-2.10.2               2022-10-19 02:43  
pulsar-2.10.3               2023-01-04 03:42  
pulsar-2.10.4               2023-04-20 09:26  
pulsar-2.10.5               2023-07-30 12:04  
pulsar-2.11.0               2023-01-10 06:28  
pulsar-2.11.1               2023-04-19 03:23  
pulsar-2.11.2               2023-07-18 08:22  


pulsar-3.0.0                2023-05-02 22:40  
pulsar-3.0.1                2023-08-04 09:59  
pulsar-3.1.0                2023-08-14 02:12  

存储和计算分离？

中国银行用？

在腾讯中应该有不同BG的不同团队，都在使用Pulsar中
https://zhuanlan.zhihu.com/p/357351711

张超，腾讯数据平台部 MQ 团队高级工程师；Apache TubeMQ(incubating) PMC；Kafka-on-Pulsar Maintainer；Apache Pulsar Contributor


Pulsar也不是特别年轻的项目了，2013年开始开发，2017年正式开源。
秦金卫 中行用Pulsar
### todo
消息队列需要存储哪些数据？
需要哪些计算？

Pulsar shell 

Offloaders

Connectors

Pulsar Manager

Pulsar Adapters

Pulsar C++ Client

## 书籍 book

Mastering Apache Pulsar Cloud Native Event Streaming at Scale 
Apache Pulsar in Action (David... (Z-Library).pdf

## source code
git clone -b v3.1.2 https://github.com/apache/pulsar.git
cd pulsar
./mvnw install -DskipTests
cd ../
git clone -b v0.5.3 https://github.com/apache/pulsar-client-reactive.git
cd pulsar-client-reactive
./gradlew build