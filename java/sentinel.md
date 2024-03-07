# sentinel

`Sentinel` 是一个流量控制和熔断降级的开源项目，由阿里巴巴开发。它主要用于保护系统的稳定性和流畅性，通过限制流量、熔断降级等手段来防止系统过载。

以下是 `Sentinel` 的一些主要特点：

1. 流量控制：Sentinel 提供了多种流量控制策略，包括基于请求次数、并发线程数等的限制。
2. 熔断降级：当某个服务出现异常时，Sentinel 可以自动触发熔断机制，快速失败并降低对其他服务的影响。
3. 系统负载均衡：Sentinel 可以根据系统的实时负载情况动态调整流量，确保系统的稳定性。
4. 实时监控：Sentinel 提供了实时监控和报警功能，帮助开发者及时发现和处理问题。
5. 易扩展：Sentinel 的设计非常灵活，可以通过自定义规则和策略来满足不同场景的需求。
6. 高性能：Sentinel 基于高性能的 Reactor 模式实现，具有很高的性能和低延迟。
7. 轻量级：Sentinel 的部署非常简单，只需要少量的配置即可快速集成到现有的系统中。

总的来说，`Sentinel` 是一个非常强大且易于使用的流量控制和熔断降级工具，适用于各种规模的系统，无论是小型服务还是大型企业级应用。

b站视频，sentinel团队离职转岗了
dubbo3进入维护状态了，不更新新功能了
dubbo进入apache了
nacos有bug

https://gitee.com/edidada/testsentinelcloud
https://github.com/edidada/testsentinel

这两个java项目有try catch代码款 aop消除？

sentinal设置dubbo service的qps，dubbo应用集群部署，sentinal如何统计多个节点dubbo接口的调用次数
在Sentinel中，可以通过配置Dubbo的provider规则，来对Dubbo服务进行流量控制。在Dubbo应用集群部署时，可以使用Sentinel Dashboard来统计多个节点Dubbo接口的调用次数，并进行流量控制。

以下是使用Sentinel控制Dubbo服务流量的步骤：

1. 配置Dubbo的provider规则

您可以在Sentinel Dashboard中配置Dubbo的provider规则，以控制Dubbo服务的流量。在配置规则时，您需要指定Dubbo服务的接口名、方法名和参数类型，并设置QPS阈值。例如，在Sentinel Dashboard中，您可以添加以下规则：

```
Resource name: com.example.service.UserService.getUser(java.lang.String)
Limit app: default
Grade: QPS
Count: 10
```

在上述规则中，我们指定了`com.example.service.UserService.getUser`方法作为资源名，并将QPS阈值设置为10。这意味着，如果该Dubbo服务的该方法的请求速率超过10次/秒，Sentinel将拒绝更多的请求。

2. 部署Sentinel Dashboard

Sentinel Dashboard是一个可视化的监控和管理平台，可以用于监控多个节点的Dubbo服务。您可以在Sentinel Dashboard中查看多个节点Dubbo服务的调用次数和流量控制情况。

在部署Sentinel Dashboard时，您需要在Dubbo的provider和consumer中添加Dubbo Filter，并将Filter注册到Dubbo的SPI扩展机制中。例如，在Dubbo的provider和consumer中，您可以添加以下Filter：

```
<bean id="sentinelFilter" class="com.alibaba.csp.sentinel.adapter.dubbo.SentinelDubboProviderFilter"/>
<bean id="sentinelFilter" class="com.alibaba.csp.sentinel.adapter.dubbo.SentinelDubboConsumerFilter"/>
```

在上述配置中，我们将Sentinel的Dubbo Filter注册到Dubbo的SPI扩展机制中。

3. 配置Dubbo服务的应用名称

在Sentinel Dashboard中，您需要为每个Dubbo服务配置应用名称。应用名称是Sentinel Dashboard中用于标识Dubbo服务的唯一标识符。您可以在Dubbo的provider和consumer中添加以下配置：

```
<dubbo:application name="example-provider" />
<dubbo:application name="example-consumer" />
```

在上述配置中，我们将Dubbo服务的应用名称分别设置为`example-provider`和`example-consumer`。

4. 在Sentinel Dashboard中查看Dubbo服务的流量控制情况

在部署好Sentinel Dashboard后，您可以登录Sentinel Dashboard，并选择Dubbo资源管理页面。在该页面中，您可以查看每个Dubbo服务的调用次数、异常次数、平均响应时间和流量控制情况等。

总之，您可以通过配置Dubbo的provider规则，来对Dubbo服务进行流量控制。在Dubbo应用集群部署时，可以使用Sentinel Dashboard来统计多个节点Dubbo接口的调用次数，并进行流量控制。需要注意的是，在使用Sentinel控制Dubbo服务流量时，您需要在Dubbo的provider和consumer中添加Sentinel的Dubbo Filter，并将Filter注册到Dubbo的SPI扩展机制中。


可以看到DefaultSlotChainBuilder已经默认排列好了调用链中的节点，其实内部就类似一个拦截器链，Slot是拦截器链中的拦截器节点，每个节点的功能不同，具体功能如下：

NodeSelectorSlot：用于创建Node节点
ClusterBuilderSlot：用于创建ClusterNode节点
LogSlot：目前对于被规则限制的情况，交给了StatLogger处理，但是好像没啥效果？
StatisticSlot：用于统计当前流量通过的情况
SystemSlot：用于系统负载规则的处理
AuthoritySlot： 用于黑白名单规则的处理
FlowSlot：用于限流规则的处理
DegradeSlot：用于降级规则的处理




[源码分析 Sentinel DegradeSlot 熔断实现原理](https://mp.weixin.qq.com/s?__biz=MzIzNzgyMjYxOQ==&mid=2247484630&idx=1&sn=efeb57c897a10a5a4e11bafbe1e4840f&chksm=e8c3f322dfb47a34531a83915cf4e1b39e0b5ff8ab241766abfefd1d556a370ffaaebbfb8d22&mpshare=1&scene=1&srcid=&sharer_sharetime=1586743819190&sharer_shareid=449cff268a54795e87b6b3027424ac69&key=9a60cb5ce21186b9b7035a06063aa5ccd234e53a1d530d9602572047f7d912a318ec2cfe5c08fbf711659464358048eecf4c8ca29cc717f62ebc918476034ec482842d3d8330c927053d73a65625a9b6&ascene=1&uin=MjA3Nzg5NzE0MA%3D%3D&devicetype=Windows+10+x64&version=62090059&lang=zh_CN&exportkey=A9XtPUu1A5eReM%2F6HEcyOFE%3D&pass_ticket=VBBFCy5vinz62%2BPIWPfjaRu5DGwdCGj8U0B%2B5xzH6h3eXm634paWlaD8d2yU4NpW)


sentinal FLOW_GRADE_QPS DEGRADE_GRADE_RT区别


在Sentinel中，`FLOW_GRADE_QPS`、`DEGRADE_GRADE_RT`是两个不同的降级规则的评估维度。
`FLOW_GRADE_QPS`是基于请求的QPS进行降级的评估维度。当应用程序的请求QPS超过了设置的阈值时，降级规则会被触发，将请求进行限流或降级处理，从而保护系统的稳定性。
`DEGRADE_GRADE_RT`是基于响应时间进行降级的评估维度。当应用程序的响应时间超过了设置的阈值时，降级规则会被触发，将请求进行限流或降级处理，从而保护系统的稳定性。
在`FLOW_GRADE_QPS`规则中，我们可以设置限流阈值，即允许通过的请求QPS的最大值。而在`DEGRADE_GRADE_RT`规则中，我们可以设置响应时间的阈值，即当应用程序的响应时间超过该阈值时，降级规则将被触发。
需要注意的是，这两个评估维度是不同的，`FLOW_GRADE_QPS`是基于请求QPS进行限流或降级处理，而`DEGRADE_GRADE_RT`是基于响应时间进行限流或降级处理。在实际使用中，我们需要根据应用程序的具体情况和性能指标来设置这些规则，以保护系统的稳定性和可用性。


Sentinel的核心的Api，SphU定义资源，Tracer定义统计，ContextUtil定义了上下文。
