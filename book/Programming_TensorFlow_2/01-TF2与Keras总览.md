# 01 · TF2 与 Keras 总览

> 章名 ⚠️ 凭记忆推定带段，逐字目录待购电子版销账。对应 *Programming TensorFlow 2*（Packt·2021 ⚠️，作者疑 Chris McLendon ⚠️）入门带段：TF2 eager 模型 + `tf.keras` 高层 API 首课。
> 时效注：书 API 截点 2021（TF 2.x + tf.keras 2.x），对照现行官方文档 tensorflow.org / keras.io；Keras 3 多后端变局见本档批判读法。🔧 一律「未实测：本机未装 tensorflow」。

## 一、核心机制

### 1. eager 执行：从图到即时求值
- TF1 时代「先建图后 session.run」被 eager（默认开启）取代：算子调用即出结果，Python 断点可进张量 ⚠️ 推定为书第 1–2 章卖点。
- 想要图性能再「编译」回去：`@tf.function` 把 Python 函数追踪（AutoGraph）成 TF 图——**eager 是默认态、graph 是优化态**，与 TF1 的方向正好相反。
- PyTorch 对照：PyTorch 自生即动态（define-by-run），TF2 是**向 PyTorch 开发体验的投降式改版**；`@tf.function` ≈ `torch.compile`（2020 年书中尚无后者），概念对位但机制不同：一个 trace 成静态图，一个编译。⚠️ 归属推定。

### 2. GradientTape：手写训练循环的底座
```python
with tf.GradientTape() as tape:                 # 记录前向运算 ⚠️ API 形状凭记忆
    logits = model(x_batch, training=True)
    loss = loss_fn(y_batch, logits)
grads = tape.gradient(loss, model.trainable_variables)
optimizer.apply_gradients(zip(grads, model.trainable_variables))
```
- PyTorch 锚点：`tape` ≈ `loss.backward()` + `optimizer.step()`；差别在 TF 把「记录带」显式化为上下文管理器，PyTorch 把梯度自动挂在叶子张量 `.grad` 上。`training=True` 参数对应 PyTorch `model.train()` 的模式开关——Keras 层把「训练/推理行为差异」（Dropout/BN）做成**调用级参数**，这是两边最易踩混的一处。

### 3. tf.keras 高层面：Model / fit / callbacks
- `Sequential([...])` 或函数式 `Model(inputs, outputs)` → `compile(optimizer, loss, metrics)` → `fit(x, y, epochs, batch_size, validation_split)` → `evaluate` / `predict`。⚠️ 参数名凭通行口径，不冒充书中原文。
- `model.fit` 的 callback 体系（EarlyStopping/ModelCheckpoint）≈ PyTorch 手写循环里塞验证逻辑——Keras 的「五行起模型」便利与 PyTorch 的「循环全裸露」透明是两种工程取舍。

## 二、批判读法
- **Keras 3 变局**：书成于 `tf.keras` 与 standalone Keras 尚未分家的 2021；此后 Keras 3 多后端（JAX/PyTorch/TF），「Keras=TF 子模块」的心智模型已过期——本带段所有 API 形状先查现行官方文档再抄 ⚠️。
- 教学册常把 `@tf.function` 追踪陷阱（Python 控制流被固化、外部可变状态失真）轻描淡写；eager↔graph 语义差是本册**最该精读**又最易被略过的一节 ⚠️ 推定。
- 与同代书重复度高：概念地图可先用 [../TensorFlow实战Google深度学习框架2.md](../TensorFlow实战Google深度学习框架2.md)（中文），本页只补工程口径。

## 三、🔧 微实验位（未实测：本机未装 tensorflow）
- E1：同一线性回归，分别用 eager 手写 GradientTape 循环与 `model.fit` 跑，对比 loss 曲线是否逐 epoch 一致——验证两条路径数值等价性。
- E2：给一个含 `if x > 0:`（张量条件）的函数加 `@tf.function`，观察 AutoGraph 转换成功/报错边界；去掉装饰器对照 eager 行为。
- E3：Dropout 层在 `training=True/False` 下输出方差对比，坐实「调用级模式开关」语义。

## 四、盘谱互链（写前 ls 实测 ✅）
- 本目录：[00-总览与阅读地图.md](00-总览与阅读地图.md)（总地图）→ 管道下钻 [02-tf.data数据管道.md](02-tf.data数据管道.md) → 训练全套 [03-经典网络与训练.md](03-经典网络与训练.md)。
- 书外：[../DeepLearningWithPython2e.md](../DeepLearningWithPython2e.md)（Chollet 本尊的 Keras 心智模型）、[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)（框架中立原理）、[../TensorFlow实战Google深度学习框架2.md](../TensorFlow实战Google深度学习框架2.md)（TF1 图时代对照，理解 eager 改版动机）。

## 五、自测（讲不出=回去重读）
1. `@tf.function` 与 eager 的语义边界在哪？哪些 Python 行为会被追踪固化？
2. GradientTape 与 `loss.backward()` 谁负责「记录什么」？`training=True` 影响哪两类层？
3. Keras 3 多后端为什么动摇了「tf.keras=Keras」这个 2021 心智模型？

## 六、中英对照

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 即时执行 | eager execution | 调用即求值，默认态 |
| 函数追踪 | tf.function / AutoGraph tracing | Python 函数编译成 TF 图 |
| 梯度记录带 | GradientTape | 显式记录前向以供求导 |
| 训练态开关 | training argument | Dropout/BN 行为随调用参数变 |
| 回调 | callback | fit 循环的钩子体系 |
| 可训练变量 | trainable variables | 模型参数的 TF 侧称呼 |

## 七、⚠️ 欠账
- 本带段逐字章名/小节目录待购电子版销账；`@tf.function` 在书中的着墨深浅未知。
- Keras 3 迁移对照（tf.keras→keras 边界）未逐 API 销账；🔧 E1–E3 全部未跑（本机无 tensorflow）。
- 书中安装/环境带段（macOS 副题所绑）本目录未单独建档，按 00 总览批判口径整带跳读 ⚠️。
