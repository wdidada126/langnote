# 项目 4：堆 / 优先队列 / Top-K

> 对应讲次：L28（堆与优先队列、heapify 线性建堆）。
> 对应课程作业：Lab8；JDK 对照：`java.util.PriorityQueue`（同小顶堆约定）。

## 知识点清单

| 文件 | 知识点 | 复杂度 |
| --- | --- | --- |
| `Heap` | 完全二叉树的数组表示（(i−1)/2、2i+1）、siftUp/siftDown、Comparator 决定堆顶语义、O(n) build、`checkHeap()` | offer/poll Θ(log n)；peek Θ(1)；build Θ(n) |
| `TopK` | 流式 Top-K：大小为 K 的候选小顶堆；泛型 + record 自定义比较器示例 | Θ(n log k) 时间 / Θ(k) 空间 |
| `Main` | poll 序列=排序（堆排序）、随机数据一致性、最大堆=reverseOrder 约定实验 | — |

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/heap/*.java
java -cp build cs61b.heap.Main
```

## 实验建议

1. 把 `build()` 改成逐个 `offer()`（Θ(n log n)），对比 n=10⁶ 的耗时——亲手验证 CLRS 6.3 的 Σh/2ʰ=Θ(n)。
2. 给 Heap 增加 `IndexHeap`（key→堆位置 的 HashMap + `decreaseKey`），这是 projects/graph 里 Dijkstra 需要"堆内更新键"的正规解法（L32 笔记：Θ((V+E)log V) 的前提）。
3. 对照阅读 JDK `PriorityQueue` 的 `siftUpComparable/siftDownComparable`——与本实现逐行同构，仅少泛型 Comparator 分支。
