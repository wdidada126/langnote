# Haskell MOOC 配套项目计划（骨架，本轮不写代码）

语言统一 Haskell（GHC 9.x，cabal 单包或 stack 管理），验收含 `-Wall` 与 hlint。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L4 基础函数/递归 | Haskell | 温度/货币换算 + 守卫式分类器 CLI | `ghc -Wall -O2 Main.hs -o main` |
| L5–L6 列表与 ADT | Haskell | 手写的 RPS（石头剪刀布）记分游戏：自定义类型建模 | `cabal build && cabal run` |
| L7 高阶函数 | Haskell | mini DSL：配置管线 map/filter/fold 组合 | `cabal test`（hedgehog 性质测试） |
| L8–L9 类型类与 IO | Haskell | 交互式 TODO 工具：文件持久化 + 自定义 typeclass | `cabal build --release` |
| L10 Monad | Haskell | 自实现 Maybe/List 单子的 Law 检查器 | `cabal test` |
| L11–L12 Monoid/Functor/Applicative | Haskell | 日志聚合器（Monoid）+ 并行配置读取（Applicative） | `cabal test`，Criterion 基准 |
| L13 Foldable/Traversable | Haskell | 树形目录 traverse 批处理工具（重命名/校验和） | `cabal build` |
| L14 惰性求值 | Haskell | 素数筛/无限序列实验 + 内存泄漏修复记录 | `ghc -O2 +RTS -s` 观察 |
| L15 Fraxp 复刻 | Haskell | 迷你 FRP：信号网络 + 动画/绘图输出 | `cabal build`，附截图测试 |

约定：本轮只列计划；依赖统一 `cabal.project`，集中编译由用户稍后执行。
