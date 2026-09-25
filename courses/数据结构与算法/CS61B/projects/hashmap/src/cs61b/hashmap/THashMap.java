package cs61b.hashmap;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;

/**
 * 分离链法哈希表（L20–L21，Lab6 风格）。
 * 要点：
 *  - 桶定位：Math.floorMod(hash(key), cap)（floorMod 处理负 hash，L21）；
 *  - hash 扰动：h ^ (h >>> 16)，把高 16 位差异搬进低位（JDK HashMap 同款，L22）；
 *  - 装填因子 α > 0.75 ⇒ 桶数倍增 + 全量再哈希（摊还 Θ(1)，与 L17 同构）；
 *  - 键的冲突处理用 equals——hashCode 相同也能正确工作，只是变慢（最坏 Θ(n)）。
 */
public class THashMap<K, V> implements Iterable<java.util.Map.Entry<K, V>> {

    private static final double MAX_LOAD_FACTOR = 0.75;

    private class Node {
        final K key; V value; Node next;
        Node(K k, V v, Node n) { key = k; value = v; next = n; }
    }

    private Node[] buckets;
    private int size;
    private long rehashCount; // 实验统计：n 次 put 共再哈希 Θ(n) 总工作量 / 次数 ≈ log2(n)

    @SuppressWarnings("unchecked")
    public THashMap() { buckets = (Node[]) new Object[8]; }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }
    public int bucketCount() { return buckets.length; }
    public long rehashCount() { return rehashCount; }

    private static int spread(int h) { return h ^ (h >>> 16); }
    private int index(Object key) {
        int h = key == null ? 0 : spread(key.hashCode()); // null 键固定走 0 桶（JDK HashMap 同款约定）
        return Math.floorMod(h, buckets.length);
    }

    /** 插入或更新；返回旧值（无则 null）。 */
    public V put(K key, V value) {
        int i = index(key);
        for (Node n = buckets[i]; n != null; n = n.next)
            if (Objects.equals(n.key, key)) { V old = n.value; n.value = value; return old; }
        buckets[i] = new Node(key, value, buckets[i]);
        size++;
        if ((double) size / buckets.length > MAX_LOAD_FACTOR) resizeAndRehash(buckets.length * 2);
        return null;
    }

    public V get(Object key) {
        Node n = find(key);
        return n == null ? null : n.value;
    }

    public boolean containsKey(Object key) { return find(key) != null; }

    private Node find(Object key) {
        for (Node n = buckets[index(key)]; n != null; n = n.next)
            if (Objects.equals(n.key, key)) return n;
        return null;
    }

    public V remove(Object key) {
        int i = index(key);
        Node prev = null;
        for (Node n = buckets[i]; n != null; prev = n, n = n.next) {
            if (Objects.equals(n.key, key)) {
                if (prev == null) buckets[i] = n.next; else prev.next = n.next;
                size--;
                return n.value;
            }
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    private void resizeAndRehash(int newCap) {
        Node[] old = buckets;
        buckets = (Node[]) new Object[newCap];
        rehashCount++;
        for (Node head : old)
            for (Node n = head; n != null; ) {
                Node next = n.next;              // 先存后继再摘链（L16 指针改写顺序）
                int h = n.key == null ? 0 : spread(n.key.hashCode());
                int i = Math.floorMod(h, newCap);
                n.next = buckets[i];
                buckets[i] = n;
                n = next;
            }
    }

    public List<K> keys() {
        List<K> out = new ArrayList<>();
        for (var e : this) out.add(e.getKey());
        return out;
    }

    public List<V> values() {
        List<V> out = new ArrayList<>();
        for (var e : this) out.add(e.getValue());
        return out;
    }

    @Override
    public Iterator<java.util.Map.Entry<K, V>> iterator() {
        return new Iterator<>() {
            private int bi = 0;
            private Node n = nextNonEmpty();
            private Node nextNonEmpty() {
                while (bi < buckets.length) {
                    if (buckets[bi] != null) return buckets[bi];
                    bi++;
                }
                return null;
            }
            public boolean hasNext() { return n != null; }
            public java.util.Map.Entry<K, V> next() {
                if (n == null) throw new NoSuchElementException();
                var e = new java.util.AbstractMap.SimpleImmutableEntry<>(n.key, n.value);
                if (n.next != null) n = n.next;
                else { bi++; n = nextNonEmpty(); }
                return e;
            }
        };
    }

    /** 诊断：最长链长度。冲突攻击/坏 hashCode 时退化 Θ(n) 的可见证据（L22）。 */
    public int longestChain() {
        int best = 0;
        for (Node head : buckets) {
            int len = 0;
            for (Node n = head; n != null; n = n.next) len++;
            best = Math.max(best, len);
        }
        return best;
    }
}
