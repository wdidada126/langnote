# CS231n 配套项目（纯 numpy + 标准库，无 torch）

> 三组项目对应课程三个 Assignment 的核心训练，按讲次递进；
> 全部数据为 numpy 程序化合成，**不下载任何数据集**；本轮"只写不编译"，
> `run.sh`/`run.bat` 为 `python -m py_compile` 语法检查模式，真实运行需 `pip install numpy`。

## 讲次 → 项目 → 知识点

| 项目 | 对应讲次 | 对标作业 | 核心知识点 |
| --- | --- | --- | --- |
| [p1_image_classifier/](p1_image_classifier/README.md) | L01-L04 | A1 | 数据三分与预处理；kNN 与向量化距离；hinge/softmax 损失与手推梯度；数值梯度检查；SGD+momentum+L2 网格调参 |
| [p2_convnet/](p2_convnet/README.md) | L04-L07 | A2 | naive 四重循环卷积 → im2col/GEMM 快速卷积（等价性校验）；卷积/pool/BN 反向；CONV-BN-ReLU-POOL×2+FC 训练循环；He 初始化与 train/eval(BN) 切换 |
| [p3_transformer_generation/](p3_transformer_generation/README.md) | L08, L13 | A3 | 缩放点积/多头注意力手推前反向；LayerNorm；patchify+位置嵌入+TinyViT 训练；GAN minimax 交替训练与模式覆盖；VAE ELBO（重构+闭式 KL）与重参数化 |

## 与课程的映射说明

- P1 覆盖 L01（管线/数据划分）、L02（kNN+SVM+softmax）、L03（优化+梯度检查）、L04（MLP 前奏）；
- P2 覆盖 L04（反向传播复用）、L05（卷积数学与两种实现）、L06（BatchNorm、卷积积木堆叠）、L07（调参：lr/初始化/早停）；
- P3 覆盖 L08（注意力/Transformer/ViT）与 L13（VAE/GAN）；L09-L12 属"任务与系统"讲次，
  以阅读与改造 P2 backbone 的方式联动（如给 P2 的 CNN 加全局池化头模拟 GAP、
  用 P2 的 conv 层搭 U-Net 玩具）；L07 RNN、L10 视频、L11 分布式、L12 自监督
  建议直接阅读对应 notes 后在 PyTorch A2/A3 中体验。

## 统一运行方式

```bash
# Linux / macOS
cd p1_image_classifier && ./run.sh && python3 main.py
cd ../p2_convnet       && ./run.sh && python3 main.py
cd ../p3_transformer_generation && ./run.sh && python3 main.py all
```

```bat
:: Windows
cd p1_image_classifier && run.bat && python main.py
cd ..\p2_convnet && run.bat && python main.py
cd ..\p3_transformer_generation && run.bat && python main.py all
```

三个 `main.py` 均设计为 CPU 秒级~分钟级；每个文件头部 docstring 标注对应讲次，
可与 `../notes/LXX.md` 交叉阅读。
