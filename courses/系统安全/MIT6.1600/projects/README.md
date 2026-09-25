# MIT 6.1600 配套项目计划

> 原则：模块 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> 与课程 6 个 Lab 的知识点保持同构，但为自制实现，不搬运课程原始骨架代码。

| 章节（模块） | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| M1 认证 L2–L3 | Python3 | 口令强度计 + 加盐慢哈希存储（argon2 对照 bcrypt）；哈希碰撞演示工具 | `python -m venv .venv` + `pip install argon2-cryptography?` → `python pwlab.py` |
| M1 协议 L4 | Python3 | NS 协议模拟器：跑通正常流程并注入中间人重放，观察失败点 | `python ns_protocol.py`（纯标准库） |
| M2 对称 L5 | Python3 | CBC 填充 oracle 攻击器：对玩具服务端逐字节解密 | `python padding_oracle.py`（cryptography 库） |
| M2 公钥 L6–L7 | Python3 | 小素数 ECDH + MITM 演示；RSA 教科书加密 vs OAEP 对照 | `python ecdh_demo.py / rsa_demo.py` |
| M2 TLS L9 | Go | 迷你 TLS 握手可视化服务器：打印消息流并强制走 1.3 | `go build ./cmd/tlsviz` |
| M3 平台 L10–L12 | C + Python | setuid 程序权限检查审计 + 能力最小化改造前后对照 | `make platlab`（Linux/Docker 环境） |
| M4 软件 L13–L15 | C + Python | 自制含 UAF 靶题 + AFL++ 脚本挂上跑通崩溃发现 | `afl-gcc -O0 target.c`（Docker: ghcr.io/aflnet? 官方 afl++ 镜像） |
| M5 人 L16 | Python/HTML | 钓鱼邮件识别小实验：本地模拟页 + 用户点击日志统计 | `python phish_lab.py` |
| M5 隐私 L17 | Python | 拉普拉斯机制聚合直方图：不同 ε 下的可用性/隐私曲线 | `python dp_hist.py` + `python plot.py` |

## 目录约定（后续填充）

```
projects/
  01_passwords/  02_ns_protocol/  03_padding_oracle/  04_ecdh_rsa/
  05_tlsviz/  06_platform_audit/  07_uaf_fuzz/  08_phish_stats/  09_dp_hist/
```

各子项目附 `README.md`（威胁设定 + 预期观察）与独立 build/run 脚本；涉及内核/特权实验统一给 Dockerfile 以保证可复现，本轮只写不编译。
