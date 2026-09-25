package cs61b.heap;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/** 自测入口：对应 L28（堆与优先队列）。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        basics();
        heapifyLinear();
        heapsort();
        topK();
        amaxHeap();
        System.out.println("\n[heap] all self-tests passed.");
    }

    static void basics() {
        Random rnd = new Random(7);
        Heap<Integer> h = new Heap<>();
        List<Integer> in = new ArrayList<>();
        for (int i = 0; i < 500; i++) { int x = rnd.nextInt(1000); in.add(x); h.offer(x); }
        h.checkHeap();
        List<Integer> out = new ArrayList<>();
        while (!h.isEmpty()) out.add(h.poll());
        List<Integer> sorted = new ArrayList<>(in);
        Collections.sort(sorted);
        check(out.equals(sorted), "offer×500 + poll 全部 = 升序排序（堆即优先队列）");
    }

    static void heapifyLinear() {
        Random rnd = new Random(1);
        List<Integer> in = new ArrayList<>();
        for (int i = 0; i < 1000; i++) in.add(rnd.nextInt(10000));
        long t0 = System.nanoTime();
        Heap<Integer> h = Heap.build(in, Comparator.naturalOrder());
        long t1 = System.nanoTime();
        h.checkHeap();
        check(h.size() == 1000 && h.peek().equals(Collections.min(in)), "O(n) build 后堆不变量成立且 peek=全局最小");
        System.out.printf("   build(1000) 用时 %.2f ms（Θ(n) 论证见 CLRS 6.3：Σ h/2^h = Θ(n)）%n", (t1 - t0) / 1e6);
    }

    static void heapsort() {
        Random rnd = new Random(2);
        int[] a = rnd.ints(3000, -100_000, 100_000).toArray();
        Heap<Integer> h = Heap.build(boxed(a), Comparator.natural());
        int[] out = new int[a.length];
        for (int i = 0; i < out.length; i++) out[i] = h.poll();
        int[] ref = a.clone();
        Arrays.sort(ref);
        check(Arrays.equals(out, ref), "堆排序 = build + n 次 poll，Θ(n log n) 最坏");
    }

    static List<Integer> boxed(int[] a) {
        List<Integer> l = new ArrayList<>(a.length);
        for (int x : a) l.add(x);
        return l;
    }

    static void topK() {
        Random rnd = new Random(3);
        List<Integer> stream = new ArrayList<>();
        for (int i = 0; i < 100_000; i++) stream.add(rnd.nextInt(1_000_000));
        List<Integer> top = TopK.topKMax(stream, 10);
        List<Integer> ref = new ArrayList<>(stream);
        Collections.sort(ref);
        Collections.reverse(ref);
        check(top.equals(ref.subList(0, 10)), "Top-10（Θ(n log k) 空间 Θ(k)）与全排序前 10 一致");
        record Player(String name, int score) {}
        var players = List.of(
                new Player("a", 10), new Player("b", 30), new Player("c", 20), new Player("d", 40));
        var best2 = TopK.topK(players, 2, Comparator.comparingInt(Player::score));
        check(best2.get(0).name().equals("d") && best2.get(1).name().equals("b"), "自定义比较器的 Top-K（游戏排行榜场景）");
    }

    static void amaxHeap() {
        // 最大堆 = 小顶堆 + reverseOrder（L28 里"谁当堆顶"是约定问题）
        Heap<Integer> max = new Heap<>(Collections.reverseOrder());
        for (int x : new int[]{5, 9, 1, 7}) max.offer(x);
        check(max.peek() == 9 && max.poll() == 9, "reverseOrder ⇒ 堆顶变最大");
        max.checkHeap();
    }
}
