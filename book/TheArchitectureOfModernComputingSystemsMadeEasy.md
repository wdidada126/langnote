# The Architecture of Modern Computing Systems Made Easy

## 版本与 ISBN

- 全名：*The Architecture of Modern Computing Systems Made Easy: Bridging Hardware and Software: ABI, Compilers, and Runtime Implications*
- 作者：Maximilian Leon Wolfgang
- 出版社：**Independently published**（作者自出版，Amazon KDP 按需印刷）
- 出版时间：2026 年
- **ISBN-13（平装 / Paperback）：`9798250284318`** → 规范化 `979-8-2502-8431-8`
- **ISBN-13（精装 / Hardcover）：`9798250284714`** → 规范化 `979-8-2502-8471-4`（该版本已标为不再供应）
- **ASIN（Kindle 电子版）：`B0GQQ6B1KM`**
- 页数：321 页（平装与精装均为 321）
- 语言：英文
- 定价：约 €30.40 起（AbeBooks 平台最低价）

> 2026-09-25 由 `2026/202609/20260918.md`（`rust abi ffi联系与区别` 一段）整理。
> ISBN-13 校验位**均已验证通过**：
> - `9798250284318`：前 12 位 1/3 交替加权和 = 112 → 校验位 8 ✔
> - `9798250284714`：前 12 位 1/3 交替加权和 = 116 → 校验位 4 ✔
> 书名 / 作者 / ISBN / 页数经 **AbeBooks（德国站）与 IberLibro 两个独立书目平台交叉确认**。

## 笔记

- 一句话定位：**解释「当你按下 Run 之后，究竟发生了什么」**——高级语言代码（C / C++ / Rust / Java）是如何经由编译器、操作系统与运行时，最终在处理器上执行完的。
- 内容主线（据出版方简介）：
  1. 数字逻辑与数据通路（digital logic & datapaths）基础
  2. 指令集架构（ISA）
  3. 汇编语言
  4. 现代处理器微架构
  5. **ABI（Application Binary Interface）**——软硬件之间的关键桥梁，本书的核心
  6. 链接器与加载器：目标文件 → 可执行程序
  7. 流水线、缓存、分支预测对性能的影响
  8. 内存模型对多线程软件的影响
  9. 现代处理器如何在**乱序执行**的同时保证正确性
- 书中承诺读者能回答的问题：
  - 指令集架构如何影响编译器设计
  - ABI 如何规定寄存器使用、栈布局与二进制兼容性
  - linkers / loaders 如何把目标文件变成可执行程序
  - 流水线 / 缓存 / 分支预测如何影响性能
  - 内存模型如何影响多线程软件
- 目标读者：计算机专业学生、系统程序员、嵌入式工程师、性能调优专家。
- 与源笔记的关联：出现在 `20260918.md` 中「rust abi ffi 联系与区别 / 汇编层面 / rust 不同版本 abi 不兼容」这条记录之后——正是本书第 5 章 ABI 主题的现实触发点。

## 获取与配套

| 项目 | 链接 |
|------|------|
| AbeBooks（德）书目页 | https://www.abebooks.de/9798250284318/Architecture-Modern-Computing-Systems-Made/plp |
| IberLibro 平装版 | https://www.iberlibro.com/Architecture-Modern-Computing-Systems-Made-Easy/32430279485/bd |
| IberLibro 精装版（ISBN 9798250284714） | https://www.iberlibro.com/products/isbn/9798250284714 |

无配套代码仓库或项目站点（自出版技术书，未见官网）。

## 备注

- 自出版 + POD，**无传统出版社评审流程**，内容深度与准确性未经同行验证，宜作为入门/梳理材料而非权威参考。
- 精装版 ISBN `9798250284714` 在书目平台已标为「该版本不再供应」，实际可购的是平装版。
- 源笔记把 ASIN `B0GQQ6B1KM` 写成「ISBN:」，严格来说是 **ASIN（亚马逊电子书编号）而非 ISBN**，此处已区分标注。
- 国内基本买不到，AbeBooks / IberLibro 多为英国仓发货的 POD 新书。

## 关联

- `paper/2026.md` — 同批整理的 2026 年笔记论文清单（19 篇）
- 主题相近的系统类书籍可对照仓库内既有的组成原理 / 体系结构相关笔记
