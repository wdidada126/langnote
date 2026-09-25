# 项目 7：并查集（Union-Find）三级演进

> 对应讲次：L31（并查集与 MST 判环）。
> 对应课程作业：Lab（UnionFind）、HW（Asteroids 连通块）；JDK 对照：**无内置**（手写高频考点）。

## 知识点清单

| 文件 | 版本 | find | union | 备注 |
| --- | --- | --- | --- | --- |
| `QuickFindUF` | 标签数组 | Θ(1) | **Θ(n)** | 大量 union 被"重贴标签"打爆 |
| `QuickUnionUF` | 森林 | O(h)，可被链攻击 Θ(n) | Θ(1) | Main 的 chainAttack 演示 |
| `WeightedQuickUnionCompUF` | 加权 + 路径压缩 | 摊还 ~Θ(α(n)) | 同左 | Tarjan 1984（papers.md C6/C7） |
| `Main` | diff testing（三实现互验）、操作计数、6 万 union 对比 | — | L13 测试思想 |

`ops` 字段把 L15 的"操作记账"变成可打印的实测数字——这是本课程"渐近分析→实验验证"闭环的最小实现。

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/uf/*.java
java -cp build cs61b.uf.Main
```

## 实验建议

1. 实现 percolation 迷你版：n×n 网格随机开格，上下边界虚拟结点用本 UF 连"贯穿"——课程 HW 原题。
2. 把两遍压缩改成"每步指向祖父"的单遍压缩（graph 项目里同款），对比 `ops`。
3. 只压缩不加权 / 只加权不压缩各做一个变体，观察 chainAttack 中哪个环节各防住了什么（加权防最坏链、压缩防重复长查）。
