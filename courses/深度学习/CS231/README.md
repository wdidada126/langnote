# 【CORE】Stanford CS231n: CNN for Visual Recognition 学习笔记

> 状态：**全量（2026-09）** —— 讲义笔记 13 讲、论文清单、三组配套 numpy 项目全部完成。
> 笔记按 Spring 2025 课表（前 13 讲核心线）撰写；L14-L18 扩展讲内容并入 `papers.md` 前沿表与各项目展望。

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS231n: Convolutional Neural Networks for Visual Recognition |
| 学校 | Stanford University |
| 主讲 | Fei-Fei Li（李飞飞，ImageNet 研究团队）领衔；2017 版由 Justin Johnson 与 Andrej Karpathy 建设；现行版本以 YouTube 公开讲座为准 |
| 教材 | 无指定教材；参考 Deep Learning Book（deeplearningbook.org），课程自写 Notes 质量极高 |
| csdiy 路径 | `深度学习/CS231`（页面更新：2025-11-13） |
| 最新期次 | Spring 2025（YouTube 全程公开，为最新版本；2017 版有 B 站搬运） |
| 状态 | 全量（2026-09）：notes/L01-L13 + papers.md + projects/P1-P3 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：机器学习基础；3 个编程作业 |

## 为什么学

- CV 深度学习的事实标准入门课：ImageNet 团队出品，直觉、数学与工程三者平衡得最好。
- 课程 Notes（特别是反向传播、卷积、优化章节）本身就是全网被引用最多的 DL 教程之一。
- 三个 Assignment（Python numpy 手写 → PyTorch/TensorFlow → GAN 生成）是"从零到能用"的最佳训练路径，Karpathy 的"make it work, make it right, make it fast"出自于此。
- 内容相对基础友好：上过 CS230 可直接上手其 Project；同时是 EECS498-007 的同源进阶参照。

## 先修与知识联系

- 先修：Python、线代、概率论、CS230/CS229 级别机器学习概念。
- 平行：EECS498-007（UMich，Johnson 主讲，材料同源、作业更细）；CMU 11-785（理论更硬）。
- 后续：分割/检测/多模态方向可接 6.S184、大模型课程群；视觉侧研究读 ResNet/ViT/CLIP/DINO 原文。

## 讲义目录（Spring 2025 课表，共 18 讲；本笔记覆盖核心前 13 讲）

| 讲次 | 标题 | 笔记 | 项目 |
| --- | --- | --- | --- |
| L01 | 课程导论与 CV 挑战（Introduction） | [notes/L01.md](notes/L01.md) | P1 |
| L02 | 线性分类器与图像分类（A1 发布） | [notes/L02.md](notes/L02.md) | P1 |
| L03 | 正则化与优化 | [notes/L03.md](notes/L03.md) | P1 |
| L04 | 神经网络与反向传播 | [notes/L04.md](notes/L04.md) | P1 |
| L05 | 卷积神经网络基础 | [notes/L05.md](notes/L05.md) | P2 |
| L06 | CNN 架构与案例研究（A1 截止） | [notes/L06.md](notes/L06.md) | P2 |
| L07 | 循环神经网络 | [notes/L07.md](notes/L07.md) | — |
| L08 | 注意力与 Transformer（A2 发布） | [notes/L08.md](notes/L08.md) | P3 |
| L09 | 目标检测、分割与可视化理解 | [notes/L09.md](notes/L09.md) | P2/P3 |
| L10 | 视频理解 | [notes/L10.md](notes/L10.md) | — |
| L11 | 大规模分布式训练 | [notes/L11.md](notes/L11.md) | — |
| L12 | 自监督学习 | [notes/L12.md](notes/L12.md) | — |
| L13 | 生成模型 I：VAE 与 GAN（A3 发布） | [notes/L13.md](notes/L13.md) | P3 |
| L14 | 生成模型 II：扩散模型 | 见 [papers.md](papers.md) 前沿表（SD3/FLUX/rectified flow） | P3 展望 |
| L15 | 3D 视觉 | 见 [papers.md](papers.md)（NeRF 后继/深度估计） | — |
| L16 | 视觉与语言 | [papers.md](papers.md)（CLIP/LLaVA/Qwen-VL） | P3 |
| L17 | 世界建模 | [papers.md](papers.md)（Cosmos/Genie） | — |
| L18 | 以人为本的 AI | 见课程官网阅读材料 | — |

> 作业线：A1（softmax 分类器与反向传播，纯 numpy，4/23 截止）→
> A2（CNN/BatchNorm/迁移/检测，PyTorch，5/7 截止）→ A3（GAN 生成与风格，5/30 截止）。
> 本仓库 `projects/` 为三作业的 numpy 重实现（数据全部合成、无需下载）。

## 目录结构

- [notes/](notes/)：L01-L13 逐讲中文全量笔记（核心概念+公式直觉、前后讲联系、跨课程联系、开源项目应用、精读论文）。
- [papers.md](papers.md)：经典论文表 + 近 5 年（2021-2026）前沿表（标注开源可用性）+ 知识点↔开源项目映射表（pytorch/timm/HF transformers·diffusers/ultralytics/llama.cpp/vLLM 等）。
- [projects/README.md](projects/README.md)：讲次→项目→知识点总表。
  - [projects/p1_image_classifier/](projects/p1_image_classifier/README.md)：kNN + 线性 SVM/softmax + 梯度检查 + SGD 调参（L01-L04，对应 A1）。
  - [projects/p2_convnet/](projects/p2_convnet/README.md)：naive→fast 卷积、BatchNorm、小型 CNN 训练循环（L04-L07，对应 A2）。
  - [projects/p3_transformer_generation/](projects/p3_transformer_generation/README.md)：注意力/TinyViT 手抄反传 + 玩具 GAN/VAE（L08/L13，对应 A3）。
