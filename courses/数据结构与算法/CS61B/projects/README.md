# CS61B 配套项目总表（projects）

> 语言 Java（**JDK 17 语法**，零外部依赖）。每个项目自洽：含包结构源码 + `main` 自测断言 + README + `build.bat`/`build.sh`（javac/java 版）。
> 统一约定：源码在 `src/cs61b/<项目>/*.java`；编译输出 `build/`；包名以 `cs61b.` 开头避免与 JDK 冲突。
> 各 main 全部以 `println("ok - …")` 报告通过、以 `AssertionError` 报告失败——可当"零配置单元测试"跑。

| # | 目录 | 主题 | 对应讲次 | 对应课程作业 | 核心知识点 | 规模 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `dllist/` | 线性表：DLList + ArraySeq(ResizableArray) | L16–L19 | Lab4 / Project1a | 哨兵、双向缝合、倍增扩容摊还、1/4 缩容防抖动 | 3 类 |
| 2 | `hashmap/` | 分离链 HashMap + 再哈希 + 哈希函数 | L20–L22 | Lab6 | floorMod、spread 扰动、α=0.75、StickyKey 碰撞攻击、Horner/31 | 3 类 |
| 3 | `bst/` | BST 与 AVL（讲透 AVL） | L25、L26–L27 | Lab7 | 删除四情形、退化实验、LL/RR/LR/RL 四旋转、1.44·log2(n+2) 界验证 | 3 类 |
| 4 | `heap/` | 二叉堆 / 优先队列 / Top-K | L28 | Lab8 | 数组完全树、O(n) heapify、Comparator 定堆顶、Θ(n log k) Top-K | 3 类 |
| 5 | `trie/` | 前缀树 / 自动补全 / 删除剪枝 | L36 | Lab(Trie) | end 标志、keysWithPrefix DFS、词频堆限 k、nodeCount 空间账 | 2 类 |
| 6 | `graph/` | 图：BFS/DFS/Dijkstra/Prim/Kruskal | L29–L32 | Lab9/Lab10/Maze HW | 邻接表 API、懒惰 PQ 松弛、cut 性质双算法互验、手工预算测试图 | 4 类 |
| 7 | `unionfind/` | 并查集三级演进 | L31 | Lab(UF)/Asteroids | quick-find vs quick-union vs 加权+压缩；ops 计数 + 链攻击 | 5 类 |
| 8 | `sorts/` | 排序家族：插入基准 + 归并/快排/堆排/基数 | L34–L35 | — | 稳定性(等键保序)、三数取中+小数组切插+尾递归、4×256 桶 LSD、2e6 计时 | 2 类 |
| 9 | `minigit/` | MiniGit：哈希寻址 blob + commit DAG | L20/L29/L36/L37 | **Project3 GITLET** | objects/xx 两级分桶、同内容同 ID 去重、ref 文件=分支 O(1)、findFile 祖先回溯 | 3 类 |

## 快速运行（任选其一）

```bash
# 以 hashmap 为例，Windows 用 build.bat
cd hashmap && ./build.sh
# 手工等价（JDK 17）：
javac -encoding UTF-8 -d build src/cs61b/hashmap/*.java
java  -cp build cs61b.hashmap.Main
```

一键全跑（Git Bash，Windows/Linux 同）：

```bash
for d in dllist hashmap bst heap trie graph unionfind sorts minigit; do
  (cd "$d" && ./build.sh) || echo "FAILED: $d"
done
```

## 建议顺序（与 notes/ 同步）

1. `dllist` → 笔记 L16–L19（先把"数组 vs 链表"的手感建立起来）
2. `hashmap` → L20–L22（第一次组合已学技术造大结构）
3. `bst` → L25 + L26–L27（重点：四旋转 + 两个高度实验对照）
4. `heap` → L28（随后在 graph 里回收：Dijkstra 的 PQ）
5. `unionfind` → L31（ops 计数是 L15/L17 摊还的实验课）
6. `graph` → L29–L32（同一测试图跑四种算法，交叉验证）
7. `sorts` → L34–L35（稳定性与退化实验）
8. `trie` → L36
9. `minigit` → 全课收官（哈希+图+I/O+序列化合体，Project3 精神续作）

## 扩展题（每个 README 底部有 3 条实验建议，以下是跨项目大题）

- 用 `hashmap` 的 THashMap 替换 `minigit` 的对象索引：内存 map(sha1→bytes) + 落盘缓存，观察代码量变化。
- 给 `graph` 加 A*（L32）：与 Dijkstra 在同一网格图上比较展开节点数。
- 把 `heap` 升级为 IndexHeap 并回灌 `graph` 的 Dijkstra，消除懒惰插入（队列 Θ(E)→Θ(V)）。
