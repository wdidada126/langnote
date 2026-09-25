# 【CORE】Stanford CS231n: CNN for Visual Recognition 学习笔记

> 本目录为 CORE 课骨架：完整 README 章节目录先行，`notes/`、`papers/`、`projects/` 正文由后续专人完成。

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS231n: Convolutional Neural Networks for Visual Recognition |
| 学校 | Stanford University |
| 主讲 | Fei-Fei Li（李飞飞，ImageNet 研究团队）领衔；2017 版由 Justin Johnson 与 Andrej Karpathy 建设；现行版本以 YouTube 公开讲座为准 |
| 教材 | 无指定教材；参考 Deep Learning Book（deeplearningbook.org），课程自写 Notes 质量极高 |
| csdiy 路径 | `深度学习/CS231`（页面更新：2025-11-13） |
| 最新期次 | Spring 2025（YouTube 全程公开，为最新版本；2017 版有 B 站搬运） |
| 状态 | CORE 骨架：README 完成，notes/papers/projects 正文待专人撰写 |
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

## 讲义章节目录（按 Spring 2025 公开视频 + 经典 Notes 整理，以官网 schedule 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论与 CV 挑战 | Notes: The Importance of Why；DLB ch.1 |
| L2 | 数据驱动学习与图像分类 | Notes: kNN 与数据分区 |
| L3 | 线性分类器（SVM/Softmax） | Notes: Linear Classifiers（作业1核心） |
| L4 | 损失函数与优化 | Notes: Loss functions / Optimization |
| L5 | 神经网络与多层感知机 | Notes: Backpropagation |
| L6 | 反向传播与计算图 | Notes: CS231n Backprop Case Study |
| L7 | 训练神经网络实用策略（调参/初始化） | Notes: Training NNs in Practice |
| L8 | 卷积神经网络架构 | Notes: CNN Architectures |
| L9 | CNN 案例研究（AlexNet/VGG/GoogLeNet/ResNet） | Notes: Case Study；作业2 |
| L10 | 目标检测 | 检测综述（R-CNN/SSD/YOLO 节选） |
| L11 | 语义/实例分割 | FCN/U-Net/Mask R-CNN 节选 |
| L12 | 可视化与理解网络 | Deep Dream/特征可视化论文 |
| L13 | 循环神经网络与视觉应用 | RNN notes、Show-and-Tell |
| L14 | 注意力与 Transformer | Attention Is All You Need；ViT |
| L15 | Transformer 视觉前沿（检测/分割/ViT 变体） | DETR/SAM 节选 |
| L16 | 生成模型：自编码器与 VAE | VAE notes |
| L17 | GAN 与图像生成 | GAN 原论文；作业3 |
| L18 | 扩散模型与当代生成 | DDPM/LDM 节选 |
| L19 | 视频理解与时序任务 | 视频综述节选 |
| L20 | 3D 视觉与隐式表示 | NeRF/点云节选 |
| L21 | 视觉与语言（多模态） | CLIP 论文 |
| L22 | 高效训练、公平性与课程总结 | ML Fairness notes；效率综述 |

> 作业线：Assignment 1（softmax 分类器与反向传播，纯 numpy）→ Assignment 2（CNN/迁移学习/检测，PyTorch）→ Assignment 3（GAN 生成与风格），另有课程项目（论文复现/新想法）。

## 目录说明

- `notes/`：待专人按上表逐讲撰写全量笔记（含公式推导与作业对照）。
- `papers/`：待建经典论文精读库（ResNet/Transformer/CLIP/DINO 等）+ 近 5 年（2021-2026）CV 前沿清单 + 开源应用对照（timm/detectron2/mmdet/diffusers 等）。
- `projects/`：待建三个 Assignment 的重实现计划与 mini-project 方案。
