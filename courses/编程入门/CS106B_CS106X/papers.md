# CS106B/X 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| A Method for Obtaining Digital Signatures… (RSA 中的数论之外，此处取) Sorting and the Theory of Big-O | Knuth TAOCP Vol.3 | L6 | 排序与复杂度分析源头 |
| Quicksort | C. A. R. Hoare, 1961 | L6 | 快排原始论文 |
| Merge Sort 归并排序分析 | J. von Neumann, 1945 | L6 | 分治排序最早描述 |
| Binary Tree Sorting 相关 | T. N. Hibbard, 1962 | L8 | BST 删除算法的经典分析 |
| Finite Hash Codes / Universal Hashing | Carter & Wegman, 1979 | L9 | 哈希理论 |
| A Method for the Construction of Minimum-Redundancy Codes | D. Huffman, 1952 | L12 | Assignment9 原型论文 |
| Prefix Trees (Trie, Bron–Jarvi–Kort) | 1975 | L12 | Trie 正式化命名前身 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| C++ Core Guidelines（持续更新） | 2021+ | 全课 | 课程老代码风格与现代规范的对照 |
| Abseil Performance Tips 文档 | 持续更新 | L3/L7 | 容器选型与内存局部性的工程观点 |
| "The Impact of Memory Hierarchy on Sorting"(近年 benchmark 文章) | 2021+ | L6 | 缓存友好的 sort 实现分析 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| vector/引用传参 (L2–L3) | 所有现代 C++ 项目 | Core Guidelines R.30 等规范 |
| 回溯 (L5) | Z3 / or-tools | 搜索与剪枝思想在约束求解中的放大 |
| 排序与 Big-O (L6) | spdlog / LLVM | `llvm::sort`（pattern-defeating quicksort）工业实现 |
| 链表与内存 (L7) | Linux kernel `list_head` | 侵入式链表对照课程双向链表 |
| BST (L8) | RocksDB memtable / std::map | 红黑树实现 |
| 哈希表 (L9) | abseil SwissTable / Redis dict | 课程 HashMap 的工业级形态 |
| 图 BFS/DFS (L11) | OSRM / 路由库 | 路网搜索基础 |
| Trie/Huffman (L12) | ripgrep(Aho-Corasick 近亲) / zstd | 压缩与多模式匹配 |
