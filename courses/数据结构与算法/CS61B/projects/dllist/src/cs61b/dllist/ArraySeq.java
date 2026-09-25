package cs61b.dllist;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * 可自动扩容/缩容的数组序列（L16 数组 + L17 动态数组/摊还）。
 * 即 61B 的 AList/ResizableArray：倍增扩容 ⇒ addLast 摊还 Θ(1)，get Θ(1)。
 * 缩容阈值取 1/4（而非 1/2）以避免抖动（thrashing），见 L17。
 */
public class ArraySeq<Item> implements Iterable<Item> {

    private Item[] items;
    private int size;
    private int resizeCount; // 实验：统计复制次数，验证 Σ2^i < 2n

    @SuppressWarnings("unchecked")
    public ArraySeq() { this(8); }

    @SuppressWarnings("unchecked")
    public ArraySeq(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        items = (Item[]) new Object[capacity];
        size = 0;
    }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }
    public int capacity() { return items.length; }
    public int resizeCount() { return resizeCount; }

    public void addLast(Item x) {
        if (size == items.length) resize(items.length * 2);
        items[size++] = x;
    }

    /** 头部插入：演示 ArraySeq 的短板——Θ(n) 搬移（对照 DLList.addFirst Θ(1)）。 */
    public void addFirst(Item x) {
        if (size == items.length) resize(items.length * 2);
        System.arraycopy(items, 0, items, 1, size);
        items[0] = x;
        size++;
    }

    public Item removeLast() {
        if (isEmpty()) throw new NoSuchElementException("empty seq");
        Item x = items[--size];
        items[size] = null; // 防内存泄漏（L16：数组元素是引用）
        // 缩容（de-grow）：负载因子 ≤ 1/2 即减半，与倍增扩容配合保证每次操作后
        // 不变量"容量 ≤ 2×size"成立（倍增/减半均为几何步长 ⇒ 摊还 Θ(1)）
        if (size > 0 && 2 * size <= items.length) resize(items.length / 2);
        return x;
    }

    public Item get(int i) { checkIndex(i); return items[i]; }
    public Item set(int i, Item x) { checkIndex(i); Item o = items[i]; items[i] = x; return o; }

    private void checkIndex(int i) {
        if (i < 0 || i >= size) throw new IndexOutOfBoundsException("index " + i + ", size " + size);
    }

    private void resize(int cap) {
        @SuppressWarnings("unchecked")
        Item[] n = (Item[]) new Object[cap];
        System.arraycopy(items, 0, n, 0, size);
        items = n;
        resizeCount++;
    }

    @Override
    public Iterator<Item> iterator() {
        return new Iterator<Item>() {
            private int i = 0;
            public boolean hasNext() { return i < size; }
            public Item next() {
                if (!hasNext()) throw new NoSuchElementException();
                return items[i++];
            }
        };
    }
}
