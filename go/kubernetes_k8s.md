# k8s kubernetes

Kubernetes（简称K8s）是一个开源的容器编排系统，用于自动部署、扩展和管理容器化应用程序。它提供了一系列功能，使容器化应用的部署和管理变得更加高效和可靠。以下是Kubernetes的一些主要功能：

自动装箱：基于容器化应用的资源需求和其他约束，自动决定容器在集群中的运行位置。
自我修复：在容器出现故障时，自动重启或替换容器，保证应用的可用性。
水平扩展：根据应用的负载情况，自动增减容器副本数量，以满足用户需求。
服务发现：为容器化的服务提供自动发现机制，使其他服务可以轻松找到并访问它们。
滚动更新：在更新应用时，通过逐步替换容器的方式，确保更新过程中服务的连续性。
版本回退：在更新出现问题时，可以迅速回退到之前的版本，降低故障影响。
密钥和配置管理：为容器化应用提供安全的密钥和配置信息管理，保证应用的安全性。
存储编排：为容器化应用提供灵活的存储解决方案，满足不同的存储需求。
数据卷共享：在Pod中的容器之间共享数据卷，方便数据共享和持久化。
应用程序健康检查：通过定期检查容器的状态，及时发现并处理潜在的问题。
弹性伸缩：根据应用的负载情况，自动调整容器副本数量，以充分利用资源。
负载均衡：为多个容器副本分配一个私有的集群IP地址，并通过负载均衡器转发请求到后端容器，提高应用的性能和可用性。
服务编排：通过描述文件部署和管理服务，简化应用部署过程。
资源监控：收集集群节点的资源数据，如CPU、内存和磁盘使用情况等，以便进行监控和性能优化。
提供认证和授权：支持角色访问控制（RBAC）等策略，保证集群的安全性。
这些功能使Kubernetes成为了一个强大且灵活的容器编排系统，广泛应用于云原生应用的部署和管理。

master
node. 对分两类

master有4个节点etcd、定时、restful api、控制

Kubernetes权威指南：从Docker到Kubernetes实践全接触（第4版）
Kubernetes in Action, Second Edition

https://www.haolizi.net/example/view_39168.html

安心做业务开发
k8s偏向于运维架构

yum centos 7安装

如果说docker中的tomcat挂掉了，自动重启一台
如果一个os节点挂掉

阿里巴巴用k8s

k8s总架构图
k8s_architect.jfif
https://blog.csdn.net/huwh_/article/details/71308171

https://www.jianshu.com/p/9e74775fb683

https://github.com/istio/istio
istio
service mesh
https://zhuanlan.zhihu.com/p/54123996

- Kubernetes权威指南：从Docker到Kubernetes实践全接触（第4版）
- Kubernetes in Action, Second Edition

[美团点评Kubernetes集群管理实践](https://blog.csdn.net/MeituanTech/article/details/100078911)

[awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes)

总体来说，Rancher和k8s都是用来作为容器的调度与编排系统。但是rancher不仅能够管理应用容器，更重要的一点是能够管理k8s集群。Rancher2.x底层基于k8s调度引擎，通过Rancher的封装，用户可以在不熟悉k8s概念的情况下轻松的通过Rancher来部署容器到k8s集群当中。为实现上述的功能，Rancher自身提供了一套完整的用于管理k8s的组件，包括Rancher API Server, Cluster Controller, Cluster Agent, Node Agent等等。组件相互协作使得Rancher能够掌控每个k8s集群，从而将多集群的管理和使用整合在统一的Rancher平台中。Rancher增强了一些k8s的功能，并提供了面向用户友好的使用方式。
Rancher有分为v1和v2版本，都是提供容器调度与编排，不同之处在于在k8s盛行之前有许多人都搞过容器编排，所以rancher v1上会有几种不同的编排模式，例如cattle ,swarm,kubernetes。从这里可以看出Rahcner v1时代，它给自己的定位是各种编排工具的上层，也就是k8s的上层，然后你再通过它去管理k8s。因为k8s后来发展得势不可挡，所以Rancher  v2应运而生，移除了其他类型的编排工具，只剩下k8s。

k8s生产环境部署

k8s书籍

源码编译

Istio是独立于平台的，旨在运行在各种环境中，包括跨云、内部部署、Kubernetes、Mesos等。您可以在Kubernetes上部署Istio或具有Consul的Nomad上部署。