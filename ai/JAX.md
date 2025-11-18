# JAX

### JAX 是什么？一句话概括

JAX 是 Google 研发的下一代高性能数值计算和机器学习框架，本质上是“NumPy 的加速器 + 自动微积分 + 编译器魔法”的完美结合。官方 slogan 是：

"NumPy + AutoDiff + XLA = JAX"

它从 2018 年左右开始在 Google 内部疯狂流行，2020 年开源后迅速把 TensorFlow/PyTorch 甩在身后，成为 2023-2025 年大模型圈真正的“内部卷王”。

### 为什么大家说 JAX 吊打 TensorFlow/PyTorch？

| 维度              | TensorFlow 2.x              | PyTorch                     | JAX                              |
|-------------------|-----------------------------|-----------------------------|----------------------------------|
| 代码风格          | 又想 eager 又想 graph，折磨  | 最像 Python，写着最爽        | 纯函数式，像写 NumPy 一样极简     |
| 自动微分          | tf.GradientTape（还行）      | 最强，最自然                 | vjp/jvp/hessian 随便玩，数学上最纯正 |
| 性能              | 一般（XLA 阉割版）           | 好，但大模型容易 OOM        | XLA 全编译，TPU 上碾压一切        |
| 并行方式          | DistributionStrategy（繁琐） | DDP/FSDP（还行）            | pmap/shard_map 一行代码全自动     |
| 大模型训练（万卡）| 基本放弃了                  | Megatron/DeepSpeed 各种 hack | GSPMD + MaxText 原生支持，代码几百行 |
| 可调试性          | 图模式基本没法 debug        | 最强                        | jit 后还能 jax.debug 可视化中间值  |
| 确定性            | 随机数各种坑                 | 容易不一致                  | 完全确定性，三种子控制一切         |

### JAX 的四大核心神器（99% 的牛逼都来自这四个）

1. jit（@jax.jit）—— 超音速编译器  
   把普通 Python 函数一键编译成 XLA 优化后的内核，第一次慢，之后快到飞起。  
   ```python
   @jax.jit
   def f(x):
       return x @ x + jnp.sin(x)  # 随便写，像 NumPy
   ```

2. grad / vmap / pmap —— 自动微分 + 自动向量化 + 自动并行  
   这三个组合拳直接把科研生产力拉到天花板：
   ```python
   from jax import grad, vmap, pmap

   grad_f = grad(lambda x: jnp.sum(x2))     # 自动求导
   batched_f = vmap(f, in_axes=0)             # 自动 batch（比 torch.vmap 还强）
   parallel_f = pmap(f, in_axes=0)            # 自动多卡/多 TPU 并行
   ```

3. pytree —— 让嵌套结构也变得优雅  
   参数可以是任意嵌套的 dict/list/tuple，JAX 自动 flatten/unflatten，训练大模型时再也不用手写 param list 了。

4. XLA + 真正的函数式变换  
   JAX 是纯函数式（pure functional），没有副作用，所以可以随意做代码变换（remat、scan、cond、while_loop 等），这才是它能轻松训练万亿参数模型的根本原因。

### 2025 年 Google 内部真实用法（基本全是这些）

- Gemini / Gemma 系列 → MaxText（基于 JAX）
- PaLM 2 / Gemini Ultra → T5X + JAX（早期）→ 后来全转 MaxText
- DeepMind AlphaFold 3、Grok 1（部分）、Gemini 1.5+ 全是 JAX
- Google 几乎所有新大模型项目默认起手就是 JAX + Flax/Orbax 或 MaxText

### 常用生态（2025 年最新）

| 库          | 用途                          | 地位                 |
|-------------|-------------------------------|----------------------|
| Flax        | 最老牌的 JAX 神经网络库        | 还活着，但被取代趋势 |
| Orbax       | 新一代 checkpoint/training 库 | 2024-2025 标配       |
| MaxText     | Google 官方万卡大模型训练框架  | 真正的内部压箱底     |
| Equinox     | PyTorch 风格的 JAX 库（最丝滑）| 个人/小团队最爱      |
| Haiku       | DeepMind 出品，儿子库         | AlphaFold 用这个     |
| Optax       | 优化器合集（比 torch.optim 强）| 人人必装             |
| Distrax     | 概率分布库（比 torch.distributions 好用） | RL/生成模型必备 |

### 给普通人的上手建议（三天就能上手）

```python
import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

@jit
def selu(x, alpha=1.67, lmbda=1.05):
    return lmbda * jnp.where(x > 0, x, alpha * jnp.exp(x) - alpha)

x = jnp.arange(1000000.)
%timeit -n 5 selu(x).block_until_ready()   # 第一次编译慢，之后超快
```

写着像 NumPy，跑着比 CUDA 手写还快，调试还简单——这就是 JAX 的魔法。

### 总结：2025 年的真实现状

- TensorFlow → 基本只剩外部生态和老项目在用，Google 内部早已边缘化
- PyTorch → 外部社区最强，科研首选，但 Google/DeepMind 内部几乎没人用了
- JAX → Google + DeepMind 当前的绝对主力，Gemini 全系列、AlphaFold 3、几乎所有新项目默认 JAX

所以当有人跟你吹“我用 TF 训练大模型”的时候，你就可以默默微笑：  
“可爱，他还不知道 2025 年谷歌内部早把 TF 当文物供起来了～”

想入坑 JAX？直接从官网教程开始，三天后你就会感叹：原来写深度学习代码可以这么优雅！  
官网：https://jax.readthedocs.io
