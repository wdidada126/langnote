# RabbitMQ

https://gitee.com/edidada/testrabbitmqspringboot

开发语言？

### 版本

https://github.com/rabbitmq/rabbitmq-server/releases
3.11

https://rabbitmq.com/changelog.html


### 书籍

RabbitMQ实战 高效部署分布式消息队列



是否支持消息分组？



https://www.rabbitmq.com/



[消息确认Ack](https://blog.csdn.net/vbirdbest/article/details/78699913)





**RabbitMQ**是实现了高级消息队列协议（AMQP）的开源消息代理软件（亦称面向消息的中间件）。RabbitMQ服务器是用[Erlang](https://baike.baidu.com/item/Erlang)语言编写的，而集群和故障转移是构建在[开放电信平台](https://baike.baidu.com/item/开放电信平台)框架上的。所有主要的编程语言均有与代理接口通讯的客户端库。


### windows安装运行
需要安装erlang库，放弃，使用docker

https://www.rabbitmq.com/install-windows-manual.html
cd E:\rabbitmq_server-3.8.17

./bin/

### mac安装运行


https://www.rabbitmq.com/install-generic-unix.html

### docker安装

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.8.34-management

### rabbitmq 命令行工具