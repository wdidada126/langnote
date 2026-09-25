# PKU 软件分析技术（北京大学，熊英飞）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 北京大学 软件分析技术（Software Analysis Techniques） |
| 学校 | 北京大学 |
| 主讲 | 熊英飞 |
| 教材 | 无固定教材（讲义 + 论文清单；可参考《软件分析》教科书与课程阅读文献） |
| csdiy 路径 | https://csdiy.wiki/编程语言设计与分析/PKU-SoftwareAnalysis/ （页面更新 2023-10-12） |
| 最新期次 | csdiy 链接为 2020 春课程主页（熊英飞主页可查更多年份滚动更新） |
| 状态 | 🚧 骨架已建，逐讲正文待填充 |
| 先修要求 | 数据结构与算法、至少熟悉一门编程语言 |
| 实现语言 | Java、Python |
| 预计学时 | 约 60 小时（csdiy 难度 ★×4） |

## 为什么学

- 广度对标学术前沿：抽象解释、SAT/SMT、符号执行、程序合成、缺陷定位与自动修复——比 NJU 软件分析覆盖更全、难度更高。
- 熊英飞团队是程序合成/APR 方向一线科研组，课程内容与顶会论文同步。
- 两个大项目（Java 指针分析系统 + 程序合成工具）直接把"分析"与"生成"两大范式各练一遍。
- 有 2020 燕云 FullTower 直播录像，中文讲解质量顶级。

## 先修与知识联系

- **先修**：数据结构、编译原理基础（IR/CFG 概念）；逻辑学直觉加分。
- **互练**：NJU-SoftwareAnalysis（更平滑的入门线，可先修）；CS242（类型理论视角）；Z3/角点：符号执行→CS6101/安全课。
- **知识映射**：数据流/指针 ↔ Andersen/RHS；抽象解释 ↔ Cousot；SMT ↔ Z3 论文；合成 ↔ Syntax-Guided Synthesis。

## 讲义章节目录（按 2020 课程主页模块整理；正式笔记以最新年份为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：软件分析的分类与应用 | 讲义 L1 |
| L2 | 数据流分析与格论基础 | 讲义 L2；龙书 ch9 |
| L3 | 过程间分析：摘要与调用上下文 | RHS 1995（IFDS）节选 |
| L4 | 指针分析：Steensgaard/Andersen 与敏感性谱系 | 讲义 + Andersen/Steensgaard 论文 |
| L5 | 指针分析项目工作坊（Java 系统实现） | 课程项目说明 |
| L6 | 抽象解释：具体语义→抽象域→soundness | Cousot & Cousot 1977 精读指引 |
| L7 | SAT 求解：DPLL/CDCL | SAT Handbook 章节 |
| L8 | SMT 与 Z3：量化/量词、程序应用 | de Moura & Bjørner（Z3 CAV 2008） |
| L9 | 符号执行与动态符号执行（concolic） | King 1976; Cadena/Bugsy 综述 |
| L10 | 程序合成 I：枚举/约束/示例引导（ Programming by Example） | Manna & Waldinger; SyGuS 论文 |
| L11 | 程序合成 II：语法引导合成（SyGuS）与案例 | SyGuS 论文与代表工具（如 CVC4/SyGuS-comp） |
| L12 | 程序合成项目工作坊（合成工具实现） | 课程项目说明 |
| L13 | 缺陷定位：频谱/可疑度排序 | Ochiai/Tarantula 论文 |
| L14 | 自动程序修复（APR）与总结 | Genprog/Kali 到 ACE 谱系 |

## 备注

- 骨架讲次为"2020 主页 + 熊主页近年模块"合并推断，填充时以当年 syllabus 校正。
