# elasticsearch_package

## org.elasticsearch





| Class                            |      | Description                                                  |
| -------------------------------- | ---- | ------------------------------------------------------------ |
| Assertions                       |      | Provides a static final field that can be used to check if assertions are enabled. |
| Build                            |      | Information about a build of Elasticsearch.                  |
| Build.Flavor                     |      |                                                              |
| Build.Type                       |      |                                                              |
| ElasticsearchCorruptionException |      | This exception is thrown when Elasticsearch detects an inconsistency in one of it's persistent files. |
| ElasticsearchException           |      | A base class for all elasticsearch exceptions.               |
| ElasticsearchGenerationException |      | A generic exception indicating failure to generate.          |
| ElasticsearchParseException      |      | Unchecked exception that is translated into a 400 BAD REQUEST error when it bubbles out over HTTP. |
| ElasticsearchSecurityException   |      | Generic security exception                                   |
| ElasticsearchStatusException     |      | Exception who's RestStatus is arbitrary rather than derived. |
| ElasticsearchTimeoutException    |      | The same as TimeoutException simply a runtime one            |
| ElasticsearchWrapperException    |      | An exception that is meant to be "unwrapped" when sent back to the user as an error because its is cause, if non-null is always more useful to the user than the exception itself. |
| ExceptionsHelper                 |      |                                                              |
| ResourceAlreadyExistsException   |      |                                                              |
| ResourceNotFoundException        |      | Generic ResourceNotFoundException corresponding to the RestStatus.NOT_FOUND status code |
| SpecialPermission                |      | Elasticsearch-specific permission to check before entering AccessController.doPrivileged() blocks. |
| Version                          |      |                                                              |


### org.elasticsearch.action



| Class                                                        | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ActionFuture<T>                                              | An extension to Future allowing for simplified "get" operations. |
| ActionListener<Response>                                     | A listener for action responses or failures.                 |
| ActionListener.Delegating<Response,DelegateResponse>         |                                                              |
| ActionListener.DelegatingActionListener<T>                   |                                                              |
| ActionListener.DelegatingFailureActionListener<T,R>          |                                                              |
| ActionListener.MappedActionListener<Response,MappedResponse> |                                                              |
| ActionListener.RunAfterActionListener<T>                     |                                                              |
| ActionListener.RunBeforeActionListener<T>                    |                                                              |
| ActionListenerResponseHandler<Response extends TransportResponse> | A simple base class for action response listeners, defaulting to using the SAME executor (as its very common on response handlers). |
| ActionModule                                                 | Builds and binds the generic action map, all TransportActions, and ActionFilters. |
| ActionRequest                                                | ActionRequestBuilder<Request extends ActionRequest,Response extends ActionResponse> |
| ActionRequestValidationException                             |                                                              |
| ActionResponse                                               | Base class for responses to action requests.                 |
| ActionResponse.Empty                                         |                                                              |
| ActionRunnable<Response>                                     | Base class for Runnables that need to call ActionListener.onFailure(Exception) in case an uncaught exception or error is thrown while the actual action is run. |
| ActionType<Response extends ActionResponse>                  | A generic action.                                            |
| AliasesRequest                                               | Needs to be implemented by all ActionRequest subclasses that relate to one or more indices and one or more aliases. |
| CompositeIndicesRequest                                      | Marker interface that needs to be implemented by all ActionRequest subclasses that are composed of multiple sub-requests which relate to one or more indices. |
| DocWriteRequest<T>                                           | Generic interface to group ActionRequest, which perform writes to a single document Action requests implementing this can be part of BulkRequest |
| DocWriteRequest.OpType                                       | Requested operation type to perform on the document          |
| DocWriteResponse                                             | A base class for the response of a write operation that involves a single doc |
| DocWriteResponse.Builder                                     | Base class of all DocWriteResponse builders.                 |
| DocWriteResponse.Result                                      | An enum that represents the results of CRUD operations, primarily used to communicate the type of operation that occurred. |
| FailedNodeException                                          |                                                              |
| IndicesRequest                                               | Needs to be implemented by all ActionRequest subclasses that relate to one or more indices. |
| IndicesRequest.Replaceable                                   |                                                              |
| LatchedActionListener<T>                                     | An action listener that allows passing in a CountDownLatch that will be counted down after onResponse or onFailure is called |
| NoShardAvailableActionException                              |                                                              |
| NoSuchNodeException                                          |                                                              |
| NotifyOnceListener<Response>                                 | A listener that ensures that only one of onResponse or onFailure is called. |
| OriginalIndices                                              | Used to keep track of original indices within internal (e.g. |
| PrimaryMissingActionException                                |                                                              |
| RealtimeRequest                                              | Indicates that a request can execute in realtime (reads from the translog). |
| RequestValidators<T extends ActionRequest>                   |                                                              |
| RequestValidators.RequestValidator<T extends ActionRequest>  | A validator that validates an request associated with indices before executing it. |
| ResultDeduplicator<T,R>                                      | Deduplicator for arbitrary keys and results that can be used to ensure a given action is only executed once at a time for a given request. |
| RoutingMissingException                                      |                                                              |
| ShardOperationFailedException                                | An exception indicating that a failure occurred performing an operation on the shard. |
| SingleResultDeduplicator<T>                                  | Wraps an async action that consumes an ActionListener such that multiple invocations of SingleResultDeduplicator.execute(ActionListener) can share the result from a single call to the wrapped action. |
| StepListener<Response>                                       | A StepListener provides a simple way to write a flow consisting of multiple asynchronous steps without having nested callbacks. |
| TaskOperationFailure                                         | Information about task operation failures The class is final due to serialization limitations |
| ThreadingModel                                               |                                                              |
| TimestampParsingException                                    |                                                              |
| TransportActionNodeProxy<Request extends ActionRequest,Response extends ActionResponse> | A generic proxy that will execute the given action against a specific node. |
| UnavailableShardsException                                   |                                                              |
| ValidateActions                                              |                                                              |



### 





| package                              | 概述                                         |
| ------------------------------------ | -------------------------------------------- |
| org.elasticsearch.action.bulk        |                                              |
| org.elasticsearch.action.datastreams |                                              |
| org.elasticsearch.action.delete      |                                              |
| org.elasticsearch.action.explain     |                                              |
| org.elasticsearch.action.fieldcaps   |                                              |
| org.elasticsearch.action.get         |                                              |
| org.elasticsearch.action.index       |                                              |
| org.elasticsearch.action.ingest      |                                              |
| org.elasticsearch.action.main        |                                              |
| org.elasticsearch.action.resync      |                                              |
| org.elasticsearch.action.search      |                                              |
| org.elasticsearch.action.support     |                                              |
| org.elasticsearch.action.termvectors | Get the term vector for a specific document. |
| org.elasticsearch.action.update      |                                              |





#### org.elasticsearch.action.bulk

| Class                    | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| BackoffPolicy            | Provides a backoff policy for bulk requests.                 |
| BulkAction               |                                                              |
| BulkItemRequest          |                                                              |
| BulkItemResponse         | Represents a single item response for an action executed as part of the bulk API. |
| BulkItemResponse.Failure | Represents a failure.                                        |
| BulkProcessor            | A bulk processor is a thread safe bulk processing class, allowing to easily set when to "flush" a new bulk request (either based on number of actions, based on the size, or time), and to easily control the number of concurrent bulk requests allowed to be executed in parallel. |
| BulkProcessor.Builder    | A builder used to create a build an instance of a bulk processor. |
| BulkProcessor.Listener   | A listener for the execution.                                |
| BulkProcessor2           | A bulk processor is a thread safe bulk processing class, allowing to easily set when to "flush" a new bulk request (either based on number of actions, based on the size, or time), and to easily control the number of concurrent bulk requests allowed to be executed in parallel. |
| BulkProcessor2.Builder   | A builder used to create a build an instance of a bulk processor. |
| BulkProcessor2.Listener  | A listener for the execution.                                |
| BulkRequest              | A bulk request holds an ordered IndexRequests, DeleteRequests and UpdateRequests and allows to executes it in a single batch. |
| BulkRequestBuilder       | A bulk request holds an ordered IndexRequests and DeleteRequests and allows to executes it in a single batch. |
| BulkRequestHandler       | Implements the low-level details of bulk request handling    |
| BulkRequestParser        | Helper to parse bulk requests.                               |
| BulkResponse             | A response of a bulk execution.                              |
| BulkShardRequest         |                                                              |
| BulkShardResponse        |                                                              |
| MappingUpdatePerformer   |                                                              |
| Retry                    | Encapsulates synchronous and asynchronous retry logic.       |
| TransportBulkAction      | Groups bulk request items by shard, optionally creating non-existent indices and delegates to TransportShardBulkAction for shard-level bulk execution |
| TransportShardBulkAction | Performs shard-level bulk (index, delete or update) operations |



#### org.elasticsearch.action.datastreams



| Class                            |      |
| -------------------------------- | ---- |
| ModifyDataStreamsAction          |      |
| ModifyDataStreamsAction.Request  |      |
| ModifyDataStreamsTransportAction |      |





# org.elasticsearch.action.delete



| Class                  | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| DeleteAction           |                                                              |
| DeleteRequest          | A request to delete a document from an index based on its type and id. |
| DeleteRequestBuilder   | A delete document action request builder.                    |
| DeleteResponse         | The response of the delete action.                           |
| DeleteResponse.Builder | Builder class for DeleteResponse.                            |
| TransportDeleteAction  | Deprecated.                                                  |





#### org.elasticsearch.action.explain

| Class                  | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| ExplainAction          | Entry point for the explain feature.                         |
| ExplainRequest         | Explain request encapsulating the explain query and document identifier to get an explanation for. |
| ExplainRequestBuilder  | A builder for ExplainRequest.                                |
| ExplainResponse        | Response containing the score explanation.                   |
| TransportExplainAction | Explain transport action.                                    |





#### org.elasticsearch.action.fieldcaps



| Class                            | Description                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| FieldCapabilities                | Describes the capabilities of a field optionally merged across multiple indices. |
| FieldCapabilitiesAction          |                                                              |
| FieldCapabilitiesFailure         |                                                              |
| FieldCapabilitiesIndexRequest    |                                                              |
| FieldCapabilitiesIndexResponse   |                                                              |
| FieldCapabilitiesRequest         |                                                              |
| FieldCapabilitiesRequestBuilder  |                                                              |
| FieldCapabilitiesResponse        | Response for FieldCapabilitiesRequest requests.              |
| IndexFieldCapabilities           | Describes the capabilities of a field in a single index.     |
| TransportFieldCapabilitiesAction |                                                              |



#### org.elasticsearch.action.get



| Class                        | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| GetAction                    |                                                              |
| GetRequest                   | A request to get a document (its source) from an index based on its id. |
| GetRequestBuilder            | A get document action request builder.                       |
| GetResponse                  | The response of a get action.                                |
| MultiGetAction               |                                                              |
| MultiGetItemResponse         | A single multi get response.                                 |
| MultiGetRequest              |                                                              |
| MultiGetRequest.Item         | A single get item.                                           |
| MultiGetRequestBuilder       | A multi get document action request builder.                 |
| MultiGetResponse             |                                                              |
| MultiGetResponse.Failure     | Represents a failure.                                        |
| MultiGetShardRequest         |                                                              |
| MultiGetShardResponse        |                                                              |
| TransportGetAction           | Performs the get operation.                                  |
| TransportMultiGetAction      |                                                              |
| TransportShardMultiGetAction |                                                              |





# org.elasticsearch.action.index



| Class                 | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| IndexAction           |                                                              |
| IndexRequest          | Index request to index a typed JSON document into a specific index and make it searchable. |
| IndexRequestBuilder   | An index document action request builder.                    |
| IndexResponse         | A response of an index operation,                            |
| IndexResponse.Builder | Builder class for IndexResponse.                             |
| TransportIndexAction  | Deprecated.                                                  |





#### org.elasticsearch.action.ingest



| Class                           | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| DeletePipelineAction            |                                                              |
| DeletePipelineRequest           |                                                              |
| DeletePipelineRequestBuilder    |                                                              |
| DeletePipelineTransportAction   |                                                              |
| GetPipelineAction               |                                                              |
| GetPipelineRequest              |                                                              |
| GetPipelineRequestBuilder       |                                                              |
| GetPipelineResponse             |                                                              |
| GetPipelineTransportAction      |                                                              |
| IngestActionForwarder           | A utility for forwarding ingest requests to ingest nodes in a round-robin fashion. |
| PutPipelineAction               |                                                              |
| PutPipelineRequest              |                                                              |
| PutPipelineRequestBuilder       |                                                              |
| PutPipelineTransportAction      |                                                              |
| SimulateDocumentBaseResult      | Holds the end result of what a pipeline did to sample document provided via the simulate api. |
| SimulateDocumentResult          |                                                              |
| SimulateDocumentVerboseResult   | Holds the result of what a pipeline did to a sample document via the simulate api, but instead of SimulateDocumentBaseResult this result class holds the intermediate result each processor did to the sample document. |
| SimulatePipelineAction          |                                                              |
| SimulatePipelineRequest         |                                                              |
| SimulatePipelineRequest.Fields  |                                                              |
| SimulatePipelineRequestBuilder  |                                                              |
| SimulatePipelineResponse        |                                                              |
| SimulatePipelineTransportAction |                                                              |
| SimulateProcessorResult         |                                                              |





#### org.elasticsearch.action.main



| Class               | Description |
| ------------------- | ----------- |
| MainAction          |             |
| MainRequest         |             |
| MainRequestBuilder  |             |
| MainResponse        |             |
| TransportMainAction |             |





#### org.elasticsearch.action.resync



| Class                            | Description                                                  |      |
| -------------------------------- | ------------------------------------------------------------ | ---- |
| ResyncReplicationRequest         | Represents a batch of operations sent from the primary to its replicas during the primary-replica resync. |      |
| ResyncReplicationResponse        |                                                              |      |
| TransportResyncReplicationAction |                                                              |      |





#### org.elasticsearch.action.search



| Class                                            | Description                                                  |      |      |
| ------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| CanMatchNodeRequest                              | Node-level request used during can-match phase               |      |      |
| CanMatchNodeRequest.Shard                        |                                                              |      |      |
| CanMatchNodeResponse                             |                                                              |      |      |
| CanMatchNodeResponse.ResponseOrFailure           |                                                              |      |      |
| ClearScrollAction                                |                                                              |      |      |
| ClearScrollController                            |                                                              |      |      |
| ClearScrollRequest                               |                                                              |      |      |
| ClearScrollRequestBuilder                        |                                                              |      |      |
| ClearScrollResponse                              |                                                              |      |      |
| ClosePointInTimeAction                           |                                                              |      |      |
| ClosePointInTimeRequest                          |                                                              |      |      |
| ClosePointInTimeResponse                         |                                                              |      |      |
| MaxScoreCollector                                | A collector that computes the maximum score.                 |      |      |
| MultiSearchAction                                |                                                              |      |      |
| MultiSearchRequest                               | A multi search API request.                                  |      |      |
| MultiSearchRequestBuilder                        | A request builder for multiple search requests.              |      |      |
| MultiSearchResponse                              | A multi search response.                                     |      |      |
| MultiSearchResponse.Item                         | A search response item, holding the actual search response, or an error message if it failed. |      |      |
| OpenPointInTimeAction                            |                                                              |      |      |
| OpenPointInTimeRequest                           |                                                              |      |      |
| OpenPointInTimeResponse                          |                                                              |      |      |
| ParsedScrollId                                   |                                                              |      |      |
| QueryPhaseResultConsumer                         | A ArraySearchPhaseResults implementation that incrementally reduces aggregation results as shard results are consumed. |      |      |
| ReduceSearchPhaseException                       | A failure during a reduce phase (when receiving results from several shards, and reducing them into one or more results and possible actions). |      |      |
| RestClosePointInTimeAction                       |                                                              |      |      |
| RestOpenPointInTimeAction                        |                                                              |      |      |
| SearchAction                                     |                                                              |      |      |
| SearchContextId                                  |                                                              |      |      |
| SearchContextIdForNode                           |                                                              |      |      |
| SearchExecutionStatsCollector                    | A wrapper of search action listeners (search results) that unwraps the query result to get the piggybacked queue size and service time EWMA, adding those values to the coordinating nodes' ResponseCollectorService. |      |      |
| SearchPhaseController                            |                                                              |      |      |
| SearchPhaseController.ReducedQueryPhase          |                                                              |      |      |
| SearchPhaseExecutionException                    |                                                              |      |      |
| SearchProgressActionListener                     | An ActionListener for search requests that allows to track progress of the SearchAction. |      |      |
| SearchProgressListener                           | A listener that allows to track progress of the SearchAction. |      |      |
| SearchRequest                                    | A request to execute search against one or more indices (or all). |      |      |
| SearchRequestBuilder                             | A search action request builder.                             |      |      |
| SearchResponse                                   | A response of a search request.                              |      |      |
| SearchResponse.Clusters                          | Holds info about the clusters that the search was executed on: how many in total, how many of them were successful and how many of them were skipped. |      |      |
| SearchResponseSections                           | Base class that holds the various sections which a search response is composed of (hits, aggs, suggestions etc.) and allows to retrieve them. |      |      |
| SearchScrollAction                               |                                                              |      |      |
| SearchScrollRequest                              |                                                              |      |      |
| SearchScrollRequestBuilder                       | A search scroll action request builder.                      |      |      |
| SearchShard                                      | A class that encapsulates the ShardId and the cluster alias of a shard used during the search action. |      |      |
| SearchShardIterator                              | Extension of PlainShardIterator used in the search api, which also holds the OriginalIndices of the search request (useful especially with cross-cluster search, as each cluster has its own set of original indices) as well as the cluster alias. |      |      |
| SearchShardTask                                  | Task storing information about a currently running search shard request. |      |      |
| SearchTask                                       | Task storing information about a currently running SearchRequest. |      |      |
| SearchTransportService                           | An encapsulation of SearchService operations exposed through transport. |      |      |
| SearchTransportService.SearchFreeContextResponse |                                                              |      |      |
| SearchType                                       | Search type represent the manner at which the search operation is executed. |      |      |
| ShardSearchFailure                               | Represents a failure to search on a specific shard.          |      |      |
| TransportClearScrollAction                       |                                                              |      |      |
| TransportClosePointInTimeAction                  |                                                              |      |      |
| TransportMultiSearchAction                       |                                                              |      |      |
| TransportOpenPointInTimeAction                   |                                                              |      |      |
| TransportSearchAction                            |                                                              |      |      |
| TransportSearchAction.SinglePhaseSearchAction    |                                                              |      |      |
| TransportSearchScrollAction                      |                                                              |      |      |
| VersionMismatchException                         |                                                              |      |      |





#### org.elasticsearch.action.support



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| ActionFilter                                                 | A filter allowing to filter transport actions                |      |      |
| ActionFilter.Simple                                          | A simple base class for injectable action filters that spares the implementation from handling the filter chain. |      |      |
| ActionFilterChain<Request extends ActionRequest,Response extends ActionResponse> | A filter chain allowing to continue and process the transport action request |      |      |
| ActionFilters                                                | Holds the action filters injected through plugins, properly sorted by ActionFilter.order() |      |      |
| ActiveShardCount                                             | A class whose instances represent a value for counting the number of active shard copies for a given shard in an index. |      |      |
| ActiveShardsObserver                                         | This class provides primitives for waiting for a configured number of shards to become active before sending a response on an ActionListener. |      |      |
| AdapterActionFuture<T,L>                                     |                                                              |      |      |
| AutoCreateIndex                                              | Encapsulates the logic of whether a new index should be automatically created when a write operation is about to happen in a non existing index. |      |      |
| ChannelActionListener<Response extends TransportResponse,Request extends TransportRequest> |                                                              |      |      |
| ContextPreservingActionListener<R>                           | Restores the given ThreadContext.StoredContext once the listener is invoked |      |      |
| DefaultShardOperationFailedException                         |                                                              |      |      |
| DestructiveOperations                                        | Helper for dealing with destructive operations and wildcard usage. |      |      |
| GroupedActionListener<T>                                     | An action listener that delegates its results to another listener once it has received N results (either successes or failures). |      |      |
| HandledTransportAction<Request extends ActionRequest,Response extends ActionResponse> | A TransportAction that self registers a handler into the transport service |      |      |
| IndicesOptions                                               | Controls how to deal with unavailable concrete indices (closed or missing), how wildcard expressions are expanded to actual indices (all, closed or open indices) and how to deal with wildcard expressions that resolve to no indices. |      |      |
| IndicesOptions.Option                                        |                                                              |      |      |
| IndicesOptions.WildcardStates                                |                                                              |      |      |
| ListenableActionFuture<T>                                    | A Future and ActionListener against which which other ActionListeners can be registered later, to support fanning-out a result to a dynamic collection of listeners. |      |      |
| ListenerTimeouts                                             |                                                              |      |      |
| NodeResponseTracker                                          | This class tracks the intermediate responses that will be used to create aggregated cluster response to a request. |      |      |
| NodeResponseTracker.DiscardedResponsesException              | This exception is thrown when the NodeResponseTracker is asked to give information about the responses after they have been discarded. |      |      |
| PlainActionFuture<T>                                         |                                                              |      |      |
| RetryableAction<Response>                                    | A action that will be retried on failure if RetryableAction.shouldRetry(Exception) returns true. |      |      |
| ThreadedActionListener<Response>                             | An action listener that wraps another action listener and threading its execution. |      |      |
| ThreadedActionListener.Wrapper                               | Wrapper that can be used to automatically wrap a listener in a threaded listener if needed. |      |      |
| TransportAction<Request extends ActionRequest,Response extends ActionResponse> |                                                              |      |      |
| TransportActions                                             |                                                              |      |      |
| WriteRequest<R extends WriteRequest<R>>                      | Interface implemented by requests that modify the documents in an index like IndexRequest, UpdateRequest, and BulkRequest. |      |      |
| WriteRequest.RefreshPolicy                                   |                                                              |      |      |
| WriteRequestBuilder<B extends WriteRequestBuilder<B>>        |                                                              |      |      |
| WriteResponse                                                | Interface implemented by responses for actions that modify the documents in an index like IndexResponse, UpdateResponse, and BulkResponse. |      |      |





#### org.elasticsearch.action.support.broadcast



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| BroadcastOperationRequestBuilder<Request extends BroadcastRequest<Request>,Response extends BroadcastResponse,RequestBuilder extends BroadcastOperationRequestBuilder<Request,Response,RequestBuilder>> |                                                              |      |      |
| BroadcastRequest<Request extends BroadcastRequest<Request>>  |                                                              |      |      |
| BroadcastResponse                                            | Base class for all broadcast operation based responses.      |      |      |
| BroadcastShardOperationFailedException                       | An exception indicating that a failure occurred performing an operation on the shard. |      |      |
| BroadcastShardRequest                                        |                                                              |      |      |
| BroadcastShardResponse                                       |                                                              |      |      |





#### org.elasticsearch.action.support.broadcast.node



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| TransportBroadcastByNodeAction<Request extends BroadcastRequest<Request>,Response extends BroadcastResponse,ShardOperationResult extends Writeable> | Abstraction for transporting aggregated shard-level operations in a single request (NodeRequest) per-node and executing the shard-level operations serially on the receiving node. |      |      |
| TransportBroadcastByNodeAction.EmptyResult                   | Can be used for implementations of shardOperation for which there is no shard-level return value. |      |      |





#### org.elasticsearch.action.support.master

| Class                                                        | Description                                                  |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| AcknowledgedRequest<Request extends MasterNodeRequest<Request>> | Abstract class that allows to mark action requests that support acknowledgements. |      |
| AcknowledgedRequestBuilder<Request extends AcknowledgedRequest<Request>,Response extends AcknowledgedResponse,RequestBuilder extends AcknowledgedRequestBuilder<Request,Response,RequestBuilder>> | Base request builder for master node operations that support acknowledgements |      |
| AcknowledgedResponse                                         | A response that indicates that a request has been acknowledged |      |
| AcknowledgedTransportMasterNodeAction<Request extends MasterNodeRequest<Request>> | Base class for the common case of a TransportMasterNodeAction that responds with an AcknowledgedResponse. |      |
| MasterNodeOperationRequestBuilder<Request extends MasterNodeRequest<Request>,Response extends ActionResponse,RequestBuilder extends MasterNodeOperationRequestBuilder<Request,Response,RequestBuilder>> | Base request builder for master node operations              |      |
| MasterNodeReadOperationRequestBuilder<Request extends MasterNodeReadRequest<Request>,Response extends ActionResponse,RequestBuilder extends MasterNodeReadOperationRequestBuilder<Request,Response,RequestBuilder>> | Base request builder for master node read operations that can be executed on the local node as well |      |
| MasterNodeReadRequest<Request extends MasterNodeReadRequest<Request>> | Base request for master based read operations that allows to read the cluster state from the local node if needed |      |
| MasterNodeRequest<Request extends MasterNodeRequest<Request>> | A based request for master based operation.                  |      |
| ShardsAcknowledgedResponse                                   |                                                              |      |
| TransportMasterNodeAction<Request extends MasterNodeRequest<Request>,Response extends ActionResponse> | A base class for operations that needs to be performed on the master node. |      |
| TransportMasterNodeReadAction<Request extends MasterNodeReadRequest<Request>,Response extends ActionResponse> | A base class for read operations that needs to be performed on the master node. |      |





#### org.elasticsearch.action.support.master.info



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
| ClusterInfoRequest<Request extends ClusterInfoRequest<Request>> |             |      |      |
| ClusterInfoRequestBuilder<Request extends ClusterInfoRequest<Request>,Response extends ActionResponse,Builder extends ClusterInfoRequestBuilder<Request,Response,Builder>> |             |      |      |
| TransportClusterInfoAction<Request extends ClusterInfoRequest<Request>,Response extends ActionResponse> |             |      |      |





#### org.elasticsearch.action.support.nodes



| Class                                                        | Description                             |      |
| ------------------------------------------------------------ | --------------------------------------- | ---- |
| BaseNodeRequest                                              |                                         |      |
| BaseNodeResponse                                             | A base class for node level operations. |      |
| BaseNodesRequest<Request extends BaseNodesRequest<Request>>  |                                         |      |
| BaseNodesResponse<TNodeResponse extends BaseNodeResponse>    |                                         |      |
| NodesOperationRequestBuilder<Request extends BaseNodesRequest<Request>,Response extends BaseNodesResponse<?>,RequestBuilder extends NodesOperationRequestBuilder<Request,Response,RequestBuilder>> |                                         |      |
| TransportNodesAction<NodesRequest extends BaseNodesRequest<NodesRequest>,NodesResponse extends BaseNodesResponse<?>,NodeRequest extends BaseNodeRequest,NodeResponse extends BaseNodeResponse> |                                         |      |





##### org.elasticsearch.action.support.replication



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| BasicReplicationRequest                                      | A replication request that has no more information than ReplicationRequest. |      |      |
| PendingReplicationActions                                    |                                                              |      |      |
| ReplicatedWriteRequest<R extends ReplicatedWriteRequest<R>>  | Requests that are both ReplicationRequests (run on a shard's primary first, then the replica) and WriteRequest (modify documents on a shard), for example BulkShardRequest, IndexRequest, and DeleteRequest. |      |      |
| ReplicationOperation<Request extends ReplicationRequest<Request>,ReplicaRequest extends ReplicationRequest<ReplicaRequest>,PrimaryResultT extends ReplicationOperation.PrimaryResult<ReplicaRequest>> |                                                              |      |      |
| ReplicationOperation.Primary<RequestT extends ReplicationRequest<RequestT>,ReplicaRequestT extends ReplicationRequest<ReplicaRequestT>,PrimaryResultT extends ReplicationOperation.PrimaryResult<ReplicaRequestT>> | An encapsulation of an operation that is to be performed on the primary shard |      |      |
| ReplicationOperation.PrimaryResult<RequestT extends ReplicationRequest<RequestT>> |                                                              |      |      |
| ReplicationOperation.ReplicaResponse                         | An interface to encapsulate the metadata needed from replica shards when they respond to operations performed on them. |      |      |
| ReplicationOperation.Replicas<RequestT extends ReplicationRequest<RequestT>> | An encapsulation of an operation that will be executed on the replica shards, if present. |      |      |
| ReplicationOperation.RetryOnPrimaryException                 |                                                              |      |      |
| ReplicationRequest<Request extends ReplicationRequest<Request>> | Requests that are run on a particular replica, first on the primary and then on the replicas like IndexRequest or TransportShardRefreshAction. |      |      |
| ReplicationRequestBuilder<Request extends ReplicationRequest<Request>,Response extends ActionResponse,RequestBuilder extends ReplicationRequestBuilder<Request,Response,RequestBuilder>> |                                                              |      |      |
| ReplicationResponse                                          | Base class for write action responses.                       |      |      |
| ReplicationResponse.ShardInfo                                |                                                              |      |      |
| ReplicationResponse.ShardInfo.Failure                        |                                                              |      |      |
| ReplicationTask                                              | Task that tracks replication actions.                        |      |      |
| ReplicationTask.Status                                       |                                                              |      |      |
| TransportBroadcastReplicationAction<Request extends BroadcastRequest<Request>,Response extends BroadcastResponse,ShardRequest extends ReplicationRequest<ShardRequest>,ShardResponse extends ReplicationResponse> | Base class for requests that should be executed on all shards of an index or several indices. |      |      |
| TransportReplicationAction<Request extends ReplicationRequest<Request>,ReplicaRequest extends ReplicationRequest<ReplicaRequest>,Response extends ReplicationResponse> | Base class for requests that should be executed on a primary copy followed by replica copies. |      |      |
| TransportReplicationAction.ConcreteReplicaRequest<R extends TransportRequest> |                                                              |      |      |
| TransportReplicationAction.ConcreteShardRequest<R extends TransportRequest> | a wrapper class to encapsulate a request when being sent to a specific allocation id |      |      |
| TransportReplicationAction.PrimaryResult<ReplicaRequest extends ReplicationRequest<ReplicaRequest>,Response extends ReplicationResponse> |                                                              |      |      |
| TransportReplicationAction.ReplicaResponse                   |                                                              |      |      |
| TransportReplicationAction.ReplicaResult                     |                                                              |      |      |
| TransportReplicationAction.RetryOnReplicaException           |                                                              |      |      |
| TransportWriteAction<Request extends ReplicatedWriteRequest<Request>,ReplicaRequest extends ReplicatedWriteRequest<ReplicaRequest>,Response extends ReplicationResponse & WriteResponse> | Base class for transport actions that modify data in some shard like index, delete, and shardBulk. |      |      |
| TransportWriteAction.WritePrimaryResult<ReplicaRequest extends ReplicatedWriteRequest<ReplicaRequest>,Response extends ReplicationResponse & WriteResponse> | Result of taking the action on the primary.                  |      |      |
| TransportWriteAction.WriteReplicaResult<ReplicaRequest extends ReplicatedWriteRequest<ReplicaRequest>> | Result of taking the action on the replica.                  |      |      |





#### org.elasticsearch.action.support.single.instance



| Class                                                        | Description |      |      |
| ------------------------------------------------------------ | ----------- | ---- | ---- |
| InstanceShardOperationRequest<Request extends InstanceShardOperationRequest<Request>> |             |      |      |
| InstanceShardOperationRequestBuilder<Request extends InstanceShardOperationRequest<Request>,Response extends ActionResponse,RequestBuilder extends InstanceShardOperationRequestBuilder<Request,Response,RequestBuilder>> |             |      |      |
| TransportInstanceSingleOperationAction<Request extends InstanceShardOperationRequest<Request>,Response extends ActionResponse> |             |      |      |



#### org.elasticsearch.action.support.single.shard



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| SingleShardOperationRequestBuilder<Request extends SingleShardRequest<Request>,Response extends ActionResponse,RequestBuilder extends SingleShardOperationRequestBuilder<Request,Response,RequestBuilder>> |                                                              |      |      |
| SingleShardRequest<Request extends SingleShardRequest<Request>> |                                                              |      |      |
| TransportSingleShardAction<Request extends SingleShardRequest<Request>,Response extends ActionResponse> | A base class for operations that need to perform a read operation on a single shard copy. |      |      |





#### org.elasticsearch.action.support.tasks



| Class                                                        | Description                                                  |      |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | ---- |
| BaseTasksRequest<Request extends BaseTasksRequest<Request>>  | A base class for task requests                               |      |      |
| BaseTasksResponse                                            | Base class for responses of task-related operations          |      |      |
| TasksRequestBuilder<Request extends BaseTasksRequest<Request>,Response extends BaseTasksResponse,RequestBuilder extends TasksRequestBuilder<Request,Response,RequestBuilder>> | Builder for task-based requests                              |      |      |
| TransportTasksAction<OperationTask extends Task,TasksRequest extends BaseTasksRequest<TasksRequest>,TasksResponse extends BaseTasksResponse,TaskResponse extends Writeable> | The base class for transport actions that are interacting with currently running tasks. |      |      |





#### org.elasticsearch.action.termvectors



| Class                                | Description                                                  |      |
| ------------------------------------ | ------------------------------------------------------------ | ---- |
| MultiTermVectorsAction               |                                                              |      |
| MultiTermVectorsItemResponse         | A single multi get response.                                 |      |
| MultiTermVectorsRequest              |                                                              |      |
| MultiTermVectorsRequestBuilder       |                                                              |      |
| MultiTermVectorsResponse             |                                                              |      |
| MultiTermVectorsResponse.Failure     | Represents a failure.                                        |      |
| MultiTermVectorsShardRequest         |                                                              |      |
| MultiTermVectorsShardResponse        |                                                              |      |
| TermVectorsAction                    |                                                              |      |
| TermVectorsFields                    | This class represents the result of a TermVectorsRequest.    |      |
| TermVectorsFilter                    |                                                              |      |
| TermVectorsFilter.ScoreTerm          |                                                              |      |
| TermVectorsRequest                   | Request returning the term vector (doc frequency, positions, offsets) for a document. |      |
| TermVectorsRequest.FilterSettings    |                                                              |      |
| TermVectorsRequest.Flag              |                                                              |      |
| TermVectorsRequestBuilder            | The builder class for a term vector request.                 |      |
| TermVectorsResponse                  |                                                              |      |
| TransportMultiTermVectorsAction      |                                                              |      |
| TransportShardMultiTermsVectorAction |                                                              |      |
| TransportTermVectorsAction           | Performs the get operation.                                  |      |





#### org.elasticsearch.action.update



| Class                                                        | Description |      |
| ------------------------------------------------------------ | ----------- | ---- |
|                                                              |             |      |
| TransportUpdateAction                                        |             |      |
|                                                              |             |      |
| UpdateAction                                                 |             |      |
|                                                              |             |      |
| UpdateHelper                                                 |             |      |
| Helper for translating an update request to an index, delete request or update response. |             |      |
| UpdateHelper.ContextFields                                   |             |      |
| Field names used to populate the script context              |             |      |
| UpdateHelper.Result                                          |             |      |
|                                                              |             |      |
| UpdateRequest                                                |             |      |
|                                                              |             |      |
| UpdateRequestBuilder                                         |             |      |
|                                                              |             |      |
| UpdateResponse                                               |             |      |
|                                                              |             |      |
| UpdateResponse.Builder                                       |             |      |
| Builder class for UpdateResponse.                            |             |      |







#### org.elasticsearch.bootstrap



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| BootstrapCheck                                               |      |      |      |
| Encapsulates a bootstrap check.                              |      |      |      |
| BootstrapCheck.BootstrapCheckResult                          |      |      |      |
| Encapsulate the result of a bootstrap check.                 |      |      |      |
| BootstrapContext                                             |      |      |      |
| Context that is passed to every bootstrap check to make decisions on. |      |      |      |
| BootstrapInfo                                                |      |      |      |
| Exposes system startup information                           |      |      |      |
| BootstrapSettings                                            |      |      |      |
|                                                              |      |      |      |
| ConsoleCtrlHandler                                           |      |      |      |
|                                                              |      |      |      |
| FilePermissionUtils                                          |      |      |      |
|                                                              |      |      |      |
| PluginPolicyInfo                                             |      |      |      |
|                                                              |      |      |      |
| PolicyUtil                                                   |      |      |      |





#### org.elasticsearch.bootstrap.plugins



| Class                                                        |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- |
| Description                                                  |      |      |      |
| LoggerTerminal                                               |      |      |      |
|                                                              |      |      |      |
| PluginsManager                                               |      |      |      |
| This class is responsible for adding, updating or removing plugins so that the list of installed plugins matches those in the elasticsearch-plugins.yml config file. |      |      |      |





