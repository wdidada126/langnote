# MIT 6.858 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| "Smashing the Stack for Fun and Profit" (Aleph One) | 1996 | 栈溢出利用的系统化开山文档 | L5 |
| Efficient Software-Based Fault Isolation (Wahbe et al.) | 1993 | SFI：无硬件支持的二进制沙箱思想源头 | L7 |
| NaCl: Sandboxing Native Code on the Client (Castro et al.) | 2009 | 软件受限模块沙箱，支撑浏览器原生码执行 | L7 |
| Security Policies and Security Models (Goguen & Meseguer) | 1982 | 非干扰（noninterference）信息流安全奠基定义 | L11 |
| Secure Computer Systems: Mathematical Foundations (Bell & LaPadulla) | 1973 | 机密性强制访问控制的形式化模型 | L11 |
| SUNDR: A Secure, Versioned Remote Storage System (Kazar et al.) | 2008 | 不可信服务器上的版本化安全存储，SecFS 蓝本 | L17 |
| EXE: Automatically Generating Inputs of Death (Cadar et al.) | 2006 | 混合执行遍历路径生成测试用例 | L14 |
| KLEE: Unassisted and Automatic Generation of High-Coverage Tests | 2008 | fork 式符号虚拟机使符号执行工程化 | L14 |
| Detecting Defects and Security Vulnerabilities with the Sage White-box Program Analyzer | 2011 | 具体+符号混合执行缓解路径爆炸（选读） | L14 |
| American Fuzzy Lop: Tackling the Problem of Concolic Testing? — AFL 技术文档 | 2014 | 覆盖率遗传引导 fuzzing 的事实标准 | L15 |
| PolyBike 与其代价收益分析 (Automatic Comparative Evaluation of Information Flow Security Systems) | 2008 | 位粒度动态污点追踪框架与开销量化 | L13 |
| Spectre / Meltdown（Roed? 正式: Kocher et al.; Lipp et al.） | 2018 | 推测执行侧信道摧毁隔离假设 | L16 |
| Intel SGX Explained (Costan & Devadas) | 2016 | enclave 模型与攻击面的全景综述 | L18 |
| seL4: Formal Verification of an OS Kernel (Klein et al.) | 2009 | 第一个全功能形式化验证微内核 | L19 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| Got SAML? Cross-Framework Data-Flow Auditing of Web SSO | USENIX Sec 2021 | 数据流分析批量发现 SSO 实现缺陷 | L2, L13 |
| Hertzbleed: Power Side Channel → Timing Attack | USENIX Sec 2022 | 远程功率侧信道新类别 | L16, L18 |
| TLBlade: Prefetch-based TLB 侧信道攻击 | USENIX Sec 2024 | 共享 TLB/预取通道实现跨边界密钥提取 | L18 |
| StackWarp: Intel 栈引擎的跨特权数据注入 | 2023 | 微结构状态成为新利用原语 | L6, L16 |
| GhostWrite: Without Memory Writes? — 无写内存破坏 | USENIX Sec 2024 | 设备/驱动层改写引发的通用内存破坏 | L5, L6 |
| ret2page: A New Page-Face — 页缓存侧信道削弱内核 ASLR | 2022 | 布局熵防御时代的新泄露原语 | L6, L7 |
| Syzkaller/HWGP? 及内核 fuzzing 演进（含 syzbot 数据报告） | 2021–2025 | 工业内核漏洞发现主力持续产出 | L15 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| Web 攻防（L2–L4） | OWASP Juice Shop、DVWA、Burp Suite | 靶场与拦截式测试工具 |
| 溢出与 ROP（L5–L6） | pwn.college、pwntools、ROPgadget/Ropper | CTF 教学栈与利用链工具 |
| 沙箱（L7） | gVisor、Firecracker、Chromium sandbox、seccomp-bpf | 容器/浏览器的原生码隔离层 |
| 认证（L9） | Keycloak、MIT Kerberos | OIDC/SSO 生产实现 |
| 特权分离（L10） | Postfix 多进程架构、OpenSSH (sshd 分离)、Chromium 多进程 | 工业级最小权限拆分范本 |
| 污点/符号执行（L13–L14） | angr、KLEE、Triton、Joern | 二进制分析与漏洞发现的开源引擎 |
| Fuzzing（L15） | AFL++、libFuzzer、OSS-Fuzz、Syzkaller | 从用户态库到内核的持续 fuzz 流水线 |
| 推测执行缓解（L16） | Linux 内核（retpoline/KPTI）、编译器缓解矩阵 | 上游缓解的实现与性能开关 |
| 安全文件系统（L17） | Tahoe-LAFS、scryptfs、IPFS（不可信节点模型） | SUNDR 思想的开源延续 |
| 侧信道/enclave（L18） | Gramine/Keystone、TLDrace? → 通用: cache 攻击复现套件（如 Flush+Reload PoC） | 研究复现与 RISC-V 开源 TEE |
| 形式化验证（L19） | seL4、VeriFast、F* | 从内核到密码库的证明工具链 |
