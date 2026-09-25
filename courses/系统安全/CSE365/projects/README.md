# CSE365 配套项目计划

> 原则：模块 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> pwn.college 的 challenge 本身在线且不可复刻，本项目计划为各知识域搭建**本地自建靶场 + 利用/防御双向练习**，全部作用于自有环境。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| L1–L2 程序滥用/提权 | C + Shell | 自制 setuid 漏洞程序（缺 euid 检查）+ 修复版 + 检测脚本 | `make suid`（gcc，Docker ubuntu 内启用 setuid） |
| L3 劫持实验 | C + Shell | PATH/LD_PRELOAD 劫持演示脚本集（含防御对照） | `bash demos/01_path_hijack.sh` |
| L4–L5 HTTP | Python | 手搓 mini HTTP 服务器（不依赖框架）+ 原始 socket 客户端报文构造 | `python miniserv.py` / `python rawhttp.py` |
| L6–L7 汇编 | x86-64 asm + C | 写 10 个 C 片段对照反汇编练习册 + gdb 步进脚本 | `make asm-lab`（gcc -S / nasm） |
| L8–L9 密码学 | Python | ECB 企鹅图生成器、口令哈希成本计时器（bcrypt/argon2 对比）、弱随机演示 | `python crypto_lab/*.py`（cryptography+bcrypt） |
| L10 XSS/命令注入靶 | Python/JS | 故意含反射型/存储型 XSS 与命令注入的留言板，附 CSP 修复版 | `python app_vuln.py` / `python app_fixed.py`（Flask） |
| L11 SQLi 靶 | Python | 拼接 SQL 的登录/搜索页 + 参数化修复版 + 自制盲注练习脚本（仅打本地靶） | `python sqli_lab.py`（sqlite3） |
| L12 综合链 | Docker Compose | 多服务迷你企业站点（web+db+内部服务）复刻入门攻击链演练环境 | `docker compose up`（附说明文档） |

## 目录约定（后续填充）

```
projects/
  01_suid_targets/  02_hijack_demos/  03_http_manual/  04_asm_workbook/
  05_crypto_lab/  06_xss_board/  07_sqli_login/  08_chain_docker/
```

README 中统一声明：仅用于自有靶场学习，禁止对任何未授权系统使用；Windows 宿主上的 Linux 实验一律走 Docker，脚本本轮只写不跑。
