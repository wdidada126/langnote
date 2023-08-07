# rocket common



## 分包解析源码



org.apache.rocketmq.common.message.Message

## org.apache.rocketmq.common



| org.apache.rocketmq.common |      |      |
| -------------------------- | ---- | ---- |
| 类                         |      |      |
|                            |      |      |
| BrokerConfig               |      |      |
| BrokerConfigSingleton      |      |      |
| ConfigManager              |      |      |
| Configuration              |      |      |
| CountDownLatch2            |      |      |
| DataVersion                |      |      |
| MixAll                     |      |      |
| MQVersion                  |      |      |
| Pair                       |      |      |
| ServiceThread              |      |      |
| SystemClock                |      |      |
| ThreadFactoryImpl          |      |      |
| TopicConfig                |      |      |
| UtilAll                    |      |      |
|                            |      |      |
| 枚举                       |      |      |
|                            |      |      |
| MQVersion.Version          |      |      |
| ServiceState               |      |      |
| TopicFilterType            |      |      |



### org.apache.rocketmq.common.admin



| org.apache.rocketmq.common.admin |      |      |
| -------------------------------- | ---- | ---- |
| 类                               |      |      |
|                                  |      |      |
| ConsumeStats                     |      |      |
| OffsetWrapper                    |      |      |
| RollbackStats                    |      |      |
| TopicOffset                      |      |      |
| TopicStatsTable                  |      |      |





### org.apache.rocketmq.common.annotation


ImportantField




### org.apache.rocketmq.common.consistenthash

接口
HashFunction
Node
类
ConsistentHashRouter
VirtualNode





### org.apache.rocketmq.common.constant

类
DBMsgConstants
LoggerName
PermName


#### org.apache.rocketmq.common.consumer

ConsumeFromWhere



### org.apache.rocketmq.common.filter
MessageFilter
类
ExpressionType
FilterAPI
FilterContext

#### org.apache.rocketmq.common.filter.impl

类
Op
Operand
Operator
PolishExpr
枚举
Type


### org.apache.rocketmq.common.help

FAQUrl


### org.apache.rocketmq.common.hook

接口
FilterCheckHook

### org.apache.rocketmq.common.message





| org.apache.rocketmq.common.message |      |      |
| ---------------------------------- | ---- | ---- |
| 类                                 |      |      |
|                                    |      |      |
| Message                            |      |      |
| MessageAccessor                    |      |      |
| MessageBatch                       |      |      |
| MessageClientExt                   |      |      |
| MessageClientIDSetter              |      |      |
| MessageConst                       |      |      |
| MessageDecoder                     |      |      |
| MessageExt                         |      |      |
| MessageExtBatch                    |      |      |
| MessageId                          |      |      |
| MessageQueue                       |      |      |
| MessageQueueForC                   |      |      |
|                                    |      |      |
| 枚举                               |      |      |
|                                    |      |      |
| MessageType                        |      |      |



### org.apache.rocketmq.common.namesrv


| org.apache.rocketmq.common.namesrv |      |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| NamesrvConfig                      |      |      |
| NamesrvUtil                        |      |      |
| RegisterBrokerResult               |      |      |
| TopAddressing                      |      |      |



### org.apache.rocketmq.common.protocol

类
MQProtosHelper
RequestCode
ResponseCode

### org.apache.rocketmq.common.protocol.body



| org.apache.rocketmq.common.protocol.body |      |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| BrokerStatsData                          |      |      |
| BrokerStatsItem                          |      |      |
| CheckClientRequestBody                   |      |      |
| ClusterInfo                              |      |      |
| Connection                               |      |      |
| ConsumeByWho                             |      |      |
| ConsumeMessageDirectlyResult             |      |      |
| ConsumeQueueData                         |      |      |
| ConsumerConnection                       |      |      |
| ConsumerOffsetSerializeWrapper           |      |      |
| ConsumerRunningInfo                      |      |      |
| ConsumeStatsList                         |      |      |
| ConsumeStatus                            |      |      |
| GetConsumerStatusBody                    |      |      |
| GroupList                                |      |      |
| KVTable                                  |      |      |
| LockBatchRequestBody                     |      |      |
| LockBatchResponseBody                    |      |      |
| ProcessQueueInfo                         |      |      |
| ProducerConnection                       |      |      |
| QueryConsumeQueueResponseBody            |      |      |
| QueryConsumeTimeSpanBody                 |      |      |
| QueryCorrectionOffsetBody                |      |      |
| QueueTimeSpan                            |      |      |
| RegisterBrokerBody                       |      |      |
| ResetOffsetBody                          |      |      |
| ResetOffsetBodyForC                      |      |      |
| SubscriptionGroupWrapper                 |      |      |
| TopicConfigSerializeWrapper              |      |      |
| TopicList                                |      |      |
| UnlockBatchRequestBody                   |      |      |
|                                          |      |      |
| 枚举                                     |      |      |
|                                          |      |      |
| CMResult                                 |      |      |



#### org.apache.rocketmq.common.protocol.header



|                                           |      |      |
| ----------------------------------------- | ---- | ---- |
| 类                                        |      |      |
|                                           |      |      |
| CheckTransactionStateRequestHeader        |      |      |
| CheckTransactionStateResponseHeader       |      |      |
| CloneGroupOffsetRequestHeader             |      |      |
| ConsumeMessageDirectlyResultRequestHeader |      |      |
| ConsumerSendMsgBackRequestHeader          |      |      |
| CreateTopicRequestHeader                  |      |      |
| DeleteSubscriptionGroupRequestHeader      |      |      |
| DeleteTopicRequestHeader                  |      |      |
| EndTransactionRequestHeader               |      |      |
| EndTransactionResponseHeader              |      |      |
| GetAllTopicConfigResponseHeader           |      |      |
| GetBrokerConfigResponseHeader             |      |      |
| GetConsumerConnectionListRequestHeader    |      |      |
| GetConsumerListByGroupRequestHeader       |      |      |
| GetConsumerListByGroupResponseBody        |      |      |
| GetConsumerListByGroupResponseHeader      |      |      |
| GetConsumerRunningInfoRequestHeader       |      |      |
| GetConsumerStatusRequestHeader            |      |      |
| GetConsumeStatsInBrokerHeader             |      |      |
| GetConsumeStatsRequestHeader              |      |      |
| GetEarliestMsgStoretimeRequestHeader      |      |      |
| GetEarliestMsgStoretimeResponseHeader     |      |      |
| GetMaxOffsetRequestHeader                 |      |      |
| GetMaxOffsetResponseHeader                |      |      |
| GetMinOffsetRequestHeader                 |      |      |
| GetMinOffsetResponseHeader                |      |      |
| GetProducerConnectionListRequestHeader    |      |      |
| GetTopicsByClusterRequestHeader           |      |      |
| GetTopicStatsInfoRequestHeader            |      |      |
| NotifyConsumerIdsChangedRequestHeader     |      |      |
| PullMessageRequestHeader                  |      |      |
| PullMessageResponseHeader                 |      |      |
| QueryConsumeQueueRequestHeader            |      |      |
| QueryConsumerOffsetRequestHeader          |      |      |
| QueryConsumerOffsetResponseHeader         |      |      |
| QueryConsumeTimeSpanRequestHeader         |      |      |
| QueryCorrectionOffsetHeader               |      |      |
| QueryMessageRequestHeader                 |      |      |
| QueryMessageResponseHeader                |      |      |
| QueryTopicConsumeByWhoRequestHeader       |      |      |
| ResetOffsetRequestHeader                  |      |      |
| SearchOffsetRequestHeader                 |      |      |
| SearchOffsetResponseHeader                |      |      |
| SendMessageRequestHeader                  |      |      |
| SendMessageRequestHeaderV2                |      |      |
| SendMessageResponseHeader                 |      |      |
| UnregisterClientRequestHeader             |      |      |
| UnregisterClientResponseHeader            |      |      |
| UpdateConsumerOffsetRequestHeader         |      |      |
| UpdateConsumerOffsetResponseHeader        |      |      |
| ViewBrokerStatsDataRequestHeader          |      |      |
| ViewMessageRequestHeader                  |      |      |
| ViewMessageResponseHeader                 |      |      |



#### org.apache.rocketmq.common.protocol.header.filtersrv

类
RegisterFilterServerRequestHeader
RegisterFilterServerResponseHeader
RegisterMessageFilterClassRequestHeader

#### org.apache.rocketmq.common.protocol.header.namesrv



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| 类                                  |      |      |
|                                     |      |      |
| DeleteKVConfigRequestHeader         |      |      |
| DeleteTopicInNamesrvRequestHeader   |      |      |
| GetKVConfigRequestHeader            |      |      |
| GetKVConfigResponseHeader           |      |      |
| GetKVListByNamespaceRequestHeader   |      |      |
| GetRouteInfoRequestHeader           |      |      |
| PutKVConfigRequestHeader            |      |      |
| QueryDataVersionRequestHeader       |      |      |
| QueryDataVersionResponseHeader      |      |      |
| RegisterBrokerRequestHeader         |      |      |
| RegisterBrokerResponseHeader        |      |      |
| RegisterOrderTopicRequestHeader     |      |      |
| UnRegisterBrokerRequestHeader       |      |      |
| WipeWritePermOfBrokerRequestHeader  |      |      |
| WipeWritePermOfBrokerResponseHeader |      |      |





#### org.apache.rocketmq.common.protocol.heartbeat



|                  |      |      |
| ---------------- | ---- | ---- |
| 类               |      |      |
|                  |      |      |
| ConsumerData     |      |      |
| HeartbeatData    |      |      |
| ProducerData     |      |      |
| SubscriptionData |      |      |
|                  |      |      |
| 枚举             |      |      |
|                  |      |      |
| ConsumeType      |      |      |
| MessageModel     |      |      |
|                  |      |      |
|                  |      |      |
|                  |      |      |
|                  |      |      |
|                  |      |      |
|                  |      |      |





#### org.apache.rocketmq.common.protocol.route

类
BrokerData
QueueData
TopicRouteData


#### org.apache.rocketmq.common.protocol.topic

OffsetMovedEvent

### org.apache.rocketmq.common.queue

ConcurrentTreeMap
RoundQueue


### org.apache.rocketmq.common.running

枚举
RunningStats

### org.apache.rocketmq.common.stats



|                    |      |      |
| ------------------ | ---- | ---- |
| 类                 |      |      |
|                    |      |      |
| MomentStatsItem    |      |      |
| MomentStatsItemSet |      |      |
| StatsItem          |      |      |
| StatsItemSet       |      |      |
| StatsSnapshot      |      |      |





### org.apache.rocketmq.common.subscription

SubscriptionGroupConfig


#### org.apache.rocketmq.common.sysflag

类
MessageSysFlag
PullSysFlag
SubscriptionSysFlag
TopicSysFlag


### org.apache.rocketmq.common.utils

类
ChannelUtil
HttpTinyClient
HttpTinyClient.HttpResult
IOTinyUtils
ThreadUtils