# Haskell MOOC 讲义要点（骨架）

## L1 导论：FP 的世界观
- 组合优于状态：程序 = 函数的组合代数。
- 为什么用 Haskell 学 FP：语言强迫纯函数，反馈直接。

## L2 值、类型与简单函数
- 强类型 + 类型推导：`::` 读作"具有类型"。
- 函数签名即文档；多态类型变量。

## L3 表达式与求值
- 表达式为中心；if 也是表达式。
- 手工"代入求值"理解语义。

## L4 守卫与模式匹配
- guard 链 vs 嵌套 if；模式匹配解构数据。
- 与 OCaml/Rust match 的差异：Haskell 无 exhaustiveness 强制（靠 -Wall）。

## L5 递归与列表
- 没有循环：递归 + 列表原语。
- zip/map/filter/foldr 的组合风格。

## L6 自定义类型与记录
- data 声明、类型构造器、导出列表。
- 用 ADT 建模业务：Money、Person 练习。

## L7 高阶函数与柯里化
- 部分应用天然存在；`(+) 1` 即新函数。
- 点/美元运算符：`.` 与 `$` 的管道思维。

## L8 类型类与 IO 前夜
- typeclass = 特多态接口；Eq/Ord/Show 实例。
- Kind 初步：`* -> *`。

## L9 IO Monad
- 纯函数如何与外界交互：IO a 是"描述"而非"执行"。
- do 记法初体验： sequencing 副作用。

## L10 Monad 本体（Part 2 分水岭）
- bind (>>=)、unit (return) 与三条 monad law。
- Maybe/List/IO 三个具体 monad 的统一视角。

## L11 Monoid 与 Functor
- mempty/<>：叠加结构；Endo 技巧。
- fmap 的函子律：结构保持的映射。

## L12 Applicative
- pure/<*>：并行组合计算，比 Monad 更弱的抽象。
- 解释 JS Promise.all 为何是 Applicative。

## L13 Foldable/Traversable
- fold/foldMap；traverse 作为"映射 + 效果交换"。
- sequence 的本质。

## L14 惰性求值
- 非严格语义、normal order；无限表与黄金水位线。
- 空间泄漏与 bang patterns 初步。

## L15 Fraxp 综合项目
- 用 Applicative/Monad 搭建迷你 FRP：信号、时间、组合子。
- 复盘：typeclass 层级 (Monoid → Functor → Applicative → Monad) 的设计美学。
