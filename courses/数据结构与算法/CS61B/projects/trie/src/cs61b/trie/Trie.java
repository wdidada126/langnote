package cs61b.trie;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/**
 * Trie / 前缀树（L36）：把"每个前缀"变成树上的一个节点。
 * 查找成本只依赖键长 m（逐字符选边），与键数 n 无关——这是对哈希表 Θ(m) 计算 hashCode
 * 的"分摊"：哈希把 m 次字符读压缩成一次乘法链，Trie 则把 m 层指针跳转作为索引本身。
 * 子表用 HashMap（工程折中：小字符集用定长数组更快，见笔记 CSAPP 节）。
 */
public class Trie {

    private class Node {
        final java.util.Map<Character, Node> next = new java.util.HashMap<>();
        boolean end;
        int freq; // 词频：自动补全排序用（L28 堆的复用）
    }

    private final Node root = new Node();
    private int distinctWords;

    public boolean isEmpty() { return distinctWords == 0; }
    public int size() { return distinctWords; }

    public void insert(String word) { insert(word, 1); }

    public void insert(String word, int deltaFreq) {
        if (word.isEmpty()) throw new IllegalArgumentException("empty word");
        Node p = root;
        for (int i = 0; i < word.length(); i++)
            p = p.next.computeIfAbsent(word.charAt(i), c -> new Node());
        if (!p.end) { p.end = true; distinctWords++; }
        p.freq += deltaFreq;
    }

    public boolean contains(String word) {
        Node p = descend(word);
        return p != null && p.end;
    }

    public boolean startsWith(String prefix) { return descend(prefix) != null; }

    private Node descend(String s) {
        Node p = root;
        for (int i = 0; i < s.length(); i++) {
            p = p.next.get(s.charAt(i));
            if (p == null) return null;
        }
        return p;
    }

    /** 删除：先清 end 标志，再自底向上剪掉"非词尾且无子"的节点（Θ(m)）。 */
    public boolean delete(String word) {
        if (!contains(word)) return false;     // 词不存在 ⇒ false（与"父节点可否被剪"是两个信号）
        delete(root, word, 0);
        return true;
    }
    private boolean delete(Node p, String word, int depth) {
        if (depth == word.length()) {
            if (!p.end) return false;
            p.end = false;
            distinctWords--;
            return p.next.isEmpty();       // true ⇒ 父节点可把我剪掉
        }
        char c = word.charAt(depth);
        Node child = p.next.get(c);
        if (child == null) return false;
        boolean pruneChild = delete(child, word, depth + 1);
        if (pruneChild) {
            p.next.remove(c);
            return !p.end && p.next.isEmpty();
        }
        return false;
    }

    /** 前缀下的所有词，字典序：Θ(前缀长 + 输出规模)——子节点排序后 DFS。 */
    public List<String> keysWithPrefix(String prefix) {
        List<String> out = new ArrayList<>();
        Node p = descend(prefix);
        if (p != null) collect(p, new StringBuilder(prefix), out);
        return out;
    }

    private void collect(Node p, StringBuilder path, List<String> out) {
        if (p.end) out.add(path.toString());
        List<Character> chars = new ArrayList<>(p.next.keySet());
        chars.sort(Comparator.naturalOrder());          // 保证字典序输出
        for (char c : chars) {
            path.append(c);
            collect(p.next.get(c), path, out);
            path.deleteCharAt(path.length() - 1);       // 回溯（撤销选择）
        }
    }

    /** 自动补全：前缀下按词频取 Top-k（小顶堆维护 k 个最优，L28 组合技）。 */
    public List<String> autocomplete(String prefix, int k) {
        record Weighted(String word, int freq) {}
        PriorityQueue<Weighted> minHeap = new PriorityQueue<>(Comparator.comparingInt(Weighted::freq));
        Node p = descend(prefix);
        if (p == null) return List.of();
        List<String> all = keysWithPrefix(prefix);
        for (String w : all) {
            minHeap.offer(new Weighted(w, freqOf(w)));
            if (minHeap.size() > k) minHeap.poll();
        }
        List<String> out = new ArrayList<>();
        while (!minHeap.isEmpty()) out.add(0, minHeap.poll().word());
        return out;
    }

    private int freqOf(String word) {
        Node p = descend(word);
        return p == null ? 0 : p.freq;
    }

    /** 统计节点总数（空间诊断：证明"最坏 Θ(总字符数)"）。 */
    public int nodeCount() { return nodeCount(root); }
    private int nodeCount(Node p) {
        int n = 0;
        for (Node c : p.next.values()) n += 1 + nodeCount(c);
        return n;
    }
}
