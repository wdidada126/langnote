# jdk1.8 HashMap源码分析

#### 简介
- 是一个数组，数组的单个元素是一系列集合，集合在数量少的时候是链表，多的时候是红黑树。
- 为什么当数量多了，就使用红黑树呢？
- 个人理解是提高操作效率。具体可以对比下链表和红黑树的异同
- 数组的大小也是不固定的，有loadFactor，一般翻译为平衡因子。
- 自动扩容，减少。

#### HashMap的方法
put方法，返回V类型的值
函数原型是
public V put(K key, V value)
个人曾经吧返回值当成是void类型的。

public V remove(Object key)


#### 成员变量
- static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
- static final int MAXIMUM_CAPACITY = 1 << 30;
- static final float DEFAULT_LOAD_FACTOR = 0.75f;
- static final int TREEIFY_THRESHOLD = 8;
- static final int UNTREEIFY_THRESHOLD = 6;
- static final int MIN_TREEIFY_CAPACITY = 64;
- transient Node<K,V>[] table;
- transient Set<Map.Entry<K,V>> entrySet;
- transient int size;

方法可以参考https://docs.oracle.com/javase/8/docs/api/ 找到HashMap这个类

#### 内部数据结构：

```java
Node<K,V>
static class Node<K,V> implements Map.Entry<K,V>{
	final int hash;
        final K key;
        V value;
        Node<K,V> next;
}
```

```java
LinkedHashMap
 static class Entry<K,V> extends HashMap.Node<K,V> {
        Entry<K,V> before, after;
        Entry(int hash, K key, V value, Node<K,V> next) {
            super(hash, key, value, next);
        }
    }
}
```

```java
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
    TreeNode<K,V> parent;  // red-black tree links
    TreeNode<K,V> left;
    TreeNode<K,V> right;
    TreeNode<K,V> prev;    // needed to unlink next upon deletion
    boolean red;
}
```

#### 参考文章
详细的分析可以参考:[Java集合源码分析之Map（五）：HashMap](https://www.jianshu.com/p/f16bfeeeea88)