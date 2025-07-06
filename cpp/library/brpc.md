# brpc

https://github.com/edidada/brpc_source_code_analysis

1.10.0 版本变更

新功能
● 支持在创建 socket 时进行连接 (#2574) by @chenBright
● 支持自定义 ServerNode 元数据 (#2603) by @chenBright
● 支持转发 baidu_std 协议请求 (#2629) by @chenBright
● 支持遍历操作 thead local 对象 (#2632) by @chenBright
● 熔断器添加 half open 状态，支持配置恢复条件 (#2634) @jiangyt-git


Bug修复
● 修复 IOBuf 采样率设置不生效问题 (#2601) by @chenBright
● 修复 run_tests.sh 查找 core 文件错误的问题 (#2614) by @chenBright
● 修复 FlatMap 赋值问题 (#2622) by @chenBright
● 修复程序路径获取方式 (#2644) by @ehds
● 修复多 cookie/set-cookie header 处理问题 (#2577) by @chenBright
● 修复 thrift、nshead 协议最大并发问题 (#2613) by @chenBright
● 修复 label 为空时误加逗号问题 (#2659) @renzhong
● 修复 h2 rpc_dump内存泄漏问题 (#2661) by @GreateCode
● 修复 socket 可能重复关闭的问题 (#2663) by @BusyJay
● 修复 Socket 本地 EndPoint 未初始化问题(#2672) by @chenBright
● 修复同一个 Server 无法同时处理 stream_rpc 以及 baidu_std 数据的问题 (#2678) by @howarle
● 修复 multi FlatMap 对重复 key 的处理以及扩容问题(#2669) by @chenBright


功能增强
● 检查 bthread tag 范围并更新相关文档 (#2607) by @yanglimingcn
● 支持根据 bthread tag 设置并发 (#2628) by @yanglimingcn
● 支持 SCOPE_EXIT 宏 (#2643) by @chenBright
● 优化异步日志性能 (#2602) by @chenBright
● 限制 BRPC_VALIDATE_GFLAG 只能在全局作用域或者 namespace 中使用 (#2625) by @chenBright
● 修正整型比较的编译警告 (#2626) by @imdouyu
● 为 MongoServiceAdaptor and SpanFilter 添加虚析构函数以修复编辑器警告 (#2651) by @yozhao
● 抽象 IO 接口，调整 EventDispatcher 支持多种 IO (#2560) by @chenBright
● 开放内部 FastPthreadMutex，并支持 contention profiler (#2589) by @chenBright
● 拒绝不包含 host 的非法HTTP请求 (#2600) by @chenBright
● 支持在写入 rpcz 数据前删除旧数据 (#2610) by @yanglimingcn
● 支持自定义延迟显示单位 (#2655) by @superhail
● 添加 Socket 健康检查日志 (#2673) by @chenBright
● 优化 bthread_local 本地存储表访问性能 (#2645) by @MJY-HUST


其他
● 修复 CI (#2611) by @chenBright
● 更新 Protobuf 依赖版本说明 (#2618) by @chenBright

glog

BRPC（baidu-rpc）的C++版本代码主要使用的是其内部集成的日志系统，而不是外部独立的日志库，如spdlog、glog、Boost.Log、log4cxx或Poco.Log等。BRPC作为百度内部广泛使用的工业级RPC框架，其日志系统被设计为与框架紧密结合，以满足高性能、易用性和灵活性的需求。

BRPC的日志系统支持以下功能：

日志重定向：BRPC的日志默认打印在STDERR，但可以通过设置将其重定向到文件或其他目的地。
自定义日志格式：BRPC允许用户自定义日志格式，以满足不同的日志记录需求。
不同级别打印到不同文件：用户可以通过继承LogSink类并修改其OnLogMessage方法，实现将不同级别的日志信息打印到不同的文件中。
BRPC的日志系统在设计时考虑了分布式系统的特点，支持在分布式环境中高效地记录和管理日志。此外，BRPC还提供了丰富的日志配置选项，允许用户根据实际需求进行灵活配置。

由于BRPC的日志系统是内部集成的，因此在使用BRPC进行开发时，通常不需要额外引入其他日志库。开发者可以直接利用BRPC提供的日志API进行日志记录和管理。

需要注意的是，虽然BRPC没有直接使用外部日志库，但其日志系统的设计和实现思路与许多优秀的C++日志库相似，都注重高性能、易用性和灵活性。因此，开发者在熟悉BRPC日志系统的同时，也可以借鉴其他日志库的设计思想，以提升自己的日志记录和管理能力。

新增支持 lldb 的 bthread 堆栈调试工具，使用方法和命令和 gdb 脚本保持一致。

https://github.com/ysj1173886760/Learning/blob/master/brpc_notes/1.md

bRPC简介
https://brpc.apache.org/zh/docs/overview/

大量机器一般通过命名服务被发现，可基于DNS, ZooKeeper, etcd等实现。在百度内，我们使用BNS (Baidu Naming Service)。brpc也提供“list://“和"file://”。用户可以指定负载均衡算法，让RPC每次选出一台机器发送请求，包括: round-robin, randomized, consistent-hashing(murmurhash3 or md5)和 locality-aware.

## brpc依赖
brpc有如下依赖：

gflags: Extensively used to define global options.
protobuf: Serializations of messages, interfaces of services.
leveldb: Required by rpcz to record RPCs for tracing.

glibc: 2.12-2.25
protobuf: 2.4+
gflags: 2.0-2.2.1
openssl: 0.97-1.1
tcmalloc: 1.7-2.5
glog: 3.3+
valgrind: 3.8+
thrift: 0.9.3-0.11.0

cmake -B build && cmake --build build -j6

git checkout 0.9.7

https://github.com/apache/brpc/blob/master/docs/cn/getting_started.md

brpc交流QQ群，committer在
498837325

0.9.5

2023年 1.4.0
vcpkg install brpc

https://blog.csdn.net/wxj1992/article/details/95249044#comments


[Linux下内存检测工具：asan](http://www.cppblog.com/markqian86/archive/2018/06/14/215728.html)


open-falcon

brpc-open-falcon github

brpc的监控方案
http

你可以使用它：

搭建能在一个端口支持多协议的服务, 或访问各种服务
restful http/https, h2/h2c (与grpc兼容, 即将开源). 使用brpc的http实现比libcurl方便多了。
redis和memcached, 线程安全，比官方client更方便。
rtmp/flv/hls, 可用于搭建直播服务.
hadoop_rpc(可能开源)
支持rdma(即将开源)
各种百度内使用的协议: baidu_std, streaming_rpc, hulu_pbrpc, sofa_pbrpc, nova_pbrpc, public_pbrpc, ubrpc和使用nshead的各种协议.
从其他语言通过HTTP+json访问基于protobuf的协议.
基于工业级的RAFT算法实现搭建高可用分布式系统，已在braft开源。
Server能同步或异步处理请求。
Client支持同步、异步、半同步，或使用组合channels简化复杂的分库或并发访问。
通过http界面调试服务, 使用cpu, heap, contention profilers.
获得更好的延时和吞吐.
把你组织中使用的协议快速地加入brpc，或定制各类组件, 包括名字服务 (dns, zk, etcd), 负载均衡 (rr, random, consistent hashing)

在用redis的时候，发现每隔20s就有一次“刺探”redis：连接redis然后马上释放连接。这有时候会导致超时。
不知道这在框架里哪里可以调整？

目前正在使用 brpc，brpc 在一些地方确实给人了一些小惊喜，比如内置的调试页面等等一些小工具确实都不错，方便了开发。但是作为一个 rpc 框架最重要的应该是能够和已有的系统结合以及良好的扩展性，brpc 在这个方面做的就很差，比如缺少多语言支持，没有 Middleware 之类的功能，内置的 bvar 监控没办法和 Prometheus 结合（ bvar 支持导出 Prometheus 格式的数据但是没有 label 支持，基本不可用），rpc 框架应该是个架子，而不是一个已经装满的架子

[核心组件bvar ](https://blog.csdn.net/wxj1992/article/details/105134641/)

bvar是Brpc使用的多线程环境下的计数器类库，作为一个完善的rpc框架，在实际生产环境中统计诸如qps、连接数等各种数值是必须的，也是服务监控的很重要的一部分，但在多线程环境下，计数器被多线程访问，容易出现cache bouncing影响性能，bvar最核心的思想就是利用thread local变量来减少cache bouncing，本质上是将写的竞争转移到了读，但在诸如监控这种场景下，通常读是远远小于写的，因此这种转移的正向效果是显著的。
bvar的官方文档对于bvar的使用介绍已经很详细，我这边打算接下来用几篇文章从源码层面入手介绍这个优秀的数值统计类库，学习下优秀的设计思想。本篇主要会根据源码先整体分析bvar的组织和实现方式，后续将会深入各个类的实现。

以前一直用 grpc，最近重新看了一下百度的 brpc，对比了一下优缺点。
brpc 优点，支持 status,lb,bvar,sessionlocal，threadlocal,logging,redis,http 等。 感觉这些是一个工程应用必须有的，比如状态监控，负载均衡，日志，常用的传输协议支持。

brpc 缺点，上手难度大，文档写的二流，很多功能要边猜边验证，支持的语言就要是 c++。
grpc 优点，支持的语言非常全，文档写的非常完善。
grpc 缺点，各种传输协议不支持（ http/2，reids ）之类的    //grpc支持http2



戈君 知乎
Brpc

在用redis的时候，发现每隔20s就有一次“刺探”redis：连接redis然后马上释放连接。这有时候会导致超时。
不知道这在框架里哪里可以调整？

目前正在使用brpc，brpc在一些地方确实给人了一些小惊喜，比如内置的调试页面等等一些小工具确实都不错，方便了开发。但是作为一个rpc框架最重要的应该是能够和已有的系统结合以及良好的扩展性，brpc在这个方面做的就很差，比如缺少多语言支持，没有Middleware之类的功能，内置的bvar监控没办法和Prometheus结合（bvar支持导出Prometheus格式的数据但是没有label支持，基本不可用），rpc框架应该是个架子，而不是一个已经装满的架子

[核心组件bvar](https://blog.csdn.net/wxj1992/article/details/105134641/)

bvar是Brpc使用的多线程环境下的计数器类库，作为一个完善的rpc框架，在实际生产环境中统计诸如qps、连接数等各种数值是必须的，也是服务监控的很重要的一部分，但在多线程环境下，计数器被多线程访问，容易出现cache bouncing影响性能，bvar最核心的思想就是利用thread local变量来减少cache bouncing，本质上是将写的竞争转移到了读，但在诸如监控这种场景下，通常读是远远小于写的，因此这种转移的正向效果是显著的。
bvar的官方文档对于bvar的使用介绍已经很详细，我这边打算接下来用几篇文章从源码层面入手介绍这个优秀的数值统计类库，学习下优秀的设计思想。本篇主要会根据源码先整体分析bvar的组织和实现方式，后续将会深入各个类的实现。

以前一直用grpc，最近重新看了一下百度的brpc，对比了一下优缺点。
brpc优点，支持status,lb,bvar,sessionlocal，threadlocal,logging,redis,http等。感觉这些是一个工程应用必须有的，比如状态监控，负载均衡，日志，常用的传输协议支持。
brpc缺点，上手难度大，文档写的二流，很多功能要边猜边验证，支持的语言就要是c++。

grpc优点，支持的语言非常全，文档写的非常完善。
grpc缺点，各种传输协议不支持（http/2，reids）之类的  //grpc支持http2

## brpc版本
1.3？
1.10.0

## brpc编译

## api class
### A
Acceptor (brpc)
NamingServiceThread::Actions (brpc)
AdaptiveConnectionType (brpc)
AdaptiveMaxConcurrency (brpc)
AdaptiveProtocolType (brpc)
LocalityAwareLoadBalancer::Weight::AddInflightResult (brpc::policy)
AMFArray (brpc)
AMFField (brpc)
AMFInputStream (brpc)
AMFObject (brpc)
AMFOutputStream (brpc)
AppConnect (brpc)
AudioSpecificConfig (brpc)
AuthContext (brpc)
Authenticator (brpc)
AutoConcurrencyLimiter (brpc::policy)
AVCDecoderConfigurationRecord (brpc)
AVCNaluIterator (brpc)
AwaitablePromise (brpc::experimental::detail)
AwaitablePromise< void > (brpc::experimental::detail)
AwaitablePromiseBase (brpc::experimental::detail)
### B
badmethod (brpc)
badmethod_Stub (brpc)
BadMethodRequestDefaultTypeInternal (brpc)
BadMethodResponseDefaultTypeInternal (brpc)
BadMethodService (brpc)
BaiduMasterService (brpc)
BaiduMasterServiceBase (brpc)
BaiduMasterServiceBase_Stub (brpc)
BitStream (brpc)
BriefSpanDefaultTypeInternal (brpc)
brpc_metrics (brpc)
brpc_metrics_Stub (brpc)
BthreadInitArgs (brpc)
bthreads (brpc)
bthreads_Stub (brpc)
BthreadsRequestDefaultTypeInternal (brpc)
BthreadsResponseDefaultTypeInternal (brpc)
BthreadsService (brpc)
BugInfo (brpc)
### C
C1 (brpc::policy::adobe_hs)
C1S1Base (brpc::policy::adobe_hs)
C2 (brpc::policy::adobe_hs)
C2S2Base (brpc::policy::adobe_hs)
Controller::Call (brpc)
LoadBalancer::CallInfo (brpc)
CallMapper (brpc)
CertInfo (brpc)
Server::CertMaps (brpc)
Channel (brpc)
ChannelBalancer (brpc::schan)
ChannelBase (brpc)
ChannelOptions (brpc)
ChannelSignature (brpc)
ChannelSSLOptions (brpc)
ChunkInfoDefaultTypeInternal (brpc)
ChunkStatus (brpc::policy)
CircuitBreaker (brpc)
Controller::ClientSettings (brpc)
ClosureGuard (brpc)
ClusterRecoverPolicy (brpc)
CommonStrings (brpc::policy)
CompareByStartRealTime (brpc)
CompareItemInPathList (brpc)
Controller::CompletionInfo (brpc)
CompressHandler (brpc)
ConcurrencyLimiter (brpc)
ConcurrencyRemover (brpc)
connections (brpc)
connections_Stub (brpc)
ConnectionsRequestDefaultTypeInternal (brpc)
ConnectionsResponseDefaultTypeInternal (brpc)
ConnectionsService (brpc)
Stream::ConnectMeta (brpc)
ConnectStatistics (brpc)
ConsistentHashingLoadBalancer (brpc::policy)
ConstantConcurrencyLimiter (brpc::policy)
ConsulNamingService (brpc::policy)
Controller (brpc)
ControllerPrivateAccessor (brpc)
CouchbaseAuthenticator (brpc::policy)
### D
DataFactory (brpc)
DebugPrinter (brpc)
DefaultClusterRecoverPolicy (brpc)
DefaultReplicaPolicy (brpc::policy)
DeleteNsheadClosure (brpc)
Describable (brpc)
DescribeOptions (brpc)
Destroyable (brpc)
Destroyer (brpc::detail)
DestroyingPtr (brpc)
DHWrapper (brpc::policy)
DigestBlock (brpc::policy::adobe_hs)
dir (brpc)
dir_Stub (brpc)
DirRequestDefaultTypeInternal (brpc)
DirResponseDefaultTypeInternal (brpc)
DirService (brpc)
DiscoveryClient (brpc::policy)
DiscoveryNamingService (brpc::policy)
DiscoveryRegisterParam (brpc::policy)
DomainListNamingService (brpc::policy)
DomainNamingService (brpc::policy)
DoNothingClosure (brpc)
DynamicPartitionChannel (brpc)
DynPartLoadBalancer (brpc::policy)
### E
CircuitBreaker::EmaErrorRecorder (brpc)
Socket::EpollOutRequest (brpc)
EqualChannelPtr (brpc)
EspAddress (brpc)
EspAuthenticator (brpc::policy)
EspHead (brpc)
EspMessage (brpc)
EspMessageBaseDefaultTypeInternal (brpc)
EventDispatcher (brpc)
ExcludedServers (brpc)
ExtendedSocketStat (brpc)
Extension (brpc)
### F
FailAllRead (brpc)
FeedbackDefaultTypeInternal (brpc)
FileNamingService (brpc::policy)
flags (brpc)
flags_Stub (brpc)
FlagsRequestDefaultTypeInternal (brpc)
FlagsResponseDefaultTypeInternal (brpc)
FlagsService (brpc)
FlushHeaderWithExtras (brpc)
FlvReader (brpc)
FlvWriter (brpc)
FlvWriterOptions (brpc)
Span::Forbidden (brpc)
VersionedRefWithId::Forbidden (brpc)
FreeBIO (brpc)
FreeEVPKEY (brpc)
MallocExtension::FreeListInfoFreeSSL (brpc)
FreeSSLCTX (brpc)
FreeX509 (brpc)
FunctionClosure0 (brpc::internal)
FunctionClosure1 (brpc::internal)
FunctionClosure10 (brpc::internal)
FunctionClosure2 (brpc::internal)
FunctionClosure3 (brpc::internal)
FunctionClosure4 (brpc::internal)
FunctionClosure5 (brpc::internal)
FunctionClosure6 (brpc::internal)
FunctionClosure7 (brpc::internal)
FunctionClosure8 (brpc::internal)
FunctionClosure9 (brpc::internal)
### G
GetFaviconRequestDefaultTypeInternal (brpc)
GetFaviconResponseDefaultTypeInternal (brpc)
GetFaviconService (brpc)
GetJsRequestDefaultTypeInternal (brpc)
GetJsResponseDefaultTypeInternal (brpc)
GetJsService (brpc)
GetLeakySingleton (butil)
GetNamingServiceThreadOptions (brpc)
GlobalExtensions (brpc)
GlobalSocketCreator (brpc)
GrpcHealthCheckService (brpc)
### H
H2Bvars (brpc::policy)
H2Context (brpc::policy)
H2FrameHead (brpc::policy)
H2GlobalStreamCreator (brpc::policy)
H2ParseResult (brpc::policy)
H2Settings (brpc)
H2StreamContext (brpc::policy)
H2UnsentRequest (brpc::policy)
H2UnsentResponse (brpc::policy)
HPacker::Header (brpc)
HeaderAndHashCode (brpc)
HeaderCstr (brpc)
HeaderEqualTo (brpc)
HeaderHasher (brpc)
Health (grpc::health::v1)
health (brpc)
health_Stub (brpc)
Health_Stub (grpc::health::v1)
HealthCheckChannel (brpc)
HealthCheckManager (brpc)
HealthCheckRequestDefaultTypeInternal (grpc::health::v1)
HealthCheckResponseDefaultTypeInternal (grpc::health::v1)
HealthCheckTask (brpc)
HealthReporter (brpc)
HealthRequestDefaultTypeInternal (brpc)
HealthResponseDefaultTypeInternal (brpc)
HealthService (brpc)
Hex (brpc)
hotspots (brpc)
hotspots_Stub (brpc)
HotspotsRequestDefaultTypeInternal (brpc)
HotspotsResponseDefaultTypeInternal (brpc)
HotspotsService (brpc)
HPacker (brpc)
HPackOptions (brpc)
http_parser (brpc)
http_parser_settings (brpc)
http_parser_url (brpc)
HttpContext (brpc::policy)
HttpHeader (brpc)
HttpMessage (brpc)
HttpMethodPair (brpc)
HttpResponseSender (brpc::policy)
HttpResponseSenderAsDone (brpc::policy)
HuffmanCode (brpc)
HuffmanDecoder (brpc)
HuffmanEncoder (brpc)
HuffmanNode (brpc)
HuffmanTree (brpc)
HuluController (brpc::policy)
HuluRawPacker (brpc::policy)
HuluRawUnpacker (brpc::policy)
HuluRpcRequestMetaDefaultTypeInternal (brpc::policy)
HuluRpcResponseMetaDefaultTypeInternal (brpc::policy)
### I
ico (brpc)
ico_Stub (brpc)
IdGen (brpc)
IdlNames (brpc)
ids (brpc)
ids_Stub (brpc)
IdsRequestDefaultTypeInternal (brpc)
IdsResponseDefaultTypeInternal (brpc)
IdsService (brpc)
IgnoreAllRead (brpc)
IncrHeaderWithExtras (brpc)
IndentingOStream (brpc)
index (brpc)
index_Stub (brpc)
IndexRequestDefaultTypeInternal (brpc)
IndexResponseDefaultTypeInternal (brpc)
IndexService (brpc)
IndexTable (brpc)
IndexTableOptions (brpc)
Controller::Inheritable (brpc)
InputMessageBase (brpc)
InputMessenger::InputMessageClosure (brpc)
InputMessageHandler (brpc)
InputMessenger (brpc)
InputResponse (brpc::policy)
Interceptor (brpc)
IOEvent (brpc)
IOEventData (brpc)
IOEventDataOptions (brpc)
is_proto_enum< ::brpc::CompressType >is_proto_enum< ::brpc::ConnectionType >is_proto_enum< ::brpc::Errno >is_proto_enum< ::brpc::FrameType >is_proto_enum< ::brpc::policy::MongoOp >is_proto_enum< ::brpc::policy::SofaCompressType >is_proto_enum< ::brpc::policy::SofaRpcMeta_Type >is_proto_enum< ::brpc::ProtocolType >is_proto_enum< ::brpc::SpanType >is_proto_enum< ::brpc::TalkType >is_proto_enum< ::brpc::TrackMeSeverity >is_proto_enum< ::grpc::health::v1::HealthCheckResponse_ServingStatus >SparseMinuteCounter::Item (brpc)

### J
js (brpc)
js_Stub (brpc)

### K
KetamaReplicaPolicy (brpc::policy)
KeyBlock (brpc::policy::adobe_hs)
KVMap (brpc)

### L
LessThanByName (brpc)
LibInfo (brpc)
list (brpc)
list_Stub (brpc)
ListNamingService (brpc::policy)
ListRequestDefaultTypeInternal (brpc)
ListResponseDefaultTypeInternal (brpc)
ListService (brpc)LoadBalancer (brpc)
LoadBalancerWithNaming (brpc)
LocalityAwareLoadBalancer (brpc::policy)
LogErrorTextAndDelete (brpc)
Controller::LogPrefixDummy (brpc)
### M
MallocExtensionMemcacheRequest (brpc)
MemcacheRequestBaseDefaultTypeInternal (brpc)
MemcacheRequestHeader (brpc::policy)
MemcacheResponse (brpc)
MemcacheResponseBaseDefaultTypeInternal (brpc)
MemcacheResponseHeader (brpc::policy)
memory (brpc)
memory_Stub (brpc)
MemoryRequestDefaultTypeInternal (brpc)
MemoryResponseDefaultTypeInternal (brpc)
MemoryService (brpc)
MessageBatcher (brpc)
RtmpContext::MessageStreamInfo (brpc::policy)
MethodClosure0 (brpc::internal)
MethodClosure1 (brpc::internal)
MethodClosure10 (brpc::internal)
MethodClosure2 (brpc::internal)
MethodClosure3 (brpc::internal)
MethodClosure4 (brpc::internal)
MethodClosure5 (brpc::internal)
MethodClosure6 (brpc::internal)
MethodClosure7 (brpc::internal)
MethodClosure8 (brpc::internal)
MethodClosure9 (brpc::internal)
Server::MethodProperty (brpc)
MethodStatus (brpc)
MetricsRequestDefaultTypeInternal (brpc)
MetricsResponseDefaultTypeInternal (brpc)
MinWidth (brpc)mongo_head_t (brpc)
MongoContext (brpc)MongoContextMessage (brpc)
MongoHeaderDefaultTypeInternal (brpc::policy)
MongoRequestDefaultTypeInternal (brpc::policy)
MongoResponseDefaultTypeInternal (brpc::policy)
MongoService (brpc::policy)
MongoService_Stub (brpc::policy)
MongoServiceAdaptor (brpc)
MostCommonMessage (brpc::policy)
### N
NacosNamingService (brpc::policy)
NameOfPoint (brpc)NamingService (brpc)
NamingServiceActions (brpc)NamingServiceFilter (brpc)
NamingServiceThread (brpc)NamingServiceWatcher (brpc)
ConsistentHashingLoadBalancer::Node (brpc::policy)
NonConstDescribable (brpc)NovaServiceAdaptor (brpc::policy)
nshead_t (brpc)NsheadClosure (brpc)NsheadMcpackAdaptor (brpc::policy)
NsheadMessage (brpc)
NsheadMessageBaseDefaultTypeInternal (brpc)
NsheadMetaDefaultTypeInternal (brpc)
NsheadPbServiceAdaptor (brpc)
NsheadService (brpc)
NsheadServiceOptions (brpc)
NSKey (brpc)NSKeyHasher (brpc)
### O
ObjectPtrOnAppHealthCheckDone (brpc)
OnClientStreamCreated (brpc)
OnPlayContinuation (brpc::policy)
OnPublishContinuation (brpc::policy)
OnServerStreamCreated (brpc::policy)
Server::MethodProperty::OpaqueParams (brpc)

### P
PackedPtr (brpc)
ParallelChannel (brpc)
ParallelChannelDone (brpc)
ParallelChannelOptions (brpc)
ParseResult (brpc)
Partition (brpc)
PartitionChannel (brpc)
PartitionChannelBase (brpc)
PartitionChannelOptions (brpc)
DynamicPartitionChannel::Partitioner (brpc)
PartitionParser (brpc)
Path (brpc)
PeriodicNamingService (brpc)
PeriodicTask (brpc)
PeriodicTaskManager (brpc)
PipelinedInfo (brpc)
PortRange (brpc)
pprof (brpc)
pprof_Stub (brpc)
PProfService (brpc)
PrefixLess (brpc)
PrintedAsDateTime (brpc)
ProfileRequestDefaultTypeInternal (brpc)
ProfileResponseDefaultTypeInternal (brpc)
ProfilerLinker (brpc)
ProfilingClient (brpc)
ProfilingEnvironment (brpc)
ProfilingResult (brpc)
ProfilingWaiter (brpc)
ProgressiveAttachment (brpc)
ProgressiveReader (brpc)
PrometheusMetricsDumper (brpc)
PrometheusMetricsService (brpc)
PROTOBUF_FINAL (grpc::health::v1)
PROTOBUF_FINAL (brpc)
PROTOBUF_FINAL (brpc::policy)
protobufs (brpc)
protobufs_Stub (brpc)
ProtobufsRequestDefaultTypeInternal (brpc)
ProtobufsResponseDefaultTypeInternal (brpc)
ProtobufsService (brpc)
Protocol (brpc)
ProtocolEntry (brpc)
ProtocolMap (brpc)
PublicPbrpcRequestDefaultTypeInternal (brpc::policy)
PublicPbrpcResponseDefaultTypeInternal (brpc::policy)
PublicPbrpcServiceAdaptor (brpc::policy)

### Q
QueryRemover (brpc)
QuerySplitter (brpc)

### R
RandomizedLoadBalancer (brpc::policy)
RdmaEndpointReadableProgressiveAttachment (brpc)
RtmpChunkStream::ReadParams (brpc::policy)
RedisAuthenticator (brpc::policy)
RedisCommandHandler (brpc)
RedisCommandParser (brpc)
RedisConnContext (brpc::policy)
RedisReply (brpc)
RedisRequest (brpc)
RedisRequestBaseDefaultTypeInternal (brpc)
RedisResponse (brpc)
RedisResponseBaseDefaultTypeInternal (brpc)
RedisService (brpc)
RedisStringPrinter (brpc)
RemoteFileNamingService (brpc::policy)
RemoveRefOnQuit (brpc::policy)
ReplicaPolicy (brpc::policy)
RequestBodyDefaultTypeInternal (brpc::policy)
RequestHeadDefaultTypeInternal (brpc::policy)
Resource (brpc::schan)
ResponseBodyDefaultTypeInternal (brpc::policy)
ResponseHeadDefaultTypeInternal (brpc::policy)
ResponseMerger (brpc)
RestfulMap (brpc)
RestfulMapping (brpc)
RestfulMethodPath (brpc)
RestfulMethodProperty (brpc)
RetryingClientMessageHandler (brpc)
RetryPolicy (brpc)
RevertServerStatus (brpc)
RoundRobinLoadBalancer (brpc::policy)
RpcDumpContext (brpc)
RpcDumpMetaDefaultTypeInternal (brpc)
RpcMeta_UserFieldsEntry_DoNotUse (brpc::policy)
RpcMeta_UserFieldsEntry_DoNotUseDefaultTypeInternal (brpc::policy)
RpcMetaDefaultTypeInternal (brpc::policy)
RpcRequestMetaDefaultTypeInternal (brpc::policy)
RpcResponseMetaDefaultTypeInternal (brpc::policy)
RpcRetryPolicy (brpc)
RpcRetryPolicyWithFixedBackoff (brpc)
RpcRetryPolicyWithJitteredBackoff (brpc)
RPCSender (brpc)
rpcz (brpc)
rpcz_Stub (brpc)
RpczRequestDefaultTypeInternal (brpc)
RpczResponseDefaultTypeInternal (brpc)
RpczService (brpc)
RpczSpanDefaultTypeInternal (brpc)
RpczSpanFilter (brpc)
RtmpAACMessage (brpc)
RtmpAudioMessage (brpc)
RtmpAVCMessage (brpc)
RtmpBasicHeader (brpc::policy)
RtmpBvars (brpc)
RtmpChunkStream (brpc::policy)
RtmpClient (brpc)
RtmpClientImpl (brpc)
RtmpClientOptions (brpc)
RtmpClientStream (brpc)
RtmpClientStreamOptions (brpc)
RtmpConnect (brpc)
RtmpConnectRequestDefaultTypeInternal (brpc)
RtmpConnectResponseDefaultTypeInternal (brpc)
RtmpContext (brpc::policy)
RtmpCreateStreamMessage (brpc::policy)
RtmpCuePoint (brpc)
RtmpEmptyObjectDefaultTypeInternal (brpc)
RtmpHashCode (brpc)
RtmpInfoDefaultTypeInternal (brpc)
RtmpMessageHandler (brpc)
RtmpMessageHeader (brpc::policy)
RtmpMetaData (brpc)
RtmpPlay2OptionsDefaultTypeInternal (brpc)
RtmpPlayOptions (brpc)
RtmpRetryingClientStream (brpc)
RtmpRetryingClientStreamOptions (brpc)
RtmpServerStream (brpc)
RtmpService (brpc)
RtmpSharedObjectMessage (brpc)
RtmpSocketCreator (brpc)
RtmpStreamBase (brpc)
RtmpTransactionHandler (brpc::policy)
RtmpUnsentMessage (brpc::policy)
RtmpVideoMessage (brpc)
RunLastMessage (brpc)
RunOnCancelThread (brpc)
### S
S1 (brpc::policy::adobe_hs)
S2 (brpc::policy::adobe_hs)
ExtendedSocketStat::Sampled (brpc)
SampledRequest (brpc)
SampleIterator (brpc)
AutoConcurrencyLimiter::SampleWindow (brpc::policy)
TimeoutConcurrencyLimiter::SampleWindow (brpc::policy)
ScopedNonServiceError (brpc)
LoadBalancer::SelectIn (brpc)
SelectiveChannel (brpc)
LoadBalancer::SelectOut (brpc)
ChannelBalancer::SelectOut (brpc::schan)
Sender (brpc::schan)
SendMongoResponse (brpc::policy)
SendNsheadPbResponse (brpc)
SerializedRequest (brpc)
SerializedRequestBaseDefaultTypeInternal (brpc)
SerializedResponse (brpc)
SerializedResponseBaseDefaultTypeInternal (brpc)
WeightedRandomizedLoadBalancer::Server (brpc::policy)
WeightedRoundRobinLoadBalancer::Server (brpc::policy)
Server (brpc)
ServerId (brpc)
ServerId2SocketIdMapper (brpc)
LocalityAwareLoadBalancer::ServerInfo (brpc::policy)
ServerNode (brpc)
NamingServiceThread::ServerNodeWithId (brpc)
ServerOptions (brpc)
ServerPrivateAccessor (brpc)
LocalityAwareLoadBalancer::Servers (brpc::policy)
RandomizedLoadBalancer::Servers (brpc::policy)
RoundRobinLoadBalancer::Servers (brpc::policy)
WeightedRandomizedLoadBalancer::Servers (brpc::policy)
WeightedRoundRobinLoadBalancer::Servers (brpc::policy)
DynPartLoadBalancer::Servers (brpc::policy)
ServerSSLOptions (brpc)
ServerStatistics (brpc)
ServiceOptions (brpc)
Server::ServiceProperty (brpc)
SessionKVFlusher (brpc)
SharedLoadBalancer (brpc)
SharedObject (brpc)
Socket::SharedPart (brpc)
SimpleDataPool (brpc)
SocketMap::SingleConnection (brpc)
Socket (brpc)
SocketConnection (brpc)
SocketCreator (brpc)
SocketKeepaliveOptions (brpc)
SocketMap (brpc)
SocketMapKey (brpc)
SocketMapKeyHasher (brpc)
SocketMapOptions (brpc)
SocketMessage (brpc)
SocketMessageDeleter (brpc::details)
SocketMessagePtr (brpc)
SocketMessagePtr< void > (brpc)
SocketOptions (brpc)
SocketPool (brpc)
sockets (brpc)
sockets_Stub (brpc)
SocketsRequestDefaultTypeInternal (brpc)
SocketsResponseDefaultTypeInternal (brpc)
SocketsService (brpc)
SocketSSLContext (brpc)
SocketStat (brpc)
SocketUser (brpc)
SocketVarsCollector (brpc)
SofaRawPacker (brpc::policy)
SofaRawUnpacker (brpc::policy)
SofaRpcMetaDefaultTypeInternal (brpc::policy)
SortByChannelPtr (brpc)
Span (brpc)
SpanAnnotationDefaultTypeInternal (brpc)
SpanDB (brpc)
SpanEarlier (brpc)
SpanFilter (brpc)
SpanInfoExtractor (brpc)
SpanPreprocessor (brpc)
SparseMinuteCounter (brpc)
Server::SSLContext (brpc)
SSLError (brpc)
SimpleDataPool::Stat (brpc)
status (brpc)
status_pair (brpc)
status_Stub (brpc)
StatusRequestDefaultTypeInternal (brpc)
StatusResponseDefaultTypeInternal (brpc)
StatusService (brpc)
StoreHeaderWithExtras (brpc)
Stream (brpc)
StreamCreator (brpc)
StreamFrameMetaDefaultTypeInternal (brpc)
StreamIdTraits (brpc::detail)
StreamInputHandler (brpc)
StreamOptions (brpc)
StreamSettingsDefaultTypeInternal (brpc)
StreamUserData (brpc)
StreamWriteOptions (brpc)
SubCall (brpc)
ParallelChannel::SubChan (brpc)
PartitionChannelBase::SubChannel (brpc)
SubChannel (brpc::schan)
RtmpContext::SubChunkArray (brpc::policy)
ParallelChannelDone::SubDone (brpc)
SubDone (brpc::schan)
DynamicPartitionChannel::Partitioner::SubPartitionChannel (brpc)
SubStreamCreator (brpc)
PrometheusMetricsDumper::SummaryItems (brpc)

### T
Tabbed (brpc)
TabInfo (brpc)
TabInfoList (brpc)
TableStruct_brpc_2fbuiltin_5fservice_2eprotoTableStruct_brpc_2ferrno_2eprotoTableStruct_brpc_2fget_5ffavicon_2eprotoTableStruct_brpc_2fget_5fjs_2eprotoTableStruct_brpc_2fgrpc_5fhealth_5fcheck_2eprotoTableStruct_brpc_2fnshead_5fmeta_2eprotoTableStruct_brpc_2foptions_2eprotoTableStruct_brpc_2fpolicy_2fbaidu_5frpc_5fmeta_2eprotoTableStruct_brpc_2fpolicy_2fhulu_5fpbrpc_5fmeta_2eprotoTableStruct_brpc_2fpolicy_2fmongo_2eprotoTableStruct_brpc_2fpolicy_2fpublic_5fpbrpc_5fmeta_2eprotoTableStruct_brpc_2fpolicy_2fsofa_5fpbrpc_5fmeta_2eprotoTableStruct_brpc_2fproto_5fbase_2eprotoTableStruct_brpc_2frpc_5fdump_2eprotoTableStruct_brpc_2frtmp_2eprotoTableStruct_brpc_2fspan_2eprotoTableStruct_brpc_2fstreaming_5frpc_5fmeta_2eprotoTableStruct_brpc_2ftrackme_2eprotoTemporaryArrayBuilder (brpc)Server::ThreadLocalOptions (brpc)
threads (brpc)
threads_Stub (brpc)
ThreadsRequestDefaultTypeInternal (brpc)
ThreadsResponseDefaultTypeInternal (brpc)
ThreadsService (brpc)
thrift_head_t (brpc::policy)
ThriftClosure (brpc::policy)
ThriftDoneWrapper (brpc::details)
ThriftFramedMessage (brpc)
ThriftFramedMessageBaseDefaultTypeInternal (brpc)
ThriftMessageBase (brpc)
ThriftMessageHolder (brpc::details)
ThriftMessageWrapper (brpc::details)
ThriftService (brpc)
ThriftStub (brpc)
LocalityAwareLoadBalancer::TimeInfo (brpc::policy)
TimeoutConcurrencyConf (brpc)
TimeoutConcurrencyLimiter (brpc::policy)
RoundRobinLoadBalancer::TLS (brpc::policy)
WeightedRoundRobinLoadBalancer::TLS (brpc::policy)
TouchHeaderWithExtras (brpc)
TracingSpanDefaultTypeInternal (brpc)
TrackMeRequestDefaultTypeInternal (brpc)
TrackMeResponseDefaultTypeInternal (brpc)
TrackMeService (brpc)
TrackMeService_Stub (brpc)
TsAdaptationField (brpc)
TsChannel (brpc)
TsChannelGroup (brpc)
TsWriter::TsMessage (brpc)
TsPacket (brpc)
TsPayload (brpc)
TsPayloadPAT (brpc)
TsPayloadPATProgram (brpc)
TsPayloadPES (brpc)
TsPayloadPMT (brpc)
TsPayloadPMTESInfo (brpc)
TsPayloadPSI (brpc)
TsWriter (brpc)
### U
UbrpcAdaptor (brpc::policy)
UbrpcCompackAdaptor (brpc::policy)
UbrpcMcpack2Adaptor (brpc::policy)
URI (brpc)
UserCode (brpc)
UserCodeBackupPool (brpc)

### V
vars (brpc)
vars_Stub (brpc)
VarsRequestDefaultTypeInternal (brpc)
VarsResponseDefaultTypeInternal (brpc)
VarsService (brpc)
VerifyOptions (brpc)
version (brpc)
version_Stub (brpc)
VersionedRefWithId (brpc)
VersionedRefWithIdDeleter (brpc)
VersionedRefWithIdDeleter< Socket > (brpc)
VersionRequestDefaultTypeInternal (brpc)
VersionResponseDefaultTypeInternal (brpc)
VersionService (brpc)
vlog (brpc)
vlog_Stub (brpc)
VLogPrinter (brpc)
VLogRequestDefaultTypeInternal (brpc)
VLogResponseDefaultTypeInternal (brpc)
VLogService (brpc)

### W
LocalityAwareLoadBalancer::Weight (brpc::policy)
WeightedRandomizedLoadBalancer (brpc::policy)
WeightedRoundRobinLoadBalancer (brpc::policy)
Stream::WritableMeta (brpc)
Socket::WriteOptions (brpc)
RtmpChunkStream::WriteParams (brpc::policy)
_
_Internal (brpc::RedisRequestBase)
_Internal (brpc::SerializedRequestBase)
_Internal (brpc::RtmpPlay2Options)
_Internal (brpc::RtmpInfo)
_Internal (brpc::RtmpEmptyObject)
_Internal (brpc::RtmpConnectResponse)
_Internal (brpc::RtmpConnectRequest)
_Internal (brpc::RpczSpan)
_Internal (brpc::RpczResponse)
_Internal (brpc::RpczRequest)
_Internal (brpc::RpcDumpMeta)
_Internal (brpc::RedisResponseBase)
_Internal (brpc::SerializedResponseBase)
_Internal (brpc::ProtobufsResponse)
_Internal (brpc::ProtobufsRequest)
_Internal (brpc::ProfileResponse)
_Internal (brpc::ProfileRequest)
_Internal (brpc::policy::SofaRpcMeta)
_Internal (brpc::policy::RpcResponseMeta)
_Internal (brpc::policy::RpcRequestMeta)
_Internal (brpc::policy::RpcMeta)
_Internal (brpc::policy::ResponseHead)
_Internal (brpc::policy::ResponseBody)
_Internal (brpc::TracingSpan)
_Internal (grpc::health::v1::HealthCheckResponse)
_Internal (grpc::health::v1::HealthCheckRequest)
_Internal (brpc::VLogResponse)
_Internal (brpc::VLogRequest)
_Internal (brpc::VersionResponse)
_Internal (brpc::VersionRequest)
_Internal (brpc::VarsResponse)
_Internal (brpc::VarsRequest)
_Internal (brpc::TrackMeResponse)
_Internal (brpc::TrackMeRequest)
_Internal (brpc::policy::RequestHead)
_Internal (brpc::ThriftFramedMessageBase)
_Internal (brpc::ThreadsResponse)
_Internal (brpc::ThreadsRequest)
_Internal (brpc::StreamSettings)
_Internal (brpc::StreamFrameMeta)
_Internal (brpc::StatusResponse)
_Internal (brpc::StatusRequest)
_Internal (brpc::SpanAnnotation)
_Internal (brpc::SocketsResponse)
_Internal (brpc::SocketsRequest)
_Internal (brpc::Feedback)
_Internal (brpc::HotspotsResponse)
_Internal (brpc::HotspotsRequest)
_Internal (brpc::HealthResponse)
_Internal (brpc::HealthRequest)
_Internal (brpc::GetJsResponse)
_Internal (brpc::GetJsRequest)
_Internal (brpc::GetFaviconResponse)
_Internal (brpc::GetFaviconRequest)
_Internal (brpc::FlagsResponse)
_Internal (brpc::FlagsRequest)
_Internal (brpc::IdsRequest)
_Internal (brpc::EspMessageBase)
_Internal (brpc::DirResponse)
_Internal (brpc::DirRequest)
_Internal (brpc::ConnectionsResponse)
_Internal (brpc::ConnectionsRequest)
_Internal (brpc::ChunkInfo)
_Internal (brpc::BthreadsResponse)
_Internal (brpc::BthreadsRequest)
_Internal (brpc::BriefSpan)
_Internal (brpc::BadMethodResponse)
_Internal (brpc::MetricsResponse)
_Internal (brpc::policy::RequestBody)
_Internal (brpc::policy::PublicPbrpcResponse)
_Internal (brpc::policy::PublicPbrpcRequest)
_Internal (brpc::policy::MongoResponse)
_Internal (brpc::policy::MongoRequest)
_Internal (brpc::policy::MongoHeader)
_Internal (brpc::policy::HuluRpcResponseMeta)
_Internal (brpc::policy::HuluRpcRequestMeta)
_Internal (brpc::NsheadMeta)
_Internal (brpc::NsheadMessageBase)
_Internal (brpc::BadMethodRequest)
_Internal (brpc::MetricsRequest)
_Internal (brpc::MemoryResponse)
_Internal (brpc::MemoryRequest)
_Internal (brpc::MemcacheResponseBase)
_Internal (brpc::MemcacheRequestBase)
_Internal (brpc::ListResponse)
_Internal (brpc::ListRequest)
_Internal (brpc::IndexResponse)
_Internal (brpc::IndexRequest)
_Internal (brpc::IdsResponse)