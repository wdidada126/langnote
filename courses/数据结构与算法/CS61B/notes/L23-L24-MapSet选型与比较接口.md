# L23–L24 Map/Set 工程对比与比较接口（Comparable/Comparator）

> 对应 spring2024 L23–L24：HashMap vs TreeMap 选型、Map/Set API 全景、Comparable/Comparator、有序遍历。作业：HW3。

## 1. 核心概念

- **同一 Map 接口，两种世界观**：
  | 维度 | HashMap | TreeMap |
  | --- | --- | --- |
  | 底层 | 桶数组+链/树 | 红黑树 |
  | get/put | Θ(1) 期望 | Θ(log n) 最坏 |
  | 迭代顺序 | 不确定（依赖 hash） | key 升序（`firstEntry`→`higherKey` 链）|
  | range/first/last | 不支持 | `subMap/floorKey/ceilingKey` Θ(log n) |
  | key 要求 | equals+hashCode | compareTo（或 Comparator）|
  | null 键 | 允许 1 个 | 不允许（无法比较）|
- **Set = Map 的投影**：`HashSet` 内部就是 `HashMap<E,PRESENT>`；TreeSet 包 TreeMap。理解映射即理解全部四大集合。
- **Comparable vs Comparator**：
  - `Comparable<T>`：自然序，写在类里，`a.compareTo(b)`；"我天生可排"。
  - `Comparator<T>`：外置序，lambda 一行：`Comparator.comparing(Player::getScore).thenComparing(p -> p.name)`；"按某把尺子排"。
  ```java
  record Point(int x, int y) implements Comparable<Point> {
      public int compareTo(Point o) { // 禁止 a-b（溢出！L02 回绕）
          return x != o.x ? Integer.compare(x, o.x) : Integer.compare(y, o.y);
      }
  }
  ```
- ** TreeSet 有序遍历 = 中序**：`forEach` 即树的中序迭代（L25 的下一次出场）；迭代器内部沿 leftmost 再 repeatedly `successor`。

## 2. 选型决策树（考试与面试模板）

1. 需要 range 查询/有序遍历/最近键？→ TreeMap（或跳表，见 L27）。
2. 只要点查、key 有良好 hash？→ HashMap。
3. 需要按多种键重复查询？→ 多个 Map 视图（数据库"二级索引"思维的雏形，呼应 CS186）。
4. 并发？→ ConcurrentHashMap（分段锁）/ synchronizedMap；TreeMap 无并发替身需自加锁。

## 3. 与前后讲联系

- 上承：L08–L11 API 规格、L20–L22 哈希、L25 起补 TreeMap 的另一半（树）。
- 下启：L25–L28 亲手造出这两大实现；L34 排序讲"数组排序 vs TreeMap 遍历"两种有序化路径；Lab6/BST Lab 的 spec 都以本讲 API 为合同。

## 4. 跨课程联系

- **CS61A**：61A 的 dict 只有哈希一种且从不比较；61B 首次直面"序"是另一种组织原则——这个二元对立会贯穿到 15-445 的 hash index vs B+ tree index。
- **6.006**：6.006 用有序数组 + 二分替代平衡树（避免红黑树工程细节），其"字典 ADT"三实现对照表（链式哈希/开放寻址/有序数组）与本讲两张表互补。
- **CSAPP**：TreeMap 的指针追逐 + 节点膨胀 vs HashMap 数组 locality——两者 benchmark 差距在 n>10⁵ 后显著，正是"渐近同类、常数分野"。
- **15-445**：Bufferpool 页内 slot 数组用 hash 定位、B+ 树页内用有序数组 + 页内二分——两大阵营在磁盘页粒度上重演本课 L23 的选择。
- **OS**：进程调度器 CFS 以 vruntime 为 key 的红黑树（有序 + 取最小 = TreeMap.firstEntry 的 O(log n) 版）。

## 5. 开源项目应用

- **JDK**：`EnumMap`（数组实现，key 小整数域时碾压前两者）、`LinkedHashMap`（HashMap+DLList，accessOrder=true 即 LRU）都是本讲谱系的扩展。
- **Lucene**：terms 按字典序存储（支持 range/prefix 查询）→ 选"树/有序"侧；`FieldInfos` 编号映射 → 哈希侧。
- **RocksDB**：默认 MemTable=SkipList（有序，范围扫描）但可换 `hash_skiplist`/`cuckoo`（点查专用）——官方文档就是一道 L23 选型题。
- **Redis**：`hash` 类型在元素少且 ≤64B 时用 ziplist（线性小数组），否则 dict（哈希）；`zset` 需要序 → dict + skiplist 双结构——"按操作画像配结构"的教科书。
- **Spring**：`Comparator` 组合子被 `@Order`/`AnnotationAwareOrderComparator` 用于切面与处理器排序。

## 6. 延伸阅读

- Hug 笔记 "Map Implementations" "Comparison Interfaces"。
- JDK javadoc 精读：`SortedMap`/`NavigableMap` 契约、`Comparator` 默认方法组。
- 《Effective Java》Item 14（compareTo 一致性）、Item 24 之后的 lambda/Comparator 惯用法；CS:APP Ch.7 关于链接与加载对性能影响。
