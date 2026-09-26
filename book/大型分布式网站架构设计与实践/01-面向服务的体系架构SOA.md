# 第 1 章　面向服务的体系架构（SOA）

> 原书第 1 章是**全书的技术地基**：HTTP/TCP 两种 RPC、序列化、服务路由与负载均衡、ZooKeeper
> 做注册中心、HTTP 服务网关。它回答的是「一个网站的多个模块怎么互相调用、怎么找到对方、怎么分流」。
> 但它也是**最需要 2026 年补丁**的一章：2014 年还在「手工 SOA」，今天已被
> gRPC/Protobuf、Nacos、Spring Cloud、Service Mesh（Istio/Envoy）整体改写。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 基于 TCP 协议的 RPC | RPC 名词解释、对象序列化、基于 TCP 自研 RPC | TCP RPC 高效但「重」：要自己管连接、协议、序列化 |
| 1.2 基于 HTTP 协议的 RPC | HTTP 协议栈、请求/响应、HttpClient、JSON/XML、RESTful 与 RPC、基于 HTTP 的 RPC 实现 | HTTP RPC 通用、穿透性强、调试友好，是跨语言互通的默认选择 |
| 1.3 服务的路由和负载均衡 | 服务化演变、负载均衡算法、动态配置、ZooKeeper 注册、zkClient、路由与负载均衡实现 | **服务发现 + 负载均衡 = 分布式调用的命门**，ZooKeeper 是当时的标准解 |
| 1.4 HTTP 服务网关 | 网关聚合/路由/协议转换 | 网关是「系统的统一入口」，把横切关注点（鉴权/限流/路由）收口 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 1.1 基于 TCP 的 RPC：把「方法调用」搬到网络上

RPC（Remote Procedure Call）的本质：**让调用远程方法像调用本地方法一样**。难点在于——
本地调用是「压栈 + 跳指令」，远程调用要把「方法名 + 参数」变成字节流，发到对面，
再把「返回值」变回来。

```text
# 教学示意，不参与构建：一次 TCP RPC 的最小闭环
Client                                   Server
  |---- 建立 TCP 连接（长连接/连接池）------>|
  |---- 序列化: invoke(method, args) ------->|  反序列化得到 method/args
  |                                        |  本地执行 method(args)
  |<--- 序列化: return(value/exception) ----|  序列化结果
  |  反序列化得到返回值                       |
```

- **对象的序列化**（1.1.2）：把内存里的对象变成可传输的字节序列。常见方案：Java 原生
  `ObjectOutputStream`、Hessian、Kryo、Protobuf（2026 视角见下）。序列化要兼顾
  **体积小、速度快、跨语言**。
- **基于 TCP 实现 RPC**（1.1.3）：核心是「自己定义应用层协议帧」——通常
  `长度(4B) + 序列化后的 payload`，解决 TCP 粘包/半包问题。

```text
# 教学示意，不参与构建：一个简单的帧格式
frame = [magic:2B][version:1B][bodyLen:4B][body:N]
读时先读 7 字节头，按 bodyLen 读满 body，再反序列化
```

### 1.2 基于 HTTP 的 RPC：用现成协议省掉「自己造轮子」

- **HTTP 协议栈**（1.2.1）：应用层 HTTP → 传输层 TCP → 网络层 IP → 链路/物理层。
  本书强调理解「HTTP 建立在 TCP 之上」这件事——HTTP 的每一次请求-响应，底层还是 TCP 连接
  （HTTP/1.1 默认 keep-alive 复用连接）。
- **HttpClient 发送请求**（1.2.3）：Java 侧用 `HttpClient`（书里是 Apache Commons HttpClient /
  `HttpURLConnection`）发 GET/POST。
- **JSON 和 XML**（1.2.5）：HTTP RPC 的 payload 常用 JSON（轻量、人读）或 XML（严谨、schema）。
- **RESTful 和 RPC**（1.2.6）：一个容易混的点——

| 维度 | RPC 风格 | RESTful 风格 |
| --- | --- | --- |
| 关注点 | 「调用哪个方法」 | 「操作哪个资源」 |
| URL 语义 | 动词为主（/userService/get） | 名词为主（GET /users/123） |
| 耦合 | 与接口定义强耦合 | 与资源模型耦合，较松 |

- **基于 HTTP 的 RPC 实现**（1.2.7）：本质是用 HTTP 当传输层，payload 里塞方法名+参数
  （类似 XML-RPC / JSON-RPC 的思路），享受 HTTP 的生态（网关、缓存、代理、调试）。

### 1.3 服务的路由和负载均衡：分布式调用的命门

- **服务化的演变**（1.3.1）：单体 → 垂直拆分 → 分布式服务化。拆开后，调用方不再知道
  「服务实例在哪台机器、有几个、挂了没」，于是需要**注册中心 + 负载均衡**。
- **负载均衡算法**（1.3.2）：轮询、加权轮询、随机、加权随机、一致性哈希、最小连接数等。
  一致性哈希在这里的价值是：**某实例下线时，只迁移它负责的 key 区间，而非全量重分布**。
- **动态配置规则**（1.3.3）：路由规则（如「把 /order/* 打到 v2 集群」）要可动态下发，
  不能写死在代码里。
- **ZooKeeper**（1.3.4–1.3.6）：用 ZK 的**临时节点**做服务注册（实例上线建节点、下线节点消失），
  用**监听（watch）**做服务发现（实例列表变化即时通知调用方）。zkClient 是对原生 ZK API 的封装。

```text
# 教学示意，不参与构建：ZK 做注册中心的典型结构
/serviceOrder/providers/192.168.1.10:8080   (临时节点)
/serviceOrder/providers/192.168.1.11:8080   (临时节点)
调用方 watch /serviceOrder/providers -> 列表变化即刷新本地路由表
负载均衡从路由表里挑一个 -> 发起 RPC
```

- **路由和负载均衡的实现**（1.3.7）：客户端拿到「可用实例列表」后，本地按算法挑一个发起调用；
  也可在**服务端**用 LVS/Nginx 做集中式负载均衡。

### 1.4 HTTP 服务网关

- 网关统一收口外部流量：路由转发、协议转换（HTTP↔内部 RPC）、鉴权、限流、日志、灰度。
  它让「后端一堆异构服务」对调用方呈现为「一个统一入口」。

## 版本演进

- **本书无第二版**；本节写 2014 年口径 → 2026 年视角的变化。
- **1.1 自研 TCP RPC → gRPC/Protobuf**（2015 开源，45341★ 实测）：今天几乎没人手搓 TCP 协议帧，
  而是用 gRPC（基于 HTTP/2 + Protobuf）拿到「强类型 IDL + 高效二进制 + 流式」一步到位。
  `google/protobuf`（72067★）成为序列化事实上标准。
- **1.3 的 ZooKeeper 注册中心 → Nacos / K8s 原生服务发现**：
  `alibaba/nacos`（33419★）把「配置中心 + 服务发现」合一，比 ZK 更贴近微服务；
  在云原生里，Kubernetes Service + CoreDNS 直接把「服务发现」变成平台能力，不再需要独立中间件。
- **1.3 负载均衡从「客户端 SDK」→「边车/Service Mesh」**：`istio/istio`（38408★）+
  `envoyproxy/envoy`（28995★）把路由/负载均衡/熔断下沉到 sidecar，业务代码零侵入。
- **1.4 网关 → 云原生网关/API Gateway**：从自研 Servlet 网关到 Spring Cloud Gateway、
  Kong、Envoy-based 网关；网关能力被 Mesh 部分吸收（东西向流量由 sidecar 接管）。
- **Spring Cloud 生态**（spring-cloud/spring-cloud 元仓库 195★，实际以各子模块计）：
  把本书「手工 SOA」需要的注册中心、配置、熔断、网关全部产品化，2015 年后成为 Java 系默认。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Fielding《Architectural Styles and the Design of Network-based Software Architectures》 | 博士论文, 2000（REST 提出） | **REST** 的源头，对应 1.2.6 |
| Waldo et al.《A Note on Distributed Computing》 | 1994 | 戳破「远程调用像本地调用」的幻想，RPC 语义边界的经典反思 |
| Vogels《Web Services: Taming the Wild Wild West》 | ACM Queue, 2003 | 分布式调用中「部分失败」的讨论 |
| Hunt, Konar et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | 本书 1.3 注册中心方案的直接原型 |
| Burrows《The Chubby lock service》 | OSDI 2006 | ZK 的设计参照（粗粒度锁 + 小文件） |
| Google《gRPC / Protocol Buffers》 | grpc.io / protobuf.dev | 2026 视角的 RPC 标准（2015 起） |
| Bu et al.《Service Mesh: A Revolutionary Approach to SOA》 | 2016（Buoyant/Istio 理念） | Service Mesh 概念成型，对应 2026 补丁 |

> 注：gRPC/Protobuf/Service Mesh 与具体论文年份较多版本，本目录只标注年份，不杜撰精确卷期。

## 近年研究与工业界开源实践（2015–2026）

- **RPC 标准化**：`grpc/grpc`（45341★）+ `google/protobuf`（72067★）是 2026 年跨语言 RPC 的事实标准；
  对比本书 1.1 的「手搓 TCP 帧 + Hessian」，今天直接用 IDL 生成多语言 stub。
- **Java 系 SOA/微服务框架**：`apache/dubbo`（41579★，阿里开源，源自淘宝内部 HSFSF/Dubbo）
  几乎就是本书所讲「淘宝 SOA」的工业级落地——注册中心、负载均衡、协议（Dubbo/ Triple=gRPC）
  一应俱全；`alibaba/nacos`（33419★）做动态配置 + 服务发现。
- **Spring 全家桶**：`spring-cloud/spring-cloud`（元仓库 195★；真正使用时以
  spring-cloud-commons、spring-cloud-gateway 等子模块计）把本书「手工 SOA」的每块能力产品化。
- **Service Mesh**：`istio/istio`（38408★）控制面 + `envoyproxy/envoy`（28995★）数据面，
  把 1.3 的「路由/负载均衡/熔断」下沉到基础设施，业务代码零改造——这是 2026 年对本章最大的改写。
- **注册中心演进**：`apache/zookeeper`（12811★）仍是存量系统主力；新系统多转向 Nacos 或
  K8s 原生（etcd + CoreDNS）。（etcd 的 star 见仓库 ../大规模分布式存储系统/ 与共识算法相关笔记。）
- **API 网关**：从本书 1.4 的自研 Servlet 网关，演进到 Spring Cloud Gateway、Kong、
  Envoy-based 网关；网关与 Mesh 的边界在「南北向/东西向」流量上重新划分。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「RPC 像本地调用，直接用就行」 | 远程调用有网络延迟、部分失败、超时三态，语义远比本地调用复杂 | 1.1 |
| 2 | 「HTTP 比 TCP 慢很多，能用 TCP 就不 HTTP」 | HTTP/2 + 二进制帧 + 连接复用后，差距大减；HTTP 的生态/调试/跨语言价值常被低估 | 1.1–1.2 |
| 3 | 「RESTful 和 RPC 是对立的」 | 二者是不同关注点（资源 vs 方法），HTTP RPC 可同时借两者的长处 | 1.2.6 |
| 4 | 「ZooKeeper 只能做注册中心」 | ZK 本质是「一致性的小数据存储 + watch」，也做分布式锁、选主、配置；且 CP 系统，网络分区时会拒绝写入 | 1.3.4 |
| 5 | 「负载均衡随机/轮询就够了」 | 节点异构、热点 key 存在时，需一致性哈希或最小连接数，否则倾斜 | 1.3.2 |
| 6 | 「网关只是路由转发」 | 网关还承担鉴权、限流、灰度、协议转换、防刷等横切关注点 | 1.4 |
| 7 | 🔧 1.1 的自研 TCP RPC 已被 gRPC/Protobuf 取代 | 2026 年手搓协议帧属于重复造轮子，gRPC 是跨语言默认 | 1.1 |
| 8 | 🔧 1.3 的 ZK 注册中心已非唯一解 | Nacos、K8s 原生服务发现成为主流，ZK 退居存量 | 1.3 |
| 9 | 🔧 缺 Service Mesh 视角 | Istio/Envoy 把服务治理下沉到边车，业务零侵入，是 2014 年没有的范式 | 1.3–1.4 |
| 10 | 🔧 缺云原生部署视角 | 容器/K8s 让「部署/扩缩容/服务发现」变成平台能力，而非应用层手工方案 | 1.3–1.4 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 1.3 的 ZooKeeper/路由 → [04-系统稳定性.md](04-系统稳定性.md)（心跳检测、容量评估要依赖服务发现）；
  - 1.2 的 HTTP → [03-互联网安全架构.md](03-互联网安全架构.md)（HTTPS/签名认证都跑在 HTTP 之上）；
  - 1.1–1.2 的序列化 → [02-分布式系统基础设施.md](02-分布式系统基础设施.md)（缓存/消息同样要序列化）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——ZooKeeper 的一致性本质是 ZAB 协议，想深究注册中心「为什么不会脑裂」去那里补。
- [../设计数据密集型应用/04-编码与演化.md](../设计数据密集型应用/04-编码与演化.md)
  ——DDIA 对序列化（Avro/Protobuf/Thrift/JSON）的系统讲法，与本章 1.1.2 直接对读。
- [../大规模分布式存储系统/03-分布式系统.md](../大规模分布式存储系统/03-分布式系统.md)
  ——3.7 的 Paxos/ZooKeeper 一致性背景，是本章注册中心的底层保证。
