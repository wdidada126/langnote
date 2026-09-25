# UMich EECS 498-007 / 598-005: Deep Learning for Computer Vision 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | EECS 498-007 / 598-005: Deep Learning for Computer Vision |
| 学校 | University of Michigan |
| 主讲 | Justin Johnson（Fei-Fei Li 博士毕业生，CS231n 2017 版主讲之一） |
| 教材 | 仅推荐教材：Deep Learning Book（Goodfellow 等，deeplearningbook.org） |
| csdiy 路径 | `深度学习/EECS498-007`（页面更新：2024-01-26） |
| 最新期次 | Winter 2022（Lectures/Notes/Assignments 全开源；YouTube 完整播放列表） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 60-80 小时；先修：Python、矩阵论（熟悉矩阵求导）、微积分 |

## 为什么学

- 视频与作业质量极高、主题覆盖全，Assignment 难度由浅入深，完整走完 CV 主流模型发展全阶段。
- 零基础友好：A1 从零教 PyTorch 与 Colab，Handout 本身就是可翻阅的工具书。
- 每个 Assignment 跟随 Handout 亲手实现课堂模型：线性分类器→CNN→检测器（SSD/Faster R-CNN）→RNN/Transformer→VAE/GAN→可视化与风格迁移。
- Autograder 虽仅对本校开放，但 ipynb 中已可确认实现正确性与预期结果，自学者无损。
- 与 CS231n 同源（Johnson 参与建设），材料部分沿用，学过 CS231n 者可作高强度复训。

## 先修与知识联系

- 先修：Python 基础、矩阵求导、微积分；无需 DL 框架经验。
- 前置可先修：CS230（概念图景）；进阶可续 CS231n（CORE 课，本目录同步建设）。
- 资源参考：@Michael-Jetson 二三十万字公开笔记（Michael-Jetson/ML_DL_CV_with_pytorch）。

## 讲义章节目录（Winter 2022，22 讲，以官网/播放列表为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论 | Syllabus / DLB ch.1 |
| L2 | 图像分类 I（kNN、线性分类器） | DLB ch.3/6.1 |
| L3 | 优化 | DLB ch.8；SGD/Adam 论文 |
| L4 | 图像分类 II（MLP 与 PyTorch 入门） | PyTorch 官方 tutorial |
| L5 | CNN I（卷积、池化） | DLB ch.9；LeNet |
| L6 | CNN II（经典架构与迁移学习） | AlexNet/VGG/ResNet |
| L7 | 正则化 | Dropout、数据增强综述 |
| L8 | 优化 II（学习率、BN） | BatchNorm 论文 |
| L9 | 语义分割 I（FCN/U-Net） | FCN、U-Net 论文 |
| L10 | 语义分割 II（全景/实例） | Mask R-CNN 节选 |
| L11 | 目标检测 I（Two-Stage：R-CNN 系） | Faster R-CNN 论文 |
| L12 | 目标检测 II（One-Stage：SSD/YOLO） | SSD 论文 |
| L13 | 循环神经网络（Vanilla/LSTM） | DLB ch.10 |
| L14 | RNN 用于视觉（图像描述） | Show-and-Tell |
| L15 | 注意力机制 | Bahdanau 论文 |
| L16 | Transformer | Attention Is All You Need |
| L17 | Transformer 用于视觉（ViT） | ViT 论文 |
| L18 | 以其他方式表示图像（像素自回归/归一化流） | PixelRNN/Flows 节选 |
| L19 | 3D 表示（点云/体素/NeRF 概览） | PointNet/NeRF |
| L20 | VAE 与像素生成 | VAE 论文 |
| L21 | GAN | GAN、DCGAN |
| L22 | 视觉与语言 / 课程总结 | CLIP、风格迁移 |

> 注：L7-L8、L17-L18 顺序以 YouTube 播放列表为准，骨架阶段允许微调。
