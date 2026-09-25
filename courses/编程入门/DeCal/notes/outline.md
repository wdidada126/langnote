# UCB Sysadmin DeCal — 笔记大纲（骨架，12 周）

## W1 Linux 基础
- 文件系统层级标准（FHS）：`/etc`、`/var`、`/usr`、`/home` 各自职责。
- 权限模型：rwx、用户/组/其他、`chmod/chown`、umask、特殊位。
- 常用命令集：ls/ps/grep/find/tar 的组合使用。
- 编辑器与分页器：nano/vim 应急、less 阅读日志。

## W2 Shell 编程与终端工具
- bash 脚本：变量、条件、循环、函数、退出码。
- 管道与重定向：`|`、`>`、`2>&1`、xargs。
- tmux：会话保持让远程任务不死；vim 基础操作。
- 把 W1 的手工操作脚本化是本层的验收标准。

## W3 包管理
- 包管理器做什么：依赖解析、签名校验、升级回滚（apt/dnf 对照）。
- 源与镜像、`dpkg -L` 查询文件归属。
- 从源码编译安装的完整链：configure/make/make install。
- Python/Node 等语言级包管理与系统级包管理的边界。

## W4 服务 Services
- 守护进程概念；systemd unit 文件结构（Service/Restart/After）。
- `systemctl start/status/journalctl` 日常三板斧。
- 端口占用排查：`ss -tulpn`、lsof。
- 日志轮转（logrotate）与排障入口。

## W5 基础计算机网络
- OSI/TCP-IP 分层落到 Linux：网卡、路由表、防火墙四个观察点。
- DNS 解析链与 `/etc/resolv.conf`、`/etc/hosts`。
- 抓包三件套：ping/traceroute/tcpdump（tshark 选读）。
- 防火墙与 NAT 的基本心智模型。

## W6 网络服务
- 搭建并配置一个 HTTP 服务（nginx）与反向代理。
- SSH 服务的部署、config 文件、跳板机思路。
- 服务开机自启、多实例、限权账户。
- 用 W4 的 systemd 知识管理 W6 的所有服务。

## W7 安全与密钥管理
- 对称/非对称与哈希的使用场景；ssh key 全生命周期。
- 最小权限原则、sudo 配置、密钥不进仓库。
- 证书与 HTTPS（letsencrypt 思路）。
- 常见事故复盘：明文密码、0.0.0.0 监听、权限 777。

## W8 Git
- 集中式 vs 分布式；分支模型与团队工作流。
- code review、PR、冲突解决实操。
- Git hooks 把检查自动化（衔接 W11 自动化主题）。
- bandit 补充练习：文件权限 + 远程登录综合场景。

## W9 Docker
- 容器 vs 虚拟机：namespace/cgroup 的直观理解。
- 镜像分层、Dockerfile 最佳实践、volume 与网络。
- 把 W6 的 nginx 服务容器化是本层的验收标准。
- 日志、资源限制与进入运行中容器排障。

## W10 Kubernetes
- 集群角色：控制面/节点池；Pod、Deployment、Service 三件套。
- 声明式 YAML 与 kubectl 日常操作。
- 扩缩容、滚动更新、健康探针。
- 理解"运维视角的抽象"：从单机 systemd 到集群调度的连续性。

## W11 Puppet
- 配置即代码：资源声明式模型（package/service/file）。
- Puppet manifest 基础与 agent/server 架构。
- 与 shell 脚本的本质区别：幂等性与收敛。
- 了解 Ansible 作为对照（现代替代）。

## W12 CUDA
- GPU 编程模型速览：kernel、线程块、显存层级。
- 驱动/CUDA 版本兼容与 `nvidia-smi` 排障。
- 容器中的 GPU（`--gpus`、device plugin）。
- 为后续深度学习系统课程留出接口。
