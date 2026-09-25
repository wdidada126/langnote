# MIT 6.1600 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| New Directions in Cryptography (Diffie & Hellman) | 1976 | 提出公钥密码与密钥交换问题 | L6 |
| A Method for Obtaining Digital Signatures… (Rivest, Shamir & Adleman) | 1978 | RSA 公钥加密与签名 | L7, L8 |
| Using Encryption for Authentication in Large Networks of Computers (Needham & Schroeder) | 1978 | 认证协议范式的起点 | L4 |
| An Attack on a Protocol… (Lowe) | 1988/1995 | 以中间人攻击修正 NS 协议，催生形式化分析 | L4 |
| The Protection of Information in Computer Systems (Saltzer & Schroeder) | 1975 | 安全设计原则，平台安全章节的纲领 | L10, L12 |
| The Dining Cryptographers Problem (Chaum) | 1988 | 匿名信道与多方隐私计算思想源头 | L17 |
| Cryptanalysis of MD5 and SHA-1 Collisions (Wang et al.) | 2004–2005 | 实际攻破 MD5/SHA-1 族，验证抗碰撞定义的重要性 | L3 |
| AES (FIPS-197) 与 HMAC (RFC 2104) | 1997/1997 | 对称加密与消息认证码的标准化落点 | L5, L3 |
| Protection in the Access Matrix Model (Harrison, Ruzzo & Ullman) | 1976 | 访问矩阵模型安全性质可判定性的经典 | L12 |
| Secure Computer Systems: Mathematical Foundations (Bell & LaPadulla) | 1973 | 形式化机密性访问控制模型 | L12 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| Post-Quantum Standards: FIPS 203 (ML-KEM) / 204 (ML-DSA) / 205 | NIST 2024 | 基于模格的密钥封装与签名标准定稿 | L6–L9 |
| Hertzbleed: Turning Power Side-Channel Attacks Into Timing Attacks | USENIX Sec 2022 | 功耗调频构成远程可观测计时信道 | L11, L14 |
| Downfall: A New Class of Transient Execution Attacks (Wikner & Keys) | 2022 | 微架构聚合缓冲新攻击面，enclave/平台安全警钟 | L11 |
| 口令泄露语料与撞库规模化测量研究（credential stuffing 系列） | 2021–2023 (IMC/USENIX) | 撞库工业化实证，支撑口令存储章节 | L2 |
| 浏览器扩展与终端攻击面测量研究族 | 2021–2024 | 终端用户威胁（扩展滥用/钓鱼）的量化画像 | L16 |
| 本地差分隐私产品化部署复盘（Apple/Google 遥测系列） | 2021–2024 | DP 从理论到落地的经验与教训 | L17 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| MAC/哈希/HMAC（L3） | OpenSSL、libsodium、Python hashlib/hmac | 完整性 API、包签名校验（PyPI/Debian） |
| 认证协议/Kerberos（L4） | MIT Kerberos (krb5)、FreeIPA | 企业认证基础设施 |
| AEAD/分组模式（L5） | Linux dm-crypt/LUKS2、Age | 磁盘与文件加密的 XChaCha20-Poly1305 |
| DH/ECDH（L6） | Signal Protocol（libsignal）、WireGuard | 双棘轮与 noise 框架的密钥协商核心 |
| 公钥加密/签名（L7–L8） | GnuPG、Sigstore/cosign | 邮件签名与软件供应链签名 |
| TLS/PKI（L9） | Let's Encrypt、Caddy、Mozilla NSS | ACME 自动化证书部署 |
| OS 隔离/最小特权（L10–L12） | Linux capabilities/seccomp、gVisor、seL4 | 容器与微内核的形式化隔离实践 |
| SGX/硬件信任根（L11） | Keystone、SGX SDK、Android StrongBox | RISC-V 开源 enclave 与移动 TEE |
| 内存漏洞与 fuzzing（L13–L14） | AFL++、OSS-Fuzz、ClusterFuzz | 工业级持续模糊测试流水线 |
| 缓解机制（L15） | Chromium（CFI/PAC）、Rust（BorrowChecker） | 浏览器与系统语言级防御 |
| 隐私（L17） | Tor、Google/Apple DP 遥测、OpenMined PyDP | 匿名网络与差分隐私库 |
