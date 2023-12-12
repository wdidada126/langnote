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





org.elasticsearch.index.analysis





org.elasticsearch.index.cache





org.elasticsearch.index.cache.bitset





org.elasticsearch.index.cache.query





org.elasticsearch.index.cache.request





org.elasticsearch.index.codec





org.elasticsearch.index.engine





org.elasticsearch.index.fielddata





org.elasticsearch.index.fielddata.fieldcomparator





org.elasticsearch.index.fielddata.ordinals





org.elasticsearch.index.fielddata.plain





org.elasticsearch.index.fieldvisitor





org.elasticsearch.index.flush





org.elasticsearch.index.get





org.elasticsearch.index.mapper





org.elasticsearch.index.mapper.flattened





org.elasticsearch.index.merge





org.elasticsearch.index.query





org.elasticsearch.index.query.functionscore





org.elasticsearch.index.query.support





org.elasticsearch.index.recovery





org.elasticsearch.index.refresh





org.elasticsearch.index.reindex





org.elasticsearch.index.search





org.elasticsearch.index.search.stats





org.elasticsearch.index.seqno





org.elasticsearch.index.shard





org.elasticsearch.index.similarity





org.elasticsearch.index.snapshots





org.elasticsearch.index.snapshots.blobstore





org.elasticsearch.index.stats





org.elasticsearch.index.store





org.elasticsearch.index.termvectors





org.elasticsearch.index.translog





org.elasticsearch.index.warmer





org.elasticsearch.indices







org.elasticsearch.indices.analysis





org.elasticsearch.indices.breaker





org.elasticsearch.indices.cluster





org.elasticsearch.indices.fielddata.cache





org.elasticsearch.indices.flush





org.elasticsearch.indices.recovery





org.elasticsearch.indices.recovery.plan





org.elasticsearch.indices.store





org.elasticsearch.ingest





org.elasticsearch.monitor





org.elasticsearch.monitor.fs





org.elasticsearch.monitor.jvm





org.elasticsearch.monitor.os





org.elasticsearch.monitor.process





org.elasticsearch.node





org.elasticsearch.persistent





org.elasticsearch.persistent.decider





org.elasticsearch.plugins



org.elasticsearch.plugins.spi



org.elasticsearch.repositories



org.elasticsearch.repositories.blobstore



org.elasticsearch.repositories.fs





org.elasticsearch.rest



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
