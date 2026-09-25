# L08–L11 泛型接口：List、Set、Map、Iterable 与泛型方法

> 对应 spring2024 L8–L11：List 层次、Set/Map 抽象、Iterable 与 foreach、泛型方法与有界类型参数、类型擦除。

## 1. 核心概念

- **List 接口层次**：`Collection ← List ← ArrayList / LinkedList`。`add/get/set/remove/size` 是规格；不同实现给出不同复杂度承诺。
- **Set/Map 抽象**：`Set` = 无重复元素的 `Collection`；`Map<K,V>` 不是 `Collection`（键集合 `keySet()`、值集合 `values()`、条目 `entrySet()` 才是）。
- **Iterable 是"可被 for-each"的契约**：
  ```java
  public interface Iterable<T> { Iterator<T> iterator(); }
  // foreach 脱糖为：
  for (Iterator<T> it = list.iterator(); it.hasNext(); ) { T x = it.next(); ... }
  ```
  实现 `iterator()` 即免费获得 foreach、Stream、`addAll` 等一切消费 Iterable 的设施。
- **泛型与有界参数**：
  ```java
  static <T extends Comparable<T>> T max(List<T> xs) { ... }
  ```
  `T extends Comparable<T>` 保证能调用 `compareTo`。PECS 口诀：Producer Extends（读），Consumer Super（写）。
- **类型擦除**：`ArrayList<String>` 运行时就是 `ArrayList`，泛型只在编译期查错；所以 `new T[]` 非法、`List<int[]>` 可行而 `List<int>` 不行（原始类型要用包装类 + 自动装箱）。

## 2. 设计要点：SLList 实现 List 接口

```java
public class SLList61B<T> implements Iterable<T> {
    private class Node { T item; Node next; }
    private Node sentinel; // 哨兵：消灭所有空链表特判
    SLList61B() { sentinel = new Node(); }
    public void addFirst(T x) {
        Node n = new Node(); n.item = x; n.next = sentinel.next; sentinel.next = n;
    }
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private Node p = sentinel.next;
            public boolean hasNext() { return p != null; }
            public T next() {
                if (!hasNext()) throw new NoSuchElementException();
                T it = p.item; p = p.next; return it;
            }
        };
    }
}
```

## 3. 复杂度视角（接口背后的实现差异）

| 操作 | ArrayList | LinkedList | 说明 |
| --- | --- | --- | --- |
| get(i) | Θ(1) | Θ(n) | 随机访问 vs 逐节点走 |
| addFirst | Θ(n) 摊还（搬移） | Θ(1) | ArrayList 头部插入要 System.arraycopy |
| addLast | 摊还 Θ(1) | Θ(1) | 尾指针 |
| iterator.next | Θ(1) | Θ(1) | foreach 遍历两者都 Θ(n) 总成本 |

## 4. 与前后讲联系

- 上承 L04–L07（接口/内部类/多态在本讲合体：每个集合类的 `Itr` 都是内部类实现 `Iterator`）。
- 下启 L16–L19（亲手实现这些接口）、L23（Map 两实现对比）、L24（`Comparable` 是有界泛型的典型）、Lab3/Lab5。

## 5. 跨课程联系

- **CS61A**：61A 用"数据抽象 + 通用性"两条腿（如 generic sum/higher-order）解决同一问题，Java 的答案是参数化类型——同一"复用"理想的类型层与函数层两种实现。
- **6.006**：6.006 用 Python 鸭子类型忽略接口层，把精力全部放在实现选择上；61B 的接口层次相当于把"ADT 规格"写进了编译器。
- **CSAPP**：泛型容器的 `Object` 擦除 = C 的 `void*`；ArrayList 元素是"指向装箱对象的指针数组"，遍历缓存不友好（装箱 + 双重间接），CSAPP 视角解释 benchmark 差异。

## 6. 开源项目应用

- **JDK**：`java.util` 全家福就是本讲接口的实现矩阵；`Arrays.sort(T[])` 是"有界泛型方法"（要求 Comparable）的标准样本；Guava 的 `Collections2.filter` 等把返回 `Collections2` 视图（迭代器壳）用到极致。
- **Lucene**：`DocsEnum extends Iterator 风格` 的稀疏迭代协议遍历倒排链；foreach 语义在列式引擎（如 Arrow）中被换成 `iterator` 的批量版本。
- **RocksDB**：`RocksIterator` 暴露 seek/next，消费方式与 Java Iterator 同构（前向单层抽象）。

## 7. 延伸阅读

- Hug 笔记 "Generic Interfaces: Lists/Sets and Maps/Iterables" "Generic Methods"。
- 《Effective Java》Item 26–31（泛型、通配符）；Angelika Langer 泛型 FAQ（类型擦除最权威解释）。
- JLS §4.6（擦除）、§14.14.2（增强 for 的脱糖）。
