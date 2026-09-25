# L26–L27 平衡树：2-3 树动机、AVL 与红黑树（附跳表）

> 对应 spring2024 L26–L27：平衡动机、2-3/2-3-4 树、旋转、AVL、红黑树；跳表对照。阅读：CLRS 13、algs4 3.3。项目对应：projects/bst（AVL 部分讲透）。

## 1. 核心概念

- **一切为了高度**：BST 所有操作 Θ(h)；h=Θ(log n) 是"平衡"的定义。
- **2-3 树**：节点存 1 或 2 个 key，2-节点有 3 个孩子；完美平衡（所有叶同深）。插入先"临时塞入→分裂→上浮中间 key"——分裂上浮是后续一切"再平衡"的原型。
- **B 树 = 2-3-4 树的磁盘化推广**：每节点塞满一整页（4KB/16KB），扇出数百、两层装下 10 亿 key；15-445 的 B+ 树、`git` 的 pack-index 分层、OS 多级页表全是这个思想（详见 L26 末与"跨课程"节）。
- **旋转（rotation）**：局部三节点重组，恢复 BST 序且高度降 1：
  ```java
  Node rotateRight(Node y) {          // 左倾 → 右旋
      Node x = y.left; y.left = x.right; x.right = y;
      y.height = 1 + Math.max(h(y.left), h(y.right));
      x.height = 1 + Math.max(h(x.left), y.height);
      return x; // x 成为新子树根
  }
  ```
- **AVL（项目主讲）**：|bal(hL−hR)| ≤ 1；插入后沿路径回溯，在不平衡节点做 LL/RR/LR/RL 四类（双旋=单旋组合）共 ≤2 次旋转复原。最坏高 ≤ 1.44·log₂n + 2 —— **全课唯一给出精确高度界的结构**。
- **红黑树（JDK TreeMap 选型）**：5 条性质（根黑/叶 NIL 黑/红不连续/黑高一致）⇒ 最长红黑路径 ≤2×最短；插入至多 2 次旋转、删除 ≤3 次，染色修复常沿路 O(log n) 但旋转少——写数据库/内核者偏爱 RB，写查询密集者偏爱 AVL。
- **跳表（Redis zset）**：分层链表，期望 Θ(log n)，无旋转、实现 50 行、天然支持 range 与无锁——"用随机性换确定性平衡"的第三条路。

## 2. 三种平衡策略对比

| 维度 | AVL | 红黑树 | 跳表 |
| --- | --- | --- | --- |
| 高度界 | 1.44 log n（严） | 2 log(n+1)（松） | 期望 O(log n) |
| 插入旋转 | ≤2 | ≤2 | 0 |
| 删除旋转 | O(log n) | ≤3 | 0 |
| 查询 | 最快 | 中 | 中+指针追逐 |
| 实现难度 | 高（平衡因子） | 很高（case 多） | 低 |
| 谁在用 | 内存字典、数据库内部索引候选 | JDK TreeMap/HashMap树化/Linux CFS/epoll | Redis、HBase/LevelDB memtable |

## 3. 复杂度视角

| 操作 | 2-3 树 | AVL/RB | 普通 BST 平均/最坏 |
| --- | --- | --- | --- |
| search/insert/delete | Θ(log n) 保证 | Θ(log n) 保证 | Θ(log n)/Θ(n) |
| floor/ceiling/successor | Θ(log n) | Θ(log n) | 同 |
| 空间 | Θ(n)（节点更大） | Θ(n) | Θ(n) |

## 4. 与前后讲联系

- 上承 L25 的"成本=树高"与删除下沉技巧（AVL 双旋常把失衡点上移一层）；L24 的 Comparable。
- 下启：L28 堆"只保证父≤子"的弱不变量换来数组存储与 O(1) peek；L36 Trie 是完全不平衡但"高=键长"的特例；L23 选型表至此补齐 TreeMap 内部机制。

## 5. 跨课程联系

- **CS61A**：无对应（61A 不碰平衡）；但 Scheme 的 `assoc-list` vs hash-table 与"有序树 vs 哈希"构成两课共同的两难叙事。
- **6.006/CS170/6.046**：6.006 明示"跳过红黑树实现，当作黑盒"；6.046/CS170 给 RB 性质的完整证明；AVL 高度递推 N(h)=N(h−1)+N(h−2)+1（斐波那契下界）是 61B 可完成的少数"证明练习"。
- **CSAPP**：旋转 = 改 2–3 个指针，常数极小；但每次下降 2 次 cache miss，树深 20 即 ~40 次 miss ≈ 百纳秒——理解"为什么磁盘上改用 B 树"。
- **DDCA/OS**：Linux 多级页表是"以地址段为 key 的静态 B 树"（4 级 × 512 扇出）；OS 用"页大小 4KB 对齐"支付 locality 成本换取扇出。
- **15-445**：B+ 树 = 2-3-4 树 + 叶级链表（范围扫描）+ 页内 slot 二分；bufferpool 使"一次树下降 = 最多 h 次 I/O"成为数据库第一成本模型；跳表在 15-445 作为 B+ 树替代索引讨论（Bw-tree）。

## 6. 开源项目应用

- **JDK**：`TreeMap` 红黑树（`fixAfterInsert` 的三色翻转+旋转）；`HashMap.TreeNode` 把冲突链树化（限深 2×bin 阈值，RB 性质兜底 L21 的最坏 Θ(n)）。
- **Linux**：CFS 调度树（rb_root_cached 取最左 O(1)）、`mm_struct` 曾用的红黑树、XFS inode B+ 树。
- **RocksDB/LevelDB**：memtable 用跳表；SST 内索引 + 顶层 manifest 是 B 树式分层。
- **Lucene**：`BKD 树`（数值多维索引）是平衡 kd 树变体，页式打包——同一"平衡+分页"哲学。
- **PostgreSQL**：B+ 树 + `btree_gin`；"B 树去重键"（deduplication）论文级工程细节可作汇报加分。

## 7. 延伸阅读

- Hug 笔记 "Balanced Trees" "AVL Tree Rotations"；CLRS 13.2（RB 插入骨架）+ 13 章习题的高度证明。
- Sedgewick algs4 3.3 左倾红黑树（LLRB，~30 行等价实现，最适合复写）。
- Pugh 跳表原论文（1990）；《The Art of Computer Programming 3》6.2.3 平衡树历史。
