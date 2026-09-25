# 项目 3：BST 与 AVL（讲透 AVL）

> 对应讲次：L25（二叉搜索树）、L26–L27（平衡树：2-3 树动机、AVL/红黑二选一——本项目选 **AVL** 并逐例讲透）。
> 对应课程作业：Lab7；JDK 对照：`java.util.TreeMap`（红黑树实现，本项目的"兄弟"）。

## 知识点清单

| 文件 | 知识点 | 复杂度 |
| --- | --- | --- |
| `BSTMap` | 迭代下降插入、中序遍历、min 沿左下降、删除四情形（后继顶替）、`checkBST()` 不变量自检 | Θ(h)；有序输入 h=n（Main 实测） |
| `AVLTree` | 高度缓存、四类失衡 LL/RR/LR/RL、单/双旋转、回溯更新高度、`checkAVL()` 全树验证 | h ≤ 1.44·log2(n+2)；插入 ≤2 次旋转 |
| `Main` | 退化对比实验（BST 高 2000 vs AVL 高 ~13）、四案例最小构造、5000 随机键全量校验 | — |

**AVL 核心问答**（面试/期末双料）：
1. 为什么 bf 只允许 ±1？——保证 h ≤ 1.44 log n；斐波那契计数证明最坏情况是"每层尽量歪"。
2. 插入回溯时为什么第一个失衡点旋转后整棵树就平衡？——子树高度恢复到插入前的值（≤2 次旋转的由来）。
3. LR 与 RL 为什么必须双旋？——单旋会把新键变成"孤儿"破坏 BST 序（Main 的四案例就是证据）。
4. AVL 删除呢？——BST 删除 + 自被删点向上回溯逐层 `rebalance`（可能 O(log n) 次旋转，比插入贵；作为练习，README 实验 2）。

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/bst/*.java
java -cp build cs61b.bst.Main
```

## 实验建议

1. 记录 `AVLTree.rotationCount`：有序插入 n=2⁴..2¹⁰ 时旋转次数约为 n/2——摊每插入 <1 次，验证"旋转便宜、失衡罕见"。
2. 给 AVLTree 增加 `delete(K)`：复用 BSTMap 的后继顶替 + 沿路径 `updateHeight/rebalanceByFactor`（不依赖 insertedKey，改看孩子 bf），并扩展 `checkAVL()` 回归。
3. 对照阅读 JDK `TreeMap.fixAfterInsertion`：红黑树用"染色 + 旋转"替代"高度缓存"，体会两种不变量的取舍（L26–L27 笔记表格）。
