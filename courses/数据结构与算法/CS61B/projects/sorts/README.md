# 项目 8：排序家族 — 插入基准 + 归并 / 快排 / 堆排 + 基数

> 对应讲次：L34（选择/插入、归并、快排）、L35（稳定性、下界、基数排序、Arrays.sort 工程）。
> JDK 对照：`java.util.Arrays`（原始类型双轴快排 / 对象 TimSort）。

## 知识点清单

| 方法 | 讲次要点 | 最好/最坏 | 稳定 | 空间 |
| --- | --- | --- | --- | --- |
| `insertion` | 自适应基准：Θ(n+逆序数)，快排小数组终结者 | Θ(n)/Θ(n²) | ✔ | Θ(1) |
| `merge`（自顶向下角色交替）/ `mergeSort`(泛型) | `<=0 取左` ⇒ 稳定性证明点在代码里 | Θ(n log n) 恒定 | ✔ | Θ(n) |
| `quick` | 三数取中 + 切插入 + 先递归小半区（栈深 O(log n)） | Θ(n log n)/Θ(n²) 全等键 | ✘ | Θ(log n) |
| `heap` | O(n) 建堆 + 原地 poll | Θ(n log n) 恒定 | ✘ | Θ(1) |
| `radixLSD` | 跳出比较模型：4 轮 × 256 桶的稳定计数排序 | Θ(4(n+256)) | ✔(轮内) | Θ(n) |

`Main` 的三组特色实验：8 组边界用例 × 4 算法对拍 `Arrays.sort`（diff testing）；等键 id 递增检验归并稳定性；2e6 规模基数排序计时。

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/sorts/*.java
java -cp build cs61b.sorts.Main
```

## 实验建议

1. 注释掉 quick 的三数取中，喂 `sorted` 用例看 O(n²) 退化（配合计时）。
2. 给 radixLSD 增加负数支持（写入前 `x ^ 0x80000000` 翻符号位，读出时翻回）。
3. 实现"多关键字稳定排序"：先用次键 mergeSort、再用主键 mergeSort，验证与 Comparator 链式 `thenComparing` 结果一致——L24 + L35 的合流。
