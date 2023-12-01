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
