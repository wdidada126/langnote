# rocketmq client



https://javadoc.io/doc/com.alibaba.rocketmq/rocketmq-client/latest/index.html



##  分包解析源码



v4.3.0


### org.apache.rocketmq.client


| org.apache.rocketmq.client |           |        |
| -------------------------- | --------- | ------ |
| MQAdmin                    | interface | 子接口 |
|                            |           |        |
|                            |           |        |

MQAdmin
类
ClientConfig
MQHelper
QueryResult
Validators


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





|                               |      |      |
| ----------------------------- | ---- | ---- |
| 接口                          |      |      |
|                               |      |      |
| AllocateMessageQueueStrategy  |      |      |
| MessageQueueListener          |      |      |
| MQConsumer                    |      |      |
| MQPullConsumer                |      |      |
| MQPushConsumer                |      |      |
| PullCallback                  |      |      |
| PullTaskCallback              |      |      |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| DefaultMQPullConsumer         |      |      |
| DefaultMQPushConsumer         |      |      |
| MessageSelector               |      |      |
| MQPullConsumerScheduleService |      |      |
| PullResult                    |      |      |
| PullTaskContext               |      |      |
|                               |      |      |
| 枚举                          |      |      |
|                               |      |      |
| PullStatus                    |      |      |



DefaultMQPushConsumer 暴露给使用者的api

void setNamesrvAddr(String namesrvAddr)

void subscribe(String topic, String subExpression)

void registerMessageListener(MessageListenerConcurrently messageListener)

start()



#### org.apache.rocketmq.client.consumer.listener





| 接口                        |      |      |
| --------------------------- | ---- | ---- |
|                             |      |      |
| MessageListener             |      |      |
| MessageListenerConcurrently |      |      |
| MessageListenerOrderly      |      |      |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| ConsumeConcurrentlyContext  |      |      |
| ConsumeOrderlyContext       |      |      |
|                             |      |      |
| 枚举                        |      |      |
|                             |      |      |
| ConsumeConcurrentlyStatus   |      |      |
| ConsumeOrderlyStatus        |      |      |
| ConsumeReturnType           |      |      |





org.apache.rocketmq.client.consumer.rebalance



|                                               |      |      |
| --------------------------------------------- | ---- | ---- |
| 接口                                          |      |      |
|                                               |      |      |
| AllocateMachineRoomNearby.MachineRoomResolver |      |      |
|                                               |      |      |
| 类                                            |      |      |
|                                               |      |      |
| AllocateMachineRoomNearby                     |      |      |
| AllocateMessageQueueAveragely                 |      |      |
| AllocateMessageQueueAveragelyByCircle         |      |      |
| AllocateMessageQueueByConfig                  |      |      |
| AllocateMessageQueueByMachineRoom             |      |      |
| AllocateMessageQueueConsistentHash            |      |      |



org.apache.rocketmq.client.consumer.store





|                         |      |      |
| ----------------------- | ---- | ---- |
| OffsetStore             |      |      |
|                         |      |      |
| 类                      |      |      |
|                         |      |      |
| LocalFileOffsetStore    |      |      |
| OffsetSerializeWrapper  |      |      |
| RemoteBrokerOffsetStore |      |      |
|                         |      |      |
| 枚举                    |      |      |
|                         |      |      |
| ReadOffsetType          |      |      |





### org.apache.rocketmq.client.exception

| org.apache.rocketmq.client.exception |      |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
|                                      |      |      |
|                                      |      |      |


MQBrokerException
MQClientException


### org.apache.rocketmq.client.hook

| org.apache.rocketmq.client.hook |      |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
|                                 |      |      |
|                                 |      |      |





|                       |      |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| CheckForbiddenHook    |      |      |
| ConsumeMessageHook    |      |      |
| FilterMessageHook     |      |      |
| SendMessageHook       |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| CheckForbiddenContext |      |      |
| ConsumeMessageContext |      |      |
| FilterMessageContext  |      |      |
| SendMessageContext    |      |      |



### org.apache.rocketmq.client.impl





| org.apache.rocketmq.client.impl |      |      |
| ------------------------------- | ---- | ---- |
| 接口                            |      |      |
|                                 |      |      |
| CheckForbiddenHook              |      |      |
| ConsumeMessageHook              |      |      |
| FilterMessageHook               |      |      |
| SendMessageHook                 |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| CheckForbiddenContext           |      |      |
| ConsumeMessageContext           |      |      |
| FilterMessageContext            |      |      |
| SendMessageContext              |      |      |





##### org.apache.rocketmq.client.impl.consumer



|                                   |      |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| ConsumeMessageService             |      |      |
| MQConsumerInner                   |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| ConsumeMessageConcurrentlyService |      |      |
| ConsumeMessageOrderlyService      |      |      |
| DefaultMQPullConsumerImpl         |      |      |
| DefaultMQPushConsumerImpl         |      |      |
| MessageQueueLock                  |      |      |
| ProcessQueue                      |      |      |
| PullAPIWrapper                    |      |      |
| PullMessageService                |      |      |
| PullRequest                       |      |      |
| PullResultExt                     |      |      |
| RebalanceImpl                     |      |      |
| RebalancePullImpl                 |      |      |
| RebalancePushImpl                 |      |      |
| RebalanceService                  |      |      |



##### org.apache.rocketmq.client.impl.factory



MQClientInstance



##### org.apache.rocketmq.client.impl.producer



接口

MQProducerInner

类

DefaultMQProducerImpl

TopicPublishInfo



### org.apache.rocketmq.client.latency

| org.apache.rocketmq.client.latency |      |      |
| ---------------------------------- | ---- | ---- |
| LatencyFaultTolerance              | 接口 |      |
| LatencyFaultToleranceImpl          | 类   |      |
| MQFaultStrategy                    |      |      |











### org.apache.rocketmq.client.log

| org.apache.rocketmq.client.log |      |      |
| ------------------------------ | ---- | ---- |
| ClientLogger                   |      |      |
|                                |      |      |
|                                |      |      |



ClientLogger





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
| ConsumerStatsManager            |      |      |
|                                 |      |      |
|                                 |      |      |