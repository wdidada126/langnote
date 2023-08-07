# rocketmq remoting





##  分包解析源码



### org.apache.rocketmq.remoting



| org.apache.rocketmq.remoting | 类型 |      |
| ---------------------------- | ---- | ---- |
| 接口                         |      |      |
|                              |      |      |
| ChannelEventListener         |      |      |
| CommandCustomHeader          |      |      |
| InvokeCallback               |      |      |
| RemotingClient               |      |      |
| RemotingServer               |      |      |
| RemotingService              |      |      |
| RPCHook                      |      |      |



### org.apache.rocketmq.remoting.annotation

| org.apache.rocketmq.remoting.annotation | 类型       |      |
| --------------------------------------- | ---------- | ---- |
| CFNotNull                               | annotation |      |
| CFNullable                              |            |      |
|                                         |            |      |











### org.apache.rocketmq.remoting.common

| org.apache.rocketmq.remoting.common | 类型 |      |
| ---------------------------- | ---- | ---- |
| RemotingHelper |      | DEFAULT_CHARSET 编码 |
| Pair |      |      |
| RemotingUtil |      |      |
| SemaphoreReleaseOnlyOnce | | |
| ServiceThread | | |
| TlsMode | 枚举 | |






















### org.apache.rocketmq.remoting.exception

| org.apache.rocketmq.remoting.exception | 类型 |      |
| ---------------------------- | ---- | ---- |
| RemotingCommandException |      |      |
| RemotingConnectException |      |      |
| RemotingException |      |      |
| RemotingSendRequestException | | |
| RemotingTimeoutException | | |
| RemotingTooMuchRequestException | | |
| | | |
| | | |




















### org.apache.rocketmq.remoting.netty



| org.apache.rocketmq.remoting.netty | 类型 |      |
| ---------------------------------- | ---- | ---- |
| NettyRequestProcessor              |      |      |
| TlsHelper.DecryptionStrategy       |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| FileRegionEncoder                  |      |      |
| NettyClientConfig                  |      |      |
| NettyDecoder                       |      |      |
| NettyEncoder                       |      |      |
| NettyEvent                         |      |      |
| NettyLogger                        |      |      |
| NettyRemotingAbstract              |      |      |
| NettyRemotingClient                |      |      |
| NettyRemotingServer                |      |      |
| NettyServerConfig                  |      |      |
| NettySystemConfig                  |      |      |
| RequestTask                        |      |      |
| ResponseFuture                     |      |      |
| TlsHelper                          |      |      |
| TlsSystemConfig                    |      |      |
|                                    |      |      |
| 枚举                               |      |      |
|                                    |      |      |
| NettyEventType                     |      |      |




### org.apache.rocketmq.remoting.protocol





| org.apache.rocketmq.remoting.protocol | 类型 |      |
| ------------------------------------- | ---- | ---- |
| RemotingCommand                       |      |      |
| RemotingSerializable                  |      |      |
| RemotingSysResponseCode               |      |      |
| RocketMQSerializable                  |      |      |
|                                       |      |      |
| 枚举                                  |      |      |
|                                       |      |      |
| LanguageCode                          |      |      |
| RemotingCommandType                   |      |      |
| SerializeType                         |      |      |

