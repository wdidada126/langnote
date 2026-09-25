# EECS498-007 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| LeNet | 1998 | L5 | 卷积网络定型 |
| AlexNet | 2012 | L6 | 深度 CNN 引爆 CV |
| VGG | 2014 | L6 | 小卷积堆叠深度化 |
| ResNet | 2015 | L6 | 残差学习百层可训 |
| Batch Normalization | 2015 | L8 | 加速收敛标配 |
| Fully Convolutional Networks (FCN) | 2014 | L9 | 全卷积语义分割 |
| U-Net | 2015 | L9 | 跳连分割医学影像经典 |
| Fast R-CNN / Faster R-CNN | 2015 | L11 | ROI 池化与 RPN 两阶段检测 |
| SSD | 2015 | L12 | anchors 单阶段检测 |
| YOLO | 2015 | L12 | 网格直接回归检测 |
| Show and Tell | 2014 | L14 | 图像描述 encoder-decoder |
| Attention Is All You Need | 2017 | L16 | Transformer |
| ViT | 2020 | L17 | 图像 patch 化 Transformer |
| PointNet | 2016 | L19 | 点云置换不变学习 |
| NeRF | 2020 | L19 | 隐式神经渲染 |
| VAE | 2013 | L20 | 变分生成 |
| GAN | 2014 | L21 | 对抗生成 |
| A Neural Algorithm of Artistic Style (Gatys) | 2015 | L22 | 风格迁移 |
| CLIP | 2021 | L22 | 图文对比学习 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| YOLOv3→v8/v11 工程演进综述 | 2021-2024 | L12 单阶段检测现役方案 |
| DINO / DINOv2 | 2021-2023 | L6/L17 自监督视觉表征 |
| Segment Anything (SAM/SAM2) | 2023-2024 | L9-L10 可提示分割基座 |
| DETR | 2020（2021 起普及） | L11-L12 集合预测端到端检测 |
| Stable Diffusion (LDM) | 2022 | L20-L21 生成主流转向扩散 |
| DiT (Diffusion Transformers) | 2023 | L17+L21 生成架构 Transformer 化 |
| LPIPS 感知度量与图像复原评估 | 2021 | L22 可视化评估 |
| VideoMAE / 视频理解进展 | 2022-2023 | L13-L14 时序扩展 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| PyTorch 基础（L4） | PyTorch 官方 tutorials | 本课程 Handout 即最佳入门材料 |
| CNN backbone（L5-L6） | timm / torchvision | 预训练权重库与训练 recipe |
| 检测（L11-L12） | ultralytics YOLO / Detectron2 | 两阶段与单阶段工业实现 |
| 分割（L9-L10） | MMSegmentation / SAM | 分割工具箱与可提示分割 |
| Transformer/ViT（L16-L17） | HF transformers (VisionTransformer) | 视觉 Transformer 标准件 |
| 3D/NeRF（L19） | nerfstudio / Open3D | 隐式渲染与点云管线 |
| 生成（L20-L22） | diffusers / StyleGAN3 官方实现 | VAE/GAN/扩散组件 |
| 风格迁移（L22） | fast-neural-style | 前馈式风格迁移复现 |
