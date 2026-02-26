# libpod
libpod 库的代码直接包含在 Podman 的源代码仓库中，两者位于同一个代码库。

1. 仓库地址与结构
libpod 不是一个独立的项目仓库，而是 Podman 项目中的一个核心子目录（/libpod）。
•   GitHub 地址：https://github.com/containers/podman
•   Go Module 路径：github.com/containers/podman/v5/libpod

2. 为什么这样做？
在 Podman 的架构设计中，libpod 是 Podman 的“内核”（Kernel）或运行时引擎。Podman 的 CLI 命令行工具实际上是调用 libpod 库的 API 来实现所有功能的。将它们放在一起便于代码管理和同步更新。

3. 如何引用代码？
如果你需要在代码中直接调用 libpod 的接口（例如实现自定义容器管理逻辑），你需要在 Go 项目中导入该路径：
import "github.com/containers/podman/v5/libpod"

注意：官方文档明确指出，libpod的API并不稳定，随时可能在补丁版本中发生变动。如果需要一个稳定的接口，建议使用Podman提供的HTTP API服务。

libpod 是 Podman 的核心底层库，它遵循“微服务化”的设计理念，将容器引擎拆解为多个独立、可复用的 Go 语言库。它负责管理容器、镜像、存储、网络以及最重要的 Pod 概念。
1. 核心架构：模块化设计
libpod 并不“大包大揽”，而是将功能解耦，通过组合其他优秀库来工作。其核心依赖关系如下：

模块 功能 对应库 说明
容器运行时 运行 OCI 容器 runc (或 crun) 实际执行容器进程的底层工具
镜像管理 拉取、推送、转换镜像 containers/image 处理镜像格式（Docker/OCI）和注册表交互
存储管理 管理镜像层、容器层 containers/storage 使用 OverlayFS 或 VFS 管理文件系统
网络管理 配置容器网络 CNI (Container Network Interface) 通过插件（如 bridge, macvlan）管理网络命名空间
构建工具 构建 OCI 镜像 Buildah 提供无守护进程的镜像构建能力
Pod 管理 管理容器组 libpod 自身 实现类似 Kubernetes 的 Pod 概念，共享网络/存储命名空间

2. 与 Docker 架构的本质区别
Docker 采用 Client-Server 架构（守护进程模式），而 libpod 是 Fork-Exec 架构（无守护进程模式）。
•   Docker：docker run 命令发送请求给 dockerd 守护进程，由守护进程创建并管理容器。守护进程拥有所有容器的父进程。
•   libpod (Podman)：podman run 命令直接 fork/exec 出 conmon 进程，该进程再启动 runc 运行容器。容器是系统的直接子进程，这使其天然支持 systemd 管理，且无单点故障风险。

3. 核心特性
•   支持 Pod：是唯一原生支持 Kubernetes Pod 概念的容器库，可以将多个容器放入同一个 Pod 中，共享网络和存储命名空间。
•   无守护进程 (Daemonless)：无需运行后台服务，更安全，资源消耗更低。
•   Rootless 容器：普通用户即可运行容器，无需 root 权限，极大提升了安全性。

4. 在生态中的位置
libpod 是 CRI-O 的底层依赖。Kubernetes 的 CRI-O 运行时使用 libpod 来管理 Pod 和容器的生命周期，这保证了开发环境（Podman）和生产环境（Kubernetes）的一致性。
总结：libpod 是一个“胶水库”，它通过组合 containers/* 系列库和 OCI 工具，构建了一个专注于 Pod 管理 和 无守护进程运行 的现代容器引擎库。