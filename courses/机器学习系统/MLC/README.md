# Machine Learning Compilation（MLC，陈天奇）学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Machine Learning Compilation（机器学习的系统方法 / ML 编译公开课） |
| 学校 | Bilibili 大学（社区公开课，mlc.ai；陈天奇 2022 暑期开设） |
| 主讲 | Tianqi Chen（陈天奇，Apache TVM 创始人之一）等 MLClang/CMU 团队 |
| 教材 | 无；官方中英讲义 + 每讲配套 Jupyter Notebook（全开源） |
| csdiy 路径 | `机器学习系统/Machine Learning Compilation`（页面更新：2022-09-06） |
| 最新期次 | Summer 2022 中文版（后续演进为 mlc.ai 的 2023 课程与 MLC-LLM 项目，csdiy 收录 summer22-zh） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 30 小时；先修：机器学习/深度学习基础；语言 Python |

## 为什么学

- ML 编译方向开创者陈天奇亲授的首门该领域系统课：国内外此前没有专门课程，是理解 TVM 与"模型→高性能硬件代码"全链路的全景图。
- 以 Apache TVM 为主例：讲清如何把开发模式（TensorFlow/PyTorch/JAX）的模型经普适抽象与优化算法变换为适配各类硬件的部署模式。
- 每讲配套可运行 Jupyter Notebook，知识点 high-level 但有代码落地；做 TVM 相关开发可直接获得规范示例。
- 资源全开源且有中英双版：B 站中文录像、YouTube 英文版、mlc.ai 讲义。

## 先修与知识联系

- 先修：深度学习基础 + 一点编译器/体系结构直觉（CS15213/CS61C 更佳，非必须）。
- 前导：CMU10-414（框架内部机制）→ 本课（编译优化）→ CMU15-442（LLM 时代系统前沿）。
- 平级：EML（算法侧效率）与 CSE234（LLM 系统）从其他角度互补。
- 知识输出：TIR/Tensor Expression → 算子内核开发；Relax/整图优化 → torch.compile/Inductor；MLC-LLM → 端侧/异构 LLM 推理。

## 讲义章节目录（对应 mlc.ai summer22 中文共 8 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 机器学习编译导论：为什么需要编译、MLC 全景 | Note 1；TVM OSDI 2018 |
| L2 | 面向模型开发者的编译 I：Keras + TVM 端到端部署 | Notebook: Keras+TVM |
| L3 | 面向模型开发者的编译 II：PyTorch/框架接入与整图优化 | Notebook: PyTorch+TVM |
| L4 | 面向硬件后端开发者的编译：tensor program、算子与 schedule | Notebook: 算子开发 |
| L5 | Tensor 表达式与 TIR：循环变换、调度原语 | TVMScript / TensorIR 文档 |
| L6 | 自动优化：AutoTVM/Ansor 搜索空间与调度学习 | Chen et al. 2018；Zheng et al. 2020 |
| L7 | 整图编译与 Relax：新架构、函数式 IR、动态形状 | Relax 讲义/论文 |
| L8 | 前沿与总结：MLC-LLM、异构部署与开放问题 | MLC-LLM 仓库 |

> 注：课程作业见 GitHub mlc-ai/notebooks/assignment；具体讲名以官网 summer22-zh 为准。

## 课程资源（摘自 csdiy）

- 课程网站：https://mlc.ai/summer22-zh/
- 课程视频：Bilibili（中/英双版，B 站为中文）
- 课程笔记：https://mlc.ai/zh/index.html
- 课程作业：https://github.com/mlc-ai/notebooks/blob/main/assignment
