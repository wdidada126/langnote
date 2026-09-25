# L36 Trie 与前缀检索（UDT 视角收官）

> 对应 spring2024 L36：Trie 结构、前缀检索、自动补全/拼写检查。阅读：CLRS 32.2（字符串匹配语境）；Lab（Trie）。项目对应：projects/trie。

## 1. 核心概念

- **Trie（前缀树）**：把"字符串的每个前缀"作为路径节点；节点存 `endOfString` 标志 + 子边表。它是"以字符为层"的多叉树——BST 的 key 比较被替换成"逐字符选边"，**比较成本与 log n 无关，只与键长 m 有关**。
- 实现（子表用 HashMap 或定长数组）：
  ```java
  private class TrieNode {
      final Map<Character, TrieNode> next = new HashMap<>();
      boolean end;
  }
  public void insert(String w) {
      TrieNode p = root;
      for (int i = 0; i < w.length(); i++)
          p = p.next.computeIfAbsent(w.charAt(i), c -> new TrieNode());
      p.end = true;
  }
  public boolean containsPrefix(String pre) { return descend(pre) != null; }
  ```
- **操作全家福**：`contains/insert/delete` Θ(m)；`keysWithPrefix` 先 descend 再 DFS（输出敏感：Θ(m + 输出节点数)）；自动补全 = prefix + top-K by weight（堆 L28 复用）。
- **压缩变体**：Patricia/Radix Trie 合并单链节点省空间（Redis `rax`、Linux FIB 树）；**DAWG/Suffix Trie→Suffix Tree** 支撑 substring 检索（CLRS 32.2 语境）。
- **UDT（用户自定义类型）收官**：Lab/HW 至此完成"链表→数组→哈希→树→堆→图→Trie"的自定义类型全景；Trie 是"结构即索引"的极端——键的每一位都参与寻址。

## 2. 复杂度视角（m=键长，n=键数）

| 操作 | Trie | 哈希表 | 平衡 BST |
| --- | --- | --- | --- |
| contains | Θ(m) | Θ(m)（hash 算全键）| Θ(m log n) |
| 前缀查询 | Θ(m + 输出) | Θ(n·m) 扫全表 | Θ(m + log n + 输出) |
| 有序遍历 | DFS 即字典序 | 不支持 | Θ(n log n) |
| 空间 | Θ(总字符数)，可爆 | Θ(n) | Θ(n) |
| 删除 | 沿路剪无子节点 | Θ(m) | Θ(m log n) |

## 3. 与前后讲联系

- 上承：L25（树的递归遍历）、L20（节点子表用 HashMap——两个结构联姻）、L28（自动补全 Top-K）。
- 下启：L37 I/O 序列化 Trie/对象（Project3 的目录树对象存储用 trie 式路径寻址）；L38 课程总结把 Trie 列为"字符串世界的通用索引"。
- 与 L34–L35：MSD 基数排序 = 按 Trie 层遍历的排序版；"排序数组 + 二分"也能前缀检索（lowerBound），Trie 用空间换时间。

## 4. 跨课程联系

- **CS61A**：61A Project 1 的 `Tree` 通用递归（`map_tree/depth/str_tree`）就是 Trie 的抽象骨架；61B 在其上贴"字符边 + end 标志"变成检索结构——"同一棵树，抽象层与实现层"两课对拍。
- **6.006/CS170**：6.006 字符串处理用 Rabin-Karp/rolling hash；CS170/6.046 的后缀数组 + LCP 是 Trie 的"排序+空间压缩"对偶（现代生物信息主流）。
- **CSAPP**：`next` 数组版（26 个指针槽）= 稀疏时 95% 空槽浪费；Map 版 = 指针追逐 + 装箱 Character。真实系统用排序边数组 + 二分（cache 友好）——字符集小正是"定长数组优于哈希"的窗口（L16 数组复权）。
- **OS/DDCA**：路由器 FIB 最长前缀匹配 = bit-level Trie（Linux `firmark`/DPDK 的 trie 与 LPM 库，网络设备的 IP 查找核心）；页表也可视作地址比特的两级 Trie。
- **15-445/CS186**：数据库索引里的 B+ 树前缀压缩（prefix-compressed keys）与 Trie 共享"利用键公共前缀"原理；全文索引的 term dictionary 用 FST（最小化 DAG 版 Trie）。

## 5. 开源项目应用

- **JDK**：无内置 Trie 是著名缺口（`PriorityQueue` 有、Trie 没有）；Lucene 的自动补全 `Completer` 模块内部就是 FST + Trie 融合。
- **Lucene**：`FST`（outputs on arcs）用于 term 字典、地名解析；`RegexQuery` 的自动化遍历共享前缀剪枝。
- **Redis**：`rax`（Radix Tree）承载 Stream 与 key 空间统计；键过期采样的 prefix 计数。
- **Git**：tree 对象按路径逐级嵌套（blob/tree 的"目录树"）是**磁盘化 Trie**：`git cat-file HEAD:src/main/App.java` 沿路径逐段解析——GITLET/Project3 直接实现它（见 projects/minigit）。
- **Linux/DPDK**：`fib_trie` IPv4 路由表；IPVS 会话表。
- **搜索引擎**：下拉联想（Google Suggest）= Trie + 频率堆 + 分布式分片（按前缀切 keyRange，呼应 L36 的 DFS 序）。

## 6. 延伸阅读

- Hug 笔记 "Tries"；CLRS 32 章（Trie 出现在线性时间多模式匹配 Aho-Corasick 11.3 节语境）。
- Sedgewick algs4 5.2（TST vs 五向/ R-way Trie 的空间实验）；Deriche & Grossman "Trie" 论文可选。
- Lucene `FST` javadoc 与 rdeshti "Radix tree" 系列博文；DPDK `rte_lpm` 源码注释。
