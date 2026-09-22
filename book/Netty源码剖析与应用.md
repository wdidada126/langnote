# Netty源码剖析与应用

zlibrary有pdf

https://book.douban.com/subject/35246428/
刘耀林，从2012年到2017年一直从事Java后台服务开发工作。在此期间曾创办过大象在线分享网，网名夜行侠老师，录制过Netty源码剖析教学视频，同时在多家互联网公司担任过系统架构师，有丰富的Java工作实战经验。从2018年至今，从事大数据研发工作，对Flink、HBase、Kafka、Elasticsearch等大数据组件有深入的研究。

第1章 Netty基础篇 1
第2章 原理部分 23
第5章 Netty读/写请求源码剖析 165
第4章 Netty核心组件源码剖析 81
第5章 Netty读/写请求源码剖析 165
第6章 Netty内存管理 195
第7章 Netty时间轮高级应用 228

知乎电子书
Netty的编码和解码除了解决TCP协议的粘包和拆包问题，还有一些编解码器做了很多额外的事情，如StringEncode（把字符串转换成字节流）、ProtobufDecoder（对Protobuf序列化数据进行解码）

韩顺平早就不是尚硅谷的了，现在应该是单干，还做培训那块，卖线上课程的

ChannelInboundHandlerAdapter

但如果是一个基础扎实的科班生，看博客捋一遍netty的基本设计原理(有一张很经典的图，告诉你各组件的分工)，用socket从bio的服务端开始写起——>多线程处理的bio——>selector注册事件的nio——>reactor模型——>主从reactor模型，最多两天时间就基本理解了。我上学期写RPC框架时候为了使用nio通信从调研学习这部分知识到写demo练习三天左右就照着netty4.x用户手册开干了，后续的话还是要持续学习，比如想新增长连接心跳检测，重连机制等等。

chatgpt
netty开启多线程主从reactor

netty定时任务心跳检测
掉线重连



## 第1章 Netty基础篇 1
## 第2章 原理部分 23
## 第5章 Netty读/写请求源码剖析 165
## 第4章 Netty核心组件源码剖析 81
## 第5章 Netty读/写请求源码剖析 165
## 第6章 Netty内存管理 195
## 第7章 Netty时间轮高级应用 228

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2023-04
> 《Netty源码剖析与应用》

