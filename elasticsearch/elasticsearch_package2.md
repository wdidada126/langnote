# elasticsearch_package

## org.elasticsearch





### org.elasticsearch.cli



| Class                      | Description                                                  |      |      |
| -------------------------- | ------------------------------------------------------------ | ---- | ---- |
| CommandLoggingConfigurator | Holder class for method to configure logging without Elasticsearch configuration files for use in CLI tools that will not read such files. |      |      |
| EnvironmentAwareCommand    | A cli command which requires an Environment to use current paths and settings. |      |      |
| KeyStoreAwareCommand       | An EnvironmentAwareCommand that needs to access the elasticsearch keystore, possibly decrypting it if it is password protected. |      |      |
| LoggingAwareCommand        | A command that is aware of logging.                          |      |      |
| LoggingAwareMultiCommand   | A multi-command that is aware of logging.                    |      |      |







org.elasticsearch.client



| Class                     | Description                                                  |      |      |
| ------------------------- | ------------------------------------------------------------ | ---- | ---- |
| AdminClient               | Administrative actions/operations against the cluster or the indices. |      |      |
| Client                    | A client provides a one stop interface for performing actions/operations against the cluster. |      |      |
| ClusterAdminClient        | Administrative actions/operations against indices.           |      |      |
| ElasticsearchClient       |                                                              |      |      |
| FilterClient              | A Client that contains another Client which it uses as its basic source, possibly transforming the requests / responses along the way or providing additional functionality. |      |      |
| IndicesAdminClient        | Administrative actions/operations against indices.           |      |      |
| OriginSettingClient       | A Client that sends requests with the origin set to a particular value and calls its ActionListener in its original ThreadContext. |      |      |
| ParentTaskAssigningClient | A Client that sets the parent task on all requests that it makes. |      |      |
| Requests                  | A handy one stop shop for creating requests (make sure to import static this class). |      |      |





org.elasticsearch.client.node







| Class      | Description                                     |      |
| ---------- | ----------------------------------------------- | ---- |
| NodeClient | Client that executes actions on the local node. |      |



org.elasticsearch.client.support

| Class          | Description |      |
| -------------- | ----------- | ---- |
| AbstractClient |             |      |





org.elasticsearch.client.transport



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| NoNodeAvailableException                                     | An exception indicating no node is available to perform the operation. |      |      |
| TransportClient                                              | Deprecated.                                                  |      |      |
| TransportClient聽is deprecated in favour of the High Level REST client and will be removed in Elasticsearch 8.0. |                                                              |      |      |
| TransportClient.HostFailureListener                          | Listener that allows to be notified whenever a node failure / disconnect happens |      |      |



org.elasticsearch.cluster

| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
|                                                              |                                                              |      |      |
| AbstractDiffable<T extends Diffable<T>>                      | Abstract diffable object with simple diffs implementation that sends the entire object if object has changed or nothing if object remained the same. |      |      |
|                                                              |                                                              |      |      |
| AbstractNamedDiffable<T extends NamedDiffable<T>>            | Abstract diffable object with simple diffs implementation that sends the entire object if object has changed or nothing is object remained the same. |      |      |
|                                                              |                                                              |      |      |
| AckedClusterStateTaskListener                                |                                                              |      |      |
|                                                              |                                                              |      |      |
| AckedClusterStateUpdateTask                                  | An extension interface to ClusterStateUpdateTask that allows to be notified when all the nodes have acknowledged a cluster state update request |      |      |
|                                                              |                                                              |      |      |
| ClusterChangedEvent                                          | An event received by the local node, signaling that the cluster state has changed. |      |      |
|                                                              |                                                              |      |      |
| ClusterInfo                                                  | ClusterInfo is an object representing a map of nodes to DiskUsage and a map of shard ids to shard sizes, see InternalClusterInfoService.shardIdentifierFromRouting(String) for the key used in the shardSizes map |      |      |
|                                                              |                                                              |      |      |
| ClusterInfo.NodeAndPath                                      | Represents a data path on a node                             |      |      |
|                                                              |                                                              |      |      |
| ClusterInfo.ReservedSpace                                    | Represents the total amount of "reserved" space on a particular data path, together with the set of shards considered. |      |      |
|                                                              |                                                              |      |      |
| ClusterInfo.ReservedSpace.Builder                            |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterInfoService                                           | Interface for a class used to gather information about a cluster periodically. |      |      |
|                                                              |                                                              |      |      |
| ClusterModule                                                | Configures classes and services that affect the entire cluster. |      |      |
|                                                              |                                                              |      |      |
| ClusterName                                                  |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterState                                                 | Represents the current state of the cluster.                 |      |      |
|                                                              |                                                              |      |      |
| ClusterState.Builder                                         |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterState.Custom                                          |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterState.FeatureAware                                    | An interface that implementors use when a class requires a client to maybe have a feature. |      |      |
|                                                              |                                                              |      |      |
| ClusterState.Metric                                          |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateApplier                                          | A component that is in charge of applying an incoming cluster state to the node internal data structures. |      |      |
|                                                              |                                                              |      |      |
| ClusterStateListener                                         | A listener to be notified when a cluster state changes.      |      |      |
|                                                              |                                                              |      |      |
| ClusterStateObserver                                         | A utility class which simplifies interacting with the cluster state in cases where one tries to take action based on the current state but may want to wait for a new state and retry upon failure. |      |      |
|                                                              |                                                              |      |      |
| ClusterStateObserver.Listener                                |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStatePublicationEvent                                 | Represents a cluster state update computed by the MasterService for publication to the cluster. |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskConfig                                       | Cluster state update task configuration for timeout and priority |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskConfig.Basic                                 |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskExecutor<T>                                  |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskExecutor.ClusterTasksResult<T>               | Represents the result of a batched execution of cluster state update tasks |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskExecutor.ClusterTasksResult.Builder<T>       |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskExecutor.TaskResult                          |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateTaskListener                                     |                                                              |      |      |
|                                                              |                                                              |      |      |
| ClusterStateUpdateTask                                       | A task that can update the cluster state.                    |      |      |
|                                                              |                                                              |      |      |
| Diff<T>                                                      | Represents difference between states of cluster state parts  |      |      |
|                                                              |                                                              |      |      |
| Diffable<T>                                                  | Cluster state part, changes in which can be serialized       |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils                                                |                                                              |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.DiffableValueReader<K,V extends Diffable<V>>   | Implementation of the ValueSerializer that wraps value and diff readers. |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.DiffableValueSerializer<K,V extends Diffable<V>> | Serializer for Diffable map values.                          |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.ImmutableOpenMapDiff<K,T>                      | Represents differences between two ImmutableOpenMap of (possibly diffable) objects |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.KeySerializer<K>                               | Provides read and write operations to serialize keys of map  |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.MapDiff<K,T,M>                                 | Represents differences between two maps of objects and is used as base class for different map implementations. |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.NonDiffableValueSerializer<K,V>                | Serializer for non-diffable map values                       |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.StringSetValueSerializer<K>                    | Implementation of ValueSerializer that serializes immutable sets |      |      |
|                                                              |                                                              |      |      |
| DiffableUtils.ValueSerializer<K,V>                           | Provides read and write operations to serialize map values.  |      |      |
|                                                              |                                                              |      |      |
| DiskUsage                                                    | Encapsulation class used to represent the amount of disk used on a node. |      |      |
|                                                              |                                                              |      |      |
| EmptyClusterInfoService                                      | ClusterInfoService that provides empty maps for disk usage and shard sizes |      |      |
|                                                              |                                                              |      |      |
| IncompatibleClusterStateVersionException                     | Thrown by Diff.apply(T) method                               |      |      |
|                                                              |                                                              |      |      |
| InternalClusterInfoService                                   | InternalClusterInfoService provides the ClusterInfoService interface, routinely updated on a timer. |      |      |
|                                                              |                                                              |      |      |
| LocalClusterUpdateTask                                       | Used to apply state updates on nodes that are not necessarily master |      |      |
|                                                              |                                                              |      |      |
| LocalNodeMasterListener                                      | Enables listening to master changes events of the local node (when the local node becomes the master, and when the local node cease being a master). |      |      |
|                                                              |                                                              |      |      |
| MasterNodeChangePredicate                                    |                                                              |      |      |
|                                                              |                                                              |      |      |
| MergableCustomMetadata<T extends Metadata.Custom>            | Interface to allow merging Metadata.Custom.                  |      |      |
|                                                              |                                                              |      |      |
| NamedDiff<T extends Diffable<T>>                             | Diff that also support NamedWriteable interface              |      |      |
|                                                              |                                                              |      |      |
| NamedDiffable<T>                                             | Diff that also support VersionedNamedWriteable interface     |      |      |
|                                                              |                                                              |      |      |
| NamedDiffableValueSerializer<T extends NamedDiffable<T>>     | Value Serializer for named diffables                         |      |      |
|                                                              |                                                              |      |      |
| NodeConnectionsService                                       | This component is responsible for maintaining connections from this node to all the nodes listed in the cluster state, and for disconnecting from nodes once they are removed from the cluster state. |      |      |
|                                                              |                                                              |      |      |
| NotMasterException                                           | Thrown when a node join request or a master ping reaches a node which is not currently acting as a master or when a cluster state update task is to be executed on a node that is no longer master. |      |      |
|                                                              |                                                              |      |      |
| RepositoryCleanupInProgress                                  |                                                              |      |      |
|                                                              |                                                              |      |      |
| RepositoryCleanupInProgress.Entry                            |                                                              |      |      |
|                                                              |                                                              |      |      |
| RestoreInProgress                                            | Meta data about restore processes that are currently executing |      |      |
|                                                              |                                                              |      |      |
| RestoreInProgress.Builder                                    |                                                              |      |      |
|                                                              |                                                              |      |      |
| RestoreInProgress.Entry                                      | Restore metadata                                             |      |      |
|                                                              |                                                              |      |      |
| RestoreInProgress.ShardRestoreStatus                         | Represents status of a restored shard                        |      |      |
|                                                              |                                                              |      |      |
| RestoreInProgress.State                                      | Shard restore process state                                  |      |      |
|                                                              |                                                              |      |      |
| SnapshotDeletionsInProgress                                  | A class that represents the snapshot deletions that are in progress in the cluster. |      |      |
|                                                              |                                                              |      |      |
| SnapshotDeletionsInProgress.Entry                            | A class representing a snapshot deletion request entry in the cluster state. |      |      |
|                                                              |                                                              |      |      |
| SnapshotDeletionsInProgress.State                            |                                                              |      |      |
|                                                              |                                                              |      |      |
| SnapshotsInProgress                                          | Meta data about snapshots that are currently executing       |      |      |
|                                                              |                                                              |      |      |
| SnapshotsInProgress.Entry                                    |                                                              |      |      |
|                                                              |                                                              |      |      |
| SnapshotsInProgress.ShardSnapshotStatus                      |                                                              |      |      |
|                                                              |                                                              |      |      |
| SnapshotsInProgress.ShardState                               |                                                              |      |      |
|                                                              |                                                              |      |      |
| SnapshotsInProgress.State                                    |                                                              |      |      |
|                                                              |                                                              |      |      |
| TimeoutClusterStateListener                                  | An exception to cluster state listener that allows for timeouts and for post added notifications. |      |      |
|                                                              |                                                              |      |      |



org.elasticsearch.cluster.ack



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
|                                                              |                                                              |      |      |
| AckedRequest                                                 | Identifies a cluster state update request with acknowledgement support |      |      |
|                                                              |                                                              |      |      |
| ClusterStateUpdateRequest<T extends ClusterStateUpdateRequest<T>> | Base class to be used when needing to update the cluster state Contains the basic fields that are always needed |      |      |
|                                                              |                                                              |      |      |
| IndicesClusterStateUpdateRequest<T extends IndicesClusterStateUpdateRequest<T>> | Base cluster state update request that allows to execute update against multiple indices |      |      |
|                                                              |                                                              |      |      |



org.elasticsearch.cluster.action.index





| Class                | Description                                                  |      |
| -------------------- | ------------------------------------------------------------ | ---- |
|                      |                                                              |      |
| MappingUpdatedAction | Called by shards in the cluster when their mapping was dynamically updated and it needs to be updated in the cluster state meta data (and broadcast to all members). |      |
|                      |                                                              |      |



org.elasticsearch.cluster.action.shard



| Class                                                 | Description |      |      |
| ----------------------------------------------------- | ----------- | ---- | ---- |
| ShardStateAction                                      |             |      |      |
| ShardStateAction.FailedShardEntry                     |             |      |      |
| ShardStateAction.NoLongerPrimaryShardException        |             |      |      |
| ShardStateAction.ShardFailedClusterStateTaskExecutor  |             |      |      |
| ShardStateAction.ShardStartedClusterStateTaskExecutor |             |      |      |
| ShardStateAction.StartedShardEntry                    |             |      |      |



org.elasticsearch.cluster.block

| Class                 | Description                                                  |      |      |
| --------------------- | ------------------------------------------------------------ | ---- | ---- |
| ClusterBlock          |                                                              |      |      |
| ClusterBlockException |                                                              |      |      |
| ClusterBlockLevel     |                                                              |      |      |
| ClusterBlocks         | Represents current cluster level blocks to block dirty operations done against the cluster. |      |      |
| ClusterBlocks.Builder |                                                              |      |      |



org.elasticsearch.cluster.coordination



| Class                                          | Description                                                  |      |      |
| ---------------------------------------------- | ------------------------------------------------------------ | ---- | ---- |
| ApplyCommitRequest                             | A master node sends this request to its peers to inform them that it could commit the cluster state with the given term and version. |      |      |
| ClusterBootstrapService                        |                                                              |      |      |
| ClusterFormationFailureHelper                  |                                                              |      |      |
| ClusterStatePublisher                          |                                                              |      |      |
| ClusterStatePublisher.AckListener              |                                                              |      |      |
| ClusterStateSerializationStats                 |                                                              |      |      |
| CoordinationMetadata                           |                                                              |      |      |
| CoordinationMetadata.Builder                   |                                                              |      |      |
| CoordinationMetadata.VotingConfigExclusion     |                                                              |      |      |
| CoordinationMetadata.VotingConfiguration       | A collection of persistent node ids, denoting the voting configuration for cluster state changes. |      |      |
| CoordinationState                              | The core class of the cluster state coordination algorithm, directly implementing the formal model |      |      |
| CoordinationState.PersistedState               | Pluggable persistence layer for CoordinationState.           |      |      |
| CoordinationState.VoteCollection               | A collection of votes, used to calculate quorums.            |      |      |
| CoordinationStateRejectedException             | This exception is thrown when rejecting state transitions on the CoordinationState object, for example when receiving a publish request with the wrong term or version. |      |      |
| Coordinator                                    |                                                              |      |      |
| Coordinator.Mode                               |                                                              |      |      |
| DetachClusterCommand                           |                                                              |      |      |
| DiscoveryUpgradeService                        | Deals with rolling upgrades of the cluster coordination layer. |      |      |
| ElasticsearchNodeCommand                       |                                                              |      |      |
| ElasticsearchNodeCommand.UnknownCondition      |                                                              |      |      |
| ElasticsearchNodeCommand.UnknownMetadataCustom |                                                              |      |      |
| ElectionSchedulerFactory                       | It's provably impossible to guarantee that any leader election algorithm ever elects a leader, but they generally work (with probability that approaches 1 over time) as long as elections occur sufficiently infrequently, compared to the time it takes to send a message to another node and receive a response back. |      |      |
| ElectionStrategy                               | Allows plugging in a custom election strategy, restricting the notion of an election quorum. |      |      |
| FailedToCommitClusterStateException            | Thrown when failing to publish a cluster state.              |      |      |
| FollowersChecker                               | The FollowersChecker is responsible for allowing a leader to check that its followers are still connected and healthy. |      |      |
| FollowersChecker.FollowerCheckRequest          |                                                              |      |      |
| InMemoryPersistedState                         |                                                              |      |      |
| Join                                           | Triggered by a StartJoinRequest, instances of this class represent join votes, and have a source and target node. |      |      |
| JoinHelper                                     |                                                              |      |      |
| JoinRequest                                    |                                                              |      |      |
| JoinTaskExecutor                               |                                                              |      |      |
| JoinTaskExecutor.Task                          |                                                              |      |      |
| LagDetector                                    | A publication can succeed and complete before all nodes have applied the published state and acknowledged it; however we need every node eventually either to apply the published state (or a later state) or be removed from the cluster. |      |      |
| LagDetector.LagListener                        |                                                              |      |      |
| LeaderChecker                                  | The LeaderChecker is responsible for allowing followers to check that the currently elected leader is still connected and healthy. |      |      |
| NodeHealthCheckFailureException                | This exception is thrown if the File system is reported unhealthy by @FsHealthService and this nodes needs to be removed from the cluster |      |      |
| NodeRemovalClusterStateTaskExecutor            |                                                              |      |      |
| NodeRemovalClusterStateTaskExecutor.Task       |                                                              |      |      |
| NodeToolCli                                    |                                                              |      |      |
| NoMasterBlockService                           |                                                              |      |      |
| PeersResponse                                  |                                                              |      |      |
| PreVoteCollector                               |                                                              |      |      |
| PreVoteRequest                                 |                                                              |      |      |
| PreVoteResponse                                |                                                              |      |      |
| Publication                                    |                                                              |      |      |
| PublicationTransportHandler                    |                                                              |      |      |
| PublishRequest                                 | Request which is used by the master node to publish cluster state changes. |      |      |
| PublishResponse                                | Response to a PublishRequest, carrying the term and version of the request. |      |      |
| PublishWithJoinResponse                        | Response to a PublishRequest.                                |      |      |
| Reconfigurator                                 | Computes the optimal configuration of voting nodes in the cluster. |      |      |
| RemoveCustomsCommand                           |                                                              |      |      |
| RemoveSettingsCommand                          |                                                              |      |      |
| StartJoinRequest                               | Represents the action of requesting a join vote (see Join) from a node. |      |      |
| UnsafeBootstrapMasterCommand                   |                                                              |      |      |
| ValidateJoinRequest                            |                                                              |      |      |





org.elasticsearch.cluster.health



| Class               | Description |      |
| ------------------- | ----------- | ---- |
|                     |             |      |
| ClusterHealthStatus |             |      |
|                     |             |      |
| ClusterIndexHealth  |             |      |
|                     |             |      |
| ClusterShardHealth  |             |      |
|                     |             |      |
| ClusterStateHealth  |             |      |



org.elasticsearch.cluster.metadata

| Class                                                        | Description                                                  |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
|                                                              |                                                              |      |
| AliasAction                                                  | Individual operation to perform on the cluster state as part of an IndicesAliasesRequest. |      |
|                                                              |                                                              |      |
| AliasAction.Add                                              | Operation to add an alias to an index.                       |      |
|                                                              |                                                              |      |
| AliasAction.AddDataStreamAlias                               |                                                              |      |
|                                                              |                                                              |      |
| AliasAction.NewAliasValidator                                | Validate a new alias.                                        |      |
|                                                              |                                                              |      |
| AliasAction.Remove                                           | Operation to remove an alias from an index.                  |      |
|                                                              |                                                              |      |
| AliasAction.RemoveDataStreamAlias                            |                                                              |      |
|                                                              |                                                              |      |
| AliasAction.RemoveIndex                                      | Operation to remove an index.                                |      |
|                                                              |                                                              |      |
| AliasMetadata                                                |                                                              |      |
|                                                              |                                                              |      |
| AliasMetadata.Builder                                        |                                                              |      |
|                                                              |                                                              |      |
| AliasValidator                                               | Validator for an alias, to be used before adding an alias to the index metadata and make sure the alias is valid |      |
|                                                              |                                                              |      |
| AutoExpandReplicas                                           | This class acts as a functional wrapper around the index.auto_expand_replicas setting. |      |
|                                                              |                                                              |      |
| ClusterNameExpressionResolver                                | Resolves cluster names from an expression.                   |      |
|                                                              |                                                              |      |
| ComponentTemplate                                            | A component template is a re-usable Template as well as metadata about the template. |      |
|                                                              |                                                              |      |
| ComponentTemplateMetadata                                    | ComponentTemplateMetadata is a custom Metadata implementation for storing a map of component templates and their names. |      |
|                                                              |                                                              |      |
| ComposableIndexTemplate                                      | An index template is comprised of a set of index patterns, an optional template, and a list of ids corresponding to component templates that should be composed in order when creating a new index. |      |
|                                                              |                                                              |      |
| ComposableIndexTemplate.Builder                              |                                                              |      |
|                                                              |                                                              |      |
| ComposableIndexTemplate.DataStreamTemplate                   |                                                              |      |
|                                                              |                                                              |      |
| ComposableIndexTemplateMetadata                              | The ComposableIndexTemplateMetadata class is a custom Metadata.Custom implementation that stores a map of ids to ComposableIndexTemplate templates. |      |
|                                                              |                                                              |      |
| DataStream                                                   |                                                              |      |
|                                                              |                                                              |      |
| DataStream.TimestampField                                    |                                                              |      |
|                                                              |                                                              |      |
| DataStreamAction                                             | Operations on data streams.                                  |      |
|                                                              |                                                              |      |
| DataStreamAction.Type                                        |                                                              |      |
|                                                              |                                                              |      |
| DataStreamAlias                                              |                                                              |      |
|                                                              |                                                              |      |
| DataStreamMetadata                                           | Custom Metadata implementation for storing a map of DataStreams and their names. |      |
|                                                              |                                                              |      |
| DiffableStringMap                                            | This is a Map<String, String> that implements AbstractDiffable so it can be used for cluster state purposes |      |
|                                                              |                                                              |      |
| DiffableStringMap.DiffableStringMapDiff                      | Represents differences between two DiffableStringMaps.       |      |
|                                                              |                                                              |      |
| IndexAbstraction                                             | An index abstraction is a reference to one or more concrete indices. |      |
|                                                              |                                                              |      |
| IndexAbstraction.Alias                                       | Represents an alias and groups all IndexMetadata instances sharing the same alias name together. |      |
|                                                              |                                                              |      |
| IndexAbstraction.ConcreteIndex                               | Represents an concrete index and encapsulates its IndexMetadata |      |
|                                                              |                                                              |      |
| IndexAbstraction.DataStream                                  |                                                              |      |
|                                                              |                                                              |      |
| IndexAbstraction.Type                                        | An index abstraction type.                                   |      |
|                                                              |                                                              |      |
| IndexAbstractionResolver                                     |                                                              |      |
|                                                              |                                                              |      |
| IndexGraveyard                                               | A collection of tombstones for explicitly marking indices as deleted in the cluster state. |      |
|                                                              |                                                              |      |
| IndexGraveyard.Builder                                       | A class to build an IndexGraveyard.                          |      |
|                                                              |                                                              |      |
| IndexGraveyard.IndexGraveyardDiff                            | A class representing a diff of two IndexGraveyard objects.   |      |
|                                                              |                                                              |      |
| IndexGraveyard.Tombstone                                     | An individual tombstone entry for representing a deleted index. |      |
|                                                              |                                                              |      |
| IndexMetadata                                                |                                                              |      |
|                                                              |                                                              |      |
| IndexMetadata.APIBlock                                       |                                                              |      |
|                                                              |                                                              |      |
| IndexMetadata.Builder                                        |                                                              |      |
|                                                              |                                                              |      |
| IndexMetadata.State                                          |                                                              |      |
|                                                              |                                                              |      |
| IndexMetadataVerifier                                        | This service is responsible for verifying index metadata when an index is introduced to the cluster, for example when restarting nodes, importing dangling indices, or restoring an index from a snapshot repository. |      |
|                                                              |                                                              |      |
| IndexNameExpressionResolver                                  |                                                              |      |
|                                                              |                                                              |      |
| IndexNameExpressionResolver.Context                          |                                                              |      |
|                                                              |                                                              |      |
| IndexNameExpressionResolver.DateMathExpressionResolver       |                                                              |      |
|                                                              |                                                              |      |
| IndexNameExpressionResolver.ResolverContext                  | This is a context for the DateMathExpressionResolver which does not require IndicesOptions or ClusterState since it uses only the start time to resolve expressions. |      |
|                                                              |                                                              |      |
| IndexTemplateMetadata                                        |                                                              |      |
|                                                              |                                                              |      |
| IndexTemplateMetadata.Builder                                |                                                              |      |
|                                                              |                                                              |      |
| ItemUsage                                                    | A class encapsulating the usage of a particular "thing" by something else |      |
|                                                              |                                                              |      |
| Manifest                                                     | This class represents the manifest file, which is the entry point for reading meta data from disk. |      |
|                                                              |                                                              |      |
| MappingMetadata                                              | Mapping configuration for a type.                            |      |
|                                                              |                                                              |      |
| MappingMetadata.Routing                                      |                                                              |      |
|                                                              |                                                              |      |
| Metadata                                                     | Metadata is the part of the ClusterState which persists across restarts. |      |
|                                                              |                                                              |      |
| Metadata.Builder                                             |                                                              |      |
|                                                              |                                                              |      |
| Metadata.Custom                                              | Custom metadata that persists (via XContent) across restarts. |      |
|                                                              |                                                              |      |
| Metadata.NonRestorableCustom                                 |                                                              |      |
|                                                              |                                                              |      |
| Metadata.XContentContext                                     |                                                              |      |
|                                                              |                                                              |      |
| MetadataCreateDataStreamService                              |                                                              |      |
|                                                              |                                                              |      |
| MetadataCreateDataStreamService.CreateDataStreamClusterStateUpdateRequest |                                                              |      |
|                                                              |                                                              |      |
| MetadataCreateIndexService                                   | Service responsible for submitting create index requests     |      |
|                                                              |                                                              |      |
| MetadataDataStreamsService                                   | Handles data stream modification requests.                   |      |
|                                                              |                                                              |      |
| MetadataDeleteIndexService                                   | Deletes indices.                                             |      |
|                                                              |                                                              |      |
| MetadataIndexAliasesService                                  | Service responsible for submitting add and remove aliases requests |      |
|                                                              |                                                              |      |
| MetadataIndexStateService                                    | Service responsible for submitting open/close index requests as well as for adding index blocks |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService                                 | Service responsible for submitting index templates updates   |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService.PutListener                     |                                                              |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService.PutRequest                      |                                                              |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService.PutResponse                     |                                                              |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService.RemoveListener                  |                                                              |      |
|                                                              |                                                              |      |
| MetadataIndexTemplateService.RemoveRequest                   |                                                              |      |
|                                                              |                                                              |      |
| MetadataMappingService                                       | Service responsible for submitting mapping changes           |      |
|                                                              |                                                              |      |
| MetadataMigrateToDataStreamService                           |                                                              |      |
|                                                              |                                                              |      |
| MetadataMigrateToDataStreamService.MigrateToDataStreamClusterStateUpdateRequest |                                                              |      |
|                                                              |                                                              |      |
| MetadataUpdateSettingsService                                | Service responsible for submitting update index settings requests |      |
|                                                              |                                                              |      |
| NodesShutdownMetadata                                        | Contains the data about nodes which are currently configured to shut down, either permanently or temporarily. |      |
|                                                              |                                                              |      |
| NodesShutdownMetadata.NodeShutdownMetadataDiff               | Handles diffing and appling diffs for NodesShutdownMetadata as necessary for the cluster state infrastructure. |      |
|                                                              |                                                              |      |
| ProcessClusterEventTimeoutException                          |                                                              |      |
|                                                              |                                                              |      |
| RepositoriesMetadata                                         | Contains metadata about registered snapshot repositories     |      |
|                                                              |                                                              |      |
| RepositoryMetadata                                           | Metadata about registered repository                         |      |
|                                                              |                                                              |      |
| ShutdownPersistentTasksStatus                                |                                                              |      |
|                                                              |                                                              |      |
| ShutdownPluginsStatus                                        |                                                              |      |
|                                                              |                                                              |      |
| ShutdownShardMigrationStatus                                 |                                                              |      |
|                                                              |                                                              |      |
| SingleNodeShutdownMetadata                                   | Contains data about a single node's shutdown readiness.      |      |
|                                                              |                                                              |      |
| SingleNodeShutdownMetadata.Builder                           |                                                              |      |
|                                                              |                                                              |      |
| SingleNodeShutdownMetadata.Status                            | Describes the status of a component of shutdown.             |      |
|                                                              |                                                              |      |
| SingleNodeShutdownMetadata.Type                              | Describes the type of node shutdown - permanent (REMOVE) or temporary (RESTART). |      |
|                                                              |                                                              |      |
| SystemIndexMetadataUpgradeService                            | A service responsible for updating the metadata used by system indices. |      |
|                                                              |                                                              |      |
| Template                                                     | A template consists of optional settings, mappings, or alias configuration for an index, however, it is entirely independent from an index. |      |
|                                                              |                                                              |      |
| TemplateUpgradeService                                       | Upgrades Templates on behalf of installed Plugins when a node joins the cluster |      |
|                                                              |                                                              |      |



org.elasticsearch.cluster.node



| Class                       | Description                                                  |      |
| --------------------------- | ------------------------------------------------------------ | ---- |
|                             |                                                              |      |
| DiscoveryNode               | A discovery node represents a node that is part of the cluster. |      |
|                             |                                                              |      |
| DiscoveryNodeFilters        |                                                              |      |
|                             |                                                              |      |
| DiscoveryNodeFilters.OpType |                                                              |      |
|                             |                                                              |      |
| DiscoveryNodeRole           | Represents a node role.                                      |      |
|                             |                                                              |      |
| DiscoveryNodes              | This class holds all DiscoveryNode in the cluster and provides convenience methods to access, modify merge / diff discovery nodes. |      |
|                             |                                                              |      |
| DiscoveryNodes.Builder      |                                                              |      |
|                             |                                                              |      |
| DiscoveryNodes.Delta        |                                                              |      |







org.elasticsearch.cluster.routing







| Class                                                        | Description                                                  |      |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- | ---- |
|                                                              |                                                              |      |      |      |
| AllocationId                                                 | Uniquely identifies an allocation.                           |      |      |      |
|                                                              |                                                              |      |      |      |
| BatchedRerouteService                                        | A BatchedRerouteService is a RerouteService that batches together reroute requests to avoid unnecessary extra reroutes. |      |      |      |
|                                                              |                                                              |      |      |      |
| DelayedAllocationService                                     | The DelayedAllocationService listens to cluster state changes and checks if there are unassigned shards with delayed allocation (unassigned shards that have the delay marker). |      |      |      |
|                                                              |                                                              |      |      |      |
| GroupShardsIterator<ShardIt extends Comparable<ShardIt> & Countable> | This class implements a compilation of ShardIterators.       |      |      |      |
|                                                              |                                                              |      |      |      |
| IllegalShardRoutingStateException                            | This exception defines illegal states of shard routing       |      |      |      |
|                                                              |                                                              |      |      |      |
| IndexRouting                                                 | Generates the shard id for (id, routing) pairs.              |      |      |      |
|                                                              |                                                              |      |      |      |
| IndexRoutingTable                                            | The IndexRoutingTable represents routing information for a single index. |      |      |      |
|                                                              |                                                              |      |      |      |
| IndexRoutingTable.Builder                                    |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| IndexShardRoutingTable                                       | IndexShardRoutingTable encapsulates all instances of a single shard. |      |      |      |
|                                                              |                                                              |      |      |      |
| IndexShardRoutingTable.Builder                               |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| Murmur3HashFunction                                          | Hash function based on the Murmur3 algorithm, which is the default as of Elasticsearch 2.0. |      |      |      |
|                                                              |                                                              |      |      |      |
| OperationRouting                                             |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| PlainShardIterator                                           | The PlainShardIterator is a ShardsIterator which iterates all shards or a given shard id |      |      |      |
|                                                              |                                                              |      |      |      |
| PlainShardsIterator                                          | A simple ShardsIterator that iterates a list or sub-list of shard indexRoutings. |      |      |      |
|                                                              |                                                              |      |      |      |
| Preference                                                   | Routing Preference Type                                      |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource                                               | Represents the recovery source of a shard.                   |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.EmptyStoreRecoverySource                      | Recovery from a fresh copy                                   |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.ExistingStoreRecoverySource                   | Recovery from an existing on-disk store                      |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.LocalShardsRecoverySource                     | recovery from other shards on same node (shrink index action) |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.PeerRecoverySource                            | peer recovery from a primary shard                           |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.SnapshotRecoverySource                        | recovery from a snapshot                                     |      |      |      |
|                                                              |                                                              |      |      |      |
| RecoverySource.Type                                          |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| RerouteService                                               | Asynchronously performs a cluster reroute, updating any shard states and rebalancing the cluster if appropriate. |      |      |      |
|                                                              |                                                              |      |      |      |
| RotationShardShuffler                                        | Basic ShardShuffler implementation that uses an AtomicInteger to generate seeds and uses a rotation to permute shards. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingChangesObserver                                       | Records changes made to RoutingNodes during an allocation round. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingChangesObserver.AbstractRoutingChangesObserver        | Abstract implementation of RoutingChangesObserver that does not take any action. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingChangesObserver.DelegatingRoutingChangesObserver      |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingException                                             | A base Exceptions for all exceptions thrown by routing related operations. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingNode                                                  | A RoutingNode represents a cluster node associated with a single DiscoveryNode including all shards that are hosted on that nodes. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingNodes                                                 | RoutingNodes represents a copy the routing information contained in the cluster state. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingNodes.UnassignedShards                                |                                                              |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingTable                                                 | Represents a global cluster-wide routing table for all indices including the version of the current routing state. |      |      |      |
|                                                              |                                                              |      |      |      |
| RoutingTable.Builder                                         | Builder for the routing table.                               |      |      |      |
|                                                              |                                                              |      |      |      |
| ShardIterator                                                | Allows to iterate over a set of shard instances (routing) within a shard id group. |      |      |      |
|                                                              |                                                              |      |      |      |
| ShardRouting                                                 | ShardRouting immutably encapsulates information about shard indexRoutings like id, state, version, etc. |      |      |      |
|                                                              |                                                              |      |      |      |
| ShardRoutingState                                            | Represents the current state of a ShardRouting as defined by the cluster. |      |      |      |
|                                                              |                                                              |      |      |      |
| ShardShuffler                                                | A shuffler for shards whose primary goal is to balance load. |      |      |      |
|                                                              |                                                              |      |      |      |
| ShardsIterator                                               | Allows to iterate over unrelated shards.                     |      |      |      |
|                                                              |                                                              |      |      |      |
| UnassignedInfo                                               | Holds additional information as to why the shard is in unassigned state. |      |      |      |
|                                                              |                                                              |      |      |      |
| UnassignedInfo.AllocationStatus                              | Captures the status of an unsuccessful allocation attempt for the shard, causing it to remain in the unassigned state. |      |      |      |
|                                                              |                                                              |      |      |      |
| UnassignedInfo.Reason                                        | Reason why the shard is in unassigned state.                 |      |      |      |
|                                                              |                                                              |      |      |      |





org.elasticsearch.cluster.routing.allocation





| Class                                               | Description                                                  |      |      |
| --------------------------------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                                                     |                                                              |      |      |
| AbstractAllocationDecision                          | An abstract class for representing various types of allocation decisions. |      |      |
|                                                     |                                                              |      |      |
| AllocateUnassignedDecision                          | Represents the allocation decision by an allocator for an unassigned shard. |      |      |
|                                                     |                                                              |      |      |
| AllocationDecision                                  | An enum which represents the various decision types that can be taken by the allocators and deciders for allocating a shard to a node. |      |      |
|                                                     |                                                              |      |      |
| AllocationService                                   | This service manages the node allocation of a cluster.       |      |      |
|                                                     |                                                              |      |      |
| AllocationService.CommandsResult                    | this class is used to describe results of applying a set of AllocationCommand |      |      |
|                                                     |                                                              |      |      |
| DataTier                                            | The DataTier class encapsulates the formalization of the "content", "hot", "warm", and "cold" tiers as node roles. |      |      |
|                                                     |                                                              |      |      |
| DataTier.DefaultHotAllocationSettingProvider        | This setting provider injects the setting allocating all newly created indices with index.routing.allocation.include._tier: "data_hot" unless the user overrides the setting while the index is being created (in a create index request for instance) |      |      |
|                                                     |                                                              |      |      |
| DiskThresholdMonitor                                | Listens for a node to go over the high watermark and kicks off an empty reroute if it does. |      |      |
|                                                     |                                                              |      |      |
| DiskThresholdSettings                               | A container to keep settings for disk thresholds up to date with cluster setting changes. |      |      |
|                                                     |                                                              |      |      |
| ExistingShardsAllocator                             | Searches for, and allocates, shards for which there is an existing on-disk copy somewhere in the cluster. |      |      |
|                                                     |                                                              |      |      |
| ExistingShardsAllocator.UnassignedAllocationHandler | Used by ExistingShardsAllocator.allocateUnassigned(org.elasticsearch.cluster.routing.ShardRouting, org.elasticsearch.cluster.routing.allocation.RoutingAllocation, org.elasticsearch.cluster.routing.allocation.ExistingShardsAllocator.UnassignedAllocationHandler) to handle its allocation decisions. |      |      |
|                                                     |                                                              |      |      |
| FailedShard                                         | A class representing a failed shard.                         |      |      |
|                                                     |                                                              |      |      |
| IndexMetadataUpdater                                | Observer that tracks changes made to RoutingNodes in order to update the primary terms and in-sync allocation ids in IndexMetadata once the allocation round has completed. |      |      |
|                                                     |                                                              |      |      |
| MoveDecision                                        | Represents a decision to move a started shard, either because it is no longer allowed to remain on its current node or because moving it to another node will form a better cluster balance. |      |      |
|                                                     |                                                              |      |      |
| NodeAllocationResult                                | This class represents the shard allocation decision and its explanation for a single node. |      |      |
|                                                     |                                                              |      |      |
| NodeAllocationResult.ShardStoreInfo                 | A class that captures metadata about a shard store on a node. |      |      |
|                                                     |                                                              |      |      |
| RerouteExplanation                                  | Class encapsulating the explanation for a single AllocationCommand taken from the Deciders |      |      |
|                                                     |                                                              |      |      |
| RoutingAllocation                                   | The RoutingAllocation keep the state of the current allocation of shards and holds the AllocationDeciders which are responsible for the current routing state. |      |      |
|                                                     |                                                              |      |      |
| RoutingAllocation.DebugMode                         |                                                              |      |      |
|                                                     |                                                              |      |      |
| RoutingExplanations                                 | Class used to encapsulate a number of RerouteExplanation explanations. |      |      |
|                                                     |                                                              |      |      |
| RoutingNodesChangedObserver                         | Records if changes were made to RoutingNodes during an allocation round. |      |      |
|                                                     |                                                              |      |      |
| ShardAllocationDecision                             | Represents the decision taken for the allocation of a single shard. |      |      |
|                                                     |                                                              |      |      |
| StaleShard                                          | A class that represents a stale shard copy.                  |      |      |
|                                                     |                                                              |      |      |



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



| Class                                                        | Description                                                  |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
|                                                              |                                                              |      |
| AbstractAllocateAllocationCommand                            | Abstract base class for allocating an unassigned shard to a node |      |
|                                                              |                                                              |      |
| AbstractAllocateAllocationCommand.Builder<T extends AbstractAllocateAllocationCommand> | Works around ObjectParser not supporting constructor arguments. |      |
|                                                              |                                                              |      |
| AllocateEmptyPrimaryAllocationCommand                        | Allocates an unassigned empty primary shard to a specific node. |      |
|                                                              |                                                              |      |
| AllocateEmptyPrimaryAllocationCommand.Builder                |                                                              |      |
|                                                              |                                                              |      |
| AllocateReplicaAllocationCommand                             | Allocates an unassigned replica shard to a specific node.    |      |
|                                                              |                                                              |      |
| AllocateReplicaAllocationCommand.Builder                     |                                                              |      |
|                                                              |                                                              |      |
| AllocateStalePrimaryAllocationCommand                        | Allocates an unassigned stale primary shard to a specific node. |      |
|                                                              |                                                              |      |
| AllocateStalePrimaryAllocationCommand.Builder                |                                                              |      |
|                                                              |                                                              |      |
| AllocationCommand                                            | A command to move shards in some way.                        |      |
|                                                              |                                                              |      |
| AllocationCommands                                           | A simple AllocationCommand composite managing several AllocationCommand implementations |      |
|                                                              |                                                              |      |
| BasePrimaryAllocationCommand                                 | Abstract base class for allocating an unassigned primary shard to a node |      |
|                                                              |                                                              |      |
| BasePrimaryAllocationCommand.Builder<T extends BasePrimaryAllocationCommand> |                                                              |      |
|                                                              |                                                              |      |
| CancelAllocationCommand                                      | A command that cancels relocation, or recovery of a given shard on a node. |      |
|                                                              |                                                              |      |
| MoveAllocationCommand                                        | A command that moves a shard from a specific node to another node. |      |
|                                                              |                                                              |      |



org.elasticsearch.cluster.routing.allocation.decider



| Class                                                  | Description                                                  |      |      |      |
| ------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- | ---- |
|                                                        |                                                              |      |      |      |
| AllocationDecider                                      | AllocationDecider is an abstract base class that allows to make dynamic cluster- or index-wide shard allocation decisions on a per-node basis. |      |      |      |
|                                                        |                                                              |      |      |      |
| AllocationDeciders                                     | A composite AllocationDecider combining the "decision" of multiple AllocationDecider implementations into a single allocation decision. |      |      |      |
|                                                        |                                                              |      |      |      |
| AwarenessAllocationDecider                             | This AllocationDecider controls shard allocation based on awareness key-value pairs defined in the node configuration. |      |      |      |
|                                                        |                                                              |      |      |      |
| ClusterRebalanceAllocationDecider                      | This AllocationDecider controls re-balancing operations based on the cluster wide active shard state. |      |      |      |
|                                                        |                                                              |      |      |      |
| ClusterRebalanceAllocationDecider.ClusterRebalanceType | An enum representation for the configured re-balance type.   |      |      |      |
|                                                        |                                                              |      |      |      |
| ConcurrentRebalanceAllocationDecider                   | Similar to the ClusterRebalanceAllocationDecider this AllocationDecider controls the number of currently in-progress re-balance (relocation) operations and restricts node allocations if the configured threshold is reached. |      |      |      |
|                                                        |                                                              |      |      |      |
| Decision                                               | This abstract class defining basic Decision used during shard allocation process. |      |      |      |
|                                                        |                                                              |      |      |      |
| Decision.Multi                                         | Simple class representing a list of decisions                |      |      |      |
|                                                        |                                                              |      |      |      |
| Decision.Single                                        | Simple class representing a single decision                  |      |      |      |
|                                                        |                                                              |      |      |      |
| Decision.Type                                          | This enumeration defines the possible types of decisions     |      |      |      |
|                                                        |                                                              |      |      |      |
| DiskThresholdDecider                                   | The DiskThresholdDecider checks that the node a shard is potentially being allocated to has enough disk space. |      |      |      |
|                                                        |                                                              |      |      |      |
| EnableAllocationDecider                                | This allocation decider allows shard allocations / rebalancing via the cluster wide settings EnableAllocationDecider.CLUSTER_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.CLUSTER_ROUTING_REBALANCE_ENABLE_SETTING and the per index setting EnableAllocationDecider.INDEX_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_REBALANCE_ENABLE_SETTING. |      |      |      |
|                                                        |                                                              |      |      |      |
| EnableAllocationDecider.Allocation                     | Allocation values or rather their string representation to be used used with EnableAllocationDecider.CLUSTER_ROUTING_ALLOCATION_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_ALLOCATION_ENABLE_SETTING via cluster / index settings. |      |      |      |
|                                                        |                                                              |      |      |      |
| EnableAllocationDecider.Rebalance                      | Rebalance values or rather their string representation to be used used with EnableAllocationDecider.CLUSTER_ROUTING_REBALANCE_ENABLE_SETTING / EnableAllocationDecider.INDEX_ROUTING_REBALANCE_ENABLE_SETTING via cluster / index settings. |      |      |      |
|                                                        |                                                              |      |      |      |
| FilterAllocationDecider                                | This AllocationDecider control shard allocation by include and exclude filters via dynamic cluster and index routing settings. |      |      |      |
|                                                        |                                                              |      |      |      |
| MaxRetryAllocationDecider                              | An allocation decider that prevents shards from being allocated on any node if the shards allocation has been retried N times without success. |      |      |      |
|                                                        |                                                              |      |      |      |
| NodeReplacementAllocationDecider                       | An allocation decider that ensures that all the shards allocated to the node scheduled for removal are relocated to the replacement node. |      |      |      |
|                                                        |                                                              |      |      |      |
| NodeShutdownAllocationDecider                          | An allocation decider that prevents shards from being allocated to a node that is in the process of shutting down. |      |      |      |
|                                                        |                                                              |      |      |      |
| NodeVersionAllocationDecider                           | An allocation decider that prevents relocation or allocation from nodes that might not be version compatible. |      |      |      |
|                                                        |                                                              |      |      |      |
| RebalanceOnlyWhenActiveAllocationDecider               | Only allow rebalancing when all shards are active within the shard replication group. |      |      |      |
|                                                        |                                                              |      |      |      |
| ReplicaAfterPrimaryActiveAllocationDecider             | An allocation strategy that only allows for a replica to be allocated when the primary is active. |      |      |      |
|                                                        |                                                              |      |      |      |
| ResizeAllocationDecider                                | An allocation decider that ensures we allocate the shards of a target index for resize operations next to the source primaries |      |      |      |
|                                                        |                                                              |      |      |      |
| RestoreInProgressAllocationDecider                     | This AllocationDecider prevents shards that have failed to be restored from a snapshot to be allocated. |      |      |      |
|                                                        |                                                              |      |      |      |
| SameShardAllocationDecider                             | An allocation decider that prevents multiple instances of the same shard to be allocated on the same node. |      |      |      |
|                                                        |                                                              |      |      |      |
| ShardsLimitAllocationDecider                           | This AllocationDecider limits the number of shards per node on a per index or node-wide basis. |      |      |      |
|                                                        |                                                              |      |      |      |
| SnapshotInProgressAllocationDecider                    | This AllocationDecider prevents shards that are currently been snapshotted to be moved to other nodes. |      |      |      |
|                                                        |                                                              |      |      |      |
| ThrottlingAllocationDecider                            | ThrottlingAllocationDecider controls the recovery process per node in the cluster. |      |      |      |
|                                                        |                                                              |      |      |      |





org.elasticsearch.cluster.service





| Class                                          | Description                                                  |      |      |
| ---------------------------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                                                |                                                              |      |      |
| ClusterApplier                                 |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterApplierRecordingService                 |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterApplierRecordingService.Stats           |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterApplierRecordingService.Stats.Recording |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterApplierService                          |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterService                                 |                                                              |      |      |
|                                                |                                                              |      |      |
| ClusterStateUpdateStats                        | Various statistics (timing information etc) about cluster state updates coordinated by this node. |      |      |
|                                                |                                                              |      |      |
| MasterService                                  |                                                              |      |      |
|                                                |                                                              |      |      |
| PendingClusterTask                             |                                                              |      |      |
|                                                |                                                              |      |      |
| SourcePrioritizedRunnable                      | PrioritizedRunnable that also has a source string            |      |      |
|                                                |                                                              |      |      |
| TaskBatcher                                    | Batching support for PrioritizedEsThreadPoolExecutor Tasks that share the same batching key are batched (see TaskBatcher.BatchedTask.batchingKey) |      |      |
|                                                |                                                              |      |      |





org.elasticsearch.common





| Class                                        | Description                                                  |      |      |
| -------------------------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                                              |                                                              |      |      |
| AsyncBiFunction<T,U,C>                       | A BiFunction-like interface designed to be used with asynchronous executions. |      |      |
|                                              |                                                              |      |      |
| CheckedBiConsumer<T,U,E extends Exception>   | A BiConsumer-like interface which allows throwing checked exceptions. |      |      |
|                                              |                                                              |      |      |
| CheckedBiFunction<T,U,R,E extends Exception> | A BiFunction-like interface which allows throwing checked exceptions. |      |      |
|                                              |                                                              |      |      |
| CheckedIntFunction<T,E extends Exception>    |                                                              |      |      |
|                                              |                                                              |      |      |
| CheckedSupplier<R,E extends Exception>       | A Supplier-like interface which allows throwing checked exceptions. |      |      |
|                                              |                                                              |      |      |
| Classes                                      |                                                              |      |      |
|                                              |                                                              |      |      |
| Explicit<T>                                  | Holds a value that is either: a) set implicitly e.g.         |      |      |
|                                              |                                                              |      |      |
| ExponentiallyWeightedMovingAverage           | Implements exponentially weighted moving averages (commonly abbreviated EWMA) for a single value. |      |      |
|                                              |                                                              |      |      |
| FieldMemoryStats                             | A reusable class to encode field -&gt; memory size mappings  |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset                              | Converts utc into local time and back again.                 |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset.Gap                          |                                                              |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset.Lookup                       | How to get instances of LocalTimeOffset.                     |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset.Overlap                      |                                                              |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset.Strategy                     |                                                              |      |      |
|                                              |                                                              |      |      |
| LocalTimeOffset.Transition                   |                                                              |      |      |
|                                              |                                                              |      |      |
| MacAddressProvider                           |                                                              |      |      |
|                                              |                                                              |      |      |
| NamedRegistry<T>                             | A registry from String to some class implementation.         |      |      |
|                                              |                                                              |      |      |
| Numbers                                      | A set of utilities for numbers.                              |      |      |
|                                              |                                                              |      |      |
| ParsingException                             | Exception that can be used when parsing queries with a given XContentParser. |      |      |
|                                              |                                                              |      |      |
| PidFile                                      | Process ID file abstraction that writes the current pid into a file and optionally removes it on system exit. |      |      |
|                                              |                                                              |      |      |
| Priority                                     |                                                              |      |      |
|                                              |                                                              |      |      |
| Randomness                                   | Provides factory methods for producing reproducible sources of randomness. |      |      |
|                                              |                                                              |      |      |
| Rounding                                     | A strategy for rounding milliseconds since epoch.            |      |      |
|                                              |                                                              |      |      |
| Rounding.Builder                             |                                                              |      |      |
|                                              |                                                              |      |      |
| Rounding.DateTimeUnit                        |                                                              |      |      |
|                                              |                                                              |      |      |
| Rounding.Prepared                            | A strategy for rounding milliseconds since epoch.            |      |      |
|                                              |                                                              |      |      |
| StopWatch                                    | Simple stop watch, allowing for timing of a number of tasks, exposing total running time and running time for each named task. |      |      |
|                                              |                                                              |      |      |
| StopWatch.TaskInfo                           | Inner class to hold data about one task executed within the stop watch. |      |      |
|                                              |                                                              |      |      |
| Strings                                      |                                                              |      |      |
|                                              |                                                              |      |      |
| SuppressLoggerChecks                         | Annotation to suppress logging usage checks errors inside a whole class or a method. |      |      |
|                                              |                                                              |      |      |
| Table                                        |                                                              |      |      |
|                                              |                                                              |      |      |
| Table.Cell                                   |                                                              |      |      |
|                                              |                                                              |      |      |
| TriConsumer<S,T,U>                           | Represents an operation that accepts three arguments and returns no result. |      |      |
|                                              |                                                              |      |      |
| TriFunction<S,T,U,R>                         | Represents a function that accepts three arguments and produces a result. |      |      |
|                                              |                                                              |      |      |
| UUIDs                                        |                                                              |      |      |
|                                              |                                                              |      |      |
| ValidationException                          | Encapsulates an accumulation of validation errors            |      |      |
|                                              |                                                              |      |      |



org.elasticsearch.common.blobstore



| Class              | Description                                                  |      |
| ------------------ | ------------------------------------------------------------ | ---- |
|                    |                                                              |      |
| BlobContainer      | An interface for managing a repository of blob entries, where each blob entry is just a named group of bytes. |      |
|                    |                                                              |      |
| BlobMetadata       | An interface for providing basic metadata about a blob.      |      |
|                    |                                                              |      |
| BlobPath           | The list of paths where a blob can reside.                   |      |
|                    |                                                              |      |
| BlobStore          | An interface for storing blobs.                              |      |
|                    |                                                              |      |
| BlobStoreException |                                                              |      |
|                    |                                                              |      |
| DeleteResult       | The result of deleting multiple blobs from a BlobStore.      |      |
|                    |                                                              |      |





org.elasticsearch.common.blobstore.fs



| Class           | Description                                          |      |
| --------------- | ---------------------------------------------------- | ---- |
| FsBlobContainer | A file system based implementation of BlobContainer. |      |
| FsBlobStore     |                                                      |      |





org.elasticsearch.common.blobstore.support



| Class                 | Description                                                  |      |      |
| --------------------- | ------------------------------------------------------------ | ---- | ---- |
| AbstractBlobContainer | A base abstract blob container that implements higher level container methods. |      |      |
| FilterBlobContainer   |                                                              |      |      |
| PlainBlobMetadata     |                                                              |      |      |



org.elasticsearch.common.breaker





| Class                             | Description                                                  |      |      |
| --------------------------------- | ------------------------------------------------------------ | ---- | ---- |
| ChildMemoryCircuitBreaker         | Breaker that will check a parent's when incrementing         |      |      |
| CircuitBreaker                    | Interface for an object that can be incremented, breaking after some configured limit has been reached. |      |      |
| CircuitBreaker.Durability         |                                                              |      |      |
| CircuitBreaker.Type               |                                                              |      |      |
| CircuitBreakingException          | Exception thrown when the circuit breaker trips              |      |      |
| NoopCircuitBreaker                | A CircuitBreaker that doesn't increment or adjust, and all operations are basically noops |      |      |
| PreallocatedCircuitBreakerService | CircuitBreakerService that preallocates some bytes on construction. |      |      |



org.elasticsearch.common.bytes



| Class                      | Description                                                  |      |      |
| -------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                            |                                                              |      |      |
| AbstractBytesReference     |                                                              |      |      |
|                            |                                                              |      |      |
| BytesArray                 |                                                              |      |      |
|                            |                                                              |      |      |
| BytesReference             | A reference to bytes.                                        |      |      |
|                            |                                                              |      |      |
| CompositeBytesReference    | A composite BytesReference that allows joining multiple bytes references into one without copying. |      |      |
|                            |                                                              |      |      |
| PagedBytesReference        | A page based bytes reference, internally holding the bytes in a paged data structure. |      |      |
|                            |                                                              |      |      |
| RecyclingBytesStreamOutput | An in-memory StreamOutput which first fills the given byte[] and then allocates more space from the given BigArrays if needed. |      |      |
|                            |                                                              |      |      |
| ReleasableBytesReference   | An extension to BytesReference that requires releasing its content. |      |      |
|                            |                                                              |      |      |



org.elasticsearch.common.cache



| Class                             | Description                |      |
| --------------------------------- | -------------------------- | ---- |
| Cache<K,V>                        | A simple concurrent cache. |      |
| Cache.CacheStats                  |                            |      |
| CacheBuilder<K,V>                 |                            |      |
| CacheLoader<K,V>                  |                            |      |
| RemovalListener<K,V>              |                            |      |
| RemovalNotification<K,V>          |                            |      |
| RemovalNotification.RemovalReason |                            |      |



org.elasticsearch.common.collect



| Class                                 | Description                                                  |      |
| ------------------------------------- | ------------------------------------------------------------ | ---- |
| CopyOnWriteHashMap<K,V>               | An immutable map whose writes result in a new copy of the map to be created. |      |
| EvictingQueue<T>                      | An EvictingQueue is a non-blocking queue which is limited to a maximum size; when new elements are added to a full queue, elements are evicted from the head of the queue to accommodate the new elements. |      |
| HppcMaps                              |                                                              |      |
| HppcMaps.Object                       |                                                              |      |
| HppcMaps.Object.Integer               |                                                              |      |
| ImmutableOpenIntMap<VType>            | An immutable map implementation based on open hash map.      |      |
| ImmutableOpenIntMap.Builder<VType>    |                                                              |      |
| ImmutableOpenMap<KType,VType>         | An immutable map implementation based on open hash map.      |      |
| ImmutableOpenMap.Builder<KType,VType> |                                                              |      |
| Iterators                             |                                                              |      |
| MapBuilder<K,V>                       |                                                              |      |





org.elasticsearch.common.component



| Class                      | Description      |      |
| -------------------------- | ---------------- | ---- |
|                            |                  |      |
| AbstractLifecycleComponent |                  |      |
|                            |                  |      |
| Lifecycle                  | Lifecycle state. |      |
|                            |                  |      |
| Lifecycle.State            |                  |      |
|                            |                  |      |
| LifecycleComponent         |                  |      |
|                            |                  |      |
| LifecycleListener          |                  |      |







org.elasticsearch.common.compress



| Class                  | Description                                                  |      |
| ---------------------- | ------------------------------------------------------------ | ---- |
| CompressedXContent     | Similar class to the String class except that it internally stores data using a compressed representation in order to require less permanent memory. |      |
| Compressor             |                                                              |      |
| CompressorFactory      |                                                              |      |
| DeflateCompressor      | Compressor implementation based on the DEFLATE compression algorithm. |      |
| NotCompressedException | Exception indicating that we were expecting something compressed, which was not compressed or corrupted so that the compression format could not be detected. |      |
| NotXContentException   | Exception indicating that we were expecting some XContent but could not detect its type. |      |





org.elasticsearch.common.document

| Class         | Description                                                  |      |
| ------------- | ------------------------------------------------------------ | ---- |
| DocumentField | A single field name and values part of SearchHit and GetResult. |      |





org.elasticsearch.common.filesystem



| Class             | Description                                                  |      |      |
| ----------------- | ------------------------------------------------------------ | ---- | ---- |
| FileSystemNatives | This class provides utility methods for calling some native methods related to filesystems. |      |      |







org.elasticsearch.common.geo



| Class                                   | Description                                                  |      |
| --------------------------------------- | ------------------------------------------------------------ | ---- |
|                                         |                                                              |      |
| GeoBoundingBox                          | A class representing a Geo-Bounding-Box for use by Geo queries and aggregations that deal with extents/rectangles representing rectangular areas of interest. |      |
|                                         |                                                              |      |
| GeoDistance                             | Geo distance calculation.                                    |      |
|                                         |                                                              |      |
| GeoFormatterFactory<T>                  | Output formatters for geo fields support extensions such as vector tiles. |      |
|                                         |                                                              |      |
| GeoFormatterFactory.FormatterFactory<T> | Defines an extension point for geometry formatter            |      |
|                                         |                                                              |      |
| GeoJson                                 | Utility class for converting libs/geo shapes to and from GeoJson |      |
|                                         |                                                              |      |
| GeoLineDecomposer                       | Splits lines by datelines.                                   |      |
|                                         |                                                              |      |
| GeometryFormatterFactory                | Output formatters supported by geometry fields.              |      |
|                                         |                                                              |      |
| GeometryIO                              | Utility class for binary serializtion/deserialization of libs/geo classes |      |
|                                         |                                                              |      |
| GeometryParser                          | An utility class with to read geometries from a XContentParser or generic object. |      |
|                                         |                                                              |      |
| GeometryParserFormat                    | Supported formats to read/write JSON geometries.             |      |
|                                         |                                                              |      |
| GeoPoint                                |                                                              |      |
|                                         |                                                              |      |
| GeoPolygonDecomposer                    | Splits polygons by datelines.                                |      |
|                                         |                                                              |      |
| GeoShapeUtils                           | Utility class that transforms Elasticsearch geometry objects to the Lucene representation |      |
|                                         |                                                              |      |
| GeoUtils                                |                                                              |      |
|                                         |                                                              |      |
| GeoUtils.EffectivePoint                 | Represents the point of the geohash cell that should be used as the value of geohash |      |
|                                         |                                                              |      |
| Orientation                             |                                                              |      |
|                                         |                                                              |      |
| ShapeRelation                           | Enum representing the relationship between a Query / Filter Shape and indexed Shapes that will be used to determine if a Document should be matched or not |      |
|                                         |                                                              |      |
| SimpleFeatureFactory                    | Transforms points and rectangles objects in WGS84 into mvt features. |      |
|                                         |                                                              |      |
| SimpleVectorTileFormatter               | A facade for SimpleFeatureFactory that converts it into FormatterFactory for use in GeoPointFieldMapper |      |
|                                         |                                                              |      |
| SpatialStrategy                         |                                                              |      |
|                                         |                                                              |      |
| SphericalMercatorUtils                  | Utility functions to transforms WGS84 coordinates into spherical mercator. |      |
|                                         |                                                              |      |
|                                         |                                                              |      |
|                                         |                                                              |      |
|                                         |                                                              |      |
|                                         |                                                              |      |





org.elasticsearch.common.hash

| Class               | Description                                                  |      |      |
| ------------------- | ------------------------------------------------------------ | ---- | ---- |
|                     |                                                              |      |      |
| MessageDigests      | This MessageDigests class provides convenience methods for obtaining thread local MessageDigest instances for MD5, SHA-1, SHA-256 and SHA-512 message digests. |      |      |
|                     |                                                              |      |      |
| Murmur3Hasher       | Wraps MurmurHash3 to provide an interface similar to MessageDigest that allows hashing of byte arrays passed through multiple calls to Murmur3Hasher.update(byte[]). |      |      |
|                     |                                                              |      |      |
| MurmurHash3         | MurmurHash3 hashing functions.                               |      |      |
|                     |                                                              |      |      |
| MurmurHash3.Hash128 | A 128-bits hash.                                             |      |      |
|                     |                                                              |      |      |







org.elasticsearch.common.inject



| Class                  | Description                                                  |      |
| ---------------------- | ------------------------------------------------------------ | ---- |
| AbstractModule         | A support class for Modules which reduces repetition and results in a more readable configuration. |      |
| Binder                 | Collects configuration information (primarily bindings) which will be used to create an Injector. |      |
| Binding<T>             | A mapping from a key (type and optional annotation) to the strategy for getting instances of the type. |      |
| BindingAnnotation      | Annotates annotations which are used for binding.            |      |
| ConfigurationException | Thrown when a programming error such as a misplaced annotation, illegal binding, or unsupported scope is found. |      |
| CreationException      | Thrown when errors occur while creating a Injector.          |      |
| Exposed                | Accompanies a @Provides method annotation in a private module to indicate that the provided binding is exposed. |      |
| Guice                  | The entry point to the Guice framework.                      |      |
| ImplementedBy          | A pointer to the default implementation of a type.           |      |
| Inject                 | Annotates members of your implementation class (constructors, methods and fields) into which the Injector should inject values. |      |
| Injector               | Builds the graphs of objects that make up your application.  |      |
| Key<T>                 | Binding key consisting of an injection type and an optional annotation. |      |
| MembersInjector<T>     | Injects dependencies into the fields and methods on instances of type T. |      |
| Module                 | A module contributes configuration information, typically interface bindings, which will be used to create an Injector. |      |
| ModulesBuilder         |                                                              |      |
| OutOfScopeException    | Thrown from Provider.get() when an attempt is made to access a scoped object while the scope in question is not currently active. |      |
| PreProcessModule       | A module can implement this interface to allow to pre process other modules before an injector is created. |      |
| PrivateBinder          | Returns a binder whose configuration information is hidden from its environment by default. |      |
| PrivateModule          | A module whose configuration information is hidden from its environment by default. |      |
| ProvidedBy             | A pointer to the default provider type for a type.           |      |
| Provider<T>            | An object capable of providing instances of type T.          |      |
| Provides               | Annotates methods of a Module to create a provider method binding. |      |
| ProvisionException     | Indicates that there was a runtime failure while providing an instance. |      |
| Scope                  | A scope is a level of visibility that instances provided by Guice may have. |      |
| ScopeAnnotation        | Annotates annotations which are used for scoping.            |      |
| Scopes                 | Built-in scope implementations.                              |      |
| Singleton              | Apply this to implementation classes when you want only one instance (per Injector) to be reused for all injections for that binding. |      |
| Stage                  | The stage we're running in.                                  |      |
| TypeLiteral<T>         | Represents a generic type T.                                 |      |





org.elasticsearch.common.inject.assistedinject





| Class              | Description                                                  |      |
| ------------------ | ------------------------------------------------------------ | ---- |
|                    |                                                              |      |
| Assisted           | Annotates an injected parameter or field whose value comes from an argument to a factory method. |      |
| AssistedInject     | Deprecated. FactoryProvider now works better with the standard @Inject annotation. |      |
| FactoryProvider<F> | Provides a factory that combines the caller's arguments with injector-supplied values to construct objects. |      |



org.elasticsearch.common.inject.binder



| Class                           | Description                      |      |
| ------------------------------- | -------------------------------- | ---- |
| AnnotatedBindingBuilder<T>      | See the EDSL examples at Binder. |      |
| AnnotatedConstantBindingBuilder | See the EDSL examples at Binder. |      |
| AnnotatedElementBuilder         | See the EDSL examples at Binder. |      |
| ConstantBindingBuilder          | Binds to a constant value.       |      |
| LinkedBindingBuilder<T>         | See the EDSL examples at Binder. |      |
| ScopedBindingBuilder            | See the EDSL examples at Binder. |      |





org.elasticsearch.common.inject.internal



| Class                           | Description                                                  |      |
| ------------------------------- | ------------------------------------------------------------ | ---- |
| AbstractBindingBuilder<T>       | Bind a value or constant.                                    |      |
| Annotations                     | Annotation utilities.                                        |      |
| BindingBuilder<T>               | Bind a non-constant key.                                     |      |
| BindingImpl<T>                  |                                                              |      |
| ConstantBindingBuilderImpl<T>   | Bind a constant.                                             |      |
| ConstructionContext<T>          | Context of a dependency construction.                        |      |
| ErrorHandler                    | Handles errors in the Injector.                              |      |
| Errors                          | A collection of error messages.                              |      |
| ErrorsException                 | Indicates that a result could not be returned while preparing or resolving a binding. |      |
| ExposedBindingImpl<T>           |                                                              |      |
| ExposureBuilder<T>              | For private binder's expose() method.                        |      |
| FailableCache<K,V>              | Lazily creates (and caches) values for keys.                 |      |
| InstanceBindingImpl<T>          |                                                              |      |
| InternalContext                 | Internal context.                                            |      |
| InternalFactory<T>              | Creates objects which will be injected.                      |      |
| InternalFactory.Instance<T>     | ES: An factory that returns a pre created instance.          |      |
| LinkedBindingImpl<T>            |                                                              |      |
| LinkedProviderBindingImpl<T>    |                                                              |      |
| MatcherAndConverter             |                                                              |      |
| MoreTypes                       | Static methods for working with types that we aren't publishing in the public Types API. |      |
| MoreTypes.GenericArrayTypeImpl  |                                                              |      |
| MoreTypes.MemberImpl            | We cannot serialize the built-in Java member classes, which prevents us from using Members in our exception types. |      |
| MoreTypes.ParameterizedTypeImpl |                                                              |      |
| MoreTypes.WildcardTypeImpl      | The WildcardType interface supports multiple upper bounds and multiple lower bounds. |      |
| Nullability                     | Whether a member supports null values injected.              |      |
| PrivateElementsImpl             |                                                              |      |
| ProviderInstanceBindingImpl<T>  |                                                              |      |
| ProviderMethod<T>               | A provider that invokes a method and returns its result.     |      |
| ProviderMethodsModule           | Creates bindings to methods annotated with @Provides.        |      |
| Scoping                         | References a scope, either directly (as a scope instance), or indirectly (as a scope annotation). |      |
| SourceProvider                  | Provides access to the calling line of code.                 |      |
| StackTraceElements              | Creates stack trace elements for members.                    |      |
| Stopwatch                       | Enables simple performance monitoring.                       |      |
| Strings                         | String utilities.                                            |      |
| ToStringBuilder                 | Helps with toString() methods.                               |      |
| UniqueAnnotations               |                                                              |      |
| UntargettedBindingImpl<T>       |                                                              |      |





org.elasticsearch.common.inject.matcher





| Class              | Description                              |      |
| ------------------ | ---------------------------------------- | ---- |
|                    |                                          |      |
| AbstractMatcher<T> | Implements and() and or().               |      |
|                    |                                          |      |
| Matcher<T>         | Returns true or false for a given input. |      |
|                    |                                          |      |
| Matchers           | Matcher implementations.                 |      |
|                    |                                          |      |



org.elasticsearch.common.inject.multibindings



| Class                                                        | Description                                                  |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
|                                                              |                                                              |      |
| MapBinder<K,V>                                               | An API to bind multiple map entries separately, only to later inject them as a complete map. |      |
|                                                              |                                                              |      |
| MapBinder.RealMapBinder<K,V>                                 | The actual mapbinder plays several roles:                    |      |
|                                                              |                                                              |      |
| MapBinder.RealMapBinder.MapBinderProviderWithDependencies<K,V> |                                                              |      |
|                                                              |                                                              |      |
| Multibinder<T>                                               | An API to bind multiple values separately, only to later inject them as a complete collection. |      |
|                                                              |                                                              |      |
| Multibinder.RealMultibinder<T>                               | The actual multibinder plays several roles:                  |      |
|                                                              |                                                              |      |





org.elasticsearch.common.inject.name

| Class | Description                          |      |
| ----- | ------------------------------------ | ---- |
| Named | Annotates named things.              |      |
| Names | Utility methods for use with @Named. |      |







org.elasticsearch.common.inject.spi





| Class                                  | Description                                                  |      |
| -------------------------------------- | ------------------------------------------------------------ | ---- |
|                                        |                                                              |      |
| BindingScopingVisitor<V>               | Visits each of the strategies used to scope an injection.    |      |
|                                        |                                                              |      |
| BindingTargetVisitor<T,V>              | Visits each of the strategies used to find an instance to satisfy an injection. |      |
|                                        |                                                              |      |
| ConstructorBinding<T>                  | A binding to the constructor of a concrete clss.             |      |
|                                        |                                                              |      |
| ConvertedConstantBinding<T>            | A binding created from converting a bound instance to a new type. |      |
|                                        |                                                              |      |
| DefaultBindingScopingVisitor<V>        | No-op visitor for subclassing.                               |      |
|                                        |                                                              |      |
| DefaultBindingTargetVisitor<T,V>       | No-op visitor for subclassing.                               |      |
|                                        |                                                              |      |
| DefaultElementVisitor<V>               | No-op visitor for subclassing.                               |      |
|                                        |                                                              |      |
| Dependency<T>                          | A variable that can be resolved by an injector.              |      |
|                                        |                                                              |      |
| Element                                | A core component of a module or injector.                    |      |
|                                        |                                                              |      |
| Elements                               | Exposes elements of a module so they can be inspected, validated or rewritten. |      |
|                                        |                                                              |      |
| ElementVisitor<V>                      | Visit elements.                                              |      |
|                                        |                                                              |      |
| ExposedBinding<T>                      | A binding to a key exposed from an enclosed private environment. |      |
|                                        |                                                              |      |
| HasDependencies                        | Implemented by bindings,providers and instances that expose their dependencies explicitly. |      |
|                                        |                                                              |      |
| InjectionListener<I>                   | Listens for injections into instances of type I.             |      |
|                                        |                                                              |      |
| InjectionPoint                         | A constructor, field or method that can receive injections.  |      |
|                                        |                                                              |      |
| InjectionRequest<T>                    | A request to inject the instance fields and methods of an instance. |      |
|                                        |                                                              |      |
| InstanceBinding<T>                     | A binding to a single instance.                              |      |
|                                        |                                                              |      |
| LinkedKeyBinding<T>                    | A binding to a linked key.                                   |      |
|                                        |                                                              |      |
| MembersInjectorLookup<T>               | A lookup of the members injector for a type.                 |      |
|                                        |                                                              |      |
| Message                                | An error message and the context in which it occurred.       |      |
|                                        |                                                              |      |
| PrivateElements                        | A private collection of elements that are hidden from the enclosing injector or module by default. |      |
|                                        |                                                              |      |
| ProviderBinding<T extends Provider<?>> | A binding to a Provider that delegates to the binding for the provided type. |      |
|                                        |                                                              |      |
| ProviderInstanceBinding<T>             | A binding to a provider instance.                            |      |
|                                        |                                                              |      |
| ProviderKeyBinding<T>                  | A binding to a provider key.                                 |      |
|                                        |                                                              |      |
| ProviderLookup<T>                      | A lookup of the provider for a type.                         |      |
|                                        |                                                              |      |
| ProviderLookup.ProviderImpl<T>         |                                                              |      |
|                                        |                                                              |      |
| ProviderWithDependencies<T>            | A provider with dependencies on other injected types.        |      |
|                                        |                                                              |      |
| ScopeBinding                           | Registration of a scope annotation with the scope that implements it. |      |
|                                        |                                                              |      |
| StaticInjectionRequest                 | A request to inject the static fields and methods of a type. |      |
|                                        |                                                              |      |
| TypeConverter                          | Converts constant string values to a different type.         |      |
|                                        |                                                              |      |
| TypeConverterBinding                   | Registration of type converters for matching target types.   |      |
|                                        |                                                              |      |
| TypeEncounter<I>                       | Context of an injectable type encounter.                     |      |
|                                        |                                                              |      |
| TypeListener                           | Listens for Guice to encounter injectable types.             |      |
|                                        |                                                              |      |
| TypeListenerBinding                    | Binds types (picked using a Matcher) to an type listener.    |      |
|                                        |                                                              |      |
| UntargettedBinding<T>                  | An untargetted binding.                                      |      |
|                                        |                                                              |      |



org.elasticsearch.common.inject.util



| Class                           | Description                                                  |      |
| ------------------------------- | ------------------------------------------------------------ | ---- |
|                                 |                                                              |      |
| Modules                         | Static utility methods for creating and working with instances of Module. |      |
|                                 |                                                              |      |
| Modules.OverriddenModuleBuilder | See the EDSL example at override().                          |      |
|                                 |                                                              |      |
| Providers                       | Static utility methods for creating and working with instances of Provider. |      |
|                                 |                                                              |      |
| Types                           | Static methods for working with types.                       |      |
|                                 |                                                              |      |





org.elasticsearch.common.io



| Class            | Description                                         |      |
| ---------------- | --------------------------------------------------- | ---- |
|                  |                                                     |      |
| Channels         |                                                     |      |
|                  |                                                     |      |
| DiskIoBufferPool |                                                     |      |
|                  |                                                     |      |
| FileSystemUtils  | Elasticsearch utils to work with Path               |      |
|                  |                                                     |      |
| Streams          | Simple utility methods for file and stream copying. |      |
|                  |                                                     |      |
| UTF8StreamWriter |                                                     |      |







org.elasticsearch.common.io.stream



| Class                                              | Description                                                  |      |      |
| -------------------------------------------------- | ------------------------------------------------------------ | ---- | ---- |
|                                                    |                                                              |      |      |
| ByteArrayStreamInput                               | Resettable StreamInput that wraps a byte array.              |      |      |
|                                                    |                                                              |      |      |
| ByteBufferStreamInput                              |                                                              |      |      |
|                                                    |                                                              |      |      |
| BytesStream                                        |                                                              |      |      |
|                                                    |                                                              |      |      |
| BytesStreamOutput                                  | A @link StreamOutput that uses BigArrays to acquire pages of bytes, which avoids frequent reallocation & copying of the internal data. |      |      |
|                                                    |                                                              |      |      |
| DataOutputStreamOutput                             |                                                              |      |      |
|                                                    |                                                              |      |      |
| DelayableWriteable<T extends Writeable>            | A holder for Writeables that delays reading the underlying object on the receiving end. |      |      |
|                                                    |                                                              |      |      |
| DelayableWriteable.Serialized<T extends Writeable> | A Writeable stored in serialized form backed by a ReleasableBytesReference. |      |      |
|                                                    |                                                              |      |      |
| FilterStreamInput                                  | Wraps a StreamInput and delegates to it.                     |      |      |
|                                                    |                                                              |      |      |
| InputStreamStreamInput                             |                                                              |      |      |
|                                                    |                                                              |      |      |
| NamedWriteable                                     | A Writeable object identified by its name.                   |      |      |
|                                                    |                                                              |      |      |
| NamedWriteableAwareStreamInput                     | Wraps a StreamInput and associates it with a NamedWriteableRegistry |      |      |
|                                                    |                                                              |      |      |
| NamedWriteableRegistry                             | A registry for Writeable.Reader readers of NamedWriteable.   |      |      |
|                                                    |                                                              |      |      |
| NamedWriteableRegistry.Entry                       | An entry in the registry, made up of a category class and name, and a reader for that category class. |      |      |
|                                                    |                                                              |      |      |
| NotSerializableExceptionWrapper                    | This exception can be used to wrap a given, not serializable exception to serialize via StreamOutput.writeException(Throwable). |      |      |
|                                                    |                                                              |      |      |
| OutputStreamStreamOutput                           |                                                              |      |      |
|                                                    |                                                              |      |      |
| PositionTrackingOutputStreamStreamOutput           |                                                              |      |      |
|                                                    |                                                              |      |      |
| ReleasableBytesStreamOutput                        | An bytes stream output that allows providing a BigArrays instance expecting it to require releasing its content (BytesStreamOutput.bytes()) once done. |      |      |
|                                                    |                                                              |      |      |
| StreamInput                                        | A stream from this node to another node.                     |      |      |
|                                                    |                                                              |      |      |
| StreamOutput                                       | A stream from another node to this node.                     |      |      |
|                                                    |                                                              |      |      |
| VersionedNamedWriteable                            | A NamedWriteable that has a minimum version associated with it. |      |      |
|                                                    |                                                              |      |      |
| Writeable                                          | Implementers can be written to a StreamOutput and read from a StreamInput. |      |      |
|                                                    |                                                              |      |      |
| Writeable.Reader<V>                                | Reference to a method that can read some object from a stream. |      |      |
|                                                    |                                                              |      |      |
| Writeable.Writer<V>                                | Reference to a method that can write some object to a StreamOutput. |      |      |
|                                                    |                                                              |      |      |







org.elasticsearch.common.joda





| Class                   | Description                                                  |      |
| ----------------------- | ------------------------------------------------------------ | ---- |
|                         |                                                              |      |
| Joda                    | Deprecated.                                                  |      |
|                         |                                                              |      |
| Joda.EpochTimeParser    |                                                              |      |
|                         |                                                              |      |
| Joda.EpochTimePrinter   |                                                              |      |
|                         |                                                              |      |
| JodaDateFormatter       |                                                              |      |
|                         |                                                              |      |
| JodaDateMathParser      | A parser for date/time formatted text with optional date math. |      |
|                         |                                                              |      |
| JodaDeprecationPatterns |                                                              |      |





org.elasticsearch.common.logging



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| ClusterIdConverter                                           |      |      |      |
| Pattern converter to format the cluster_id variable into JSON fields cluster.id. |      |      |      |
| DeprecatedMessage                                            |      |      |      |
| A logger message used by DeprecationLogger.                  |      |      |      |
| DeprecationCategory                                          |      |      |      |
| Deprecation log messages are categorised so that consumers of the logs can easily aggregate them. |      |      |      |
| DeprecationLogger                                            |      |      |      |
| A logger that logs deprecation notices.                      |      |      |      |
| ESJsonLayout                                                 |      |      |      |
| Formats log events as strings in a json format.              |      |      |      |
| ESJsonLayout.Builder<B extends ESJsonLayout.Builder<B>>      |      |      |      |
|                                                              |      |      |      |
| ESLogMessage                                                 |      |      |      |
| A base class for custom log4j logger messages.               |      |      |      |
| ESMessageFieldConverter                                      |      |      |      |
| Pattern converter to populate ESMessageField in a pattern.   |      |      |      |
| HeaderWarning                                                |      |      |      |
| This is a simplistic logger that adds warning messages to HTTP headers. |      |      |      |
| HeaderWarningAppender                                        |      |      |      |
|                                                              |      |      |      |
| JsonThrowablePatternConverter                                |      |      |      |
| Outputs the Throwable portion of the LoggingEvent as a Json formatted field with array "exception": [ "stacktrace", "lines", "as", "array", "elements" ] Reusing @link org.apache.logging.log4j.core.pattern.ExtendedThrowablePatternConverter which already converts a Throwable from LoggingEvent into a multiline string |      |      |      |
| LogConfigurator                                              |      |      |      |
|                                                              |      |      |      |
| LoggerMessageFormat                                          |      |      |      |
| Format string for Elasticsearch log messages.                |      |      |      |
| Loggers                                                      |      |      |      |
| A set of utilities around Logging.                           |      |      |      |
| NodeAndClusterIdConverter                                    |      |      |      |
| Pattern converter to format the node_and_cluster_id variable into JSON fields node.id and cluster.uuid. |      |      |      |
| NodeAndClusterIdStateListener                                |      |      |      |
| The NodeAndClusterIdStateListener listens to cluster state changes and ONLY when receives the first update it sets the clusterUUID and nodeID in log4j pattern converter NodeAndClusterIdConverter. |      |      |      |
| NodeIdConverter                                              |      |      |      |
| Pattern converter to format the node_id variable into JSON fields node.id . |      |      |      |
| NodeNamePatternConverter                                     |      |      |      |
| Converts %node_name in log4j patterns into the current node name. |      |      |      |
| ProductOriginConverter                                       |      |      |      |
| Pattern converter to format the X-elastic-product-origin into plaintext logs. |      |      |      |
| RateLimitingFilter                                           |      |      |      |
| A filter used for throttling deprecation logs.               |      |      |      |
| TraceIdConverter                                             |      |      |      |
| Pattern converter to format the trace id provided in the traceparent header into JSON fields trace.id. |      |      |      |



org.elasticsearch.common.lucene



org.elasticsearch.common.lucene.index



org.elasticsearch.common.lucene.search



org.elasticsearch.common.lucene.search.function



org.elasticsearch.common.lucene.store



org.elasticsearch.common.lucene.uid



org.elasticsearch.common.metrics

| Class         | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| CounterMetric | A CounterMetric is used to track the number of completed and outstanding items, for example, the number of executed refreshes, the currently used memory by indexing, the current pending search requests. |
| MeanMetric    |                                                              |



org.elasticsearch.common.network



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| CIDRUtils                                                    |             |      |      |
|                                                              |             |      |      |
| CloseableChannel                                             |             |      |      |
|                                                              |             |      |      |
| IfConfig                                                     |             |      |      |
| Simple class to log ifconfig-style output at DEBUG logging.  |             |      |      |
| InetAddresses                                                |             |      |      |
|                                                              |             |      |      |
| NetworkAddress                                               |             |      |      |
| Utility functions for presentation of network addresses.     |             |      |      |
| NetworkModule                                                |             |      |      |
| A module to handle registering and binding all network related classes. |             |      |      |
| NetworkService                                               |             |      |      |
|                                                              |             |      |      |
| NetworkService.CustomNameResolver                            |             |      |      |
| A custom name resolver can support custom lookup keys (my_net_key:ipv4) and also change the default inet address used in case no settings is provided. |             |      |      |
| NetworkUtils                                                 |             |      |      |
| Utilities for network interfaces / addresses binding and publishing. |             |      |      |





org.elasticsearch.common.path



| Class            |      | Description |
| ---------------- | ---- | ----------- |
|                  |      |             |
| PathTrie<T>      |      |             |
|                  |      |             |
| PathTrie.Decoder |      |             |





org.elasticsearch.common.recycler



| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| AbstractRecyclerC<T>                                         |             |      |
|                                                              |             |      |
| ConcurrentDequeRecycler<T>                                   |             |      |
| A Recycler implementation based on a concurrent Deque.       |             |      |
| DequeRecycler<T>                                             |             |      |
| A Recycler implementation based on a Deque.                  |             |      |
| NoneRecycler<T>                                              |             |      |
|                                                              |             |      |
| NoneRecycler.NV<T>                                           |             |      |
|                                                              |             |      |
| Recycler<T>                                                  |             |      |
| A recycled object, note, implementations should support calling obtain and then recycle on different threads. |             |      |
| Recycler.C<T>                                                |             |      |
|                                                              |             |      |
| Recycler.Factory<T>                                          |             |      |
|                                                              |             |      |
| Recycler.V<T>                                                |             |      |
|                                                              |             |      |
| Recyclers                                                    |             |      |





org.elasticsearch.common.regex

| Class | Description |      |
| ----- | ----------- | ---- |
|       |             |      |
| Regex |             |      |



org.elasticsearch.common.rounding



| Class            | Description |      |
| ---------------- | ----------- | ---- |
|                  |             |      |
| DateTimeUnit     |             |      |
|                  |             |      |
| Rounding         |             |      |
| Deprecated.      |             |      |
| Rounding.Builder |             |      |
|                  |             |      |
| Rounding.Streams |             |      |







org.elasticsearch.common.settings



| Class                                                        | Description                                                  |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
|                                                              |                                                              |      |
| AbstractScopedSettings                                       | A basic setting service that can be used for per-index and per-cluster settings. |      |
|                                                              |                                                              |      |
| AbstractScopedSettings.SettingUpdater<T>                     | Transactional interface to update settings.                  |      |
|                                                              |                                                              |      |
| BaseKeyStoreCommand                                          |                                                              |      |
|                                                              |                                                              |      |
| ClusterSettings                                              | Encapsulates all valid cluster level settings.               |      |
|                                                              |                                                              |      |
| ConsistentSettingsService                                    | Used to publish secure setting hashes in the cluster state and to validate those hashes against the local values of those same settings. |      |
|                                                              |                                                              |      |
| HasPasswordKeyStoreCommand                                   |                                                              |      |
|                                                              |                                                              |      |
| IndexScopedSettings                                          | Encapsulates all valid index level settings.                 |      |
|                                                              |                                                              |      |
| KeyStoreWrapper                                              | A disk based container for sensitive settings in Elasticsearch. |      |
|                                                              |                                                              |      |
| NoClassSettingsException                                     |                                                              |      |
| A specific type of SettingsException indicating failure to load a class based on a settings value. |                                                              |      |
| SecureSetting<T>                                             |                                                              |      |
| A secure setting.                                            |                                                              |      |
| SecureSettings                                               |                                                              |      |
| An accessor for settings which are securely stored.          |                                                              |      |
| SecureString                                                 |                                                              |      |
| A String implementations which allows clearing the underlying char array. |                                                              |      |
| Setting<T>                                                   |                                                              |      |
| A setting.                                                   |                                                              |      |
| Setting.AffixKey                                             |                                                              |      |
| A key that allows for static pre and suffix.                 |                                                              |      |
| Setting.AffixSetting<T>                                      |                                                              |      |
|                                                              |                                                              |      |
| Setting.AffixSettingDependency                               |                                                              |      |
| Allows an affix setting to declare a dependency on another affix setting. |                                                              |      |
| Setting.GroupKey                                             |                                                              |      |
|                                                              |                                                              |      |
| Setting.Key                                                  |                                                              |      |
|                                                              |                                                              |      |
| Setting.ListKey                                              |                                                              |      |
|                                                              |                                                              |      |
| Setting.Property                                             |                                                              |      |
|                                                              |                                                              |      |
| Setting.SettingDependency                                    |                                                              |      |
| Allows a setting to declare a dependency on another setting being set. |                                                              |      |
| Setting.SimpleKey                                            |                                                              |      |
|                                                              |                                                              |      |
| Setting.Validator<T>                                         |                                                              |      |
| Represents a validator for a setting.                        |                                                              |      |
| Settings                                                     |                                                              |      |
| An immutable settings implementation.                        |                                                              |      |
| Settings.Builder                                             |                                                              |      |
| A builder allowing to put different settings and then Settings.Builder.build() an immutable settings implementation. |                                                              |      |
| SettingsException                                            |                                                              |      |
| A generic failure to handle settings.                        |                                                              |      |
| SettingsFilter                                               |                                                              |      |
| A class that allows to filter settings objects by simple regular expression patterns or full settings keys. |                                                              |      |
| SettingsModule                                               |                                                              |      |
| A module that binds the provided settings to the Settings interface. |                                                              |      |
| SettingUpgrader<T>                                           |                                                              |      |
| Represents the logic to upgrade a setting.                   |                                                              |      |
| UpgradeKeyStoreCommand                                       |                                                              |      |
| A sub-command for the keystore CLI that enables upgrading the keystore format. |                                                              |      |







org.elasticsearch.common.text



| Class                                                      | Description |      |
| ---------------------------------------------------------- | ----------- | ---- |
|                                                            |             |      |
| Text                                                       |             |      |
| Both String and BytesReference representation of the text. |             |      |





org.elasticsearch.common.time



| Class                                                        |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| Description                                                  |      |      |
| DateFormatter                                                |      |      |
|                                                              |      |      |
| DateFormatters                                               |      |      |
|                                                              |      |      |
| DateMathParser                                               |      |      |
| An abstraction over date math parsing to allow different implementation for joda and java time. |      |      |
| DateUtils                                                    |      |      |
|                                                              |      |      |
| FormatNames                                                  |      |      |
|                                                              |      |      |
| IsoCalendarDataProvider                                      |      |      |
| This class is loaded by JVM SPI mechanism in order to provide ISO compatible behaviour for week calculations using java.time. |      |      |
| JavaDateMathParser                                           |      |      |
| A parser for date/time formatted text with optional date math. |      |      |
| WriteableZoneId                                              |      |      |
| Simple wrapper around ZoneId so that it can be written to XContent |      |      |





org.elasticsearch.common.transport





| Class                   | Description                                                  |      |
| ----------------------- | ------------------------------------------------------------ | ---- |
|                         |                                                              |      |
| BoundTransportAddress   | A bounded transport address is a tuple of TransportAddress, one array that represents the addresses the transport is bound to, and the other is the published one that represents the address clients should communicate on. |      |
|                         |                                                              |      |
| NetworkExceptionHelper  |                                                              |      |
|                         |                                                              |      |
| PortsRange              |                                                              |      |
|                         |                                                              |      |
| PortsRange.PortCallback |                                                              |      |
|                         |                                                              |      |
| TransportAddress        | A transport address used for IP socket address (wraps InetSocketAddress). |      |
|                         |                                                              |      |



org.elasticsearch.common.unit



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
|                                                              |             |      |      |
| ByteSizeUnit                                                 |             |      |      |
| A SizeUnit represents size at a given unit of granularity and provides utility methods to convert across units. |             |      |      |
| ByteSizeValue                                                |             |      |      |
|                                                              |             |      |      |
| DistanceUnit                                                 |             |      |      |
| The DistanceUnit enumerates several units for measuring distances. |             |      |      |
| DistanceUnit.Distance                                        |             |      |      |
| This class implements a value+unit tuple.                    |             |      |      |
| Fuzziness                                                    |             |      |      |
| A unit class that encapsulates all in-exact search parsing and conversion from similarities to edit distances etc. |             |      |      |
| MemorySizeValue                                              |             |      |      |
| Utility methods to get memory sizes.                         |             |      |      |
| RatioValue                                                   |             |      |      |
| Utility class to represent ratio and percentage values between 0 and 100 |             |      |      |
| RelativeByteSizeValue                                        |             |      |      |
| A byte size value that allows specification using either of: 1. |             |      |      |
| SizeUnit                                                     |             |      |      |
|                                                              |             |      |      |
| SizeValue                                                    |             |      |      |





org.elasticsearch.common.util



| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| ArrayUtils                                                   |             |      |
|                                                              |             |      |
| BigArray                                                     |             |      |
| Base abstraction of an array.                                |             |      |
| BigArrays                                                    |             |      |
| Utility class to work with arrays.                           |             |      |
| BigArrays.DoubleBinarySearcher                               |             |      |
|                                                              |             |      |
| BinarySearcher                                               |             |      |
| Performs binary search on an arbitrary data structure.       |             |      |
| BitArray                                                     |             |      |
| A bit array that is implemented using a growing LongArray created from BigArrays. |             |      |
| ByteArray                                                    |             |      |
| Abstraction of an array of byte values.                      |             |      |
| BytesRefHash                                                 |             |      |
| Specialized hash table implementation similar to Lucene's BytesRefHash that maps BytesRef values to ids. |             |      |
| ByteUtils                                                    |             |      |
| Utility methods to do byte-level encoding.                   |             |      |
| CachedSupplier<T>                                            |             |      |
| A Supplier that caches its return value.                     |             |      |
| CancellableSingleObjectCache<Input,Key,Value>                |             |      |
| A cache of a single object whose refresh process can be cancelled. |             |      |
| CancellableThreads                                           |             |      |
| A utility class for multi threaded operation that needs to be cancellable via interrupts. |             |      |
| CancellableThreads.ExecutionCancelledException               |             |      |
|                                                              |             |      |
| CancellableThreads.Interruptible                             |             |      |
|                                                              |             |      |
| CancellableThreads.OnCancel                                  |             |      |
|                                                              |             |      |
| CollectionUtils                                              |             |      |
| Collections-related utility methods.                         |             |      |
| CombinedRateLimiter                                          |             |      |
| A rate limiter designed for multiple concurrent users.       |             |      |
| Comparators                                                  |             |      |
| Comparator-related utility methods.                          |             |      |
| Countable                                                    |             |      |
|                                                              |             |      |
| CuckooFilter                                                 |             |      |
| An approximate set membership datastructure CuckooFilters are similar to Bloom Filters in usage; values are inserted, and the Cuckoo can be asked if it has seen a particular value before. |             |      |
| DoubleArray                                                  |             |      |
| Abstraction of an array of double values.                    |             |      |
| FloatArray                                                   |             |      |
| Abstraction of an array of double values.                    |             |      |
| IntArray                                                     |             |      |
| Abstraction of an array of integer values.                   |             |      |
| LazyInitializable<T,E extends Exception>                     |             |      |
| Encapsulates a CheckedSupplier which is lazily invoked once on the first call to #getOrCompute(). |             |      |
| LazyMap<K,V>                                                 |             |      |
|                                                              |             |      |
| LocaleUtils                                                  |             |      |
| Utilities for for dealing with Locale objects                |             |      |
| LongArray                                                    |             |      |
| Abstraction of an array of long values.                      |             |      |
| LongHash                                                     |             |      |
| Specialized hash table implementation similar to BytesRefHash that maps long values to ids. |             |      |
| LongLongHash                                                 |             |      |
| Specialized hash table implementation similar to BytesRefHash that maps two long values to ids. |             |      |
| LongObjectPagedHashMap<T>                                    |             |      |
| A hash table from native longs to objects.                   |             |      |
| LongObjectPagedHashMap.Cursor<T>                             |             |      |
|                                                              |             |      |
| Maps                                                         |             |      |
|                                                              |             |      |
| ObjectArray<T>                                               |             |      |
| Abstraction of an array of object values.                    |             |      |
| PageCacheRecycler                                            |             |      |
| A recycler of fixed-size pages.                              |             |      |
| PageCacheRecycler.Type                                       |             |      |
|                                                              |             |      |
| PlainIterator<T>                                             |             |      |
|                                                              |             |      |
| SetBackedScalingCuckooFilter                                 |             |      |
| An approximate set membership datastructure that scales as more unique values are inserted. |             |      |
| SingleObjectCache<T>                                         |             |      |
| A very simple single object cache that allows non-blocking refresh calls triggered by expiry time. |             |      |
| StringLiteralDeduplicator                                    |             |      |
| A cache in front of Java's string interning.                 |             |      |
| URIPattern                                                   |             |      |
| URI Pattern matcher The pattern is URI in which authority, path, query and fragment can be replace with simple pattern. |             |      |





org.elasticsearch.common.util.concurrent





| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| AbstractAsyncTask                                            |             |      |
| A base class for tasks that need to repeat.                  |             |      |
| AbstractLifecycleRunnable                                    |             |      |
| AbstractLifecycleRunnable is a service-lifecycle aware AbstractRunnable. |             |      |
| AbstractRunnable                                             |             |      |
| An extension to runnable.                                    |             |      |
| AdjustableSemaphore                                          |             |      |
|                                                              |             |      |
| AsyncIOProcessor<Item>                                       |             |      |
| This async IO processor allows to batch IO operations and have a single writer processing the write operations. |             |      |
| AtomicArray<E>                                               |             |      |
| A list backed by an AtomicReferenceArray with potential null values, easily allowing to get the concrete values as a list using AtomicArray.asList(). |             |      |
| BaseFuture<V>                                                |             |      |
|                                                              |             |      |
| ConcurrentCollections                                        |             |      |
|                                                              |             |      |
| ConcurrentMapLong<T>                                         |             |      |
|                                                              |             |      |
| CountDown                                                    |             |      |
| A simple thread safe count-down class that in contrast to a CountDownLatch never blocks. |             |      |
| EsAbortPolicy                                                |             |      |
|                                                              |             |      |
| EsExecutors                                                  |             |      |
|                                                              |             |      |
| EsRejectedExecutionException                                 |             |      |
|                                                              |             |      |
| EsRejectedExecutionHandler                                   |             |      |
|                                                              |             |      |
| EsThreadPoolExecutor                                         |             |      |
| An extension to thread pool executor, allowing (in the future) to add specific additional stats to it. |             |      |
| EsThreadPoolExecutor.ShutdownListener                        |             |      |
|                                                              |             |      |
| FutureUtils                                                  |             |      |
|                                                              |             |      |
| KeyedLock<T>                                                 |             |      |
| This class manages locks.                                    |             |      |
| ListenableFuture<V>                                          |             |      |
| A future implementation that allows for the result to be passed to listeners waiting for notification. |             |      |
| PrioritizedCallable<T>                                       |             |      |
|                                                              |             |      |
| PrioritizedEsThreadPoolExecutor                              |             |      |
| A prioritizing executor which uses a priority queue as a work queue. |             |      |
| PrioritizedEsThreadPoolExecutor.Pending                      |             |      |
|                                                              |             |      |
| PrioritizedEsThreadPoolExecutor.StarvationWatcher            |             |      |
| We expect the work queue to be empty fairly frequently; if the queue remains nonempty for sufficiently long then there's a risk that some lower-priority tasks are being starved of access to the executor. |             |      |
| PrioritizedRunnable                                          |             |      |
|                                                              |             |      |
| QueueResizingEsThreadPoolExecutor                            |             |      |
| An extension to thread pool executor, which automatically adjusts the queue size of the ResizableBlockingQueue according to Little's Law. |             |      |
| ReleasableLock                                               |             |      |
| Releasable lock used inside of Engine implementations        |             |      |
| RunOnce                                                      |             |      |
| Runnable that can only be run one time.                      |             |      |
| SizeBlockingQueue<E>                                         |             |      |
| A size based queue wrapping another blocking queue to provide (somewhat relaxed) capacity checks. |             |      |
| ThreadContext                                                |             |      |
| A ThreadContext is a map of string headers and a transient map of keyed objects that are associated with a thread. |             |      |
| ThreadContext.StoredContext                                  |             |      |
|                                                              |             |      |
| UncategorizedExecutionException                              |             |      |
|                                                              |             |      |
| WrappedRunnable                                              |             |      |





org.elasticsearch.common.util.iterable





| Class     | Description |
| --------- | ----------- |
| Iterables |             |





org.elasticsearch.common.util.set



| Class | Description |      |
| ----- | ----------- | ---- |
| Sets  |             |      |



org.elasticsearch.common.xcontent



| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| LoggingDeprecationHandler                                    |             |      |
| Logs deprecations to the DeprecationLogger.                  |             |      |
| ObjectParserHelper<Value,Context>                            |             |      |
| This class provides helpers for ObjectParser that allow dealing with classes outside of the xcontent dependencies. |             |      |
| ParseFieldRegistry<T>                                        |             |      |
| Registry for looking things up using ParseField semantics.   |             |      |
| StatusToXContentObject                                       |             |      |
| Objects that can both render themselves in as json/yaml/etc and can provide a RestStatus for their response. |             |      |
| SuggestingErrorOnUnknown                                     |             |      |
|                                                              |             |      |
| XContentElasticsearchExtension                               |             |      |
| SPI extensions for Elasticsearch-specific classes (like the Lucene or Joda dependency classes) that need to be encoded by XContentBuilder in a specific way. |             |      |
| XContentHelper                                               |             |      |
|                                                              |             |      |
| XContentParserUtils                                          |             |      |
| A set of static methods to get XContentParser.Token from XContentParser while checking for their types and throw ParsingException if needed. |             |      |





org.elasticsearch.common.xcontent.support



| Class             | Description |      |
| ----------------- | ----------- | ---- |
|                   |             |      |
| XContentMapValues |             |      |
