# rocketmq client



##  分包解析源码



v4.3.0


### org.apache.rocketmq.client


| org.apache.rocketmq.client |           |        |
| -------------------------- | --------- | ------ |
| MQAdmin                    | interface | 子接口 |
|                            |           |        |
|                            |           |        |

### org.apache.rocketmq.client.admin

```
MQAdminExtInner
```

### org.apache.rocketmq.client.common

| org.apache.rocketmq.client.common |      |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
|                                   |      |      |
|                                   |      |      |


### org.apache.rocketmq.client.consumer

| org.apache.rocketmq.client.consumer |      |                          |
| ----------------------------------- | ---- | ------------------------ |
| DefaultMQPushConsumer               |      | MQPushConsumer接口实现类 |
|                                     |      |                          |
|                                     |      |                          |



DefaultMQPushConsumer 暴露给使用者的api

void setNamesrvAddr(String namesrvAddr)

void subscribe(String topic, String subExpression)

void registerMessageListener(MessageListenerConcurrently messageListener)

start()





### org.apache.rocketmq.client.exception

| org.apache.rocketmq.client.exception |      |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
|                                      |      |      |
|                                      |      |      |



### org.apache.rocketmq.client.hook

| org.apache.rocketmq.client.hook |      |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
|                                 |      |      |
|                                 |      |      |


### org.apache.rocketmq.client.impl

| org.apache.rocketmq.client.impl |      |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
|                                 |      |      |
|                                 |      |      |


### org.apache.rocketmq.client.latency

| org.apache.rocketmq.client.latency |      |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
|                                    |      |      |
|                                    |      |      |


### org.apache.rocketmq.client.log

| org.apache.rocketmq.client.log |      |      |
| ------------------------------ | ---- | ---- |
| ClientLogger                   |      |      |
|                                |      |      |
|                                |      |      |

### org.apache.rocketmq.client.producer

| org.apache.rocketmq.client.producer |           |                                       |
| ----------------------------------- | --------- | ------------------------------------- |
| DefaultMQProducer                   |           | MQProducer接口实现类 ClientConfig子类 |
| LocalTransactionState               | enum      |                                       |
| MessageQueueSelector                | interface | 子类                                  |
| MQProducer                          | interface |                                       |
| SendCallback                        | interface |                                       |
| SendResult                          |           |                                       |
| SendStatus                          | enum      |                                       |
| TransactionListener                 | interface |                                       |
| TransactionMQProducer               |           |                                       |
| TransactionSendResult               |           |                                       |




##### org.apache.rocketmq.client.producer.selector

​	

| org.apache.rocketmq.client.producer.selector |      |                                |
| -------------------------------------------- | ---- | ------------------------------ |
| SelectMessageQueueByHash                     |      | MessageQueueSelector接口实现类 |
| SelectMessageQueueByMachineRoom              |      | MessageQueueSelector接口实现类 |
| SelectMessageQueueByRandom                   |      | MessageQueueSelector接口实现类 |

DefaultMQProducer常用方法
DefaultMQProducer(final String producerGroup) 
setNamesrvAddr(String namesrvAddr)
start()
void setRetryTimesWhenSendAsyncFailed(final int retryTimesWhenSendAsyncFailed)
void send(Message msg,SendCallback sendCallback)
void shutdown()

void sendOneway(Message msg)



ClientConfig (org.apache.rocketmq.client)
    DefaultMQPushConsumer (org.apache.rocketmq.client.consumer)
    DefaultMQPullConsumer (org.apache.rocketmq.client.consumer)
    DefaultMQProducer (org.apache.rocketmq.client.producer)
        TransactionMQProducer (org.apache.rocketmq.client.producer)



### org.apache.rocketmq.client.stat

| org.apache.rocketmq.client.stat |      |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
|                                 |      |      |
|                                 |      |      |