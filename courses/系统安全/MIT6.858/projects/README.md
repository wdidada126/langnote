# MIT 6.858 配套项目计划

> 原则：章节 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译。
> 注：不复刻 Zoobar 官方骨架与题解（尊重课程学术诚信），以下均为同知识点自制项目。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| L2–L3 Web 攻防 | Python | 自制含 XSS/CSRF 的书签小站 + 修复版 + 双版本对照测试 | `python app.py`（Flask + sqlite） |
| L5–L6 溢出利用 | C + x86-64 asm + Python | 靶题三件套：ret2win / ret2libc / 单 gadget ROP，pwntools 脚本驱动 | `make targets`（gcc -no-pie -m64），`python exploit_*.py`（Docker ubuntu 环境） |
| L7 沙箱 | C | 迷你 SFI：解释执行受限指针算例子集，掩码法隔离 | `make sfi` |
| L10 特权分离 | Go | 把单体 HTTP 笔记服务拆成前端解析(无密钥)/后端存储两进程，socket 鉴权 | `go build ./cmd/...` |
| L13 污点追踪 | Python | 表达式求值器的动态污点标签传播 demo（source→sink 报告） | `python taint_demo.py` |
| L14 符号执行 | Python | 迷你 concolic 引擎：对含 magic check 的关卡程序自动生成通过输入 | `python concolic.py`（z3-solver） |
| L15 Fuzzing | C + Python | 自制解析器靶（图片头解析）+ 简单覆盖率引导 fuzz 循环，对照 AFL++ 跑 | `afl-clang-fast -O0 parser.c`；无 AFL 时 `python mini_fuzz.py` |
| L16 侧信道 | C + Python | Flush+Reload 原型：共享页读探测 + 比特序列还原 | `gcc -O0 spy.c target.c`（Linux，需 perf 权限或 Docker） |
| L17 安全文件系统 | Go/Rust | SecFS 精简版：本地不可信「服务器」目录 + Merkle 树完整性 + 版本分叉检测 | `go build ./cmd/secfs`，`secfs mount` 以 FUSE 或 CLI 模拟 |
| L19 验证导览 | Python | TLA+ 风格的协议小模型：对认证流程写不变量并枚举检验 | `python model_check.py`（或 TLC 跑 TLA+ 文件） |

## 目录约定（后续填充）

```
projects/
  01_xss_notebook/  02_rop_targets/  03_minisfi/  04_privsep/
  05_taint_demo/  06_concolic/  07_fuzz_parser/  08_flush_reload/
  09_secfs_lite/  10_tla_auth/
```

需要 Linux 内核特性（perf/ASLR 控制/FUSE）的项目一律附 Dockerfile；本轮只写不编译，集中验证稍后统一进行。
