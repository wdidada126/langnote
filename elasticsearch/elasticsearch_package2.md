# elasticsearch_package

## org.elasticsearch





### org.elasticsearch.cli



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| CommandLoggingConfigurator                                   |      |      |      |
| Holder class for method to configure logging without Elasticsearch configuration files for use in CLI tools that will not read such files. |      |      |      |
| EnvironmentAwareCommand                                      |      |      |      |
| A cli command which requires an Environment to use current paths and settings. |      |      |      |
| KeyStoreAwareCommand                                         |      |      |      |
| An EnvironmentAwareCommand that needs to access the elasticsearch keystore, possibly decrypting it if it is password protected. |      |      |      |
| LoggingAwareCommand                                          |      |      |      |
| A command that is aware of logging.                          |      |      |      |
| LoggingAwareMultiCommand                                     |      |      |      |
| A multi-command that is aware of logging.                    |      |      |      |







org.elasticsearch.client



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AdminClient                                                  |      |      |      |
| Administrative actions/operations against the cluster or the indices. |      |      |      |
| Client                                                       |      |      |      |
| A client provides a one stop interface for performing actions/operations against the cluster. |      |      |      |
| ClusterAdminClient                                           |      |      |      |
| Administrative actions/operations against indices.           |      |      |      |
| ElasticsearchClient                                          |      |      |      |
|                                                              |      |      |      |
| FilterClient                                                 |      |      |      |
| A Client that contains another Client which it uses as its basic source, possibly transforming the requests / responses along the way or providing additional functionality. |      |      |      |
| IndicesAdminClient                                           |      |      |      |
| Administrative actions/operations against indices.           |      |      |      |
| OriginSettingClient                                          |      |      |      |
| A Client that sends requests with the origin set to a particular value and calls its ActionListener in its original ThreadContext. |      |      |      |
| ParentTaskAssigningClient                                    |      |      |      |
| A Client that sets the parent task on all requests that it makes. |      |      |      |
| Requests                                                     |      |      |      |
| A handy one stop shop for creating requests (make sure to import static this class). |      |      |      |





org.elasticsearch.client.node







| Class                                           |      |      |
| ----------------------------------------------- | ---- | ---- |
| Description                                     |      |      |
| NodeClient                                      |      |      |
| Client that executes actions on the local node. |      |      |



org.elasticsearch.client.support

| Class          |      |      |
| -------------- | ---- | ---- |
| Description    |      |      |
| AbstractClient |      |      |





org.elasticsearch.client.transport



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| NoNodeAvailableException                                     |      |      |      |
| An exception indicating no node is available to perform the operation. |      |      |      |
| TransportClient                                              |      |      |      |
| Deprecated.                                                  |      |      |      |
| TransportClient聽is deprecated in favour of the High Level REST client and will be removed in Elasticsearch 8.0. |      |      |      |
| TransportClient.HostFailureListener                          |      |      |      |
| Listener that allows to be notified whenever a node failure / disconnect happens |      |      |      |



org.elasticsearch.cluster

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractDiffable<T extends Diffable<T>>                      |      |      |      |
| Abstract diffable object with simple diffs implementation that sends the entire object if object has changed or nothing if object remained the same. |      |      |      |
| AbstractNamedDiffable<T extends NamedDiffable<T>>            |      |      |      |
| Abstract diffable object with simple diffs implementation that sends the entire object if object has changed or nothing is object remained the same. |      |      |      |
| AckedClusterStateTaskListener                                |      |      |      |
|                                                              |      |      |      |
| AckedClusterStateUpdateTask                                  |      |      |      |
| An extension interface to ClusterStateUpdateTask that allows to be notified when all the nodes have acknowledged a cluster state update request |      |      |      |
| ClusterChangedEvent                                          |      |      |      |
| An event received by the local node, signaling that the cluster state has changed. |      |      |      |
| ClusterInfo                                                  |      |      |      |
| ClusterInfo is an object representing a map of nodes to DiskUsage and a map of shard ids to shard sizes, see InternalClusterInfoService.shardIdentifierFromRouting(String) for the key used in the shardSizes map |      |      |      |
| ClusterInfo.NodeAndPath                                      |      |      |      |
| Represents a data path on a node                             |      |      |      |
| ClusterInfo.ReservedSpace                                    |      |      |      |
| Represents the total amount of "reserved" space on a particular data path, together with the set of shards considered. |      |      |      |
| ClusterInfo.ReservedSpace.Builder                            |      |      |      |
|                                                              |      |      |      |
| ClusterInfoService                                           |      |      |      |
| Interface for a class used to gather information about a cluster periodically. |      |      |      |
| ClusterModule                                                |      |      |      |
| Configures classes and services that affect the entire cluster. |      |      |      |
| ClusterName                                                  |      |      |      |
|                                                              |      |      |      |
| ClusterState                                                 |      |      |      |
| Represents the current state of the cluster.                 |      |      |      |
| ClusterState.Builder                                         |      |      |      |
|                                                              |      |      |      |
| ClusterState.Custom                                          |      |      |      |
|                                                              |      |      |      |
| ClusterState.FeatureAware                                    |      |      |      |
| An interface that implementors use when a class requires a client to maybe have a feature. |      |      |      |
| ClusterState.Metric                                          |      |      |      |
|                                                              |      |      |      |
| ClusterStateApplier                                          |      |      |      |
| A component that is in charge of applying an incoming cluster state to the node internal data structures. |      |      |      |
| ClusterStateListener                                         |      |      |      |
| A listener to be notified when a cluster state changes.      |      |      |      |
| ClusterStateObserver                                         |      |      |      |
| A utility class which simplifies interacting with the cluster state in cases where one tries to take action based on the current state but may want to wait for a new state and retry upon failure. |      |      |      |
| ClusterStateObserver.Listener                                |      |      |      |
|                                                              |      |      |      |
| ClusterStatePublicationEvent                                 |      |      |      |
| Represents a cluster state update computed by the MasterService for publication to the cluster. |      |      |      |
| ClusterStateTaskConfig                                       |      |      |      |
| Cluster state update task configuration for timeout and priority |      |      |      |
| ClusterStateTaskConfig.Basic                                 |      |      |      |
|                                                              |      |      |      |
| ClusterStateTaskExecutor<T>                                  |      |      |      |
|                                                              |      |      |      |
| ClusterStateTaskExecutor.ClusterTasksResult<T>               |      |      |      |
| Represents the result of a batched execution of cluster state update tasks |      |      |      |
| ClusterStateTaskExecutor.ClusterTasksResult.Builder<T>       |      |      |      |
|                                                              |      |      |      |
| ClusterStateTaskExecutor.TaskResult                          |      |      |      |
|                                                              |      |      |      |
| ClusterStateTaskListener                                     |      |      |      |
|                                                              |      |      |      |
| ClusterStateUpdateTask                                       |      |      |      |
| A task that can update the cluster state.                    |      |      |      |
| Diff<T>                                                      |      |      |      |
| Represents difference between states of cluster state parts  |      |      |      |
| Diffable<T>                                                  |      |      |      |
| Cluster state part, changes in which can be serialized       |      |      |      |
| DiffableUtils                                                |      |      |      |
|                                                              |      |      |      |
| DiffableUtils.DiffableValueReader<K,V extends Diffable<V>>   |      |      |      |
| Implementation of the ValueSerializer that wraps value and diff readers. |      |      |      |
| DiffableUtils.DiffableValueSerializer<K,V extends Diffable<V>> |      |      |      |
| Serializer for Diffable map values.                          |      |      |      |
| DiffableUtils.ImmutableOpenMapDiff<K,T>                      |      |      |      |
| Represents differences between two ImmutableOpenMap of (possibly diffable) objects |      |      |      |
| DiffableUtils.KeySerializer<K>                               |      |      |      |
| Provides read and write operations to serialize keys of map  |      |      |      |
| DiffableUtils.MapDiff<K,T,M>                                 |      |      |      |
| Represents differences between two maps of objects and is used as base class for different map implementations. |      |      |      |
| DiffableUtils.NonDiffableValueSerializer<K,V>                |      |      |      |
| Serializer for non-diffable map values                       |      |      |      |
| DiffableUtils.StringSetValueSerializer<K>                    |      |      |      |
| Implementation of ValueSerializer that serializes immutable sets |      |      |      |
| DiffableUtils.ValueSerializer<K,V>                           |      |      |      |
| Provides read and write operations to serialize map values.  |      |      |      |
| DiskUsage                                                    |      |      |      |
| Encapsulation class used to represent the amount of disk used on a node. |      |      |      |
| EmptyClusterInfoService                                      |      |      |      |
| ClusterInfoService that provides empty maps for disk usage and shard sizes |      |      |      |
| IncompatibleClusterStateVersionException                     |      |      |      |
| Thrown by Diff.apply(T) method                               |      |      |      |
| InternalClusterInfoService                                   |      |      |      |
| InternalClusterInfoService provides the ClusterInfoService interface, routinely updated on a timer. |      |      |      |
| LocalClusterUpdateTask                                       |      |      |      |
| Used to apply state updates on nodes that are not necessarily master |      |      |      |
| LocalNodeMasterListener                                      |      |      |      |
| Enables listening to master changes events of the local node (when the local node becomes the master, and when the local node cease being a master). |      |      |      |
| MasterNodeChangePredicate                                    |      |      |      |
|                                                              |      |      |      |
| MergableCustomMetadata<T extends Metadata.Custom>            |      |      |      |
| Interface to allow merging Metadata.Custom.                  |      |      |      |
| NamedDiff<T extends Diffable<T>>                             |      |      |      |
| Diff that also support NamedWriteable interface              |      |      |      |
| NamedDiffable<T>                                             |      |      |      |
| Diff that also support VersionedNamedWriteable interface     |      |      |      |
| NamedDiffableValueSerializer<T extends NamedDiffable<T>>     |      |      |      |
| Value Serializer for named diffables                         |      |      |      |
| NodeConnectionsService                                       |      |      |      |
| This component is responsible for maintaining connections from this node to all the nodes listed in the cluster state, and for disconnecting from nodes once they are removed from the cluster state. |      |      |      |
| NotMasterException                                           |      |      |      |
| Thrown when a node join request or a master ping reaches a node which is not currently acting as a master or when a cluster state update task is to be executed on a node that is no longer master. |      |      |      |
| RepositoryCleanupInProgress                                  |      |      |      |
|                                                              |      |      |      |
| RepositoryCleanupInProgress.Entry                            |      |      |      |
|                                                              |      |      |      |
| RestoreInProgress                                            |      |      |      |
| Meta data about restore processes that are currently executing |      |      |      |
| RestoreInProgress.Builder                                    |      |      |      |
|                                                              |      |      |      |
| RestoreInProgress.Entry                                      |      |      |      |
| Restore metadata                                             |      |      |      |
| RestoreInProgress.ShardRestoreStatus                         |      |      |      |
| Represents status of a restored shard                        |      |      |      |
| RestoreInProgress.State                                      |      |      |      |
| Shard restore process state                                  |      |      |      |
| SnapshotDeletionsInProgress                                  |      |      |      |
| A class that represents the snapshot deletions that are in progress in the cluster. |      |      |      |
| SnapshotDeletionsInProgress.Entry                            |      |      |      |
| A class representing a snapshot deletion request entry in the cluster state. |      |      |      |
| SnapshotDeletionsInProgress.State                            |      |      |      |
|                                                              |      |      |      |
| SnapshotsInProgress                                          |      |      |      |
| Meta data about snapshots that are currently executing       |      |      |      |
| SnapshotsInProgress.Entry                                    |      |      |      |
|                                                              |      |      |      |
| SnapshotsInProgress.ShardSnapshotStatus                      |      |      |      |
|                                                              |      |      |      |
| SnapshotsInProgress.ShardState                               |      |      |      |
|                                                              |      |      |      |
| SnapshotsInProgress.State                                    |      |      |      |
|                                                              |      |      |      |
| TimeoutClusterStateListener                                  |      |      |      |
| An exception to cluster state listener that allows for timeouts and for post added notifications. |      |      |      |



org.elasticsearch.cluster.ack



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AckedRequest                                                 |      |      |      |
| Identifies a cluster state update request with acknowledgement support |      |      |      |
| ClusterStateUpdateRequest<T extends ClusterStateUpdateRequest<T>> |      |      |      |
| Base class to be used when needing to update the cluster state Contains the basic fields that are always needed |      |      |      |
| IndicesClusterStateUpdateRequest<T extends IndicesClusterStateUpdateRequest<T>> |      |      |      |
| Base cluster state update request that allows to execute update against multiple indices |      |      |      |



org.elasticsearch.cluster.action.index





| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| MappingUpdatedAction                                         |      |      |
| Called by shards in the cluster when their mapping was dynamically updated and it needs to be updated in the cluster state meta data (and broadcast to all members). |      |      |



org.elasticsearch.cluster.action.shard



| Class                                                 |      |      |      |
| ----------------------------------------------------- | ---- | ---- | ---- |
| Description                                           |      |      |      |
| ShardStateAction                                      |      |      |      |
|                                                       |      |      |      |
| ShardStateAction.FailedShardEntry                     |      |      |      |
|                                                       |      |      |      |
| ShardStateAction.NoLongerPrimaryShardException        |      |      |      |
|                                                       |      |      |      |
| ShardStateAction.ShardFailedClusterStateTaskExecutor  |      |      |      |
|                                                       |      |      |      |
| ShardStateAction.ShardStartedClusterStateTaskExecutor |      |      |      |
|                                                       |      |      |      |
| ShardStateAction.StartedShardEntry                    |      |      |      |

org.elasticsearch.cluster.block

| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ClusterBlock                                                 |      |      |      |
|                                                              |      |      |      |
| ClusterBlockException                                        |      |      |      |
|                                                              |      |      |      |
| ClusterBlockLevel                                            |      |      |      |
|                                                              |      |      |      |
| ClusterBlocks                                                |      |      |      |
| Represents current cluster level blocks to block dirty operations done against the cluster. |      |      |      |
| ClusterBlocks.Builder                                        |      |      |      |



org.elasticsearch.cluster.coordination



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ApplyCommitRequest                                           |      |      |      |
| A master node sends this request to its peers to inform them that it could commit the cluster state with the given term and version. |      |      |      |
| ClusterBootstrapService                                      |      |      |      |
|                                                              |      |      |      |
| ClusterFormationFailureHelper                                |      |      |      |
|                                                              |      |      |      |
| ClusterStatePublisher                                        |      |      |      |
|                                                              |      |      |      |
| ClusterStatePublisher.AckListener                            |      |      |      |
|                                                              |      |      |      |
| ClusterStateSerializationStats                               |      |      |      |
|                                                              |      |      |      |
| CoordinationMetadata                                         |      |      |      |
|                                                              |      |      |      |
| CoordinationMetadata.Builder                                 |      |      |      |
|                                                              |      |      |      |
| CoordinationMetadata.VotingConfigExclusion                   |      |      |      |
|                                                              |      |      |      |
| CoordinationMetadata.VotingConfiguration                     |      |      |      |
| A collection of persistent node ids, denoting the voting configuration for cluster state changes. |      |      |      |
| CoordinationState                                            |      |      |      |
| The core class of the cluster state coordination algorithm, directly implementing the formal model |      |      |      |
| CoordinationState.PersistedState                             |      |      |      |
| Pluggable persistence layer for CoordinationState.           |      |      |      |
| CoordinationState.VoteCollection                             |      |      |      |
| A collection of votes, used to calculate quorums.            |      |      |      |
| CoordinationStateRejectedException                           |      |      |      |
| This exception is thrown when rejecting state transitions on the CoordinationState object, for example when receiving a publish request with the wrong term or version. |      |      |      |
| Coordinator                                                  |      |      |      |
|                                                              |      |      |      |
| Coordinator.Mode                                             |      |      |      |
|                                                              |      |      |      |
| DetachClusterCommand                                         |      |      |      |
|                                                              |      |      |      |
| DiscoveryUpgradeService                                      |      |      |      |
| Deals with rolling upgrades of the cluster coordination layer. |      |      |      |
| ElasticsearchNodeCommand                                     |      |      |      |
|                                                              |      |      |      |
| ElasticsearchNodeCommand.UnknownCondition                    |      |      |      |
|                                                              |      |      |      |
| ElasticsearchNodeCommand.UnknownMetadataCustom               |      |      |      |
|                                                              |      |      |      |
| ElectionSchedulerFactory                                     |      |      |      |
| It's provably impossible to guarantee that any leader election algorithm ever elects a leader, but they generally work (with probability that approaches 1 over time) as long as elections occur sufficiently infrequently, compared to the time it takes to send a message to another node and receive a response back. |      |      |      |
| ElectionStrategy                                             |      |      |      |
| Allows plugging in a custom election strategy, restricting the notion of an election quorum. |      |      |      |
| FailedToCommitClusterStateException                          |      |      |      |
| Thrown when failing to publish a cluster state.              |      |      |      |
| FollowersChecker                                             |      |      |      |
| The FollowersChecker is responsible for allowing a leader to check that its followers are still connected and healthy. |      |      |      |
| FollowersChecker.FollowerCheckRequest                        |      |      |      |
|                                                              |      |      |      |
| InMemoryPersistedState                                       |      |      |      |
|                                                              |      |      |      |
| Join                                                         |      |      |      |
| Triggered by a StartJoinRequest, instances of this class represent join votes, and have a source and target node. |      |      |      |
| JoinHelper                                                   |      |      |      |
|                                                              |      |      |      |
| JoinRequest                                                  |      |      |      |
|                                                              |      |      |      |
| JoinTaskExecutor                                             |      |      |      |
|                                                              |      |      |      |
| JoinTaskExecutor.Task                                        |      |      |      |
|                                                              |      |      |      |
| LagDetector                                                  |      |      |      |
| A publication can succeed and complete before all nodes have applied the published state and acknowledged it; however we need every node eventually either to apply the published state (or a later state) or be removed from the cluster. |      |      |      |
| LagDetector.LagListener                                      |      |      |      |
|                                                              |      |      |      |
| LeaderChecker                                                |      |      |      |
| The LeaderChecker is responsible for allowing followers to check that the currently elected leader is still connected and healthy. |      |      |      |
| NodeHealthCheckFailureException                              |      |      |      |
| This exception is thrown if the File system is reported unhealthy by @FsHealthService and this nodes needs to be removed from the cluster |      |      |      |
| NodeRemovalClusterStateTaskExecutor                          |      |      |      |
|                                                              |      |      |      |
| NodeRemovalClusterStateTaskExecutor.Task                     |      |      |      |
|                                                              |      |      |      |
| NodeToolCli                                                  |      |      |      |
|                                                              |      |      |      |
| NoMasterBlockService                                         |      |      |      |
|                                                              |      |      |      |
| PeersResponse                                                |      |      |      |
|                                                              |      |      |      |
| PreVoteCollector                                             |      |      |      |
|                                                              |      |      |      |
| PreVoteRequest                                               |      |      |      |
|                                                              |      |      |      |
| PreVoteResponse                                              |      |      |      |
|                                                              |      |      |      |
| Publication                                                  |      |      |      |
|                                                              |      |      |      |
| PublicationTransportHandler                                  |      |      |      |
|                                                              |      |      |      |
| PublishRequest                                               |      |      |      |
| Request which is used by the master node to publish cluster state changes. |      |      |      |
| PublishResponse                                              |      |      |      |
| Response to a PublishRequest, carrying the term and version of the request. |      |      |      |
| PublishWithJoinResponse                                      |      |      |      |
| Response to a PublishRequest.                                |      |      |      |
| Reconfigurator                                               |      |      |      |
| Computes the optimal configuration of voting nodes in the cluster. |      |      |      |
| RemoveCustomsCommand                                         |      |      |      |
|                                                              |      |      |      |
| RemoveSettingsCommand                                        |      |      |      |
|                                                              |      |      |      |
| StartJoinRequest                                             |      |      |      |
| Represents the action of requesting a join vote (see Join) from a node. |      |      |      |
| UnsafeBootstrapMasterCommand                                 |      |      |      |
|                                                              |      |      |      |
| ValidateJoinRequest                                          |      |      |      |





org.elasticsearch.cluster.health



| Class               |      |      |
| ------------------- | ---- | ---- |
| Description         |      |      |
| ClusterHealthStatus |      |      |
|                     |      |      |
| ClusterIndexHealth  |      |      |
|                     |      |      |
| ClusterShardHealth  |      |      |
|                     |      |      |
| ClusterStateHealth  |      |      |



org.elasticsearch.cluster.metadata

| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AliasAction                                                  |      |      |
| Individual operation to perform on the cluster state as part of an IndicesAliasesRequest. |      |      |
| AliasAction.Add                                              |      |      |
| Operation to add an alias to an index.                       |      |      |
| AliasAction.AddDataStreamAlias                               |      |      |
|                                                              |      |      |
| AliasAction.NewAliasValidator                                |      |      |
| Validate a new alias.                                        |      |      |
| AliasAction.Remove                                           |      |      |
| Operation to remove an alias from an index.                  |      |      |
| AliasAction.RemoveDataStreamAlias                            |      |      |
|                                                              |      |      |
| AliasAction.RemoveIndex                                      |      |      |
| Operation to remove an index.                                |      |      |
| AliasMetadata                                                |      |      |
|                                                              |      |      |
| AliasMetadata.Builder                                        |      |      |
|                                                              |      |      |
| AliasValidator                                               |      |      |
| Validator for an alias, to be used before adding an alias to the index metadata and make sure the alias is valid |      |      |
| AutoExpandReplicas                                           |      |      |
| This class acts as a functional wrapper around the index.auto_expand_replicas setting. |      |      |
| ClusterNameExpressionResolver                                |      |      |
| Resolves cluster names from an expression.                   |      |      |
| ComponentTemplate                                            |      |      |
| A component template is a re-usable Template as well as metadata about the template. |      |      |
| ComponentTemplateMetadata                                    |      |      |
| ComponentTemplateMetadata is a custom Metadata implementation for storing a map of component templates and their names. |      |      |
| ComposableIndexTemplate                                      |      |      |
| An index template is comprised of a set of index patterns, an optional template, and a list of ids corresponding to component templates that should be composed in order when creating a new index. |      |      |
| ComposableIndexTemplate.Builder                              |      |      |
|                                                              |      |      |
| ComposableIndexTemplate.DataStreamTemplate                   |      |      |
|                                                              |      |      |
| ComposableIndexTemplateMetadata                              |      |      |
| The ComposableIndexTemplateMetadata class is a custom Metadata.Custom implementation that stores a map of ids to ComposableIndexTemplate templates. |      |      |
| DataStream                                                   |      |      |
|                                                              |      |      |
| DataStream.TimestampField                                    |      |      |
|                                                              |      |      |
| DataStreamAction                                             |      |      |
| Operations on data streams.                                  |      |      |
| DataStreamAction.Type                                        |      |      |
|                                                              |      |      |
| DataStreamAlias                                              |      |      |
|                                                              |      |      |
| DataStreamMetadata                                           |      |      |
| Custom Metadata implementation for storing a map of DataStreams and their names. |      |      |
| DiffableStringMap                                            |      |      |
| This is a Map<String, String> that implements AbstractDiffable so it can be used for cluster state purposes |      |      |
| DiffableStringMap.DiffableStringMapDiff                      |      |      |
| Represents differences between two DiffableStringMaps.       |      |      |
| IndexAbstraction                                             |      |      |
| An index abstraction is a reference to one or more concrete indices. |      |      |
| IndexAbstraction.Alias                                       |      |      |
| Represents an alias and groups all IndexMetadata instances sharing the same alias name together. |      |      |
| IndexAbstraction.ConcreteIndex                               |      |      |
| Represents an concrete index and encapsulates its IndexMetadata |      |      |
| IndexAbstraction.DataStream                                  |      |      |
|                                                              |      |      |
| IndexAbstraction.Type                                        |      |      |
| An index abstraction type.                                   |      |      |
| IndexAbstractionResolver                                     |      |      |
|                                                              |      |      |
| IndexGraveyard                                               |      |      |
| A collection of tombstones for explicitly marking indices as deleted in the cluster state. |      |      |
| IndexGraveyard.Builder                                       |      |      |
| A class to build an IndexGraveyard.                          |      |      |
| IndexGraveyard.IndexGraveyardDiff                            |      |      |
| A class representing a diff of two IndexGraveyard objects.   |      |      |
| IndexGraveyard.Tombstone                                     |      |      |
| An individual tombstone entry for representing a deleted index. |      |      |
| IndexMetadata                                                |      |      |
|                                                              |      |      |
| IndexMetadata.APIBlock                                       |      |      |
|                                                              |      |      |
| IndexMetadata.Builder                                        |      |      |
|                                                              |      |      |
| IndexMetadata.State                                          |      |      |
|                                                              |      |      |
| IndexMetadataVerifier                                        |      |      |
| This service is responsible for verifying index metadata when an index is introduced to the cluster, for example when restarting nodes, importing dangling indices, or restoring an index from a snapshot repository. |      |      |
| IndexNameExpressionResolver                                  |      |      |
|                                                              |      |      |
| IndexNameExpressionResolver.Context                          |      |      |
|                                                              |      |      |
| IndexNameExpressionResolver.DateMathExpressionResolver       |      |      |
|                                                              |      |      |
| IndexNameExpressionResolver.ResolverContext                  |      |      |
| This is a context for the DateMathExpressionResolver which does not require IndicesOptions or ClusterState since it uses only the start time to resolve expressions. |      |      |
| IndexTemplateMetadata                                        |      |      |
|                                                              |      |      |
| IndexTemplateMetadata.Builder                                |      |      |
|                                                              |      |      |
| ItemUsage                                                    |      |      |
| A class encapsulating the usage of a particular "thing" by something else |      |      |
| Manifest                                                     |      |      |
| This class represents the manifest file, which is the entry point for reading meta data from disk. |      |      |
| MappingMetadata                                              |      |      |
| Mapping configuration for a type.                            |      |      |
| MappingMetadata.Routing                                      |      |      |
|                                                              |      |      |
| Metadata                                                     |      |      |
| Metadata is the part of the ClusterState which persists across restarts. |      |      |
| Metadata.Builder                                             |      |      |
|                                                              |      |      |
| Metadata.Custom                                              |      |      |
| Custom metadata that persists (via XContent) across restarts. |      |      |
| Metadata.NonRestorableCustom                                 |      |      |
|                                                              |      |      |
| Metadata.XContentContext                                     |      |      |
|                                                              |      |      |
| MetadataCreateDataStreamService                              |      |      |
|                                                              |      |      |
| MetadataCreateDataStreamService.CreateDataStreamClusterStateUpdateRequest |      |      |
|                                                              |      |      |
| MetadataCreateIndexService                                   |      |      |
| Service responsible for submitting create index requests     |      |      |
| MetadataDataStreamsService                                   |      |      |
| Handles data stream modification requests.                   |      |      |
| MetadataDeleteIndexService                                   |      |      |
| Deletes indices.                                             |      |      |
| MetadataIndexAliasesService                                  |      |      |
| Service responsible for submitting add and remove aliases requests |      |      |
| MetadataIndexStateService                                    |      |      |
| Service responsible for submitting open/close index requests as well as for adding index blocks |      |      |
| MetadataIndexTemplateService                                 |      |      |
| Service responsible for submitting index templates updates   |      |      |
| MetadataIndexTemplateService.PutListener                     |      |      |
|                                                              |      |      |
| MetadataIndexTemplateService.PutRequest                      |      |      |
|                                                              |      |      |
| MetadataIndexTemplateService.PutResponse                     |      |      |
|                                                              |      |      |
| MetadataIndexTemplateService.RemoveListener                  |      |      |
|                                                              |      |      |
| MetadataIndexTemplateService.RemoveRequest                   |      |      |
|                                                              |      |      |
| MetadataMappingService                                       |      |      |
| Service responsible for submitting mapping changes           |      |      |
| MetadataMigrateToDataStreamService                           |      |      |
|                                                              |      |      |
| MetadataMigrateToDataStreamService.MigrateToDataStreamClusterStateUpdateRequest |      |      |
|                                                              |      |      |
| MetadataUpdateSettingsService                                |      |      |
| Service responsible for submitting update index settings requests |      |      |
| NodesShutdownMetadata                                        |      |      |
| Contains the data about nodes which are currently configured to shut down, either permanently or temporarily. |      |      |
| NodesShutdownMetadata.NodeShutdownMetadataDiff               |      |      |
| Handles diffing and appling diffs for NodesShutdownMetadata as necessary for the cluster state infrastructure. |      |      |
| ProcessClusterEventTimeoutException                          |      |      |
|                                                              |      |      |
| RepositoriesMetadata                                         |      |      |
| Contains metadata about registered snapshot repositories     |      |      |
| RepositoryMetadata                                           |      |      |
| Metadata about registered repository                         |      |      |
| ShutdownPersistentTasksStatus                                |      |      |
|                                                              |      |      |
| ShutdownPluginsStatus                                        |      |      |
|                                                              |      |      |
| ShutdownShardMigrationStatus                                 |      |      |
|                                                              |      |      |
| SingleNodeShutdownMetadata                                   |      |      |
| Contains data about a single node's shutdown readiness.      |      |      |
| SingleNodeShutdownMetadata.Builder                           |      |      |
|                                                              |      |      |
| SingleNodeShutdownMetadata.Status                            |      |      |
| Describes the status of a component of shutdown.             |      |      |
| SingleNodeShutdownMetadata.Type                              |      |      |
| Describes the type of node shutdown - permanent (REMOVE) or temporary (RESTART). |      |      |
| SystemIndexMetadataUpgradeService                            |      |      |
| A service responsible for updating the metadata used by system indices. |      |      |
| Template                                                     |      |      |
| A template consists of optional settings, mappings, or alias configuration for an index, however, it is entirely independent from an index. |      |      |
| TemplateUpgradeService                                       |      |      |
| Upgrades Templates on behalf of installed Plugins when a node joins the cluster |      |      |



org.elasticsearch.cluster.node



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| DiscoveryNode                                                |      |      |
| A discovery node represents a node that is part of the cluster. |      |      |
| DiscoveryNodeFilters                                         |      |      |
|                                                              |      |      |
| DiscoveryNodeFilters.OpType                                  |      |      |
|                                                              |      |      |
| DiscoveryNodeRole                                            |      |      |
| Represents a node role.                                      |      |      |
| DiscoveryNodes                                               |      |      |
| This class holds all DiscoveryNode in the cluster and provides convenience methods to access, modify merge / diff discovery nodes. |      |      |
| DiscoveryNodes.Builder                                       |      |      |
|                                                              |      |      |
| DiscoveryNodes.Delta                                         |      |      |







org.elasticsearch.cluster.routing







| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AllocationId                                                 |      |      |      |      |
| Uniquely identifies an allocation.                           |      |      |      |      |
| BatchedRerouteService                                        |      |      |      |      |
| A BatchedRerouteService is a RerouteService that batches together reroute requests to avoid unnecessary extra reroutes. |      |      |      |      |
| DelayedAllocationService                                     |      |      |      |      |
| The DelayedAllocationService listens to cluster state changes and checks if there are unassigned shards with delayed allocation (unassigned shards that have the delay marker). |      |      |      |      |
| GroupShardsIterator<ShardIt extends Comparable<ShardIt> & Countable> |      |      |      |      |
| This class implements a compilation of ShardIterators.       |      |      |      |      |
| IllegalShardRoutingStateException                            |      |      |      |      |
| This exception defines illegal states of shard routing       |      |      |      |      |
| IndexRouting                                                 |      |      |      |      |
| Generates the shard id for (id, routing) pairs.              |      |      |      |      |
| IndexRoutingTable                                            |      |      |      |      |
| The IndexRoutingTable represents routing information for a single index. |      |      |      |      |
| IndexRoutingTable.Builder                                    |      |      |      |      |
|                                                              |      |      |      |      |
| IndexShardRoutingTable                                       |      |      |      |      |
| IndexShardRoutingTable encapsulates all instances of a single shard. |      |      |      |      |
| IndexShardRoutingTable.Builder                               |      |      |      |      |
|                                                              |      |      |      |      |
| Murmur3HashFunction                                          |      |      |      |      |
| Hash function based on the Murmur3 algorithm, which is the default as of Elasticsearch 2.0. |      |      |      |      |
| OperationRouting                                             |      |      |      |      |
|                                                              |      |      |      |      |
| PlainShardIterator                                           |      |      |      |      |
| The PlainShardIterator is a ShardsIterator which iterates all shards or a given shard id |      |      |      |      |
| PlainShardsIterator                                          |      |      |      |      |
| A simple ShardsIterator that iterates a list or sub-list of shard indexRoutings. |      |      |      |      |
| Preference                                                   |      |      |      |      |
| Routing Preference Type                                      |      |      |      |      |
| RecoverySource                                               |      |      |      |      |
| Represents the recovery source of a shard.                   |      |      |      |      |
| RecoverySource.EmptyStoreRecoverySource                      |      |      |      |      |
| Recovery from a fresh copy                                   |      |      |      |      |
| RecoverySource.ExistingStoreRecoverySource                   |      |      |      |      |
| Recovery from an existing on-disk store                      |      |      |      |      |
| RecoverySource.LocalShardsRecoverySource                     |      |      |      |      |
| recovery from other shards on same node (shrink index action) |      |      |      |      |
| RecoverySource.PeerRecoverySource                            |      |      |      |      |
| peer recovery from a primary shard                           |      |      |      |      |
| RecoverySource.SnapshotRecoverySource                        |      |      |      |      |
| recovery from a snapshot                                     |      |      |      |      |
| RecoverySource.Type                                          |      |      |      |      |
|                                                              |      |      |      |      |
| RerouteService                                               |      |      |      |      |
| Asynchronously performs a cluster reroute, updating any shard states and rebalancing the cluster if appropriate. |      |      |      |      |
| RotationShardShuffler                                        |      |      |      |      |
| Basic ShardShuffler implementation that uses an AtomicInteger to generate seeds and uses a rotation to permute shards. |      |      |      |      |
| RoutingChangesObserver                                       |      |      |      |      |
| Records changes made to RoutingNodes during an allocation round. |      |      |      |      |
| RoutingChangesObserver.AbstractRoutingChangesObserver        |      |      |      |      |
| Abstract implementation of RoutingChangesObserver that does not take any action. |      |      |      |      |
| RoutingChangesObserver.DelegatingRoutingChangesObserver      |      |      |      |      |
|                                                              |      |      |      |      |
| RoutingException                                             |      |      |      |      |
| A base Exceptions for all exceptions thrown by routing related operations. |      |      |      |      |
| RoutingNode                                                  |      |      |      |      |
| A RoutingNode represents a cluster node associated with a single DiscoveryNode including all shards that are hosted on that nodes. |      |      |      |      |
| RoutingNodes                                                 |      |      |      |      |
| RoutingNodes represents a copy the routing information contained in the cluster state. |      |      |      |      |
| RoutingNodes.UnassignedShards                                |      |      |      |      |
|                                                              |      |      |      |      |
| RoutingTable                                                 |      |      |      |      |
| Represents a global cluster-wide routing table for all indices including the version of the current routing state. |      |      |      |      |
| RoutingTable.Builder                                         |      |      |      |      |
| Builder for the routing table.                               |      |      |      |      |
| ShardIterator                                                |      |      |      |      |
| Allows to iterate over a set of shard instances (routing) within a shard id group. |      |      |      |      |
| ShardRouting                                                 |      |      |      |      |
| ShardRouting immutably encapsulates information about shard indexRoutings like id, state, version, etc. |      |      |      |      |
| ShardRoutingState                                            |      |      |      |      |
| Represents the current state of a ShardRouting as defined by the cluster. |      |      |      |      |
| ShardShuffler                                                |      |      |      |      |
| A shuffler for shards whose primary goal is to balance load. |      |      |      |      |
| ShardsIterator                                               |      |      |      |      |
| Allows to iterate over unrelated shards.                     |      |      |      |      |
| UnassignedInfo                                               |      |      |      |      |
| Holds additional information as to why the shard is in unassigned state. |      |      |      |      |
| UnassignedInfo.AllocationStatus                              |      |      |      |      |
| Captures the status of an unsuccessful allocation attempt for the shard, causing it to remain in the unassigned state. |      |      |      |      |
| UnassignedInfo.Reason                                        |      |      |      |      |
| Reason why the shard is in unassigned state.                 |      |      |      |      |





org.elasticsearch.cluster.routing.allocation





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| AbstractAllocationDecision                                   |      |      |      |
| An abstract class for representing various types of allocation decisions. |      |      |      |
| AllocateUnassignedDecision                                   |      |      |      |
| Represents the allocation decision by an allocator for an unassigned shard. |      |      |      |
| AllocationDecision                                           |      |      |      |
| An enum which represents the various decision types that can be taken by the allocators and deciders for allocating a shard to a node. |      |      |      |
| AllocationService                                            |      |      |      |
| This service manages the node allocation of a cluster.       |      |      |      |
| AllocationService.CommandsResult                             |      |      |      |
| this class is used to describe results of applying a set of AllocationCommand |      |      |      |
| DataTier                                                     |      |      |      |
| The DataTier class encapsulates the formalization of the "content", "hot", "warm", and "cold" tiers as node roles. |      |      |      |
| DataTier.DefaultHotAllocationSettingProvider                 |      |      |      |
| This setting provider injects the setting allocating all newly created indices with index.routing.allocation.include._tier: "data_hot" unless the user overrides the setting while the index is being created (in a create index request for instance) |      |      |      |
| DiskThresholdMonitor                                         |      |      |      |
| Listens for a node to go over the high watermark and kicks off an empty reroute if it does. |      |      |      |
| DiskThresholdSettings                                        |      |      |      |
| A container to keep settings for disk thresholds up to date with cluster setting changes. |      |      |      |
| ExistingShardsAllocator                                      |      |      |      |
| Searches for, and allocates, shards for which there is an existing on-disk copy somewhere in the cluster. |      |      |      |
| ExistingShardsAllocator.UnassignedAllocationHandler          |      |      |      |
| Used by ExistingShardsAllocator.allocateUnassigned(org.elasticsearch.cluster.routing.ShardRouting, org.elasticsearch.cluster.routing.allocation.RoutingAllocation, org.elasticsearch.cluster.routing.allocation.ExistingShardsAllocator.UnassignedAllocationHandler) to handle its allocation decisions. |      |      |      |
| FailedShard                                                  |      |      |      |
| A class representing a failed shard.                         |      |      |      |
| IndexMetadataUpdater                                         |      |      |      |
| Observer that tracks changes made to RoutingNodes in order to update the primary terms and in-sync allocation ids in IndexMetadata once the allocation round has completed. |      |      |      |
| MoveDecision                                                 |      |      |      |
| Represents a decision to move a started shard, either because it is no longer allowed to remain on its current node or because moving it to another node will form a better cluster balance. |      |      |      |
| NodeAllocationResult                                         |      |      |      |
| This class represents the shard allocation decision and its explanation for a single node. |      |      |      |
| NodeAllocationResult.ShardStoreInfo                          |      |      |      |
| A class that captures metadata about a shard store on a node. |      |      |      |
| RerouteExplanation                                           |      |      |      |
| Class encapsulating the explanation for a single AllocationCommand taken from the Deciders |      |      |      |
| RoutingAllocation                                            |      |      |      |
| The RoutingAllocation keep the state of the current allocation of shards and holds the AllocationDeciders which are responsible for the current routing state. |      |      |      |
| RoutingAllocation.DebugMode                                  |      |      |      |
|                                                              |      |      |      |
| RoutingExplanations                                          |      |      |      |
| Class used to encapsulate a number of RerouteExplanation explanations. |      |      |      |
| RoutingNodesChangedObserver                                  |      |      |      |
| Records if changes were made to RoutingNodes during an allocation round. |      |      |      |
| ShardAllocationDecision                                      |      |      |      |
| Represents the decision taken for the allocation of a single shard. |      |      |      |
| StaleShard                                                   |      |      |      |
| A class that represents a stale shard copy.                  |      |      |      |



org.elasticsearch.cluster.routing.allocation.allocator



| Class                            | Description                                                  |      |
| -------------------------------- | ------------------------------------------------------------ | ---- |
|                                  |                                                              |      |
| BalancedShardsAllocator          | The BalancedShardsAllocator re-balances the nodes allocations within an cluster based on a BalancedShardsAllocator.WeightFunction. |      |
|                                  |                                                              |      |
| BalancedShardsAllocator.Balancer | A BalancedShardsAllocator.Balancer                           |      |
|                                  |                                                              |      |
| ShardsAllocator                  | A ShardsAllocator is the main entry point for shard allocation on nodes in the cluster. |      |
|                                  |                                                              |      |





org.elasticsearch.cluster.routing.allocation.command



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| AbstractAllocateAllocationCommand                            |      |      |
| Abstract base class for allocating an unassigned shard to a node |      |      |
| AbstractAllocateAllocationCommand.Builder<T extends AbstractAllocateAllocationCommand> |      |      |
| Works around ObjectParser not supporting constructor arguments. |      |      |
| AllocateEmptyPrimaryAllocationCommand                        |      |      |
| Allocates an unassigned empty primary shard to a specific node. |      |      |
| AllocateEmptyPrimaryAllocationCommand.Builder                |      |      |
|                                                              |      |      |
| AllocateReplicaAllocationCommand                             |      |      |
| Allocates an unassigned replica shard to a specific node.    |      |      |
| AllocateReplicaAllocationCommand.Builder                     |      |      |
|                                                              |      |      |
| AllocateStalePrimaryAllocationCommand                        |      |      |
| Allocates an unassigned stale primary shard to a specific node. |      |      |
| AllocateStalePrimaryAllocationCommand.Builder                |      |      |
|                                                              |      |      |
| AllocationCommand                                            |      |      |
| A command to move shards in some way.                        |      |      |
| AllocationCommands                                           |      |      |
| A simple AllocationCommand composite managing several AllocationCommand implementations |      |      |
| BasePrimaryAllocationCommand                                 |      |      |
| Abstract base class for allocating an unassigned primary shard to a node |      |      |
| BasePrimaryAllocationCommand.Builder<T extends BasePrimaryAllocationCommand> |      |      |
|                                                              |      |      |
| CancelAllocationCommand                                      |      |      |
| A command that cancels relocation, or recovery of a given shard on a node. |      |      |
| MoveAllocationCommand                                        |      |      |
| A command that moves a shard from a specific node to another node. |      |      |



org.elasticsearch.cluster.routing.allocation.decider



| Class                                                        |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- |
| Description                                                  |      |      |      |      |
| AllocationDecider                                            |      |      |      |      |
| AllocationDecider is an abstract base class that allows to make dynamic cluster- or index-wide shard allocation decisions on a per-node basis. |      |      |      |      |
| AllocationDeciders                                           |      |      |      |      |
| A composite AllocationDecider combining the "decision" of multiple AllocationDecider implementations into a single allocation decision. |      |      |      |      |
| AwarenessAllocationDecider                                   |      |      |      |      |
| This AllocationDecider controls shard allocation based on awareness key-value pairs defined in the node configuration. |      |      |      |      |
| ClusterRebalanceAllocationDecider                            |      |      |      |      |
| This AllocationDecider controls re-balancing operations based on the cluster wide active shard state. |      |      |      |      |
| ClusterRebalanceAllocationDecider.ClusterRebalanceType       |      |      |      |      |
| An enum representation for the configured re-balance type.   |      |      |      |      |
| ConcurrentRebalanceAllocationDecider                         |      |      |      |      |
| Similar to the ClusterRebalanceAllocationDecider this AllocationDecider controls the number of currently in-progress re-balance (relocation) operations and restricts node allocations if the configured threshold is reached. |      |      |      |      |
| Decision                                                     |      |      |      |      |
| This abstract class defining basic Decision used during shard allocation process. |      |      |      |      |
| Decision.Multi                                               |      |      |      |      |
| Simple class representing a list of decisions                |      |      |      |      |
| Decision.Single                                              |      |      |      |      |
| Simple class representing a single decision                  |      |      |      |      |
| Decision.Type                                                |      |      |      |      |
| This enumeration defines the possible types of decisions     |      |      |      |      |
| DiskThresholdDecider                                         |      |      |      |      |
| The DiskThresholdDecider checks that the node a shard is potentially being allocated to has enough disk space. |      |      |      |      |
| EnableAllocationDecider                                      |      |      |      |      |
| This allocation decider allows shard allocations / rebalancing via the cluster wide settings EnableAllocationDecider.CLUSTER_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.CLUSTER_ROUTING_REBALANCE_ENABLE_SETTING and the per index setting EnableAllocationDecider.INDEX_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_REBALANCE_ENABLE_SETTING. |      |      |      |      |
| EnableAllocationDecider.Allocation                           |      |      |      |      |
| Allocation values or rather their string representation to be used used with EnableAllocationDecider.CLUSTER_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_ALLOCATION_ENABLE_SETTING via cluster / index settings. |      |      |      |      |
| EnableAllocationDecider.Rebalance                            |      |      |      |      |
| Rebalance values or rather their string representation to be used used with EnableAllocationDecider.CLUSTER_ROUTING_REBALANCE_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_REBALANCE_ENABLE_SETTING via cluster / index settings. |      |      |      |      |
| FilterAllocationDecider                                      |      |      |      |      |
| This AllocationDecider control shard allocation by include and exclude filters via dynamic cluster and index routing settings. |      |      |      |      |
| MaxRetryAllocationDecider                                    |      |      |      |      |
| An allocation decider that prevents shards from being allocated on any node if the shards allocation has been retried N times without success. |      |      |      |      |
| NodeReplacementAllocationDecider                             |      |      |      |      |
| An allocation decider that ensures that all the shards allocated to the node scheduled for removal are relocated to the replacement node. |      |      |      |      |
| NodeShutdownAllocationDecider                                |      |      |      |      |
| An allocation decider that prevents shards from being allocated to a node that is in the process of shutting down. |      |      |      |      |
| NodeVersionAllocationDecider                                 |      |      |      |      |
| An allocation decider that prevents relocation or allocation from nodes that might not be version compatible. |      |      |      |      |
| RebalanceOnlyWhenActiveAllocationDecider                     |      |      |      |      |
| Only allow rebalancing when all shards are active within the shard replication group. |      |      |      |      |
| ReplicaAfterPrimaryActiveAllocationDecider                   |      |      |      |      |
| An allocation strategy that only allows for a replica to be allocated when the primary is active. |      |      |      |      |
| ResizeAllocationDecider                                      |      |      |      |      |
| An allocation decider that ensures we allocate the shards of a target index for resize operations next to the source primaries |      |      |      |      |
| RestoreInProgressAllocationDecider                           |      |      |      |      |
| This AllocationDecider prevents shards that have failed to be restored from a snapshot to be allocated. |      |      |      |      |
| SameShardAllocationDecider                                   |      |      |      |      |
| An allocation decider that prevents multiple instances of the same shard to be allocated on the same node. |      |      |      |      |
| ShardsLimitAllocationDecider                                 |      |      |      |      |
| This AllocationDecider limits the number of shards per node on a per index or node-wide basis. |      |      |      |      |
| SnapshotInProgressAllocationDecider                          |      |      |      |      |
| This AllocationDecider prevents shards that are currently been snapshotted to be moved to other nodes. |      |      |      |      |
| ThrottlingAllocationDecider                                  |      |      |      |      |
| ThrottlingAllocationDecider controls the recovery process per node in the cluster. |      |      |      |      |





org.elasticsearch.cluster.service





| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ClusterApplier                                               |      |      |      |
|                                                              |      |      |      |
| ClusterApplierRecordingService                               |      |      |      |
|                                                              |      |      |      |
| ClusterApplierRecordingService.Stats                         |      |      |      |
|                                                              |      |      |      |
| ClusterApplierRecordingService.Stats.Recording               |      |      |      |
|                                                              |      |      |      |
| ClusterApplierService                                        |      |      |      |
|                                                              |      |      |      |
| ClusterService                                               |      |      |      |
|                                                              |      |      |      |
| ClusterStateUpdateStats                                      |      |      |      |
| Various statistics (timing information etc) about cluster state updates coordinated by this node. |      |      |      |
| MasterService                                                |      |      |      |
|                                                              |      |      |      |
| PendingClusterTask                                           |      |      |      |
|                                                              |      |      |      |
| SourcePrioritizedRunnable                                    |      |      |      |
| PrioritizedRunnable that also has a source string            |      |      |      |
| TaskBatcher                                                  |      |      |      |
| Batching support for PrioritizedEsThreadPoolExecutor Tasks that share the same batching key are batched (see TaskBatcher.BatchedTask.batchingKey) |      |      |      |





org.elasticsearch.common





org.elasticsearch.common.blobstore







org.elasticsearch.common.blobstore.fs









org.elasticsearch.common.blobstore.support
org.elasticsearch.common.breaker
org.elasticsearch.common.bytes
org.elasticsearch.common.cache
org.elasticsearch.common.collect
org.elasticsearch.common.component
org.elasticsearch.common.compress
org.elasticsearch.common.document
org.elasticsearch.common.filesystem
org.elasticsearch.common.geo
org.elasticsearch.common.hash
org.elasticsearch.common.inject
org.elasticsearch.common.inject.assistedinject
org.elasticsearch.common.inject.binder
org.elasticsearch.common.inject.internal
org.elasticsearch.common.inject.matcher
org.elasticsearch.common.inject.multibindings
org.elasticsearch.common.inject.name
org.elasticsearch.common.inject.spi
org.elasticsearch.common.inject.util
org.elasticsearch.common.io
org.elasticsearch.common.io.stream
org.elasticsearch.common.joda
org.elasticsearch.common.logging
org.elasticsearch.common.lucene
org.elasticsearch.common.lucene.index
org.elasticsearch.common.lucene.search
org.elasticsearch.common.lucene.search.function
org.elasticsearch.common.lucene.store
org.elasticsearch.common.lucene.uid
org.elasticsearch.common.metrics
org.elasticsearch.common.network
org.elasticsearch.common.path
org.elasticsearch.common.recycler
org.elasticsearch.common.regex
org.elasticsearch.common.rounding
org.elasticsearch.common.settings
org.elasticsearch.common.text
org.elasticsearch.common.time
org.elasticsearch.common.transport
org.elasticsearch.common.unit
org.elasticsearch.common.util
org.elasticsearch.common.util.concurrent
org.elasticsearch.common.util.iterable
org.elasticsearch.common.util.set
org.elasticsearch.common.xcontent
org.elasticsearch.common.xcontent.support
