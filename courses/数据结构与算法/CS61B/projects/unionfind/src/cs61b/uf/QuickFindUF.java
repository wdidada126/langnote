package cs61b.uf;

/**
 * quick-find：find Θ(1)（直接读 id[p]），union Θ(n)（全表改标签）。
 * 大量 union 少量 find 的场景会被打爆——Main 里用 ops 计数证明（L31）。
 */
public class QuickFindUF implements UF {

    private final int[] id;
    private int count;
    public long ops; // 数组访问计数：把 L15 的"操作记账"变成实测

    public QuickFindUF(int n) {
        id = new int[n];
        count = n;
        for (int i = 0; i < n; i++) id[i] = i;
    }

    @Override
    public int find(int p) { ops++; return id[p]; }

    @Override
    public boolean union(int a, int b) {
        int ta = find(a), tb = find(b);
        if (ta == tb) return false;
        for (int i = 0; i < id.length; i++) {
            ops++;
            if (id[i] == ta) id[i] = tb;
        }
        count--;
        return true;
    }

    @Override
    public boolean connected(int a, int b) { return find(a) == find(b); }
    @Override
    public int count() { return count; }
}
