# MIT 6.5940: TinyML and Efficient Deep Learning Computing 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 6.5940: TinyML and Efficient Deep Learning Computing（原 6.5945/6.884 系谱） |
| 学校 | MIT |
| 主讲 | Song Han（韩松） |
| 教材 | 无；官方 slides + Han 组论文清单即为阅读材料 |
| csdiy 路径 | `机器学习系统/MIT6.5940: TinyML and Efficient Deep Learning Computing`（页面更新：2025-01-09） |
| 最新期次 | Fall 2024（官网提供 2024fall/2023fall 两版完整资源） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 50 小时；先修：体系结构、深度学习基础；语言 Python |

## 为什么学

- 韩松（Song Han）亲授的高效 ML 标杆课：剪枝、量化、蒸馏、NAS、稀疏化与高效芯片设计是其开创方向（Deep Compression 等代表作）。
- 三段式全栈覆盖：①神经网络轻量化关键技术 → ②面向大模型/多模态/生成模型的高效推理与系统 → ③大规模分布式高效训练。
- 内容与工业界同步：LLM 推理优化（vLLM/AWQ/投机解码）、长上下文、后训练加速都是 2023-2024 热点。
- 5 个作业难度友好且直击核心：量化、剪枝、NAS、LLM 压缩、LLM 高效部署。

## 先修与知识联系

- 先修：体系结构（CS61C/CA）、深度学习基础（CS230 级别）。
- 前导：CMU10-414（系统骨架）；NeuralNets-ZeroToHero（模型侧）。
- 平级：MLC（编译视角互补）、CSE234/CMU15-442（LLM 系统进阶）、AICS（全栈实验中文路线）。
- 知识输出：量化 → llm.cpp/AWQ/TensorRT；稀疏化 → NVIDIA Sparse Tensor Core；NAS → MNN/Once-for-All。

## 讲义章节目录（对应 Fall 2024 官方讲次）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：高效 ML 全景与算力/能耗瓶颈 | Lecture 1 slides |
| L2 | 高效深度学习设计 I：剪枝（结构化/非结构化、Lottery Ticket） | Han et al. 2015/2016 |
| L3 | 高效深度学习设计 II：NAS 与轻量化架构（MobileNet/ShuffleNet/EfficientNet） | Zoph & Le 2017；Howard et al. |
| L4 | 量化与低精度：PTQ/QAT、权重激活量化 | Han et al. 2016；Jacob et al. 2018 |
| L5 | TinyML I：MCU 上的模型压缩与部署（Edge Impulse 案例） | Banbury/Dave 讲义 |
| L6 | TinyML II：高效芯片与系统（Eyeriss/小硬件设计） | 课程 papers |
| L7 | 高效 Transformer：稀疏/低秩注意力、长上下文 | Tay et al. 2020 效率综述 |
| L8 | 高效 LLM 推理 I：GPTQ/AWQ/SmoothQuant/LLM.int8 | Frantar 2023；Lin 2023；Xiao 2023；Dettmers 2022 |
| L9 | 高效 LLM 推理 II：vLLM/PagedAttention、投机解码、离群值 | Kwon 2023；Leviathan 2023；Dettmers 2024 LLM in a flash |
| L10 | 多模态与视觉高效模型：ViT/MLLMA 压缩与蒸馏 | 相关论文 |
| L11 | 扩散模型与生成模型加速 | Chen 2023 蒸馏/采样加速 |
| L12 | 高效训练 I：分布式并行（DP/TP/PP/ZeRO） | Sheng? ZeRO 2020；Megatron 2019 |
| L13 | 高效训练 II：梯度压缩、通信高效、MoE | Sheng et al. FLGC / Mixtral 2024 |
| L14 | 端侧训练与联邦、后训练加速与总结 | SGLB/JanusAI 等延伸 |

> 注：各学期讲次名称略有调整，以 eecs.mit.edu 6.5940 课程站为准。

## 课程资源（摘自 csdiy）

- 课程网站：2024fall / 2023fall（MIT EECS 课程页）
- 课程视频：YouTube 官方；B 站有生肉/熟肉搬运
- 课程作业：共 5 个实验（量化/剪枝/NAS/LLM 压缩/LLM 部署）
- 资源汇总：PKUFlyingPig/MIT6.5940_TinyML（GitHub）
