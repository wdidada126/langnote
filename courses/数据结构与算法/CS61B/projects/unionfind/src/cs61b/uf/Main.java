package cs61b.uf;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/** 自测入口：对应 L31（并查集三级演进 + 复杂度实测）。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        correctnessAllSame();
        chainAttack();
        randomBenchmark();
        System.out.println("\n[unionfind] all self-tests passed.");
    }

    /** 同一随机操作序列喂给三个实现，connected 查询答案必须逐一相同（diff testing，L13）。 */
    static void correctnessAllSame() {
        int n = 200;
        Random rnd = new Random(5);
        UF[] impls = {new QuickFindUF(n), new QuickUnionUF(n), new WeightedQuickUnionCompUF(n)};
        List<int[]> queries = new ArrayList<>();
        for (int step = 0; step < 2000; step++) {
            int a = rnd.nextInt(n), b = rnd.nextInt(n);
            for (UF u : impls) u.union(a, b);
            if (step % 10 == 0) queries.add(new int[]{a, b});
        }
        for (int[] q : queries) {
            boolean expect = impls[0].connected(q[0], q[1]);
            for (UF u : impls)
                if (u.connected(q[0], q[1]) != expect) throw new AssertionError("FAIL: 实现间答案不一致");
        }
        check(impls[2].count() == impls[0].count(), "最终分量数一致 = " + impls[0].count());
    }

    /** 链攻击：union(i+1, i) 序列让无加权版把森林拉成一条链；加权+压缩则天然免疫。 */
    static void chainAttack() {
        int n = 10_000;
        QuickUnionUF plain = new QuickUnionUF(n);
        WeightedQuickUnionCompUF wqc = new WeightedQuickUnionCompUF(n);
        for (int i = 0; i + 1 < n; i++) { plain.union(i + 1, i); wqc.union(i + 1, i); }
        plain.ops = 0; wqc.ops = 0;
        plain.find(0);
        long chainOps = plain.ops;             // 无加权：沿链 0→1→2→…→n-1
        wqc.find(0);
        long firstFind = wqc.ops;
        wqc.ops = 0;
        wqc.find(0);                           // 压缩后：第二次近乎免费
        System.out.printf("   链上 find(0)：无加权 %d 次数组访问；加权+压缩首次 %d、再次 %d%n",
                chainOps, firstFind, wqc.ops);
        check(chainOps > n / 2, "无加权 quick-union 确实退化成链（find 走了半条链以上）");
        check(wqc.ops < 10 && firstFind < n / 2, "加权防住链攻击：首次 find 也不长，压缩后近乎 O(1)");
    }

    /** 万级混合操作：三种实现的数组访问量对比（把 L15 渐近记号变成可数的账）。 */
    static void randomBenchmark() {
        int n = 20_000, m = 60_000;
        Random rnd = new Random(42);
        int[][] pairs = new int[m][2];
        for (int i = 0; i < m; i++) { pairs[i][0] = rnd.nextInt(n); pairs[i][1] = rnd.nextInt(n); }

        QuickFindUF qf = new QuickFindUF(n);
        QuickUnionUF qu = new QuickUnionUF(n);
        WeightedQuickUnionCompUF wqc = new WeightedQuickUnionCompUF(n);
        long t0 = System.nanoTime();
        for (int[] p : pairs) qf.union(p[0], p[1]);
        long tQF = System.nanoTime() - t0;
        t0 = System.nanoTime();
        for (int[] p : pairs) wqc.union(p[0], p[1]);
        long tW = System.nanoTime() - t0;
        for (int[] p : pairs) qu.union(p[0], p[1]);

        System.out.printf("   %d union @n=%d: quick-find %d 访问(%dms) | quick-union %d | 加权+压缩 %d(%dms)%n",
                m, n, qf.ops, tQF / 1_000_000, qu.ops, wqc.ops, tW / 1_000_000);
        check(qf.ops > 10L * wqc.ops, "quick-find 的账高出最终形态一个量级以上（Θ(n)/union vs ~Θ(1)）");
        check(wqc.count() == qu.count() && wqc.count() == qf.count(), "三方分量数一致");
        check(tW <= tQF, "墙钟时间同向印证（数值随机器波动）");
    }
}
