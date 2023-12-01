# elasticsearch_package

## org.elasticsearch





| Class                            |      | Description                                                  |
| -------------------------------- | ---- | ------------------------------------------------------------ |
|                                  |      |                                                              |
| Assertions                       |      | Provides a static final field that can be used to check if assertions are enabled. |
|                                  |      |                                                              |
| Build                            |      | Information about a build of Elasticsearch.                  |
|                                  |      |                                                              |
| Build.Flavor                     |      |                                                              |
|                                  |      |                                                              |
| Build.Type                       |      |                                                              |
|                                  |      |                                                              |
| ElasticsearchCorruptionException |      | This exception is thrown when Elasticsearch detects an inconsistency in one of it's persistent files. |
|                                  |      |                                                              |
| ElasticsearchException           |      | A base class for all elasticsearch exceptions.               |
|                                  |      |                                                              |
| ElasticsearchGenerationException |      | A generic exception indicating failure to generate.          |
|                                  |      |                                                              |
| ElasticsearchParseException      |      | Unchecked exception that is translated into a 400 BAD REQUEST error when it bubbles out over HTTP. |
|                                  |      |                                                              |
| ElasticsearchSecurityException   |      | Generic security exception                                   |
|                                  |      |                                                              |
| ElasticsearchStatusException     |      | Exception who's RestStatus is arbitrary rather than derived. |
|                                  |      |                                                              |
| ElasticsearchTimeoutException    |      | The same as TimeoutException simply a runtime one.           |
|                                  |      |                                                              |
| ElasticsearchWrapperException    |      | An exception that is meant to be "unwrapped" when sent back to the user as an error because its is cause, if non-null is always more useful to the user than the exception itself. |
|                                  |      |                                                              |
| ExceptionsHelper                 |      |                                                              |
|                                  |      |                                                              |
| ResourceAlreadyExistsException   |      |                                                              |
|                                  |      |                                                              |
| ResourceNotFoundException        |      | Generic ResourceNotFoundException corresponding to the RestStatus.NOT_FOUND status code |
|                                  |      |                                                              |
| SpecialPermission                |      | Elasticsearch-specific permission to check before entering AccessController.doPrivileged() blocks. |
|                                  |      |                                                              |
| Version                          |      |                                                              |
|                                  |      |                                                              |