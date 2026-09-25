# 第 12 章 DES / 第 13 章 其他分组密码 / 第 14 章 仍在增加的分组密码 / 第 15 章 组合分组密码

> **一句话**：第 12–15 章是全书最「厚」也最沉没的部分——**四章共七十几页的密码家族志**，而今天活下来的只有其中两个（3DES 与 Blowfish 的遗产），加上一个 1996 年根本不存在的 AES。

---

## 本章地图（Ch12 DES）

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 12.1 | 背景 | DES 的来历：1972 年 IBM Lucifer 的研究与美国 NSA 的介入 |
| 12.2 | DES 的描述 | Feistel 网络、16 轮、初始与最终置换、每轮 F 函数 |
| 12.3 | DES 的安全性 | 56 位实际密钥、互补性（互补明文/密钥等价）、[Saouter 的关键路径研究] |
| 12.4 | **差分分析与线性分析** | 本书唯一系统讲密码分析的地方，见 `concepts/` 专篇 |
| 12.5 | 真正的设计标准 | 为什么 S 盒与非线性；「设计标准被隐藏」的争议 |
| 12.6 | DES 变体 | DES-X、3DES（EDE）、CDMF、白化 |
| 12.7 | DES 今天安全吗 | 1998 年 EFF Deep Crack 给出答案 |

## 本章地图（Ch13 其他分组密码）

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 13.1–13.3 | Lucifer、Madryga、NewDES | 早期替代候选；NewDES 与 DES 的结构同源 |
| 13.4 | FEAL | 1990 年代被差分攻击击穿的著名案例 |
| 13.5–13.7 | REDOC、LOKI、Khufu/Khafre | 结构与安全性各异，多已沉没 |
| 13.8 | RC2 | 变长密钥的专利算法，遗产之一 |
| 13.9 | IDEA | 64 位块 + 128 位密钥，PGP 用过；今天仍被部分系统使用 |
| 13.10–13.11 | MMB、CA-1.1 | 冷门候选 |
| 13.12 | Skipjack | 曾用于 Clipper，密钥托管争议的中心 |

## 本章地图（Ch14 仍在增加的分组密码）

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1–14.8 | GOST、CAST、**Blowfish**、**SAFER**、3-Way、Crab、SXAL8/MBAL、**RC5** | 这一段几乎就是 1996 年 AES 候选的提前预演 |
| 14.9–14.12 | 其他算法、设计理论、用哈希构造、如何选择 | 作者明确呼吁读者不要自己造算法 |

## 本章地图（Ch15 组合分组密码）

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 15.1–15.2 | 双重加密、三重加密 | 2DES 的中途相遇攻击；3DES 由此成为过渡标准 |
| 15.3 | 加倍分组长度 | 扩大块长以抵抗生日碰撞 |
| 15.4–15.5 | 其他多重加密、CDMF 缩短密钥 | 复杂性换兼容性的典型实践 |
| 15.6 | 白化（whitening） | 抗密钥相关的结构攻击 |
| 15.7–15.8 | 级联与混合多个块密码 | 级联不一定更安全——**并行级联可被 meet-in-the-middle** |

---

## 核心精讲

> 以下全部是**教学示意代码，不参与构建、不编译、不运行**。

### Feistel 网络：DES 的全部结构（12.2）

```
明文 → IP → L0 || R0
for i = 1..16:
    Li = Ri-1
    Ri = Li-1 ⊕ F(Ri-1, Ki)          # 只改右半边
→ FP ← R16 || L16
```

```python
# 教学示意，不参与构建、不编译、不运行
def feistel_round(left: int, right: int, round_key: int) -> tuple[int, int]:
    """DES / Blowfish / RC5 共同的骨架：一轮只改右半。"""
    return right, left ^ round_key

def feistel_encrypt(block: int, keys: list[int], half: int) -> int:
    left = right = 0
    for i in range(1, block.bit_length() + 1):
        bit = (block >> (block.bit_length() - i)) & 1
        if i <= half:
            left = (left << 1) | bit
        else:
            right = (right << 1) | bit
    for k in keys:
        left, right = feistel_round(left, right, k)
    return (left << half) | right
```

> Feistel 的价值在于**加密与解密只是「把子密钥倒着用」**——这个性质让 DES 的硬件实现极简（这正是 1996 年 EFF 能把 Deep Crack 做进一个机箱的原因）。

### 3DES（EDE）：从 DES 到今天的过渡

```python
# 教学示意，不参与构建、不编译、不运行
def triple_des_encrypt(des, k1: bytes, k2: bytes, k3: bytes, pt: bytes) -> bytes:
    """EDE：加密-解密-加密。注意 k1 == k3 时等价于 2DES。"""
    return des(k1, des(k2, des(k1, pt), decrypt=True), decrypt=False)
```

> 3DES 在 2001–2015 年间是「唯一稳妥的兼容选项」，今天则是**遗留兼容代码**。它的 64 位块在长连接下已经不安全（SWEET32），且软件实现约为单 DES 的 3 倍开销。

### AES 的 SPN 结构（1996 年的书里没有，必须补）

```python
# 教学示意，不参与构建、不编译、不运行
def aes_round_summary(state: list[list[int]], key: list[list[int]]) -> list[list[int]]:
    """AES 不是 Feistel，而是代换-置换网络（SPN）的十轮迭代：
       SubBytes（S 盒查表） → ShiftRows（行移位） → MixColumns（列混淆） → AddRoundKey
       最后一轮去掉 MixColumns。AES-128/192/256 分别为 10/12/14 轮。"""
    return [[state[r][c] ^ key[r][c] for c in range(4)] for r in range(4)]
```

> **为什么必须补这一段**：本书第 12–15 章讨论的全部是「如果 AES 存在会怎样」的背景知识，真正的分组密码是 **FIPS 197（2001-11-26）** 里的 Rijndael。Rijndael 的关键设计取舍（SPN 而非 Feistel、可变轮数、128/192/256 位密钥与 128 位块）在 1996 年的书里只能通过对 Blowfish/RC5 的对比间接体会——**这正是「1996 年的书无法预测 AES」的直接证据**。

---

## 版本演进

| 年份 | 事件 |
| --- | --- |
| **1972–1975** | IBM Lucifer 研究；DES 的雏形（16 轮 Feistel，128 位 → 56 位） |
| **1977** | DES 成为 **FIPS 46** 标准 |
| **1990** | 差分密码分析（Biham-Shamir）攻击 FEAL 等算法成功，DES 进入「设计已过期但强度未知」的阶段 |
| **1993** | 线性密码分析（Matsui）出现，把攻击 8 轮 DES 所需数据量降到可实用 |
| **1994** | 本书第 1 版 |
| **1996** | 本书第 2 版：第 12 章已把「DES 何时被破」当作进行时的问题 |
| **1997-09** | NIST 公开征集 **AES**：这是分组密码史上最重要的一次转向 |
| **1998** | **EFF Deep Crack** 用 56 小时、约 20 万美元硬件成本破 DES（12.7 的答案是「2000 万美元以内可以素」） |
| **1999** | DES 挑战赛在 22 小时 15 分内被破（3DES 開始成为常用方案） |
| **2001-11** | **FIPS 197（AES）** 发布；Rijndael 中选 |
| **2005** | 理论证明：2DES 的复杂度远低于「两次单 DES」（中途相遇），3DES 成为唯一安全选项 |
| **2008** | **Debian 的 PRNG 缺陷**影响批量生成的 RSA/DES 密钥 |
| **2011** | **SHA-1 与 CBC 波及其余部分**；SSLv3 被弃用（POODLE 前奏） |
| **2013** | **RC4 的关键恢复攻击**（Knudsen 等）确立；**RFC 7465（2014）全面禁止 RC4** |
| **2016** | **SWEET32**：64 位块（DES/3DES/Blowfish）在长会话下的生日碰撞 |
| **2018** | TLS 1.3 只保留 AEAD，**DES/3DES/RC4/CBC 全部出局** |
| **2024** | FIPS 203/204/205；AES 仍是后量子时代对称侧的基石（唯一不变的结论） |

> 一条必须记住的对照：**AES 于 1997 年才被征集、2001 年才成为标准**。本书 1996 年成书时，第 12–15 章讨论的「下一代算法」完全不是 AES，而 AES 最终采用的 SPN 结构、可变轮数、以及「不需要置换层也能抗差分分析」的设计哲学，都与第 12–15 章的 Feistel 家族截然不同。**这是全书最大的一处历史性错位。**

---

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| *Data Encryption Standard* | NIST FIPS 46-3，1999（最初的 1977 版） | 12.1/12.2 的权威规范 |
| *Cryptanalysis of the DES and Related Cryptosystems* | B. Biham, A. Shamir，*Advances in Cryptology*（JCSS 1991） | 差分密码分析的奠基作，12.4 的来源 |
| *The Design and Analysis of Linear Cryptanalysis*（线性密码分析） | M. Matsui，*Advances in Cryptology* — EUROCRYPT '93 / AES 相关讲义 | 与差分分析对偶的另一半，12.4 的来源 |
| *Cryptanalysis of the Full 16-Round DES* 的实用化工作 | A. Biryukov 等，2001 | 揭示 DES 的实测强度与理论下界的差距 |
| *Effective Key Recovery on Full DES* 及互补性研究 | 关于 DES 互补密钥等价与关键路径的论文 | 12.3 中「DES 有对称性弱点」的学术根据 |
| *The Design of the Rijndael Cipher* / FIPS 197 | J. Daemen, V. Rijmen | AES 的设计书；本目录必须补读 |
| *Triple DES with Independent Keys* 与 meet-in-the-middle 分析 | 关于 2DES 复杂度的经典结论 | 15.1/15.2「双重加密不安全」的证明 |
| *SWEET32: Birthday Attacks on 64-bit Block Ciphers* | 32nd AES/GCM Workshop，2016 | 64 位块在现代长连接下的重生威胁 |
| *The Road to AES*（NIST 的历史叙述与遴选过程） | NIST / *Cryptologia* 相关回顾文章 | 本节「1997 征集 → 2001 标准」的最权威出处 |

---

## 近年研究与工业界开源实践（2015–2026）

**趋势**：分组密码的算法研究几乎停摆——学者转向 AEAD、格密码与侧信道防御；工业界则继续把 DES/3DES/RC4 从代码库里清除，剩下 20 多年的「兼容债」。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `openssl/openssl` | **30844★**（2026-09-25 实测） | `EVP_aes_*` 的全部实现；3DES（`DES-EDE3-CBC`）仍在库里仅为兼容 |
| `jedisct1/libsodium` | **13962★**（实测） | 不含任何 DES/RC4，只有 Salsa/ChaCha 与 AEAD——本书这些章节的「对照组」 |
| `golang/go` | **138993★**（实测） | `crypto/aes`、`crypto/des` 的教科书式实现：CBC/CTR/GCM 一目了然 |
| `pyca/cryptography` | **7784★**（实测） | 复现 ECB 企鹅、3DES 与 AES 对比实验最方便 |
| `C2SP/wycheproof` | **3114★**（实测） | 每种块密码 + 每种模式 × 每种库的攻击用例 |
| `jvdsn/crypto-attacks` | **1285★**（实测） | 差分/线性/积分攻击的可运行实现（12.4 的动手版） |

---

## 常见误区与本书需修正之处

| 问题 | 说明 |
| --- | --- |
| 🔧 **12–15 章的密码列表不是今天的密码库** | IDEA、RC5、Blowfish、CAST、GOST 在今天各自只剩遗产场景；**新项目用 AES-256-GCM 或 XChaCha20-Poly1305** |
| 🔧 **AES 缺席是结构性缺陷** | 全书没有 AES 的一行代码；读完这四章必须立刻补 FIPS 197 与 Rijndael 的设计书，否则会误以为「DES 家族＝分组密码」 |
| 🔧 **3DES 被当作长期方案** | 3DES 有 64 位块（SWEET32）与软件性能问题；NIST 自 2013 年起不再为新的 3DES 使用背书 |
| **「DES 已经安全了几十年」的错觉** | 1999 年 DES 挑战赛在 22 小时内被破；Deep Crack 之后 3DES 又用了十年只是因为它兼容，不是因为它更强 |
| **RC2/RC4 的「变长密钥」优势被高估** | 13.8 的 RC2 与 17.1 的 RC4 都被证明有状态恢复类缺陷；RC4 在 RFC 7465 中被全面禁用 |
| 🔧 **「自己设计分组密码」的暗示** | 14.10–14.12 明明劝阻读者，但本书提供了 30 多种自造算法的例子，反而形成了负面示范；现代结论是：**密码设计必须公开竞赛，不能私造** |
| **级联加密 = 更安全** | 15.7 的并行级联可被中途相遇攻击；**串联（连续使用不同密钥）才可能是安全增加** |
| 🔧 **未覆盖后量子时代的对称密码** | AES 在这场大迁徙里是唯一不变的常量——因为 Shor 算法对它的影响只是常数级（Grover），这恰恰是 2024 年 FIPS 203/204/205 只替换公钥部分的原因 |

---

## 与其他章 / 其他书的联系

- **→ `concepts/密码分析与侧信道.md`**：12.4 的差分与线性分析在专篇里被完整展开；定时攻击与能量分析也在那里。
- **→ 本目录 08 章**：这里的「算法」必须配第 9 章的「模式」才有意义；DES 再强，用错 ECB 也会泄露图像。
- **→ 本目录 11 章**：15.1 的双重加密与中途相遇攻击，是 11.6 复杂度思想的直接应用。
- **↔ `book/计算机程序的构造和解释（原书第2版）/`**：Feistel 轮的 `L, R = R, L ⊕ F(R, K)` 是纯函数式的**不动点迭代**；用 SICP 的流模型可以把「16 轮」写成 `stream of rounds`，从而清楚看到「加密」与「解密」只是把子密钥序列反过来喂——这种「结构决定可逆性」的视角与 SICP 第 3 章讨论的迭代/递归等价性是同一件事。
- **↔ `book/设计模式GoF/`**：3DES 的 EDE 是 **Template Method**（同一套流程、第三个步骤不同）；而 15.7 的级联失败说明**模式组合不等于安全**：装饰器可以任意嵌套，密码学不行。
- **↔ `book/数据库系统概念6/23-XML.md`**：该文讲的 XXE 与序列化安全说明「**解析器/实现层的选择决定安全水平**」，与本节「同一个算法在不同实现下安全级别不同」（如 DES 的硬件无关实现 vs 侧信道脆弱实现）是同一个教训。
- **↔ `book/Java并发编程之美/concepts/伪共享FalseSharing.md`**：AES 的查表实现（T-table）会因缓存未命中而**泄露访问模式**，伪共享则因缓存行共享而**泄露时序**——二者都在提醒：看得见的复杂度常数之外，还有一层看不见的信息流。
