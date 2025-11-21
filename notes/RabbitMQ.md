# RabbitMQ


rabbitmq有几个明显问题，一个是消息队列无法堆积，太多消息，消息数量到达mq上限后，会无法写入队列，这导致消费者挂掉后 会影响生产者，mq本质是接耦生产和消费，不应该丢消息。其二是消息消费完后，消息就丢掉了，所以无法回溯。其三，自带的延时消息，rabbitmq是放在内存里面的你敢信，我司就因为有的业务乱发延时消息，直接把rabbitmq打死的。说白了rabbitmq的设计的确是过时了，而且对开发者有一点的学习要求，所以注定gg

### rabbitmq如何避免消息丢失
producer等待server返回ack
server设置消息持久化机制
consumer设置成手动确认消息

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