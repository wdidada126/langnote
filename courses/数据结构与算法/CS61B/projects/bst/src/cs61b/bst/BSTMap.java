package cs61b.bst;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * 普通二叉搜索树（L25）：一切成本 = Θ(树高)。
 * 不变量：任意节点 x，左子树所有 key < x.key < 右子树所有 key ⇒ 中序即升序。
 * 本类不保证平衡——Main 里演示有序输入退化成链表。
 */
public class BSTMap<K extends Comparable<K>, V> {

    private class Node {
        K key; V value; Node left, right;
        Node(K k, V v) { key = k; value = v; }
    }

    private Node root;
    private int size;

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    /** 迭代下降插入/更新，返回旧值（无则 null）。最坏 Θ(h)。 */
    public V put(K key, V value) {
        if (root == null) { root = new Node(key, value); size++; return null; }
        Node p = root;
        while (true) {
            int c = key.compareTo(p.key);
            if (c == 0) { V old = p.value; p.value = value; return old; }
            if (c < 0) {
                if (p.left == null) { p.left = new Node(key, value); size++; return null; }
                p = p.left;
            } else {
                if (p.right == null) { p.right = new Node(key, value); size++; return null; }
                p = p.right;
            }
        }
    }

    public V get(Object key) {
        Node x = root;
        @SuppressWarnings("unchecked")
        K k = (K) key;
        while (x != null) {
            int c = k.compareTo(x.key);
            if (c == 0) return x.value;
            x = c < 0 ? x.left : x.right;
        }
        return null;
    }

    public K min() {
        if (root == null) throw new NoSuchElementException("empty");
        Node x = root;
        while (x.left != null) x = x.left;
        return x.key;
    }

    /** 中序遍历：Θ(n)，与树形无关（每边访问一次）。 */
    public List<K> keysInOrder() {
        List<K> out = new ArrayList<>();
        inorder(root, out);
        return out;
    }
    private void inorder(Node x, List<K> out) {
        if (x == null) return;
        inorder(x.left, out);
        out.add(x.key);
        inorder(x.right, out);
    }

    /** 删除四情形（L25）：叶 / 独子 / 双子（用中序后继替换再删后继）。 */
    public V remove(K key) {
        found = false;
        lastRemovedValue = null;
        root = remove(root, key);
        return found ? lastRemovedValue : null;
    }

    private V lastRemovedValue;
    private boolean found;

    private Node remove(Node x, K key) {
        if (x == null) return null;
        int c = key.compareTo(x.key);
        if (c < 0) { x.left = remove(x.left, key); return x; }
        if (c > 0) { x.right = remove(x.right, key); return x; }
        found = true;
        lastRemovedValue = x.value;
        size--;
        if (x.left == null) return x.right;
        if (x.right == null) return x.left;
        // 双子：右子树最左（中序后继）顶替，只下沉一层
        Node succParent = x, succ = x.right;
        while (succ.left != null) { succParent = succ; succ = succ.left; }
        if (succParent == x) x.right = succ.right; else succParent.left = succ.right;
        succ.left = x.left;
        succ.right = x.right;
        return succ;
    }

    /** 树高（空树记 0）：退化诊断用。 */
    public int height() { return height(root); }
    private int height(Node x) {
        if (x == null) return 0;
        return 1 + Math.max(height(x.left), height(x.right));
    }

    /** 调试：验证 BST 不变量（中序严格升序）。 */
    public void checkBST() {
        K prev = null;
        for (K k : keysInOrder()) {
            if (prev != null && !(prev.compareTo(k) < 0)) throw new AssertionError("BST 不变量被破坏");
            prev = k;
        }
    }

    @Override
    public String toString() { return "BST" + keysInOrder(); }
}
