# 赫尔辛基 Haskell MOOC

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | University of Helsinki: Haskell MOOC (Functional Programming in Haskell) |
| 学校 | University of Helsinki（赫尔辛基大学） |
| 主讲 | Haskell MOOC 课程组（mooc.fi 团队，Markus Kettunen 等主讲历史，以官网为准） |
| 教材 | 课程官网即教材：https://haskell.mooc.fi/ （Part 1 & Part 2，在线免费） |
| csdiy 路径 | https://csdiy.wiki/编程入门/Functional/Haskell-MOOC/ （页面更新 2024-04-14） |
| 最新期次 | 常年开放 MOOC；作业仓库 moocfi/haskell-mooc 持续维护 |
| 难度/学时 | 🌟🌟 / 因人而异 |
| 状态 | 骨架 |

## 为什么学

- 课名是 Haskell，核心其实是函数式编程思想：用刚够用的语法和库解释核心程序语义，不让人陷入语言生态细节。
- 回答"Java Streams、JS Promises、ECMAScript Record & Tuple 为什么存在、为什么长这样"的设计层问题——学完 FP 才有答案。
- 覆盖 Pure Function、Lazy Evaluation、强类型与类型推导、Curry、Monoid/Functor/Monad/Applicative。
- 练习体验像 CS61A：注释提示充足，提交后给反馈，官方 Telegram 社区活跃；Part 1 简单，难度集中在 Part 2 第十三章之后。

## 先修与知识联系

- 先修：无（有编程经验则 Part 1 很快）。
- 联系：与 CS3110 (OCaml) 同属 ML 家族对照面（Haskell 更学术：类型类/惰性求值）；Monad/Applicative 直接解释 JS Promise 与 Java Stream/Optional 的设计动机；与 cs220 的 Option/Result、迭代器组合子互为印证；范畴论概念可延伸 Cambridge Semantics/CS242。

## 最新年份讲义章节目录（官网现行版，Part 1 + Part 2 共 20+ 章，按主题组归纳）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 函数式编程导论与安装环境 | mooc.fi Part1 ch.1 |
| L2 | 值与类型、简单函数 | Part1 ch.2–3 |
| L3 | 基本表达式与求值 | Part1 ch.4 |
| L4 | 守卫与条件表达式、模式匹配入门 | Part1 ch.5–6 |
| L5 | 递归与列表 | Part1 ch.7 |
| L6 | 元组、记录与自定义类型 | Part1 ch.8–9 |
| L7 | 高阶函数与柯里化 | Part1 后段章节 |
| L8 | 类型类初步与更多类型 | Part2 ch.10–11 |
| L9 | IO Monad 与副作用 | Part2 ch.12 |
| L10 | Monad：定义、law 与 do 记法 | Part2 ch.13 起（难度分水岭） |
| L11 | Monoid 与 Functor | Part2 对应章节 |
| L12 | Applicative Functor | Part2 对应章节 |
| L13 | Foldable/Traversable 与其他类型类 | Part2 对应章节 |
| L14 | 惰性求值 (Lazy Evaluation) | Part2 对应章节 |
| L15 | 综合项目：Fraxp（函数式响应式编程迷你 FRP） | Part2 末章 + 作业仓库 README |

> 注：官方章节号随修订浮动，正式填充笔记时以 haskell.mooc.fi 当期目录为准逐章对齐。
