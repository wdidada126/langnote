# SEED Labs 学习要点提纲（骨架）

> 每单元 3–5 条要点；正文笔记按 Lab 完成后填充。

## L1 缓冲区溢出攻击
- setuid root 程序 + 无保护编译选项下，覆盖返回地址跳转到栈上 shellcode。
- NOP sled 与地址猜测：栈基址在关闭 ASLR 的 VM 中可预测。
- shellcode 用 execve("/bin/sh") 构造，避开坏字符。
- 复盘点：环境差异（32/64 位、glibc）导致的失败模式。

## L2 非执行栈攻防
- NX 位使栈页不可执行 → 注入代码路线封死。
- 退路一：ret2libc 复用已有代码；退路二：mprotect 类系统调用改页属性。
- 理解「数据 vs 代码」边界即内存安全的核心不变量。

## L3 绕过 ASLR
- 泄露原语前置：通过格式化字符串/越界读得到运行时地址。
- 部分覆盖（partial overwrite）与 16 位熵的现实破解成本。
- 与 L1 组合完成现代 pwn 的「leak → calc base → hijack」模板。

## L4 格式化字符串攻击
- printf 参数即内存：`%x` 泄露、`%n` 写任意地址。
- 从泄露 canary/返回地址到 GOT 覆写的利用链。
- 防御：编译期 -Wformat、运行期 FORTIFY。

## L5 竞态条件攻击
- TOCTOU：检查与使用之间的窗口期替换符号链接/文件。
- 放大窗口手段：文件系统延迟、CPU 亲和、大量并发线程。
- 防御：原子操作（openat + 权限语义）、mkstemp 模式。

## L6 权限程序滥用
- setuid 程序环境变量信任链事故：LD_PRELOAD 对 suid 失效的原因（AT_SECURE）。
- PATH 与相对路径在特权上下文的重演（CSE365 同源）。
- /etc/passwd、shadow 权限模型与最小特权反思。

## L7 加密基础实验
- OpenSSL 命令行完成 AES/RSA 往返调用，理解填充与模式参数。
- 密钥长度/模式选择对密文形态的影响观察。
- 目标：把 API 使用变成肌肉记忆（与 6.1600 理论对齐）。

## L8 随机数攻击
- `rand()/srand(time)` 可预测种子 → 密钥空间塌缩到一天内秒数。
- CSPRNG 的熵源要求；/dev/urandom 与 getrandom。
- 真实案例视角：WPA/SSL 弱随机历史漏洞。

## L9 ECB 与填充攻击
- ECB 相同明文块 → 相同密文块的图形泄露（企鹅图）。
- CBC bit-flipping：篡改 IV/密文可控改动解密明文。
- Padding oracle：错误信息即侧信道，逐字节解密。

## L10 Hash 长度扩展
- MD/SHA-2 Merkle-Damgård 结构：已知 key+msg 伪造 HMAC 之外的 `hash(key||msg||pad')`。
- 正确姿势：HMAC 或 SHA-3。
- 实验：伪造认证消息的完整复现。

## L11 口令与启动安全
- Linux 启动链：GRUB 密码保护物理攻击面。
- /etc/shadow 哈希格式演进（DES→MD5→SHA-512→yescrypt）与破解成本。
- John/hashcat 在自有样例上的离线破解演示。

## L12 DNS 基础设施
- BIND 服务器加固：视图、递归限制、TSIG。
- 实验环境内搭建权威/递归双角色。
- 为网络类 Lab 的 DNS 攻击提供地基。

## L13 嗅探与 Spoofing
- raw socket 构造伪造源地址的 TCP/UDP 包（scapy）。
- ARP 欺骗中间人：交换机时代仍可行的原因。
- ICMP 重定向与路由劫持演示。

## L14 TCP 会话劫持
- 序列号猜测空间与现代随机化。
- RST 注入拆连接：中间人降级的最小动作。
- 与 TLS 结合：为何应用层认证能补救传输层天真。

## L15 防火墙
- netfilter/iptables 五链模型与规则次序敏感。
- 实验：包过滤规则编写 → 自己的客户端探测绕过。
- nftables 迁移注意点。

## L16 IDS
- Snort/Suricata 规则语言：签名式检测的表达力。
- 用分片/编码/TTL 规避签名检测。
- 误报/漏报权衡：检测即概率。

## L17 VPN 与 TLS MITM
- 自签证书 + ARP 欺骗打通 TLS 中间人（前提：客户端无固定）。
- IPsec 隧道 Lab 理解 ESP/AH；证书固定为何关键。
- 与 PKI Lab 互证信任链。

## L18–L20 Web 三件套
- SQL 注入：从绕过登录到 UNION 拖库（本地靶）。
- XSS/CSRF：凭证自动附带 + 数据当代码的组合灾难。
- 会话固定与劫持：Cookie 属性矩阵实验。
- 修复任务与攻击任务成对出现，形成「攻防双写」笔记法。

## L21 PKI/DNSSEC/HTTPS
- 用自造 CA 全链路签发，证书验证逐步拆解。
- DNS 欺骗下 HTTPS 是否安全？取决于信任锚暴露面。
- DNSSEC 配置实验：签名区与校验器。

## L22 Android 安全
- 权限模型与 manifest 声明即攻击面。
- Content Provider 未设权限导致的数据泄露复现。
- 移动沙箱与 Linux uid 沙箱的哲学差异。

## L23 侧信道
- 缓存计时：Prime+Probe/Flush+Reload 复现密钥位推断。
- Spectre 迷你 Lab：分支训练读内核内存（VM 内）。
- 结论：隔离必须覆盖微结构状态。

## L24 防御与前沿专题
- ASan/UBSan/CFI 重编译旧靶题，量化各缓解的拦截率。
- 容器逃逸/云元数据 Lab：新基础设施的攻击面。
- 区块链/无线 Lab 选做，记录威胁模型变化。
