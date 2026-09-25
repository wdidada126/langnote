package cs61b.graph;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 自测入口：对应 L29–L32。
 * 测试图（V=9，含孤立分量 {7,8}）：
 *  0-1:4  0-2:2  1-2:1  1-3:5  2-3:8  2-4:10  3-4:2  3-5:6  4-5:3  5-6:2  3-6:7  7-8:1
 * 手工算得：MST 权 18+1=19；Dijkstra(0)=[0,3,2,8,10,13,15,∞,∞]；BFS 跳数=[0,1,1,2,3,3,3,-1,-1]。
 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    static Graph build() {
        Graph g = new Graph(9);
        g.addEdge(0, 1, 4); g.addEdge(0, 2, 2); g.addEdge(1, 2, 1);
        g.addEdge(1, 3, 5); g.addEdge(2, 3, 8); g.addEdge(2, 4, 10);
        g.addEdge(3, 4, 2); g.addEdge(3, 5, 6); g.addEdge(4, 5, 3);
        g.addEdge(5, 6, 2); g.addEdge(3, 6, 7); g.addEdge(7, 8, 1);
        return g;
    }

    public static void main(String[] args) {
        Graph g = build();
        check(g.V() == 9 && g.directedEdgeCount() == 24, "V/E 统计（无向边存两条有向记录）");

        // BFS（L30）
        int[] hops = GraphAlgorithms.bfsHops(g, 0);
        check(Arrays.equals(hops, new int[]{0, 1, 1, 2, 3, 3, 3, -1, -1}), "BFS 跳数含不可达 -1");

        // DFS 与连通分量（L30）
        List<Integer> order = new ArrayList<>();
        check(GraphAlgorithms.connectedComponents(g) == 2, "连通分量数 = 2（{0..6} 与 {7,8}）");
        GraphAlgorithms.dfsOrder(g, 0, order, new boolean[g.V()]);
        check(order.size() == 7 && order.get(0) == 0, "DFS 访问顺序覆盖整分量");

        // Dijkstra（L32）
        int[] edgeTo = new int[g.V()];
        double[] dist = GraphAlgorithms.dijkstra(g, 0, edgeTo);
        System.out.println("   dist = " + Arrays.toString(dist));
        check(Math.abs(dist[1] - 3) < 1e-9 && Math.abs(dist[5] - 13) < 1e-9
                && Math.abs(dist[6] - 15) < 1e-9, "Dijkstra 关键距离（0→5 走 0-2-1-3-4-5=13）");
        check(Double.isInfinite(dist[7]), "不可达顶点保持 ∞");
        check(edgeTo[2] == 0 && edgeTo[6] != -1, "edgeTo 最短路树有记录");

        // MST 双算法对照（L31）：不同算法、同一权重（本图边权无并列 ⇒ 唯一 MST）
        var k = GraphAlgorithms.kruskal(g);
        var p = GraphAlgorithms.prim(g);
        double kw = GraphAlgorithms.totalWeight(k), pw = GraphAlgorithms.totalWeight(p);
        System.out.printf("   kruskal %d 条边 权 %.1f；prim %d 条边 权 %.1f%n", k.size(), kw, p.size(), pw);
        check(Math.abs(kw - 19) < 1e-9, "Kruskal MST 总权 = 19（含孤立分量边 7-8）");
        check(Math.abs(pw - 19) < 1e-9 && k.size() == p.size(), "Prim 与 Kruskal 一致（MST 唯一性侧面验证）");

        // 并查集在 Kruskal 中的角色回放（L31）
        UnionFind uf = new UnionFind(4);
        uf.union(0, 1); uf.union(2, 3);
        check(!uf.connected(0, 2), "两棵树未连通");
        uf.union(1, 2);
        check(uf.count() == 1, "合并后单分量");

        System.out.println("\n[graph] all self-tests passed.");
    }
}
