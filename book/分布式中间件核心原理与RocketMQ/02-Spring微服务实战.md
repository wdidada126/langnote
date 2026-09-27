# 第 2 章　Spring 微服务实战

> 原书第 2 章是**工程基座**：先讲 Spring Boot（快速建项目、定时任务），再讲 Spring Cloud
> （以电商系统为例搭建微服务骨架）。这是后面所有实战（RocketMQ 整合、容器部署、电商案例）的底座。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 Spring Boot 实战 | 是什么、创建项目、定时访问数据库 | Spring Boot 用自动装配与起步依赖消灭样板代码 |
| 2.1.1 什么是 Spring Boot | 约定优于配置、内嵌容器 | 微服务单体的标准外壳 |
| 2.1.2 创建 Spring Boot 项目 | start.spring.io / IDE 脚手架 | 一个 `main` 方法即可启动 |
| 2.1.3 定时访问数据库实战 | `@Scheduled` + JPA/MyBatis | 演示 Boot 工程的最小闭环 |
| 2.2 Spring Cloud 实战 | 是什么、电商架构、搭建电商项目 | Cloud 在 Boot 之上提供注册/调用/容错等治理 |
| 2.2.1 什么是 Spring Cloud | 一套微服务规范 + 多实现 | 解决「服务在哪、怎么调、挂了怎么办」 |
| 2.2.2 从电商系统看基本架构 | 订单/库存/用户等服务 + 注册中心 | 拆分后的协作拓扑 |
| 2.2.3 搭建 Spring Cloud 电商项目 | 多模块、Feign 调用、注册中心 | 跑通服务间调用 |
| 2.3 小结 | 收束基座章 | 进入第 3 章容器部署 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）本章代码偏脚手架，重点理解
「Boot 解决单体便利、Cloud 解决多体协作」的分层。

### 2.1.3 定时任务（教学示意）

```java
// 教学示意，不参与构建：Spring Boot 定时访问数据库
@SpringBootApplication
@EnableScheduling
public class DemoApp {
    public static void main(String[] args) { SpringApplication.run(DemoApp.class, args); }
}

@Component
public class DbPoller {
    @Autowired OrderMapper mapper;
    @Scheduled(fixedDelay = 5000)   // 每 5 秒
    public void poll() { mapper.countPending(); }
}
```

### 2.2.2–2.2.3 电商微服务骨架（教学示意）

```yaml
# 教学示意，不参与构建：订单服务注册到 Nacos（2026 主流，原书多用 Eureka/Consul 思路）
spring:
  application:
    name: order-service
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
```

```java
// 教学示意，不参与构建：用 OpenFeign 调用户服务
@FeignClient(name = "user-service")
public interface UserClient {
    @GetMapping("/users/{id}") UserDTO get(@PathVariable("id") Long id);
}
```

> 注意：原书 2023 年示例多以 Spring Cloud Netflix / Consul 思路写，2026 年实际工程几乎一律
> 用 **Spring Cloud Alibaba（Nacos + OpenFeign/Sentinel）**，详见本章「版本演进」。

## 版本演进

- **本书基于 Spring Boot 2.x / Spring Cloud 202x 系**（具体小版本以纸书为准，未能逐字核实）。
- **🔧 2026 视角：Netflix 套件退役**。Eureka、Hystrix、Zuul、Ribbon 早已进入维护/停止状态；
  注册发现用 **Nacos / Eureka 替代 Consul 居多**，熔断限流用 **Sentinel**，网关用 **Spring Cloud Gateway**
  （替代 Zuul）。新项目基本落在 **Spring Cloud Alibaba** 全家桶。
- **🔧 2026 视角：Spring Boot 3.x + Jakarta 命名空间**（javax → jakarta）已成主流，
  且要求 Java 17+；GraalVM 原生镜像（Native Image）开始进入生产，启动毫秒级、内存更省。
- **🔧 2026 视角：云原生接管部分治理能力**。Kubernetes Service + Ingress 可替代部分注册/网关职责，
  服务网格（Istio/Linkerd）把熔断、重试、mTLS 下沉到 sidecar——与 Spring Cloud 在应用层的能力重叠。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Spring 官方文档（spring.io/projects/spring-boot） | spring.io | Boot 自动装配、起步依赖权威出处 |
| Spring Cloud 官方文档（spring.io/projects/spring-cloud） | spring.io | Cloud 抽象与各组件权威出处 |
| Spring Cloud Alibaba 文档（github.com/alibaba/spring-cloud-alibaba） | github | Nacos/Sentinel/Dubbo 整合权威出处 |
| Fowler《Microservices》 | 2014 | 微服务拆分与团队对齐（康威定律） |

> 第 2 章是工程实战章，原书不引论文；上表补官方文档与微服务定义出处。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `spring-projects/spring-boot` | 微服务基座 | 81511 |
| `alibaba/spring-cloud-alibaba` | 2026 主流微服务套件 | 29179 |
| `alibaba/nacos` | 注册 + 配置中心 | 33419 |
| `apache/dubbo` | RPC（常配合 Cloud Alibaba） | 41579 |

- **趋势**：Spring Boot 3 / Java 17 / Jakarta 普及；Native Image 降低容器冷启动；
  微服务治理「双轨」——要么用 Spring Cloud Alibaba 在应用层做，要么用 K8s + Service Mesh 在基础设施层做。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Spring Boot = Spring Cloud」 | Boot 是单体便利，Cloud 是协作治理，两者分层 |
| 2 | 「微服务拆得越细越好」 | 拆细增加网络调用与运维成本，按业务边界拆 |
| 3 | 「定时任务能替代消息队列」 | 定时轮询有延迟与空转；实时异步应交给 MQ（见第 4、8 章） |
| 4 | 🔧 本书按旧 Cloud 套件写 | 2026 应明确 Nacos/Sentinel/Gateway + Alibaba 为主流 |
| 5 | 🔧 本书未提 Boot 3/Jakarta/原生镜像 | 2026 新项目默认 Java 17+ 与 Native Image |

## 与其他章 / 其他书的联系

- **本书内**：
  - 2.2 电商骨架 → 第 12 章电商实战（直接用 Spring Cloud Alibaba + Nacos + Dubbo）；
  - 2.1 的 Java 工程基座 → 第 3 章容器打包、第 7 章 Spring Boot 整合 RocketMQ；
  - 2.2 服务调用 → 第 10 章分布式事务（跨服务一致性）、第 11 章分布式锁（跨服务并发）。
- 跨书：可对照 [../分布式中间件技术实战/05-消息中间件RabbitMQ.md](../分布式中间件技术实战/05-消息中间件RabbitMQ.md)
  中 Spring Boot 整合 MQ 的写法，与本书第 7 章 RocketMQ 整合互参。
