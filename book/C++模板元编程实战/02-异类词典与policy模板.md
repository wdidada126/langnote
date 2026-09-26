# 第 2 章 异类词典与 policy 模板——具名参数的编译期引擎

> 原书第 2 章（P28–61，第一部分收官）。目录口径见 [../C++模板元编程实战.md](../C++模板元编程实战.md)。
> 总览见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

本章是全书技术含量密度最高的一章：**异类词典（VarTypeDict）把"类型当键、值当载荷"
的编译期哈希表做出来，policy 模板把"行为当参数"的 Loki 路线工程化**。
两者的组合直接决定了第二部分所有层对象"如何被配置"——MetaNN 层的构造函数
收到的不是几十个位置参数，而是一个 policy 容器 + 一个具名参数字典。

## 核心概念速览（中英对照）

- **具名参数** — named parameters：以"标签类型→值"映射代替位置参数的调用风格
- **异类词典** — heterogeneous dictionary（书中 VarTypeDict）：按键类型索引、值类型各异的编译期查找表
- **键的表示** — tag as key：空类标签即键，`Tag2ID_` 把键映射为 tuple 下标
- **policy 模板** — policy-based class template：把类的可变行为抽为模板参数的设计模式（Alexandrescu《Modern C++ Design》2001 提出）
- **policy 对象** — policy object：`PolicyContainer<...>` 打包出的策略集合（本书术语）
- **支配** — domination：多个 policy 含同名嵌套 typedef 时的歧义裁决关系（Loki 概念）
- **policy 选择元函数** — PolicySelector：从容器中按特征挑出唯一匹配项
- **policy 修正/替换** — Change_Policy：编译期"换掉容器中第 N 个策略"（MetaNN 的 `change_policy.h`）
- **policy 注入** — InjectPolicy：把外层容器的策略灌进子层（第 6/7 章复合层复用）
- **std::tuple 作缓存** — tuple as storage：词典的值存储现代形态

## 动机：位置参数在"层"这种高配置密度对象上会崩

一个神经网络层的构造要回答：输入输出维度、参数初始化器（gaussian/var_scale filler）、
是否可训练、权重共享组名……用位置参数写出来是
`WeightLayer("w", 784, 10, GaussianFiller(0, 0.01), trainable, shared)`——
顺序不可记、默认值不可省、扩展即破坏 ABI。运行期 solution（选项 builder）解决不了
**类型层面的组合爆炸**：MetaNN 需要"不同 policy 组合 = 不同类型"，因为梯度收集、
初始化策略这些行为要在**编译期**焊死，才能零开销内联进正向/反向传播。
于是需要：①一种编译期键值存储（异类词典）装参数，②一种类型级组件模型（policy）装行为。

## 机制精讲

### 2.1–2.2 异类词典 VarTypeDict

机制三步（对照真实源码 `MetaNN/facilities/var_type_dict.h`，实测可访问）：

1. **键=空标签类**：`struct Input; struct Output;` 只以其类型身份存在，零开销。
2. **键→下标**：`Tag2ID_<TFindTag, N, TTags...>` 递归匹配，全特化在命中处停下——
   就是第 1 章"循环+分支"的组合应用；查不到的键在编译期硬错误（这是特性：
   参数名打错 = 编译不过，具名参数获得**类型安全**）。
3. **值=同形 tuple**：`NewTupleType_` 把 `std::tuple<Tags...>` 与值类型列表拼装成
   `std::tuple<Entry<Tag, Val>...>`；读写都经 `Tag2ID` 定位下标 + `std::get`。

书中还给出两个性能阀门：`VarTypeDict` 编译期查找是 O(键数)，作者用"高频键前置"
与 §2.2.5 的 **std::tuple 缓存**（构造完的词典直接以 tuple 形态内嵌进对象，
跳过重复装配）缓解。等价复现（机制转述，我的教学版而非原书码）：

```cpp
// 🔧 已实测 g++ 15.2（-std=gnu++23）：标签作键的迷你异类词典（VarTypeDict 教学等价物）
struct LR {}; struct Epoch {};                       // 具名参数的"名"=空标签
template <class Tag, class Val>
struct Entry { using TagType = Tag; Val val; };      // 键被"萃取"进值包装
// 键→下标：递归元函数，未命中返回 SIZE_MAX，由 static_assert 拦截（打错参数名=编译错误）
template <class K, size_t I, class... Es>
struct IndexOf { static constexpr size_t value = SIZE_MAX; };
template <class K, size_t I, class E, class... Es>
struct IndexOf<K, I, E, Es...> {
    static constexpr size_t value = std::is_same_v<typename E::TagType, K>
        ? I : IndexOf<K, I + 1, Es...>::value;
};
template <class... Es> struct Dict {
    std::tuple<Es...> es;
    template <class K> constexpr auto& get() const {
        constexpr size_t i = IndexOf<K, 0, Es...>::value;
        static_assert(i != SIZE_MAX, "key not found");
        return std::get<i>(es).val;
    }
};
int main() {  // 输出：epoch=100 lr=0.01 —— 存取顺序无关
    Dict<Entry<LR, float>, Entry<Epoch, int>> d{
        std::tuple{Entry<LR, float>{0.01f}, Entry<Epoch, int>{100}} };
    printf("epoch=%d lr=%g\n", d.get<Epoch>(), d.get<LR>());
}
```

### 2.3 policy 模板：从 Alexandrescu 到 MetaNN

Loki 原版 policy 用**多继承基链**（`Class<P1,B1, P2,B2...>`），policy 之间同名成员
要靠**支配关系**（谁"拥有"typedef，谁赢）裁决；书中 §2.3.4 专讲支配与虚继承的坑
（同名 typedef 二义、虚继承的运行期成本）。本书的工程决策是**放弃继承链，改用
聚合容器**：`PolicyContainer<Ps...>` 只是一个变参包装（实测：MetaNN-book 分支
`policies/policy_container.h` 全文仅约 25 行，定义 `PolicyContainer`/
`SubPolicyContainer<TLayerName, Ps...>` 与 `IsPolicyContainer` 判定变量模板），
所有"取用"通过 `PolicySelector` 元函数在容器上做模式匹配——**组合优于继承的
编译期版本**。这一改动让"支配"从继承疑难退化为容器内查找规则，值得单独表扬。

- **policy 对象声明**：书中 §2.3.7 用 `policy_macro_begin.h/policy_macro_end.h`
  一对宏包装变参声明（实测：两文件确实存在于仓库，配合 MSVC2013 时代的变参宏
  兼容），现代编译器可直接 `template <typename...> ...` 删掉这对宏。
- **InjectPolicy**（`policies/inject_policy.h`）：复合层把外层 policy 按子层
  匹配规则注入——policy 模板从"配置一个类"升级为"配置一棵类树"。
- → 框架落点：第 6 章层的常用 policy 对象、第 7 章复合层 policy 继承与修正。

## 权衡

| 维度 | 异类词典+PolicyContainer（本书） | Loki 继承链 | 运行期选项对象（如 torch API） |
| --- | --- | --- | --- |
| 查找成本 | 编译期 O(N)，产物零成本 | 编译期 | 运行期字符串/枚举分派 |
| 组合扩展 | 变参任意加，无基类数上限 | 受基类数/宏重复（MAX_POLICIES） | 任意 |
| 错误信息 | 键不存在=模板错误（刺耳） | 支配歧义（更难读） | 运行期断言（友好） |
| 二进制 | 每种组合一个类型（代码膨胀风险） | 同 | 单一类型 |

异类词典的 O(N) 查找与 tuple 缓存这对组合说明：**即便"零开销抽象"，
编译期数据结构也有自己的性能账**，这是本书比多数 TMP 教材诚实的地方。

## 相邻概念对比

- 本章 policy 容器 vs [../More_Effective_C++/08-补编-从MEC++到Loki定制技法谱系.md](../More_Effective_C++/08-补编-从MEC++到Loki定制技法谱系.md)：那份补编讲"从 MEC++ 到 Loki"的起源，本书讲"Loki 思想在 2018 年后如何被容器化改造"——正好接成一条时间线。
- 词典的 `Tag→下标` 与第 1 章 `At<I,...>` 是同一枚硬币：一个按键找位，一个按下标找型。
- [../C++模板元编程/03-高阶元函数与lambda.md](../C++模板元编程/03-高阶元函数与lambda.md)（Abrahams）：元组+索引那一章处理同个问题（编译期 shuffle），但无"域"背景；读起来会发现本书第 2 章是它的工程应用文。

## 最新演进与工业实践

- **具名参数的现代语法**：C++20 **指定初始化器**（designated initializers，
  `Options{.lr = 0.01f, .epoch = 100}`，cppreference 记载为 C++20 特性；其采纳轮次未逐文核对 ⚠️）
  在**运行期**提供了同款的"顺序无关+类型安全"参数包。
  但它不能改变类型组合，policy 类需求（"不同配置=不同类型=不同代码路径"）
  仍归模板方案。两者分工：参数**数据**用 designated init，参数**行为**用 policy。
- **变参词典的直接后继**是"编译期字符串键 + 类型化值"的 reflection 路线；
  C++26 反射提案（如 [P2996R6](https://wg21.link/P2996)，实测 302 可跳转）方向
  是数据成员名在编译期可读——若采纳，`Tag2ID` 这类样板有望由编译器生成。⚠️ 采纳进度以最新 WG21 纪要为准。
- **工业对照**：PyTorch C++ 前端的 `torch::TensorOptions().dtype(f32).device(kCUDA)`
  （[github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)，API 实测存在）是**运行期**
  具名参数（链式 builder，返回类型不变）；MetaNN 的选择说明编译期配置在"行为内联"
  诉求下仍不可替代，但今天多数框架不再需要——因为它们转向了**代码生成**（第 6 章再讲）。
- **policy→concepts**：Loki/本书时代 policy 的"契约"只能靠"用到才知道"（duck typing），
  C++20 concepts 可写 `template <TrainingPolicy P> ...` 把约束前移到声明处，
  书中 `PolicySelector` 的模式匹配思路被 `requires` 表达式直接表达。

## 小结与练习指向

第一部分至此完结。原书 §2.5 练习提示：给词典加"键重名编译期断言"、手写 `Change_Policy`。
进入第二部分：[03-深度学习概述.md](03-深度学习概述.md) 会把镜头从语法拉回领域，
回答"为什么深度学习框架需要这些元编程"。

- 上一章：[01-基本技巧.md](01-基本技巧.md) | 下一章：[03-深度学习概述.md](03-深度学习概述.md)
- 全书地图：[00-总览与阅读地图.md](00-总览与阅读地图.md) | 大纲：[../C++模板元编程实战.md](../C++模板元编程实战.md) | 系列：[../C++系列·总索引.md](../C++系列·总索引.md)
