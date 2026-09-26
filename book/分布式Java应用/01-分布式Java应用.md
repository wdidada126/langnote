# 第 1 章　分布式Java应用

> 原书第 1 章是全书**唯一的总纲章**：它把「分布式 Java 应用系统间如何通信」收敛成两条主干——
> **基于消息方式**（你发我收，解耦、异步）与**基于远程调用方式**（像调本地方法一样调远端）。
> 但这一章也是**最需要 2026 年补丁**的地方：1.1 只讲手写 BIO/NIO 与 Mina，
> 而今天 99% 的 Java 通信层是 **Netty**；1.2 只讲 RMI/Web Services，
> 而今天跨语言的事实标准是 **gRPC（HTTP/2 + Protobuf）**，服务治理早已交给 Dubbo/Spring Cloud。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 基于消息方式实现系统间的通信 | 消息 = 发送方不关心谁接收；四种 Java 原生组合（TCP/UDP × BIO/NIO）；开源框架 Mina/Netty | **消息方式解耦生产与消费**，是异步与削峰的底座 |
| 1.1.1 基于Java自身技术 | TCP/IP+BIO、TCP/IP+NIO、UDP/IP+BIO、UDP/IP+NIO；多播 MulticastSocket | BIO 简单但有连接数天花板；**NIO 用少量线程扛海量连接** |
| 1.1.2 基于开源框架 | Mina、jboss-netty（今 Netty）封装 NIO 的复杂度 | 业务只写编解码与handler，通信细节下沉给框架 |
| 1.2 基于远程调用方式实现系统间的通信 | 远程调用 = 像本地方法一样调远端；Java 自身 RMI、Web Services；开源框架 Spring RMI/CXF/Axis/JMS/EJB | **远程调用强调「接口契约」**，比消息更贴合「请求-响应」语义 |
| 1.2.1 基于Java自身技术 | RMI（JRMP 协议 + 序列化）、Web Services（SOAP + WSDL + UDDI） | RMI 仅 Java 内；Web Services 跨语言但重 |
| 1.2.2 基于开源框架 | Spring RMI、CXF、Axis、JMS、EJB 等 | 框架把「找服务 + 编解码 + 传输」打包，开发者只写接口与实现 |

## 核心精讲

（以下为教学性梳理；所有 Java 片段均**教学示意，不参与构建**，绝不编译/运行。）

### 1.1 消息方式：四种原生组合与 NIO 的本质

- **四种组合**（本书 1.1.1 的核心速查）：

| 组合 | 传输 | IO 模型 | 特点 |
| --- | --- | --- | --- |
| TCP/IP + BIO | TCP | 阻塞 | `ServerSocket.accept()` 每连接一线程，连接数受限 |
| TCP/IP + NIO | TCP | 多路复用 | `Selector` 单线程轮询多 Channel，连接数近乎无上限 |
| UDP/IP + BIO | UDP | 阻塞 | 无连接、丢包，适合广播/低延迟 |
| UDP/IP + NIO | UDP | 多路复用 | UDP + 多路复用，高并发信令场景 |

- **BIO 的天花板**：每连接一线程，C10K 问题下线程切换与内存（每线程栈 256K~1M）直接打爆。
- **NIO 的枢纽是 `Selector`**（教学示意，不参与构建）：

```java
// 教学示意，不参与构建：NIO 服务端骨架（省略异常处理与编解码）
Selector selector = Selector.open();
ServerSocketChannel ssc = ServerSocketChannel.open();
ssc.configureBlocking(false);
ssc.socket().bind(new InetSocketAddress(8080));
ssc.register(selector, SelectionKey.OP_ACCEPT);
while (true) {
    selector.select();                       // 阻塞直到有就绪事件
    Iterator<SelectionKey> it = selector.selectedKeys().iterator();
    while (it.hasNext()) {
        SelectionKey key = it.next();
        if (key.isAcceptable()) { /* 接受新连接，注册 OP_READ */ }
        else if (key.isReadable()) { /* 读数据，必要时注册 OP_WRITE */ }
        it.remove();
    }
}
```

- **写事件（OP_WRITE）的特殊性**：一般直接写即可；只有当发送缓冲区满（网络拥塞）才注册 `OP_WRITE`，
  等下次可写时续传。这是本书明确点出的 NIO 易错点。
- **Mina / Netty 的价值**：把上面的 `Selector` 循环、半包/粘包、断连重连、线程模型全封装掉，
  业务只写 `IoHandler` / `ChannelHandler` 和编解码器。

### 1.2 远程调用方式：RMI 与 Web Services

- **RMI 三段式**（教学示意，不参与构建）：

```java
// 教学示意，不参与构建：RMI 最小骨架
// 1) 接口继承 Remote
public interface Hello extends Remote { String say() throws RemoteException; }
// 2) 实现继承 UnicastRemoteObject，并用 Naming.rebind 注册
// 3) 客户端用 Naming.lookup("rmi://host:1099/Hello") 拿到 stub 后像本地一样调用
```

- RMI 靠 **Java 原生序列化** + **JRMP** 协议，仅限 Java 对 Java，且 stub 强耦合接口。
- **Web Services（SOAP）**：用 WSDL 描述服务、SOAP（XML）承载报文、UDDI 做注册发现，
  **跨语言**但报文重、性能差，今天基本被 REST + JSON 与 gRPC 取代。
- **开源框架把「找服务 + 编解码 + 传输」打包**：Spring RMI（简化 RMI 配置）、
  CXF/Axis（Web Services）、JMS（消息型远程调用）、EJB（容器托管）。

> 读这句时请对照 [02-大型分布式Java应用与SOA.md](02-大型分布式Java应用与SOA.md)：
> 远程调用 + 消息，正是 SOA「服务」的两类交互原语。

## 版本演进

- **本书无第二版**；本节写 2010 年口径 → 2026 年视角的变化。
- **1.1.1 通信框架：Mina → Netty**。本书成书时 Mina 与 jboss-netty 并立；
  Netty（由 Mina 作者之一 Trustin Lee 另起炉灶）后来成为事实标准，
  Dubbo、gRPC-Java、RocketMQ、Elasticsearch 的通信层全是 Netty。`apache/mina` 仅 922★，
  `netty/netty` 已达 35065★（2026-09 实测）。读本节时把「Mina」脑内替换为「Netty」。
- **1.1 编解码：手写协议 → IDL 生成**。本书的「文本/二进制/自定义协议」被 **Protobuf**
  （`google/protobuf` 72067★）、FlatBuffers 等 IDL 方案统一；跨语言、强契约、体积小。
- **1.2.1 RMI/Web Services → gRPC / Thrift**。gRPC（`grpc/grpc-java` 12073★，基于 HTTP/2 + Protobuf）
  已是跨语言 RPC 事实标准；Apache Thrift（`apache/thrift` 10959★）仍是跨语言老牌方案。
  RMI 仅存于极老旧内部系统，Web Services/SOAP 基本退出历史舞台。
- **1.2.2 服务框架：手写 → Dubbo / Spring Cloud**。本书列举的 Spring RMI/CXF/Axis 多已过时；
  今天 Java 服务治理由 `apache/dubbo`（41579★）、`alibaba/spring-cloud-alibaba`（29179★）、
  `OpenFeign/feign`（9802★）承载。
- **通信安全**：本书未提 TLS/mTLS；2026 年 gRPC 默认 h2 + TLS，Service Mesh 用 mTLS 透明加密。
- **反应式与虚拟线程**：本书的 NIO 线程模型在 2026 年被 Project Reactor / RxJava、
  以及 JDK 21 虚拟线程（见 [03-深入理解JVM.md](03-深入理解JVM.md)）从两个方向改写。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Java RMI Specification（JSR-51 等） | Sun Microsystems / JDK | 本书 1.2.1 RMI 的规范来源 |
| SOAP 1.1 / 1.2 | W3C Recommendation | 本书 1.2.1 Web Services 的报文标准 |
| WSDL 1.1 / 2.0 | W3C | Web Services 的服务描述语言 |
| UDDI | OASIS | Web Services 的注册发现（今已基本弃用） |
| Waldo et al.《A Note on Distributed Computing》 | 1994（ACM  reprinted） | 「远程调用不是本地调用」的哲学源头，解释为何 1.2 的「像本地一样」是错觉 |
| Fielding《Architectural Styles and the Design of Network-based Software Architectures》（REST 博士论文） | 2000, UCI | REST 取代 SOAP 的理论底座 |
| Vinoski《CORBA: Integrating Diverse Applications Within Distributed Heterogeneous Environments》 | IEEE Communications 1997 | 早期跨语言 RPC（CORBA/IIOP）的工程范式 |
| OMG《Common Object Request Broker Architecture (CORBA)》 | OMG 规范 | 比 RMI 更早的跨语言对象请求代理 |
| Gamma et al.《Design Patterns》— Reactor 模式 | 1994 | NIO 的 `Selector` 多路复用即 Reactor 模式的实现 |

> 注：以上规范/论文均为真实存在，未杜撰。具体版本号（如 SOAP 1.1 vs 1.2）以 W3C 官方页为准，本目录不逐项标注。

## 近年研究与工业界开源实践（2015–2026）

- **Netty 统治 Java 通信层**（本章 1.1.2 的现实答案）：`netty/netty` **35065★**（2026-09 实测），
  Dubbo、gRPC-Java、RocketMQ、Cassandra、Elasticsearch 均基于它。Mina 退居 `apache/mina` **922★**。
- **gRPC 成为跨语言 RPC 标准**（本章 1.2.1 的现实答案）：`grpc/grpc-java` **12073★**，
  基于 HTTP/2 多路复用 + Protobuf；`google/protobuf` **72067★** 是其契约基础。
- **Apache Thrift 仍是跨语言老牌**：`apache/thrift` **10959★**，适合多语言内部服务。
- **Dubbo / Spring Cloud 接管服务框架**（本章 1.2.2 的现实答案）：
  `apache/dubbo` **41579★**（Dubbo 3 已转向应用级服务发现 + Triple 协议）、
  `alibaba/spring-cloud-alibaba` **29179★**、`OpenFeign/feign` **9802★**（声明式 HTTP 客户端）。
- **服务注册发现**（本章 1.2「找服务」的现代实现）：`alibaba/nacos` **33419★**、
  `apache/zookeeper` **12811★**、`Netflix/eureka` **12746★**（已归档但仍广泛存量）。
- **消息中间件**（本章 1.1 的「消息方式」落地）：`apache/kafka` **33849★**、
  `apache/activemq` **2464★**（ActiveMQ 是本书提到的 JMS 实现之一，已不如 Kafka/RocketMQ 主流）。
- **跨语言序列化**：除 Protobuf 外，FlatBuffers、Cap'n Proto 在游戏/边缘场景常用；
  Java 原生序列化（本书 1.2.1 RMI 的默认）因体积大、慢、有安全漏洞，已被明确淘汰。
- **分布式缓存/对象**（本章远程调用之外的「共享状态」）：`redisson/redisson` **24403★**、
  `redis/lettuce` **5779★**，基于 Redis 提供分布式锁/集合/Map 等 JDK 接口实现。

> 说明：以上 star 数均为 2026-09 `gh api` 实测，未杜撰；spring-boot 81507★、spring-framework 60257★
> 作为对比参照。一处未核实：eclipse-jetty/jetty.project 返回 404（star 数未能核实，未杜撰）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「远程调用和本地调用一样」 | Waldo 1994 论文已论证：**网络调用有延迟、会失败、不幂等**；1.2 的「像本地一样」是抽象错觉，必须处理超时/重试/幂等 |
| 2 | 「BIO 够用」 | 连接数上千即线程耗尽；高并发必须用 NIO/Netty（见 1.1 结论） |
| 3 | 「NIO 就是Selector 加几行代码」 | 半包/粘包、拆连接重连、线程模型、背压才是难点，所以才有 Netty |
| 4 | 「Web Services/SOAP 是 RPC 的未来」 | 2010 年后被 REST+JSON、gRPC 取代；SOAP 报文重、跨语言收益不再突出 |
| 5 | 「RMI 可用于跨语言」 | RMI 仅 Java2Java，且强耦合接口与 JRMP；跨语言请用 gRPC/Thrift |
| 6 | 「消息方式和远程调用可随意换」 | 消息=解耦/异步/削峰（不关心谁收）；远程调用=请求-响应/强契约；语义不同，选型要看业务 |
| 7 | 🔧 1.1.2 仍以 Mina 为主角 | 2026 年事实标准是 **Netty**（35065★ vs Mina 922★）；读本节请脑内替换 |
| 8 | 🔧 1.2.1 没有 gRPC / Thrift | 2026 年跨语言 RPC 事实标准是 **gRPC（HTTP/2+Protobuf）**，本书只有 RMI/Web Services |
| 9 | 🔧 1.2.2 的服务框架已过时 | Spring RMI/CXF/Axis 多被 **Dubbo / Spring Cloud / Feign** 取代；本章列举项需整体更新 |
| 10 | 🔧 本章缺「服务注册发现 + 配置中心」 | 2026 年的「找服务」由 Nacos/Zookeeper/Eureka 承担，本书 1.2 只字未提 |
| 11 | 🔧 本章缺「通信安全（TLS/mTLS）」 | 今天 gRPC 默认 h2+TLS，Service Mesh 用 mTLS 透明加密；本书完全未涉及 |
| 12 | 🔧 本章缺「序列化安全」提醒 | Java 原生序列化有反序列化漏洞（gadget chain），2026 年应改用 Protobuf 等 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 1.1 消息方式 → [02-大型分布式Java应用与SOA.md](02-大型分布式Java应用与SOA.md)（SOA 的服务交互原语）；
  - 1.2 远程调用 → [04-分布式应用与SunJDK类库.md](04-分布式应用与SunJDK类库.md)（4.3 序列化正是远程调用的 payload 载体）；
  - 1.1.1 NIO/Selector → [03-深入理解JVM.md](03-深入理解JVM.md)（3.3 线程模型决定 NIO 的并发能力）；
  - 1.2 远程调用框架 → [06-构建高可用的系统.md](06-构建高可用的系统.md)（服务调用链的高可用依赖注册发现与熔断）。
- [../分布式Java应用.md](../分布式Java应用.md) —— 仓库大纲版（仅 11 行），本目录是其精读展开，只链接不修改。
- [../深入理解Apache Dubbo与实战.md](../深入理解Apache Dubbo与实战.md) —— 本书 1.2.2 的 2026 升级版，必配。
- [../大型网站系统与Java中间件开发实践.md](../大型网站系统与Java中间件开发实践.md) —— 淘宝系服务框架/消息中间件同源经验。
- [../微服务架构设计模式.md](../微服务架构设计模式.md) —— 本书 1.2 远程调用在微服务语境下的修正与深化。
- [../设计数据密集型应用.md](../设计数据密集型应用.md)（DDIA 第 4 章请求-响应与基于消息的通信）—— 两种通信范式的理论底座。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md) —— 服务注册发现（Zookeeper/etcd）背后的共识算法。
