# 01 · TF2 与 Keras 基础

> ⚠️ 题注：章名为本笔记按书中网络类型带段**自拟映射**（对应 TF2/Keras 上手内容段），
> 逐字目录待销账，不冒充原书章名。三态口径：✅=tensorflow.org/Keras 官方文档口径；
> ⚠️=凭记忆推定书中内容；🔧=未实测：本机未装 tensorflow（2026-10 实测 tf/torch 均无）。

## 核心机制

1. **Eager execution 是 TF2 的地基**：TF1 的「先建图后 feed」静态图心智被动态 eager
   替换，Python 控制流即真控制流——这与 PyTorch 2017 起的 Define-by-Run 是同一路
   （✅ 口径）。`tf.function` 再按需把 eager 代码图化，对应 PyTorch 的 `torch.compile`
   （书后产物 ⚠️ 提及不展开）。
2. **Keras 训练三件套**：`model = Sequential([...])` → `compile(loss, optimizer,
   metrics)` → `fit(x, y, epochs)`。对照 PyTorch 显式循环：

   ```python
   # Keras（✅ API 口径；🔧 未实测：本机未装 tensorflow）
   model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
   model.fit(x_train, y_train, epochs=5)

   # PyTorch 等价物：优化器与 loss 手工接线
   # opt = torch.optim.Adam(net.parameters()); crit = nn.CrossEntropyLoss()
   # for xb, yb in loader:
   #     opt.zero_grad(); crit(net(xb), yb).backward(); opt.step()
   ```
   Keras 把「梯度归零/backward/step」藏进 `fit`，换来黑箱感——2026 视角：Keras 3
   多后端（JAX/torch/TF）后高层 API 走向变局 🟡，书中 `tf.keras` v2 细节别当现行。
3. **数据管道**：`tf.data.Dataset`（batch/shuffle/prefetch 的声明式流水线）对照
   PyTorch `Dataset`+`DataLoader`（命令式、多进程 worker）。Java/C++ 锚：TF 生态另有
   C API 与 Lite 运行时，DL4J 用 `DataSetIterator` 承担同一角色（衔接 06 档）。

## 批判读法

- 食谱式起步快，但 `fit` 一藏，学员不知道「反向传播发生在哪一行」——练完本书这段，
  务必用 d2l 手写一次训练循环再回头。
- 书中若仍以 `model.layers.add` 时代口吻讲 v1/v2 兼容层（`tf.compat.v1`）🟡：2026
  直接跳过，v1 图模式 API 已死。

## 🔧 微实验位（未实测：本机未装 tensorflow）

1. 同一 MLP 分别用 Keras `fit` 与手写 `tf.GradientTape` 循环训练，对比逐 epoch loss，
   验证 `fit` 的默认 shuffle 差异。
2. `prefetch(tf.data.AUTOTUNE)` on/off 的吞吐计时——理解声明式管道「存在意义」。

## 中英对照

| 英文 | 中文 | 一句注 |
| --- | --- | --- |
| eager execution | 即时执行 | TF2 默认，动态求值 |
| graph mode / `tf.function` | 图模式 | 需要时再编译加速 |
| compile / fit / evaluate | 编译/训练/评估 | Keras 三件套动词 |
| dataset pipeline | 数据管道 | tf.data 声明式 |
| callback | 回调 | 早停、检查点挂载点 |

## 盘谱互链（均已实测存在）

- 回：[00-总览与阅读地图.md](00-总览与阅读地图.md)；下：[02-前馈与回归.md](02-前馈与回归.md)。
- 同线：[../ProgrammingTensorFlow2.md](../ProgrammingTensorFlow2.md)（同为 2021 TF2 书，API 章对读）；
  [../TensorFlow实战Google深度学习框架2.md](../TensorFlow实战Google深度学习框架2.md)（中文概念地图，1.x 已废）。
- 深度：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)、[../深度学习_花书.md](../深度学习_花书.md)。

## ⚠️ 欠账

逐字章名/页码未销账；Keras 3 迁移影响面待有环境后实测回填。
