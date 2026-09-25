# csdiy 全课程笔记工程

来源：[csdiy.wiki 计算机自学指南](https://csdiy.wiki/)。本工程按 csdiy 分类为每门课程建独立目录，依据最新年份（2025/2026）讲义记笔记，并配套：

- **经典论文 + 近5年（2021–2026）论文**清单，标注与讲义章节的关联；
- **知识点 → 最新开源项目应用**映射（Linux、LLVM、TiKV、PostgreSQL、vLLM、PyTorch 等）；
- **知识联系**：每门课 README 说明先修/后继，跨课程脉络见下文学习地图；
- **配套项目**：每章节选合适语言的实践小项目与独立 build 脚本（本轮只写不编译，集中编译脚本后续统一验证）。

课程目录规范：`courses/<分类>/<课程>/`，内含 `README.md`（总览+章节目录）、`notes/`（讲义笔记）、`papers.md`（论文+开源映射）、`projects/`（配套项目）。

状态说明：**全量** = 逐章完整笔记；**骨架** = 总览+章节TOC+论文/开源/项目规划，笔记待分批填充。

## 学习地图（跨课程知识联系主线）

1. **工具线**：MIT Missing Semester → Git/Linux/Vim/Make/CMake → 贯穿所有课程 projects/。
2. **编程到系统**：CS61A（程序抽象）→ CS61B（数据结构）/ CS50、CS106B（C++）→ CSAPP（内存、链接、IO、并发）→ DDCA/CS61C（从门电路到机器）→ 6.S081/NJUOS/CS162（内核）→ CS149/6.824（并行与分布式）。
3. **数据与软件**：CS61B → 6.006/CS170（算法）→ 6.031/CS169（工程质量）→ CS186/15-445/CS122（数据库）→ CS144/topdown（网络）→ CS143/NJU/USTC（编译器回到 CSAPP 的机器表示）。
4. **数学到 AI**：18.06/6.042/CS70 → 凸优化/概率论 → CS188 → CS229/CS189 → CS231n/CS224n/李宏毅 → CS285/11-785 → 深度生成模型（MIT6.S184、扩散/流匹配）→ LLM 系统（CMU 11-868/15-779）↔ 机器学习系统（15-442、10-414、MLC）把 AI 线接回系统线（GPU、编译器、分布式）。
5. **图形与 Web**：18.06+DDCA → GAMES101/202 → 光追/管线 ↔ GPU 开源栈；CS142/fullstackopen/CS571 → Web 全栈 ↔ 网络与数据库。

## 课程索引

### 必学工具
不单独立项；相关技能（Git/Make/CMake/Vim/LaTeX/Docker）融入各课程 projects/ 的编译脚本与说明中。

### 数学基础（状态：骨架）
| 课程 | 文件夹 | 主讲/教材 | 最新期次 |
|---|---|---|---|
| MIT 18.01/18.02 微积分 | 数学基础/MITmaths | MIT notes | — |
| MIT 18.06 线性代数 | 数学基础/MITLA | Gilbert Strang | 2023春 |
| MIT 6.050J 信息论与熵 | 数学基础/information | Penfield | — |

### 数学进阶（骨架）
| 课程 | 文件夹 | 主讲/教材 | 最新期次 |
|---|---|---|---|
| UCB CS70 离散数学与概率 | 数学进阶/CS70 | 课程notes | — |
| UCB CS126 概率论 | 数学进阶/CS126 | Walrand | — |
| MIT 6.042J 数学CS导论 | 数学进阶/6.042J | Leighton | spring2015 |
| MIT 18.330 数值分析 | 数学进阶/numerical | Julia/fncbook | 2025更新 |
| Stanford EE364A 凸优化 | 数学进阶/convex | Boyd | — |
| Cambridge 信息论·模式识别·神经网络 | 数学进阶/The_Information_Theory_Pattern_Recognition_and_Neural_Networks | MacKay | — |

### 编程入门（除 CS61A 外骨架）
| 课程 | 文件夹 | 语言 | 最新期次 | 状态 |
|---|---|---|---|---|
| MIT Missing Semester | 编程入门/MIT-Missing-Semester | Shell | IAP2026 | 骨架 |
| UCB Sysadmin DeCal | 编程入门/DeCal | — | — | 骨架 |
| UCB CS61A | 编程入门/CS61A | Python/Scheme | fall2024/spring2026 | **全量** |
| Harvard CS50P | 编程入门/CS50P | Python | 2022 | 骨架 |
| MIT 6.100L | 编程入门/MIT6.100L | Python | — | 骨架 |
| Harvard CS50x | 编程入门/CS50 | C | 2025 | 骨架 |
| AUT AP1400 | 编程入门/AUT1400 | C++ | — | 骨架 |
| Stanford CS106L | 编程入门/CS106L | C++ | — | 骨架 |
| Stanford CS106B/X | 编程入门/CS106B_CS106X | C++ | 2022win | 骨架 |
| MIT 6.092 | 编程入门/MIT6.092 | Java | 2010 | 骨架 |
| Stanford CS110L | 编程入门/CS110L | Rust | 2019 | 骨架 |
| KAIST CS220 | 编程入门/cs220 | Rust | 2025 | 骨架 |
| KAIST CS431 | 编程入门/cs431 | Rust | — | 骨架 |
| Cornell CS3110 | 编程入门/CS3110 | OCaml | 2021 | 骨架 |
| Helsinki Haskell MOOC | 编程入门/Haskell-MOOC | Haskell | — | 骨架 |

### 电子基础（骨架）
| 课程 | 文件夹 | 主讲/教材 |
|---|---|---|
| UCB EE16A/B | 电子基础/EE16 | 课程notes |
| UCB EE120 信号与系统 | 电子基础/signal | 课程notes |
| MIT 6.007 | 电子基础/Signals_and_Systems_AVO | Oppenheim |

### 数据结构与算法
| 课程 | 文件夹 | 主讲/教材 | 最新期次 | 状态 |
|---|---|---|---|---|
| UCB CS61B | 数据结构与算法/CS61B | Josh Hug | spring2024 | **全量** |
| Princeton Algorithms | 数据结构与算法/Algo | Sedgewick | — | 骨架 |
| MIT 6.006 | 数据结构与算法/6.006 | Demaine/CLRS | Fall2011 | **全量** |
| MIT 6.046 | 数据结构与算法/6.046 | Demaine/Devadas/Lynch | Spring2015 | 骨架 |
| UCB CS170 | 数据结构与算法/CS170 | 课程notes | — | 骨架 |

### 软件工程（骨架）
| 课程 | 文件夹 | 最新期次 |
|---|---|---|
| MIT 6.031 | 软件工程/6031 | latest |
| UCB CS169 | 软件工程/CS169 | — |
| CMU 17-803 | 软件工程/17803 | Spring2024 |

### 计算机系统基础
| 课程 | 文件夹 | 教材 | 状态 |
|---|---|---|---|
| CMU 15-213 CSAPP | 计算机系统基础/CSAPP | CSAPP 3/E | **全量** |
| Stanford CS110 | 计算机系统基础/CS110 | CSAPP | 骨架 |

### 体系结构
| 课程 | 文件夹 | 主讲 | 最新期次 | 状态 |
|---|---|---|---|---|
| Nand2Tetris | 体系结构/N2T | Nisan & Schocken | — | 骨架 |
| UCB CS61C | 体系结构/CS61C | — | Fa25 | 骨架 |
| ETH DDCA | 体系结构/DDCA | Onur Mutlu | 2024/25 | **全量** |
| ETH CA | 体系结构/CA | Onur Mutlu | 2024 | 骨架 |

### 操作系统
| 课程 | 文件夹 | 主讲/教材 | 最新期次 | 状态 |
|---|---|---|---|---|
| MIT 6.1810/6.S081 | 操作系统/MIT6.S081 | Morris, xv6 | 最新届 | **全量** |
| UCB CS162 | 操作系统/CS162 | OS:PPuP | Fa25 | 骨架 |
| 南大 OS | 操作系统/NJUOS | 蒋炎岩, OSTEP | — | 骨架 |
| 哈工大 OS | 操作系统/HITOS | 李治军, Linux0.11 | — | 骨架 |

### 并行与分布式系统
| 课程 | 文件夹 | 状态 |
|---|---|---|
| Stanford CS149 | 并行与分布式系统/CS149 | 骨架 |
| MIT 6.5840/6.824 | 并行与分布式系统/MIT6.824 | **全量**（论文课，2026-09 页面更新） |

### 系统安全（骨架）
CS161、MIT 6.1600、MIT 6.858、ASU CSE365（s2025）、CSE466、SEED Labs → `系统安全/` 下同名文件夹。

### 计算机网络
| 课程 | 文件夹 | 教材 | 状态 |
|---|---|---|---|
| UCB CS168 | 计算机网络/CS168 | cs168.io | 骨架（SP2025） |
| Stanford CS144 | 计算机网络/CS144 | — | 骨架（2024） |
| USTC 自顶向下 | 计算机网络/topdown_ustc | Kurose 7版 | 骨架 |
| 自顶向下方法 | 计算机网络/topdown | Kurose & Ross | **全量** |

### 数据库系统
| 课程 | 文件夹 | 状态 |
|---|---|---|
| UCB CS186 | 数据库系统/CS186 | 骨架 |
| CMU 15-445 | 数据库系统/15445 | **全量**（Andy Pavlo Fall2023） |
| Caltech CS122 | 数据库系统/CS122 | 骨架 |
| Stanford CS346 | 数据库系统/CS346 | 骨架 |
| CMU 15-799 | 数据库系统/15799 | 骨架 |

### 编译原理
| 课程 | 文件夹 | 状态 |
|---|---|---|
| 北大编译实践 | 编译原理/PKU-Compilers | 骨架 |
| Stanford CS143 | 编译原理/CS143 | **全量** |
| 南大编译原理 | 编译原理/NJU-Compilers | 骨架 |
| KAIST CS420 | 编译原理/CS420 | 骨架 |
| USTC 编译 | 编译原理/USTC-Compilers | 骨架 |
| 上交编译 | 编译原理/SJTU-Compilers | 骨架（2026更新） |

### 编程语言设计与分析（骨架）
CS242、南大软件分析、北大软件分析、Cambridge Semantics → `编程语言设计与分析/` 下同名文件夹。

### 计算机图形学
| 课程 | 文件夹 | 状态 |
|---|---|---|
| GAMES101 | 计算机图形学/GAMES101 | **全量**（闫令琪） |
| GAMES202 / GAMES103 / CS148 / 15-462 / USTC-CG | 计算机图形学/ | 骨架 |

### Web开发（骨架）
mitweb、CS142、fullstackopen、CS571 → `Web开发/` 下同名文件夹。

### 数据科学（骨架）
UCB Data100 → `数据科学/Data100/`。

### 人工智能
| 课程 | 文件夹 | 状态 |
|---|---|---|
| Karpathy 神经网络从零实现 | 人工智能/NeuralNets-ZeroToHero | 骨架 |
| Harvard CS50 AI | 人工智能/CS50AI | 骨架 |
| UCB CS188 | 人工智能/CS188 | **全量**（AIMA, Spring2024） |

### 机器学习
| 课程 | 文件夹 | 状态 |
|---|---|---|
| Coursera ML (Ng) | 机器学习/ML | 骨架 |
| Stanford CS229 | 机器学习/CS229 | **全量** |
| UCB CS189 | 机器学习/CS189 | 骨架 |

### 机器学习系统（骨架）
CMU 15-442（2026春）、AICS、CMU 10-414、MIT 6.5940、MLC、CSE234 → `机器学习系统/` 下同名文件夹。

### 深度学习
| 课程 | 文件夹 | 状态 |
|---|---|---|
| CS230 / LHY(2025春) / 11-785(2026-02) / 6.7960 / NYU / 498-007 / CS224n(2025) / CS224w / CS285 | 深度学习/ | 骨架 |
| Stanford CS231n | 深度学习/CS231 | **全量**（Spring2025） |

### 深度生成模型（骨架）
MIT 6.S184（2025）；大语言模型子组：CMU 11-868、11-667、11-711、15-779（2026-02）。

### 机器学习进阶（骨架）
CMU 10-708、Columbia STAT 8201、U Toronto STA 4273、Stanford CS229M。

## 进度表

| 批次 | 内容 | 状态 |
|---|---|---|
| 1 | 全 65 课骨架（README+TOC+论文/开源/项目规划） | ✅ 完成（2026-09-25） |
| 2 | 核心课全量·第一批：CS61A、CS61B、6.006、CSAPP、DDCA、6.S081 | ✅ 完成（2026-09-25） |
| 3 | 核心课全量·第二批：6.824、topdown、15-445、CS143、CS188、CS229、CS231n、GAMES101 | ✅ 完成（2026-09-25） |
| 4 | 核心课配套项目代码 + 各课 build 脚本 + 聚合脚本 | ✅ 完成（本轮只写不编译） |
| 5 | 集中编译验证（用户自行执行） | ⏳ 待执行 |

## 集中编译（待用户执行）

14 门核心课共 90+ 个配套项目，每个项目目录自带 `build.bat`/`build.sh`（或 `run.bat`/`run.sh`），顶层提供聚合脚本：

- **Windows**：在 Developer Command Prompt（先 `vcvarsall`）下运行 `courses\build-all.bat`；可用 `build-all.bat "计算机系统基础\CSAPP"` 限定单课。
- **Linux/macOS/Git-Bash**：`./courses/build-all.sh`；`--check` 模式只做 Python 语法检查，不触发 C/C++/Java/Verilog/Go 编译。

工具链要求：MSVC（cl）或 gcc/g++、JDK 17（javac）、Go、Python 3、iverilog（DDCA 的 Verilog 项目）。各语言项目分布：C（CSAPP/6.S081）、C++17（15-445/CS143/GAMES101）、Java（CS61B）、Python（CS61A/6.006/CS188/CS229/CS231n/topdown）、Go（6.824）、Verilog（DDCA）。

## 后续批次建议

剩余 51 门骨架课的笔记可按主题分批推进：① 数学与电子基础（9 门，支撑 AI 线）；② 系统与 PL 进阶（CS110/N2T/CS61C/CS162/NJUOS/HITOS/6031/CS242 等）；③ 安全六门与编译三门（与核心课已互相链接）；④ AI 全家桶进阶（ML系统 6 门 + 深度生成模型 5 门 + ML进阶 4 门，接 LLM 热点）。

