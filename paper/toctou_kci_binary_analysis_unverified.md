# ⚠️ 存疑条目：Detecting TOCTOU Race Condition on UNIX Kernel Based File System through Binary Analysis

> **状态：无法核实。本文件用于记录核查过程与结论，不是论文笔记。**
> 整理日期：2026-09-25

## 原始记录

出处：`2026/202609/20260922.md`，原文片段：

> 3. 《Detecting TOCTOU Race Condition on UNIX Kernel Based File System through Binary Analysis》
> · 来源：KCI（韩国学术期刊）
> · 作者：汉阳大学
> · 内容定位：这篇论文从二进制分析角度检测 UNIX 内核文件系统的 TOCTOU 竞态条件。作者指出，现有静态分析工具依赖源码分析，而二进制层面的研究几乎空白。论文提出了基于控制流图（CFG）和调用图（Call Graph）的检测方法。

原始记录**未提供**：作者姓名、期刊名称、卷期、页码、年份、DOI。

## 核查过程与结果

| 渠道 | 查询方式 | 结果 |
|------|----------|------|
| Google（英文标题精确匹配） | `"Detecting TOCTOU Race Condition on UNIX Kernel Based File System through Binary Analysis"` | ❌ 零命中，返回的均为泛泛的 TOCTOU 科普/CWE 页面 |
| Google（英文变体） | `"Detecting TOCTOU Race Condition" "Binary Analysis" Hanyang KCI 2017/2018/2019` | ❌ 无相关结果 |
| Google（韩文） | `"TOCTOU" "이진 분석" 파일 시스템 레이스 컨디션 탐지 한양대 논문` | ❌ 无相关结果 |
| IEEE Xplore / ACM DL / Scopus | 标题关键词组合 | ❌ 未命中 |
| GitHub | 相关代码仓库检索 | ❌ 无对应实现 |

**同时检索成功的对照**：同批笔记里的另外两篇（IEEE Access 2022 综述、FAST'08 硬度放大）均在首次检索即命中，且 DOI 经 IEEE Xplore / ACM DL / dblp 三方交叉验证通过。这说明**不是检索方法的问题，而是这条记录本身存疑**。

## 结论

**判定为疑似 AI 幻觉条目，建议从笔记中剔除。**

判断依据：

1. 该笔记整段（第 18–109 行）以「目前搜索结果中……以下按类别整理」开头，是**典型的 AI 回答口吻**，且结尾还有「如果你需要针对特定场景……可以告诉我，我再帮你细化检索方向」——确认这段内容来自某次 AI 对话，非人工核实
2. 同段的另外两条（IEEE Access 综述、ACM TOS 论文）**真实存在且信息准确**，说明 AI 混合了真实条目与编造条目——这正是幻觉最难识别的形态：真假掺半
3. 「汉阳大学 + KCI + 二进制分析检测 TOCTOU」这个组合，在公开学术数据库中检索不到任何支撑

## 若仍想追查

需要补充的关键字段（原笔记完全缺失）：**作者姓名**（汉阳大学只是机构）、**期刊名**（KCI 是索引库不是期刊）、**发表年份**。

拿到作者名后可查：
- DBLP（https://dblp.org）——计算机领域覆盖最全
- KCI 韩国学术期刊引文索引（https://www.kci.go.kr）
- 汉阳大学研究人员主页

## 教训

> 从日常笔记批量提取论文时，**AI 生成的内容片段是高风险区**。凡是笔记中出现「目前搜索结果中……」「以下按类别整理」这类措辞的段落，其中的条目必须逐条外部核实，不能因为同一段里其他条目是真的就默认全部为真。

本次同批 3 条论文中，2 条真、1 条假——**幻觉率 33%**。
