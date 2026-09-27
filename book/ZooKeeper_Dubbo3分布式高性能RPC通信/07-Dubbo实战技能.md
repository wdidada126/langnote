# 第 7 章　Dubbo 实战技能

> 原书第 7 章是 Dubbo 的「动手核心」：从多模块 Maven 工程（父模块/my-api）起步，
> 用 ZooKeeper 注册中心打通一次 RPC 调用，再逐个演练直连提供者、隐式参数、服务分组、
> 多版本、启动时检查、令牌验证、超时和线程池，最后引入 Nacos 注册中心并演示「结合 ZK 集群」。
> 这是把第 6 章概念变成可运行 DEMO 的一章。2026 视角要补：**应用级服务发现、Triple、
> Spring Boot 自动装配、以及 Nacos 与 ZK 的取舍**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 父模块 my-parent | Maven 聚合/依赖管理 | 统一版本，子模块继承 |
| 7.2 my-api 模块 | 共享接口契约 | 接口先行，provider/consumer 共依赖 |
| 7.3 ZK 注册中心 RPC | 完整打通一次调用 | 注册中心只管地址，调用直连 |
| 7.4 直连提供者 | 绕过注册中心点对点 | 调试/测试用，生产不推荐 |
| 7.5 隐式参数 | Attachment 透传 | 链路传参不走接口签名 |
| 7.6 服务分组 | group 隔离同接口多实现 | 灰度/环境隔离手段 |
| 7.7 多版本 | version 路由 | 接口不兼容升级的平滑过渡 |
| 7.8 启动时检查 | check 属性 | 启动即校验依赖是否就绪 |
| 7.9 令牌验证 | token 防冒充 | 简单的 provider 接入鉴权 |
| 7.10 超时和线程池 | timeout / 线程池大小 | 性能与雪崩防护的关键旋钮 |
| 7.11 Nacos 介绍 / 7.12 单机 / 7.13 注册 RPC | 替代注册中心 | Nacos 集注册+配置，AP/CP 可选 |
| 7.14 结合 ZK 注册中心集群 | 多注册中心 | 多注册中心并存 |

## 核心精讲

（以下为教学性梳理，Java/XML 均**教学示意，不参与构建**。） 

### 7.2 / 7.3 接口先行 + 一次 RPC 打通

```java
// 教学示意，不参与构建：共享 API 模块（my-api）
public interface OrderService { String create(String req); }

// Provider 端
@DubboService
public class OrderServiceImpl implements OrderService {
    public String create(String req) { return "ok:" + req; }
}

// Consumer 端
@DubboReference
private OrderService orderService;   // 由注册中心注入远端代理
// 调用 orderService.create(...) 即发起一次 RPC（直连 Provider，不经 Registry）
```

> 工程要点：**API 模块独立**，provider/consumer 都依赖它——契约先行，序列化靠共享接口。

### 7.6 服务分组 / 7.7 多版本（灰度三板斧之二）

```text
# 教学示意，不参与构建
group="gray"   -> 同一接口的不同实现隔离（如新旧算法并存）
version="1.0"  -> 同一接口的不兼容版本路由（version="2.0" 平滑切换）
组合使用：可按 group+version 精确路由，做灰度发布
```

### 7.8 启动时检查（check）

- `check="true"`（默认）：Consumer 启动时若找不到 Provider 则**启动失败**——利于早暴露问题；
- `check="false"`：启动不校验，运行时再发现——利于 Consumer 先于 Provider 启动的场景。

### 7.9 令牌验证（token）

- Provider 配置 `token="xxx"`，Consumer 必须带匹配 token 才能调用，**防止未授权服务冒充调用**。
- 属轻量鉴权，非完整安全方案（生产还需 TLS + 接入网关/鉴权中心）。

### 7.10 超时与线程池（防雪崩旋钮）

```text
# 教学示意，不参与构建：超时与线程池的意义
timeout=1000ms   -> 调用超过 1s 即中断，避免线程被慢调用长期占用
线程池大小         -> 决定并发处理能力；过小则拒绝，过大则上下文切换/资源耗尽
二者配合：超时不当 + 线程池打满 = 上游调用线程连环阻塞 = 雪崩
```

> 这是本书离「高可用」最近的一节，与第 8 章集群容错形成组合拳。

### 7.11–7.14 Nacos 与多注册中心

- Nacos 把**注册中心 + 配置中心**合一，且支持 AP/CP 模式切换（见 05.6 CAP）；
- 7.14「结合 ZK 注册中心集群」演示 Dubbo 支持**多注册中心并存**，是迁移/双写场景的实用能力。

## 版本演进

- **本书无第二版**；本节写 2022 年口径 → 2026 年视角的变化。
- **应用级服务发现（本书缺口）**：本书 7.3 用 ZK 临时节点做**接口级注册**（每个接口一个 znode），
  海量实例下写放大严重。Dubbo 3 改用**应用级注册**（应用为单位的元数据 + 接口映射表），
  大幅降低注册中心压力。本书未覆盖。
- **Triple 协议（本书缺口）**：本书 RPC 调用默认走 Dubbo 私有协议；Dubbo 3 推荐 Triple
  （HTTP/2+Protobuf），跨语言、流式。本书 7.3 的 DEMO 未演示 Triple。
- **Spring Boot 自动装配**：本书用传统多模块 + 注解/XML，2026 年生产几乎都用
  `spring-boot-starter-dubbo` + 配置化，极大简化 7.1/7.2 的样板。
- **配置中心分离**：Dubbo 2.7+ 把配置/元数据从注册中心拆出（Nacos/ZK 专用），本书把注册中心一家独大。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Apache Dubbo 官方文档（Service Group/Version/Token/Timeout） | dubbo.apache.org | 分组/版本/令牌/超时的权威语义（版本较多） |
| Apache Dubbo 官方文档（Service Discovery / Triple） | dubbo.apache.org | 应用级服务发现、Triple 协议（本书未覆盖，必补） |
| gRPC 官方文档 | grpc.io | Triple 的协议近亲，跨语言契约基础 |

## 近年研究与工业界开源实践（2015–2026）

- **apache/dubbo（41579★，2026-09 实测）**：3.x 主线，应用级服务发现、Triple 已生产可用。
- **alibaba/nacos（33419★）**：本书 7.11–7.14 引入，注册+配置合一，国产生态主流。
- **apache/zookeeper（12811★）**：Dubbo 2.x 默认注册中心，本书 7.3 范式。
- **spring-cloud-alibaba**：Dubbo + Spring Boot/Cloud 整合的事实标准（本书未覆盖）。
- **grpc/grpc-java（12072★）**：Triple 协议对照物。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「直连提供者可用于生产」 | 直连仅调试/测试，绕过注册发现失去弹性 |
| 2 | 「启动时 check 默认关」 | 默认 `check=true`，找不到依赖会启动失败（有利早暴露） |
| 3 | 「token 等于完整安全」 | token 是轻量防冒充，非完整鉴权（仍需 TLS+网关） |
| 4 | 「超时设越大越稳」 | 过大易线程堆积雪崩，应按 P99 设合理上限 |
| 5 | 🔧 接口级注册写放大 | Dubbo 3 改用应用级服务发现，本书仍以 ZK 接口级 znode 为范式 |
| 6 | 🔧 未演示 Triple 协议 | Dubbo 3 推荐 Triple，本书 DEMO 仍是私有协议 |
| 7 | 🔧 未用 Spring Boot starter | 2026 生产用 starter 自动装配，本书仍是传统多模块样板 |
| 8 | 🔧 未提配置中心分离 | Dubbo 2.7+ 配置/元数据从注册中心拆出，本书未体现 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 7.3 注册 → [01-ZooKeeper核心理论.md](01-ZooKeeper核心理论.md)（ZK 注册支撑）、[06-Dubbo介绍.md](06-Dubbo介绍.md)（注册发现必要性）；
  - 7.10 超时 → [08-Dubbo高级技能.md](08-Dubbo高级技能.md)（集群容错与负载均衡组合）；
  - 7.11 Nacos → [05-软件技术架构的发展.md](05-软件技术架构的发展.md)（CAP 取舍的落地）。
- 跨书/跨项目：补 Triple 与应用级服务发现，需对照 Dubbo 3 官方文档与 gRPC 资料（本书缺口）。
