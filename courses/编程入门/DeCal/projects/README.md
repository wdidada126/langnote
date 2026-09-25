# UCB Sysadmin DeCal — 配套项目计划（骨架）

> 本轮不写代码。主线：在虚拟机（推荐 Ubuntu Server）上从裸系统逐步演进到"容器化 + 配置管理 + GPU"的小型个人基础设施，全部练习可用 bandit 前 15 关热身替代内网作业。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| W1 Linux 基础 | Bash | 虚拟机装机 + 目录结构与权限审计脚本（输出异常权限文件清单） | VirtualBox/Vagrant 起机；`bash audit.sh` |
| W2 Shell 编程 | Bash + tmux | `deploy-helper.sh`：一键打包/上传/解压发布包的工作流脚本 | `./deploy-helper.sh` + tmux 会话 |
| W3 包管理 | Shell | 把小项目做成 `.deb`（dpkg-buildpackage）并安装/卸载验证 | `debuild -us -uc` |
| W4 服务 | systemd unit | 为自己的 Python/Node 小程序写 unit：崩溃自重启 + 日志接入 journald | `systemctl --user enable --now app.service` |
| W5/W6 网络 | nginx conf | 起 nginx 反向代理 + HTTPS（自签/letsencrypt 测试），DNS 与抓包排障报告 | `nginx -t && systemctl reload nginx` |
| W7 安全 | OpenSSH 配置 | 禁用密码登录、仅密钥认证、跳板机 ProxyJump 全套演练 | `ssh -J bastion host` 验证 |
| W8 Git | Git + hooks | 把以上所有配置文件放进私有仓库 + pre-commit 校验 + PR 流程自演 | `git init` + GitHub 私有仓库 |
| W9 Docker | Dockerfile | 将 W4/W6 的服务全部容器化（多阶段构建、volume、healthcheck） | `docker build -t myapp . && docker compose up` |
| W10 Kubernetes | YAML | k3s/minikube 上部署 W9 镜像：Deployment+Service+Ingress+探针 | `kubectl apply -f k8s/` |
| W11 Puppet/Ansible | Puppet/YAML | 用配置管理重写"装机→服务→防火墙"全过程，验证幂等（跑两遍无 diff） | `puppet apply site.pp` 或 `ansible-playbook site.yml` |
| W12 CUDA | C++/Python | 有 GPU 则跑 deviceQuery + 容器内 `--gpus` 运行样例；无 GPU 写调研报告 | `docker run --gpus all cuda-sample` |

## 验收清单
- [ ] 一台可复现的个人服务器环境：裸机 → 配置管理脚本一键重建，服务全部容器化并有健康检查。
