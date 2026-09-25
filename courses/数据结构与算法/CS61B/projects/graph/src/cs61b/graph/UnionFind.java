package cs61b.graph;

/** 加权 quick-union + 路径压缩（L31；graph 的 Kruskal 需要，与 projects/unionfind 同源）。 */
public class UnionFind {

    private final int[] parent;
    private final int[] compSize;
    private int count;

    public UnionFind(int n) {
        parent = new int[n];
        compSize = new int[n];
        count = n;
        for (int i = 0; i < n; i++) { parent[i] = i; compSize[i] = 1; }
    }

    /** 迭代式 find + 路径压缩（每步指向祖父）。 */
    public int find(int p) {
        validate(p);
        while (p != parent[p]) {
            parent[p] = parent[parent[p]];
            p = parent[p];
        }
        return p;
    }

    public boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (compSize[ra] < compSize[rb]) { int t = ra; ra = rb; rb = t; } // 按大小加权
        parent[rb] = ra;
        compSize[ra] += compSize[rb];
        count--;
        return true;
    }

    public boolean connected(int a, int b) { return find(a) == find(b); }
    public int count() { return count; }

    private void validate(int p) {
        if (p < 0 || p >= parent.length) throw new IndexOutOfBoundsException("p=" + p);
    }
}
