package cs61b.sorts;

import java.util.Comparator;

/**
 * 排序家族（L34–L35）：insertion（基准/小数组终结者）、merge（稳定最坏 nlogn）、
 * quick（三数取中 + 小数组切插入 + 尾递归先推小半区）、heap（原地最坏 nlogn）、
 * radix LSD（跳出比较模型：Θ(d(n+R))）。
 */
public final class Sorts {

    private Sorts() {}

    /* ---------- 插入排序：Θ(n²)，但近乎有序时 Θ(n + 逆序数) ---------- */

    public static void insertion(int[] a) { insertion(a, 0, a.length); }

    static void insertion(int[] a, int lo, int hi) { // 半开区间 [lo, hi)
        for (int i = lo + 1; i < hi; i++) {
            int v = a[i], j = i - 1;
            while (j >= lo && a[j] > v) { a[j + 1] = a[j]; j--; }
            a[j + 1] = v;
        }
    }

    /* ---------- 归并排序：稳定，Θ(n log n) 最坏，Θ(n) 辅助空间 ---------- */

    /** 通用版（供稳定性实验）：cmp(aux[i], aux[j]) <= 0 时优先取左半 ⇒ 相等键保序。 */
    @SuppressWarnings("unchecked")
    public static <T> void mergeSort(T[] a, Comparator<? super T> cmp) {
        T[] aux = (T[]) a.clone();
        mergeSort(a, aux, cmp, 0, a.length);
    }

    private static <T> void mergeSort(T[] a, T[] aux, Comparator<? super T> cmp, int lo, int hi) {
        if (hi - lo <= 1) return;
        int mid = (lo + hi) >>> 1;
        mergeSort(aux, a, cmp, lo, mid);      // 交替角色省一次复制
        mergeSort(aux, a, cmp, mid, hi);
        int i = lo, j = mid;
        for (int k = lo; k < hi; k++)
            if (i < mid && (j >= hi || cmp.compare(aux[i], aux[j]) <= 0)) a[k] = aux[i++];
            else a[k] = aux[j++];
    }

    public static void merge(int[] a) {
        int[] aux = a.clone();
        merge(aux, a, 0, a.length);
    }

    /** 自底向上归并（int 版，避免泛型数组问题）：aux/a 角色每层交换。 */
    private static void merge(int[] src, int[] dst, int lo, int hi) {
        if (hi - lo <= 1) { System.arraycopy(src, lo, dst, lo, hi - lo); return; }
        int mid = (lo + hi) >>> 1;
        merge(dst, src, lo, mid);             // 注意：递归里 src/dst 已互换
        merge(dst, src, mid, hi);
        int i = lo, j = mid;
        for (int k = lo; k < hi; k++)
            if (i < mid && (j >= hi || src[i] <= src[j])) dst[k] = src[i++];
            else dst[k] = src[j++];
    }

    /* ---------- 快速排序：期望 Θ(n log n)；工程三件套见注释 ---------- */

    public static void quick(int[] a) { quick(a, 0, a.length); }

    private static void quick(int[] a, int lo, int hi) {
        while (hi - lo > 8) {                       // 小数组切插入排序（阈值 ~8–16）
            int p = partitionMedian3(a, lo, hi);
            if (p - lo < hi - p - 1) {              // 先递归小半区，循环推大半区：
                quick(a, lo, p);                    // 栈深保证 O(log n)（尾递归优化）
                lo = p + 1;
            } else {
                quick(a, p + 1, hi);
                hi = p;
            }
        }
        insertion(a, lo, hi);
    }

    private static int partitionMedian3(int[] a, int lo, int hi) {
        int mid = (lo + hi) >>> 1, last = hi - 1;   // 三数取中选 pivot，防有序输入退化
        if (a[mid] < a[lo]) swap(a, lo, mid);
        if (a[last] < a[mid]) { swap(a, mid, last); if (a[mid] < a[lo]) swap(a, lo, mid); }
        swap(a, mid, last);                         // pivot 放最后
        int pivot = a[last], i = lo;
        for (int j = lo; j < last; j++)
            if (a[j] < pivot) swap(a, i++, j);      // Lomuto：a[lo..i) < pivot
        swap(a, i, last);
        return i;                                   // pivot 归位
    }

    /* ---------- 堆排序：原地、最坏 Θ(n log n)，但不稳定、缓存差 ---------- */

    public static void heap(int[] a) {
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--) sink(a, i, n);   // O(n) 建堆（L28 heapify）
        for (int end = n - 1; end > 0; end--) {
            swap(a, 0, end);                        // 最大值移到已排区
            sink(a, 0, end);
        }
    }

    private static void sink(int[] a, int i, int size) {     // 大顶堆
        int v = a[i];
        while (true) {
            int l = 2 * i + 1;
            if (l >= size) break;
            int best = l;
            if (l + 1 < size && a[l + 1] > a[l]) best = l + 1;
            if (a[best] <= v) break;
            a[i] = a[best];
            i = best;
        }
        a[i] = v;
    }

    /* ---------- 基数排序 LSD：非负 int，4 轮 × 256 桶，稳定计数排序做轮内核 ---------- */

    public static void radixLSD(int[] a) {          // 仅演示非负键（负数先翻符号位，留作练习）
        int n = a.length;
        if (n <= 1) return;
        int[] aux = new int[n];
        for (int d = 0; d < 4; d++) {
            int shift = 8 * d;
            int[] cnt = new int[257];
            for (int x : a) cnt[((x >>> shift) & 0xFF) + 1]++;
            for (int i = 1; i < 257; i++) cnt[i] += cnt[i - 1];
            for (int x : a) aux[cnt[((x >>> shift) & 0xFF)]++] = x;
            System.arraycopy(aux, 0, a, 0, n);
        }
    }
}
