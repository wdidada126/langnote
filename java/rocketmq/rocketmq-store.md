# rocketmq-store



org.apache.rocketmq.store







|                                  |      |      |
| -------------------------------- | ---- | ---- |
| 接口                             |      |      |
|                                  |      |      |
| AppendMessageCallback            |      |      |
| CommitLogDispatcher              |      |      |
| MessageArrivingListener          |      |      |
| MessageFilter                    |      |      |
| MessageStore                     |      |      |
| PutMessageLock                   |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| AllocateMappedFileService        |      |      |
| AppendMessageResult              |      |      |
| CommitLog                        |      |      |
| CommitLog.GroupCommitRequest     |      |      |
| CommitLog.MessageExtBatchEncoder |      |      |
| ConsumeQueue                     |      |      |
| ConsumeQueueExt                  |      |      |
| ConsumeQueueExt.CqExtUnit        |      |      |
| DefaultMessageFilter             |      |      |
| DefaultMessageStore              |      |      |
| DispatchRequest                  |      |      |
| GetMessageResult                 |      |      |
| MappedFile                       |      |      |
| MappedFileQueue                  |      |      |
| MessageExtBrokerInner            |      |      |
| PutMessageReentrantLock          |      |      |
| PutMessageResult                 |      |      |
| PutMessageSpinLock               |      |      |
| QueryMessageResult               |      |      |
| ReferenceResource                |      |      |
| RunningFlags                     |      |      |
| SelectMappedBufferResult         |      |      |
| StoreCheckpoint                  |      |      |
| StoreStatsService                |      |      |
| StoreUtil                        |      |      |
| TransientStorePool               |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| AppendMessageStatus              |      |      |
| GetMessageStatus                 |      |      |
| PutMessageStatus                 |      |      |



org.apache.rocketmq.store.config



|                       |      |      |
| --------------------- | ---- | ---- |
| MessageStoreConfig    |      |      |
| StorePathConfigHelper |      |      |
|                       |      |      |
| 枚举                  |      |      |
|                       |      |      |
| BrokerRole            |      |      |
| FlushDiskType         |      |      |



org.apache.rocketmq.store.ha



|                  |      |      |
| ---------------- | ---- | ---- |
| 类               |      |      |
|                  |      |      |
| HAConnection     |      |      |
| HAService        |      |      |
| WaitNotifyObject |      |      |



org.apache.rocketmq.store.index



|                   |      |      |
| ----------------- | ---- | ---- |
| 类                |      |      |
|                   |      |      |
| IndexFile         |      |      |
| IndexHeader       |      |      |
| IndexService      |      |      |
| QueryOffsetResult |      |      |



org.apache.rocketmq.store.schedule





类

DelayOffsetSerializeWrapper

ScheduleMessageService



org.apache.rocketmq.store.stats





类

BrokerStats

BrokerStatsManager

枚举

BrokerStatsManager.StatsType



org.apache.rocketmq.store.util



LibC