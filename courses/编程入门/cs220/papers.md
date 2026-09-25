# CS220 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| RustBelt: Securing the Foundations of the Rust Programming Language | Jung et al., POPL 2018 | L5/L10 | 所有权+类型系统健全性证明 |
| Abstractions and Types: Advanced Topics in Types and Programming Languages (ATTAPL) | B. Pierce (ed.), 2005 | L3/L4/L6 | 子类型、类型类、生命周期背后的类型理论文集 |
| Compiling Pattern Matching to Good Decision Trees | G. Maranget, ICFP 2003 | L3 | 穷尽性检查与 match 编译的实现 |
| Semantics of Move Semantics（以 C++ 提案/论文为对照） | J. Chamberlain 等提案文档, 2010 | L5 | 与 C++ 移动语义横向对照 |
| Rustonomicon（官方 unsafe 手册） | Rust 团队, 持续 | L11 | 语言语义底层文档 |
| Programming Rust, 2nd ed. | Blandy, Orendorff, Tindall, 2021 | 全课 | slides 之外的系统参考书 |

> 骨架注：以类型理论 + Rust 语义证明类文献为主，正式填充时逐讲对应 slides 引用。

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| 课程 2025 版 slides/homework（ku-ccamp GitHub） | 2025 | 全课 | 第一手最新材料 |
| Tree Borrows 别名模型 | Jung et al., 2023 | L5/L6 | 借用规则的语义依据更新 |
| Jeehoon Kang 关于 AI 辅助编程的课堂说明（课程主页/公告） | 2024–2025 | 全课 | 课程鼓励 AI 辅助但核心工作需自己完成 |
| Rust 2024 Edition | 2024 | 全课 | 新版语法/预lude 变化对 slides 的影响 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| ADT/模式匹配 (L3) | rustc 编译器自身 (HIR/MIR) | 大型解释器式 AST 处理 |
| Trait 抽象 (L4) | serde | trait 驱动的多格式序列化 |
| 借用检查 (L5) | 任何中大型 Rust 项目: ripgrep | 性能关键路径的无拷贝解析 |
| 生命周期 (L6) | wasm-bindgen | FFI 边界的生命周期管理 |
| 迭代器 (L7) | polars / DataFusion | 组合子式数据管线 |
| Rc<RefCell>/Weak (L8) | rust-analyzer | 增量计算依赖图 |
| Send/Sync (L10) | crossbeam / tokio | 并发库的类型级安全设计 |
