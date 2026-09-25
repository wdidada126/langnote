# UCB Sysadmin DeCal — 论文与工程实践对照（骨架）

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联周次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System | 1974 | 现代 Linux 一切文件/权限/进程模型的祖先 | W1/W2 |
| The Design and Implementation of the 4.4BSD Operating System（Leffler 等，专著视同） | 1989/2003 | BSD 血统解释 /etc 配置与服务体系的来源 | W3/W4 |
| Ext4 - The Third Generation ext4 Filesystem | 2010 | 日志文件系统如何保证崩溃一致性 | W1/W3 |
| glibc/NSS 文档（Name Service Switch） | 1990s | `/etc/hosts`、DNS、NIS 解析顺序的实现来源 | W5/W7 |
| BitTorrent Incentive Engineering（Cohen） | 2003 | 分布式分发协议，理解包管理镜像与 P2P 分发 | W3 |
| Monads and Effectful Programming 之外的运维经典：The Tail at Scale（Baron, CACM） | 2009 | 大规模服务运维的故障模式总览 | W9/W10 |

## 二、近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联周次 |
| --- | --- | --- | --- |
| Firecracker: Lightweight Virtualization for Serverless Applications（NSDI'20，后续扩展 2021） | 2020 | microVM 隔离模型，容器/虚拟机边界的新方案 | W9 |
| A Survey on Container Security / eBPF 安全可观测系列（如 "Visibility is All You Need: eBPF"） | 2022–2024 | eBPF 成为 Linux 可观测性与网络安全事实标准 | W4/W5/W9 |
| Kubernetes Security 相关基准（KCSA / CIS K8s 加固研究） | 2022 | 集群侧密钥与 RBAC 攻击面系统化 | W7/W10 |
| GPU 集群调度与 MIG 相关论文（如 "AntMan", "TAPIRES"） | 2021–2023 | 多租户 GPU 共享与利用率问题，落地 W12 运维视角 | W12 |
| Configuration Management Drift 检测研究 | 2023 | 声明式配置（Puppet 思路）在生产中的偏移与自动修复 | W11 |

## 三、知识点在开源项目中的应用

| 课程知识点 | 开源项目案例 | 说明 |
| --- | --- | --- |
| 权限/文件系统 | coreutils、shadow-utils | sudo 配置与文件权限实战 |
| 包管理 | apt/dnf、Nix | Nix 将"声明式包管理"推到极致，衔接 W11 |
| 服务管理 | systemd（freedesktop） | W4 全部内容即其日常接口 |
| 网络排障 | iproute2、tcpdump、nmap | W5/W6 实验主力工具 |
| 密钥与安全 | OpenSSH、certbot、Vault | W7 实操对象 |
| Git 协作 | GitHub Actions、pre-commit | W8 hooks 自动化 |
| 容器 | moby/moby、containerd、podman | W9 本体 |
| 集群 | kubernetes/kubernetes、k3s、Helm | W10 本体与包分发 |
| 配置即代码 | puppet/puppet、ansible、Terraform | W11 对照生态 |
| GPU | nvidia-container-toolkit、CUDA Samples | W12 实操环境 |
