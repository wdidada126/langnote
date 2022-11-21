# cilium



k8s


API-aware Networking and Security

#### API-aware Networking and Security




ClusterMesh是*Cilium*的多集群实现,可以帮助*cilium*实现跨数据中心、跨VPC的多K8S集群管理

Cilium是一个纯开源软件，没有哪家公司提供商业化支持，也不是由某一公司开源，该软件用于透明地保护使用Linux容器管理平台（如Docker和Kubernetes）部署的应用程序服务之间的网络连接。

Cilium的基础是一种名为BPF的新Linux内核技术，它可以在Linux本身动态插入强大的安全可见性和控制逻辑。由于BPF在Linux内核中运行，因此可以应用和更新Cilium安全策略，而无需对应用程序代码或容器配置进行任何更改。



https://cilium.slack.com/



Cilium 是一个用于容器网络领域的开源项目，主要是面向容器而使用，用于提供并透明地保护应用程序工作负载（如应用程序容器或进程）之间的网络连接和负载均衡。
Cilium 在第 3/4 层运行，以提供传统的网络和安全服务，还在第 7 层运行，以保护现代应用协议（如 HTTP, gRPC 和 Kafka）的使用。 Cilium 被集成到常见的容器编排框架中，如 Kubernetes 和 Mesos。
Cilium 的底层基础是 BPF，Cilium 的工作模式是生成内核级别的 BPF 程序与容器直接交互。区别于为容器创建 overlay 网络，Cilium 允许每个容器分配一个 IPv6 地址（或者 IPv4 地址），使用容器标签而不是网络路由规则去完成容器间的网络隔离。它还包含创建并实施 Cilium 规则的编排系统的整合。

