# 项目 2：HashMap — 分离链 + 倍增再哈希

> 对应讲次：L20（hash code 契约、分离链）、L21（装填因子、倍增再哈希）、L22（好哈希、扰动、字符串键）。
> 对应课程作业：Lab6（THashMap 官方模板同款）；JDK 对照：`java.util.HashMap`。

## 知识点清单

| 文件 | 知识点 | 复杂度 |
| --- | --- | --- |
| `THashMap` | 桶数组 + 链、`Math.floorMod` 防负 hash、`spread` 高位扰动、α>0.75 再哈希、迭代器（跳空桶）、null 键、`longestChain()` 诊断 | put/get 期望 Θ(1)、最坏 Θ(n)；再哈希摊还 Θ(1) |
| `HashFunctions` | Horner/31 字符串哈希、均匀性直方图、"Aa"/"``" 碰撞对（X 差 31、Y 差 1） | 字符串哈希 Θ(m) |
| `Main` | 更新语义、5000 键再哈希后抽查、StickyKey（hashCode≡1）攻击实验、低位全 0 键实验 | — |

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
# 等价手工命令：
javac -encoding UTF-8 -d build src/cs61b/hashmap/*.java
java -cp build cs61b.hashmap.Main
```

## 实验建议

1. 把 `MAX_LOAD_FACTOR` 改为 0.5 / 0.95，观察 `rehashCount` 与 `longestChain` 的空间-时间交换。
2. 删掉 `spread`（扰动），用 `i * 512` 做键跑 `uniformity` 思路的测试，理解 JDK 为什么要 `h ^ (h>>>16)`（桶数是 2 的幂时低位主导）。
3. 对照阅读：JDK `HashMap.resize()`（一次遍历同时完成高低位拆分）与 `HashMap.TreeNode`（链长>8 转红黑树，L27 的伏笔）。
