# 《Programming PyTorch for Deep Learning》章档 01 · PyTorch 基础与张量操作

> ⚠️ 题注：章名凭记忆推定带段，逐字目录待购电子版销账——本节机制口径标 ✅ 者均为 pytorch.org 官方文档级常识，**不承诺本书如此讲**；书中位置全部未核。
> 🔧 未实测：本机未装 torch，微实验仅为设计。总纲与裁决位见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心机制

### Tensor：ndarray 的血统 + autograd 的附加协议

- `torch.tensor`/`zeros`/`randn` 等创建 API 与 NumPy 家族同构（✅）——对照：../PythonDataScienceHandbook2e.md（✅ 在盘）的 ndarray 章可直接迁移；差异在每枚 tensor 可挂 `requires_grad` 标记（✅），0.4 起 Variable 并入 Tensor 本体（✅），Manning DLwP（../DeepLearningWithPyTorch.md，✅ 在盘）正卡在交接期、其 Variable 叙述属旧 API ⚠️ 读时需换血。
- `dtype` 与 `device` 双属性：`to("cuda")`/`.cpu()` 搬运显式（✅）——对比 C++/CPython 对象「数据即内存、位置隐式」（../CPython设计与实现.md，✅ 在盘），PyTorch 把「数据住在哪块内存」升格为一等公民，这是 GPU 时代框架与朴素数值库的分水岭（✅）。

### 形状代数：view / reshape / 广播

- 广播规则与 NumPy 完全同款：尾部对齐、1 可伸展（✅）；PyTorch 特有雷区是**原地操作污染 view**：`a.view(...)` 与 `a` 共享存储，对 `a` 的 in-place 改（`a.add_`）会穿透到派生 tensor（✅）。对照：NumPy 同样有 view 语义（✅），但 PyTorch 叠加 autograd 后，改 view 还会让 `backward` 报「leaf 被原地修改」类错（✅ 机理口径）。
- 要断开连接：`clone()` 复制数据、`detach()` 只摘计算图（✅）——两者正交，「既要副本又要图」需 `clone().detach()` 连写（✅ 口径）。

### autograd：动态图的一次前向一张账

- 每次运算在 `requires_grad=True` 的输入下建图，`.backward()` 反向填充 `.grad`（✅）；图用完即弃，下一轮重筑（✅）。对照 TF1 时代「先建静态图再喂 Session」的显式两拍（../TensorFlow实战Google深度学习框架2.md，✅ 在盘，1.x 口径），PyTorch 的 define-by-run 让 Python 控制流直接进模型——这是 2017 后生态胜负手（✅ 定性）。
- 梯度只落在**叶子张量**上：中间量想看梯度需 `retain_grad()`（✅ 机理）——调试小网络时「.grad 为 None」多半是找错了对象而非图断了。
- 梯度**默认累加不覆盖**：不清零则第二轮把两轮梯度相加（✅）——为 02 册训练循环的 `zero_grad()` 埋点。

## 批判读法（Packt 短书质量存疑位）

1. 本书为 Packt 短书，基础章大概率为 API 走查式罗列 ⚠️——走查式讲法「能跑但不知界」（广播报错形态、view 别名陷阱常缺席），本档以上述机制清单为验收标尺：书中缺哪条，那条就永久让位官方文档。
2. 2020 截点风险：若书仍带 Variable 遗迹或旧式 `torch.autograd.Variable(x)` 包法 ⚠️，一律按 0.4+ 现行口径改写后再入库。
3. 作者名录未证实 ⚠️（见 00 册）——本档不引任何「书中说」句式，未销账前所有论断只挂 ✅（官方口径）或 ⚠️（推定）。
4. 张量章常见的教学空洞：device×dtype 组合错（如 CUDA 半精度 matmul 报 dtype mismatch）与 `torch.equal` 判浮点相等的陷阱 ⚠️——书若未提，登记为官方文档补齐位。
5. 不虚构引文页码：本档无页码位，购电子版前不补。

## 🔧 微实验（未实测：本机未装 torch，仅为设计）

- 实验 A：广播失败矩阵 `(3,2)+(2,3)`，记录报错的 shape 对齐提示，与 NumPy 同操作报错逐字对比。
- 实验 B：`a.add_(1)` 后读 `a.view_as(a)` 派生量，实证别名穿透；再用 `clone()` 复现隔离。
- 实验 C：两轮 `backward` 不清零观察 `.grad` 累加，为 02 册循环做铺垫。

## 盘谱互链

- 上一章：无（本档为首章）；下一章 [02-构建与训练第一个网络.md](02-构建与训练第一个网络.md)。
- 重叠裁决对象 Manning DLwP 的 autograd 纵深章：../DeepLearningWithPyTorch.md（✅ 在盘，若二选一判归它，本档为其前菜）。
- 广播/ndarray 前置：../PythonDataScienceHandbook2e.md；数学直觉：../深度学习入门.md（✅ 在盘）。
- 总索引挂靠：../Python系列·总索引.md（✅ 在盘，补编节 PyTorch 线）。

## 核心概念中英对照

- **张量** — tensor：带 dtype/device/grad 三附加态的多维数组。
- **按需求梯度** — requires_grad：挂在 tensor 上的建图开关。
- **视图** — view：共享存储的形状别名，原地改互相穿透。
- **广播** — broadcasting：NumPy 同款的尾部对齐伸展规则。
- **动态图** — dynamic computational graph：define-by-run，前向即建图。
- **梯度累加** — gradient accumulation：.grad 默认加不加清。
- **原地操作** — in-place op：方法名带 `_` 后缀、直改共享存储的写法。

> ⚠️ 欠账：本书基础章逐字章名/是否含 Variable 旧写法/例程清单——待购电子版验目录销账；三枚 🔧 实验待装 torch 的机器补跑。
