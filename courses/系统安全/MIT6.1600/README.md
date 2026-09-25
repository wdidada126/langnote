# MIT 6.1600 计算机安全基础（Foundations of Computer Security）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | MIT 6.1600: Foundations of Computer Security（本科版；研究生并行版 6.1601） |
| 学校 | Massachusetts Institute of Technology |
| 主讲 | Shafi Goldwasser 等（MIT Cryptography and Information Security 组） |
| 教材 | 无指定教材，每讲有课程 notes；参考 Katz-Lindell、Boneh-Shoup 风格材料 |
| csdiy 路径 | `系统安全/MIT6.1600`（csdiy 归类「计算机系统安全」） |
| 最新期次 | Fall 2023（opencourseware 镜像含 fall22/fall23） |
| 状态 | 骨架 |

- 课程网站：https://ocw.mit.edu/courses/6-1600-foundations-of-computer-security-fall-2023/ （及 6.9880/6.1601 对应页）
- 语言：Python3（实验）；作业：6 个难度适中的编程实验
- csdiy 资源汇总：PKUFlyingPig/MIT6.1600

## 为什么学

- MIT 安全入门的正统路线：五大模块（认证 → 传输安全 → 平台安全 → 软件安全 → 人/终端用户安全）覆盖概念全景，理论密度高于多数同类课。
- 每讲由真实漏洞案例落地抽象概念（协议缺陷、哈希碰撞滥用、平台提权），配合 6 个动手实验写漏洞利用，感性理性双收。
- 主讲出自密码学顶级学派（Goldwasser 为图灵奖得主），对「安全证明式思维」的养成优于工程导向课程，是 6.858 攻防课的理想前置。

## 先修与知识联系

- 先修：离散数学（CS70/6.042J 级别）、编程基础（Python）、计算机系统基础（CSAPP/6.004 任一）。
- 联系：与 CS161 互为「理论/工程」两面（CS161 偏系统与攻防实操，本课偏模型与证明直觉）；下游 6.858 直接消费其密码与平台安全概念；SEED Labs 可作实验弹药库。

## 讲义章节目录（按 Fall 2023 五模块整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| **M1 认证（Authentication）** | | |
| L1 | 导入：安全目标、威胁模型与攻击者能力 | 课程 notes |
| L2 | 身份认证基础：口令、熵与离线破解 | notes；口令强度分析材料 |
| L3 | 消息完整性与哈希函数、MAC | notes |
| L4 | 认证协议：挑战-应答、中间人与重放 | Needham-Schroeder (1978)；Lowe (1995) |
| **M2 传输安全（Transport Security）** | | |
| L5 | 机密性与对称加密：IND-CPA 语义安全 | notes；Katz-Lindell 节选 |
| L6 | 密钥交换：Diffie-Hellman 与其主动攻击缺陷 | Diffie & Hellman (1976) |
| L7 | 公钥加密与混合加密 | RSA (1978) |
| L8 | 数字签名与哈希的滥用 | notes |
| L9 | TLS 与 PKI：密钥分发和信任 | 课程 notes |
| **M3 平台安全（Platform Security）** | | |
| L10 | OS 安全：隔离、特权级与最小特权 | Saltzer & Schroeder (1975) |
| L11 | 硬件信任根与安全 enclave | SGX 论文/白皮书节选 |
| L12 | 文件系统/访问控制/能力机制 | notes |
| **M4 软件安全（Software Security）** | | |
| L13 | 内存错误与利用基础 | 教材化 notes；Aleph One (1996) |
| L14 | 软件漏洞挖掘：fuzzing 与程序分析 | AFL (Zalewski 2014) 节选 |
| L15 | 缓解与防御：编译器/OS 加固 | notes |
| **M5 人与终端用户（Human / End-User Security）** | | |
| L16 | 可用性与安全、钓鱼与社会工程 | 课程 notes（红队演练材料） |
| L17 | 隐私：匿名通信与差分隐私导论 | Dining Cryptographers (Chaum 1988)；DP 入门节选 |
| L18 | 群体/系统级安全与课程总结 | notes |

> 注：6.1600 各届讲序有微调，本表按五模块骨架整理，填充笔记时对照当期 schedule。
> 实验：Lab1 哈希/MAC 应用、Lab2 认证协议攻击、Lab3 分组模式与填充 oracle、Lab4 签名/PKI 实操、Lab5 内存漏洞利用、Lab6 侧信道/平台攻击（以当期发布为准）。

## 作业与项目（概览）

6 个 Python 实验，围绕「实现→打破→修复」循环。配套复刻计划见 `projects/README.md`。
