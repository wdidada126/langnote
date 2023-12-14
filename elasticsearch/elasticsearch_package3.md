# elasticsearch_package3





org.elasticsearch.discovery



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AckClusterStatePublishResponseHandler                        |      |      |
| Allows to wait for all nodes to reply to the publish of a new cluster state and notifies the ClusterStatePublisher.AckListener so that the cluster state update can be acknowledged |      |      |
| BlockingClusterStatePublishResponseHandler                   |      |      |
| Handles responses obtained when publishing a new cluster state from master to all non master nodes. |      |      |
| ConfiguredHostsResolver                                      |      |      |
|                                                              |      |      |
| Discovery                                                    |      |      |
| A pluggable module allowing to implement discovery of other nodes, publishing of the cluster state to all nodes, electing a master of the cluster that raises cluster state change events. |      |      |
| DiscoveryModule                                              |      |      |
| A module for loading classes for node discovery.             |      |      |
| DiscoverySettings                                            |      |      |
| Exposes common discovery settings that may be supported by all the different discovery implementations |      |      |
| DiscoveryStats                                               |      |      |
|                                                              |      |      |
| FileBasedSeedHostsProvider                                   |      |      |
| An implementation of SeedHostsProvider that reads hosts/ports from FileBasedSeedHostsProvider.UNICAST_HOSTS_FILE. |      |      |
| HandshakingTransportAddressConnector                         |      |      |
|                                                              |      |      |
| MasterNotDiscoveredException                                 |      |      |
|                                                              |      |      |
| PeerFinder                                                   |      |      |
|                                                              |      |      |
| PeersRequest                                                 |      |      |
|                                                              |      |      |
| ProbeConnectionResult                                        |      |      |
| The result of a "probe" connection to a transport address, if it successfully discovered a valid node and established a full connection with it. |      |      |
| SeedHostsProvider                                            |      |      |
| A pluggable provider of the list of seed hosts to use for discovery. |      |      |
| SeedHostsProvider.HostsResolver                              |      |      |
| Helper object that allows to resolve a list of hosts to a list of transport addresses. |      |      |
| SeedHostsResolver                                            |      |      |
|                                                              |      |      |
| SettingsBasedSeedHostsProvider                               |      |      |
| An implementation of SeedHostsProvider that reads hosts/ports from the "discovery.seed_hosts" node setting. |      |      |
| TransportAddressConnector                                    |      |      |





org.elasticsearch.discovery.zen



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| ElectMasterService                                           |      |      |
|                                                              |      |      |
| ElectMasterService.MasterCandidate                           |      |      |
| a class to encapsulate all the information about a candidate in a master election that is needed to decided which of the candidates should win |      |      |
| FaultDetection                                               |      |      |
| A base class for MasterFaultDetection & NodesFaultDetection, making sure both use the same setting. |      |      |
| MasterFaultDetection                                         |      |      |
| A fault detection that pings the master periodically to see if its alive. |      |      |
| MasterFaultDetection.Listener                                |      |      |
|                                                              |      |      |
| MasterFaultDetection.MasterPingRequest                       |      |      |
|                                                              |      |      |
| MasterFaultDetection.MasterPingResponseResponse              |      |      |
|                                                              |      |      |
| MasterFaultDetection.ThisIsNotTheMasterYouAreLookingForException |      |      |
| Thrown when a ping reaches the wrong node                    |      |      |
| MembershipAction                                             |      |      |
|                                                              |      |      |
| MembershipAction.JoinCallback                                |      |      |
|                                                              |      |      |
| MembershipAction.JoinRequest                                 |      |      |
|                                                              |      |      |
| MembershipAction.LeaveRequest                                |      |      |
|                                                              |      |      |
| MembershipAction.MembershipListener                          |      |      |
|                                                              |      |      |
| NodeJoinController                                           |      |      |
| This class processes incoming join request (passed zia ZenDiscovery). |      |      |
| NodeJoinController.ElectionCallback                          |      |      |
|                                                              |      |      |
| NodesFaultDetection                                          |      |      |
| A fault detection of multiple nodes.                         |      |      |
| NodesFaultDetection.Listener                                 |      |      |
|                                                              |      |      |
| NodesFaultDetection.PingRequest                              |      |      |
|                                                              |      |      |
| NodesFaultDetection.PingResponse                             |      |      |
|                                                              |      |      |
| PendingClusterStatesQueue                                    |      |      |
| A queue that holds all "in-flight" incoming cluster states from the master. |      |      |
| PendingClusterStateStats                                     |      |      |
| Class encapsulating stats about the PendingClusterStatsQueue |      |      |
| PingContextProvider                                          |      |      |
|                                                              |      |      |
| PublishClusterStateAction                                    |      |      |
|                                                              |      |      |
| PublishClusterStateAction.CommitClusterStateRequest          |      |      |
|                                                              |      |      |
| PublishClusterStateAction.IncomingClusterStateListener       |      |      |
|                                                              |      |      |
| PublishClusterStateStats                                     |      |      |
| Class encapsulating stats about the PublishClusterStateAction |      |      |
| UnicastZenPing                                               |      |      |
|                                                              |      |      |
| UnicastZenPing.UnicastPingRequest                            |      |      |
|                                                              |      |      |
| UnicastZenPing.UnicastPingResponse                           |      |      |
|                                                              |      |      |
| ZenDiscovery                                                 |      |      |
|                                                              |      |      |
| ZenDiscovery.RejoinClusterRequest                            |      |      |
|                                                              |      |      |
| ZenPing                                                      |      |      |
|                                                              |      |      |
| ZenPing.PingCollection                                       |      |      |
| a utility collection of pings where only the most recent ping is stored per node |      |      |
| ZenPing.PingResponse                                         |      |      |


ZenDiscovery
`ZenDiscovery` 类是 Elasticsearch 中的一个关键组件，负责集群的发现和节点的加入。它实现了 Elasticsearch 的自动发现和节点协调功能，确保集群中的节点能够相互发现和通信。

`ZenDiscovery` 类的主要作用如下：
1. 集群发现：`ZenDiscovery` 通过使用 Zen 协议（基于 gossip 协议）来实现集群中的节点发现。它通过在集群中的节点之间传播状态信息和变更事件，使得节点能够相互感知和发现彼此。这种自动发现机制使得新的节点能够加入集群，而无需手动配置节点信息。
2. 节点加入：一旦节点发现了集群中的其他节点，`ZenDiscovery` 负责协调新节点的加入过程。它将新节点的信息发送给集群中的主节点，并与主节点进行通信以完成加入过程。这包括分配节点ID、获取集群状态、同步索引等操作。
3. 节点通信：`ZenDiscovery` 确保集群中的节点能够相互通信和交互。它维护节点之间的连接和通信通道，使得节点能够发送和接收索引数据、搜索请求和集群状态信息等。
4. 主节点选举：在集群中，只有一个节点被选举为主节点，负责集群的决策和协调工作。`ZenDiscovery` 在主节点选举过程中起到重要的作用，它通过与其他节点进行竞选和协商，最终确定主节点。一旦主节点选举完成，集群中的其他节点将向该主节点报告并接受其指导。
总的来说，`ZenDiscovery` 类在 Elasticsearch 中扮演着集群发现和节点协调的核心角色。它通过自动发现和节点加入机制，确保集群中的节点能够相互发现和通信，以实现分布式的数据存储和处理能力。

org.elasticsearch.discovery.zen.ZenDiscovery#doStart
`org.elasticsearch.discovery.zen.ZenDiscovery#doStart` 是 Elasticsearch 中负责协调集群发现和节点加入的核心类的方法。下面是对该方法的源代码分析：

```java
protected synchronized void doStart() {
    if (transportService.getLocalNode().isMasterNode()) {
        // If this node is the elected master node, start the ZenDiscovery process
        logger.trace("starting to ping");
        pingTask = threadPool.scheduleWithFixedDelay(new Runnable() {
            @Override
            public void run() {
                try {
                    // Send a ping request to other nodes in the cluster
                    ping();
                } catch (Throwable e) {
                    logger.warn("unexpected failure during [zen-disco-join (elected_as_master) [" + getNodeAddress() + "]]", e);
                }
            }
        }, randomInitialDelay(), pingInterval, ThreadPool.Names.SAME);
    } else {
        // If this node is not the elected master node, start the join process
        logger.trace("starting to join");
        joinTask = threadPool.scheduleWithFixedDelay(new Runnable() {
            @Override
            public void run() {
                try {
                    // Send a join request to the master node
                    joinCluster();
                } catch (Throwable e) {
                    logger.warn("unexpected failure during [zen-disco-join (not_master) [" + getNodeAddress() + "]]", e);
                }
            }
        }, randomInitialDelay(), pingInterval, ThreadPool.Names.SAME);
    }
}
```

在这个方法中，根据当前节点是否为选举的主节点，采取不同的动作：

1. 如果当前节点是选举的主节点（`transportService.getLocalNode().isMasterNode()` 返回 `true`），则启动 ZenDiscovery 过程。这个过程将定期发送 ping 请求给集群中的其他节点。

2. 如果当前节点不是选举的主节点，则启动加入集群的过程。这个过程将定期发送 join 请求给主节点。

这两个过程都是由 `Runnable` 对象在后台线程中执行的，并通过 `threadPool.scheduleWithFixedDelay` 方法定期执行。执行时间间隔由 `pingInterval` 参数指定。

在方法的实现中，还包含了异常处理和日志记录，以捕获和处理在执行过程中可能发生的异常。

总的来说，`doStart` 方法是 ZenDiscovery 类的核心方法之一，负责启动集群发现和节点加入过程，以确保集群的正常运行和节点的连通性。



Zen 协议是 Elasticsearch 中使用的基于 gossip 协议的集群发现和节点协调协议。它允许节点在集群中自动发现和通信，以便进行数据复制、故障检测和集群状态同步等操作。
Zen 协议基于 gossip 协议的概念，其中节点通过相互交换状态信息和变更事件来传播集群的状态。节点定期选择随机的一组对等节点进行通信，并将自己的状态信息传播给这些节点。这种信息传播的随机性和分散性，使得集群中的节点能够快速地相互发现和了解彼此的状态。
Zen 协议的具体实现涉及到节点之间的网络通信和消息传递。节点通常通过多播或单播方式发送和接收消息，以确保消息能够在集群中传播。消息通常包含节点的状态信息、集群的状态、索引的分片信息、节点的加入和离开事件等。
要进行 Zen 协议的抓包操作，你可以使用网络抓包工具（如 Wireshark）来捕获节点之间的网络通信流量。通过设置过滤器和捕获规则，你可以选择捕获与 Zen 协议相关的网络流量，以便进一步分析和调试。
请注意，Zen 协议是 Elasticsearch 中较低层次的网络协议，它的具体实现可能会随着 Elasticsearch 版本的更新而有所变化。因此，在进行抓包操作时，你可能需要参考具体版本的 Elasticsearch 文档或相关资源，以了解 Zen 协议的详细信息和特定版本的实现细节。


org.elasticsearch.env



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| Environment                                                  |      |      |
| The environment of where things exists.                      |      |      |
| NodeEnvironment                                              |      |      |
| A component that holds all data paths for a single node.     |      |      |
| NodeEnvironment.DataPath                                     |      |      |
|                                                              |      |      |
| NodeEnvironment.NodeLock                                     |      |      |
|                                                              |      |      |
| NodeEnvironment.ShardLocker                                  |      |      |
| A functional interface that people can use to reference NodeEnvironment.shardLock(ShardId, String, long) |      |      |
| NodeMetadata                                                 |      |      |
| Metadata associated with this node: its persistent node ID and its version. |      |      |
| NodeRepurposeCommand                                         |      |      |
|                                                              |      |      |
| OverrideNodeVersionCommand                                   |      |      |
|                                                              |      |      |
| ShardLock                                                    |      |      |
| A shard lock guarantees exclusive access to a shards data directory. |      |      |
| ShardLockObtainFailedException                               |      |      |
| Exception used when the in-memory lock for a shard cannot be obtained |      |      |





org.elasticsearch.gateway



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AsyncShardFetch<T extends BaseNodeResponse>                  |      |      |      |
| Allows to asynchronously fetch shard related data from other nodes for allocation, without blocking the cluster update thread. |      |      |      |
| AsyncShardFetch.FetchResult<T extends BaseNodeResponse>      |      |      |      |
| The result of a fetch operation.                             |      |      |      |
| AsyncShardFetch.Lister<NodesResponse extends BaseNodesResponse<NodeResponse>,NodeResponse extends BaseNodeResponse> |      |      |      |
| An action that lists the relevant shard data that needs to be fetched. |      |      |      |
| BaseGatewayShardAllocator                                    |      |      |      |
| An abstract class that implements basic functionality for allocating shards to nodes based on shard copies that already exist in the cluster. |      |      |      |
| ClusterStateUpdaters                                         |      |      |      |
|                                                              |      |      |      |
| CorruptStateException                                        |      |      |      |
| This exception is thrown when Elasticsearch detects an inconsistency in one of it's persistent states. |      |      |      |
| DanglingIndicesState                                         |      |      |      |
| The dangling indices state is responsible for finding new dangling indices (indices that have their state written on disk, but don't exists in the metadata of the cluster), and importing them into the cluster. |      |      |      |
| Gateway                                                      |      |      |      |
|                                                              |      |      |      |
| Gateway.GatewayStateRecoveredListener                        |      |      |      |
|                                                              |      |      |      |
| GatewayAllocator                                             |      |      |      |
|                                                              |      |      |      |
| GatewayMetaState                                             |      |      |      |
| Loads (and maybe upgrades) cluster metadata at startup, and persistently stores cluster metadata for future restarts. |      |      |      |
| GatewayModule                                                |      |      |      |
|                                                              |      |      |      |
| GatewayService                                               |      |      |      |
|                                                              |      |      |      |
| IncrementalClusterStateWriter                                |      |      |      |
| Tracks the metadata written to disk, allowing updated metadata to be written incrementally (i.e. |      |      |      |
| LocalAllocateDangledIndices                                  |      |      |      |
|                                                              |      |      |      |
| LocalAllocateDangledIndices.AllocateDangledRequest           |      |      |      |
|                                                              |      |      |      |
| LocalAllocateDangledIndices.AllocateDangledResponse          |      |      |      |
|                                                              |      |      |      |
| MetadataStateFormat<T>                                       |      |      |      |
| MetadataStateFormat is a base class to write checksummed XContent based files to one or more directories in a standardized directory structure. |      |      |      |
| MetaStateService                                             |      |      |      |
| Handles writing and loading Manifest, Metadata and IndexMetadata |      |      |      |
| PersistedClusterStateService                                 |      |      |      |
| Stores cluster metadata in a bare Lucene index (per data path) split across a number of documents. |      |      |      |
| PersistedClusterStateService.OnDiskState                     |      |      |      |
|                                                              |      |      |      |
| PersistedClusterStateService.Writer                          |      |      |      |
|                                                              |      |      |      |
| PrimaryShardAllocator                                        |      |      |      |
| The primary shard allocator allocates unassigned primary shards to nodes that hold valid copies of the unassigned primaries. |      |      |      |
| PriorityComparator                                           |      |      |      |
| A comparator that compares ShardRouting instances based on various properties. |      |      |      |
| ReplicaShardAllocator                                        |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayMetaState                           |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayMetaState.NodeGatewayMetaState      |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayMetaState.NodeRequest               |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayMetaState.NodesGatewayMetaState     |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayMetaState.Request                   |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayStartedShards                       |      |      |      |
| This transport action is used to fetch the shard version from each node during primary allocation in GatewayAllocator. |      |      |      |
| TransportNodesListGatewayStartedShards.NodeGatewayStartedShards |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayStartedShards.NodeRequest           |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayStartedShards.NodesGatewayStartedShards |      |      |      |
|                                                              |      |      |      |
| TransportNodesListGatewayStartedShards.Request               |      |      |      |
|                                                              |      |      |      |
| WriteStateException                                          |      |      |      |
| This exception is thrown when there is a problem of writing state to disk. |      |      |      |







org.elasticsearch.http





| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AbstractHttpServerTransport                                  |      |      |
|                                                              |      |      |
| BindHttpException                                            |      |      |
|                                                              |      |      |
| CorsHandler                                                  |      |      |
| This file is forked from the https://netty.io project.       |      |      |
| CorsHandler.Config                                           |      |      |
|                                                              |      |      |
| DefaultRestChannel                                           |      |      |
| The default rest channel for incoming requests.              |      |      |
| HttpChannel                                                  |      |      |
|                                                              |      |      |
| HttpClientStatsTracker                                       |      |      |
| Tracks a collection of HttpStats.ClientStats for current and recently-closed HTTP connections. |      |      |
| HttpException                                                |      |      |
|                                                              |      |      |
| HttpHandlingSettings                                         |      |      |
|                                                              |      |      |
| HttpHeadersValidationException                               |      |      |
|                                                              |      |      |
| HttpInfo                                                     |      |      |
|                                                              |      |      |
| HttpPipelinedMessage                                         |      |      |
|                                                              |      |      |
| HttpPipelinedRequest                                         |      |      |
|                                                              |      |      |
| HttpPipelinedResponse                                        |      |      |
|                                                              |      |      |
| HttpPipeliningAggregator<Listener>                           |      |      |
|                                                              |      |      |
| HttpPreRequest                                               |      |      |
| A slim interface for precursors to HTTP requests, which doesn't expose access to the request's body, because it's not available yet. |      |      |
| HttpReadTimeoutException                                     |      |      |
|                                                              |      |      |
| HttpRequest                                                  |      |      |
| A basic http request abstraction.                            |      |      |
| HttpRequest.HttpVersion                                      |      |      |
|                                                              |      |      |
| HttpResponse                                                 |      |      |
| A basic http response abstraction.                           |      |      |
| HttpServerChannel                                            |      |      |
|                                                              |      |      |
| HttpServerTransport                                          |      |      |
|                                                              |      |      |
| HttpServerTransport.Dispatcher                               |      |      |
| Dispatches HTTP requests.                                    |      |      |
| HttpStats                                                    |      |      |
|                                                              |      |      |
| HttpStats.ClientStats                                        |      |      |
|                                                              |      |      |
| HttpTransportSettings                                        |      |      |
|                                                              |      |      |
| HttpUtils                                                    |      |      |



org.elasticsearch.index



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractIndexComponent                                       |      |      |      |
|                                                              |      |      |      |
| Index                                                        |      |      |      |
| A value class representing the basic required properties of an Elasticsearch index. |      |      |      |
| IndexComponent                                               |      |      |      |
|                                                              |      |      |      |
| IndexingPressure                                             |      |      |      |
|                                                              |      |      |      |
| IndexingSlowLog                                              |      |      |      |
|                                                              |      |      |      |
| IndexModule                                                  |      |      |      |
| IndexModule represents the central extension point for index level custom implementations like: Similarity - New Similarity implementations can be registered through IndexModule.addSimilarity(String, TriFunction) while existing Providers can be referenced through Settings under the IndexModule.SIMILARITY_SETTINGS_PREFIX prefix along with the "type" value. |      |      |      |
| IndexModule.Type                                             |      |      |      |
|                                                              |      |      |      |
| IndexNotFoundException                                       |      |      |      |
|                                                              |      |      |      |
| IndexService                                                 |      |      |      |
|                                                              |      |      |      |
| IndexService.IndexCreationContext                            |      |      |      |
|                                                              |      |      |      |
| IndexService.ShardStoreDeleter                               |      |      |      |
|                                                              |      |      |      |
| IndexSettings                                                |      |      |      |
| This class encapsulates all index level settings and handles settings updates. |      |      |      |
| IndexSortConfig                                              |      |      |      |
| Holds all the information that is used to build the sort order of an index. |      |      |      |
| IndexWarmer                                                  |      |      |      |
|                                                              |      |      |      |
| IndexWarmer.Listener                                         |      |      |      |
|                                                              |      |      |      |
| IndexWarmer.TerminationHandle                                |      |      |      |
| A handle on the execution of warm-up action.                 |      |      |      |
| MergePolicyConfig                                            |      |      |      |
| A shard in elasticsearch is a Lucene index, and a Lucene index is broken down into segments. |      |      |      |
| MergeSchedulerConfig                                         |      |      |      |
| The merge scheduler (ConcurrentMergeScheduler) controls the execution of merge operations once they are needed (according to the merge policy). |      |      |      |
| SearchSlowLog                                                |      |      |      |
|                                                              |      |      |      |
| SlowLogLevel                                                 |      |      |      |
|                                                              |      |      |      |
| VersionType                                                  |      |      |      |





org.elasticsearch.index.analysis



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AbstractCharFilterFactory                                    |      |      |      |      |
|                                                              |      |      |      |      |
| AbstractIndexAnalyzerProvider<T extends org.apache.lucene.analysis.Analyzer> |      |      |      |      |
|                                                              |      |      |      |      |
| AbstractTokenFilterFactory                                   |      |      |      |      |
|                                                              |      |      |      |      |
| AbstractTokenizerFactory                                     |      |      |      |      |
|                                                              |      |      |      |      |
| Analysis                                                     |      |      |      |      |
|                                                              |      |      |      |      |
| AnalysisMode                                                 |      |      |      |      |
| Enum representing the mode in which token filters and analyzers are allowed to operate. |      |      |      |      |
| AnalysisRegistry                                             |      |      |      |      |
| An internal registry for tokenizer, token filter, char filter and analyzer. |      |      |      |      |
| AnalyzerComponents                                           |      |      |      |      |
| A class that groups analysis components necessary to produce a custom analyzer. |      |      |      |      |
| AnalyzerComponentsProvider                                   |      |      |      |      |
| Analyzers that provide access to their token filters should implement this |      |      |      |      |
| AnalyzerProvider<T extends org.apache.lucene.analysis.Analyzer> |      |      |      |      |
|                                                              |      |      |      |      |
| AnalyzerScope                                                |      |      |      |      |
|                                                              |      |      |      |      |
| CharFilterFactory                                            |      |      |      |      |
|                                                              |      |      |      |      |
| CustomAnalyzer                                               |      |      |      |      |
|                                                              |      |      |      |      |
| CustomAnalyzerProvider                                       |      |      |      |      |
| A custom analyzer that is built out of a single Tokenizer and a list of TokenFilters. |      |      |      |      |
| CustomNormalizerProvider                                     |      |      |      |      |
| A custom normalizer that is built out of a char and token filters. |      |      |      |      |
| HunspellTokenFilterFactory                                   |      |      |      |      |
|                                                              |      |      |      |      |
| IndexAnalyzers                                               |      |      |      |      |
| IndexAnalyzers contains a name to analyzer mapping for a specific index. |      |      |      |      |
| KeywordAnalyzerProvider                                      |      |      |      |      |
|                                                              |      |      |      |      |
| LowercaseNormalizer                                          |      |      |      |      |
| Normalizer used to lowercase values                          |      |      |      |      |
| LowercaseNormalizerProvider                                  |      |      |      |      |
| Builds an analyzer for normalization that lowercases terms.  |      |      |      |      |
| NamedAnalyzer                                                |      |      |      |      |
| Named analyzer is an analyzer wrapper around an actual analyzer (NamedAnalyzer.analyzer that is associated with a name (NamedAnalyzer.name(). |      |      |      |      |
| NameOrDefinition                                             |      |      |      |      |
|                                                              |      |      |      |      |
| NormalizingCharFilterFactory                                 |      |      |      |      |
| A CharFilterFactory that also supports normalization The default implementation of NormalizingCharFilterFactory.normalize(Reader) delegates to CharFilterFactory.create(Reader) |      |      |      |      |
| NormalizingTokenFilterFactory                                |      |      |      |      |
| A TokenFilterFactory that may be used for normalization The default implementation delegates NormalizingTokenFilterFactory.normalize(TokenStream) to TokenFilterFactory.create(TokenStream)}. |      |      |      |      |
| PreBuiltAnalyzerProvider                                     |      |      |      |      |
|                                                              |      |      |      |      |
| PreBuiltAnalyzerProviderFactory                              |      |      |      |      |
|                                                              |      |      |      |      |
| PreConfiguredAnalysisComponent<T>                            |      |      |      |      |
| Shared implementation for pre-configured analysis components. |      |      |      |      |
| PreConfiguredCharFilter                                      |      |      |      |      |
| Provides pre-configured, shared CharFilters.                 |      |      |      |      |
| PreConfiguredTokenFilter                                     |      |      |      |      |
| Provides pre-configured, shared TokenFilters.                |      |      |      |      |
| PreConfiguredTokenizer                                       |      |      |      |      |
| Provides pre-configured, shared Tokenizers.                  |      |      |      |      |
| ReloadableCustomAnalyzer                                     |      |      |      |      |
|                                                              |      |      |      |      |
| ShingleTokenFilterFactory                                    |      |      |      |      |
|                                                              |      |      |      |      |
| ShingleTokenFilterFactory.Factory                            |      |      |      |      |
|                                                              |      |      |      |      |
| SimpleAnalyzerProvider                                       |      |      |      |      |
|                                                              |      |      |      |      |
| StandardAnalyzerProvider                                     |      |      |      |      |
|                                                              |      |      |      |      |
| StandardTokenizerFactory                                     |      |      |      |      |
|                                                              |      |      |      |      |
| StopAnalyzerProvider                                         |      |      |      |      |
|                                                              |      |      |      |      |
| StopTokenFilterFactory                                       |      |      |      |      |
|                                                              |      |      |      |      |
| TokenFilterFactory                                           |      |      |      |      |
|                                                              |      |      |      |      |
| TokenizerFactory                                             |      |      |      |      |
|                                                              |      |      |      |      |
| WhitespaceAnalyzerProvider                                   |      |      |      |      |





org.elasticsearch.index.cache





| Class      | Description |      |
| ---------- | ----------- | ---- |
| IndexCache |             |      |



org.elasticsearch.index.cache.bitset



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| BitsetFilterCache                                            |             |      |      |
| This is a cache for BitDocIdSet based filters and is unbounded by size or time. |             |      |      |
| BitsetFilterCache.Listener                                   |             |      |      |
| A listener interface that is executed for each onCache / onRemoval event |             |      |      |
| BitsetFilterCache.Value                                      |             |      |      |
|                                                              |             |      |      |
| ShardBitsetFilterCache                                       |             |      |      |



org.elasticsearch.index.cache.query

| Class                        |      | Description |      |
| ---------------------------- | ---- | ----------- | ---- |
|                              |      |             |      |
| DisabledQueryCache           |      |             |      |
|                              |      |             |      |
| IndexQueryCache              |      |             |      |
| The index-level query cache. |      |             |      |
| QueryCache                   |      |             |      |
|                              |      |             |      |
| QueryCacheStats              |      |             |      |



org.elasticsearch.index.cache.request



| Class             | Description                                                  |      |
| ----------------- | ------------------------------------------------------------ | ---- |
|                   |                                                              |      |
| RequestCacheStats |                                                              |      |
|                   |                                                              |      |
| ShardRequestCache | Tracks the portion of the request cache in use for a particular shard. |      |
|                   |                                                              |      |



org.elasticsearch.index.codec

| Class                             | Description                                                  |      |      |
| --------------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                                   |                                                              |      |      |
| CodecService                      | Since Lucene 4.0 low level index segments are read and written through a codec layer that allows to use use-case specific file formats & data-structures per field. |      |      |
|                                   |                                                              |      |      |
| PerFieldMappingPostingFormatCodec | This postings format is the default PostingsFormat for Elasticsearch. |      |      |
|                                   |                                                              |      |      |



org.elasticsearch.index.engine



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| CombinedDeletionPolicy                                       |      |      |
| An IndexDeletionPolicy that coordinates between Lucene's commits and the retention of translog generation files, making sure that all translog files that are needed to recover from the Lucene commit are not deleted. |      |      |
| CommitStats                                                  |      |      |
| a class the returns dynamic information with respect to the last commit point of this shard |      |      |
| DocumentMissingException                                     |      |      |
|                                                              |      |      |
| DocumentSourceMissingException                               |      |      |
|                                                              |      |      |
| Engine                                                       |      |      |
|                                                              |      |      |
| Engine.CommitId                                              |      |      |
|                                                              |      |      |
| Engine.Delete                                                |      |      |
|                                                              |      |      |
| Engine.DeleteResult                                          |      |      |
|                                                              |      |      |
| Engine.EventListener                                         |      |      |
|                                                              |      |      |
| Engine.Get                                                   |      |      |
|                                                              |      |      |
| Engine.GetResult                                             |      |      |
|                                                              |      |      |
| Engine.HistorySource                                         |      |      |
| Whether we should read history operations from translog or Lucene index |      |      |
| Engine.Index                                                 |      |      |
|                                                              |      |      |
| Engine.IndexCommitRef                                        |      |      |
|                                                              |      |      |
| Engine.IndexResult                                           |      |      |
|                                                              |      |      |
| Engine.IndexThrottle                                         |      |      |
| A throttling class that can be activated, causing the acquireThrottle method to block on a lock when throttling is enabled |      |      |
| Engine.NoOp                                                  |      |      |
|                                                              |      |      |
| Engine.NoOpLock                                              |      |      |
| A Lock implementation that always allows the lock to be acquired |      |      |
| Engine.NoOpResult                                            |      |      |
|                                                              |      |      |
| Engine.Operation                                             |      |      |
|                                                              |      |      |
| Engine.Operation.Origin                                      |      |      |
|                                                              |      |      |
| Engine.Operation.TYPE                                        |      |      |
| type of operation (index, delete), subclasses use static types |      |      |
| Engine.Result                                                |      |      |
| Base class for index and delete operation results Holds result meta data (e.g. |      |      |
| Engine.Result.Type                                           |      |      |
|                                                              |      |      |
| Engine.Searcher                                              |      |      |
|                                                              |      |      |
| Engine.SearcherScope                                         |      |      |
|                                                              |      |      |
| Engine.SearcherSupplier                                      |      |      |
|                                                              |      |      |
| Engine.SyncedFlushResult                                     |      |      |
|                                                              |      |      |
| Engine.TranslogRecoveryRunner                                |      |      |
|                                                              |      |      |
| Engine.Warmer                                                |      |      |
| Called for each new opened engine reader to warm new segments |      |      |
| EngineConfig                                                 |      |      |
|                                                              |      |      |
| EngineCreationFailureException                               |      |      |
| An exception indicating that an Engine creation failed.      |      |      |
| EngineException                                              |      |      |
|                                                              |      |      |
| EngineFactory                                                |      |      |
| Simple Engine Factory                                        |      |      |
| FlushFailedEngineException                                   |      |      |
|                                                              |      |      |
| InternalEngine                                               |      |      |
|                                                              |      |      |
| InternalEngine.DeletionStrategy                              |      |      |
|                                                              |      |      |
| InternalEngine.IndexingStrategy                              |      |      |
|                                                              |      |      |
| InternalEngineFactory                                        |      |      |
|                                                              |      |      |
| MissingHistoryOperationsException                            |      |      |
| Exception indicating that not all requested operations from LuceneChangesSnapshot are available. |      |      |
| NoOpEngine                                                   |      |      |
| NoOpEngine is an engine implementation that does nothing but the bare minimum required in order to have an engine. |      |      |
| ReadOnlyEngine                                               |      |      |
| A basic read-only engine that allows switching a shard to be true read-only temporarily or permanently. |      |      |
| RecoveryEngineException                                      |      |      |
|                                                              |      |      |
| RefreshFailedEngineException                                 |      |      |
|                                                              |      |      |
| SafeCommitInfo                                               |      |      |
| Information about the safe commit, for making decisions about recoveries. |      |      |
| Segment                                                      |      |      |
|                                                              |      |      |
| SegmentsStats                                                |      |      |
|                                                              |      |      |
| SegmentsStats.FileStats                                      |      |      |
|                                                              |      |      |
| VersionConflictEngineException                               |      |      |



org.elasticsearch.index.fielddata



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractBinaryDocValues                                      |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| AbstractNumericDocValues                                     |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| AbstractSortedDocValues                                      |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| AbstractSortedNumericDocValues                               |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| AbstractSortedSetDocValues                                   |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| AbstractSortingNumericDocValues                              |      |      |      |
| Base implementation that throws an IOException for the DocIdSetIterator APIs. |      |      |      |
| BinaryScriptFieldData                                        |      |      |      |
|                                                              |      |      |      |
| BinaryScriptFieldData.BinaryScriptLeafFieldData              |      |      |      |
|                                                              |      |      |      |
| BooleanScriptDocValues                                       |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldData                                       |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldData.BooleanScriptLeafFieldData            |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldData.Builder                               |      |      |      |
|                                                              |      |      |      |
| DateScriptFieldData                                          |      |      |      |
|                                                              |      |      |      |
| DateScriptFieldData.Builder                                  |      |      |      |
|                                                              |      |      |      |
| DateScriptFieldData.DateScriptLeafFieldData                  |      |      |      |
|                                                              |      |      |      |
| DocValueBits                                                 |      |      |      |
|                                                              |      |      |      |
| DoubleScriptDocValues                                        |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldData                                        |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldData.Builder                                |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldData.DoubleScriptLeafFieldData              |      |      |      |
|                                                              |      |      |      |
| FieldData                                                    |      |      |      |
| Utility methods, similar to Lucene's DocValues.              |      |      |      |
| FieldDataStats                                               |      |      |      |
|                                                              |      |      |      |
| FormattedDocValues                                           |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptDocValues                                      |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldData                                      |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldData.Builder                              |      |      |      |
|                                                              |      |      |      |
| GeoPointValues                                               |      |      |      |
| Per-document geo-point values.                               |      |      |      |
| HistogramValue                                               |      |      |      |
| Per-document histogram value.                                |      |      |      |
| HistogramValues                                              |      |      |      |
| Per-segment histogram values.                                |      |      |      |
| IndexFieldData<FD extends LeafFieldData>                     |      |      |      |
| Thread-safe utility class that allows to get per-segment values via the IndexFieldData.load(LeafReaderContext) method. |      |      |      |
| IndexFieldData.Builder                                       |      |      |      |
|                                                              |      |      |      |
| IndexFieldData.Global<FD extends LeafFieldData>              |      |      |      |
|                                                              |      |      |      |
| IndexFieldData.XFieldComparatorSource                        |      |      |      |
|                                                              |      |      |      |
| IndexFieldData.XFieldComparatorSource.Nested                 |      |      |      |
| Simple wrapper class around a filter that matches parent documents and a filter that matches child documents. |      |      |      |
| IndexFieldDataCache                                          |      |      |      |
| A simple field data cache abstraction on the *index* level.  |      |      |      |
| IndexFieldDataCache.Listener                                 |      |      |      |
|                                                              |      |      |      |
| IndexFieldDataCache.None                                     |      |      |      |
|                                                              |      |      |      |
| IndexFieldDataService                                        |      |      |      |
|                                                              |      |      |      |
| IndexGeoPointFieldData                                       |      |      |      |
| Specialization of IndexFieldData for geo points.             |      |      |      |
| IndexHistogramFieldData                                      |      |      |      |
| Specialization of IndexFieldData for histograms.             |      |      |      |
| IndexNumericFieldData                                        |      |      |      |
| Base class for numeric field data.                           |      |      |      |
| IndexNumericFieldData.NumericType                            |      |      |      |
| The type of number.                                          |      |      |      |
| IndexOrdinalsFieldData                                       |      |      |      |
| Specialization of IndexFieldData for data that is indexed with ordinals. |      |      |      |
| IpScriptDocValues                                            |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldData                                            |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldData.Builder                                    |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldData.IpScriptDocValues                          |      |      |      |
| Doc values implementation for ips.                           |      |      |      |
| LeafFieldData                                                |      |      |      |
| The thread safe LeafReader level cache of the data.          |      |      |      |
| LeafGeoPointFieldData                                        |      |      |      |
| LeafFieldData specialization for geo points.                 |      |      |      |
| LeafHistogramFieldData                                       |      |      |      |
| LeafFieldData specialization for histogram data.             |      |      |      |
| LeafNumericFieldData                                         |      |      |      |
| Specialization of LeafFieldData for numeric data.            |      |      |      |
| LeafOrdinalsFieldData                                        |      |      |      |
| Specialization of LeafFieldData for data that is indexed with ordinals. |      |      |      |
| LongScriptDocValues                                          |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldData                                          |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldData.Builder                                  |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldData.LongScriptLeafFieldData                  |      |      |      |
|                                                              |      |      |      |
| MultiGeoPointValues                                          |      |      |      |
| A stateful lightweight per document set of GeoPoint values.  |      |      |      |
| NumericDoubleValues                                          |      |      |      |
| A per-document numeric value.                                |      |      |      |
| RamAccountingTermsEnum                                       |      |      |      |
| TermsEnum that takes a CircuitBreaker, increasing the breaker every time .next(...) is called. |      |      |      |
| ScriptDocValues<T>                                           |      |      |      |
| Script level doc values, the assumption is that any implementation will implement a getValue method. |      |      |      |
| ScriptDocValues.Booleans                                     |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.BytesRefs                                    |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.Dates                                        |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.Doubles                                      |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.Geometry<T>                                  |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.GeoPoints                                    |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.Longs                                        |      |      |      |
|                                                              |      |      |      |
| ScriptDocValues.Strings                                      |      |      |      |
|                                                              |      |      |      |
| ShardFieldData                                               |      |      |      |
|                                                              |      |      |      |
| SortedBinaryDocValues                                        |      |      |      |
| A list of per-document binary values, sorted according to BytesRef.compareTo(BytesRef). |      |      |      |
| SortedNumericDoubleValues                                    |      |      |      |
| Clone of SortedNumericDocValues for double values.           |      |      |      |
| SortingBinaryDocValues                                       |      |      |      |
| Base class for building SortedBinaryDocValues instances based on unsorted content. |      |      |      |
| SortingNumericDocValues                                      |      |      |      |
| Base class for building SortedNumericDocValues instances based on unsorted content. |      |      |      |
| SortingNumericDoubleValues                                   |      |      |      |
| Base class for building SortedNumericDoubleValues instances based on unsorted content. |      |      |      |
| StringScriptDocValues                                        |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldData                                        |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldData.Builder                                |      |      |      |





org.elasticsearch.index.fielddata.fieldcomparator



| Class                                       |      |      |
| ------------------------------------------- | ---- | ---- |
| Description                                 |      |      |
| BytesRefFieldComparatorSource               |      |      |
| Comparator source for string/binary values. |      |      |
| DoubleValuesComparatorSource                |      |      |
| Comparator source for double values.        |      |      |
| FloatValuesComparatorSource                 |      |      |
| Comparator source for float values.         |      |      |
| LongValuesComparatorSource                  |      |      |
| Comparator source for long values.          |      |      |



org.elasticsearch.index.fielddata.ordinals

| Class                        | Description                                                  |      |
| ---------------------------- | ------------------------------------------------------------ | ---- |
|                              |                                                              |      |
| GlobalOrdinalsBuilder        | Utility class to build global ordinals.                      |      |
|                              |                                                              |      |
| GlobalOrdinalsIndexFieldData | Concrete implementation of IndexOrdinalsFieldData for global ordinals. |      |
|                              |                                                              |      |
| MultiOrdinals                | Ordinals implementation which is efficient at storing field data ordinals for multi-valued or sparse fields. |      |
|                              |                                                              |      |
| Ordinals                     | A thread safe ordinals abstraction.                          |      |
|                              |                                                              |      |
| Ordinals.ValuesHolder        |                                                              |      |
|                              |                                                              |      |
| OrdinalsBuilder              | Simple class to build document ID <-> ordinal mapping.       |      |
|                              |                                                              |      |
| SinglePackedOrdinals         |                                                              |      |



org.elasticsearch.index.fielddata.plain



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractIndexOrdinalsFieldData                               |      |      |      |
|                                                              |      |      |      |
| AbstractIndexOrdinalsFieldData.PerValueEstimator             |      |      |      |
| A PerValueEstimator is a sub-class that can be used to estimate the memory overhead for loading the data. |      |      |      |
| AbstractLatLonPointIndexFieldData                            |      |      |      |
|                                                              |      |      |      |
| AbstractLatLonPointIndexFieldData.Builder                    |      |      |      |
|                                                              |      |      |      |
| AbstractLatLonPointIndexFieldData.LatLonPointIndexFieldData  |      |      |      |
|                                                              |      |      |      |
| AbstractLeafGeoPointFieldData                                |      |      |      |
|                                                              |      |      |      |
| AbstractLeafOrdinalsFieldData                                |      |      |      |
|                                                              |      |      |      |
| BinaryDVLeafFieldData                                        |      |      |      |
| LeafFieldData impl on top of Lucene's binary doc values.     |      |      |      |
| BinaryIndexFieldData                                         |      |      |      |
|                                                              |      |      |      |
| BinaryIndexFieldData.Builder                                 |      |      |      |
|                                                              |      |      |      |
| BytesBinaryIndexFieldData                                    |      |      |      |
|                                                              |      |      |      |
| BytesBinaryIndexFieldData.Builder                            |      |      |      |
|                                                              |      |      |      |
| ConstantIndexFieldData                                       |      |      |      |
|                                                              |      |      |      |
| ConstantIndexFieldData.Builder                               |      |      |      |
|                                                              |      |      |      |
| LeafDoubleFieldData                                          |      |      |      |
| Specialization of LeafNumericFieldData for floating-point numerics. |      |      |      |
| LeafLongFieldData                                            |      |      |      |
| Specialization of LeafNumericFieldData for integers.         |      |      |      |
| PagedBytesIndexFieldData                                     |      |      |      |
|                                                              |      |      |      |
| PagedBytesIndexFieldData.Builder                             |      |      |      |
|                                                              |      |      |      |
| PagedBytesLeafFieldData                                      |      |      |      |
|                                                              |      |      |      |
| SortedNumericIndexFieldData                                  |      |      |      |
| FieldData backed by LeafReader.getSortedNumericDocValues(String) |      |      |      |
| SortedNumericIndexFieldData.Builder                          |      |      |      |
|                                                              |      |      |      |
| SortedSetBytesLeafFieldData                                  |      |      |      |
| An LeafFieldData implementation that uses Lucene SortedSetDocValues. |      |      |      |
| SortedSetOrdinalsIndexFieldData                              |      |      |      |
|                                                              |      |      |      |
| SortedSetOrdinalsIndexFieldData.Builder                      |      |      |      |
|                                                              |      |      |      |
| StringBinaryIndexFieldData                                   |      |      |      |





org.elasticsearch.index.fieldvisitor



| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| CustomFieldsVisitor                                          |             |      |
| A field visitor that allows to load a selection of the stored fields by exact name or by pattern. |             |      |
| FieldNamesProvidingStoredFieldsVisitor                       |             |      |
| Stored fields visitor which provides information about the field names that will be requested |             |      |
| FieldsVisitor                                                |             |      |
| Base StoredFieldVisitor that retrieves all non-redundant metadata. |             |      |
| SingleFieldsVisitor                                          |             |      |
| StoredFieldVisitor that loads a single field value.          |             |      |



org.elasticsearch.index.flush

| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| [FlushStats](D:\git\github\langnote\elasticsearch\elasticsearch-7.17.13-javadoc\org\elasticsearch\index\flush\FlushStats.html) |      |      |





org.elasticsearch.index.get



| Class           | Description |      |
| --------------- | ----------- | ---- |
| GetResult       |             |      |
| GetStats        |             |      |
| ShardGetService |             |      |



org.elasticsearch.index.mapper



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractGeometryFieldMapper<T>                               |      |      |      |
| Base field mapper class for all spatial field types          |      |      |      |
| AbstractGeometryFieldMapper.AbstractGeometryFieldType<T>     |      |      |      |
|                                                              |      |      |      |
| AbstractGeometryFieldMapper.Parser<T>                        |      |      |      |
| Interface representing parser in geometry indexing pipeline. |      |      |      |
| AbstractPointGeometryFieldMapper<T>                          |      |      |      |
| Base class for for spatial fields that only support indexing points |      |      |      |
| AbstractPointGeometryFieldMapper.PointParser<T>              |      |      |      |
| A base parser implementation for point formats               |      |      |      |
| AbstractShapeGeometryFieldMapper<T>                          |      |      |      |
| Base class for GeoShapeFieldMapper                           |      |      |      |
| AbstractShapeGeometryFieldMapper.AbstractShapeGeometryFieldType<T> |      |      |      |
|                                                              |      |      |      |
| AllFieldMapper                                               |      |      |      |
| Noop mapper that ensures that mappings created in 6x that explicitly disable the _all field can be restored in this version. |      |      |      |
| AllFieldMapper.Builder                                       |      |      |      |
|                                                              |      |      |      |
| AllFieldMapper.Defaults                                      |      |      |      |
|                                                              |      |      |      |
| ArraySourceValueFetcher                                      |      |      |      |
| An implementation of ValueFetcher that knows how to extract values from the document source. |      |      |      |
| BinaryFieldMapper                                            |      |      |      |
|                                                              |      |      |      |
| BinaryFieldMapper.BinaryFieldType                            |      |      |      |
|                                                              |      |      |      |
| BinaryFieldMapper.Builder                                    |      |      |      |
|                                                              |      |      |      |
| BinaryFieldMapper.CustomBinaryDocValuesField                 |      |      |      |
|                                                              |      |      |      |
| BooleanFieldMapper                                           |      |      |      |
| A field mapper for boolean fields.                           |      |      |      |
| BooleanFieldMapper.BooleanFieldType                          |      |      |      |
|                                                              |      |      |      |
| BooleanFieldMapper.Builder                                   |      |      |      |
|                                                              |      |      |      |
| BooleanFieldMapper.Defaults                                  |      |      |      |
|                                                              |      |      |      |
| BooleanFieldMapper.Values                                    |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldType                                       |      |      |      |
|                                                              |      |      |      |
| CompletionFieldMapper                                        |      |      |      |
| Mapper for completion field.                                 |      |      |      |
| CompletionFieldMapper.Builder                                |      |      |      |
| Builder for CompletionFieldMapper                            |      |      |      |
| CompletionFieldMapper.CompletionFieldType                    |      |      |      |
|                                                              |      |      |      |
| CompletionFieldMapper.Defaults                               |      |      |      |
|                                                              |      |      |      |
| CompletionFieldMapper.Fields                                 |      |      |      |
|                                                              |      |      |      |
| CompositeRuntimeField                                        |      |      |      |
| A runtime field of type object.                              |      |      |      |
| ConstantFieldType                                            |      |      |      |
| A MappedFieldType that has the same value for all documents. |      |      |      |
| ContentPath                                                  |      |      |      |
|                                                              |      |      |      |
| CustomDocValuesField                                         |      |      |      |
|                                                              |      |      |      |
| CustomTermFreqField                                          |      |      |      |
| Custom field that allows storing an integer value as a term frequency in lucene. |      |      |      |
| DataStreamTimestampFieldMapper                               |      |      |      |
| FieldMapper for the data-stream's timestamp meta-field.      |      |      |      |
| DataStreamTimestampFieldMapper.Builder                       |      |      |      |
|                                                              |      |      |      |
| DataStreamTimestampFieldMapper.TimestampFieldType            |      |      |      |
|                                                              |      |      |      |
| DateFieldMapper                                              |      |      |      |
| A FieldMapper for dates.                                     |      |      |      |
| DateFieldMapper.Builder                                      |      |      |      |
|                                                              |      |      |      |
| DateFieldMapper.DateFieldType                                |      |      |      |
|                                                              |      |      |      |
| DateFieldMapper.Resolution                                   |      |      |      |
|                                                              |      |      |      |
| DateScriptFieldType                                          |      |      |      |
|                                                              |      |      |      |
| DocCountFieldMapper                                          |      |      |      |
| Mapper for the doc_count field.                              |      |      |      |
| DocCountFieldMapper.DocCountFieldType                        |      |      |      |
|                                                              |      |      |      |
| DocumentMapper                                               |      |      |      |
|                                                              |      |      |      |
| DocumentParser                                               |      |      |      |
| A parser for documents                                       |      |      |      |
| DocumentParserContext                                        |      |      |      |
| Context used when parsing incoming documents.                |      |      |      |
| DocValueFetcher                                              |      |      |      |
| Value fetcher that loads from doc values.                    |      |      |      |
| DoubleScriptFieldType                                        |      |      |      |
|                                                              |      |      |      |
| DynamicFieldType                                             |      |      |      |
| Defines a MappedFieldType that exposes dynamic child field types If the field is named 'my_field', then a user is able to search on the field in both of the following ways: - Using the field name 'my_field', which will delegate to the field type as usual. |      |      |      |
| DynamicTemplate                                              |      |      |      |
|                                                              |      |      |      |
| DynamicTemplate.MatchType                                    |      |      |      |
|                                                              |      |      |      |
| DynamicTemplate.XContentFieldType                            |      |      |      |
| The type of a field as detected while parsing a json document. |      |      |      |
| FieldAliasMapper                                             |      |      |      |
| A mapper for field aliases.                                  |      |      |      |
| FieldAliasMapper.Builder                                     |      |      |      |
|                                                              |      |      |      |
| FieldAliasMapper.Names                                       |      |      |      |
|                                                              |      |      |      |
| FieldAliasMapper.TypeParser                                  |      |      |      |
|                                                              |      |      |      |
| FieldMapper                                                  |      |      |      |
|                                                              |      |      |      |
| FieldMapper.Builder                                          |      |      |      |
| A Builder for a ParametrizedFieldMapper                      |      |      |      |
| FieldMapper.Conflicts                                        |      |      |      |
|                                                              |      |      |      |
| FieldMapper.CopyTo                                           |      |      |      |
| Represents a list of fields with optional boost factor where the current field should be copied to |      |      |      |
| FieldMapper.CopyTo.Builder                                   |      |      |      |
|                                                              |      |      |      |
| FieldMapper.MergeValidator<T>                                |      |      |      |
|                                                              |      |      |      |
| FieldMapper.MultiFields                                      |      |      |      |
|                                                              |      |      |      |
| FieldMapper.MultiFields.Builder                              |      |      |      |
|                                                              |      |      |      |
| FieldMapper.Parameter<T>                                     |      |      |      |
| A configurable parameter for a field mapper                  |      |      |      |
| FieldMapper.Serializer<T>                                    |      |      |      |
| Serializes a parameter                                       |      |      |      |
| FieldMapper.SerializerCheck<T>                               |      |      |      |
| Check on whether or not a parameter should be serialized     |      |      |      |
| FieldMapper.TypeParser                                       |      |      |      |
| TypeParser implementation that automatically handles parsing |      |      |      |
| FieldNamesFieldMapper                                        |      |      |      |
| A mapper that indexes the field names of a document under _field_names. |      |      |      |
| FieldNamesFieldMapper.Defaults                               |      |      |      |
|                                                              |      |      |      |
| FieldNamesFieldMapper.FieldNamesFieldType                    |      |      |      |
|                                                              |      |      |      |
| GeoPointFieldMapper                                          |      |      |      |
| Field Mapper for geo_point types.                            |      |      |      |
| GeoPointFieldMapper.Builder                                  |      |      |      |
|                                                              |      |      |      |
| GeoPointFieldMapper.GeoPointFieldType                        |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldType                                      |      |      |      |
|                                                              |      |      |      |
| GeoShapeFieldMapper                                          |      |      |      |
| FieldMapper for indexing LatLonShapes.                       |      |      |      |
| GeoShapeFieldMapper.Builder                                  |      |      |      |
|                                                              |      |      |      |
| GeoShapeFieldMapper.GeoShapeFieldType                        |      |      |      |
|                                                              |      |      |      |
| GeoShapeIndexer                                              |      |      |      |
| Utility class that converts geometries into Lucene-compatible form for indexing in a geo_shape field. |      |      |      |
| GeoShapeParser                                               |      |      |      |
|                                                              |      |      |      |
| GeoShapeQueryable                                            |      |      |      |
| Implemented by MappedFieldType that support GeoShape queries. |      |      |      |
| IdFieldMapper                                                |      |      |      |
| A mapper for the _id field.                                  |      |      |      |
| IdFieldMapper.Defaults                                       |      |      |      |
|                                                              |      |      |      |
| IgnoredFieldMapper                                           |      |      |      |
| A field mapper that records fields that have been ignored because they were malformed. |      |      |      |
| IgnoredFieldMapper.Defaults                                  |      |      |      |
|                                                              |      |      |      |
| IgnoredFieldMapper.IgnoredFieldType                          |      |      |      |
|                                                              |      |      |      |
| IndexFieldMapper                                             |      |      |      |
|                                                              |      |      |      |
| IpFieldMapper                                                |      |      |      |
| A FieldMapper for ip addresses.                              |      |      |      |
| IpFieldMapper.Builder                                        |      |      |      |
|                                                              |      |      |      |
| IpFieldMapper.IpFieldType                                    |      |      |      |
|                                                              |      |      |      |
| IpFieldMapper.IpFieldType.IpScriptDocValues                  |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldType                                            |      |      |      |
|                                                              |      |      |      |
| KeywordFieldMapper                                           |      |      |      |
| A field mapper for keywords.                                 |      |      |      |
| KeywordFieldMapper.Builder                                   |      |      |      |
|                                                              |      |      |      |
| KeywordFieldMapper.Defaults                                  |      |      |      |
|                                                              |      |      |      |
| KeywordFieldMapper.KeywordField                              |      |      |      |
|                                                              |      |      |      |
| KeywordFieldMapper.KeywordFieldType                          |      |      |      |
|                                                              |      |      |      |
| KeywordScriptFieldType                                       |      |      |      |
|                                                              |      |      |      |
| LeafRuntimeField                                             |      |      |      |
| RuntimeField base class for leaf fields that will only ever return a single MappedFieldType from RuntimeField.asMappedFieldTypes(). |      |      |      |
| LongScriptFieldType                                          |      |      |      |
|                                                              |      |      |      |
| LuceneDocument                                               |      |      |      |
| Fork of Document with additional functionality.              |      |      |      |
| MappedFieldType                                              |      |      |      |
| This defines the core properties and functions to operate on a field. |      |      |      |
| MappedFieldType.CollapseType                                 |      |      |      |
|                                                              |      |      |      |
| MappedFieldType.Relation                                     |      |      |      |
| An enum used to describe the relation between the range of terms in a shard when compared with a query range |      |      |      |
| Mapper                                                       |      |      |      |
|                                                              |      |      |      |
| Mapper.Builder                                               |      |      |      |
|                                                              |      |      |      |
| Mapper.TypeParser                                            |      |      |      |
|                                                              |      |      |      |
| MapperBuilderContext                                         |      |      |      |
| Holds context for building Mapper objects from their Builders |      |      |      |
| MapperException                                              |      |      |      |
|                                                              |      |      |      |
| MapperParsingException                                       |      |      |      |
|                                                              |      |      |      |
| MapperRegistry                                               |      |      |      |
| A registry for all field mappers.                            |      |      |      |
| MapperService                                                |      |      |      |
|                                                              |      |      |      |
| MapperService.MergeReason                                    |      |      |      |
| The reason why a mapping is being merged.                    |      |      |      |
| Mapping                                                      |      |      |      |
| Wrapper around everything that defines a mapping, without references to utility classes like MapperService, ... |      |      |      |
| MappingLookup                                                |      |      |      |
| A (mostly) immutable snapshot of the current mapping of an index with access to everything we need for the search phase. |      |      |      |
| MappingLookup.CacheKey                                       |      |      |      |
| Key for the lookup to be used in caches.                     |      |      |      |
| MappingParser                                                |      |      |      |
| Parser for Mapping provided in CompressedXContent format     |      |      |      |
| MappingParserContext                                         |      |      |      |
| Holds everything that is needed to parse mappings.           |      |      |      |
| MetadataFieldMapper                                          |      |      |      |
| A mapper for a builtin field containing metadata about a document. |      |      |      |
| MetadataFieldMapper.Builder                                  |      |      |      |
|                                                              |      |      |      |
| MetadataFieldMapper.ConfigurableTypeParser                   |      |      |      |
|                                                              |      |      |      |
| MetadataFieldMapper.FixedTypeParser                          |      |      |      |
| A type parser for an unconfigurable metadata field.          |      |      |      |
| MetadataFieldMapper.TypeParser                               |      |      |      |
|                                                              |      |      |      |
| NestedObjectMapper                                           |      |      |      |
| A Mapper for nested objects                                  |      |      |      |
| NestedObjectMapper.Builder                                   |      |      |      |
|                                                              |      |      |      |
| NestedObjectMapper.TypeParser                                |      |      |      |
|                                                              |      |      |      |
| NestedValueFetcher                                           |      |      |      |
|                                                              |      |      |      |
| NumberFieldMapper                                            |      |      |      |
| A FieldMapper for numeric types: byte, short, int, long, float and double. |      |      |      |
| NumberFieldMapper.Builder                                    |      |      |      |
|                                                              |      |      |      |
| NumberFieldMapper.NumberFieldType                            |      |      |      |
|                                                              |      |      |      |
| NumberFieldMapper.NumberType                                 |      |      |      |
|                                                              |      |      |      |
| ObjectMapper                                                 |      |      |      |
|                                                              |      |      |      |
| ObjectMapper.Builder                                         |      |      |      |
|                                                              |      |      |      |
| ObjectMapper.Defaults                                        |      |      |      |
|                                                              |      |      |      |
| ObjectMapper.Dynamic                                         |      |      |      |
|                                                              |      |      |      |
| ObjectMapper.TypeParser                                      |      |      |      |
|                                                              |      |      |      |
| ParsedDocument                                               |      |      |      |
| The result of parsing a document.                            |      |      |      |
| RangeFieldMapper                                             |      |      |      |
| A FieldMapper for indexing numeric and date ranges, and creating queries |      |      |      |
| RangeFieldMapper.Builder                                     |      |      |      |
|                                                              |      |      |      |
| RangeFieldMapper.Defaults                                    |      |      |      |
|                                                              |      |      |      |
| RangeFieldMapper.Range                                       |      |      |      |
| Class defining a range                                       |      |      |      |
| RangeFieldMapper.RangeFieldType                              |      |      |      |
|                                                              |      |      |      |
| RangeType                                                    |      |      |      |
| Enum defining the type of range                              |      |      |      |
| RangeType.LengthType                                         |      |      |      |
|                                                              |      |      |      |
| RootObjectMapper                                             |      |      |      |
|                                                              |      |      |      |
| RootObjectMapper.Builder                                     |      |      |      |
|                                                              |      |      |      |
| RootObjectMapper.Defaults                                    |      |      |      |
|                                                              |      |      |      |
| RoutingFieldMapper                                           |      |      |      |
|                                                              |      |      |      |
| RoutingFieldMapper.Builder                                   |      |      |      |
|                                                              |      |      |      |
| RoutingFieldMapper.Defaults                                  |      |      |      |
|                                                              |      |      |      |
| RuntimeField                                                 |      |      |      |
| Definition of a runtime field that can be defined as part of the runtime section of the index mappings |      |      |      |
| RuntimeField.Builder                                         |      |      |      |
|                                                              |      |      |      |
| RuntimeField.Parser                                          |      |      |      |
| Parser for a runtime field.                                  |      |      |      |
| SeqNoFieldMapper                                             |      |      |      |
| Mapper for the _seq_no field.                                |      |      |      |
| SeqNoFieldMapper.SequenceIDFields                            |      |      |      |
| A sequence ID, which is made up of a sequence number (both the searchable and doc_value version of the field) and the primary term. |      |      |      |
| SimpleMappedFieldType                                        |      |      |      |
| MappedFieldType base impl for field types that are neither dates nor ranges. |      |      |      |
| SourceFieldMapper                                            |      |      |      |
|                                                              |      |      |      |
| SourceFieldMapper.Builder                                    |      |      |      |
|                                                              |      |      |      |
| SourceFieldMapper.Defaults                                   |      |      |      |
|                                                              |      |      |      |
| SourceToParse                                                |      |      |      |
|                                                              |      |      |      |
| SourceToParse.Origin                                         |      |      |      |
|                                                              |      |      |      |
| SourceValueFetcher                                           |      |      |      |
| An implementation of ValueFetcher that knows how to extract values from the document source. |      |      |      |
| StoredValueFetcher                                           |      |      |      |
| Value fetcher that loads from stored values.                 |      |      |      |
| StrictDynamicMappingException                                |      |      |      |
|                                                              |      |      |      |
| StringFieldType                                              |      |      |      |
| Base class for MappedFieldType implementations that use the same representation for internal index terms as the external representation so that partial matching queries such as prefix, wildcard and fuzzy queries can be implemented. |      |      |      |
| TermBasedFieldType                                           |      |      |      |
| Base MappedFieldType implementation for a field that is indexed with the inverted index. |      |      |      |
| TextFieldMapper                                              |      |      |      |
| A FieldMapper for full-text fields.                          |      |      |      |
| TextFieldMapper.Builder                                      |      |      |      |
|                                                              |      |      |      |
| TextFieldMapper.Defaults                                     |      |      |      |
|                                                              |      |      |      |
| TextFieldMapper.TextFieldType                                |      |      |      |
|                                                              |      |      |      |
| TextParams                                                   |      |      |      |
| Utility functions for text mapper parameters                 |      |      |      |
| TextParams.Analyzers                                         |      |      |      |
|                                                              |      |      |      |
| TextSearchInfo                                               |      |      |      |
| Encapsulates information about how to perform text searches over a field |      |      |      |
| TextSearchInfo.TermVector                                    |      |      |      |
| What sort of term vectors are available                      |      |      |      |
| TimeSeriesParams                                             |      |      |      |
| Utility functions for time series related mapper parameters  |      |      |      |
| TimeSeriesParams.MetricType                                  |      |      |      |
|                                                              |      |      |      |
| TypeFieldMapper                                              |      |      |      |
|                                                              |      |      |      |
| TypeFieldMapper.Defaults                                     |      |      |      |
|                                                              |      |      |      |
| TypeFieldMapper.TypeFieldType                                |      |      |      |
|                                                              |      |      |      |
| TypeFieldType                                                |      |      |      |
| Mediates access to the deprecated _type field                |      |      |      |
| TypeParsers                                                  |      |      |      |
|                                                              |      |      |      |
| Uid                                                          |      |      |      |
|                                                              |      |      |      |
| ValueFetcher                                                 |      |      |      |
| A helper class for fetching field values during the FetchFieldsPhase. |      |      |      |
| VersionFieldMapper                                           |      |      |      |
| Mapper for the _version field.                               |      |      |      |



org.elasticsearch.index.mapper.flattened



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| FlattenedFieldMapper                                         |      |      |      |
| A field mapper that accepts a JSON object and flattens it into a single field. |      |      |      |
| FlattenedFieldMapper.Builder                                 |      |      |      |
|                                                              |      |      |      |
| FlattenedFieldMapper.KeyedFlattenedFieldData                 |      |      |      |
| A field data implementation that gives access to the values associated with a particular JSON key. |      |      |      |
| FlattenedFieldMapper.KeyedFlattenedFieldData.Builder         |      |      |      |
|                                                              |      |      |      |
| FlattenedFieldMapper.KeyedFlattenedFieldType                 |      |      |      |
| A field type that represents the values under a particular JSON key, used when searching under a specific key as in 'my_flattened.key: some_value'. |      |      |      |
| FlattenedFieldMapper.RootFlattenedFieldType                  |      |      |      |
| A field type that represents all 'root' values.              |      |      |      |
| KeyedFlattenedLeafFieldData                                  |      |      |      |
| The atomic field data implementation for聽FlattenedFieldMapper.KeyedFlattenedFieldType. |      |      |      |



org.elasticsearch.index.merge



| Class                                               |      |      |      |
| --------------------------------------------------- | ---- | ---- | ---- |
| Description                                         |      |      |      |
| MergeStats                                          |      |      |      |
|                                                     |      |      |      |
| OnGoingMerge                                        |      |      |      |
| Represents a single on going merge within an index. |      |      |      |



org.elasticsearch.index.query



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractGeometryQueryBuilder<QB extends AbstractGeometryQueryBuilder<QB>> |      |      |      |
| Base QueryBuilder that builds a Geometry Query               |      |      |      |
| AbstractGeometryQueryBuilder.ParsedGeometryQueryParams       |      |      |      |
| local class that encapsulates xcontent parsed shape parameters |      |      |      |
| AbstractQueryBuilder<QB extends AbstractQueryBuilder<QB>>    |      |      |      |
| Base class for all classes producing lucene queries.         |      |      |      |
| BaseTermQueryBuilder<QB extends BaseTermQueryBuilder<QB>>    |      |      |      |
|                                                              |      |      |      |
| BoolQueryBuilder                                             |      |      |      |
| A Query that matches documents matching boolean combinations of other queries. |      |      |      |
| BoostingQueryBuilder                                         |      |      |      |
| The BoostingQuery class can be used to effectively demote results that match a given query. |      |      |      |
| CombinedFieldsQueryBuilder                                   |      |      |      |
| A query that matches on multiple text fields, as if the field contents had been indexed into a single combined field. |      |      |      |
| CommonTermsQueryBuilder                                      |      |      |      |
| Deprecated.                                                  |      |      |      |
| Since max_optimization optimization landed in 7.0, normal MatchQuery will achieve the same result without any configuration. |      |      |      |
| ConstantScoreQueryBuilder                                    |      |      |      |
| A query that wraps a filter and simply returns a constant score equal to the query boost for every document in the filter. |      |      |      |
| CoordinatorRewriteContext                                    |      |      |      |
| Context object used to rewrite QueryBuilder instances into simplified version in the coordinator. |      |      |      |
| CoordinatorRewriteContextProvider                            |      |      |      |
|                                                              |      |      |      |
| DateRangeIncludingNowQuery                                   |      |      |      |
| A simple wrapper class that indicates that the wrapped query has made use of NOW when parsing its datemath. |      |      |      |
| DisMaxQueryBuilder                                           |      |      |      |
| A query that generates the union of documents produced by its sub-queries, and that scores each document with the maximum score for that document as produced by any sub-query, plus a tie breaking increment for any additional matching sub-queries. |      |      |      |
| DistanceFeatureQueryBuilder                                  |      |      |      |
| A query to boost scores based on their proximity to the given origin for date, date_nanos and geo_point field types |      |      |      |
| DistanceFeatureQueryBuilder.Origin                           |      |      |      |
|                                                              |      |      |      |
| ExistsQueryBuilder                                           |      |      |      |
| Constructs a query that only match on documents that the field has a value in them. |      |      |      |
| FieldMaskingSpanQueryBuilder                                 |      |      |      |
|                                                              |      |      |      |
| FuzzyQueryBuilder                                            |      |      |      |
| A Query that does fuzzy matching for a specific value.       |      |      |      |
| GeoBoundingBoxQueryBuilder                                   |      |      |      |
| Creates a Lucene query that will filter for all documents that lie within the specified bounding box. |      |      |      |
| GeoDistanceQueryBuilder                                      |      |      |      |
| Filter results of a query to include only those within a specific distance to some geo point. |      |      |      |
| GeoExecType                                                  |      |      |      |
| Specifies how a geo query should be run.                     |      |      |      |
| GeoPolygonQueryBuilder                                       |      |      |      |
| Deprecated.                                                  |      |      |      |
| use GeoShapeQueryBuilder                                     |      |      |      |
| GeoShapeQueryBuilder                                         |      |      |      |
| Derived AbstractGeometryQueryBuilder that builds a lat, lon GeoShape Query. |      |      |      |
| GeoValidationMethod                                          |      |      |      |
| This enum is used to determine how to deal with invalid geo coordinates in geo related queries: On STRICT validation invalid coordinates cause an exception to be thrown. |      |      |      |
| IdsQueryBuilder                                              |      |      |      |
| A query that will return only documents matching specific ids (and a type). |      |      |      |
| InnerHitBuilder                                              |      |      |      |
|                                                              |      |      |      |
| InnerHitContextBuilder                                       |      |      |      |
| A builder for InnerHitsContext.InnerHitSubContext            |      |      |      |
| IntervalBuilder                                              |      |      |      |
| Constructs an IntervalsSource based on analyzed text         |      |      |      |
| IntervalFilterScript                                         |      |      |      |
| Base class for scripts used as interval filters, see IntervalsSourceProvider.IntervalFilter |      |      |      |
| IntervalFilterScript.Factory                                 |      |      |      |
|                                                              |      |      |      |
| IntervalFilterScript.Interval                                |      |      |      |
|                                                              |      |      |      |
| IntervalQueryBuilder                                         |      |      |      |
| Builder for IntervalQuery                                    |      |      |      |
| IntervalsSourceProvider                                      |      |      |      |
| Factory class for IntervalsSource Built-in sources include IntervalsSourceProvider.Match, which analyzes a text string and converts it to a proximity source (phrase, ordered or unordered depending on how strict the matching should be); IntervalsSourceProvider.Combine, which allows proximity queries between different sub-sources; and IntervalsSourceProvider.Disjunction. |      |      |      |
| IntervalsSourceProvider.Combine                              |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.Disjunction                          |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.Fuzzy                                |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.IntervalFilter                       |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.Match                                |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.Prefix                               |      |      |      |
|                                                              |      |      |      |
| IntervalsSourceProvider.Wildcard                             |      |      |      |
|                                                              |      |      |      |
| MatchAllQueryBuilder                                         |      |      |      |
| A query that matches on all documents.                       |      |      |      |
| MatchBoolPrefixQueryBuilder                                  |      |      |      |
| The boolean prefix query analyzes the input text and creates a boolean query containing a Term query for each term, except for the last term, which is used to create a prefix query |      |      |      |
| MatchNoneQueryBuilder                                        |      |      |      |
| A query that matches no document.                            |      |      |      |
| MatchPhrasePrefixQueryBuilder                                |      |      |      |
| Match query is a query that analyzes the text and constructs a phrase prefix query as the result of the analysis. |      |      |      |
| MatchPhraseQueryBuilder                                      |      |      |      |
| Match query is a query that analyzes the text and constructs a phrase query as the result of the analysis. |      |      |      |
| MatchQueryBuilder                                            |      |      |      |
| Match query is a query that analyzes the text and constructs a query as the result of the analysis. |      |      |      |
| MoreLikeThisQueryBuilder                                     |      |      |      |
| A more like this query that finds documents that are "like" the provided set of document(s). |      |      |      |
| MoreLikeThisQueryBuilder.Item                                |      |      |      |
| A single item to be used for a MoreLikeThisQueryBuilder.     |      |      |      |
| MultiMatchQueryBuilder                                       |      |      |      |
| Same as MatchQueryBuilder but supports multiple fields.      |      |      |      |
| MultiMatchQueryBuilder.Type                                  |      |      |      |
|                                                              |      |      |      |
| MultiTermQueryBuilder                                        |      |      |      |
|                                                              |      |      |      |
| NestedQueryBuilder                                           |      |      |      |
|                                                              |      |      |      |
| Operator                                                     |      |      |      |
|                                                              |      |      |      |
| ParsedQuery                                                  |      |      |      |
| The result of parsing a query.                               |      |      |      |
| PrefixQueryBuilder                                           |      |      |      |
| A Query that matches documents containing terms with a specified prefix. |      |      |      |
| QueryBuilder                                                 |      |      |      |
|                                                              |      |      |      |
| QueryBuilders                                                |      |      |      |
| Utility class to create search queries.                      |      |      |      |
| QueryParser<QB extends QueryBuilder>                         |      |      |      |
| Defines a query parser that is able to parse QueryBuilders from XContent. |      |      |      |
| QueryRewriteContext                                          |      |      |      |
| Context object used to rewrite QueryBuilder instances into simplified version. |      |      |      |
| QueryShardException                                          |      |      |      |
| Exception that is thrown when creating lucene queries on the shard |      |      |      |
| QueryStringQueryBuilder                                      |      |      |      |
| A query that parses a query string and runs it.              |      |      |      |
| QueryValidationException                                     |      |      |      |
| This exception can be used to indicate various reasons why validation of a query has failed. |      |      |      |
| RangeQueryBuilder                                            |      |      |      |
| A Query that matches documents within an range of terms.     |      |      |      |
| RegexpFlag                                                   |      |      |      |
| Regular expression syntax flags.                             |      |      |      |
| RegexpQueryBuilder                                           |      |      |      |
| A Query that does fuzzy matching for a specific value.       |      |      |      |
| Rewriteable<T>                                               |      |      |      |
| A basic interface for rewriteable classes.                   |      |      |      |
| ScriptQueryBuilder                                           |      |      |      |
|                                                              |      |      |      |
| SearchExecutionContext                                       |      |      |      |
| The context used to execute a search request on a shard.     |      |      |      |
| SearchIndexNameMatcher                                       |      |      |      |
| A predicate that checks whether an index pattern matches the current search shard target. |      |      |      |
| SimpleQueryStringBuilder                                     |      |      |      |
| SimpleQuery is a query parser that acts similar to a query_string query, but won't throw exceptions for any weird string syntax. |      |      |      |
| SimpleQueryStringFlag                                        |      |      |      |
| Flags for the XSimpleQueryString parser                      |      |      |      |
| SpanContainingQueryBuilder                                   |      |      |      |
| Builder for SpanContainingQuery.                             |      |      |      |
| SpanFirstQueryBuilder                                        |      |      |      |
|                                                              |      |      |      |
| SpanMultiTermQueryBuilder                                    |      |      |      |
| Query that allows wrapping a MultiTermQueryBuilder (one of wildcard, fuzzy, prefix, term, range or regexp query) as a SpanQueryBuilder so it can be nested. |      |      |      |
| SpanNearQueryBuilder                                         |      |      |      |
| Matches spans which are near one another.                    |      |      |      |
| SpanNearQueryBuilder.SpanGapQueryBuilder                     |      |      |      |
| SpanGapQueryBuilder enables gaps in a SpanNearQuery.         |      |      |      |
| SpanNotQueryBuilder                                          |      |      |      |
|                                                              |      |      |      |
| SpanOrQueryBuilder                                           |      |      |      |
| Span query that matches the union of its clauses.            |      |      |      |
| SpanQueryBuilder                                             |      |      |      |
| Marker interface for a specific type of QueryBuilder that allows to build span queries. |      |      |      |
| SpanQueryBuilder.SpanQueryBuilderUtil                        |      |      |      |
|                                                              |      |      |      |
| SpanTermQueryBuilder                                         |      |      |      |
| A Span Query that matches documents containing a term.       |      |      |      |
| SpanWithinQueryBuilder                                       |      |      |      |
| Builder for SpanWithinQuery.                                 |      |      |      |
| TermQueryBuilder                                             |      |      |      |
| A Query that matches documents containing a term.            |      |      |      |
| TermsQueryBuilder                                            |      |      |      |
| A filter for a field based on several terms matching on any of them. |      |      |      |
| TermsSetQueryBuilder                                         |      |      |      |
|                                                              |      |      |      |
| TypeQueryBuilder                                             |      |      |      |
|                                                              |      |      |      |
| WildcardQueryBuilder                                         |      |      |      |
| Implements the wildcard search query.                        |      |      |      |
| WrapperQueryBuilder                                          |      |      |      |
| A Query builder which allows building a query given JSON string or binary data provided as input. |      |      |      |
| ZeroTermsQueryOption                                         |      |      |      |





org.elasticsearch.index.query.functionscore



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| DecayFunction                                                |      |      |
| Implement this interface to provide a decay function that is executed on a distance. |      |      |
| DecayFunctionBuilder<DFB extends DecayFunctionBuilder<DFB>>  |      |      |
|                                                              |      |      |
| DecayFunctionBuilder.AbstractDistanceScoreFunction           |      |      |
| This is the base class for scoring a single field.           |      |      |
| DecayFunctionParser<DFB extends DecayFunctionBuilder<DFB>>   |      |      |
| Parser used for all decay functions, one instance each.      |      |      |
| ExponentialDecayFunctionBuilder                              |      |      |
|                                                              |      |      |
| FieldValueFactorFunctionBuilder                              |      |      |
| Builder to construct field_value_factor functions for a function score query. |      |      |
| FunctionScoreQueryBuilder                                    |      |      |
| A query that uses a filters with a script associated with them to compute the score. |      |      |
| FunctionScoreQueryBuilder.FilterFunctionBuilder              |      |      |
| Function to be associated with an optional filter, meaning it will be executed only for the documents that match the given filter. |      |      |
| GaussDecayFunctionBuilder                                    |      |      |
|                                                              |      |      |
| LinearDecayFunctionBuilder                                   |      |      |
|                                                              |      |      |
| RandomScoreFunctionBuilder                                   |      |      |
| A function that computes a random score for the matched documents |      |      |
| ScoreFunctionBuilder<FB extends ScoreFunctionBuilder<FB>>    |      |      |
|                                                              |      |      |
| ScoreFunctionBuilders                                        |      |      |
| Static method aliases for constructors of known ScoreFunctionBuilders. |      |      |
| ScoreFunctionParser<FB extends ScoreFunctionBuilder<FB>>     |      |      |
| Parses XContent into a ScoreFunctionBuilder.                 |      |      |
| ScriptScoreFunctionBuilder                                   |      |      |
| A function that uses a script to compute or influence the score of documents that match with the inner query or filter. |      |      |
| ScriptScoreQueryBuilder                                      |      |      |
| A query that computes a document score based on the provided script |      |      |
| WeightBuilder                                                |      |      |
| A query that multiplies the weight to the score.             |      |      |



org.elasticsearch.index.query.support

| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| NestedScope                                                  |             |      |      |
| During query parsing this keeps track of the current nested level. |             |      |      |
| QueryParsers                                                 |             |      |      |



org.elasticsearch.index.recovery

| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| RecoveryStats                                                |             |      |      |
| Recovery related statistics, starting at the shard level and allowing aggregation to indices and node level |             |      |      |





org.elasticsearch.index.refresh

| Class        |      |      |
| ------------ | ---- | ---- |
| Description  |      |      |
| RefreshStats |      |      |



org.elasticsearch.index.reindex

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractBulkByScrollRequest<Self extends AbstractBulkByScrollRequest<Self>> |      |      |      |
|                                                              |      |      |      |
| AbstractBulkByScrollRequestBuilder<Request extends AbstractBulkByScrollRequest<Request>,Self extends AbstractBulkByScrollRequestBuilder<Request,Self>> |      |      |      |
|                                                              |      |      |      |
| AbstractBulkIndexByScrollRequest<Self extends AbstractBulkIndexByScrollRequest<Self>> |      |      |      |
|                                                              |      |      |      |
| AbstractBulkIndexByScrollRequestBuilder<Request extends AbstractBulkIndexByScrollRequest<Request>,Self extends AbstractBulkIndexByScrollRequestBuilder<Request,Self>> |      |      |      |
|                                                              |      |      |      |
| BulkByScrollResponse                                         |      |      |      |
| Response used for actions that index many documents using a scroll request. |      |      |      |
| BulkByScrollTask                                             |      |      |      |
| Task storing information about a currently running BulkByScroll request. |      |      |      |
| BulkByScrollTask.Status                                      |      |      |      |
| Status of the reindex, update by query, or delete by query.  |      |      |      |
| BulkByScrollTask.StatusBuilder                               |      |      |      |
| This class acts as a builder for BulkByScrollTask.Status.    |      |      |      |
| BulkByScrollTask.StatusOrException                           |      |      |      |
| The status of a slice of the request.                        |      |      |      |
| ClientScrollableHitSource                                    |      |      |      |
| A scrollable source of hits from a Client instance.          |      |      |      |
| DeleteByQueryAction                                          |      |      |      |
|                                                              |      |      |      |
| DeleteByQueryRequest                                         |      |      |      |
| Creates a new DeleteByQueryRequest that uses scrolling and bulk requests to delete all documents matching the query. |      |      |      |
| DeleteByQueryRequestBuilder                                  |      |      |      |
|                                                              |      |      |      |
| LeaderBulkByScrollTaskState                                  |      |      |      |
| Tracks the state of sliced subtasks and provides unified status information for a sliced BulkByScrollRequest. |      |      |      |
| ReindexAction                                                |      |      |      |
|                                                              |      |      |      |
| ReindexRequest                                               |      |      |      |
| Request to reindex some documents from one index to another. |      |      |      |
| ReindexRequestBuilder                                        |      |      |      |
|                                                              |      |      |      |
| RejectAwareActionListener<T>                                 |      |      |      |
|                                                              |      |      |      |
| RemoteInfo                                                   |      |      |      |
|                                                              |      |      |      |
| ScrollableHitSource                                          |      |      |      |
| A scrollable source of results.                              |      |      |      |
| ScrollableHitSource.AsyncResponse                            |      |      |      |
|                                                              |      |      |      |
| ScrollableHitSource.BasicHit                                 |      |      |      |
| An implementation of ScrollableHitSource.Hit that uses getters and setters. |      |      |      |
| ScrollableHitSource.Hit                                      |      |      |      |
| A document returned as part of the response.                 |      |      |      |
| ScrollableHitSource.Response                                 |      |      |      |
| Response from each scroll batch.                             |      |      |      |
| ScrollableHitSource.SearchFailure                            |      |      |      |
| A failure during search.                                     |      |      |      |
| SuccessfullyProcessed                                        |      |      |      |
| Implemented by WorkerBulkByScrollTaskState and BulkByScrollTask.Status to consistently implement SuccessfullyProcessed.getSuccessfullyProcessed(). |      |      |      |
| UpdateByQueryAction                                          |      |      |      |
|                                                              |      |      |      |
| UpdateByQueryRequest                                         |      |      |      |
| Request to update some documents.                            |      |      |      |
| UpdateByQueryRequestBuilder                                  |      |      |      |
|                                                              |      |      |      |
| WorkerBulkByScrollTaskState                                  |      |      |      |
| Task behavior for BulkByScrollTask that does the actual work of querying and indexing |      |      |      |



org.elasticsearch.index.search

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ESToParentBlockJoinQuery                                     |      |      |      |
| A ToParentBlockJoinQuery that allows to retrieve its nested path. |      |      |      |
| MatchQueryParser                                             |      |      |      |
|                                                              |      |      |      |
| MatchQueryParser.Type                                        |      |      |      |
|                                                              |      |      |      |
| MultiMatchQueryParser                                        |      |      |      |
|                                                              |      |      |      |
| NestedHelper                                                 |      |      |      |
| Utility class to filter parent and children clauses when building nested queries. |      |      |      |
| QueryParserHelper                                            |      |      |      |
| Helpers to extract and expand field names and boosts         |      |      |      |
| QueryStringQueryParser                                       |      |      |      |
| A XQueryParser that uses the MapperService in order to build smarter queries based on the mapping information. |      |      |      |
| SimpleQueryStringQueryParser                                 |      |      |      |
| Wrapper class for Lucene's SimpleQueryStringQueryParser that allows us to redefine different types of queries. |      |      |      |
| SimpleQueryStringQueryParser.Settings                        |      |      |      |
| Class encapsulating the settings for the SimpleQueryString query, with their default values |      |      |      |



org.elasticsearch.index.search.stats



| Class                                  |      |      |      |
| -------------------------------------- | ---- | ---- | ---- |
| Description                            |      |      |      |
| FieldUsageStats                        |      |      |      |
|                                        |      |      |      |
| FieldUsageStats.PerFieldUsageStats     |      |      |      |
|                                        |      |      |      |
| FieldUsageStats.UsageContext           |      |      |      |
|                                        |      |      |      |
| SearchStats                            |      |      |      |
|                                        |      |      |      |
| SearchStats.Stats                      |      |      |      |
|                                        |      |      |      |
| ShardFieldUsageTracker                 |      |      |      |
| Records and provides field usage stats |      |      |      |
| ShardSearchStats                       |      |      |      |





org.elasticsearch.index.seqno



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| CountedBitSet                                                |      |      |
| A CountedBitSet wraps a FixedBitSet but automatically releases the internal bitset when all bits are set to reduce memory usage. |      |      |
| GlobalCheckpointSyncAction                                   |      |      |
| Background global checkpoint sync action initiated when a shard goes inactive. |      |      |
| GlobalCheckpointSyncAction.Request                           |      |      |
|                                                              |      |      |
| LocalCheckpointTracker                                       |      |      |
| This class generates sequences numbers and keeps track of the so-called "local checkpoint" which is the highest number for which all previous sequence numbers have been processed (inclusive). |      |      |
| ReplicationTracker                                           |      |      |
| This class is responsible for tracking the replication group with its progress and safety markers (local and global checkpoints). |      |      |
| ReplicationTracker.CheckpointState                           |      |      |
|                                                              |      |      |
| ReplicationTracker.PrimaryContext                            |      |      |
| Represents the sequence number component of the primary context. |      |      |
| RetentionLease                                               |      |      |
| A "shard history retention lease" (or "retention lease" for short) is conceptually a marker containing a retaining sequence number such that all operations with sequence number at least that retaining sequence number will be retained during merge operations (which could otherwise merge away operations that have been soft deleted). |      |      |
| RetentionLeaseActions                                        |      |      |
| This class holds all actions related to retention leases.    |      |      |
| RetentionLeaseActions.Add                                    |      |      |
|                                                              |      |      |
| RetentionLeaseActions.Add.TransportAction                    |      |      |
|                                                              |      |      |
| RetentionLeaseActions.AddRequest                             |      |      |
|                                                              |      |      |
| RetentionLeaseActions.Remove                                 |      |      |
|                                                              |      |      |
| RetentionLeaseActions.Remove.TransportAction                 |      |      |
|                                                              |      |      |
| RetentionLeaseActions.RemoveRequest                          |      |      |
|                                                              |      |      |
| RetentionLeaseActions.Renew                                  |      |      |
|                                                              |      |      |
| RetentionLeaseActions.Renew.TransportAction                  |      |      |
|                                                              |      |      |
| RetentionLeaseActions.RenewRequest                           |      |      |
|                                                              |      |      |
| RetentionLeaseAlreadyExistsException                         |      |      |
|                                                              |      |      |
| RetentionLeaseBackgroundSyncAction                           |      |      |
| Replication action responsible for background syncing retention leases to replicas. |      |      |
| RetentionLeaseBackgroundSyncAction.Request                   |      |      |
|                                                              |      |      |
| RetentionLeaseInvalidRetainingSeqNoException                 |      |      |
|                                                              |      |      |
| RetentionLeaseNotFoundException                              |      |      |
|                                                              |      |      |
| RetentionLeases                                              |      |      |
| Represents a versioned collection of retention leases.       |      |      |
| RetentionLeaseStats                                          |      |      |
| Represents retention lease stats.                            |      |      |
| RetentionLeaseSyncAction                                     |      |      |
| Write action responsible for syncing retention leases to replicas. |      |      |
| RetentionLeaseSyncAction.Request                             |      |      |
|                                                              |      |      |
| RetentionLeaseSyncAction.Response                            |      |      |
|                                                              |      |      |
| RetentionLeaseSyncer                                         |      |      |
|                                                              |      |      |
| RetentionLeaseSyncer.BackgroundSyncAction                    |      |      |
| Represents an action that is invoked periodically to sync retention leases to replica shards after some retention lease has been renewed or expired. |      |      |
| RetentionLeaseSyncer.SyncAction                              |      |      |
| Represents an action that is invoked to sync retention leases to replica shards after a retention lease is added or removed on the primary. |      |      |
| SeqNoStats                                                   |      |      |
|                                                              |      |      |
| SequenceNumbers                                              |      |      |
| A utility class for handling sequence numbers.               |      |      |
| SequenceNumbers.CommitInfo                                   |      |      |



org.elasticsearch.index.shard

| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AbstractIndexShardComponent                                  |      |      |
|                                                              |      |      |
| DocsStats                                                    |      |      |
|                                                              |      |      |
| ElasticsearchMergePolicy                                     |      |      |
| A MergePolicy that upgrades segments and can upgrade merges. |      |      |
| GlobalCheckpointListeners                                    |      |      |
| Represents a collection of global checkpoint listeners.      |      |      |
| GlobalCheckpointListeners.GlobalCheckpointListener           |      |      |
| A global checkpoint listener consisting of a callback that is notified when the global checkpoint is updated or the shard is closed. |      |      |
| IllegalIndexShardStateException                              |      |      |
|                                                              |      |      |
| IndexEventListener                                           |      |      |
| An index event listener is the primary extension point for plugins and build-in services to react / listen to per-index and per-shard events. |      |      |
| IndexingOperationListener                                    |      |      |
| An indexing listener for indexing, delete, events.           |      |      |
| IndexingOperationListener.CompositeListener                  |      |      |
| A Composite listener that multiplexes calls to each of the listeners methods. |      |      |
| IndexingStats                                                |      |      |
|                                                              |      |      |
| IndexingStats.Stats                                          |      |      |
|                                                              |      |      |
| IndexLongFieldRange                                          |      |      |
| Class representing an (inclusive) range of long values in a field in an index which may comprise multiple shards. |      |      |
| IndexSettingProvider                                         |      |      |
| An IndexSettingProvider is a provider for index level settings that can be set explicitly as a default value (so they show up as "set" for newly created indices) |      |      |
| IndexShard                                                   |      |      |
|                                                              |      |      |
| IndexShard.ShardFailure                                      |      |      |
| Simple struct encapsulating a shard failure                  |      |      |
| IndexShardClosedException                                    |      |      |
|                                                              |      |      |
| IndexShardComponent                                          |      |      |
|                                                              |      |      |
| IndexShardNotRecoveringException                             |      |      |
|                                                              |      |      |
| IndexShardNotStartedException                                |      |      |
|                                                              |      |      |
| IndexShardRecoveringException                                |      |      |
|                                                              |      |      |
| IndexShardRecoveryException                                  |      |      |
|                                                              |      |      |
| IndexShardRelocatedException                                 |      |      |
|                                                              |      |      |
| IndexShardStartedException                                   |      |      |
|                                                              |      |      |
| IndexShardState                                              |      |      |
|                                                              |      |      |
| PrimaryReplicaSyncer                                         |      |      |
|                                                              |      |      |
| PrimaryReplicaSyncer.ResyncRequest                           |      |      |
|                                                              |      |      |
| PrimaryReplicaSyncer.ResyncTask                              |      |      |
|                                                              |      |      |
| PrimaryReplicaSyncer.ResyncTask.Status                       |      |      |
|                                                              |      |      |
| PrimaryReplicaSyncer.SyncAction                              |      |      |
|                                                              |      |      |
| RefreshListeners                                             |      |      |
| Allows for the registration of listeners that are called when a change becomes visible for search. |      |      |
| RemoveCorruptedLuceneSegmentsAction                          |      |      |
| Removes corrupted Lucene index segments                      |      |      |
| RemoveCorruptedShardDataCommand                              |      |      |
|                                                              |      |      |
| RemoveCorruptedShardDataCommand.CleanStatus                  |      |      |
|                                                              |      |      |
| ReplicationGroup                                             |      |      |
| Replication group for a shard.                               |      |      |
| SearchOperationListener                                      |      |      |
| An listener for search, fetch and context events.            |      |      |
| SearchOperationListener.CompositeListener                    |      |      |
| A Composite listener that multiplexes calls to each of the listeners methods. |      |      |
| ShardCountStats                                              |      |      |
|                                                              |      |      |
| ShardId                                                      |      |      |
| Allows for shard level components to be injected with the shard id. |      |      |
| ShardLongFieldRange                                          |      |      |
| Class representing an (inclusive) range of long values in a field in a single shard. |      |      |
| ShardNotFoundException                                       |      |      |
|                                                              |      |      |
| ShardNotInPrimaryModeException                               |      |      |
|                                                              |      |      |
| ShardPath                                                    |      |      |
|                                                              |      |      |
| ShardStateMetadata                                           |      |      |
|                                                              |      |      |
| ShardToolCli                                                 |      |      |
| Class encapsulating and dispatching commands from the elasticsearch-shard command line tool |      |      |
| ShardUtils                                                   |      |      |



org.elasticsearch.index.similarity



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| NonNegativeScoresSimilarity                                  |      |      |
| A Similarity that rejects negative scores.                   |      |      |
| ScriptedSimilarity                                           |      |      |
| A Similarity implementation that allows scores to be scripted. |      |      |
| ScriptedSimilarity.Doc                                       |      |      |
| Statistics that are specific to a document.                  |      |      |
| ScriptedSimilarity.Field                                     |      |      |
| Statistics that are specific to a given field.               |      |      |
| ScriptedSimilarity.Query                                     |      |      |
| Scoring factors that come from the query.                    |      |      |
| ScriptedSimilarity.Term                                      |      |      |
| Statistics that are specific to a given term.                |      |      |
| SimilarityProvider                                           |      |      |
| Wrapper around a Similarity and its name.                    |      |      |
| SimilarityService                                            |      |      |



org.elasticsearch.index.snapshots



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
| IndexShardRestoreException                                   |             |      |      |
| Generic shard restore exception                              |             |      |      |
| IndexShardRestoreFailedException                             |             |      |      |
| Thrown when restore of a shard fails                         |             |      |      |
| IndexShardSnapshotException                                  |             |      |      |
| Generic shard snapshot exception                             |             |      |      |
| IndexShardSnapshotFailedException                            |             |      |      |
| Thrown when snapshot process is failed on a shard level      |             |      |      |
| IndexShardSnapshotStatus                                     |             |      |      |
| Represent shard snapshot status                              |             |      |      |
| IndexShardSnapshotStatus.Copy                                |             |      |      |
| Returns an immutable state of聽IndexShardSnapshotStatus聽at a given point in time. |             |      |      |
| IndexShardSnapshotStatus.Stage                               |             |      |      |
| Snapshot stage                                               |             |      |      |





org.elasticsearch.index.snapshots.blobstore

| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| BlobStoreIndexShardSnapshot                                  |             |      |      |
| Shard snapshot metadata                                      |             |      |      |
| BlobStoreIndexShardSnapshot.FileInfo                         |             |      |      |
| Information about snapshotted file                           |             |      |      |
| BlobStoreIndexShardSnapshots                                 |             |      |      |
| Contains information about all snapshots for the given shard in repository |             |      |      |
| RateLimitingInputStream                                      |             |      |      |
| Rate limiting wrapper for InputStream                        |             |      |      |
| RateLimitingInputStream.Listener                             |             |      |      |
|                                                              |             |      |      |
| SlicedInputStream                                            |             |      |      |
| A聽SlicedInputStream聽is a logical concatenation one or more input streams. |             |      |      |
| SnapshotFiles                                                |             |      |      |
| Contains a list of files participating in a snapshot         |             |      |      |



org.elasticsearch.index.stats





| Class                 |      | Description |
| --------------------- | ---- | ----------- |
| IndexingPressureStats |      |             |



org.elasticsearch.index.store





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| FsDirectoryFactory                                           |      |      |      |
| 聽                                                           |      |      |      |
| ImmutableDirectoryException                                  |      |      |      |
| Exception thrown if trying to mutate files in an immutable directory. |      |      |      |
| LuceneFilesExtensions                                        |      |      |      |
| 聽                                                           |      |      |      |
| Store                                                        |      |      |      |
| A Store provides plain access to files written by an elasticsearch index shard. |      |      |      |
| Store.MetadataSnapshot                                       |      |      |      |
| Represents a snapshot of the current directory build from the latest Lucene commit. |      |      |      |
| Store.OnClose                                                |      |      |      |
| A listener that is executed once the store is closed and all references to it are released |      |      |      |
| Store.RecoveryDiff                                           |      |      |      |
| A class representing the diff between a recovery source and recovery target |      |      |      |
| StoreFileMetadata                                            |      |      |      |
| 聽                                                           |      |      |      |
| StoreStats                                                   |      |      |      |
| 聽                                                           |      |      |      |
| VerifyingIndexOutput                                         |      |      |      |
| abstract class for verifying what was written.               |      |      |      |



org.elasticsearch.index.termvectors



| Class              | Description |      |
| ------------------ | ----------- | ---- |
|                    |             |      |
| TermVectorsService |             |      |



org.elasticsearch.index.translog



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| BaseTranslogReader                                           |             |      |      |
| A base class for all classes that allows reading ops from translog files |             |      |      |
| BufferedChecksumStreamInput                                  |             |      |      |
| Similar to Lucene's BufferedChecksumIndexInput, however this wraps a StreamInput so anything read will update the checksum |             |      |      |
| BufferedChecksumStreamOutput                                 |             |      |      |
| Similar to Lucene's BufferedChecksumIndexOutput, however this wraps a StreamOutput so anything written will update the checksum |             |      |      |
| ChannelFactory                                               |             |      |      |
| only for testing until we have a disk-full FileSystem        |             |      |      |
| TragicExceptionHolder                                        |             |      |      |
|                                                              |             |      |      |
| Translog                                                     |             |      |      |
| A Translog is a per index shard component that records all non-committed index operations in a durable manner. |             |      |      |
| Translog.Delete                                              |             |      |      |
|                                                              |             |      |      |
| Translog.Durability                                          |             |      |      |
|                                                              |             |      |      |
| Translog.Index                                               |             |      |      |
|                                                              |             |      |      |
| Translog.Location                                            |             |      |      |
|                                                              |             |      |      |
| Translog.NoOp                                                |             |      |      |
|                                                              |             |      |      |
| Translog.Operation                                           |             |      |      |
| A generic interface representing an operation performed on the transaction log. |             |      |      |
| Translog.Operation.Type                                      |             |      |      |
|                                                              |             |      |      |
| Translog.Snapshot                                            |             |      |      |
| A snapshot of the transaction log, allows to iterate over all the transaction log operations. |             |      |      |
| Translog.Source                                              |             |      |      |
|                                                              |             |      |      |
| Translog.TranslogGeneration                                  |             |      |      |
| References a transaction log generation                      |             |      |      |
| TranslogConfig                                               |             |      |      |
|                                                              |             |      |      |
| TranslogCorruptedException                                   |             |      |      |
|                                                              |             |      |      |
| TranslogDeletionPolicy                                       |             |      |      |
|                                                              |             |      |      |
| TranslogException                                            |             |      |      |
|                                                              |             |      |      |
| TranslogReader                                               |             |      |      |
| an immutable translog filereader                             |             |      |      |
| TranslogStats                                                |             |      |      |
|                                                              |             |      |      |
| TranslogWriter                                               |             |      |      |
|                                                              |             |      |      |
| TruncatedTranslogException                                   |             |      |      |
|                                                              |             |      |      |
| TruncateTranslogAction                                       |             |      |      |





org.elasticsearch.index.warmer

| Class                   |      |      |
| ----------------------- | ---- | ---- |
| Description             |      |      |
| ShardIndexWarmerService |      |      |
|                         |      |      |
| WarmerStats             |      |      |



org.elasticsearch.indices



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AliasFilterParsingException                                  |      |      |      |
|                                                              |      |      |      |
| AssociatedIndexDescriptor                                    |      |      |      |
| An "associated index" is an index that is related to or derived from a system index, but should not be considered a system index, usually because it is meant to be visible to users. |      |      |      |
| ESCacheHelper                                                |      |      |      |
| Cache helper that allows swapping in implementations that are different to Lucene's IndexReader.CacheHelper which ties its lifecycle to that of the underlying reader. |      |      |      |
| ESCacheHelper.ClosedListener                                 |      |      |      |
|                                                              |      |      |      |
| ESCacheHelper.Wrapper                                        |      |      |      |
| Implementation of ESCacheHelper that wraps an IndexReader.CacheHelper. |      |      |      |
| ExecutorNames                                                |      |      |      |
| A class that gathers the names of thread pool executors that should be used for a particular system index or system data stream. |      |      |      |
| ExecutorSelector                                             |      |      |      |
| Some operations need to use different executors for different index patterns. |      |      |      |
| IndexClosedException                                         |      |      |      |
| Exception indicating that one or more requested indices are closed. |      |      |      |
| IndexCreationException                                       |      |      |      |
|                                                              |      |      |      |
| IndexingMemoryController                                     |      |      |      |
|                                                              |      |      |      |
| IndexPatternMatcher                                          |      |      |      |
| An IndexPatternMatcher holds an index pattern in a string and, given a Metadata object, can return a list of index names matching that pattern. |      |      |      |
| IndexPrimaryShardNotAllocatedException                       |      |      |      |
| Thrown when some action cannot be performed because the primary shard of some shard group in an index has not been allocated post api action. |      |      |      |
| IndexTemplateMissingException                                |      |      |      |
|                                                              |      |      |      |
| IndicesModule                                                |      |      |      |
| Configures classes and services that are shared by indices on each node. |      |      |      |
| IndicesQueryCache                                            |      |      |      |
|                                                              |      |      |      |
| IndicesRequestCache                                          |      |      |      |
| The indices request cache allows to cache a shard level request stage responses, helping with improving similar requests that are potentially expensive (because of aggs for example). |      |      |      |
| IndicesService                                               |      |      |      |
|                                                              |      |      |      |
| IndicesService.ShardDeletionCheckResult                      |      |      |      |
| result type returned by signaling different reasons why a shard can / cannot be deleted |      |      |      |
| InvalidAliasNameException                                    |      |      |      |
|                                                              |      |      |      |
| InvalidIndexNameException                                    |      |      |      |
|                                                              |      |      |      |
| InvalidIndexTemplateException                                |      |      |      |
|                                                              |      |      |      |
| InvalidTypeNameException                                     |      |      |      |
|                                                              |      |      |      |
| NodeIndicesStats                                             |      |      |      |
| Global information on indices stats running on a specific node. |      |      |      |
| ShardLimitValidator                                          |      |      |      |
| This class contains the logic used to check the cluster-wide shard limit before shards are created and ensuring that the limit is updated correctly on setting updates, etc. |      |      |      |
| SystemDataStreamDescriptor                                   |      |      |      |
| Describes a DataStream that is reserved for use by a system component. |      |      |      |
| SystemDataStreamDescriptor.Type                              |      |      |      |
|                                                              |      |      |      |
| SystemIndexDescriptor                                        |      |      |      |
| A system index descriptor describes one or more system indices. |      |      |      |
| SystemIndexDescriptor.Builder                                |      |      |      |
| Provides a fluent API for building a SystemIndexDescriptor.  |      |      |      |
| SystemIndexDescriptor.Type                                   |      |      |      |
| The specific type of system index that this descriptor represents. |      |      |      |
| SystemIndexManager                                           |      |      |      |
| This class ensures that all system indices have up-to-date mappings, provided those indices can be automatically managed. |      |      |      |
| SystemIndices                                                |      |      |      |
| This class holds the SystemIndexDescriptor objects that represent system indices the node knows about. |      |      |      |
| SystemIndices.Feature                                        |      |      |      |
| Class holding a description of a stateful feature.           |      |      |      |
| SystemIndices.Feature.MigrationCompletionHandler             |      |      |      |
| Type for the handler that's invoked when all of a feature's system indices have been migrated. |      |      |      |
| SystemIndices.Feature.MigrationPreparationHandler            |      |      |      |
| Type for the handler that's invoked prior to migrating a Feature's system indices. |      |      |      |
| SystemIndices.SystemIndexAccessLevel                         |      |      |      |
|                                                              |      |      |      |
| TermsLookup                                                  |      |      |      |
| Encapsulates the parameters needed to fetch terms.           |      |      |      |
| TimestampFieldMapperService                                  |      |      |      |
| Tracks the mapping of the @timestamp field of immutable indices that expose their timestamp range in their index metadata. |      |      |      |
| TypeMissingException                                         |      |      |      |





org.elasticsearch.indices.analysis



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AnalysisModule                                               |      |      |      |
| Sets up AnalysisRegistry.                                    |      |      |      |
| AnalysisModule.AnalysisProvider<T>                           |      |      |      |
| The basic factory interface for analysis components.         |      |      |      |
| HunspellService                                              |      |      |      |
| Serves as a node level registry for hunspell dictionaries.   |      |      |      |
| PreBuiltAnalyzers                                            |      |      |      |
|                                                              |      |      |      |
| PreBuiltCacheFactory                                         |      |      |      |
|                                                              |      |      |      |
| PreBuiltCacheFactory.CachingStrategy                         |      |      |      |
| The strategy of caching the analyzer ONE Exactly one version is stored. |      |      |      |
| PreBuiltCacheFactory.PreBuiltCache<T>                        |      |      |      |
|                                                              |      |      |      |
| PreBuiltTokenizers                                           |      |      |      |



org.elasticsearch.indices.breaker





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AllCircuitBreakerStats                                       |      |      |      |
| Stats class encapsulating all of the different circuit breaker stats |      |      |      |
| BreakerSettings                                              |      |      |      |
| Settings for a聽CircuitBreaker                               |      |      |      |
| CircuitBreakerService                                        |      |      |      |
| Interface for Circuit Breaker services, which provide breakers to classes that load field data. |      |      |      |
| CircuitBreakerStats                                          |      |      |      |
| Class encapsulating stats about the circuit breaker          |      |      |      |
| HierarchyCircuitBreakerService                               |      |      |      |
| CircuitBreakerService that attempts to redistribute space between breakers if tripped |      |      |      |
| NoneCircuitBreakerService                                    |      |      |      |
| Class that returns a breaker that never breaks               |      |      |      |





org.elasticsearch.indices.cluster





| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| IndicesClusterStateService                                   |             |      |      |
|                                                              |             |      |      |
| IndicesClusterStateService.AllocatedIndex<T extends IndicesClusterStateService.Shard> |             |      |      |
|                                                              |             |      |      |
| IndicesClusterStateService.AllocatedIndices<T extends IndicesClusterStateService.Shard,U extends IndicesClusterStateService.AllocatedIndex<T>> |             |      |      |
|                                                              |             |      |      |
| IndicesClusterStateService.AllocatedIndices.IndexRemovalReason |             |      |      |
|                                                              |             |      |      |
| IndicesClusterStateService.Shard                             |             |      |      |



org.elasticsearch.indices.fielddata.cache



| Class                                  |      | Description |      |
| -------------------------------------- | ---- | ----------- | ---- |
|                                        |      |             |      |
| IndicesFieldDataCache                  |      |             |      |
|                                        |      |             |      |
| IndicesFieldDataCache.FieldDataWeigher |      |             |      |
|                                        |      |             |      |
| IndicesFieldDataCache.Key              |      |             |      |





org.elasticsearch.indices.flush





org.elasticsearch.indices.recovery





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ShardsSyncedFlushResult                                      |      |      |      |
| Result for all copies of a shard                             |      |      |      |
| SyncedFlushService                                           |      |      |      |
|                                                              |      |      |      |
| SyncedFlushService.InFlightOpsRequest                        |      |      |      |
|                                                              |      |      |      |
| SyncedFlushService.PreShardSyncedFlushRequest                |      |      |      |
|                                                              |      |      |      |
| SyncedFlushService.ShardSyncedFlushRequest                   |      |      |      |
|                                                              |      |      |      |
| SyncedFlushService.ShardSyncedFlushResponse                  |      |      |      |
| Response for third step of synced flush (writing the sync id) for one shard copy |      |      |      |





org.elasticsearch.indices.recovery.plan



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| PeerOnlyRecoveryPlannerService                               |             |      |      |
| Service in charge of computing a ShardRecoveryPlan using only the physical files from the source peer. |             |      |      |
| RecoveryPlannerService                                       |             |      |      |
|                                                              |             |      |      |
| ShardRecoveryPlan                                            |             |      |      |
|                                                              |             |      |      |
| ShardRecoveryPlan.SnapshotFilesToRecover                     |             |      |      |
|                                                              |             |      |      |
| ShardSnapshot                                                |             |      |      |
|                                                              |             |      |      |
| ShardSnapshotsService                                        |             |      |      |
|                                                              |             |      |      |
| SnapshotsRecoveryPlannerService                              |             |      |      |





org.elasticsearch.indices.store



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| CompositeIndexFoldersDeletionListener                        |             |      |      |
|                                                              |             |      |      |
| IndicesStore                                                 |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata                         |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata.NodeRequest             |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata.NodesStoreFilesMetadata |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata.NodeStoreFilesMetadata  |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata.Request                 |             |      |      |
|                                                              |             |      |      |
| TransportNodesListShardStoreMetadata.StoreFilesMetadata      |             |      |      |







org.elasticsearch.ingest





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractProcessor                                            |      |      |      |
| An Abstract Processor that holds tag and description information about the processor. |      |      |      |
| CompoundProcessor                                            |      |      |      |
| A Processor that executes a list of other "processors".      |      |      |      |
| ConditionalProcessor                                         |      |      |      |
|                                                              |      |      |      |
| ConfigurationUtils                                           |      |      |      |
|                                                              |      |      |      |
| DropProcessor                                                |      |      |      |
| Drop processor only returns null for the execution result to indicate that any document executed by it should not be indexed. |      |      |      |
| DropProcessor.Factory                                        |      |      |      |
|                                                              |      |      |      |
| IngestDocument                                               |      |      |      |
| Represents a single document being captured before indexing and holds the source and metadata (like id, type and index). |      |      |      |
| IngestDocument.Metadata                                      |      |      |      |
|                                                              |      |      |      |
| IngestInfo                                                   |      |      |      |
|                                                              |      |      |      |
| IngestMetadata                                               |      |      |      |
| Holds the ingest pipelines that are available in the cluster |      |      |      |
| IngestProcessorException                                     |      |      |      |
| A dedicated wrapper for exceptions encountered executing an ingest processor. |      |      |      |
| IngestService                                                |      |      |      |
| Holder class for several ingest related services.            |      |      |      |
| IngestStats                                                  |      |      |      |
|                                                              |      |      |      |
| IngestStats.PipelineStat                                     |      |      |      |
| Container for pipeline stats.                                |      |      |      |
| IngestStats.ProcessorStat                                    |      |      |      |
| Container for processor stats.                               |      |      |      |
| IngestStats.Stats                                            |      |      |      |
|                                                              |      |      |      |
| Pipeline                                                     |      |      |      |
| A pipeline is a list of Processor instances grouped under a unique id. |      |      |      |
| PipelineConfiguration                                        |      |      |      |
| Encapsulates a pipeline's id and configuration as a blob     |      |      |      |
| PipelineProcessor                                            |      |      |      |
|                                                              |      |      |      |
| PipelineProcessor.Factory                                    |      |      |      |
|                                                              |      |      |      |
| Processor                                                    |      |      |      |
| A processor implementation may modify the data belonging to a document. |      |      |      |
| Processor.Factory                                            |      |      |      |
| A factory that knows how to construct a processor based on a map of maps. |      |      |      |
| Processor.Parameters                                         |      |      |      |
| Infrastructure class that holds services that can be used by processor factories to create processor instances and that gets passed around to all IngestPlugins. |      |      |      |
| ProcessorInfo                                                |      |      |      |
|                                                              |      |      |      |
| TrackingResultProcessor                                      |      |      |      |
| Processor to be used within Simulate API to keep track of processors executed in pipeline. |      |      |      |
| ValueSource                                                  |      |      |      |
| Holds a value.                                               |      |      |      |
| ValueSource.ByteValue                                        |      |      |      |
|                                                              |      |      |      |
| ValueSource.ListValue                                        |      |      |      |
|                                                              |      |      |      |
| ValueSource.MapValue                                         |      |      |      |
|                                                              |      |      |      |
| ValueSource.ObjectValue                                      |      |      |      |
|                                                              |      |      |      |
| ValueSource.TemplatedValue                                   |      |      |      |
|                                                              |      |      |      |
| WrappingProcessor                                            |      |      |      |
| A srapping processor is one that encapsulates an inner processor, or a processor that the wrapped processor enacts upon. |      |      |      |



org.elasticsearch.monitor



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| MonitorService                                               |             |      |      |
|                                                              |             |      |      |
| NodeHealthService                                            |             |      |      |
|                                                              |             |      |      |
| Probes                                                       |             |      |      |
|                                                              |             |      |      |
| StatusInfo                                                   |             |      |      |
| Class that represents the Health status for a node as determined by NodeHealthService and provides additional info explaining the reasons |             |      |      |
| StatusInfo.Status                                            |             |      |      |





org.elasticsearch.monitor.fs



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| FsHealthService                                              |             |      |      |
| Runs periodically and attempts to create a temp file to see if the filesystem is writable. |             |      |      |
| FsInfo                                                       |             |      |      |
|                                                              |             |      |      |
| FsInfo.DeviceStats                                           |             |      |      |
|                                                              |             |      |      |
| FsInfo.IoStats                                               |             |      |      |
|                                                              |             |      |      |
| FsInfo.Path                                                  |             |      |      |
|                                                              |             |      |      |
| FsProbe                                                      |             |      |      |
|                                                              |             |      |      |
| FsService                                                    |             |      |      |





org.elasticsearch.monitor.jvm



| Class                         |      |      |
| ----------------------------- | ---- | ---- |
| Description                   |      |      |
| DeadlockAnalyzer              |      |      |
|                               |      |      |
| DeadlockAnalyzer.Deadlock     |      |      |
|                               |      |      |
| GcNames                       |      |      |
|                               |      |      |
| HotThreads                    |      |      |
|                               |      |      |
| HotThreads.ReportType         |      |      |
|                               |      |      |
| HotThreads.SleepFunction<T,R> |      |      |
|                               |      |      |
| HotThreads.SortOrder          |      |      |
|                               |      |      |
| JvmGcMonitorService           |      |      |
|                               |      |      |
| JvmInfo                       |      |      |
|                               |      |      |
| JvmInfo.Mem                   |      |      |
|                               |      |      |
| JvmService                    |      |      |
|                               |      |      |
| JvmStats                      |      |      |
|                               |      |      |
| JvmStats.BufferPool           |      |      |
|                               |      |      |
| JvmStats.Classes              |      |      |
|                               |      |      |
| JvmStats.GarbageCollector     |      |      |
|                               |      |      |
| JvmStats.GarbageCollectors    |      |      |
|                               |      |      |
| JvmStats.Mem                  |      |      |
|                               |      |      |
| JvmStats.MemoryPool           |      |      |
|                               |      |      |
| JvmStats.Threads              |      |      |
|                               |      |      |
| SunThreadInfo                 |      |      |





org.elasticsearch.monitor.os

| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| OsInfo                                                       |      |      |
|                                                              |      |      |
| OsProbe                                                      |      |      |
| The OsProbe class retrieves information about the physical and swap size of the machine memory, as well as the system load average and cpu load. |      |      |
| OsService                                                    |      |      |
|                                                              |      |      |
| OsStats                                                      |      |      |
|                                                              |      |      |
| OsStats.Cgroup                                               |      |      |
| Encapsulates basic cgroup statistics.                        |      |      |
| OsStats.Cgroup.CpuStat                                       |      |      |
| Encapsulates CPU time statistics.                            |      |      |
| OsStats.Cpu                                                  |      |      |
|                                                              |      |      |
| OsStats.Mem                                                  |      |      |
|                                                              |      |      |
| OsStats.Swap                                                 |      |      |
|                                                              |      |      |





org.elasticsearch.monitor.process



| Class            | Description |      |
| ---------------- | ----------- | ---- |
|                  |             |      |
| ProcessInfo      |             |      |
|                  |             |      |
| ProcessProbe     |             |      |
|                  |             |      |
| ProcessService   |             |      |
|                  |             |      |
| ProcessStats     |             |      |
|                  |             |      |
| ProcessStats.Cpu |             |      |
|                  |             |      |
| ProcessStats.Mem |             |      |





org.elasticsearch.node



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AdaptiveSelectionStats                                       |      |      |      |
| Class representing statistics about adaptive replica selection. |      |      |      |
| InternalSettingsPreparer                                     |      |      |      |
|                                                              |      |      |      |
| Node                                                         |      |      |      |
| A node represent a node within a cluster (cluster.name).     |      |      |      |
| NodeClosedException                                          |      |      |      |
| An exception indicating that node is closed.                 |      |      |      |
| NodeRoleSettings                                             |      |      |      |
|                                                              |      |      |      |
| NodeService                                                  |      |      |      |
|                                                              |      |      |      |
| NodeValidationException                                      |      |      |      |
| An exception thrown during node validation.                  |      |      |      |
| ReportingService<I extends ReportingService.Info>            |      |      |      |
|                                                              |      |      |      |
| ReportingService.Info                                        |      |      |      |
|                                                              |      |      |      |
| ResponseCollectorService                                     |      |      |      |
| Collects statistics about queue size, response time, and service time of tasks executed on each node, making the EWMA of the values available to the coordinating node. |      |      |      |
| ResponseCollectorService.ComputedNodeStats                   |      |      |      |
| Struct-like class encapsulating a point-in-time snapshot of a particular node's statistics. |      |      |      |







org.elasticsearch.persistent



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AllocatedPersistentTask                                      |      |      |      |
| Represents a executor node operation that corresponds to a persistent task |      |      |      |
| AllocatedPersistentTask.State                                |      |      |      |
|                                                              |      |      |      |
| CompletionPersistentTaskAction                               |      |      |      |
| ActionType that is used by executor node to indicate that the persistent action finished or failed on the node and needs to be removed from the cluster state in case of successful completion or restarted on some other node in case of failure. |      |      |      |
| CompletionPersistentTaskAction.Request                       |      |      |      |
|                                                              |      |      |      |
| CompletionPersistentTaskAction.RequestBuilder                |      |      |      |
|                                                              |      |      |      |
| CompletionPersistentTaskAction.TransportAction               |      |      |      |
|                                                              |      |      |      |
| NodePersistentTasksExecutor                                  |      |      |      |
| This component is responsible for execution of persistent tasks. |      |      |      |
| PersistentTaskParams                                         |      |      |      |
| Parameters used to start persistent task                     |      |      |      |
| PersistentTaskResponse                                       |      |      |      |
| Response upon a successful start or an persistent task       |      |      |      |
| PersistentTasksClusterService                                |      |      |      |
| Component that runs only on the master node and is responsible for assigning running tasks to nodes |      |      |      |
| PersistentTasksCustomMetadata                                |      |      |      |
| A cluster state record that contains a list of all running persistent tasks |      |      |      |
| PersistentTasksCustomMetadata.Assignment                     |      |      |      |
|                                                              |      |      |      |
| PersistentTasksCustomMetadata.Builder                        |      |      |      |
|                                                              |      |      |      |
| PersistentTasksCustomMetadata.PersistentTask<P extends PersistentTaskParams> |      |      |      |
| A record that represents a single running persistent task    |      |      |      |
| PersistentTasksExecutor<Params extends PersistentTaskParams> |      |      |      |
| An executor of tasks that can survive restart of requesting or executing node. |      |      |      |
| PersistentTasksExecutorRegistry                              |      |      |      |
| Components that registers all persistent task executors      |      |      |      |
| PersistentTasksNodeService                                   |      |      |      |
| This component is responsible for coordination of execution of persistent tasks on individual nodes. |      |      |      |
| PersistentTasksNodeService.Status                            |      |      |      |
|                                                              |      |      |      |
| PersistentTasksService                                       |      |      |      |
| This service is used by persistent tasks and allocated persistent tasks to communicate changes to the master node so that the master can update the cluster state and can track of the states of the persistent tasks. |      |      |      |
| PersistentTasksService.WaitForPersistentTaskListener<P extends PersistentTaskParams> |      |      |      |
|                                                              |      |      |      |
| PersistentTaskState                                          |      |      |      |
| PersistentTaskState represents the state of the persistent tasks, as it is persisted in the cluster state. |      |      |      |
| RemovePersistentTaskAction                                   |      |      |      |
|                                                              |      |      |      |
| RemovePersistentTaskAction.Request                           |      |      |      |
|                                                              |      |      |      |
| RemovePersistentTaskAction.RequestBuilder                    |      |      |      |
|                                                              |      |      |      |
| RemovePersistentTaskAction.TransportAction                   |      |      |      |
|                                                              |      |      |      |
| StartPersistentTaskAction                                    |      |      |      |
| This action can be used to add the record for the persistent action to the cluster state. |      |      |      |
| StartPersistentTaskAction.Request                            |      |      |      |
|                                                              |      |      |      |
| StartPersistentTaskAction.RequestBuilder                     |      |      |      |
|                                                              |      |      |      |
| StartPersistentTaskAction.TransportAction                    |      |      |      |
|                                                              |      |      |      |
| UpdatePersistentTaskStatusAction                             |      |      |      |
|                                                              |      |      |      |
| UpdatePersistentTaskStatusAction.Request                     |      |      |      |
|                                                              |      |      |      |
| UpdatePersistentTaskStatusAction.RequestBuilder              |      |      |      |
|                                                              |      |      |      |
| UpdatePersistentTaskStatusAction.TransportAction             |      |      |      |





org.elasticsearch.persistent.decider



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| AssignmentDecision                                           |             |      |      |
| AssignmentDecision represents the decision made during the process of assigning a persistent task to a node of the cluster. |             |      |      |
| AssignmentDecision.Type                                      |             |      |      |
|                                                              |             |      |      |
| EnableAssignmentDecider                                      |             |      |      |
| EnableAssignmentDecider is used to allow/disallow the persistent tasks to be assigned to cluster nodes. |             |      |      |
| EnableAssignmentDecider.Allocation                           |             |      |      |
| Allocation values or rather their string representation to be used used with EnableAssignmentDecider.CLUSTER_TASKS_ALLOCATION_ENABLE_SETTING via cluster settings. |             |      |      |





org.elasticsearch.plugins



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ActionPlugin                                                 |      |      |      |
| An additional extension point for Plugins that extends Elasticsearch's scripting functionality. |      |      |      |
| ActionPlugin.ActionHandler<Request extends ActionRequest,Response extends ActionResponse> |      |      |      |
|                                                              |      |      |      |
| AnalysisPlugin                                               |      |      |      |
| An additional extension point for Plugins that extends Elasticsearch's analysis functionality. |      |      |      |
| CircuitBreakerPlugin                                         |      |      |      |
| An extension point for Plugin implementations to add custom circuit breakers |      |      |      |
| ClusterPlugin                                                |      |      |      |
| An extension point for Plugin implementations to customer behavior of cluster management. |      |      |      |
| DiscoveryPlugin                                              |      |      |      |
| An additional extension point for Plugins that extends Elasticsearch's discovery functionality. |      |      |      |
| EnginePlugin                                                 |      |      |      |
| A plugin that provides alternative engine implementations.   |      |      |      |
| ExtensiblePlugin                                             |      |      |      |
| An extension point for Plugin implementations to be themselves extensible. |      |      |      |
| ExtensiblePlugin.ExtensionLoader                             |      |      |      |
|                                                              |      |      |      |
| IndexStorePlugin                                             |      |      |      |
| A plugin that provides alternative directory implementations. |      |      |      |
| IndexStorePlugin.DirectoryFactory                            |      |      |      |
| An interface that describes how to create a new directory instance per shard. |      |      |      |
| IndexStorePlugin.IndexFoldersDeletionListener                |      |      |      |
| IndexStorePlugin.IndexFoldersDeletionListener are invoked before the folders of a shard or an index are deleted from disk. |      |      |      |
| IndexStorePlugin.RecoveryStateFactory                        |      |      |      |
| An interface that allows to create a new RecoveryState per shard. |      |      |      |
| IndexStorePlugin.SnapshotCommitSupplier                      |      |      |      |
| An interface that allows plugins to override the IndexCommit of which a snapshot is taken. |      |      |      |
| IngestPlugin                                                 |      |      |      |
| An extension point for Plugin implementations to add custom ingest processors |      |      |      |
| MapperPlugin                                                 |      |      |      |
| An extension point for Plugin implementations to add custom mappers |      |      |      |
| MetadataUpgrader                                             |      |      |      |
| Upgrades Metadata on startup on behalf of installed Plugins  |      |      |      |
| NetworkPlugin                                                |      |      |      |
| Plugin for extending network and transport related classes   |      |      |      |
| PersistentTaskPlugin                                         |      |      |      |
| Plugin for registering persistent tasks executors.           |      |      |      |
| Platforms                                                    |      |      |      |
| Encapsulates platform-dependent methods for handling native components of plugins. |      |      |      |
| Plugin                                                       |      |      |      |
| An extension point allowing to plug in custom functionality. |      |      |      |
| PluginDescriptor                                             |      |      |      |
| An in-memory representation of the plugin descriptor.        |      |      |      |
| PluginsService                                               |      |      |      |
|                                                              |      |      |      |
| PluginsService.Bundle                                        |      |      |      |
|                                                              |      |      |      |
| PluginsSynchronizer                                          |      |      |      |
| This is a marker interface for classes that are capable of synchronizing the currently-installed ES plugins with those that ought to be installed according to a configuration file. |      |      |      |
| PluginType                                                   |      |      |      |
| Indicates the type of an Elasticsearch plugin.               |      |      |      |
| ReloadablePlugin                                             |      |      |      |
| An extension point for Plugins that can be reloaded.         |      |      |      |
| RepositoryPlugin                                             |      |      |      |
| An extension point for Plugin implementations to add custom snapshot repositories. |      |      |      |
| ScriptPlugin                                                 |      |      |      |
| An additional extension point for Plugins that extends Elasticsearch's scripting functionality. |      |      |      |
| SearchPlugin                                                 |      |      |      |
| Plugin for extending search time behavior.                   |      |      |      |
| SearchPlugin.AggregationSpec                                 |      |      |      |
| Specification for an Aggregation.                            |      |      |      |
| SearchPlugin.FetchPhaseConstructionContext                   |      |      |      |
| Context available during fetch phase construction.           |      |      |      |
| SearchPlugin.PipelineAggregationSpec                         |      |      |      |
| Specification for a PipelineAggregator.                      |      |      |      |
| SearchPlugin.QuerySpec<T extends QueryBuilder>               |      |      |      |
| Specification of custom Query.                               |      |      |      |
| SearchPlugin.RescorerSpec<T extends RescorerBuilder<T>>      |      |      |      |
|                                                              |      |      |      |
| SearchPlugin.ScoreFunctionSpec<T extends ScoreFunctionBuilder<T>> |      |      |      |
| Specification of custom ScoreFunction.                       |      |      |      |
| SearchPlugin.SearchExtensionSpec<W extends NamedWriteable,P> |      |      |      |
| Specification of search time behavior extension like a custom MovAvgModel or ScoreFunction. |      |      |      |
| SearchPlugin.SearchExtSpec<T extends SearchExtBuilder>       |      |      |      |
| Specification for a SearchExtBuilder which represents an additional section that can be parsed in a search request (within the ext element). |      |      |      |
| SearchPlugin.SignificanceHeuristicSpec<T extends SignificanceHeuristic> |      |      |      |
| Specification of custom SignificanceHeuristic.               |      |      |      |
| SearchPlugin.SuggesterSpec<T extends SuggestionBuilder<T>>   |      |      |      |
| Specification for a Suggester.                               |      |      |      |
| ShutdownAwarePlugin                                          |      |      |      |
| A ShutdownAwarePlugin is a plugin that can be made aware of a shutdown. |      |      |      |
| SystemIndexPlugin                                            |      |      |      |
| Plugin for defining system indices.                          |      |      |      |





org.elasticsearch.plugins.spi



| Class                            | Description |      |
| -------------------------------- | ----------- | ---- |
|                                  |             |      |
| NamedXContentProvider            |             |      |
| Provides named XContent parsers. |             |      |





org.elasticsearch.repositories



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| FilterRepository                                             |      |      |      |
|                                                              |      |      |      |
| FinalizeSnapshotContext                                      |      |      |      |
| Context for finalizing a snapshot.                           |      |      |      |
| GetSnapshotInfoContext                                       |      |      |      |
| Describes the context of fetching one or more SnapshotInfo via Repository.getSnapshotInfo(GetSnapshotInfoContext). |      |      |      |
| IndexId                                                      |      |      |      |
| Represents a single snapshotted index in the repository.     |      |      |      |
| IndexMetaDataGenerations                                     |      |      |      |
| Tracks the blob uuids of blobs containing IndexMetadata for snapshots as well an identifier for each of these blobs. |      |      |      |
| IndexSnapshotsService                                        |      |      |      |
|                                                              |      |      |      |
| RepositoriesModule                                           |      |      |      |
| Sets up classes for Snapshot/Restore.                        |      |      |      |
| RepositoriesService                                          |      |      |      |
| Service responsible for maintaining and providing access to snapshot repositories on nodes. |      |      |      |
| RepositoriesStatsArchive                                     |      |      |      |
|                                                              |      |      |      |
| Repository                                                   |      |      |      |
| An interface for interacting with a repository in snapshot and restore. |      |      |      |
| Repository.Factory                                           |      |      |      |
| An factory interface for constructing repositories.          |      |      |      |
| RepositoryCleanupResult                                      |      |      |      |
|                                                              |      |      |      |
| RepositoryData                                               |      |      |      |
| A class that represents the data in a repository, as captured in the repository's index blob. |      |      |      |
| RepositoryData.SnapshotDetails                               |      |      |      |
| A few details of an individual snapshot stored in the top-level index blob, so they are readily accessible without having to load the corresponding SnapshotInfo blob for each snapshot. |      |      |      |
| RepositoryException                                          |      |      |      |
| Generic repository exception                                 |      |      |      |
| RepositoryInfo                                               |      |      |      |
|                                                              |      |      |      |
| RepositoryMissingException                                   |      |      |      |
| Repository missing exception                                 |      |      |      |
| RepositoryOperation                                          |      |      |      |
| Coordinates of an operation that modifies a repository, assuming that repository at a specific generation. |      |      |      |
| RepositoryShardId                                            |      |      |      |
| Represents a shard snapshot in a repository.                 |      |      |      |
| RepositoryStats                                              |      |      |      |
|                                                              |      |      |      |
| RepositoryStatsSnapshot                                      |      |      |      |
|                                                              |      |      |      |
| RepositoryVerificationException                              |      |      |      |
| Repository verification exception                            |      |      |      |
| ShardGeneration                                              |      |      |      |
| The generation ID of a shard, used to name the shard-level index-$SHARD_GEN file that represents a BlobStoreIndexShardSnapshots instance. |      |      |      |
| ShardGenerations                                             |      |      |      |
| Represents the current ShardGeneration for each shard in a repository. |      |      |      |
| ShardGenerations.Builder                                     |      |      |      |
|                                                              |      |      |      |
| ShardSnapshotInfo                                            |      |      |      |
|                                                              |      |      |      |
| ShardSnapshotResult                                          |      |      |      |
| The details of a successful shard-level snapshot that are used to build the overall snapshot during finalization. |      |      |      |
| SnapshotShardContext                                         |      |      |      |
| Context holding the state for creating a shard snapshot via Repository.snapshotShard(SnapshotShardContext). |      |      |      |
| VerificationFailure                                          |      |      |      |
|                                                              |      |      |      |
| VerifyNodeRepositoryAction                                   |      |      |      |
|                                                              |      |      |      |
| VerifyNodeRepositoryAction.VerifyNodeRepositoryRequest       |      |      |      |





org.elasticsearch.repositories.blobstore



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| BlobContainer                                                |      |      |      |
| An interface for managing a repository of blob entries, where each blob entry is just a named group of bytes. |      |      |      |
| BlobMetadata                                                 |      |      |      |
| An interface for providing basic metadata about a blob.      |      |      |      |
| BlobPath                                                     |      |      |      |
| The list of paths where a blob can reside.                   |      |      |      |
| BlobStore                                                    |      |      |      |
| An interface for storing blobs.                              |      |      |      |
| BlobStoreException                                           |      |      |      |
|                                                              |      |      |      |
| DeleteResult                                                 |      |      |      |
| The result of deleting multiple blobs from a BlobStore.      |      |      |      |





org.elasticsearch.repositories.fs



| Class                                                |      |      |
| ---------------------------------------------------- | ---- | ---- |
| Description                                          |      |      |
| FsBlobContainer                                      |      |      |
| A file system based implementation of BlobContainer. |      |      |
| FsBlobStore                                          |      |      |

org.elasticsearch.rest



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AbstractRestChannel                                          |      |      |
|                                                              |      |      |
| BaseRestHandler                                              |      |      |
| Base handler for REST requests.                              |      |      |
| BaseRestHandler.RestChannelConsumer                          |      |      |
| REST requests are handled by preparing a channel consumer that represents the execution of the request against a channel. |      |      |
| BaseRestHandler.Wrapper                                      |      |      |
|                                                              |      |      |
| BytesRestResponse                                            |      |      |
|                                                              |      |      |
| DeprecationRestHandler                                       |      |      |
| DeprecationRestHandler provides a proxy for any existing RestHandler so that usage of the handler can be logged using the DeprecationLogger. |      |      |
| FilterRestHandler                                            |      |      |
|                                                              |      |      |
| RestChannel                                                  |      |      |
| A channel used to construct bytes / builder based outputs, and send responses. |      |      |
| RestController                                               |      |      |
|                                                              |      |      |
| RestHandler                                                  |      |      |
| Handler for REST requests                                    |      |      |
| RestHandler.Route                                            |      |      |
|                                                              |      |      |
| RestHandler.Route.RouteBuilder                               |      |      |
|                                                              |      |      |
| RestHeaderDefinition                                         |      |      |
| A definition for an http header that should be copied to the ThreadContext when reading the request on the rest layer. |      |      |
| RestRequest                                                  |      |      |
|                                                              |      |      |
| RestRequest.BadParameterException                            |      |      |
|                                                              |      |      |
| RestRequest.ContentTypeHeaderException                       |      |      |
|                                                              |      |      |
| RestRequest.Method                                           |      |      |
|                                                              |      |      |
| RestRequestFilter                                            |      |      |
| Identifies an object that supplies a filter for the content of a RestRequest. |      |      |
| RestResponse                                                 |      |      |
|                                                              |      |      |
| RestStatus                                                   |      |      |
|                                                              |      |      |
| RestUtils                                                    |      |      |



org.elasticsearch.rest.action



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| DispatchingRestToXContentListener<Response extends StatusToXContentObject> |      |      |      |
| Response listener for REST requests which dispatches the serialization of the response off of the thread on which the response was received, since that thread is often a transport thread and XContent serialization might be expensive. |      |      |      |
| RestActionListener<Response>                                 |      |      |      |
| An action listener that requires RestActionListener.processResponse(Object) to be implemented and will automatically handle failures. |      |      |      |
| RestActions                                                  |      |      |      |
|                                                              |      |      |      |
| RestActions.NodesResponseRestListener<NodesResponse extends BaseNodesResponse<?> & ToXContent> |      |      |      |
| NodesResponseRestBuilderListener automatically translates any BaseNodesResponse (multi-node) response that is ToXContent-compatible into a RestResponse with the necessary header info (e.g., "cluster_name"). |      |      |      |
| RestBuilderListener<Response>                                |      |      |      |
| A REST action listener that builds an XContentBuilder based response. |      |      |      |
| RestCancellableNodeClient                                    |      |      |      |
| A Client that cancels tasks executed locally when the provided HttpChannel is closed before completion. |      |      |      |
| RestFieldCapabilitiesAction                                  |      |      |      |
|                                                              |      |      |      |
| RestMainAction                                               |      |      |      |
|                                                              |      |      |      |
| RestResponseListener<Response>                               |      |      |      |
| A REST enabled action listener that has a basic onFailure implementation, and requires sub classes to only implement RestResponseListener.buildResponse(Object). |      |      |      |
| RestStatusToXContentListener<Response extends StatusToXContentObject> |      |      |      |
| Content listener that extracts that RestStatus from the response. |      |      |      |
| RestToXContentListener<Response extends ToXContentObject>    |      |      |      |
| A REST based action listener that requires the response to implement ToXContentObject and automatically builds an XContent based response. |      |      |      |





org.elasticsearch.rest.action.admin.cluster





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| RestAddVotingConfigExclusionAction                           |      |      |      |
|                                                              |      |      |      |
| RestCancelTasksAction                                        |      |      |      |
|                                                              |      |      |      |
| RestCleanupRepositoryAction                                  |      |      |      |
| Cleans up a repository                                       |      |      |      |
| RestClearVotingConfigExclusionsAction                        |      |      |      |
|                                                              |      |      |      |
| RestCloneSnapshotAction                                      |      |      |      |
| Clones indices from one snapshot into another snapshot in the same repository |      |      |      |
| RestClusterAllocationExplainAction                           |      |      |      |
| Class handling cluster allocation explanation at the REST level |      |      |      |
| RestClusterGetSettingsAction                                 |      |      |      |
|                                                              |      |      |      |
| RestClusterHealthAction                                      |      |      |      |
|                                                              |      |      |      |
| RestClusterRerouteAction                                     |      |      |      |
|                                                              |      |      |      |
| RestClusterSearchShardsAction                                |      |      |      |
|                                                              |      |      |      |
| RestClusterStateAction                                       |      |      |      |
|                                                              |      |      |      |
| RestClusterStatsAction                                       |      |      |      |
|                                                              |      |      |      |
| RestClusterUpdateSettingsAction                              |      |      |      |
|                                                              |      |      |      |
| RestCreateSnapshotAction                                     |      |      |      |
| Creates a new snapshot                                       |      |      |      |
| RestDeleteRepositoryAction                                   |      |      |      |
| Unregisters a repository                                     |      |      |      |
| RestDeleteSnapshotAction                                     |      |      |      |
| Deletes a snapshot                                           |      |      |      |
| RestDeleteStoredScriptAction                                 |      |      |      |
|                                                              |      |      |      |
| RestGetFeatureUpgradeStatusAction                            |      |      |      |
| Endpoint for getting the system feature upgrade status       |      |      |      |
| RestGetRepositoriesAction                                    |      |      |      |
| Returns repository information                               |      |      |      |
| RestGetScriptContextAction                                   |      |      |      |
|                                                              |      |      |      |
| RestGetScriptLanguageAction                                  |      |      |      |
|                                                              |      |      |      |
| RestGetSnapshotsAction                                       |      |      |      |
| Returns information about snapshot                           |      |      |      |
| RestGetStoredScriptAction                                    |      |      |      |
|                                                              |      |      |      |
| RestGetTaskAction                                            |      |      |      |
|                                                              |      |      |      |
| RestListTasksAction                                          |      |      |      |
|                                                              |      |      |      |
| RestNodesHotThreadsAction                                    |      |      |      |
|                                                              |      |      |      |
| RestNodesInfoAction                                          |      |      |      |
|                                                              |      |      |      |
| RestNodesStatsAction                                         |      |      |      |
|                                                              |      |      |      |
| RestNodesUsageAction                                         |      |      |      |
|                                                              |      |      |      |
| RestPendingClusterTasksAction                                |      |      |      |
|                                                              |      |      |      |
| RestPostFeatureUpgradeAction                                 |      |      |      |
| Endpoint for triggering a system feature upgrade             |      |      |      |
| RestPutRepositoryAction                                      |      |      |      |
| Registers repositories                                       |      |      |      |
| RestPutStoredScriptAction                                    |      |      |      |
|                                                              |      |      |      |
| RestReloadSecureSettingsAction                               |      |      |      |
|                                                              |      |      |      |
| RestRemoteClusterInfoAction                                  |      |      |      |
|                                                              |      |      |      |
| RestResetFeatureStateAction                                  |      |      |      |
| Rest handler for feature state reset requests                |      |      |      |
| RestRestoreSnapshotAction                                    |      |      |      |
| Restores a snapshot                                          |      |      |      |
| RestSnapshotsStatusAction                                    |      |      |      |
| Returns status of currently running snapshot                 |      |      |      |
| RestSnapshottableFeaturesAction                              |      |      |      |
|                                                              |      |      |      |
| RestVerifyRepositoryAction                                   |      |      |      |





org.elasticsearch.rest.action.admin.cluster.dangling



| Class                         |      | Description |
| ----------------------------- | ---- | ----------- |
|                               |      |             |
| RestDeleteDanglingIndexAction |      |             |
|                               |      |             |
| RestImportDanglingIndexAction |      |             |
|                               |      |             |
| RestListDanglingIndicesAction |      |             |





org.elasticsearch.rest.action.admin.indices



| Class                                                     |      |      |      |
| --------------------------------------------------------- | ---- | ---- | ---- |
| Description                                               |      |      |      |
| AliasesNotFoundException                                  |      |      |      |
|                                                           |      |      |      |
| RestAddIndexBlockAction                                   |      |      |      |
|                                                           |      |      |      |
| RestAnalyzeAction                                         |      |      |      |
|                                                           |      |      |      |
| RestAnalyzeIndexDiskUsageAction                           |      |      |      |
|                                                           |      |      |      |
| RestClearIndicesCacheAction                               |      |      |      |
|                                                           |      |      |      |
| RestCloseIndexAction                                      |      |      |      |
|                                                           |      |      |      |
| RestCreateIndexAction                                     |      |      |      |
|                                                           |      |      |      |
| RestDeleteComponentTemplateAction                         |      |      |      |
|                                                           |      |      |      |
| RestDeleteComposableIndexTemplateAction                   |      |      |      |
|                                                           |      |      |      |
| RestDeleteIndexAction                                     |      |      |      |
|                                                           |      |      |      |
| RestDeleteIndexTemplateAction                             |      |      |      |
|                                                           |      |      |      |
| RestFieldUsageStatsAction                                 |      |      |      |
|                                                           |      |      |      |
| RestFlushAction                                           |      |      |      |
|                                                           |      |      |      |
| RestForceMergeAction                                      |      |      |      |
|                                                           |      |      |      |
| RestGetAliasesAction                                      |      |      |      |
| The REST handler for get alias and head alias APIs.       |      |      |      |
| RestGetComponentTemplateAction                            |      |      |      |
|                                                           |      |      |      |
| RestGetComposableIndexTemplateAction                      |      |      |      |
|                                                           |      |      |      |
| RestGetFieldMappingAction                                 |      |      |      |
|                                                           |      |      |      |
| RestGetIndexTemplateAction                                |      |      |      |
| The REST handler for get template and head template APIs. |      |      |      |
| RestGetIndicesAction                                      |      |      |      |
| The REST handler for get index and head index APIs.       |      |      |      |
| RestGetMappingAction                                      |      |      |      |
|                                                           |      |      |      |
| RestGetSettingsAction                                     |      |      |      |
|                                                           |      |      |      |
| RestIndexDeleteAliasesAction                              |      |      |      |
|                                                           |      |      |      |
| RestIndexPutAliasAction                                   |      |      |      |
|                                                           |      |      |      |
| RestIndicesAliasesAction                                  |      |      |      |
|                                                           |      |      |      |
| RestIndicesSegmentsAction                                 |      |      |      |
|                                                           |      |      |      |
| RestIndicesShardStoresAction                              |      |      |      |
| Rest action for IndicesShardStoresAction                  |      |      |      |
| RestIndicesStatsAction                                    |      |      |      |
|                                                           |      |      |      |
| RestOpenIndexAction                                       |      |      |      |
|                                                           |      |      |      |
| RestPutComponentTemplateAction                            |      |      |      |
|                                                           |      |      |      |
| RestPutComposableIndexTemplateAction                      |      |      |      |
|                                                           |      |      |      |
| RestPutIndexTemplateAction                                |      |      |      |
|                                                           |      |      |      |
| RestPutMappingAction                                      |      |      |      |
|                                                           |      |      |      |
| RestRecoveryAction                                        |      |      |      |
| REST handler to report on index recoveries.               |      |      |      |
| RestRefreshAction                                         |      |      |      |
|                                                           |      |      |      |
| RestResizeHandler                                         |      |      |      |
|                                                           |      |      |      |
| RestResizeHandler.RestCloneIndexAction                    |      |      |      |
|                                                           |      |      |      |
| RestResizeHandler.RestShrinkIndexAction                   |      |      |      |
|                                                           |      |      |      |
| RestResizeHandler.RestSplitIndexAction                    |      |      |      |
|                                                           |      |      |      |
| RestResolveIndexAction                                    |      |      |      |
|                                                           |      |      |      |
| RestRolloverIndexAction                                   |      |      |      |
|                                                           |      |      |      |
| RestSimulateIndexTemplateAction                           |      |      |      |
|                                                           |      |      |      |
| RestSimulateTemplateAction                                |      |      |      |
|                                                           |      |      |      |
| RestSyncedFlushAction                                     |      |      |      |
|                                                           |      |      |      |
| RestUpdateSettingsAction                                  |      |      |      |
|                                                           |      |      |      |
| RestUpgradeActionDeprecated                               |      |      |      |
|                                                           |      |      |      |
| RestUpgradeStatusActionDeprecated                         |      |      |      |
|                                                           |      |      |      |
| RestValidateQueryAction                                   |      |      |      |





org.elasticsearch.rest.action.cat



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AbstractCatAction                                            |      |      |
|                                                              |      |      |
| RestAliasAction                                              |      |      |
|                                                              |      |      |
| RestAllocationAction                                         |      |      |
|                                                              |      |      |
| RestCatAction                                                |      |      |
|                                                              |      |      |
| RestCatRecoveryAction                                        |      |      |
| RestRecoveryAction provides information about the status of replica recovery in a string format, designed to be used at the command line. |      |      |
| RestCountAction                                              |      |      |
|                                                              |      |      |
| RestFielddataAction                                          |      |      |
| Cat API class to display information about the size of fielddata fields per node |      |      |
| RestHealthAction                                             |      |      |
|                                                              |      |      |
| RestIndicesAction                                            |      |      |
|                                                              |      |      |
| RestMasterAction                                             |      |      |
|                                                              |      |      |
| RestNodeAttrsAction                                          |      |      |
|                                                              |      |      |
| RestNodesAction                                              |      |      |
|                                                              |      |      |
| RestPendingClusterTasksAction                                |      |      |
|                                                              |      |      |
| RestPluginsAction                                            |      |      |
|                                                              |      |      |
| RestRepositoriesAction                                       |      |      |
| Cat API class to display information about snapshot repositories |      |      |
| RestSegmentsAction                                           |      |      |
|                                                              |      |      |
| RestShardsAction                                             |      |      |
|                                                              |      |      |
| RestSnapshotAction                                           |      |      |
| Cat API class to display information about snapshots         |      |      |
| RestTable                                                    |      |      |
|                                                              |      |      |
| RestTasksAction                                              |      |      |
|                                                              |      |      |
| RestTemplatesAction                                          |      |      |
|                                                              |      |      |
| RestThreadPoolAction                                         |      |      |





org.elasticsearch.rest.action.datastreams

| Class                       |      |      |      |
| --------------------------- | ---- | ---- | ---- |
| Description                 |      |      |      |
| RestModifyDataStreamsAction |      |      |      |



org.elasticsearch.rest.action.document



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| RestBulkAction                                               |      |      |      |
| { "index" : { "_index" : "test", "_type" : "type1", "_id" : "1" } { "type1" : { "field1" : "value1" } } { "delete" : { "_index" : "test", "_type" : "type1", "_id" : "2" } } { "create" : { "_index" : "test", "_type" : "type1", "_id" : "1" } { "type1" : { "field1" : "value1" } } |      |      |      |
| RestDeleteAction                                             |      |      |      |
|                                                              |      |      |      |
| RestGetAction                                                |      |      |      |
|                                                              |      |      |      |
| RestGetSourceAction                                          |      |      |      |
| The REST handler for get source and head source APIs.        |      |      |      |
| RestIndexAction                                              |      |      |      |
|                                                              |      |      |      |
| RestIndexAction.AutoIdHandler                                |      |      |      |
|                                                              |      |      |      |
| RestIndexAction.CreateHandler                                |      |      |      |
|                                                              |      |      |      |
| RestMultiGetAction                                           |      |      |      |
|                                                              |      |      |      |
| RestMultiTermVectorsAction                                   |      |      |      |
|                                                              |      |      |      |
| RestTermVectorsAction                                        |      |      |      |
| This class parses the json request and translates it into a TermVectorsRequest. |      |      |      |
| RestUpdateAction                                             |      |      |      |





org.elasticsearch.rest.action.ingest





| Class                      |      |      |      |
| -------------------------- | ---- | ---- | ---- |
| Description                |      |      |      |
| RestDeletePipelineAction   |      |      |      |
|                            |      |      |      |
| RestGetPipelineAction      |      |      |      |
|                            |      |      |      |
| RestPutPipelineAction      |      |      |      |
|                            |      |      |      |
| RestSimulatePipelineAction |      |      |      |





org.elasticsearch.rest.action.search

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| RestClearScrollAction                                        |      |      |      |
|                                                              |      |      |      |
| RestCountAction                                              |      |      |      |
|                                                              |      |      |      |
| RestExplainAction                                            |      |      |      |
| Rest action for computing a score explanation for specific documents. |      |      |      |
| RestMultiSearchAction                                        |      |      |      |
|                                                              |      |      |      |
| RestSearchAction                                             |      |      |      |
|                                                              |      |      |      |
| RestSearchScrollAction                                       |      |      |      |

org.elasticsearch.rollup



| Class       |      |      |
| ----------- | ---- | ---- |
| Description |      |      |
| RollupV2    |      |      |



org.elasticsearch.script



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AbstractFieldScript                                          |      |      |      |      |
| Abstract base for scripts to execute to build scripted fields. |      |      |      |      |
| AbstractLongFieldScript                                      |      |      |      |      |
| Common base class for script field scripts that return long values. |      |      |      |      |
| AggregationScript                                            |      |      |      |      |
|                                                              |      |      |      |      |
| AggregationScript.Factory                                    |      |      |      |      |
| A factory to construct stateful AggregationScript factories for a specific index. |      |      |      |      |
| AggregationScript.LeafFactory                                |      |      |      |      |
| A factory to construct AggregationScript instances.          |      |      |      |      |
| BooleanFieldScript                                           |      |      |      |      |
|                                                              |      |      |      |      |
| BooleanFieldScript.Emit                                      |      |      |      |      |
|                                                              |      |      |      |      |
| BooleanFieldScript.Factory                                   |      |      |      |      |
|                                                              |      |      |      |      |
| BooleanFieldScript.LeafFactory                               |      |      |      |      |
|                                                              |      |      |      |      |
| BucketAggregationScript                                      |      |      |      |      |
| A script used in bucket aggregations that returns a double value. |      |      |      |      |
| BucketAggregationScript.Factory                              |      |      |      |      |
|                                                              |      |      |      |      |
| BucketAggregationSelectorScript                              |      |      |      |      |
| A script used in bucket aggregations that returns a boolean value. |      |      |      |      |
| BucketAggregationSelectorScript.Factory                      |      |      |      |      |
|                                                              |      |      |      |      |
| ClassPermission                                              |      |      |      |      |
| Checked by scripting engines to allow loading a java class.  |      |      |      |      |
| CompositeFieldScript                                         |      |      |      |      |
| A script that emits a map of multiple values, that can then be accessed by child runtime fields. |      |      |      |      |
| CompositeFieldScript.EmitField                               |      |      |      |      |
|                                                              |      |      |      |      |
| CompositeFieldScript.EmitMap                                 |      |      |      |      |
|                                                              |      |      |      |      |
| CompositeFieldScript.Factory                                 |      |      |      |      |
|                                                              |      |      |      |      |
| CompositeFieldScript.LeafFactory                             |      |      |      |      |
|                                                              |      |      |      |      |
| DateFieldScript                                              |      |      |      |      |
|                                                              |      |      |      |      |
| DateFieldScript.Emit                                         |      |      |      |      |
|                                                              |      |      |      |      |
| DateFieldScript.Factory                                      |      |      |      |      |
|                                                              |      |      |      |      |
| DateFieldScript.LeafFactory                                  |      |      |      |      |
|                                                              |      |      |      |      |
| DateFieldScript.Parse                                        |      |      |      |      |
| Temporary parse method that takes into account the date format. |      |      |      |      |
| DocBasedScript                                               |      |      |      |      |
|                                                              |      |      |      |      |
| DocReader                                                    |      |      |      |      |
| Access the document in a script, provides both old-style, doc['fieldname'], and new style field('fieldname') access to the fields. |      |      |      |      |
| DocValuesDocReader                                           |      |      |      |      |
| Provide access to DocValues for script field api and doc API. |      |      |      |      |
| DoubleFieldScript                                            |      |      |      |      |
|                                                              |      |      |      |      |
| DoubleFieldScript.Emit                                       |      |      |      |      |
|                                                              |      |      |      |      |
| DoubleFieldScript.Factory                                    |      |      |      |      |
|                                                              |      |      |      |      |
| DoubleFieldScript.LeafFactory                                |      |      |      |      |
|                                                              |      |      |      |      |
| DynamicMap                                                   |      |      |      |      |
| DynamicMap is used to wrap a Map for a script parameter.     |      |      |      |      |
| ExplainableScoreScript                                       |      |      |      |      |
| To be implemented by ScoreScript which can provided an Explanation of the score This is currently not used inside elasticsearch but it is used, see for example here: https://github.com/elastic/elasticsearch/issues/8561 |      |      |      |      |
| FieldScript                                                  |      |      |      |      |
| A script to produce dynamic values for return fields.        |      |      |      |      |
| FieldScript.Factory                                          |      |      |      |      |
|                                                              |      |      |      |      |
| FieldScript.LeafFactory                                      |      |      |      |      |
| A factory to construct FieldScript instances.                |      |      |      |      |
| FilterScript                                                 |      |      |      |      |
| A script implementation of a query filter.                   |      |      |      |      |
| FilterScript.Factory                                         |      |      |      |      |
| A factory to construct stateful FilterScript factories for a specific index. |      |      |      |      |
| FilterScript.LeafFactory                                     |      |      |      |      |
| A factory to construct FilterScript instances.               |      |      |      |      |
| GeneralScriptException                                       |      |      |      |      |
| Deprecated.                                                  |      |      |      |      |
| Use ScriptException for exceptions from the scripting engine, otherwise use a more appropriate exception (e.g. |      |      |      |      |
| GeoPointFieldScript                                          |      |      |      |      |
| Script producing geo points.                                 |      |      |      |      |
| GeoPointFieldScript.Emit                                     |      |      |      |      |
|                                                              |      |      |      |      |
| GeoPointFieldScript.Factory                                  |      |      |      |      |
|                                                              |      |      |      |      |
| GeoPointFieldScript.LeafFactory                              |      |      |      |      |
|                                                              |      |      |      |      |
| IngestConditionalScript                                      |      |      |      |      |
| A script used by ConditionalProcessor.                       |      |      |      |      |
| IngestConditionalScript.Factory                              |      |      |      |      |
|                                                              |      |      |      |      |
| IngestScript                                                 |      |      |      |      |
| A script used by the Ingest Script Processor.                |      |      |      |      |
| IngestScript.Factory                                         |      |      |      |      |
|                                                              |      |      |      |      |
| IpFieldScript                                                |      |      |      |      |
| Script producing IP addresses.                               |      |      |      |      |
| IpFieldScript.Emit                                           |      |      |      |      |
|                                                              |      |      |      |      |
| IpFieldScript.Factory                                        |      |      |      |      |
|                                                              |      |      |      |      |
| IpFieldScript.LeafFactory                                    |      |      |      |      |
|                                                              |      |      |      |      |
| JodaCompatibleZonedDateTime                                  |      |      |      |      |
| A wrapper around ZonedDateTime that exposes joda methods for backcompat. |      |      |      |      |
| LeafReaderContextSupplier                                    |      |      |      |      |
| Provides direct access to a LeafReaderContext                |      |      |      |      |
| LongFieldScript                                              |      |      |      |      |
|                                                              |      |      |      |      |
| LongFieldScript.Emit                                         |      |      |      |      |
|                                                              |      |      |      |      |
| LongFieldScript.Factory                                      |      |      |      |      |
|                                                              |      |      |      |      |
| LongFieldScript.LeafFactory                                  |      |      |      |      |
|                                                              |      |      |      |      |
| NumberSortScript                                             |      |      |      |      |
|                                                              |      |      |      |      |
| NumberSortScript.Factory                                     |      |      |      |      |
| A factory to construct stateful NumberSortScript factories for a specific index. |      |      |      |      |
| NumberSortScript.LeafFactory                                 |      |      |      |      |
| A factory to construct NumberSortScript instances.           |      |      |      |      |
| ScoreScript                                                  |      |      |      |      |
| A script used for adjusting the score on a per document basis. |      |      |      |      |
| ScoreScript.ExplanationHolder                                |      |      |      |      |
| A helper to take in an explanation from a script and turn it into an Explanation |      |      |      |      |
| ScoreScript.Factory                                          |      |      |      |      |
| A factory to construct stateful ScoreScript factories for a specific index. |      |      |      |      |
| ScoreScript.LeafFactory                                      |      |      |      |      |
| A factory to construct ScoreScript instances.                |      |      |      |      |
| ScoreScriptUtils                                             |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayDateExp                                |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayDateGauss                              |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayDateLinear                             |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayGeoExp                                 |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayGeoGauss                               |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayGeoLinear                              |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayNumericExp                             |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayNumericGauss                           |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.DecayNumericLinear                          |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.RandomScoreDoc                              |      |      |      |      |
|                                                              |      |      |      |      |
| ScoreScriptUtils.RandomScoreField                            |      |      |      |      |
|                                                              |      |      |      |      |
| Script                                                       |      |      |      |      |
| Script represents used-defined input that can be used to compile and execute a script from the ScriptService based on the ScriptType. |      |      |      |      |
| ScriptCache                                                  |      |      |      |      |
| Script cache and compilation rate limiter.                   |      |      |      |      |
| ScriptCache.CompilationRate                                  |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptCacheStats                                             |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptCompiler                                               |      |      |      |      |
| Takes a Script definition and returns a compiled script factory |      |      |      |      |
| ScriptContext<FactoryType>                                   |      |      |      |      |
| The information necessary to compile and run a script.       |      |      |      |      |
| ScriptContextInfo                                            |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptContextInfo.ScriptMethodInfo                           |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptContextInfo.ScriptMethodInfo.ParameterInfo             |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptContextStats                                           |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptContextStats.TimeSeries                                |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts                                    |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.CombineScript                      |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.CombineScript.Factory              |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.InitScript                         |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.InitScript.Factory                 |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.MapScript                          |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.MapScript.Factory                  |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.MapScript.LeafFactory              |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.ReduceScript                       |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptedMetricAggContexts.ReduceScript.Factory               |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptEngine                                                 |      |      |      |      |
| A script language implementation.                            |      |      |      |      |
| ScriptException                                              |      |      |      |      |
| Exception from a scripting engine.                           |      |      |      |      |
| ScriptException.Position                                     |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptFactory                                                |      |      |      |      |
| Contains utility methods for compiled scripts without impacting concrete script signatures |      |      |      |      |
| ScriptLanguagesInfo                                          |      |      |      |      |
| The allowable types, languages and their corresponding contexts. |      |      |      |      |
| ScriptMetadata                                               |      |      |      |      |
| ScriptMetadata is used to store user-defined scripts as part of the ClusterState using only an id as the key. |      |      |      |      |
| ScriptMetadata.Builder                                       |      |      |      |      |
| A builder used to modify the currently stored scripts data held within the ClusterState. |      |      |      |      |
| ScriptMetrics                                                |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptModule                                                 |      |      |      |      |
| Manages building ScriptService.                              |      |      |      |      |
| ScriptService                                                |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptService.ContextSettings                                |      |      |      |      |
| Collect settings related to script context and general caches. |      |      |      |      |
| ScriptStats                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| ScriptType                                                   |      |      |      |      |
| ScriptType represents the way a script is stored and retrieved from the ScriptService. |      |      |      |      |
| SignificantTermsHeuristicScoreScript                         |      |      |      |      |
| A script used in significant terms heuristic scoring.        |      |      |      |      |
| SignificantTermsHeuristicScoreScript.Factory                 |      |      |      |      |
|                                                              |      |      |      |      |
| SimilarityScript                                             |      |      |      |      |
| A script that is used to build ScriptedSimilarity instances. |      |      |      |      |
| SimilarityScript.Factory                                     |      |      |      |      |
|                                                              |      |      |      |      |
| SimilarityWeightScript                                       |      |      |      |      |
| A script that is used to compute scoring factors that are the same for all documents. |      |      |      |      |
| SimilarityWeightScript.Factory                               |      |      |      |      |
|                                                              |      |      |      |      |
| StoredScriptSource                                           |      |      |      |      |
| StoredScriptSource represents user-defined parameters for a script saved in the ClusterState. |      |      |      |      |
| StringFieldScript                                            |      |      |      |      |
|                                                              |      |      |      |      |
| StringFieldScript.Emit                                       |      |      |      |      |
|                                                              |      |      |      |      |
| StringFieldScript.Factory                                    |      |      |      |      |
|                                                              |      |      |      |      |
| StringFieldScript.LeafFactory                                |      |      |      |      |
|                                                              |      |      |      |      |
| StringSortScript                                             |      |      |      |      |
|                                                              |      |      |      |      |
| StringSortScript.Factory                                     |      |      |      |      |
| A factory to construct stateful StringSortScript factories for a specific index. |      |      |      |      |
| StringSortScript.LeafFactory                                 |      |      |      |      |
| A factory to construct StringSortScript instances.           |      |      |      |      |
| TemplateScript                                               |      |      |      |      |
| A string template rendered as a script.                      |      |      |      |      |
| TemplateScript.Factory                                       |      |      |      |      |
|                                                              |      |      |      |      |
| TermsSetQueryScript                                          |      |      |      |      |
|                                                              |      |      |      |      |
| TermsSetQueryScript.Factory                                  |      |      |      |      |
| A factory to construct stateful TermsSetQueryScript factories for a specific index. |      |      |      |      |
| TermsSetQueryScript.LeafFactory                              |      |      |      |      |
| A factory to construct TermsSetQueryScript instances.        |      |      |      |      |
| UpdateScript                                                 |      |      |      |      |
| An update script.                                            |      |      |      |      |
| UpdateScript.Factory                                         |      |      |      |      |





org.elasticsearch.script.field



| Class                                                      |      |      |      |
| ---------------------------------------------------------- | ---- | ---- | ---- |
| Description                                                |      |      |      |
| DocValuesField                                             |      |      |      |
|                                                            |      |      |      |
| EmptyField                                                 |      |      |      |
| Script field with no mapping, always returns defaultValue. |      |      |      |
| Field                                                      |      |      |      |
| A field in a document accessible via scripting.            |      |      |      |





org.elasticsearch.search



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| CanMatchShardResponse                                        |      |      |      |      |
| Shard-level response for can-match requests                  |      |      |      |      |
| DocValueFormat                                               |      |      |      |      |
| A formatter for values as returned by the fielddata/doc-values APIs. |      |      |      |      |
| DocValueFormat.BinaryDocValueFormat                          |      |      |      |      |
| Singleton, stateless formatter, for representing bytes as base64 strings |      |      |      |      |
| DocValueFormat.BooleanDocValueFormat                         |      |      |      |      |
| Stateless, Singleton formatter for boolean values.           |      |      |      |      |
| DocValueFormat.DateTime                                      |      |      |      |      |
|                                                              |      |      |      |      |
| DocValueFormat.Decimal                                       |      |      |      |      |
|                                                              |      |      |      |      |
| DocValueFormat.GeoHashDocValueFormat                         |      |      |      |      |
| Singleton, stateless formatter for geo hash values           |      |      |      |      |
| DocValueFormat.GeoTileDocValueFormat                         |      |      |      |      |
|                                                              |      |      |      |      |
| DocValueFormat.IpDocValueFormat                              |      |      |      |      |
| Stateless, singleton formatter for IP address data           |      |      |      |      |
| DocValueFormat.RawDocValueFormat                             |      |      |      |      |
| Singleton, stateless formatter for "Raw" values, generally taken to mean keywords and other strings. |      |      |      |      |
| DocValueFormat.UnsignedLongShiftedDocValueFormat             |      |      |      |      |
| DocValues format for unsigned 64 bit long values, that are stored as shifted signed 64 bit long values. |      |      |      |      |
| LeafNestedDocuments                                          |      |      |      |      |
| Manages loading information about nested documents for a single index segment |      |      |      |      |
| MultiValueMode                                               |      |      |      |      |
| Defines what values to pick in the case a document contains multiple values for a particular field. |      |      |      |      |
| NestedDocuments                                              |      |      |      |      |
| Manages loading information about nested documents           |      |      |      |      |
| NestedUtils                                                  |      |      |      |      |
| Utility methods for dealing with nested mappers              |      |      |      |      |
| RescoreDocIds                                                |      |      |      |      |
| Since SearchContext no longer hold the states of search, the top K results (i.e., documents that will be rescored by query rescorers) need to be serialized/ deserialized between search phases. |      |      |      |      |
| Scroll                                                       |      |      |      |      |
| A scroll enables scrolling of search request.                |      |      |      |      |
| SearchContextMissingException                                |      |      |      |      |
|                                                              |      |      |      |      |
| SearchContextSourcePrinter                                   |      |      |      |      |
|                                                              |      |      |      |      |
| SearchException                                              |      |      |      |      |
|                                                              |      |      |      |      |
| SearchExtBuilder                                             |      |      |      |      |
| Intermediate serializable representation of a search ext section. |      |      |      |      |
| SearchHit                                                    |      |      |      |      |
| A single search hit.                                         |      |      |      |      |
| SearchHit.Fields                                             |      |      |      |      |
|                                                              |      |      |      |      |
| SearchHit.NestedIdentity                                     |      |      |      |      |
| Encapsulates the nested identity of a hit.                   |      |      |      |      |
| SearchHits                                                   |      |      |      |      |
|                                                              |      |      |      |      |
| SearchHits.Fields                                            |      |      |      |      |
|                                                              |      |      |      |      |
| SearchModule                                                 |      |      |      |      |
| Sets up things that can be done at search time like queries, aggregations, and suggesters. |      |      |      |      |
| SearchParseException                                         |      |      |      |      |
|                                                              |      |      |      |      |
| SearchPhaseResult                                            |      |      |      |      |
| This class is a base class for all search related results.   |      |      |      |      |
| SearchService                                                |      |      |      |      |
|                                                              |      |      |      |      |
| SearchShardTarget                                            |      |      |      |      |
| The target that the search request was executed on.          |      |      |      |      |
| SearchSortValues                                             |      |      |      |      |
|                                                              |      |      |      |      |
| SearchSortValuesAndFormats                                   |      |      |      |      |







org.elasticsearch.search.aggregations



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AbstractAggregationBuilder<AB extends AbstractAggregationBuilder<AB>> |      |      |      |      |
| Base implementation of a AggregationBuilder.                 |      |      |      |      |
| AdaptingAggregator                                           |      |      |      |      |
| An Aggregator that delegates collection to another Aggregator and then translates its results into the results you'd expect from another aggregation. |      |      |      |      |
| Aggregation                                                  |      |      |      |      |
| An aggregation.                                              |      |      |      |      |
| Aggregation.CommonFields                                     |      |      |      |      |
| Common xcontent fields that are shared among addAggregation  |      |      |      |      |
| AggregationBuilder                                           |      |      |      |      |
| A factory that knows how to create an Aggregator of a specific type. |      |      |      |      |
| AggregationBuilder.BucketCardinality                         |      |      |      |      |
| A rough count of the number of buckets that Aggregators built by this builder will contain per parent bucket used to validate sorts and pipeline aggregations. |      |      |      |      |
| AggregationBuilder.CommonFields                              |      |      |      |      |
| Common xcontent fields shared among aggregator builders      |      |      |      |      |
| AggregationBuilders                                          |      |      |      |      |
| Utility class to create aggregations.                        |      |      |      |      |
| AggregationExecutionException                                |      |      |      |      |
| Thrown when failing to execute an aggregation                |      |      |      |      |
| AggregationInitializationException                           |      |      |      |      |
| Thrown when failing to execute an aggregation                |      |      |      |      |
| AggregationPhase                                             |      |      |      |      |
| Aggregation phase of a search request, used to collect aggregations |      |      |      |      |
| Aggregations                                                 |      |      |      |      |
| Represents a set of Aggregations                             |      |      |      |      |
| Aggregator                                                   |      |      |      |      |
| An Aggregator.                                               |      |      |      |      |
| Aggregator.BucketComparator                                  |      |      |      |      |
| Compare two buckets by their ordinal.                        |      |      |      |      |
| Aggregator.Parser                                            |      |      |      |      |
| Parses the aggregation request and creates the appropriate aggregator factory for it. |      |      |      |      |
| Aggregator.SubAggCollectionMode                              |      |      |      |      |
| Aggregation mode for sub aggregations.                       |      |      |      |      |
| AggregatorBase                                               |      |      |      |      |
| Base implementation for concrete aggregators.                |      |      |      |      |
| AggregatorFactories                                          |      |      |      |      |
| An immutable collection of AggregatorFactories.              |      |      |      |      |
| AggregatorFactories.Builder                                  |      |      |      |      |
| A mutable collection of AggregationBuilders and PipelineAggregationBuilders. |      |      |      |      |
| AggregatorFactory                                            |      |      |      |      |
|                                                              |      |      |      |      |
| BaseAggregationBuilder                                       |      |      |      |      |
| Interface shared by AggregationBuilder and PipelineAggregationBuilder so they can conveniently share the same namespace for XContentParser.namedObject(Class, String, Object). |      |      |      |      |
| BucketCollector                                              |      |      |      |      |
| A Collector that can collect data in separate buckets.       |      |      |      |      |
| BucketOrder                                                  |      |      |      |      |
| MultiBucketsAggregation.Bucket ordering strategy.            |      |      |      |      |
| CardinalityUpperBound                                        |      |      |      |      |
| Upper bound of how many owningBucketOrds that an Aggregator will have to collect into. |      |      |      |      |
| DelayedBucket<B extends InternalMultiBucketAggregation.InternalBucket> |      |      |      |      |
| A wrapper around reducing buckets with the same key that can delay that reduction as long as possible. |      |      |      |      |
| HasAggregations                                              |      |      |      |      |
|                                                              |      |      |      |      |
| InternalAggregation                                          |      |      |      |      |
| An internal implementation of Aggregation.                   |      |      |      |      |
| InternalAggregation.ReduceContext                            |      |      |      |      |
|                                                              |      |      |      |      |
| InternalAggregation.ReduceContextBuilder                     |      |      |      |      |
| Builds InternalAggregation.ReduceContext.                    |      |      |      |      |
| InternalAggregations                                         |      |      |      |      |
| An internal implementation of Aggregations.                  |      |      |      |      |
| InternalMultiBucketAggregation<A extends InternalMultiBucketAggregation,B extends InternalMultiBucketAggregation.InternalBucket> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMultiBucketAggregation.InternalBucket                |      |      |      |      |
|                                                              |      |      |      |      |
| InternalOrder                                                |      |      |      |      |
| Implementations for MultiBucketsAggregation.Bucket ordering strategies. |      |      |      |      |
| InternalOrder.Aggregation                                    |      |      |      |      |
| MultiBucketsAggregation.Bucket ordering strategy to sort by a sub-aggregation. |      |      |      |      |
| InternalOrder.CompoundOrder                                  |      |      |      |      |
| MultiBucketsAggregation.Bucket ordering strategy to sort by multiple criteria. |      |      |      |      |
| InternalOrder.Parser                                         |      |      |      |      |
| Contains logic for parsing a BucketOrder from a XContentParser. |      |      |      |      |
| InternalOrder.Streams                                        |      |      |      |      |
| Contains logic for reading/writing BucketOrder from/to streams. |      |      |      |      |
| InvalidAggregationPathException                              |      |      |      |      |
|                                                              |      |      |      |      |
| KeyComparable<T extends MultiBucketsAggregation.Bucket & KeyComparable<T>> |      |      |      |      |
| Defines behavior for comparing bucket keys to imposes a total ordering of buckets of the same type. |      |      |      |      |
| LeafBucketCollector                                          |      |      |      |      |
| Collects results for a particular segment.                   |      |      |      |      |
| LeafBucketCollectorBase                                      |      |      |      |      |
| A LeafBucketCollector that delegates all calls to the sub leaf aggregator and sets the scorer on its source of values if it implements ScorerAware. |      |      |      |      |
| MultiBucketCollector                                         |      |      |      |      |
| A BucketCollector which allows running a bucket collection with several BucketCollectors. |      |      |      |      |
| MultiBucketConsumerService                                   |      |      |      |      |
| An aggregation service that creates instances of MultiBucketConsumerService.MultiBucketConsumer. |      |      |      |      |
| MultiBucketConsumerService.MultiBucketConsumer               |      |      |      |      |
| An IntConsumer that throws a MultiBucketConsumerService.TooManyBucketsException when the sum of the provided values is above the limit (`search.max_buckets`). |      |      |      |      |
| MultiBucketConsumerService.TooManyBucketsException           |      |      |      |      |
|                                                              |      |      |      |      |
| NonCollectingAggregator                                      |      |      |      |      |
| An aggregator that is not collected, this can typically be used when running an aggregation over a field that doesn't have a mapping. |      |      |      |      |
| ParsedAggregation                                            |      |      |      |      |
| An implementation of Aggregation that is parsed from a REST response. |      |      |      |      |
| ParsedMultiBucketAggregation<B extends MultiBucketsAggregation.Bucket> |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedMultiBucketAggregation.ParsedBucket                    |      |      |      |      |
|                                                              |      |      |      |      |
| PipelineAggregationBuilder                                   |      |      |      |      |
| A factory that knows how to create an PipelineAggregator of a specific type. |      |      |      |      |
| PipelineAggregationBuilder.ValidationContext                 |      |      |      |      |
|                                                              |      |      |      |      |
| PipelineAggregatorBuilders                                   |      |      |      |      |
|                                                              |      |      |      |      |
| SearchContextAggregations                                    |      |      |      |      |
| The aggregation context that is part of the search context.  |      |      |      |      |
| TopBucketBuilder<B extends InternalMultiBucketAggregation.InternalBucket> |      |      |      |      |
| Merges many buckets into the "top" buckets as sorted by BucketOrder. |      |      |      |      |







org.elasticsearch.search.aggregations.bucket



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| BestBucketsDeferringCollector                                |      |      |      |      |
| A specialization of DeferringBucketCollector that collects all matches and then is able to replay a given subset of buckets which represent the survivors from a pruning process performed by the aggregator that owns this collector. |      |      |      |      |
| BucketsAggregator                                            |      |      |      |      |
|                                                              |      |      |      |      |
| BucketsAggregator.BucketBuilderForFixedCount<B>              |      |      |      |      |
|                                                              |      |      |      |      |
| BucketsAggregator.BucketBuilderForVariable<B>                |      |      |      |      |
|                                                              |      |      |      |      |
| BucketsAggregator.ResultBuilderForVariable<B>                |      |      |      |      |
|                                                              |      |      |      |      |
| BucketsAggregator.SingleBucketResultBuilder                  |      |      |      |      |
|                                                              |      |      |      |      |
| BucketUtils                                                  |      |      |      |      |
| Helper functions for common Bucketing functions              |      |      |      |      |
| DeferableBucketAggregator                                    |      |      |      |      |
|                                                              |      |      |      |      |
| DeferringBucketCollector                                     |      |      |      |      |
| A BucketCollector that records collected doc IDs and buckets and allows to replay a subset of the collected buckets. |      |      |      |      |
| DocCountProvider                                             |      |      |      |      |
| An implementation of a doc_count provider that reads the value of the _doc_count field in the document. |      |      |      |      |
| InternalSingleBucketAggregation                              |      |      |      |      |
| A base class for all the single bucket aggregations.         |      |      |      |      |
| IteratorAndCurrent<B extends InternalMultiBucketAggregation.InternalBucket> |      |      |      |      |
|                                                              |      |      |      |      |
| MultiBucketsAggregation                                      |      |      |      |      |
| An aggregation that returns multiple buckets                 |      |      |      |      |
| MultiBucketsAggregation.Bucket                               |      |      |      |      |
| A bucket represents a criteria to which all documents that fall in it adhere to. |      |      |      |      |
| ParsedSingleBucketAggregation                                |      |      |      |      |
| A base class for all the single bucket aggregations.         |      |      |      |      |
| SingleBucketAggregation                                      |      |      |      |      |
| A single bucket aggregation                                  |      |      |      |      |
| SingleBucketAggregator                                       |      |      |      |      |
| A bucket aggregator that doesn't create new buckets.         |      |      |      |      |





org.elasticsearch.search.aggregations.bucket.adjacency



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AdjacencyMatrix                                              |      |      |
| A multi bucket aggregation where the buckets are defined by a set of filters (a bucket is produced per filter plus a bucket for each non-empty filter intersection so A, B and A&B). |      |      |
| AdjacencyMatrix.Bucket                                       |      |      |
| A bucket associated with a specific filter or pair (identified by its key) |      |      |
| AdjacencyMatrixAggregationBuilder                            |      |      |
|                                                              |      |      |
| AdjacencyMatrixAggregator                                    |      |      |
| Aggregation for adjacency matrices.                          |      |      |
| AdjacencyMatrixAggregator.KeyedFilter                        |      |      |
|                                                              |      |      |
| AdjacencyMatrixAggregatorFactory                             |      |      |
|                                                              |      |      |
| InternalAdjacencyMatrix                                      |      |      |
|                                                              |      |      |
| InternalAdjacencyMatrix.InternalBucket                       |      |      |
|                                                              |      |      |
| ParsedAdjacencyMatrix                                        |      |      |
|                                                              |      |      |
| ParsedAdjacencyMatrix.ParsedBucket                           |      |      |





org.elasticsearch.search.aggregations.bucket.composite



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CompositeAggregation                                         |      |      |      |
|                                                              |      |      |      |
| CompositeAggregation.Bucket                                  |      |      |      |
|                                                              |      |      |      |
| CompositeAggregationBuilder                                  |      |      |      |
|                                                              |      |      |      |
| CompositeAggregator                                          |      |      |      |
|                                                              |      |      |      |
| CompositeValuesSourceBuilder<AB extends CompositeValuesSourceBuilder<AB>> |      |      |      |
| A ValuesSource builder for CompositeAggregationBuilder       |      |      |      |
| CompositeValuesSourceConfig                                  |      |      |      |
|                                                              |      |      |      |
| CompositeValuesSourceConfig.SingleDimensionValuesSourceProvider |      |      |      |
|                                                              |      |      |      |
| CompositeValuesSourceParserHelper                            |      |      |      |
|                                                              |      |      |      |
| DateHistogramValuesSource                                    |      |      |      |
| A SingleDimensionValuesSource for date histogram values.     |      |      |      |
| DateHistogramValuesSourceBuilder                             |      |      |      |
| A CompositeValuesSourceBuilder that builds a RoundingValuesSource from a Script or a field name using the provided interval. |      |      |      |
| DateHistogramValuesSourceBuilder.DateHistogramCompositeSupplier |      |      |      |
|                                                              |      |      |      |
| GeoTileGridValuesSourceBuilder                               |      |      |      |
|                                                              |      |      |      |
| GeoTileGridValuesSourceBuilder.GeoTileCompositeSuppier       |      |      |      |
|                                                              |      |      |      |
| HistogramValuesSourceBuilder                                 |      |      |      |
| A CompositeValuesSourceBuilder that builds a HistogramValuesSource from another numeric values source using the provided interval. |      |      |      |
| HistogramValuesSourceBuilder.HistogramCompositeSupplier      |      |      |      |
|                                                              |      |      |      |
| InternalComposite                                            |      |      |      |
|                                                              |      |      |      |
| InternalComposite.InternalBucket                             |      |      |      |
|                                                              |      |      |      |
| MissingOrder                                                 |      |      |      |
|                                                              |      |      |      |
| ParsedComposite                                              |      |      |      |
|                                                              |      |      |      |
| ParsedComposite.ParsedBucket                                 |      |      |      |
|                                                              |      |      |      |
| TermsValuesSourceBuilder                                     |      |      |      |
| A CompositeValuesSourceBuilder that builds a ValuesSource from a Script or a field name. |      |      |      |
| TermsValuesSourceBuilder.TermsCompositeSupplier              |      |      |      |







org.elasticsearch.search.aggregations.bucket.filter



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| Filter                                                       |      |      |      |
| A filter aggregation.                                        |      |      |      |
| FilterAggregationBuilder                                     |      |      |      |
|                                                              |      |      |      |
| FilterAggregator                                             |      |      |      |
| Aggregate all docs that match a filter.                      |      |      |      |
| FilterAggregatorFactory                                      |      |      |      |
|                                                              |      |      |      |
| FilterByFilterAggregator                                     |      |      |      |
| Collects results by running each filter against the searcher and doesn't build any LeafBucketCollectors which is generally faster than FiltersAggregator.Compatible but doesn't support when there is a parent aggregator or any child aggregators. |      |      |      |
| FilterByFilterAggregator.AdapterBuilder<T>                   |      |      |      |
| Builds FilterByFilterAggregator when the filters are valid and it would be faster than a "native" aggregation implementation. |      |      |      |
| Filters                                                      |      |      |      |
| A multi bucket aggregation where the buckets are defined by a set of filters (a bucket per filter). |      |      |      |
| Filters.Bucket                                               |      |      |      |
| A bucket associated with a specific filter (identified by its key) |      |      |      |
| FiltersAggregationBuilder                                    |      |      |      |
|                                                              |      |      |      |
| FiltersAggregator                                            |      |      |      |
| Aggregator for filters.                                      |      |      |      |
| FiltersAggregator.KeyedFilter                                |      |      |      |
|                                                              |      |      |      |
| FiltersAggregatorFactory                                     |      |      |      |
|                                                              |      |      |      |
| InternalFilter                                               |      |      |      |
|                                                              |      |      |      |
| InternalFilters                                              |      |      |      |
|                                                              |      |      |      |
| InternalFilters.InternalBucket                               |      |      |      |
|                                                              |      |      |      |
| MergedPointRangeQuery                                        |      |      |      |
| Query merging two point in range queries.                    |      |      |      |
| ParsedFilter                                                 |      |      |      |
|                                                              |      |      |      |
| ParsedFilters                                                |      |      |      |
|                                                              |      |      |      |
| ParsedFilters.ParsedBucket                                   |      |      |      |
|                                                              |      |      |      |
| QueryToFilterAdapter<Q extends org.apache.lucene.search.Query> |      |      |      |
| Adapts a Lucene Query to the behaviors used be the FiltersAggregator. |      |      |      |









org.elasticsearch.search.aggregations.bucket.geogrid



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| GeoGrid                                                      |      |      |      |
| A geo-grid aggregation.                                      |      |      |      |
| GeoGrid.Bucket                                               |      |      |      |
| A bucket that is associated with a geo-grid cell.            |      |      |      |
| GeoGridAggregationBuilder                                    |      |      |      |
|                                                              |      |      |      |
| GeoGridAggregationBuilder.PrecisionParser                    |      |      |      |
|                                                              |      |      |      |
| GeoGridAggregator<T extends InternalGeoGrid<?>>              |      |      |      |
| Aggregates data expressed as longs (for efficiency's sake) but formats results as aggregation-specific strings. |      |      |      |
| GeoHashCellIdSource                                          |      |      |      |
| Class to help convert MultiGeoPointValues to GeoHash bucketing. |      |      |      |
| GeoHashGridAggregationBuilder                                |      |      |      |
|                                                              |      |      |      |
| GeoHashGridAggregator                                        |      |      |      |
| Aggregates data expressed as GeoHash longs (for efficiency's sake) but formats results as Geohash strings. |      |      |      |
| GeoHashGridAggregatorFactory                                 |      |      |      |
|                                                              |      |      |      |
| GeoTileCellIdSource                                          |      |      |      |
| Class to help convert MultiGeoPointValues to GeoTile bucketing. |      |      |      |
| GeoTileGridAggregationBuilder                                |      |      |      |
|                                                              |      |      |      |
| GeoTileGridAggregator                                        |      |      |      |
| Aggregates data expressed as geotile longs (for efficiency's sake) but formats results as geotile strings. |      |      |      |
| GeoTileGridAggregatorFactory                                 |      |      |      |
|                                                              |      |      |      |
| GeoTileUtils                                                 |      |      |      |
| Implements geotile key hashing, same as used by many map tile implementations. |      |      |      |
| InternalGeoGrid<B extends InternalGeoGridBucket>             |      |      |      |
| Represents a grid of cells where each cell's location is determined by a specific geo hashing algorithm. |      |      |      |
| InternalGeoGridBucket                                        |      |      |      |
|                                                              |      |      |      |
| InternalGeoHashGrid                                          |      |      |      |
| Represents a grid of cells where each cell's location is determined by a geohash. |      |      |      |
| InternalGeoHashGridBucket                                    |      |      |      |
|                                                              |      |      |      |
| InternalGeoTileGrid                                          |      |      |      |
| Represents a grid of cells where each cell's location is determined by a geohash. |      |      |      |
| InternalGeoTileGridBucket                                    |      |      |      |
|                                                              |      |      |      |
| ParsedGeoGrid                                                |      |      |      |
|                                                              |      |      |      |
| ParsedGeoGridBucket                                          |      |      |      |
|                                                              |      |      |      |
| ParsedGeoHashGrid                                            |      |      |      |
|                                                              |      |      |      |
| ParsedGeoHashGridBucket                                      |      |      |      |
|                                                              |      |      |      |
| ParsedGeoTileGrid                                            |      |      |      |
|                                                              |      |      |      |
| ParsedGeoTileGridBucket                                      |      |      |      |





org.elasticsearch.search.aggregations.bucket.global



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| Global                                                       |      |      |      |
| A global aggregation.                                        |      |      |      |
| GlobalAggregationBuilder                                     |      |      |      |
|                                                              |      |      |      |
| GlobalAggregator                                             |      |      |      |
|                                                              |      |      |      |
| GlobalAggregatorFactory                                      |      |      |      |
|                                                              |      |      |      |
| InternalGlobal                                               |      |      |      |
| A global scope get (the document set on which we aggregate is all documents in the search context (ie. |      |      |      |
| ParsedGlobal                                                 |      |      |      |





org.elasticsearch.search.aggregations.bucket.histogram



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractHistogramAggregator                                  |      |      |      |
| Base class for functionality shared between aggregators for this histogram aggregation. |      |      |      |
| AutoDateHistogramAggregationBuilder                          |      |      |      |
|                                                              |      |      |      |
| AutoDateHistogramAggregationBuilder.RoundingInfo             |      |      |      |
|                                                              |      |      |      |
| AutoDateHistogramAggregatorFactory                           |      |      |      |
|                                                              |      |      |      |
| AutoDateHistogramAggregatorSupplier                          |      |      |      |
|                                                              |      |      |      |
| DateHistogramAggregationBuilder                              |      |      |      |
| A builder for histograms on date fields.                     |      |      |      |
| DateHistogramAggregationSupplier                             |      |      |      |
|                                                              |      |      |      |
| DateHistogramAggregatorFactory                               |      |      |      |
|                                                              |      |      |      |
| DateHistogramInterval                                        |      |      |      |
| The interval the date histogram is based on.                 |      |      |      |
| DateIntervalConsumer<T>                                      |      |      |      |
| A shared interface for aggregations that parse and use "interval" parameters. |      |      |      |
| DateIntervalWrapper                                          |      |      |      |
| A class that handles all the parsing, bwc and deprecations surrounding date histogram intervals. |      |      |      |
| DateIntervalWrapper.IntervalTypeEnum                         |      |      |      |
|                                                              |      |      |      |
| DoubleBounds                                                 |      |      |      |
| Represent hard_bounds and extended_bounds in histogram aggregations. |      |      |      |
| Histogram                                                    |      |      |      |
| A histogram aggregation.                                     |      |      |      |
| Histogram.Bucket                                             |      |      |      |
| A bucket in the histogram where documents fall in            |      |      |      |
| HistogramAggregationBuilder                                  |      |      |      |
| A builder for histograms on numeric fields.                  |      |      |      |
| HistogramAggregatorFactory                                   |      |      |      |
| Constructs the per-shard aggregator instance for histogram aggregation. |      |      |      |
| HistogramAggregatorSupplier                                  |      |      |      |
|                                                              |      |      |      |
| HistogramFactory                                             |      |      |      |
| Implemented by histogram aggregations and used by pipeline aggregations to insert buckets. |      |      |      |
| InternalAutoDateHistogram                                    |      |      |      |
| Implementation of Histogram.                                 |      |      |      |
| InternalAutoDateHistogram.Bucket                             |      |      |      |
|                                                              |      |      |      |
| InternalDateHistogram                                        |      |      |      |
| Implementation of Histogram.                                 |      |      |      |
| InternalDateHistogram.Bucket                                 |      |      |      |
|                                                              |      |      |      |
| InternalHistogram                                            |      |      |      |
| Implementation of Histogram.                                 |      |      |      |
| InternalHistogram.Bucket                                     |      |      |      |
|                                                              |      |      |      |
| InternalHistogram.EmptyBucketInfo                            |      |      |      |
|                                                              |      |      |      |
| InternalVariableWidthHistogram                               |      |      |      |
|                                                              |      |      |      |
| InternalVariableWidthHistogram.Bucket                        |      |      |      |
|                                                              |      |      |      |
| InternalVariableWidthHistogram.Bucket.BucketBounds           |      |      |      |
|                                                              |      |      |      |
| LongBounds                                                   |      |      |      |
| Represent hard_bounds and extended_bounds in date-histogram aggregations. |      |      |      |
| NumericHistogramAggregator                                   |      |      |      |
| An aggregator for numeric values.                            |      |      |      |
| ParsedAutoDateHistogram                                      |      |      |      |
|                                                              |      |      |      |
| ParsedAutoDateHistogram.ParsedBucket                         |      |      |      |
|                                                              |      |      |      |
| ParsedDateHistogram                                          |      |      |      |
|                                                              |      |      |      |
| ParsedDateHistogram.ParsedBucket                             |      |      |      |
|                                                              |      |      |      |
| ParsedHistogram                                              |      |      |      |
|                                                              |      |      |      |
| ParsedVariableWidthHistogram                                 |      |      |      |
|                                                              |      |      |      |
| ParsedVariableWidthHistogram.ParsedBucket                    |      |      |      |
|                                                              |      |      |      |
| RangeHistogramAggregator                                     |      |      |      |
|                                                              |      |      |      |
| SizedBucketAggregator                                        |      |      |      |
| An aggregator capable of reporting bucket sizes in requested units. |      |      |      |
| SizedBucketAggregatorBuilder                                 |      |      |      |
| An aggregator capable of reporting bucket sizes in milliseconds. |      |      |      |
| VariableWidthHistogramAggregationBuilder                     |      |      |      |
|                                                              |      |      |      |
| VariableWidthHistogramAggregator                             |      |      |      |
|                                                              |      |      |      |
| VariableWidthHistogramAggregatorFactory                      |      |      |      |
|                                                              |      |      |      |
| VariableWidthHistogramAggregatorSupplier                     |      |      |      |



org.elasticsearch.search.aggregations.bucket.missing



| Class                     |      |      |      |
| ------------------------- | ---- | ---- | ---- |
| Description               |      |      |      |
| InternalMissing           |      |      |      |
|                           |      |      |      |
| Missing                   |      |      |      |
| A missing aggregation.    |      |      |      |
| MissingAggregationBuilder |      |      |      |
|                           |      |      |      |
| MissingAggregator         |      |      |      |
|                           |      |      |      |
| MissingAggregatorFactory  |      |      |      |
|                           |      |      |      |
| MissingAggregatorSupplier |      |      |      |
|                           |      |      |      |
| ParsedMissing             |      |      |      |





org.elasticsearch.search.aggregations.bucket.nested



| Class                                  |      |      |      |
| -------------------------------------- | ---- | ---- | ---- |
| Description                            |      |      |      |
| InternalNested                         |      |      |      |
| Result of the NestedAggregator.        |      |      |      |
| InternalReverseNested                  |      |      |      |
| Result of the ReverseNestedAggregator. |      |      |      |
| Nested                                 |      |      |      |
| A nested aggregation.                  |      |      |      |
| NestedAggregationBuilder               |      |      |      |
|                                        |      |      |      |
| NestedAggregator                       |      |      |      |
|                                        |      |      |      |
| NestedAggregatorFactory                |      |      |      |
|                                        |      |      |      |
| ParsedNested                           |      |      |      |
|                                        |      |      |      |
| ParsedReverseNested                    |      |      |      |
|                                        |      |      |      |
| ReverseNested                          |      |      |      |
| A reverse nested aggregation.          |      |      |      |
| ReverseNestedAggregationBuilder        |      |      |      |
|                                        |      |      |      |
| ReverseNestedAggregator                |      |      |      |
|                                        |      |      |      |
| ReverseNestedAggregatorFactory         |      |      |      |





org.elasticsearch.search.aggregations.bucket.range



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractRangeAggregatorFactory<R extends RangeAggregator.Range> |      |      |      |
|                                                              |      |      |      |
| AbstractRangeBuilder<AB extends AbstractRangeBuilder<AB,R>,R extends RangeAggregator.Range> |      |      |      |
|                                                              |      |      |      |
| BinaryRangeAggregator                                        |      |      |      |
| A range aggregator for values that are stored in SORTED_SET doc values. |      |      |      |
| BinaryRangeAggregator.Range                                  |      |      |      |
|                                                              |      |      |      |
| BinaryRangeAggregatorFactory                                 |      |      |      |
|                                                              |      |      |      |
| DateRangeAggregationBuilder                                  |      |      |      |
|                                                              |      |      |      |
| DateRangeAggregatorFactory                                   |      |      |      |
|                                                              |      |      |      |
| GeoDistanceAggregationBuilder                                |      |      |      |
|                                                              |      |      |      |
| GeoDistanceAggregationBuilder.Range                          |      |      |      |
|                                                              |      |      |      |
| GeoDistanceAggregatorSupplier                                |      |      |      |
|                                                              |      |      |      |
| GeoDistanceRangeAggregatorFactory                            |      |      |      |
|                                                              |      |      |      |
| InternalBinaryRange                                          |      |      |      |
| A range aggregation for data that is encoded in doc values using a binary representation. |      |      |      |
| InternalBinaryRange.Bucket                                   |      |      |      |
|                                                              |      |      |      |
| InternalDateRange                                            |      |      |      |
|                                                              |      |      |      |
| InternalDateRange.Bucket                                     |      |      |      |
|                                                              |      |      |      |
| InternalDateRange.Factory                                    |      |      |      |
|                                                              |      |      |      |
| InternalGeoDistance                                          |      |      |      |
|                                                              |      |      |      |
| InternalGeoDistance.Factory                                  |      |      |      |
|                                                              |      |      |      |
| InternalRange<B extends InternalRange.Bucket,R extends InternalRange<B,R>> |      |      |      |
|                                                              |      |      |      |
| InternalRange.Bucket                                         |      |      |      |
|                                                              |      |      |      |
| InternalRange.Factory<B extends InternalRange.Bucket,R extends InternalRange<B,R>> |      |      |      |
|                                                              |      |      |      |
| IpRangeAggregationBuilder                                    |      |      |      |
|                                                              |      |      |      |
| IpRangeAggregationBuilder.Range                              |      |      |      |
|                                                              |      |      |      |
| IpRangeAggregatorSupplier                                    |      |      |      |
|                                                              |      |      |      |
| ParsedBinaryRange                                            |      |      |      |
|                                                              |      |      |      |
| ParsedBinaryRange.ParsedBucket                               |      |      |      |
|                                                              |      |      |      |
| ParsedDateRange                                              |      |      |      |
|                                                              |      |      |      |
| ParsedDateRange.ParsedBucket                                 |      |      |      |
|                                                              |      |      |      |
| ParsedGeoDistance                                            |      |      |      |
|                                                              |      |      |      |
| ParsedGeoDistance.ParsedBucket                               |      |      |      |
|                                                              |      |      |      |
| ParsedRange                                                  |      |      |      |
|                                                              |      |      |      |
| ParsedRange.ParsedBucket                                     |      |      |      |
|                                                              |      |      |      |
| Range                                                        |      |      |      |
| A range aggregation.                                         |      |      |      |
| Range.Bucket                                                 |      |      |      |
| A bucket associated with a specific range                    |      |      |      |
| RangeAggregationBuilder                                      |      |      |      |
|                                                              |      |      |      |
| RangeAggregator                                              |      |      |      |
| Aggregator for range.                                        |      |      |      |
| RangeAggregator.Range                                        |      |      |      |
|                                                              |      |      |      |
| RangeAggregator.Unmapped<R extends RangeAggregator.Range>    |      |      |      |
|                                                              |      |      |      |
| RangeAggregatorFactory                                       |      |      |      |
|                                                              |      |      |      |
| RangeAggregatorSupplier                                      |      |      |      |







org.elasticsearch.search.aggregations.bucket.sampler



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| BestDocsDeferringCollector                                   |      |      |      |
| A specialization of DeferringBucketCollector that collects all matches and then replays only the top scoring documents to child aggregations. |      |      |      |
| DiversifiedAggregationBuilder                                |      |      |      |
|                                                              |      |      |      |
| DiversifiedAggregatorFactory                                 |      |      |      |
|                                                              |      |      |      |
| DiversifiedAggregatorSupplier                                |      |      |      |
|                                                              |      |      |      |
| DiversifiedBytesHashSamplerAggregator                        |      |      |      |
| Alternative, faster implementation for converting String keys to longs but with the potential for hash collisions. |      |      |      |
| DiversifiedMapSamplerAggregator                              |      |      |      |
|                                                              |      |      |      |
| DiversifiedNumericSamplerAggregator                          |      |      |      |
|                                                              |      |      |      |
| DiversifiedOrdinalsSamplerAggregator                         |      |      |      |
|                                                              |      |      |      |
| InternalSampler                                              |      |      |      |
|                                                              |      |      |      |
| ParsedSampler                                                |      |      |      |
|                                                              |      |      |      |
| Sampler                                                      |      |      |      |
| A filter aggregation that defines a single bucket to hold a sample of top-matching documents. |      |      |      |
| SamplerAggregationBuilder                                    |      |      |      |
|                                                              |      |      |      |
| SamplerAggregator                                            |      |      |      |
| Aggregate on only the top-scoring docs on a shard.           |      |      |      |
| SamplerAggregator.ExecutionMode                              |      |      |      |
|                                                              |      |      |      |
| SamplerAggregatorFactory                                     |      |      |      |
|                                                              |      |      |      |
| UnmappedSampler                                              |      |      |      |





org.elasticsearch.search.aggregations.bucket.terms





| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AbstractInternalTerms<A extends AbstractInternalTerms<A,B>,B extends AbstractInternalTerms.AbstractTermsBucket> |      |      |      |      |
| Base class for terms and multi_terms aggregation that handles common reduce logic |      |      |      |      |
| AbstractInternalTerms.AbstractTermsBucket                    |      |      |      |      |
|                                                              |      |      |      |      |
| AbstractRareTermsAggregator                                  |      |      |      |      |
|                                                              |      |      |      |      |
| BucketPriorityQueue<B>                                       |      |      |      |      |
|                                                              |      |      |      |      |
| BucketSignificancePriorityQueue<B extends SignificantTerms.Bucket> |      |      |      |      |
|                                                              |      |      |      |      |
| BytesKeyedBucketOrds                                         |      |      |      |      |
| Maps BytesRef bucket keys to bucket ordinals.                |      |      |      |      |
| BytesKeyedBucketOrds.BucketOrdsEnum                          |      |      |      |      |
| An iterator for buckets inside a particular owningBucketOrd. |      |      |      |      |
| DoubleTerms                                                  |      |      |      |      |
| Result of the TermsAggregator when the field is some kind of decimal number like a float, double, or distance. |      |      |      |      |
| GlobalOrdinalsStringTermsAggregator                          |      |      |      |      |
| An aggregator of string values that relies on global ordinals in order to build buckets. |      |      |      |      |
| GlobalOrdinalsStringTermsAggregator.GlobalOrdLookupFunction  |      |      |      |      |
|                                                              |      |      |      |      |
| IncludeExclude                                               |      |      |      |      |
| Defines the include/exclude regular expression filtering for string terms aggregation. |      |      |      |      |
| IncludeExclude.Filter                                        |      |      |      |      |
|                                                              |      |      |      |      |
| IncludeExclude.LongFilter                                    |      |      |      |      |
|                                                              |      |      |      |      |
| IncludeExclude.OrdinalsFilter                                |      |      |      |      |
|                                                              |      |      |      |      |
| IncludeExclude.SetBackedLongFilter                           |      |      |      |      |
|                                                              |      |      |      |      |
| IncludeExclude.StringFilter                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMappedRareTerms<A extends InternalRareTerms<A,B>,B extends InternalRareTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMappedSignificantTerms<A extends InternalMappedSignificantTerms<A,B>,B extends InternalSignificantTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMappedTerms<A extends InternalTerms<A,B>,B extends InternalTerms.Bucket<B>> |      |      |      |      |
| Common superclass for results of the terms aggregation on mapped fields. |      |      |      |      |
| InternalRareTerms<A extends InternalRareTerms<A,B>,B extends InternalRareTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalRareTerms.Bucket<B extends InternalRareTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalRareTerms.Bucket.Reader<B extends InternalRareTerms.Bucket<B>> |      |      |      |      |
| Reads a bucket.                                              |      |      |      |      |
| InternalSignificantTerms<A extends InternalSignificantTerms<A,B>,B extends InternalSignificantTerms.Bucket<B>> |      |      |      |      |
| Result of the significant terms aggregation.                 |      |      |      |      |
| InternalSignificantTerms.Bucket<B extends InternalSignificantTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalSignificantTerms.Bucket.Reader<B extends InternalSignificantTerms.Bucket<B>> |      |      |      |      |
| Reads a bucket.                                              |      |      |      |      |
| InternalTerms<A extends InternalTerms<A,B>,B extends InternalTerms.Bucket<B>> |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTerms.Bucket<B extends InternalTerms.Bucket<B>>      |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTerms.Bucket.Reader<B extends InternalTerms.Bucket<B>> |      |      |      |      |
| Reads a bucket.                                              |      |      |      |      |
| LongKeyedBucketOrds                                          |      |      |      |      |
| Maps owning bucket ordinals and long bucket keys to bucket ordinals. |      |      |      |      |
| LongKeyedBucketOrds.BucketOrdsEnum                           |      |      |      |      |
| An iterator for buckets inside a particular owningBucketOrd. |      |      |      |      |
| LongKeyedBucketOrds.FromMany                                 |      |      |      |      |
| Implementation that works properly when collecting from many buckets. |      |      |      |      |
| LongKeyedBucketOrds.FromManySmall                            |      |      |      |      |
| Implementation that packs the owningbucketOrd into the top bits of a long and uses the bottom bits for the value. |      |      |      |      |
| LongKeyedBucketOrds.FromSingle                               |      |      |      |      |
| Implementation that only works if it is collecting from a single bucket. |      |      |      |      |
| LongRareTerms                                                |      |      |      |      |
| Result of the RareTerms aggregation when the field is some kind of whole number like a integer, long, or a date. |      |      |      |      |
| LongRareTerms.Bucket                                         |      |      |      |      |
|                                                              |      |      |      |      |
| LongRareTermsAggregator                                      |      |      |      |      |
| An aggregator that finds "rare" string values (e.g.          |      |      |      |      |
| LongTerms                                                    |      |      |      |      |
| Result of the TermsAggregator when the field is some kind of whole number like a integer, long, or a date. |      |      |      |      |
| LongTerms.Bucket                                             |      |      |      |      |
|                                                              |      |      |      |      |
| MapStringTermsAggregator                                     |      |      |      |      |
| An aggregator of string values that hashes the strings on the fly rather than up front like the GlobalOrdinalsStringTermsAggregator. |      |      |      |      |
| MapStringTermsAggregator.CollectConsumer                     |      |      |      |      |
|                                                              |      |      |      |      |
| MapStringTermsAggregator.CollectorSource                     |      |      |      |      |
| Abstraction on top of building collectors to fetch values so terms, significant_terms, and significant_text can share a bunch of aggregation code. |      |      |      |      |
| MapStringTermsAggregator.ValuesSourceCollectorSource         |      |      |      |      |
| Fetch values from a ValuesSource.                            |      |      |      |      |
| NumericTermsAggregator                                       |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedDoubleTerms                                            |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedDoubleTerms.ParsedBucket                               |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedLongRareTerms                                          |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedLongRareTerms.ParsedBucket                             |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedLongTerms                                              |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedLongTerms.ParsedBucket                                 |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedRareTerms                                              |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedRareTerms.ParsedBucket                                 |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantLongTerms                                   |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantLongTerms.ParsedBucket                      |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantStringTerms                                 |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantStringTerms.ParsedBucket                    |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantTerms                                       |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedSignificantTerms.ParsedBucket                          |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedStringRareTerms                                        |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedStringRareTerms.ParsedBucket                           |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedStringTerms                                            |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedStringTerms.ParsedBucket                               |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedTerms                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| ParsedTerms.ParsedBucket                                     |      |      |      |      |
|                                                              |      |      |      |      |
| RareTerms                                                    |      |      |      |      |
|                                                              |      |      |      |      |
| RareTerms.Bucket                                             |      |      |      |      |
| A bucket that is associated with a single term               |      |      |      |      |
| RareTermsAggregationBuilder                                  |      |      |      |      |
|                                                              |      |      |      |      |
| RareTermsAggregatorFactory                                   |      |      |      |      |
|                                                              |      |      |      |      |
| RareTermsAggregatorFactory.ExecutionMode                     |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantLongTerms                                         |      |      |      |      |
| Result of the running the significant terms aggregation on a numeric field. |      |      |      |      |
| SignificantLongTerms.Bucket                                  |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantStringTerms                                       |      |      |      |      |
| Result of the running the significant terms aggregation on a String field. |      |      |      |      |
| SignificantStringTerms.Bucket                                |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTerms                                             |      |      |      |      |
| An aggregation that collects significant terms in comparison to a background set. |      |      |      |      |
| SignificantTerms.Bucket                                      |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTermsAggregationBuilder                           |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTermsAggregatorFactory                            |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTermsAggregatorFactory.ExecutionMode              |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTextAggregationBuilder                            |      |      |      |      |
|                                                              |      |      |      |      |
| SignificantTextAggregatorFactory                             |      |      |      |      |
|                                                              |      |      |      |      |
| StringRareTerms                                              |      |      |      |      |
|                                                              |      |      |      |      |
| StringRareTerms.Bucket                                       |      |      |      |      |
|                                                              |      |      |      |      |
| StringRareTermsAggregator                                    |      |      |      |      |
| An aggregator that finds "rare" string values (e.g.          |      |      |      |      |
| StringTerms                                                  |      |      |      |      |
| Result of the TermsAggregator when the field is a String.    |      |      |      |      |
| StringTerms.Bucket                                           |      |      |      |      |
|                                                              |      |      |      |      |
| StringTermsAggregatorFromFilters                             |      |      |      |      |
| Adapts a terms aggregation into a filters aggregation.       |      |      |      |      |
| Terms                                                        |      |      |      |      |
| A terms aggregation.                                         |      |      |      |      |
| Terms.Bucket                                                 |      |      |      |      |
| A bucket that is associated with a single term               |      |      |      |      |
| TermsAggregationBuilder                                      |      |      |      |      |
|                                                              |      |      |      |      |
| TermsAggregator                                              |      |      |      |      |
|                                                              |      |      |      |      |
| TermsAggregator.BucketCountThresholds                        |      |      |      |      |
|                                                              |      |      |      |      |
| TermsAggregatorFactory                                       |      |      |      |      |
|                                                              |      |      |      |      |
| TermsAggregatorFactory.ExecutionMode                         |      |      |      |      |
|                                                              |      |      |      |      |
| UnmappedRareTerms                                            |      |      |      |      |
| Result of the RareTerms aggregation when the field is unmapped. |      |      |      |      |
| UnmappedRareTerms.Bucket                                     |      |      |      |      |
|                                                              |      |      |      |      |
| UnmappedSignificantTerms                                     |      |      |      |      |
| Result of the running the significant terms aggregation on an unmapped field. |      |      |      |      |
| UnmappedSignificantTerms.Bucket                              |      |      |      |      |
| Concrete type that can't be built because Java needs a concrete type so InternalTerms.Bucket can have a self type but UnmappedTerms doesn't ever need to build it because it never returns any buckets. |      |      |      |      |
| UnmappedTerms                                                |      |      |      |      |
| Result of the TermsAggregator when the field is unmapped.    |      |      |      |      |
| UnmappedTerms.Bucket                                         |      |      |      |      |
| Concrete type that can't be built because Java needs a concrete type so InternalTerms.Bucket can have a self type but UnmappedTerms doesn't ever need to build it because it never returns any buckets. |      |      |      |      |





org.elasticsearch.search.aggregations.bucket.terms.heuristic

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ChiSquare                                                    |      |      |      |
|                                                              |      |      |      |
| ChiSquare.ChiSquareBuilder                                   |      |      |      |
|                                                              |      |      |      |
| GND                                                          |      |      |      |
|                                                              |      |      |      |
| GND.GNDBuilder                                               |      |      |      |
|                                                              |      |      |      |
| JLHScore                                                     |      |      |      |
|                                                              |      |      |      |
| JLHScore.JLHScoreBuilder                                     |      |      |      |
|                                                              |      |      |      |
| MutualInformation                                            |      |      |      |
|                                                              |      |      |      |
| MutualInformation.MutualInformationBuilder                   |      |      |      |
|                                                              |      |      |      |
| NXYSignificanceHeuristic                                     |      |      |      |
|                                                              |      |      |      |
| NXYSignificanceHeuristic.Frequencies                         |      |      |      |
|                                                              |      |      |      |
| NXYSignificanceHeuristic.NXYBuilder                          |      |      |      |
|                                                              |      |      |      |
| PercentageScore                                              |      |      |      |
|                                                              |      |      |      |
| PercentageScore.PercentageScoreBuilder                       |      |      |      |
|                                                              |      |      |      |
| ScriptHeuristic                                              |      |      |      |
|                                                              |      |      |      |
| SignificanceHeuristic                                        |      |      |      |
| Heuristic for that SignificantTerms uses to pick out significant terms. |      |      |      |
| SignificanceHeuristicBuilder                                 |      |      |      |







org.elasticsearch.search.aggregations.metrics



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AbstractHyperLogLog                                          |      |      |      |      |
| Hyperloglog counter, implemented based on pseudo code from http://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40671.pdf and its appendix https://docs.google.com/document/d/1gyjfMHy43U9OWBXxfaeG-3MjGzejW1dlpyMwEYAAWEI/view?fullscreen Trying to understand what this class does without having read the paper is considered adventurous. |      |      |      |      |
| AbstractHyperLogLog.RunLenIterator                           |      |      |      |      |
| Iterator over a HyperLogLog register                         |      |      |      |      |
| AbstractHyperLogLogPlusPlus                                  |      |      |      |      |
| Base class for HLL++ algorithms.                             |      |      |      |      |
| AbstractLinearCounting                                       |      |      |      |      |
| Linear counter, implemented based on pseudo code from http://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40671.pdf and its appendix https://docs.google.com/document/d/1gyjfMHy43U9OWBXxfaeG-3MjGzejW1dlpyMwEYAAWEI/view?fullscreen Trying to understand what this class does without having read the paper is considered adventurous. |      |      |      |      |
| AbstractLinearCounting.HashesIterator                        |      |      |      |      |
| Iterator over the hash values                                |      |      |      |      |
| AbstractPercentilesAggregationBuilder<T extends AbstractPercentilesAggregationBuilder<T>> |      |      |      |      |
| This provides a base class for aggregations that are building percentiles or percentiles-like functionality (e.g. |      |      |      |      |
| Avg                                                          |      |      |      |      |
| An aggregation that computes the average of the values in the current bucket. |      |      |      |      |
| AvgAggregationBuilder                                        |      |      |      |      |
|                                                              |      |      |      |      |
| Cardinality                                                  |      |      |      |      |
| An aggregation that computes approximate numbers of unique terms. |      |      |      |      |
| CardinalityAggregationBuilder                                |      |      |      |      |
|                                                              |      |      |      |      |
| CardinalityAggregator                                        |      |      |      |      |
| An aggregator that computes approximate counts of unique values. |      |      |      |      |
| CardinalityAggregatorSupplier                                |      |      |      |      |
|                                                              |      |      |      |      |
| CompensatedSum                                               |      |      |      |      |
| Used to calculate sums using the Kahan summation algorithm.  |      |      |      |      |
| ExtendedStats                                                |      |      |      |      |
| Statistics over a set of values (either aggregated over field data or scripts) |      |      |      |      |
| ExtendedStats.Bounds                                         |      |      |      |      |
|                                                              |      |      |      |      |
| ExtendedStatsAggregationBuilder                              |      |      |      |      |
|                                                              |      |      |      |      |
| ExtendedStatsAggregatorProvider                              |      |      |      |      |
|                                                              |      |      |      |      |
| GeoBounds                                                    |      |      |      |      |
| An aggregation that computes a bounding box in which all documents of the current bucket are. |      |      |      |      |
| GeoBoundsAggregationBuilder                                  |      |      |      |      |
|                                                              |      |      |      |      |
| GeoBoundsAggregatorSupplier                                  |      |      |      |      |
|                                                              |      |      |      |      |
| GeoCentroid                                                  |      |      |      |      |
| Interface for GeoCentroidAggregator                          |      |      |      |      |
| GeoCentroidAggregationBuilder                                |      |      |      |      |
|                                                              |      |      |      |      |
| GeoGridAggregatorSupplier                                    |      |      |      |      |
|                                                              |      |      |      |      |
| GlobalOrdCardinalityAggregator                               |      |      |      |      |
| An aggregator that computes approximate counts of unique values using global ords. |      |      |      |      |
| HyperLogLogPlusPlus                                          |      |      |      |      |
| Hyperloglog++ counter, implemented based on pseudo code from http://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40671.pdf and its appendix https://docs.google.com/document/d/1gyjfMHy43U9OWBXxfaeG-3MjGzejW1dlpyMwEYAAWEI/view?fullscreen This implementation is different from the original implementation in that it uses a hash table instead of a sorted list for linear counting. |      |      |      |      |
| InternalAvg                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalCardinality                                          |      |      |      |      |
|                                                              |      |      |      |      |
| InternalExtendedStats                                        |      |      |      |      |
|                                                              |      |      |      |      |
| InternalGeoBounds                                            |      |      |      |      |
|                                                              |      |      |      |      |
| InternalGeoCentroid                                          |      |      |      |      |
| Serialization and merge logic for GeoCentroidAggregator.     |      |      |      |      |
| InternalHDRPercentileRanks                                   |      |      |      |      |
|                                                              |      |      |      |      |
| InternalHDRPercentileRanks.Iter                              |      |      |      |      |
|                                                              |      |      |      |      |
| InternalHDRPercentiles                                       |      |      |      |      |
|                                                              |      |      |      |      |
| InternalHDRPercentiles.Iter                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMax                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMedianAbsoluteDeviation                              |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMin                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalMultiValueAggregation                                |      |      |      |      |
|                                                              |      |      |      |      |
| InternalNumericMetricsAggregation                            |      |      |      |      |
|                                                              |      |      |      |      |
| InternalNumericMetricsAggregation.MultiValue                 |      |      |      |      |
|                                                              |      |      |      |      |
| InternalNumericMetricsAggregation.SingleValue                |      |      |      |      |
|                                                              |      |      |      |      |
| InternalScriptedMetric                                       |      |      |      |      |
|                                                              |      |      |      |      |
| InternalStats                                                |      |      |      |      |
|                                                              |      |      |      |      |
| InternalSum                                                  |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTDigestPercentileRanks                               |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTDigestPercentileRanks.Iter                          |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTDigestPercentiles                                   |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTDigestPercentiles.Iter                              |      |      |      |      |
|                                                              |      |      |      |      |
| InternalTopHits                                              |      |      |      |      |
| Results of the TopHitsAggregator.                            |      |      |      |      |
| InternalValueCount                                           |      |      |      |      |
| An internal implementation of ValueCount.                    |      |      |      |      |
| InternalWeightedAvg                                          |      |      |      |      |
|                                                              |      |      |      |      |
| Max                                                          |      |      |      |      |
| An aggregation that computes the maximum of the values in the current bucket. |      |      |      |      |
| MaxAggregationBuilder                                        |      |      |      |      |
|                                                              |      |      |      |      |
| MedianAbsoluteDeviation                                      |      |      |      |      |
| An aggregation that approximates the median absolute deviation of a numeric field |      |      |      |      |
| MedianAbsoluteDeviationAggregationBuilder                    |      |      |      |      |
|                                                              |      |      |      |      |
| MedianAbsoluteDeviationAggregator                            |      |      |      |      |
|                                                              |      |      |      |      |
| MedianAbsoluteDeviationAggregatorFactory                     |      |      |      |      |
|                                                              |      |      |      |      |
| MedianAbsoluteDeviationAggregatorSupplier                    |      |      |      |      |
|                                                              |      |      |      |      |
| MetricAggregatorSupplier                                     |      |      |      |      |
|                                                              |      |      |      |      |
| MetricInspectionHelper                                       |      |      |      |      |
| Counterpart to AggregationInspectionHelper, providing helpers for some aggs that have package-private getters. |      |      |      |      |
| MetricsAggregator                                            |      |      |      |      |
|                                                              |      |      |      |      |
| Min                                                          |      |      |      |      |
| An aggregation that computes the minimum of the values in the current bucket. |      |      |      |      |
| MinAggregationBuilder                                        |      |      |      |      |
|                                                              |      |      |      |      |
| MinAggregator                                                |      |      |      |      |
|                                                              |      |      |      |      |
| MultiValueAggregation                                        |      |      |      |      |
|                                                              |      |      |      |      |
| NumericMetricsAggregation                                    |      |      |      |      |







org.elasticsearch.search.aggregations.pipeline



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractPipelineAggregationBuilder<PAB extends AbstractPipelineAggregationBuilder<PAB>> |      |      |      |
| Base implementation of a PipelineAggregationBuilder.         |      |      |      |
| AvgBucketPipelineAggregationBuilder                          |      |      |      |
|                                                              |      |      |      |
| AvgBucketPipelineAggregator                                  |      |      |      |
|                                                              |      |      |      |
| BucketHelpers                                                |      |      |      |
| A set of static helpers to simplify working with aggregation buckets, in particular providing utilities that help pipeline aggregations. |      |      |      |
| BucketHelpers.GapPolicy                                      |      |      |      |
| A gap policy determines how "holes" in a set of buckets should be handled. |      |      |      |
| BucketMetricsParser                                          |      |      |      |
| A parser for parsing requests for a BucketMetricsPipelineAggregator |      |      |      |
| BucketMetricsPipelineAggregationBuilder<AF extends BucketMetricsPipelineAggregationBuilder<AF>> |      |      |      |
|                                                              |      |      |      |
| BucketMetricsPipelineAggregator                              |      |      |      |
| A class of sibling pipeline aggregations which calculate metrics across the buckets of a sibling aggregation |      |      |      |
| BucketMetricValue                                            |      |      |      |
|                                                              |      |      |      |
| BucketScriptPipelineAggregationBuilder                       |      |      |      |
|                                                              |      |      |      |
| BucketScriptPipelineAggregator                               |      |      |      |
|                                                              |      |      |      |
| BucketSelectorPipelineAggregationBuilder                     |      |      |      |
|                                                              |      |      |      |
| BucketSelectorPipelineAggregator                             |      |      |      |
|                                                              |      |      |      |
| BucketSortPipelineAggregationBuilder                         |      |      |      |
| Builds a pipeline aggregation that allows sorting the buckets of its parent aggregation. |      |      |      |
| BucketSortPipelineAggregator                                 |      |      |      |
|                                                              |      |      |      |
| CumulativeSumPipelineAggregationBuilder                      |      |      |      |
|                                                              |      |      |      |
| CumulativeSumPipelineAggregator                              |      |      |      |
|                                                              |      |      |      |
| Derivative                                                   |      |      |      |
|                                                              |      |      |      |
| DerivativePipelineAggregationBuilder                         |      |      |      |
|                                                              |      |      |      |
| DerivativePipelineAggregator                                 |      |      |      |
|                                                              |      |      |      |
| EwmaModel                                                    |      |      |      |
| Calculate a exponentially weighted moving average            |      |      |      |
| EwmaModel.EWMAModelBuilder                                   |      |      |      |
|                                                              |      |      |      |
| ExtendedStatsBucket                                          |      |      |      |
| Extended Statistics over a set of buckets                    |      |      |      |
| ExtendedStatsBucketParser                                    |      |      |      |
|                                                              |      |      |      |
| ExtendedStatsBucketPipelineAggregationBuilder                |      |      |      |
|                                                              |      |      |      |
| ExtendedStatsBucketPipelineAggregator                        |      |      |      |
|                                                              |      |      |      |
| HoltLinearModel                                              |      |      |      |
| Calculate a doubly exponential weighted moving average       |      |      |      |
| HoltLinearModel.HoltLinearModelBuilder                       |      |      |      |
|                                                              |      |      |      |
| HoltWintersModel                                             |      |      |      |
| Calculate a triple exponential weighted moving average       |      |      |      |
| HoltWintersModel.HoltWintersModelBuilder                     |      |      |      |
|                                                              |      |      |      |
| HoltWintersModel.SeasonalityType                             |      |      |      |
|                                                              |      |      |      |
| InternalBucketMetricValue                                    |      |      |      |
|                                                              |      |      |      |
| InternalDerivative                                           |      |      |      |
|                                                              |      |      |      |
| InternalExtendedStatsBucket                                  |      |      |      |
|                                                              |      |      |      |
| InternalPercentilesBucket                                    |      |      |      |
|                                                              |      |      |      |
| InternalPercentilesBucket.Iter                               |      |      |      |
|                                                              |      |      |      |
| InternalSimpleValue                                          |      |      |      |
|                                                              |      |      |      |
| InternalStatsBucket                                          |      |      |      |
|                                                              |      |      |      |
| LinearModel                                                  |      |      |      |
| Calculate a linearly weighted moving average, such that older values are linearly less important. |      |      |      |
| LinearModel.LinearModelBuilder                               |      |      |      |
|                                                              |      |      |      |
| MaxBucketPipelineAggregationBuilder                          |      |      |      |
|                                                              |      |      |      |
| MaxBucketPipelineAggregator                                  |      |      |      |
|                                                              |      |      |      |
| MinBucketPipelineAggregationBuilder                          |      |      |      |
|                                                              |      |      |      |
| MinBucketPipelineAggregator                                  |      |      |      |
|                                                              |      |      |      |
| MovAvgModel                                                  |      |      |      |
|                                                              |      |      |      |
| MovAvgModel.AbstractModelParser                              |      |      |      |
| Abstract class which also provides some concrete parsing functionality. |      |      |      |
| MovAvgModelBuilder                                           |      |      |      |
| Represents the common interface that all moving average models share. |      |      |      |
| MovAvgPipelineAggregationBuilder                             |      |      |      |







org.elasticsearch.search.aggregations.support



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AggregationContext                                           |      |      |      |
| Everything used to build and execute aggregations and the data sources that power them. |      |      |      |
| AggregationContext.ProductionAggregationContext              |      |      |      |
| Implementation of AggregationContext for production usage that wraps our ubiquitous SearchExecutionContext and anything else specific to aggregations. |      |      |      |
| AggregationInfo                                              |      |      |      |
|                                                              |      |      |      |
| AggregationInspectionHelper                                  |      |      |      |
| Provides a set of static helpers to determine if a particular type of InternalAggregation "has a value" or not. |      |      |      |
| AggregationPath                                              |      |      |      |
| A path that can be used to sort/order buckets (in some multi-bucket aggregations, e.g. |      |      |      |
| AggregationPath.PathElement                                  |      |      |      |
|                                                              |      |      |      |
| AggregationUsageService                                      |      |      |      |
|                                                              |      |      |      |
| AggregationUsageService.Builder                              |      |      |      |
|                                                              |      |      |      |
| CoreValuesSourceType                                         |      |      |      |
| CoreValuesSourceType holds the ValuesSourceType implementations for the core aggregations package. |      |      |      |
| FieldContext                                                 |      |      |      |
| Used by all field data based aggregators.                    |      |      |      |
| MissingValues                                                |      |      |      |
| Utility class that allows to return views of ValuesSources that replace the missing value with a configured value. |      |      |      |
| MultiValuesSource<VS extends ValuesSource>                   |      |      |      |
| Class to encapsulate a set of ValuesSource objects labeled by field name |      |      |      |
| MultiValuesSource.NumericMultiValuesSource                   |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceAggregationBuilder<AB extends MultiValuesSourceAggregationBuilder<AB>> |      |      |      |
| Similar to ValuesSourceAggregationBuilder, except it references multiple ValuesSources (e.g. |      |      |      |
| MultiValuesSourceAggregationBuilder.LeafOnly<AB extends MultiValuesSourceAggregationBuilder<AB>> |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceAggregatorFactory                           |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceFieldConfig                                 |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceFieldConfig.Builder                         |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceFieldConfig.ParserBuilder                   |      |      |      |
|                                                              |      |      |      |
| MultiValuesSourceParseHelper                                 |      |      |      |
|                                                              |      |      |      |
| ValuesSource                                                 |      |      |      |
| A unified interface to different ways of getting input data for Aggregators like DocValues from Lucene or script output. |      |      |      |
| ValuesSource.Bytes                                           |      |      |      |
| ValuesSource for fields who's values are best thought of as byte arrays without any other meaning like keyword or ip. |      |      |      |
| ValuesSource.Bytes.FieldData                                 |      |      |      |
|                                                              |      |      |      |
| ValuesSource.Bytes.Script                                    |      |      |      |
| ValuesSource implementation for stand alone scripts returning a Bytes value |      |      |      |
| ValuesSource.Bytes.WithOrdinals                              |      |      |      |
| Specialization of ValuesSource.Bytes who's underlying storage de-duplicates its bytes by storing them in a per-leaf sorted lookup table. |      |      |      |
| ValuesSource.Bytes.WithOrdinals.FieldData                    |      |      |      |
|                                                              |      |      |      |
| ValuesSource.Bytes.WithScript                                |      |      |      |
| ValuesSource subclass for Bytes fields with a Value Script applied |      |      |      |
| ValuesSource.GeoPoint                                        |      |      |      |
| ValuesSource for fields who's values are best thought of as points on a globe. |      |      |      |
| ValuesSource.GeoPoint.Fielddata                              |      |      |      |
|                                                              |      |      |      |
| ValuesSource.Numeric                                         |      |      |      |
| ValuesSource for fields who's values are best thought of as numbers. |      |      |      |
| ValuesSource.Numeric.FieldData                               |      |      |      |
|                                                              |      |      |      |
| ValuesSource.Numeric.Script                                  |      |      |      |
| ValuesSource implementation for stand alone scripts returning a Numeric value |      |      |      |
| ValuesSource.Numeric.WithScript                              |      |      |      |
| ValuesSource subclass for Numeric fields with a Value Script applied |      |      |      |
| ValuesSource.Range                                           |      |      |      |
| ValuesSource for fields who's values are best thought of as ranges of numbers, dates, or IP addresses. |      |      |      |
| ValuesSourceAggregationBuilder<AB extends ValuesSourceAggregationBuilder<AB>> |      |      |      |
|                                                              |      |      |      |
| ValuesSourceAggregationBuilder.LeafOnly<VS extends ValuesSource,AB extends ValuesSourceAggregationBuilder<AB>> |      |      |      |
|                                                              |      |      |      |
| ValuesSourceAggregationBuilder.MetricsAggregationBuilder<VS extends ValuesSource,AB extends ValuesSourceAggregationBuilder<AB>> |      |      |      |
|                                                              |      |      |      |
| ValuesSourceAggregationBuilder.SingleMetricAggregationBuilder<VS extends ValuesSource,AB extends ValuesSourceAggregationBuilder<AB>> |      |      |      |
|                                                              |      |      |      |
| ValuesSourceAggregatorFactory                                |      |      |      |
|                                                              |      |      |      |
| ValuesSourceConfig                                           |      |      |      |
| A configuration that tells aggregations how to retrieve data from the index in order to run a specific aggregation. |      |      |      |
| ValuesSourceRegistry                                         |      |      |      |
| ValuesSourceRegistry holds the mapping from ValuesSourceTypes to functions for building aggregation components. |      |      |      |
| ValuesSourceRegistry.Builder                                 |      |      |      |
|                                                              |      |      |      |
| ValuesSourceRegistry.RegistryKey<T>                          |      |      |      |
|                                                              |      |      |      |
| ValuesSourceType                                             |      |      |      |
| ValuesSourceType represents a collection of fields that share a common set of operations, for example all numeric fields. |      |      |      |
| ValueType                                                    |      |      |      |







org.elasticsearch.search.aggregations.support.values



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ScriptBytesValues                                            |      |      |      |
| SortedBinaryDocValues implementation that reads values from a script. |      |      |      |
| ScriptDoubleValues                                           |      |      |      |
| SortingNumericDoubleValues implementation which is based on a script |      |      |      |
| ScriptLongValues                                             |      |      |      |
| LongValues implementation which is based on a script         |      |      |      |





org.elasticsearch.search.builder



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| PointInTimeBuilder                                           |      |      |      |
| A search request with a point in time will execute using the reader contexts associated with that point time instead of the latest reader contexts. |      |      |      |
| SearchSourceBuilder                                          |      |      |      |
| A search source builder allowing to easily build search source. |      |      |      |
| SearchSourceBuilder.IndexBoost                               |      |      |      |
|                                                              |      |      |      |
| SearchSourceBuilder.ScriptField                              |      |      |      |
|                                                              |      |      |      |
| SearchSourceBuilderException                                 |      |      |      |





org.elasticsearch.search.collapse



| Class                                                      |      |      |      |
| ---------------------------------------------------------- | ---- | ---- | ---- |
| Description                                                |      |      |      |
| CollapseBuilder                                            |      |      |      |
| A builder that enables field collapsing on search request. |      |      |      |
| CollapseContext                                            |      |      |      |
| Context used for field collapsing                          |      |      |      |







org.elasticsearch.search.dfs



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AggregatedDfs                                                |      |      |      |
|                                                              |      |      |      |
| DfsPhase                                                     |      |      |      |
| Dfs phase of a search request, used to make scoring 100% accurate by collecting additional info from each shard before the query phase. |      |      |      |
| DfsPhaseExecutionException                                   |      |      |      |
|                                                              |      |      |      |
| DfsSearchResult                                              |      |      |      |





org.elasticsearch.search.fetch



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| FetchContext                                                 |      |      |      |
| Encapsulates state required to execute fetch phases          |      |      |      |
| FetchPhase                                                   |      |      |      |
| Fetch phase of a search request, used to fetch the actual top matching documents to be returned to the client, identified after reducing all of the matches returned by the query phase |      |      |      |
| FetchPhaseExecutionException                                 |      |      |      |
|                                                              |      |      |      |
| FetchProfiler                                                |      |      |      |
|                                                              |      |      |      |
| FetchSearchResult                                            |      |      |      |
|                                                              |      |      |      |
| FetchSubPhase                                                |      |      |      |
| Sub phase within the fetch phase used to fetch things *about* the documents like highlighting or matched queries. |      |      |      |
| FetchSubPhase.HitContext                                     |      |      |      |
|                                                              |      |      |      |
| FetchSubPhaseProcessor                                       |      |      |      |
| Executes the logic for a FetchSubPhase against a particular leaf reader and hit |      |      |      |
| QueryFetchSearchResult                                       |      |      |      |
|                                                              |      |      |      |
| ScrollQueryFetchSearchResult                                 |      |      |      |
|                                                              |      |      |      |
| ShardFetchRequest                                            |      |      |      |
| Shard level fetch base request.                              |      |      |      |
| ShardFetchSearchRequest                                      |      |      |      |
| Shard level fetch request used with search.                  |      |      |      |
| StoredFieldsContext                                          |      |      |      |
| Context used to fetch the stored_fields.                     |      |      |      |







org.elasticsearch.search.fetch.subphase



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ExplainPhase                                                 |      |      |      |
| Explains the scoring calculations for the top hits.          |      |      |      |
| FetchDocValuesContext                                        |      |      |      |
| All the required context to pull a field from the doc values. |      |      |      |
| FetchDocValuesPhase                                          |      |      |      |
| Fetch sub phase which pulls data from doc values.            |      |      |      |
| FetchFieldsContext                                           |      |      |      |
| The context needed to retrieve fields.                       |      |      |      |
| FetchFieldsPhase                                             |      |      |      |
| A fetch sub-phase for high-level field retrieval.            |      |      |      |
| FetchScorePhase                                              |      |      |      |
|                                                              |      |      |      |
| FetchSourceContext                                           |      |      |      |
| Context used to fetch the _source.                           |      |      |      |
| FetchSourcePhase                                             |      |      |      |
|                                                              |      |      |      |
| FetchVersionPhase                                            |      |      |      |
|                                                              |      |      |      |
| FieldAndFormat                                               |      |      |      |
| Wrapper around a field name and the format that should be used to display values of this field. |      |      |      |
| FieldFetcher                                                 |      |      |      |
| A helper class to FetchFieldsPhase that's initialized with a list of field patterns to fetch. |      |      |      |
| InnerHitsContext                                             |      |      |      |
| Context used for inner hits retrieval                        |      |      |      |
| InnerHitsContext.InnerHitSubContext                          |      |      |      |
| A SubSearchContext that associates TopDocs to each SearchHit in the parent search context |      |      |      |
| InnerHitsPhase                                               |      |      |      |
|                                                              |      |      |      |
| MatchedQueriesPhase                                          |      |      |      |
|                                                              |      |      |      |
| ScriptFieldsContext                                          |      |      |      |
|                                                              |      |      |      |
| ScriptFieldsContext.ScriptField                              |      |      |      |
|                                                              |      |      |      |
| ScriptFieldsPhase                                            |      |      |      |
|                                                              |      |      |      |
| SeqNoPrimaryTermPhase                                        |      |      |      |
|                                                              |      |      |      |
| UnmappedFieldFetcher                                         |      |      |      |
| Class to fetch all unmapped fields from a Source that match a set of patterns Takes a set of mapped fields to ignore when matching, which should include any nested mappers. |      |      |      |





org.elasticsearch.search.fetch.subphase.highlight



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractHighlighterBuilder<HB extends AbstractHighlighterBuilder<?>> |      |      |      |
| This abstract class holds parameters shared by HighlightBuilder and HighlightBuilder.Field and provides the common setters, equality, hashCode calculation and common serialization |      |      |      |
| CustomQueryScorer                                            |      |      |      |
|                                                              |      |      |      |
| FastVectorHighlighter                                        |      |      |      |
|                                                              |      |      |      |
| FieldHighlightContext                                        |      |      |      |
|                                                              |      |      |      |
| FragmentBuilderHelper                                        |      |      |      |
| Simple helper class for FastVectorHighlighter FragmentsBuilder implementations. |      |      |      |
| HighlightBuilder                                             |      |      |      |
| A builder for search highlighting.                           |      |      |      |
| HighlightBuilder.BoundaryScannerType                         |      |      |      |
|                                                              |      |      |      |
| HighlightBuilder.Field                                       |      |      |      |
|                                                              |      |      |      |
| HighlightBuilder.Order                                       |      |      |      |
|                                                              |      |      |      |
| Highlighter                                                  |      |      |      |
| Highlights a search result.                                  |      |      |      |
| HighlightField                                               |      |      |      |
| A field highlighted with its highlighted fragments.          |      |      |      |
| HighlightPhase                                               |      |      |      |
|                                                              |      |      |      |
| HighlightUtils                                               |      |      |      |
|                                                              |      |      |      |
| HighlightUtils.Encoders                                      |      |      |      |
|                                                              |      |      |      |
| LimitTokenOffsetAnalyzer                                     |      |      |      |
| This analyzer limits the highlighting once it sees a token with a start offset <= the configured limit, which won't pass and will end the stream. |      |      |      |
| PlainHighlighter                                             |      |      |      |
|                                                              |      |      |      |
| SearchHighlightContext                                       |      |      |      |
|                                                              |      |      |      |
| SearchHighlightContext.Field                                 |      |      |      |
|                                                              |      |      |      |
| SearchHighlightContext.FieldOptions                          |      |      |      |
|                                                              |      |      |      |
| SimpleFragmentsBuilder                                       |      |      |      |
| Direct Subclass of Lucene's org.apache.lucene.search.vectorhighlight.SimpleFragmentsBuilder that corrects offsets for broken analysis chains. |      |      |      |
| SourceScoreOrderFragmentsBuilder                             |      |      |      |
|                                                              |      |      |      |
| SourceSimpleFragmentsBuilder                                 |      |      |      |
|                                                              |      |      |      |
| UnifiedHighlighter                                           |      |      |      |





org.elasticsearch.search.internal



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AliasFilter                                                  |      |      |      |
| Represents a QueryBuilder and a list of alias names that filters the builder is composed of. |      |      |      |
| ContextIndexSearcher                                         |      |      |      |
| Context-aware extension of IndexSearcher.                    |      |      |      |
| FieldUsageTrackingDirectoryReader                            |      |      |      |
| Wraps a DirectoryReader and tracks all access to fields, notifying a FieldUsageTrackingDirectoryReader.FieldUsageNotifier upon access. |      |      |      |
| FieldUsageTrackingDirectoryReader.FieldUsageNotifier         |      |      |      |
|                                                              |      |      |      |
| FilteredSearchContext                                        |      |      |      |
|                                                              |      |      |      |
| FilterFieldNamesProvidingStoredFieldsVisitor                 |      |      |      |
|                                                              |      |      |      |
| FilterStoredFieldVisitor                                     |      |      |      |
|                                                              |      |      |      |
| InternalScrollSearchRequest                                  |      |      |      |
|                                                              |      |      |      |
| InternalSearchResponse                                       |      |      |      |
| SearchResponseSections subclass that can be serialized over the wire. |      |      |      |
| LegacyReaderContext                                          |      |      |      |
|                                                              |      |      |      |
| ReaderContext                                                |      |      |      |
| Holds a reference to a point in time Engine.Searcher that will be used to construct SearchContext. |      |      |      |
| ScrollContext                                                |      |      |      |
| Wrapper around information that needs to stay around when scrolling. |      |      |      |
| SearchContext                                                |      |      |      |
| This class encapsulates the state needed to execute a search. |      |      |      |
| ShardSearchContextId                                         |      |      |      |
|                                                              |      |      |      |
| ShardSearchRequest                                           |      |      |      |
| Shard level request that represents a search.                |      |      |      |
| SubSearchContext                                             |      |      |      |







org.elasticsearch.search.lookup



| Class                                  |      |      |      |
| -------------------------------------- | ---- | ---- | ---- |
| Description                            |      |      |      |
| FieldLookup                            |      |      |      |
|                                        |      |      |      |
| FieldValues<T>                         |      |      |      |
| Represents values for a given document |      |      |      |
| LeafDocLookup                          |      |      |      |
|                                        |      |      |      |
| LeafSearchLookup                       |      |      |      |
| Per-segment version of SearchLookup.   |      |      |      |
| LeafStoredFieldsLookup                 |      |      |      |
|                                        |      |      |      |
| SearchLookup                           |      |      |      |
|                                        |      |      |      |
| SourceLookup                           |      |      |      |





org.elasticsearch.search.profile



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractInternalProfileTree<PB extends聽AbstractProfileBreakdown<?>,E> |      |      |      |
| 聽                                                           |      |      |      |
| AbstractProfileBreakdown<T extends聽Enum<T>>                 |      |      |      |
| A record of timings for the various operations that may happen during query execution. |      |      |      |
| AbstractProfiler<PB extends聽AbstractProfileBreakdown<?>,E>  |      |      |      |
| 聽                                                           |      |      |      |
| ProfileResult                                                |      |      |      |
| The result of a profiled *thing*, like a query or an aggregation. |      |      |      |
| Profilers                                                    |      |      |      |
| Wrapper around all the profilers that makes management easier. |      |      |      |
| SearchProfileQueryPhaseResult                                |      |      |      |
| Profile results from a shard for the search phase.           |      |      |      |
| SearchProfileResults                                         |      |      |      |
| Profile results for all shards.                              |      |      |      |
| SearchProfileResultsBuilder                                  |      |      |      |
| Profile results for the query phase run on all shards.       |      |      |      |
| SearchProfileShardResult                                     |      |      |      |
| Profile results from a particular shard for all search phases. |      |      |      |
| Timer                                                        |      |      |      |
| Helps measure how much time is spent running some methods.   |      |      |      |





org.elasticsearch.search.profile.aggregation



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AggregationProfileBreakdown                                  |      |      |      |
| AbstractProfileBreakdown customized to work with aggregations. |      |      |      |
| AggregationProfiler                                          |      |      |      |
|                                                              |      |      |      |
| AggregationProfileShardResult                                |      |      |      |
| A container class to hold the profile results for a single shard in the request. |      |      |      |
| AggregationTimingType                                        |      |      |      |
|                                                              |      |      |      |
| InternalAggregationProfileTree                               |      |      |      |
|                                                              |      |      |      |
| ProfilingAggregator                                          |      |      |      |
|                                                              |      |      |      |
| ProfilingLeafBucketCollector                                 |      |      |      |







org.elasticsearch.search.profile.query





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CollectorResult                                              |      |      |      |
| Public interface and serialization container for profiled timings of the Collectors used in the search. |      |      |      |
| InternalProfileCollector                                     |      |      |      |
| This class wraps a Lucene Collector and times the execution of: - setScorer() - collect() - doSetNextReader() - needsScores() InternalProfiler facilitates the linking of the Collector graph |      |      |      |
| ProfileWeight                                                |      |      |      |
| Weight wrapper that will compute how much time it takes to build the Scorer and then return a Scorer that is wrapped in order to compute timings as well. |      |      |      |
| QueryProfileBreakdown                                        |      |      |      |
| A record of timings for the various operations that may happen during query execution. |      |      |      |
| QueryProfiler                                                |      |      |      |
| This class acts as a thread-local storage for profiling a query. |      |      |      |
| QueryProfileShardResult                                      |      |      |      |
| A container class to hold the profile results for a single shard in the request. |      |      |      |
| QueryTimingType                                              |      |      |      |





org.elasticsearch.search.query

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| EarlyTerminatingCollector                                    |      |      |      |
| A Collector that early terminates collection after maxCountHits docs have been collected. |      |      |      |
| QueryPhase                                                   |      |      |      |
| Query phase of a search request, used to run the query and get back from each shard information about the matching documents (document ids and score or sort criteria) so that matches can be reduced on the coordinating node |      |      |      |
| QueryPhaseExecutionException                                 |      |      |      |
|                                                              |      |      |      |
| QuerySearchRequest                                           |      |      |      |
|                                                              |      |      |      |
| QuerySearchResult                                            |      |      |      |
|                                                              |      |      |      |
| ScrollQuerySearchResult                                      |      |      |      |







org.elasticsearch.search.rescore

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| QueryRescoreMode                                             |      |      |      |
|                                                              |      |      |      |
| QueryRescorer                                                |      |      |      |
|                                                              |      |      |      |
| QueryRescorer.QueryRescoreContext                            |      |      |      |
|                                                              |      |      |      |
| QueryRescorerBuilder                                         |      |      |      |
|                                                              |      |      |      |
| RescoreContext                                               |      |      |      |
| Context available to the rescore while it is running.        |      |      |      |
| RescorePhase                                                 |      |      |      |
| Rescore phase of a search request, used to run potentially expensive scoring models against the top matching documents. |      |      |      |
| Rescorer                                                     |      |      |      |
| A query rescorer interface used to re-rank the Top-K results of a previously executed search. |      |      |      |
| RescorerBuilder<RB extends RescorerBuilder<RB>>              |      |      |      |
| The abstract base builder for instances of RescorerBuilder.  |      |      |      |



org.elasticsearch.search.runtime



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractScriptFieldQuery<S extends AbstractFieldScript>      |      |      |      |
| Abstract base class for building queries based on script fields. |      |      |      |
| AbstractStringScriptFieldAutomatonQuery                      |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldExistsQuery                                |      |      |      |
|                                                              |      |      |      |
| BooleanScriptFieldTermQuery                                  |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldExistsQuery                                 |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldRangeQuery                                  |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldTermQuery                                   |      |      |      |
|                                                              |      |      |      |
| DoubleScriptFieldTermsQuery                                  |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldDistanceFeatureQuery                      |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldExistsQuery                               |      |      |      |
|                                                              |      |      |      |
| GeoPointScriptFieldGeoShapeQuery                             |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldExistsQuery                                     |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldRangeQuery                                      |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldTermQuery                                       |      |      |      |
|                                                              |      |      |      |
| IpScriptFieldTermsQuery                                      |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldDistanceFeatureQuery                          |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldExistsQuery                                   |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldRangeQuery                                    |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldTermQuery                                     |      |      |      |
|                                                              |      |      |      |
| LongScriptFieldTermsQuery                                    |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldExistsQuery                                 |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldFuzzyQuery                                  |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldPrefixQuery                                 |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldRangeQuery                                  |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldRegexpQuery                                 |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldTermQuery                                   |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldTermsQuery                                  |      |      |      |
|                                                              |      |      |      |
| StringScriptFieldWildcardQuery                               |      |      |      |





org.elasticsearch.search.searchafter







| Class              |      |      |
| ------------------ | ---- | ---- |
| Description        |      |      |
| SearchAfterBuilder |      |      |





org.elasticsearch.search.slice



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| DocIdSliceQuery                                              |      |      |      |
| A SliceQuery that partitions documents based on their Lucene ID. |      |      |      |
| DocValuesSliceQuery                                          |      |      |      |
| A SliceQuery that uses the numeric doc values of a field to do the slicing. |      |      |      |
| SliceBuilder                                                 |      |      |      |
| A slice builder allowing to split a scroll in multiple partitions. |      |      |      |
| SliceQuery                                                   |      |      |      |
| An abstract Query that defines an hash function to partition the documents in multiple slices. |      |      |      |
| TermsSliceQuery                                              |      |      |      |
| A SliceQuery that uses the terms dictionary of a field to do the slicing. |      |      |      |







org.elasticsearch.search.sort

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| BucketedSort                                                 |      |      |      |
| Type specialized sort implementations designed for use in aggregations. |      |      |      |
| BucketedSort.ExtraData                                       |      |      |      |
| Callbacks for storing extra data along with competitive sorts. |      |      |      |
| BucketedSort.ExtraData.Loader                                |      |      |      |
|                                                              |      |      |      |
| BucketedSort.ForDoubles                                      |      |      |      |
| Superclass for implementations of BucketedSort for double keys. |      |      |      |
| BucketedSort.ForFloats                                       |      |      |      |
| Superclass for implementations of BucketedSort for float keys. |      |      |      |
| BucketedSort.ForLongs                                        |      |      |      |
| Superclass for implementations of BucketedSort for long keys. |      |      |      |
| BucketedSort.ResultBuilder<T>                                |      |      |      |
| Used with BucketedSort.getValues(long, ResultBuilder) to build results from the sorting operation. |      |      |      |
| FieldSortBuilder                                             |      |      |      |
| A sort builder to sort based on a document field.            |      |      |      |
| GeoDistanceSortBuilder                                       |      |      |      |
| A geo distance based sorting on a geo point like field.      |      |      |      |
| MinAndMax<T extends Comparable<? super T>>                   |      |      |      |
| A class that encapsulates a minimum and a maximum, that are of the same type and Comparable. |      |      |      |
| NestedSortBuilder                                            |      |      |      |
|                                                              |      |      |      |
| ScoreSortBuilder                                             |      |      |      |
| A sort builder allowing to sort by score.                    |      |      |      |
| ScriptSortBuilder                                            |      |      |      |
| Script sort builder allows to sort based on a custom script expression. |      |      |      |
| ScriptSortBuilder.ScriptSortType                             |      |      |      |
|                                                              |      |      |      |
| ShardDocSortField                                            |      |      |      |
| A SortField that first compares the shard index and then uses the document number (_doc) to tiebreak if the value is the same. |      |      |      |
| SortAndFormats                                               |      |      |      |
|                                                              |      |      |      |
| SortBuilder<T extends SortBuilder<T>>                        |      |      |      |
|                                                              |      |      |      |
| SortBuilders                                                 |      |      |      |
| A set of static factory methods for SortBuilders.            |      |      |      |
| SortFieldAndFormat                                           |      |      |      |
|                                                              |      |      |      |
| SortMode                                                     |      |      |      |
| Elasticsearch supports sorting by array or multi-valued fields. |      |      |      |
| SortOrder                                                    |      |      |      |
| A sorting order.                                             |      |      |      |
| SortValue                                                    |      |      |      |
| A Comparable, DocValueFormat aware wrapper around a sort value. |      |      |      |







org.elasticsearch.search.suggest



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| DirectSpellcheckerSettings                                   |      |      |      |
|                                                              |      |      |      |
| SortBy                                                       |      |      |      |
| An enum representing the valid sorting options               |      |      |      |
| Suggest                                                      |      |      |      |
| Top level suggest result, containing the result for each suggestion. |      |      |      |
| Suggest.Suggestion<T extends Suggest.Suggestion.Entry>       |      |      |      |
| The suggestion responses corresponding with the suggestions in the request. |      |      |      |
| Suggest.Suggestion.Entry<O extends Suggest.Suggestion.Entry.Option> |      |      |      |
| Represents a part from the suggest text with suggested options. |      |      |      |
| Suggest.Suggestion.Entry.Option                              |      |      |      |
| Contains the suggested text with its document frequency and score. |      |      |      |
| SuggestBuilder                                               |      |      |      |
| Defines how to perform suggesting.                           |      |      |      |
| SuggestBuilders                                              |      |      |      |
| A static factory for building suggester lookup queries       |      |      |      |
| Suggester<T extends SuggestionSearchContext.SuggestionContext> |      |      |      |
|                                                              |      |      |      |
| SuggestionBuilder<T extends SuggestionBuilder<T>>            |      |      |      |
| Base class for the different suggestion implementations.     |      |      |      |
| SuggestionSearchContext                                      |      |      |      |
|                                                              |      |      |      |
| SuggestionSearchContext.SuggestionContext                    |      |      |      |
|                                                              |      |      |      |
| SuggestPhase                                                 |      |      |      |
| Suggest phase of a search request, used to collect suggestions |      |      |      |



org.elasticsearch.search.suggest.completion



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CompletionStats                                              |      |      |      |
|                                                              |      |      |      |
| CompletionSuggester                                          |      |      |      |
|                                                              |      |      |      |
| CompletionSuggestion                                         |      |      |      |
| Suggestion response for CompletionSuggester results Response format for each entry: { "text" : STRING "score" : FLOAT "contexts" : CONTEXTS } CONTEXTS : { "CONTEXT_NAME" : ARRAY, .. |      |      |      |
| CompletionSuggestion.Entry                                   |      |      |      |
|                                                              |      |      |      |
| CompletionSuggestion.Entry.Option                            |      |      |      |
|                                                              |      |      |      |
| CompletionSuggestionBuilder                                  |      |      |      |
| Defines a suggest command based on a prefix, typically to provide "auto-complete" functionality for users as they type search terms. |      |      |      |
| CompletionSuggestionContext                                  |      |      |      |
|                                                              |      |      |      |
| FuzzyOptions                                                 |      |      |      |
| Fuzzy options for completion suggester                       |      |      |      |
| FuzzyOptions.Builder                                         |      |      |      |
| Options for fuzzy queries                                    |      |      |      |
| RegexOptions                                                 |      |      |      |
| Regular expression options for completion suggester          |      |      |      |
| RegexOptions.Builder                                         |      |      |      |
| Options for regular expression queries                       |      |      |      |







org.elasticsearch.search.suggest.completion.context



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CategoryContextMapping                                       |      |      |      |
| A ContextMapping that uses a simple string as a criteria The suggestions are boosted and/or filtered by their associated category (string) value. |      |      |      |
| CategoryContextMapping.Builder                               |      |      |      |
| Builder for CategoryContextMapping                           |      |      |      |
| CategoryQueryContext                                         |      |      |      |
| Defines the query context for CategoryContextMapping         |      |      |      |
| CategoryQueryContext.Builder                                 |      |      |      |
|                                                              |      |      |      |
| ContextBuilder<E extends ContextMapping<?>>                  |      |      |      |
| Builder for ContextMapping                                   |      |      |      |
| ContextMapping<T extends ToXContent>                         |      |      |      |
| A ContextMapping defines criteria that can be used to filter and/or boost suggestions at query time for CompletionFieldMapper. |      |      |      |
| ContextMapping.InternalQueryContext                          |      |      |      |
|                                                              |      |      |      |
| ContextMapping.Type                                          |      |      |      |
|                                                              |      |      |      |
| ContextMappings                                              |      |      |      |
| ContextMappings indexes context-enabled suggestion fields and creates context queries for defined ContextMappings for a CompletionFieldMapper |      |      |      |
| GeoContextMapping                                            |      |      |      |
| A ContextMapping that uses a geo location/area as a criteria. |      |      |      |
| GeoContextMapping.Builder                                    |      |      |      |
|                                                              |      |      |      |
| GeoQueryContext                                              |      |      |      |
| Defines the query context for GeoContextMapping              |      |      |      |
| GeoQueryContext.Builder                                      |      |      |      |







org.elasticsearch.search.suggest.phrase



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| CandidateGenerator                                           |      |      |      |      |
|                                                              |      |      |      |      |
| Correction                                                   |      |      |      |      |
|                                                              |      |      |      |      |
| DirectCandidateGenerator                                     |      |      |      |      |
|                                                              |      |      |      |      |
| DirectCandidateGenerator.Candidate                           |      |      |      |      |
|                                                              |      |      |      |      |
| DirectCandidateGenerator.CandidateSet                        |      |      |      |      |
|                                                              |      |      |      |      |
| DirectCandidateGenerator.TokenConsumer                       |      |      |      |      |
|                                                              |      |      |      |      |
| DirectCandidateGeneratorBuilder                              |      |      |      |      |
|                                                              |      |      |      |      |
| Laplace                                                      |      |      |      |      |
| An additive smoothing model.                                 |      |      |      |      |
| LinearInterpolatingScorer                                    |      |      |      |      |
|                                                              |      |      |      |      |
| LinearInterpolation                                          |      |      |      |      |
| Linear interpolation smoothing model.                        |      |      |      |      |
| MultiCandidateGeneratorWrapper                               |      |      |      |      |
|                                                              |      |      |      |      |
| PhraseSuggester                                              |      |      |      |      |
|                                                              |      |      |      |      |
| PhraseSuggestion                                             |      |      |      |      |
| Suggestion entry returned from the PhraseSuggester.          |      |      |      |      |
| PhraseSuggestion.Entry                                       |      |      |      |      |
|                                                              |      |      |      |      |
| PhraseSuggestion.Entry.Option                                |      |      |      |      |
|                                                              |      |      |      |      |
| PhraseSuggestionBuilder                                      |      |      |      |      |
| Defines the actual suggest command for phrase suggestions ( phrase). |      |      |      |      |
| PhraseSuggestionBuilder.CandidateGenerator                   |      |      |      |      |
| PhraseSuggestionBuilder.CandidateGenerator interface.        |      |      |      |      |
| SmoothingModel                                               |      |      |      |      |
|                                                              |      |      |      |      |
| StupidBackoff                                                |      |      |      |      |
| A "stupid-backoff" smoothing model similar to Katz's Backoff. |      |      |      |      |
| WordScorer                                                   |      |      |      |      |
|                                                              |      |      |      |      |
| WordScorer.WordScorerFactory                                 |      |      |      |      |





org.elasticsearch.search.suggest.term

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| TermSuggester                                                |      |      |      |
|                                                              |      |      |      |
| TermSuggestion                                               |      |      |      |
| The suggestion responses corresponding with the suggestions in the request. |      |      |      |
| TermSuggestion.Entry                                         |      |      |      |
| Represents a part from the suggest text with suggested options. |      |      |      |
| TermSuggestion.Entry.Option                                  |      |      |      |
| Contains the suggested text with its document frequency and score. |      |      |      |
| TermSuggestion.Frequency                                     |      |      |      |
|                                                              |      |      |      |
| TermSuggestion.Score                                         |      |      |      |
|                                                              |      |      |      |
| TermSuggestionBuilder                                        |      |      |      |
| Defines the actual suggest command.                          |      |      |      |
| TermSuggestionBuilder.StringDistanceImpl                     |      |      |      |
| An enum representing the valid string edit distance algorithms for determining suggestions. |      |      |      |
| TermSuggestionBuilder.SuggestMode                            |      |      |      |
| An enum representing the valid suggest modes.                |      |      |      |

org.elasticsearch.shutdown

| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| PluginShutdownService                                        |      |      |
| The PluginShutdownService is used for the node shutdown infrastructure to signal to plugins that a shutdown is occurring, and to check whether it is safe to shut down. |      |      |



org.elasticsearch.snapshots



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbortedSnapshotException                                     |      |      |      |
|                                                              |      |      |      |
| ConcurrentSnapshotExecutionException                         |      |      |      |
| Thrown when a user tries to multiple conflicting snapshot/restore operations at the same time. |      |      |      |
| EmptySnapshotsInfoService                                    |      |      |      |
|                                                              |      |      |      |
| InFlightShardSnapshotStates                                  |      |      |      |
| Holds information about currently in-flight shard level snapshot or clone operations on a per-shard level. |      |      |      |
| InternalSnapshotsInfoService                                 |      |      |      |
|                                                              |      |      |      |
| InternalSnapshotsInfoService.SnapshotShard                   |      |      |      |
|                                                              |      |      |      |
| InvalidSnapshotNameException                                 |      |      |      |
| Thrown on the attempt to create a snapshot with invalid name |      |      |      |
| RestoreInfo                                                  |      |      |      |
| Information about successfully completed restore operation.  |      |      |      |
| RestoreService                                               |      |      |      |
| Service responsible for restoring snapshots                  |      |      |      |
| RestoreService.RestoreCompletionResponse                     |      |      |      |
|                                                              |      |      |      |
| RestoreService.RestoreInProgressUpdater                      |      |      |      |
|                                                              |      |      |      |
| SearchableSnapshotsSettings                                  |      |      |      |
|                                                              |      |      |      |
| Snapshot                                                     |      |      |      |
| Basic information about a snapshot - a SnapshotId and the repository that the snapshot belongs to. |      |      |      |
| SnapshotCreationException                                    |      |      |      |
| Deprecated.                                                  |      |      |      |
| This exception isn't thrown anymore.                         |      |      |      |
| SnapshotException                                            |      |      |      |
| Generic snapshot exception                                   |      |      |      |
| SnapshotFeatureInfo                                          |      |      |      |
|                                                              |      |      |      |
| SnapshotId                                                   |      |      |      |
| SnapshotId - snapshot name + snapshot UUID                   |      |      |      |
| SnapshotInfo                                                 |      |      |      |
| Information about a snapshot                                 |      |      |      |
| SnapshotInfo.IndexSnapshotDetails                            |      |      |      |
|                                                              |      |      |      |
| SnapshotInfo.SnapshotInfoBuilder                             |      |      |      |
|                                                              |      |      |      |
| SnapshotInProgressException                                  |      |      |      |
| Thrown on the attempt to execute an action that requires that no snapshot is in progress. |      |      |      |
| SnapshotMissingException                                     |      |      |      |
| Thrown if requested snapshot doesn't exist                   |      |      |      |
| SnapshotRestoreException                                     |      |      |      |
| Snapshot restore exception                                   |      |      |      |
| SnapshotShardFailure                                         |      |      |      |
| Stores information about failures that occurred during shard snapshotting process |      |      |      |
| SnapshotShardSizeInfo                                        |      |      |      |
|                                                              |      |      |      |
| SnapshotShardsService                                        |      |      |      |
| This service runs on data nodes and controls currently running shard snapshots on these nodes. |      |      |      |
| SnapshotsInfoService                                         |      |      |      |
|                                                              |      |      |      |
| SnapshotsService                                             |      |      |      |
| Service responsible for creating snapshots.                  |      |      |      |
| SnapshotState                                                |      |      |      |
| Represents the state that a snapshot can be in               |      |      |      |
| SnapshotUtils                                                |      |      |      |
| Snapshot utilities                                           |      |      |      |
| UpdateIndexShardSnapshotStatusRequest                        |      |      |      |
| Internal request that is used to send changes in snapshot status to master |      |      |      |







org.elasticsearch.tasks



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CancellableTask                                              |      |      |      |
| A task that can be cancelled                                 |      |      |      |
| CancellableTask.CancellationListener                         |      |      |      |
| This interface is implemented by any class that needs to react to the cancellation of this task. |      |      |      |
| CancellableTasksTracker<T>                                   |      |      |      |
| Tracks items that are associated with cancellable tasks, supporting efficient lookup by task ID and by parent task ID |      |      |      |
| LoggingTaskListener<Response>                                |      |      |      |
| A TaskListener that just logs the response at the info level. |      |      |      |
| RawTaskStatus                                                |      |      |      |
| Raw, unparsed status from the task results index.            |      |      |      |
| Task                                                         |      |      |      |
| Current task information                                     |      |      |      |
| Task.Status                                                  |      |      |      |
| Report of the internal status of a task.                     |      |      |      |
| TaskAwareRequest                                             |      |      |      |
| An interface for a request that can be used to register a task manager task |      |      |      |
| TaskCancellationService                                      |      |      |      |
| 聽                                                           |      |      |      |
| TaskCancelledException                                       |      |      |      |
| A generic exception that can be thrown by a task when it's cancelled by the task manager API |      |      |      |
| TaskId                                                       |      |      |      |
| Task id that consists of node id and id of the task on the node |      |      |      |
| TaskInfo                                                     |      |      |      |
| Information about a currently running task.                  |      |      |      |
| TaskListener<Response>                                       |      |      |      |
| Listener for Task success or failure.                        |      |      |      |
| TaskManager                                                  |      |      |      |
| Task Manager service for keeping track of currently running tasks on the nodes |      |      |      |
| TaskResult                                                   |      |      |      |
| Information about a running task or a task that stored its result. |      |      |      |
| TaskResultsService                                           |      |      |      |
| Service that can store task results.                         |      |      |      |





org.elasticsearch.threadpool



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AutoQueueAdjustingExecutorBuilder                            |      |      |      |
| A builder for executors that automatically adjust the queue length as needed, depending on Little's Law. |      |      |      |
| ExecutorBuilder<U extends org.elasticsearch.threadpool.ExecutorBuilder.ExecutorSettings> |      |      |      |
| Base class for executor builders.                            |      |      |      |
| FixedExecutorBuilder                                         |      |      |      |
| A builder for fixed executors.                               |      |      |      |
| ScalingExecutorBuilder                                       |      |      |      |
| A builder for scaling executors.                             |      |      |      |
| Scheduler                                                    |      |      |      |
| Scheduler that allows to schedule one-shot and periodic commands. |      |      |      |
| Scheduler.Cancellable                                        |      |      |      |
| This interface represents an object whose execution may be cancelled during runtime. |      |      |      |
| Scheduler.ReschedulingRunnable                               |      |      |      |
| This class encapsulates the scheduling of a Runnable that needs to be repeated on a interval. |      |      |      |
| Scheduler.SafeScheduledThreadPoolExecutor                    |      |      |      |
| This subclass ensures to properly bubble up Throwable instances of both type Error and Exception thrown in submitted/scheduled tasks to the uncaught exception handler |      |      |      |
| Scheduler.ScheduledCancellable                               |      |      |      |
| A scheduled cancellable allow cancelling and reading the remaining delay of a scheduled task. |      |      |      |
| ThreadPool                                                   |      |      |      |
|                                                              |      |      |      |
| ThreadPool.Info                                              |      |      |      |
|                                                              |      |      |      |
| ThreadPool.Names                                             |      |      |      |
|                                                              |      |      |      |
| ThreadPool.ThreadPoolType                                    |      |      |      |
|                                                              |      |      |      |
| ThreadPoolInfo                                               |      |      |      |
|                                                              |      |      |      |
| ThreadPoolStats                                              |      |      |      |
|                                                              |      |      |      |
| ThreadPoolStats.Stats                                        |      |      |      |







org.elasticsearch.transport



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ActionNotFoundTransportException                             |      |      |      |
| An exception indicating that a transport action was not found. |      |      |      |
| ActionTransportException                                     |      |      |      |
| An action invocation failure.                                |      |      |      |
| BindTransportException                                       |      |      |      |
|                                                              |      |      |      |
| BytesTransportRequest                                        |      |      |      |
| A specialized, bytes only request, that can potentially be optimized on the network layer, specifically for the same large buffer send to several nodes. |      |      |      |
| CloseableConnection                                          |      |      |      |
| Abstract Transport.Connection that provides common close logic. |      |      |      |
| ClusterConnectionManager                                     |      |      |      |
| This class manages node connections within a cluster.        |      |      |      |
| Compression                                                  |      |      |      |
|                                                              |      |      |      |
| Compression.Enabled                                          |      |      |      |
|                                                              |      |      |      |
| Compression.Scheme                                           |      |      |      |
|                                                              |      |      |      |
| ConnectionManager                                            |      |      |      |
|                                                              |      |      |      |
| ConnectionManager.ConnectionValidator                        |      |      |      |
|                                                              |      |      |      |
| ConnectionManager.DelegatingNodeConnectionListener           |      |      |      |
|                                                              |      |      |      |
| ConnectionProfile                                            |      |      |      |
| A connection profile describes how many connection are established to specific node for each of the available request types. |      |      |      |
| ConnectionProfile.Builder                                    |      |      |      |
| A builder to build a new ConnectionProfile                   |      |      |      |
| ConnectTransportException                                    |      |      |      |
|                                                              |      |      |      |
| DeflateTransportDecompressor                                 |      |      |      |
|                                                              |      |      |      |
| EmptyTransportResponseHandler                                |      |      |      |
|                                                              |      |      |      |
| FutureTransportResponseHandler<T extends TransportResponse>  |      |      |      |
| A response handler to be used when all interaction will be done through the TransportFuture. |      |      |      |
| Header                                                       |      |      |      |
|                                                              |      |      |      |
| InboundAggregator                                            |      |      |      |
|                                                              |      |      |      |
| InboundDecoder                                               |      |      |      |
|                                                              |      |      |      |
| InboundHandler                                               |      |      |      |
| Handles inbound messages by first deserializing a TransportMessage from an InboundMessage and then passing it to the appropriate handler. |      |      |      |
| InboundMessage                                               |      |      |      |
|                                                              |      |      |      |
| InboundPipeline                                              |      |      |      |
|                                                              |      |      |      |
| Lz4TransportDecompressor                                     |      |      |      |
| This file is forked from the https://netty.io project.       |      |      |      |
| NetworkMessage                                               |      |      |      |
| Represents a transport message sent over the network.        |      |      |      |
| NetworkTraceFlag                                             |      |      |      |
|                                                              |      |      |      |
| NodeDisconnectedException                                    |      |      |      |
|                                                              |      |      |      |
| NodeNotConnectedException                                    |      |      |      |
| An exception indicating that a message is sent to a node that is not connected. |      |      |      |
| NoSeedNodeLeftException                                      |      |      |      |
| Thrown after completely failing to connect to any node of the remote cluster. |      |      |      |
| NoSuchRemoteClusterException                                 |      |      |      |
| An exception that remote cluster is missing or connectivity to the remote connection is failing |      |      |      |
| NotSerializableTransportException                            |      |      |      |
|                                                              |      |      |      |
| PlainTransportFuture<V extends TransportResponse>            |      |      |      |
|                                                              |      |      |      |
| ProxyConnectionStrategy                                      |      |      |      |
|                                                              |      |      |      |
| ProxyConnectionStrategy.ProxyModeInfo                        |      |      |      |
|                                                              |      |      |      |
| RawIndexingDataTransportRequest                              |      |      |      |
| Requests that implement this interface will be compressed when TransportSettings.TRANSPORT_COMPRESS is configured to Compression.Enabled.INDEXING_DATA and isRawIndexingData() returns true. |      |      |      |
| ReceiveTimeoutTransportException                             |      |      |      |
|                                                              |      |      |      |
| RemoteClusterAware                                           |      |      |      |
| Base class for all services and components that need up-to-date information about the registered remote clusters |      |      |      |
| RemoteClusterAwareRequest                                    |      |      |      |
|                                                              |      |      |      |
| RemoteClusterService                                         |      |      |      |
| Basic service for accessing remote clusters via gateway nodes |      |      |      |
| RemoteConnectionInfo                                         |      |      |      |
| This class encapsulates all remote cluster information to be rendered on _remote/info requests. |      |      |      |
| RemoteConnectionInfo.ModeInfo                                |      |      |      |
|                                                              |      |      |      |
| RemoteConnectionManager                                      |      |      |      |
|                                                              |      |      |      |
| RemoteConnectionStrategy                                     |      |      |      |
|                                                              |      |      |      |
| RemoteTransportException                                     |      |      |      |
| A remote exception for an action.                            |      |      |      |
| RequestHandlerRegistry<Request extends TransportRequest>     |      |      |      |
|                                                              |      |      |      |
| ResponseHandlerFailureTransportException                     |      |      |      |
| A failure to handle the response of a transaction action.    |      |      |      |
| ReuseBuffersLZ4BlockOutputStream                             |      |      |      |
| This file is forked from https://github.com/lz4/lz4-java.    |      |      |      |
| SendRequestTransportException                                |      |      |      |
|                                                              |      |      |      |
| SniffConnectionStrategy                                      |      |      |      |
|                                                              |      |      |      |
| SniffConnectionStrategy.SniffModeInfo                        |      |      |      |
|                                                              |      |      |      |
| StatsTracker                                                 |      |      |      |
|                                                              |      |      |      |
| TaskTransportChannel                                         |      |      |      |
|                                                              |      |      |      |
| TcpChannel                                                   |      |      |      |
| This is a tcp channel representing a single channel connection to another node. |      |      |      |
| TcpChannel.ChannelStats                                      |      |      |      |
|                                                              |      |      |      |
| TcpHeader                                                    |      |      |      |
|                                                              |      |      |      |
| TcpServerChannel                                             |      |      |      |
| This is a tcp channel representing a server channel listening for new connections. |      |      |      |
| TcpTransport                                                 |      |      |      |
|                                                              |      |      |      |
| TcpTransport.HttpRequestOnTransportException                 |      |      |      |
| A helper exception to mark an incoming connection as potentially being HTTP so an appropriate error code can be returned |      |      |      |
| TcpTransport.ProfileSettings                                 |      |      |      |
| Representation of a transport profile settings for a transport.profiles.$profilename.* |      |      |      |
| TcpTransportChannel                                          |      |      |      |
|                                                              |      |      |      |
| Transport                                                    |      |      |      |
|                                                              |      |      |      |
| Transport.Connection                                         |      |      |      |
| A unidirectional connection to a DiscoveryNode               |      |      |      |
| Transport.RequestHandlers                                    |      |      |      |
|                                                              |      |      |      |
| Transport.ResponseContext<T extends TransportResponse>       |      |      |      |
| This class represents a response context that encapsulates the actual response handler, the action and the connection it was executed on. |      |      |      |







org.elasticsearch.upgrades





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| FeatureMigrationResults                                      |      |      |      |
| Holds the results of the most recent attempt to migrate system indices. |      |      |      |
| FeatureMigrationResults.ResultsDiff                          |      |      |      |
|                                                              |      |      |      |
| MigrationResultsUpdateTask                                   |      |      |      |
| Handles updating the FeatureMigrationResults in the cluster state. |      |      |      |
| SingleFeatureMigrationResult                                 |      |      |      |
| Holds the results of migrating a single feature.             |      |      |      |
| SystemIndexMigrationExecutor                                 |      |      |      |
| Starts the process of migrating system indices.              |      |      |      |
| SystemIndexMigrationTaskParams                               |      |      |      |
| The params used to initialize SystemIndexMigrator when it's initially kicked off. |      |      |      |
| SystemIndexMigrationTaskState                                |      |      |      |
| Contains the current state of system index migration progress. |      |      |      |
| SystemIndexMigrator                                          |      |      |      |
| This is where the logic to actually perform the migration lives - SystemIndexMigrator.run(SystemIndexMigrationTaskState) will be invoked when the migration process is started, plus any time the node running the migration drops from the cluster/crashes/etc. |      |      |      |





org.elasticsearch.usage



| Class                                                 |      |      |      |
| ----------------------------------------------------- | ---- | ---- | ---- |
| Description                                           |      |      |      |
| UsageService                                          |      |      |      |
| A service to monitor usage of Elasticsearch features. |      |      |      |





org.elasticsearch.watcher



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractResourceWatcher<Listener>                            |      |      |      |
| Abstract resource watcher framework, which handles adding and removing listeners and calling resource observer. |      |      |      |
| FileChangesListener                                          |      |      |      |
| Callback interface that file changes File Watcher is using to notify listeners about changes. |      |      |      |
| FileWatcher                                                  |      |      |      |
| File resources watcher The file watcher checks directory and all its subdirectories for file changes and notifies its listeners accordingly |      |      |      |
| ResourceWatcher                                              |      |      |      |
| Abstract resource watcher interface.                         |      |      |      |
| ResourceWatcherService                                       |      |      |      |
| Generic resource watcher service Other elasticsearch services can register their resource watchers with this service using ResourceWatcherService.add(ResourceWatcher) method. |      |      |      |
| ResourceWatcherService.Frequency                             |      |      |      |
|                                                              |      |      |      |
| WatcherHandle<W extends ResourceWatcher>                     |      |      |      |





org.joda.time.format





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| StrictISODateTimeFormat                                      |      |      |      |
| Factory that creates instances of DateTimeFormatter based on the ISO8601 standard. |      |      |      |

