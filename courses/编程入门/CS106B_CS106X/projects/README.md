# CS106B/X 配套项目计划（骨架，本轮不写代码）

对应 2022 winter 9 个 assignment 的主题，改造为自研小项目；语言为 C++17。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L4 集合与函数设计 | C++17 | 姓名统计器：map/set 词频 TopK | `g++ -std=c++17 -Wall` 单文件 |
| L5 递归 | C++17 | 目录树递归遍历 + 大小汇总（对照 A1 风格） | CMake |
| L6 回溯 | C++17 | 数独求解器 + 可视化解法计数 | CMake + Catch2 |
| L7–L8 排序 | C++17 | sort benchmark：自写 merge/quicksort vs std::sort | CMake Release `-O2`，附计时脚本 |
| L9 链表/内存 | C++17 | 手写双向链表 + valgrind/ASan 泄漏检查 | CMake + `-fsanitize=address` |
| L10 BST | C++17 | BST 可视化导出 DOT → graphviz（对照 A5） | CMake |
| L11 哈希 | C++17 | 通用 `ChainingHashMap<K,V>`（对照 A6 精神） | CMake + GoogleTest |
| L12 OOP | C++17 | 图片滤镜流水线：继承式 filter（对照 A6） | CMake + stb_image（头文件库） |
| L13 图 | C++17 | 迷宫生成+求解：BFS/DFS 对比，加"debugger 找线索"彩蛋（对照 A8） | CMake |
| L14 Trie/Huffman | C++17 | 文件压缩器 huff/huffman+自动补全 Trie（对照 A9） | CMake，附压缩率测试脚本 |

约定：本轮只列计划；每个项目后续放独立子目录并自带 build 脚本。
