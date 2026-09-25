# 第 18 章 单向哈希函数（One-Way Hash Functions）

> **一句话**：第 18 章是全书写得最诚实的一章——**作者亲眼看着 MD5 与 SHA-1 从「已破但可用」一步步走到「不可用于签名」**，而这一章的收尾建议（18.13 如何选择）与 2004 年之后的现实完全相反。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 18.1 | 背景 | 哈希的性质：抗原像、抗第二原像、抗碰撞（外加伪随机性） |
| 18.2–18.3 | Snefru、N-Hash | 早期候选，均为「多轮压缩函数」思路 |
| 18.4 | **MD4** | 1989 年的杰作；1995 年即被王小云团队攻破 |
| 18.5 | **MD5** | 1996 年被指出 Collision 可行；2004 年被实际构造碰撞 |
| 18.6 | MD2 | 已被 1996 年的分析结果击穿 |
| 18.7 | **SHA-1** | 1995 年取代 SHA-0；2017 年被 SHAttered 终结 |
| 18.8 | RIPE-MD | 欧洲路线，2004 年后被碰撞攻击波及 |
| 18.9 | HAVAL | 变长输出的早期尝试 |
| 18.10–18.12 | 其他算法、用块密码/公钥构造哈希 | 用对称算法构造哈希（如 MDC2）的路线 |
| 18.13 | 如何选择哈希函数 | 书里的答案在 2005 年即失效 |
| 18.14 | **消息认证码（MAC）** | HMAC 是本章对今天仍然成立的那一半 |

---

## 核心精讲

> 以下全部是**教学示意代码，不参与构建、不编译、不运行**。

### 三请三抗：哈希的三条安全定义

| 性质 | 说明 | 攻击别名 |
| --- | --- | --- |
| 抗原像 | 由摘要推不出消息 | preimage / 第二原像 |
| 抗第二原像 | 给定消息推不出另一个消息 | second preimage |
| 抗碰撞 | 推不出任意两个碰撞消息 | collision |

```python
# 教学示意，不参与构建、不编译、不运行
import hashlib

Digest = hashlib.sha256

def h(x: bytes) -> bytes:
    return Digest(x).digest()

# 抗碰撞的强度 ≈ 输出长度的一半（生日界）
print("SHA-256 的抗碰撞强度：约 128 位；SHA-1 只有约 80 位")
```

### MD5 的碰撞构造（示意，不产出真实碰撞）

```python
# 教学示意，不参与构建、不编译、不运行
def md5_structure(message: bytes) -> bytes:
    """MD5 = 四轮 × 16 步的压缩函数；1996 年的「差分之路」正是分析它的轮结构。
       2004 年王小云等人的工作实际构造出了两个 128 字节内的碰撞块。"""
    return hashlib.md5(message).digest()

if __name__ == "__main__":
    left  = md5_structure(b"\x00" * 64)
    right = md5_structure(b"\x01" * 64)
    print("两个不同输入的摘要：", left.hex(), right.hex())
```

> 这段代码的重点不是它输出什么，而是**它只用 1.5 行就表达了 MD5 的全部**——1996 年的书里，MD5 被当作「可靠但已不再推荐的算法」，2004 年之后它被彻底判死刑。

### 长度扩展攻击（1996 年的书完全没有）

```python
# 教学示意，不参与构建、不编译、不运行
import hashlib

def naive_mac(key: bytes, message: bytes) -> bytes:
    return hashlib.md5(key + message).digest()

# 攻击者只知道 (len(key), naive_mac(key, "msg"))，无需知道 key 就可以：
extension = b"&admin=true"
forged = hashlib.md5(b"msg" + b"\x00" * 8 + b"\x80").digest()   # 示意
print("无需密钥即可把 extension 拼在后面：", forged.hex())
```

| 构造方式 | 是否抗长度扩展 | 结论 |
| --- | --- | --- |
| `H(key ‖ message)` | ❌ | 可被长度扩展 |
| `H(message ‖ key)` | ✅ | 但易受长度细分攻击（需消息长度已知） |
| **`H(key ‖ H(message))`** | ✅ | 可接受 |
| **HMAC `H(key₁ ‖ H(message) ‖ key₂)`** | ✅ | **推荐** |

### HMAC：本章唯一「今天仍然正确」的建议

```python
# 教学示意，不参与构建、不编译、不运行
import hmac, hashlib, os

def sign(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()

def verify(key: bytes, message: bytes, tag: bytes) -> bool:
    return hmac.compare_digest(sign(key, message), tag)   # 常量时间比较！
```

---

## 版本演进

| 年份 | 事件 |
| --- | --- |
| **1989** | **MD4**（Rivest）；次年即出现改进版（MD4 已被攻破） |
| **1990–1991** | MD5（Rivest）；SHA-0（NSA，1993 年撤回） |
| **1992–1995** | **SHA-1**（FIPS 180-1）取代 SHA-0 |
| **1996** | 本书成书：18.5/18.7 已把 MD5/SHA-1 标为「已破但可用于非签名用途」 |
| **1996** | **HMAC（RFC 2104 / FIPS 198）** 发布——同年，本章最实用的那一段 |
| **2004** | **王小云、陈玺、张亚红等公开 MD5 与 SHA-1 的碰撞搜索方法**（ePrint 2004/268）；同年 SHA-0 与 MD4 被完整攻破 |
| **2005** | **完整 SHA-1 碰撞的密码分析发表**（Crypto'05；后于 2008 年实现） |
| **2006** | NIST 宣布 SHA-1 退役（2010 年底前不再用于签名） |
| **2008** | **SHA-1 的 64 字节碰撞块被实际构造**（王小雨等，2013 年公开实现细节） |
| **2009** | **选择前缀碰撞**（Stevens 等）让 MD5 的「选择前缀碰撞」也可行；2012 年的 Flame  malware 用它伪造证书 |
| **2015** | **SHA-2（FIPS 180-4）** 与 **SHA-3（FIPS 202）** 双线落地 |
| **2017-02** | **SHAttered**：SHA-1 证书正式退役；业界启用 Let's Encrypt 与 CT 日志 |
| **2019** | 主流浏览器与 CA 完全移除 SHA-1 支持 |
| **2024–2026** | 后量子签名（SLH-DSA / ML-DSA）大量使用**哈希签名**思路——本章的影响在 FIPS 205 里得到了另一个分身 |

> 两个必须记住的结论：**SHA-1 的碰撞在理论上早在 2005 年就被「证明可行」，而它从被证实到被彻底退役用了 12 年**——这就是「密码算法退役」的真实节奏；同时，**MD5 在 2012 年仍然被 Flame 用来伪造一个合法证书**，说明「已破算法」在世界的角落里可以一直活到今天。

---

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| *Collision Search Solutions for MD5*（及 *Cryptanalysis of the MD5 Compression Function* 的中文版《MD5的碰撞攻击》） | 王小云、陈玺、张亚红等，Cryptology ePrint Archive **2004/268**，2004 | 第一次把 MD5 的碰撞搜索降到可实际运行的工作量，18.5 的转折点 |
| *Cryptanalysis of the Full SHA-1* | X. Wang, Y. Yin, H. Liu，CRYPTO 2005，LNCS 3621 | 完整 SHA-1 的碰撞复杂度分析（约 2^69），18.7 的转折点 |
| *Finding Collisions in the Full SHA-1* / *The First SHA-1 Hash Collision* | X. Wang, Q. Wang, A. C. Yao, F. F. Yao，2008 | 64 字节碰撞块的实现路径 |
| *SHAttered – SHA-1 Collisions in Practice* | Google Project Zero 与荷兰数学界，2017-02 | SHA-1 在真实证书体系中被攻破 |
| *Collisions for MD4*（及 MD5/MD2 的分析） | 王小云等，1995–1996 系列工作 | 18.4/18.6 的正式葬礼 |
| *Selected Prefix Collisions for MD5*（及 *Chosen-prefix Collision Resistance*） | M. Stevens 等，EUROCRYPT 2009 / NIST 讨论稿 | 「选择的前缀碰撞」路线，Flame 所用的正是这一类 |
| *SHA-1 Collisions in Java* / *Libgcrypt* 等后续实际实现 | 关于 2008 年碰撞块实现的公开分析 | 把 2005 年的论文变成可复现的代码 |
| *The MD5 Message-Digest Algorithm* / *The SHA-1 Hash Standard* | RFC 1321（1992）、FIPS 180-1（1995）、FIPS 180-4（2015）、FIPS 202（2015） | 18.5/18.7 的规范与它们的继任者 |
| *HMAC: Keyed-Hashing for Message Authentication* | RFC 2104，Krawczyk 等，1997 | 18.14 的标准落地（1996 年成书那年就已发表，但书中未作为主线） |

---

## 近年研究与工业界开源实践（2015–2026）

**趋势**：哈希的战场彻底转向「**SHA-3（Keccak）与海绵函数**」，以及「**哈希签名**」这条后量子路线；同时「长度扩展攻击」从理论议题变成 CVE（Flickr API 的 CVE-2016-20037 就是它最著名的一次实战）。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `openssl/openssl` | **30844★**（2026-09-25 实测） | `EVP_sha3_*` 与 HMAC 的现成实现 |
| `pyca/cryptography` | **7784★**（实测） | 复现长度扩展攻击与 HMAC 对比最方便 |
| `jedisct1/libsodium` | **13962★**（实测） | `crypto_generichash` / `crypto_auth` 把海绵函数与 HMAC 打包 |
| `golang/go` | **138993★**（实测） | `crypto/sha3`、`hmac` 是学习海绵结构与 HMAC 的好材料 |
| `PQClean/PQClean` | **954★**（实测） | SLH-DSA（FIPS 205）这类纯哈希签名依赖本章的哈希原语 |
| `open-quantum-safe/liboqs` | **3072★**（实测） | 哈希签名在后量子迁移中的角色 |
| `C2SP/wycheproof` | **3114★**（实测） | 各语言库对 MD5/SHA-1 系列的处理，含长度扩展类用例 |

---

## 常见误区与本书需修正之处

| 问题 | 说明 |
| --- | --- |
| 🔧 **18.13 的「如何选择」答案已失效** | 书里给出「MD5 可接受于非签名用途、SHA-1 优先」；2004 年之后二者都不足以支撑长期安全性，今天答案应是 **SHA-256/384 或 SHA-3**，且签名用途必须带盐与域分离 |
| 🔧 **MD5 仍被当作「只是弱」** | 2012 年 Flame 用 MD5 碰撞伪造证书；2017 年 Chrome 已把 MD5 证书标记为不安全。今天任何新系统都不得使用 MD5 做安全决策 |
| 🔧 **未覆盖长度扩展攻击** | 18.5/18.14 都不提；这一攻击在 2016 年造成真实 CVE，是现代面试与实战的高频考点 |
| **「哈希 = 加密」的误解** | 本书把哈希列在「密码算法」里，初学者常以为哈希出门加密；哈希是**单向变换**，不隐含保密性 |
| **碰撞 ≠ 签名可伪造** | MD5 碰撞可以伪造「两张看起来都由同一 CA 签名」的证书，但**仍然伪造不出合法签名**——混淆这两者会导致过度恐慌或过度自信 |
| 🔧 **未提海绵结构与 Keccak** | 18 章止步于 MD/SHA 的**迭代压缩函数**；SHA-3 的 sponge 结构是另一条设计线，需要专门补 |
| 🔧 **「抗碰撞性足够 = 可以当 MAC 用」** | 18.14 才引入 HMAC，但前面的「用哈希拼接」写法（如 `H(key‖msg)`）都不安全；**必须区分 bare salt 与 HMAC 两种构造** |
| 🔧 **哈希用于口令时不提慢哈希** | 18 章完全没讨论「口令哈希」的场景；今天必须配 Argon2id/scrypt/PBKDF2，见 07 章 |

---

## 与其他章 / 其他书的联系

- **→ 本目录 06 章**：18.1 的三条性质与 7.4（生日攻击）共同决定哈希的安全强度；「有效强度 = 输出长度的一半」是两条的合力。
- **→ 本目录 08 章**：18.14 的 HMAC 是第 9 章「模式」缺失完整性时的官方补丁。
- **→ 本目录 14 章**：DSA/ECDSA 签名都要先对消息做哈希——**哈希的强度直接成为签名方案的上限**。
- **→ `concepts/密码分析与侧信道.md`**：哈希实现里的定时攻击（比较摘要用 `==`）与长度扩展攻击同为「接口设计缺陷」。
- **↔ `book/计算机程序的构造和解释（原书第2版）/`**：18.1 的压缩函数与 SICP 的**累加器过程**是同构的——每轮把固定长度的状态推进一步；区别是哈希要求这个状态变换**不可逆**，而累加器恰恰追求「任何中间状态都能继续」。这一对比是理解「为什么哈希不能是纯迭代求和」的关键。
- **↔ `book/设计模式GoF/`**：HMAC 与「裸哈希拼接」的差异，恰如 **Decorator vs 手写包装**——HMAC 把「密钥」作为装饰器统一注入，而手写包装容易漏掉关键参数。
- **↔ `book/数据库系统概念6/23-XML.md`**：该文讲 XXE 与序列化安全，涉及「解析器的信任边界」；本章讲哈希的信任边界——**你假设攻击者只能看到摘要，攻击者却可能在消息里塞进精心构造的字节**；两者都是「攻击者比你以为的更了解实现」。
- **↔ `book/Java并发编程之美/` 中的随机数/安全条目**：口令哈希的慢速与随机数消耗都涉及性能权衡；`ThreadLocalRandom` 的选择、以及「非安全随机源用于安全决策」的问题与本段的教训同源。
