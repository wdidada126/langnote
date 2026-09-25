# CS161 配套项目计划

> 原则：章节 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> 注：不复刻课程原始 Project 源码（尊重官方学术诚信要求），以下为同知识点的自制替代练习。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| L3 访问控制 | Python | 迷你 RBAC 引擎：角色继承 + 策略求值 + 单元测试 | `python -m pytest`（纯标准库） |
| L5–L6 内存攻击 | C + Python | 自制靶题：有意留洞的服务程序 + Python 构造溢出 payload 夺 flag | `make vulnerable`（gcc -m32 -fno-stack-protector） |
| L7 加固对照 | C | 同一靶题开 canary/ASLR/NX 四组合，记录绕过难度差异 | `make hardened`（脚本矩阵跑） |
| L8 对称加密 | Python | ECB 图像加密演示 + padding oracle 攻击模拟器 | `python -m venv` + cryptography 库 |
| L9–L11 公钥与 TLS | Go | 迷你混合加密聊天：ECDH 会话密钥 + AES-GCM + 自签证书 | `go build ./cmd/chat` |
| L13 Web 攻击 | Python/JS | 故意含 SQLi/XSS/CSRF 的笔记应用 + 修复前后对照 + 自制 scanner | `python app.py`（Flask）+ sqlite3 |
| L14 综合设计 | Go | 安全文件分享系统精简版（自制规格）：令牌认证/过期/审计日志 | `go build ./...`，`go test ./...` |
| L15 DNS | Python | DNS 报文解析器 + 缓存投毒模拟（事务ID 熵测量） | `python dns_lab.py`（需 root 抓包或离线 pcap） |
| L17 侧信道 | C | 计时信道 demo：同程序密钥比较的 timing 差异统计 | `make timing`（gcc -O2） |

## 目录约定（后续填充）

```
projects/
  01_rbac/  02_stack_target/  03_hardening_matrix/  04_ecb_oracle/
  05_minisend_tls/  06_vuln_noteapp/  07_fileshare_lite/  08_dns_lab/  09_timing/
```

每个子项目含独立 `Makefile`/`build.sh` 与 `README`（漏洞设定与修复说明）；Windows 下 `-m32` 靶题建议走 Docker/Linux 镜像，脚本本轮只写不跑。
