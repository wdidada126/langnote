package cs61b.uf;

/**
 * 最终形态：按大小加权 + 路径压缩（迭代两遍法：第一遍找根，第二遍改道）（L31 / Lab）。
 * 加权保证树高 O(log n)；压缩让后续 find 近似 O(1)；
 * 两者合力的 m 次操作摊还 Θ(m·α(m,n))（Tarjan & van Leeuwen 1984，见 papers.md C7）。
 */
public class WeightedQuickUnionCompUF implements UF {

    private final int[] parent;
    private final int[] compSize;
    private int count;
    public long ops;

    public WeightedQuickUnionCompUF(int n) {
        parent = new int[n];
        compSize = new int[n];
        count = n;
        for (int i = 0; i < n; i++) { parent[i] = i; compSize[i] = 1; }
    }

    @Override
    public int find(int p) {
        int root = p;
        while (root != parent[root]) { ops++; root = parent[root]; }
        while (p != root) {                     // 第二遍：沿途全部直挂根（路径压缩）
            ops++;
            int next = parent[p];
            parent[p] = root;
            p = next;
        }
        ops++;
        return root;
    }

    @Override
    public boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (compSize[ra] < compSize[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        compSize[ra] += compSize[rb];
        count--;
        return true;
    }

    @Override
    public boolean connected(int a, int b) { return find(a) == find(b); }
    @Override
    public int count() { return count; }
}
