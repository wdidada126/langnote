# CS110L 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| RustBelt: Securing the Foundations of the Rust Programming Language | Jung, Jourdan, Krebbers, Appel (POPL 2018) | L3/L7 | Rust 类型系统健全性的首个机检证明，理解"安全系统编程"的理论底座 |
| Stacked Borrows: An Aliasing Model for Rust | Jung, Lande, Weinert, Flur, Shriram, Parizek, Jagannathan (POPL 2020) | L3 | 借用检查器背后的别名模型 |
| The Problem with Threads | E. A. Lee (CACM 2006) | L8–L10 | 线程范式缺陷论证，课程并发对比章节的思想背景 |
| Why Threads Are a Bad Idea (and How to Write Concurrent Programs on a Shared-Memory Multiprocessor Without Them) | J. Ousterhout (USENIX 1995) | L10 | 事件驱动 vs 线程，Project2 直接相关 |
| Programming in Rust: Beyond Speed (CACM 文章) | A. Coghlan, 2009? 稳妥替代：The Rust Programming Language 论文/设计文档 (RFC 体系与 Graydon Hoare 早期设计稿) | 全课 | 语言设计动机 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Tree Borrows: A New Alias Policy for Rust | Jung et al., 2023 (Jung 博士论文相关章节) | L3 | Stacked Borrows 的继任别名模型 |
| rCore-Tutorial 文档（清华大学） | 持续更新 | L8–L10 | 基于 Rust 的 OS 实验课，csdiy 页面直接推荐衔接 |
| Tokio 官方 tutorial（async 生态事实标准） | 2021–2025 持续更新 | L9–L10 | 课程 2020 版 futures 内容的现代落点 |
| Rust 2024 Edition RFC/公告 | 2024 | 全课 | 课程停更后语言演进（impl Trait、生命周期保留字等） |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 所有权/借用 (L3) | Servo | 并行浏览器引擎，fearless concurrency 的旗舰案例 |
| Trait 与泛型 (L4) | tokio | 泛型 async runtime 组件设计 |
| Result/错误传播 (L5) | anyhow / thiserror | Rust 错误处理生态事实标准 |
| Rc<RefCell<T>> (L7) | rustc 数据结构 / wasm-bindgen | 图状/内部可变数据惯用法 |
| 线程与消息通道 (L8) | crossbeam | 课程并发原语的工业级库 |
| Futures/async (L9) | hyper / tonic | Project2 负载均衡器的现代写法 |
| ptrace 系统编程 (Project1) | bpftrace / strace（对照）、gdb 生态 | 调试器与观测工具族 |
