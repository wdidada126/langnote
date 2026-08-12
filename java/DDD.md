# DDD

DDD解决扩展性问题

DDD研究十年心得：《复杂软件设计之道：领域驱动设计全面解析与实战》出版
https://www.jdon.com/54881

大型系统应用架构实战：部署、容灾、性能优化
https://www.douban.com/doubanapp/dispatch/review/12094490

领域驱动设计中国峰会 2017所有文档

https://github.com/heynickc/awesome-ddd
https://zhuanlan.zhihu.com/p/97680152
https://blog.csdn.net/m0_37055174/article/details/102656194
https://zhuanlan.zhihu.com/p/32459776

[DDD解决扩展性问题](https://www.douban.com/doulist/113575586/)

极客时间有

DO
DTO
是模型

领域模型又是？

我们还是来看看《阿里开发手册》提供的分层领域模型规约参考：

DO(Data Object)：此对象与数据库表结构一一对应，通过DAO层想上传输数据源对象。
DTO(Data Transfer Object)：数据传输对象，Service或Manager向外传输的对象。
BO(Business Object)：业务对象，由Service层输出的封装业务逻辑的对象。
AO(Application Object)：应用对象，在Web层与Service层之间抽象的复用对象模型，极为贴近展示层，复用度不高。
VO(View Object)：显示层对象，通常是Web向模版渲染引擎层传输的对象。
Query：数据查询对象，各层接收上层的查询请求。注意超过2个参数的查询封装，禁止使用Map类来传输。

一般的工作流程 写概要设计文档 数据库表 -> 
MyBatais也是基于

领域驱动设计
假设内存无限大，数据不需要存在数据库

[阿里盒马领域驱动设计实践](https://www.infoq.cn/article/alibaba-freshhema-ddd-practice)

对data model/domain model的对比

失学 贫血 充血模型的讲解

张群辉，阿里盒马架构总监。10多年技术及管理实战经验，前阿里基础机构事业部工程效率总监，长期在一线指导大型复杂系统的架构设计。DevOps、微服务架构及领域驱动设计国内最早的实践者一员。崇尚实践出真知，一直奋斗在技术一线。

在非 DDD 设计思路下的项目，我们一般先根据需求做数据库表的设计，然后根据表结构设计推导出相应的实体对象，这样的实体对象是数据模型转换的结果。此时，这些对象只是数据的载体，是没有行为的。在这种设计模式下，业务流程实现上仍旧是面向过程式，是一种以数据为中心的过程式思想，其开发过程可以理解为是对数据移动、处理和实现的过程。而如果采用 DDD 的思想去设计，我们将建立一个基于面向对象设计的系统

[领域驱动设计（DDD）在有赞教育线索资源管理的实践](https://www.infoq.cn/article/HVTWari0Ru4MSSGPvkYv)

需求分析利器 — 四色原型图

程英杰  有赞教育

[基于DDD的微服务设计和开发实战](https://weibo.com/ttarticle/p/show?id=2309404386442074813348&sudaref=www.google.com&display=0&retcode=6102)

DDD 名词和术语 

Event Storming（事件风暴）：事件风暴是一项团队活动，旨在通过领域事件识别出聚合根，进而划分微服务的限界上下文。在活动中，团队先通过头脑风暴的形式罗列出领域中所有的领域事件，整合之后形成最终的领域事件集合，然后对于每一个事件，标注出导致该事件的命令（Command），再然后为每个事件标注出命令发起方的角色，命令可以是用户发起，也可以是第三方系统调用或者是定时器触发等。最后对事件进行分类整理出聚合根以及限界上下文。
Entity（实体）：每个实体是唯一的，并且可以相当长的一段时间内持续地变化。我们可以对实体做多次修改，故一个实体对象可能和它先前的状态大不相同。但是，由于它们拥有相同的身份标识，他们依然是同一个实体。例如一件商品在电商商品上下文中是一个实体，通过商品中台唯一的商品 id 来标示这个实体。
ValueObject（值对象）：值对象用于度量和描述事物，当你只关心某个对象的属性时，该对象便可作为一个值对象。实体与值对象的区别在于唯一的身份标识和可变性。当一个对象用于描述一个事物，但是又没有唯一标示，那么它就是一个值对象。例如商品中的商品类别，类别就没有一个唯一标识，通过图书、服装等这些值就能明确表示这个商品类别。
Aggregate（聚合）：聚合是实体的升级，是由一组与生俱来就密切相关实体和值对象组合而成的，整个组合的最上层实体就是聚合。
Bounded Context（限界上下文）：用来封装通用语言和领域对象，为领域提供上下文语境，保证在领域之内的一些术语、业务相关对象等（通用语言）有一个确切的含义，没有二义性。使团队所有成员能够明确地知道什么必须保持一致，什么必须独立开发。

## DDD 综合笔记（截至 2026-08）

### DDD 要解决什么，不解决什么

DDD（Domain-Driven Design，领域驱动设计）是让代码模型、团队语言和业务规则保持一致的一组建模原则与模式，重点是处理规则复杂、概念易变、多人协作的核心业务复杂度。它不是数据库设计方法、Java 框架、四层模板或把所有对象改成“充血模型”的口号。

简单 CRUD、报表、后台配置和稳定的技术适配层可以使用朴素分层或事务脚本；只有业务规则密集且变化频繁的部分才值得投入事件风暴、限界上下文和聚合建模。DDD 不自动带来微服务、高可用或性能，错误的边界反而会把单体复杂度转成分布式复杂度。

原笔记中的 DO、DTO、BO、AO、VO 是分层传输/展示对象的约定，不等于 DDD 的领域模型。一个领域实体不应直接承担 ORM 映射、HTTP JSON、页面渲染和跨服务传输的所有职责；它可以与持久化对象在小型项目中复用，但要明确这是工程权衡，而非 DDD 的必然要求。

| 概念 | 核心问题 | 典型位置 |
| --- | --- | --- |
| 领域（Domain）/子域 | 业务要解决什么问题，什么构成竞争力 | 核心、支撑、通用子域。 |
| 通用语言（UL） | 业务、产品、开发、测试是否用同一术语说同一件事 | 需求、代码、接口、指标和测试都应使用。 |
| 限界上下文（BC） | 一个术语和模型在哪个边界内有效 | 订单中的“客户”与风控中的“客户”可有不同模型。 |
| 实体（Entity） | 是否按身份和生命周期区分 | `OrderId` 相同即同一订单，属性可变。 |
| 值对象（VO） | 是否按值相等、通常不可变 | Money、地址快照、时间区间。 |
| 聚合/聚合根 | 哪些不变量必须在一次本地事务中成立 | 只经根修改和引用内部对象。 |
| 领域服务 | 哪条业务规则不自然属于单一实体/值对象 | 定价、授信决策等无状态领域操作。 |
| 应用服务 | 一个用例如何编排、授权、开事务和调用端口 | 不承载核心业务规则。 |

### 战略设计：先画边界，再写类

从用户旅程、规则变化点、组织责任、数据所有权和失败代价开始，而不是先按表名、前端菜单或技术层拆服务。事件风暴可以用“领域事件 -> 命令 -> 参与者/策略 -> 读模型/外部系统”发现语言和冲突点，但产出必须回到可评审的领域词汇表、业务规则、上下文地图和接口契约。

上下文地图显式记录关系：合作关系（Partnership）、共享内核（Shared Kernel）、客户-供应商（Customer-Supplier）、防腐层（ACL）、公开主机服务（OHS）等。共享数据库、复制同名 DTO 或让下游直接读上游表都不是上下文集成；它们会绕过边界，使模型和发布节奏重新耦合。

服务边界不是机械地“一 BC 一个微服务”。一个 BC 可先在模块化单体中以模块、独立 schema 和内部 API 落地；当团队独立交付、扩缩容、可靠性目标或数据主权确有需要，再拆成可独立部署服务。一个微服务不应混合多个 BC，也不宜小于需要单事务维护不变量的聚合。

### 战术设计：聚合是事务一致性边界

聚合不是“实体的升级”或任意实体集合，而是一组对象的不变量边界。外部只持有聚合根 ID；一次命令只修改一个聚合；跨聚合、跨服务的业务流程通过领域事件、补偿、对账和最终一致性完成。聚合通常应小，避免把订单、商品、库存、账户等不同生命周期对象塞进一次大事务。

```java
public final class Order {
    private final OrderId id;
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status = OrderStatus.DRAFT;

    public void addLine(ProductId productId, int quantity, Money unitPrice) {
        if (status != OrderStatus.DRAFT) throw new DomainException("已提交订单不可修改");
        if (quantity <= 0 || !unitPrice.isPositive()) throw new DomainException("数量和单价必须为正");
        lines.add(new OrderLine(productId, quantity, unitPrice));
    }

    public OrderSubmitted submit() {
        if (lines.isEmpty()) throw new DomainException("订单至少需要一条明细");
        status = OrderStatus.SUBMITTED;
        return new OrderSubmitted(id, total());
    }
}
```

上例的关键不是 Java 类的私有字段，而是 `submit` 前的业务不变量只能经 `Order` 检查。库存扣减不应直接修改订单内部集合；它应消费已提交事件，在自己的库存聚合中做条件更新。并发命令要使用版本号/乐观锁、唯一约束或条件写入保护不变量，不能只依赖“事件最终会到达”。

### 事件、消息与一致性

领域事件描述业务已经发生的事实，如 `OrderSubmitted`，而不是“插入了一行表”或“调用了某个 REST API”。领域事件可先在同一进程内触发；跨边界发布的集成事件是经过版本化、脱敏和稳定契约设计后的消息，二者不可混同。

可靠发布常见闭环：本地事务同时写聚合状态和 outbox 记录 -> 独立发布者投递消息 -> 消费者按业务键幂等处理 -> 失败重试/死信/人工补偿 -> 用对账任务发现漏处理。消息系统通常是至少一次投递，消费者必须处理重复、乱序、延迟和重放；不要声称“exactly once”而忽略外部副作用。

CQRS 是读写模型分离，不等于必须引入事件溯源。读模型可以由同库查询、投影表、搜索索引或缓存实现；是否异步取决于读写压力、延迟目标和一致性要求。事件溯源是以事件序列作为状态事实来源，审计价值高但版本演进、重放、删除/隐私合规、查询投影和运维成本也更高。

### Java 落地结构与测试

建议让依赖从外向内：`interfaces`（HTTP/MQ/CLI）-> `application`（用例编排）-> `domain`（模型与规则）<- `infrastructure`（JPA、MQ、RPC 实现）。Repository 是领域侧定义的集合式访问端口，基础设施实现它；不要把 ORM Repository 的任意查询能力泄漏到领域代码。

```text
order
  domain/          Order, OrderId, Money, OrderRepository, OrderSubmitted
  application/     SubmitOrder, SubmitOrderHandler
  interfaces/      OrderController, SubmitOrderRequest
  infrastructure/  JpaOrderRepository, OutboxPublisher
```

测试按风险分层：值对象/聚合不变量用快速单元测试；应用服务验证授权、事务和端口协作；Repository/outbox/消费者用集成测试验证数据库与消息语义；再用契约测试固定外部 API 和事件 schema。不要用 mock 验证大量内部调用顺序来替代对业务规则和持久化语义的验证。

### 常见失败方式与检查问题

1. **按数据库表拆服务。** 表之间强事务和频繁 join 仍存在时，服务只是远程 DAO。
2. **全系统一套“通用领域模型”。** 同名概念被迫统一，导致模型巨大且无法演进；应先允许 BC 内语义独立。
3. **聚合过大或跨聚合强事务。** 锁竞争和分布式事务增加；将真正需要同步维护的不变量留在聚合内。
4. **把应用服务写成巨型流程脚本。** 规则散在 `if/else`、Controller 和 SQL 中；把稳定的业务决策收敛到实体、值对象或领域服务。
5. **为了 DDD 而 DDD。** 简单 CRUD 引入 Factory、Repository、Domain Service 等空壳，只增加间接层；复杂度应由业务规则证明。

每次设计评审至少回答：术语在此 BC 中的定义是什么？核心不变量是什么、由哪个聚合根维护？哪个数据源拥有真相？跨边界是同步调用还是异步事件？失败、重复、超时和补偿由谁处理？哪些变化会破坏接口兼容？

### 学习顺序与资料

1. 先读 Eric Evans 的《Domain-Driven Design》与其免费的 [DDD Reference](https://www.domainlanguage.com/ddd/reference/)，建立通用语言、BC、聚合和上下文映射的准确词义。
2. 再读 Vaughn Vernon 的《Implementing Domain-Driven Design》或《Domain-Driven Design Distilled》，用一个真实业务完成事件风暴、上下文地图、聚合和事件设计。
3. 对照 [Martin Fowler 的 Bounded Context](https://martinfowler.com/bliki/BoundedContext.html) 与 [Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html)，避免把模型边界误解成数据结构。
4. 实现层可参考 [Microsoft 的 DDD 微服务建模指南](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)：复杂 BC 使用聚合和领域事件，简单 CRUD 保持简单。
