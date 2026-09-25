# P3 · Transformer 与生成模型（attention/TinyViT + 玩具 GAN/VAE）

> 对应讲次：L02（softmax 头）、L04（反向传播）、L06（BN→LN）、L07（残差）、
> L08（注意力与 ViT）、L13（VAE/GAN）。对标 Assignment 3 的 numpy 玩具版。
> 纯 numpy + 标准库，不依赖 torch；数据全部合成。

## 知识点 ↔ 文件

| 文件 | 知识点 | 讲次 |
| --- | --- | --- |
| `mlp.py` | affine/relu/softmax 层、通用 MLP 与 SGD+momentum（三模型共用积木） | L02-L04 |
| `data.py` | 四象限斑点图（ViT 分类任务）、2D 三高斯混合（GAN/VAE 目标分布） | L08, L13 |
| `attention.py` | 缩放点积注意力（`√d_k`、softmax 反向 `P⊙(dP-rowsum)`）、多头投影 | L08 |
| `layernorm.py` | LayerNorm 前反向（对比 spatial BN：逐样本、无 train/eval 差异） | L06, L08 |
| `vit.py` | patchify、位置嵌入、post-LN Transformer 块、cls 头、全手动反传 | L08 |
| `gan.py` | minimax 训练循环、D/G 交替、模式覆盖统计 | L13 |
| `vae.py` | ELBO（重构+闭式 KL）、重参数化、手推 μ/logvar 梯度、先验采样 | L13 |
| `gradient_check.py` | 通用闭包式梯度检查 | L03 |
| `main.py` | `vit/gan/vae/all` 三个子命令 | 全流程 |

## 运行

需要 Python ≥ 3.8 与 `numpy`。

- Linux / macOS：
  ```bash
  ./run.sh                      # 语法检查模式（py_compile 全部 .py）
  python3 main.py all           # 真实演示（CPU 分钟级内）
  ```
- Windows：
  ```bat
  run.bat
  python main.py vit            :: 或 gan / vae / all
  ```

## 观察与练习

1. MHA/LayerNorm 的梯度检查相对误差应在 1e-5 以下——注意力反传是 A3/面试高频考点；
2. TinyViT 在小数据上即可分类四象限任务；把 `pos` 置零再训：位置信息消失后学不动（L08 1.3）；
3. GAN 的 `mode_stats` 打印覆盖模式数：调大 D 学习率观察模式崩溃/震荡（L13 1.3）；
4. VAE 样本均值趋近数据重心：重构-锐度权衡；把 `dec_std` 调小→更像 MSE 自编码器；
5. 同一积木（mlp.py + 手推梯度）支撑三种范式：分类（P1）、判别（GAN 的 D）、生成（G/VAE 解码器）——
   这就是 CS231n 想让你体会的"深度学习大一统"。
