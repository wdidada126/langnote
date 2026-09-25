package cs61b.dllist;

import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Objects;

/**
 * 泛型双向链表（L18）。哨兵节点使首/尾/空表统一处理，
 * 任意位置已知节点的插入/删除为 Θ(1)（L18 检查清单）。
 * 不变量：对任意节点 p，p.next.prev == p 且 p.prev.next == p；
 *         空表时 sentinel.next == sentinel.prev == sentinel。
 */
public class DLList<Item> implements Iterable<Item> {

    private class Node {
        Item item;
        Node prev, next;
        Node(Item i, Node p, Node n) { item = i; prev = p; next = n; }
    }

    private final Node sentinel;
    private int size;
    private int modCount; // fail-fast 迭代器（L18 检查清单第 3 条）

    public DLList() {
        sentinel = new Node(null, null, null);
        sentinel.next = sentinel;
        sentinel.prev = sentinel;
        size = 0;
        modCount = 0;
    }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    public void addFirst(Item x) { insertAfter(sentinel, x); }
    public void addLast(Item x) { insertAfter(sentinel.prev, x); }

    private void insertAfter(Node p, Item x) {
        Node n = new Node(x, p, p.next);
        p.next.prev = n;
        p.next = n;
        size++; modCount++;
    }

    public Item removeFirst() {
        if (isEmpty()) throw new NoSuchElementException("empty list");
        return unlink(sentinel.next);
    }

    public Item removeLast() {
        if (isEmpty()) throw new NoSuchElementException("empty list");
        return unlink(sentinel.prev);
    }

    private Item unlink(Node p) {
        p.prev.next = p.next;
        p.next.prev = p.prev;
        size--; modCount++;
        return p.item;
    }

    /** Θ(min(i+1, size-i))：双向链表的优势——从近的一端走（L24 JDK LinkedList 同款补偿）。 */
    private Node node(int i) {
        if (i < 0 || i >= size) throw new IndexOutOfBoundsException("index " + i + ", size " + size);
        Node p;
        if (i < size / 2) {
            p = sentinel.next;
            for (int k = 0; k < i; k++) p = p.next;
        } else {
            p = sentinel.prev;
            for (int k = size - 1; k > i; k--) p = p.prev;
        }
        return p;
    }

    public Item get(int i) { return node(i).item; }
    public Item set(int i, Item x) {
        Node p = node(i);
        Item old = p.item;
        p.item = x;
        return old;
    }
    public void add(int i, Item x) {
        if (i == size) { addLast(x); return; }
        insertAfter(node(i).prev, x);
    }
    public Item remove(int i) { return unlink(node(i)); }

    public boolean contains(Item x) {
        for (Node p = sentinel.next; p != sentinel; p = p.next)
            if (Objects.equals(p.item, x)) return true;
        return false;
    }

    @Override
    public Iterator<Item> iterator() {
        return new Iterator<Item>() {
            private Node p = sentinel.next;
            private final int expected = modCount;
            public boolean hasNext() { return p != sentinel; }
            public Item next() {
                if (modCount != expected)
                    throw new java.util.ConcurrentModificationException();
                if (!hasNext()) throw new NoSuchElementException();
                Item it = p.item;
                p = p.next;
                return it;
            }
        };
    }

    /** 调试用：全表双向一致性检查（L18 检查清单第 1 条），违反不变量即抛异常。 */
    public void checkInvariants() {
        if (sentinel.next == null || sentinel.prev == null) throw new AssertionError("null link");
        int n = 0;
        for (Node p = sentinel.next; p != sentinel; p = p.next) {
            if (p.next.prev != p || p.prev.next != p) throw new AssertionError("broken link at " + p.item);
            n++;
        }
        int m = 0;
        for (Node p = sentinel.prev; p != sentinel; p = p.prev) m++;
        if (n != size || m != size) throw new AssertionError("size mismatch: fwd " + n + " back " + m + " book " + size);
    }
}
