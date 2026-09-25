# 项目 1：线性表三件套 — DLList / ArraySeq / ResizableArray

> 对应讲次：L16（数组与链表）、L17（动态数组与摊还）、L18（双向链表）、L19（Deque 设计语境）。
> 对应课程作业：Lab4 / Project1a 的手写结构部分；JDK 对照：`java.util.LinkedList`、`java.util.ArrayList`。

## 知识点清单

| 类 | 知识点 | 复杂度承诺 |
| --- | --- | --- |
| `DLList` | 哨兵节点、prev/next 缝合、双向遍历、fail-fast 迭代器、不变量自检 `checkInvariants()` | 两端 add/remove Θ(1)；get Θ(min(i, n−i)) |
| `ArraySeq` | 泛型数组创建限制、倍增扩容、`System.arraycopy`、1/4 缩容防抖动 | addLast/removeLast/get 摊还 Θ(1)；addFirst Θ(n) |
| `Main` | 摊还实验（1e4 次 add 扩容 <20 次）、双向链表链完整性断言、选型对比 | — |

## 编译与运行（JDK 17，无外部依赖）

```bash
# Linux/macOS
./build.sh
# Windows
build.bat
```

手工命令等价：

```bash
javac -encoding UTF-8 -d build src/cs61b/dllist/*.java
java -cp build cs61b.dllist.Main
```

## 实验建议

1. 把 `ArraySeq` 扩容量从 `*2` 改为 `+8`，观察 `resizeCount` 从 <20 变为 ~1250——亲手复现 L17"为什么必须几何扩容"。
2. 给 `DLList` 增加 `reverse()`（Θ(n) 交换每个节点 prev/next），再调用 `checkInvariants()`。
3. 对照阅读：JDK `LinkedList.linkLast/unlink` 与 `ArrayList.grow()` 源码。
