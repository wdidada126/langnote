# rocketmq-tools



### org.apache.rocketmq.tools.admin



|                       |      |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| MQAdminExt            |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| DefaultMQAdminExt     |      |      |
| DefaultMQAdminExtImpl |      |      |



#### org.apache.rocketmq.tools.admin.api



MessageTrack

枚举

TrackType



### org.apache.rocketmq.tools.command



|                     |      |      |
| ------------------- | ---- | ---- |
| 接口                |      |      |
|                     |      |      |
| SubCommand          |      |      |
|                     |      |      |
| 类                  |      |      |
|                     |      |      |
| CommandUtil         |      |      |
| MQAdminStartup      |      |      |
|                     |      |      |
| 异常错误            |      |      |
|                     |      |      |
| SubCommandException |      |      |



#### org.apache.rocketmq.tools.command.broker



|                              |      |      |
| ---------------------------- | ---- | ---- |
| 类                           |      |      |
|                              |      |      |
| BrokerConsumeStatsSubCommad  |      |      |
| BrokerStatusSubCommand       |      |      |
| CleanExpiredCQSubCommand     |      |      |
| CleanUnusedTopicCommand      |      |      |
| GetBrokerConfigCommand       |      |      |
| SendMsgStatusCommand         |      |      |
| UpdateBrokerConfigSubCommand |      |      |





#### org.apache.rocketmq.tools.command.cluster





类

ClusterListSubCommand

CLusterSendMsgRTCommand



#### org.apache.rocketmq.tools.command.connection



类

ConsumerConnectionSubCommand

ProducerConnectionSubCommand







#### org.apache.rocketmq.tools.command.consumer





| 类                             |      |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| ConsumerProgressSubCommand     |      |      |
| ConsumerStatusSubCommand       |      |      |
| ConsumerSubCommand             |      |      |
| DeleteSubscriptionGroupCommand |      |      |
| StartMonitoringSubCommand      |      |      |
| UpdateSubGroupSubCommand       |      |      |



#### org.apache.rocketmq.tools.command.message



| 类                                |      |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| CheckMsgSendRTCommand             |      |      |
| ConsumeMessageCommand             |      |      |
| DecodeMessageIdCommond            |      |      |
| PrintMessageByQueueCommand        |      |      |
| PrintMessageSubCommand            |      |      |
| QueryMsgByIdSubCommand            |      |      |
| QueryMsgByKeySubCommand           |      |      |
| QueryMsgByOffsetSubCommand        |      |      |
| QueryMsgByUniqueKeySubCommand     |      |      |
| SendMessageCommand                |      |      |
|                                   |      |      |
| 枚举                              |      |      |
|                                   |      |      |
| ConsumeMessageCommand.ConsumeType |      |      |



#### org.apache.rocketmq.tools.command.namesrv







| 类                         |      |      |
| -------------------------- | ---- | ---- |
|                            |      |      |
| DeleteKvConfigCommand      |      |      |
| GetNamesrvConfigCommand    |      |      |
| UpdateKvConfigCommand      |      |      |
| UpdateNamesrvConfigCommand |      |      |
| WipeWritePermSubCommand    |      |      |



#### org.apache.rocketmq.tools.command.offset



| 类                          |      |      |
| --------------------------- | ---- | ---- |
|                             |      |      |
| CloneGroupOffsetCommand     |      |      |
| GetConsumerStatusCommand    |      |      |
| ResetOffsetByTimeCommand    |      |      |
| ResetOffsetByTimeOldCommand |      |      |



#### org.apache.rocketmq.tools.command.queue



QueryConsumeQueueCommand



#### org.apache.rocketmq.tools.command.stats





StatsAllSubCommand



#### org.apache.rocketmq.tools.command.topic





|                           |      |      |
| ------------------------- | ---- | ---- |
| 类                        |      |      |
|                           |      |      |
| AllocateMQSubCommand      |      |      |
| DeleteTopicSubCommand     |      |      |
| RebalanceResult           |      |      |
| TopicClusterSubCommand    |      |      |
| TopicListSubCommand       |      |      |
| TopicRouteSubCommand      |      |      |
| TopicStatusSubCommand     |      |      |
| UpdateOrderConfCommand    |      |      |
| UpdateTopicPermSubCommand |      |      |
| UpdateTopicSubCommand     |      |      |



### org.apache.rocketmq.tools.monitor



| org.apache.rocketmq.tools.monitor |      |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| MonitorListener                   |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| DefaultMonitorListener            |      |      |
| DeleteMsgsEvent                   |      |      |
| FailedMsgs                        |      |      |
| MonitorConfig                     |      |      |
| MonitorService                    |      |      |
| UndoneMsgs                        |      |      |