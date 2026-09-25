package cs61b.heap;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Top-K 流式算法（L28 的核心应用，15-445 ORDER BY…LIMIT K 的原型）：
 * 维护大小为 K 的"最小堆"，任何新元素只需与堆顶（当前第 K 名）比较一次。
 * Θ(n log k) 时间、Θ(k) 空间——对比全排序 Θ(n log n)。
 */
public final class TopK {

    private TopK() {}

    /** 返回前 K 大（降序排列）。 */
    public static <T extends Comparable<T>> List<T> topKMax(List<T> stream, int k) {
        if (k <= 0) return List.of();
        Heap<T> h = new Heap<>();                     // 小顶堆装候选
        for (T x : stream) {
            if (h.size() < k) h.offer(x);
            else if (x.compareTo(h.peek()) > 0) { h.poll(); h.offer(x); }
        }
        List<T> out = new ArrayList<>();
        while (!h.isEmpty()) out.add(0, h.poll());    // 依次弹出得降序
        return out;
    }

    public static <T> List<T> topK(List<T> stream, int k, Comparator<T> better) {
        if (k <= 0) return List.of();
        Heap<T> h = new Heap<>(better);               // 堆顶即 better 序最小 = "最差候选"（第 K 名）
        for (T x : stream) {
            if (h.size() < k) h.offer(x);
            else if (better.compare(x, h.peek()) > 0) { h.poll(); h.offer(x); }
        }
        List<T> out = new ArrayList<>();
        while (!h.isEmpty()) out.add(0, h.poll());
        return out;
    }
}
