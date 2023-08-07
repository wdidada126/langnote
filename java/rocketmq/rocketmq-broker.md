# rocketmq-broker





## org.apache.rocketmq.broker



BrokerController

BrokerPathConfigHelper

BrokerStartup





### org.apache.rocketmq.broker.client



| org.apache.rocketmq.broker.client |      |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| ConsumerIdsChangeListener         |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| ClientChannelInfo                 |      |      |
| ClientHousekeepingService         |      |      |
| ConsumerGroupInfo                 |      |      |
| ConsumerManager                   |      |      |
| DefaultConsumerIdsChangeListener  |      |      |
| ProducerManager                   |      |      |
|                                   |      |      |
| 枚举                              |      |      |
|                                   |      |      |
| ConsumerGroupEvent                |      |      |



#### org.apache.rocketmq.broker.client.net



Broker2Client



#### org.apache.rocketmq.broker.client.rebalance



RebalanceLockManager



### org.apache.rocketmq.broker.filter



| org.apache.rocketmq.broker.filter          |      |      |
| ------------------------------------------ | ---- | ---- |
|                                            |      |      |
| 类                                         |      |      |
|                                            |      |      |
| CommitLogDispatcherCalcBitMap              |      |      |
| ConsumerFilterData                         |      |      |
| ConsumerFilterManager                      |      |      |
| ConsumerFilterManager.FilterDataMapByTopic |      |      |
| ExpressionForRetryMessageFilter            |      |      |
| ExpressionMessageFilter                    |      |      |
| MessageEvaluationContext                   |      |      |



### org.apache.rocketmq.broker.filtersrv



FilterServerManager

FilterServerUtil





### org.apache.rocketmq.broker.latency



BrokerFastFailure

BrokerFixedThreadPoolExecutor

FutureTaskExt



### org.apache.rocketmq.broker.longpolling







ManyPullRequest

NotifyMessageArrivingListener

PullRequest

PullRequestHoldService



### org.apache.rocketmq.broker.mqtrace



| org.apache.rocketmq.broker.mqtrace |      |      |
| ---------------------------------- | ---- | ---- |
| 接口                               |      |      |
|                                    |      |      |
| ConsumeMessageHook                 |      |      |
| SendMessageHook                    |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| ConsumeMessageContext              |      |      |
| SendMessageContext                 |      |      |



### org.apache.rocketmq.broker.offset



ConsumerOffsetManager





### org.apache.rocketmq.broker.out



BrokerOuterAPI



### org.apache.rocketmq.broker.pagecache







ManyMessageTransfer

OneMessageTransfer

QueryMessageTransfer



### org.apache.rocketmq.broker.plugin







AbstractPluginMessageStore

MessageStoreFactory

MessageStorePluginContext



### org.apache.rocketmq.broker.processor



| org.apache.rocketmq.broker.processor |      |      |
| ------------------------------------ | ---- | ---- |
| 类                                   |      |      |
|                                      |      |      |
| AbstractSendMessageProcessor         |      |      |
| AdminBrokerProcessor                 |      |      |
| ClientManageProcessor                |      |      |
| ConsumerManageProcessor              |      |      |
| EndTransactionProcessor              |      |      |
| ForwardRequestProcessor              |      |      |
| PullMessageProcessor                 |      |      |
| QueryMessageProcessor                |      |      |
| SendMessageProcessor                 |      |      |





### org.apache.rocketmq.broker.slave



SlaveSynchronize





### org.apache.rocketmq.broker.subscription







SubscriptionGroupManager



### org.apache.rocketmq.broker.topic



TopicConfigManager





### org.apache.rocketmq.broker.transaction





| org.apache.rocketmq.broker.transaction    |      |      |
| ----------------------------------------- | ---- | ---- |
| 接口                                      |      |      |
|                                           |      |      |
| TransactionalMessageService               |      |      |
| TransactionStore                          |      |      |
|                                           |      |      |
| 类                                        |      |      |
|                                           |      |      |
| AbstractTransactionalMessageCheckListener |      |      |
| OperationResult                           |      |      |
| TransactionalMessageCheckService          |      |      |
| TransactionRecord                         |      |      |





#### org.apache.rocketmq.broker.transaction.jdbc





JDBCTransactionStore

JDBCTransactionStoreConfig



#### org.apache.rocketmq.broker.transaction.queue





|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| DefaultTransactionalMessageCheckListener |      |      |
| GetResult                                |      |      |
| TransactionalMessageBridge               |      |      |
| TransactionalMessageServiceImpl          |      |      |
| TransactionalMessageUtil                 |      |      |



### org.apache.rocketmq.broker.util



PositiveAtomicCounter

ServiceProvider