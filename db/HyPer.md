# HyPer

HyPer（有时写作 Hyper）是一个高性能内存数据库系统（in-memory DBMS），专为混合 OLTP & OLAP 工作负载（Hybrid Transactional/Analytical Processing，简称 HTAP）设计。它起源于德国慕尼黑工业大学（Technical University of Munich, TUM）的学术研究项目，由 Alfons Kemper 和 Thomas Neumann 教授领导的小组从 2008 年左右开始开发。

### 核心特点和技术亮点
- 混合 OLTP/OLAP：同一系统内同时支持高吞吐事务处理（OLTP）和复杂分析查询（OLAP），无需分离系统。
- 内存驻留 + 虚拟内存快照：通过 fork OLTP 进程创建一致性快照（virtual memory snapshots），OLAP 查询在快照上运行，避免干扰 OLTP 事务。
- 查询编译执行：开创性引入数据中心代码生成（data-centric code generation）和即时编译（just-in-time compilation）查询计划，利用现代 CPU 特性（如 SIMD、branch prediction）实现极高性能。
- NewSQL 风格：关系型 SQL，支持 ACID 事务，但表布局可根据 workload 自适应（非固定行存/列存）。
- 性能：在 TPC-H 等基准中长期领先，许多论文（如 VLDB 2011 的查询编译论文）获 Test-of-Time Award，影响了 DuckDB、SingleStore、Tableau Hyper 等后续系统。

### 发展历史
- 2008–2015：TUM 学术项目（原名 HyPer，Hybrid High Performance）。
- 2015：团队创办 Hyper 初创公司，商业化。
- 2016：被 Tableau 收购（Tableau 当时被 Salesforce 收购前夕）。
- 收购后：HyPer 引擎重命名为 Hyper，集成进 Tableau 的数据引擎（.hyper 文件格式），用于 Tableau Desktop/Server/Cloud 的 extract（提取）加速和实时分析。
- 当前（2026年）：Hyper 已成为 Tableau / Salesforce 生态的核心数据引擎，支持交互式分析“最新数据状态”（freshest state of data）。它不是独立产品，而是 Tableau 的内部 SQL 引擎。

### 代码是否开源？
不完全开源，但部分相关组件开源：
- 核心 HyPer/Hyper DBMS 引擎：不开源，仍是 Tableau/Salesforce 的专有技术（proprietary）。
- Hyper API（用于操作 .hyper 文件的库，支持 Python、Java、C++ 等）：从 2024 年起转为 Apache 2.0 开源许可，可在 GitHub 上找到文档和部分示例，但核心引擎二进制不开源。
  - GitHub 仓库：https://github.com/tableau/hyper-db （主要是文档和 API 相关）。
  - Python 安装：`pip install tableauhyperapi`。
- 早期学术论文和原型代码公开，但完整生产级源码不公开。

### 简单总结
- 学术影响力：极高，许多现代数据库（如 DuckDB 的向量化/编译执行）受其启发。
- 实际使用：主要嵌入 Tableau 生态，用于 BI/分析场景（.hyper 文件本质上是 Hyper 数据库文件）。
- 如果你想体验：用 Tableau Desktop 创建 extract，或通过 Hyper API 直接操作 .hyper 文件（免费，但受许可限制）。

如果你对 HyPer 的查询编译、虚拟快照机制、或与 DuckDB/ClickHouse 的性能对比感兴趣，可以继续问，我可以深入解释！
