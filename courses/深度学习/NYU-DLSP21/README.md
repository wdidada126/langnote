# NYU Deep Learning (DLSP21) 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | NYU Deep Learning (GU4443-001), Spring 2021 |
| 学校 | New York University |
| 主讲 | Yann LeCun（图灵奖得主、CNN 之父）＋ Alfredo Canziani（助教/联合授课），多位客座讲师 |
| 教材 | Lecture Notes / Slides（课程网站全开源，中英字幕视频） |
| csdiy 路径 | `深度学习/NYU-DLSP21`（页面更新：2026-02-21） |
| 最新期次 | Spring 2021（该公开版本为经典期；后续学期有延续但以此版资源最完整） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：线代、概率论、Python |

## 为什么学

- 极少见的公开系统课：能完整听到 LeCun 本人从一线研究者视角讲深度学习。
- 理论与直觉兼顾、偏研究导向，专治"会用不会想"的建模品味问题。
- 期末作业"从零实现 GPT-2 mini"是全网口碑最硬的 LLM 实战训练之一。
- 作为主线课程之外的高质量补充极有价值：每讲 slides + 作业自成体系。

## 先修与知识联系

- 先修：Python、线代、概率论；建议先过 CS230 建立全局图景。
- 纵向：本课 L6-L8 语言模型线直通 CS224n；L4 CNN 线衔接 CS231n/EECS498-007。
- 横向：L9 强化学习可作 CS285 预热；期末 GPT-2 mini 与 llama.c/HF nanoGPT 同源互参。

## 讲义章节目录（Spring 2021 十周课表，据公开讲义页整理）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 深度学习导论与线性模型（LeCun） | Intro & Linear Models slides |
| L2 | 多层感知机（LeCun） | MLP slides |
| L3 | 自动微分（客座：François Fleuret） | autodiff 讲义 |
| L4 | 卷积神经网络（LeCun/Canziani） | CNN slides；LeNet 论文 |
| L5 | 无监督学习：嵌入、聚类与倒排索引（Canziani） | JEPA/能量视角笔记 |
| L6 | 序列模型与语言建模（客座：Kyunghyun Cho） | RNN/LSTM/GRU slides |
| L7 | 注意力机制与 Transformer | Attention slides |
| L8 | 深度语言模型：BERT 与 GPT（客座：Zoltán Ambrus） | BERT/GPT 论文 |
| L9 | 强化学习（客座） | DQN/PPO 讲义 |
| L10 | 深度学习新浪潮（Guest）＋ 期末项目：Build GPT-2 Mini | nanoGPT 说明 |

> 作业线：每周 Assignment（numpy/PyTorch），压轴为多周推进的 Final Project——从零搭出可训练的 GPT-2 mini。
