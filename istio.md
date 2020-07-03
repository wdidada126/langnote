# istio



在 Istio 和 Envoy 中，对通讯协议的支持，主要体现在 HTTP/1.1 和 HTTP/2 上，这两个是 Istio / Envoy 中的一等公民。而基于 HTTP/1.1 的 REST 和基于 HTTP/2 的 gRPC，一个是目前社区最主流的通讯协议，一个是未来的主流，Google 的宠儿，CNCF 御用的 RPC 方案，这两个组成了目前 Istio 和 Envoy（乃至 CNCF 所有项目）的黄金组合。 

而我们 SOFAMesh，在第一时间就遇到和 Istio/Envoy 不同的情况，我们需要支持 REST 和 gRPC 之外的众多协议： 

SOFARPC：这是蚂蚁金服大量使用的 RPC 协议(已开源) 

HSF RPC：这是阿里集团内部大量使用的 RPC 协议(未开源) 

Dubbo RPC: 这是社区广泛使用的 RPC 协议(已开源) 
其他私有协议：在过去几个月间，我们收到需求，期望在 SOFAMesh 上运行其他 TCP 协议，大部分是私有协议

sidecar 概念 envoy是具体实现，sidercar模式



Sidecar模式

https://www.jianshu.com/p/330b00dc40d7





Init 容器：Pod 中的一种专用的容器，在应用程序容器启动之前运行，用来包含一些应用镜像中不存在的实用工具或安装脚本。



iptables：流量劫持是通过 iptables 转发实现的。
其他私有协议：在过去几个月间，我们收到需求，期望在 SOFAMesh 上运行其他 TCP 协议，大部分是私有协议