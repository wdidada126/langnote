# CS231n 论文清单与开源映射（papers.md）

> 配套 `notes/L01–L13.md` 与 `projects/` 使用；讲次编号按 Spring 2025 课表。
> 状态：全量（2026-09）。

## 一、经典论文表（课程主线，1989–2020）

| 论文 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| LeCun et al., *Backprop Applied to Handwritten Zip Codes* / LeNet-5 (1998) | 1989/1998 | 端到端 CNN 手写识别，卷积/池化/共享全部原语 | L01, L04, L05 |
| Krizhevsky et al., **AlexNet** | 2012 | ImageNet 夺冠：ReLU/Dropout/数据增强/GPU 双卡 | L01, L06 |
| Simonyan & Zisserman, **VGG** | 2014 | 3×3+pool 极简语法堆到 16–19 层，迁移学习首选 backbone | L06 |
| Szegedy et al., **GoogLeNet / Inception** | 2014 | 多分支并联 + 1×1 瓶颈降维 | L06 |
| He et al., **ResNet**（+ v2 预激活） | 2015 | 残差连接治"退化"，152 层可训，深度里程碑 | L06, L08 |
| Ioffiche & Szegedy, **Batch Normalization** | 2015 | 激活标准化平滑损失面、提速训练 | L06 |
| Sandler et al., **MobileNetV2** | 2018 | 深度可分离 + 倒残差，端侧高效 backbone | L06 |
| Girshick et al., **R-CNN** → He et al., **Mask R-CNN**（系列：Fast/ Faster R-CNN） | 2014–2017 | 候选区域→两阶段检测，Faster R-CNN 的 RPN 端到端化 | L09 |
| Liu et al., **SSD** | 2016 | 多尺度锚框单阶段检测 | L09 |
| Redmon et al., **YOLO**（→ YOLOv2/v3/v5） | 2016 | 网格直接回归框，实时检测范式 | L09 |
| Long et al., **FCN**；Ronneberger et al., **U-Net** | 2015 | 全卷积语义分割；编解码+跳连（医学影像标配） | L09 |
| Szegedy et al., **Deep Dream / 特征可视化**；Selvaraju, **Grad-CAM** | 2015/2017 | 理解网络内部表示与归因可视化 | L09 |
| Mikolov et al., word2vec；Sutskever et al., seq2seq | 2013/2014 | 嵌入与编码-解码：序列视觉的前夜 | L07 |
| Hochreiter & Schmidhuber, **LSTM** | 1997 | 门控记忆治梯度消失 | L07 |
| Bahdanau et al., 注意力；**Vaswani et al., Transformer** | 2014/2017 | 注意力对齐 → 纯注意力并行序列模型 | L08 |
| Dosovitskiy et al., **ViT** | 2021 | 图像切 patch 进 Transformer，大数据下超越 CNN | L08 |
| Radford et al., **CLIP** | 2021 | 4 亿图文对比学习，开放词汇识别与零样本 | L08, L12 |
| Goodfellow et al., **GAN** | 2014 | 生成器-判别器极小极大博弈 | L13 |
| Kingma & Welling, **VAE** | 2013 | 变分下界 ELBO 端到端生成 | L13 |
| Kingma & Ba, **Adam**；Loshchilov & Hutter, **AdamW** | 2015/2019 | 自适应优化与解耦权重衰减，训练标配 | L03 |
| Srivastava et al., **Dropout** | 2014 | 随机失活作为组合正则 | L03, L07(训练策略) |

## 二、近 5 年论文表（2021–2026，标注开源可用性）

| 论文 | 年份 | 一句话贡献 | 关联讲次 | 开源 |
| --- | --- | --- | --- | --- |
| Liu et al., **Swin Transformer** | 2021 | 移位窗口注意力把 Transformer 拉回层级视觉 | L08 | 是（MS, mit-swin） |
| Woo et al., **ConvNeXt** | 2022 | 现代化纯 CNN 对齐 ViT，"卷积没死" | L06, L08 | 是（timm/FAIR） |
| Ramesh et al., **DALL·E 2 / Imagen**；Rombach et al., **Stable Diffusion (LDM)** | 2022 | 文本→图像扩散生成；潜空间降算力 | L13 | SD 是（CompVis/Stability），其余部分 |
| He et al., **MAE** | 2022 | 掩码自编码像素重建，视觉自监督简单粗暴有效 | L12 | 是（FAIR/timm） |
| Oquab et al., **DINOv2** | 2023 | 自蒸馏 + 大规模策展，通用视觉特征即拿即用 | L12 | 是（facebookresearch/dinov2） |
| Kirillov et al., **SAM**；Ravi et al., **SAM 2** | 2023/2024 | 可提示分割基础模型；SAM2 扩展至视频 | L09, L10, L12 | 是（facebookresearch/sam2） |
| Yang et al., **Depth Anything V2** | 2024 | 单目深度稠密预测的"类 SAM 时刻" | L09, L12 | 是 |
| Li et al., **LLaVA** | 2023 | CLIP 视觉塔 + LLM 的开源多模态对话 | L08, L13(多模态) | 是（haotian-liu/LLaVA） |
| Alayrac et al., **Flamingo**；OpenAI **GPT-4V** 系 | 2022/2023 | 交叉注意力桥接冻结 LLM 的视觉语言模型 | L08, L13 | 部分/否（方法公开，权重未全开） |
| Kirilyuk et al., **Grounding DINO**；Deformable DETR 系 | 2023 | 开放集检测，文本查询框 | L09 | 是（IDEA） |
| Li et al., **VideoMAE / X-CLIP** 等视频自监督 | 2022 | 视频掩码重建/跨模态对比 | L10 | 是 |
| Dao et al., **FlashAttention-2/3** | 2022–2024 | IO 感知精确注意力，长序列训练提速数倍 | L08, L11 | 是（Dao-AILab） |
| Shoeybi et al. → Rajbhandari, **ZeRO / DeepSpeed** | 2019–2022 | 优化器状态/参数/梯度切分，单机装下大模型 | L11 | 是（Microsoft） |
| Gu & Dao, **Mamba**（状态空间模型） | 2023 | 选择性 SSM 线性复杂度，RNN 思想的现代复活 | L07, L08 | 是（state-spaces/mamba） |
| Yang et al., **Qwen-VL / Qwen2.5-VL** | 2023–2025 | 开源多模态 LLM 主力，原生动态分辨率 | L08, L13 | 是（Qwen 团队） |
| Esser et al., **Stable Diffusion 3 / rectified flow**；Black Forest **FLUX** | 2024 | 流匹配扩散简化与 DiT 主干生成 SOTA | L13 | 部分（权重可下载，训练数据不开源） |
| Bai et al., **LLaVA-OneVision**；Qwen2.5-VL 技术报告 | 2024–2025 | 单图/多图/视频统一输入，视觉思维链与高分辨率原生支持 | L10, L13 | 是 |
| NVIDIA **Cosmos / Genie 系世界模型** | 2024–2025 | 视频生成作为世界模拟/机器人数据引擎 | L10, L13 | 部分（开放权重/数据不开源） |
| **OpenVLA / π0** | 2024–2025 | 视觉-语言-动作（VLA）模型开源化 | L13, 课程尾声 | 是（OpenVLA）/部分（π0） |

## 三、知识点 ↔ 开源项目映射表

| 知识点（讲次） | 开源项目 | 对应位置 |
| --- | --- | --- |
| 线性分类/softmax（L02） | scikit-learn；**projects/P1** | `LogisticRegression`/`SGDClassifier(hinge)`；numpy 手写 |
| 优化器/调度（L03） | PyTorch `optim`、timm、DeepSpeed | `AdamW`/`CosineAnnealingLR`/ZeRO |
| 反向传播/自动微分（L04） | PyTorch autograd、JAX、**micrograd**、tinygrad；**projects/P1/P2** | 计算图与 `backward()` |
| 卷积与 fast conv（L05） | cuDNN、ggml/llama.cpp、**projects/P2** | im2col+GEMM/Winograd |
| CNN 架构（L06） | **timm**、torchvision、pycls | `resnet50`/`vgg16`/`convnext_*` 预训练权重 |
| BatchNorm（L06） | timm `BatchNormAct2d`；**projects/P2** | 含 train/eval 差异的手写 BN |
| RNN/LSTM（L07） | PyTorch `nn.LSTM`、ESPnet、llama.cpp(whisper 前端) | 序列塔 |
| 注意力/Transformer/ViT（L08） | **HF transformers**（`ViTModel`）、timm `vit_*`、flash-attn | 缩放点积/多头实现；**projects/P3** numpy 版 |
| 检测（L09） | **ultralytics YOLO**、Detectron2、mmdetection、Grounding DINO | 训练/推理全套；RPN/anchor-free |
| 分割（L09） | segment-anything（SAM/SAM2）、MMSeg、nnU-Net(U-Net 继承者) | 可提示分割/医学分割标配 |
| 可视化理解（L09） | LIT、caporn Caparn、pytorch-grad-cam | 特征图归因 |
| 视频（L10） | PyTorchVideo、MMAction2、SAM2(视频)、X-CLIP | 时间采样+两流/3D 卷积 |
| 分布式/效率（L11） | DeepSpeed、PyTorch FSDP、Megatron-LM、accelerate | AllReduce/流水并行/混合精度 |
| 自监督（L12） | DINOv2、MAE 官方实现、timm 自监督 recipe、CLIP openai/CLIP | 预训练代码+权重 |
| 生成模型（L13） | **HF diffusers**（Stable Diffusion/FLUX 管线）、StyleGAN3（NVLabs）、torchvision wgan；**projects/P3** 玩具 GAN/VAE | 采样循环/训练循环 |
| 多模态（L13） | LLaVA、Qwen2.5-VL（HF transformers 集成）、**vLLM**（多模态推理引擎）、llama.cpp（MTMD 视觉） | 视觉塔+投影+LLM 的部署栈 |

## 四、建议精读路线（三遍法）

1. **第一遍（随课）**：AlexNet → VGG → ResNet → BN → Transformer → ViT → CLIP → GAN/VAE，每篇配一篇 Notes。
2. **第二遍（作业驱动）**：A1 前后重读 Backprop Notes；A2 时读 Faster R-CNN+U-Net+ResNet 代码级复现；A3 时读 DCGAN/WGAN-GP 与 VAE 原文。
3. **第三遍（前沿对齐）**：按第二张表挑近 5 年 3–5 篇做"复现级"精读（推荐：DINOv2、SAM、MAE、ConvNeXt、LDM），
   并用本仓库 [projects/](projects/README.md) 的 numpy 玩具版校准理解——写得出最小实现，才算真读懂。
