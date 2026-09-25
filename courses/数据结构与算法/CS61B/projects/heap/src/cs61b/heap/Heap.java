package cs61b.heap;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * 二叉堆（L28）：完全二叉树塞进数组——parent(i)=(i-1)/2，child(i)=2i+1/2i+2。
 * 约定：堆顶是 Comparator 意义下的"最小"（JDK PriorityQueue 同约定），
 *       要最大堆就传 Collections.reverseOrder()。
 * 不变量：任意父 ≤ 其子（兄弟间无序——这正是它能用数组、findMin Θ(1) 的原因）。
 */
public class Heap<T> {

    private final ArrayList<T> data = new ArrayList<>();
    private final Comparator<T> cmp;

    public Heap(Comparator<T> cmp) { this.cmp = cmp; }

    @SuppressWarnings({"unchecked", "rawtypes"})
    public Heap() { this((Comparator) Comparator.naturalOrder()); } // raw 传入：T 未限定 Comparable，强转交给调用方约定

    public int size() { return data.size(); }
    public boolean isEmpty() { return data.isEmpty(); }

    public T peek() {
        if (isEmpty()) throw new NoSuchElementException("empty heap");
        return data.get(0);
    }

    public T offer(T x) {
        data.add(x);
        siftUp(data.size() - 1);
        return x;
    }

    public T poll() {
        T top = peek();
        int last = data.size() - 1;
        data.set(0, data.get(last));
        data.remove(last);
        if (!isEmpty()) siftDown(0);
        return top;
    }

    /** O(n) 线性建堆（heapify）：自底向上对每个内部节点 siftDown（L28/CLRS 6.3）。 */
    public static <T> Heap<T> build(List<T> items, Comparator<T> cmp) {
        Heap<T> h = new Heap<>(cmp);
        h.data.addAll(items);
        for (int i = h.data.size() / 2 - 1; i >= 0; i--) h.siftDown(i);
        return h;
    }

    private void siftUp(int i) {
        T x = data.get(i);
        while (i > 0) {
            int p = (i - 1) / 2;
            if (cmp.compare(x, data.get(p)) >= 0) break;
            data.set(i, data.get(p));
            i = p;
        }
        data.set(i, x);
    }

    private void siftDown(int i) {
        T x = data.get(i);
        int n = data.size();
        while (true) {
            int l = 2 * i + 1;
            if (l >= n) break;
            int best = l;
            int r = l + 1;
            if (r < n && cmp.compare(data.get(r), data.get(l)) < 0) best = r; // 与"较小"孩子换
            if (cmp.compare(data.get(best), x) >= 0) break;
            data.set(i, data.get(best));
            i = best;
        }
        data.set(i, x);
    }

    /** 调试/教学：验证堆不变量（每个父 ≤ 子）。 */
    public void checkHeap() {
        for (int i = 1; i < data.size(); i++)
            if (cmp.compare(data.get(i), data.get((i - 1) / 2)) < 0)
                throw new AssertionError("堆不变量被破坏 at " + i);
    }

    public List<T> snapshot() { return new ArrayList<>(data); }
}
