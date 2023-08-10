jraft


https://gitee.com/sofastack/sofa-jraft


## example
https://gitee.com/edidada/jraft-example

nacos 1.4.2用jraft
```xml
        <dependency>
            <groupId>com.alipay.sofa</groupId>
            <artifactId>jraft-core</artifactId>
            <version>1.3.5</version>
        </dependency>
```

## 源代码分包解析
https://javadoc.dev/online/api/com.alipay.sofa/jraft-core/1.3.5/index.html

com.alipay.sofa.jraft



| com.alipay.sofa.jraft                 | 类型 | 说明 |
| ------------------------------------- | ---- | ---- |
| 接口                                  |      |      |
|                                       |      |      |
| CliService                            |      |      |
| Closure                               |      |      |
| FSMCaller                             |      |      |
| FSMCaller.LastAppliedLogIndexListener |      |      |
| Iterator                              |      |      |
| JRaftServiceFactory                   |      |      |
| Lifecycle                             |      |      |
| Node                                  |      |      |
| ReadOnlyService                       |      |      |
| ReplicatorGroup                       |      |      |
| StateMachine                          |      |      |
|                                       |      |      |
| 类                                    |      |      |
|                                       |      |      |
| JRaftUtils                            |      |      |
| NodeDescribeSignalHandler             |      |      |
| NodeManager                           |      |      |
| NodeMetricsSignalHandler              |      |      |
| RaftGroupService                      |      |      |
| RaftServiceFactory                    |      |      |
| RouteTable                            |      |      |
| Status                                |      |      |
| ThreadPoolMetricsSignalHandler        |      |      |

## com.alipay.sofa.jraft.closure

| com.alipay.sofa.jraft.closure | 类型 | 说明 |
| ----------------------------- | ---- | ---- |
| ClosureQueue                  |      |      |
| LoadSnapshotClosure           |      |      |
| SaveSnapshotClosure           |      |      |
| TaskClosure                   |      |      |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| CatchUpClosure                |      |      |
| ClosureQueueImpl              |      |      |
| JoinableClosure               |      |      |
| ReadIndexClosure              |      |      |
| SynchronizedClosure           |      |      |





## com.alipay.sofa.jraft.conf



Configuration

ConfigurationEntry

ConfigurationManager



## com.alipay.sofa.jraft.core



| com.alipay.sofa.jraft.core         | 类型 | 说明 |
| ---------------------------------- | ---- | ---- |
| Replicator.ReplicatorStateListener |      |      |
| Scheduler                          |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| BallotBox                          |      |      |
| CliServiceImpl                     |      |      |
| DefaultJRaftServiceFactory         |      |      |
| ElectionPriority                   |      |      |
| FSMCallerImpl                      |      |      |
| IteratorImpl                       |      |      |
| IteratorWrapper                    |      |      |
| NodeImpl                           |      |      |
| NodeMetrics                        |      |      |
| ReadOnlyServiceImpl                |      |      |
| Replicator                         |      |      |
| ReplicatorGroupImpl                |      |      |
| StateMachineAdapter                |      |      |
| TimerManager                       |      |      |
|                                    |      |      |
| 枚举                               |      |      |
|                                    |      |      |
| Replicator.State                   |      |      |
| ReplicatorType                     |      |      |
| State                              |      |      |



## com.alipay.sofa.jraft.entity



| com.alipay.sofa.jraft.entity                         | 类型 | 说明 |
| ---------------------------------------------------- | ---- | ---- |
| Checksum                                             |      |      |
| LocalFileMetaOutter.LocalFileMetaOrBuilder           |      |      |
| LocalStorageOutter.ConfigurationPBMetaOrBuilder      |      |      |
| LocalStorageOutter.LocalSnapshotPbMeta.FileOrBuilder |      |      |
| LocalStorageOutter.LocalSnapshotPbMetaOrBuilder      |      |      |
| LocalStorageOutter.LogPBMetaOrBuilder                |      |      |
| LocalStorageOutter.StablePBMetaOrBuilder             |      |      |
| RaftOutter.EntryMetaOrBuilder                        |      |      |
| RaftOutter.SnapshotMetaOrBuilder                     |      |      |
|                                                      |      |      |
| 类                                                   |      |      |
|                                                      |      |      |
| Ballot                                               |      |      |
| Ballot.PosHint                                       |      |      |
| Ballot.UnfoundPeerId                                 |      |      |
| EnumOutter                                           |      |      |
| LeaderChangeContext                                  |      |      |
| LocalFileMetaOutter                                  |      |      |
| LocalFileMetaOutter.LocalFileMeta                    |      |      |
| LocalFileMetaOutter.LocalFileMeta.Builder            |      |      |
| LocalStorageOutter                                   |      |      |
| LocalStorageOutter.ConfigurationPBMeta               |      |      |
| LocalStorageOutter.ConfigurationPBMeta.Builder       |      |      |
| LocalStorageOutter.LocalSnapshotPbMeta               |      |      |
| LocalStorageOutter.LocalSnapshotPbMeta.Builder       |      |      |
| LocalStorageOutter.LocalSnapshotPbMeta.File          |      |      |
| LocalStorageOutter.LocalSnapshotPbMeta.File.Builder  |      |      |
| LocalStorageOutter.LogPBMeta                         |      |      |
| LocalStorageOutter.LogPBMeta.Builder                 |      |      |
| LocalStorageOutter.StablePBMeta                      |      |      |
| LocalStorageOutter.StablePBMeta.Builder              |      |      |
| LogEntry                                             |      |      |
| LogId                                                |      |      |
| NodeId                                               |      |      |
| PeerId                                               |      |      |
| RaftOutter                                           |      |      |
| RaftOutter.EntryMeta                                 |      |      |
| RaftOutter.EntryMeta.Builder                         |      |      |
| RaftOutter.SnapshotMeta                              |      |      |
| RaftOutter.SnapshotMeta.Builder                      |      |      |
| ReadIndexState                                       |      |      |
| ReadIndexStatus                                      |      |      |
| Task                                                 |      |      |
| UserLog                                              |      |      |
|                                                      |      |      |
| 枚举                                                 |      |      |
|                                                      |      |      |
| EnumOutter.EntryType                                 |      |      |
| EnumOutter.ErrorType                                 |      |      |
| LocalFileMetaOutter.FileSource                       |      |      |



#### com.alipay.sofa.jraft.entity.codec



| com.alipay.sofa.jraft.entity.codec | 类型 | 说明 |
| ---------------------------------- | ---- | ---- |
| 接口                               |      |      |
|                                    |      |      |
| LogEntryCodecFactory               |      |      |
| LogEntryDecoder                    |      |      |
| LogEntryEncoder                    |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| AutoDetectDecoder                  |      |      |
| DefaultLogEntryCodecFactory        |      |      |



com.alipay.sofa.jraft.entity.codec.v1

LogEntryV1CodecFactory

V1Decoder

V1Encoder



#### com.alipay.sofa.jraft.entity.codec.v2



| com.alipay.sofa.jraft.entity.codec.v2 | 类型 | 说明 |
| ------------------------------------- | ---- | ---- |
| LogOutter.PBLogEntryOrBuilder         |      |      |
|                                       |      |      |
| 类                                    |      |      |
|                                       |      |      |
| LogEntryV2CodecFactory                |      |      |
| LogOutter                             |      |      |
| LogOutter.PBLogEntry                  |      |      |
| LogOutter.PBLogEntry.Builder          |      |      |
| V2Decoder                             |      |      |
| V2Encoder                             |      |      |



## com.alipay.sofa.jraft.error



| com.alipay.sofa.jraft.error   | 类型 | 说明 |
| ----------------------------- | ---- | ---- |
| RaftException                 |      |      |
|                               |      |      |
| 枚举                          |      |      |
|                               |      |      |
| RaftError                     |      |      |
|                               |      |      |
| 异常错误                      |      |      |
|                               |      |      |
| InvokeTimeoutException        |      |      |
| JRaftException                |      |      |
| LogEntryCorruptedException    |      |      |
| LogIndexOutOfBoundsException  |      |      |
| LogNotFoundException          |      |      |
| MessageClassNotFoundException |      |      |
| RemotingException             |      |      |
| RetryAgainException           |      |      |



## com.alipay.sofa.jraft.option



| com.alipay.sofa.jraft.option | 类型 | 说明 |
| ---------------------------- | ---- | ---- |
| BallotBoxOptions             |      |      |
| BootstrapOptions             |      |      |
| CliOptions                   |      |      |
| CopyOptions                  |      |      |
| FSMCallerOptions             |      |      |
| LogManagerOptions            |      |      |
| LogStorageOptions            |      |      |
| NodeOptions                  |      |      |
| RaftMetaStorageOptions       |      |      |
| RaftOptions                  |      |      |
| ReadOnlyServiceOptions       |      |      |
| ReplicatorGroupOptions       |      |      |
| ReplicatorOptions            |      |      |
| RpcOptions                   |      |      |
| SnapshotCopierOptions        |      |      |
| SnapshotExecutorOptions      |      |      |
|                              |      |      |
| 枚举                         |      |      |
|                              |      |      |
| ReadOnlyOption               |      |      |



## com.alipay.sofa.jraft.rpc



| com.alipay.sofa.jraft.rpc                       | 类型 | 说明 |
| ----------------------------------------------- | ---- | ---- |
| CliClientService                                |      |      |
| ClientService                                   |      |      |
| CliRequests.AddLearnersRequestOrBuilder         |      |      |
| CliRequests.AddPeerRequestOrBuilder             |      |      |
| CliRequests.AddPeerResponseOrBuilder            |      |      |
| CliRequests.ChangePeersRequestOrBuilder         |      |      |
| CliRequests.ChangePeersResponseOrBuilder        |      |      |
| CliRequests.GetLeaderRequestOrBuilder           |      |      |
| CliRequests.GetLeaderResponseOrBuilder          |      |      |
| CliRequests.GetPeersRequestOrBuilder            |      |      |
| CliRequests.GetPeersResponseOrBuilder           |      |      |
| CliRequests.LearnersOpResponseOrBuilder         |      |      |
| CliRequests.RemoveLearnersRequestOrBuilder      |      |      |
| CliRequests.RemovePeerRequestOrBuilder          |      |      |
| CliRequests.RemovePeerResponseOrBuilder         |      |      |
| CliRequests.ResetLearnersRequestOrBuilder       |      |      |
| CliRequests.ResetPeerRequestOrBuilder           |      |      |
| CliRequests.SnapshotRequestOrBuilder            |      |      |
| CliRequests.TransferLeaderRequestOrBuilder      |      |      |
| Connection                                      |      |      |
| InvokeCallback                                  |      |      |
| RaftClientService                               |      |      |
| RaftRpcFactory                                  |      |      |
| RaftRpcFactory.ConfigHelper                     |      |      |
| RaftServerService                               |      |      |
| RpcClient                                       |      |      |
| RpcContext                                      |      |      |
| RpcProcessor                                    |      |      |
| RpcProcessor.ExecutorSelector                   |      |      |
| RpcRequests.AppendEntriesRequestHeaderOrBuilder |      |      |
| RpcRequests.AppendEntriesRequestOrBuilder       |      |      |
| RpcRequests.AppendEntriesResponseOrBuilder      |      |      |
| RpcRequests.ErrorResponseOrBuilder              |      |      |
| RpcRequests.GetFileRequestOrBuilder             |      |      |
| RpcRequests.GetFileResponseOrBuilder            |      |      |
| RpcRequests.InstallSnapshotRequestOrBuilder     |      |      |
| RpcRequests.InstallSnapshotResponseOrBuilder    |      |      |
| RpcRequests.PingRequestOrBuilder                |      |      |
| RpcRequests.ReadIndexRequestOrBuilder           |      |      |
| RpcRequests.ReadIndexResponseOrBuilder          |      |      |
| RpcRequests.RequestVoteRequestOrBuilder         |      |      |
| RpcRequests.RequestVoteResponseOrBuilder        |      |      |
| RpcRequests.TimeoutNowRequestOrBuilder          |      |      |
| RpcRequests.TimeoutNowResponseOrBuilder         |      |      |
| RpcResponseClosure                              |      |      |
| RpcResponseFactory                              |      |      |
| RpcServer                                       |      |      |
|                                                 |      |      |
| 类                                              |      |      |
|                                                 |      |      |
| CliRequests                                     |      |      |
| CliRequests.AddLearnersRequest                  |      |      |
| CliRequests.AddLearnersRequest.Builder          |      |      |
| CliRequests.AddPeerRequest                      |      |      |
| CliRequests.AddPeerRequest.Builder              |      |      |
| CliRequests.AddPeerResponse                     |      |      |
| CliRequests.AddPeerResponse.Builder             |      |      |
| CliRequests.ChangePeersRequest                  |      |      |
| CliRequests.ChangePeersRequest.Builder          |      |      |
| CliRequests.ChangePeersResponse                 |      |      |
| CliRequests.ChangePeersResponse.Builder         |      |      |
| CliRequests.GetLeaderRequest                    |      |      |
| CliRequests.GetLeaderRequest.Builder            |      |      |
| CliRequests.GetLeaderResponse                   |      |      |
| CliRequests.GetLeaderResponse.Builder           |      |      |
| CliRequests.GetPeersRequest                     |      |      |
| CliRequests.GetPeersRequest.Builder             |      |      |
| CliRequests.GetPeersResponse                    |      |      |
| CliRequests.GetPeersResponse.Builder            |      |      |
| CliRequests.LearnersOpResponse                  |      |      |
| CliRequests.LearnersOpResponse.Builder          |      |      |
| CliRequests.RemoveLearnersRequest               |      |      |
| CliRequests.RemoveLearnersRequest.Builder       |      |      |
| CliRequests.RemovePeerRequest                   |      |      |
| CliRequests.RemovePeerRequest.Builder           |      |      |
| CliRequests.RemovePeerResponse                  |      |      |
| CliRequests.RemovePeerResponse.Builder          |      |      |
| CliRequests.ResetLearnersRequest                |      |      |
| CliRequests.ResetLearnersRequest.Builder        |      |      |
| CliRequests.ResetPeerRequest                    |      |      |
| CliRequests.ResetPeerRequest.Builder            |      |      |
| CliRequests.SnapshotRequest                     |      |      |
| CliRequests.SnapshotRequest.Builder             |      |      |
| CliRequests.TransferLeaderRequest               |      |      |
| CliRequests.TransferLeaderRequest.Builder       |      |      |
| InvokeContext                                   |      |      |
| ProtobufMsgFactory                              |      |      |
| ProtobufSerializer                              |      |      |
| RaftRpcServerFactory                            |      |      |
| RpcRequestClosure                               |      |      |
| RpcRequestProcessor                             |      |      |
| RpcRequests                                     |      |      |
| RpcRequests.AppendEntriesRequest                |      |      |
| RpcRequests.AppendEntriesRequest.Builder        |      |      |
| RpcRequests.AppendEntriesRequestHeader          |      |      |
| RpcRequests.AppendEntriesRequestHeader.Builder  |      |      |
| RpcRequests.AppendEntriesResponse               |      |      |
| RpcRequests.AppendEntriesResponse.Builder       |      |      |
| RpcRequests.ErrorResponse                       |      |      |
| RpcRequests.ErrorResponse.Builder               |      |      |
| RpcRequests.GetFileRequest                      |      |      |
| RpcRequests.GetFileRequest.Builder              |      |      |
| RpcRequests.GetFileResponse                     |      |      |
| RpcRequests.GetFileResponse.Builder             |      |      |
| RpcRequests.InstallSnapshotRequest              |      |      |
| RpcRequests.InstallSnapshotRequest.Builder      |      |      |
| RpcRequests.InstallSnapshotResponse             |      |      |
| RpcRequests.InstallSnapshotResponse.Builder     |      |      |
| RpcRequests.PingRequest                         |      |      |
| RpcRequests.PingRequest.Builder                 |      |      |
| RpcRequests.ReadIndexRequest                    |      |      |
| RpcRequests.ReadIndexRequest.Builder            |      |      |
| RpcRequests.ReadIndexResponse                   |      |      |
| RpcRequests.ReadIndexResponse.Builder           |      |      |
| RpcRequests.RequestVoteRequest                  |      |      |
| RpcRequests.RequestVoteRequest.Builder          |      |      |
| RpcRequests.RequestVoteResponse                 |      |      |
| RpcRequests.RequestVoteResponse.Builder         |      |      |
| RpcRequests.TimeoutNowRequest                   |      |      |
| RpcRequests.TimeoutNowRequest.Builder           |      |      |
| RpcRequests.TimeoutNowResponse                  |      |      |
| RpcRequests.TimeoutNowResponse.Builder          |      |      |
| RpcResponseClosureAdapter                       |      |      |
| RpcUtils                                        |      |      |



### com.alipay.sofa.jraft.rpc.impl



| com.alipay.sofa.jraft.rpc.impl | 类型 | 说明 |
| ------------------------------ | ---- | ---- |
| ConnectionClosedEventListener  |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| AbstractClientService          |      |      |
| BoltRaftRpcFactory             |      |      |
| BoltRpcClient                  |      |      |
| BoltRpcServer                  |      |      |
| FutureImpl                     |      |      |
| PingRequestProcessor           |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |
|                                |      |      |





#### com.alipay.sofa.jraft.rpc.impl.cli

| com.alipay.sofa.jraft.rpc.impl.cli        | 类型 | 说明 |
| ----------------------------------------- | ---- | ---- |
| AddLearnersRequestProcessor               |      |      |
| AddPeerRequestProcessor                   |      |      |
| BaseCliRequestProcessor                   |      |      |
| BaseCliRequestProcessor.CliRequestContext |      |      |
| ChangePeersRequestProcessor               |      |      |
| CliClientServiceImpl                      |      |      |
| GetLeaderRequestProcessor                 |      |      |
| GetPeersRequestProcessor                  |      |      |
| RemoveLearnersRequestProcessor            |      |      |
| RemovePeerRequestProcessor                |      |      |
| ResetLearnersRequestProcessor             |      |      |
| ResetPeerRequestProcessor                 |      |      |
| SnapshotRequestProcessor                  |      |      |
| TransferLeaderRequestProcessor            |      |      |

#### com.alipay.sofa.jraft.rpc.impl.core



| com.alipay.sofa.jraft.rpc.impl.core       | 类型 | 说明 |
| ----------------------------------------- | ---- | ---- |
| AddLearnersRequestProcessor               |      |      |
| AddPeerRequestProcessor                   |      |      |
| BaseCliRequestProcessor                   |      |      |
| BaseCliRequestProcessor.CliRequestContext |      |      |
| ChangePeersRequestProcessor               |      |      |
| CliClientServiceImpl                      |      |      |
| GetLeaderRequestProcessor                 |      |      |
| GetPeersRequestProcessor                  |      |      |
| RemoveLearnersRequestProcessor            |      |      |
| RemovePeerRequestProcessor                |      |      |
| ResetLearnersRequestProcessor             |      |      |
| ResetPeerRequestProcessor                 |      |      |
| SnapshotRequestProcessor                  |      |      |
| TransferLeaderRequestProcessor            |      |      |



## com.alipay.sofa.jraft.storage



| com.alipay.sofa.jraft.storage   | 类型 | 说明 |
| ------------------------------- | ---- | ---- |
| LogManager                      |      |      |
| LogManager.LastLogIndexListener |      |      |
| LogManager.NewLogCallback       |      |      |
| LogStorage                      |      |      |
| RaftMetaStorage                 |      |      |
| SnapshotExecutor                |      |      |
| SnapshotStorage                 |      |      |
| SnapshotThrottle                |      |      |
| Storage                         |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| FileService                     |      |      |
| LogManager.StableClosure        |      |      |



#### com.alipay.sofa.jraft.storage.impl



| com.alipay.sofa.jraft.storage.impl  | 类型 | 说明 |
| ----------------------------------- | ---- | ---- |
| RocksDBLogStorage.WriteContext      |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| LocalRaftMetaStorage                |      |      |
| LogManagerImpl                      |      |      |
| RocksDBLogStorage                   |      |      |
| RocksDBLogStorage.EmptyWriteContext |      |      |



com.alipay.sofa.jraft.storage.io

FileReader

类

LocalDirReader

ProtoBufFile

#### com.alipay.sofa.jraft.storage.log



| com.alipay.sofa.jraft.storage.log            | 类型 | 说明 |
| -------------------------------------------- | ---- | ---- |
| LibC                                         |      |      |
|                                              |      |      |
| 类                                           |      |      |
|                                              |      |      |
| AbortFile                                    |      |      |
| CheckpointFile                               |      |      |
| CheckpointFile.Checkpoint                    |      |      |
| RocksDBSegmentLogStorage                     |      |      |
| RocksDBSegmentLogStorage.BarrierWriteContext |      |      |
| RocksDBSegmentLogStorage.Builder             |      |      |
| SegmentFile                                  |      |      |
| SegmentFile.SegmentFileOptions               |      |      |
| SegmentFile.SegmentFileOptions.Builder       |      |      |
| SegmentFile.SegmentHeader                    |      |      |



#### com.alipay.sofa.jraft.storage.snapshot

| com.alipay.sofa.jraft.storage.snapshot | 类型 | 说明 |
| -------------------------------------- | ---- | ---- |
| Snapshot                               |      |      |
| SnapshotCopier                         |      |      |
| SnapshotExecutorImpl                   |      |      |
| SnapshotReader                         |      |      |
| SnapshotWriter                         |      |      |
| ThroughputSnapshotThrottle             |      |      |

#### com.alipay.sofa.jraft.storage.snapshot.local

| com.alipay.sofa.jraft.storage.snapshot.local | 类型 | 说明 |
| -------------------------------------------- | ---- | ---- |
| LocalSnapshot                                |      |      |
| LocalSnapshotCopier                          |      |      |
| LocalSnapshotMetaTable                       |      |      |
| LocalSnapshotReader                          |      |      |
| LocalSnapshotStorage                         |      |      |
| LocalSnapshotWriter                          |      |      |
| SnapshotFileReader                           |      |      |

com.alipay.sofa.jraft.storage.snapshot.remote



Session

类

CopySession

RemoteFileCopier

## com.alipay.sofa.jraft.util

| com.alipay.sofa.jraft.util           | 类型 | 说明 |
| ------------------------------------ | ---- | ---- |
| AdaptiveBufAllocator.Handle          |      |      |
| BytesUtil.ByteArrayComparator        |      |      |
| Copiable                             |      |      |
| Describer                            |      |      |
| Describer.Printer                    |      |      |
| JRaftSignalHandler                   |      |      |
| LogExceptionHandler.OnEventException |      |      |
| Recyclable                           |      |      |
| Recyclers.Handle                     |      |      |
| ThreadId.OnError                     |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| AdaptiveBufAllocator                 |      |      |
| ArrayDeque                           |      |      |
| AsciiStringUtil                      |      |      |
| Bits                                 |      |      |
| ByteBufferCollector                  |      |      |
| Bytes                                |      |      |
| BytesUtil                            |      |      |
| CountDownEvent                       |      |      |
| CRC64                                |      |      |
| CrcUtil                              |      |      |
| DebugStatistics                      |      |      |
| Describer.DefaultPrinter             |      |      |
| DisruptorBuilder                     |      |      |
| DisruptorMetricSet                   |      |      |
| Endpoint                             |      |      |
| ExecutorServiceHelper                |      |      |
| FileOutputSignalHandler              |      |      |
| Ints                                 |      |      |
| JRaftServiceLoader                   |      |      |
| LogExceptionHandler                  |      |      |
| LogScheduledThreadPoolExecutor       |      |      |
| LogThreadPoolExecutor                |      |      |
| MetricReporter                       |      |      |
| MetricReporter.Builder               |      |      |
| MetricScheduledThreadPoolExecutor    |      |      |
| MetricThreadPoolExecutor             |      |      |
| Mpsc                                 |      |      |
| NamedThreadFactory                   |      |      |
| NonReentrantLock                     |      |      |
| Platform                             |      |      |
| RecyclableByteBufferList             |      |      |
| Recyclers                            |      |      |
| RecycleUtil                          |      |      |
| RepeatedTimer                        |      |      |
| Requires                             |      |      |
| RpcFactoryHelper                     |      |      |
| SegmentList                          |      |      |
| SignalHelper                         |      |      |
| StorageOptionsFactory                |      |      |
| SystemPropertyUtil                   |      |      |
| ThreadHelper                         |      |      |
| ThreadHelper.Spinner                 |      |      |
| ThreadId                             |      |      |
| ThreadPoolMetricRegistry             |      |      |
| ThreadPoolMetricSet                  |      |      |
| ThreadPoolUtil                       |      |      |
| ThreadPoolUtil.PoolBuilder           |      |      |
| ThreadPoolUtil.ScheduledPoolBuilder  |      |      |
| Utils                                |      |      |
|                                      |      |      |
| 枚举                                 |      |      |
|                                      |      |      |
| DirectExecutor                       |      |      |
|                                      |      |      |
| 注释类型                             |      |      |
|                                      |      |      |
| OnlyForTest                          |      |      |
| SPI                                  |      |      |



com.alipay.sofa.jraft.util.concurrent





| com.alipay.sofa.jraft.util.concurrent      | 类型 | 说明 |
| ------------------------------------------ | ---- | ---- |
| ExecutorChooserFactory                     |      |      |
| ExecutorChooserFactory.ExecutorChooser     |      |      |
| FixedThreadsExecutorGroup                  |      |      |
| FixedThreadsExecutorGroupFactory           |      |      |
| RejectedExecutionHandler                   |      |      |
| SingleThreadExecutor                       |      |      |
|                                            |      |      |
| 类                                         |      |      |
|                                            |      |      |
| AdjustableSemaphore                        |      |      |
| ConcurrentHashSet                          |      |      |
| DefaultExecutorChooserFactory              |      |      |
| DefaultFixedThreadsExecutorGroup           |      |      |
| DefaultFixedThreadsExecutorGroupFactory    |      |      |
| DefaultSingleThreadExecutor                |      |      |
| LongHeldDetectingReadWriteLock             |      |      |
| MpscSingleThreadExecutor                   |      |      |
| RejectedExecutionHandlers                  |      |      |
|                                            |      |      |
| 枚举                                       |      |      |
|                                            |      |      |
| LongHeldDetectingReadWriteLock.AcquireMode |      |      |



### com.alipay.sofa.jraft.util.internal



| com.alipay.sofa.jraft.util.internal | 类型 | 说明 |
| ----------------------------------- | ---- | ---- |
| IntegerFieldUpdater                 |      |      |
| LongFieldUpdater                    |      |      |
| ReferenceFieldUpdater               |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| ThrowUtil                           |      |      |
| UnsafeUtf8Util                      |      |      |
| UnsafeUtil                          |      |      |
| UnsafeUtil.UnsafeAccessor           |      |      |
| Updaters                            |      |      |



#### com.alipay.sofa.jraft.util.timer

| com.alipay.sofa.jraft.util.timer | 类型 | 说明 |
| -------------------------------- | ---- | ---- |
| RaftTimerFactory                 |      |      |
| Timeout                          |      |      |
| Timer                            |      |      |
| TimerTask                        |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| DefaultRaftTimerFactory          |      |      |
| DefaultTimer                     |      |      |
| HashedWheelTimer                 |      |      |



## com.google.protobuf



| com.google.protobuf  | 类型 | 说明 |
| -------------------- | ---- | ---- |
| BytesCarrier         |      |      |
| ZeroByteStringHelper |      |      |