# 《TensorFlow：实战Google深度学习框架（第2版）》章笔记 01 · TensorFlow基础与计算图

> ⚠️ 章名题注：带段划分凭记忆，与书中逐章对应待版权页目录销账。三态标注：✅=官方文档/盘上直证口径；⚠️=凭记忆；🔧=未实测（本机未装 tensorflow）。本册覆盖原书"TensorFlow 与深度学习简介 + 基础概念（计算图/会话）"主题线 ⚠️。

## 核心机制

### 张量、计算图与两阶段执行

- 本书第一支柱：**一切皆计算图（graph）**——先以 `tf.constant/tf.Variable/tf.matmul` 等声明"运算的描述"（⚠️ 具体例名凭记忆），图只是拓扑定义、不执行；再用 Session 驱动。对照 PyTorch：eager mode（define-by-run）默认逐行执行，`y = x @ W` 立刻出数值（✅ torch 官方口径）；TF 的"先画图后开闸"是 define-then-run。
- Java/C++ 概念锚：**图=IR、Session=JVM**。类比 `javac` 先编译出字节码（结构可优化、可跨机分发）再由 JVM 解释执行——TF1 先构图再做常量折叠/算子融合/分区，再由 Session 派发到设备；PyTorch eager 则像逐行 eval 的解释器，好调试、少全局优化。TorchScript/ONNX 后来给 PyTorch 补上"能导出成图"的回路（✅），恰证明两种形态各有所长。
- `tf.Session()`（**2026 已废**：TF2 默认 eager，Session API 仅剩 `tf.compat.v1` 遗产位）：`sess.run(tensor, feed_dict={...})` 一次 run 只对目标张量**反向裁剪**求值，未被依赖的子图不动——这是"惰性求值+按需拉取"，对照 C++ 表达式模板的惰性求值同一味（⚠️ 类比口径）。
- `tf.placeholder`（**2026 已废**，无 TF2 对位物）：图的入参孔位，`feed_dict` 注数据。今天读它只需记一件事：**数据与图分离**正是这套 API 死掉、被 `tf.data`+eager 取代的病根。
- 变量生命周期：`tf.Variable` 声明在图上、`sess.run(tf.global_variables_initializer())`（**2026 已废**）才真分配——"声明≠存在"是 1.x 头号新手坑；PyTorch 里 `nn.Parameter` 构造即有值（✅），无此仪式。

### 命名、集合与图管理

- name_scope/variable_scope 拼出层级名（⚠️ 书中细节凭记忆；variable_scope 复用机制是后文 CNN/RNN 权重共享的地基）；同名冲突自动加 `_1` 后缀。
- 隐式全局图+集合（collection）机制：算子声明时自动进当前图与命名集合——隐式上下文对位 C++ 全局单例/线程局部存储的利弊同款：省事、但"谁改了全局状态"难追（⚠️ 评述）。

### 为什么先画图：图的三笔红利

- **可优化**：图是全局静态结构，常量折叠、公共子表达式、算子融合、梯度算子自动拼接都在 run 前完成——JIT 编译器的经典优化在 ML 上的复刻（✅ 通识口径）。
- **可移植/可分发**：GraphDef 序列化为 protobuf（✅），一份图定义可跨语言（Python/C++/Go/Java API 同存 ✅）、跨设备、跨机器分区执行——本书后段分布式章（见 06 册）的可行性正建立在"图与执行分离"上。
- **可部署**：冻结图（frozen graph，变量折成常量导出单文件 ⚠️ 书中是否讲存疑）曾是 TF1 移动/服务器推理的主形态（**2026 已废**为 SavedModel/TFLite 口径 ✅）。
- 代价同样明确：构图期无值可看、调试靠 fetch 猜、控制流要进图（`tf.cond/tf.while_loop`，**2026 已废**为 eager 直写）——这正是 PyTorch define-by-run 在 2017–2019 夺走研究社区的力学原因（✅ 通史口径）。

## 批判读法（易错与存疑）

1. **"计算图=TensorFlow"过时期**：图只是编译中间表示，XLA/TVMScript/TorchScript 都在图这一层竞争；2026 视角应把本册读成"静态图 IR 的第一课"，不是"TF 教程"。
2. **feed_dict 记忆残留**：若你按本书路径学过 1.x，`placeholder` 肌肉记忆会害你在 TF2 教程里找不到入口——2026 实操线一律 `tf.keras`+`tf.data`（✅ 官方口径），本册所有代码示例视为反面教材。
3. 书中"会话是运行期环境、图是定义"的两分讲法 ⚠️ 是否给出图分区到多设备的细节，待目录销账。
4. 概念混淆预警：张量（数据描述）≠ 数据本身，`tf.constant` 构图时即定值、`tf.Variable` 值随 run 变——书中是否显式区分 ⚠️ 存疑。

## 🔧 微实验（未实测：本机未装 tensorflow，pip 冻结，仅为设计）

- 实验 A：装 TF1 遗产口径（`tf.compat.v1`）搭两输入一乘加的小图，`sess.run` 只 fetch 部分节点，观察未依赖子图不执行（打印副作用算子计数）。
- 实验 B：同一公式在 PyTorch eager 里三行写完，对比调试体验（pdb/断点能否进构图期）。
- 实验 C：`tf.get_default_graph().as_graph_def()` 打印 protobuf 文本，肉眼确认"图=序列化 IR"（✅ GraphDef 为 protobuf 是官方文档口径）。

## 盘谱互链

- 上一章 [00-总览与阅读地图.md](00-总览与阅读地图.md)；下一章 [02-神经网络基础.md](02-神经网络基础.md)。
- 手推版"无框架计算图"（加法节点/乘法节点/反向）：[../深度学习入门.md](../深度学习入门.md) 第 5 章（✅ 盘上档含目录）。
- 图与自动微分现代表：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)；TF2 工程口径：[../ProgrammingTensorFlow2.md](../ProgrammingTensorFlow2.md)。
- 母档：[../TensorFlow实战Google深度学习框架2.md](../TensorFlow实战Google深度学习框架2.md)。

## 核心概念中英对照

- **计算图** — computational graph：运算的拓扑描述，先定义后执行。
- **会话** — Session：图的运行期环境（1.x；2026 已废）。
- **占位符** — placeholder：图的输入孔位（1.x；2026 已废）。
- **惰性求值** — lazy evaluation：run 到才算值，按需裁剪子图。
- **变量初始化** — variable initialization：声明与赋值分离的仪式（1.x 特有）。
- **静态图/动态图** — static vs dynamic graph：define-then-run vs define-by-run。

> ⚠️ 欠账：原书第 1–2 章逐节目录与例程（书中是否讲 GraphDef protobuf 细节、是否提前引出 estimator）；本机零实测（无 tensorflow）——购书+搭环境后销账。
