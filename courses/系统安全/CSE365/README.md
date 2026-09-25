# ASU CSE365 网络安全导论（Introduction to Cybersecurity）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | Arizona State University CSE365: Introduction to Cybersecurity |
| 学校 | Arizona State University |
| 主讲 | Trevor Pounds / Kang Li 等（pwn.college 教研组，Shoumik Lodh 等助教团队） |
| 教材 | 无；以 pwn.college 在线讲义 + Challenge 为主 |
| csdiy 路径 | `系统安全/CSE365` |
| 最新期次 | Spring 2025（站点：pwn.college/cse365-s2025/） |
| 状态 | 骨架 |

- 课程网站：https://pwn.college/cse365-s2025/
- 视频：YouTube @pwncollege；直播 Twitch @pwncollege；Discord 答疑
- 作业：8 个模块、共 444 个 challenges（CTF 形式，难度递增）
- 注意：官方不鼓励上传解题思路（每模块前两题除外），笔记只记概念与通用方法，不写题解。

## 为什么学

- 「做中学」的网络安全导论：课程即 pwn.college dojo，每个知识点都对应可验证的 challenge，反馈密度远超传统讲课。
- 覆盖面精准务实：Linux 滥用、Web 基础、汇编、密码学、Web 注入攻击，是后续 CSE466/6.858 攻防深潜的合格地基。
- CTF 文化入口：Discord 社区活跃，卡关有路；学完即具备打入门 CTF（picoCTF 级别以上）的实战能力。

## 先修与知识联系

- 先修：无硬性要求；建议会基础编程（Python/C）与 Linux 命令行。
- 联系：与 CS161 相比更「攻」更动手；汇编/内存部分与 CSAPP/CS61C 互证；Web 部分是 CS161 Part4 的实战化；后继直通 CSE466（系统安全）、SEED Labs（成体系实验）。

## 讲义章节目录（s2025 模块化课程，按知识域整理为讲/模块）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| M1/L1 | Linux 命令行与程序滥用 | pwn.college 模块讲义（Program Misuse） |
| L2 | 权限提升与 setuid/SUID 滥用 | 同上；课程阅读材料 |
| L3 | 环境变量/路径/共享库劫持类攻击 | pwn.college 讲义 |
| M2/L4 | Web 基础：HTTP 协议、请求/响应语义 | MDN HTTP 文档 + 课程讲义 |
| L5 | Web 服务器与拦截代理（Burp 使用） | 课程讲义 + Burp 文档 |
| M3/L6 | x86 汇编：寄存器与寻址 | 课程汇编讲义 |
| L7 | 汇编：内存布局与控制流 | 同上 |
| M4/L8 | 密码学 I：对称加密与常见误用 | 课程 crypto 讲义 |
| L9 | 密码学 II：非对称、哈希与信任 | 同上 |
| M5/L10 | Web 安全 I：命令注入与 HTML/JS 注入（XSS） | 课程讲义 |
| L11 | Web 安全 II：SQL 注入与栈类注入 | 同上 |
| M6–L12 起 | 综合模块与期末考试（Capture the Flag 式） | 当期公告 |

> 注：pwn.college 以模块→关卡组织，本表按 csdiy 列出的知识域（Program Misuse / Web fundamentals / Assembly / Cryptography / Web security）整理为 12 讲骨架，最终对齐 s2025 页面模块列表。

## 作业与项目（概览）

全部作业为在线 challenge，无法本地复刻；`projects/README.md` 给出每个知识域的自制实验环境与小项目（含 Docker 靶场）。
