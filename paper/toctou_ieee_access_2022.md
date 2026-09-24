# Defense and Attack Techniques Against File-Based TOCTOU Vulnerabilities: A Systematic Review

> 本文件由 `2026/202609/20260922.md` 日常笔记中提取，2026-09-25 整理。
> 全文已下载并逐页解析（17 页），以下数据除注明外均出自论文正文。

## 元信息

| 项目 | 内容 |
|------|------|
| 标题 | Defense and Attack Techniques Against File-Based TOCTOU Vulnerabilities: A Systematic Review |
| 作者 | Razvan Raducu, Ricardo J. Rodríguez (Member, IEEE), Pedro Álvarez |
| 单位 | University of Zaragoza, Department of Computer Science and Systems Engineering, 50009 Zaragoza, Spain |
| 通讯作者 | Ricardo J. Rodríguez — rjrodriguez@unizar.es |
| 期刊 | IEEE Access, Volume 10 |
| 页码 | 21742 – 21758（共 17 页） |
| 时间线 | 收稿 2022-01-26 / 录用 2022-02-05 / 发表 2022-02-21 / 当前版本 2022-03-03 |
| **DOI** | **10.1109/ACCESS.2022.3153064** |
| IEEE Xplore | document/9718065 |
| 开放获取 | ✅ Open Access，CC BY-NC-ND 4.0（署名-非商业-禁止演绎） |
| 免费全文 | https://zaguan.unizar.es/record/112159/files/texto_completo.pdf （萨拉戈萨大学机构库） |
| ISSN | 2169-3536 |
| 索引 | SCI-E / EI / Scopus；JCR 2022 IF 3.9（Q2） |
| 资助 | 西班牙经济与竞争力部 PDC2021-121072-C22；阿拉贡政府 DisCo 研究组 T21-20R；Fundación Ibercaja JIUZ-2020-TIC-08 |
| 关键词 | File-based race condition, TOCTOU vulnerability, avoidance techniques |

### BibTeX

```bibtex
@article{raducu2022defense,
  author  = {Raducu, Razvan and Rodr{\'i}guez, Ricardo J. and {\'A}lvarez, Pedro},
  title   = {Defense and Attack Techniques Against File-Based {TOCTOU} Vulnerabilities: A Systematic Review},
  journal = {IEEE Access},
  volume  = {10},
  pages   = {21742--21758},
  year    = {2022},
  doi     = {10.1109/ACCESS.2022.3153064}
}
```

## 一句话结论

> 近 50 年的文件型 TOCTOU 问题**至今没有通用解**。41 篇入选文献里 37 篇做防御、4 篇做攻击；防御方案可归为 6 类；**约 3/4 的方案无法复现**（无源码、无工具、细节不足）；作者认为通用解大概率不存在，现实出路是「FD 化 API + 内核改造 + 事务型文件系统」的组合。

## 核心笔记

### 1. 研究问题（RQ1–RQ5）

| RQ | 问题 |
|----|------|
| RQ1 | 文件型 TOCTOU 的攻防技术分别是怎么工作的？ |
| RQ2 | 它们驻留在内存的哪一层（用户态 / 内核态）？ |
| RQ3 | 漏洞是何时被检测或被利用的（静态 / 动态）？ |
| RQ4 | 技术实现在哪个操作系统上？ |
| **RQ5** | **是否有工具或源码可用来验证/复现实验结果？** ← 本文最扎心的部分 |

### 2. 检索方法（可复现协议）

- **数据库**：IEEE Xplore、ScienceDirect、Scopus、ACM
- **检索式**：`(TOCTOU OR TOCTTOU OR "time of check to time of use") AND file AND (attack* OR exploit* OR abus* OR defen* OR mitigat* OR fix*)`，检索至 2021 年，无起始年限制
- **工具**：StArt（系统综述流程工具），打分制——标题命中 +5、摘要命中 +3、关键词命中 +2，阈值 15
- **关键词袋**：TOCTOU、attack、concurrency、defense、exploit、filesystem、interference、mitigation、race condition、data race（含同义词与变体）
- **人工补充**：逐届核查 Tier-1/Tier-2 安全会议共 **470 届**（Tier-1 216 + Tier-2 264），如 IEEE S&P 从 1995 到 2020 共 25 届全查
- **筛选漏斗（PRISMA）**：563 篇 → 去重 −66 → 打分阈值后 126 篇 → 人工补充 13 篇（去重 −6、主题不符 −6）→ **最终纳入 41 篇**；另通过滚雪球（参考文献追踪）补充 11 篇

### 3. 核心数据（Section IV / V）

**攻防配比**
- 防御方案 **37 / 41**；攻击方案 **4 / 41**
- 攻击方案中，一半是「刻意制造更耗时的 I/O」来拉宽竞态窗口，另一半聚焦「从外部存储设备安装程序」的利用

**防御六分类**
1. **源码检测**（source code detection）— 静态分析源码
2. **事后检测**（post-mortem detection）— 执行后用执行轨迹/审计日志回溯判定
3. **系统调用拦截**（system call interposition）— 用户态或内核态挂钩 syscall
4. **内存一致性**（memory consistency）— 进程内 / 进程间
5. **事务型系统调用**（transactional system calls）
6. **沙箱文件系统**（sandbox filesystems）

**检测时机**：静态方案只出现在防御侧，再细分为「源码检测」与「事后检测」；动态方案 25/35（含系统调用拦截、内存一致性、事务型调用、沙箱文件系统）。

**驻留层级**：内核态 21/35，用户态 14/35。**所有攻击技术都在用户态发起。**

**操作系统**：全部防御方案面向 Unix-like；攻击方案 3 个面向 Unix-like，1 个面向 Android。

**元数据使用**：20/35 的防御方案用 **inode** 作为文件对象唯一标识。作者实测发现——**inode 是否被复用取决于底层文件系统**（见 Table 4），因此 inode 不能当作可靠的「唯一区分项」。这一条直接动摇了一大票防御方案的根基。

### 4. RQ5：可复现性（最值得记住的一节）

> **近 3/4 的文献不可复现**——要么没给源码/工具，要么细节不足以自己实现。

- 攻击侧：2 篇（[65][66]）判定为「部分可复现」（虽无源码但描述足够详细）；另外 2 篇（[67][68]）判定为「已不可复现」——**原文给出的源码仓库链接已失效**。
- 作者呼吁：任何提出新工具/新方法的成果都应公开可获取，否则后人无法评估、对比与改进。
- 限制（Limitations）：只收英文文献；结果受 StArt 打分体系与关键词袋约束；**排除了灰色文献**——而作者自己也承认灰色文献（如 Openwall 内核补丁 [78]）在系统安全领域是重要知识来源。

### 5. 未来方向（Section V-B）

作者认为**通用解大概率不存在**（TOCTOU 本身非确定性 + 环境变量等外部因素影响），现实出路是组合拳：

1. **新的（或改造现有的）API**：以**文件描述符而非文件名**为基础的 race-free、安全导向 API。缺点是存量软件依然脆弱，且负担转嫁给开发者——他们得知道并主动用这一套。
2. **改造内核，全程以 FD 工作**：更彻底，但意味着大幅改动内核，**会引发严重的向后兼容问题**。
3. **事务型文件系统**：让文件/目录的创建、修改、重命名、删除成为原子操作，从结构上保证 TOCTOU 成对系统调用之间对象不变。

### 6. 背景数据（可直接引用）

- 文件型 TOCTOU 最早可追溯到 **1970 年代中期**（McPhee 1974 / Abbott et al. 1976 NBSIR 76-1041），20 年后才被系统研究。
- 2020 年**权限提升类漏洞占微软全部漏洞的 44%**（引 BeyondTrust 报告）。
- 论文写作时，**NVD 检索 TOCTOU 相关漏洞返回 786 条结果**。
- 根因：文件名 → (inode, device number) 的映射是**易变的**；而 (inode, device) → 文件描述符的映射是无竞态的。**问题出在文件名这一层。**
- 经典案例：`sendmail`（先检查 mailbox 属性再追加，两步非原子）；`access()` + `open()` 的 setuid 提权。
- 关联场景：内核 double-fetch（内存 TOCTOU）、远程证明、可信计算（TCG/VMM）。

## 代码仓库信息

### 官方产出

**无。** 本文是系统性文献综述（SLR），不提出新工具，因此没有配套代码仓库。

已核查确认：
- 作者 Razvan Raducu：GitHub 无同名账号
- 作者 Ricardo J. Rodríguez：GitHub `rjrodriguez` 为同名的平面/网页设计师，**非本文作者**
- 论文正文、IEEE Xplore 页面、萨拉戈萨大学机构库记录均未给出任何仓库链接

### 社区/教学实现（可作为动手起点）

| 仓库 | 语言 | Star | 最后更新 | 对应分类 |
|------|------|------|----------|----------|
| [ncu-psl/TOCTOU-Detection](https://github.com/ncu-psl/TOCTOU-Detection) | C++ | 6 | 2020-02 | **源码静态检测**（Clang Static Analyzer 插件，checker 名 `alpha.toctou`） |
| [pranjalm37/race-condition-exploiter](https://github.com/pranjalm37/race-condition-exploiter) | Python | 31 | 2026-08 | 攻防双侧：漏洞/修复样例 + 竞态利用框架 + AST 扫描器 |
| [davidenetti/TOCTOU_Vulnerability](https://github.com/davidenetti/TOCTOU_Vulnerability) | C | 14 | 2023-09 | 攻击侧 PoC（`access()`/`open()` 经典模式） |
| [tobiasGuta/Race-Condition-Gate](https://github.com/tobiasGuta/Race-Condition-Gate) | Java | 1 | 2026-08 | 同步测试工具 |
| [SnailSploit/Claude-Red · offensive-toctou](https://github.com/SnailSploit/Claude-Red) | Markdown | — | — | 攻击侧方法论：FUSE 慢文件系统、userfaultfd、`renameat2(RENAME_EXCHANGE)`、cgroup freeze 等窗口放大技法 |
| [wcventure/ConcurrencyPaper](https://github.com/wcventure/ConcurrencyPaper) | — | — | — | 并发方向论文 + 工具索引（含 LLOV、OMPRacer、RELAY 等） |

### `ncu-psl/TOCTOU-Detection` 速览（最贴近本文「源码检测」分支）

```bash
# 环境：ubuntu 12.04 LTS（较老，需注意兼容性）
apt-get install build-essential zlib1g-dev python
git clone https://github.com/ncu-psl/TOCTOU-Detection.git llvm
mkdir build && cd build
../llvm/configure --enable-optimized
make && make install

# 使用
clang --analyze -Xanalyzer -analyzer-checker=alpha.toctou testCase.c
```

> 注意：该仓库最后更新于 2020 年，依赖的是较老的 LLVM 构建方式（`configure` 而非 CMake），在现代发行版上大概率需要改造。

## 与本仓库其他笔记的关联

- `2026/202609/20260922.md`：本篇的原始出处，同段还记录了 CWE-367、CWE-440 分类，以及 TOCTOU 四类攻击模式（权限可降级型 / FD 可检查型 / 双重检查型 / 其他配对）
- `paper/20260922.md`：本次提取的完整论文清单

## 收获与吐槽

- 这篇综述最值钱的地方不是「分类」，而是 **RQ5 那记重锤**：整个领域 50 年、41 篇论文，工具几乎全军覆没，仓库链接都失效了。做安全研究的复现债，可见一斑。
- **inode 复用表（Table 4）** 是个被低估的贡献——它直接说明「用 inode 做文件唯一标识」这一大票方案的假设不成立，且结论随文件系统而异。
- 作者自己承认排除了灰色文献，却又在 Limitations 里点名 Openwall 内核补丁的价值。这个自我矛盾挺诚实：学术检索协议越严谨，离真实的安全实践反而越远。
