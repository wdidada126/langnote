# Algorithms I & II 配套项目计划（骨架，本轮不写代码）

语言：Java 17（与课程一致）；依赖：algs4.jar（https://algs4.cs.princeton.edu/code/）+ JUnit 5。
约定：每个项目独立子目录（`p01_xxx/`），自带 `build.sh`/`run.sh`，只写不编译，集中验证由用户后续统一执行。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1 算法分析 | Java | 动态数组扩容成本实测：统计 N 次 add 的总复制量，拟合 ~cN | `javac -cp algs4.jar *.java && java -cp .:algs4.jar Main` |
| L2 基础排序 | Java | 排序计时台：insertion/shell/Arrays.sort 在有序、逆序、重复键输入上的对比矩阵 | 同上 + `StopWatch` 计时；输出 CSV |
| L3 快排与归并 | Java | 自写 Merge + 三路切分 Quick + 小数组切换；与 `Arrays.sort` 做基准（附退化输入） | `javac -O`；`java -Xms/-Xmx` 固定堆跑基准 |
| L4 堆与优先队列 | Java | Top-K 热词统计 + 事件驱动模拟（合单/合并 K 个有序流） | `javac -cp algs4.jar` + JUnit |
| L5–L6 符号表与平衡树 | Java | 有序映射 MiniMap：BST → 红黑（LLRB）两版，接口一致可切换；与 `TreeMap` 对拍 | `javac` + 随机对拍测试（JUnit `@RepeatedTest`） |
| L7–L8 图与有向图 | Java | 迷宫生成/求解（DFS+BFS 双解）+ 依赖解析器（拓扑排序 + 环路径报告） | `javac -cp algs4.jar`；文本 I/O 用 In/Out |
| L9 MST 与并查集 | Java | 图像连通域标记 + 路网 MST（Kruskal/Prim 双实现，输出 DOT 可视化） | `javac` + `dot -Tpng` 生成图片 |
| L10 最短路径 | Java | 城市路网导航：Dijkstra + A*（欧氏启发式），负权时用 Bellman-Ford 并报告负环 | `javac -cp algs4.jar`；附小规模 .graph 测试数据 |
| L11 字符串与基数排序 | Java | 倒排索引检索引擎：三向字符串快排建索引 + Trie 前缀自动补全 | `javac` + 大文本语料（古腾堡计划）跑通 |
| L12 搜索/正则/压缩 | Java | 文件压缩器：Huffman 编解码 + Rabin-Karp 多模式扫描（恶意串检测） | `javac` + 往返一致性测试（压缩→解压 diff 为空） |
| 延伸 B 网络流 | Java | 二分图最大匹配（课程—学生分派）与"棒球淘汰"归约，自写 Ford-Fulkerson | `javac -cp algs4.jar`；对拍小样例答案 |
| 综合（Part I+II） | Java | 迷你搜索引擎：抓取→索引(基数排序/Trie)→查询(BM25 排序用优先队列)→结果图分析 | `build.sh`（javac + jar 打包），JUnit 全绿 |

> 参考课程原版 Project（10 个）主题：Percolation、Randomized Queues & Deques、Collinear Points、8 Puzzle(A*)、WordNet、Degrees of Separation、Fat Trees、Soccer/Baseball Elimination(网络流)、KD-Trees、Search/Compression 类，上表为对应自研替代版。
