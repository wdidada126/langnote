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



org.elasticsearch.rest.action.admin.cluster



org.elasticsearch.rest.action.admin.cluster.dangling



org.elasticsearch.rest.action.admin.indices



org.elasticsearch.rest.action.cat



org.elasticsearch.rest.action.datastreams





org.elasticsearch.rest.action.document



org.elasticsearch.rest.action.ingest



org.elasticsearch.rest.action.search



org.elasticsearch.rollup





org.elasticsearch.script



org.elasticsearch.script.field





org.elasticsearch.search





org.elasticsearch.search.aggregations



org.elasticsearch.search.aggregations.bucket





org.elasticsearch.search.aggregations.bucket.adjacency





org.elasticsearch.search.aggregations.bucket.composite





org.elasticsearch.search.aggregations.bucket.filter





org.elasticsearch.search.aggregations.bucket.geogrid





org.elasticsearch.search.aggregations.bucket.global





org.elasticsearch.search.aggregations.bucket.histogram



org.elasticsearch.search.aggregations.bucket.missing





org.elasticsearch.search.aggregations.bucket.nested





org.elasticsearch.search.aggregations.bucket.range





org.elasticsearch.search.aggregations.bucket.sampler





org.elasticsearch.search.aggregations.bucket.terms





org.elasticsearch.search.aggregations.bucket.terms.heuristic





org.elasticsearch.search.aggregations.metrics



org.elasticsearch.search.aggregations.pipeline





org.elasticsearch.search.aggregations.support





org.elasticsearch.search.aggregations.support.values





org.elasticsearch.search.builder





org.elasticsearch.search.collapse





org.elasticsearch.search.dfs





org.elasticsearch.search.fetch



org.elasticsearch.search.fetch.subphase



org.elasticsearch.search.fetch.subphase.highlight



org.elasticsearch.search.internal





org.elasticsearch.search.lookup





org.elasticsearch.search.profile



org.elasticsearch.search.profile.aggregation



org.elasticsearch.search.profile.query



org.elasticsearch.search.query





org.elasticsearch.search.rescore





org.elasticsearch.search.runtime





org.elasticsearch.search.searchafter





org.elasticsearch.search.slice





org.elasticsearch.search.sort





org.elasticsearch.search.suggest



org.elasticsearch.search.suggest.completion



org.elasticsearch.search.suggest.completion.context



org.elasticsearch.search.suggest.phrase





org.elasticsearch.search.suggest.term



org.elasticsearch.shutdown





org.elasticsearch.snapshots



org.elasticsearch.tasks



org.elasticsearch.threadpool





org.elasticsearch.transport



org.elasticsearch.upgrades





org.elasticsearch.usage





org.elasticsearch.watcher





org.joda.time.format
