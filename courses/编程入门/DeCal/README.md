# UCB Sysadmin DeCal：Linux 系统管理入门

## 一、课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 / 课程号 | Systems at Berkeley: Sysadmin DeCal（UCB DeCal 学生主讲课程，无正式课程号） |
| 学校 | UC Berkeley |
| 主讲 | UCB 系统与计算服务部（SIR）学生助教团队（学生 DeCal 形式） |
| 教材 | 无指定教材；每周 lab 自带阅读材料 |
| csdiy 路径 | `编程入门/DeCal`（csdiy.wiki） |
| 最新期次 | 以官网当季春季班为准（csdiy 页面更新于 2024-04-14） |
| 状态 | 骨架已建，笔记待填充 |

- 课程网站：官网 decal.berkeley.edu 的 Sysadmin 页（csdiy 链接），讲义/lab 在课程 GitHub 组织公开
- 视频：原版见官网，B 站有搬运
- csdiy 标注：先修无 ｜ 语言 shell ｜ 难度 🌟🌟🌟 ｜ 预计 20 小时

## 二、为什么学

- 与 Missing Semester 同题材但**更系统、更清晰、面向零基础**，csdiy 首推本课程入门 Linux 运维。
- 12 周从 Linux 基础一路讲到 Docker、Kubernetes、Puppet、CUDA，覆盖一名工程师日常所需的全部"环境侧"知识。
- 每周 lab 动手为主，是后续 OS/分布式/体系结构课程实验（虚拟机、容器、集群）的直接预演。
- 部分作业需 UCB 内网远程服务器，可用自建虚拟机 + OverTheWire **bandit**（前 15 关即纯 Linux 练习）替代补齐。

## 三、先修与知识联系

- 先修：无；与 Missing Semester 任选其一先学均可，DeCal 学完后 Missing Semester 可当作快速复习。
- 后续联系：
  - 包管理/服务/systemd → MIT 6.S081、CS162 的进程与服务概念落地；
  - 网络基础/网络服务 → CS168/CS144 实验环境；
  - Docker/Kubernetes/Puppet → 15-445、CS149、MIT 6.5840 的部署与复现基础；
  - CUDA 周 → 深度学习系统类课程（10-414/6.5940）。

## 四、讲义章节目录（12 周）

| 周次 | 标题 | 阅读材料 |
| --- | --- | --- |
| W1 | Linux 基础：文件系统、权限、shell 入门 | 课程官网 Week1 讲义 + lab1 阅读材料 |
| W2 | Shell 编程与终端工具（tmux、vim） | Week2 讲义 + lab2 |
| W3 | 包管理（apt/yum、软件如何被安装） | Week3 讲义 + lab3 |
| W4 | 服务 Services（systemd、守护进程、日志） | Week4 讲义 + lab4 |
| W5 | 基础计算机网络（TCP/IP、DNS、抓包） | Week5 讲义 + lab5 |
| W6 | 网络服务（HTTP/SSH/邮件等常驻服务配置） | Week6 讲义 + lab6 |
| W7 | 安全与密钥管理（ssh key、证书、最小权限） | Week7 讲义 + lab7 |
| W8 | Git 与协作 | Week8 讲义 + lab8 |
| W9 | Docker 与容器 | Week9 讲义 + lab9 |
| W10 | Kubernetes 与集群编排 | Week10 讲义 + lab10 |
| W11 | Puppet 配置管理与自动化运维 | Week11 讲义 + lab11 |
| W12 | CUDA 与 GPU 运维视角 | Week12 讲义 + lab12 |
