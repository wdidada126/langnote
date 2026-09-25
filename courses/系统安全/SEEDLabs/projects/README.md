# SEED Labs 配套项目计划

> 原则：主题 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> SEED 官方 Lab 材料本身开源（CC 许可），但本计划仍以「自制环境 + 自制靶」为主，避免直接搬运题解；官方 VM/Docker 仅作为对照基线。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| 环境 | Docker/Shell | 一键起「SEED 风格」实验底座：关 ASLR、32 位库、内网多机的 compose | `docker compose up -d`（Dockerfile + setup.sh） |
| L1–L3 溢出系列 | C + x86 asm + Python | 自制 setuid 靶（-m32 -fno-stack-protector）+ scapy/pwntools 利用脚本 + 逐层开 NX/ASLR/canary 复测 | `make vuln && python exploit.py` |
| L4–L5 格式化字符串/竞态 | C | fmt 漏洞日志程序（泄露+ GOT 写）；TOCTOU 备份脚本靶 + 竞态放大脚本 | `make fmtlab racelab` |
| L7–L10 密码系列 | Python | 弱随机密钥破解器、ECB 企鹅生成器、CBC 翻转与 padding oracle 服务端/客户端对、长度扩展伪造器 | `python crypto/*.py`（cryptography + hashpump 思路自实现） |
| L13–L14 网络系列 | Python (Scapy) | ARP 欺骗中间人 + TCP RST 注入演示（全内网 Docker 拓扑） | `python net/*.py`（容器内 root） |
| L15–L16 防火墙/IDS | Shell + Snort 规则 | 规则集编写 + 自制流量回放验证绕过/检测 | `nft -f rules.nft`、`snort -r pcap/` |
| L18–L20 Web 系列 | Python/JS | 含 SQLi/XSS/CSRF/会话固定四类洞的论坛靶 + 修复 PR 对照 | `python app.py`（Flask） |
| L21 PKI | Shell + OpenSSL | 三级 CA 脚本链（root→intermediate→leaf）+ 自签 HTTPS 站点 | `bash pki/setup.sh` |
| L22 Android | Java/Kotlin | 权限缺失的 ContentProvider 示例 App（仅本地 AVD 实验） | Gradle 构建文件（本轮只写不跑） |
| L23 侧信道 | C + Python | Flush+Reload 迷你复现：共享页读写计时直方图 | `make sidechan`（Linux 容器） |
| L24 防御度量 | C + Makefile 矩阵 | 同一靶题 × {no-pie, pie+canary, CFI, Rust 重写} 的加固对照报告脚手架 | `make matrix` |

## 目录约定（后续填充）

```
projects/
  env/                    # docker-compose 底座
  01_overflow/  04_fmt_race/  07_crypto/  13_network/
  15_fw_ids/  18_web/  21_pki/  22_android/  23_sidechan/  24_hardening/
```

每个子项目独立 build 脚本与 README（威胁设定/预期观察/自查清单）；ASLR 开关、setuid 等操作仅在 Docker/VM 内执行；Windows 宿主统一走 WSL2/Docker，脚本本轮只写不编译。
