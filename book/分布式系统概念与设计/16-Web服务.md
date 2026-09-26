# 16 Web 服务（第 9 章 Web 服务）

> **本章地图**：Web 服务定位（用 Web 技术做的分布式中间件，面向异构互操作）→ 服务描述与 IDL 之别 → **SOAP**（信封：Header/Body、编码、HTTP 之上的 RPC 与文档式交换、中介者）→ **WSDL**（抽象接口 + 具体绑定：types/message/portType/binding/port/service）→ **UDDI** 与服务发现（白/黄/绿页、三种数据结构）→ **XML 安全**：XML Signature、XML Encryption、WS-Security、分布式对象访问控制案例。

## 本章地图

第 5 版把 Web 服务从「案例研究」提升为正文一章（第 9 章，位于 Middleware 部分），主张它是「跨组织、跨平台的 CORBA 替代者」。三大件 **SOAP/WSDL/UDDI** 构成「消息—描述—发现」闭环，XML 安全补充跨信任域的安全承诺。2026 年回看：这套栈在企业遗留系统里仍在运行，但新系统已转向 REST/OpenAPI、gRPC 与 GraphQL——本章的价值在于理解「面向服务」的抽象本身：消息契约、描述与绑定分离、可发现的注册中心。

## 核心精讲

> 以下 XML/伪代码均为**教学示意，不参与构建**。

### 9.1 Web 服务的动机与定位

- 与第 8 章（分布式对象/CORBA，见 05-分布式对象与远程调用.md）对比：CORBA 靠**共享二进制协议与 IDL**，跨组织部署几乎不可能；Web 服务全部用**文本 + HTTP + 广泛实现的规范**，牺牲效率换互操作。
- 服务不共享「对象引用」，共享的是**消息契约**——这是从「分布式对象」到「面向服务（SOA）」的世界观转变。
- **服务与组件的界面**：服务边界只暴露业务操作，不暴露对象状态；无状态化让横向扩展与组合（orchestration/choreography）成为可能。
- 🔧 这一转变的直接继承者是 REST（资源 + 统一接口）与 gRPC（重新拥抱二进制与 IDL——历史画了个圈）。

### 9.2 SOAP

- 信封结构（教学示意）：

  ```xml
  <Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
    <Header>
      <t:txn mustUnderstand="1">T-1001</t:txn>
    </Header>
    <Body>
      <m:getPrice><m:symbol>ACME</m:symbol></m:getPrice>
    </Body>
  </Envelope>
  ```

- 两种交互风格：**RPC 风格**（方法/参数编码）与**文档风格**（整份业务文档交换，文档驱动）。
- 传输不限于 HTTP（SMTP、消息队列亦可）；Header 块支持**中介者（intermediary）**逐跳处理，`role`/`mustUnderstand` 控制谁必须理解哪个块。
- **Fault 结构**：code/subcode/reason/detail——错误也是契约的一部分。
- 🔧 工程教训：SOAP 的「规范组合爆炸」（WS-* 家族数十个标准）正是后来业界退回简单性（REST）的原因——复杂性税按服务数量平方增长。

### 9.3 WSDL（Web Services Description Language）

- 分离**抽象**与**具体**：

  | 元素 | 层次 | 作用 |
  | --- | --- | --- |
  | `<types>` | 抽象 | XML Schema 数据类型 |
  | `<message>` | 抽象 | 消息部件 |
  | `<portType>` | 抽象 | 抽象操作集（类比 IDL 接口） |
  | `<binding>` | 具体 | 协议/编码绑定（如 SOAP over HTTP） |
  | `<port>/<service>` | 具体 | 网络地址 |

- 与 CORBA IDL 的差别：WSDL 是**XML 文档**而非编译期产物；绑定可替换（同一 portType 多种 binding）。
- WSDL 2.0 的改进：统一 message/interface 语义、支持 REST 式 HTTP 绑定——「同一个接口，两种世界观」。
- 🔧 现代对应物：OpenAPI（Swagger，REST 的契约描述）与 protobuf IDL（gRPC）——抽象/具体分离的设计被完整继承。

### 9.4 UDDI 与服务发现

- 三类页：**白页**（谁）、**黄页**（按行业分类）、**绿页**（技术描述，指向 WSDL）。
- 数据结构：`businessEntity`（组织）→ `businessService`（服务）→ `bindingTemplate`（访问点 + tModel 引用），`tModel` 是「技术指纹」的注册单位。
- 发现 = 查询注册中心获得 WSDL 地址 → 客户端按 WSDL 生成调用代码。
- 🔧 实际历史：公共 UDDI 注册中心从未流行（IBM/Microsoft 的根节点 2005 年前后关闭）；服务发现以企业内部注册中心（Eureka、Consul）或 API 网关/服务网格形态存活——发现的问题没消失，只是换了层。

### 9.5 XML 安全

- **XML Signature**：对 XML 子树**选择性签名**（可只签文档一部分），解决「一份文档多人依次签名」场景；代价是规范化（canonicalization）的复杂与安全陷阱（包裹签名混淆、实体扩展攻击）。
- **XML Encryption**：对元素级加密，同文档内不同接收者读不同部分。
- **WS-Security**：把签名/加密令牌（X.509、Kerberos 票据、SAML 断言）放进 SOAP Header，实现**消息级安全**（端到端，不依赖传输层 TLS 的逐跳安全）。
- 访问控制案例（书中）：分布式对象系统的调用按调用者凭据 + 策略决定是否授权——策略语言思想（XACML 思路）的先驱。
- 🔧 现代注脚：传输级 TLS + JWT/OIDC 的组合以简单性取胜；消息级安全保留在金融/政务等强合规场景。

### 算法走查（教学示意，不参与构建）

**走查 1：一次 SOAP 调用的全链路**

1. 客户端从 UDDI/配置取得 WSDL → 按 portType 生成代理存根（或手写模板）；
2. 存根把调用参数序列化为 SOAP Body，安全需求塞进 Header（WS-Security 时间戳 + 签名）；
3. 经 HTTP POST 到 binding 指定的 endpoint，Content-Type 为 SOAP 媒体类型；
4. 服务端按 Header 的 role/mustUnderstand 决定哪些中介者处理哪些块，未理解的 mustUnderstand 块 → 返回 Fault；
5. Body 交给业务层，响应反向序列化回存根；
6. 任意一步失败 → SOAP Fault（code/detail）沿原路返回。

**走查 2：XML 签名包裹攻击（signature wrapping）**

- 签名只覆盖 `<Body>` 里的某个**元素**（引用按 ID 定位）；
- 攻击者把原元素挪走，塞进一个自己的恶意元素，再把**原元素原样复制**进文档另一处——签名校验仍能找到「一个匹配的已签名元素」并通过；
- 防御要点：校验「签名引用的元素是**唯一**的」「处理逻辑只读取被引用的那个元素」——规范化的实现细节就是攻击面。
- 🔧 这正是「文档级灵活性的代价」的具体案例，也是消息级安全被简化方案（TLS + JWT）替代的原因之一。

**走查 3：WSDL → 客户端代码的映射**

```text
portType: getQuote(symbol: xsd:string) → xsd:decimal   （抽象操作）
binding : 上述操作绑定到 SOAP/HTTP, literal 编码        （具体协议）
port/service: http://quotes.example.com/soap           （具体地址）
生成产物（教学示意）:
  interface Quotes { decimal getQuote(string symbol); }
  Quotes q = QuotesFactory.fromWSDL(url).getPort();
```

- 抽象/具体分离的好处：同一 portType 换 binding（如改走 JMS）不动业务代码——OpenAPI/protobuf 保留了这一分层。

### 自测问答（教学自用）

- **Q：SOAP Header 的 mustUnderstand 有什么工程意义？** 它把「扩展」变成可协商的：中介者遇到必须理解却不认识的块必须整体拒绝——这等价于数据库 schema 的严格校验，防止「静默忽略关键指令」（如事务块被跳过）。
- **Q：文档风格 SOAP 为什么比 RPC 风格更长寿？** 文档（业务单据）演进慢、可以 schema 校验、易于异步队列传递；RPC 方法签名耦合实现，改一个参数就破坏所有客户端——微服务「消息契约优先」的直觉由此而来。
- **Q：UDDI 失败的根本原因？** 公共注册中心假设「陌生人按分类目录找服务并直接调用」，现实集成总是双边契约（密钥、SLA、计费）——发现可以自动化，**信任**不能；所以 API 网关（双边信任的载体）活了下来。
- **Q：REST 是不是「没有描述语言」？** 有，OpenAPI，但 REST 的核心是**统一接口 + 超媒体**：描述只辅助开发期，运行时靠自描述消息——这正是它与 SOAP「运行时依赖契约」的分野。
- **Q：gRPC 为什么放弃 HTTP 的「缓存与统一接口」？** RPC 语义（动词自定义、幂等性不统一）与 HTTP 缓存语义天然冲突；gRPC 用 HTTP/2 只取其多路复用与流控——这是对 REST 教条的务实背离。

## 版本演进

- 第 1–3 版：无独立 Web 服务章（SOAP 2000 年前后才出现）。
- 第 4 版（2005）：「Web Services」首成一章，覆盖 SOAP/WSDL/UDDI/Grid 初步。
- 第 5 版（2012，中译本第 9 章）：归入 Middleware 部分，与第 8 章「分布式对象和组件」并列；Grid/OGSA 材料移至配套网站。注意本版目录中 **Web 服务在第 9 章**（不是 4 版习惯里的第 19 章），名字服务在其后第 13 章。
- 中译本（机械工业出版社 2013）章题「Web 服务」，与英文第 5 版第 9 章 Web Services 对应。

## 经典论文与原始文献

| 论文/规范 | 出处 | 贡献 |
| --- | --- | --- |
| W3C《SOAP Version 1.2》 | W3C Recommendation, 2003/2007 | SOAP 规范本体 |
| W3C《Web Services Description Language (WSDL) 1.1/2.0》 | W3C, 2001/2007 | 服务描述 |
| OASIS《UDDI Version 3》 | OASIS Standard, 2002–2005 | 注册中心 |
| W3C《XML Signature Syntax and Processing》 | W3C/IETF, 2002 | 结构化文档签名 |
| W3C《XML Encryption Syntax and Processing》 | W3C, 2002 | 元素级加密 |
| OASIS《WS-Security: SOAP Message Security 1.1》 | OASIS Standard, 2006 | 消息级安全 |
| Fielding《Architectural Styles and the Design of Network-based Software Architectures》 | 2000（UCI 博士论文） | REST（对照面） |

## 近年研究与工业界开源实践（2015–2026）

- **SOAP→REST 的全面迁移**：公开 API 中 SOAP 已边缘化（仅存于银行/电信/政务遗留集成）；OpenAPI 规范成为契约描述的事实标准。
- **gRPC 的兴起**：protobuf IDL + HTTP/2 多路复用 + 四种流式模式，把「高效 IDL + 强契约」请回舞台——本质是对 SOAP 时代「强契约 + 弱性能」的反转补正（`grpc/grpc`，45342★）。
- **GraphQL**：客户端声明式取数，服务端单一 schema（`graphql/graphql-js`，20346★），解决了 REST 的过度获取/多次往返问题；联邦（federation）架构对应 UDDI 的「跨服务组合」需求。
- **服务网格**：`istio/istio`（38408★）把 Header 块的中介者语义下沉到 sidecar（mTLS 重试、熔断、按策略路由）——WS-* 想在消息里做的事，网格在基础设施层做完了。
- **RPC 中间件对照**：`apache/dubbo`（41578★）从「泛化调用 + 注册中心」演进到与 gRPC/HTTP 三协议并存，是国内 SOA→微服务演进的活样本；`apache/rocketmq`（22620★）的事务消息承接文档式异步交换。
- **API 治理的当代形态**：API 网关（限流/鉴权/计量）替代 UDDI 的「企业内注册中心」角色；契约测试（consumer-driven contracts）替代「先注册后调用」的开发流。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Web 服务 = SOAP/WSDL/UDDI 三件套」 | 那是 2000s 的具体化；「Web 服务」的现代形态是 REST/OpenAPI/gRPC/GraphQL |
| 2 | 「UDDI 是服务发现的标配」 | 公共 UDDI 早已关闭；发现由内部注册中心与网关/网格承担 |
| 3 | 「消息级安全优于 TLS」 | 二者解决不同问题；默认 TLS + 令牌即可满足绝大多数场景，且少一个规范化漏洞面 |
| 4 | 🔧 本书未覆盖 | REST 的架构约束与超媒体、HTTP/2/3 对 RPC 语义的影响、API 网关与服务的可观测性 |
| 5 | 「WSDL 已无用」 | 其抽象/绑定分离设计在 OpenAPI 与 protobuf 中原样存活；读 WSDL 是维护遗留集成的必备技能 |
| 6 | 「SOAP Header 的中介者只是历史」 | 服务网格 sidecar 的 mTLS/重试/路由恰是「逐跳处理块」的基础设施化 |

## 与其他章 / 其他书的联系

- 与第 8 章（CORBA，见 05-分布式对象与远程调用.md）对读：**同一问题（远程调用/描述/发现）的两代答案**。
- UDDI/发现与 14-移动与无处不在计算.md 的发现服务、09-名称服务与全局状态.md 的目录服务是同一问题的三种尺度。
- WS-Security 与第 11 章「安全性」（见 07-安全.md）互补；跨信任域授权与现代 API 安全对照 [book/分布式数据库入门进阶与实战/11-数据库中间件与SQL类数据库进化与选型.md](../分布式数据库入门进阶与实战/11-数据库中间件与SQL类数据库进化与选型.md)（中间件协议层）。
- 服务网格时代的事务/消息语义承接 12-分布式事务.md 的 TP monitor 现代形态。
