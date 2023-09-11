# RPC手撸专栏

https://gitee.com/edidada/bhrpc-learning

网上开源的系统
https://github.com/Snailclimb/guide-rpc-framework

一个较为完毕的RPC框架由服务提供者、服务消费者、注册中心和监控中心组成

## chap. 2 
一个较为完善的RPC框架的实现会涉及到众多的技术点，但是最核心的技术点大体上包含：服务注册与发现、网络通信协议、序列化与反序列化、RPC调用方式、线程模型、动态代理、负载均衡等

### 5.2 Dubbo线程模型的分发策略

## 第6章：自定义网络传输协议的实现
自定义网络传输协议主要由7个类组成，分别是RpcType、RpcMessage、RpcRequest、RpcResponse、RpcHeader、RpcHeaderFactory和RpcProtocol。

RpcType：枚举类，主要标识传输消息的类型，包括：请求消息、响应消息和心跳消息。
RpcMessage：基础消息类，包含是否单向发送和是否异步发送两个字段，bhrpc框架支持单向发送和异步发送。
RpcRequest：请求消息的消息体数据，继承RpcMessage类，除了是否单向发送和是否异步发送两个字段外，在bhrpc框架中包含请求的类名、方法名称、参数类型数组、参数数组、版本号和分组字段。
RpcResponse：响应消息的消息体数据，继承RpcMessage类，除了是否单向发送和是否异步发送两个字段外，在bhrpc框架中包含错误信息和返回的结果数据。
RpcHeader：网络传输协议的消息头，包括：魔数、消息类型、消息状态、消息ID、序列化类型和消息长度等。
RpcHeaderFactory：创建RpcHeader的工厂类，依赖RpcHeader类和RpcType枚举类。
RpcProtocol：真正在bhrpc框架中传输数据的协议实体类，包含消息头和消息体，消息头为Header对象，消息体为传入的泛型对象。

## 第9章：服务提供者调用真实方法的实现
在服务消费者向服务提供者发起调用时，传递以下几个重要的参数。

要调用的真实方法所在的类名称。
要调用的真实方法的名称。
要调用的真实方法的参数类型数组。
要调用的真实方法的参数数组。
要调用的真实方法所在类的版本号，
要调用的真实方法所在类的分组。
