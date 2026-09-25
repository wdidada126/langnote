package cs61b.bst;

import java.util.ArrayList;
import java.util.List;

/**
 * AVL 树（L26–L27，"讲透 AVL"）：|左右子树高度差| ≤ 1。
 * 插入后沿递归路径回溯，在第一个失衡节点做四类旋转之一：
 *   LL：一次右旋；RR：一次左旋；LR：先左旋子再右旋；RL：对称。
 * 定理：n 节点 AVL 高度 ≤ 1.44·log2(n+2)（斐波那契计数，见笔记）。
 */
public class AVLTree<K extends Comparable<K>> {

    private class Node {
        K key; Node left, right; int height = 1;
        Node(K k) { key = k; }
    }

    private Node root;
    private int size;
    int rotationCount; // 实验统计：一次插入最多 2 次旋转

    public int size() { return size; }
    public int height() { return h(root); }

    // Node 是泛型外部类的非静态内部类（引用类型变量 K），无法声明为 static；
    // 因此这里用实例方法而非静态方法，规避"静态上下文引用非静态类"。
    private int h(Node x) { return x == null ? 0 : x.height; }

    public boolean contains(K key) {
        Node x = root;
        while (x != null) {
            int c = key.compareTo(x.key);
            if (c == 0) return true;
            x = c < 0 ? x.left : x.right;
        }
        return false;
    }

    /** 插入（重复键忽略）。递归模板：下降→挂新→回溯更新高度→必要时旋转。 */
    public void insert(K key) {
        int[] added = new int[1];
        root = insert(root, key, added);
        size += added[0];
    }

    private Node insert(Node x, K key, int[] added) {
        if (x == null) { added[0] = 1; return new Node(key); }
        int c = key.compareTo(x.key);
        if (c < 0) x.left = insert(x.left, key, added);
        else if (c > 0) x.right = insert(x.right, key, added);
        else return x;                       // 重复：AVL 集合语义，忽略
        if (added[0] == 0) return x;         // 下层没真正加（重复），无需再平衡
        updateHeight(x);
        return rebalance(x, key);
    }

    private void updateHeight(Node x) {
        x.height = 1 + Math.max(h(x.left), h(x.right));
    }

    private Node rebalance(Node x, K insertedKey) {
        int bf = h(x.left) - h(x.right);
        if (bf > 1) {
            // 左侧高：看左孩子的倾向
            if (insertedKey.compareTo(x.left.key) < 0) {       // LL
                rotationCount++;
                return rotateRight(x);
            } else {                                            // LR
                rotationCount += 2;
                x.left = rotateLeft(x.left);
                return rotateRight(x);
            }
        }
        if (bf < -1) {
            if (insertedKey.compareTo(x.right.key) > 0) {       // RR
                rotationCount++;
                return rotateLeft(x);
            } else {                                            // RL
                rotationCount += 2;
                x.right = rotateRight(x.right);
                return rotateLeft(x);
            }
        }
        return x;
    }

    /** 左旋（y 的右子 x 上位）——与 rotateRight 镜像。 */
    private Node rotateLeft(Node y) {
        Node x = y.right;
        y.right = x.left;
        x.left = y;
        updateHeight(y);          // 先更新被压下去的 y
        updateHeight(x);
        return x;
    }

    private Node rotateRight(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        updateHeight(y);
        updateHeight(x);
        return x;
    }

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

    /** 全树验证 AVL 不变量：|bf|≤1 且 height 字段与实际一致。 */
    public void checkAVL() { checkAVL(root); }
    private int checkAVL(Node x) {
        if (x == null) return 0;
        int lh = checkAVL(x.left), rh = checkAVL(x.right);
        if (Math.abs(lh - rh) > 1) throw new AssertionError("失衡节点 " + x.key);
        if (x.height != 1 + Math.max(lh, rh)) throw new AssertionError("height 字段过期 " + x.key);
        return 1 + Math.max(lh, rh);
    }

    /** 演示用：按插入顺序构造后返回高度，供 Main 验证 1.44·log2(n+2) 上界。 */
    public static <T extends Comparable<T>> AVLTree<T> of(Iterable<T> keys) {
        AVLTree<T> t = new AVLTree<>();
        for (T k : keys) t.insert(k);
        return t;
    }
}
