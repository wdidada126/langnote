# cncf
云原生计算基金会 (Cloud Native Computing Foundation, CNCF)
- containerd
- CoreDNS
- Envoy
- etcd
- Fluentd
- Harbor
- Helm
- Jaeger
- Kubernetes
- Open Policy Agent
- Prometheus
- Rook
- TiKV
- TUF
- Vitess

Sandbox projects
Artifact Hub
Athenz
Backstage
BFE
Brigade
cert-manager
Chaos Mesh
ChubaoFS
Cloud Custodian
Cloud Development Kit for Kubernetes (cdk8s)
CNI-Genie
Crossplane
Curiefense
Dex
Distribution
Flux
GitOps Working Group
in-toto
k3s
k8dash
KEDA
Keptn
Keylime
Kube-OVN
KubeVirt
KUDO
Kuma
Kyverno
LitmusChaos
Longhorn
metal3-io
Network Service Mesh
Open Service Mesh
OpenEBS
OpenKruise
OpenMetrics
OpenTelemetry
OpenYurt
Parsec
Piraeus-Datastore
Porter
Pravega
SchemaHero
Serverless Workflow Specification
Service Mesh Interface
Strimzi
Telepresence
Tinkerbell
Tremor
Virtual Kubelet
Volcano


- brpc

asf

linux基金会

鉴于 Apache 基金会、Linux 基金会和云原生计算基金会 (CNCF) 是全球最活跃的开源组织，它们每年新增的孵化或托管项目数量众多。要列出 2024 年和 2025 年的完整列表比较困难，因为项目加入的时间点分散，且基金会的新项目通常通过不同阶段（如 Apache 的 Incubator、CNCF 的 Sandbox）逐步推进。

以下是根据公开信息和新闻稿整理的，在 2024 年和 2025 年新加入或毕业/升级的知名项目的示例和趋势。

### 1. Apache 开源基金会 (Apache Software Foundation, ASF)

Apache 项目必须经过 Incubator（孵化器）阶段。以下是在 2024-2025 年间进入孵化或从孵化器毕业的项目：

| 阶段 | 项目名称 | 领域/简介 | 时间（示例） |
| :--- | :--- | :--- | :--- |
| 新进入孵化器 | *需要查阅 ASF 孵化器邮件列表或官方公告获取最新列表* | *项目数量较多，且持续加入中。* | *N/A (持续加入)* |
| 从孵化器毕业 | Apache HertzBeat | 一款易于使用、无 Agent 的开源实时监控系统，兼容 Prometheus。 | 2025 年 8 月毕业 |
| 从孵化器毕业 | Apache Gravitino | 一款高性能、分布式、且兼容性强的元数据和数据湖治理框架。 | 2025 年 6 月毕业 |
| 从孵化器毕业 | Apache StormCrawler | 一套用于构建可扩展 Web 爬虫的开源工具。 | 2025 年 6 月毕业 |
| 从孵化器毕业 | Apache StreamPark | 一款基于 Apache Flink 和 Apache Spark 的流批统一计算平台。 | 2025 年 1 月毕业 |
| 已孵化项目 | Apache Kvrocks | 分布式 Key-Value NoSQL 数据库，兼容 Redis 协议。 | 2024-2025 年持续活跃 |

趋势： ASF 的新项目主要集中在大数据生态系统、AI/数据基础设施、分布式存储和实时数据处理领域。

### 2. 云原生计算基金会 (Cloud Native Computing Foundation, CNCF)

CNCF 的项目孵化流程分为三个阶段：Sandbox（沙箱） $\to$ Incubating（孵化中） $\to$ Graduated（已毕业）。新加入的项目首先进入 Sandbox。

#### 2024-2025 年部分新加入 Sandbox 或升级的项目：

| 阶段 | 项目名称 | 领域/简介 | 时间（示例） |
| :--- | :--- | :--- | :--- |
| 新加入 Sandbox | Kube-burner | CI/CD 性能测试工具，用于大规模 Kubernetes 集群的压力测试和负载生成。 | 2024 年底 |
| 新加入 Sandbox | Kuasar | 高效的容器运行时，支持 MicroVM、WASM 等多种沙箱技术，提供全场景容器解决方案。 | 2024 年底 |
| 新加入 Sandbox | K8sGPT | 提高可观测性的工具，利用 AI/LLM 诊断和解释 Kubernetes 集群的问题。 | 2024 年底 |
| 新加入 Sandbox | Easegress | 高性能、可扩展的云原生流量编排系统/API 网关。 | 2024 年底 |
| 升级至 Incubating | WasmCloud | 基于 WebAssembly 的分布式应用运行时，专注于分布式、安全和可移植的微服务。 | 2024 年底 |
| 升级至 Graduated | Dapr | 分布式应用运行时，用于简化微服务构建。 | 2 024 年升级 |
| 升级至 Graduated | cert-manager | 自动化证书管理工具。 | 2024 年升级 |

趋势： CNCF 的新项目强烈聚焦于：AI/MLOps in Cloud Native (如 K8sGPT)、安全和合规性、边缘计算/WebAssembly (WASM)、以及下一代容器运行时。

### 3. Linux 开源基金会 (Linux Foundation, LF)

Linux 基金会是一个伞形组织，旗下管理着数百个子基金会和项目（如 CNCF、Hyperledger、LF AI & Data 等）。因此，“新孵化项目”通常指的是新成立的子基金会或重要的新顶级项目。

| 类型 | 项目名称/基金会 | 领域/简介 | 时间（示例） |
| :--- | :--- | :--- | :--- |
| 新基金会/项目 | React Foundation | 旨在围绕流行的 React 框架创建一个中立的协作机构。 | 2025 年 10 月 (意向宣布) |
| 新基金会/项目 | LF Decentralized Trust | 一个伞形项目，整合了 Hyperledger、Trust Over IP 等生态系统，专注于去中心化信任和 Web3 领域。 | 2024 年 10 月 |
| 报告趋势 | AI/ML 领域项目 | LF AI & Data 基金会持续快速增长，托管了大量 AI 领域的开源项目，如 OpenMMLab、PyTorch 等。 | 2024-2025 年 |

趋势： Linux 基金会专注于AI/ML 基础设施、去中心化技术（Web3）、关键技术人才和技术标准的建设。

除了您提到的 Apache 软件基金会 (ASF)、Linux 基金会 (LF) 及其子基金会 云原生计算基金会 (CNCF) 之外，全球还有许多其他重要的开源组织和基金会，它们在不同的技术领域发挥着关键作用。

以下是一些类似的主要开源组织：

### 1. 软件开发和技术生态系统类

这类基金会通常专注于特定的编程语言、技术栈或开发者工具。

| 基金会名称 (英文/中文) | 重点领域/简介 | 知名项目举例 |
| :--- | :--- | :--- |
| Eclipse Foundation | 专注于 IDE（集成开发环境）、Java 技术、物联网 (IoT) 和规范。它是一个独立的非营利性机构。 | Eclipse IDE, Jakarta EE (原 Java EE), Eclipse Mosquitto (IoT) |
| Python Software Foundation (PSF) | 致力于推广和保护 Python 编程语言及其社区。 | Python 语言本身, PyPI (Python 包索引) |
| Mozilla Foundation | 致力于开放互联网，并保护用户在线隐私和安全。其商业子公司 Mozilla Corporation 负责开发 Firefox 浏览器。 | Firefox 浏览器, Rust 语言 (虽然 Rust 现在独立于一个基金会，但其起源于 Mozilla) |
| OpenJS Foundation | 专注于 JavaScript 和 Web 生态系统中的关键项目。 | Node.js, jQuery, Express.js |

### 2. 中国本土的开源基金会

为推动中国开源生态发展而成立的非营利组织。

| 基金会名称 (英文/中文) | 重点领域/简介 | 知名项目举例 |
| :--- | :--- | :--- |
| 开放原子开源基金会 (OpenAtom Foundation) | 中国首家开源基金会，专注于促进开源软件的推广、法务协助、资金支持和开放治理。 | OpenHarmony, OpenCloudOS, TKEStack 等中国本土重要项目。 |

### 3. Linux 基金会旗下的主要子基金会

虽然它们隶属于 Linux 基金会，但其规模和影响力都非常大，通常被视为独立的技术生态。

| 子基金会名称 (英文) | 重点领域/简介 | 知名项目举例 |
| :--- | :--- | :--- |
| LF AI & Data Foundation | 专注于人工智能 (AI)、机器学习 (ML) 和数据领域。 | PyTorch, Acumos, OpenMMLab |
| Hyperledger Foundation | 专注于跨行业的开源区块链技术。 | Hyperledger Fabric, Hyperledger Besu, Hyperledger Indy |
| Open Infrastructure Foundation (OpenInfra Foundation) | 专注于开放基础设施技术，如云计算、边缘计算和容器。 | OpenStack, Kata Containers, StarlingX |
| Zephyr Project | 专注于物联网 (IoT) 设备的实时操作系统 (RTOS)。 | Zephyr RTOS |

### 4. 特定技术领域基金会

| 基金会名称 (英文/中文) | 重点领域/简介 | 知名项目举例 |
| :--- | :--- | :--- |
| RISC-V International | 负责管理和推广开源指令集架构 RISC-V。 | RISC-V 架构规范和生态系统。 |
| OpenStreetMap Foundation (OSMF) | 致力于开放地理空间数据，支持 OpenStreetMap 地图项目。 | OpenStreetMap (OSM) |

GitHub 上有大量与 CUDA 相关的开源项目，它们涵盖了从深度学习框架到高性能计算库、再到基础工具和示例等多个层面。

由于 CUDA 是 NVIDIA 专有的并行计算平台，许多最重要的开源项目都由 NVIDIA 或其赞助的生态系统（如 RAPIDS）直接托管在 GitHub 上。

以下是一些最重要和热门的开源 CUDA 项目类别：

---

### 1. 深度学习框架 (Deep Learning Frameworks)

这些是使用 CUDA 进行 GPU 加速的最流行的项目，其核心计算都依赖 CUDA 编程。

| 项目名称 | GitHub 组织 | 领域/简介 |
| :--- | :--- | :--- |
| PyTorch | `pytorch/pytorch` | 一个开源的机器学习框架，广泛用于研究和生产。其 Tensors (张量) 和动态神经网络的核心加速依赖于 CUDA。 |
| TensorFlow | `tensorflow/tensorflow` | 另一个主要的机器学习框架。虽然核心代码库巨大，但其 GPU 加速部分是基于 CUDA 实现的。 |
| FlashAttention / FlashInfer | `Dao-AILab/flashattention` / `flashinfer-ai/flashinfer` | 针对 LLM (大型语言模型) 推理和训练的优化 CUDA 内核库，极大地提高了 Transformer 模型中 Attention 机制的效率。 |

### 2. NVIDIA 核心高性能计算库

这些是 NVIDIA 官方开源的、作为 CUDA 工具包核心组成部分的库和工具，它们提供了底层的并行计算原语。

| 项目名称 | GitHub 组织 | 领域/简介 |
| :--- | :--- | :--- |
| CUDA Samples | `NVIDIA/cuda-samples` | 官方提供的 CUDA 开发者示例集合，用于演示 CUDA Toolkit 的各种功能和 API。（这是学习 CUDA 编程的起点） |
| CCCL (CUDA Core Compute Libraries) | `NVIDIA/cccl` | 包含了 CUDA C++ 标准库、Thrust 和 CUB (CUDA Unbound) 等关键组件。它们提供了高性能的并行算法原语。 |
| NCCL (Collective Communication Library) | `NVIDIA/nccl` | 优化过的集合通信库，用于多 GPU 或多节点之间的快速数据传输（如 All-reduce, Broadcast），是分布式深度学习的关键。 |
| NVIDIA Container Toolkit | `NVIDIA/container-toolkit` | 允许用户在 Docker 和其他容器运行时环境中构建和运行 GPU 加速容器的工具。 |

### 3. RAPIDS 生态系统 (数据科学和 ML)

RAPIDS 是一个由 NVIDIA 领导的开源项目套件，旨在利用 CUDA 加速整个数据科学工作流。

| 项目名称 | GitHub 组织 | 领域/简介 |
| :--- | :--- | :--- |
| cuDF | `rapidsai/cudf` | GPU DataFrame 库，类似于 Pandas，但完全在 GPU 上运行，用于加速数据加载、清洗和操作。 |
| cuML | `rapidsai/cuml` | GPU 加速的机器学习算法库，提供与 Scikit-learn 类似的 API。 |
| cuGraph | `rapidsai/cugraph` | GPU 加速的图分析库，用于大规模图数据处理。 |
| RAFT | `rapidsai/raft` | 包含了基础、常用的机器学习和信息检索算法原语，作为 cuML 等库的构建块。 |

### 4. 其他重要领域

| 项目名称 | GitHub 组织/相关方 | 领域/简介 |
| :--- | :--- | :--- |
| HugeCTR | `NVIDIA/HugeCTR` | 专为点击率 (CTR) 估计训练设计的高效 GPU 框架，适用于推荐系统。 |
| CV-CUDA | `NVIDIA/CV-CUDA` | GPU 加速的云规模图像处理和计算机视觉软件库。 |
| OpenCV (部分) | `opencv/opencv` | 广为人知的计算机视觉库，其部分模块（如 CUDA 模块）包含 CUDA 加速实现。 |
| HPC 科学计算 | 各种 HPC 项目 | 许多高性能计算和科学仿真项目（例如分子动力学、流体动力学等）都直接包含大量的 CUDA C/C++ 代码。 |

