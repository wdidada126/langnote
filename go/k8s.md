# k8s


[美团点评Kubernetes集群管理实践](https://blog.csdn.net/MeituanTech/article/details/100078911)



[awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes)


总体来说，Rancher和k8s都是用来作为容器的调度与编排系统。但是rancher不仅能够管理应用容器，更重要的一点是能够管理k8s集群。Rancher2.x底层基于k8s调度引擎，通过Rancher的封装，用户可以在不熟悉k8s概念的情况下轻松的通过Rancher来部署容器到k8s集群当中。为实现上述的功能，Rancher自身提供了一套完整的用于管理k8s的组件，包括Rancher API Server, Cluster Controller, Cluster Agent, Node Agent等等。组件相互协作使得Rancher能够掌控每个k8s集群，从而将多集群的管理和使用整合在统一的Rancher平台中。Rancher增强了一些k8s的功能，并提供了面向用户友好的使用方式。
Rancher有分为v1和v2版本，都是提供容器调度与编排，不同之处在于在k8s盛行之前有许多人都搞过容器编排，所以rancher v1上会有几种不同的编排模式，例如cattle ,swarm,kubernetes。从这里可以看出Rahcner v1时代，它给自己的定位是各种编排工具的上层，也就是k8s的上层，然后你再通过它去管理k8s。因为k8s后来发展得势不可挡，所以Rancher  v2应运而生，移除了其他类型的编排工具，只剩下k8s。

