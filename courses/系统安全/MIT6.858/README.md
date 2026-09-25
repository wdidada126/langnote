# MIT 6.858 计算机系统安全（Computer System Security）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | MIT 6.858: Computer System Security（研究生/高阶本科攻防课； undergrad 版对应 6.1601） |
| 学校 | Massachusetts Institute of Technology |
| 主讲 | Adam Smith（近年）；历史版本由 Karl Levchenko、Nickolai Zeldovich 等执教 |
| 教材 | 无指定教材，以论文 + 讲义为主 |
| csdiy 路径 | `系统安全/MIT6.858` |
| 最新期次 | 课程开源资源以 2022 版为主（css.csail.mit.edu/6.858/2022），每学期更新 |
| 状态 | 骨架 |

- 课程网站：http://css.csail.mit.edu/6.858/2022/ （当期入口沿用同域名换年份）
- 实验靶系统：Web 应用 **Zoobar**；4 个 Lab + Final Project（如 SecFS）
- 语言：C、Python（x86 汇编基础）

## 为什么学

- 系统攻防的「硬核正统」：围绕同一个真实 Web 应用从缓冲区溢出打到符号执行找 bug，再逐层构建特权分离与浏览器防线。
- 每讲精读体系化论文（SFI、NaCl、SUNDR、EXE/KLEE、Spectre…），直接对接 USENIX/S&P 主流研究脉络。
- Lab 3 混合符号执行、Final Project SecFS（对抗不可信服务器的远端文件系统，参考 SUNDR）是把「程序分析 + 系统构造」同时练到的稀缺作业。

## 先修与知识联系

- 先修：计算机体系结构、OS（6.S081/CS162 级）、熟悉 C 与 Python；建议先修 6.1600 或 CS161 补密码学概念。
- 联系：本课 = CS161 的广度换成纵深（利用、分析、构造）；Lab3 的符号执行通向软件分析课（CS242/NJU 软分）；Final Project 通向存储/分布式（6.5840 的容错视角在信任边界上的镜像）。

## 讲义章节目录（按 2022 版 + 经典课表整理，以当期为准）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| **Part 1 原则与 Web 攻防** | | |
| L1 | 导入：原则、威胁模型、混淆加密 | 讲义；Lessons from "Observe and Divide"? 导论材料 |
| L2 | Web 攻击 I：XSS、CSRF、会话劫持 | 讲义 + Zoobar 源码 |
| L3 | Web 攻击 II 与防御：同源策略、沙箱 | 讲义；浏览器安全材料 |
| L4 | 浏览器安全与扩展信任 | 讲义（NoScript/扩展攻击面） |
| **Part 2 原生代码攻击** | | |
| L5 | 缓冲区溢出与 shellcode | Aleph One (1996)；现代利用综述 |
| L6 | 利用与缓解：ROP、ASLR、CFI | "Buffer Overflows: Attacks and Defenses" (2003) |
| L7 | 语言防护与软件沙箱 | SFI (Wahbe 1993)；NaCl (2009) |
| **Part 3 密码学与认证（速览）** | | |
| L8 | 密钥管理与 TLS/PKI | 讲义（对接 6.1600 概念） |
| L9 | 认证协议与单点登录 | Kerberos (Steiner 1988) |
| **Part 4 特权分离与访问控制** | | |
| L10 | 特权分离设计 | "Iron Fleet"? → 经典：web 分层架构论文（Exokernel? 选读） |
| L11 | 访问控制与信息流模型 | Bell-LaPadulla (1973)；非干扰 (Goguen & Meseguer 1982) |
| L12 | 能力系统与 Flask/SELinux | "Flask: Security for Policy, not Poly"?（当期选读） |
| **Part 5 程序分析找漏洞** | | |
| L13 | 动态污点追踪 | BitBlaze/"Taint Analysis" 材料；PolyBike (S&P'08) |
| L14 | 符号执行与混合执行 | EXE (SOSP'06)；KLEE (OSDI'08) |
| L15 | Fuzzing 与现代漏洞挖掘 | AFL (2014)；Syzkaller 材料（选读） |
| **Part 6 高级主题** | | |
| L16 | 推测执行攻击 | Spectre (2018)/Meltdown；Foreshadow |
| L17 | 安全文件系统与可信路径 | SUNDR (ATC'08)；SecFS 项目指南 |
| L18 | 侧信道与 enclave | SGX (Costan 2016)；ENCLAZE? 选读 |
| L19 | 软件验证 | CertiKOS/SeL4 节选（当期自选） |
| L20 | 隐私与课程复盘 | DP 导论节选 + final 分享 |

> Lab 对应：Lab1=Zoobar 缓冲区溢出攻破（L5–L6）；Lab2=特权分离加固（L10）；Lab3=Python 代码混合符号执行找 bug（L14）；Lab4=浏览器攻击防御（L3–L4）；Final Project=SecFS 远端安全文件系统（L17，参考 SUNDR）。

## 作业与项目（概览）

4 Labs + Final Project/Lab5；评分围绕 exploit 有效性、分析工具覆盖率与系统设计报告。详见 `projects/README.md`。
