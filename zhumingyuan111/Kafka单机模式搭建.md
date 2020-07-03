---
title: Kafka单机模式搭建
date: 2017-06-26 09:32:45
tags: CSDN迁移
---
  Kafka作为一种高吞吐量的分布式发布订阅消息系统现在非常流行，所以自己也在该技术上进行简单的尝试，为了以后深入研究打下基础。下面主要介绍一下在ubuntu单机环境下kafka安装和简单使用。

 
### 下载kafka安装包

 kafka_2.10-0.8.2.2.tgz   
 解压并重命名

 
```
tar -zxvf kafka_2.10-0.8.2.2.tgz -C /usr/local/
mv kafka_2.10-0.8.2.2 kafka
```
 因为之前已经安装zookeeper，所以今天只安装kafka即可。

 
### 修改kafka配置

 修改server.properties，只需要修改log.dirs,其他属性保持不变。

 
```
log.dirs=/usr/local-extend/kafka/kafka-logs
```
 建立相关文件夹

 
```
mkdir /usr/local-extend/kafka/kafka-logs
```
 修改zookeeper.properties，只修改dataDir属性，其他保持不变。

 
```
dataDir=/usr/local-extend/kafka/zk-data
```
 建立相关文件夹

 
```
mkdir /usr/local-extend/kafka/zk-data
```
 到此为止kafak配置完成，下面介绍kafka的简单使用。

 
### kafka 简单使用

  
  * 在启动kafka服务之前首先要启动zookeeper;   
     -启动kafka ，新窗口输入命令： `./bin/kafka-server-start.sh config/server.properties`   
  * 创建topic ，新窗口输入命令： `./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka_test1`  
  * 查看topic，新窗口输入命令：  `./bin/kafka-topics.sh --list --zookeeper localhost:2181`  
  * 启动生产者 ，新窗口输入命令： `./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka_test1`  
  * 启动消费者 ，新窗口输入命令： `./bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic kafka_test1 --from-beginning`    
     在生产者窗口输入一些字符床，然后回车，这样就消息就实现发送;在消费者窗口就能查看到相关信息。    
  