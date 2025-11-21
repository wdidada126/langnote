# cloudstack

apache的
iaas

openstack 放弃维护了

开发者 用户邮件列表

cloudstack之父 梁胜 创建了Rancher

梁胜现任Citrix System公司云平台首席技术执行官，是Citrix公司首位华人CTO。他是位标准的技术梦想家;他亦是位具有开拓精神的创业家和优秀的企业家。在加入Citrix公司之前，梁生创立了Cloud.com公司并担任首席执行官，直至2011年7月被Citrix并购。他作为Sun Microsystems公司核心技术人员，开发了JVM (Java 虚拟机)。在Sun公司之前，他作为创始人之一，创立了Teros网络安全公司(之后被Citrix公司并购)。他还担任过SEVEN网络公司的工程副总裁，以及Openwave System技术主任。梁胜毕业于中国科技大学少年班，并拥有耶鲁大学计算机博士学位。

https://cloudstack.apache.org/

https://github.com/apache/cloudstack
Java Python的

OpenStack与CloudStack
https://blog.csdn.net/lsw_dabaojian/article/details/125470431

CloudStack

CloudStack是由VMOps(后来改名为Cloud.com)在2009年首先推出的软件。Citrix在2011年收购了Cloud.com，后让其开源，并在2012年将CloudStack贡献给Apache软件基金会，成为Apache的孵化项目（项目网站 http：//cloudstack.apache.org/），同时将授权协议改为更加宽松开放和商业友好的Apache许可协议，CloudStack在2013年3月份升级为Apache的正式项目。CloudStack的目标是提供高度可用的、高度可扩展的能够进行大规模虚拟机部署和管理的开放云平台。

CloudStack由Apache CloudStack社区维护，发布周期不固定。版本发布历史可以参见 ：
Apache CloudStack Release Notes — Apache CloudStack Release Notes 4.12.0.0 documentation


据Statista称，OpenStack 是最受欢迎的开源云平台，近年来其采用率稳步增长。截至 2020 年，30% 的受访者确认他们在生产中使用 OpenStack。

现在不管国内国外，主流公有云厂商的底座，都可以说是自研的。当然各个厂商自研的程度有区别，有的是从OpenStack某个版本切出来开始自己改，有的是借用了OpenStack某些模块，有的只是借鉴了OpenStack的设计思想，毕竟OpenStack作为开源云计算系统的标杆性项目，架构设计理念虽然不及Kubernetes，但也是云计算领域的佼佼者了。

CloudStack是一个开源的公有云计算平台，它提供了一个管理界面，可以方便地管理虚拟机实例、存储、网络和数据中心。
K8S是一个开源的容器编排系统，它可以自动部署、扩展和管理容器化的应用程序。K8S提供了一组API，可以使开发人员和运维人员方便地管理容器。
两者的不同点在于，CloudStack是一个虚拟化平台，而K8S是一个容器编排系统。 CloudStack更侧重于整体的资源管理（如虚拟机、存储、网络），而K8S更侧重于对容器的编排和管理。

cloudstack支持k8s吗


如何融合OpenStack和Kubernetes，构建新一代私有云和容器云？
在8月16-17日由OpenStack基金会举办的国内极具影响力的开源盛会2020 OpenInfra Days China大会上，易捷行云EasyStack容器架构师、产品线负责人王后明带来《Kubernetes和OpenStack 1+1 大于 2 构建新一代私有云和容器云》主题分享，议题结合 3 年时间服务了几百家企业客户的最佳实践，分享如何结合两者的优势，构建可进化的新一代私有云、如何充分利用 OpenStack 的云基础设施能力，给用户提供Kubernetes容器云能力。

OpenStack 作为私有云事实标准，具备强大的基础设施管理能力；Kubernetes 作为数据中心的统一控制平面，具备强大的应用管理能力。易捷行云在构建新一代私有云和新一代容器云的时候，做到了Kubernetes和OpenStack 1+1 大于 2，每一套新一代私有云ECS天生就是一套Kubernetes集群，带给客户全新的体验，目前，易捷行云新一代私有云ECS已服务超1000家国内外大中型企业，部署规模数万节点。

1、 统一架构，同时支撑控制平面和云原生业务
使用Kubernetes统一IaaS 平台和 PaaS 平台基础架构。Kubernetes 既支撑云平台控制平面服务，又提供用户可全生命周期管理的自建 Kubernetes 容器集群，支撑用户云原生业务。
易捷行云构建的主管集群（EOS，EasyStack Orchestration Service），既是控制平面管理集群，可运行于裸机服务器，编排管理控制平面提供云基础设施，又是用户业务集群(EKS， EasyStack Kubernetes Service)的元集群，可运行于云主机，帮助用户充分利用云基础设施能力。
2、 基于Kubernetes实现新一代私有云的可进化
易捷行云新一代私有云EasyStack ECS基于安全、稳定、高效的新一代数据中心分布式云操作系统，通过一体化、场景化的设计理念将平台与服务相分离，实现了全平台的可进化能力，包括产品形态可进化、服务能力可进化、支撑场景可进化。
易捷行云新一代私有云ECS所有控制平面服务云原生化，并持续滚动更新，让进化过程平滑无感，用户业务不中断。基于可进化的核心特性，私有云可以进化出容器云能力，随客户业务形态的发展而不断变化。
3、 针对异构CPU 架构打造多云异构管理平台
随着国产化大趋势以及客户对多云的接受程度越来越高，客户IT资源中越来越多的应用会同时运行在x86和non-x86平台。不同架构资源池，需要针对性优化、独立运行。易捷行云应用Kubernetes以统一权限体系接入云平台，复用镜像仓库、稳定可靠高性能的存储等云基础设施能力，统一分发、调度应用，实现对异构CPU架构的统一管理。
4、 全平面编排实现IaaS 平台和容器的统一管理
实现私有云和容器云之间的统一管理和不同负载之间的网络直联，是当前客户的一个迫切需求。而易捷行云使用统一的声明式管理方式，将虚拟机、裸金属等服务，以 CRD+ Operator 模式接入 Kubernetes 生态，让虚拟机/裸金属也能云原生化，充分利用云基础设施提供的全平面统一网络方案，实现不同租户VPC 隔离、子网内二层直通。
之所以能够实现对不同业务负载实现统一管理，其背后核心是利用了Kubernetes的声明式(Declarative) API + 控制器的原理。Kubernetes的API是声明式而不是命令式的，这使得Kubernetes可以非常便捷接近不同业务生态系统，以 CRD+ Operator 模式同时打通和统一南北向和东西向接口：南向统一接入规范、北向统一集成接口，东西向则充分复用 list-watch 机制，和Kubernetes 核心资源和控制逻辑打通。
5、 安全增强，将云主机级安全隔离机制引入容器
通过将云主机级安全隔离机制引入容器, 使得新一代容器云具备容器的便捷和云主机级别的安全隔离能力，提供极致的容器体验。其核心是深度优化的云操作系统和虚拟化组件，不再需要云主机内部嵌套容器，提升性能减少损耗。
6、 OpenStack云基础设施为 Kubernetes 提供统一权限体系、统一网络、统一存储
Kubernetes 发展需要融合OpenStack云基础设施能力。比如，依托 OpenStack Neutron 可以为Kubernetes提供 SDN 网络方案，使用Neutron统一管理容器平台和OpenStack平台的网络，实现容器与容器之间，以及容器与VM、裸机之间的直连，还可将Neutron的高级特性引入容器网络中，诸如安全组、FloatingIP、QoS、LBaaS、FWaaS、VPNaaS等。此外，还可依托OpenStack Cinder/Manila 提供存储方案，依托OpenStack Keystone实现统一权限和租户间安全隔离。
Kubernetes和OpenStack两者优势互补，充分融合并发挥各自优势，可形成 1+1>2的效果。易捷行云在建设新一代私有云和容器云的时候，充分融合了两者优势，利用Kubernetes 统一IaaS 平台和 PaaS 平台基础架构，将虚拟机、裸金属等服务，以CRD+ Operator 模式接入 Kubernetes 生态，让虚拟机/裸金属也能云原生化；利用OpenStack为Kubernetes提供统一权限体系、统一网络方案、统一存储。总结来说，OpenStack云基础设施需要融入 Kubernetes能力，Kubernetes 也需要融合OpenStack云基础设施，两者1+1实现大于2的效果。
OpenStack进入中国十年，已然成为开源基础设施即服务的标准。云计算技术的快速演变升级涌现出大量的新需求，且行业需求不断细化，使得开源社区之间的技术协作与集成测试已不可或缺。易捷行云一直是中国开源云计算的领导者，积极参与国际开源社区并贡献核心代码，不仅是OpenStack基金会黄金会员，Ceph基金会创始会员，CNCF、OCF、Linux基金会会员，拥有私有云事实技术标准OpenStack全球技术委员会亚太国家中唯一委员；同时在kubernetes、Ceph、OpenStack的核心代码贡献中多次排名全球前十名。


