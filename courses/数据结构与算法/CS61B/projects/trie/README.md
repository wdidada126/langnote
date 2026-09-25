# 项目 5：Trie 前缀树与自动补全

> 对应讲次：L36（Trie、前缀检索、拼写检查/补全应用）。
> 对应课程作业：Lab（Trie）；JDK 对照：**无内置**（java.util 著名缺口）；工业对照：Lucene FST、Redis rax、Linux fib_trie。

## 知识点清单

| 要点 | 实现处 | 复杂度（m=键长，n=键数） |
| --- | --- | --- |
| end 标志区分"前缀"与"整词" | `Node.end` | contains Θ(m) |
| 词频字段 freq | `insert(word, delta)` | — |
| 删除剪枝（自底向上，保留共享前缀） | `delete` 递归返回"可否剪" | Θ(m) |
| 前缀枚举字典序 | `keysWithPrefix`：descend + 排序 DFS | Θ(m + 输出) |
| 自动补全 Top-k by freq | `autocomplete`：JDK `PriorityQueue` 小顶堆限 k | Θ(m + 子树 + s log k) |
| 空间下界实验 | `nodeCount()`：共享前缀省内存 | 最坏 Θ(总字符数) |

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/trie/*.java
java -cp build cs61b.trie.Main
```

## 实验建议

1. 把 `Node.next` 从 HashMap 换成 `Node[26]`（小写字母表），对英文语料比较 `nodeCount()` 与实际内存——验证 L36 笔记"字符集小正是数组复权窗口"。
2. 实现压缩 Trie（Patricia：合并只有一个孩子的链），观察节点数下降幅度（词库越大共享前缀越多，收益越明显）。
3. 拼写检查器：对每个词生成"删一字符/换一字符/换位"的编辑距离 1 候选，用 `contains` 过滤——体会"哈希表 O(1) 点查"与"Trie 前缀剪枝"如何在同一应用分工。
