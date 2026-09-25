# CMU 11-785: Introduction to Deep Learning 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 11-785 Introduction to Deep Learning (LTI Institute) |
| 学校 | Carnegie Mellon University |
| 主讲 | Bhiksha Raj（LTI 课程组，每学期轮换讲师） |
| 教材 | 无固定教材；Lecture Notes/Slides + 论文阅读为主 |
| csdiy 路径 | `深度学习/CMU11-785`（页面更新：2026-02-21） |
| 最新期次 | Spring 2026（官网 deeplearning.cs.cmu.edu/S26，csdiy 缓存时页面 2026-02 更新） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟🌟（本课程最难档），约 120 小时；先修：线代、概率论、Python、机器学习基础 |

## 为什么学

- CMU LTI 的"硬核"深度学习核心课：扎实、节奏快、几乎无水内容。
- 从神经网络基础到 CNN/RNN/Attention/Transformer/生成模型/优化与泛化全链路打通。
- 作业不是套模板跑通，而是要求理解模型行为、训练细节与实验设计——研究生强度训练。
- 想建立长期可迁移的 DL 能力（而非只会调 API）的话，投入产出比极高。

## 先修与知识联系

- 先修：CS229/机器学习基础、线代、概率论、Python。
- 纵向：比 CS230 深一层，是 CS231n（CV）、CS224n（NLP）、CS285（RL）的公共底座。
- 配套：CMU 10-414 Deep Learning Systems（手写 autograd/反向传播实现）互补实践。
- 作业含语音（ASR）、视觉、NLP 三大 Assignment 线，是少数多模态全覆盖的导论课。

## 讲义章节目录（按 S26/F25 公开课表整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 引言：深度学习与感知任务 | 课程 notes ch.1 |
| L2 | 前馈网络（FFN）与损失 | ch.2；Rumelhart 1986（BP） |
| L3 | 反向传播与优化（SGD/动量/Adam） | ch.3；Adam 论文 |
| L4 | 卷积神经网络 | ch.4；LeNet、AlexNet |
| L5 | NLP 基础：词嵌入与序列分类 | word2vec、GloVe |
| L6 | 残差网络与深层训练 | ResNet、Highway Networks、BatchNorm |
| L7 | 循环网络：RNN/GRU/LSTM | LSTM、GRU 综述 |
| L8 | 注意力与 Transformer | Attention Is All You Need |
| L9 | Transformer 应用：视觉 (ViT) 与语音 (ASR/CTC) | ViT、wav2vec 2.0 |
| L10 | 深度生成模型 I：自编码器与 VAE | Auto-Encoder、VAE |
| L11 | 深度生成模型 II：GAN 与扩散模型 | GAN、DDPM |
| L12 | 优化理论：收敛性与学习率调度 | 课程优化 notes |
| L13 | 泛化与正则化：为什么过参数化不崩 | dropout、双下降相关论文 |
| L14 | 图神经网络与对比学习 | GCN、SimCLR/CLIP |
| L15 | 强化学习基础与 seq 决策 | DQN/PPO 综述 |
| L16 | 前沿专题与期末项目分享 | 当季论文列表 |

> 作业线：HW1 反向传播手写 → HW2 CNN 语音/视觉 → HW3 Transformer NLP → HW4 生成模型 → Course Project（自选方向）。
