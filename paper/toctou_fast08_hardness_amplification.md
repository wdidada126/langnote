# Portably Solving File TOCTTOU Races with Hardness Amplification

> 本文件由 `2026/202609/20260922.md` 日常笔记中提取，2026-09-25 整理。
> 全文（18 页）已下载并逐页解析，以下代码与数据均出自论文正文。

## 元信息

| 项目 | 内容 |
|------|------|
| 标题 | Portably Solving File **TOCTTOU** Races with Hardness Amplification（会议版）<br>Portably Solving File Races with Hardness Amplification（期刊版，标题去掉了 TOCTTOU） |
| 作者 | Dan Tsafrir（IBM Research, Yorktown Heights, NY）<br>Tomer Hertz（Microsoft Research, Redmond, WA）<br>David Wagner（UC Berkeley, Berkeley, CA）<br>Dilma Da Silva（IBM Research, Yorktown Heights, NY） |
| 会议 | FAST '08: 6th USENIX Conference on File and Storage Technologies，2008-02-26~29，San Jose, CA |
| 会议页码 | pp. 189 – 206（18 页） |
| **荣誉** | 🏆 **Best Paper — Pat Goldberg Memorial Best Paper Award** |
| 期刊版 | ACM Transactions on Storage (TOS), Vol.4, No.3, Article 9, pp.9:1–9:30，2008-11-24 |
| **DOI（期刊版）** | **10.1145/1416944.1416948** |
| dblp key | `conf/fast/TsafrirHWS08` / `journals/tos/TsafrirHWS08` |
| 开放获取 | ✅ USENIX 开放获取 |
| 全文 PDF | https://www.usenix.org/legacy/events/fast08/tech/full_papers/tsafrir/tsafrir.pdf |
| 全文 HTML | https://www.usenix.org/legacy/events/fast08/tech/full_papers/tsafrir/tsafrir_html/index.html |
| 演示音频 | USENIX 提供 MP3 |
| 后续工作 | IBM 技术报告 RC24572：《Portably preventing file race attacks with user-mode path resolution》（2008-06），**确定性**版本，开销显著降低 |
| Shepherd | Mary Baker |
| 致谢 | 感谢 Nikita Borisov、Alan Hu、Ethan Miller、Wietse Venema、Erez Zadok 对早期版本的反馈 |

### BibTeX

```bibtex
@inproceedings{tsafrir2008portably,
  author    = {Tsafrir, Dan and Hertz, Tomer and Wagner, David and Da Silva, Dilma},
  title     = {Portably Solving File {TOCTTOU} Races with Hardness Amplification},
  booktitle = {6th {USENIX} Conference on File and Storage Technologies ({FAST} '08)},
  pages     = {189--206},
  year      = {2008},
  note      = {Best Paper (Pat Goldberg Memorial Best Paper Award)}
}

@article{tsafrir2008portablytos,
  author  = {Tsafrir, Dan and Hertz, Tomer and Wagner, David A. and Da Silva, Dilma},
  title   = {Portably solving file races with hardness amplification},
  journal = {{ACM} Transactions on Storage},
  volume  = {4}, number = {3}, pages = {9:1--9:30},
  year    = {2008},
  doi     = {10.1145/1416944.1416948}
}
```

## 一句话结论

> 把路径解析**从「按行遍历」改成「按列遍历」**——不再每轮重新解析整条路径，而是**一个路径分量一个分量地啃，每个分量连续做 K 次**——就能让 Dean & Hu 的概率式 K-race 重新变得不可攻破，即使用「文件系统迷宫」也不行，纯用户态、不改内核、可移植。

## 核心笔记

### 1. 论文要解决的真正问题

前面四十年研究都在「**找出**漏洞」，没人帮程序员在**现有系统上修好**一个已知的 TOCTOU。作者把已有方案归为四类：

| 类别 | 代表工作 |
|------|----------|
| **静态检测** | Bishop（模式匹配找 check/use 对）、ITS4、Eau Claire、MOPS、RacerX、Engler 系列 |
| **动态检测** | Ko & Redmond（内核打日志事后分析）、Wei & Pu（穷举 Linux 所有 TOCTOU 对）、IntroVirt（VM 检查点重放事后判定） |
| **动态防护** | RaceGuard（Cowan 2001，内核缓存「stat 发现不存在」的文名）、Tsyrklevich & Yee（2003，伪事务挂起干扰进程）、Pu & Wei EDGI |
| **新 API** | `O_RUID`（Dean & Hu）、`faccess`（Bishop）、`O_NOFOLLOW`、**事务型文件系统**、Mazières & Kaashoek 的「全 FD 化」编程范式 |

**为什么修起来这么难**（Section 2.3，这段最值得读）：

- ❌ `set*uid` 切换身份后再 `open` —— Dean & Hu 原话：`setuid` 系列是 **"rats nest"**，不同 Unix 同名同参的系统调用语义不同，甚至可能**静默失败**，不可移植
- ❌ `open` 后用 `fstat` 代替 `access` —— 行不通。文件访问权限不是单个 inode 的权限位，而是**路径上每一级目录权限的合取**。文件 `x/y` 中若 `x` 仅属主可访问，则他人即便 `fstat`（root 调用）显示可读也不该能读
- ❌ fork 子进程降权后 open，再通过 Unix domain socket 传回 fd —— 降权本身不可移植；且**光传 fd 就够呛**：`msg_accrights` 被 POSIX 换成 `msg_control` 数组，但 Solaris/HPUX 保留旧版为默认；RFC 3542 又定义了一套宏，Linux 强制但部分宏尚未标准化 → 代码里全是 `#ifdef`
- ❌ Dean & Hu 的 K-race —— 见下，被迷宫打穿

### 2. Dean & Hu 的 K-race（2004，被攻破的那个）

借用了密码学里的 **hardness amplification** 思想：拿一个「有点难」的问题造一个「非常难」的问题。

- 「有点难」= 在 `access` 与 `open` 之间的窗口内完成一次文件替换
- 「非常难」= 连续成功 **2K+1 次**

K-race 流程：一次标准 `access` + `open`，然后 **K 轮加固**，每轮再 `access` + `open`，并校验当前打开的文件与上一轮相同。`K=0` 时退化为原始 TOCTOU 竞态。

### 3. 文件系统迷宫攻击（Borisov et al., USENIX Security 2005）

论文：*"Fixing races for fun and profit: how to abuse atime"*。

**迷宫构造**：一条超长符号链接链，需要内核解析约 **300MB** 目录数据才能完成路径解析。

**攻击原理**（妙在把 atime 当侧信道）：

1. 内核遍历符号链接时会**更新每个链接的 atime**
2. 路径解析所需的目录项只要有一个不在缓存里，发起调用的进程就会**阻塞睡眠等 I/O**
3. 攻击者建 `2K+2` 个目录 `dir1..dir2K+2`，各藏一个新迷宫；奇数号迷宫出口指向公开文件，偶数号指向**受保护文件**；再用符号链接 `activedir` 指向 `dir1`
4. 反复 poll `activedir/sentry` 的 atime → 一旦发现更新，就知道受害者的 `access` 已经进入飞行状态 → 把 `activedir` 切到 `dir2` → 受害者 I/O 完成、`access` 成功返回 → 接着 `open` 时重演……
5. 一路骗到 K-race 全部系统调用完成，成功打开受保护文件

**增强手段**：并行跑 `grep -r anystring /usr > /dev/null` 刷掉文件系统缓存。

**连随机化都打穿了**：Borisov 等人还考虑过「在加固循环里随机翻转 access/open 顺序」这一技术上正确的防御，并通过 **Solaris 9 的 `/proc/pid/psinfo`** 读出目标进程当前系统调用号，从而推断正在执行哪个调用，再次击败。

> 作者的关键判断：**迷宫是一类通用方法，能「确定性」地赢下大量 TOCTOU 竞态——概率很小的时代结束了。**

### 4. 本文方案：列优先 K-Race（CKR）

**关键洞察**：`open`/`stat`/`chdir`/`access`/`chown` 这些吃文件名的系统调用，本质上是 **O(n) 算法**（n = 路径分量数，含需递归展开的符号链接）。要解析 n 分量路径，就得顺序走过 n 个 inode。

对于 `/f1/f2/f3`、K=2：

```
行优先（Dean & Hu）： /, f1, f2, f3, /, f1, f2, f3     ← 每轮重解析整条路径
列优先（本文）：      /, /,  f1, f1,  f2, f2,  f3, f3   ← 一个分量连做 K 次
```

行优先为什么输：迷宫把 n 做得极大，导致**两次「相邻访问」同一 inode 之间的时间被拉得很长**，攻击者有充足时间动手脚。

列优先为什么赢：**对手不再能控制相邻两次访问同一 inode 的间隔**。该 inode 大概率整段 K-race 期间都躺在缓存里——而连续两次迭代中**只要有一次命中缓存就足以挫败攻击**。竞态重新变「公平」了。

**论文给出的完整源码**（这也使得它比绝大多数安全论文可复现得多）：

| 函数 | 作用 |
|------|------|
| `chop_1st(char *path)` | 切掉相对路径的第一个分量，返回剩余部分（相对形式，无前导 `/`） |
| `is_symlink(atom, target[], stat*, bool*)` | `lstat` 该 atom；若是软链则 `readlink` 取目标（递归处理）；若是硬链则记录 `stat` 结构作为后续比对基准 `s0` |
| `atom_race(atom, s0)` | **安全性全部归结于此**。先 `access`+`open`+`fstat` 得 `s1`，校验 `s0 == s1`；再进 K 轮加固，每轮比对 `s0==s1==s2`（`s2` 来自 `lstat`） |
| `access_open(...)` | 列优先遍历主过程：逐分量推进，遇软链**递归调用自身**，遇硬链做 `atom_race`；拿到有效 fd 后 `fchdir` 进入下一层 |

**为什么必须三个 stat 结构全等**（`s0 = s1 = s2`）：只校验 `s1 == s2` 能确定「被 lstat 的和被 open 的是同一个文件」，但还不够——若不同时校验 `s0`，攻击者只需赢两次竞态：① `is_symlink` 判定 `myfile` 非软链后，初始 `access` 前把它换成指向目标文件的软链；② 初始 `open` 后换回来；③ 后续所有加固轮次躺赢。

### 5. 实验：给自己上强度的「暴露型防守方」

作者没有只测迷宫，而是构造了一个**远比迷宫强的假想攻击**：防守方主动把自己暴露——通过共享内存把循环计数暴露给攻击者，使攻击者拥有**完全、即时的知识**并能**完美同步**（Section 5）。

**度量公式**：连赢 k 轮所需期望时间

```
Bk = t · p^(-k)
```

（几何分布期望。举例：`t=1ms`、`p=0.1` 时，`B2/B3/B4/B5` = 100 毫秒 / 1 秒 / 167 分钟 / 28 小时）

**测试机（5 台，横跨老新架构与三家 OS）**：

| CPU | OS | CPUs | 主频 | 内存 |
|-----|-----|------|-------|------|
| UltraSPARC-II | Solaris 8 | 4 | 448 MHz | 2 GB |
| Pentium-III | Linux 2.4.26 | 4 | 550 MHz | 1 GB |
| Power4 | AIX 5.3 | 8 | 1450 MHz | 16 GB |
| Dual Core AMD | Linux 2.6.22 | 4 | 2200 MHz | 8 GB |
| Intel Core 2 Duo | Linux 2.6.20 | 2 | 2400 MHz | 4 GB |

**规模**：攻击者两个可调参数各取 22 种取值 → `22² = 484` 组实验 × 同时攻击者数 1–6 → **每台机器 2,904 次运行**。

**结果**：
- 单轮获胜概率 p 最高接近 **6%**（Sparc/Solaris 三攻击者的场景、Power4/AIX 两攻击者的场景）——注意这是**单轮**，不是连赢 K 轮
- 攻击者各种增强手段（并发 `grep -r` 刷缓存、数万文件的大目录、并发多个防守方、把 Linux 内核内存压到 256MB）**均无显著影响**
- 唯一有效的是 Wei & Pu 指出的「**多攻击者并发打同一个文件**」，论文专门测了 1–6 个并发攻击者
- **Figure 13 是全文最有画面感的一张图**：K=7 / 8 / 9 时，攻击者连赢 K 轮的期望时间以**年**为单位纵轴对数刻度铺开，**K=9 时达到数十至数百万年量级**

### 6. 泛化（Section 7）

- **check-open 工具**：把 `access` 换成函数指针参数，调用方可传 `access`、`stat` 或任何自定义检查 → 可考虑加进 libc
- **check-use 通用工具**：把硬度放大**从核心算法里剥离，变成可选策略插件**。剩下的核心是**用户态路径解析遍历**——逐分量 `fchdir`，遇软链递归，且保证只 `fchdir` 进硬链目录（对下一级 atom 目录 `lstat` 得 `s1` → `open` → `fstat` 得 `s2` → 校验同一文件对象）。接口为四个函数指针：`F_dir_chk`、`F_link_chk`、`F_last_chk`、`F_last_use`
- **为什么聚焦 `open` 作为「使用」操作并不窄**：**文件描述符到文件对象的绑定是不可变的**，天然免疫 TOCTOU。一旦安全拿到 fd，后续就能用 `fchown`/`fchmod`/`fchdir`/`fstat`/`ftruncate` 这一整族安全调用，替代 `chown`/`chmod`/`chdir`/`stat`/`truncate` 这些吃文件名、易受攻击的版本

### 7. 结论原文摘录

> "**The POSIX API is broken**: Its semantics inherently promote TOCTTOU races between check-use operations and make systems vulnerable to malicious attacks."

作者主张：给程序员提供**标准通用抽象**，把 check-use 对绑成单个伪原子事务，并且这个目标**在用户态、可移植、不改内核**的前提下就能基本达成。

## 代码仓库信息

### 官方产出

**无公开代码仓库。** 但——**论文正文把源码全贴了**（Figure 6/7/8/9：`chop_1st`、`is_symlink`、`atom_race`、`access_open`）。作者明确写了 *"all source code included, as an indication of its simplicity"*。

这在 TOCTOU 领域已经属于稀有物种：第 1 篇 IEEE Access 综述统计出约 3/4 的方案不可复现，而这篇至少给了完整可抄的实现。

已核查渠道：
- Dan Tsafrir 个人主页 `dants.github.io` — 该条目只有 `Abstract / BibTeX / PDF / Definitive`，**无 Software 链接**
- 对比：其同页 2008 年另一篇《The murky issue of changing process identity》条目是**有 `Software` 链接**的，说明主页惯例是「有代码就给链接」，这篇确实没有
- dblp、ACM DL、Technion CRIS 记录均无代码链接

### 相关可动手资源

| 资源 | 说明 |
|------|------|
| IBM RC24572 | 《Portably preventing file race attacks with user-mode path resolution》(2008-06)。**确定性**版本，开销显著低于本文概率式方案——若要实现，建议从这篇入手而非 FAST 版本 |
| [`ncu-psl/TOCTOU-Detection`](https://github.com/ncu-psl/TOCTOU-Detection) | Clang Static Analyzer 插件（对应「静态检测」分支，非本文的运行时防护） |
| [`pranjalm37/race-condition-exploiter`](https://github.com/pranjalm37/race-condition-exploiter) | Python TOCTOU 攻防套件，可用来复现「check-then-open」模式被 symlink 打穿的过程 |
| Linux `openat(2)` + `O_NOFOLLOW` | 论文参考文献 [23] 提到的现代替代路径。与本文的关系：`O_NOFOLLOW` **只作用于路径最后一段**，前面几段的软链仍可被攻击者操纵（论文 Figure 2a 正是此场景）——这也是本文存在的原因 |

### 复现提示

论文实验依赖 `atime` 侧信道与共享内存同步，且跑在 Solaris 8 / AIX 5.3 等老系统上。在现代 Linux 上复现需注意：

- 多数发行版默认挂载带 `relatime`/`noatime`，**atime 侧信道已经不好使了**——这反而是好事，说明攻击面被时代顺手削掉一块
- 迷宫依赖 `PATH_MAX` 与符号链接级数限制（Linux 单路径软链解析上限通常 40 层），构造方式与 2008 年不同
- 核心算法（列优先遍历 + atom_race）不依赖这些，可直接移植

## 与第 1 篇综述的关系

第 1 篇（IEEE Access 2022）把防御方案归为六类，本文落在 **「系统调用拦截 / 用户态」** 与 **「源码检测之外的运行时防护」** 之间——更准确说，它属于综述里说的**可移植用户态解法**这一支。综述的结论之一「没有通用解、现有方案普遍不可复现」与本文的自证（源码全贴）形成了有趣的张力：本文大概是那 1/4 里的一员。

## 收获与吐槽

- **「行优先 vs 列优先」这个洞察太漂亮了。** 表面上是安全问题的攻防升级，实质是**把一个 O(n) 路径解析的遍历顺序换了一下**。安全研究里这种「换个循环嵌套顺序就把攻击面消掉」的解法，比堆复杂度优雅得多。
- **atime 侧信道**是全篇最骚的一笔——攻击者靠观察「访问时间被内核更新了」来判断受害者进程走到哪一步。2008 年能玩，2026 年因为 `relatime` 默认化基本玩不了。安全与工程实践就是这样互相消磨的。
- 论文自己把安全性**归约到 `atom_race` 一个函数**（"all other functions are completely safe"），这种收敛做得很干净，值得学。
- 拿「暴露型防守方」（让攻击者拥有完全即时知识 + 完美同步）来做上界测试，是很扎实的自证方式——比起只打败已知攻击强得多。
