package cs61b.sorts;

import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

/** 自测入口：对应 L34–L35（排序家族、稳定性、基数排序）。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        correctnessSweep();
        stability();
        insertionAdaptive();
        radixBigScale();
        System.out.println("\n[sorts] all self-tests passed.");
    }

    static int[][] cases() {
        Random rnd = new Random(9);
        int[] random = rnd.ints(500, -100_000, 100_000).toArray();
        int[] sorted = random.clone();
        Arrays.sort(sorted);
        int[] reversed = sorted.clone();
        for (int i = 0; i < reversed.length / 2; i++) {
            int t = reversed[i]; reversed[i] = reversed[reversed.length - 1 - i];
            reversed[reversed.length - 1 - i] = t;
        }
        int[] allSame = new int[200];
        Arrays.fill(allSame, 7);
        return new int[][]{
                {}, {42}, {2, 1}, sorted, reversed, allSame, random,
                rnd.ints(999, 0, 3).toArray()                     // 少键值：基数/计数的主场
        };
    }

    static void correctnessSweep() {
        var algos = java.util.List.<java.function.Consumer<int[]>>of(
                Sorts::insertion, Sorts::merge, Sorts::quick, Sorts::heap);
        for (int[] tc : cases()) {
            int[] ref = tc.clone();
            Arrays.sort(ref);
            for (var algo : algos) {
                int[] x = tc.clone();
                algo.accept(x);
                if (!Arrays.equals(x, ref))
                    throw new AssertionError("FAIL: 算法结果与 Arrays.sort 不一致 on case len=" + tc.length);
            }
        }
        System.out.println("ok - 插入/归并/快排/堆排 × 8 组边界用例 与 Arrays.sort 全对");
        // 基数排序仅非负键
        for (int[] tc : cases()) {
            if (Arrays.stream(tc).anyMatch(v -> v < 0)) continue;
            int[] x = tc.clone();
            Sorts.radixLSD(x);
            int[] ref = tc.clone();
            Arrays.sort(ref);
            if (!Arrays.equals(x, ref)) throw new AssertionError("FAIL: radix 错在 " + Arrays.toString(tc));
        }
        System.out.println("ok - 基数排序（非负键）× 全部用例通过");
    }

    /** 稳定性：同键必须保持原相对序。归并 ✔（cmp<=0 取左侧）；快排/堆排不承诺。 */
    static void stability() {
        record Row(int key, int id) {}
        Random rnd = new Random(4);
        Row[] rows = new Row[300];
        for (int i = 0; i < rows.length; i++) rows[i] = new Row(rnd.nextInt(5), i);
        Sorts.mergeSort(rows, Comparator.comparingInt(Row::key));
        for (int i = 1; i < rows.length; i++)
            if (rows[i].key() == rows[i - 1].key() && rows[i].id() < rows[i - 1].id())
                throw new AssertionError("FAIL: 归并不稳定");
        System.out.println("ok - mergeSort 稳定：等键区间内 id 仍升序（多关键字排序的基础，L35）");
    }

    /** 插入排序的自适应：近乎有序时 Θ(n)——对照组是乱序。 */
    static void insertionAdaptive() {
        int n = 200_000;
        int[] sorted = new int[n];
        for (int i = 0; i < n; i++) sorted[i] = i;
        int[] nearly = sorted.clone();
        for (int i = 0; i < 100; i++) {           // 制造 100 个"微扰"
            int a = new Random(i).nextInt(n), b = new Random(i + 1).nextInt(n);
            int t = nearly[a]; nearly[a] = nearly[b]; nearly[b] = t;
        }
        long t0 = System.nanoTime();
        Sorts.insertion(nearly);
        long t1 = System.nanoTime();
        System.out.printf("   插入排序 2e5 近有序（100 次交换扰动）用时 %.1f ms——Θ(n+逆序数) 的威力%n",
                (t1 - t0) / 1e6);
        check(Arrays.equals(nearly, sorted), "微扰数组修复后完全有序");
    }

    static void radixBigScale() {
        Random rnd = new Random(11);
        int[] big = rnd.ints(2_000_000, 0, Integer.MAX_VALUE).toArray();
        long t0 = System.nanoTime();
        Sorts.radixLSD(big);
        long t1 = System.nanoTime();
        boolean sortedOk = true;
        for (int i = 1; i < big.length; i++) if (big[i - 1] > big[i]) { sortedOk = false; break; }
        System.out.printf("   基数排序 2e6 非负随机数用时 %.0f ms（Θ(4n)，无比较、无递归）%n", (t1 - t0) / 1e6);
        check(sortedOk, "基数排序结果有序");
    }
}
