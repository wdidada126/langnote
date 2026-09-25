# L25 二叉搜索树 BST（插入/查找/删除与中序遍历）

> 对应 spring2024 L25：BST 性质、插入、查找、删除（四情形）、遍历三式。阅读：CLRS 12；Lab7。项目对应：projects/bst。

## 1. 核心概念

- **BST 不变量**：任意节点 x，左子树所有 key < x.key < 右子树所有 key。由此**中序遍历即排序**：
  ```java
  void inorder(Node x) { if (x == null) return; inorder(x.left); visit(x); inorder(x.right); }
  ```
- **查找/插入（递归模板，61B 风格）**：
  ```java
  Node insert(Node x, K key) {
      if (x == null) return new Node(key);
      int c = key.compareTo(x.key);
      if (c < 0) x.left = insert(x.left, key);
      else if (c > 0) x.right = insert(x.right, key);
      // c == 0：更新 x.val
      return x;
  }
  ```
- **删除四情形**：叶→直接摘；独子→子代位（接爷爷的引用）；双子→**用中序后继（右子树最左）替换 key 再递归删后继**，保持BST性且只下沉一层。
- **三遍历配对**：pre（复制树/序列化）、in（排序）、post（删除整树、表达式树求值——Lab7 的"家族树"与目录大小统计皆 post）。
- **病态形状**：有序输入插入 ⇒ 退化成链表，Θ(n) 高。这是 L26–L27 平衡化的唯一动机。

## 2. 复杂度视角

| 操作 | 平均 | 最坏（退化） | 最坏成因 |
| --- | --- | --- | --- |
| search/insert/delete | Θ(log n) | Θ(n) | 树高 h；随机插入期望 h≈1.39 log n |
| min/max | Θ(h) | Θ(n) | 沿一侧走到底 |
| 中序遍历 n 节点 | Θ(n) | Θ(n) | 每边访问一次（与 h 无关） |
| successor（无 parent 指针） | Θ(h) | Θ(n) | 重新从根下降 |

**一切成本 = Θ(树高)** 是 BST 的公理式结论，后面所有平衡树都在压低 h。

## 3. 实现检查清单

1. 比较一律用 `compareTo`/`equals`，别对字符串用 `==`（L02 回魂）。
2. 递归写"返回值接回"：`x.left = insert(x.left, k)`——否则新节点挂不上。
3. 删除双子节点时同步 size/height 等簿记字段；AVL（L27）里"height 缓存失效"是首要 bug 源。
4. 测试用中序断言：`tree.inorder().equals(sorted(list))` 一条打尽所有结构 bug。

## 4. 与前后讲联系

- 上承：L24 的 Comparable 是 BST 的准入证；L16 链表 = 高度退化 BST 的极限。
- 下启：L26 用 2-3 树解释"为什么高会坏、矮就能好"；L27 AVL/RB 给出工程答案；L28 堆是"放弃有序换完全二叉树"的镜像决策；L36 Trie 是"以字符为 key 层"的多叉 BST 亲戚。

## 5. 跨课程联系

- **CS61A**：61A Tree 抽象（`tree(label, branches)`）的 set-membership 正是 BST 查找的"数据抽象版"；61A 不分析形状，61B 补上形状决定论。Scheme 的 `datum->structure` 构造表达式树 = 61B 的 parse tree 练习。
- **6.006/CS170**：CLRS 12 用 parent 指针与 `TREE-DELETE` 三情形（合并到" transplant" 原语）；6.006 干脆跳过平衡树讲有序数组，红黑树留给 6.046。
- **CSAPP**：每节点 ~40B + 两次依赖 load 的下降路径 ⇒ 与跳表/数组二分同 Θ(log n) 时实测差 3–5 倍——B 树（L26 末）"用更宽节点换更浅访问"的动机在内存层就已成立。
- **DDCA**：比较-分支即硬件 comparator + mux 链，树高 = 关键路径级数。

## 6. 开源项目应用

- **JDK**：`TreeMap` 即红黑树化 BST（对外 API 全在讲"order statistics 缺失"的普通 BST 能力）；`Arrays.parallelSort` 不用树，但 `PriorityQueue` 不用 BST——看谁承担"序"的责任。
- **Linux**：epoll  Interest 列表按 (fd, addr) 红黑树（前身正是纯 BST，2.6.27 前）；进程虚拟区 `vm_area_struct` 曾为红黑树（6.1 起改 maple tree——多叉版，仍是"矮 > 窄"）。
- **Lucene**：term 字典 BlockTree 中 block 内前缀压缩有序数组 + 索引层树——"BST 思路 + B 树扇出"的混合。
- **Git**：commit-graph 文件本身是"按 commit 位置排序的数组 + 二分"，用有序数组替代 BST——工程上"排序数组 + 二分"是 BST 最常见替身。

## 7. 延伸阅读

- Hug 笔记 "Binary Search Trees"；CLRS 12.3（删除正确性证明）。
- Sedgewick algs4 3.2（BST 及其退化实验）；"A Note on Binary Search Trees"（Knuth 平均值分析古典文献）。
- 练习：用本讲代码统计"有序输入插入 n=10⁵ 时的树高"（对照 log₂ 10⁵≈17）。
