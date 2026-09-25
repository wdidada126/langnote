package cs61b.bst;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/** 自测入口：对应 L25（BST）与 L26–L27（AVL）。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        bstBasics();
        bstDeleteCases();
        bstDegenerates();
        avlSortedInput();
        avlRandom();
        avlFourCases();
        System.out.println("\n[bst/avl] all self-tests passed.");
    }

    static void bstBasics() {
        BSTMap<String, Integer> t = new BSTMap<>();
        String[] words = {"dog", "cat", "ant", "bee", "fox", "cod"};
        for (int i = 0; i < words.length; i++) t.put(words[i], i);
        check(t.get("cat") == 1 && t.get("zzz") == null, "get 命中/未命中");
        check(t.size() == 6, "size");
        List<String> sorted = new ArrayList<>(List.of(words));
        Collections.sort(sorted);
        check(t.keysInOrder().equals(sorted), "中序即升序：" + t.keysInOrder());
        check(t.min().equals("ant"), "min 沿左下降");
        t.checkBST();
    }

    static void bstDeleteCases() {
        BSTMap<Integer, String> t = new BSTMap<>();
        for (int k : new int[]{50, 30, 70, 20, 40, 60, 80, 35, 38}) t.put(k, "v" + k);
        check(t.remove(30).equals("v30") && t.get(35) != null, "删除双子节点（中序后继 35 顶替）");
        check(t.remove(20).equals("v20"), "删除叶子");
        t.checkBST();
        check(t.remove(999) == null && t.size() == 7, "删除不存在的键：返回 null 且 size 不变");
        check(t.get(50).equals("v50"), "根不受影响");
    }

    static void bstDegenerates() {
        BSTMap<Integer, String> t = new BSTMap<>();
        int n = 2000;
        for (int i = 1; i <= n; i++) t.put(i, "x");     // 有序输入
        System.out.println("   有序插入 BST 高 = " + t.height() + "（理想 log2(2000)≈11）——完全退化成链表（L25）");
        check(t.height() == n, "高度 = n：最坏 Θ(n) 实锤");
    }

    static void avlSortedInput() {
        AVLTree<Integer> a = new AVLTree<>();
        int n = 2000;
        for (int i = 1; i <= n; i++) a.insert(i);
        a.checkAVL();
        int bound = (int) Math.ceil(1.44 * (Math.log(n + 2) / Math.log(2)));
        System.out.println("   有序插入 AVL 高 = " + a.height() + " ≤ 理论上界 " + bound);
        check(a.height() <= bound, "AVL 高度上界 1.44·log2(n+2)");
        check(a.keysInOrder().size() == n && a.contains(1500), "AVL 查找/遍历正确");
    }

    static void avlRandom() {
        Random rnd = new Random(42);
        List<Integer> keys = new ArrayList<>();
        for (int i = 0; i < 5000; i++) keys.add(rnd.nextInt(100_000));
        AVLTree<Integer> a = AVLTree.of(keys);
        a.checkAVL();
        List<Integer> expect = new ArrayList<>(new java.util.HashSet<>(keys));
        Collections.sort(expect);
        check(a.keysInOrder().equals(expect), "5000 随机键（含重复）中序 == 去重排序");
        for (int k : expect) if (!a.contains(k)) throw new AssertionError("FAIL: 缺键 " + k);
        System.out.println("   插入 " + keys.size() + " 次、净 " + a.size() + " 键，旋转 " + a.rotationCount + " 次");
    }

    static void avlFourCases() {
        // 构造 LL / RR / LR / RL 四种失衡的最小例子（插入后检查高度与根）
        check(AVLTree.of(List.of(3, 2, 1)).height() == 2, "LL 右旋：1,2,3 → 平衡高 2");
        check(AVLTree.of(List.of(1, 2, 3)).height() == 2, "RR 左旋");
        check(AVLTree.of(List.of(3, 1, 2)).height() == 2, "LR 双旋");
        check(AVLTree.of(List.of(1, 3, 2)).height() == 2, "RL 双旋");
        AVLTree<Integer> t = AVLTree.of(List.of(1, 3, 2));
        check(t.keysInOrder().equals(List.of(1, 2, 3)) && t.contains(2), "双旋后序与内容不变");
    }
}
