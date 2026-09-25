package cs61b.uf;

/**
 * quick-union（无加权、无压缩）：find 沿 parent 上溯到根，union 只接两根 Θ(1)。
 * 弱点：随机合并期望树高 Θ(log n)，但最坏可退化成链（union(0,1),(1,2),(2,3)…），find Θ(n)。
 * Main 的"链攻击"演示正是 L31 笔记说的"quick-union 的阿喀琉斯之踵"。
 */
public class QuickUnionUF implements UF {

    private final int[] parent;
    private int count;
    public long ops;

    public QuickUnionUF(int n) {
        parent = new int[n];
        count = n;
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    @Override
    public int find(int p) {
        while (p != parent[p]) { ops += 2; p = parent[p]; }
        ops++;
        return p;
    }

    @Override
    public boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        parent[rb] = ra;
        count--;
        return true;
    }

    @Override
    public boolean connected(int a, int b) { return find(a) == find(b); }
    @Override
    public int count() { return count; }
}
