# drogon

https://www.cnblogs.com/zx-admin/p/14028089.html

学sprigmvc的，控制器自动发现

testdrogon

    message(FATAL_ERROR "c++17 or higher is required")
有命令行工具

依赖jsoncpp

#include <drogon/orm/DbClient.h>

## 配置项目
    drogon::app().loadConfigFile("config.json");

    app().loadConfigFile("./config.json").run();

## vcpkg
vcpkg search drogon
drogon                   1.9.10           A C++14/17 based HTTP web application framework running on Linux/macOS/Uni...
drogon[ctl]                               Build drogon_ctl tool.
drogon[mysql]                             Support reading and writing from/to MySQL databases.
drogon[orm]                               Build with object-relational mapping support.
drogon[postgres]                          Support reading and writing from/to Postgres databases.
drogon[redis]                             Support reading and writing from/to Redis databases.
drogon[sqlite3]                           Support reading and writing from/to SQLite databases.
drogon[yaml]                              Support YAML Drogon configuration files

vcpkg install jsoncpp:x64-windows zlib:x64-windows openssl:x64-windows sqlite3:x64-windows libpq:x64-windows libpqxx:x64-windows libmariadb drogon[core,ctl,sqlite3,postgres,mysql,orm]:x64-windows --recurse


 .\drogon_ctl.exe version
     _
  __| |_ __ ___   __ _  ___  _ __
 / _` | '__/ _ \ / _` |/ _ \| '_ \
| (_| | | | (_) | (_| | (_) | | | |
 \__,_|_|  \___/ \__, |\___/|_| |_|
                 |___/

A utility for drogon
Version: 1.9.10
Git commit:
Compilation:
  Compiler: cl.exe
  Compiler ID: MSVC
  Compilation flags: /MD /O2 /Oi /Gy /DNDEBUG /Z7  -std=c++20 -ID:/develops/tools/vcpkg/installed/x64-windows/include -ID:/develops/tools/vcpkg/packages/drogon_x64-windows/include
Libraries:
  postgresql: yes  (pipeline mode: yes)
  mariadb: yes
  sqlite3: yes
  ssl/tls backend: OpenSSL
  brotli: yes
  hiredis: no
  c-ares: yes
  yaml-cpp: no


     _
  __| |_ __ ___   __ _  ___  _ __
 / _` | '__/ _ \ / _` |/ _ \| '_ \
| (_| | | | (_) | (_| | (_) | | | |
 \__,_|_|  \___/ \__, |\___/|_| |_|
                 |___/
A utility for drogon
Version: 1.9.10
Git commit: cbf63f8fc4d849bbb82eeb1c83fcf8ff953f19f3
Compilation: 
  Compiler: c++
  Compiler ID: GNU
  Compilation flags: -std=c++17 -I/usr/include/jsoncpp -I/usr/local/include
Libraries: 
  postgresql: yes  (pipeline mode: yes)
  mariadb: yes
  sqlite3: yes
  ssl/tls backend: OpenSSL
  brotli: yes
  hiredis: yes
  c-ares: yes
  yaml-cpp: yes


```shell
    app().addListener("127.0.0.1", 8848).run();
    app().addListener("0.0.0.0", 8848).run();
```

一个是只绑定localhost，另一个是任意ip

同样的代码，vcpkg处理的依赖库，win报错，ubuntu正常


    

drogon_ctl create model 
/home/wdidada/vcpkg/installed/x64-linux/tools/drogon/drogon_ctl create project xxx

/home/wdidada/vcpkg/installed/x64-linux/tools/drogon/drogon_ctl create model modles


/home/wdidada/vcpkg/installed/x64-linux/tools/drogon/drogon_ctl create filter LoggingInterceptor
https://blog.csdn.net/weixin_50308184/article/details/134359378

## website

https://drogon.org/

## class api doc

### doxygen
file:///D:/develops/git/github/cpp/drogon/docs/html/namespaces.html

https://drogonframework.github.io/drogon-docs/#/

### DrObjectBase

struct isAutoCreationClass

template <typename T>
class DrObject : public virtual DrObjectBase

### DrClassMap

class HttpControllerBase
class HttpSimpleControllerBase
class WebSocketControllerBase


## 依赖库
### trantor


### A
AAcceptor (trantor)
AccessLogger (drogon::plugin)
AopAdvice (drogon)
ApiTest (api::v1)
AresResolver (trantor)
ArgumentError (drogon::orm)
ArrayParser (drogon::orm)
AsyncBufferNode (trantor)
AsyncFileLogger (trantor)
AsyncStream (trantor)
AsyncStreamImplAsyncTask (drogon)
Attachment (api)
Attributes (drogon)
await_result (drogon)

### B
BBase64CharMap (drogon::utils)
BaseBuilder (drogon::orm)
BeginAdviceTestBinderArgTypeTraits (drogon::internal)
BinderArgTypeTraits< const T & > (drogon::internal)
BinderArgTypeTraits< const T && > (drogon::internal)
BinderArgTypeTraits< T & > (drogon::internal)
BinderArgTypeTraits< T && > (drogon::internal)
BinderArgTypeTraits< T * > (drogon::internal)
blake2b_paramblake2b_stateBlog (drogon_model::drogonTestMysql)
Blog (drogon_model::sqlite3)
Blog (drogon_model::postgres)
BlogTag (drogon_model::drogonTestMysql)
BlogTag (drogon_model::postgres)
BlogTag (drogon_model::sqlite3)
BotanCertificateBotanTLSProviderBrokenConnection (drogon::orm)
MultipartStreamParser::Buffer (drogon)
BufferNode (trantor)
MpscQueue::BufferNode (trantor)

### C
CCacheFile (drogon)
CacheMap (drogon)
CallbackArgTypeTraits (drogon::orm::internal)
CallbackArgTypeTraits< const T & > (drogon::orm::internal)
CallbackArgTypeTraits< T & > (drogon::orm::internal)
CallbackArgTypeTraits< T && > (drogon::orm::internal)
CallbackArgTypeTraits< T * > (drogon::orm::internal)
CallbackAwaiter (drogon)
CallbackAwaiter< void > (drogon)
CallbackEntry (drogon)
TimingWheel::CallbackEntry (trantor)
CallbackHolder (drogon::orm::internal)
CallbackHolderBase (drogon::orm::internal)
CallbackParamPackCanConstructFromString (drogon::internal)
CanConvertFromString (drogon::internal)
CanConvertFromStringStream (drogon::internal)
CanConvertFromStringStream< T, std::void_t< decltype(std::declval< std::stringstream & >()
 >> std::declval< T & >()
)
> > (drogon::internal)
CanConvertToString (drogon::internal)
CanConvertToString< T, std::void_t< decltype(std::to_string(std::declval< T >()
)
)
> > (drogon::internal)
Case (drogon::test)
CaseBase (drogon::test)
Category (drogon_model::drogonTestMysql)
Category (drogon_model::postgres)
Category (drogon_model::sqlite3)
Certificate (trantor)
Channel (trantor)
CheckViolation (drogon::orm)
ChunkingParamsRealIpResolver::CIDR (drogon::plugin)
Collector (drogon::monitoring)
CollectorBase (drogon::monitoring)
Wallets::Cols (drogon_model::sqlite3)
Users::Cols (drogon_model::sqlite3)
Tag::Cols (drogon_model::sqlite3)
Groups::Cols (drogon_model::sqlite3)
Category::Cols (drogon_model::sqlite3)
BlogTag::Cols (drogon_model::sqlite3)
Blog::Cols (drogon_model::sqlite3)
Wallets::Cols (drogon_model::postgres)
Users::Cols (drogon_model::postgres)
Category::Cols (drogon_model::postgres)
Tag::Cols (drogon_model::postgres)
Blog::Cols (drogon_model::drogonTestMysql)
BlogTag::Cols (drogon_model::drogonTestMysql)
Category::Cols (drogon_model::drogonTestMysql)
Tag::Cols (drogon_model::drogonTestMysql)
Wallets::Cols (drogon_model::drogonTestMysql)
Blog::Cols (drogon_model::postgres)
BlogTag::Cols (drogon_model::postgres)
Users::Cols (drogon_model::drogonTestMysql)
ColumnInfo (drogon_ctl)
CommandHandlerComparsionResult (drogon::test::internal)
ConcurrentTaskQueue (trantor)
ConfigAdapter (drogon)
ConfigAdapterManager (drogon)
ConfigLoader (drogon)
Connector (trantor)
ConstResultIterator (drogon::orm)
ConstReverseResultIterator (drogon::orm)
ConstReverseRowIterator (drogon::orm)
ConstRowIterator (drogon::orm)
ConstructibleFromStringCacheMap::ControlBlock (drogon)
ControllerBinderBase (drogon)
ConversionError (drogon::orm)
ConvertibleFromStringConvertibleFromStringStreamConvertMethod (drogon_ctl)
Cookie (drogon)
CookieSameSiteControllerCookieSameSiteSequenceCoroFilterMutex::CoroMutexAwaiter (drogon)
CoroTest (api::v1)
Counter (drogon::monitoring)
create (drogon_ctl)
create_controller (drogon_ctl)
create_filter (drogon_ctl)
create_model (drogon_ctl)
create_plugin (drogon_ctl)
create_project (drogon_ctl)
create_view (drogon_ctl)
CredentialsCriteria (drogon::orm)
CtrlCustomCtrlCustomHeaderFilterCustomSql (drogon::orm)

### D
DataException (drogon::orm)
DataPackDate (trantor)
DbClient (drogon::orm)
DbClientImpl (drogon::orm)
DbClientLockFree (drogon::orm)
DbClientManager (drogon::orm)
DbConnection (drogon::orm)
DbClientManager::DbInfo (drogon::orm)
DbListener (drogon::orm)
DeadlockDetected (drogon::orm)
Decomposer (drogon::test::internal)
DefaultStreamReader (drogon)
DefaultValue (drogon::orm)
DigestAuthFilterDiskFull (drogon::orm)
SharedLibManager::DLStat (drogon)
DoNothingPluginDrObject::DrAllocator (drogon)
DrClassMap (drogon)
DrObject (drogon)
DrObjectBase (drogon)
DrogonDbException (drogon::orm)
DrogonFileLocker (drogon)
DrTemplate (drogon)
DrTemplateBase (drogon)

### E
EndAwaiter (drogon::internal)
epoll_dataepoll_eventEpollPoller (trantor)
EventLoop (trantor)
EventLoopAwaiter (drogon::internal)
EventLoopThread (trantor)
EventLoopThreadPool (trantor)

### F
Failure (drogon::orm)
FeatureNotSupported (drogon::orm)
Field (drogon::orm)
FileBufferNode (trantor)
FileRange (drogon)
FileStatFilter (drogon::orm)
FilterBuilder (drogon::orm)
final_awaiter (drogon)
FixedBuffer (trantor::detail)
FixedWindowRateLimiter (drogon)
Fmt (trantor)
ForeignKeyViolation (drogon::orm)
ForwardCtrlFunctionTraits (drogon::internal)
FunctionTraits (drogon::orm::internal)
FunctionTraits< ReturnType(*)
(Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(*)
(Arguments...)
> (drogon::orm::internal)
FunctionTraits< ReturnType(*)
(bool, Arguments...)
> (drogon::orm::internal)
FunctionTraits< ReturnType(*)
(const HttpRequestPtr &req, RequestStreamPtr &&streamCtx, std::function< void(const HttpResponsePtr &)
> &&callback, Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(*)
(const HttpRequestPtr &req, std::function< void(const HttpResponsePtr &)
> &&callback, Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(*)
(HttpRequestPtr &&req, std::function< void(const HttpResponsePtr &)
> &&callback, Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(*)
(HttpRequestPtr &req, std::function< void(const HttpResponsePtr &)
> &&callback, Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(*)
(T &&customReq, std::function< void(const HttpResponsePtr &)
> &&callback, Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(ClassType::*)
(Arguments...)
 const > (drogon::internal)
FunctionTraits< ReturnType(ClassType::*)
(Arguments...)
 const > (drogon::orm::internal)
FunctionTraits< ReturnType(ClassType::*)
(Arguments...)
> (drogon::internal)
FunctionTraits< ReturnType(ClassType::*)
(Arguments...)
> (drogon::orm::internal)
FunctionTraits< void(*)
()
> (drogon::orm::internal)
FunctionTraits< void(*)
(const DrogonDbException &)
> (drogon::orm::internal)
FunctionTraits< void(*)
(const Result &)
> (drogon::orm::internal)
FunctionTraits< void(*)
(const std::exception_ptr &)
> (drogon::orm::internal)

### G
Gauge (drogon::monitoring)
GlobalFilters (drogon::plugin)
Groups (drogon_model::sqlite3)

### H
handler (api::v1)
has_sqlForDeletingByPrimaryKey (drogon::orm::internal)
has_sqlForFindingByPrimaryKey (drogon::orm::internal)
Hash128 (trantor::utils)
Hash160 (trantor::utils)
Hash256 (trantor::utils)
help (drogon_ctl)
hh (api::v1)
Histogram (drogon::monitoring)
Hodor (drogon::plugin)
HttpAppFramework (drogon)
HttpAppFrameworkImpl (drogon)
HttpBinder (drogon::internal)
HttpBinderBase (drogon::internal)
HttpClient (drogon)
HttpClientImpl (drogon)
HttpConnectionLimit (drogon)
HttpConstraint (drogon::internal)
HttpController (drogon)
HttpControllerBase (drogon)
HttpControllerBinder (drogon)
HttpControllersRouter::HttpControllerRouterItem (drogon)
HttpControllersRouter (drogon)
HttpFile (drogon)
HttpFileImpl (drogon)
HttpFileUploadRequest (drogon)
HttpFilter (drogon)
HttpFilterBase (drogon)
HttpInternalForwardHelper (drogon)
HttpMessageBody (drogon)
HttpMessageStringBody (drogon)
HttpMessageStringViewBody (drogon)
HttpMiddleware (drogon)
HttpMiddlewareBase (drogon)
HttpRequest (drogon)
HttpRequestImpl (drogon)
HttpServer::HttpRequestParamPack (drogon)
HttpRequestParser (drogon)
HttpResponse (drogon)
HttpResponseImpl (drogon)
HttpResponseParser (drogon)
HttpServer (drogon)
HttpSimpleController (drogon)
HttpSimpleControllerBase (drogon)
HttpSimpleControllerBinder (drogon)
HttpViewData (drogon)

### I
TcpServer::IgnoreSigPipe (trantor)
TcpClient::IgnoreSigPipe (trantor)
InDoubtError (drogon::orm)
InetAddress (trantor)
InitBeforeMainFunction (drogon)
InsufficientPrivilege (drogon::orm)
InsufficientResources (drogon::orm)
IntegrityConstraintViolation (drogon::orm)
InternalError (drogon::orm)
IntranetIpFilter (drogon)
InvalidCursorName (drogon::orm)
InvalidCursorState (drogon::orm)
InvalidSqlStatementName (drogon::orm)
IOThreadStorage (drogon)
iovecis_awaitable (drogon)
is_awaitable< T, std::void_t< decltype(internal::getAwaiter(std::declval< T >()
)
)
> > (drogon)
is_printable (drogon::test::internal)
is_printable< _Tp, std::enable_if_t< std::is_same_v< decltype(std::cout<< std::declval< _Tp >()
)
, std::ostream & > > > (drogon::test::internal)
is_resumable (drogon)
is_resumable< AsyncTask, std::void_t< AsyncTask > > (drogon)
is_resumable< T, std::void_t< decltype(internal::getAwaiter(std::declval< T >()
)
)
> > (drogon)
isAutoCreationClass (drogon)
IsPlugin (drogon)

### J
JsonConfigAdapter (drogon)
JsonTestController
K
TcpConnectionImpl::KickoffEntry (trantor)
KQueue (trantor)

### L
Lhs (drogon::test::internal)
AresResolver::LibraryInitializer (trantor)
LifeTimeWatch (drogon)
Hodor::LimitStrategy (drogon::plugin)
ListenerManager::ListenerInfo (drogon)
ListenerManager (drogon)
ListParaCtlLocalHostFilter (drogon)
StaticFileRouter::Location (drogon)
Logger (trantor)
AsyncFileLogger::LoggerFile (trantor)
LogStream (trantor)
LoopAwaiter (drogon::internal)

### M
Mapper (drogon::orm)
CacheMap::MapValue (drogon)
MD5_CTXMemBufferNode (trantor)
Wallets::MetaData (drogon_model::sqlite3)
Users::MetaData (drogon_model::sqlite3)
Tag::MetaData (drogon_model::sqlite3)
Groups::MetaData (drogon_model::sqlite3)
Category::MetaData (drogon_model::sqlite3)
BlogTag::MetaData (drogon_model::sqlite3)
Blog::MetaData (drogon_model::sqlite3)
Wallets::MetaData (drogon_model::postgres)
Users::MetaData (drogon_model::postgres)
BlogTag::MetaData (drogon_model::drogonTestMysql)
Tag::MetaData (drogon_model::postgres)
Blog::MetaData (drogon_model::drogonTestMysql)
Category::MetaData (drogon_model::drogonTestMysql)
Tag::MetaData (drogon_model::drogonTestMysql)
Users::MetaData (drogon_model::drogonTestMysql)
Wallets::MetaData (drogon_model::drogonTestMysql)
Blog::MetaData (drogon_model::postgres)
BlogTag::MetaData (drogon_model::postgres)
Category::MetaData (drogon_model::postgres)
HttpController::methodRegistrator (drogon)
MethodTestMetric (drogon::monitoring)
Middleware1Middleware2Middleware3Middleware4MiddlewareBlockMiddlewareTestMpscQueue (trantor)
MsgBuffer (trantor)
MultipartHeader (drogon)
MultiPartParser (drogon)
MultipartStreamParser (drogon)
MultipartStreamReader (drogon)
Mutex (drogon)
MyClassMysqlConfig (drogon::orm)
MysqlConnection (drogon::orm)
MysqlConnection::MysqlEnv (drogon::orm)
MysqlResultImpl (drogon::orm)
MysqlConnection::MysqlThreadEnv (drogon::orm)

### N
NonCopyable (trantor)
NormalResolver (trantor)
NotConstructibleFromStringNotConvertibleFromStringNotConvertibleFromStringStreamNotFound (drogon)
NotNullViolation (drogon::orm)
NullStreamReader (drogon)

### O
ObjectPool (trantor)
OpenSSLCertificate (trantor)
OpenSSLProviderOStringStream (drogon)
OutOfMemory (drogon::orm)

### P
WebSocketController::pathRegistrator (drogon)
HttpSimpleController::pathRegistrator (drogon)
PgConnection (drogon::orm)
PgListener (drogon::orm)
PipeliningTestPivotTable (drogon_ctl)
Plugin (drogon)
PluginBase (drogon)
PluginsManager (drogon)
poll_groupPoller (trantor)
PollPoller (trantor)
port_statePostgresConfig (drogon::orm)
PostgreSQLResultImpl (drogon::orm)
press (drogon_ctl)
PromExporter (drogon::plugin)
AsyncTask::promise_type (drogon)
Task::promise_type (drogon)
Task< void >::promise_type (drogon)
PubSubService (drogon)

### Q
QueryBuilder (drogon::orm)
AresResolver::QueryData (trantor)
queuequeue_node

### R
RangeError (drogon::orm)
RangeTestControllerRateLimiter (drogon)
RawLogger (trantor)
RealIpControllerRealIpResolver (drogon::plugin)
Redirector (drogon::plugin)
RedisClient (drogon::nosql)
RedisClientImpl (drogon::nosql)
RedisClientLockFree (drogon::nosql)
RedisClientManager (drogon::nosql)
RedisConnection (drogon::nosql)
RedisException (drogon::nosql)
RedisClientManager::RedisInfo (drogon::nosql)
RedisResult (drogon::nosql)
RedisSubscriber (drogon::nosql)
RedisSubscriberImpl (drogon::nosql)
RedisTransaction (drogon::nosql)
RedisTransactionImpl (drogon::nosql)
reflockHttpControllersRouter::RegExWebSocketControllerRouterItem (drogon)
Registry (drogon::monitoring)
Relationship (drogon_ctl)
RequestCallbackParamsRequestStream (drogon)
RequestStreamImpl (drogon)
RequestStreamReader (drogon)
RequestStreamTestCtrlResolver (trantor)
ResponseStream (drogon)
RestfulController (drogon)
RestrictViolation (drogon::orm)
Result (drogon::orm)
ResultImpl (drogon::orm)
resumable_type (drogon::internal)
RngState (trantor::utils)
RouteResult (drogon)
Row (drogon::orm)

### S
SafeRateLimiter (drogon)
SafeStringHash (drogon::utils::internal)
SameContentSample (drogon::monitoring)
SamplesGroup (drogon::monitoring)
Mutex::ScopedCoroMutexAwaiter (drogon)
SecureSSLRedirector (drogon::plugin)
SerializationFailure (drogon::orm)
SerialTaskQueue (trantor)
Session (drogon)
SessionManager::SessionData (trantor)
SessionManager (drogon)
SessionManager (trantor)
SHA1_CTXSHA256_CTXsha3_ctx_tSharedLibManager (drogon)
SimpleControllerProcessResultHttpControllersRouter::SimpleControllerRouterItem (drogon)
SimpleCtrlSimpleSpinLock (drogon)
SlashRemover (drogon::plugin)
SlidingWindowRateLimiter (drogon)
sock_stateSocket (trantor)
SomeStruct (drogon::internal)
Logger::SourceFile (trantor)
SpinLock (drogon)
SqlBinder (drogon::orm::internal)
SqlCmd (drogon::orm)
TransactionImpl::SqlCmd (drogon::orm)
SqlError (drogon::orm)
Sqlite3Config (drogon::orm)
Sqlite3Connection (drogon::orm)
Sqlite3ResultImpl (drogon::orm)
SSLContext (trantor)
StatementCompletionUnknown (drogon::orm)
StaticFileRouter (drogon)
Statistics (drogon_ctl)
StopWatch (drogon)
StreamBufferNode (trantor)
StreamError (drogon)
StructAwaiter (drogon::internal)
SubscribeContext (drogon::nosql)
SubscriberSwitchThreadAwaiter (drogon::internal)
SyntaxError (drogon::orm)

### T
T (trantor)
Tag (drogon_model::drogonTestMysql)
Tag (drogon_model::sqlite3)
Tag (drogon_model::postgres)
Task (drogon)
Task< void > (drogon)
task_awaiter (drogon)
TaskQueue (trantor)
TaskTimeoutFlag (drogon)
TcpClient (trantor)
TcpConnection (trantor)
TcpConnectionImpl (trantor)
TcpServer (trantor)
Test (api::v1)
TestATestB (test)
TestCase (drogon::test)
TestController (example)
TestCookieTestPluginTestViewCtlThreadSafeStream (drogon::test)
Histogram::TimeBucket (drogon::monitoring)
TimeFilterTimeoutError (drogon::orm)
Timer (trantor)
TimerAwaiter (drogon::internal)
TimerPtrComparer (trantor)
TimerQueue (trantor)
TimingWheel (trantor)
TLSPolicy (trantor)
TLSProvider (trantor)
TokenBucketRateLimiter (drogon)
TooManyConnections (drogon::orm)
Topic (drogon)
Traits (drogon::orm::internal)
Traits< T, false > (drogon::orm::internal)
Transaction (drogon::orm)
TransactionImpl (drogon::orm)
TransactionRollback (drogon::orm)
TransformBuilder (drogon::orm)
TrantorPolicytreetree_nodets_treets_tree_node
U
UndefinedColumn (drogon::orm)
UndefinedFunction (drogon::orm)
UndefinedTable (drogon::orm)
UnexpectedRows (drogon::orm)
UniqueViolation (drogon::orm)
UploadFile (drogon)
UsageError (drogon::orm)
UserUsers (drogon_model::drogonTestMysql)
Users (drogon_model::postgres)
Users (drogon_model::sqlite3)

### V
VectorTypeTraits (drogon::orm::internal)
VectorTypeTraits< std::string > (drogon::orm::internal)
VectorTypeTraits< std::vector< std::shared_ptr< T > > > (drogon::orm::internal)
version (drogon_ctl)

### W
Wallets (drogon_model::drogonTestMysql)
Wallets (drogon_model::postgres)
Wallets (drogon_model::sqlite3)
WebSocketClient (drogon)
WebSocketClientImpl (drogon)
WebSocketConnection (drogon)
WebSocketConnectionImpl (drogon)
WebSocketController (drogon)
WebSocketControllerBase (drogon)
WebsocketControllerBinder (drogon)
HttpControllersRouter::WebSocketControllerRouterItem (drogon)
WebSocketMessageParser (drogon)
WebSocketTest (example)
WsCtrlHttpServer::WsRequestParamPack (drogon)

### X
XForwardedForParser
Y
YamlConfigAdapter (drogon)
_
_AFD_POLL_HANDLE_INFO_AFD_POLL_INFO_IO_STATUS_BLOCK_OBJECT_ATTRIBUTES_UNICODE_STRING
